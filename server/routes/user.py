import uuid
import json
from typing import Optional, Union
from datetime import timedelta

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Header, HTTPException
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from sqlalchemy.orm import Session
from server.utils.auth import create_access_token, get_current_user

from server import crud, schemas
from server.models import user as models
from server.utils.config import settings
from server.utils.database import get_db

import firebase_admin
from firebase_admin import credentials, auth

router = APIRouter(prefix="/user")
access_token_expires = timedelta(minutes=500000)



cred = credentials.Certificate("./_service_account_keys.json")
firebase = firebase_admin.initialize_app(cred)


@router.post("/login")
async def login(
    payload: schemas.user.FreeUserLogin,
    db: Session = Depends(get_db),
    user_agent: Union[str, None] = Header(default=None),
):
    try:
        user = (
            db.query(models.User)
            .filter(models.User.browser_token == payload.browser_token)
            .first()
        )
        if not user:
            user = crud.user.create(
                db,
                obj_in=schemas.user.UserBase(
                    id=uuid.uuid4(),
                    browser_token=payload.browser_token,
                    client_country=payload.client_country,
                    client_ip=payload.client_ip,
                    client_browser=user_agent,
                ),
            )
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": {"is_new": True},
                    "message": "Image liked",
                    "error": None,
                },
            )
        return True
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e,
        )
    finally:
        db.close()


@router.post("/token", response_model=schemas.OutputSessionLogin)
def session_login(
    input_data: schemas.SessionLoginInput,
    sign_in_with: schemas.SignInWithEnum,
    is_web: Optional[bool] = False,
    db: Session = Depends(get_db),
) -> any:
    id_token = input_data.id_token
    email = ""
    avatar = ""
    displayName = "Guest"
    providers = [sign_in_with]
    if sign_in_with == schemas.SignInWithEnum.google:
        try:
            if is_web:
                google_user_info = google_id_token.verify_oauth2_token(
                    id_token,
                    google_requests.Request(),
                    settings.GOOGLE_CLIENT_ID,
                )
            else:
                google_user_info = auth.verify_id_token(id_token)

            email = google_user_info["email"]
            current_user = crud.user.get_by_email(db, email=email)
            displayName = google_user_info["name"]
            if "picture" in google_user_info:
                avatar = google_user_info["picture"]
        except ValueError:
            raise HTTPException(406, "Invalid Google Auth")

    if not current_user:
        # create account
        providers = [sign_in_with]
        current_user = crud.user.create(
            db,
            obj_in=schemas.UserCreate(
                name=displayName,
                email=email,
                avatar=avatar,
                is_verified=google_user_info["email_verified"],
                providers=json.dumps(providers),
            ),
        )
    providers = []
    if current_user.providers:
        try:
            new_providers = json.loads(current_user.providers)
            if type(new_providers) == list:
                providers = new_providers
        except Exception:
            pass
    # if sign_in_with not in providers:
    #     providers.append(sign_in_with)
    # obj_in = schemas.UserUpdate(
    #     last_signed_date=datetime.utcnow(),
    #     providers=json.dumps(providers),
    # )
    # if avatar:
    #     obj_in.avatar = avatar
    # current_user = crud.user.update(
    #     db,
    #     db_obj=current_user,
    #     obj_in=obj_in,
    # )

    return schemas.OutputSessionLogin(
        id=str(current_user.id),
        email=email,
        token=create_access_token(
            data={"id": str(current_user.id)}, expires_delta=access_token_expires
        ),
    )


@router.get("/profile", response_model=schemas.OutputUser)
async def read_users_me(
    db: Session = Depends(get_db),
    current_user: schemas.OutputUser = Depends(get_current_user),
):
    likes = crud.user.get_total_likes(db, user_id=current_user.id)
    current_user.total_likes = likes
    return current_user
