ROOM_DIMENSIONS = {
    "single_room_size": 3.0,
    "room_width": 4.2,
    "room_depth": 3.6,
    "ensuite_depth": 2.2,
    "hallway_depth": 1.25,
    "room_height": 2.35,
    "wall_thickness": 0.12,
}

DEFAULT_HOUSE_CONFIG = {
    "bedrooms": 2,
    "bathrooms": 2,
    "kitchens": 1,
    "living_rooms": 1,
    "dining_rooms": 1,
    "attach_bathroom_to_bedroom": True,
    "ensuite_bathrooms": 1,
    "road_lanes": 2,
    "sidewalk_width": 1.8,
    "setback_width": 2.4,
    "add_crosswalks": True,
}

DEFAULT_WALL_COLORS = {
    "north": "#334155",
    "south": "#475569",
    "east": "#3b4257",
    "west": "#516175",
    "interior": "#64748b",
}

ROOM_TYPE_PRIORITY = {
    "living": 0,
    "dining": 1,
    "kitchen": 2,
    "bedroom": 3,
    "bathroom": 4,
    "outdoor": 5,
    "street": 6,
}

PROMPT_ZONE_KEYWORDS = {
    "bathroom": ("bath", "bathroom", "pedestal", "shower", "toilet", "towel", "vanity"),
    "bedroom": ("bed", "bedroom", "blanket", "closet", "dresser", "nightstand", "pillow", "wardrobe"),
    "kitchen": ("bar stool", "counter", "cook", "dining", "fridge", "island", "kitchen", "microwave", "oven", "sink cabinet", "stove"),
    "living": ("armchair", "bookcase", "coffee table", "couch", "living", "lounge", "sofa", "tv"),
    "dining": ("dining", "dinner", "banquette", "buffet"),
}

ROOM_TARGETS_BY_TYPE = {
    "armchair": ("living",),
    "bathtub": ("bathroom",),
    "bed": ("bedroom",),
    "bench": ("living", "dining"),
    "bookcase": ("living", "bedroom", "dining"),
    "bunk_bed": ("bedroom",),
    "chair": ("dining", "kitchen"),
    "closet": ("bedroom",),
    "coffee_table": ("living",),
    "countertop": ("kitchen",),
    "couch": ("living",),
    "cupboard": ("kitchen",),
    "desk": ("bedroom",),
    "dining_table": ("dining", "kitchen"),
    "dresser": ("bedroom",),
    "fridge": ("kitchen",),
    "microwave": ("kitchen",),
    "nightstand": ("bedroom",),
    "oven": ("kitchen",),
    "shower": ("bathroom",),
    "sofa": ("living",),
    "stool": ("dining", "kitchen"),
    "stove": ("kitchen",),
    "table": ("dining", "kitchen"),
    "toilet": ("bathroom",),
    "towel_rack": ("bathroom",),
    "tv_stand": ("living",),
    "wardrobe": ("bedroom",),
}

OUTDOOR_TARGETS_BY_TYPE = {
    "street_lamp": ("outdoor",),
    "traffic_light": ("street", "outdoor"),
    "road_sign": ("outdoor", "street"),
    "street_bench": ("outdoor",),
    "mailbox": ("outdoor",),
    "trash_can": ("outdoor",),
    "bus_stop": ("outdoor",),
    "phone_booth": ("outdoor",),
    "car": ("street",),
    "truck": ("street",),
    "bike": ("outdoor", "street"),
    "motorcycle": ("street",),
    "tractor": ("street",),
    "battle_tank": ("street",),
    "fence": ("outdoor",),
    "gate": ("outdoor",),
    "railing": ("outdoor",),
    "bridge": ("outdoor",),
    "oak_tree": ("outdoor",),
    "pine_tree": ("outdoor",),
    "birch_tree": ("outdoor",),
    "palm_tree": ("outdoor",),
    "dead_tree": ("outdoor",),
    "sapling": ("outdoor",),
    "grass": ("outdoor",),
    "bush": ("outdoor",),
    "shrub": ("outdoor",),
    "fern": ("outdoor",),
    "flower": ("outdoor",),
    "moss": ("outdoor",),
    "small_rock": ("outdoor",),
    "boulder": ("outdoor",),
    "rock_cluster": ("outdoor",),
    "cliff_section": ("outdoor",),
    "log": ("outdoor",),
    "tree_stump": ("outdoor",),
    "fallen_tree": ("outdoor",),
    "mushroom": ("outdoor",),
    "vine": ("outdoor",),
    "root": ("outdoor",),
    "pond": ("outdoor",),
    "river_segment": ("outdoor",),
    "waterfall": ("outdoor",),
    "stream": ("outdoor",),
    "terrain": ("outdoor",),
    "hill": ("outdoor",),
    "mountain": ("outdoor",),
    "cliff": ("outdoor",),
    "valley": ("outdoor",),
    "cave": ("outdoor",),
    "ground_tile": ("outdoor",),
    "road_tile": ("street",),
    "path_tile": ("outdoor",),
    "river_tile": ("outdoor",),
    "dungeon_tile": ("outdoor",),
}

