import test_utils
import server


def test_update_employee():
    # inject in-memory DB
    server.TEST_DB_CONN = test_utils.get_test_connection()

    server.add_employee("Alice", 30, "Developer")
    server.add_employee("Bose", 20, "QA")
    rows = server.list_employees()
    assert len(rows) == 2

    # Correct update: id=1
    server.update_employee(rows[1]["id"], "pavan", 25, "SE")

    rows = server.list_employees()
    assert rows[1]["name"] == "pavan"
    assert rows[1]["age"] == 25
    assert rows[1]["role"] == "SE"