from typing import List, Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session

from server import crud
from server.crud.base import CRUDBase
from server.models.generation_history import GenerationHistory
from server.schemas.generation_history import (
    GenerationHistoryCreate,
    GenerationHistoryUpdate,
)
from server.utils.config import settings


class CRUDGenerationHistory(
    CRUDBase[GenerationHistory, GenerationHistoryCreate, GenerationHistoryUpdate]
):
    def get_all(self, db: Session) -> List[GenerationHistory]:
        return db.query(GenerationHistory).all()

    def get_by_id(self, db: Session, *, id: str) -> GenerationHistory:
        return db.query(GenerationHistory).filter(GenerationHistory.id == id).first()

    def create(
        self, db: Session, *, obj_in: GenerationHistoryCreate
    ) -> GenerationHistory:
        return super().create(db, obj_in=obj_in)

    def update(
        self, db: Session, *, db_obj: GenerationHistory, obj_in: GenerationHistoryUpdate
    ) -> GenerationHistory:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, *, id: str) -> Optional[GenerationHistory]:
        return super().remove(db, id=id)

    def get_owned_by_id(self, db: Session, *, history_id: str, user_id: str):
        return (
            db.query(GenerationHistory)
            .filter(
                GenerationHistory.id == history_id, GenerationHistory.user_id == user_id
            )
            .first()
        )

    def get_owned_all(
        self,
        db: Session,
        *,
        user_id: str,
        skip: int = 0,
        n: int = settings.PAGINATION_SIZE
    ) -> GenerationHistory:
        return (
            db.query(GenerationHistory)
            .filter(GenerationHistory.user_id == user_id)
            .order_by(desc(GenerationHistory.created_at))
            .offset(skip)
            .limit(n)
            .all()
        )


generation_history = CRUDGenerationHistory(GenerationHistory)