SINGLE_ROOM_LAYOUTS = {"bedroom", "living", "dining", "kitchen", "bathroom"}
CITY_LANE_WIDTH = 2.6


def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))


def to_int(value, fallback):
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def to_float(value, fallback):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def normalize_color(value, fallback):
    if isinstance(value, str) and len(value) == 7 and value.startswith("#"):
        try:
            int(value[1:], 16)
            return value.lower()
        except ValueError:
            return fallback
    return fallback


def normalize_prompt(prompt):
    return str(prompt or "").lower()


def infer_prompt_room_type(prompt):
    normalized = normalize_prompt(prompt)
    for room_type, keywords in PROMPT_ZONE_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return room_type
    return None


def normalize_wall_colors(wall_colors=None):
    wall_colors = wall_colors or {}
    return {
        key: normalize_color(wall_colors.get(key), DEFAULT_WALL_COLORS[key])
        for key in DEFAULT_WALL_COLORS
    }


def normalize_house_config(house_config=None):
    house_config = house_config or {}
    bedrooms = clamp(to_int(house_config.get("bedrooms"), DEFAULT_HOUSE_CONFIG["bedrooms"]), 1, 6)
    bathrooms = clamp(to_int(house_config.get("bathrooms"), DEFAULT_HOUSE_CONFIG["bathrooms"]), 1, 6)
    kitchens = clamp(to_int(house_config.get("kitchens"), DEFAULT_HOUSE_CONFIG["kitchens"]), 1, 3)
    living_rooms = clamp(to_int(house_config.get("living_rooms", house_config.get("livingRooms")), DEFAULT_HOUSE_CONFIG["living_rooms"]), 1, 3)
    dining_rooms = clamp(to_int(house_config.get("dining_rooms", house_config.get("diningRooms")), DEFAULT_HOUSE_CONFIG["dining_rooms"]), 0, 3)
    road_lanes = clamp(to_int(house_config.get("road_lanes", house_config.get("roadLanes")), DEFAULT_HOUSE_CONFIG["road_lanes"]), 1, 4)
    sidewalk_width = clamp(
        to_float(house_config.get("sidewalk_width", house_config.get("sidewalkWidth")), DEFAULT_HOUSE_CONFIG["sidewalk_width"]),
        0.8,
        6.0,
    )
    setback_width = clamp(
        to_float(house_config.get("setback_width", house_config.get("setbackWidth")), DEFAULT_HOUSE_CONFIG["setback_width"]),
        0.8,
        8.0,
    )
    attach_bathroom_to_bedroom = house_config.get("attach_bathroom_to_bedroom", house_config.get("attachBathroomToBedroom", True)) is not False
    add_crosswalks = house_config.get("add_crosswalks", house_config.get("addCrosswalks", True)) is not False
    requested_ensuites = clamp(
        to_int(house_config.get("ensuite_bathrooms", house_config.get("ensuiteBathrooms")), DEFAULT_HOUSE_CONFIG["ensuite_bathrooms"]),
        0,
        min(bedrooms, bathrooms),
    ) if attach_bathroom_to_bedroom else 0

    return {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "kitchens": kitchens,
        "living_rooms": living_rooms,
        "dining_rooms": dining_rooms,
        "attach_bathroom_to_bedroom": attach_bathroom_to_bedroom,
        "ensuite_bathrooms": requested_ensuites,
        "road_lanes": road_lanes,
        "sidewalk_width": round(float(sidewalk_width), 2),
        "setback_width": round(float(setback_width), 2),
        "add_crosswalks": add_crosswalks,
    }


def build_centered_positions(count, width):
    return [(-((count - 1) * width) / 2.0) + index * width for index in range(max(count, 0))]


def create_rect_space(space_id, room_type, label, center_x, center_z, width, depth, row, attached_to=None, material_key="floor"):
    return {
        "id": space_id,
        "type": room_type,
        "label": label,
        "row": row,
        "attached_to": attached_to,
        "material_key": material_key,
        "width": width,
        "depth": depth,
        "center": (center_x, 0.0, center_z),
        "rect": {
            "min_x": center_x - width / 2.0,
            "max_x": center_x + width / 2.0,
            "min_z": center_z - depth / 2.0,
            "max_z": center_z + depth / 2.0,
        },
    }


