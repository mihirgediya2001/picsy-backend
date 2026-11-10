import json

from typing import Dict
from fastapi import APIRouter, Body, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from server.utils.config import settings
from server import crud, schemas
from server.utils.auth import authenticate_admin
from server.utils.database import get_db


def read_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{file_path}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def write_json_file(data, file_path):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)
        print(f"JSON data written successfully to '{file_path}'.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


router = APIRouter(prefix="/admin")


@router.get("/get-splash-screen")
def get_splash_screen_config(
    db: Session = Depends(get_db),
):
    try:
        file_path = f"server/static/prod/splash-screen.json"
        data = read_json_file(file_path)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": data,
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


@router.post("/splash-screen")
def splash_screen_config(
    admin: bool = Depends(authenticate_admin),
    db: Session = Depends(get_db),
    data: dict = Body(...),
):
    try:
        file_path = f"server/static/{data.get('env_type')}/splash-screen.json"
        data = read_json_file(file_path)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": data,
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


@router.post("/update-splash-screen")
def update_splash_screen_config(
    admin: bool = Depends(authenticate_admin),
    data: dict = Body(...),
    env_type: str = Body(...),
    db: Session = Depends(get_db),
):
    try:
        file_path = f"server/static/{env_type}/splash-screen.json"
        write_json_file(data, file_path)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": data,
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


@router.post("/get-all-users")
def get_all_users(
    admin: bool = Depends(authenticate_admin),
    page: int = Body(0),
    n: int = Body(10),
    db: Session = Depends(get_db),
):
    try:
        users = crud.user.get_all_with_email(db=db, skip=page, n=n)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": [
                    {
                        "id": str(schema.id),
                        "avatar": str(schema.avatar),
                        "name": str(schema.name),
                        "email": str(schema.email),
                        "created_at": str(schema.created_at),
                        "is_verified": schema.is_verified,
                        "is_deleted": schema.is_deleted,
                        "fb_uid": schema.fb_uid,
                        "providers": schema.providers,
                    }
                    for schema in users
                ],
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


@router.post("/get-total-users")
def get_total_users(
    admin: bool = Depends(authenticate_admin),
    db: Session = Depends(get_db),
):
    try:
        total = crud.user.get_total_with_email(db=db)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": total,
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
