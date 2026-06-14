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

def generate_armchair(params):
    w = params.get("width", 85.0) / 100.0  # convert cm to meters
    d = params.get("depth", 80.0) / 100.0
    h = params.get("height", 85.0) / 100.0
    style = params.get("style", "classic")
    material = params.get("material", "fabric")

    parts = []

    # 1. Create Materials
    # Velvet/Teal, Leather/Brown, Fabric/Grey
    if material == "leather":
        upholstery_color = (0.22, 0.12, 0.06, 1.0) # Rich Brown
        metallic = 0.05
        roughness = 0.45
    elif material == "velvet":
        upholstery_color = (0.02, 0.3, 0.18, 1.0) # Forest Green
        metallic = 0.0
        roughness = 0.9
    else: # fabric
        upholstery_color = (0.55, 0.52, 0.48, 1.0) # Beige Fabric
        metallic = 0.0
        roughness = 0.85

    uph_mat = utils.create_material("ArmchairUpholstery", diffuse_color=upholstery_color, metallic=metallic, roughness=roughness)
    wood_mat = utils.create_material("ArmchairWood", diffuse_color=(0.25, 0.15, 0.08, 1.0), metallic=0.0, roughness=0.7)
    metal_mat = utils.create_material("ArmchairMetal", diffuse_color=(0.15, 0.15, 0.15, 1.0), metallic=0.9, roughness=0.2)

    # 2. Dimensions setup
    leg_h = 0.14
    base_h = 0.15
    arm_w = 0.12 if style != "modern" else 0.04
    arm_h = 0.52
    back_thick = 0.12
    cushion_h = 0.15

    # Adjust values for recliner
    if style == "recliner":
        leg_h = 0.05 # Recliners sit very low, blocky
        base_h = 0.22
        arm_w = 0.16
        arm_h = 0.60
        cushion_h = 0.18

    # 3. Legs
    leg_offset_x = (w / 2.0) - 0.05
    leg_offset_y = (d / 2.0) - 0.05
    
    leg_mat = wood_mat if style != "modern" else metal_mat
    
    # Generate 4 legs
    for lx in [-leg_offset_x, leg_offset_x]:
        for ly in [-leg_offset_y, leg_offset_y]:
            if style == "recliner":
                # blocky legs
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, leg_h / 2.0))
                leg = bpy.context.active_object
                leg.name = f"ArmchairLeg_{lx}_{ly}"
                leg.scale = (0.08, 0.08, leg_h)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(leg, width=0.005)
            else:
                # cylindrical or splayed legs
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=12,
                    radius=0.024,
                    depth=leg_h,
                    location=(lx, ly, leg_h / 2.0)
                )
                leg = bpy.context.active_object
                leg.name = f"ArmchairLeg_{lx}_{ly}"
                utils.apply_smooth_by_angle(leg, angle=40.0)
                
            utils.apply_material(leg, leg_mat)
            parts.append(leg)

    # 4. Main Support Base Frame
    base_z = leg_h + (base_h / 2.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, base_z))
    base = bpy.context.active_object
    base.name = "ArmchairBase"
    base.scale = (w, d, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(base, width=0.012)
    utils.apply_material(base, uph_mat)
    parts.append(base)

    # 5. Side Armrests
    for side in [-1.0, 1.0]:
        arm_x = side * ((w / 2.0) - (arm_w / 2.0))
        arm_z = leg_h + (arm_h / 2.0)
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(arm_x, 0.0, arm_z))
        arm = bpy.context.active_object
        arm.name = f"ArmchairArm_{'L' if side < 0 else 'R'}"
        arm.scale = (arm_w, d, arm_h - leg_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(arm, width=0.018 if style == "classic" else 0.005)
        
        if style == "modern":
            # Modern style armrests are wooden or metal wrapper panels
            utils.apply_material(arm, leg_mat)
        else:
            utils.apply_material(arm, uph_mat)
        parts.append(arm)

    # 6. Seat Cushion
    cushion_w = w - (2.0 * arm_w) - 0.005
    cushion_z = leg_h + base_h + (cushion_h / 2.0)
    cush_y = -back_thick / 2.0
    cush_d = d - back_thick - 0.01
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, cush_y, cushion_z))
    cushion = bpy.context.active_object
    cushion.name = "ArmchairSeatCushion"
    cushion.scale = (cushion_w, cush_d, cushion_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(cushion, width=0.02)
    utils.apply_material(cushion, uph_mat)
    parts.append(cushion)

    # 7. Recliner footrest
    if style == "recliner":
        footrest_d = 0.28
        footrest_y = cush_y - (cush_d / 2.0) - (footrest_d / 2.0) + 0.02
        footrest_z = cushion_z - 0.05
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, footrest_y, footrest_z))
        footrest = bpy.context.active_object
        footrest.name = "ArmchairFootrest"
        footrest.scale = (cushion_w - 0.02, footrest_d, cushion_h - 0.04)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(footrest, width=0.015)
        utils.apply_material(footrest, uph_mat)
        parts.append(footrest)

    # 8. Backrest Cushion
    back_h = h - leg_h - base_h - cushion_h + 0.15
    back_z = leg_h + base_h + cushion_h + (back_h / 2.0) - 0.05
    back_y = (d / 2.0) - (back_thick / 2.0)
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, back_y, back_z))
    back = bpy.context.active_object
    back.name = "ArmchairBackCushion"
    back.scale = (cushion_w + (0.02 if style == "classic" else 0.0), back_thick, back_h)
    back.rotation_euler = (-0.1, 0, 0) # tilt slightly back
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    utils.apply_bevel(back, width=0.02 if style == "classic" else 0.006)
    utils.apply_material(back, uph_mat)
    parts.append(back)

    # Join all armchair parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    
    base.name = "ArmchairAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return base

def main():
    parser = argparse.ArgumentParser(description="Procedural Armchair Generator")
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
    armchair_obj = generate_armchair(params)
    
    if args.render:
        utils.setup_lighting_and_camera(armchair_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
