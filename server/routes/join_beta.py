import re

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from server.schemas.join_beta_control import JoinBetaSchema
from server.models.join_beta import JoinBeta
from server.utils.database import get_db

router = APIRouter(prefix="/join-beta")

emailP_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


def validate_email(email):
    if re.fullmatch(emailP_regex, email):
        return True
    return False


@router.post("")
def join_beta(
    payload: JoinBetaSchema,
    db: Session = Depends(get_db),
    request: Request = None,
):
    client_host = request.client.host
    email = payload.email.strip()
    try:
        valiudate = validate_email(email)
        if valiudate:
            existing = db.query(JoinBeta).filter(JoinBeta.email == email).first()
            if existing:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "data": None,
                        "message": "Email is already in waitlist",
                        "error": None,
                    },
                )
            db.add(JoinBeta(email=email, client_host=client_host))
            db.commit()
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "data": None,
                    "message": "Invalid email",
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
