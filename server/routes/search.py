import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from server import crud, schemas
from server.schemas.search import SearchPrompt
from server.utils.auth import get_current_user
from server.utils.config import settings
from server.utils.database import SessionLocal, get_db
from server.utils.opensearch import client, index_name
import re


router = APIRouter(prefix="/search")


def os_get_image_by_id(id):
    response = client.search(index=index_name, body={"query": {"term": {"_id": id}}})
    return response


def os_response_modifier(response, user=None):
    os_response = [{"_id": i["_id"], **i["_source"]} for i in response["hits"]["hits"]]
    for item in os_response:
        item["is_liked"] = False
        item["idx"] = item["_id"]
        del item["_id"]
        content = re.sub(
            r"--.*",
            "",
            item["content"].replace("- Upscaled by", "") if item["content"] else "",
        ).strip()
        item["content"] = content
        for image in item["images"]:
            del image["proxy_url"]
            image["url"] = image["url"].replace(
                "https://cdn.discordapp.com/attachments/",
                "https://api.picsy.art/image/",
            )

    if user:
        ids = [ele["idx"] for ele in os_response]
        db = SessionLocal()
        like_data = crud.image_like.get_my_liked(db, user_id=user.id, ids=ids)
        final_arr = []
        for i in os_response:
            for j in like_data:
                if i["idx"] == j.image_id:
                    i["is_liked"] = True
            final_arr.append(i)
        db.close()
        return final_arr
    return os_response


@router.post("/random")
def search_image(
    user: Optional[schemas.UserBase] = Depends(get_current_user),
):
    try:
        query = {
            "query": {
                "function_score": {
                    "query": {"match": {"has_upscaled": "true"}},
                    "functions": [
                        {"filter": {"range": {"ratio": {"gt": 1}}}, "weight": 100},
                        {"filter": {"range": {"ratio": {"lte": 0}}}, "weight": 1},
                        {"random_score": {}},
                    ],
                    "boost_mode": "multiply",
                }
            },
            "size": settings.PAGINATION_SIZE,
        }

        response = client.search(index=index_name, body=query)
        os_response = os_response_modifier(response, user)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": jsonable_encoder(os_response),
                "message": (
                    "No result found"
                    if len(os_response) == 0
                    else "Data fetched successfully"
                ),
                "error": None,
            },
        )

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": None,
                "message": "Something went wrong",
                "error": str(e),
            },
        )


@router.post("")
def search_image(
    payload: SearchPrompt,
    db: Session = Depends(get_db),
    user: Optional[schemas.UserBase] = Depends(get_current_user),
):
    search_text = payload.query.strip()
    try:
        query = (
            {
                "size": settings.PAGINATION_SIZE,
                "query": {
                    "bool": {
                        "must": [
                            # {"match": {"has_upscaled": "true"}},
                            # {
                            #     "match_phrase_prefix": {
                            #         "content": {
                            #             "query": search_text.split(" "),
                            #         }
                            #     }
                            # },
                            {
                                "multi_match": {
                                    "query": search_text,
                                    "type": "cross_fields",
                                    "fields": ["content"],
                                }
                            },
                        ],
                    },
                },
                "sort": [{"id": "desc"}, {"has_upscaled.keyword": {"order": "asc"}}],
                "search_after": [payload.search_after, 1],
            }
            if payload.search_after
            else {
                "size": settings.PAGINATION_SIZE,
                "query": {
                    "bool": {
                        "must": [
                            # {"match": {"has_upscaled": "true"}},
                            # {
                            #     "match_phrase_prefix": {
                            #         "content": {
                            #             "query": search_text.split(" "),
                            #         }
                            #     }
                            # },
                            {
                                "multi_match": {
                                    "query": search_text,
                                    "type": "cross_fields",
                                    "fields": ["content"],
                                }
                            },
                        ],
                    },
                },
                "sort": [{"id": "desc"}, {"has_upscaled.keyword": {"order": "asc"}}],
            }
        )

        if not payload.search_after:
            crud.search.create(
                db,
                obj_in=schemas.SearchCreate(
                    prompt=search_text,
                    client_country=payload.location,
                    client_ip=payload.ip,
                ),
            )

        response = client.search(index=index_name, body=query)
        os_response = os_response_modifier(response, user)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": jsonable_encoder(os_response),
                "is_last": len(os_response) < settings.PAGINATION_SIZE,
                "message": (
                    "No result found"
                    if len(os_response) == 0
                    else "Data fetched successfully"
                ),
                "error": None,
            },
        )

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": None,
                "message": "Something went wrong",
                "error": str(e),
            },
        )

    finally:
        db.close()


