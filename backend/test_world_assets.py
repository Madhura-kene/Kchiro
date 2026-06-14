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
    AirlockSchema,
    ArtifactSchema,
    BattleTankSchema,
    BusStopSchema,
    CarSchema,
    CoinSchema,
    ControlPanelSchema,
    DogSchema,
    GeneratorSchema,
    GameBackground2DSchema,
    MerchantSchema,
    PipeSchema,
    PhoneBoothSchema,
    TerrainSchema,
    TrafficLightSchema,
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
            "asset_type": "control_panel",
            "width": 140.0,
            "depth": 80.0,
            "height": 110.0,
            "material": "darksteel",
            "accent_color": "cyan",
            "screen_count": 4,
        }, ControlPanelSchema),
        ({
            "asset_type": "airlock",
            "width": 220.0,
            "depth": 280.0,
            "height": 250.0,
            "material": "steel",
            "accent_color": "blue",
            "door_count": 2,
            "has_control_panel": True,
        }, AirlockSchema),
        ({
            "asset_type": "generator",
            "width": 180.0,
            "depth": 120.0,
            "height": 140.0,
            "material": "darksteel",
            "accent_color": "yellow",
        }, GeneratorSchema),
        ({
            "asset_type": "car",
            "width": 180.0,
            "depth": 420.0,
            "height": 155.0,
            "body_style": "sedan",
            "body_color": "red",
        }, CarSchema),
        ({
            "asset_type": "battle_tank",
            "width": 320.0,
            "depth": 640.0,
            "height": 220.0,
            "body_color": "olive",
            "turret_style": "angular",
        }, BattleTankSchema),
        ({
            "asset_type": "merchant",
            "width": 58.0,
            "depth": 40.0,
            "height": 176.0,
            "skin_tone": "medium",
            "outfit_color": "green",
        }, MerchantSchema),
        ({
            "asset_type": "dog",
            "width": 46.0,
            "depth": 90.0,
            "height": 62.0,
            "fur_color": "brown",
        }, DogSchema),
        ({
            "asset_type": "coin",
            "width": 4.0,
            "depth": 4.0,
            "height": 0.4,
        }, CoinSchema),
        ({
            "asset_type": "artifact",
            "width": 34.0,
            "depth": 34.0,
            "height": 72.0,
            "artifact_style": "obelisk",
        }, ArtifactSchema),
        ({
            "asset_type": "terrain",
            "width": 500.0,
            "depth": 500.0,
            "height": 90.0,
            "material": "grass",
        }, TerrainSchema),
        ({
            "asset_type": "traffic_light",
            "width": 46.0,
            "depth": 36.0,
            "height": 320.0,
            "material": "darksteel",
            "active_light": "green",
            "orientation": "vertical",
        }, TrafficLightSchema),
        ({
            "asset_type": "bus_stop",
            "width": 280.0,
            "depth": 120.0,
            "height": 240.0,
            "material": "steel",
            "has_bench": True,
        }, BusStopSchema),
        ({
            "asset_type": "phone_booth",
            "width": 120.0,
            "depth": 120.0,
            "height": 240.0,
            "material": "mail_red",
            "booth_style": "classic",
            "accent_color": "white",
        }, PhoneBoothSchema),
        ({
            "asset_type": "game_background_2d",
            "width": 1400.0,
            "depth": 36.0,
            "height": 800.0,
            "theme": "city",
            "time_of_day": "night",
            "layer_count": 5,
            "has_celestial": True,
        }, GameBackground2DSchema),
    ],
)
def test_validate_world_schemas(payload, expected_type):
    validated = validate_asset_params(payload)
    assert isinstance(validated, expected_type)


def test_repair_units_for_world_assets():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({}))

    repaired_pipe = processor.repair_units({
        "asset_type": "pipe",
        "diameter": 0.3,
        "length": 2.2,
    })
    assert repaired_pipe["diameter"] == 30.0
    assert repaired_pipe["length"] == 220.0

    repaired_car = processor.repair_units({
        "asset_type": "car",
        "width": 1.8,
        "depth": 4.2,
        "height": 1.55,
    })
    assert repaired_car["width"] == 180.0
    assert repaired_car["depth"] == 420.0
    assert repaired_car["height"] == 155.0

    repaired_terrain = processor.repair_units({
        "asset_type": "terrain",
        "width": 5.0,
        "depth": 5.0,
        "height": 0.9,
    })
    assert repaired_terrain["width"] == 500.0
    assert repaired_terrain["depth"] == 500.0
    assert repaired_terrain["height"] == 90.0


