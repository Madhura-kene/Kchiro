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

def generate_chair(params):
    width = params.get("width", 50.0) / 100.0  # convert cm to meters
    depth = params.get("depth", 50.0) / 100.0
    seat_height = params.get("seat_height", 45.0) / 100.0
    backrest_height = params.get("backrest_height", 50.0) / 100.0
    leg_style = params.get("leg_style", "square")
    
    parts = []
    
    # 1. Create Wood Material
    wood_mat = utils.create_material("ChairWood", diffuse_color=(0.42, 0.26, 0.15, 1.0), metallic=0.0, roughness=0.6)
    
    # 2. Seat Panel
    thickness = 0.035  # 3.5cm seat thickness
    seat_z = seat_height - (thickness / 2.0)
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, seat_z))
    seat = bpy.context.active_object
    seat.name = "ChairSeat"
    seat.scale = (width, depth, thickness)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(seat, width=0.005)
    utils.apply_material(seat, wood_mat)
    parts.append(seat)
    
    # 3. Four Legs
    leg_h = seat_height - thickness
    leg_z = leg_h / 2.0
    
    # Offset legs slightly inside the seat edges
    inset = 0.05
    pos_x = (width / 2.0) - inset
    pos_y = (depth / 2.0) - inset
    
    leg_positions = [
        (-pos_x, -pos_y),
        (pos_x, -pos_y),
        (-pos_x, pos_y),
        (pos_x, pos_y)
    ]
    
    for idx, (x, y) in enumerate(leg_positions):
        if leg_style == "round":
            radius = 0.022
            bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=leg_h, location=(x, y, leg_z))
            leg = bpy.context.active_object
            leg.name = f"Leg_{idx}"
            utils.apply_smooth_by_angle(leg)
        else:  # square default
            size = 0.045
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, leg_z))
            leg = bpy.context.active_object
            leg.name = f"Leg_{idx}"
            leg.scale = (size, size, leg_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(leg, width=0.003)
            
        utils.apply_material(leg, wood_mat)
        parts.append(leg)
        
    # 4. Backrest (two vertical posts at the rear, connected by horizontal slats)
    post_w = 0.035
    post_z = seat_height + (backrest_height / 2.0)
    
    rear_positions = [
        (-pos_x, pos_y),
        (pos_x, pos_y)
    ]
    
    for idx, (x, y) in enumerate(rear_positions):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, post_z))
        post = bpy.context.active_object
        post.name = f"BackPost_{idx}"
        post.scale = (post_w, post_w, backrest_height)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(post, width=0.003)
        utils.apply_material(post, wood_mat)
        parts.append(post)
        
    # Horizontal Slats
    slat_h = 0.04
    slat_thick = 0.015
    slat_w = width - (2.0 * inset)
    
    # 3 slats spaced out along the backrest height
    slat_z_factors = [0.4, 0.7, 0.95]
    for idx, factor in enumerate(slat_z_factors):
        sz = seat_height + (backrest_height * factor)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, pos_y, sz))
        slat = bpy.context.active_object
        slat.name = f"BackSlat_{idx}"
        slat.scale = (slat_w, slat_thick, slat_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(slat, width=0.002)
        utils.apply_material(slat, wood_mat)
        parts.append(slat)
        
    # Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = seat
    bpy.ops.object.join()
    
    seat.name = "ChairAsset"
    # Place pivot point at ground level center (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return seat

def main():
    parser = argparse.ArgumentParser(description="Procedural Chair Generator")
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
    chair_obj = generate_chair(params)
    
    if args.render:
        utils.setup_lighting_and_camera(chair_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
