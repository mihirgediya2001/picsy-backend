from typing import List, Optional
from sqlalchemy.orm import Session

from server import crud
from server.crud.base import CRUDBase
from server.models.search import Search
from server.schemas.search import SearchCreate, SearchUpdate


class CRUDSearch(CRUDBase[Search, SearchCreate, SearchUpdate]):
    def get_all(self, db: Session) -> List[Search]:
        return db.query(Search).all()

    def get_by_id(self, db: Session, *, id: str) -> Search:
        return db.query(Search).filter(Search.id == id).first()

    def create(self, db: Session, *, obj_in: SearchCreate) -> Search:
        return super().create(db, obj_in=obj_in)

    def update(self, db: Session, *, db_obj: Search, obj_in: SearchUpdate) -> Search:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, *, id: str) -> Optional[Search]:
        return super().remove(db, id=id)


search = CRUDSearch(Search)
