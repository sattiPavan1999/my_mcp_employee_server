import test_utils
import server


def test_list_all_employees():
    # inject in-memory DB
    server.TEST_DB_CONN = test_utils.get_test_connection()

    server.add_employee("A", 20, "admin")
    server.add_employee("B", 30, "admin")
    server.add_employee("C", 40, "user")
    rows = server.list_employees()
    assert len(rows) == 3

    get_employee = server.list_specific_employees(rows[1]["id"], "B")
    assert len(get_employee) != 0