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
    ArchwaySchema,
    BalconySchema,
    BridgeSchema,
    ChimneySchema,
    DoorSchema,
    FenceSchema,
    FoundationSchema,
    GateSchema,
    LadderSchema,
    PillarSchema,
    PorchSchema,
    RailingSchema,
    RampSchema,
    RoofSchema,
    StairsSchema,
    WallSchema,
    WindowSchema,
    validate_asset_params,
)


class DummyOllamaClient:
    def __init__(self, payload):
        self.payload = payload

    def generate_json_spec(self, _prompt):
        return dict(self.payload)


def test_validate_architecture_schemas():
    foundation = validate_asset_params({
        "asset_type": "foundation",
        "width": 860.0,
        "depth": 620.0,
        "height": 80.0,
        "footing_depth": 140.0,
        "material": "concrete",
        "has_footings": True,
    })
    assert isinstance(foundation, FoundationSchema)

    wall = validate_asset_params({
        "asset_type": "wall",
        "width": 360.0,
        "height": 300.0,
        "thickness": 20.0,
        "material": "brick",
        "opening_type": "door",
        "opening_width": 110.0,
        "opening_height": 220.0,
        "has_trim": True,
    })
    assert isinstance(wall, WallSchema)

    roof = validate_asset_params({
        "asset_type": "roof",
        "width": 640.0,
        "depth": 480.0,
        "thickness": 18.0,
        "slope": 34.0,
        "roof_style": "gabled",
        "overhang": 40.0,
        "material": "clay_tiles",
    })
    assert isinstance(roof, RoofSchema)

    door = validate_asset_params({
        "asset_type": "door",
        "width": 95.0,
        "height": 210.0,
        "thickness": 4.5,
        "material": "wood",
        "panel_style": "inset",
        "has_frame": True,
        "has_handle": True,
    })
    assert isinstance(door, DoorSchema)

    window = validate_asset_params({
        "asset_type": "window",
        "width": 150.0,
        "height": 120.0,
        "thickness": 12.0,
        "frame_material": "aluminum",
        "has_mullions": True,
        "has_sill": True,
    })
    assert isinstance(window, WindowSchema)

    archway = validate_asset_params({
        "asset_type": "archway",
        "width": 220.0,
        "height": 280.0,
        "thickness": 28.0,
        "support_width": 32.0,
        "material": "stone",
    })
    assert isinstance(archway, ArchwaySchema)

    gate = validate_asset_params({
        "asset_type": "gate",
        "width": 240.0,
        "height": 180.0,
        "thickness": 8.0,
        "material": "iron",
        "gate_style": "barred",
        "bar_count": 9,
    })
    assert isinstance(gate, GateSchema)

    stairs = validate_asset_params({
        "asset_type": "stairs",
        "width": 120.0,
        "step_count": 8,
        "step_height": 17.0,
        "step_depth": 28.0,
        "material": "wood",
        "has_railing": True,
    })
    assert isinstance(stairs, StairsSchema)

    ladder = validate_asset_params({
        "asset_type": "ladder",
        "width": 50.0,
        "height": 260.0,
        "rung_count": 8,
        "material": "wood",
    })
    assert isinstance(ladder, LadderSchema)

    ramp = validate_asset_params({
        "asset_type": "ramp",
        "width": 140.0,
        "depth": 320.0,
        "height": 55.0,
        "slope": 12.0,
        "material": "concrete",
        "has_side_curbs": True,
    })
    assert isinstance(ramp, RampSchema)

    bridge = validate_asset_params({
        "asset_type": "bridge",
        "length": 900.0,
        "width": 220.0,
        "height": 180.0,
        "deck_thickness": 24.0,
        "material": "wood",
        "support_count": 4,
        "has_railings": True,
    })
    assert isinstance(bridge, BridgeSchema)

    balcony = validate_asset_params({
        "asset_type": "balcony",
        "width": 320.0,
        "depth": 160.0,
        "height": 105.0,
        "thickness": 18.0,
        "material": "concrete",
        "has_railings": True,
    })
    assert isinstance(balcony, BalconySchema)

    fence = validate_asset_params({
        "asset_type": "fence",
        "width": 420.0,
        "height": 160.0,
        "thickness": 10.0,
        "material": "wood",
        "fence_style": "picket",
        "section_count": 10,
    })
    assert isinstance(fence, FenceSchema)

    railing = validate_asset_params({
        "asset_type": "railing",
        "width": 280.0,
        "height": 105.0,
        "depth": 14.0,
        "material": "steel",
        "baluster_count": 8,
    })
    assert isinstance(railing, RailingSchema)

    chimney = validate_asset_params({
        "asset_type": "chimney",
        "width": 90.0,
        "depth": 90.0,
        "height": 240.0,
        "material": "brick",
        "has_cap": True,
    })
    assert isinstance(chimney, ChimneySchema)

    porch = validate_asset_params({
        "asset_type": "porch",
        "width": 360.0,
        "depth": 220.0,
        "height": 260.0,
        "material": "wood",
        "pillar_count": 4,
        "has_steps": True,
    })
    assert isinstance(porch, PorchSchema)


