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

Detected dependencies (from `requirements.txt` and imports)
- Declared in `requirements.txt`: `certifi`, `google`, `pymongo`, `Unidecode`, `simplejson` (many entries are commented out).
- Files import these libraries: `pymongo`, `googlesearch` (`from googlesearch import search`), `unidecode`, `langdetect`, `certifi`, and standard libs `urllib`, `re`, `ssl`, `time`.

Import & function map (quick reference)
- `queryman.py` imports: `components.config_db`, `components.dbagent` (uses `db_status`, `query_list`), `components.ioagent`.
- `components/dbagent - Copy.py`: provides `db_core`, `db_status`, `db_core_collection`, CRUD helpers (`db_insertone`, `db_findmany`, `db_findone`, `db_updateone`, etc.).
- `components/Copy (1) ioagent - Copy.py`: provides `query_lastnum`, `query_list` and wraps `dbagent` helpers.
- `components/googleagent - Copy.py`: provides `google_search(search_query)` which uses `googlesearch.search` and sanitizes queries.
- `components/Copy (1) langagent - Copy.py`: provides `langdet(text)` using `langdetect.detect`.

Duplicate / copy-file pattern
- The `components/` folder contains several files with `Copy` or `Copy (1)` in their names. Examples:
  - `components/Copy (1) config_db.py`
  - `components/Copy (1) ioagent - Copy.py`
  - `components/Copy (1) langagent - Copy.py`
  - `components/dbagent - Copy.py`
  - `components/googleagent - Copy.py`
- Treat these as intentionally retained artifacts. Do NOT rename or delete them without the repo owner's explicit approval. If you consolidate, update imports in `queryman.py` and other modules.

Security & secrets note
- `components/Copy (1) config_db.py` contains a hard-coded MongoDB password and host values. Treat this as a secret leak: do not commit real credentials, and rotate/remove them immediately. When running locally, prefer using environment variables or a secure vault.

Suggested quick tasks for maintainers
- Add a small `README.md` describing how `queryman.py` composes `components/` and which files are canonical versus duplicates.
- Add `tests/` with unit tests for `dbagent` (mock `pymongo`) and `ioagent` wrappers.
- Replace the hard-coded credentials with environment-variable loading and document the vars in `README.md`.

-- End of file
