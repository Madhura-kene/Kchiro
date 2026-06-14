import os
import re
import sys
import logging
from typing import Dict, Any, Tuple

# Dynamic path resolution to find schemas and backend
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.ollama_client import OllamaClient
from schemas.asset_schemas import validate_asset_params, AssetParams, SCHEMA_BY_ASSET_TYPE

logger = logging.getLogger("PromptProcessor")

ARCHITECTURE_ASSET_TYPES = {
    "wall",
    "floor",
    "ceiling",
    "roof",
    "pillar",
    "beam",
    "foundation",
    "door",
    "window",
    "archway",
    "gate",
    "stairs",
    "ladder",
    "ramp",
    "bridge",
    "balcony",
    "fence",
    "railing",
    "chimney",
    "porch",
}

ARCHITECTURE_TYPE_ALIASES = {
    "wall": "wall",
    "wall section": "wall",
    "wall_section": "wall",
    "partition wall": "wall",
    "partition_wall": "wall",
    "interior wall": "wall",
    "interior_wall": "wall",
    "foundation": "foundation",
    "foundation slab": "foundation",
    "foundation_slab": "foundation",
    "base slab": "foundation",
    "base_slab": "foundation",
    "footing": "foundation",
    "floor": "floor",
    "floor slab": "floor",
    "floor_slab": "floor",
    "ceiling": "ceiling",
    "ceiling panel": "ceiling",
    "ceiling_panel": "ceiling",
    "roof": "roof",
    "gabled roof": "roof",
    "gabled_roof": "roof",
    "flat roof": "roof",
    "flat_roof": "roof",
    "hip roof": "roof",
    "hip_roof": "roof",
    "mansard roof": "roof",
    "mansard_roof": "roof",
    "pillar": "pillar",
    "column": "pillar",
    "beam": "beam",
    "support beam": "beam",
    "support_beam": "beam",
    "door": "door",
    "entry door": "door",
    "entry_door": "door",
    "interior door": "door",
    "interior_door": "door",
    "window": "window",
    "glass window": "window",
    "glass_window": "window",
    "window_frame": "window",
    "archway": "archway",
    "arch": "archway",
    "gate": "gate",
    "stairs": "stairs",
    "staircase": "stairs",
    "stairway": "stairs",
    "ladder": "ladder",
    "ramp": "ramp",
    "inclined ramp": "ramp",
    "bridge": "bridge",
    "foot bridge": "bridge",
    "footbridge": "bridge",
    "balcony": "balcony",
    "railing": "railing",
    "handrail": "railing",
    "fence": "fence",
    "chimney": "chimney",
    "porch": "porch",
}

GENERIC_ARCHITECTURE_TYPES = {
    "wall",
    "floor",
    "ceiling",
    "roof",
    "pillar",
    "beam",
}

WEAPON_ASSET_TYPES = {
    "sword",
    "dagger",
    "axe",
    "hammer",
    "mace",
    "spear",
    "halberd",
    "staff",
    "bow",
    "crossbow",
    "arrow",
    "bolt",
    "magic_staff",
    "wand",
    "orb",
}

WEAPON_TYPE_ALIASES = {
    "sword": "sword",
    "broadsword": "sword",
    "longsword": "sword",
    "shortsword": "sword",
    "dagger": "dagger",
    "knife": "dagger",
    "dirk": "dagger",
    "stiletto": "dagger",
    "axe": "axe",
    "battle axe": "axe",
    "battle_axe": "axe",
    "battleaxe": "axe",
    "hatchet": "axe",
    "hammer": "hammer",
    "war hammer": "hammer",
    "war_hammer": "hammer",
    "warhammer": "hammer",
    "mace": "mace",
    "morningstar": "mace",
    "spear": "spear",
    "pike": "spear",
    "javelin": "spear",
    "halberd": "halberd",
    "poleaxe": "halberd",
    "pole axe": "halberd",
    "polearm": "halberd",
    "staff": "staff",
    "bow": "bow",
    "longbow": "bow",
    "shortbow": "bow",
    "recurve bow": "bow",
    "recurve_bow": "bow",
    "crossbow": "crossbow",
    "arrow": "arrow",
    "bolt": "bolt",
    "crossbow bolt": "bolt",
    "crossbow_bolt": "bolt",
    "magic staff": "magic_staff",
    "magic_staff": "magic_staff",
    "mage staff": "magic_staff",
    "mage_staff": "magic_staff",
    "wizard staff": "magic_staff",
    "wizard_staff": "magic_staff",
    "arcane staff": "magic_staff",
    "arcane_staff": "magic_staff",
    "wand": "wand",
    "orb": "orb",
    "magic orb": "orb",
    "magic_orb": "orb",
}

ADVENTURE_ASSET_TYPES = {
    "chestplate",
    "gauntlets",
    "boots",
    "backpack",
    "belt",
    "pouch",
    "cape",
    "tent",
    "campfire",
    "sleeping_bag",
    "lantern",
    "cooking_pot",
    "supply_box",
    "castle_wall",
    "tower",
    "drawbridge",
    "throne",
    "banner",
    "market_stall",
    "well",
    "cart",
    "anvil",
    "forge",
}

ADVENTURE_TYPE_ALIASES = {
    "chestplate": "chestplate",
    "chest plate": "chestplate",
    "breastplate": "chestplate",
    "cuirass": "chestplate",
    "gauntlet": "gauntlets",
    "gauntlets": "gauntlets",
    "boot": "boots",
    "boots": "boots",
    "backpack": "backpack",
    "pack": "backpack",
    "rucksack": "backpack",
    "belt": "belt",
    "pouch": "pouch",
    "satchel": "pouch",
    "cape": "cape",
    "cloak": "cape",
    "tent": "tent",
    "campfire": "campfire",
    "camp fire": "campfire",
    "fire pit": "campfire",
    "sleeping bag": "sleeping_bag",
    "sleeping_bag": "sleeping_bag",
    "bedroll": "sleeping_bag",
    "lantern": "lantern",
    "cooking pot": "cooking_pot",
    "cooking_pot": "cooking_pot",
    "cook pot": "cooking_pot",
    "supply box": "supply_box",
    "supply_box": "supply_box",
    "provision box": "supply_box",
    "castle wall": "castle_wall",
    "castle_wall": "castle_wall",
    "fort wall": "castle_wall",
    "tower": "tower",
    "watchtower": "tower",
    "watch tower": "tower",
    "drawbridge": "drawbridge",
    "draw bridge": "drawbridge",
    "throne": "throne",
    "banner": "banner",
    "market stall": "market_stall",
    "market_stall": "market_stall",
    "well": "well",
    "cart": "cart",
    "wagon": "cart",
    "anvil": "anvil",
    "forge": "forge",
    "smithy": "forge",
    "blacksmith forge": "forge",
}

NATURE_ASSET_TYPES = {
    "oak_tree",
    "pine_tree",
    "birch_tree",
    "palm_tree",
    "dead_tree",
    "sapling",
    "grass",
    "bush",
    "shrub",
    "fern",
    "flower",
    "moss",
    "small_rock",
    "boulder",
    "rock_cluster",
    "cliff_section",
    "log",
    "tree_stump",
    "fallen_tree",
    "mushroom",
    "vine",
    "root",
    "pond",
    "river_segment",
    "waterfall",
    "stream",
}

NATURE_TYPE_ALIASES = {
    "oak tree": "oak_tree",
    "oak_tree": "oak_tree",
    "pine tree": "pine_tree",
    "pine_tree": "pine_tree",
    "birch tree": "birch_tree",
    "birch_tree": "birch_tree",
    "palm tree": "palm_tree",
    "palm_tree": "palm_tree",
    "dead tree": "dead_tree",
    "dead_tree": "dead_tree",
    "sapling": "sapling",
    "grass patch": "grass",
    "grass": "grass",
    "bush": "bush",
    "shrub": "shrub",
    "fern": "fern",
    "flower": "flower",
    "moss": "moss",
    "small rock": "small_rock",
    "stone": "small_rock",
    "boulder": "boulder",
    "rock cluster": "rock_cluster",
    "rocks": "rock_cluster",
    "cliff section": "cliff_section",
    "cliff": "cliff_section",
    "log": "log",
    "tree stump": "tree_stump",
    "stump": "tree_stump",
    "fallen tree": "fallen_tree",
    "mushroom": "mushroom",
    "vine": "vine",
    "ivy": "vine",
    "root": "root",
    "tree root": "root",
    "pond": "pond",
    "river segment": "river_segment",
    "river": "river_segment",
    "waterfall": "waterfall",
    "stream": "stream",
    "creek": "stream",
    "brook": "stream",
}

WORLD_ASSET_TYPES = {
    "control_panel",
    "terminal",
    "computer",
    "server_rack",
    "energy_cell",
    "tech_crate",
    "space_door",
    "airlock",
    "turret",
    "drone",
    "pipe",
    "valve",
    "tank",
    "generator",
    "conveyor_belt",
    "toolbox",
    "forklift",
    "storage_rack",
    "street_lamp",
    "traffic_light",
    "road_sign",
    "street_bench",
    "mailbox",
    "trash_can",
    "bus_stop",
    "phone_booth",
    "car",
    "truck",
    "bike",
    "motorcycle",
    "tractor",
    "battle_tank",
    "boat",
    "canoe",
    "ship",
    "plane",
    "helicopter",
    "male",
    "female",
    "child",
    "elder",
    "merchant",
    "guard",
    "farmer",
    "blacksmith",
    "soldier",
    "elf",
    "orc",
    "goblin",
    "dwarf",
    "dragon",
    "dog",
    "cat",
    "horse",
    "cow",
    "deer",
    "wolf",
    "bird",
    "fish",
    "coin",
    "gem",
    "key",
    "scroll",
    "potion",
    "treasure_chest",
    "artifact",
    "terrain",
    "hill",
    "mountain",
    "cliff",
    "valley",
    "cave",
    "ground_tile",
    "road_tile",
    "path_tile",
    "river_tile",
    "dungeon_tile",
    "game_background_2d",
}

