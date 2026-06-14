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

def generate_couch(params):
    w = params.get("width", 200.0) / 100.0  # convert cm to meters
    d = params.get("depth", 90.0) / 100.0
    h = params.get("height", 85.0) / 100.0
    has_chaise = params.get("has_chaise", False)
    material = params.get("material", "fabric")

    parts = []

    # 1. Create Materials
    # Velvet/Teal, Leather/Brown, Fabric/Grey
    if material == "leather":
        upholstery_color = (0.28, 0.15, 0.08, 1.0) # Rich Brown
        metallic = 0.05
        roughness = 0.4
    elif material == "velvet":
        upholstery_color = (0.08, 0.22, 0.35, 1.0) # Sapphire Blue
        metallic = 0.0
        roughness = 0.9
    else: # fabric
        upholstery_color = (0.45, 0.44, 0.42, 1.0) # Grey Fabric
        metallic = 0.0
        roughness = 0.8

    couch_mat = utils.create_material("CouchUpholstery", diffuse_color=upholstery_color, metallic=metallic, roughness=roughness)
    wood_mat = utils.create_material("CouchLegsWood", diffuse_color=(0.18, 0.1, 0.05, 1.0), metallic=0.0, roughness=0.8)

    # 2. Dimensions setup
    leg_h = 0.10
    base_h = 0.14
    arm_w = 0.15
    arm_h = 0.55
    back_thick = 0.14
    cushion_h = 0.16

    # 3. Add Corner Legs
    # If we have a chaise, we'll need extra legs. Let's place standard corner legs first.
    leg_offset_x = (w / 2.0) - 0.06
    leg_offset_y = (d / 2.0) - 0.06
    
    # 4 standard legs
    for lx in [-leg_offset_x, leg_offset_x]:
        for ly in [-leg_offset_y, leg_offset_y]:
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=12,
                radius=0.03,
                depth=leg_h,
                location=(lx, ly, leg_h / 2.0)
            )
            leg = bpy.context.active_object
            leg.name = f"CouchLeg_{'L' if lx < 0 else 'R'}_{'F' if ly < 0 else 'B'}"
            utils.apply_smooth_by_angle(leg, angle=40.0)
            utils.apply_material(leg, wood_mat)
            parts.append(leg)

    # If chaise is active, add 2 additional legs forward on the right-hand side
    if has_chaise:
        chaise_center_y = d * 0.7  # forward placement
        for lx in [leg_offset_x - 0.1, leg_offset_x - d/2.0]:
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=12,
                radius=0.03,
                depth=leg_h,
                location=(lx, chaise_center_y, leg_h / 2.0)
            )
            leg = bpy.context.active_object
            leg.name = f"CouchLeg_Chaise_{lx}"
            utils.apply_smooth_by_angle(leg, angle=40.0)
            utils.apply_material(leg, wood_mat)
            parts.append(leg)

    # 4. Main Support Base Frame
    base_z = leg_h + (base_h / 2.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, base_z))
    base = bpy.context.active_object
    base.name = "CouchBase"
    base.scale = (w, d, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(base, width=0.012)
    utils.apply_material(base, couch_mat)
    parts.append(base)

    if has_chaise:
        # Extend base frame forward on the right side
        chaise_w = (w - (2.0 * arm_w)) / 3.0 + 0.05
        chaise_base_x = (w / 2.0) - arm_w - (chaise_w / 2.0)
        chaise_base_y = (d / 2.0) + (d * 0.4)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(chaise_base_x, chaise_base_y, base_z))
        chaise_base = bpy.context.active_object
        chaise_base.name = "CouchBaseChaise"
        chaise_base.scale = (chaise_w, d * 0.8, base_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(chaise_base, width=0.012)
        utils.apply_material(chaise_base, couch_mat)
        parts.append(chaise_base)

    # 5. Side Armrests
    for side in [-1.0, 1.0]:
        arm_x = side * ((w / 2.0) - (arm_w / 2.0))
        arm_z = leg_h + (arm_h / 2.0)
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(arm_x, 0.0, arm_z))
        arm = bpy.context.active_object
        arm.name = f"CouchArm_{'L' if side < 0 else 'R'}"
        arm.scale = (arm_w, d, arm_h - leg_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(arm, width=0.015)
        utils.apply_material(arm, couch_mat)
        parts.append(arm)

    # 6. Seat Cushions
    cushion_w = w - (2.0 * arm_w)
    cushion_z = leg_h + base_h + (cushion_h / 2.0)
    
    num_cushions = 3 if w > 1.8 else 2
    single_cushion_w = (cushion_w / num_cushions) - 0.006

    for i in range(num_cushions):
        offset_multiplier = i - (num_cushions - 1) / 2.0
        c_x = offset_multiplier * (single_cushion_w + 0.006)
        
        # If chaise is active and this is the rightmost cushion, stretch it forward
        if has_chaise and i == (num_cushions - 1):
            chaise_c_y = (d * 0.4) - (back_thick / 2.0)
            chaise_c_d = d * 1.8 - back_thick
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(c_x, chaise_c_y, cushion_z))
            cushion = bpy.context.active_object
            cushion.name = "CouchChaiseCushion"
            cushion.scale = (single_cushion_w, chaise_c_d, cushion_h)
        else:
            c_y = -back_thick / 2.0
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(c_x, c_y, cushion_z))
            cushion = bpy.context.active_object
            cushion.name = f"CouchSeatCushion_{i}"
            cushion.scale = (single_cushion_w, d - back_thick - 0.02, cushion_h)
            
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(cushion, width=0.02)
        utils.apply_material(cushion, couch_mat)
        parts.append(cushion)

    # 7. Backrest Cushions
    back_h = h - leg_h - base_h - cushion_h + 0.15
    back_z = leg_h + base_h + cushion_h + (back_h / 2.0) - 0.05
    back_y = (d / 2.0) - (back_thick / 2.0)

    # Place back cushions matching seat cushion width (but don't cover the chaise extension, just standard back)
    for i in range(num_cushions):
        offset_multiplier = i - (num_cushions - 1) / 2.0
        b_x = offset_multiplier * (cushion_w / num_cushions)
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(b_x, back_y, back_z))
        back = bpy.context.active_object
        back.name = f"CouchBackCushion_{i}"
        back.scale = ((cushion_w / num_cushions) - 0.005, back_thick, back_h)
        back.rotation_euler = (-0.08, 0, 0) # slight tilt
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_bevel(back, width=0.02)
        utils.apply_material(back, couch_mat)
        parts.append(back)

    # Join all couch parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    
    base.name = "CouchAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return base

def main():
    parser = argparse.ArgumentParser(description="Procedural Couch Generator")
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
    couch_obj = generate_couch(params)
    
    if args.render:
        utils.setup_lighting_and_camera(couch_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
