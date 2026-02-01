class FeedbackService:
    """
    Handles feedback-related business logic:
    - attach feedback to requirements
    - compute marking results
    - retrieve feedback for scenarios
    """

    def __init__(self, feedback_repo):
        self.feedback = feedback_repo