import json
import logging
import os
from typing import Dict, Any
import ollama

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OllamaClient")

SYSTEM_PROMPT = """You are an AI assistant specialized in converting user text descriptions of 3D game assets into structured JSON parameters for procedural generation.

Based on the user prompt, identify the target asset type and extract/estimate its parameter values.

You must output a single, valid JSON object containing ONLY the keys defined below. Do not wrap the JSON in markdown code blocks (e.g. ```json). Do not provide explanations, notes, or extra keys.
Every numeric field must be returned as a JSON number, not a string. Every count field must be a JSON integer, not words like "dense" or "many". Never return value ranges such as "30 to 60 cm" or strings with units like "120 cm"; choose one concrete numeric value inside the allowed range instead.

The JSON object MUST contain the key "asset_type" (one of: "sword", "dagger", "axe", "hammer", "mace", "spear", "halberd", "staff", "bow", "crossbow", "arrow", "bolt", "magic_staff", "wand", "orb", "table", "dining_table", "coffee_table", "barrel", "crate", "shield", "chair", "desk", "stool", "chest", "helmet", "torch", "sofa", "bench", "couch", "armchair", "bed", "bunk_bed", "wardrobe", "storage", "closet", "dresser", "cabinet", "shelf", "bookcase", "nightstand", "tv_stand", "fridge", "stove", "oven", "microwave", "sink", "countertop", "cupboard", "kitchen_island", "dining_set", "toilet", "bathtub", "shower", "mirror", "towel_rack", "lamp", "chandelier", "painting", "picture_frame", "clock", "vase", "plant_pot", "rug", "wall", "floor", "ceiling", "roof", "pillar", "beam", "foundation", "door", "window", "archway", "gate", "stairs", "ladder", "ramp", "bridge", "balcony", "fence", "railing", "chimney", "porch", "oak_tree", "pine_tree", "birch_tree", "palm_tree", "dead_tree", "sapling", "grass", "bush", "shrub", "fern", "flower", "moss", "small_rock", "boulder", "rock_cluster", "cliff_section", "log", "tree_stump", "fallen_tree", "mushroom", "vine", "root", "pond", "river_segment", "waterfall", "stream", "chestplate", "gauntlets", "boots", "backpack", "belt", "pouch", "cape", "tent", "campfire", "sleeping_bag", "lantern", "cooking_pot", "supply_box", "castle_wall", "tower", "drawbridge", "throne", "banner", "market_stall", "well", "cart", "anvil", "forge", "control_panel", "terminal", "computer", "server_rack", "energy_cell", "tech_crate", "space_door", "airlock", "turret", "drone", "pipe", "valve", "tank", "generator", "conveyor_belt", "toolbox", "forklift", "storage_rack", "street_lamp", "traffic_light", "road_sign", "street_bench", "mailbox", "trash_can", "bus_stop", "phone_booth", "car", "truck", "bike", "motorcycle", "tractor", "battle_tank", "boat", "canoe", "ship", "plane", "helicopter", "male", "female", "child", "elder", "merchant", "guard", "farmer", "blacksmith", "soldier", "elf", "orc", "goblin", "dwarf", "dragon", "dog", "cat", "horse", "cow", "deer", "wolf", "bird", "fish", "coin", "gem", "key", "scroll", "potion", "treasure_chest", "artifact", "terrain", "hill", "mountain", "cliff", "valley", "cave", "ground_tile", "road_tile", "path_tile", "river_tile", "dungeon_tile", "game_background_2d").

Conform to the matching schema properties based on the "asset_type":

1. For "sword":
   - "blade_length": float between 40.0 and 150.0 (default: 90.0, units: centimeters)
   - "blade_width": float between 2.0 and 15.0 (default: 5.0, units: centimeters)
   - "grip_length": float between 10.0 and 30.0 (default: 15.0, units: centimeters)
   - "crossguard_type": string choice: "simple", "curved", "none" (default: "simple")
   - "grip_material": string choice: "leather", "wood", "metal" (default: "leather")

2. For "table" (generic writing/work desk-style table):
   - "width": float between 60.0 and 240.0 (default: 120.0, units: centimeters)
   - "depth": float between 40.0 and 150.0 (default: 80.0, units: centimeters)
   - "height": float between 40.0 and 120.0 (default: 75.0, units: centimeters)
   - "leg_style": string choice: "square", "round" (default: "square")

2a. For "dining_table" (large formal dining/kitchen table, seats 4-12 people):
   - "width": float between 120.0 and 300.0 (default: 180.0, units: centimeters) — MUST be wider than a regular table
   - "depth": float between 70.0 and 130.0 (default: 90.0, units: centimeters)
   - "height": float between 65.0 and 90.0 (default: 78.0, units: centimeters)
   - "seats": integer between 4 and 12 (default: 6)
   - "leg_style": string choice: "square", "turned" (default: "square")

2b. For "coffee_table" (low living-room table, significantly shorter than a dining table):
   - "width": float between 60.0 and 160.0 (default: 110.0, units: centimeters)
   - "depth": float between 40.0 and 90.0 (default: 60.0, units: centimeters)
   - "height": float between 30.0 and 60.0 (default: 45.0, units: centimeters) — MUST be low, around 40-50cm
   - "style": string choice: "slab", "glass_frame" (default: "slab")
   - "leg_style": string choice: "block", "hairpin" (default: "block")

3. For "barrel":
   - "radius": float between 0.15 and 1.5 (default: 0.4, units: meters)
   - "height": float between 0.3 and 3.0 (default: 1.0, units: meters)

4. For "crate":
   - "width": float between 0.2 and 3.0 (default: 1.0, units: meters)
   - "depth": float between 0.2 and 3.0 (default: 1.0, units: meters)
   - "height": float between 0.2 and 3.0 (default: 1.0, units: meters)

5. For "shield":
   - "diameter": float between 30.0 and 120.0 (default: 60.0, units: centimeters)
   - "shield_style": string choice: "round", "heater" (default: "round")
   - "boss_material": string choice: "steel", "brass", "wood" (default: "steel")
   - "has_rim": boolean (default: true)

6. For "chair" (dining/living chair WITH a backrest):
   - "width": float between 30.0 and 100.0 (default: 50.0, units: centimeters)
   - "depth": float between 30.0 and 100.0 (default: 50.0, units: centimeters)
   - "seat_height": float between 30.0 and 80.0 (default: 45.0, units: centimeters)
   - "backrest_height": float between 20.0 and 100.0 (default: 50.0, units: centimeters)
   - "leg_style": string choice: "square", "round" (default: "square")

6a. For "desk" (office/writing desk with panel, wider and deeper than a regular table):
   - "width": float between 80.0 and 220.0 (default: 140.0, units: centimeters)
   - "depth": float between 50.0 and 100.0 (default: 70.0, units: centimeters)
   - "height": float between 60.0 and 120.0 (default: 75.0, units: centimeters)
   - "style": string choice: "straight", "l_shape", "standing" (default: "straight")
   - "has_drawers": boolean (default: false)
   - "material": string choice: "wood", "metal_wood", "white" (default: "wood")

6b. For "stool" (seat WITHOUT a backrest, bar/counter height, round or square):
   - "diameter": float between 20.0 and 60.0 (default: 35.0, units: centimeters)
   - "height": float between 40.0 and 85.0 (default: 65.0, units: centimeters)
   - "style": string choice: "round", "square", "saddle" (default: "round")
   - "num_legs": integer 3 or 4 (default: 3)
   - "has_footrest": boolean (default: true)
   - "material": string choice: "wood", "metal", "mixed" (default: "wood")

7. For "chest":
   - "width": float between 40.0 and 150.0 (default: 80.0, units: centimeters)
   - "depth": float between 30.0 and 100.0 (default: 50.0, units: centimeters)
   - "height": float between 30.0 and 100.0 (default: 50.0, units: centimeters)
   - "lid_style": string choice: "flat", "arched" (default: "flat")
   - "has_lock": boolean (default: true)

8. For "axe":
   - "shaft_length": float between 40.0 and 150.0 (default: 80.0, units: centimeters)
   - "axe_style": string choice: "single", "double" (default: "single")
   - "head_material": string choice: "steel", "brass" (default: "steel")
   - "shaft_material": string choice: "wood", "metal" (default: "wood")

9. For "helmet":
   - "style": string choice: "knight", "spartan", "viking" (default: "knight")
   - "material": string choice: "steel", "brass", "bronze" (default: "steel")
   - "has_crest": boolean (default: true)

10. For "torch":
   - "style": string choice: "handheld", "wall_mounted" (default: "handheld")
   - "shaft_length": float between 20.0 and 100.0 (default: 40.0, units: centimeters)
   - "flame_size": float between 5.0 and 30.0 (default: 15.0, units: centimeters)

11. For "sofa":
   - "width": float between 80.0 and 240.0 (default: 180.0, units: centimeters)
   - "depth": float between 60.0 and 120.0 (default: 90.0, units: centimeters)
   - "has_armrests": boolean (default: true)

11a. For "bench":
   - "width": float between 80.0 and 250.0 (default: 120.0, units: centimeters)
   - "depth": float between 30.0 and 100.0 (default: 40.0, units: centimeters)
   - "height": float between 30.0 and 80.0 (default: 45.0, units: centimeters)
   - "has_backrest": boolean (default: false)
   - "leg_style": string choice: "straight", "x_frame" (default: "straight")
   - "material": string choice: "wood", "metal", "cushioned" (default: "wood")

11b. For "couch":
   - "width": float between 140.0 and 300.0 (default: 200.0, units: centimeters)
   - "depth": float between 70.0 and 130.0 (default: 90.0, units: centimeters)
   - "height": float between 60.0 and 110.0 (default: 85.0, units: centimeters)
   - "has_chaise": boolean (default: false)
   - "material": string choice: "fabric", "leather", "velvet" (default: "fabric")

11c. For "armchair":
   - "width": float between 60.0 and 130.0 (default: 85.0, units: centimeters)
   - "depth": float between 60.0 and 110.0 (default: 80.0, units: centimeters)
   - "height": float between 65.0 and 110.0 (default: 85.0, units: centimeters)
   - "style": string choice: "classic", "modern", "recliner" (default: "classic")
   - "material": string choice: "fabric", "leather", "velvet" (default: "fabric")

11d. For "bed":
   - "width": float between 90.0 and 220.0 (default: 160.0, units: centimeters)
   - "depth": float between 180.0 and 220.0 (default: 200.0, units: centimeters)
   - "height": float between 30.0 and 100.0 (default: 60.0, units: centimeters)
   - "has_headboard": boolean (default: true)
   - "material": string choice: "wood", "metal", "padded" (default: "wood")

11e. For "bunk_bed":
   - "width": float between 80.0 and 140.0 (default: 100.0, units: centimeters)
   - "depth": float between 180.0 and 220.0 (default: 200.0, units: centimeters)
   - "height": float between 140.0 and 220.0 (default: 180.0, units: centimeters)
   - "has_ladder": boolean (default: true)
   - "material": string choice: "wood", "metal" (default: "wood")

11f. For "wardrobe":
   - "width": float between 60.0 and 200.0 (default: 120.0, units: centimeters)
   - "depth": float between 40.0 and 90.0 (default: 60.0, units: centimeters)
   - "height": float between 140.0 and 240.0 (default: 190.0, units: centimeters)
   - "style": string choice: "classic", "modern", "open" (default: "classic")
   - "has_mirror": boolean (default: false)

12. For "storage":
   - "style": string choice: "cabinet", "shelf", "wardrobe", "bookcase" (default: "shelf")
   - "width": float between 40.0 and 200.0 (default: 100.0, units: centimeters)
   - "depth": float between 30.0 and 80.0 (default: 40.0, units: centimeters)
   - "height": float between 60.0 and 220.0 (default: 160.0, units: centimeters)
   - "num_shelves": integer between 1 and 6 (default: 3)
   - "has_doors": boolean (default: false)

13. For "lamp":
   - "height": float between 20.0 and 220.0 (default: 60.0, units: centimeters)
   - "style": string choice: "table", "floor" (default: "table")
   - "shade_shape": string choice: "conical", "cylindrical" (default: "conical")
   - "is_lit": boolean (default: true)

13a. For "chandelier":
   - "width": float between 40.0 and 160.0 (default: 80.0, units: centimeters)
   - "height": float between 30.0 and 150.0 (default: 70.0, units: centimeters)
   - "arms": integer between 3 and 12 (default: 5)
   - "style": string choice: "classic", "modern" (default: "classic")
   - "is_lit": boolean (default: true)

13b. For "painting":
   - "width": float between 30.0 and 200.0 (default: 80.0, units: centimeters)
   - "height": float between 30.0 and 200.0 (default: 60.0, units: centimeters)
   - "frame_width": float between 1.0 and 10.0 (default: 3.0, units: centimeters)
   - "style": string choice: "landscape", "portrait", "square" (default: "landscape")
   - "art_type": string choice: "abstract", "minimalist", "geometric" (default: "abstract")

13c. For "picture_frame":
   - "width": float between 15.0 and 120.0 (default: 40.0, units: centimeters)
   - "height": float between 15.0 and 150.0 (default: 50.0, units: centimeters)
   - "border_thickness": float between 0.8 and 8.0 (default: 2.5, units: centimeters)
   - "style": string choice: "classic", "modern" (default: "modern")
   - "has_matting": boolean (default: true)

13d. For "clock":
   - "width": float between 20.0 and 120.0 (default: 40.0, units: centimeters)
   - "height": float between 20.0 and 120.0 (default: 40.0, units: centimeters)
   - "depth": float between 3.0 and 15.0 (default: 5.0, units: centimeters)
   - "shape": string choice: "circular", "rectangular" (default: "circular")
   - "style": string choice: "wall", "tabletop" (default: "wall")
   - "material": string choice: "wood", "metal", "plastic" (default: "wood")

13e. For "vase":
   - "height": float between 15.0 and 80.0 (default: 35.0, units: centimeters)
   - "diameter": float between 10.0 and 40.0 (default: 18.0, units: centimeters)
   - "neck_diameter": float between 3.0 and 15.0 (default: 6.0, units: centimeters)
   - "style": string choice: "classic", "modern", "geometric" (default: "classic")
   - "material": string choice: "ceramic", "glass", "clay" (default: "ceramic")

13f. For "plant_pot":
   - "width": float between 15.0 and 80.0 (default: 30.0, units: centimeters)
   - "depth": float between 15.0 and 80.0 (default: 30.0, units: centimeters)
   - "height": float between 15.0 and 80.0 (default: 30.0, units: centimeters)
   - "shape": string choice: "cylindrical", "square", "rounded" (default: "cylindrical")
   - "material": string choice: "terracotta", "ceramic", "plastic", "wood" (default: "terracotta")
   - "has_plant": boolean (default: true)

13g. For "rug":
   - "width": float between 60.0 and 400.0 (default: 150.0, units: centimeters)
   - "depth": float between 60.0 and 400.0 (default: 100.0, units: centimeters)
   - "thickness": float between 0.5 and 5.0 (default: 1.2, units: centimeters)
   - "shape": string choice: "rectangular", "circular" (default: "rectangular")
   - "pattern": string choice: "solid", "geometric", "oriental", "striped" (default: "geometric")
   - "color": string choice: "cream", "red", "blue", "grey", "green" (default: "cream")

13h. For building / architecture assets:
   - "wall": "width" 120.0 to 1200.0 cm, "height" 240.0 to 400.0 cm, "thickness" 10.0 to 50.0 cm, "material" choice "brick" or "concrete" or "stone" or "wood" or "plaster", "opening_type" choice "none" or "door" or "window", "opening_width" 60.0 to 220.0 cm, "opening_height" 60.0 to 260.0 cm, "has_trim" boolean
   - "floor": "width" 200.0 to 1600.0 cm, "depth" 200.0 to 1600.0 cm, "thickness" 10.0 to 50.0 cm, "material" choice "wood" or "stone" or "tile" or "concrete", "tile_divisions" integer 0 to 20
   - "ceiling": "width" 200.0 to 1600.0 cm, "depth" 200.0 to 1600.0 cm, "thickness" 5.0 to 30.0 cm, "material" choice "plaster" or "wood" or "concrete", "has_trim" boolean
   - "roof": "width" 240.0 to 2000.0 cm, "depth" 240.0 to 2000.0 cm, "thickness" 10.0 to 40.0 cm, "slope" 15.0 to 60.0 degrees, "roof_style" choice "gabled" or "flat" or "hip" or "mansard", "overhang" 0.0 to 100.0 cm, "material" choice "clay_tiles" or "wood_shingles" or "metal_sheets"
   - "pillar": "height" 200.0 to 800.0 cm, "width" 20.0 to 80.0 cm, "shape" choice "cylindrical" or "square", "material" choice "stone" or "marble" or "concrete" or "wood", "has_capital" boolean
   - "beam": "length" 100.0 to 2000.0 cm, "width" 10.0 to 60.0 cm, "height" 10.0 to 80.0 cm, "material" choice "wood" or "steel" or "concrete"
   - "foundation": "width" 300.0 to 2400.0 cm, "depth" 300.0 to 2400.0 cm, "height" 40.0 to 140.0 cm, "footing_depth" 50.0 to 300.0 cm, "material" choice "concrete" or "stone", "has_footings" boolean
   - "door": "width" 80.0 to 120.0 cm, "height" 200.0 to 220.0 cm, "thickness" 3.0 to 6.0 cm, "material" choice "wood" or "metal", "panel_style" choice "plain" or "inset" or "double", "has_frame" boolean, "has_handle" boolean
   - "window": "width" 60.0 to 200.0 cm, "height" 60.0 to 180.0 cm, "thickness" 6.0 to 20.0 cm, "frame_material" choice "wood" or "aluminum", "has_mullions" boolean, "has_sill" boolean
   - "archway": "width" 100.0 to 400.0 cm, "height" 200.0 to 500.0 cm, "thickness" 15.0 to 80.0 cm, "support_width" 20.0 to 80.0 cm, "material" choice "stone" or "brick"
   - "gate": "width" 100.0 to 1000.0 cm, "height" 100.0 to 500.0 cm, "thickness" 4.0 to 20.0 cm, "material" choice "wood" or "iron", "gate_style" choice "barred" or "solid", "bar_count" integer 3 to 16
   - "stairs": "width" 80.0 to 220.0 cm, "step_count" integer 3 to 18, "step_height" 15.0 to 22.0 cm, "step_depth" 24.0 to 36.0 cm, "material" choice "wood" or "stone" or "concrete", "has_railing" boolean
   - "ladder": "width" 40.0 to 60.0 cm, "height" 120.0 to 500.0 cm, "rung_count" integer 4 to 18, "material" choice "wood" or "metal"
   - "ramp": "width" 80.0 to 500.0 cm, "depth" 120.0 to 1200.0 cm, "height" 15.0 to 300.0 cm, "slope" 5.0 to 30.0 degrees, "material" choice "wood" or "concrete" or "stone", "has_side_curbs" boolean
   - "bridge": "length" 200.0 to 10000.0 cm, "width" 120.0 to 600.0 cm, "height" 60.0 to 800.0 cm, "deck_thickness" 10.0 to 60.0 cm, "material" choice "wood" or "stone" or "steel", "support_count" integer 2 to 12, "has_railings" boolean
   - "balcony": "width" 180.0 to 800.0 cm, "depth" 100.0 to 300.0 cm, "height" 90.0 to 140.0 cm, "thickness" 10.0 to 40.0 cm, "material" choice "wood" or "stone" or "concrete", "has_railings" boolean
   - "fence": "width" 120.0 to 1200.0 cm, "height" 100.0 to 300.0 cm, "thickness" 4.0 to 20.0 cm, "material" choice "wood" or "iron", "fence_style" choice "picket" or "panel", "section_count" integer 3 to 24
   - "railing": "width" 120.0 to 1200.0 cm, "height" 90.0 to 120.0 cm, "depth" 8.0 to 30.0 cm, "material" choice "wood" or "steel", "baluster_count" integer 3 to 24
   - "chimney": "width" 40.0 to 180.0 cm, "depth" 40.0 to 180.0 cm, "height" 100.0 to 500.0 cm, "material" choice "brick" or "stone", "has_cap" boolean
   - "porch": "width" 200.0 to 600.0 cm, "depth" 100.0 to 400.0 cm, "height" 220.0 to 360.0 cm, "material" choice "wood" or "stone" or "concrete", "pillar_count" integer 2 to 6, "has_steps" boolean

14. For "closet":
   - "width": float between 80.0 and 250.0 (default: 150.0, units: centimeters)
   - "depth": float between 50.0 and 100.0 (default: 65.0, units: centimeters)
   - "height": float between 160.0 and 250.0 (default: 200.0, units: centimeters)
   - "door_style": string choice: "sliding", "hinged", "walk_in" (default: "hinged")
   - "doors": integer between 0 and 4 (default: 2)
   - "material": string choice: "wood", "white_laminate", "dark_oak" (default: "wood")

15. For "dresser":
   - "width": float between 60.0 and 180.0 (default: 120.0, units: centimeters)
   - "depth": float between 40.0 and 80.0 (default: 50.0, units: centimeters)
   - "height": float between 60.0 and 130.0 (default: 90.0, units: centimeters)
   - "drawers_rows": integer between 2 and 5 (default: 3)
   - "drawers_cols": integer between 1 and 3 (default: 2)
   - "style": string choice: "modern", "classic", "rustic" (default: "classic")

16. For "cabinet":
   - "width": float between 40.0 and 150.0 (default: 80.0, units: centimeters)
   - "depth": float between 30.0 and 70.0 (default: 40.0, units: centimeters)
   - "height": float between 60.0 and 200.0 (default: 120.0, units: centimeters)
   - "has_glass": boolean (default: false)
   - "shelves": integer between 1 and 5 (default: 3)
   - "style": string choice: "kitchen", "display", "credenza", "bathroom" (default: "display")

17. For "shelf":
   - "width": float between 40.0 and 150.0 (default: 80.0, units: centimeters)
   - "depth": float between 15.0 and 45.0 (default: 25.0, units: centimeters)
   - "height": float between 10.0 and 40.0 (default: 20.0, units: centimeters)
   - "material": string choice: "wood", "metal", "glass" (default: "wood")
   - "brackets": string choice: "none", "floating", "industrial" (default: "floating")

18. For "bookcase":
   - "width": float between 40.0 and 160.0 (default: 90.0, units: centimeters)
   - "depth": float between 25.0 and 60.0 (default: 35.0, units: centimeters)
   - "height": float between 100.0 and 240.0 (default: 180.0, units: centimeters)
   - "shelves": integer between 2 and 7 (default: 4)
   - "has_back_panel": boolean (default: true)
   - "material": string choice: "wood", "painted_mdf", "metal_frame" (default: "wood")

19. For "nightstand":
   - "width": float between 35.0 and 75.0 (default: 50.0, units: centimeters)
   - "depth": float between 30.0 and 60.0 (default: 40.0, units: centimeters)
   - "height": float between 40.0 and 80.0 (default: 60.0, units: centimeters)
   - "drawers": integer between 0 and 3 (default: 1)
   - "has_open_shelf": boolean (default: true)
   - "style": string choice: "modern", "classic", "mid_century" (default: "modern")

 20. For "tv_stand":
    - "width": float between 100.0 and 220.0 (default: 150.0, units: centimeters)
    - "depth": float between 35.0 and 60.0 (default: 45.0, units: centimeters)
    - "height": float between 30.0 and 85.0 (default: 50.0, units: centimeters)
    - "compartments": integer between 2 and 5 (default: 3)
    - "has_doors": boolean (default: false)
    - "style": string choice: "modern", "industrial", "classic" (default: "modern")

 21. For "fridge":
    - "width": float between 50.0 and 100.0 (default: 75.0, units: centimeters)
    - "depth": float between 50.0 and 90.0 (default: 70.0, units: centimeters)
    - "height": float between 120.0 and 220.0 (default: 180.0, units: centimeters)
    - "style": string choice: "single_door", "double_door", "french_door" (default: "double_door")
    - "material": string choice: "stainless_steel", "white", "black_matte" (default: "stainless_steel")
    - "has_dispenser": boolean (default: false)

 22. For "stove":
    - "width": float between 50.0 and 100.0 (default: 75.0, units: centimeters)
    - "depth": float between 50.0 and 80.0 (default: 60.0, units: centimeters)
    - "height": float between 80.0 and 100.0 (default: 90.0, units: centimeters)
    - "burners": integer between 2 and 6 (default: 4)
    - "style": string choice: "gas", "electric_glass" (default: "gas")
    - "material": string choice: "stainless_steel", "black", "white" (default: "stainless_steel")

 23. For "oven":
    - "width": float between 50.0 and 90.0 (default: 60.0, units: centimeters)
    - "depth": float between 45.0 and 75.0 (default: 55.0, units: centimeters)
    - "height": float between 45.0 and 90.0 (default: 60.0, units: centimeters)
    - "has_glass_window": boolean (default: true)
    - "shelves": integer between 1 and 4 (default: 2)
    - "style": string choice: "built_in", "freestanding" (default: "built_in")

 24. For "microwave":
    - "width": float between 40.0 and 70.0 (default: 55.0, units: centimeters)
    - "depth": float between 30.0 and 50.0 (default: 40.0, units: centimeters)
    - "height": float between 25.0 and 45.0 (default: 35.0, units: centimeters)
    - "style": string choice: "countertop", "built_in" (default: "countertop")
    - "has_glass_door": boolean (default: true)

 25. For "sink":
    - "width": float between 45.0 and 120.0 (default: 80.0, units: centimeters)
    - "depth": float between 45.0 and 80.0 (default: 60.0, units: centimeters)
    - "height": float between 70.0 and 100.0 (default: 85.0, units: centimeters)
    - "style": string choice: "single_basin", "double_basin", "pedestal", "wall_mounted" (default: "single_basin")
    - "faucet_style": string choice: "goose_neck", "standard" (default: "goose_neck")

 26. For "countertop":
    - "width": float between 60.0 and 240.0 (default: 120.0, units: centimeters)
    - "depth": float between 50.0 and 80.0 (default: 60.0, units: centimeters)
    - "height": float between 80.0 and 100.0 (default: 90.0, units: centimeters)
    - "has_drawers": boolean (default: true)
    - "has_backsplash": boolean (default: true)
    - "material": string choice: "marble", "granite", "wood" (default: "marble")

 27. For "cupboard":
    - "width": float between 60.0 and 180.0 (default: 100.0, units: centimeters)
    - "depth": float between 35.0 and 70.0 (default: 45.0, units: centimeters)
    - "height": float between 120.0 and 220.0 (default: 180.0, units: centimeters)
    - "style": string choice: "hutch", "pantry" (default: "hutch")
    - "has_drawers": boolean (default: true)
    - "shelves": integer between 1 and 5 (default: 3)

 28. For "kitchen_island":
    - "width": float between 100.0 and 240.0 (default: 160.0, units: centimeters)
    - "depth": float between 60.0 and 120.0 (default: 90.0, units: centimeters)
    - "height": float between 80.0 and 100.0 (default: 90.0, units: centimeters)
    - "overhang_depth": float between 10.0 and 40.0 (default: 25.0, units: centimeters)
    - "has_stools": boolean (default: true)
    - "stools_count": integer between 0 and 4 (default: 2)
    - "material": string choice: "wood_marble", "industrial_metal" (default: "wood_marble")

 29. For "dining_set":
    - "table_width": float between 120.0 and 260.0 (default: 180.0, units: centimeters)
    - "table_depth": float between 70.0 and 120.0 (default: 90.0, units: centimeters)
    - "table_height": float between 65.0 and 90.0 (default: 75.0, units: centimeters)
    - "chair_count": integer between 2 and 10 (default: 6)
    - "chair_style": string choice: "classic", "modern" (default: "classic")
    - "material": string choice: "oak", "walnut" (default: "oak")

 30. For "toilet":
    - "width": float between 35.0 and 70.0 (default: 50.0, units: centimeters)
    - "depth": float between 55.0 and 90.0 (default: 70.0, units: centimeters)
    - "height": float between 65.0 and 95.0 (default: 80.0, units: centimeters)
    - "bowl_shape": string choice: "round", "elongated" (default: "elongated")
    - "has_lid_open": boolean (default: false)
    - "tank_width": float between 30.0 and 60.0 (default: 45.0, units: centimeters)
    - "tank_depth": float between 15.0 and 30.0 (default: 20.0, units: centimeters)

 31. For "bathtub":
    - "width": float between 120.0 and 200.0 (default: 160.0, units: centimeters)
    - "depth": float between 60.0 and 100.0 (default: 75.0, units: centimeters)
    - "height": float between 45.0 and 80.0 (default: 60.0, units: centimeters)
    - "style": string choice: "freestanding", "alcove", "clawfoot" (default: "freestanding")
    - "material": string choice: "ceramic", "copper", "stone" (default: "ceramic")
    - "has_faucet": boolean (default: true)

 32. For "shower":
    - "width": float between 70.0 and 150.0 (default: 90.0, units: centimeters)
    - "depth": float between 70.0 and 150.0 (default: 90.0, units: centimeters)
    - "height": float between 180.0 and 240.0 (default: 210.0, units: centimeters)
    - "enclosure": string choice: "glass_door", "curtain", "none" (default: "glass_door")
    - "head_type": string choice: "rain", "standard", "handheld" (default: "standard")
    - "material": string choice: "chrome", "brass", "matte_black" (default: "chrome")

 33. For "mirror":
    - "width": float between 30.0 and 120.0 (default: 60.0, units: centimeters)
    - "height": float between 30.0 and 150.0 (default: 80.0, units: centimeters)
    - "shape": string choice: "rectangular", "circular", "oval" (default: "rectangular")
    - "border_style": string choice: "metallic", "wood", "frameless" (default: "metallic")
    - "border_color": string choice: "gold", "chrome", "black", "wood" (default: "black")

 34. For "towel_rack":
    - "width": float between 30.0 and 120.0 (default: 60.0, units: centimeters)
    - "depth": float between 8.0 and 30.0 (default: 15.0, units: centimeters)
    - "height": float between 10.0 and 60.0 (default: 20.0, units: centimeters)
    - "bar_style": string choice: "single_bar", "double_bar", "shelf_style" (default: "single_bar")
    - "material": string choice: "chrome", "brass", "matte_black", "wood" (default: "chrome")
    - "has_towel": boolean (default: true)
    - "towel_color": string choice: "white", "blue", "gray", "green" (default: "white")

 35. For tree assets:
    - "oak_tree": "height" 320.0 to 1200.0 cm, "canopy_width" 180.0 to 900.0 cm, "trunk_radius" 8.0 to 60.0 cm
    - "pine_tree": "height" 400.0 to 1400.0 cm, "canopy_width" 120.0 to 500.0 cm, "trunk_radius" 6.0 to 40.0 cm, "layers" integer 3 to 8
    - "birch_tree": "height" 300.0 to 1100.0 cm, "canopy_width" 120.0 to 420.0 cm, "trunk_radius" 5.0 to 30.0 cm
    - "palm_tree": "height" 300.0 to 1000.0 cm, "frond_span" 120.0 to 500.0 cm, "trunk_radius" 6.0 to 30.0 cm
    - "dead_tree": "height" 250.0 to 900.0 cm, "branch_count" integer 3 to 12, "trunk_radius" 6.0 to 40.0 cm
    - "sapling": "height" 40.0 to 250.0 cm, "canopy_width" 20.0 to 140.0 cm

 36. For ground cover assets:
    - "grass": "width" 40.0 to 200.0 cm, "height" 10.0 to 60.0 cm, "density" integer 8 to 60
    - "bush": "width" 60.0 to 240.0 cm, "height" 40.0 to 160.0 cm, "density" integer 5 to 18
    - "shrub": "width" 60.0 to 240.0 cm, "height" 60.0 to 220.0 cm, "stems" integer 3 to 12
    - "fern": "width" 40.0 to 180.0 cm, "height" 30.0 to 120.0 cm, "fronds" integer 4 to 12
    - "flower": "height" 15.0 to 90.0 cm, "petals" integer 4 to 16, "bloom_color" choice "pink" or "yellow"
    - "moss": "width" 40.0 to 200.0 cm, "depth" 30.0 to 180.0 cm, "thickness" 4.0 to 30.0 cm

 37. For rock assets:
    - "small_rock": "width" 15.0 to 120.0 cm, "depth" 12.0 to 100.0 cm, "height" 10.0 to 80.0 cm
    - "boulder": "width" 80.0 to 320.0 cm, "depth" 60.0 to 260.0 cm, "height" 50.0 to 220.0 cm
    - "rock_cluster": "width" 60.0 to 320.0 cm, "depth" 40.0 to 240.0 cm, "rocks" integer 3 to 12
    - "cliff_section": "width" 120.0 to 500.0 cm, "depth" 60.0 to 260.0 cm, "height" 120.0 to 520.0 cm

 38. For natural prop assets:
    - "log": "length" 60.0 to 500.0 cm, "radius" 6.0 to 60.0 cm
    - "tree_stump": "radius" 10.0 to 90.0 cm, "height" 10.0 to 120.0 cm
    - "fallen_tree": "length" 120.0 to 700.0 cm, "trunk_radius" 6.0 to 50.0 cm, "has_leaves" boolean
    - "mushroom": "cap_diameter" 8.0 to 80.0 cm, "height" 6.0 to 80.0 cm
    - "vine": "length" 60.0 to 600.0 cm, "leaf_density" integer 3 to 20
    - "root": "width" 60.0 to 320.0 cm, "depth" 40.0 to 240.0 cm, "height" 10.0 to 120.0 cm

 39. For water feature assets:
    - "pond": "width" 100.0 to 420.0 cm, "depth" 80.0 to 340.0 cm, "bank_height" 6.0 to 60.0 cm
    - "river_segment": "width" 60.0 to 300.0 cm, "length" 120.0 to 700.0 cm, "curve" 0.0 to 180.0 cm
    - "waterfall": "width" 60.0 to 260.0 cm, "height" 80.0 to 500.0 cm, "pool_radius" 40.0 to 240.0 cm
    - "stream": "width" 20.0 to 160.0 cm, "length" 80.0 to 500.0 cm, "curve" 0.0 to 120.0 cm

Unit Conversion Note:
If the user specifies dimensions in different units (like meters for indoor or nature assets, or centimeters for a barrel/crate), convert them to the unit requested by the schema. All listed assets except "barrel" and "crate" use centimeters. "barrel" and "crate" use meters. If a parameter is not specified, omit it or let it fall back to the default.


IMPORTANT DISAMBIGUATION:
- If the user says "dining table", "dinner table", "kitchen table", or "seats N people" → use "dining_table".
- If the user says "coffee table", "living room table", "low table", or "lounge table" → use "coffee_table".
- Otherwise use "table" for a generic writing desk or small table.
- If the user says "desk", "office desk", "computer desk", "workstation", or "writing desk" → use "desk".
- If the user says "stool", "bar stool", "counter stool", or "bar seat" (which has no backrest) → use "stool".
- If the user says "chair", "dining chair", "seat with back" → use "chair".
- If the user says "dagger", "knife", "dirk", or "stiletto" → use "dagger", not "sword".
- If the user says "sword", "broadsword", "longsword", or "shortsword" → use "sword".
- If the user says "war hammer", "warhammer", or "hammer weapon" → use "hammer", not a tool or prop.
- If the user says "mace" or "morningstar" → use "mace", not "hammer".
- If the user says "spear", "pike", or "javelin" → use "spear".
- If the user says "halberd", "poleaxe", or "polearm" → use "halberd", not "axe" or "spear".
- If the user says "staff" and it is clearly magical → use "magic_staff"; otherwise use "staff".
- If the user says "bow", "longbow", "shortbow", or "recurve bow" → use "bow".
- If the user says "crossbow" → use "crossbow".
- If the user says "crossbow bolt" or "bolt" in a ranged-weapon context → use "bolt", not "arrow".
- If the user says "arrow" → use "arrow".
- If the user says "wand" → use "wand".
- If the user says "orb" or "magic orb" → use "orb".
- If the user says "bench", "park bench", "garden bench", "dining bench", "wooden bench" → use "bench".
- If the user says "couch", "sectional", "sectional couch", "comfy couch", "sofa bed" → use "couch".
- If the user says "armchair", "lounge chair", "recliner", "single seater", "cushioned armchair" → use "armchair".
- If the user says "sofa", "3-seater", "fabric sofa" → use "sofa".
- If the user says "bed", "double bed", "queen bed", "king bed", "single bed", "canopy bed" → use "bed".
- If the user says "bunk bed", "loft bed", "double decker bed" → use "bunk_bed".
- If the user says "wardrobe", "armoire", "clothes cupboard" → use "wardrobe".
- If the user says "closet", "walk-in closet", "built-in closet" → use "closet".
- If the user says "dresser", "chest of drawers", "tallboy", "bureau" → use "dresser".
- If the user says "cabinet", "credenza", "display cabinet", "kitchen cabinet" → use "cabinet".
- If the user says "storage", "shelves", "bookcase" → use "storage".
- If the user says "shelf", "wall shelf", "hanging shelf" → use "shelf".
- If the user says "bookcase", "bookshelf", "library shelving" → use "bookcase".
- If the user says "nightstand", "bedside table", "bed table" → use "nightstand".
- If the user says "tv stand", "media console", "credenza tv", "lowboard" → use "tv_stand".
- If the user says "fridge", "refrigerator", "freezer" → use "fridge".
- If the user says "stove", "cooktop", "range", "stove top" → use "stove".
- If the user says "oven", "baking oven", "toaster oven" → use "oven".
- If the user says "microwave", "microwave oven" → use "microwave".
- If the user says "sink", "basin", "washbasin", "wash basin" → use "sink".
- If the user says "countertop", "counter", "kitchen counter" → use "countertop".
- If the user says "cupboard", "hutch", "kitchen cupboard", "china cupboard" → use "cupboard".
- If the user says "kitchen island", "island table", "cooking island" → use "kitchen_island".
- If the user says "dining set", "table and chairs", "dining table set" → use "dining_set".
- If the user says "toilet", "commode", "water closet" → use "toilet".
- If the user says "bathtub", "tub", "bath tub" → use "bathtub".
- If the user says "shower", "shower stall", "shower cabin" → use "shower".
- If the user says "mirror", "looking glass" → use "mirror".
- If the user says "towel rack", "towel bar", "towel rail" → use "towel_rack".
- If the user says "clock", "wall clock", "table clock", "timepiece" → use "clock".
- If the user says "vase", "urn", "flower holder" → use "vase".
- If the user says "plant pot", "flower pot", "pot", "plant_pot" → use "plant_pot".
- If the user says "rug", "carpet", "mat" → use "rug".
- If the user says "wall section", "partition wall", "brick wall", or "interior wall" → use "wall".
- If the user says "floor slab", "tile floor", "wood floor", or "concrete floor" → use "floor".
- If the user says "ceiling", "ceiling panel", or "drop ceiling" → use "ceiling".
- If the user says "roof", "gabled roof", "hip roof", or "mansard roof" → use "roof".
- If the user says "pillar" or "column" → use "pillar".
- If the user says "beam", "support beam", or "ceiling beam" → use "beam".
- If the user says "foundation", "foundation slab", "base slab", or "footing" → use "foundation".
- If the user says "door", "entry door", "interior door", or "door panel" → use "door" unless they clearly asked for a wall with a door opening.
- If the user says "window", "glass window", or "window frame" → use "window" unless they clearly asked for a wall with a window opening.
- If the user says "archway", "arch opening", or "stone arch" → use "archway".
- If the user says "gate", "garden gate", "iron gate", or "wood gate" → use "gate".
- If the user says "stairs", "staircase", or "stairway" → use "stairs".
- If the user says "ladder" → use "ladder".
- If the user says "ramp", "inclined ramp", or "access ramp" → use "ramp".
- If the user says "bridge", "foot bridge", or "footbridge" → use "bridge".
- If the user says "balcony" → use "balcony".
- If the user says "fence", "picket fence", or "privacy fence" → use "fence".
- If the user says "railing" or "handrail" → use "railing".
- If the user says "chimney" → use "chimney".
- If the user says "porch", "entry porch", or "front porch" → use "porch".
"""


class OllamaClient:
    def __init__(self, host: str = None, model: str = None):
        self.host = host or os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        # Initialize the official Ollama client
        self.client = ollama.Client(host=self.host)
        
    def generate_json_spec(self, user_prompt: str) -> Dict[str, Any]:
        """Queries local Ollama to parse the user prompt and extract structured JSON parameters."""
        logger.info(f"Sending prompt to Ollama ({self.model}): '{user_prompt}'")
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                format="json",  # Forces the model to return valid JSON
                options={"temperature": 0.0}  # Enforces deterministic extraction
            )
            
            content = response.get("message", {}).get("content", "").strip()
            logger.info(f"Ollama raw response content: {content}")
            
            # Parse response content as JSON dictionary
            spec = json.loads(content)
            return spec
            
        except Exception as e:
            logger.error(f"Failed to generate spec from Ollama: {e}")
            raise RuntimeError(f"Ollama extraction failed: {e}")