def create_wall_segment(segment_id, orientation, length, center_x, center_z, interior=False):
    room_height = ROOM_DIMENSIONS["room_height"]
    wall_thickness = ROOM_DIMENSIONS["wall_thickness"]
    if orientation in ("north", "south"):
        size = (length, room_height, wall_thickness)
    else:
        size = (wall_thickness, room_height, length)
    return {
        "id": segment_id,
        "orientation": orientation,
        "interior": interior,
        "material_key": "interior" if interior else orientation,
        "size": size,
        "position": (center_x, room_height / 2.0, center_z),
    }


def add_row_wall_segments(rooms, row_kind, segments):
    if not rooms:
        return

    wall_thickness = ROOM_DIMENSIONS["wall_thickness"]
    sorted_rooms = sorted(rooms, key=lambda room: room["rect"]["min_x"])

    for index, room in enumerate(sorted_rooms):
        if index == 0:
            segments.append(
                create_wall_segment(
                    f"{room['id']}_west_outer",
                    "west",
                    room["depth"],
                    room["rect"]["min_x"] - wall_thickness / 2.0,
                    room["center"][2],
                )
            )
        else:
            segments.append(
                create_wall_segment(
                    f"{room['id']}_west_partition",
                    "west",
                    room["depth"],
                    room["rect"]["min_x"],
                    room["center"][2],
                    True,
                )
            )

        if index == len(sorted_rooms) - 1:
            segments.append(
                create_wall_segment(
                    f"{room['id']}_east_outer",
                    "east",
                    room["depth"],
                    room["rect"]["max_x"] + wall_thickness / 2.0,
                    room["center"][2],
                )
            )

        if row_kind == "public":
            segments.append(
                create_wall_segment(
                    f"{room['id']}_north_outer",
                    "north",
                    room["width"],
                    room["center"][0],
                    room["rect"]["min_z"] - wall_thickness / 2.0,
                )
            )

        if row_kind == "private" and not room.get("has_ensuite"):
            segments.append(
                create_wall_segment(
                    f"{room['id']}_south_outer",
                    "south",
                    room["width"],
                    room["center"][0],
                    room["rect"]["max_z"] + wall_thickness / 2.0,
                )
            )

        if row_kind == "ensuite":
            segments.append(
                create_wall_segment(
                    f"{room['id']}_south_outer",
                    "south",
                    room["width"],
                    room["center"][0],
                    room["rect"]["max_z"] + wall_thickness / 2.0,
                )
            )


def build_single_room_walls(room):
    wall_thickness = ROOM_DIMENSIONS["wall_thickness"]
    return [
        create_wall_segment(
            f"{room['id']}_north_outer",
            "north",
            room["width"],
            room["center"][0],
            room["rect"]["min_z"] - wall_thickness / 2.0,
        ),
        create_wall_segment(
            f"{room['id']}_west_outer",
            "west",
            room["depth"],
            room["rect"]["min_x"] - wall_thickness / 2.0,
            room["center"][2],
        ),
        create_wall_segment(
            f"{room['id']}_east_outer",
            "east",
            room["depth"],
            room["rect"]["max_x"] + wall_thickness / 2.0,
            room["center"][2],
        ),
    ]


def build_house_walls(public_rooms, private_rooms, ensuite_rooms):
    segments = []
    add_row_wall_segments(public_rooms, "public", segments)
    add_row_wall_segments(private_rooms, "private", segments)
    add_row_wall_segments(ensuite_rooms, "ensuite", segments)
    return segments


