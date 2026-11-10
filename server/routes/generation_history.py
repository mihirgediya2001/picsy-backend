import json
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sdxl import ImageGenerator
from sqlalchemy.orm import Session

from server import crud, schemas
from server.utils.auth import get_current_user
from server.utils.config import settings
from server.utils.database import get_db
from server.utils import meta_images

client = ImageGenerator()

router = APIRouter(prefix="/image-generation")


@router.post("/generate")
def generate_image(
    data: schemas.GenerateImageInput = Body(...),
    db: Session = Depends(get_db),
    user: schemas.UserBase = Depends(get_current_user),
):
    try:
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Please login to generate the image",
            )

        output = meta_images.generate_image(data.prompt)
        if (
            output.get("data", {})
            .get("xfb_genai_imagine_results_for_prompt", {})
            .get("success")
            == True
        ):
            output_arr = [
                ele.get("imagine_result_success").get("uri")
                for ele in output.get("data", {})
                .get("xfb_genai_imagine_results_for_prompt")
                .get("response", [])
            ]
            result = crud.generation_history.create(
                db,
                obj_in=schemas.GenerationHistoryCreate(
                    inputs=data.model_dump(),
                    output={"images": output_arr},
                    user_id=str(user.id),
                    is_deleted=False,
                    prompt=data.prompt,
                ),
            )
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": {
                        "id": str(result.id),
                        "inputs": result.inputs,
                        "is_deleted": result.is_deleted,
                        "output": result.output,
                        "prompt": result.prompt,
                        "updated_at": str(result.updated_at),
                        "created_at": str(result.created_at),
                    },
                    "message": "Images generated successfully",
                },
            )

        elif (
            output.get("data", {})
            .get("xfb_genai_imagine_results_for_prompt", {})
            .get("success")
            == False
        ) and (
            output.get("data", {})
            .get("xfb_genai_imagine_results_for_prompt", {})
            .get("response", {})[0]
            .get("__typename", "")
            == "XFBGenAIImagineResultGenericError"
        ):
            raise HTTPException(
                status_code=400,
                detail="This Image cannot be generated. Please try another prompt",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Image generation failed",
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
def remove_history(
    data: schemas.ImageID = Body(...),
    db: Session = Depends(get_db),
    user: schemas.UserBase = Depends(get_current_user),
):
    try:
        existing = crud.generation_history.get_owned_by_id(
            db, user_id=user.id, image_id=data.image_id
        )
        if existing:
            crud.image_like.remove(db, id=existing.id)
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": None,
                    "message": "Image removed",
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
        existing = crud.generation_history.get_owned_all(
            db, user_id=user.id, skip=offset
        )
        resp = [
            {
                "id": str(ele.id),
                "prompt": ele.prompt,
                "inputs": ele.inputs,
                "output": ele.output,
                "is_deleted": ele.is_deleted,
                "created_at": str(ele.created_at),
                "updated_at": str(ele.updated_at),
            }
            for ele in existing
        ]
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
