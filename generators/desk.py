import os
import sys
import json
import argparse

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

def generate_desk(params):
    """
    Office / writing desk — wide top, modesty panel on the back,
    optional side-pedestal drawer unit, cable-management cutout.

    Params (all cm):
      - width:        default 140  (wider than a chair table)
      - depth:        default 70   (deep enough for a monitor)
      - height:       default 75
      - style:        'straight' | 'l_shape' | 'standing'  (default 'straight')
      - has_drawers:  bool, adds a pedestal block on the right  (default False)
      - material:     'wood' | 'metal_wood' | 'white'  (default 'wood')
    """
    width       = params.get("width",  140.0) / 100.0
    depth       = params.get("depth",   70.0) / 100.0
    height      = params.get("height",  75.0) / 100.0
    style       = params.get("style", "straight")
    has_drawers = params.get("has_drawers", False)
    material    = params.get("material", "wood")

    parts = []

    # ── Materials ─────────────────────────────────────────────────────────────
    if material == "white":
        top_mat  = utils.create_material("DeskTop",
            diffuse_color=(0.90, 0.90, 0.90, 1.0), metallic=0.0, roughness=0.4)
        leg_mat  = utils.create_material("DeskLeg",
            diffuse_color=(0.85, 0.85, 0.85, 1.0), metallic=0.2, roughness=0.35)
    elif material == "metal_wood":
        top_mat  = utils.create_material("DeskTop",
            diffuse_color=(0.55, 0.38, 0.22, 1.0), metallic=0.0, roughness=0.5)
        leg_mat  = utils.create_material("DeskLeg",
            diffuse_color=(0.12, 0.12, 0.14, 1.0), metallic=0.9, roughness=0.2)
    else:  # wood
        top_mat  = utils.create_material("DeskTop",
            diffuse_color=(0.52, 0.34, 0.18, 1.0), metallic=0.0, roughness=0.55)
        leg_mat  = utils.create_material("DeskLeg",
            diffuse_color=(0.38, 0.22, 0.10, 1.0), metallic=0.0, roughness=0.6)

    top_thick  = 0.04    # 4 cm thick desktop
    panel_thick = 0.025  # 2.5 cm modesty / back panel
    leg_w       = 0.06   # square leg width
    inset       = 0.08

    standing_offset = 0.40 if style == "standing" else 0.0   # raise legs for standing desk

    real_height = height + standing_offset
    leg_h = real_height - top_thick

    # ── Desktop ───────────────────────────────────────────────────────────────
    top_z = real_height - top_thick / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, top_z))
    top = bpy.context.active_object
    top.name = "DeskTop"
    top.scale = (width, depth, top_thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(top, width=0.007)
    utils.apply_material(top, top_mat)
    parts.append(top)

    # ── L-shape extension (adds a perpendicular wing on the left) ─────────────
    if style == "l_shape":
        wing_w = depth * 0.85   # wing width = depth of main surface
        wing_d = width * 0.55   # wing depth
        wing_x = -(width / 2.0 + wing_w / 2.0 - top_thick)
        wing_y = depth / 2.0 - wing_d / 2.0

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wing_x, wing_y, top_z))
        wing = bpy.context.active_object
        wing.name = "DeskWing"
        wing.scale = (wing_w, wing_d, top_thick)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(wing, width=0.007)
        utils.apply_material(wing, top_mat)
        parts.append(wing)

    # ── Back modesty panel ────────────────────────────────────────────────────
    panel_h   = min(leg_h * 0.65, 0.45)
    panel_z   = real_height - top_thick - panel_h / 2.0
    back_y    = -(depth / 2.0 - panel_thick / 2.0)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, back_y, panel_z))
    panel = bpy.context.active_object
    panel.name = "DeskPanel"
    panel.scale = (width - inset * 2, panel_thick, panel_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(panel, leg_mat)
    parts.append(panel)

    # ── Legs ──────────────────────────────────────────────────────────────────
    px = width  / 2.0 - inset
    py = depth  / 2.0 - inset
    leg_z = leg_h / 2.0

    for lx, ly in [(-px, -py), (px, -py), (-px, py), (px, py)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, leg_z))
        leg = bpy.context.active_object
        leg.scale = (leg_w, leg_w, leg_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(leg, width=0.005)
        utils.apply_material(leg, leg_mat)
        parts.append(leg)

    # ── Drawer pedestal (right side, if requested) ────────────────────────────
    if has_drawers:
        ped_w   = 0.40
        ped_d   = depth - inset * 2
        ped_h   = leg_h
        ped_x   = width / 2.0 - inset - ped_w / 2.0
        ped_y   = 0.0
        ped_z   = ped_h / 2.0

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ped_x, ped_y, ped_z))
        ped = bpy.context.active_object
        ped.name = "DrawerPedestal"
        ped.scale = (ped_w, ped_d, ped_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(ped, leg_mat)
        parts.append(ped)

        # Three drawer fronts
        drawer_h = ped_h / 3.5
        gap = 0.008
        for i in range(3):
            dz = ped_z - ped_h / 2.0 + drawer_h * (i + 0.5) + gap * i
            bpy.ops.mesh.primitive_cube_add(size=1.0,
                location=(ped_x, -(ped_d / 2.0 + 0.005), dz))
            dr = bpy.context.active_object
            dr.scale = (ped_w - 0.02, 0.015, drawer_h - 0.01)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(dr, top_mat)
            parts.append(dr)

    # ── Join ──────────────────────────────────────────────────────────────────
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = top
    bpy.ops.object.join()
    top.name = "DeskAsset"
    return top


def main():
    parser = argparse.ArgumentParser(description="Procedural Desk Generator")
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
    obj = generate_desk(params)
    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
