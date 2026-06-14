import os
import sys

import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.blender_executor import BlenderExecutor
from backend.prompt_processor import PromptProcessor
from schemas.asset_schemas import (
    ArrowSchema,
    BoltSchema,
    BowSchema,
    CrossbowSchema,
    DaggerSchema,
    HalberdSchema,
    HammerSchema,
    MagicStaffSchema,
    MaceSchema,
    OrbSchema,
    SpearSchema,
    StaffSchema,
    SwordSchema,
    WandSchema,
    validate_asset_params,
)


class DummyOllamaClient:
    def __init__(self, payload):
        self.payload = payload

    def generate_json_spec(self, _prompt):
        return dict(self.payload)


@pytest.mark.parametrize(
    ("payload", "expected_type"),
    [
        ({
            "asset_type": "sword",
            "blade_length": 92.0,
            "blade_width": 5.2,
            "grip_length": 16.0,
            "crossguard_type": "simple",
            "grip_material": "leather",
        }, SwordSchema),
        ({
            "asset_type": "dagger",
            "blade_length": 36.0,
            "blade_width": 3.2,
            "grip_length": 10.0,
            "crossguard_type": "curved",
            "grip_material": "wood",
        }, DaggerSchema),
        ({
            "asset_type": "hammer",
            "handle_length": 92.0,
            "head_width": 24.0,
            "head_height": 14.0,
            "head_material": "steel",
            "handle_material": "wood",
        }, HammerSchema),
        ({
            "asset_type": "mace",
            "shaft_length": 88.0,
            "head_radius": 11.0,
            "flange_count": 6,
            "shaft_material": "wood",
            "head_material": "iron",
        }, MaceSchema),
        ({
            "asset_type": "spear",
            "shaft_length": 240.0,
            "tip_length": 42.0,
            "shaft_material": "wood",
            "tip_material": "steel",
        }, SpearSchema),
        ({
            "asset_type": "halberd",
            "shaft_length": 260.0,
            "blade_size": 48.0,
            "hook_size": 22.0,
            "shaft_material": "wood",
            "head_material": "steel",
        }, HalberdSchema),
        ({
            "asset_type": "staff",
            "height": 190.0,
            "shaft_radius": 2.5,
            "material": "wood",
            "tip_style": "ring",
        }, StaffSchema),
        ({
            "asset_type": "bow",
            "height": 170.0,
            "width": 56.0,
            "material": "wood",
            "bow_style": "recurve",
        }, BowSchema),
        ({
            "asset_type": "crossbow",
            "width": 82.0,
            "stock_length": 96.0,
            "material": "wood",
            "has_bolt": True,
        }, CrossbowSchema),
        ({
            "asset_type": "arrow",
            "length": 78.0,
            "shaft_radius": 1.0,
            "shaft_material": "wood",
            "tip_material": "steel",
            "fletching_color": "white",
        }, ArrowSchema),
        ({
            "asset_type": "bolt",
            "length": 34.0,
            "shaft_radius": 1.3,
            "shaft_material": "wood",
            "tip_material": "steel",
            "fletching_color": "black",
        }, BoltSchema),
        ({
            "asset_type": "magic_staff",
            "height": 210.0,
            "shaft_material": "darkwood",
            "gem_color": "blue",
            "head_style": "orb",
        }, MagicStaffSchema),
        ({
            "asset_type": "wand",
            "length": 32.0,
            "shaft_material": "wood",
            "tip_style": "gem",
            "gem_color": "purple",
        }, WandSchema),
        ({
            "asset_type": "orb",
            "diameter": 24.0,
            "orb_material": "crystal",
            "glow_color": "blue",
            "has_stand": True,
        }, OrbSchema),
    ],
)
def test_validate_weapon_schemas(payload, expected_type):
    validated = validate_asset_params(payload)
    assert isinstance(validated, expected_type)


