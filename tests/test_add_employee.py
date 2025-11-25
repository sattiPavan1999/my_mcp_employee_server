import test_utils
import server


def test_add_employee():
    # inject in-memory DB
    server.TEST_DB_CONN = test_utils.get_test_connection()

    # call tool
    res = server.add_employee("Alice", 30, "Developer")
    assert "successfully" in res.lower()

    rows = server.list_employees()
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"
    assert rows[0]["age"] == 30
    assert rows[0]["role"] == "Developer"
