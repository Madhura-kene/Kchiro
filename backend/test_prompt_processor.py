import sys
import os
import pytest

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.prompt_processor import PromptProcessor
from schemas.asset_schemas import SwordSchema, TableSchema, BarrelSchema, CrateSchema, CupboardSchema, KitchenIslandSchema, DiningSetSchema, ToiletSchema, BathtubSchema, ShowerSchema, MirrorSchema, TowelRackSchema

def test_unit_repair_barrel_cm_to_m():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "barrel",
        "radius": 40.0,  # 40cm -> 0.4m
        "height": 100.0  # 100cm -> 1.0m
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["radius"] == 0.4
    assert repaired["height"] == 1.0

def test_unit_repair_sword_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "sword",
        "blade_length": 0.95,  # 0.95m -> 95cm
        "grip_length": 0.15   # 0.15m -> 15cm
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["blade_length"] == 95.0
    assert repaired["grip_length"] == 15.0

def test_unit_repair_table_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "table",
        "width": 1.2,   # 1.2m -> 120cm
        "depth": 0.8,   # 0.8m -> 80cm
        "height": 0.75  # 0.75m -> 75cm
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 120.0
    assert repaired["depth"] == 80.0
    assert repaired["height"] == 75.0

def test_unit_repair_shield_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "shield",
        "diameter": 0.7  # 0.7m -> 70cm
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["diameter"] == 70.0

def test_unit_repair_chair_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "chair",
        "width": 0.5,
        "depth": 0.5,
        "seat_height": 0.45,
        "backrest_height": 0.5
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 50.0
    assert repaired["depth"] == 50.0
    assert repaired["seat_height"] == 45.0
    assert repaired["backrest_height"] == 50.0

def test_unit_repair_chest_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "chest",
        "width": 0.8,
        "depth": 0.5,
        "height": 0.5
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 80.0
    assert repaired["depth"] == 50.0
    assert repaired["height"] == 50.0

def test_unit_repair_axe_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "axe",
        "shaft_length": 0.8
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["shaft_length"] == 80.0

def test_unit_repair_torch_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "torch",
        "shaft_length": 0.45,
        "flame_size": 0.12
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["shaft_length"] == 45.0
    assert repaired["flame_size"] == 12.0

def test_unit_repair_sofa_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "sofa",
        "width": 1.8,
        "depth": 0.9
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 180.0
    assert repaired["depth"] == 90.0

def test_unit_repair_bench_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "bench",
        "width": 1.2,
        "depth": 0.4,
        "height": 0.45
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 120.0
    assert repaired["depth"] == 40.0
    assert repaired["height"] == 45.0

def test_unit_repair_couch_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "couch",
        "width": 2.0,
        "depth": 0.9,
        "height": 0.85
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 200.0
    assert repaired["depth"] == 90.0
    assert repaired["height"] == 85.0

def test_unit_repair_armchair_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "armchair",
        "width": 0.85,
        "depth": 0.8,
        "height": 0.85
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 85.0
    assert repaired["depth"] == 80.0
    assert repaired["height"] == 85.0

def test_unit_repair_bed_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "bed",
        "width": 1.6,
        "depth": 2.0,
        "height": 0.6
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 160.0
    assert repaired["depth"] == 200.0
    assert repaired["height"] == 60.0

def test_unit_repair_bunk_bed_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "bunk_bed",
        "width": 1.0,
        "depth": 2.0,
        "height": 1.8
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 100.0
    assert repaired["depth"] == 200.0
    assert repaired["height"] == 180.0

def test_unit_repair_wardrobe_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "wardrobe",
        "width": 1.2,
        "depth": 0.6,
        "height": 1.9
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 120.0
    assert repaired["depth"] == 60.0
    assert repaired["height"] == 190.0

def test_unit_repair_storage_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "storage",
        "width": 1.0,
        "depth": 0.4,
        "height": 1.6
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 100.0
    assert repaired["depth"] == 40.0
    assert repaired["height"] == 160.0

def test_unit_repair_lighting_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "lighting",
        "height": 1.2
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["height"] == 120.0

def test_unit_repair_crate_cm_to_m():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "crate",
        "width": 150.0,
        "depth": 150.0,
        "height": 150.0
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 1.5
    assert repaired["depth"] == 1.5
    assert repaired["height"] == 1.5

def test_unit_repair_closet_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "closet",
        "width": 1.5,
        "depth": 0.65,
        "height": 2.0
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 150.0
    assert repaired["depth"] == 65.0
    assert repaired["height"] == 200.0

def test_unit_repair_dresser_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "dresser",
        "width": 1.2,
        "depth": 0.5,
        "height": 0.9
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 120.0
    assert repaired["depth"] == 50.0
    assert repaired["height"] == 90.0

def test_unit_repair_cabinet_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "cabinet",
        "width": 0.8,
        "depth": 0.4,
        "height": 1.2
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 80.0
    assert repaired["depth"] == 40.0
    assert repaired["height"] == 120.0

def test_unit_repair_shelf_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "shelf",
        "width": 0.8,
        "depth": 0.25,
        "height": 0.2
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 80.0
    assert repaired["depth"] == 25.0
    assert repaired["height"] == 20.0

