import sqlite3
from mcp.server.fastmcp import FastMCP

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "employees.db")


mcp = FastMCP("EmployeeMCP", json_response=True)


TEST_DB_CONN = None  # used only for tests


def get_conn():
    """Return connection for production or testing (if TEST_DB_CONN set)."""
    global TEST_DB_CONN
    if TEST_DB_CONN:
        return TEST_DB_CONN
    return sqlite3.connect(DB_FILE)


# ===============================
#     TOOL: ADD EMPLOYEE
# ===============================
@mcp.tool()
def add_employee(name: str, age: int, role: str) -> str:
    """Add an employee to the database."""
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO employees (name, age, role) VALUES (?, ?, ?)",
        (name, age, role)
    )

    conn.commit()
    if TEST_DB_CONN is None:
        conn.close()

    return f"Employee '{name}' added successfully."


# ===============================
#     TOOL: UPDATE EMPLOYEE
# ===============================
@mcp.tool()
def update_employee(id: int, name: str, age: int, role: str) -> str:
    """Update an employee in the database."""
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE employees SET name = ?, age = ?, role = ? WHERE id = ?",
        (name, age, role, id)
    )

    conn.commit()
    rows_count = cursor.rowcount
    if TEST_DB_CONN is None:
        conn.close()
    if (rows_count == 0):
        return f"No Employee with the id: {id} found"  
    return f"Employee '{name}' and '{id}' updated successfully."


# ===============================
#     TOOL: DELETE EMPLOYEE
# ===============================
@mcp.tool()
def delete_employee(id: int) -> str:
    """Delete an employee in the database."""
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id = ?",
        (id,)
    )

    conn.commit()
    rows_count = cursor.rowcount
    if TEST_DB_CONN is None:
        conn.close()
    if (rows_count == 0):
        return f"No Employee with the id: {id} found"
    return f"Employee with id: '{id}' deleted successfully."


# ===============================
#     TOOL: LIST EMPLOYEES
# ===============================
@mcp.tool()
def list_employees() -> list:
    """Return all employees from the database."""
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, age, role FROM employees")
    rows = cursor.fetchall()

    if TEST_DB_CONN is None:
        conn.close()

    return [
        {"id": r[0], "name": r[1], "age": r[2], "role": r[3]}
        for r in rows
    ]


# ===============================
#     TOOL: LIST SPECIFIC EMPLOYEES
# ===============================
@mcp.tool()
def list_specific_employees(
    id: int | None = None, 
    name: str | None = None, 
    name_contains: str | None = None,
    age: int | None = None, 
    role: str | None = None,
    role_contains: str | None = None,
    min_age: int | None = None,
    max_age: int | None = None
) -> list:
    """Return employees matching filters"""

    conn = get_conn()
    cursor = conn.cursor()

    query = "SELECT id, name, age, role FROM employees WHERE 1=1"
    params = []

    if id is not None:
        query += " AND id = ?"
        params.append(id)

    if name:
        query += " AND name = ?"
        params.append(name)

    if name_contains:
        query += " AND LOWER(name) LIKE ?"
        params.append(f"%{name_contains.lower()}%")

    if age is not None:
        query += " AND age = ?"
        params.append(age)

    if role:
        query += " AND LOWER(role) = ?"
        params.append(role.lower())

    if role_contains:
        query += " AND LOWER(role) LIKE ?"
        params.append(f"%{role_contains.lower()}%")

    if min_age is not None:
        query += " AND age >= ?"
        params.append(min_age)

    if max_age is not None:
        query += " AND age <= ?"
        params.append(max_age)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    if TEST_DB_CONN is None:
        conn.close()

    return [
        {"id": r[0], "name": r[1], "age": r[2], "role": r[3]}
        for r in rows
    ]


# ===============================
#     START MCP SERVER
# ===============================
if __name__ == "__main__":
    mcp.run()
