import pytest
from pydantic import ValidationError
from asset_schemas import validate_asset_params, SwordSchema, TableSchema, BarrelSchema, CrateSchema, ShieldSchema, ChairSchema, ChestSchema, AxeSchema, HelmetSchema, TorchSchema, SofaSchema, BenchSchema, CouchSchema, ArmchairSchema, BedSchema, BunkBedSchema, WardrobeSchema, StorageSchema, LightingSchema, ClosetSchema, DresserSchema, CabinetSchema, ShelfSchema, BookcaseSchema, NightstandSchema, TVStandSchema, FridgeSchema, StoveSchema, OvenSchema, MicrowaveSchema, SinkSchema, CountertopSchema, CupboardSchema, KitchenIslandSchema, DiningSetSchema, ToiletSchema, BathtubSchema, ShowerSchema, MirrorSchema, TowelRackSchema, TankSchema

def test_valid_sword():
    data = {
        "asset_type": "sword",
        "blade_length": 95.0,
        "blade_width": 6.0,
        "grip_length": 18.0,
        "crossguard_type": "curved",
        "grip_material": "wood"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, SwordSchema)
    assert validated.blade_length == 95.0
    assert validated.crossguard_type == "curved"
    assert validated.grip_material == "wood"

def test_sword_out_of_bounds():
    data = {
        "asset_type": "sword",
        "blade_length": 300.0,  # Max limit is 150
    }
    with pytest.raises(ValidationError):
        validate_asset_params(data)

def test_invalid_crossguard_type():
    data = {
        "asset_type": "sword",
        "crossguard_type": "fancy_engraved"  # Not in simple/curved/none
    }
    with pytest.raises(ValidationError):
        validate_asset_params(data)

def test_valid_table():
    data = {
        "asset_type": "table",
        "width": 150.0,
        "leg_style": "round"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, TableSchema)
    assert validated.width == 150.0
    assert validated.depth == 80.0  # default
    assert validated.leg_style == "round"

def test_table_out_of_bounds():
    data = {
        "asset_type": "table",
        "depth": 10.0  # Min limit is 40
    }
    with pytest.raises(ValidationError):
        validate_asset_params(data)

def test_valid_barrel():
    data = {
        "asset_type": "barrel",
        "radius": 0.5,
        "height": 1.2
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, BarrelSchema)
    assert validated.radius == 0.5
    assert validated.height == 1.2

def test_valid_crate():
    data = {
        "asset_type": "crate",
        "width": 1.5,
        "depth": 1.5,
        "height": 1.5
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, CrateSchema)
    assert validated.width == 1.5

def test_valid_shield():
    data = {
        "asset_type": "shield",
        "shield_style": "heater",
        "diameter": 70.0,
        "boss_material": "brass"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, ShieldSchema)
    assert validated.shield_style == "heater"
    assert validated.diameter == 70.0
    assert validated.has_rim is True

def test_valid_chair():
    data = {
        "asset_type": "chair",
        "width": 45.0,
        "depth": 45.0,
        "seat_height": 40.0,
        "backrest_height": 55.0,
        "leg_style": "round"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, ChairSchema)
    assert validated.width == 45.0
    assert validated.leg_style == "round"

def test_valid_chest():
    data = {
        "asset_type": "chest",
        "width": 90.0,
        "depth": 60.0,
        "height": 55.0,
        "lid_style": "arched",
        "has_lock": True
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, ChestSchema)
    assert validated.width == 90.0
    assert validated.lid_style == "arched"

def test_valid_axe():
    data = {
        "asset_type": "axe",
        "shaft_length": 95.0,
        "axe_style": "double",
        "head_material": "steel",
        "shaft_material": "wood"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, AxeSchema)
    assert validated.shaft_length == 95.0
    assert validated.axe_style == "double"

