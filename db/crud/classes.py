from db.crud.base_repository import BaseRepository
from db.models import Class

class ClassRepository(BaseRepository):
    model = Class