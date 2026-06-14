import json
import math
import os
import sys

import bpy
import mathutils


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from blender import utils
from backend.room_layout import (
    DEFAULT_WALL_COLORS,
    build_layout_plan,
    build_layout_placements,
    normalize_wall_colors,
)


DETAIL_ROLE_DEFINITIONS = [
    ("pillows_sheets", ["pillow", "sheet", "sheets"]),
    ("blankets", ["blanket", "duvet", "comforter", "quilt"]),
    ("cushions", ["cushion", "upholstery"]),
    ("frame", ["frame", "wood", "oak", "board", "carcass", "shelf", "door"]),
    ("metal", ["metal", "steel", "iron", "chrome", "brass", "handle", "hoop"]),
    ("glass_mirror", ["glass", "mirror"]),
    ("accent", ["canvas", "shade", "dial", "face", "trim"]),
]

PRIMARY_EXCLUSION_KEYWORDS = [
    "glass",
    "soil",
    "stem",
    "leaf",
    "plant",
    "water",
    "flame",
    "ticks",
    "mirror",
    "fringe",
    "glow",
    "hands",
    "pin",
]


def parse_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1 :]
    else:
        argv = []

    manifest_path = None
    output_path = None
    for index, arg in enumerate(argv):
        if arg == "--manifest" and index + 1 < len(argv):
            manifest_path = argv[index + 1]
        if arg == "--output" and index + 1 < len(argv):
            output_path = argv[index + 1]

    if not manifest_path or not output_path:
        raise ValueError("Missing --manifest or --output argument.")

    return os.path.abspath(manifest_path), os.path.abspath(output_path)


def hex_to_rgba(hex_value, alpha=1.0):
    if not isinstance(hex_value, str) or not hex_value.startswith("#") or len(hex_value) != 7:
        return None
    return (
        int(hex_value[1:3], 16) / 255.0,
        int(hex_value[3:5], 16) / 255.0,
        int(hex_value[5:7], 16) / 255.0,
        alpha,
    )


def create_room_material(name, color_rgba, metallic=0.0, roughness=0.6, alpha=1.0):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color_rgba
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Alpha"].default_value = alpha
    if alpha < 1.0:
        material.blend_method = "BLEND"
        material.shadow_method = "HASHED"
    return material


def create_shell_materials(wall_colors):
    materials = {
        "floor": create_room_material("RoomFloor", (0.06, 0.075, 0.12, 1.0), metallic=0.2, roughness=0.5),
        "lot": create_room_material("RoomLot", (0.08, 0.1, 0.14, 1.0), metallic=0.08, roughness=0.66),
        "sidewalk": create_room_material("RoomSidewalk", (0.49, 0.54, 0.6, 1.0), metallic=0.06, roughness=0.72),
        "road": create_room_material("RoomRoad", (0.14, 0.16, 0.2, 1.0), metallic=0.1, roughness=0.62),
        "crosswalk": create_room_material("RoomCrosswalk", (0.88, 0.91, 0.95, 1.0), metallic=0.04, roughness=0.42),
    }
    for key, fallback_color in DEFAULT_WALL_COLORS.items():
        wall_rgba = hex_to_rgba(wall_colors.get(key, fallback_color), alpha=0.72) or (0.2, 0.25, 0.33, 0.72)
        materials[key] = create_room_material(
            f"RoomWall_{key.title()}",
            wall_rgba,
            metallic=0.1,
            roughness=0.7,
            alpha=0.72,
        )
    return materials


def add_box_panel(location, size, material, name):
    bpy.ops.mesh.primitive_cube_add(location=location)
    panel = bpy.context.active_object
    panel.name = name
    panel.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    utils.apply_material(panel, material)


def create_layout_shell(layout_plan, wall_colors):
    materials = create_shell_materials(wall_colors)
    wall_thickness = layout_plan["dimensions"]["wall_thickness"]

    for floor_space in layout_plan["floors"]:
        add_box_panel(
            location=(floor_space["center"][0], floor_space["center"][2], -wall_thickness / 2.0),
            size=(floor_space["width"], floor_space["depth"], wall_thickness),
            material=materials.get(floor_space.get("material_key", "floor"), materials["floor"]),
            name=f"{floor_space['id']}_floor",
        )

    for wall_segment in layout_plan["walls"]:
        add_box_panel(
            location=(wall_segment["position"][0], wall_segment["position"][2], wall_segment["position"][1]),
            size=(wall_segment["size"][0], wall_segment["size"][2], wall_segment["size"][1]),
            material=materials.get(wall_segment["material_key"], materials["interior"]),
            name=wall_segment["id"],
        )


def find_detail_role(material_name):
    lower_name = (material_name or "").lower()
    for role_key, keywords in DETAIL_ROLE_DEFINITIONS:
        if any(keyword in lower_name for keyword in keywords):
            return role_key
    return None


def is_primary_material(material_name):
    lower_name = (material_name or "").lower()
    return not any(keyword in lower_name for keyword in PRIMARY_EXCLUSION_KEYWORDS)


def apply_material_color(material, color_hex):
    rgba = hex_to_rgba(color_hex)
    if not rgba:
        return
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba


def duplicate_materials(imported_objects, prefix):
    for obj in imported_objects:
        if obj.type != "MESH":
            continue
        for slot in obj.material_slots:
            if slot.material:
                slot.material = slot.material.copy()
                slot.material.name = f"{prefix}_{slot.material.name}"


