<!-- Purpose: concise guidance for AI coding agents working in this repository -->
# Copilot / AI agent instructions for this repository

Goal
- Help AI agents be productive quickly by documenting the project's structure, entrypoints, developer workflows, and important local conventions discovered in the repo.

Quick summary
- This repo is a small Python-based agent/connector collection. Key items you will use:
  - `queryman.py` — primary script / high-level entrypoint to inspect first.
  - `requirements.txt` — Python dependencies; create a venv and `pip install -r requirements.txt`.
  - `components/` — contains agent modules (DB agent, Google agent, language agent);
    many files are duplicated with names containing "Copy (1)" or " - Copy" — treat these as potential duplicates and do not rename or remove them without asking the user.
  - `DOCS/` — architecture/diagram artifacts (look in `DOCS/Sybil Diagrams/` for DB and flow diagrams such as `mongodb_schema.drawio`).

Big picture / architecture notes (discoverable)
- The repository implements small, mostly independent agent modules under `components/` that appear to be composed by `queryman.py` at runtime. When you need to change behavior, inspect `queryman.py` to learn how it instantiates or imports components.
- Data flows to look for: agent modules in `components/` appear to perform I/O (DB, Google API, language models) and thus are the main integration points. Check `components/*config*` and `components/*db*` files when investigating persistence.

Developer workflows (how to build/run/test)
- Python environment (assumed):
  - Create venv: `python -m venv .venv`
  - Activate (Windows PowerShell): `.\.venv\Scripts\Activate.ps1`
  - Install deps: `pip install -r requirements.txt`
  - Run main: `python queryman.py`
- There are no discoverable pytest or automated test files in the repo root. If you add tests, prefer `pytest` and place tests in `tests/`.
- Note: VS Code tasks in this workspace reference Maven tasks; ignore those for Python development unless you explicitly confirm a Java/Maven subproject exists.

Patterns & conventions specific to this repo
- Duplicate filenames: Many files in `components/` include `Copy` in their name. These are likely artifacts from copying — avoid bulk renames/deletions. If consolidating, ask the owner first and update imports in `queryman.py` accordingly.
- Minimal module packaging: modules appear to be standalone Python scripts (not installed packages). Prefer simple edits (in-place) and minimal refactors that preserve the module-level script interface.
- Config discovery: search for `config`, `config_db`, or `settings` in `components/` when changing database or API settings.

Integration & external dependencies
- External services you will commonly encounter:
  - Databases (review `DOCS/Sybil Diagrams/mongodb_schema.drawio` for DB usage hints).
  - External APIs (e.g., Google API integrations in files named `googleagent*`).
- Always do a quick grep for API keys or credentials before running networked code locally. Prefer stubbing/mocking external calls in edits and tests.

Editing rules for AI agents (must-follow)
- Do not rename or delete files that contain "Copy" without explicit confirmation from the repo owner. These may be intentionally retained.
- Keep changes minimal and targeted: alter the smallest number of files to implement a feature/bugfix.
- When adding or changing dependencies, notify the user and provide the exact `pip` command. Ask before modifying `requirements.txt`.
- If you modify runtime wiring (imports in `queryman.py`), include a brief note in `DOCS/` or update `README.txt` to explain the change and why.

Examples (where to look in the codebase)
- Entrypoint/flow: `queryman.py`
- Agents and connectors: `components/` (look for filenames like `dbagent - Copy.py`, `googleagent - Copy.py`, `langagent - Copy.py`)
- Dependency list: `requirements.txt`
- Diagrams and persistent-model hints: `DOCS/Sybil Diagrams/mongodb_schema.drawio`

If you need clarification
- Ask the repository owner before making bulk renames, dependency changes, or when enabling networked calls.
- After making edits, ask whether to run the code locally or to produce a PR.

Next step for humans
- Please review these instructions and tell me if you'd like me to merge duplicate modules, add a README.md, or scaffold tests and a `tests/` directory.

-- End of file