@router.post("/{id}")
def get_by_id(
    id: str,
    db: Session = Depends(get_db),
    user: Optional[schemas.UserBase] = Depends(get_current_user),
):
    try:
        response = os_get_image_by_id(id=id)
        os_response = os_response_modifier(response, user)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": jsonable_encoder(os_response),
                "message": (
                    "No result found"
                    if len(os_response) == 0
                    else "Data fetched successfully"
                ),
                "error": None,
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": None,
                "message": "Something went wrong",
                "error": str(e),
            },
        )
    finally:
        db.close()


@router.delete("/{id}")
def delete_by_id(
    id: str,
    db: Session = Depends(get_db),
):
    try:
        response = client.delete(index=index_name, id=id)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": jsonable_encoder(response),
                "message": (
                    "No result found"
                    if len(response) == 0
                    else "Data Deleted successfully"
                ),
                "error": None,
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": None,
                "message": "Something went wrong",
                "error": str(e),
            },
        )
    finally:
        db.close()


@router.get("/image-of-day/get")
def get_image_of_day(
    date: str,
    db: Session = Depends(get_db),
    user: Optional[schemas.UserBase] = Depends(get_current_user),
):
    try:
        image = crud.image_of_day.get_by_date(db, date=date)
        response = os_get_image_by_id(id=image.image_id)
        os_response = os_response_modifier(response, user)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": jsonable_encoder(os_response),
                "message": (
                    "No result found"
                    if len(os_response) == 0
                    else "Data fetched successfully"
                ),
                "error": None,
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": None,
                "message": "Something went wrong",
                "error": str(e),
            },
        )
    finally:
        db.close()


@router.post("/image-of-day/create")
def create_image_of_day(
    data: schemas.ImageOfDayCreate,
    db: Session = Depends(get_db),
    user: Optional[schemas.UserBase] = Depends(get_current_user),
):
    try:
        response = os_get_image_by_id(id=data.image_id)
        if response.get("hits").get("hits"):
            image = crud.image_of_day.create(
                db,
                obj_in=schemas.ImageOfDayCreate(date=data.date, image_id=data.image_id),
            )
            response = os_get_image_by_id(id=image.id)
            os_response = os_response_modifier(response, user)

            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": jsonable_encoder(os_response),
                    "message": (
                        "No result found"
                        if len(os_response) == 0
                        else "Data added successfully"
                    ),
                    "error": None,
                },
            )
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "data": None,
                    "message": "Image cannot be found",
                },
            )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": None,
                "message": "Something went wrong",
                "error": str(e),
            },
        )
    finally:
        db.close()


@router.put("/image-of-day/update")
def update_image_of_day(
    data: schemas.ImageOfDayCreate,
    db: Session = Depends(get_db),
    user: Optional[schemas.UserBase] = Depends(get_current_user),
):
    try:
        response = os_get_image_by_id(id=data.image_id)
        if response.get("hits").get("hits"):
            image_obj = crud.image_of_day.get_by_id(db, id=data.id)
            image = crud.image_of_day.update(
                db,
                db_obj=image_obj,
                obj_in=schemas.ImageOfDayCreate(date=data.date, image_id=data.image_id),
            )
            response = os_get_image_by_id(id=image.id)
            os_response = os_response_modifier(response, user)

            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": jsonable_encoder(os_response),
                    "message": "Data updated successfully",
                    "error": None,
                },
            )
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "data": None,
                    "message": "Image cannot be found",
                },
            )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": None,
                "message": "Something went wrong",
                "error": str(e),
            },
        )
    finally:
        db.close()


@router.delete("/image-of-day/delete")
def get_image_of_day(
    id: str,
    db: Session = Depends(get_db),
    user: Optional[schemas.UserBase] = Depends(get_current_user),
):
    try:
        image = crud.image_of_day.get_by_id(db, id=id)
        if image:
            crud.image_of_day.remove(db, id=id)
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": [],
                    "message": "Image removed successfully",
                    "error": None,
                },
            )
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "data": None,
                    "message": "Image cannot be found",
                },
            )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": None,
                "message": "Something went wrong",
                "error": str(e),
            },
        )
    finally:
        db.close()
