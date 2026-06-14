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
    BackpackSchema,
    CampfireSchema,
    CastleWallSchema,
    ChestplateSchema,
    CookingPotSchema,
    DrawbridgeSchema,
    ForgeSchema,
    LanternSchema,
    MarketStallSchema,
    TentSchema,
    ThroneSchema,
    TowerSchema,
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
            "asset_type": "chestplate",
            "width": 58.0,
            "height": 72.0,
            "depth": 28.0,
            "material": "steel",
            "style": "knight",
        }, ChestplateSchema),
        ({
            "asset_type": "backpack",
            "width": 42.0,
            "depth": 22.0,
            "height": 56.0,
            "material": "canvas",
            "has_bedroll": True,
        }, BackpackSchema),
        ({
            "asset_type": "tent",
            "width": 240.0,
            "depth": 280.0,
            "height": 165.0,
            "material": "canvas",
            "tent_style": "ridge",
        }, TentSchema),
        ({
            "asset_type": "campfire",
            "width": 90.0,
            "depth": 90.0,
            "height": 34.0,
            "log_count": 5,
            "is_lit": True,
        }, CampfireSchema),
        ({
            "asset_type": "lantern",
            "width": 24.0,
            "depth": 18.0,
            "height": 42.0,
            "material": "iron",
            "is_lit": True,
        }, LanternSchema),
        ({
            "asset_type": "cooking_pot",
            "diameter": 38.0,
            "height": 28.0,
            "material": "iron",
            "has_lid": True,
        }, CookingPotSchema),
        ({
            "asset_type": "castle_wall",
            "width": 420.0,
            "thickness": 70.0,
            "height": 320.0,
            "material": "stone",
            "has_crenellations": True,
        }, CastleWallSchema),
        ({
            "asset_type": "tower",
            "diameter": 320.0,
            "height": 620.0,
            "material": "stone",
            "roof_style": "battlement",
        }, TowerSchema),
        ({
            "asset_type": "drawbridge",
            "width": 260.0,
            "length": 420.0,
            "thickness": 24.0,
            "material": "wood",
            "chain_count": 2,
        }, DrawbridgeSchema),
        ({
            "asset_type": "throne",
            "width": 105.0,
            "depth": 90.0,
            "height": 190.0,
            "material": "wood",
            "has_cushion": True,
        }, ThroneSchema),
        ({
            "asset_type": "market_stall",
            "width": 260.0,
            "depth": 180.0,
            "height": 250.0,
            "frame_material": "wood",
            "canopy_color": "striped",
        }, MarketStallSchema),
        ({
            "asset_type": "forge",
            "width": 220.0,
            "depth": 150.0,
            "height": 130.0,
            "material": "stone",
            "is_lit": True,
        }, ForgeSchema),
    ],
)
def test_validate_adventure_schemas(payload, expected_type):
    validated = validate_asset_params(payload)
    assert isinstance(validated, expected_type)


def test_repair_units_for_adventure_assets():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({}))

    repaired_tent = processor.repair_units({
        "asset_type": "tent",
        "width": 2.4,
        "depth": 2.8,
        "height": 1.65,
    })
    assert repaired_tent["width"] == 240.0
    assert repaired_tent["depth"] == 280.0
    assert repaired_tent["height"] == 165.0

    repaired_tower = processor.repair_units({
        "asset_type": "tower",
        "diameter": 3.2,
        "height": 6.2,
    })
    assert repaired_tower["diameter"] == 320.0
    assert repaired_tower["height"] == 620.0

    repaired_pot = processor.repair_units({
        "asset_type": "cooking_pot",
        "diameter": 0.38,
        "height": 0.28,
    })
    assert repaired_pot["diameter"] == 38.0
    assert repaired_pot["height"] == 28.0


@pytest.mark.parametrize(
    ("raw_payload", "prompt", "expected_type"),
    [
        ({"asset_type": "table", "width": 0.42, "depth": 0.22, "height": 0.56, "material": "canvas"}, "Canvas adventurer backpack with leather straps and a rolled bedroll on top", BackpackSchema),
        ({"asset_type": "torch", "width": 0.9, "depth": 0.9, "height": 0.34, "is_lit": True}, "Lit campfire with stacked logs and a stone ring", CampfireSchema),
        ({"asset_type": "wall", "width": 4.2, "height": 3.2, "thickness": 0.7, "material": "stone"}, "Stone castle wall section with crenellated battlements", CastleWallSchema),
        ({"asset_type": "bridge", "width": 2.6, "length": 4.2, "thickness": 0.24, "material": "wood"}, "Massive wooden drawbridge with iron chains and heavy plank decking", DrawbridgeSchema),
        ({"asset_type": "table", "width": 2.6, "depth": 1.8, "height": 2.5, "frame_material": "wood", "canopy_color": "striped"}, "Wooden medieval market stall with striped canopy and sturdy merchant counter", MarketStallSchema),
        ({"asset_type": "chimney", "width": 2.2, "depth": 1.5, "height": 1.3, "material": "stone", "is_lit": True}, "Stone blacksmith forge with a chimney hood and a hot burning coal bed", ForgeSchema),
    ],
)
def test_process_prompt_overrides_for_adventure_inference(raw_payload, prompt, expected_type):
    processor = PromptProcessor(ollama_client=DummyOllamaClient(raw_payload))
    params, generator_path = processor.process_prompt(prompt)
    assert isinstance(params, expected_type)
    assert generator_path.endswith("adventure_asset.py")


@pytest.mark.parametrize(
    ("asset_type", "params"),
    [
        ("chestplate", {
            "asset_type": "chestplate",
            "width": 58.0,
            "height": 72.0,
            "depth": 28.0,
            "material": "steel",
            "style": "knight",
        }),
        ("backpack", {
            "asset_type": "backpack",
            "width": 42.0,
            "depth": 22.0,
            "height": 56.0,
            "material": "canvas",
            "has_bedroll": True,
        }),
        ("tent", {
            "asset_type": "tent",
            "width": 240.0,
            "depth": 280.0,
            "height": 165.0,
            "material": "canvas",
            "tent_style": "ridge",
        }),
        ("lantern", {
            "asset_type": "lantern",
            "width": 24.0,
            "depth": 18.0,
            "height": 42.0,
            "material": "iron",
            "is_lit": True,
        }),
        ("castle_wall", {
            "asset_type": "castle_wall",
            "width": 420.0,
            "thickness": 70.0,
            "height": 320.0,
            "material": "stone",
            "has_crenellations": True,
        }),
        ("throne", {
            "asset_type": "throne",
            "width": 105.0,
            "depth": 90.0,
            "height": 190.0,
            "material": "wood",
            "has_cushion": True,
        }),
        ("cart", {
            "asset_type": "cart",
            "width": 170.0,
            "depth": 260.0,
            "height": 150.0,
            "material": "wood",
            "has_canopy": False,
        }),
        ("forge", {
            "asset_type": "forge",
            "width": 220.0,
            "depth": 150.0,
            "height": 130.0,
            "material": "stone",
            "is_lit": True,
        }),
    ],
)
def test_adventure_generator_smoke(asset_type, params):
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "adventure_asset.py")
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
