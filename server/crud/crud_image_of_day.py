from typing import List, Optional

from sqlalchemy import Date, cast, desc
from sqlalchemy.orm import Session

from server import crud
from server.crud.base import CRUDBase
from server.models.image_of_day import ImageOfDay
from server.schemas.image_of_day import ImageOfDayCreate, ImageOfDayUpdate
from server.utils.config import settings


class CRUDImageOfDay(CRUDBase[ImageOfDay, ImageOfDayCreate, ImageOfDayUpdate]):
    def get_all(self, db: Session) -> List[ImageOfDay]:
        return db.query(ImageOfDay).all()

    def get_by_id(self, db: Session, *, id: str) -> ImageOfDay:
        return db.query(ImageOfDay).filter(ImageOfDay.id == id).first()

    def get_by_date(self, db: Session, *, date) -> ImageOfDay:
        return (
            db.query(ImageOfDay)
            .filter(ImageOfDay.date == date)
            .first()
        )

    def create(self, db: Session, *, obj_in: ImageOfDayCreate) -> ImageOfDay:
        return super().create(db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: ImageOfDay, obj_in: ImageOfDayUpdate
    ) -> ImageOfDay:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, *, id: str) -> Optional[ImageOfDay]:
        return super().remove(db, id=id)


image_of_day = CRUDImageOfDay(ImageOfDay)