def get_single_room_placement(asset_type, index):
    offset = index * 0.25

    if asset_type == "rug":
        return {"pos": (0.0, 0.01 + index * 0.005, 0.0), "rot_y": 0.0, "scale": 1.2}
    if asset_type == "coffee_table":
        return {"pos": (0.0, 0.0, 0.1 + offset), "rot_y": 0.0, "scale": 1.0}
    if asset_type in ("table", "dining_table"):
        return {"pos": (0.0, 0.0, 0.3 + offset), "rot_y": 0.0, "scale": 1.0}
    if asset_type == "desk":
        return {"pos": (-0.6, 0.0, -1.0 + offset), "rot_y": 0.0, "scale": 1.0}
    if asset_type in ("chair", "stool"):
        if index == 0:
            return {"pos": (-0.6, 0.0, -0.6), "rot_y": 0.0, "scale": 1.0}
        if index == 1:
            return {"pos": (-0.5, 0.0, 0.3), "rot_y": 1.5707963267948966, "scale": 1.0}
        if index == 2:
            return {"pos": (0.5, 0.0, 0.3), "rot_y": -1.5707963267948966, "scale": 1.0}
        return {"pos": (0.0, 0.0, 0.8 + offset), "rot_y": 3.141592653589793, "scale": 1.0}
    if asset_type in ("sofa", "couch"):
        return {"pos": (-1.2, 0.0, 0.4 + offset), "rot_y": 1.5707963267948966, "scale": 1.0}
    if asset_type == "armchair":
        return {"pos": (1.1, 0.0, 0.8 + offset), "rot_y": -0.7853981633974483, "scale": 1.0}
    if asset_type == "bench":
        return {"pos": (0.7, 0.0, 1.0 + offset), "rot_y": 3.141592653589793, "scale": 1.0}
    if asset_type in ("bed", "bunk_bed"):
        return {"pos": (0.4, 0.0, -1.1 + offset), "rot_y": 3.141592653589793, "scale": 1.0}
    if asset_type == "nightstand":
        return {"pos": (-0.4 + offset, 0.0, -1.3), "rot_y": 3.141592653589793, "scale": 1.0}
    if asset_type in ("wardrobe", "closet", "dresser", "cabinet", "cupboard"):
        return {"pos": (1.2, 0.0, -0.6 + offset), "rot_y": -1.5707963267948966, "scale": 1.0}
    if asset_type in ("bookcase", "shelf"):
        return {"pos": (1.2, 0.0, 0.3 + offset), "rot_y": -1.5707963267948966, "scale": 1.0}
    if asset_type == "tv_stand":
        return {"pos": (-1.2, 0.0, -0.4 + offset), "rot_y": 1.5707963267948966, "scale": 1.0}
    if asset_type == "lamp":
        return {"pos": (1.2, 0.0, -1.2 + offset), "rot_y": 0.0, "scale": 1.0}
    if asset_type == "clock":
        return {"pos": (0.8 - offset * 0.5, 1.4, -1.46), "rot_y": 0.0, "scale": 1.0}
    if asset_type in ("painting", "picture_frame"):
        return {"pos": (-0.6 + offset, 1.3, -1.46), "rot_y": 0.0, "scale": 1.0}
    if asset_type == "mirror":
        return {"pos": (-1.46, 1.3, 0.0 + offset), "rot_y": 1.5707963267948966, "scale": 1.0}
    if asset_type == "vase":
        return {"pos": (0.0, 0.75, 0.3 + offset), "rot_y": 0.0, "scale": 0.6}
    if asset_type == "plant_pot":
        return {"pos": (-1.1 + offset * 0.3, 0.0, 1.2 + offset), "rot_y": 0.0, "scale": 0.9}
    if asset_type == "fridge":
        return {"pos": (-1.2, 0.0, -1.1 + offset), "rot_y": 3.141592653589793, "scale": 1.0}
    if asset_type in ("stove", "oven"):
        return {"pos": (-0.6, 0.0, -1.25 + offset), "rot_y": 3.141592653589793, "scale": 1.0}
    if asset_type in ("sink", "countertop"):
        return {"pos": (0.1 + offset, 0.0, -1.25), "rot_y": 3.141592653589793, "scale": 1.0}
    if asset_type == "microwave":
        return {"pos": (0.45 + offset * 0.2, 0.95, -1.18), "rot_y": 3.141592653589793, "scale": 0.7}
    if asset_type == "toilet":
        return {"pos": (1.2, 0.0, -1.1 + offset), "rot_y": 3.141592653589793, "scale": 1.0}
    if asset_type == "bathtub":
        return {"pos": (0.5, 0.0, -1.25 + offset), "rot_y": 3.141592653589793, "scale": 1.0}
    if asset_type == "shower":
        return {"pos": (-1.2, 0.0, -1.1 + offset), "rot_y": 3.141592653589793, "scale": 1.0}
    if asset_type == "towel_rack":
        return {"pos": (1.46, 1.2, 0.3 + offset), "rot_y": -1.5707963267948966, "scale": 1.0}

    return {"pos": (-1.0 + index * 0.4, 0.0, 1.0), "rot_y": 0.0, "scale": 1.0}


def scale_placement_to_room(placement, room):
    x_scale = room["width"] / ROOM_DIMENSIONS["single_room_size"]
    z_scale = room["depth"] / ROOM_DIMENSIONS["single_room_size"]
    return {
        "pos": (
            placement["pos"][0] * x_scale,
            placement["pos"][1],
            placement["pos"][2] * z_scale,
        ),
        "rot_y": placement["rot_y"],
        "scale": placement["scale"],
    }


