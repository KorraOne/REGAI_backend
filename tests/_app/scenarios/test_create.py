def test_create_scenario(auth_client):
    client = auth_client("a@b.com", "pass")
    payload = {
        "title": "My Scenario",
        "short_desc": "Short",
        "long_desc": "Long",
        "categories": [],
        "stakeholders": [
            {"id": 1, "name": "Alice", "role": "Manager", "desc": "Boss"}
        ]
    }
    res = client.post("/scenarios/", json=payload)
    assert res.status_code == 200
    assert res.json()["scenario_id"] == 1