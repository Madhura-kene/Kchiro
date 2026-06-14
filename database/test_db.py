import os
import sys
import tempfile
import pytest

# Dynamic path resolution to find database package
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) # Project root folder
if project_root not in sys.path:
    sys.path.append(project_root)

from database.db import DatabaseManager

@pytest.fixture
def temp_db():
    # Setup temporary database file
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db = DatabaseManager(db_path=path)
    yield db
    # Teardown
    if os.path.exists(path):
        os.remove(path)

def test_create_and_get_asset(temp_db):
    prompt = "Create a fancy medieval sword"
    params = {"blade_length": 90, "hilt_type": "crossguard"}
    
    asset_id = temp_db.create_asset(prompt, "sword", params)
    assert asset_id > 0
    
    asset = temp_db.get_asset(asset_id)
    assert asset is not None
    assert asset["prompt"] == prompt
    assert asset["asset_type"] == "sword"
    assert asset["parameters"] == params
    assert asset["status"] == "generating"

def test_update_status(temp_db):
    prompt = "Create a table"
    params = {"width": 120}
    asset_id = temp_db.create_asset(prompt, "table", params)
    
    # Success update
    temp_db.update_asset_success(asset_id, "exports/table_1.glb", "renders/table_1.png")
    asset = temp_db.get_asset(asset_id)
    assert asset["status"] == "completed"
    assert asset["glb_path"] == "exports/table_1.glb"
    assert asset["render_path"] == "renders/table_1.png"
    assert asset["error_message"] is None
    
    # Fail update on another asset
    asset_id_2 = temp_db.create_asset(prompt, "table", params)
    temp_db.update_asset_failed(asset_id_2, "Failed to build table leg")
    asset_2 = temp_db.get_asset(asset_id_2)
    assert asset_2["status"] == "failed"
    assert asset_2["error_message"] == "Failed to build table leg"

def test_get_all_and_delete(temp_db):
    temp_db.create_asset("Sword 1", "sword", {})
    temp_db.create_asset("Sword 2", "sword", {})
    
    assets = temp_db.get_assets()
    assert len(assets) == 2
    
    # Delete one
    deleted = temp_db.delete_asset(assets[0]["id"])
    assert deleted is True
    
    assets_after = temp_db.get_assets()
    assert len(assets_after) == 1
