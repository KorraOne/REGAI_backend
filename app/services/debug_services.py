class DebugService:
    """
    Provides debug and development utilities:
    - inspect database state
    - clear all tables (soft + hard delete)
    """

    def __init__(self, db):
        self.db = db

    # ---------------------------------------------------------
    # GET DATABASE STATE
    # ---------------------------------------------------------
    def get_db_state(self):
        """
        Return a summary of row counts for each table.
        Useful for debugging and verifying test data.
        """
        from db.models import (
            Users,
            Class,
            ClassTeacher,
            StudentsOfClass,
            Scenarios,
            Requirements,
            Stakeholder,
            Categories,
            ScenarioCategories,
            SeniorDevTemplates,
            ChatHistory,
            ChatMessage,
            FeedbackReference,
        )

        tables = {
            "users": Users,
            "class": Class,
            "class_teacher": ClassTeacher,
            "students_of_class": StudentsOfClass,
            "scenarios": Scenarios,
            "requirements": Requirements,
            "stakeholder": Stakeholder,
            "categories": Categories,
            "scenario_categories": ScenarioCategories,
            "senior_dev_templates": SeniorDevTemplates,
            "chat_history": ChatHistory,
            "chat_message": ChatMessage,
            "feedback_reference": FeedbackReference,
        }

        state = {}
        for name, model in tables.items():
            count = self.db.query(model).count()
            state[name] = count

        return state

    # ---------------------------------------------------------
    # CLEAR DATABASE
    # ---------------------------------------------------------
    def clear_database(self):
        """
        Hard-delete all rows from all tables.
        This is ONLY for development/testing.
        """

        from db.models import (
            Users,
            Class,
            ClassTeacher,
            StudentsOfClass,
            Scenarios,
            Requirements,
            Stakeholder,
            Categories,
            ScenarioCategories,
            SeniorDevTemplates,
            ChatHistory,
            ChatMessage,
            FeedbackReference,
        )

        models = [
            FeedbackReference,
            ChatMessage,
            ChatHistory,
            Requirements,
            Stakeholder,
            ScenarioCategories,
            Categories,
            SeniorDevTemplates,
            Scenarios,
            StudentsOfClass,
            ClassTeacher,
            Class,
            Users,
        ]

        # Delete in dependency-safe order
        for model in models:
            self.db.query(model).delete()

        self.db.commit()

        return {"status": "database cleared"}