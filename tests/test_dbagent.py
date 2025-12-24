import sys
import types
import importlib.util
from pathlib import Path

import mongomock


def _load_component_module(module_name: str, file_path: Path):
    """Load a components.* module from file path into sys.modules."""
    # Ensure package module exists
    pkg_name = "components"
    components_dir = str(file_path.parent)
    if pkg_name not in sys.modules:
        pkg = types.ModuleType(pkg_name)
        pkg.__path__ = [components_dir]
        sys.modules[pkg_name] = pkg

    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_dbagent_insert_and_find():
    base = Path(__file__).resolve().parent.parent
    components_dir = base / "components"
    config_path = components_dir / "Copy (1) config_db.py"
    dbagent_path = components_dir / "dbagent - Copy.py"

    # Load config and dbagent as package modules
    config_mod = _load_component_module("components.config_db", config_path)
    db_mod = _load_component_module("components.dbagent", dbagent_path)

    # Replace db_core with mongomock client
    mock_client = mongomock.MongoClient()

    def _mock_db_core():
        return mock_client

    db_mod.db_core = _mock_db_core

    # Ensure dbagent uses a test db name
    db_mod.mongodb_dbname = "test_spade_db"

    # Insert a document using the dbagent helper
    inserted_id = db_mod.db_insertone("queries", {"URL": "http://example", "Title": "Example", "Timestamp": 1})
    assert inserted_id is not None

    # Find the inserted document
    found = db_mod.db_findone("queries", {"URL": "http://example"})
    assert found and found.get("Title") == "Example"


def test_dbagent_findmany_and_update():
    base = Path(__file__).resolve().parent.parent
    components_dir = base / "components"
    dbagent_path = components_dir / "dbagent - Copy.py"

    db_mod = sys.modules.get("components.dbagent")
    if db_mod is None:
        db_mod = _load_component_module("components.dbagent", dbagent_path)

    # Ensure db_core still returns mongomock from prior test run
    mock_client = mongomock.MongoClient()

    def _mock_db_core():
        return mock_client

    db_mod.db_core = _mock_db_core
    db_mod.mongodb_dbname = "test_spade_db"

    # Seed multiple docs
    docs = [{"q": i} for i in range(5)]
    for d in docs:
        db_mod.db_insertone("many", d)

    results = db_mod.db_findmany("many", {})
    assert isinstance(results, list)
    assert len(results) == 5

    # Update one
    res = db_mod.db_updateone("many", {"q": 0}, {"$set": {"q": 999}})
    assert res is not None