def build_house_plan(house_config=None):
    normalized = normalize_house_config(house_config)
    room_width = ROOM_DIMENSIONS["room_width"]
    room_depth = ROOM_DIMENSIONS["room_depth"]
    ensuite_depth = ROOM_DIMENSIONS["ensuite_depth"]
    hallway_depth = ROOM_DIMENSIONS["hallway_depth"]
    wall_thickness = ROOM_DIMENSIONS["wall_thickness"]

    public_definitions = (
        [
            {
                "id": f"living_{index + 1}",
                "type": "living",
                "label": f"Living Room {index + 1}" if normalized["living_rooms"] > 1 else "Living Room",
            }
            for index in range(normalized["living_rooms"])
        ]
        + [
            {
                "id": f"dining_{index + 1}",
                "type": "dining",
                "label": f"Dining Room {index + 1}" if normalized["dining_rooms"] > 1 else "Dining Room",
            }
            for index in range(normalized["dining_rooms"])
        ]
        + [
            {
                "id": f"kitchen_{index + 1}",
                "type": "kitchen",
                "label": f"Kitchen {index + 1}" if normalized["kitchens"] > 1 else "Kitchen",
            }
            for index in range(normalized["kitchens"])
        ]
    )

    shared_bathrooms = max(normalized["bathrooms"] - normalized["ensuite_bathrooms"], 0)
    private_definitions = (
        [
            {
                "id": f"bedroom_{index + 1}",
                "type": "bedroom",
                "label": f"Bedroom {index + 1}" if normalized["bedrooms"] > 1 else "Bedroom",
            }
            for index in range(normalized["bedrooms"])
        ]
        + [
            {
                "id": f"bathroom_shared_{index + 1}",
                "type": "bathroom",
                "label": f"Bathroom {index + 1}" if shared_bathrooms > 1 else "Bathroom",
            }
            for index in range(shared_bathrooms)
        ]
    )

    public_row_width = len(public_definitions) * room_width
    private_row_width = len(private_definitions) * room_width
    house_width = max(public_row_width, private_row_width, room_width)

    public_center_z = -(hallway_depth / 2.0 + room_depth / 2.0)
    private_center_z = hallway_depth / 2.0 + room_depth / 2.0
    ensuite_center_z = private_center_z + room_depth / 2.0 + ensuite_depth / 2.0

    public_positions = build_centered_positions(len(public_definitions), room_width)
    private_positions = build_centered_positions(len(private_definitions), room_width)

    public_rooms = [
        create_rect_space(
            definition["id"],
            definition["type"],
            definition["label"],
            public_positions[index],
            public_center_z,
            room_width,
            room_depth,
            "public",
        )
        for index, definition in enumerate(public_definitions)
    ]
    for room in public_rooms:
        room["assignable"] = True

    private_rooms = [
        create_rect_space(
            definition["id"],
            definition["type"],
            definition["label"],
            private_positions[index],
            private_center_z,
            room_width,
            room_depth,
            "private",
        )
        for index, definition in enumerate(private_definitions)
    ]
    for room in private_rooms:
        room["assignable"] = True

    bedroom_rooms = [room for room in private_rooms if room["type"] == "bedroom"]
    ensuite_rooms = []
    for index, bedroom in enumerate(bedroom_rooms[: normalized["ensuite_bathrooms"]]):
        bedroom["has_ensuite"] = True
        ensuite_room = create_rect_space(
            f"bathroom_ensuite_{index + 1}",
            "bathroom",
            f"Ensuite {index + 1}",
            bedroom["center"][0],
            ensuite_center_z,
            room_width,
            ensuite_depth,
            "ensuite",
            bedroom["id"],
        )
        ensuite_room["assignable"] = True
        ensuite_rooms.append(ensuite_room)

    corridor = create_rect_space(
        "hallway_main",
        "hallway",
        "Hallway",
        0.0,
        0.0,
        house_width,
        hallway_depth,
        "corridor",
    )
    corridor["assignable"] = False

    all_spaces = public_rooms + private_rooms + ensuite_rooms + [corridor]
    min_x = min(space["rect"]["min_x"] for space in all_spaces) - wall_thickness
    max_x = max(space["rect"]["max_x"] for space in all_spaces) + wall_thickness
    min_z = min(space["rect"]["min_z"] for space in all_spaces) - wall_thickness
    max_z = max(space["rect"]["max_z"] for space in all_spaces) + wall_thickness

    return {
        "mode": "house",
        "house_config": normalized,
        "rooms": public_rooms + private_rooms + ensuite_rooms,
        "floors": public_rooms + private_rooms + ensuite_rooms + [corridor],
        "corridor": corridor,
        "walls": build_house_walls(public_rooms, private_rooms, ensuite_rooms),
        "bounds": {
            "min_x": min_x,
            "max_x": max_x,
            "min_z": min_z,
            "max_z": max_z,
            "width": max_x - min_x,
            "depth": max_z - min_z,
            "center_x": (min_x + max_x) / 2.0,
            "center_z": (min_z + max_z) / 2.0,
        },
        "dimensions": {
            "room_height": ROOM_DIMENSIONS["room_height"],
            "wall_thickness": wall_thickness,
        },
    }


