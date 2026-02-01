class ScenariosService:
    """
    Handles scenario-related business logic:
    - create scenarios
    - add requirements
    - assign stakeholders
    - manage categories
    - handle templates
    """

    def __init__(
        self,
        scenarios_repo,
        requirements_repo,
        stakeholders_repo,
        categories_repo,
        scenario_categories_repo,
        templates_repo
    ):
        self.scenarios = scenarios_repo
        self.requirements = requirements_repo
        self.stakeholders = stakeholders_repo
        self.categories = categories_repo
        self.scenario_categories = scenario_categories_repo
        self.templates = templates_repo