def test_repair_units_for_architecture_assets():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({}))
    repaired = processor.repair_units({
        "asset_type": "foundation",
        "width": 7.2,
        "depth": 5.6,
        "height": 0.7,
        "footing_depth": 1.2,
    })
    assert repaired["width"] == 720.0
    assert repaired["depth"] == 560.0
    assert repaired["height"] == 70.0
    assert repaired["footing_depth"] == 120.0

    repaired_stairs = processor.repair_units({
        "asset_type": "stairs",
        "width": 1.2,
        "step_height": 0.17,
        "step_depth": 0.28,
    })
    assert repaired_stairs["width"] == 120.0
    assert repaired_stairs["step_height"] == 17.0
    assert repaired_stairs["step_depth"] == 28.0

    repaired_bridge = processor.repair_units({
        "asset_type": "bridge",
        "length": 9.0,
        "width": 2.2,
        "height": 1.8,
        "deck_thickness": 0.24,
    })
    assert repaired_bridge["length"] == 900.0
    assert repaired_bridge["width"] == 220.0
    assert repaired_bridge["height"] == 180.0
    assert repaired_bridge["deck_thickness"] == 24.0


def test_repair_units_applies_architecture_prompt_overrides():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({}))
    repaired = processor.repair_units({
        "asset_type": "wall",
        "material": "plaster",
        "opening_type": "none",
        "has_trim": False,
    }, "Brick wall section with plaster trim and a centered window opening")

    assert repaired["material"] == "brick"
    assert repaired["opening_type"] == "window"
    assert repaired["has_trim"] is True


def test_process_prompt_overrides_old_asset_type_for_architecture():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({
        "asset_type": "table",
        "height": 3.2,
        "width": 0.45,
        "shape": "cylindrical",
        "material": "marble",
        "has_capital": True,
    }))

    params, generator_path = processor.process_prompt("Marble pillar with a cylindrical shaft and decorative capital")

    assert isinstance(params, PillarSchema)
    assert params.height == 320.0
    assert params.width == 45.0
    assert generator_path.endswith("architecture_asset.py")


def test_process_prompt_overrides_old_asset_type_for_stairs():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({
        "asset_type": "table",
        "width": 1.2,
        "step_count": 9,
        "step_height": 0.17,
        "step_depth": 0.28,
        "material": "concrete",
        "has_railing": True,
    }))

    params, generator_path = processor.process_prompt("Concrete staircase with nine even steps and a side railing")

    assert isinstance(params, StairsSchema)
    assert params.width == 120.0
    assert params.step_height == 17.0
    assert params.step_depth == 28.0
    assert generator_path.endswith("architecture_asset.py")


def test_process_prompt_overrides_old_asset_type_for_bridge():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({
        "asset_type": "table",
        "length": 9.0,
        "width": 2.4,
        "height": 2.0,
        "deck_thickness": 0.24,
        "material": "wood",
        "support_count": 4,
        "has_railings": True,
    }))

    params, generator_path = processor.process_prompt("Long wooden bridge with support pillars and side railings")

    assert isinstance(params, BridgeSchema)
    assert params.length == 900.0
    assert params.width == 240.0
    assert params.height == 200.0
    assert generator_path.endswith("architecture_asset.py")