def test_unit_repair_bookcase_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "bookcase",
        "width": 0.9,
        "depth": 0.35,
        "height": 1.8
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 90.0
    assert repaired["depth"] == 35.0
    assert repaired["height"] == 180.0

def test_unit_repair_nightstand_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "nightstand",
        "width": 0.5,
        "depth": 0.4,
        "height": 0.6
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 50.0
    assert repaired["depth"] == 40.0
    assert repaired["height"] == 60.0

def test_unit_repair_tv_stand_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "tv_stand",
        "width": 1.5,
        "depth": 0.45,
        "height": 0.5
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 150.0
    assert repaired["depth"] == 45.0
    assert repaired["height"] == 50.0

def test_unit_repair_fridge_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "fridge",
        "width": 0.75,
        "depth": 0.7,
        "height": 1.8
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 75.0
    assert repaired["depth"] == 70.0
    assert repaired["height"] == 180.0

def test_unit_repair_stove_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "stove",
        "width": 0.75,
        "depth": 0.6,
        "height": 0.9
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 75.0
    assert repaired["depth"] == 60.0
    assert repaired["height"] == 90.0

def test_unit_repair_oven_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "oven",
        "width": 0.6,
        "depth": 0.55,
        "height": 0.6
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 60.0
    assert repaired["depth"] == 55.0
    assert repaired["height"] == 60.0

def test_unit_repair_microwave_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "microwave",
        "width": 0.55,
        "depth": 0.4,
        "height": 0.35
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 55.0
    assert repaired["depth"] == 40.0
    assert repaired["height"] == 35.0

def test_unit_repair_sink_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "sink",
        "width": 0.8,
        "depth": 0.6,
        "height": 0.85
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 80.0
    assert repaired["depth"] == 60.0
    assert repaired["height"] == 85.0

def test_unit_repair_countertop_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "countertop",
        "width": 1.2,
        "depth": 0.6,
        "height": 0.9
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 120.0
    assert repaired["depth"] == 60.0
    assert repaired["height"] == 90.0

def test_unit_repair_cupboard_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "cupboard",
        "width": 1.0,
        "depth": 0.45,
        "height": 1.8
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 100.0
    assert repaired["depth"] == 45.0
    assert repaired["height"] == 180.0

def test_unit_repair_kitchen_island_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "kitchen_island",
        "width": 1.6,
        "depth": 0.9,
        "height": 0.9
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 160.0
    assert repaired["depth"] == 90.0
    assert repaired["height"] == 90.0

def test_unit_repair_dining_set_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "dining_set",
        "table_width": 1.8,
        "table_depth": 0.9,
        "table_height": 0.75
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["table_width"] == 180.0
    assert repaired["table_depth"] == 90.0
    assert repaired["table_height"] == 75.0

def test_unit_repair_toilet_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "toilet",
        "width": 0.5,
        "depth": 0.7,
        "height": 0.8,
        "tank_width": 0.45,
        "tank_depth": 0.2
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 50.0
    assert repaired["depth"] == 70.0
    assert repaired["height"] == 80.0
    assert repaired["tank_width"] == 45.0
    assert repaired["tank_depth"] == 20.0

def test_unit_repair_bathtub_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "bathtub",
        "width": 1.6,
        "depth": 0.75,
        "height": 0.6
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 160.0
    assert repaired["depth"] == 75.0
    assert repaired["height"] == 60.0

def test_unit_repair_shower_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "shower",
        "width": 0.9,
        "depth": 0.9,
        "height": 2.1
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 90.0
    assert repaired["depth"] == 90.0
    assert repaired["height"] == 210.0

def test_unit_repair_mirror_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "mirror",
        "width": 0.6,
        "height": 0.8
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 60.0
    assert repaired["height"] == 80.0

def test_unit_repair_towel_rack_m_to_cm():
    processor = PromptProcessor()
    raw_data = {
        "asset_type": "towel_rack",
        "width": 0.6,
        "depth": 0.15,
        "height": 0.2
    }
    repaired = processor.repair_units(raw_data)
    assert repaired["width"] == 60.0
    assert repaired["depth"] == 15.0
    assert repaired["height"] == 20.0

def test_end_to_end_pipeline_integration():
    # Run a real test against the local Ollama instance
    if os.getenv("RUN_OLLAMA_INTEGRATION_TESTS") != "1":
        pytest.skip("Set RUN_OLLAMA_INTEGRATION_TESTS=1 to run tests that call local Ollama.")

    processor = PromptProcessor()
    prompt = "Create a wooden table that is 140cm wide and 75cm high with round legs."
    
    print(f"\nTesting pipeline with prompt: \"{prompt}\"")
    try:
        params, generator_path = processor.process_prompt(prompt)
        print("Pipeline output validated parameters:")
        print(params)
        print(f"Pipeline output generator path: {generator_path}")
        
        assert isinstance(params, TableSchema)
        assert params.width == 140.0
        assert params.height == 75.0
        assert params.leg_style == "round"
        assert "table.py" in generator_path
        
    except Exception as e:
        pytest.fail(f"Pipeline integration test failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
