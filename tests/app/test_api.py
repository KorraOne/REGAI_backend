from tests.app.helpers import run_test, get, post, print_summary, clear_db
from tests.app.config import TEST_USERS, TEST_SCENARIO


def main():
    print("\n=== Starting API Test Suite ===\n")
    clear_db()

    # 1. Debug DB
    run_test("Debug DB (initial)", 200, lambda: get("/debug/db"))

    # 2. Register User #1
    run_test("Register User #1", 200,
             lambda: post("/auth/register", json=TEST_USERS["user1"]))

    # 3. Register User #2
    run_test("Register User #2", 200,
             lambda: post("/auth/register", json=TEST_USERS["user2"]))

    # 4. Duplicate email
    run_test("Register duplicate email", 409,
             lambda: post("/auth/register", json=TEST_USERS["user1"]))

    # 5. Login User #1
    login_res = run_test("Login User #1", 200,
                         lambda: post("/auth/login", json={
                             "email": TEST_USERS["user1"]["email"],
                             "password": TEST_USERS["user1"]["password"]
                         }))
    token = login_res.json()["access_token"]

    # 6. Get scenarios (empty)
    run_test("Get scenarios (empty)", 200,
             lambda: get("/scenarios/", token=token))

    # 7. Get scenario #1 (should fail)
    run_test("Get scenario #1 (not found)", 404,
             lambda: get("/scenarios/1", token=token))

    # 8. Create scenario
    create_res = run_test("Create scenario", 200,
                          lambda: post("/scenarios/", json=TEST_SCENARIO, token=token))

    # 9. Get scenarios (should have 1)
    run_test("Get scenarios (after creation)", 200,
             lambda: get("/scenarios/", token=token))

    # 10. Get scenario #1 (exists now)
    run_test("Get scenario #1 (exists)", 200,
             lambda: get("/scenarios/1", token=token))

    print("\n=== Test Suite Complete ===\n")

    print_summary()


if __name__ == "__main__":
    main()