def test_repair_units_for_weapon_assets():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({}))
    repaired = processor.repair_units({
        "asset_type": "dagger",
        "blade_length": 0.42,
        "grip_length": 0.11,
    })
    assert repaired["blade_length"] == 42.0
    assert repaired["grip_length"] == 11.0

    repaired_bow = processor.repair_units({
        "asset_type": "bow",
        "height": 1.7,
        "width": 0.56,
    })
    assert repaired_bow["height"] == 170.0
    assert repaired_bow["width"] == 56.0

    repaired_halberd = processor.repair_units({
        "asset_type": "halberd",
        "shaft_length": 2.6,
        "blade_size": 0.48,
        "hook_size": 0.22,
    })
    assert repaired_halberd["shaft_length"] == 260.0
    assert repaired_halberd["blade_size"] == 48.0
    assert repaired_halberd["hook_size"] == 22.0


@pytest.mark.parametrize(
    ("raw_payload", "prompt", "expected_type"),
    [
        ({"asset_type": "table", "blade_length": 0.38, "grip_length": 0.1}, "Slim steel dagger with short guard", DaggerSchema),
        ({"asset_type": "arrow", "length": 0.34, "fletching_color": "black"}, "Short crossbow bolt with black fletching", BoltSchema),
        ({"asset_type": "torch", "height": 2.1, "gem_color": "red"}, "Arcane magic staff with a red crystal head", MagicStaffSchema),
        ({"asset_type": "sword", "width": 0.56, "height": 1.7}, "Recurve bow with curved wood limbs", BowSchema),
    ],
)
def test_process_prompt_overrides_for_weapon_inference(raw_payload, prompt, expected_type):
    processor = PromptProcessor(ollama_client=DummyOllamaClient(raw_payload))
    params, generator_path = processor.process_prompt(prompt)
    assert isinstance(params, expected_type)
    assert generator_path.endswith("weapon_asset.py")


@pytest.mark.parametrize(
    ("asset_type", "params"),
    [
        ("sword", {
            "asset_type": "sword",
            "blade_length": 96.0,
            "blade_width": 5.2,
            "grip_length": 16.0,
            "crossguard_type": "simple",
            "grip_material": "leather",
        }),
        ("dagger", {
            "asset_type": "dagger",
            "blade_length": 36.0,
            "blade_width": 3.2,
            "grip_length": 10.0,
            "crossguard_type": "curved",
            "grip_material": "wood",
        }),
        ("hammer", {
            "asset_type": "hammer",
            "handle_length": 94.0,
            "head_width": 24.0,
            "head_height": 14.0,
            "head_material": "steel",
            "handle_material": "wood",
        }),
        ("halberd", {
            "asset_type": "halberd",
            "shaft_length": 260.0,
            "blade_size": 50.0,
            "hook_size": 22.0,
            "shaft_material": "wood",
            "head_material": "steel",
        }),
        ("bow", {
            "asset_type": "bow",
            "height": 170.0,
            "width": 58.0,
            "material": "wood",
            "bow_style": "recurve",
        }),
        ("crossbow", {
            "asset_type": "crossbow",
            "width": 84.0,
            "stock_length": 98.0,
            "material": "wood",
            "has_bolt": True,
        }),
        ("magic_staff", {
            "asset_type": "magic_staff",
            "height": 210.0,
            "shaft_material": "darkwood",
            "gem_color": "blue",
            "head_style": "orb",
        }),
        ("orb", {
            "asset_type": "orb",
            "diameter": 24.0,
            "orb_material": "crystal",
            "glow_color": "blue",
            "has_stand": True,
        }),
        ("arrow", {
            "asset_type": "arrow",
            "length": 78.0,
            "shaft_radius": 1.0,
            "shaft_material": "wood",
            "tip_material": "steel",
            "fletching_color": "white",
        }),
    ],
)
def test_weapon_generator_smoke(asset_type, params):
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "weapon_asset.py")
    export_path = os.path.join(project_root, "exports", f"test_{asset_type}.glb")

    if os.path.exists(export_path):
        try:
            os.remove(export_path)
        except Exception:
            pass

    success, logs = executor.execute_generator(
        generator_script=generator_script,
        params=params,
        export_path=export_path,
        render_path=None,
        timeout_seconds=120,
    )

    assert success, f"{asset_type} generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), f"{asset_type} GLB export failed"

    if os.path.exists(export_path):
        os.remove(export_path)
