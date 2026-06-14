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

def generate_picture_frame(params):
    w = params.get("width", 40.0) / 100.0  # cm to meters
    h = params.get("height", 50.0) / 100.0 # cm to meters
    border_t = params.get("border_thickness", 2.5) / 100.0 # cm to meters
    style = params.get("style", "modern")
    has_matting = params.get("has_matting", True)

    parts = []
    center_z = h / 2.0

    # 1. Create Materials
    if style == "classic":
        # Classic mahogany wood frame with gold inner trim
        frame_mat = utils.create_material("FrameWoodClassic", diffuse_color=(0.32, 0.12, 0.05, 1.0), metallic=0.0, roughness=0.55)
        trim_mat = utils.create_material("FrameGoldTrim", diffuse_color=(0.85, 0.65, 0.2, 1.0), metallic=0.85, roughness=0.25)
    else:
        # Modern matte black frame
        frame_mat = utils.create_material("FrameMetalModern", diffuse_color=(0.06, 0.06, 0.08, 1.0), metallic=0.75, roughness=0.3)
        trim_mat = frame_mat

    # Matting (passepartout) - light ivory
    mat_mat = utils.create_material("FrameMatting", diffuse_color=(0.94, 0.92, 0.87, 1.0), roughness=0.85)

    # Photo - Sepia/Grey portrait
    photo_mat = utils.create_material("FramePhoto", diffuse_color=(0.58, 0.48, 0.38, 1.0), roughness=0.5)

    # Glass front pane
    glass_mat = utils.create_material("FrameGlass", diffuse_color=(0.95, 0.98, 1.0, 0.2), metallic=0.0, roughness=0.02)
    glass_mat.blend_method = 'BLEND'

    # Backing board
    backing_mat = utils.create_material("FrameBacking", diffuse_color=(0.15, 0.12, 0.1, 1.0), roughness=0.9)

    # 2. Build Border Frame (4 segments)
    frame_d = 0.025  # 2.5cm deep frame border
    
    # Top border
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h - border_t / 2.0))
    top_b = bpy.context.active_object
    top_b.name = "FrameBorder_Top"
    top_b.scale = (w, frame_d, border_t)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(top_b, width=0.002)
    utils.apply_material(top_b, frame_mat)
    parts.append(top_b)

    # Bottom border
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, border_t / 2.0))
    bot_b = bpy.context.active_object
    bot_b.name = "FrameBorder_Bottom"
    bot_b.scale = (w, frame_d, border_t)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(bot_b, width=0.002)
    utils.apply_material(bot_b, frame_mat)
    parts.append(bot_b)

    # Left border
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-w / 2.0 + border_t / 2.0, 0, center_z))
    left_b = bpy.context.active_object
    left_b.name = "FrameBorder_Left"
    left_b.scale = (border_t, frame_d, h - 2.0 * border_t)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(left_b, width=0.002)
    utils.apply_material(left_b, frame_mat)
    parts.append(left_b)

    # Right border
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(w / 2.0 - border_t / 2.0, 0, center_z))
    right_b = bpy.context.active_object
    right_b.name = "FrameBorder_Right"
    right_b.scale = (border_t, frame_d, h - 2.0 * border_t)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(right_b, width=0.002)
    utils.apply_material(right_b, frame_mat)
    parts.append(right_b)

    # Inner Gold Trim (for Classic style)
    inner_w = w - 2.0 * border_t
    inner_h = h - 2.0 * border_t
    
    if style == "classic":
        trim_w = 0.006
        trim_d = 0.016
        trim_y = -frame_d / 2.0 + trim_d / 2.0 + 0.003
        
        # 4 thin trim strips
        for side, loc, sz in [
            ("Top", (0, trim_y, center_z + inner_h / 2.0 - trim_w / 2.0), (inner_w, trim_d, trim_w)),
            ("Bottom", (0, trim_y, center_z - inner_h / 2.0 + trim_w / 2.0), (inner_w, trim_d, trim_w)),
            ("Left", (-inner_w / 2.0 + trim_w / 2.0, trim_y, center_z), (trim_w, trim_d, inner_h - 2.0 * trim_w)),
            ("Right", (inner_w / 2.0 - trim_w / 2.0, trim_y, center_z), (trim_w, trim_d, inner_h - 2.0 * trim_w)),
        ]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
            trim = bpy.context.active_object
            trim.name = f"FrameTrim_{side}"
            trim.scale = sz
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(trim, width=0.001)
            utils.apply_material(trim, trim_mat)
            parts.append(trim)

    # 3. Backing Board
    backing_depth = 0.008
    backing_y = frame_d / 2.0 - backing_depth / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, backing_y, center_z))
    backing = bpy.context.active_object
    backing.name = "FrameBacking"
    backing.scale = (w - 0.006, backing_depth, h - 0.006)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(backing, backing_mat)
    parts.append(backing)

    # 4. Matting / Passepartout
    glass_depth = 0.004
    photo_w = inner_w
    photo_h = inner_h
    
    if has_matting:
        mat_border = min(inner_w, inner_h) * 0.16
        photo_w = inner_w - 2.0 * mat_border
        photo_h = inner_h - 2.0 * mat_border
        mat_depth = 0.004
        mat_y = backing_y - backing_depth / 2.0 - mat_depth / 2.0
        
        # Build matting as four borders within the frame inner cavity
        for side, loc, sz in [
            ("Top", (0, mat_y, center_z + inner_h / 2.0 - mat_border / 2.0), (inner_w - 0.002, mat_depth, mat_border)),
            ("Bottom", (0, mat_y, center_z - inner_h / 2.0 + mat_border / 2.0), (inner_w - 0.002, mat_depth, mat_border)),
            ("Left", (-inner_w / 2.0 + mat_border / 2.0, mat_y, center_z), (mat_border, mat_depth, inner_h - 2.0 * mat_border)),
            ("Right", (inner_w / 2.0 - mat_border / 2.0, mat_y, center_z), (mat_border, mat_depth, inner_h - 2.0 * mat_border)),
        ]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
            mat_obj = bpy.context.active_object
            mat_obj.name = f"FrameMatting_{side}"
            mat_obj.scale = sz
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(mat_obj, mat_mat)
            parts.append(mat_obj)

    # 5. Photo Inset Plane
    photo_y = backing_y - backing_depth / 2.0 - 0.001
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, photo_y, center_z))
    photo = bpy.context.active_object
    photo.name = "FramePhotoContent"
    photo.scale = (photo_w, 0.002, photo_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(photo, photo_mat)
    parts.append(photo)

    # 6. Glass Pane
    glass_y = -frame_d / 2.0 + glass_depth / 2.0 + 0.004
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, glass_y, center_z))
    glass = bpy.context.active_object
    glass.name = "FrameGlassFront"
    glass.scale = (inner_w - 0.002, glass_depth, inner_h - 0.002)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(glass, glass_mat)
    parts.append(glass)

    # 7. Easel Stand (Back support leg)
    # Add an easel back support leg if the frame height is small/medium (table size)
    if h < 0.6:
        leg_w = 0.025
        leg_thickness = 0.008
        leg_l = h * 0.72
        
        # Rotated slightly backwards at an angle (e.g. 18 degrees)
        leg_rot_x = math.radians(18.0)
        # Location offset to touch ground Z = 0
        leg_offset_y = math.sin(leg_rot_x) * (leg_l / 2.0)
        leg_center_z = (h * 0.6) - math.cos(leg_rot_x) * (leg_l / 2.0)
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, backing_y + backing_depth / 2.0 + leg_offset_y, leg_center_z))
        easel_leg = bpy.context.active_object
        easel_leg.name = "FrameEaselStand"
        easel_leg.scale = (leg_w, leg_thickness, leg_l)
        easel_leg.rotation_euler = (leg_rot_x, 0, 0)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        utils.apply_bevel(easel_leg, width=0.002)
        utils.apply_material(easel_leg, backing_mat)
        parts.append(easel_leg)

        # Small connecting hinge block at top of easel leg
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, backing_y + backing_depth / 2.0 + 0.004, h * 0.6))
        hinge = bpy.context.active_object
        hinge.name = "FrameEaselHinge"
        hinge.scale = (0.035, 0.008, 0.02)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(hinge, frame_mat)
        parts.append(hinge)

    # 8. Join components
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()

    # Rename asset and center origin to bottom center
    parts[0].name = "PictureFrameAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return parts[0]

def main():
    parser = argparse.ArgumentParser(description="Procedural Picture Frame Generator")
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
    frame_obj = generate_picture_frame(params)
    
    if args.render:
        utils.setup_lighting_and_camera(frame_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
