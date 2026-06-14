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

def generate_tv_stand(params):
    w = params.get("width", 150.0) / 100.0  # convert cm to meters
    d = params.get("depth", 45.0) / 100.0
    h = params.get("height", 50.0) / 100.0
    compartments = params.get("compartments", 3)
    has_doors = params.get("has_doors", False)
    style = params.get("style", "modern")

    parts = []

    # 1. Setup Materials
    if style == "industrial":
        # Dark reclaimed wood + black iron legs
        carcass_color = (0.38, 0.25, 0.15, 1.0)
        rough_carcass = 0.8
        door_color = carcass_color
        leg_color = (0.08, 0.08, 0.09, 1.0)
        metallic_leg = 0.95
        carcass_mat = utils.create_material("TVStandWood", diffuse_color=carcass_color, metallic=0.0, roughness=rough_carcass)
        door_mat = carcass_mat
        leg_mat = utils.create_material("TVStandIron", diffuse_color=leg_color, metallic=metallic_leg, roughness=0.45)
    elif style == "classic":
        # Reddish cherry wood + matching wood doors
        carcass_color = (0.42, 0.18, 0.1, 1.0)
        rough_carcass = 0.6
        door_color = carcass_color
        leg_color = carcass_color
        carcass_mat = utils.create_material("TVStandCherry", diffuse_color=carcass_color, metallic=0.0, roughness=rough_carcass)
        door_mat = carcass_mat
        leg_mat = carcass_mat
    else: # modern
        # Warm wood carcass + charcoal doors + brass/gold accents
        carcass_color = (0.68, 0.48, 0.32, 1.0) # honey oak
        rough_carcass = 0.65
        door_color = (0.15, 0.15, 0.16, 1.0)  # matte charcoal
        leg_color = (0.15, 0.15, 0.16, 1.0)
        carcass_mat = utils.create_material("TVStandOak", diffuse_color=carcass_color, metallic=0.0, roughness=rough_carcass)
        door_mat = utils.create_material("TVStandModernDoor", diffuse_color=door_color, metallic=0.0, roughness=0.5)
        leg_mat = utils.create_material("TVStandLegs", diffuse_color=leg_color, metallic=0.0, roughness=0.4)

    handle_mat = utils.create_material("TVStandHandle", diffuse_color=(0.75, 0.55, 0.2, 1.0), metallic=0.9, roughness=0.15) # Brass/Gold

    # 2. Dimensions & Legs setup
    leg_h = 0.12
    box_h = h - leg_h
    thick = 0.025
    box_center_z = leg_h + box_h / 2.0

    # 3. Build Legs
    if style == "industrial":
        # Loop frame legs at left and right ends (trapezoid metal plates)
        loop_w = 0.04
        loop_thick = 0.012
        for side in [-1.0, 1.0]:
            lx = side * (w / 2.0 - 0.1)
            # Leg loop structure: front post, back post, bottom connector bar
            # Front post
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, -d/2.0 + 0.04, leg_h / 2.0))
            fpost = bpy.context.active_object
            fpost.name = f"LegF_{side}"
            fpost.scale = (loop_w, loop_thick, leg_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(fpost, leg_mat)
            parts.append(fpost)
            
            # Back post
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, d/2.0 - 0.04, leg_h / 2.0))
            bpost = bpy.context.active_object
            bpost.name = f"LegB_{side}"
            bpost.scale = (loop_w, loop_thick, leg_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(bpost, leg_mat)
            parts.append(bpost)

            # Bottom bar
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, 0.0, loop_thick / 2.0))
            bbar = bpy.context.active_object
            bbar.name = f"LegBar_{side}"
            bbar.scale = (loop_w, d - 0.08, loop_thick)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(bbar, leg_mat)
            parts.append(bbar)

    elif style == "classic":
        # 4 turned wooden bun feet
        px = w / 2.0 - 0.12
        py = d / 2.0 - 0.08
        for lx in [-px, px]:
            for ly in [-py, py]:
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=0.035,
                    depth=leg_h,
                    location=(lx, ly, leg_h / 2.0)
                )
                foot = bpy.context.active_object
                foot.name = f"Foot_{lx}_{ly}"
                utils.apply_smooth_by_angle(foot, angle=40.0)
                utils.apply_material(foot, leg_mat)
                parts.append(foot)
                
    else: # modern
        # 4 angled thin round tapered legs
        px = w / 2.0 - 0.12
        py = d / 2.0 - 0.08
        for lx in [-px, px]:
            for ly in [-py, py]:
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=0.02,
                    depth=leg_h,
                    location=(lx, ly, leg_h / 2.0)
                )
                leg = bpy.context.active_object
                leg.name = f"Leg_{lx}_{ly}"
                
                # Angled outwards
                rot_y = -0.1 if lx > 0 else 0.1
                rot_x = 0.1 if ly > 0 else -0.1
                leg.rotation_euler = (rot_x, rot_y, 0.0)
                
                bpy.ops.object.transform_apply(rotation=True)
                utils.apply_smooth_by_angle(leg, angle=30.0)
                utils.apply_material(leg, leg_mat)
                parts.append(leg)

    # 4. Console Cabinet Box
    # Left Panel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-w/2.0 + thick/2.0, 0.0, box_center_z))
    left = bpy.context.active_object
    left.name = "ConsoleSideL"
    left.scale = (thick, d, box_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(left, width=0.004)
    utils.apply_material(left, carcass_mat)
    parts.append(left)
    master_obj = left

    # Right Panel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(w/2.0 - thick/2.0, 0.0, box_center_z))
    right = bpy.context.active_object
    right.name = "ConsoleSideR"
    right.scale = (thick, d, box_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(right, width=0.004)
    utils.apply_material(right, carcass_mat)
    parts.append(right)

    # Top Panel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, h - thick/2.0))
    top = bpy.context.active_object
    top.name = "ConsoleTop"
    top.scale = (w - thick*2.0, d, thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(top, width=0.004)
    utils.apply_material(top, carcass_mat)
    parts.append(top)

    # Bottom Panel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, leg_h + thick/2.0))
    bottom = bpy.context.active_object
    bottom.name = "ConsoleBottom"
    bottom.scale = (w - thick*2.0, d, thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(bottom, width=0.004)
    utils.apply_material(bottom, carcass_mat)
    parts.append(bottom)

    # Back Panel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, d/2.0 - 0.005, box_center_z))
    back = bpy.context.active_object
    back.name = "ConsoleBack"
    back.scale = (w - thick*2.0, 0.01, box_h - thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(back, carcass_mat)
    parts.append(back)

    # 5. Compartment Dividers
    interior_w = w - thick * 2.0
    part_thick = 0.015
    part_count = compartments - 1
    comp_space = interior_w - part_thick * part_count
    comp_w = comp_space / compartments

    # Create vertical partitions
    for c in range(part_count):
        px = -interior_w / 2.0 + (c + 1) * comp_w + c * part_thick + part_thick / 2.0
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, 0.01, box_center_z))
        divider = bpy.context.active_object
        divider.name = f"ConsoleDivider_{c}"
        divider.scale = (part_thick, d - 0.02, box_h - thick * 2.0)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(divider, width=0.002)
        utils.apply_material(divider, carcass_mat)
        parts.append(divider)

    # 6. Doors & Shelves inside Compartments
    door_thick = 0.018
    door_h = box_h - thick * 2.0 - 0.006
    door_z = leg_h + thick + door_h / 2.0 + 0.003
    door_y = -d / 2.0 - door_thick / 2.0

    for j in range(compartments):
        cx = -interior_w / 2.0 + (j + 0.5) * comp_w + j * part_thick
        
        # Decide if this compartment has a door
        is_door = False
        if has_doors:
            if compartments == 2:
                is_door = True
            elif compartments == 3:
                is_door = (j == 0 or j == 2) # open center shelf
            elif compartments == 4:
                is_door = (j == 0 or j == 3) # open middle shelves
            elif compartments == 5:
                is_door = (j == 0 or j == 2 or j == 4) # open 1 & 3, closed 0, 2, 4
                
        if is_door:
            # Add drawer / cupboard door panel
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, door_y, door_z))
            door = bpy.context.active_object
            door.name = f"ConsoleDoor_{j}"
            door.scale = (comp_w - 0.004, door_thick, door_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(door, width=0.002)
            utils.apply_material(door, door_mat)
            parts.append(door)
            
            # Simple handle knob/bar
            hy = door_y - 0.012
            if style == "classic":
                # round brass pull knob
                bpy.ops.mesh.primitive_ico_sphere_add(
                    radius=0.012,
                    subdivisions=2,
                    location=(cx, hy, door_z)
                )
                hnd = bpy.context.active_object
                hnd.name = f"ConsoleHandle_{j}"
                utils.apply_smooth_by_angle(hnd, angle=40.0)
                utils.apply_material(hnd, handle_mat)
                parts.append(hnd)
            else:
                # sleek brass metal pull bar
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, hy, door_z))
                hnd = bpy.context.active_object
                hnd.name = f"ConsoleHandle_{j}"
                hnd.scale = (0.12, 0.01, 0.015)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(hnd, width=0.002)
                utils.apply_material(hnd, handle_mat)
                parts.append(hnd)
        else:
            # Open compartment: add a middle shelf board for consoles
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, 0.01, box_center_z))
            mid_shelf = bpy.context.active_object
            mid_shelf.name = f"ConsoleMidShelf_{j}"
            mid_shelf.scale = (comp_w - 0.002, d - 0.02, 0.018)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(mid_shelf, width=0.002)
            utils.apply_material(mid_shelf, carcass_mat)
            parts.append(mid_shelf)

    # 7. Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = master_obj
    bpy.ops.object.join()

    master_obj.name = "TVStandAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return master_obj

def main():
    parser = argparse.ArgumentParser(description="Procedural TV Stand Generator")
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
    tv_stand_obj = generate_tv_stand(params)
    
    if args.render:
        utils.setup_lighting_and_camera(tv_stand_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
