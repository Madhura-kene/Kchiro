import os
import sys
import json
import argparse
import math

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

def generate_closet(params):
    w = params.get("width", 150.0) / 100.0  # convert cm to meters
    d = params.get("depth", 65.0) / 100.0
    h = params.get("height", 200.0) / 100.0
    door_style = params.get("door_style", "hinged")
    doors_count = params.get("doors", 2)
    material_name = params.get("material", "wood")

    parts = []

    # 1. Setup Materials
    if material_name == "dark_oak":
        main_color = (0.12, 0.08, 0.05, 1.0)
        rough = 0.85
    elif material_name == "white_laminate":
        main_color = (0.92, 0.92, 0.92, 1.0)
        rough = 0.4
    else: # default wood
        main_color = (0.35, 0.22, 0.12, 1.0)
        rough = 0.75

    main_mat = utils.create_material("ClosetMain", diffuse_color=main_color, metallic=0.0, roughness=rough)
    handle_mat = utils.create_material("ClosetHandle", diffuse_color=(0.85, 0.85, 0.9, 1.0), metallic=0.9, roughness=0.1) # Chrome
    rod_mat = utils.create_material("ClosetRod", diffuse_color=(0.8, 0.8, 0.8, 1.0), metallic=0.95, roughness=0.15)

    carcass_thick = 0.04
    base_h = 0.08

    # 2. Main Carcass Box
    carcass_z = h / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, carcass_z))
    carcass = bpy.context.active_object
    carcass.name = "ClosetCarcass"
    carcass.scale = (w, d, h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(carcass, width=0.008)
    utils.apply_material(carcass, main_mat)
    parts.append(carcass)

    # 3. Base Kicker Trim
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.01, base_h / 2.0))
    kicker = bpy.context.active_object
    kicker.name = "ClosetBase"
    kicker.scale = (w - 0.02, d - 0.02, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(kicker, width=0.003)
    utils.apply_material(kicker, main_mat)
    parts.append(kicker)

    # 4. Interior details
    if door_style == "walk_in":
        # Create an open walk-in layout with divider and shelves
        # Vertical divider
        div_w = 0.03
        div_z = base_h + (h - base_h - carcass_thick) / 2.0
        div_h = h - base_h - carcass_thick * 2.0
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, div_z))
        divider = bpy.context.active_object
        divider.name = "ClosetDivider"
        divider.scale = (div_w, d - carcass_thick * 2.0, div_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(divider, main_mat)
        parts.append(divider)

        # Left side shelves (stack of 5 shelves for shoes/clothes)
        shelf_thick = 0.02
        shelf_w = (w - div_w - carcass_thick * 2.0) / 2.0
        left_shelf_x = -w / 4.0
        
        for s_idx in range(5):
            sz = base_h + (div_h) * (s_idx + 1) / 6.0
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(left_shelf_x, 0.0, sz))
            shelf = bpy.context.active_object
            shelf.name = f"ClosetLeftShelf_{s_idx}"
            shelf.scale = (shelf_w, d - carcass_thick * 2.0, shelf_thick)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(shelf, width=0.003)
            utils.apply_material(shelf, main_mat)
            parts.append(shelf)

        # Right side double hanging rods
        right_rod_x = w / 4.0
        for r_idx, rod_z in enumerate([base_h + div_h * 0.45, base_h + div_h * 0.85]):
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.015,
                depth=shelf_w,
                location=(right_rod_x, 0.0, rod_z)
            )
            rod = bpy.context.active_object
            rod.name = f"ClosetHangingRod_{r_idx}"
            rod.rotation_euler = (0, math.pi / 2.0, 0)
            bpy.ops.object.transform_apply(rotation=True)
            utils.apply_smooth_by_angle(rod, angle=40.0)
            utils.apply_material(rod, rod_mat)
            parts.append(rod)

    elif door_style == "sliding":
        # Two overlapping sliding doors
        door_w = w / 2.0 + 0.015
        door_h = h - base_h - 0.02
        door_thick = 0.025
        door_z = base_h + door_h / 2.0

        # Left sliding door (outer pane)
        left_x = -w / 4.0 + 0.005
        left_y = -d / 2.0 - door_thick / 2.0
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(left_x, left_y, door_z))
        door_l = bpy.context.active_object
        door_l.name = "ClosetDoorSliding_L"
        door_l.scale = (door_w, door_thick, door_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(door_l, width=0.004)
        utils.apply_material(door_l, main_mat)
        parts.append(door_l)

        # Right sliding door (inner pane, recessed)
        right_x = w / 4.0 - 0.005
        right_y = -d / 2.0 + door_thick / 2.0
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(right_x, right_y, door_z))
        door_r = bpy.context.active_object
        door_r.name = "ClosetDoorSliding_R"
        door_r.scale = (door_w, door_thick, door_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(door_r, width=0.004)
        utils.apply_material(door_r, main_mat)
        parts.append(door_r)

        # Recessed handle slots
        for side, dx, dy in [(-1.0, left_x + door_w / 2.0 - 0.05, left_y - 0.002), (1.0, right_x - door_w / 2.0 + 0.05, right_y - 0.002)]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, dy, door_z))
            hnd = bpy.context.active_object
            hnd.name = f"SlidingHandle_{'L' if side < 0 else 'R'}"
            hnd.scale = (0.02, 0.004, 0.2)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(hnd, handle_mat)
            parts.append(hnd)

    else:  # hinged doors
        door_w = w / doors_count - 0.005
        door_h = h - base_h - 0.02
        door_thick = 0.02
        door_z = base_h + door_h / 2.0
        door_y = -d / 2.0 - door_thick / 2.0

        for idx in range(doors_count):
            # Calculate position along X
            door_x = -w / 2.0 + (idx + 0.5) * (w / doors_count)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y, door_z))
            door = bpy.context.active_object
            door.name = f"ClosetHingedDoor_{idx}"
            door.scale = (door_w, door_thick, door_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(door, width=0.004)
            utils.apply_material(door, main_mat)
            parts.append(door)

            # Modern long metal bar handles
            # Placed near the meeting edges
            is_right_handle = (idx % 2 == 0)
            handle_offset = door_w / 2.0 - 0.05
            handle_x = door_x + (handle_offset if is_right_handle else -handle_offset)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(handle_x, door_y - 0.015, door_z))
            hnd = bpy.context.active_object
            hnd.name = f"HingedHandle_{idx}"
            hnd.scale = (0.015, 0.015, 0.4)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(hnd, width=0.002)
            utils.apply_material(hnd, handle_mat)
            parts.append(hnd)

    # Join parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = carcass
    bpy.ops.object.join()
    
    carcass.name = "ClosetAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return carcass

def main():
    parser = argparse.ArgumentParser(description="Procedural Closet Generator")
    parser.add_argument("--params", type=str, required=True, help="Path to JSON parameter file")
    parser.add_argument("--export", type=str, required=True, help="Path to export GLB")
    parser.add_argument("--render", type=str, help="Path to render preview PNG")
    
    try:
        args_idx = sys.argv.index("--")
        script_args = sys.argv[args_idx + 1:]
    except ValueError:
        script_args = []
        
    args = parser.parse_args(script_args)
    
    with open(args.params, 'r') as f:
        params = json.load(f)
        
    utils.cleanup_scene()
    closet_obj = generate_closet(params)
    
    if args.render:
        utils.setup_lighting_and_camera(closet_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
