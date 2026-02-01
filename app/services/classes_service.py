class ClassesService:
    """
    Handles class-related business logic:
    - create classes
    - list classes
    - manage class membership
    """

    def __init__(self, class_repo):
        self.classes = class_repo