def test_valid_helmet():
    data = {
        "asset_type": "helmet",
        "style": "spartan",
        "material": "bronze",
        "has_crest": True
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, HelmetSchema)
    assert validated.style == "spartan"
    assert validated.material == "bronze"
    assert validated.has_crest is True

def test_valid_torch():
    data = {
        "asset_type": "torch",
        "style": "wall_mounted",
        "shaft_length": 45.0,
        "flame_size": 18.0
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, TorchSchema)
    assert validated.style == "wall_mounted"
    assert validated.shaft_length == 45.0
    assert validated.flame_size == 18.0

def test_valid_sofa():
    data = {
        "asset_type": "sofa",
        "style": "couch",
        "width": 200.0,
        "depth": 85.0,
        "has_armrests": True
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, SofaSchema)
    assert validated.style == "couch"
    assert validated.width == 200.0
    assert validated.has_armrests is True

def test_valid_storage():
    data = {
        "asset_type": "storage",
        "style": "bookcase",
        "width": 120.0,
        "depth": 35.0,
        "height": 180.0,
        "num_shelves": 4,
        "has_doors": False
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, StorageSchema)
    assert validated.style == "bookcase"
    assert validated.num_shelves == 4
    assert validated.has_doors is False

def test_valid_lighting():
    data = {
        "asset_type": "lighting",
        "style": "lamp",
        "height": 150.0,
        "is_lit": True
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, LightingSchema)
    assert validated.style == "lamp"
    assert validated.height == 150.0
    assert validated.is_lit is True

def test_valid_bench():
    data = {
        "asset_type": "bench",
        "width": 140.0,
        "depth": 45.0,
        "height": 45.0,
        "has_backrest": True,
        "leg_style": "x_frame",
        "material": "metal"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, BenchSchema)
    assert validated.width == 140.0
    assert validated.leg_style == "x_frame"
    assert validated.material == "metal"

def test_valid_couch():
    data = {
        "asset_type": "couch",
        "width": 220.0,
        "depth": 95.0,
        "height": 80.0,
        "has_chaise": True,
        "material": "leather"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, CouchSchema)
    assert validated.width == 220.0
    assert validated.has_chaise is True
    assert validated.material == "leather"

def test_valid_armchair():
    data = {
        "asset_type": "armchair",
        "width": 90.0,
        "depth": 85.0,
        "height": 85.0,
        "style": "recliner",
        "material": "velvet"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, ArmchairSchema)
    assert validated.width == 90.0
    assert validated.style == "recliner"
    assert validated.material == "velvet"

def test_valid_bed():
    data = {
        "asset_type": "bed",
        "width": 180.0,
        "depth": 200.0,
        "height": 65.0,
        "has_headboard": True,
        "material": "padded"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, BedSchema)
    assert validated.width == 180.0
    assert validated.material == "padded"

def test_valid_bunk_bed():
    data = {
        "asset_type": "bunk_bed",
        "width": 90.0,
        "depth": 190.0,
        "height": 170.0,
        "has_ladder": True,
        "material": "metal"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, BunkBedSchema)
    assert validated.width == 90.0
    assert validated.material == "metal"

def test_valid_wardrobe():
    data = {
        "asset_type": "wardrobe",
        "width": 150.0,
        "depth": 65.0,
        "height": 210.0,
        "style": "classic",
        "has_mirror": True
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, WardrobeSchema)
    assert validated.width == 150.0
    assert validated.has_mirror is True

def test_valid_closet():
    data = {
        "asset_type": "closet",
        "width": 160.0,
        "depth": 70.0,
        "height": 220.0,
        "door_style": "walk_in",
        "doors": 0,
        "material": "dark_oak"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, ClosetSchema)
    assert validated.width == 160.0
    assert validated.door_style == "walk_in"
    assert validated.doors == 0

def test_valid_dresser():
    data = {
        "asset_type": "dresser",
        "width": 130.0,
        "depth": 55.0,
        "height": 85.0,
        "drawers_rows": 4,
        "drawers_cols": 2,
        "style": "modern"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, DresserSchema)
    assert validated.width == 130.0
    assert validated.drawers_rows == 4

