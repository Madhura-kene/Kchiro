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

def generate_towel_rack(params):
    w = params.get("width", 60.0) / 100.0  # cm to meters
    d = params.get("depth", 15.0) / 100.0  # cm to meters
    h = params.get("height", 20.0) / 100.0 # cm to meters
    bar_style = params.get("bar_style", "single_bar")
    material_type = params.get("material", "chrome")
    has_towel = params.get("has_towel", True)
    towel_color = params.get("towel_color", "white")

    parts = []

    # 1. Setup Materials
    # Metal/Wood Rack Material
    if material_type == "brass":
        rack_diffuse = (0.75, 0.60, 0.20, 1.0)
        rack_metallic = 0.9
        rack_roughness = 0.2
    elif material_type == "matte_black":
        rack_diffuse = (0.1, 0.1, 0.1, 1.0)
        rack_metallic = 0.15
        rack_roughness = 0.85
    elif material_type == "wood":
        rack_diffuse = (0.40, 0.25, 0.15, 1.0)
        rack_metallic = 0.0
        rack_roughness = 0.7
    else: # chrome
        rack_diffuse = (0.85, 0.85, 0.88, 1.0)
        rack_metallic = 0.95
        rack_roughness = 0.05

    rack_mat = utils.create_material(f"RackMaterial_{material_type}", diffuse_color=rack_diffuse, metallic=rack_metallic, roughness=rack_roughness)

    # Towel Fabric Material
    if towel_color == "blue":
        towel_diffuse = (0.22, 0.48, 0.75, 1.0)
    elif towel_color == "gray":
        towel_diffuse = (0.45, 0.47, 0.50, 1.0)
    elif towel_color == "green":
        towel_diffuse = (0.28, 0.55, 0.38, 1.0)
    else: # white
        towel_diffuse = (0.95, 0.95, 0.95, 1.0)

    towel_mat = utils.create_material(f"TowelFabric_{towel_color}", diffuse_color=towel_diffuse, metallic=0.0, roughness=0.95)

    # We position the rack centered on X, mounted on the wall at Y = 0.
    # Height Z is centered at h.
    center_z = max(0.5, h) # Keep height off the ground

    # 2. Build Brackets/Wall Mounts
    bracket_radius = 0.012
    bracket_depth = d - 0.02 # leave room for bar caps
    
    # Left & Right side bracket stems extending from wall
    for side in [-1, 1]:
        bx = side * (w / 2.0 - 0.02)
        
        if bar_style == "shelf_style":
            # For shelf style, brackets are flat side panels or dual supports
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, -d / 2.0, center_z))
            side_panel = bpy.context.active_object
            side_panel.name = f"SidePanel_{'L' if side < 0 else 'R'}"
            side_panel.scale = (0.015, d, 0.08)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(side_panel, width=0.003)
            utils.apply_material(side_panel, rack_mat)
            parts.append(side_panel)

            # Back wall mount plates
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, -0.005, center_z))
            wall_plate = bpy.context.active_object
            wall_plate.name = f"WallPlate_{'L' if side < 0 else 'R'}"
            wall_plate.scale = (0.04, 0.01, 0.12)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(wall_plate, width=0.002)
            utils.apply_material(wall_plate, rack_mat)
            parts.append(wall_plate)

        else: # single_bar or double_bar
            # Wall mount base plate (flange)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.01, location=(bx, -0.005, center_z))
            flange = bpy.context.active_object
            flange.name = f"WallFlange_{'L' if side < 0 else 'R'}"
            flange.rotation_euler = (math.radians(90.0), 0, 0)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            utils.apply_smooth_by_angle(flange)
            utils.apply_material(flange, rack_mat)
            parts.append(flange)

            if bar_style == "double_bar":
                # Double bar brackets are Y-shaped or dual stems
                # Upper stem (longer/deeper)
                bpy.ops.mesh.primitive_cylinder_add(radius=bracket_radius, depth=bracket_depth, location=(bx, -bracket_depth / 2.0, center_z + 0.04))
                stem_u = bpy.context.active_object
                stem_u.rotation_euler = (math.radians(90.0), 0, 0)
                bpy.ops.object.transform_apply(scale=True, rotation=True)
                utils.apply_smooth_by_angle(stem_u)
                utils.apply_material(stem_u, rack_mat)
                parts.append(stem_u)

                # Lower stem (shorter/shallower)
                lower_depth = bracket_depth * 0.65
                bpy.ops.mesh.primitive_cylinder_add(radius=bracket_radius, depth=lower_depth, location=(bx, -lower_depth / 2.0, center_z - 0.04))
                stem_l = bpy.context.active_object
                stem_l.rotation_euler = (math.radians(90.0), 0, 0)
                bpy.ops.object.transform_apply(scale=True, rotation=True)
                utils.apply_smooth_by_angle(stem_l)
                utils.apply_material(stem_l, rack_mat)
                parts.append(stem_l)
            else: # single_bar
                # Single bracket stem
                bpy.ops.mesh.primitive_cylinder_add(radius=bracket_radius, depth=bracket_depth, location=(bx, -bracket_depth / 2.0, center_z))
                stem = bpy.context.active_object
                stem.rotation_euler = (math.radians(90.0), 0, 0)
                bpy.ops.object.transform_apply(scale=True, rotation=True)
                utils.apply_smooth_by_angle(stem)
                utils.apply_material(stem, rack_mat)
                parts.append(stem)

    # 3. Build Bars
    bar_radius = 0.01
    towel_bar_y = 0.0 # Will track where the towel should hang
    towel_bar_z = 0.0

    if bar_style == "single_bar":
        towel_bar_y = -d + 0.015
        towel_bar_z = center_z
        bpy.ops.mesh.primitive_cylinder_add(radius=bar_radius, depth=w, location=(0, towel_bar_y, towel_bar_z))
        bar = bpy.context.active_object
        bar.name = "SingleTowelBar"
        bar.rotation_euler = (0, math.radians(90.0), 0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_smooth_by_angle(bar)
        utils.apply_material(bar, rack_mat)
        parts.append(bar)

    elif bar_style == "double_bar":
        # Upper/Back bar
        bpy.ops.mesh.primitive_cylinder_add(radius=bar_radius, depth=w, location=(0, -d + 0.015, center_z + 0.04))
        bar_u = bpy.context.active_object
        bar_u.rotation_euler = (0, math.radians(90.0), 0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_smooth_by_angle(bar_u)
        utils.apply_material(bar_u, rack_mat)
        parts.append(bar_u)

        # Lower/Front bar (this is where the towel hangs)
        towel_bar_y = -d * 0.65 + 0.015
        towel_bar_z = center_z - 0.04
        bpy.ops.mesh.primitive_cylinder_add(radius=bar_radius, depth=w, location=(0, towel_bar_y, towel_bar_z))
        bar_l = bpy.context.active_object
        bar_l.rotation_euler = (0, math.radians(90.0), 0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_smooth_by_angle(bar_l)
        utils.apply_material(bar_l, rack_mat)
        parts.append(bar_l)

    elif bar_style == "shelf_style":
        # Create a shelf grid (4 thin parallel bars)
        shelf_z = center_z + 0.03
        num_shelf_bars = 4
        for i in range(num_shelf_bars):
            sy = -0.02 - i * ((d - 0.04) / (num_shelf_bars - 1))
            bpy.ops.mesh.primitive_cylinder_add(radius=0.007, depth=w - 0.04, location=(0, sy, shelf_z))
            sbar = bpy.context.active_object
            sbar.rotation_euler = (0, math.radians(90.0), 0)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            utils.apply_smooth_by_angle(sbar)
            utils.apply_material(sbar, rack_mat)
            parts.append(sbar)

        # Front guard/rim bar
        bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=w, location=(0, -d + 0.01, shelf_z + 0.02))
        guard_bar = bpy.context.active_object
        guard_bar.rotation_euler = (0, math.radians(90.0), 0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_smooth_by_angle(guard_bar)
        utils.apply_material(guard_bar, rack_mat)
        parts.append(guard_bar)

        # Hanging towel bar underneath
        towel_bar_y = -d + 0.03
        towel_bar_z = center_z - 0.03
        bpy.ops.mesh.primitive_cylinder_add(radius=bar_radius, depth=w - 0.04, location=(0, towel_bar_y, towel_bar_z))
        hbar = bpy.context.active_object
        hbar.rotation_euler = (0, math.radians(90.0), 0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_smooth_by_angle(hbar)
        utils.apply_material(hbar, rack_mat)
        parts.append(hbar)

    # 4. Build Towel
    if has_towel:
        towel_w = w * 0.55
        towel_thickness = 0.006

        # Front drape (hangs lower)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, towel_bar_y - bar_radius - towel_thickness/2.0, towel_bar_z - 0.16))
        towel_front = bpy.context.active_object
        towel_front.name = "TowelFront"
        towel_front.scale = (towel_w, towel_thickness, 0.30)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(towel_front, width=0.002)
        utils.apply_material(towel_front, towel_mat)
        parts.append(towel_front)

        # Back drape (hangs slightly shorter)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, towel_bar_y + bar_radius + towel_thickness/2.0, towel_bar_z - 0.12))
        towel_back = bpy.context.active_object
        towel_back.name = "TowelBack"
        towel_back.scale = (towel_w, towel_thickness, 0.22)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(towel_back, width=0.002)
        utils.apply_material(towel_back, towel_mat)
        parts.append(towel_back)

        # Top loop/fold (covers the top of the bar)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, towel_bar_y, towel_bar_z + bar_radius))
        towel_top = bpy.context.active_object
        towel_top.name = "TowelTop"
        towel_top.scale = (towel_w, bar_radius * 2.0 + towel_thickness, 0.015)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(towel_top, width=0.002)
        utils.apply_material(towel_top, towel_mat)
        parts.append(towel_top)

    # 5. Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    
    # Active object is the main bracket or frame
    main_obj = parts[0]
    bpy.context.view_layer.objects.active = main_obj
    bpy.ops.object.join()

    main_obj.name = "TowelRackAsset"
    # Set origin to (0, 0, 0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return main_obj

def main():
    parser = argparse.ArgumentParser(description="Procedural Towel Rack Generator")
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
    obj = generate_towel_rack(params)

    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
