import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.room_layout import build_layout_plan, build_layout_placements


def test_city_layout_builds_road_shell_and_crosswalks():
    house_config = {
        "bedrooms": 3,
        "bathrooms": 2,
        "kitchens": 1,
        "livingRooms": 1,
        "diningRooms": 1,
        "roadLanes": 3,
        "sidewalkWidth": 2.2,
        "setbackWidth": 3.0,
        "addCrosswalks": True,
    }

    city_plan = build_layout_plan("city", house_config)
    house_plan = build_layout_plan("house", house_config)

    assert city_plan["mode"] == "city"
    assert city_plan["bounds"]["width"] > house_plan["bounds"]["width"]
    assert city_plan["bounds"]["depth"] > house_plan["bounds"]["depth"]
    assert any(space.get("material_key") == "road" for space in city_plan["floors"])
    assert any(space.get("material_key") == "sidewalk" for space in city_plan["floors"])
    assert any(space.get("material_key") == "crosswalk" for space in city_plan["floors"])
    assert any(room["type"] == "street" for room in city_plan["rooms"])
    assert any(room["type"] == "outdoor" for room in city_plan["rooms"])


def test_city_layout_routes_urban_assets_outdoors():
    placements = build_layout_placements(
        [
            {"asset_id": 1, "asset_type": "car", "prompt": "Modern red sedan car"},
            {"asset_id": 2, "asset_type": "street_lamp", "prompt": "Modern street lamp"},
            {"asset_id": 3, "asset_type": "bed", "prompt": "King size wooden bed"},
        ],
        "city",
        {
            "bedrooms": 2,
            "bathrooms": 2,
            "kitchens": 1,
            "livingRooms": 1,
            "diningRooms": 1,
            "roadLanes": 2,
            "sidewalkWidth": 1.8,
            "setbackWidth": 2.4,
            "addCrosswalks": True,
        },
    )

    assert placements[1]["room_type"] == "street"
    assert placements[2]["room_type"] == "outdoor"
    assert placements[3]["room_type"] == "bedroom"
