import os
import sys

import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.blender_executor import BlenderExecutor
from backend.prompt_processor import PromptProcessor
from schemas.asset_schemas import OakTreeSchema, RiverSegmentSchema, WaterfallSchema, validate_asset_params


class DummyOllamaClient:
    def __init__(self, payload):
        self.payload = payload

    def generate_json_spec(self, _prompt):
        return dict(self.payload)


def test_validate_nature_schemas():
    oak = validate_asset_params({
        "asset_type": "oak_tree",
        "height": 600.0,
        "canopy_width": 430.0,
        "trunk_radius": 24.0,
    })
    assert isinstance(oak, OakTreeSchema)

    waterfall = validate_asset_params({
        "asset_type": "waterfall",
        "width": 180.0,
        "height": 280.0,
        "pool_radius": 140.0,
    })
    assert isinstance(waterfall, WaterfallSchema)


def test_repair_units_for_nature_assets():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({}))
    repaired = processor.repair_units({
        "asset_type": "river_segment",
        "width": 1.6,
        "length": 3.4,
        "curve": 0.6,
    })
    assert repaired["width"] == 160.0
    assert repaired["length"] == 340.0
    assert repaired["curve"] == 60.0


def test_repair_units_coerces_nature_descriptors_and_ranges():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({}))
    repaired = processor.repair_units({
        "asset_type": "grass",
        "height": "30.0 to 60.0 cm",
        "density": "dense",
    }, "Dense grass patch with natural green blades")

    assert repaired["height"] == 45.0
    assert repaired["density"] == 50


def test_repair_units_clamps_small_moss_values_without_meter_blowup():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({}))
    repaired = processor.repair_units({
        "asset_type": "moss",
        "width": 30.0,
        "depth": 10.0,
        "thickness": 2.0,
    }, "Soft moss patch")

    assert repaired["width"] == 40.0
    assert repaired["depth"] == 30.0
    assert repaired["thickness"] == 4.0


def test_process_prompt_overrides_old_asset_type_for_nature():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({
        "asset_type": "table",
        "height": 6.0,
        "canopy_width": 4.2,
        "trunk_radius": 0.24,
    }))

    params, generator_path = processor.process_prompt("Oak tree with a broad canopy and thick trunk")

    assert isinstance(params, OakTreeSchema)
    assert params.height == 600.0
    assert params.canopy_width == 420.0
    assert params.trunk_radius == 24.0
    assert generator_path.endswith("nature_asset.py")


def test_process_prompt_validates_grass_with_descriptor_payload():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({
        "asset_type": "grass",
        "height": "30.0 to 60.0 cm",
        "density": "dense",
    }))

    params, generator_path = processor.process_prompt("Dense grass patch with natural green blades")

    assert params.asset_type == "grass"
    assert params.height == 45.0
    assert params.density == 50
    assert generator_path.endswith("nature_asset.py")


def test_process_prompt_validates_moss_with_small_values():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({
        "asset_type": "moss",
        "width": 30.0,
        "depth": 10.0,
        "thickness": 2.0,
    }))

    params, generator_path = processor.process_prompt("Soft moss patch")

    assert params.asset_type == "moss"
    assert params.width == 40.0
    assert params.depth == 30.0
    assert params.thickness == 4.0
    assert generator_path.endswith("nature_asset.py")


@pytest.mark.parametrize(
    ("asset_type", "params"),
    [
        ("oak_tree", {
            "asset_type": "oak_tree",
            "height": 560.0,
            "canopy_width": 420.0,
            "trunk_radius": 22.0,
        }),
        ("rock_cluster", {
            "asset_type": "rock_cluster",
            "width": 180.0,
            "depth": 120.0,
            "rocks": 5,
        }),
        ("waterfall", {
            "asset_type": "waterfall",
            "width": 160.0,
            "height": 260.0,
            "pool_radius": 120.0,
        }),
    ],
)
def test_nature_generator_smoke(asset_type, params):
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "nature_asset.py")
    export_path = os.path.join(project_root, "exports", f"test_{asset_type}.glb")
    render_path = os.path.join(project_root, "renders", f"test_{asset_type}.png")

    for path in (export_path, render_path):
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

    success, logs = executor.execute_generator(
        generator_script=generator_script,
        params=params,
        export_path=export_path,
        render_path=render_path,
        timeout_seconds=120,
    )

    assert success, f"{asset_type} generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), f"{asset_type} GLB export failed"
    assert os.path.exists(render_path), f"{asset_type} preview render failed"

    for path in (export_path, render_path):
        if os.path.exists(path):
            os.remove(path)
