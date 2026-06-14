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

def generate_crate(params):
    w = params.get("width", 1.0)
    d = params.get("depth", 1.0)
    h = params.get("height", 1.0)
    
    parts = []
    
    # 1. Create Materials
    light_wood = utils.create_material("CrateInner", diffuse_color=(0.58, 0.45, 0.32, 1.0), metallic=0.0, roughness=0.8)
    dark_wood = utils.create_material("CrateFrame", diffuse_color=(0.35, 0.24, 0.15, 1.0), metallic=0.0, roughness=0.7)
    
    # 2. Inner Box Panel
    panel_inset = 0.05
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h / 2.0))
    inner_box = bpy.context.active_object
    inner_box.name = "InnerBox"
    inner_box.scale = (w - panel_inset, d - panel_inset, h - panel_inset)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(inner_box, width=0.005)
    utils.apply_material(inner_box, light_wood)
    parts.append(inner_box)
    
    # 3. Outer Frame Elements (Dark Wood)
    frame_w = 0.07  # width of the wooden beams
    frame_d = 0.02  # thickness of the beams
    
    # 3a. Vertical Corner Columns (4 columns)
    col_x = (w / 2.0) - (frame_w / 2.0)
    col_y = (d / 2.0) - (frame_w / 2.0)
    col_positions = [
        (-col_x, -col_y),
        (col_x, -col_y),
        (-col_x, col_y),
        (col_x, col_y)
    ]
    
    for idx, (cx, cy) in enumerate(col_positions):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, h / 2.0))
        col = bpy.context.active_object
        col.name = f"CornerCol_{idx}"
        col.scale = (frame_w, frame_w, h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(col, width=0.005)
        utils.apply_material(col, dark_wood)
        parts.append(col)
        
    # 3b. Horizontal Edge Beams (Top and Bottom, 4 on X-axis, 4 on Y-axis)
    # Z positions for top and bottom beams
    beam_z_pos = [frame_w / 2.0, h - (frame_w / 2.0)]
    
    for bz in beam_z_pos:
        # X-axis beams (Front and Back)
        y_positions = [-(d / 2.0) + (frame_w / 2.0), (d / 2.0) - (frame_w / 2.0)]
        for idx, by in enumerate(y_positions):
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, by, bz))
            beam = bpy.context.active_object
            beam.name = f"BeamX_{bz:.2f}_{idx}"
            beam.scale = (w, frame_w, frame_w)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(beam, width=0.005)
            utils.apply_material(beam, dark_wood)
            parts.append(beam)
            
        # Y-axis beams (Left and Right)
        x_positions = [-(w / 2.0) + (frame_w / 2.0), (w / 2.0) - (frame_w / 2.0)]
        for idx, bx in enumerate(x_positions):
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0, bz))
            beam = bpy.context.active_object
            beam.name = f"BeamY_{bz:.2f}_{idx}"
            beam.scale = (frame_w, d - (frame_w * 2.0), frame_w)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(beam, width=0.005)
            utils.apply_material(beam, dark_wood)
            parts.append(beam)
            
    # 3c. Diagonal Cross Bracing (Front and Back faces)
    # Calculate length and angle for diagonal beam
    diag_w = w - (frame_w * 2.0)
    diag_h = h - (frame_w * 2.0)
    diag_len = math.sqrt(diag_w**2 + diag_h**2)
    angle_y = math.atan2(diag_h, diag_w)
    
    # Front and Back Face Diagonal coordinates
    diag_y_pos = [-(d / 2.0) + (frame_d / 2.0), (d / 2.0) - (frame_d / 2.0)]
    for idx, dy in enumerate(diag_y_pos):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, dy, h / 2.0))
        diag = bpy.context.active_object
        diag.name = f"DiagFrontBack_{idx}"
        # Rotate diagonal (around Y-axis)
        # Flip sign for back face to cross in different direction if desired, or keep symmetric
        rotation_sign = 1.0 if idx == 0 else -1.0
        diag.rotation_euler = (0, rotation_sign * angle_y, 0)
        diag.scale = (diag_len, frame_w, frame_d)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(diag, width=0.003)
        utils.apply_material(diag, dark_wood)
        parts.append(diag)
        
    # Join all elements
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = inner_box
    bpy.ops.object.join()
    
    inner_box.name = "CrateAsset"
    # Place origin/pivot at ground level center (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return inner_box

def main():
    parser = argparse.ArgumentParser(description="Procedural Crate Generator")
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
    crate_obj = generate_crate(params)
    
    # Setup rendering and export
    if args.render:
        utils.setup_lighting_and_camera(crate_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
