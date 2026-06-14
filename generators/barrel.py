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

def generate_barrel(params):
    radius = params.get("radius", 0.4)
    height = params.get("height", 1.0)
    
    parts = []
    
    # 1. Create Materials
    wood_mat = utils.create_material("BarrelWood", diffuse_color=(0.33, 0.20, 0.11, 1.0), metallic=0.0, roughness=0.75)
    hoop_mat = utils.create_material("HoopIron", diffuse_color=(0.20, 0.20, 0.20, 1.0), metallic=0.85, roughness=0.4)
    
    # 2. Barrel Body (Bulging Cylinder)
    # Start with a cylinder centered at Z = height/2
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=radius, depth=height, location=(0, 0, height / 2.0))
    body = bpy.context.active_object
    body.name = "BarrelBody"
    utils.apply_smooth_by_angle(body, angle=40.0)
    
    # Modify vertices to create a bulge in the middle
    # Local Z ranges from -height/2 to height/2
    half_h = height / 2.0
    for v in body.data.vertices:
        # local z coordinate
        local_z = v.co.z
        # Normalized z from -1.0 (bottom) to 1.0 (top)
        nz = local_z / half_h
        # Parabolic bulge formula: radius factor peaks at 1.15 in the center (nz = 0)
        bulge_factor = 1.0 + 0.16 * (1.0 - nz**2)
        v.co.x *= bulge_factor
        v.co.y *= bulge_factor
        
    utils.apply_material(body, wood_mat)
    parts.append(body)
    
    # 3. Add Iron Hoops (Metals bands)
    # We place two hoops: one at 25% height, one at 75% height
    hoop_positions_z = [height * 0.22, height * 0.78]
    hoop_thickness = 0.012  # thickness extending outward from barrel
    hoop_height = 0.04      # height of the metal band
    
    for idx, hz in enumerate(hoop_positions_z):
        # Calculate local barrel radius at this height to match the bulge
        local_z = hz - half_h
        nz = local_z / half_h
        local_radius = radius * (1.0 + 0.16 * (1.0 - nz**2))
        
        # Create a cylinder representing the hoop, slightly larger than the barrel radius
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=24, 
            radius=local_radius + hoop_thickness, 
            depth=hoop_height, 
            location=(0, 0, hz)
        )
        hoop = bpy.context.active_object
        hoop.name = f"IronHoop_{idx}"
        utils.apply_smooth_by_angle(hoop, angle=40.0)
        utils.apply_bevel(hoop, width=0.002)
        
        utils.apply_material(hoop, hoop_mat)
        parts.append(hoop)
        
    # Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    
    body.name = "BarrelAsset"
    # Place origin/pivot at ground level center (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return body

def main():
    parser = argparse.ArgumentParser(description="Procedural Barrel Generator")
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
    barrel_obj = generate_barrel(params)
    
    # Setup rendering and export
    if args.render:
        utils.setup_lighting_and_camera(barrel_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
