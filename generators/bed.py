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

def generate_bed(params):
    w = params.get("width", 160.0) / 100.0  # convert cm to meters
    d = params.get("depth", 200.0) / 100.0  # bed length
    h = params.get("height", 60.0) / 100.0   # height of mattress top
    has_headboard = params.get("has_headboard", True)
    material = params.get("material", "wood")

    parts = []

    # 1. Create Materials
    wood_mat = utils.create_material("BedWood", diffuse_color=(0.32, 0.18, 0.08, 1.0), metallic=0.0, roughness=0.7)
    metal_mat = utils.create_material("BedMetal", diffuse_color=(0.12, 0.12, 0.12, 1.0), metallic=0.9, roughness=0.3)
    sheet_mat = utils.create_material("BedSheets", diffuse_color=(0.85, 0.85, 0.85, 1.0), metallic=0.0, roughness=0.9)
    blanket_mat = utils.create_material("BedBlanket", diffuse_color=(0.48, 0.15, 0.18, 1.0), metallic=0.0, roughness=0.85) # Crimson red

    frame_mat = wood_mat if material == "wood" else (metal_mat if material == "metal" else blanket_mat)

    # Dimensions
    leg_h = 0.18
    frame_h = 0.22
    mattress_h = 0.25
    headboard_h = 1.1

    # 2. Add Corner Legs
    leg_w = 0.06
    inset_x = (w / 2.0) - leg_w/2.0
    inset_y = (d / 2.0) - leg_w/2.0
    
    for lx in [-inset_x, inset_x]:
        for ly in [-inset_y, inset_y]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, leg_h / 2.0))
            leg = bpy.context.active_object
            leg.name = f"BedLeg_{lx}_{ly}"
            leg.scale = (leg_w, leg_w, leg_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(leg, width=0.005)
            utils.apply_material(leg, frame_mat)
            parts.append(leg)

    # 3. Bed Frame Box
    frame_z = leg_h + (frame_h / 2.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, frame_z))
    frame = bpy.context.active_object
    frame.name = "BedFrame"
    frame.scale = (w, d, frame_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(frame, width=0.01)
    utils.apply_material(frame, frame_mat)
    parts.append(frame)

    # 4. Headboard
    if has_headboard:
        hb_thick = 0.08
        hb_y = (d / 2.0) - (hb_thick / 2.0)
        hb_z = leg_h + (headboard_h / 2.0)
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, hb_y, hb_z))
        hb = bpy.context.active_object
        hb.name = "BedHeadboard"
        hb.scale = (w + 0.04, hb_thick, headboard_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(hb, width=0.015)
        utils.apply_material(hb, frame_mat)
        parts.append(hb)

    # 5. Mattress
    mattress_z = leg_h + frame_h + (mattress_h / 2.0) - 0.05 # slightly inset
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.02, mattress_z))
    mattress = bpy.context.active_object
    mattress.name = "BedMattress"
    mattress.scale = (w - 0.04, d - 0.08, mattress_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(mattress, width=0.025)
    utils.apply_material(mattress, sheet_mat)
    parts.append(mattress)

    # 6. Pillows
    pillow_w = 0.50
    pillow_d = 0.35
    pillow_h = 0.10
    pillow_z = mattress_z + (mattress_h / 2.0) + 0.02
    pillow_y = (d / 2.0) - 0.30

    if w > 1.2:
        # Two pillows
        pillow_positions = [-w/4.0, w/4.0]
    else:
        # One pillow
        pillow_positions = [0.0]

    for px in pillow_positions:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, pillow_y, pillow_z))
        pillow = bpy.context.active_object
        pillow.name = f"BedPillow_{px}"
        pillow.scale = (pillow_w, pillow_d, pillow_h)
        # Slant pillow slightly back
        pillow.rotation_euler = (0.15, 0, 0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_bevel(pillow, width=0.02)
        utils.apply_material(pillow, sheet_mat)
        parts.append(pillow)

    # 7. Folded Blanket/Duvet at the foot end
    blanket_d = d * 0.55
    blanket_y = -d/2.0 + blanket_d/2.0 + 0.04
    blanket_z = mattress_z + (mattress_h / 2.0) + 0.01
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, blanket_y, blanket_z))
    blanket = bpy.context.active_object
    blanket.name = "BedBlanketSheet"
    blanket.scale = (w - 0.02, blanket_d, 0.03)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(blanket, width=0.008)
    utils.apply_material(blanket, blanket_mat)
    parts.append(blanket)

    # Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = frame
    bpy.ops.object.join()
    
    frame.name = "BedAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return frame

def main():
    parser = argparse.ArgumentParser(description="Procedural Bed Generator")
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
    bed_obj = generate_bed(params)
    
    if args.render:
        utils.setup_lighting_and_camera(bed_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
