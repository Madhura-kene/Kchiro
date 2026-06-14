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

def generate_sword(params):
    # Extract params and convert cm to meters
    blade_length = params.get("blade_length", 90.0) / 100.0
    blade_width = params.get("blade_width", 5.0) / 100.0
    grip_length = params.get("grip_length", 15.0) / 100.0
    crossguard_type = params.get("crossguard_type", "simple")
    grip_mat_type = params.get("grip_material", "leather")
    
    parts = []
    
    # 1. Create Materials
    steel_mat = utils.create_material("BladeSteel", diffuse_color=(0.75, 0.75, 0.78, 1.0), metallic=0.9, roughness=0.2)
    brass_mat = utils.create_material("HiltBrass", diffuse_color=(0.85, 0.65, 0.25, 1.0), metallic=0.95, roughness=0.15)
    
    if grip_mat_type == "wood":
        grip_mat = utils.create_material("GripWood", diffuse_color=(0.4, 0.25, 0.15, 1.0), metallic=0.0, roughness=0.7)
    elif grip_mat_type == "metal":
        grip_mat = brass_mat
    else:  # leather default
        grip_mat = utils.create_material("GripLeather", diffuse_color=(0.3, 0.18, 0.12, 1.0), metallic=0.0, roughness=0.85)

    # 2. Pommel (Z bottom)
    pommel_radius = 0.035
    pommel_z = pommel_radius
    bpy.ops.mesh.primitive_uv_sphere_add(radius=pommel_radius, location=(0, 0, pommel_z))
    pommel = bpy.context.active_object
    pommel.name = "Pommel"
    utils.apply_smooth_by_angle(pommel)
    utils.apply_bevel(pommel, width=0.002)
    utils.apply_material(pommel, brass_mat)
    parts.append(pommel)
    
    # 3. Grip (Z middle)
    grip_radius = 0.016
    grip_z = pommel_z + pommel_radius + (grip_length / 2.0)
    bpy.ops.mesh.primitive_cylinder_add(radius=grip_radius, depth=grip_length, location=(0, 0, grip_z))
    grip = bpy.context.active_object
    grip.name = "Grip"
    # Scale Y slightly to make grip oval (ergonomic)
    grip.scale = (1.0, 0.75, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_smooth_by_angle(grip)
    utils.apply_material(grip, grip_mat)
    parts.append(grip)
    
    # 4. Crossguard
    crossguard_z = grip_z + (grip_length / 2.0) + 0.0125
    if crossguard_type == "curved":
        # Draw two curved arms
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        c_left = bpy.context.active_object
        c_left.name = "CrossguardLeft"
        c_left.scale = (blade_width * 2.0, 0.02, 0.02)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(c_left, width=0.002)
        c_left.location = (-blade_width * 1.0, 0, crossguard_z + 0.01)
        c_left.rotation_euler = (0, 0.2, 0) # Rotate up slightly
        utils.apply_material(c_left, brass_mat)
        parts.append(c_left)
        
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        c_right = bpy.context.active_object
        c_right.name = "CrossguardRight"
        c_right.scale = (blade_width * 2.0, 0.02, 0.02)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(c_right, width=0.002)
        c_right.location = (blade_width * 1.0, 0, crossguard_z + 0.01)
        c_right.rotation_euler = (0, -0.2, 0)
        utils.apply_material(c_right, brass_mat)
        parts.append(c_right)
    elif crossguard_type == "none":
        # No crossguard, just a small brass ring
        bpy.ops.mesh.primitive_cylinder_add(radius=blade_width * 0.8, depth=0.015, location=(0, 0, crossguard_z))
        hilt_ring = bpy.context.active_object
        hilt_ring.name = "HiltRing"
        utils.apply_material(hilt_ring, brass_mat)
        parts.append(hilt_ring)
    else:  # simple straight crossguard
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        guard = bpy.context.active_object
        guard.name = "Crossguard"
        guard.scale = (blade_width * 4.0, 0.025, 0.025)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(guard, width=0.002)
        guard.location = (0, 0, crossguard_z)
        utils.apply_material(guard, brass_mat)
        parts.append(guard)

    # 5. Blade
    # We leave 10 cm at the top of the length parameter for the tapered point
    main_blade_len = max(0.1, blade_length - 0.1)
    tip_len = 0.1
    
    blade_start_z = crossguard_z + 0.0125
    blade_center_z = blade_start_z + (main_blade_len / 2.0)
    
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    blade = bpy.context.active_object
    blade.name = "Blade"
    # Flatten the cube to make it a blade shape
    blade.scale = (blade_width, 0.008, main_blade_len)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(blade, width=0.001)
    blade.location = (0, 0, blade_center_z)
    utils.apply_material(blade, steel_mat)
    parts.append(blade)
    
    # 6. Blade Tip
    # A cone scaled to thinness makes a perfect tapered tip
    tip_z = blade_start_z + main_blade_len + (tip_len / 2.0)
    bpy.ops.mesh.primitive_cone_add(radius1=blade_width / 2.0, radius2=0.0, depth=tip_len, location=(0, 0, tip_z))
    tip = bpy.context.active_object
    tip.name = "BladeTip"
    # Rotate cone so it points UP (+Z)
    tip.rotation_euler = (0, 0, 0)
    # Scale thickness (Y-axis) to match blade thickness
    tip.scale = (2.0, 0.008 / (blade_width / 2.0), 1.0)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(tip, steel_mat)
    parts.append(tip)
    
    # Join all parts into one model
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
    
    # Make the blade the active object to join into
    bpy.context.view_layer.objects.active = blade
    bpy.ops.object.join()
    
    blade.name = "SwordAsset"
    # Place pivot point at the bottom of the pommel (0, 0, 0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return blade

def main():
    parser = argparse.ArgumentParser(description="Procedural Sword Generator")
    parser.add_argument("--params", type=str, required=True, help="Path to JSON parameter file")
    parser.add_argument("--export", type=str, required=True, help="Path to export GLB")
    parser.add_argument("--render", type=str, help="Path to render preview PNG")
    
    # Find arguments after '--'
    try:
        args_idx = sys.argv.index("--")
        script_args = sys.argv[args_idx + 1:]
    except ValueError:
        script_args = []
        
    args = parser.parse_args(script_args)
    
    # Load parameters
    with open(args.params, 'r') as f:
        params = json.load(f)
        
    # Run Generation
    utils.cleanup_scene()
    sword_obj = generate_sword(params)
    
    # Setup rendering and export
    if args.render:
        utils.setup_lighting_and_camera(sword_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