def test_valid_cabinet():
    data = {
        "asset_type": "cabinet",
        "width": 90.0,
        "depth": 45.0,
        "height": 140.0,
        "has_glass": True,
        "shelves": 4,
        "style": "display"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, CabinetSchema)
    assert validated.width == 90.0
    assert validated.has_glass is True

def test_valid_shelf():
    data = {
        "asset_type": "shelf",
        "width": 80.0,
        "depth": 25.0,
        "height": 20.0,
        "material": "wood",
        "brackets": "floating"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, ShelfSchema)
    assert validated.width == 80.0
    assert validated.material == "wood"
    assert validated.brackets == "floating"

def test_valid_bookcase():
    data = {
        "asset_type": "bookcase",
        "width": 90.0,
        "depth": 35.0,
        "height": 180.0,
        "shelves": 5,
        "has_back_panel": True,
        "material": "metal_frame"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, BookcaseSchema)
    assert validated.width == 90.0
    assert validated.shelves == 5
    assert validated.material == "metal_frame"

def test_valid_nightstand():
    data = {
        "asset_type": "nightstand",
        "width": 50.0,
        "depth": 40.0,
        "height": 60.0,
        "drawers": 2,
        "has_open_shelf": False,
        "style": "mid_century"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, NightstandSchema)
    assert validated.width == 50.0
    assert validated.drawers == 2
    assert validated.style == "mid_century"

def test_valid_tv_stand():
    data = {
        "asset_type": "tv_stand",
        "width": 160.0,
        "depth": 45.0,
        "height": 55.0,
        "compartments": 4,
        "has_doors": True,
        "style": "modern"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, TVStandSchema)
    assert validated.width == 160.0
    assert validated.compartments == 4
    assert validated.has_doors is True

def test_missing_asset_type():
    data = {
        "width": 1.0
    }
    with pytest.raises(ValueError, match="Field 'asset_type' is required"):
        validate_asset_params(data)

def test_valid_fridge():
    data = {
        "asset_type": "fridge",
        "width": 80.0,
        "depth": 75.0,
        "height": 190.0,
        "style": "french_door",
        "material": "stainless_steel",
        "has_dispenser": True
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, FridgeSchema)
    assert validated.width == 80.0
    assert validated.style == "french_door"
    assert validated.has_dispenser is True

def test_valid_stove():
    data = {
        "asset_type": "stove",
        "width": 80.0,
        "depth": 65.0,
        "height": 92.0,
        "burners": 5,
        "style": "electric_glass",
        "material": "black"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, StoveSchema)
    assert validated.width == 80.0
    assert validated.burners == 5
    assert validated.style == "electric_glass"

def test_valid_oven():
    data = {
        "asset_type": "oven",
        "width": 70.0,
        "depth": 60.0,
        "height": 65.0,
        "has_glass_window": True,
        "shelves": 3,
        "style": "built_in"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, OvenSchema)
    assert validated.width == 70.0
    assert validated.shelves == 3
    assert validated.style == "built_in"

def test_valid_microwave():
    data = {
        "asset_type": "microwave",
        "width": 60.0,
        "depth": 45.0,
        "height": 38.0,
        "style": "built_in",
        "has_glass_door": True
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, MicrowaveSchema)
    assert validated.width == 60.0
    assert validated.style == "built_in"
    assert validated.has_glass_door is True

def test_valid_sink():
    data = {
        "asset_type": "sink",
        "width": 90.0,
        "depth": 65.0,
        "height": 88.0,
        "style": "double_basin",
        "faucet_style": "goose_neck"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, SinkSchema)
    assert validated.width == 90.0
    assert validated.style == "double_basin"
    assert validated.faucet_style == "goose_neck"

