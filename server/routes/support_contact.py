import re

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from server.schemas.support_contact import SupportContactSchema
from server.models.support_contact import SupportContact
from server.utils.database import get_db

router = APIRouter(prefix="/support-contact")

emailP_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


def validate_email(email):
    if re.fullmatch(emailP_regex, email):
        return True
    return False


@router.post("")
def join_beta(
    payload: SupportContactSchema,
    db: Session = Depends(get_db),
    request: Request = None,
):
    client_host = request.client.host
    email = payload.email.strip()
    try:
        validate = validate_email(email)
        if validate:
            db.add(
                SupportContact(
                    email=email,
                    name=payload.name,
                    message=payload.name,
                    client_host=client_host,
                )
            )
            db.commit()
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "data": None,
                    "message": "Invalid email provided",
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
