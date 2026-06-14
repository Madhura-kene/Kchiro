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

def generate_nightstand(params):
    w = params.get("width", 50.0) / 100.0  # convert cm to meters
    d = params.get("depth", 40.0) / 100.0
    h = params.get("height", 60.0) / 100.0
    drawers_count = params.get("drawers", 1)
    has_open_shelf = params.get("has_open_shelf", True)
    style = params.get("style", "modern")

    parts = []

    # 1. Setup Materials
    if style == "classic":
        carcass_color = (0.35, 0.16, 0.1, 1.0) # Mahogany
        rough_carcass = 0.6
        handle_color = (0.75, 0.55, 0.2, 1.0) # Brass
        metallic_handle = 0.9
        carcass_mat = utils.create_material("NightstandWood", diffuse_color=carcass_color, metallic=0.0, roughness=rough_carcass)
        leg_mat = carcass_mat
    elif style == "mid_century":
        carcass_color = (0.58, 0.35, 0.18, 1.0) # Teak wood
        rough_carcass = 0.7
        handle_color = (0.75, 0.55, 0.2, 1.0) # Brass accents
        metallic_handle = 0.9
        carcass_mat = utils.create_material("NightstandTeak", diffuse_color=carcass_color, metallic=0.0, roughness=rough_carcass)
        leg_mat = carcass_mat
    else: # modern
        carcass_color = (0.95, 0.95, 0.95, 1.0) # Clean White
        rough_carcass = 0.45
        handle_color = (0.8, 0.8, 0.8, 1.0) # Silver steel
        metallic_handle = 0.9
        carcass_mat = utils.create_material("NightstandModern", diffuse_color=carcass_color, metallic=0.0, roughness=rough_carcass)
        leg_mat = utils.create_material("NightstandModernLeg", diffuse_color=(0.1, 0.1, 0.1, 1.0), metallic=0.7, roughness=0.3)

    handle_mat = utils.create_material("NightstandHandle", diffuse_color=handle_color, metallic=metallic_handle, roughness=0.15)
    tip_mat = utils.create_material("NightstandLegTip", diffuse_color=(0.75, 0.55, 0.2, 1.0), metallic=0.9, roughness=0.2) # Gold tips

    # 2. Dimensions & Legs
    if style == "mid_century":
        leg_h = 0.22
    elif style == "classic":
        leg_h = 0.06
    else: # modern
        leg_h = 0.04
        
    box_h = h - leg_h
    thick = 0.02
    box_center_z = leg_h + box_h / 2.0

    # 3. Corner Legs
    px = w / 2.0 - 0.04
    py = d / 2.0 - 0.04
    
    if style == "mid_century":
        # Four tapered angled legs
        for lx in [-px, px]:
            for ly in [-py, py]:
                # Top position
                lz = leg_h
                # Add tapered leg cylinder (use cone or cylinder, cylinder is easier then scale top/bottom)
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=0.02,
                    depth=leg_h,
                    location=(lx, ly, leg_h / 2.0)
                )
                leg = bpy.context.active_object
                leg.name = f"Leg_{lx}_{ly}"
                
                # Angled outwards
                rot_y = -0.12 if lx > 0 else 0.12
                rot_x = 0.12 if ly > 0 else -0.12
                leg.rotation_euler = (rot_x, rot_y, 0.0)
                
                # Apply rotation and scaling
                bpy.ops.object.transform_apply(rotation=True)
                utils.apply_smooth_by_angle(leg, angle=30.0)
                utils.apply_material(leg, leg_mat)
                parts.append(leg)
                
                # Gold brass tips at the bottom of the legs
                tip_h = 0.04
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=0.015,
                    depth=tip_h,
                    location=(lx + (math.sin(rot_y) * (leg_h/2.0 - tip_h/2.0)), ly - (math.sin(rot_x) * (leg_h/2.0 - tip_h/2.0)), tip_h/2.0)
                )
                tip = bpy.context.active_object
                tip.name = f"LegTip_{lx}_{ly}"
                tip.rotation_euler = (rot_x, rot_y, 0.0)
                bpy.ops.object.transform_apply(rotation=True)
                utils.apply_smooth_by_angle(tip, angle=30.0)
                utils.apply_material(tip, tip_mat)
                parts.append(tip)
                
    elif style == "classic":
        # Plinth solid base frame
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, leg_h / 2.0))
        plinth = bpy.context.active_object
        plinth.name = "PlinthBase"
        plinth.scale = (w - 0.02, d - 0.02, leg_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(plinth, width=0.003)
        utils.apply_material(plinth, leg_mat)
        parts.append(plinth)
        
    else: # modern
        # 4 small square block legs
        for lx in [-px, px]:
            for ly in [-py, py]:
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, leg_h / 2.0))
                block = bpy.context.active_object
                block.name = f"LegBlock_{lx}_{ly}"
                block.scale = (0.04, 0.04, leg_h)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(block, width=0.002)
                utils.apply_material(block, leg_mat)
                parts.append(block)

    # 4. Main Cabinet Carcass
    # Left side
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-w/2.0 + thick/2.0, 0.0, box_center_z))
    left = bpy.context.active_object
    left.name = "CarcassSideL"
    left.scale = (thick, d, box_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(left, width=0.003)
    utils.apply_material(left, carcass_mat)
    parts.append(left)
    master_obj = left

    # Right side
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(w/2.0 - thick/2.0, 0.0, box_center_z))
    right = bpy.context.active_object
    right.name = "CarcassSideR"
    right.scale = (thick, d, box_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(right, width=0.003)
    utils.apply_material(right, carcass_mat)
    parts.append(right)

    # Top panel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, h - thick/2.0))
    top = bpy.context.active_object
    top.name = "CarcassTop"
    top.scale = (w - thick*2.0, d, thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(top, width=0.003)
    utils.apply_material(top, carcass_mat)
    parts.append(top)

    # Bottom panel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, leg_h + thick/2.0))
    bottom = bpy.context.active_object
    bottom.name = "CarcassBottom"
    bottom.scale = (w - thick*2.0, d, thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(bottom, width=0.003)
    utils.apply_material(bottom, carcass_mat)
    parts.append(bottom)

    # Back panel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, d/2.0 - 0.005, box_center_z))
    back = bpy.context.active_object
    back.name = "CarcassBack"
    back.scale = (w - thick*2.0, 0.01, box_h - thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(back, carcass_mat)
    parts.append(back)

    # 5. Dividers & Drawers
    interior_bottom = leg_h + thick
    interior_top = h - thick
    interior_h = interior_top - interior_bottom

    drawer_area_bottom = interior_bottom
    drawer_area_h = interior_h

    # If open shelf is requested, partition the top part as open shelf
    if has_open_shelf:
        open_shelf_ratio = 0.45 if drawers_count > 0 else 1.0
        open_shelf_h = interior_h * open_shelf_ratio
        
        # Shelf divider board
        divider_z = interior_top - open_shelf_h - thick/2.0
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.01, divider_z))
        divider = bpy.context.active_object
        divider.name = "ShelfDivider"
        divider.scale = (w - thick*2.0 - 0.002, d - 0.02, thick)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(divider, width=0.002)
        utils.apply_material(divider, carcass_mat)
        parts.append(divider)
        
        # Adjust drawers area to below the shelf
        drawer_area_h = divider_z - thick/2.0 - interior_bottom
        # drawer_area_bottom is already interior_bottom

    # Drawers logic
    if drawers_count > 0:
        dh = drawer_area_h / drawers_count
        for i in range(drawers_count):
            dz = drawer_area_bottom + (i + 0.5) * dh
            
            # Drawer front pane
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -d/2.0 - 0.005, dz))
            front = bpy.context.active_object
            front.name = f"DrawerFront_{i}"
            front.scale = (w - thick*2.0 - 0.006, 0.015, dh - 0.006)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(front, width=0.002)
            utils.apply_material(front, carcass_mat)
            parts.append(front)
            
            # Handle centered on drawer front
            hy = -d/2.0 - 0.016
            if style == "modern":
                # Sleek modern metal tab/bar handle
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, hy, dz))
                hnd = bpy.context.active_object
                hnd.name = f"Handle_{i}"
                hnd.scale = (0.12, 0.015, 0.015)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(hnd, width=0.002)
                utils.apply_material(hnd, handle_mat)
                parts.append(hnd)
            elif style == "classic":
                # Classic brass handle knob
                bpy.ops.mesh.primitive_ico_sphere_add(
                    radius=0.012,
                    subdivisions=2,
                    location=(0.0, hy, dz)
                )
                hnd = bpy.context.active_object
                hnd.name = f"Handle_{i}"
                utils.apply_smooth_by_angle(hnd, angle=40.0)
                utils.apply_material(hnd, handle_mat)
                parts.append(hnd)
            else: # mid_century
                # Wooden button/peg handle knob
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=0.015,
                    depth=0.015,
                    location=(0.0, hy, dz)
                )
                hnd = bpy.context.active_object
                hnd.name = f"Handle_{i}"
                hnd.rotation_euler = (math.pi/2.0, 0.0, 0.0)
                bpy.ops.object.transform_apply(rotation=True)
                utils.apply_smooth_by_angle(hnd, angle=30.0)
                utils.apply_material(hnd, handle_mat)
                parts.append(hnd)

    # 6. Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = master_obj
    bpy.ops.object.join()

    master_obj.name = "NightstandAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return master_obj

def main():
    parser = argparse.ArgumentParser(description="Procedural Nightstand Generator")
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
    nightstand_obj = generate_nightstand(params)
    
    if args.render:
        utils.setup_lighting_and_camera(nightstand_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