WORLD_TYPE_ALIASES = {
    "control panel": "control_panel",
    "control_panel": "control_panel",
    "terminal": "terminal",
    "computer": "computer",
    "server rack": "server_rack",
    "server_rack": "server_rack",
    "energy cell": "energy_cell",
    "energy_cell": "energy_cell",
    "tech crate": "tech_crate",
    "tech crate": "tech_crate",
    "sci fi crate": "tech_crate",
    "sci-fi crate": "tech_crate",
    "futuristic crate": "tech_crate",
    "cargo crate": "tech_crate",
    "space door": "space_door",
    "space_door": "space_door",
    "air lock": "airlock",
    "airlock": "airlock",
    "turret": "turret",
    "drone": "drone",
    "pipe": "pipe",
    "valve": "valve",
    "storage tank": "tank",
    "fuel tank": "tank",
    "industrial tank": "tank",
    "tank": "tank",
    "generator": "generator",
    "conveyor belt": "conveyor_belt",
    "conveyor_belt": "conveyor_belt",
    "toolbox": "toolbox",
    "forklift": "forklift",
    "storage rack": "storage_rack",
    "storage_rack": "storage_rack",
    "street lamp": "street_lamp",
    "street_lamp": "street_lamp",
    "traffic light": "traffic_light",
    "traffic_light": "traffic_light",
    "road sign": "road_sign",
    "road_sign": "road_sign",
    "street bench": "street_bench",
    "city bench": "street_bench",
    "urban bench": "street_bench",
    "street_bench": "street_bench",
    "mailbox": "mailbox",
    "mail box": "mailbox",
    "trash can": "trash_can",
    "trash_can": "trash_can",
    "trash bin": "trash_can",
    "bin": "trash_can",
    "bus stop": "bus_stop",
    "bus_stop": "bus_stop",
    "phone booth": "phone_booth",
    "telephone booth": "phone_booth",
    "phone_booth": "phone_booth",
    "car": "car",
    "truck": "truck",
    "bike": "bike",
    "bicycle": "bike",
    "motorcycle": "motorcycle",
    "motorbike": "motorcycle",
    "tractor": "tractor",
    "battle tank": "battle_tank",
    "battle_tank": "battle_tank",
    "military tank": "battle_tank",
    "armored tank": "battle_tank",
    "armoured tank": "battle_tank",
    "boat": "boat",
    "canoe": "canoe",
    "ship": "ship",
    "plane": "plane",
    "airplane": "plane",
    "aeroplane": "plane",
    "helicopter": "helicopter",
    "male": "male",
    "female": "female",
    "woman": "female",
    "child": "child",
    "kid": "child",
    "elder": "elder",
    "old person": "elder",
    "merchant": "merchant",
    "guard": "guard",
    "farmer": "farmer",
    "blacksmith": "blacksmith",
    "soldier": "soldier",
    "elf": "elf",
    "orc": "orc",
    "goblin": "goblin",
    "dwarf": "dwarf",
    "dragon": "dragon",
    "dog": "dog",
    "cat": "cat",
    "horse": "horse",
    "cow": "cow",
    "deer": "deer",
    "wolf": "wolf",
    "bird": "bird",
    "fish": "fish",
    "coin": "coin",
    "gem": "gem",
    "key": "key",
    "scroll": "scroll",
    "potion": "potion",
    "treasure chest": "treasure_chest",
    "treasure_chest": "treasure_chest",
    "artifact": "artifact",
    "terrain": "terrain",
    "hill": "hill",
    "mountain": "mountain",
    "cliff": "cliff",
    "valley": "valley",
    "cave": "cave",
    "ground tile": "ground_tile",
    "ground_tile": "ground_tile",
    "road tile": "road_tile",
    "road_tile": "road_tile",
    "path tile": "path_tile",
    "path_tile": "path_tile",
    "river tile": "river_tile",
    "river_tile": "river_tile",
    "dungeon tile": "dungeon_tile",
    "dungeon_tile": "dungeon_tile",
    "2d background": "game_background_2d",
    "2d game background": "game_background_2d",
    "2d level background": "game_background_2d",
    "video game background": "game_background_2d",
    "parallax background": "game_background_2d",
    "platformer background": "game_background_2d",
    "side scroller background": "game_background_2d",
    "side-scroller background": "game_background_2d",
    "game_background_2d": "game_background_2d",
}

NATURE_UNIT_MINIMUMS = {
    "oak_tree": {"height": 320.0, "canopy_width": 180.0, "trunk_radius": 8.0},
    "pine_tree": {"height": 400.0, "canopy_width": 120.0, "trunk_radius": 6.0},
    "birch_tree": {"height": 300.0, "canopy_width": 120.0, "trunk_radius": 5.0},
    "palm_tree": {"height": 300.0, "frond_span": 120.0, "trunk_radius": 6.0},
    "dead_tree": {"height": 250.0, "trunk_radius": 6.0},
    "sapling": {"height": 40.0, "canopy_width": 20.0},
    "grass": {"width": 40.0, "height": 10.0},
    "bush": {"width": 60.0, "height": 40.0},
    "shrub": {"width": 60.0, "height": 60.0},
    "fern": {"width": 40.0, "height": 30.0},
    "flower": {"height": 15.0},
    "moss": {"width": 40.0, "depth": 30.0, "thickness": 4.0},
    "small_rock": {"width": 15.0, "depth": 12.0, "height": 10.0},
    "boulder": {"width": 80.0, "depth": 60.0, "height": 50.0},
    "rock_cluster": {"width": 60.0, "depth": 40.0},
    "cliff_section": {"width": 120.0, "depth": 60.0, "height": 120.0},
    "log": {"length": 60.0, "radius": 6.0},
    "tree_stump": {"radius": 10.0, "height": 10.0},
    "fallen_tree": {"length": 120.0, "trunk_radius": 6.0},
    "mushroom": {"cap_diameter": 8.0, "height": 6.0},
    "vine": {"length": 60.0},
    "root": {"width": 60.0, "depth": 40.0, "height": 10.0},
    "pond": {"width": 100.0, "depth": 80.0, "bank_height": 6.0},
    "river_segment": {"width": 60.0, "length": 120.0},
    "waterfall": {"width": 60.0, "height": 80.0, "pool_radius": 40.0},
    "stream": {"width": 20.0, "length": 80.0},
}

NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "single": 1,
    "double": 2,
    "triple": 3,
    "quad": 4,
}

COUNT_FIELD_HINTS = {
    "density",
    "layers",
    "branch_count",
    "stems",
    "fronds",
    "petals",
    "rocks",
    "leaf_density",
    "doors",
    "drawers",
    "shelves",
    "arms",
    "burners",
    "chair_count",
    "stools_count",
    "compartments",
    "bar_count",
    "step_count",
    "rung_count",
    "support_count",
    "section_count",
    "baluster_count",
    "pillar_count",
    "screen_count",
    "rack_units",
    "door_count",
    "barrel_count",
    "roller_count",
    "seat_count",
    "layer_count",
}

LOW_DENSITY_KEYWORDS = {
    "few",
    "light",
    "low",
    "minimal",
    "sparse",
    "thin",
}

MEDIUM_DENSITY_KEYWORDS = {
    "average",
    "medium",
    "moderate",
    "normal",
    "regular",
    "standard",
}

HIGH_DENSITY_KEYWORDS = {
    "abundant",
    "bushy",
    "clustered",
    "crowded",
    "dense",
    "full",
    "heavy",
    "high",
    "layered",
    "lush",
    "many",
    "thick",
}

LOW_SIZE_KEYWORDS = {
    "compact",
    "little",
    "narrow",
    "short",
    "shallow",
    "small",
    "slender",
    "thin",
    "tiny",
}

MEDIUM_SIZE_KEYWORDS = {
    "average",
    "medium",
    "moderate",
    "normal",
    "regular",
    "standard",
}

HIGH_SIZE_KEYWORDS = {
    "big",
    "broad",
    "deep",
    "giant",
    "huge",
    "large",
    "long",
    "spreading",
    "tall",
    "thick",
    "wide",
}


def infer_architecture_asset_type(lower_prompt: str):
    keyword_checks = [
        ("mansard roof", "roof"),
        ("hip roof", "roof"),
        ("gabled roof", "roof"),
        ("flat roof", "roof"),
        ("foot bridge", "bridge"),
        ("footbridge", "bridge"),
        ("bridge", "bridge"),
        ("front porch", "porch"),
        ("entry porch", "porch"),
        ("porch", "porch"),
        ("balcony", "balcony"),
        ("chimney", "chimney"),
        ("foundation slab", "foundation"),
        ("base slab", "foundation"),
        ("foundation", "foundation"),
        ("footing", "foundation"),
        ("staircase", "stairs"),
        ("stairway", "stairs"),
        ("stairs", "stairs"),
        ("ladder", "ladder"),
        ("handrail", "railing"),
        ("railing", "railing"),
        ("picket fence", "fence"),
        ("privacy fence", "fence"),
        ("fence", "fence"),
        ("access ramp", "ramp"),
        ("inclined ramp", "ramp"),
        ("ramp", "ramp"),
        ("support beam", "beam"),
        ("ceiling beam", "beam"),
        ("roof beam", "beam"),
        ("beam", "beam"),
        ("roof", "roof"),
        ("pillar", "pillar"),
        ("column", "pillar"),
        ("archway", "archway"),
        ("stone arch", "archway"),
        ("brick arch", "archway"),
        ("iron gate", "gate"),
        ("wood gate", "gate"),
        ("garden gate", "gate"),
        ("gate", "gate"),
        ("ceiling panel", "ceiling"),
        ("ceiling surface", "ceiling"),
        ("drop ceiling", "ceiling"),
        ("ceiling", "ceiling"),
        ("floor slab", "floor"),
        ("tile floor", "floor"),
        ("wood floor", "floor"),
        ("stone floor", "floor"),
        ("concrete floor", "floor"),
        ("brick wall", "wall"),
        ("stone wall", "wall"),
        ("concrete wall", "wall"),
        ("plaster wall", "wall"),
        ("wood wall", "wall"),
        ("partition wall", "wall"),
        ("interior wall", "wall"),
        ("wall section", "wall"),
        ("entry door", "door"),
        ("interior door", "door"),
        ("front door", "door"),
        ("door panel", "door"),
        ("door", "door"),
        ("glass window", "window"),
        ("window frame", "window"),
        ("window", "window"),
    ]
    for keyword, asset_type in keyword_checks:
        if keyword in lower_prompt:
            return asset_type
    return None


def infer_weapon_asset_type(lower_prompt: str):
    keyword_checks = [
        ("crossbow bolt", "bolt"),
        ("crossbow_bolt", "bolt"),
        ("magic staff", "magic_staff"),
        ("mage staff", "magic_staff"),
        ("wizard staff", "magic_staff"),
        ("arcane staff", "magic_staff"),
        ("poleaxe", "halberd"),
        ("pole axe", "halberd"),
        ("polearm", "halberd"),
        ("halberd", "halberd"),
        ("crossbow", "crossbow"),
        ("recurve bow", "bow"),
        ("longbow", "bow"),
        ("shortbow", "bow"),
        ("bow", "bow"),
        ("morningstar", "mace"),
        ("mace", "mace"),
        ("warhammer", "hammer"),
        ("war hammer", "hammer"),
        ("hammer", "hammer"),
        ("battleaxe", "axe"),
        ("battle axe", "axe"),
        ("hatchet", "axe"),
        ("axe", "axe"),
        ("dagger", "dagger"),
        ("dirk", "dagger"),
        ("stiletto", "dagger"),
        ("knife", "dagger"),
        ("spear", "spear"),
        ("pike", "spear"),
        ("javelin", "spear"),
        ("staff", "staff"),
        ("arrow", "arrow"),
        ("bolt", "bolt"),
        ("wand", "wand"),
        ("magic orb", "orb"),
        ("orb", "orb"),
        ("broadsword", "sword"),
        ("longsword", "sword"),
        ("shortsword", "sword"),
        ("sword", "sword"),
    ]
    for keyword, asset_type in keyword_checks:
        if keyword in lower_prompt:
            return asset_type
    return None


def infer_adventure_asset_type(lower_prompt: str):
    keyword_checks = [
        ("castle wall", "castle_wall"),
        ("fort wall", "castle_wall"),
        ("drawbridge", "drawbridge"),
        ("draw bridge", "drawbridge"),
        ("market stall", "market_stall"),
        ("blacksmith forge", "forge"),
        ("sleeping bag", "sleeping_bag"),
        ("sleeping_bag", "sleeping_bag"),
        ("cooking pot", "cooking_pot"),
        ("cook pot", "cooking_pot"),
        ("supply box", "supply_box"),
        ("camp fire", "campfire"),
        ("campfire", "campfire"),
        ("fire pit", "campfire"),
        ("watchtower", "tower"),
        ("watch tower", "tower"),
        ("breastplate", "chestplate"),
        ("chestplate", "chestplate"),
        ("cuirass", "chestplate"),
        ("gauntlets", "gauntlets"),
        ("gauntlet", "gauntlets"),
        ("boots", "boots"),
        ("boot", "boots"),
        ("backpack", "backpack"),
        ("rucksack", "backpack"),
        ("belt", "belt"),
        ("pouch", "pouch"),
        ("satchel", "pouch"),
        ("cloak", "cape"),
        ("cape", "cape"),
        ("tent", "tent"),
        ("lantern", "lantern"),
        ("throne", "throne"),
        ("banner", "banner"),
        ("well", "well"),
        ("wagon", "cart"),
        ("cart", "cart"),
        ("anvil", "anvil"),
        ("forge", "forge"),
        ("tower", "tower"),
    ]
    for keyword, asset_type in keyword_checks:
        if keyword in lower_prompt:
            return asset_type
    return None


