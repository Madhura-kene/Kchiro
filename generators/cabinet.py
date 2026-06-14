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

def generate_cabinet(params):
    w = params.get("width", 80.0) / 100.0  # convert cm to meters
    d = params.get("depth", 40.0) / 100.0
    h = params.get("height", 120.0) / 100.0
    has_glass = params.get("has_glass", False)
    shelves_count = params.get("shelves", 3)
    style = params.get("style", "display")

    parts = []

    # 1. Setup Materials
    if style == "kitchen":
        carcass_color = (0.9, 0.9, 0.9, 1.0) # White Laminate
        rough_carcass = 0.4
        handle_color = (0.8, 0.8, 0.8, 1.0) # Silver steel
        metallic_handle = 0.9
    elif style == "bathroom":
        carcass_color = (0.95, 0.95, 0.95, 1.0) # Glossy White Lacquer
        rough_carcass = 0.15
        handle_color = (0.85, 0.85, 0.87, 1.0) # Chrome
        metallic_handle = 0.95
    elif style == "credenza":
        carcass_color = (0.45, 0.3, 0.18, 1.0) # Mid wood tone
        rough_carcass = 0.7
        handle_color = (0.7, 0.55, 0.2, 1.0) # Brass
        metallic_handle = 0.9
    else: # display
        carcass_color = (0.2, 0.12, 0.08, 1.0) # Dark mahogany
        rough_carcass = 0.75
        handle_color = (0.75, 0.55, 0.2, 1.0) # Brass
        metallic_handle = 0.9

    carcass_mat = utils.create_material("CabinetCarcass", diffuse_color=carcass_color, metallic=0.0, roughness=rough_carcass)
    handle_mat = utils.create_material("CabinetHandle", diffuse_color=handle_color, metallic=metallic_handle, roughness=0.15)
    glass_mat = utils.create_material("CabinetGlass", diffuse_color=(0.85, 0.95, 0.95, 0.15), metallic=0.0, roughness=0.05)
    
    carcass_thick = 0.03
    base_h = 0.08

    # 2. Main Carcass Box
    carcass_z = h / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, carcass_z))
    carcass = bpy.context.active_object
    carcass.name = "CabinetCarcass"
    carcass.scale = (w, d, h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(carcass, width=0.005)
    utils.apply_material(carcass, carcass_mat)
    parts.append(carcass)

    # 3. Kicker Base Trim
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.01, base_h / 2.0))
    kicker = bpy.context.active_object
    kicker.name = "CabinetBase"
    kicker.scale = (w - 0.02, d - 0.02, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(kicker, width=0.003)
    utils.apply_material(kicker, carcass_mat)
    parts.append(kicker)

    # 4. Shelves Inside
    shelf_thick = 0.02
    if style == "bathroom":
        interior_start = base_h + (h - base_h) * 0.28 + 0.02
        interior_h = h - interior_start - carcass_thick
    else:
        interior_start = base_h + carcass_thick
        interior_h = h - base_h - carcass_thick * 2.0

    for s in range(shelves_count):
        # Evenly space shelves vertically within active interior space
        sz = interior_start + (s + 1) * (interior_h / (shelves_count + 1))
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, sz))
        shelf = bpy.context.active_object
        shelf.name = f"CabinetShelf_{s}"
        shelf.scale = (w - carcass_thick * 2.0, d - carcass_thick * 2.0 - 0.02, shelf_thick)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(shelf, width=0.002)
        utils.apply_material(shelf, carcass_mat)
        parts.append(shelf)

    if style == "bathroom":
        # Open towel rack partition shelf board under main doors
        partition_z = base_h + (h - base_h) * 0.28
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, partition_z))
        part_board = bpy.context.active_object
        part_board.name = "CabinetPartitionShelf"
        part_board.scale = (w - carcass_thick * 2.0, d - carcass_thick * 2.0 - 0.01, 0.02)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(part_board, width=0.002)
        utils.apply_material(part_board, carcass_mat)
        parts.append(part_board)

        # Integrated chrome towel bar hanging underneath the shelf partition
        bar_z = base_h + (h - base_h) * 0.14
        bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=w - carcass_thick * 2.0 - 0.02, location=(0.0, -d/2.0 + 0.04, bar_z))
        towel_bar = bpy.context.active_object
        towel_bar.name = "CabinetTowelBar"
        towel_bar.rotation_euler = (0, math.radians(90.0), 0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_smooth_by_angle(towel_bar)
        utils.apply_material(towel_bar, handle_mat)
        parts.append(towel_bar)

    # 5. Front Doors
    door_w = w / 2.0 - 0.004
    door_thick = 0.02
    door_y = -d / 2.0 - door_thick / 2.0

    if style == "bathroom":
        door_h = (h - base_h) * 0.72 - 0.01
        door_z = base_h + (h - base_h) * 0.28 + door_h / 2.0
    else:
        door_h = h - base_h - 0.02
        door_z = base_h + door_h / 2.0

    for side in [-1.0, 1.0]:
        door_x = side * (door_w / 2.0 + 0.001)

        if has_glass:
            # Frame
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y, door_z))
            door_frame = bpy.context.active_object
            door_frame.name = f"CabinetDoorFrame_{'L' if side < 0 else 'R'}"
            door_frame.scale = (door_w, door_thick, door_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(door_frame, width=0.003)
            utils.apply_material(door_frame, carcass_mat)
            parts.append(door_frame)

            # Glass
            glass_w = door_w - 0.08
            glass_h = door_h - 0.12
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y - 0.002, door_z))
            glass = bpy.context.active_object
            glass.name = f"CabinetGlassPane_{'L' if side < 0 else 'R'}"
            glass.scale = (glass_w, 0.006, glass_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(glass, glass_mat)
            parts.append(glass)
        else:
            # Solid wooden/lacquered door
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y, door_z))
            door = bpy.context.active_object
            door.name = f"CabinetDoorSolid_{'L' if side < 0 else 'R'}"
            door.scale = (door_w, door_thick, door_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(door, width=0.004)
            utils.apply_material(door, carcass_mat)
            parts.append(door)

            if style == "display":
                # Inset panel detail
                panel_h = door_h - 0.08
                panel_w = door_w - 0.06
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y - 0.004, door_z))
                panel = bpy.context.active_object
                panel.name = f"CabinetPanel_{'L' if side < 0 else 'R'}"
                panel.scale = (panel_w, 0.008, panel_h)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(panel, width=0.002)
                utils.apply_material(panel, carcass_mat)
                parts.append(panel)

        # Handles
        handle_offset_x = side * (door_w / 2.0 - 0.04)
        handle_z = door_z
        handle_y = door_y - 0.012

        if style in ["kitchen", "bathroom"]:
            # Modern thin steel handle
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(handle_offset_x, handle_y, handle_z))
            hnd = bpy.context.active_object
            hnd.name = f"CabinetHandle_{'L' if side < 0 else 'R'}"
            hnd.scale = (0.015, 0.015, 0.15 if style == "bathroom" else 0.2)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(hnd, width=0.002)
            utils.apply_material(hnd, handle_mat)
            parts.append(hnd)
        else:
            # Classic brass handle knob
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=0.012,
                subdivisions=2,
                location=(handle_offset_x, handle_y, handle_z)
            )
            hnd = bpy.context.active_object
            hnd.name = f"CabinetHandle_{'L' if side < 0 else 'R'}"
            utils.apply_smooth_by_angle(hnd, angle=40.0)
            utils.apply_material(hnd, handle_mat)
            parts.append(hnd)

    # Join cabinet parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = carcass
    bpy.ops.object.join()
    
    carcass.name = "CabinetAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return carcass

def main():
    parser = argparse.ArgumentParser(description="Procedural Cabinet Generator")
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
    cabinet_obj = generate_cabinet(params)
    
    if args.render:
        utils.setup_lighting_and_camera(cabinet_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
