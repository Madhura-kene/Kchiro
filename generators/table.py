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

def generate_table(params):
    # Extract params and convert cm to meters
    width = params.get("width", 120.0) / 100.0
    depth = params.get("depth", 80.0) / 100.0
    height = params.get("height", 75.0) / 100.0
    leg_style = params.get("leg_style", "square")
    
    parts = []
    
    # 1. Create wood material
    wood_mat = utils.create_material("TableWood", diffuse_color=(0.42, 0.26, 0.15, 1.0), metallic=0.0, roughness=0.6)
    
    # 2. Tabletop
    thickness = 0.04  # 4cm thickness
    tabletop_z = height - (thickness / 2.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, tabletop_z))
    tabletop = bpy.context.active_object
    tabletop.name = "Tabletop"
    tabletop.scale = (width, depth, thickness)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(tabletop, width=0.006)
    utils.apply_material(tabletop, wood_mat)
    parts.append(tabletop)
    
    # 3. Legs
    leg_h = height - thickness
    leg_z = leg_h / 2.0
    
    # Position legs slightly offset from tabletop edges
    inset = 0.08
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
            radius = 0.035
            bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=leg_h, location=(x, y, leg_z))
            leg = bpy.context.active_object
            leg.name = f"Leg_{idx}"
            utils.apply_smooth_by_angle(leg)
        else:  # square default
            size = 0.07
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, leg_z))
            leg = bpy.context.active_object
            leg.name = f"Leg_{idx}"
            leg.scale = (size, size, leg_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(leg, width=0.005)
            
        utils.apply_material(leg, wood_mat)
        parts.append(leg)
        
    # Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = tabletop
    bpy.ops.object.join()
    
    tabletop.name = "TableAsset"
    # Place origin/pivot at ground level center (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return tabletop

def main():
    parser = argparse.ArgumentParser(description="Procedural Table Generator")
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
    table_obj = generate_table(params)
    
    # Setup rendering and export
    if args.render:
        utils.setup_lighting_and_camera(table_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