def parse_number_from_text(value: str):
    stripped = str(value).strip().lower()
    if not stripped:
        return None

    range_matches = re.findall(r"-?\d+(?:\.\d+)?", stripped)
    if len(range_matches) >= 2 and any(token in stripped for token in (" to ", " between ", " range ", " - ")):
        first = float(range_matches[0])
        second = float(range_matches[1])
        midpoint = (first + second) / 2.0
        if any("." in match for match in range_matches[:2]):
            return midpoint
        return int(round(midpoint))

    numeric_match = re.search(r"-?\d+(?:\.\d+)?", stripped)
    if numeric_match:
        number_text = numeric_match.group(0)
        return float(number_text) if "." in number_text else int(number_text)

    if stripped in NUMBER_WORDS:
        return NUMBER_WORDS[stripped]

    tokens = re.split(r"[\s_-]+", stripped)
    for token in tokens:
        if token in NUMBER_WORDS:
            return NUMBER_WORDS[token]

    return None


def choose_bucket_value(bucket: str, minimum, maximum, default, as_int: bool):
    if minimum is None or maximum is None:
        return default

    if bucket == "low":
        value = minimum + (maximum - minimum) * 0.2
    elif bucket == "high":
        value = minimum + (maximum - minimum) * 0.8
    else:
        value = default if default is not None else minimum + (maximum - minimum) * 0.5

    if as_int:
        return int(round(value))
    return round(float(value), 1)


def infer_descriptor_bucket(text: str, field_name: str):
    normalized = f" {str(text or '').lower()} "
    keyword_source = normalized

    if field_name in COUNT_FIELD_HINTS:
        if any(f" {keyword} " in keyword_source for keyword in HIGH_DENSITY_KEYWORDS):
            return "high"
        if any(f" {keyword} " in keyword_source for keyword in LOW_DENSITY_KEYWORDS):
            return "low"
        if any(f" {keyword} " in keyword_source for keyword in MEDIUM_DENSITY_KEYWORDS):
            return "medium"
        return None

    if any(f" {keyword} " in keyword_source for keyword in HIGH_SIZE_KEYWORDS):
        return "high"
    if any(f" {keyword} " in keyword_source for keyword in LOW_SIZE_KEYWORDS):
        return "low"
    if any(f" {keyword} " in keyword_source for keyword in MEDIUM_SIZE_KEYWORDS):
        return "medium"
    return None


def coerce_schema_field_values(asset_type: str, repaired: Dict[str, Any], user_prompt: str = "") -> Dict[str, Any]:
    schema_model = SCHEMA_BY_ASSET_TYPE.get(asset_type)
    if schema_model is None:
        return repaired

    json_schema = schema_model.model_json_schema()
    properties = json_schema.get("properties", {})

    for field_name, field_schema in properties.items():
        if field_name not in repaired:
            continue

        current_value = repaired[field_name]
        if not isinstance(current_value, str):
            continue

        schema_type = field_schema.get("type")
        numeric_like = parse_number_from_text(current_value)

        if schema_type == "integer":
            if numeric_like is not None:
                repaired[field_name] = int(round(float(numeric_like)))
                continue

            bucket = infer_descriptor_bucket(f"{current_value} {user_prompt}", field_name)
            if bucket:
                repaired[field_name] = choose_bucket_value(
                    bucket,
                    field_schema.get("minimum"),
                    field_schema.get("maximum"),
                    field_schema.get("default"),
                    True,
                )
        elif schema_type == "number":
            if numeric_like is not None:
                repaired[field_name] = float(numeric_like)
                continue

            bucket = infer_descriptor_bucket(f"{current_value} {user_prompt}", field_name)
            if bucket:
                repaired[field_name] = choose_bucket_value(
                    bucket,
                    field_schema.get("minimum"),
                    field_schema.get("maximum"),
                    field_schema.get("default"),
                    False,
                )

    return repaired


def get_schema_field_spec(asset_type: str, field_name: str):
    schema_model = SCHEMA_BY_ASSET_TYPE.get(asset_type)
    if schema_model is None:
        return None
    return schema_model.model_json_schema().get("properties", {}).get(field_name)


def should_convert_cm_value_from_meters(asset_type: str, field_name: str, value) -> bool:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
        return False

    field_schema = get_schema_field_spec(asset_type, field_name)
    if not field_schema:
        return value < 3.5

    reference_scale = None
    for candidate_key in ("minimum", "default", "maximum"):
        candidate = field_schema.get(candidate_key)
        if isinstance(candidate, (int, float)) and candidate > 0:
            reference_scale = float(candidate)
            break

    if reference_scale is None:
        return value < 3.5

    # Treat bare numeric values as meters only when they are far below the
    # field's expected centimeter scale, e.g. 1.6 for a 160 cm river width.
    return float(value) < reference_scale * 0.2


def clamp_numeric_values_to_schema(asset_type: str, repaired: Dict[str, Any]) -> Dict[str, Any]:
    schema_model = SCHEMA_BY_ASSET_TYPE.get(asset_type)
    if schema_model is None:
        return repaired

    properties = schema_model.model_json_schema().get("properties", {})
    for field_name, field_schema in properties.items():
        if field_name not in repaired:
            continue

        current_value = repaired[field_name]
        if not isinstance(current_value, (int, float)) or isinstance(current_value, bool):
            continue

        schema_type = field_schema.get("type")
        if schema_type not in {"integer", "number"}:
            continue

        minimum = field_schema.get("minimum")
        maximum = field_schema.get("maximum")
        clamped_value = float(current_value)

        if isinstance(minimum, (int, float)) and clamped_value < minimum:
            clamped_value = float(minimum)
        if isinstance(maximum, (int, float)) and clamped_value > maximum:
            clamped_value = float(maximum)

        if clamped_value != float(current_value):
            logger.info(
                "Clamping %s %s from %s to %s to fit schema bounds",
                asset_type,
                field_name,
                current_value,
                clamped_value,
            )

        if schema_type == "integer":
            repaired[field_name] = int(round(clamped_value))
        else:
            repaired[field_name] = round(clamped_value, 1)

    return repaired

def infer_nature_asset_type(lower_prompt: str):
    keyword_checks = [
        ("waterfall", "waterfall"),
        ("river segment", "river_segment"),
        ("river", "river_segment"),
        ("stream", "stream"),
        ("creek", "stream"),
        ("brook", "stream"),
        ("pond", "pond"),
        ("oak tree", "oak_tree"),
        ("pine tree", "pine_tree"),
        ("birch tree", "birch_tree"),
        ("palm tree", "palm_tree"),
        ("dead tree", "dead_tree"),
        ("fallen tree", "fallen_tree"),
        ("tree stump", "tree_stump"),
        ("sapling", "sapling"),
        ("rock cluster", "rock_cluster"),
        ("small rock", "small_rock"),
        ("boulder", "boulder"),
        ("cliff section", "cliff_section"),
        ("cliff", "cliff_section"),
        ("mushroom", "mushroom"),
        ("fern", "fern"),
        ("shrub", "shrub"),
        ("bush", "bush"),
        ("grass", "grass"),
        ("moss", "moss"),
        ("flower", "flower"),
        ("vine", "vine"),
        ("ivy", "vine"),
        ("tree root", "root"),
        ("root", "root"),
        ("log", "log"),
    ]
    for keyword, asset_type in keyword_checks:
        if keyword in lower_prompt:
            return asset_type
    return None


def infer_world_asset_type(lower_prompt: str):
    keyword_checks = [
        ("2d game background", "game_background_2d"),
        ("video game background", "game_background_2d"),
        ("parallax background", "game_background_2d"),
        ("side scroller background", "game_background_2d"),
        ("side-scroller background", "game_background_2d"),
        ("platformer background", "game_background_2d"),
        ("2d background", "game_background_2d"),
        ("battle tank", "battle_tank"),
        ("military tank", "battle_tank"),
        ("armored tank", "battle_tank"),
        ("armoured tank", "battle_tank"),
        ("treasure chest", "treasure_chest"),
        ("tech crate", "tech_crate"),
        ("sci-fi crate", "tech_crate"),
        ("sci fi crate", "tech_crate"),
        ("futuristic crate", "tech_crate"),
        ("server rack", "server_rack"),
        ("energy cell", "energy_cell"),
        ("space door", "space_door"),
        ("air lock", "airlock"),
        ("conveyor belt", "conveyor_belt"),
        ("storage rack", "storage_rack"),
        ("street lamp", "street_lamp"),
        ("traffic light", "traffic_light"),
        ("road sign", "road_sign"),
        ("street bench", "street_bench"),
        ("city bench", "street_bench"),
        ("urban bench", "street_bench"),
        ("bus stop", "bus_stop"),
        ("phone booth", "phone_booth"),
        ("road tile", "road_tile"),
        ("ground tile", "ground_tile"),
        ("path tile", "path_tile"),
        ("river tile", "river_tile"),
        ("dungeon tile", "dungeon_tile"),
        ("control panel", "control_panel"),
        ("terminal", "terminal"),
        ("computer", "computer"),
        ("turret", "turret"),
        ("drone", "drone"),
        ("pipe", "pipe"),
        ("valve", "valve"),
        ("generator", "generator"),
        ("toolbox", "toolbox"),
        ("forklift", "forklift"),
        ("mailbox", "mailbox"),
        ("trash can", "trash_can"),
        ("car", "car"),
        ("truck", "truck"),
        ("motorcycle", "motorcycle"),
        ("motorbike", "motorcycle"),
        ("bike", "bike"),
        ("bicycle", "bike"),
        ("tractor", "tractor"),
        ("boat", "boat"),
        ("canoe", "canoe"),
        ("ship", "ship"),
        ("airplane", "plane"),
        ("aeroplane", "plane"),
        ("plane", "plane"),
        ("helicopter", "helicopter"),
        ("merchant", "merchant"),
        ("blacksmith", "blacksmith"),
        ("soldier", "soldier"),
        ("guard", "guard"),
        ("farmer", "farmer"),
        ("elder", "elder"),
        ("child", "child"),
        ("female", "female"),
        ("male", "male"),
        ("elf", "elf"),
        ("orc", "orc"),
        ("goblin", "goblin"),
        ("dwarf", "dwarf"),
        ("dragon", "dragon"),
        ("dog", "dog"),
        ("cat", "cat"),
        ("horse", "horse"),
        ("cow", "cow"),
        ("deer", "deer"),
        ("wolf", "wolf"),
        ("bird", "bird"),
        ("fish", "fish"),
        ("coin", "coin"),
        ("gem", "gem"),
        ("key", "key"),
        ("scroll", "scroll"),
        ("potion", "potion"),
        ("artifact", "artifact"),
        ("terrain", "terrain"),
        ("hill", "hill"),
        ("mountain", "mountain"),
        ("cliff", "cliff"),
        ("valley", "valley"),
        ("cave", "cave"),
    ]
    for keyword, asset_type in keyword_checks:
        if re.search(rf"\b{re.escape(keyword)}\b", lower_prompt):
            return asset_type
    return None


def find_first_prompt_keyword(lower_prompt: str, choices):
    for choice in choices:
        spaced_choice = choice.replace("_", " ")
        if re.search(rf"\b{re.escape(spaced_choice)}\b", lower_prompt):
            return choice
    return None


