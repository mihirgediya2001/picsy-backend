from typing import List, Optional

from sqlalchemy import Date, cast, desc
from sqlalchemy.orm import Session

from server import crud
from server.crud.base import CRUDBase
from server.models.image_like import ImageLike
from server.schemas.image_like import ImageLikeCreate, ImageLikeUpdate
from server.utils.config import settings


class CRUDImageLike(CRUDBase[ImageLike, ImageLikeCreate, ImageLikeUpdate]):
    def get_all(self, db: Session) -> List[ImageLike]:
        return db.query(ImageLike).all()

    def get_by_id(self, db: Session, *, id: str) -> ImageLike:
        return db.query(ImageLike).filter(ImageLike.id == id).first()

    def get_owned_by_id(self, db: Session, *, image_id: str, user_id: str) -> ImageLike:
        return (
            db.query(ImageLike)
            .filter(ImageLike.image_id == image_id, ImageLike.user_id == user_id)
            .first()
        )

    def get_owned_all(
        self,
        db: Session,
        *,
        user_id: str,
        skip: int = 0,
        n: int = settings.PAGINATION_SIZE
    ) -> ImageLike:
        return (
            db.query(ImageLike)
            .filter(ImageLike.user_id == user_id)
            .order_by(desc(ImageLike.created_at))
            .with_entities(ImageLike.image_id, ImageLike.created_at)
            .offset(skip)
            .limit(n)
            .all()
        )

    def get_my_liked(self, db: Session, *, user_id: str, ids) -> ImageLike:
        return (
            db.query(ImageLike)
            .filter(ImageLike.user_id == user_id, ImageLike.image_id.in_(ids))
            .all()
        )

    def create(self, db: Session, *, obj_in: ImageLikeCreate) -> ImageLike:
        return super().create(db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: ImageLike, obj_in: ImageLikeUpdate
    ) -> ImageLike:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, *, id: str) -> Optional[ImageLike]:
        return super().remove(db, id=id)


image_like = CRUDImageLike(ImageLike)
