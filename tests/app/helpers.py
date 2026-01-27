import requests
from tests.app.config import BASE_URL

# Store results for summary
TEST_RESULTS = []

def clear_db():
    """Reset the backend in-memory DB to a clean state."""
    try:
        res = requests.delete(f"{BASE_URL}/debug/db")
        if res.status_code != 200:
            print(f"[WARN] clear_db() returned {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[ERROR] clear_db() failed: {e}")
        

def print_result(name, expected, actual, body):
    status = "PASS" if expected == actual else "FAIL"
    print(f"\n=== {name} ===")
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")
    print(f"Result:   {status}")
    print(f"Body:     {body}")

def print_summary():
    total = len(TEST_RESULTS)
    passed = sum(1 for r in TEST_RESULTS if r["passed"])
    failed = total - passed

    print("\n==================== TEST SUMMARY ====================")
    print(f"Total tests: {total}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")
    print("======================================================")

    if failed > 0:
        print("\nFailed tests:")
        for r in TEST_RESULTS:
            if not r["passed"]:
                print(f" - {r['name']} (expected {r['expected']}, got {r['actual']})")

def run_test(name, expected_status, func):
    try:
        response = func()
        actual_status = response.status_code
        body = response.json() if response.content else None
    except Exception as e:
        actual_status = "ERROR"
        body = str(e)

    # Print result
    print_result(name, expected_status, actual_status, body)

    # Record result
    TEST_RESULTS.append({
        "name": name,
        "expected": expected_status,
        "actual": actual_status,
        "passed": expected_status == actual_status
    })

    return response

def get(url, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.get(f"{BASE_URL}{url}", headers=headers)

def post(url, json=None, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.post(f"{BASE_URL}{url}", json=json, headers=headers)