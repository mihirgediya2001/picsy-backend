import json
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from server import crud, schemas
from server.routes.search import os_get_image_by_id, os_response_modifier
from server.utils.auth import get_current_user
from server.utils.database import get_db
from server.utils.opensearch import client, index_name
from server.utils.config import settings

router = APIRouter(prefix="/like")


@router.post("/add")
def add_like(
    data: schemas.ImageID = Body(...),
    db: Session = Depends(get_db),
    user: schemas.UserBase = Depends(get_current_user),
):
    try:
        if not data.image_id:
            raise HTTPException(status_code=400, detail="Please provide image id")
        image_obj = os_get_image_by_id(id=data.image_id)
        if not image_obj.get("hits").get("hits"):
            raise HTTPException(status_code=400, detail="Image not found")

        existing = crud.image_like.get_owned_by_id(
            db, user_id=user.id, image_id=data.image_id
        )
        if existing:
            return HTTPException(status_code=400, detail="Image already liked")
        else:
            crud.image_like.create(
                db,
                obj_in=schemas.ImageLikeCreate(image_id=data.image_id, user_id=user.id),
            )
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": None,
                    "message": "Image liked",
                    "error": None,
                },
            )
    except HTTPException:
        raise
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


@router.post("/remove")
def remove_like(
    data: schemas.ImageID = Body(...),
    db: Session = Depends(get_db),
    user: schemas.UserBase = Depends(get_current_user),
):
    try:
        existing = crud.image_like.get_owned_by_id(
            db, user_id=user.id, image_id=data.image_id
        )
        if existing:
            crud.image_like.remove(db, id=existing.id)
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": None,
                    "message": "Image like removed",
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


@router.post("/get-my-all")
def get_my_all(
    offset: int = 0,
    db: Session = Depends(get_db),
    user: schemas.UserBase = Depends(get_current_user),
):
    try:
        existing = crud.image_like.get_owned_all(db, user_id=user.id, skip=offset)
        ids = [ele.image_id for ele in existing]
        resp = []
        if existing:
            response = client.search(
                index=index_name,
                body={
                    "query": {"ids": {"values": ids}},
                    "size": settings.PAGINATION_SIZE,
                },
            )

            os_response = os_response_modifier(response)
            
            for obj in existing:
                for obj_ in os_response:
                    if str(obj.image_id) == str(obj_.get("idx")):
                        obj_["is_liked"] = True
                        resp.append(obj_)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": jsonable_encoder(resp),
                "is_last": len(resp) < settings.PAGINATION_SIZE,
                "message": "Image fetched successfully",
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


@router.post("/get-i-liked")
def get_i_liked(
    data: schemas.ImageID = Body(...),
    db: Session = Depends(get_db),
    user: schemas.UserBase = Depends(get_current_user),
):
    existing = crud.image_like.get_owned_by_id(
        db, user_id=user.id, image_id=data.image_id
    )
    db.close()
    if existing:
        return True
    return False