def test_process_prompt_overrides_old_asset_type_for_porch():
    processor = PromptProcessor(ollama_client=DummyOllamaClient({
        "asset_type": "roof",
        "width": 3.6,
        "depth": 2.2,
        "height": 2.6,
        "material": "wood",
        "pillar_count": 4,
        "has_steps": True,
    }))

    params, generator_path = processor.process_prompt("Covered front porch with a platform, support pillars, roof, and entry steps")

    assert isinstance(params, PorchSchema)
    assert params.width == 360.0
    assert params.depth == 220.0
    assert params.height == 260.0
    assert generator_path.endswith("architecture_asset.py")


@pytest.mark.parametrize(
    ("asset_type", "params"),
    [
        ("wall", {
            "asset_type": "wall",
            "width": 360.0,
            "height": 290.0,
            "thickness": 18.0,
            "material": "brick",
            "opening_type": "window",
            "opening_width": 120.0,
            "opening_height": 110.0,
            "has_trim": True,
        }),
        ("roof", {
            "asset_type": "roof",
            "width": 620.0,
            "depth": 440.0,
            "thickness": 18.0,
            "slope": 35.0,
            "roof_style": "hip",
            "overhang": 36.0,
            "material": "clay_tiles",
        }),
        ("pillar", {
            "asset_type": "pillar",
            "height": 320.0,
            "width": 42.0,
            "shape": "cylindrical",
            "material": "stone",
            "has_capital": True,
        }),
        ("foundation", {
            "asset_type": "foundation",
            "width": 840.0,
            "depth": 620.0,
            "height": 80.0,
            "footing_depth": 140.0,
            "material": "concrete",
            "has_footings": True,
        }),
        ("door", {
            "asset_type": "door",
            "width": 95.0,
            "height": 210.0,
            "thickness": 4.5,
            "material": "wood",
            "panel_style": "inset",
            "has_frame": True,
            "has_handle": True,
        }),
        ("window", {
            "asset_type": "window",
            "width": 150.0,
            "height": 120.0,
            "thickness": 12.0,
            "frame_material": "aluminum",
            "has_mullions": True,
            "has_sill": True,
        }),
        ("archway", {
            "asset_type": "archway",
            "width": 220.0,
            "height": 280.0,
            "thickness": 28.0,
            "support_width": 34.0,
            "material": "stone",
        }),
        ("gate", {
            "asset_type": "gate",
            "width": 240.0,
            "height": 190.0,
            "thickness": 8.0,
            "material": "iron",
            "gate_style": "barred",
            "bar_count": 8,
        }),
        ("stairs", {
            "asset_type": "stairs",
            "width": 130.0,
            "step_count": 8,
            "step_height": 17.0,
            "step_depth": 28.0,
            "material": "wood",
            "has_railing": True,
        }),
        ("ladder", {
            "asset_type": "ladder",
            "width": 50.0,
            "height": 260.0,
            "rung_count": 8,
            "material": "wood",
        }),
        ("ramp", {
            "asset_type": "ramp",
            "width": 140.0,
            "depth": 320.0,
            "height": 55.0,
            "slope": 12.0,
            "material": "concrete",
            "has_side_curbs": True,
        }),
        ("bridge", {
            "asset_type": "bridge",
            "length": 900.0,
            "width": 220.0,
            "height": 180.0,
            "deck_thickness": 24.0,
            "material": "wood",
            "support_count": 4,
            "has_railings": True,
        }),
        ("balcony", {
            "asset_type": "balcony",
            "width": 320.0,
            "depth": 160.0,
            "height": 105.0,
            "thickness": 18.0,
            "material": "concrete",
            "has_railings": True,
        }),
        ("fence", {
            "asset_type": "fence",
            "width": 420.0,
            "height": 160.0,
            "thickness": 10.0,
            "material": "wood",
            "fence_style": "picket",
            "section_count": 10,
        }),
        ("railing", {
            "asset_type": "railing",
            "width": 280.0,
            "height": 105.0,
            "depth": 14.0,
            "material": "steel",
            "baluster_count": 8,
        }),
        ("chimney", {
            "asset_type": "chimney",
            "width": 90.0,
            "depth": 90.0,
            "height": 240.0,
            "material": "brick",
            "has_cap": True,
        }),
        ("porch", {
            "asset_type": "porch",
            "width": 360.0,
            "depth": 220.0,
            "height": 260.0,
            "material": "wood",
            "pillar_count": 4,
            "has_steps": True,
        }),
    ],
)
def test_architecture_generator_smoke(asset_type, params):
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "architecture_asset.py")
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
