from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, ForeignKey,
    Enum, TIMESTAMP, func
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# ---------------------------------------------------------
# Soft delete mixin
# ---------------------------------------------------------
class SoftDeleteMixin:
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

# ---------------------------------------------------------
# Created at mixin
# ---------------------------------------------------------
class TimestampMixin:
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

# ---------------------------------------------------------
# Enum for marking status
# ---------------------------------------------------------
class MarkingStatus(PyEnum):
    draft = "draft"
    submitted = "submitted"
    marked = "marked"
    returned = "returned"

# ---------------------------------------------------------
# USERS
# ---------------------------------------------------------
class Users(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    fname = Column(String(100), nullable=False)
    lname = Column(String(100), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    subscription_expires_at = Column(TIMESTAMP(timezone=True), nullable=True)
    subscription_tier = Column(String(50), nullable=True)

    owned_scenarios = relationship("Scenarios", back_populates="owner")

# ---------------------------------------------------------
# CLASS
# ---------------------------------------------------------
class Class(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "class"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    students = relationship("StudentsOfClass", back_populates="class_")
    teachers = relationship("ClassTeacher", back_populates="class_")

# ---------------------------------------------------------
# CLASS ↔ TEACHER (many-to-many)
# ---------------------------------------------------------
class ClassTeacher(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "class_teacher"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class.id"), nullable=False)

    teacher = relationship("Users")
    class_ = relationship("Class", back_populates="teachers")

# ---------------------------------------------------------
# STUDENTS OF CLASS (many-to-many)
# ---------------------------------------------------------
class StudentsOfClass(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "students_of_class"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class.id"), nullable=False)

    user = relationship("Users")
    class_ = relationship("Class", back_populates="students")

# ---------------------------------------------------------
# SENIOR DEV TEMPLATES
# ---------------------------------------------------------
class SeniorDevTemplates(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "senior_dev_templates"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    desc = Column(Text, nullable=True)
    prompt = Column(Text, nullable=False)

# ---------------------------------------------------------
# SCENARIOS
# ---------------------------------------------------------
class Scenarios(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    short_desc = Column(Text, nullable=True)
    long_desc = Column(Text, nullable=True)
    marking_status = Column(Enum(MarkingStatus), default=MarkingStatus.draft)

    owner = relationship("Users", back_populates="owned_scenarios")
    stakeholders = relationship("Stakeholder", back_populates="scenario")
    requirements = relationship("Requirements", back_populates="scenario")
    categories = relationship("ScenarioCategories", back_populates="scenario")
    feedback = relationship("FeedbackReference", back_populates="scenario")

# ---------------------------------------------------------
# CATEGORIES
# ---------------------------------------------------------
class Categories(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    scenarios = relationship("ScenarioCategories", back_populates="category")

# ---------------------------------------------------------
# SCENARIO ↔ CATEGORY (many-to-many)
# ---------------------------------------------------------
class ScenarioCategories(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "scenario_categories"

    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    scenario = relationship("Scenarios", back_populates="categories")
    category = relationship("Categories", back_populates="scenarios")

# ---------------------------------------------------------
# STAKEHOLDER
# ---------------------------------------------------------
class Stakeholder(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "stakeholder"

    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    desc = Column(Text, nullable=True)
    prompt = Column(Text, nullable=False)
    is_senior_dev = Column(Boolean, default=False)

    scenario = relationship("Scenarios", back_populates="stakeholders")
    chat_histories = relationship("ChatHistory", back_populates="stakeholder")

# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------
class ChatHistory(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)
    stakeholder_id = Column(Integer, ForeignKey("stakeholder.id"), nullable=False)

    stakeholder = relationship("Stakeholder", back_populates="chat_histories")
    messages = relationship("ChatMessage", back_populates="history")

# ---------------------------------------------------------
# CHAT MESSAGE
# ---------------------------------------------------------
class ChatMessage(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "chat_message"

    id = Column(Integer, primary_key=True)
    chat_history_id = Column(Integer, ForeignKey("chat_history.id"), nullable=False)
    sent_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    sent_by = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)

    history = relationship("ChatHistory", back_populates="messages")
    feedback_refs = relationship("FeedbackReference", back_populates="chat_message")

# ---------------------------------------------------------
# REQUIREMENTS
# ---------------------------------------------------------
class Requirements(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    type = Column(String(255), nullable=False)
    requirement = Column(Text, nullable=False)

    scenario = relationship("Scenarios", back_populates="requirements")
    feedback_refs = relationship("FeedbackReference", back_populates="requirement")

# ---------------------------------------------------------
# FEEDBACK REFERENCE
# ---------------------------------------------------------
class FeedbackReference(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "feedback_reference"

    id = Column(Integer, primary_key=True)
    feedback = Column(Text, nullable=False)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=True)
    chat_message_id = Column(Integer, ForeignKey("chat_message.id"), nullable=True)

    scenario = relationship("Scenarios", back_populates="feedback")
    requirement = relationship("Requirements", back_populates="feedback_refs")
    chat_message = relationship("ChatMessage", back_populates="feedback_refs")