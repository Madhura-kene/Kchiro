import os
import sys
import json
import argparse

# Dynamic import setup for Blender environment
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    import bpy
    import blender.utils as utils
except ImportError:
    print("Failed to import Blender API (bpy) or utilities.")
    sys.exit(1)

def generate_cupboard(params):
    w = params.get("width", 100.0) / 100.0  # cm to meters
    d = params.get("depth", 45.0) / 100.0
    h = params.get("height", 180.0) / 100.0
    style = params.get("style", "hutch")
    has_drawers = params.get("has_drawers", True)
    shelves_count = params.get("shelves", 3)

    parts = []

    # 1. Setup Materials
    # Warm rustic cherry/oak finish
    wood_color = (0.55, 0.35, 0.2, 1.0)
    knob_color = (0.75, 0.55, 0.15, 1.0) # brass
    
    wood_mat = utils.create_material("CupboardWood", diffuse_color=wood_color, metallic=0.0, roughness=0.6)
    knob_mat = utils.create_material("CupboardKnob", diffuse_color=knob_color, metallic=0.9, roughness=0.15)
    backing_mat = utils.create_material("CupboardBacking", diffuse_color=(0.4, 0.25, 0.15, 1.0), metallic=0.0, roughness=0.8)

    carcass_thick = 0.03
    base_h = h * 0.45  # Base section is 45% of height

    # ── BASE SECTION ────────────────────────────────────────────────────────
    # 2. Base Carcass
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, base_h / 2.0))
    base_box = bpy.context.active_object
    base_box.name = "BaseCarcass"
    base_box.scale = (w, d, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(base_box, width=0.005)
    utils.apply_material(base_box, wood_mat)
    parts.append(base_box)

    # 3. Base Kicker
    kicker_h = 0.08
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.01, kicker_h / 2.0))
    kicker = bpy.context.active_object
    kicker.name = "BaseKicker"
    kicker.scale = (w - 0.02, d - 0.02, kicker_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(kicker, wood_mat)
    parts.append(kicker)

    # 4. Drawers or Doors in Base
    # If has_drawers, model drawer fronts, otherwise doors
    if has_drawers:
        # 3 Stacked Drawers
        drawer_rows = 3
        drawer_h = (base_h - kicker_h - 0.04) / drawer_rows
        drawer_w = w - 0.04
        drawer_thick = 0.02
        drawer_y = -d / 2.0 - drawer_thick / 2.0

        for r in range(drawer_rows):
            drawer_z = kicker_h + 0.02 + r * drawer_h + drawer_h / 2.0
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, drawer_y, drawer_z))
            front = bpy.context.active_object
            front.name = f"DrawerFront_{r}"
            front.scale = (drawer_w, drawer_thick, drawer_h - 0.005)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(front, width=0.003)
            utils.apply_material(front, wood_mat)
            parts.append(front)

            # Center knob handles
            for knob_x in [-0.15, 0.15] if w > 1.2 else [0.0]:
                bpy.ops.mesh.primitive_ico_sphere_add(
                    radius=0.012,
                    subdivisions=2,
                    location=(knob_x, drawer_y - 0.012, drawer_z)
                )
                knob = bpy.context.active_object
                knob.name = f"DrawerKnob_{r}"
                utils.apply_smooth_by_angle(knob)
                utils.apply_material(knob, knob_mat)
                parts.append(knob)
    else:
        # Two solid doors
        door_w = w / 2.0 - 0.015
        door_h = base_h - kicker_h - 0.03
        door_thick = 0.02
        door_z = kicker_h + door_h / 2.0 + 0.01
        door_y = -d / 2.0 - door_thick / 2.0

        for side in [-1.0, 1.0]:
            door_x = side * (door_w / 2.0 + 0.003)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y, door_z))
            door = bpy.context.active_object
            door.name = f"BaseDoor_{'L' if side < 0 else 'R'}"
            door.scale = (door_w, door_thick, door_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(door, width=0.004)
            utils.apply_material(door, wood_mat)
            parts.append(door)

            # Knobs
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=0.012,
                subdivisions=2,
                location=(door_x + side * (door_w / 2.0 - 0.04), door_y - 0.012, door_z)
            )
            knob = bpy.context.active_object
            knob.name = f"BaseDoorKnob_{'L' if side < 0 else 'R'}"
            utils.apply_smooth_by_angle(knob)
            utils.apply_material(knob, knob_mat)
            parts.append(knob)

    # ── UPPER SECTION (HUTCH OR TALL UNIT) ──────────────────────────────────
    # For hutch style, it is recessed in depth.
    upper_d = d - 0.10 if style == "hutch" else d - 0.02
    upper_w = w - 0.02
    upper_h = h - base_h
    upper_z_center = base_h + upper_h / 2.0
    # Center shifts back slightly if depth is recessed
    upper_y = (d - upper_d) / 2.0 if style == "hutch" else 0.0

    # Upper back panel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, upper_y + upper_d/2.0 - carcass_thick/2.0, upper_z_center))
    back = bpy.context.active_object
    back.name = "UpperBack"
    back.scale = (upper_w, carcass_thick, upper_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(back, backing_mat)
    parts.append(back)

    # Upper Side panels
    for side in [-1.0, 1.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * (upper_w/2.0 - carcass_thick/2.0), upper_y, upper_z_center))
        side_panel = bpy.context.active_object
        side_panel.name = f"UpperSide_{'L' if side < 0 else 'R'}"
        side_panel.scale = (carcass_thick, upper_d, upper_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(side_panel, width=0.003)
        utils.apply_material(side_panel, wood_mat)
        parts.append(side_panel)

    # Upper Top board
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, upper_y, h - carcass_thick/2.0))
    top_board = bpy.context.active_object
    top_board.name = "UpperTop"
    top_board.scale = (upper_w, upper_d, carcass_thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(top_board, width=0.003)
    utils.apply_material(top_board, wood_mat)
    parts.append(top_board)

    # Shelves
    shelf_thick = 0.02
    shelf_w = upper_w - carcass_thick * 2.0
    shelf_d = upper_d - 0.02
    interior_h = upper_h - carcass_thick * 2.0
    for s in range(shelves_count):
        sz = base_h + carcass_thick + (s + 1) * (interior_h / (shelves_count + 1))
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, upper_y - 0.01, sz))
        shelf = bpy.context.active_object
        shelf.name = f"UpperShelf_{s}"
        shelf.scale = (shelf_w, shelf_d, shelf_thick)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(shelf, width=0.002)
        utils.apply_material(shelf, wood_mat)
        parts.append(shelf)

    # ── Join all parts ────────────────────────────────────────────────────────
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = base_box
    bpy.ops.object.join()
    base_box.name = "CupboardAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    return base_box

def main():
    parser = argparse.ArgumentParser(description="Procedural Cupboard Generator")
    parser.add_argument("--params", type=str, required=True)
    parser.add_argument("--export", type=str, required=True)
    parser.add_argument("--render", type=str)

    try:
        args_idx = sys.argv.index("--")
        script_args = sys.argv[args_idx + 1:]
    except ValueError:
        script_args = []

    args = parser.parse_args(script_args)

    with open(args.params, 'r') as f:
        params = json.load(f)

    utils.cleanup_scene()
    obj = generate_cupboard(params)

    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