def test_valid_countertop():
    data = {
        "asset_type": "countertop",
        "width": 180.0,
        "depth": 65.0,
        "height": 92.0,
        "has_drawers": True,
        "has_backsplash": True,
        "material": "granite"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, CountertopSchema)
    assert validated.width == 180.0
    assert validated.has_drawers is True
    assert validated.material == "granite"

def test_valid_cupboard():
    data = {
        "asset_type": "cupboard",
        "width": 110.0,
        "depth": 50.0,
        "height": 190.0,
        "style": "pantry",
        "has_drawers": False,
        "shelves": 4
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, CupboardSchema)
    assert validated.width == 110.0
    assert validated.has_drawers is False
    assert validated.style == "pantry"

def test_valid_kitchen_island():
    data = {
        "asset_type": "kitchen_island",
        "width": 180.0,
        "depth": 100.0,
        "height": 95.0,
        "overhang_depth": 30.0,
        "has_stools": True,
        "stools_count": 3,
        "material": "industrial_metal"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, KitchenIslandSchema)
    assert validated.width == 180.0
    assert validated.stools_count == 3
    assert validated.material == "industrial_metal"

def test_valid_dining_set():
    data = {
        "asset_type": "dining_set",
        "table_width": 200.0,
        "table_depth": 100.0,
        "table_height": 78.0,
        "chair_count": 8,
        "chair_style": "modern",
        "material": "walnut"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, DiningSetSchema)
    assert validated.table_width == 200.0
    assert validated.chair_count == 8
    assert validated.material == "walnut"

def test_valid_toilet():
    data = {
        "asset_type": "toilet",
        "width": 45.0,
        "depth": 65.0,
        "height": 78.0,
        "bowl_shape": "round",
        "has_lid_open": True,
        "tank_width": 40.0,
        "tank_depth": 18.0
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, ToiletSchema)
    assert validated.width == 45.0
    assert validated.has_lid_open is True
    assert validated.bowl_shape == "round"

def test_valid_bathtub():
    data = {
        "asset_type": "bathtub",
        "width": 170.0,
        "depth": 80.0,
        "height": 55.0,
        "style": "clawfoot",
        "material": "copper",
        "has_faucet": False
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, BathtubSchema)
    assert validated.width == 170.0
    assert validated.material == "copper"
    assert validated.has_faucet is False

def test_valid_shower():
    data = {
        "asset_type": "shower",
        "width": 100.0,
        "depth": 100.0,
        "height": 220.0,
        "enclosure": "curtain",
        "head_type": "rain",
        "material": "brass"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, ShowerSchema)
    assert validated.width == 100.0
    assert validated.enclosure == "curtain"
    assert validated.head_type == "rain"

def test_valid_mirror():
    data = {
        "asset_type": "mirror",
        "width": 50.0,
        "height": 70.0,
        "shape": "circular",
        "border_style": "wood",
        "border_color": "wood"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, MirrorSchema)
    assert validated.width == 50.0
    assert validated.shape == "circular"
    assert validated.border_style == "wood"

def test_valid_towel_rack():
    data = {
        "asset_type": "towel_rack",
        "width": 70.0,
        "depth": 12.0,
        "height": 15.0,
        "bar_style": "double_bar",
        "material": "chrome",
        "has_towel": True,
        "towel_color": "blue"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, TowelRackSchema)
    assert validated.width == 70.0
    assert validated.bar_style == "double_bar"
    assert validated.towel_color == "blue"

def test_storage_tank_alias_normalizes_to_tank():
    data = {
        "asset_type": "storage_tank",
        "diameter": 180.0,
        "height": 320.0,
        "material": "steel",
        "orientation": "vertical"
    }
    validated = validate_asset_params(data)
    assert isinstance(validated, TankSchema)
    assert validated.asset_type == "tank"
    assert validated.diameter == 180.0
    assert validated.orientation == "vertical"

if __name__ == "__main__":
    pytest.main([__file__])
