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

def generate_painting(params):
    w = params.get("width", 80.0) / 100.0  # cm to meters
    h = params.get("height", 60.0) / 100.0 # cm to meters
    frame_w = params.get("frame_width", 3.0) / 100.0  # cm to meters
    style = params.get("style", "landscape")
    art_type = params.get("art_type", "abstract")

    parts = []

    # Adjust width and height based on style orientation if needed
    if style == "portrait" and w > h:
        w, h = h, w
    elif style == "landscape" and h > w:
        w, h = h, w
    elif style == "square":
        # Average them out
        avg = (w + h) / 2.0
        w, h = avg, avg

    # 1. Create Materials
    # Frame material: Rich Walnut Wood
    frame_mat = utils.create_material("PaintingFrameWood", diffuse_color=(0.28, 0.16, 0.08, 1.0), metallic=0.0, roughness=0.65)
    
    # Canvas material: Textured off-white fabric
    canvas_mat = utils.create_material("PaintingCanvas", diffuse_color=(0.95, 0.94, 0.9, 1.0), metallic=0.0, roughness=0.95)

    # Artwork paint materials
    terracotta_mat = utils.create_material("ArtTerracotta", diffuse_color=(0.75, 0.35, 0.22, 1.0), roughness=0.6)
    teal_mat = utils.create_material("ArtTeal", diffuse_color=(0.1, 0.32, 0.3, 1.0), roughness=0.5)
    gold_mat = utils.create_material("ArtGoldLacquer", diffuse_color=(0.85, 0.65, 0.18, 1.0), metallic=0.7, roughness=0.25)
    charcoal_mat = utils.create_material("ArtCharcoal", diffuse_color=(0.08, 0.08, 0.1, 1.0), roughness=0.455)
    cream_mat = utils.create_material("ArtCream", diffuse_color=(0.92, 0.88, 0.82, 1.0), roughness=0.7)

    # 2. Build Outer Frame
    # We will build it from 4 bordering box segments (Top, Bottom, Left, Right)
    frame_depth = 0.035  # 3.5cm frame depth
    center_z = h / 2.0

    # Top border
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h - frame_w / 2.0))
    top_b = bpy.context.active_object
    top_b.name = "Frame_Top"
    top_b.scale = (w, frame_depth, frame_w)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(top_b, width=0.002)
    utils.apply_material(top_b, frame_mat)
    parts.append(top_b)

    # Bottom border
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, frame_w / 2.0))
    bot_b = bpy.context.active_object
    bot_b.name = "Frame_Bottom"
    bot_b.scale = (w, frame_depth, frame_w)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(bot_b, width=0.002)
    utils.apply_material(bot_b, frame_mat)
    parts.append(bot_b)

    # Left border
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-w / 2.0 + frame_w / 2.0, 0, center_z))
    left_b = bpy.context.active_object
    left_b.name = "Frame_Left"
    left_b.scale = (frame_w, frame_depth, h - 2.0 * frame_w)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(left_b, width=0.002)
    utils.apply_material(left_b, frame_mat)
    parts.append(left_b)

    # Right border
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(w / 2.0 - frame_w / 2.0, 0, center_z))
    right_b = bpy.context.active_object
    right_b.name = "Frame_Right"
    right_b.scale = (frame_w, frame_depth, h - 2.0 * frame_w)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(right_b, width=0.002)
    utils.apply_material(right_b, frame_mat)
    parts.append(right_b)

    # 3. Canvas (Inset plate)
    canvas_w = w - 2.0 * frame_w
    canvas_h = h - 2.0 * frame_w
    canvas_depth = 0.012
    # Recessed slightly: place front face of canvas 1cm back from the frame front face
    canvas_y = -frame_depth / 2.0 + canvas_depth / 2.0 + 0.008

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, canvas_y, center_z))
    canvas = bpy.context.active_object
    canvas.name = "CanvasPlate"
    canvas.scale = (canvas_w, canvas_depth, canvas_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(canvas, canvas_mat)
    parts.append(canvas)

    # 4. Generate Abstract Painted Artwork Elements on Canvas Face
    # Place layers at slightly increasing Y positions (moving towards camera)
    art_y_base = canvas_y + canvas_depth / 2.0 + 0.001
    
    # Backdrop shapes: large cream arch/rectangle on the left
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-canvas_w * 0.18, art_y_base, center_z - canvas_h * 0.05))
    rect_art = bpy.context.active_object
    rect_art.name = "ArtShape_BackgroundRect"
    rect_art.scale = (canvas_w * 0.38, 0.001, canvas_h * 0.6)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(rect_art, cream_mat)
    parts.append(rect_art)

    # Large Terracotta Circle/Half-sun in the middle
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=canvas_h * 0.28,
        depth=0.001,
        location=(canvas_w * 0.12, art_y_base + 0.0005, center_z + canvas_h * 0.12),
        rotation=(math.pi / 2.0, 0, 0)
    )
    sun_art = bpy.context.active_object
    sun_art.name = "ArtShape_Sun"
    utils.apply_smooth_by_angle(sun_art, angle=30.0)
    utils.apply_material(sun_art, terracotta_mat)
    parts.append(sun_art)

    # Teal sweeping block / ribbon
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(canvas_w * 0.05, art_y_base + 0.001, center_z - canvas_h * 0.2))
    ribbon_art = bpy.context.active_object
    ribbon_art.name = "ArtShape_Ribbon"
    ribbon_art.scale = (canvas_w * 0.55, 0.001, canvas_h * 0.18)
    # Rotate ribbon slightly
    ribbon_art.rotation_euler = (0, 0, math.radians(-12.0))
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    utils.apply_material(ribbon_art, teal_mat)
    parts.append(ribbon_art)

    # Gold metallic accent circle
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=canvas_h * 0.12,
        depth=0.001,
        location=(-canvas_w * 0.15, art_y_base + 0.0015, center_z + canvas_h * 0.18),
        rotation=(math.pi / 2.0, 0, 0)
    )
    gold_art = bpy.context.active_object
    gold_art.name = "ArtShape_GoldDot"
    utils.apply_smooth_by_angle(gold_art, angle=30.0)
    utils.apply_material(gold_art, gold_mat)
    parts.append(gold_art)

    # Charcoal thin line/bars
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-canvas_w * 0.08, art_y_base + 0.002, center_z + canvas_h * 0.05))
    bar_art = bpy.context.active_object
    bar_art.name = "ArtShape_LineBar"
    bar_art.scale = (0.015, 0.001, canvas_h * 0.72)
    # Tilt the bar slightly
    bar_art.rotation_euler = (0, 0, math.radians(15.0))
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    utils.apply_material(bar_art, charcoal_mat)
    parts.append(bar_art)

    # 5. Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()

    # Rename asset and center origin to bottom center
    parts[0].name = "PaintingAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return parts[0]

def main():
    parser = argparse.ArgumentParser(description="Procedural Painting Generator")
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
    painting_obj = generate_painting(params)
    
    if args.render:
        utils.setup_lighting_and_camera(painting_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