@pytest.mark.parametrize(
    ("raw_payload", "prompt", "expected_asset_type"),
    [
        ({"asset_type": "crate", "width": 1.0, "depth": 0.7, "height": 0.7}, "Futuristic tech crate with armored panels and blue light strips", "tech_crate"),
        ({"asset_type": "bench", "width": 1.4, "depth": 0.52, "height": 0.88}, "Urban street bench with wood slats and dark steel frame", "street_bench"),
        ({"asset_type": "table", "width": 1.8, "depth": 4.2, "height": 1.55}, "Modern red sedan car with glass windows and four wheels", "car"),
        ({"asset_type": "tank", "diameter": 1.6, "height": 2.6}, "Armored military battle tank with olive body and angular turret", "battle_tank"),
        ({"asset_type": "chair", "width": 0.58, "depth": 0.4, "height": 1.76}, "Merchant character with green clothes, hat, and pouch", "merchant"),
        ({"asset_type": "vase", "height": 0.28, "diameter": 0.12, "style": "modern", "material": "glass"}, "Blue potion bottle with glass body and cork stopper", "potion"),
        ({"asset_type": "rug", "width": 2.0, "depth": 2.0, "thickness": 1.0, "shape": "rectangular", "pattern": "solid"}, "Dungeon tile made of stone blocks with dark grooves", "dungeon_tile"),
        ({"asset_type": "terrain", "width": 5.0, "depth": 5.0, "height": 0.9}, "2D game background with a neon city skyline, glowing windows, rooftop antennas, and a moonlit night sky", "game_background_2d"),
    ],
)
def test_process_prompt_world_inference(raw_payload, prompt, expected_asset_type):
    processor = PromptProcessor(ollama_client=DummyOllamaClient(raw_payload))
    params, generator_path = processor.process_prompt(prompt)
    assert params.asset_type == expected_asset_type
    assert generator_path.endswith("world_asset.py")


@pytest.mark.parametrize(
    ("asset_type", "params"),
    [
        ("control_panel", {
            "asset_type": "control_panel",
            "width": 140.0,
            "depth": 80.0,
            "height": 110.0,
            "material": "darksteel",
            "accent_color": "cyan",
            "screen_count": 4,
        }),
        ("car", {
            "asset_type": "car",
            "width": 180.0,
            "depth": 420.0,
            "height": 155.0,
            "body_style": "sedan",
            "body_color": "red",
        }),
        ("drone", {
            "asset_type": "drone",
            "width": 90.0,
            "depth": 90.0,
            "height": 36.0,
            "material": "plastic_dark",
            "accent_color": "cyan",
            "drone_style": "quad",
        }),
        ("plane", {
            "asset_type": "plane",
            "width": 1200.0,
            "depth": 900.0,
            "height": 260.0,
            "plane_style": "jet",
            "body_color": "white",
            "accent_color": "blue",
        }),
        ("helicopter", {
            "asset_type": "helicopter",
            "width": 320.0,
            "depth": 820.0,
            "height": 300.0,
            "body_color": "gray",
            "accent_color": "red",
            "has_skids": True,
        }),
        ("merchant", {
            "asset_type": "merchant",
            "width": 58.0,
            "depth": 40.0,
            "height": 176.0,
            "skin_tone": "medium",
            "outfit_color": "green",
        }),
        ("horse", {
            "asset_type": "horse",
            "width": 80.0,
            "depth": 180.0,
            "height": 160.0,
            "fur_color": "brown",
        }),
        ("dragon", {
            "asset_type": "dragon",
            "width": 260.0,
            "depth": 520.0,
            "height": 240.0,
            "scale_color": "green",
            "pose": "standing",
        }),
        ("coin", {
            "asset_type": "coin",
            "width": 4.0,
            "depth": 4.0,
            "height": 0.4,
        }),
        ("terrain", {
            "asset_type": "terrain",
            "width": 500.0,
            "depth": 500.0,
            "height": 90.0,
            "material": "grass",
        }),
        ("phone_booth", {
            "asset_type": "phone_booth",
            "width": 120.0,
            "depth": 120.0,
            "height": 240.0,
            "material": "mail_red",
            "booth_style": "classic",
            "accent_color": "white",
        }),
        ("game_background_2d", {
            "asset_type": "game_background_2d",
            "width": 1400.0,
            "depth": 36.0,
            "height": 800.0,
            "theme": "forest",
            "time_of_day": "sunset",
            "layer_count": 5,
            "has_celestial": True,
        }),
    ],
)
def test_world_generator_smoke(asset_type, params):
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "world_asset.py")
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
