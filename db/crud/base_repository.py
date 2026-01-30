from datetime import datetime
from sqlalchemy.orm import Session

class Base_Repository:
    """
    Generic repository providing CRUD + soft delete operations.
    Subclasses must set `model` to a SQLAlchemy model class.
    """

    model = None  # override in subclasses

    def __init__(self, db: Session):
        self.db = db

    # -----------------------------
    # GET (active only)
    # -----------------------------
    def get(self, id: int):
        return (
            self.db.query(self.model)
            .filter(self.model.id == id, self.model.deleted_at.is_(None))
            .first()
        )

    # -----------------------------
    # LIST (active only)
    # -----------------------------
    def list(self, **filters):
        return (
            self.db.query(self.model)
            .filter(self.model.deleted_at.is_(None))
            .filter_by(**filters)
            .all()
        )

    # -----------------------------
    # CREATE
    # -----------------------------
    def create(self, **data):
        obj = self.model(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update(self, id: int, **data):
        obj = self.get(id)
        if not obj:
            return None

        for key, value in data.items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    # -----------------------------
    # SOFT DELETE
    # -----------------------------
    def delete(self, id: int):
        obj = self.get(id)
        if not obj:
            return None

        obj.deleted_at = datetime.utcnow()
        self.db.commit()
        return obj

    # -----------------------------
    # RESTORE
    # -----------------------------
    def restore(self, id: int):
        obj = (
            self.db.query(self.model)
            .filter(self.model.id == id, self.model.deleted_at.is_not(None))
            .first()
        )
        if not obj:
            return None

        obj.deleted_at = None
        self.db.commit()
        return obj

    # -----------------------------
    # GET ALL (active + deleted)
    # -----------------------------
    def all(self, **filters):
        return self.db.query(self.model).filter_by(**filters).all()