def build_city_plan(house_config=None):
    normalized = normalize_house_config(house_config)
    base_plan = build_house_plan(normalized)
    wall_thickness = ROOM_DIMENSIONS["wall_thickness"]

    lot_min_x = base_plan["bounds"]["min_x"] - normalized["setback_width"]
    lot_max_x = base_plan["bounds"]["max_x"] + normalized["setback_width"]
    lot_min_z = base_plan["bounds"]["min_z"] - normalized["setback_width"]
    lot_max_z = base_plan["bounds"]["max_z"] + normalized["setback_width"]

    sidewalk_min_x = lot_min_x - normalized["sidewalk_width"]
    sidewalk_max_x = lot_max_x + normalized["sidewalk_width"]
    sidewalk_min_z = lot_min_z - normalized["sidewalk_width"]
    sidewalk_max_z = lot_max_z + normalized["sidewalk_width"]

    road_width = normalized["road_lanes"] * CITY_LANE_WIDTH
    road_min_x = sidewalk_min_x - road_width
    road_max_x = sidewalk_max_x + road_width
    road_min_z = sidewalk_min_z - road_width
    road_max_z = sidewalk_max_z + road_width

    center_x = (road_min_x + road_max_x) / 2.0
    center_z = (road_min_z + road_max_z) / 2.0
    lot_width = lot_max_x - lot_min_x
    lot_depth = lot_max_z - lot_min_z

    outdoor_rooms = [
        create_rect_space(
            "city_outdoor_north",
            "outdoor",
            "Front Court",
            base_plan["bounds"]["center_x"],
            (lot_min_z + base_plan["bounds"]["min_z"]) / 2.0,
            base_plan["bounds"]["width"],
            normalized["setback_width"],
            "outdoor",
            material_key="lot",
        ),
        create_rect_space(
            "city_outdoor_south",
            "outdoor",
            "Back Court",
            base_plan["bounds"]["center_x"],
            (base_plan["bounds"]["max_z"] + lot_max_z) / 2.0,
            base_plan["bounds"]["width"],
            normalized["setback_width"],
            "outdoor",
            material_key="lot",
        ),
        create_rect_space(
            "city_outdoor_west",
            "outdoor",
            "West Court",
            (lot_min_x + base_plan["bounds"]["min_x"]) / 2.0,
            base_plan["bounds"]["center_z"],
            normalized["setback_width"],
            base_plan["bounds"]["depth"],
            "outdoor",
            material_key="lot",
        ),
        create_rect_space(
            "city_outdoor_east",
            "outdoor",
            "East Court",
            (base_plan["bounds"]["max_x"] + lot_max_x) / 2.0,
            base_plan["bounds"]["center_z"],
            normalized["setback_width"],
            base_plan["bounds"]["depth"],
            "outdoor",
            material_key="lot",
        ),
    ]
    for room in outdoor_rooms:
        room["assignable"] = True

    street_rooms = [
        create_rect_space(
            "city_street_north",
            "street",
            "North Street",
            center_x,
            (road_min_z + sidewalk_min_z) / 2.0,
            road_max_x - road_min_x,
            road_width,
            "street",
            material_key="road",
        ),
        create_rect_space(
            "city_street_south",
            "street",
            "South Street",
            center_x,
            (sidewalk_max_z + road_max_z) / 2.0,
            road_max_x - road_min_x,
            road_width,
            "street",
            material_key="road",
        ),
        create_rect_space(
            "city_street_west",
            "street",
            "West Street",
            (road_min_x + sidewalk_min_x) / 2.0,
            center_z,
            road_width,
            sidewalk_max_z - sidewalk_min_z,
            "street",
            material_key="road",
        ),
        create_rect_space(
            "city_street_east",
            "street",
            "East Street",
            (sidewalk_max_x + road_max_x) / 2.0,
            center_z,
            road_width,
            sidewalk_max_z - sidewalk_min_z,
            "street",
            material_key="road",
        ),
    ]
    for room in street_rooms:
        room["assignable"] = True

    floor_spaces = [
        *[
            {**space, "material_key": space.get("material_key", "floor")}
            for space in base_plan["floors"]
        ],
        create_rect_space(
            "city_lot",
            "lot",
            "Lot",
            (lot_min_x + lot_max_x) / 2.0,
            (lot_min_z + lot_max_z) / 2.0,
            lot_width,
            lot_depth,
            "lot",
            material_key="lot",
        ),
        create_rect_space(
            "city_sidewalk_north",
            "sidewalk",
            "North Sidewalk",
            center_x,
            (sidewalk_min_z + lot_min_z) / 2.0,
            sidewalk_max_x - sidewalk_min_x,
            normalized["sidewalk_width"],
            "sidewalk",
            material_key="sidewalk",
        ),
        create_rect_space(
            "city_sidewalk_south",
            "sidewalk",
            "South Sidewalk",
            center_x,
            (lot_max_z + sidewalk_max_z) / 2.0,
            sidewalk_max_x - sidewalk_min_x,
            normalized["sidewalk_width"],
            "sidewalk",
            material_key="sidewalk",
        ),
        create_rect_space(
            "city_sidewalk_west",
            "sidewalk",
            "West Sidewalk",
            (sidewalk_min_x + lot_min_x) / 2.0,
            center_z,
            normalized["sidewalk_width"],
            lot_depth,
            "sidewalk",
            material_key="sidewalk",
        ),
        create_rect_space(
            "city_sidewalk_east",
            "sidewalk",
            "East Sidewalk",
            (lot_max_x + sidewalk_max_x) / 2.0,
            center_z,
            normalized["sidewalk_width"],
            lot_depth,
            "sidewalk",
            material_key="sidewalk",
        ),
        *street_rooms,
    ]

    if normalized["add_crosswalks"]:
        floor_spaces.extend(
            [
                create_rect_space(
                    "city_crosswalk_north",
                    "crosswalk",
                    "North Crosswalk",
                    center_x,
                    (road_min_z + sidewalk_min_z) / 2.0,
                    max(3.0, min(base_plan["bounds"]["width"] * 0.72, sidewalk_max_x - sidewalk_min_x - 0.4)),
                    max(1.2, road_width * 0.72),
                    "crosswalk",
                    material_key="crosswalk",
                ),
                create_rect_space(
                    "city_crosswalk_south",
                    "crosswalk",
                    "South Crosswalk",
                    center_x,
                    (sidewalk_max_z + road_max_z) / 2.0,
                    max(3.0, min(base_plan["bounds"]["width"] * 0.72, sidewalk_max_x - sidewalk_min_x - 0.4)),
                    max(1.2, road_width * 0.72),
                    "crosswalk",
                    material_key="crosswalk",
                ),
                create_rect_space(
                    "city_crosswalk_west",
                    "crosswalk",
                    "West Crosswalk",
                    (road_min_x + sidewalk_min_x) / 2.0,
                    center_z,
                    max(1.2, road_width * 0.72),
                    max(3.0, min(base_plan["bounds"]["depth"] * 0.72, sidewalk_max_z - sidewalk_min_z - 0.4)),
                    "crosswalk",
                    material_key="crosswalk",
                ),
                create_rect_space(
                    "city_crosswalk_east",
                    "crosswalk",
                    "East Crosswalk",
                    (sidewalk_max_x + road_max_x) / 2.0,
                    center_z,
                    max(1.2, road_width * 0.72),
                    max(3.0, min(base_plan["bounds"]["depth"] * 0.72, sidewalk_max_z - sidewalk_min_z - 0.4)),
                    "crosswalk",
                    material_key="crosswalk",
                ),
            ]
        )

    return {
        **base_plan,
        "mode": "city",
        "house_config": normalized,
        "rooms": [*base_plan["rooms"], *outdoor_rooms, *street_rooms],
        "floors": floor_spaces,
        "bounds": {
            "min_x": road_min_x - wall_thickness,
            "max_x": road_max_x + wall_thickness,
            "min_z": road_min_z - wall_thickness,
            "max_z": road_max_z + wall_thickness,
            "width": road_max_x - road_min_x + wall_thickness * 2.0,
            "depth": road_max_z - road_min_z + wall_thickness * 2.0,
            "center_x": center_x,
            "center_z": center_z,
        },
    }


