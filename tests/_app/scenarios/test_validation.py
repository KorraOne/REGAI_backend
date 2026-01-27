def test_create_scenario_missing_title(auth_client):
    client = auth_client("a@b.com", "pass")
    payload = {
        "short_desc": "Short",
        "long_desc": "Long",
        "categories": [],
        "stakeholders": []
    }
    res = client.post("/scenarios/", json=payload)
    assert res.status_code == 422

def test_create_scenario_missing_short_desc(auth_client):
    client = auth_client("a@b.com", "pass")
    payload = {
        "title": "My Scenario",
        "long_desc": "Long",
        "categories": [],
        "stakeholders": []
    }
    res = client.post("/scenarios/", json=payload)
    assert res.status_code == 422

def test_create_scenario_title_wrong_type(auth_client):
    client = auth_client("a@b.com", "pass")
    payload = {
        "title": 123,  # invalid
        "short_desc": "Short",
        "long_desc": "Long",
        "categories": [],
        "stakeholders": []
    }
    res = client.post("/scenarios/", json=payload)
    assert res.status_code == 422


def test_create_scenario_stakeholder_missing_fields(auth_client):
    client = auth_client("a@b.com", "pass")
    payload = {
        "title": "Scenario",
        "short_desc": "Short",
        "long_desc": "Long",
        "categories": [],
        "stakeholders": [
            {"id": 1, "name": "Alice"}  # missing role + desc
        ]
    }
    res = client.post("/scenarios/", json=payload)
    assert res.status_code == 422

def test_create_scenario_category_missing_fields(auth_client):
    client = auth_client("a@b.com", "pass")
    payload = {
        "title": "Scenario",
        "short_desc": "Short",
        "long_desc": "Long",
        "categories": [
            {"id": 1}  # missing name
        ],
        "stakeholders": []
    }
    res = client.post("/scenarios/", json=payload)
    assert res.status_code == 422

def test_create_scenario_stakeholders_not_list(auth_client):
    client = auth_client("a@b.com", "pass")
    payload = {
        "title": "Scenario",
        "short_desc": "Short",
        "long_desc": "Long",
        "categories": [],
        "stakeholders": "not-a-list"
    }
    res = client.post("/scenarios/", json=payload)
    assert res.status_code == 422