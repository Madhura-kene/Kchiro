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

def generate_bench(params):
    w = params.get("width", 120.0) / 100.0  # convert cm to meters
    d = params.get("depth", 40.0) / 100.0
    h = params.get("height", 45.0) / 100.0
    has_backrest = params.get("has_backrest", False)
    leg_style = params.get("leg_style", "straight")
    material = params.get("material", "wood")

    parts = []

    # 1. Create Materials
    wood_mat = utils.create_material("BenchWood", diffuse_color=(0.35, 0.22, 0.12, 1.0), metallic=0.0, roughness=0.7)
    metal_mat = utils.create_material("BenchMetal", diffuse_color=(0.15, 0.15, 0.15, 1.0), metallic=0.9, roughness=0.25)
    cushion_mat = utils.create_material("BenchCushion", diffuse_color=(0.55, 0.5, 0.45, 1.0), metallic=0.0, roughness=0.85)

    # 2. Seat Panel
    thickness = 0.04  # 4cm thickness
    seat_z = h - (thickness / 2.0)
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, seat_z))
    seat = bpy.context.active_object
    seat.name = "BenchSeat"
    seat.scale = (w, d, thickness)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(seat, width=0.006)
    
    if material == "cushioned":
        utils.apply_material(seat, cushion_mat)
    else:
        utils.apply_material(seat, wood_mat)
    parts.append(seat)

    # 3. Leg Supports
    leg_h = h - thickness
    leg_z = leg_h / 2.0
    inset = 0.08
    pos_x = (w / 2.0) - inset

    # Define leg material
    leg_mat = metal_mat if material == "metal" else wood_mat

    if leg_style == "x_frame":
        # Create X-frame legs on left and right sides
        for lx in [-pos_x, pos_x]:
            # X leg 1 (forward-slash style)
            angle = math.atan(d / leg_h)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, 0, leg_z))
            x1 = bpy.context.active_object
            x1.name = f"LegX1_{'L' if lx < 0 else 'R'}"
            x1.scale = (0.04, 0.04, leg_h * 1.1)
            x1.rotation_euler = (angle, 0, 0)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            utils.apply_bevel(x1, width=0.003)
            utils.apply_material(x1, leg_mat)
            parts.append(x1)

            # X leg 2 (backslash style)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, 0, leg_z))
            x2 = bpy.context.active_object
            x2.name = f"LegX2_{'L' if lx < 0 else 'R'}"
            x2.scale = (0.04, 0.04, leg_h * 1.1)
            x2.rotation_euler = (-angle, 0, 0)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            utils.apply_bevel(x2, width=0.003)
            utils.apply_material(x2, leg_mat)
            parts.append(x2)
            
            # Bottom horizontal connector runner
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, 0, 0.02))
            runner = bpy.context.active_object
            runner.name = f"LegRunner_{'L' if lx < 0 else 'R'}"
            runner.scale = (0.04, d - 0.04, 0.03)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(runner, width=0.003)
            utils.apply_material(runner, leg_mat)
            parts.append(runner)
            
        # Add a center support beam connecting the two X-frames
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, leg_z))
        beam = bpy.context.active_object
        beam.name = "LegCenterBeam"
        beam.scale = (w - 2.0 * inset - 0.04, 0.04, 0.04)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(beam, width=0.003)
        utils.apply_material(beam, leg_mat)
        parts.append(beam)

    else:  # straight legs
        # Four vertical corner posts
        pos_y = (d / 2.0) - inset
        leg_positions = [
            (-pos_x, -pos_y),
            (pos_x, -pos_y),
            (-pos_x, pos_y),
            (pos_x, pos_y)
        ]
        leg_size = 0.045
        
        for idx, (x, y) in enumerate(leg_positions):
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, leg_z))
            leg = bpy.context.active_object
            leg.name = f"Leg_{idx}"
            leg.scale = (leg_size, leg_size, leg_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(leg, width=0.004)
            utils.apply_material(leg, leg_mat)
            parts.append(leg)

        # Runner beams underneath seat for straight wood legs
        if material != "metal":
            for side_x in [-pos_x, pos_x]:
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, 0, h - thickness - 0.02))
                run_y = bpy.context.active_object
                run_y.name = f"SideRunner_{'L' if side_x < 0 else 'R'}"
                run_y.scale = (leg_size, d - inset * 2.0, 0.04)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(run_y, width=0.003)
                utils.apply_material(run_y, leg_mat)
                parts.append(run_y)
                
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h - thickness - 0.02))
            run_x = bpy.context.active_object
            run_x.name = "LongRunner"
            run_x.scale = (w - inset * 2.0, leg_size, 0.04)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(run_x, width=0.003)
            utils.apply_material(run_x, leg_mat)
            parts.append(run_x)

    # 4. Optional Backrest
    if has_backrest:
        back_h = 0.35  # height of backrest above seat
        back_thick = 0.03
        back_z = h + (back_h / 2.0)
        back_y = (d / 2.0) - (back_thick / 2.0)
        
        # Two vertical support posts at the back
        post_size = 0.035
        for px in [-pos_x, pos_x]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, back_y, h + back_h / 3.0))
            post = bpy.context.active_object
            post.name = f"BackPost_{'L' if px < 0 else 'R'}"
            post.scale = (post_size, post_size, back_h * 1.2)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(post, width=0.003)
            utils.apply_material(post, leg_mat)
            parts.append(post)
            
        # Horizontal backrest board
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, back_y, h + back_h - 0.08))
        board = bpy.context.active_object
        board.name = "BackBoard"
        board.scale = (w - 0.1, back_thick, 0.15)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(board, width=0.004)
        
        if material == "cushioned":
            utils.apply_material(board, cushion_mat)
        else:
            utils.apply_material(board, wood_mat)
        parts.append(board)

    # Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = seat
    bpy.ops.object.join()
    
    seat.name = "BenchAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return seat

def main():
    parser = argparse.ArgumentParser(description="Procedural Bench Generator")
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
    bench_obj = generate_bench(params)
    
    if args.render:
        utils.setup_lighting_and_camera(bench_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