def build_single_room_plan(layout_mode="living"):
    room_type = layout_mode if layout_mode in SINGLE_ROOM_LAYOUTS else "living"
    size = ROOM_DIMENSIONS["single_room_size"]
    room = create_rect_space(
        f"{room_type}_single",
        room_type,
        "Room",
        0.0,
        0.0,
        size,
        size,
        "single",
    )
    room["assignable"] = True
    wall_thickness = ROOM_DIMENSIONS["wall_thickness"]
    return {
        "mode": room_type,
        "house_config": normalize_house_config(DEFAULT_HOUSE_CONFIG),
        "rooms": [room],
        "floors": [room],
        "corridor": None,
        "walls": build_single_room_walls(room),
        "bounds": {
            "min_x": room["rect"]["min_x"] - wall_thickness,
            "max_x": room["rect"]["max_x"] + wall_thickness,
            "min_z": room["rect"]["min_z"] - wall_thickness,
            "max_z": room["rect"]["max_z"],
            "width": size + wall_thickness * 2.0,
            "depth": size + wall_thickness,
            "center_x": 0.0,
            "center_z": 0.0,
        },
        "dimensions": {
            "room_height": ROOM_DIMENSIONS["room_height"],
            "wall_thickness": wall_thickness,
        },
    }


def build_layout_plan(layout_mode, house_config=None):
    if layout_mode == "city":
        return build_city_plan(house_config)
    if layout_mode == "house":
        return build_house_plan(house_config)
    return build_single_room_plan(layout_mode)


