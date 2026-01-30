from datetime import datetime, timezone
from sqlalchemy.orm import Session

def soft_delete(db: Session, model, id: int):
    """Soft delete a row by setting deleted_at."""
    obj = (
        db.query(model)
        .filter(model.id == id, model.deleted_at.is_(None))
        .first()
    )
    if not obj:
        return None

    obj.deleted_at = datetime.now(timezone.utc)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def restore(db: Session, model, id: int):
    """Restore a soft-deleted row."""
    obj = (
        db.query(model)
        .filter(model.id == id, model.deleted_at.is_not(None))
        .first()
    )
    if not obj:
        return None

    obj.deleted_at = None
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_active(db: Session, model, **filters):
    """Return only non-deleted rows."""
    return (
        db.query(model)
        .filter(model.deleted_at.is_(None))
        .filter_by(**filters)
        .all()
    )


def get_deleted(db: Session, model, **filters):
    """Return only soft-deleted rows."""
    return (
        db.query(model)
        .filter(model.deleted_at.is_not(None))
        .filter_by(**filters)
        .all()
    )


def get_all(db: Session, model, **filters):
    """Return all rows, including deleted ones."""
    return db.query(model).filter_by(**filters).all()