def apply_color_overrides(imported_objects, custom_color, detail_colors):
    for obj in imported_objects:
        if obj.type != "MESH":
            continue
        for slot in obj.material_slots:
            material = slot.material
            if not material:
                continue

            material_name = material.name or ""
            if custom_color and is_primary_material(material_name):
                apply_material_color(material, custom_color)

            role_key = find_detail_role(material_name)
            if role_key and detail_colors.get(role_key):
                apply_material_color(material, detail_colors[role_key])


def compute_bounds(objects):
    min_corner = mathutils.Vector((float("inf"), float("inf"), float("inf")))
    max_corner = mathutils.Vector((float("-inf"), float("-inf"), float("-inf")))
    found_bounds = False

    for obj in objects:
        if obj.type != "MESH":
            continue
        for corner in obj.bound_box:
            world_corner = obj.matrix_world @ mathutils.Vector(corner)
            min_corner.x = min(min_corner.x, world_corner.x)
            min_corner.y = min(min_corner.y, world_corner.y)
            min_corner.z = min(min_corner.z, world_corner.z)
            max_corner.x = max(max_corner.x, world_corner.x)
            max_corner.y = max(max_corner.y, world_corner.y)
            max_corner.z = max(max_corner.z, world_corner.z)
            found_bounds = True

    if not found_bounds:
        return None, None

    return min_corner, max_corner


def import_asset(filepath):
    before_ids = {obj.as_pointer() for obj in bpy.data.objects}
    bpy.ops.import_scene.gltf(filepath=filepath)
    return [obj for obj in bpy.data.objects if obj.as_pointer() not in before_ids]


def normalize_asset(imported_objects):
    min_corner, max_corner = compute_bounds(imported_objects)
    if not min_corner or not max_corner:
        return 1.0

    center_x = (min_corner.x + max_corner.x) / 2.0
    center_y = (min_corner.y + max_corner.y) / 2.0
    min_z = min_corner.z
    size = max_corner - min_corner
    max_dim = max(size.x, size.y, size.z)
    normalize_scale = 1.0 / max_dim if max_dim > 0.001 else 1.0

    root_objects = [obj for obj in imported_objects if obj.parent is None]
    for obj in root_objects:
        obj.location.x -= center_x
        obj.location.y -= center_y
        obj.location.z -= min_z

    return normalize_scale


def parent_to_anchor(imported_objects, anchor_name):
    anchor = bpy.data.objects.new(anchor_name, None)
    bpy.context.collection.objects.link(anchor)
    for obj in imported_objects:
        if obj.parent is None:
            obj.parent = anchor
            obj.matrix_parent_inverse = anchor.matrix_world.inverted()
    return anchor


def build_room_scene(manifest):
    utils.cleanup_scene()
    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.device = "CPU"
    bpy.context.scene.unit_settings.system = "METRIC"
    layout_mode = manifest.get("layout_mode", "living")
    house_config = manifest.get("house_config") or {}
    wall_colors = normalize_wall_colors(manifest.get("wall_colors") or {})
    layout_plan = build_layout_plan(layout_mode, house_config)

    create_layout_shell(
        layout_plan=layout_plan,
        wall_colors=wall_colors,
    )
    placements = build_layout_placements(manifest.get("assets", []), layout_mode, house_config)

    for asset in manifest.get("assets", []):
        glb_file = asset["glb_file"]
        if not os.path.exists(glb_file):
            print(f"Skipping missing asset file: {glb_file}")
            continue

        imported_objects = import_asset(glb_file)
        if not imported_objects:
            print(f"No objects imported from: {glb_file}")
            continue

        duplicate_materials(imported_objects, f"RoomAsset{asset['asset_id']}")
        apply_color_overrides(
            imported_objects,
            asset.get("custom_color"),
            asset.get("detail_colors") or {},
        )

        normalize_scale = normalize_asset(imported_objects)
        anchor = parent_to_anchor(imported_objects, f"RoomAsset_{asset['asset_id']}")

        placement = placements.get(asset["asset_id"])
        if not placement:
            continue

        base_pos = placement["pos"]
        base_rot_y = placement["rot_y"]
        base_scale = placement["scale"]
        anchor.location = (
            base_pos[0] + asset.get("pos_x", 0.0),
            base_pos[2] + asset.get("pos_z", 0.0),
            base_pos[1] + asset.get("pos_y", 0.0),
        )
        anchor.rotation_euler = (0.0, 0.0, base_rot_y + math.radians(asset.get("rot_y", 0.0)))

        scale_factor = asset.get("scale", 1.0)
        final_scale = base_scale * normalize_scale * scale_factor
        anchor.scale = (final_scale, final_scale, final_scale)

    target_location = (
        layout_plan["bounds"]["center_x"],
        layout_plan["bounds"]["center_z"],
        1.0,
    )
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=target_location)
    room_target = bpy.context.active_object
    room_target.name = "LayoutCenterTarget"
    utils.setup_lighting_and_camera(target_obj=room_target)


def save_output_file(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    extension = os.path.splitext(output_path)[1].lower()

    if extension == ".blend":
        bpy.ops.wm.save_as_mainfile(filepath=output_path)
        print(f"Saved Blender room file to: {output_path}")
        return

    if extension == ".stl":
        utils.export_stl(output_path)
        print(f"Saved STL room file to: {output_path}")
        return

    raise ValueError(f"Unsupported room export format: {extension}")


def main():
    manifest_path, output_path = parse_args()
    with open(manifest_path, "r", encoding="utf-8") as manifest_file:
        manifest = json.load(manifest_file)

    build_room_scene(manifest)
    save_output_file(output_path)


if __name__ == "__main__":
    main()
