To run tests: pytest -v
To install mcp server: mcp install server.py
To run mcp server: mcp dev server.py
To create venv: python3 -m venv venv
To activate venv: source venv/bin/activate


To install all packages listed in your requirements.txt, the command is:
pip install -r requirements.txt

If you're using a virtual environment (recommended), activate it first:
macOS / Linux:
source venv/bin/activate

Windows:
venv\Scripts\activate

Then run:
pip install -r requirements.txt


⭐ If you want to upgrade all packages in the file:
pip install --upgrade -r requirements.txt


⭐ If you want to confirm what was installed:
pip list


⭐ If pip = Python mismatch (common issue)
Use:
python -m pip install -r requirements.txt

This guarantees pip installs into the correct Python.

If you want, I can generate a clean requirements.txt for your MCP + SQLite + Pytest project.
