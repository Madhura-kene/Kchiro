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

def generate_shower(params):
    w = params.get("width", 90.0) / 100.0  # cm to meters
    d = params.get("depth", 90.0) / 100.0
    h = params.get("height", 210.0) / 100.0
    enclosure = params.get("enclosure", "glass_door")
    head_type = params.get("head_type", "standard")
    fixture_material = params.get("material", "chrome")

    parts = []

    # 1. Setup Materials
    # Base Pan / Tile wall
    base_color = (0.9, 0.92, 0.95, 1.0) # light tiled look
    base_mat = utils.create_material("ShowerBase", diffuse_color=base_color, metallic=0.0, roughness=0.3)
    wall_mat = utils.create_material("ShowerWall", diffuse_color=(0.85, 0.85, 0.85, 1.0), metallic=0.0, roughness=0.4)

    # Fixtures
    if fixture_material == "brass":
        fix_color = (0.75, 0.60, 0.20, 1.0)
        fix_metal = 0.9
        fix_rough = 0.2
    elif fixture_material == "matte_black":
        fix_color = (0.1, 0.1, 0.1, 1.0)
        fix_metal = 0.1
        fix_rough = 0.8
    else: # chrome
        fix_color = (0.85, 0.85, 0.85, 1.0)
        fix_metal = 0.95
        fix_rough = 0.05

    fix_mat = utils.create_material("ShowerFixture", diffuse_color=fix_color, metallic=fix_metal, roughness=fix_rough)
    glass_mat = utils.create_material("ShowerGlass", diffuse_color=(0.85, 0.95, 0.95, 0.15), metallic=0.0, roughness=0.05)
    curtain_mat = utils.create_material("ShowerCurtain", diffuse_color=(0.95, 0.92, 0.88, 1.0), metallic=0.0, roughness=0.9)

    # ── FLOOR PAN BASE ──────────────────────────────────────────────────────
    pan_h = 0.06
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, pan_h / 2.0))
    pan = bpy.context.active_object
    pan.name = "ShowerPan"
    pan.scale = (w, d, pan_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(pan, width=0.005)
    utils.apply_material(pan, base_mat)
    parts.append(pan)

    # Floor drain plate (small cylinder centered)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.002, location=(0, 0, pan_h + 0.001))
    drain = bpy.context.active_object
    drain.name = "ShowerDrain"
    utils.apply_smooth_by_angle(drain)
    utils.apply_material(drain, fix_mat)
    parts.append(drain)

    # ── CORNER TILED WALLS ──────────────────────────────────────────────────
    # Back wall (along positive Y)
    wall_thick = 0.03
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, d/2.0 - wall_thick/2.0, h/2.0))
    back_wall = bpy.context.active_object
    back_wall.name = "ShowerBackWall"
    back_wall.scale = (w, wall_thick, h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(back_wall, wall_mat)
    parts.append(back_wall)

    # Left wall (along negative X)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-w/2.0 + wall_thick/2.0, 0, h/2.0))
    left_wall = bpy.context.active_object
    left_wall.name = "ShowerLeftWall"
    left_wall.scale = (wall_thick, d - wall_thick, h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(left_wall, wall_mat)
    parts.append(left_wall)

    # ── SHOWER FIXTURES ─────────────────────────────────────────────────────
    # Placed on the left wall facing positive X
    fixture_x = -w/2.0 + wall_thick + 0.02
    fixture_y = 0.0
    
    # Shower column pipe
    pipe_h = 1.30
    pipe_z = 0.8 + pipe_h / 2.0
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=pipe_h, location=(fixture_x, fixture_y, pipe_z))
    pipe = bpy.context.active_object
    pipe.name = "ShowerPipe"
    utils.apply_smooth_by_angle(pipe)
    utils.apply_material(pipe, fix_mat)
    parts.append(pipe)

    # Shower knobs/controls
    knob_z = 1.0
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.02, location=(fixture_x + 0.01, fixture_y, knob_z))
    control_valve = bpy.context.active_object
    control_valve.name = "ShowerValve"
    control_valve.rotation_euler = (0, math.radians(90.0), 0)
    utils.apply_smooth_by_angle(control_valve)
    utils.apply_material(control_valve, fix_mat)
    parts.append(control_valve)

    # Knob handle lever
    bpy.ops.mesh.primitive_cylinder_add(radius=0.006, depth=0.08, location=(fixture_x + 0.025, fixture_y, knob_z + 0.03))
    lever = bpy.context.active_object
    lever.name = "ShowerLever"
    utils.apply_smooth_by_angle(lever)
    utils.apply_material(lever, fix_mat)
    parts.append(lever)

    # Top shower arm (horizontal pipe extending out)
    arm_len = 0.25
    arm_x = fixture_x + arm_len / 2.0
    arm_z = 2.05
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=arm_len, location=(arm_x, fixture_y, arm_z))
    arm = bpy.context.active_object
    arm.name = "ShowerArm"
    arm.rotation_euler = (0, math.radians(90.0), 0)
    utils.apply_smooth_by_angle(arm)
    utils.apply_material(arm, fix_mat)
    parts.append(arm)

    # Shower Head
    head_x = fixture_x + arm_len
    if head_type == "rain":
        # Large flat rain showerhead disk
        bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=0.015, location=(head_x, fixture_y, arm_z - 0.02))
        head = bpy.context.active_object
        head.name = "ShowerHeadRain"
        utils.apply_smooth_by_angle(head)
        utils.apply_material(head, fix_mat)
        parts.append(head)
    elif head_type == "handheld":
        # Handheld wand bracket and hose
        # Bracket
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(fixture_x + 0.015, fixture_y, 1.4))
        bracket = bpy.context.active_object
        bracket.name = "HoseBracket"
        bracket.scale = (0.03, 0.03, 0.04)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(bracket, fix_mat)
        parts.append(bracket)

        # Handheld Wand
        bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.15, location=(fixture_x + 0.035, fixture_y, 1.45))
        wand = bpy.context.active_object
        wand.name = "ShowerWand"
        wand.rotation_euler = (0, math.radians(-15.0), 0)
        utils.apply_smooth_by_angle(wand)
        utils.apply_material(wand, fix_mat)
        parts.append(wand)
    else: # standard
        # Standard cone showerhead
        bpy.ops.mesh.primitive_cone_add(radius1=0.012, radius2=0.04, depth=0.06, location=(head_x, fixture_y, arm_z - 0.03))
        head = bpy.context.active_object
        head.name = "ShowerHeadStandard"
        head.rotation_euler = (0, math.radians(15.0), 0)
        utils.apply_smooth_by_angle(head)
        utils.apply_material(head, fix_mat)
        parts.append(head)

    # ── ENCLOSURE (GLASS OR CURTAIN) ────────────────────────────────────────
    if enclosure == "glass_door":
        # Glass wall partition on the side (along positive X)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(w/2.0 - 0.01, 0, h/2.0))
        glass_side = bpy.context.active_object
        glass_side.name = "ShowerGlassSide"
        glass_side.scale = (0.015, d - 0.02, h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(glass_side, glass_mat)
        parts.append(glass_side)

        # Glass panel door in front (along negative Y)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -d/2.0 + 0.01, h/2.0))
        glass_front = bpy.context.active_object
        glass_front.name = "ShowerGlassFront"
        glass_front.scale = (w - 0.02, 0.015, h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(glass_front, glass_mat)
        parts.append(glass_front)

        # Metallic support frame on top
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h - 0.02))
        top_frame = bpy.context.active_object
        top_frame.name = "ShowerGlassFrame"
        top_frame.scale = (w, d, 0.03)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(top_frame, width=0.003)
        utils.apply_material(top_frame, fix_mat)
        parts.append(top_frame)

    elif enclosure == "curtain":
        # Rod at the top (curving or straight)
        rod_z = h - 0.10
        bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=w, location=(0, -d/2.0 + 0.05, rod_z))
        rod = bpy.context.active_object
        rod.name = "CurtainRod"
        rod.rotation_euler = (0, math.radians(90.0), 0)
        utils.apply_smooth_by_angle(rod)
        utils.apply_material(rod, fix_mat)
        parts.append(rod)

        # Folded curtain sheet
        curt_h = rod_z - pan_h
        curt_z = pan_h + curt_h / 2.0
        
        # We can model a corrugated curtain using a thin box
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -d/2.0 + 0.05, curt_z))
        curtain = bpy.context.active_object
        curtain.name = "ShowerCurtainFabric"
        curtain.scale = (w - 0.02, 0.03, curt_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(curtain, width=0.01)
        utils.apply_material(curtain, curtain_mat)
        parts.append(curtain)

    # ── Join all parts ────────────────────────────────────────────────────────
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = pan
    bpy.ops.object.join()
    
    pan.name = "ShowerAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    return pan

def main():
    parser = argparse.ArgumentParser(description="Procedural Shower Generator")
    parser.add_argument("--params", type=str, required=True)
    parser.add_argument("--export", type=str, required=True)
    parser.add_argument("--render", type=str)

    try:
        args_idx = sys.argv.index("--")
        script_args = sys.argv[args_idx + 1:]
    except ValueError:
        script_args = []

    args = parser.parse_args(script_args)

    with open(args.params, 'r') as f:
        params = json.load(f)

    utils.cleanup_scene()
    obj = generate_shower(params)

    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