def apply_world_prompt_overrides(asset_type: str, repaired: Dict[str, Any], lower_prompt: str):
    tech_colors = ["blue", "cyan", "green", "red", "yellow", "purple", "white"]
    vehicle_colors = ["red", "blue", "green", "yellow", "white", "black", "silver", "gray", "orange", "olive", "sand"]
    character_colors = ["red", "blue", "green", "brown", "black", "white", "gray"]
    animal_colors = ["brown", "black", "white", "golden", "gray", "orange", "tan"]
    background_themes = ["forest", "desert", "city", "cave", "snow", "space", "volcanic"]
    background_times = ["day", "sunset", "night", "dawn"]

    if asset_type == "game_background_2d":
        theme_choice = find_first_prompt_keyword(lower_prompt, background_themes)
        time_choice = find_first_prompt_keyword(lower_prompt, background_times)
        if theme_choice:
            repaired["theme"] = theme_choice
        if time_choice:
            repaired["time_of_day"] = time_choice
        if "moon" in lower_prompt or "sun" in lower_prompt or "planet" in lower_prompt or "stars" in lower_prompt:
            repaired["has_celestial"] = True
        if "no moon" in lower_prompt or "no sun" in lower_prompt or "without moon" in lower_prompt:
            repaired["has_celestial"] = False
        if "parallax" in lower_prompt or "layered" in lower_prompt:
            repaired["layer_count"] = max(5, int(repaired.get("layer_count", 4)))
        if "space" in lower_prompt:
            repaired["theme"] = "space"
            repaired["has_celestial"] = True
        elif "snow" in lower_prompt or "icy" in lower_prompt:
            repaired["theme"] = "snow"
        elif "volcano" in lower_prompt or "lava" in lower_prompt:
            repaired["theme"] = "volcanic"
        return

    if asset_type in {"control_panel", "terminal", "computer", "server_rack", "energy_cell", "tech_crate", "space_door", "airlock", "turret", "drone", "generator", "road_sign", "phone_booth"}:
        color_choice = find_first_prompt_keyword(lower_prompt, tech_colors)
        if color_choice:
            accent_field = "accent_color" if "accent_color" in SCHEMA_BY_ASSET_TYPE[asset_type].model_json_schema().get("properties", {}) else None
            if accent_field:
                repaired[accent_field] = color_choice

    if asset_type in {"pipe", "valve", "tank", "conveyor_belt", "toolbox", "forklift", "storage_rack", "street_lamp", "traffic_light", "mailbox", "trash_can", "bus_stop"}:
        if "steel" in lower_prompt:
            repaired["material"] = "steel"
        elif "aluminum" in lower_prompt or "aluminium" in lower_prompt:
            repaired["material"] = "aluminum"
        elif "iron" in lower_prompt and asset_type in {"pipe", "valve", "tank"}:
            repaired["material"] = "iron"

    if asset_type == "space_door":
        if "iris" in lower_prompt:
            repaired["door_style"] = "iris"
        elif "sliding" in lower_prompt:
            repaired["door_style"] = "sliding"
    elif asset_type == "terminal":
        if "wall" in lower_prompt:
            repaired["terminal_style"] = "wall"
    elif asset_type == "computer":
        if "laptop" in lower_prompt:
            repaired["computer_style"] = "laptop"
        elif "desktop" in lower_prompt:
            repaired["computer_style"] = "desktop"
    elif asset_type == "drone":
        if "hex" in lower_prompt or "six rotor" in lower_prompt:
            repaired["drone_style"] = "hex"
    elif asset_type == "pipe":
        if "elbow" in lower_prompt or "corner pipe" in lower_prompt:
            repaired["pipe_style"] = "elbow"
    elif asset_type == "valve":
        if "lever" in lower_prompt:
            repaired["handle_style"] = "lever"
    elif asset_type == "tank":
        if "horizontal" in lower_prompt:
            repaired["orientation"] = "horizontal"
        elif "vertical" in lower_prompt:
            repaired["orientation"] = "vertical"
    elif asset_type == "traffic_light":
        light = find_first_prompt_keyword(lower_prompt, ["red", "yellow", "green"])
        if light:
            repaired["active_light"] = light
        if "horizontal" in lower_prompt:
            repaired["orientation"] = "horizontal"
    elif asset_type == "road_sign":
        if "circle" in lower_prompt or "round" in lower_prompt:
            repaired["sign_shape"] = "circle"
        elif "triangle" in lower_prompt:
            repaired["sign_shape"] = "triangle"
    elif asset_type == "street_bench":
        if "without back" in lower_prompt or "no backrest" in lower_prompt:
            repaired["has_backrest"] = False
    elif asset_type == "mailbox":
        if "wall mounted" in lower_prompt or "wall mailbox" in lower_prompt:
            repaired["mailbox_style"] = "wall"
    elif asset_type == "trash_can":
        if "without lid" in lower_prompt or "open top" in lower_prompt:
            repaired["has_lid"] = False
    elif asset_type == "bus_stop":
        if "without bench" in lower_prompt:
            repaired["has_bench"] = False
    elif asset_type == "phone_booth":
        if "enclosed" in lower_prompt:
            repaired["booth_style"] = "enclosed"

    if asset_type in {"car", "truck", "motorcycle", "tractor", "battle_tank", "plane", "helicopter"}:
        color_choice = find_first_prompt_keyword(lower_prompt, vehicle_colors)
        if color_choice:
            repaired["body_color"] = color_choice
    if asset_type == "car":
        style = find_first_prompt_keyword(lower_prompt, ["sedan", "hatchback", "suv"])
        if style:
            repaired["body_style"] = style
    elif asset_type == "truck":
        style = find_first_prompt_keyword(lower_prompt, ["pickup", "box", "semi"])
        if style:
            repaired["truck_style"] = style
        if "cargo" in lower_prompt or "loaded" in lower_prompt:
            repaired["has_cargo"] = True
    elif asset_type == "bike":
        style = find_first_prompt_keyword(lower_prompt, ["road", "mountain", "city"])
        if style:
            repaired["bike_style"] = style
        color_choice = find_first_prompt_keyword(lower_prompt, vehicle_colors)
        if color_choice:
            repaired["frame_color"] = color_choice
        if "basket" in lower_prompt:
            repaired["has_basket"] = True
    elif asset_type == "motorcycle":
        style = find_first_prompt_keyword(lower_prompt, ["sport", "cruiser", "dirt"])
        if style:
            repaired["motorcycle_style"] = style
        if "without windshield" in lower_prompt:
            repaired["has_windshield"] = False
    elif asset_type == "tractor":
        if "open cab" in lower_prompt or "without cab" in lower_prompt:
            repaired["has_cab"] = False
    elif asset_type == "battle_tank":
        style = find_first_prompt_keyword(lower_prompt, ["angular", "rounded"])
        if style:
            repaired["turret_style"] = style
    elif asset_type == "boat":
        style = find_first_prompt_keyword(lower_prompt, ["motorboat", "rowboat", "sailboat"])
        if style:
            repaired["boat_style"] = style
        if "canopy" in lower_prompt:
            repaired["has_canopy"] = True
    elif asset_type == "canoe":
        if "fiberglass" in lower_prompt:
            repaired["material"] = "fiberglass"
        elif "wood" in lower_prompt:
            repaired["material"] = "wood"
    elif asset_type == "ship":
        style = find_first_prompt_keyword(lower_prompt, ["cargo", "sailing", "warship"])
        if style:
            repaired["ship_style"] = style
    elif asset_type == "plane":
        style = find_first_prompt_keyword(lower_prompt, ["prop", "jet"])
        if style:
            repaired["plane_style"] = style
    elif asset_type == "helicopter":
        if "without skid" in lower_prompt or "wheels" in lower_prompt:
            repaired["has_skids"] = False

    if asset_type in {"male", "female", "child", "elder", "merchant", "guard", "farmer", "blacksmith", "soldier", "elf", "orc", "goblin", "dwarf"}:
        skin = find_first_prompt_keyword(lower_prompt, ["light", "medium", "dark"])
        outfit = find_first_prompt_keyword(lower_prompt, character_colors)
        if skin:
            repaired["skin_tone"] = skin
        if outfit:
            repaired["outfit_color"] = outfit
    elif asset_type == "dragon":
        color_choice = find_first_prompt_keyword(lower_prompt, ["red", "green", "blue", "black", "gray", "brown"])
        if color_choice:
            repaired["scale_color"] = color_choice
        pose = find_first_prompt_keyword(lower_prompt, ["standing", "flying", "perched"])
        if pose:
            repaired["pose"] = pose

    if asset_type in {"dog", "cat", "horse", "cow", "deer", "wolf"}:
        fur = find_first_prompt_keyword(lower_prompt, animal_colors)
        if fur:
            repaired["fur_color"] = fur
    elif asset_type == "bird":
        color_choice = find_first_prompt_keyword(lower_prompt, ["red", "blue", "green", "yellow", "white", "black", "gray", "orange"])
        style = find_first_prompt_keyword(lower_prompt, ["perched", "flying", "songbird"])
        if color_choice:
            repaired["body_color"] = color_choice
        if style:
            repaired["bird_style"] = style
    elif asset_type == "fish":
        color_choice = find_first_prompt_keyword(lower_prompt, ["red", "blue", "green", "yellow", "white", "black", "gray", "orange", "silver"])
        style = find_first_prompt_keyword(lower_prompt, ["stream", "tropical", "shark"])
        if color_choice:
            repaired["body_color"] = color_choice
        if style:
            repaired["fish_style"] = style

    if asset_type == "gem":
        color_choice = find_first_prompt_keyword(lower_prompt, ["red", "blue", "green", "yellow", "purple", "white"])
        if color_choice:
            repaired["gem_color"] = color_choice
    elif asset_type == "key":
        mat = find_first_prompt_keyword(lower_prompt, ["gold", "bronze", "steel"])
        if mat:
            repaired["material"] = mat
    elif asset_type == "scroll":
        if "untied" in lower_prompt or "open scroll" in lower_prompt:
            repaired["tied"] = False
    elif asset_type == "potion":
        color_choice = find_first_prompt_keyword(lower_prompt, ["red", "blue", "green"])
        if color_choice:
            repaired["liquid_color"] = color_choice
    elif asset_type == "treasure_chest":
        if "without gem" in lower_prompt or "plain lid" in lower_prompt:
            repaired["has_gems"] = False
    elif asset_type == "artifact":
        style = find_first_prompt_keyword(lower_prompt, ["obelisk", "orb"])
        if style:
            repaired["artifact_style"] = style
    elif asset_type == "terrain":
        material = find_first_prompt_keyword(lower_prompt, ["grass", "dirt", "stone"])
        if material:
            repaired["material"] = material