def get_room_type_candidates(asset, house_config):
    asset_type = asset.get("asset_type")
    prompt_type = infer_prompt_room_type(asset.get("prompt"))

    if asset_type in OUTDOOR_TARGETS_BY_TYPE:
        return OUTDOOR_TARGETS_BY_TYPE[asset_type]

    if asset_type == "sink":
        return ("bathroom", "kitchen") if prompt_type == "bathroom" else ("kitchen", "bathroom")

    if asset_type == "cabinet":
        if prompt_type == "bathroom":
            return ("bathroom", "kitchen", "dining")
        if prompt_type == "kitchen":
            return ("kitchen", "bathroom", "dining")
        return ("kitchen", "bathroom", "dining")

    if asset_type == "mirror":
        if prompt_type == "bathroom":
            return ("bathroom", "bedroom", "living")
        return ("bedroom", "bathroom", "living")

    if asset_type in ("painting", "picture_frame"):
        return ("living", "bedroom", "dining" if house_config["dining_rooms"] > 0 else "kitchen")

    if asset_type == "clock":
        return ("living", "dining" if house_config["dining_rooms"] > 0 else "kitchen", "bedroom", "bathroom")

    if asset_type == "rug":
        return ("living", "bedroom", "dining" if house_config["dining_rooms"] > 0 else "kitchen")

    if asset_type == "lamp":
        return ("living", "bedroom", "dining" if house_config["dining_rooms"] > 0 else "kitchen")

    if asset_type in ("vase", "plant_pot"):
        return ("living", "dining" if house_config["dining_rooms"] > 0 else "kitchen", "bedroom")

    if asset_type in ("shelf", "bookcase"):
        return ("living", "bedroom", "kitchen")

    if asset_type in ROOM_TARGETS_BY_TYPE:
        return ROOM_TARGETS_BY_TYPE[asset_type]

    if prompt_type in SINGLE_ROOM_LAYOUTS:
        return (prompt_type,)

    return ("living",)


def choose_room_for_asset(asset, plan, house_config, room_loads):
    rooms_by_type = {}
    for room in plan["rooms"]:
        if not room.get("assignable"):
            continue
        rooms_by_type.setdefault(room["type"], []).append(room)

    candidate_rooms = []
    for room_type in get_room_type_candidates(asset, house_config):
        candidate_rooms.extend(rooms_by_type.get(room_type, []))

    if not candidate_rooms:
        fallback_rooms = sorted(
            [room for room in plan["rooms"] if room.get("assignable")],
            key=lambda room: (ROOM_TYPE_PRIORITY.get(room["type"], 99), room["id"]),
        )
        return fallback_rooms[0] if fallback_rooms else None

    return sorted(
        candidate_rooms,
        key=lambda room: (
            room_loads.get(room["id"], 0),
            ROOM_TYPE_PRIORITY.get(room["type"], 99),
            room["id"],
        ),
    )[0]


def build_layout_placements(asset_list, layout_mode, house_config=None):
    plan = build_layout_plan(layout_mode, house_config)
    placements = {}

    if plan["mode"] not in {"house", "city"}:
        room = plan["rooms"][0]
        type_counts = {}
        for asset in asset_list:
            type_index = type_counts.get(asset["asset_type"], 0)
            type_counts[asset["asset_type"]] = type_index + 1
            local_placement = scale_placement_to_room(
                get_single_room_placement(asset["asset_type"], type_index),
                room,
            )
            placements[asset["asset_id"]] = {
                "room_id": room["id"],
                "room_type": room["type"],
                "pos": (
                    local_placement["pos"][0] + room["center"][0],
                    local_placement["pos"][1],
                    local_placement["pos"][2] + room["center"][2],
                ),
                "rot_y": local_placement["rot_y"],
                "scale": local_placement["scale"],
            }
        return placements

    normalized = normalize_house_config(house_config)
    room_loads = {}
    room_type_counts = {}

    for asset in asset_list:
        room = choose_room_for_asset(asset, plan, normalized, room_loads)
        if not room:
            continue

        room_loads[room["id"]] = room_loads.get(room["id"], 0) + 1
        room_type_key = f"{room['id']}:{asset['asset_type']}"
        local_index = room_type_counts.get(room_type_key, 0)
        room_type_counts[room_type_key] = local_index + 1

        local_placement = scale_placement_to_room(
            get_single_room_placement(asset["asset_type"], local_index),
            room,
        )

        placements[asset["asset_id"]] = {
            "room_id": room["id"],
            "room_type": room["type"],
            "pos": (
                local_placement["pos"][0] + room["center"][0],
                local_placement["pos"][1],
                local_placement["pos"][2] + room["center"][2],
            ),
            "rot_y": local_placement["rot_y"],
            "scale": local_placement["scale"],
        }

    return placements
