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

def generate_sofa(params):
    style = params.get("style", "sofa")
    w = params.get("width", 180.0) / 100.0  # convert cm to meters
    d = params.get("depth", 90.0) / 100.0
    has_armrests = params.get("has_armrests", True)
    
    parts = []
    
    # 1. Create Materials
    fabric_mat = utils.create_material("SofaFabric", diffuse_color=(0.22, 0.35, 0.45, 1.0), metallic=0.0, roughness=0.85) # Teal fabric
    wood_mat = utils.create_material("SofaLegsWood", diffuse_color=(0.28, 0.18, 0.1, 1.0), metallic=0.0, roughness=0.75) # Dark wood
    
    # Adapt width for armchair if needed
    if style == "armchair":
        w = max(0.75, min(1.10, w))
        
    # Dimensions setup
    leg_h = 0.12
    base_h = 0.15
    arm_w = 0.12 if has_armrests else 0.0
    arm_h = 0.52
    
    # 2. Add Corner Legs
    leg_offset_x = (w / 2.0) - 0.05
    leg_offset_y = (d / 2.0) - 0.05
    
    for lx in [-leg_offset_x, leg_offset_x]:
        for ly in [-leg_offset_y, leg_offset_y]:
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=12,
                radius=0.024,
                depth=leg_h,
                location=(lx, ly, leg_h / 2.0)
            )
            leg = bpy.context.active_object
            leg.name = f"SofaLeg_{'L' if lx < 0 else 'R'}_{'F' if ly < 0 else 'B'}"
            utils.apply_smooth_by_angle(leg, angle=40.0)
            utils.apply_material(leg, wood_mat)
            parts.append(leg)
            
    # 3. Main Support Base Frame
    base_z = leg_h + (base_h / 2.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, base_z))
    base = bpy.context.active_object
    base.name = "SofaBase"
    base.scale = (w, d, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(base, width=0.01)
    utils.apply_material(base, fabric_mat)
    parts.append(base)
    
    # 4. Side Armrests
    if has_armrests:
        for side in [-1.0, 1.0]:
            arm_x = side * ((w / 2.0) - (arm_w / 2.0))
            arm_z = leg_h + (arm_h / 2.0)
            
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(arm_x, 0.05, arm_z))
            arm = bpy.context.active_object
            arm.name = f"SofaArm_{'L' if side < 0 else 'R'}"
            # Extend armrest along depth but keep front slightly cut back
            arm.scale = (arm_w, d - 0.05, arm_h - leg_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(arm, width=0.012)
            utils.apply_material(arm, fabric_mat)
            parts.append(arm)
            
    # 5. Seat Cushions
    # Inner seat width between armrests
    cushion_w = w - (2.0 * arm_w)
    cushion_h = 0.15
    cushion_z = leg_h + base_h + (cushion_h / 2.0)
    
    # Split cushion into pieces based on width
    num_cushions = 1
    if style == "sofa" and w > 1.4:
        num_cushions = 3 if w > 2.0 else 2
    elif style == "couch":
        num_cushions = 2
        
    single_cushion_w = (cushion_w / num_cushions) - 0.005 # Small gap
    
    for i in range(num_cushions):
        # Calculate X position for each cushion
        offset_multiplier = i - (num_cushions - 1) / 2.0
        c_x = offset_multiplier * (single_cushion_w + 0.005)
        # Position cushion slightly forward (Y < 0)
        c_y = -0.02
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(c_x, c_y, cushion_z))
        cushion = bpy.context.active_object
        cushion.name = f"SofaSeatCushion_{i}"
        # Cushion depth is slightly shorter than total depth to leave room for backrest
        cushion.scale = (single_cushion_w, d - 0.16, cushion_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(cushion, width=0.016)
        utils.apply_material(cushion, fabric_mat)
        parts.append(cushion)
        
    # 6. Backrest cushions/board
    back_w = cushion_w if has_armrests else w
    back_h = 0.44
    back_thick = 0.12
    back_z = leg_h + base_h + (back_h / 2.0) + 0.08
    back_y = (d / 2.0) - (back_thick / 2.0) - 0.02
    
    # Split backrest cushion same as seat cushions
    for i in range(num_cushions):
        offset_multiplier = i - (num_cushions - 1) / 2.0
        b_x = offset_multiplier * (back_w / num_cushions)
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(b_x, back_y, back_z))
        back = bpy.context.active_object
        back.name = f"SofaBackCushion_{i}"
        back.scale = ((back_w / num_cushions) - 0.004, back_thick, back_h)
        # Rotate backrest cushion slightly backwards for comfort angle
        back.rotation_euler = (-0.1, 0, 0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_bevel(back, width=0.016)
        utils.apply_material(back, fabric_mat)
        parts.append(back)
        
    # Join all sofa parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    
    base.name = "SofaAsset"
    # Place pivot point at bottom center (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return base

def main():
    parser = argparse.ArgumentParser(description="Procedural Sofa Generator")
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
    sofa_obj = generate_sofa(params)
    
    if args.render:
        utils.setup_lighting_and_camera(sofa_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
