from db.crud.base_repository import BaseRepository
from db.models import Users, StudentsOfClass, ClassTeacher

class UsersRepository(BaseRepository):
    model = Users

class StudentsOfClassRepository(BaseRepository):
    model = StudentsOfClass

class ClassTeacherRepository(BaseRepository):
    model = ClassTeacher