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

def generate_axe(params):
    shaft_len = params.get("shaft_length", 80.0) / 100.0  # convert cm to meters
    style = params.get("axe_style", "single")
    head_mat_type = params.get("head_material", "steel")
    shaft_mat_type = params.get("shaft_material", "wood")
    
    parts = []
    
    # 1. Create Materials
    steel_mat = utils.create_material("AxeSteel", diffuse_color=(0.7, 0.7, 0.72, 1.0), metallic=0.9, roughness=0.25)
    brass_mat = utils.create_material("AxeBrass", diffuse_color=(0.85, 0.65, 0.25, 1.0), metallic=0.95, roughness=0.2)
    wood_mat = utils.create_material("AxeWood", diffuse_color=(0.38, 0.24, 0.13, 1.0), metallic=0.0, roughness=0.7)
    leather_mat = utils.create_material("AxeLeather", diffuse_color=(0.25, 0.15, 0.1, 1.0), metallic=0.0, roughness=0.85)
    
    # Select materials
    head_mat = brass_mat if head_mat_type == "brass" else steel_mat
    shaft_mat = steel_mat if shaft_mat_type == "metal" else wood_mat
    
    # 2. Main Shaft
    shaft_radius = 0.016
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=shaft_radius,
        depth=shaft_len,
        location=(0, 0, shaft_len / 2.0)
    )
    shaft = bpy.context.active_object
    shaft.name = "AxeShaft"
    utils.apply_smooth_by_angle(shaft)
    utils.apply_material(shaft, shaft_mat)
    parts.append(shaft)
    
    # 3. Grip Wrap (Leather cover at the bottom third)
    grip_len = shaft_len * 0.35
    grip_z = 0.04 + (grip_len / 2.0)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=shaft_radius + 0.003,
        depth=grip_len,
        location=(0, 0, grip_z)
    )
    grip = bpy.context.active_object
    grip.name = "AxeGrip"
    utils.apply_smooth_by_angle(grip)
    utils.apply_material(grip, leather_mat)
    parts.append(grip)
    
    # 4. Bottom Cap
    cap_h = 0.03
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=shaft_radius + 0.006,
        depth=cap_h,
        location=(0, 0, cap_h / 2.0)
    )
    cap = bpy.context.active_object
    cap.name = "AxeCap"
    utils.apply_smooth_by_angle(cap)
    utils.apply_material(cap, head_mat)
    parts.append(cap)
    
    # 5. Socket (Metal bracket at the top of the shaft)
    socket_h = 0.12
    socket_z = shaft_len - 0.08
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, socket_z))
    socket = bpy.context.active_object
    socket.name = "AxeSocket"
    socket.scale = (shaft_radius * 2.6, shaft_radius * 2.6, socket_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(socket, width=0.003)
    utils.apply_material(socket, head_mat)
    parts.append(socket)
    
    # 6. Axe Blades
    blade_w = 0.16  # width extending out
    blade_h = 0.09  # height of center blade
    blade_thick = 0.008
    
    def create_blade(direction):
        # Direction is 1.0 (pointing right) or -1.0 (pointing left)
        blade_x = direction * (blade_w / 2.0 + shaft_radius)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(blade_x, 0, socket_z))
        blade = bpy.context.active_object
        blade.name = f"AxeBlade_{'R' if direction > 0 else 'L'}"
        
        # Scale to blade shape
        blade.scale = (blade_w, blade_thick, blade_h)
        bpy.ops.object.transform_apply(scale=True)
        
        # Deform to create a flared crescent edge
        for v in blade.data.vertices:
            # local coords: x ranges from -w/2 to w/2, z from -h/2 to h/2
            local_x = v.co.x
            local_z = v.co.z
            
            # Check if this vertex is towards the cutting edge
            is_edge = (direction > 0 and local_x > 0) or (direction < 0 and local_x < 0)
            
            if is_edge:
                # Flare cutting edge Z outwards
                v.co.z = local_z * 1.7
                # Taper Y to make it thin/sharp
                v.co.y = v.co.y * 0.15
                
        utils.apply_bevel(blade, width=0.002)
        utils.apply_material(blade, head_mat)
        return blade
        
    # Add right blade
    right_blade = create_blade(1.0)
    parts.append(right_blade)
    
    # Add left blade if double-headed
    if style == "double":
        left_blade = create_blade(-1.0)
        parts.append(left_blade)
        
    # Join all axe parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = shaft
    bpy.ops.object.join()
    
    shaft.name = "AxeAsset"
    # Place pivot point at bottom ground center (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return shaft

def main():
    parser = argparse.ArgumentParser(description="Procedural Axe Generator")
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
    axe_obj = generate_axe(params)
    
    if args.render:
        utils.setup_lighting_and_camera(axe_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
