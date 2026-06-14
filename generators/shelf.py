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

def generate_shelf(params):
    w = params.get("width", 80.0) / 100.0  # convert cm to meters
    d = params.get("depth", 25.0) / 100.0
    h = params.get("height", 20.0) / 100.0
    material_type = params.get("material", "wood")
    brackets_style = params.get("brackets", "floating")

    parts = []

    # 1. Setup Materials
    if material_type == "glass":
        board_color = (0.8, 0.95, 0.95, 0.2)
        metallic_board = 0.0
        rough_board = 0.05
        board_thick = 0.012  # Glass is thinner
        board_mat = utils.create_material("ShelfGlassBoard", diffuse_color=board_color, metallic=metallic_board, roughness=rough_board)
    elif material_type == "metal":
        board_color = (0.2, 0.2, 0.2, 1.0) # Dark steel
        metallic_board = 0.8
        rough_board = 0.4
        board_thick = 0.02
        board_mat = utils.create_material("ShelfMetalBoard", diffuse_color=board_color, metallic=metallic_board, roughness=rough_board)
    else: # wood
        board_color = (0.55, 0.38, 0.24, 1.0) # Nice Oak wood
        metallic_board = 0.0
        rough_board = 0.65
        board_thick = 0.03
        board_mat = utils.create_material("ShelfWoodBoard", diffuse_color=board_color, metallic=metallic_board, roughness=rough_board)

    # Brackets material (dark metal or brass)
    bracket_mat = utils.create_material("ShelfBracketMetal", diffuse_color=(0.1, 0.1, 0.1, 1.0), metallic=0.8, roughness=0.35)

    # 2. Add Main Board
    # Place board near the top of the height boundary
    board_z = h - (board_thick / 2.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, board_z))
    board = bpy.context.active_object
    board.name = "ShelfBoard"
    board.scale = (w, d, board_thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(board, width=0.003 if material_type != "glass" else 0.001)
    utils.apply_material(board, board_mat)
    parts.append(board)

    # 3. Add Brackets
    if brackets_style == "floating":
        # Hidden brackets/pins extending from wall (back of shelf is Y = d/2)
        pin_radius = 0.008
        pin_len = d * 0.7
        pin_z = board_z
        # Let's add 2 pins for standard, or 3 if very wide
        x_offsets = [-w / 3.0, w / 3.0]
        if w > 1.2:
            x_offsets = [-w / 3.0, 0.0, w / 3.0]
            
        for x in x_offsets:
            # Anchor pins at back wall, extending into the board
            bpy.ops.mesh.primitive_cylinder_add(
                radius=pin_radius,
                depth=pin_len,
                location=(x, d / 2.0 - pin_len / 2.0, pin_z)
            )
            pin = bpy.context.active_object
            pin.name = f"ShelfFloatingPin_{x}"
            pin.rotation_euler = (math.pi / 2.0, 0.0, 0.0) # Rotated to point forward (along Y)
            bpy.ops.object.transform_apply(rotation=True)
            utils.apply_smooth_by_angle(pin, angle=30.0)
            utils.apply_material(pin, bracket_mat)
            parts.append(pin)

    elif brackets_style == "industrial":
        # Two industrial L-pipe brackets under the shelf
        bracket_x = w / 3.0
        for side in [-1.0, 1.0]:
            bx = side * bracket_x
            
            # Wall flange (attachment plate) at Y = d/2
            flange_radius = 0.03
            flange_thick = 0.006
            flange_z = h / 2.0
            bpy.ops.mesh.primitive_cylinder_add(
                radius=flange_radius,
                depth=flange_thick,
                location=(bx, d / 2.0 - flange_thick / 2.0, flange_z)
            )
            flange = bpy.context.active_object
            flange.name = f"ShelfFlange_{'L' if side < 0 else 'R'}"
            flange.rotation_euler = (math.pi / 2.0, 0.0, 0.0)
            bpy.ops.object.transform_apply(rotation=True)
            utils.apply_smooth_by_angle(flange, angle=30.0)
            utils.apply_material(flange, bracket_mat)
            parts.append(flange)

            # L-Pipe: Horizontal support bar directly under the board
            # from Y = d/2 to Y = -d/2 + 0.02
            pipe_rad = 0.01
            hbar_len = d - 0.03
            hbar_y = d / 2.0 - hbar_len / 2.0 - 0.01
            hbar_z = board_z - board_thick / 2.0 - pipe_rad
            bpy.ops.mesh.primitive_cylinder_add(
                radius=pipe_rad,
                depth=hbar_len,
                location=(bx, hbar_y, hbar_z)
            )
            hbar = bpy.context.active_object
            hbar.name = f"ShelfPipeH_{'L' if side < 0 else 'R'}"
            hbar.rotation_euler = (math.pi / 2.0, 0.0, 0.0)
            bpy.ops.object.transform_apply(rotation=True)
            utils.apply_smooth_by_angle(hbar, angle=30.0)
            utils.apply_material(hbar, bracket_mat)
            parts.append(hbar)

            # L-Pipe: Vertical support bar down to flange
            vbar_h = hbar_z - flange_z
            vbar_z = flange_z + vbar_h / 2.0
            vbar_y = d / 2.0 - 0.02
            bpy.ops.mesh.primitive_cylinder_add(
                radius=pipe_rad,
                depth=vbar_h,
                location=(bx, vbar_y, vbar_z)
            )
            vbar = bpy.context.active_object
            vbar.name = f"ShelfPipeV_{'L' if side < 0 else 'R'}"
            utils.apply_smooth_by_angle(vbar, angle=30.0)
            utils.apply_material(vbar, bracket_mat)
            parts.append(vbar)

    # 4. Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = board
    bpy.ops.object.join()

    board.name = "ShelfAsset"
    # Ensure local origin is at (0, 0, 0) of the scene for placement logic
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return board

def main():
    parser = argparse.ArgumentParser(description="Procedural Shelf Generator")
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
    shelf_obj = generate_shelf(params)
    
    if args.render:
        utils.setup_lighting_and_camera(shelf_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
