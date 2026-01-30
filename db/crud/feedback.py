from db.crud.base_repository import BaseRepository
from db.models import FeedbackReference

class FeedbackReferenceRepository(BaseRepository):
    model = FeedbackReference