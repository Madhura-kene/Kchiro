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

def generate_dining_table(params):
    """
    Generates a formal dining table with thick legs and an apron (frame) under the top.
    Params:
      - width (cm): table width (long side), default 180
      - depth (cm): table depth (short side), default 90
      - height (cm): total table height, default 78
      - seats: number of seats — affects proportions (4, 6, 8), default 6
      - leg_style: 'square' or 'turned', default 'square'
    """
    width  = params.get("width",  180.0) / 100.0
    depth  = params.get("depth",   90.0) / 100.0
    height = params.get("height",  78.0) / 100.0
    leg_style = params.get("leg_style", "square")

    parts = []

    # Materials
    oak_mat = utils.create_material("DiningOak",
        diffuse_color=(0.55, 0.35, 0.18, 1.0), metallic=0.0, roughness=0.55)

    top_thickness = 0.05          # 5 cm tabletop
    apron_h       = 0.08          # 8 cm apron
    leg_size      = 0.09          # 9 cm square leg
    leg_h         = height - top_thickness
    inset         = 0.12          # leg inset from edges

    # ── Tabletop ─────────────────────────────────────────────────────────────
    top_z = height - top_thickness / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, top_z))
    top = bpy.context.active_object
    top.name = "DiningTop"
    top.scale = (width, depth, top_thickness)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(top, width=0.008)
    utils.apply_material(top, oak_mat)
    parts.append(top)

    # ── Apron (four side rails under the top) ────────────────────────────────
    apron_z = height - top_thickness - apron_h / 2.0
    rail_thickness = 0.03

    # Long rails (front/back)
    for sign in (-1, 1):
        bpy.ops.mesh.primitive_cube_add(size=1.0,
            location=(0, sign * (depth / 2.0 - inset / 2.0), apron_z))
        rail = bpy.context.active_object
        rail.name = f"LongRail_{sign}"
        rail.scale = (width - inset * 2, rail_thickness, apron_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(rail, oak_mat)
        parts.append(rail)

    # Short rails (left/right)
    for sign in (-1, 1):
        bpy.ops.mesh.primitive_cube_add(size=1.0,
            location=(sign * (width / 2.0 - inset / 2.0), 0, apron_z))
        rail = bpy.context.active_object
        rail.name = f"ShortRail_{sign}"
        rail.scale = (rail_thickness, depth - inset * 2, apron_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(rail, oak_mat)
        parts.append(rail)

    # ── Four Legs ─────────────────────────────────────────────────────────────
    px = width  / 2.0 - inset
    py = depth  / 2.0 - inset
    leg_z_center = leg_h / 2.0

    for lx, ly in [(-px, -py), (px, -py), (-px, py), (px, py)]:
        if leg_style == "turned":
            # Turned leg = stacked cylinders tapering
            for seg, (seg_r, seg_h, seg_z_off) in enumerate([
                (0.045, 0.12, leg_h - 0.06),   # top collar
                (0.035, leg_h - 0.24, leg_h / 2.0 - 0.06),  # main shaft
                (0.030, 0.12, 0.06),            # bottom foot
            ]):
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=seg_r, depth=seg_h, location=(lx, ly, seg_z_off))
                seg_obj = bpy.context.active_object
                seg_obj.name = f"LegSeg_{lx:.2f}_{ly:.2f}_{seg}"
                utils.apply_smooth_by_angle(seg_obj)
                utils.apply_material(seg_obj, oak_mat)
                parts.append(seg_obj)
        else:  # square
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, leg_z_center))
            leg = bpy.context.active_object
            leg.name = f"Leg_{lx:.2f}_{ly:.2f}"
            leg.scale = (leg_size, leg_size, leg_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(leg, width=0.006)
            utils.apply_material(leg, oak_mat)
            parts.append(leg)

    # ── Join all parts ────────────────────────────────────────────────────────
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = top
    bpy.ops.object.join()
    top.name = "DiningTableAsset"
    return top


def main():
    parser = argparse.ArgumentParser(description="Procedural Dining Table Generator")
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
    obj = generate_dining_table(params)

    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)


if __name__ == "__main__":
    main()