class PromptProcessor:
    def __init__(self, ollama_client: OllamaClient = None):
        self.client = ollama_client or OllamaClient()
        
    def repair_units(self, data: Dict[str, Any], user_prompt: str = "") -> Dict[str, Any]:
        """Intelligently detects and repairs unit discrepancies in the raw JSON output.
        
        Example: If the LLM generates 80cm instead of 0.8m for a barrel, this function 
        detects that 80 is far out of bounds for meters and divides it by 100.
        """
        repaired = data.copy()
        
        # Normalize common key variations from LLM output
        if "type" in repaired and "asset_type" not in repaired:
            repaired["asset_type"] = repaired.pop("type")
        if "legs" in repaired and "leg_style" not in repaired:
            repaired["leg_style"] = repaired.pop("legs")
            
        # Normalize asset_type string values to match schema asset_type literals
        if "asset_type" in repaired and isinstance(repaired["asset_type"], str):
            asset_type_lower = repaired["asset_type"].lower()
            asset_type_spaced = asset_type_lower.replace("_", " ")
            if asset_type_lower in ["refrigerator", "freezer"]:
                repaired["asset_type"] = "fridge"
            elif asset_type_lower in ["cooktop", "range", "stove top"]:
                repaired["asset_type"] = "stove"
            elif asset_type_lower in ["baking oven", "toaster oven"]:
                repaired["asset_type"] = "oven"
            elif asset_type_lower in ["basin", "washbasin"]:
                repaired["asset_type"] = "sink"
            elif asset_type_lower in ["counter"]:
                repaired["asset_type"] = "countertop"
            elif asset_type_lower in ["island", "kitchen island", "kitchen_island"]:
                repaired["asset_type"] = "kitchen_island"
            elif asset_type_lower in ["dining set", "dining_set"]:
                repaired["asset_type"] = "dining_set"
            elif asset_type_lower in ["cupboard"]:
                repaired["asset_type"] = "cupboard"
            elif asset_type_lower in ["commode"]:
                repaired["asset_type"] = "toilet"
            elif asset_type_lower in ["tub", "bath tub"]:
                repaired["asset_type"] = "bathtub"
            elif asset_type_lower in ["shower stall", "shower cabin"]:
                repaired["asset_type"] = "shower"
            elif asset_type_lower in ["mirror", "looking glass"]:
                repaired["asset_type"] = "mirror"
            elif asset_type_lower in ["towel rack", "towel bar", "towel rail", "towel_rack"]:
                repaired["asset_type"] = "towel_rack"
            elif asset_type_lower in ["lamp", "table lamp", "floor lamp", "desk lamp"]:
                repaired["asset_type"] = "lamp"
            elif asset_type_lower in ["chandelier", "hanging light", "pendant light"]:
                repaired["asset_type"] = "chandelier"
            elif asset_type_lower in ["painting", "canvas", "artwork", "art"]:
                repaired["asset_type"] = "painting"
            elif asset_type_lower in ["picture frame", "picture_frame", "photo frame", "frame"]:
                repaired["asset_type"] = "picture_frame"
            elif asset_type_lower in ["clock", "timepiece", "wall clock"]:
                repaired["asset_type"] = "clock"
            elif asset_type_lower in ["vase", "urn", "flower holder"]:
                repaired["asset_type"] = "vase"
            elif asset_type_lower in ["plant_pot", "plant pot", "flowerpot", "flower pot", "pot"]:
                repaired["asset_type"] = "plant_pot"
            elif asset_type_lower in ["rug", "carpet", "mat"]:
                repaired["asset_type"] = "rug"
            elif asset_type_lower in ARCHITECTURE_TYPE_ALIASES:
                repaired["asset_type"] = ARCHITECTURE_TYPE_ALIASES[asset_type_lower]
            elif asset_type_spaced in ARCHITECTURE_TYPE_ALIASES:
                repaired["asset_type"] = ARCHITECTURE_TYPE_ALIASES[asset_type_spaced]
            elif asset_type_lower in WEAPON_TYPE_ALIASES:
                repaired["asset_type"] = WEAPON_TYPE_ALIASES[asset_type_lower]
            elif asset_type_spaced in WEAPON_TYPE_ALIASES:
                repaired["asset_type"] = WEAPON_TYPE_ALIASES[asset_type_spaced]
            elif asset_type_lower in ADVENTURE_TYPE_ALIASES:
                repaired["asset_type"] = ADVENTURE_TYPE_ALIASES[asset_type_lower]
            elif asset_type_spaced in ADVENTURE_TYPE_ALIASES:
                repaired["asset_type"] = ADVENTURE_TYPE_ALIASES[asset_type_spaced]
            elif asset_type_lower in WORLD_TYPE_ALIASES:
                repaired["asset_type"] = WORLD_TYPE_ALIASES[asset_type_lower]
            elif asset_type_spaced in WORLD_TYPE_ALIASES:
                repaired["asset_type"] = WORLD_TYPE_ALIASES[asset_type_spaced]
            elif asset_type_lower in NATURE_TYPE_ALIASES:
                repaired["asset_type"] = NATURE_TYPE_ALIASES[asset_type_lower]
            elif asset_type_spaced in NATURE_TYPE_ALIASES:
                repaired["asset_type"] = NATURE_TYPE_ALIASES[asset_type_spaced]
            elif "tree" in asset_type_lower:
                inferred_nature = infer_nature_asset_type(user_prompt.lower()) if user_prompt else None
                if inferred_nature:
                    repaired["asset_type"] = inferred_nature
            elif asset_type_lower == "lighting":
                # Intercept old lighting asset type and map to specific generators based on prompt keywords
                lower_p = user_prompt.lower()
                if "chandelier" in lower_p:
                    repaired["asset_type"] = "chandelier"
                elif "lamp" in lower_p:
                    repaired["asset_type"] = "lamp"
                else:
                    repaired["asset_type"] = "lighting"
            else:
                repaired["asset_type"] = asset_type_lower
            
        asset_type = repaired.get("asset_type")
        if not asset_type:
            return repaired
            
        # Apply keyword overrides for style variations if explicitly mentioned in user prompt
        if user_prompt:
            lower_prompt = user_prompt.lower()
            if "round" in lower_prompt:
                if asset_type in ["table", "dining_table", "chair"]:
                    repaired["leg_style"] = "round"
            elif "square" in lower_prompt:
                if asset_type in ["table", "dining_table", "chair"]:
                    repaired["leg_style"] = "square"
            elif "turned" in lower_prompt:
                if asset_type == "dining_table":
                    repaired["leg_style"] = "turned"
            elif "block" in lower_prompt:
                if asset_type == "coffee_table":
                    repaired["leg_style"] = "block"
            elif "hairpin" in lower_prompt:
                if asset_type in ["coffee_table", "stool"]:
                    repaired["leg_style"] = "hairpin"
            elif "x_frame" in lower_prompt or "x-frame" in lower_prompt or "x frame" in lower_prompt:
                if asset_type == "bench":
                    repaired["leg_style"] = "x_frame"
            elif "straight" in lower_prompt:
                if asset_type == "bench":
                    repaired["leg_style"] = "straight"

            if asset_type == "wall":
                if "window" in lower_prompt:
                    repaired["opening_type"] = "window"
                elif "door" in lower_prompt:
                    repaired["opening_type"] = "door"
                if "trim" in lower_prompt:
                    repaired["has_trim"] = True
                for material_name in ["brick", "concrete", "stone", "wood", "plaster"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "floor":
                for material_name in ["wood", "stone", "tile", "concrete"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "ceiling":
                if "trim" in lower_prompt:
                    repaired["has_trim"] = True
                for material_name in ["plaster", "wood", "concrete"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "roof":
                if "hip roof" in lower_prompt:
                    repaired["roof_style"] = "hip"
                elif "mansard roof" in lower_prompt:
                    repaired["roof_style"] = "mansard"
                elif "flat roof" in lower_prompt:
                    repaired["roof_style"] = "flat"
                elif "gabled roof" in lower_prompt or "gable roof" in lower_prompt:
                    repaired["roof_style"] = "gabled"
                for material_name in ["clay tiles", "wood shingles", "metal sheets"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name.replace(" ", "_")
                        break
            elif asset_type == "pillar":
                if "square" in lower_prompt:
                    repaired["shape"] = "square"
                elif "cylindrical" in lower_prompt or "round" in lower_prompt or "column" in lower_prompt:
                    repaired["shape"] = "cylindrical"
                if "plain" in lower_prompt and "capital" not in lower_prompt:
                    repaired["has_capital"] = False
                elif "capital" in lower_prompt or "base" in lower_prompt:
                    repaired["has_capital"] = True
                for material_name in ["stone", "marble", "concrete", "wood"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "beam":
                for material_name in ["wood", "steel", "concrete"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "foundation":
                if "no footing" in lower_prompt or "without footing" in lower_prompt or "without footings" in lower_prompt:
                    repaired["has_footings"] = False
                elif "footing" in lower_prompt or "footings" in lower_prompt:
                    repaired["has_footings"] = True
                for material_name in ["concrete", "stone"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "door":
                if "plain" in lower_prompt or "flush" in lower_prompt:
                    repaired["panel_style"] = "plain"
                elif "double" in lower_prompt:
                    repaired["panel_style"] = "double"
                elif "inset" in lower_prompt or "panel" in lower_prompt or "paneled" in lower_prompt:
                    repaired["panel_style"] = "inset"
                if "frameless" in lower_prompt or "without frame" in lower_prompt:
                    repaired["has_frame"] = False
                elif "frame" in lower_prompt:
                    repaired["has_frame"] = True
                if "handleless" in lower_prompt or "without handle" in lower_prompt:
                    repaired["has_handle"] = False
                elif "handle" in lower_prompt:
                    repaired["has_handle"] = True
                for material_name in ["wood", "metal"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "window":
                if "without mullion" in lower_prompt or "without mullions" in lower_prompt:
                    repaired["has_mullions"] = False
                elif "mullion" in lower_prompt or "grille" in lower_prompt or "grid" in lower_prompt:
                    repaired["has_mullions"] = True
                if "without sill" in lower_prompt or "frameless sill" in lower_prompt:
                    repaired["has_sill"] = False
                elif "sill" in lower_prompt:
                    repaired["has_sill"] = True
                if "aluminum" in lower_prompt or "aluminium" in lower_prompt or "metal frame" in lower_prompt:
                    repaired["frame_material"] = "aluminum"
                elif "wood" in lower_prompt:
                    repaired["frame_material"] = "wood"
            elif asset_type == "archway":
                for material_name in ["stone", "brick"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "gate":
                if "solid" in lower_prompt or "panel" in lower_prompt:
                    repaired["gate_style"] = "solid"
                elif "bar" in lower_prompt or "slat" in lower_prompt or "picket" in lower_prompt:
                    repaired["gate_style"] = "barred"
                for material_name in ["wood", "iron"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "stairs":
                if "without railing" in lower_prompt or "open stair" in lower_prompt:
                    repaired["has_railing"] = False
                elif "railing" in lower_prompt or "handrail" in lower_prompt:
                    repaired["has_railing"] = True
                for material_name in ["wood", "stone", "concrete"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "ladder":
                for material_name in ["wood", "metal"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "ramp":
                if "without curb" in lower_prompt or "without curbs" in lower_prompt or "flush edges" in lower_prompt:
                    repaired["has_side_curbs"] = False
                elif "curb" in lower_prompt or "curbs" in lower_prompt or "edge lip" in lower_prompt:
                    repaired["has_side_curbs"] = True
                for material_name in ["wood", "concrete", "stone"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "bridge":
                if "without railing" in lower_prompt or "without railings" in lower_prompt:
                    repaired["has_railings"] = False
                elif "railing" in lower_prompt or "railings" in lower_prompt:
                    repaired["has_railings"] = True
                for material_name in ["wood", "stone", "steel"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "balcony":
                if "without railing" in lower_prompt or "without railings" in lower_prompt:
                    repaired["has_railings"] = False
                elif "railing" in lower_prompt or "railings" in lower_prompt:
                    repaired["has_railings"] = True
                for material_name in ["wood", "stone", "concrete"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "fence":
                if "panel" in lower_prompt or "privacy" in lower_prompt or "solid" in lower_prompt:
                    repaired["fence_style"] = "panel"
                elif "picket" in lower_prompt or "slat" in lower_prompt or "bar" in lower_prompt:
                    repaired["fence_style"] = "picket"
                for material_name in ["wood", "iron"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "railing":
                for material_name in ["wood", "steel"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "chimney":
                if "without cap" in lower_prompt or "open top" in lower_prompt:
                    repaired["has_cap"] = False
                elif "cap" in lower_prompt:
                    repaired["has_cap"] = True
                for material_name in ["brick", "stone"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "porch":
                if "without steps" in lower_prompt or "step-free" in lower_prompt:
                    repaired["has_steps"] = False
                elif "steps" in lower_prompt:
                    repaired["has_steps"] = True
                for material_name in ["wood", "stone", "concrete"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type in ["sword", "dagger"]:
                if "without guard" in lower_prompt or "guardless" in lower_prompt:
                    repaired["crossguard_type"] = "none"
                elif "curved guard" in lower_prompt or "curved crossguard" in lower_prompt:
                    repaired["crossguard_type"] = "curved"
                elif "straight guard" in lower_prompt or "simple guard" in lower_prompt:
                    repaired["crossguard_type"] = "simple"
                for material_name in ["leather", "wood", "metal"]:
                    if material_name in lower_prompt:
                        repaired["grip_material"] = material_name
                        break
            elif asset_type == "axe":
                if "double" in lower_prompt:
                    repaired["axe_style"] = "double"
                elif "single" in lower_prompt:
                    repaired["axe_style"] = "single"
                for material_name in ["steel", "brass"]:
                    if material_name in lower_prompt:
                        repaired["head_material"] = material_name
                        break
                if "metal handle" in lower_prompt or "metal shaft" in lower_prompt:
                    repaired["shaft_material"] = "metal"
                elif "wood" in lower_prompt:
                    repaired["shaft_material"] = "wood"
            elif asset_type == "hammer":
                for material_name in ["steel", "brass", "stone"]:
                    if material_name in lower_prompt:
                        repaired["head_material"] = material_name
                        break
                if "metal handle" in lower_prompt:
                    repaired["handle_material"] = "metal"
                elif "wood" in lower_prompt:
                    repaired["handle_material"] = "wood"
            elif asset_type == "mace":
                for material_name in ["iron", "steel", "brass"]:
                    if material_name in lower_prompt:
                        repaired["head_material"] = material_name
                        break
                if "metal shaft" in lower_prompt or "metal handle" in lower_prompt:
                    repaired["shaft_material"] = "metal"
                elif "wood" in lower_prompt:
                    repaired["shaft_material"] = "wood"
                if "morningstar" in lower_prompt or "spiked" in lower_prompt:
                    repaired["flange_count"] = max(int(repaired.get("flange_count", 6)), 8)
            elif asset_type == "spear":
                if "metal shaft" in lower_prompt:
                    repaired["shaft_material"] = "metal"
                elif "wood" in lower_prompt:
                    repaired["shaft_material"] = "wood"
                for material_name in ["steel", "iron", "brass"]:
                    if material_name in lower_prompt:
                        repaired["tip_material"] = material_name
                        break
            elif asset_type == "halberd":
                if "metal shaft" in lower_prompt:
                    repaired["shaft_material"] = "metal"
                elif "wood" in lower_prompt:
                    repaired["shaft_material"] = "wood"
                for material_name in ["steel", "iron", "brass"]:
                    if material_name in lower_prompt:
                        repaired["head_material"] = material_name
                        break
            elif asset_type == "staff":
                if "ring" in lower_prompt:
                    repaired["tip_style"] = "ring"
                elif "carved" in lower_prompt or "gnarled" in lower_prompt:
                    repaired["tip_style"] = "carved"
                elif "plain" in lower_prompt or "simple" in lower_prompt:
                    repaired["tip_style"] = "plain"
                for material_name in ["darkwood", "bone", "wood"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "bow":
                if "recurve" in lower_prompt:
                    repaired["bow_style"] = "recurve"
                elif "shortbow" in lower_prompt or "short bow" in lower_prompt:
                    repaired["bow_style"] = "shortbow"
                elif "longbow" in lower_prompt or "long bow" in lower_prompt:
                    repaired["bow_style"] = "longbow"
                for material_name in ["darkwood", "bone", "wood"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "crossbow":
                if "without bolt" in lower_prompt or "unloaded" in lower_prompt:
                    repaired["has_bolt"] = False
                elif "loaded" in lower_prompt or "with bolt" in lower_prompt:
                    repaired["has_bolt"] = True
                if "darkwood stock" in lower_prompt or "dark wood stock" in lower_prompt:
                    repaired["material"] = "darkwood"
                elif "wood stock" in lower_prompt or "wooden stock" in lower_prompt:
                    repaired["material"] = "wood"
                elif "steel stock" in lower_prompt or "metal stock" in lower_prompt:
                    repaired["material"] = "steel"
                else:
                    for material_name in ["darkwood", "wood", "steel"]:
                        if material_name in lower_prompt:
                            repaired["material"] = material_name
                            break
            elif asset_type in ["arrow", "bolt"]:
                for material_name in ["obsidian", "steel", "brass"]:
                    if material_name in lower_prompt:
                        repaired["tip_material"] = material_name
                        break
                for material_name in ["darkwood", "bone", "wood"]:
                    if material_name in lower_prompt:
                        repaired["shaft_material"] = material_name
                        break
                for color_name in ["white", "red", "black", "green", "blue"]:
                    if color_name in lower_prompt:
                        repaired["fletching_color"] = color_name
                        break
            elif asset_type == "magic_staff":
                if "crystal" in lower_prompt:
                    repaired["head_style"] = "crystal"
                elif "crescent" in lower_prompt:
                    repaired["head_style"] = "crescent"
                elif "orb" in lower_prompt:
                    repaired["head_style"] = "orb"
                for material_name in ["obsidian", "darkwood", "wood"]:
                    if material_name in lower_prompt:
                        repaired["shaft_material"] = material_name
                        break
                for color_name in ["blue", "green", "red", "purple"]:
                    if color_name in lower_prompt:
                        repaired["gem_color"] = color_name
                        break
            elif asset_type == "wand":
                if "forked" in lower_prompt:
                    repaired["tip_style"] = "forked"
                elif "plain" in lower_prompt or "simple" in lower_prompt:
                    repaired["tip_style"] = "plain"
                elif "gem" in lower_prompt or "crystal" in lower_prompt:
                    repaired["tip_style"] = "gem"
                for material_name in ["obsidian", "bone", "wood"]:
                    if material_name in lower_prompt:
                        repaired["shaft_material"] = material_name
                        break
                for color_name in ["blue", "green", "red", "purple"]:
                    if color_name in lower_prompt:
                        repaired["gem_color"] = color_name
                        break
            elif asset_type == "orb":
                if "without stand" in lower_prompt or "floating orb" in lower_prompt:
                    repaired["has_stand"] = False
                elif "stand" in lower_prompt or "pedestal" in lower_prompt:
                    repaired["has_stand"] = True
                for material_name in ["obsidian", "glass", "crystal"]:
                    if material_name in lower_prompt:
                        repaired["orb_material"] = material_name
                        break
                for color_name in ["blue", "green", "red", "purple"]:
                    if color_name in lower_prompt:
                        repaired["glow_color"] = color_name
                        break
            elif asset_type == "chestplate":
                if "fantasy" in lower_prompt:
                    repaired["style"] = "fantasy"
                elif "breastplate" in lower_prompt:
                    repaired["style"] = "breastplate"
                elif "knight" in lower_prompt:
                    repaired["style"] = "knight"
                for material_name in ["steel", "iron", "bronze", "leather"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "gauntlets":
                if "spiked" in lower_prompt:
                    repaired["style"] = "spiked"
                elif "leather" in lower_prompt:
                    repaired["style"] = "leather"
                elif "plate" in lower_prompt:
                    repaired["style"] = "plate"
                for material_name in ["steel", "iron", "bronze", "leather"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "boots":
                if "riding" in lower_prompt:
                    repaired["style"] = "riding"
                elif "plate" in lower_prompt or "armored" in lower_prompt or "armoured" in lower_prompt:
                    repaired["style"] = "plate"
                elif "travel" in lower_prompt:
                    repaired["style"] = "travel"
                for material_name in ["leather", "steel", "iron"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "backpack":
                if "bedroll" in lower_prompt or "bed roll" in lower_prompt:
                    repaired["has_bedroll"] = True
                for material_name in ["canvas", "leather", "cloth"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "belt":
                for material_name in ["leather", "cloth"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
                for material_name in ["steel", "brass", "iron"]:
                    if material_name in lower_prompt:
                        repaired["buckle_material"] = material_name
                        break
            elif asset_type == "pouch":
                for material_name in ["leather", "cloth"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
                for material_name in ["steel", "brass", "bone"]:
                    if material_name in lower_prompt:
                        repaired["clasp_material"] = material_name
                        break
            elif asset_type == "cape":
                for color_name in ["red", "blue", "green", "black", "brown"]:
                    if color_name in lower_prompt:
                        repaired["fabric"] = color_name
                        break
                for material_name in ["steel", "brass", "gold"]:
                    if material_name in lower_prompt:
                        repaired["clasp_material"] = material_name
                        break
            elif asset_type == "tent":
                if "a frame" in lower_prompt or "a-frame" in lower_prompt:
                    repaired["tent_style"] = "a_frame"
                elif "pup" in lower_prompt:
                    repaired["tent_style"] = "pup"
                elif "ridge" in lower_prompt:
                    repaired["tent_style"] = "ridge"
                for material_name in ["canvas", "cloth", "hide"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "campfire":
                if "unlit" in lower_prompt or "extinguished" in lower_prompt or "not lit" in lower_prompt:
                    repaired["is_lit"] = False
                elif "lit" in lower_prompt or "burning" in lower_prompt or "flame" in lower_prompt:
                    repaired["is_lit"] = True
            elif asset_type == "sleeping_bag":
                for color_name in ["blue", "green", "red", "brown", "gray"]:
                    if color_name in lower_prompt:
                        repaired["fabric"] = color_name
                        break
            elif asset_type == "lantern":
                if "unlit" in lower_prompt or "dark" in lower_prompt:
                    repaired["is_lit"] = False
                elif "lit" in lower_prompt or "glowing" in lower_prompt or "burning" in lower_prompt:
                    repaired["is_lit"] = True
                for material_name in ["iron", "brass", "steel"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "cooking_pot":
                if "without lid" in lower_prompt or "open pot" in lower_prompt:
                    repaired["has_lid"] = False
                elif "lid" in lower_prompt:
                    repaired["has_lid"] = True
                for material_name in ["iron", "steel", "copper"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "supply_box":
                if "without rope" in lower_prompt or "plain handles" in lower_prompt:
                    repaired["has_rope"] = False
                elif "rope" in lower_prompt:
                    repaired["has_rope"] = True
                for material_name in ["wood", "metal", "canvas"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "castle_wall":
                if "without crenellation" in lower_prompt or "without crenellations" in lower_prompt or "plain parapet" in lower_prompt:
                    repaired["has_crenellations"] = False
                elif "crenellation" in lower_prompt or "crenellations" in lower_prompt or "battlement" in lower_prompt:
                    repaired["has_crenellations"] = True
                for material_name in ["stone", "brick"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "tower":
                if "cone roof" in lower_prompt or "conical roof" in lower_prompt:
                    repaired["roof_style"] = "cone"
                elif "flat top" in lower_prompt or "flat roof" in lower_prompt:
                    repaired["roof_style"] = "flat"
                elif "battlement" in lower_prompt or "crenellation" in lower_prompt:
                    repaired["roof_style"] = "battlement"
                for material_name in ["stone", "brick"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "drawbridge":
                for material_name in ["wood", "iron"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "throne":
                if "without cushion" in lower_prompt or "bare seat" in lower_prompt:
                    repaired["has_cushion"] = False
                elif "cushion" in lower_prompt:
                    repaired["has_cushion"] = True
                for material_name in ["gold", "stone", "wood"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "banner":
                for color_name in ["red", "blue", "green", "black", "gold"]:
                    if color_name in lower_prompt:
                        repaired["fabric"] = color_name
                        break
                for material_name in ["wood", "steel", "brass"]:
                    if material_name in lower_prompt:
                        repaired["pole_material"] = material_name
                        break
            elif asset_type == "market_stall":
                if "striped" in lower_prompt:
                    repaired["canopy_color"] = "striped"
                else:
                    for color_name in ["red", "blue", "green"]:
                        if color_name in lower_prompt:
                            repaired["canopy_color"] = color_name
                            break
                for material_name in ["darkwood", "wood"]:
                    if material_name in lower_prompt:
                        repaired["frame_material"] = material_name
                        break
            elif asset_type == "well":
                if "without roof" in lower_prompt or "open well" in lower_prompt:
                    repaired["roof_style"] = "none"
                elif "flat roof" in lower_prompt:
                    repaired["roof_style"] = "flat"
                elif "gable" in lower_prompt or "pitched roof" in lower_prompt:
                    repaired["roof_style"] = "gable"
                for material_name in ["stone", "brick", "wood"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "cart":
                if "canopy" in lower_prompt or "covered cart" in lower_prompt:
                    repaired["has_canopy"] = True
                elif "open cart" in lower_prompt or "without canopy" in lower_prompt:
                    repaired["has_canopy"] = False
                for material_name in ["darkwood", "wood"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "anvil":
                for material_name in ["iron", "steel"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break
            elif asset_type == "forge":
                if "cold forge" in lower_prompt or "unlit forge" in lower_prompt or "without fire" in lower_prompt:
                    repaired["is_lit"] = False
                elif "lit" in lower_prompt or "burning" in lower_prompt or "fire" in lower_prompt:
                    repaired["is_lit"] = True
                for material_name in ["stone", "brick", "iron"]:
                    if material_name in lower_prompt:
                        repaired["material"] = material_name
                        break

            if asset_type in WORLD_ASSET_TYPES:
                apply_world_prompt_overrides(asset_type, repaired, lower_prompt)
            
            # Explicit dimension overrides via regex parsing
            import re

            def _convert_prompt_dimension(raw_value, unit_name):
                value = float(raw_value)
                if unit_name.startswith("m"):
                    return value * 100.0 if asset_type not in ["barrel", "crate"] else value
                return value if asset_type not in ["barrel", "crate"] else value / 100.0

            def _assign_prompt_dimension(target_key, pattern):
                match = re.search(pattern, lower_prompt)
                if not match:
                    return
                repaired[target_key] = round(_convert_prompt_dimension(match.group(1), match.group(2)), 1)

            if asset_type in ["sword", "dagger"]:
                _assign_prompt_dimension("blade_length", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:blade|blade length|long blade)')
                _assign_prompt_dimension("blade_width", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:blade width|wide blade)')
                _assign_prompt_dimension("grip_length", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:grip|handle|hilt)')
            elif asset_type == "axe":
                _assign_prompt_dimension("shaft_length", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:shaft|handle|long)')
            elif asset_type == "hammer":
                _assign_prompt_dimension("handle_length", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:handle|shaft|long)')
                _assign_prompt_dimension("head_width", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:head width|wide head|wide)')
                _assign_prompt_dimension("head_height", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:head height|tall head)')
            elif asset_type in ["mace", "spear", "halberd"]:
                _assign_prompt_dimension("shaft_length", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:shaft|handle|pole|long)')
            elif asset_type in ["staff", "magic_staff"]:
                _assign_prompt_dimension("height", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:tall|high|height)')
            elif asset_type == "crossbow":
                _assign_prompt_dimension("stock_length", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:stock|stock length|long)')
            elif asset_type in ["arrow", "bolt", "wand"]:
                _assign_prompt_dimension("length", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:long|length)')
            elif asset_type == "drawbridge":
                _assign_prompt_dimension("length", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:long|length|span)')
            elif asset_type in ["tower", "well", "cooking_pot"]:
                _assign_prompt_dimension("diameter", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:diameter|across)')
            elif asset_type in ["pipe", "conveyor_belt"]:
                _assign_prompt_dimension("length", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:long|length|span)')
            elif asset_type in ["energy_cell", "tank", "valve", "trash_can"]:
                _assign_prompt_dimension("diameter", r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:diameter|across)')
            
            # Width/table_width
            skip_generic_width = asset_type in {"drawbridge", "pipe", "conveyor_belt"} and re.search(
                r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:long|length|span)',
                lower_prompt,
            )
            width_match = None if skip_generic_width else re.search(r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:wide|width|long|length)', lower_prompt)
            if width_match:
                val = float(width_match.group(1))
                unit = width_match.group(2)
                if unit.startswith('m'):
                    if asset_type not in ["barrel", "crate"]:
                        val *= 100.0
                else:
                    if asset_type in ["barrel", "crate"]:
                        val /= 100.0
                if asset_type == "dining_set":
                    repaired["table_width"] = round(val, 1)
                else:
                    repaired["width"] = round(val, 1)
                    
            # Height/table_height
            height_match = re.search(r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:high|height|tall)', lower_prompt)
            if height_match:
                val = float(height_match.group(1))
                unit = height_match.group(2)
                if unit.startswith('m'):
                    if asset_type not in ["barrel", "crate"]:
                        val *= 100.0
                else:
                    if asset_type in ["barrel", "crate"]:
                        val /= 100.0
                if asset_type == "dining_set":
                    repaired["table_height"] = round(val, 1)
                else:
                    repaired["height"] = round(val, 1)
                    
            # Depth/table_depth
            depth_match = re.search(r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)\s*(?:deep|depth)', lower_prompt)
            if depth_match:
                val = float(depth_match.group(1))
                unit = depth_match.group(2)
                if unit.startswith('m'):
                    if asset_type not in ["barrel", "crate"]:
                        val *= 100.0
                else:
                    if asset_type in ["barrel", "crate"]:
                        val /= 100.0
                if asset_type == "dining_set":
                    repaired["table_depth"] = round(val, 1)
                else:
                    repaired["depth"] = round(val, 1)
                    
        # Normalise specific wood species/types to 'wood' for schemas with strict material literals
        for mat_key in ["material", "grip_material", "shaft_material", "handle_material", "head_material", "tip_material", "buckle_material", "clasp_material", "frame_material", "pole_material"]:
            if mat_key in repaired and isinstance(repaired[mat_key], str):
                mat_val = repaired[mat_key].lower()
                if mat_val in ["oak", "teak", "mahogany", "cherry", "pine", "walnut", "rosewood", "plywood", "ash", "birch", "maple", "wood"]:
                    if asset_type in ["shelf", "bed", "bunk_bed", "wardrobe", "bookcase", "sword", "dagger", "staff", "bow", "crossbow", "arrow", "bolt", "magic_staff", "wand", "countertop", "banner", "market_stall", "cart"]:
                        repaired[mat_key] = "wood"
                elif mat_val in ["blackwood", "ebony", "dark wood"]:
                    if asset_type in ["staff", "bow", "crossbow", "arrow", "bolt", "magic_staff", "market_stall", "cart"]:
                        repaired[mat_key] = "darkwood"
                elif mat_val in ["bronze"]:
                    if mat_key in ["head_material", "tip_material", "buckle_material", "clasp_material", "pole_material"] or asset_type == "hammer":
                        repaired[mat_key] = "brass"
        
        # Barrels and Crates are in meters (e.g. valid range 0.15m to 3.0m)
        if asset_type in ["barrel", "crate"]:
            for key in ["radius", "height", "width", "depth"]:
                if key in repaired and repaired[key] is not None:
                    val = repaired[key]
                    # If value is greater than 5.0 (which is huge for a crate/barrel in meters),
                    # it was almost certainly specified in centimeters. Convert to meters.
                    if isinstance(val, (int, float)) and val > 5.0:
                        logger.info(f"Auto-repairing {asset_type} {key}: {val} cm -> {val / 100.0} m")
                        repaired[key] = round(val / 100.0, 3)
                        
        # Swords, Tables, Shields, Chairs, Chests, Axes, Helmets, Torches, Sofas, Benches, Couches, Armchairs, Beds, Bunk Beds, Wardrobes, Storage, Lighting, Closets, Dressers, Cabinets, Shelves, Bookcases, Nightstands, TV Stands, Fridges, Stoves, Ovens, Microwaves, Sinks, and Countertops are in centimeters (e.g. valid range 10cm to 240cm)
        elif asset_type in [*sorted(WEAPON_ASSET_TYPES), "table", "dining_table", "coffee_table", "shield", "chair", "desk", "stool", "chest", "helmet", "torch", "sofa", "bench", "couch", "armchair", "bed", "bunk_bed", "wardrobe", "storage", "lighting", "closet", "dresser", "cabinet", "shelf", "bookcase", "nightstand", "tv_stand", "fridge", "stove", "oven", "microwave", "sink", "countertop", "cupboard", "kitchen_island", "dining_set", "toilet", "bathtub", "shower", "mirror", "towel_rack", "lamp", "chandelier", "painting", "picture_frame", "clock", "vase", "plant_pot", "rug", *sorted(ARCHITECTURE_ASSET_TYPES), *sorted(NATURE_ASSET_TYPES), *sorted(ADVENTURE_ASSET_TYPES), *sorted(WORLD_ASSET_TYPES)]:
            # Check dimensions that might have been output in meters
            keys_to_check = ["blade_length", "blade_width", "grip_length", "handle_length", "head_width", "head_height", "head_radius", "tip_length", "blade_size", "hook_size", "stock_length", "shaft_radius", "width", "depth", "height", "diameter", "seat_height", "backrest_height", "shaft_length", "flame_size", "table_width", "table_depth", "table_height", "overhang_depth", "overhang", "opening_width", "opening_height", "tank_width", "tank_depth", "border_thickness", "neck_diameter", "thickness", "canopy_width", "trunk_radius", "frond_span", "cap_diameter", "length", "radius", "pool_radius", "bank_height", "curve", "footing_depth", "support_width", "step_height", "step_depth", "deck_thickness"]
            for key in keys_to_check:
                if key in repaired and repaired[key] is not None:
                    val = repaired[key]
                    if should_convert_cm_value_from_meters(asset_type, key, val):
                        logger.info(f"Auto-repairing {asset_type} {key}: {val} m -> {val * 100.0} cm")
                        repaired[key] = round(val * 100.0, 1)

        if asset_type in NATURE_ASSET_TYPES:
            minimums = NATURE_UNIT_MINIMUMS.get(asset_type, {})
            for key, min_value in minimums.items():
                val = repaired.get(key)
                if should_convert_cm_value_from_meters(asset_type, key, val):
                    logger.info(f"Auto-repairing {asset_type} {key}: {val} m -> {val * 100.0} cm (nature minimum heuristic)")
                    repaired[key] = round(val * 100.0, 1)

        repaired = coerce_schema_field_values(asset_type, repaired, user_prompt)
        repaired = clamp_numeric_values_to_schema(asset_type, repaired)
                        
        return repaired
 
    def get_generator_path(self, asset_type: str) -> str:
        """Returns the absolute path to the generator script for the given asset type."""
        if asset_type in NATURE_ASSET_TYPES:
            generator_file = "nature_asset.py"
        elif asset_type in ARCHITECTURE_ASSET_TYPES:
            generator_file = "architecture_asset.py"
        elif asset_type in WEAPON_ASSET_TYPES:
            generator_file = "weapon_asset.py"
        elif asset_type in ADVENTURE_ASSET_TYPES:
            generator_file = "adventure_asset.py"
        elif asset_type in WORLD_ASSET_TYPES:
            generator_file = "world_asset.py"
        else:
            # asset_type strings map directly to file names (underscores preserved)
            generator_file = f"{asset_type}.py"
        return os.path.abspath(os.path.join(project_root, "generators", generator_file))
 
 
    def process_prompt(self, user_prompt: str) -> Tuple[AssetParams, str]:
        """Runs the entire pipeline: 
        Prompt -> Ollama Spec -> Auto-Repair -> Pydantic Validation -> Select Generator
        
        Returns:
            Tuple[AssetParams, str]: The validated schema parameters object and the absolute path to the generator script.
        """
        # 1. Query Ollama to get raw dictionary
        raw_spec = self.client.generate_json_spec(user_prompt)
        lower_prompt = user_prompt.lower()
        inferred_architecture_type = infer_architecture_asset_type(lower_prompt)
        inferred_weapon_type = infer_weapon_asset_type(lower_prompt)
        inferred_adventure_type = infer_adventure_asset_type(lower_prompt)
        inferred_world_type = infer_world_asset_type(lower_prompt)
        inferred_nature_type = infer_nature_asset_type(lower_prompt)

        if inferred_architecture_type:
            existing_type = str(raw_spec.get("asset_type", "")).lower()
            should_override_architecture = (
                existing_type not in ARCHITECTURE_ASSET_TYPES
                or (existing_type in GENERIC_ARCHITECTURE_TYPES and existing_type != inferred_architecture_type)
            )
            if should_override_architecture:
                logger.info(f"Overriding asset_type with inferred architecture type '{inferred_architecture_type}' from prompt: '{user_prompt}'")
                raw_spec["asset_type"] = inferred_architecture_type

        if inferred_weapon_type:
            existing_type = str(raw_spec.get("asset_type", "")).lower()
            should_override_weapon = (
                existing_type not in WEAPON_ASSET_TYPES
                or existing_type != inferred_weapon_type
            )
            if should_override_weapon and existing_type not in ARCHITECTURE_ASSET_TYPES:
                logger.info(f"Overriding asset_type with inferred weapon type '{inferred_weapon_type}' from prompt: '{user_prompt}'")
                raw_spec["asset_type"] = inferred_weapon_type

        if inferred_adventure_type:
            existing_type = str(raw_spec.get("asset_type", "")).lower()
            should_override_adventure = (
                existing_type not in ADVENTURE_ASSET_TYPES
                or existing_type != inferred_adventure_type
            )
            if should_override_adventure and existing_type not in WEAPON_ASSET_TYPES and existing_type not in NATURE_ASSET_TYPES:
                logger.info(f"Overriding asset_type with inferred adventure type '{inferred_adventure_type}' from prompt: '{user_prompt}'")
                raw_spec["asset_type"] = inferred_adventure_type

        if inferred_world_type:
            existing_type = str(raw_spec.get("asset_type", "")).lower()
            should_override_world = (
                existing_type not in WORLD_ASSET_TYPES
                or existing_type != inferred_world_type
            )
            actor_world_types = {
                "male", "female", "child", "elder", "merchant", "guard", "farmer", "blacksmith", "soldier",
                "elf", "orc", "goblin", "dwarf", "dragon", "dog", "cat", "horse", "cow", "deer", "wolf",
                "bird", "fish",
            }
            wants_actor = any(token in lower_prompt for token in ("character", "npc", "person", "creature", "animal"))
            can_override_architecture = (
                existing_type not in ARCHITECTURE_ASSET_TYPES
                or inferred_world_type not in actor_world_types
                or wants_actor
                or inferred_world_type in {"space_door", "airlock", "phone_booth"}
            )
            can_override_adventure = (
                existing_type not in ADVENTURE_ASSET_TYPES
                or (inferred_world_type in actor_world_types and wants_actor)
            )
            if (
                should_override_world
                and existing_type not in WEAPON_ASSET_TYPES
                and can_override_adventure
                and can_override_architecture
            ):
                logger.info(f"Overriding asset_type with inferred world type '{inferred_world_type}' from prompt: '{user_prompt}'")
                raw_spec["asset_type"] = inferred_world_type

        if inferred_nature_type:
            existing_type = str(raw_spec.get("asset_type", "")).lower()
            if existing_type not in NATURE_ASSET_TYPES and existing_type not in ARCHITECTURE_ASSET_TYPES and existing_type not in WEAPON_ASSET_TYPES and existing_type not in ADVENTURE_ASSET_TYPES and existing_type not in WORLD_ASSET_TYPES:
                logger.info(f"Overriding asset_type with inferred nature type '{inferred_nature_type}' from prompt: '{user_prompt}'")
                raw_spec["asset_type"] = inferred_nature_type
        
        # Fallback keyword match if LLM forgets to specify asset_type / type
        if "asset_type" not in raw_spec and "type" not in raw_spec:
            inferred_type = None
            # Prioritized specific nouns first
            if inferred_adventure_type:
                inferred_type = inferred_adventure_type
            elif inferred_world_type:
                inferred_type = inferred_world_type
            elif inferred_architecture_type:
                inferred_type = inferred_architecture_type
            elif inferred_weapon_type:
                inferred_type = inferred_weapon_type
            elif inferred_nature_type:
                inferred_type = inferred_nature_type
            elif "bunk bed" in lower_prompt or "loft bed" in lower_prompt:
                inferred_type = "bunk_bed"
            elif "wardrobe" in lower_prompt or "armoire" in lower_prompt:
                inferred_type = "wardrobe"
            elif "closet" in lower_prompt:
                inferred_type = "closet"
            elif "dresser" in lower_prompt or "chest of drawers" in lower_prompt:
                inferred_type = "dresser"
            elif "nightstand" in lower_prompt or "bedside" in lower_prompt:
                inferred_type = "nightstand"
            elif "tv stand" in lower_prompt or "media console" in lower_prompt or "lowboard" in lower_prompt:
                inferred_type = "tv_stand"
            elif "fridge" in lower_prompt or "refrigerator" in lower_prompt:
                inferred_type = "fridge"
            elif "stove" in lower_prompt or "cooktop" in lower_prompt or "range" in lower_prompt:
                inferred_type = "stove"
            elif "oven" in lower_prompt:
                inferred_type = "oven"
            elif "microwave" in lower_prompt:
                inferred_type = "microwave"
            elif "sink" in lower_prompt or "basin" in lower_prompt or "washbasin" in lower_prompt:
                inferred_type = "sink"
            elif "kitchen island" in lower_prompt or "island" in lower_prompt:
                inferred_type = "kitchen_island"
            elif "countertop" in lower_prompt or "counter" in lower_prompt:
                inferred_type = "countertop"
            elif "bookcase" in lower_prompt or "bookshelf" in lower_prompt:
                inferred_type = "bookcase"
            elif "shelf" in lower_prompt or "shelving" in lower_prompt:
                inferred_type = "shelf"
            elif "cupboard" in lower_prompt:
                inferred_type = "cupboard"
            elif "cabinet" in lower_prompt or "credenza" in lower_prompt:
                inferred_type = "cabinet"
            elif "toilet" in lower_prompt or "commode" in lower_prompt:
                inferred_type = "toilet"
            elif "bathtub" in lower_prompt or "bath tub" in lower_prompt or "tub" in lower_prompt:
                inferred_type = "bathtub"
            elif "shower" in lower_prompt:
                inferred_type = "shower"
            elif "mirror" in lower_prompt or "looking glass" in lower_prompt:
                inferred_type = "mirror"
            elif "towel rack" in lower_prompt or "towel bar" in lower_prompt or "towel rail" in lower_prompt or "towel_rack" in lower_prompt:
                inferred_type = "towel_rack"
            elif "dining set" in lower_prompt or "dining_set" in lower_prompt:
                inferred_type = "dining_set"
            elif "bed" in lower_prompt:
                inferred_type = "bed"
            elif "chair" in lower_prompt:
                inferred_type = "chair"
            elif "stool" in lower_prompt:
                inferred_type = "stool"
            elif "desk" in lower_prompt:
                inferred_type = "desk"
            elif "dining table" in lower_prompt:
                inferred_type = "dining_table"
            elif "coffee table" in lower_prompt:
                inferred_type = "coffee_table"
            elif "table" in lower_prompt:
                inferred_type = "table"
            elif "shield" in lower_prompt:
                inferred_type = "shield"
            elif "chest" in lower_prompt:
                inferred_type = "chest"
            elif "barrel" in lower_prompt:
                inferred_type = "barrel"
            elif "crate" in lower_prompt:
                inferred_type = "crate"
            elif "helmet" in lower_prompt:
                inferred_type = "helmet"
            elif "torch" in lower_prompt:
                inferred_type = "torch"
            elif "sofa" in lower_prompt:
                inferred_type = "sofa"
            elif "bench" in lower_prompt:
                inferred_type = "bench"
            elif "couch" in lower_prompt:
                inferred_type = "couch"
            elif "armchair" in lower_prompt:
                inferred_type = "armchair"
            elif "chandelier" in lower_prompt:
                inferred_type = "chandelier"
            elif "lamp" in lower_prompt:
                inferred_type = "lamp"
            elif "lighting" in lower_prompt:
                inferred_type = "lighting"
            elif "picture frame" in lower_prompt or "photo frame" in lower_prompt or "picture_frame" in lower_prompt or "frame" in lower_prompt:
                inferred_type = "picture_frame"
            elif "painting" in lower_prompt or "artwork" in lower_prompt or "canvas" in lower_prompt or "art" in lower_prompt:
                inferred_type = "painting"
            elif "clock" in lower_prompt or "timepiece" in lower_prompt:
                inferred_type = "clock"
            elif "vase" in lower_prompt or "urn" in lower_prompt:
                inferred_type = "vase"
            elif "plant pot" in lower_prompt or "flower pot" in lower_prompt or "plant_pot" in lower_prompt or "flowerpot" in lower_prompt:
                inferred_type = "plant_pot"
            elif "rug" in lower_prompt or "carpet" in lower_prompt:
                inferred_type = "rug"
            elif "pillar" in lower_prompt or "column" in lower_prompt:
                inferred_type = "pillar"
            elif "beam" in lower_prompt:
                inferred_type = "beam"
            elif "roof" in lower_prompt:
                inferred_type = "roof"
            elif "ceiling" in lower_prompt:
                inferred_type = "ceiling"
            elif "floor" in lower_prompt and "lamp" not in lower_prompt:
                inferred_type = "floor"
            elif "wall" in lower_prompt and "mounted" not in lower_prompt:
                inferred_type = "wall"
            elif "storage" in lower_prompt:
                inferred_type = "storage"

                
            # Generic/feature keyword fallbacks as a secondary pass
            if not inferred_type:
                if "drawers" in lower_prompt:
                    inferred_type = "dresser"
                elif "shelves" in lower_prompt:
                    inferred_type = "storage"
                
            if inferred_type:
                logger.info(f"Inferred missing asset_type '{inferred_type}' from user prompt: '{user_prompt}'")
                raw_spec["asset_type"] = inferred_type
        
        # 2. Heuristic Unit Repair
        repaired_spec = self.repair_units(raw_spec, user_prompt)
        
        # 3. Pydantic validation
        try:
            validated_params = validate_asset_params(repaired_spec)
            logger.info(f"Successfully validated parameters for {validated_params.asset_type}")
        except Exception as e:
            logger.error(f"Pydantic validation failed for spec {repaired_spec}: {e}")
            raise ValueError(f"Schema validation failed: {e}")
            
        # 4. Get generator path
        generator_path = self.get_generator_path(validated_params.asset_type)
        if not os.path.exists(generator_path):
            raise FileNotFoundError(f"Procedural generator script not found at: {generator_path}")
            
        return validated_params, generator_path
