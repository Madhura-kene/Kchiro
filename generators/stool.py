import os
import sys
import json
import argparse
import math

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

def generate_stool(params):
    """
    Stool — seat without a backrest.
    Distinctly different from Chair (no backrest posts/slats) and
    typically taller (bar/counter height) or with a round seat.

    Params (all cm):
      - diameter:    seat diameter if round, or seat width if square (default 35)
      - height:      total seat height (default 65 — counter height)
      - style:       'round' | 'square' | 'saddle'  (default 'round')
      - num_legs:    3 or 4  (default 3 for stools — more distinctive)
      - has_footrest: bool — adds a horizontal ring/rail at mid-leg  (default True)
      - material:    'wood' | 'metal' | 'mixed'  (default 'wood')
    """
    diam       = params.get("diameter",  35.0) / 100.0
    height     = params.get("height",   65.0) / 100.0
    style      = params.get("style", "round")
    num_legs   = params.get("num_legs", 3)
    footrest   = params.get("has_footrest", True)
    material   = params.get("material", "wood")

    parts = []

    # ── Materials ─────────────────────────────────────────────────────────────
    if material == "metal":
        seat_mat = utils.create_material("StoolSeat",
            diffuse_color=(0.18, 0.18, 0.20, 1.0), metallic=0.95, roughness=0.2)
        leg_mat  = seat_mat
    elif material == "mixed":
        seat_mat = utils.create_material("StoolSeat",
            diffuse_color=(0.55, 0.38, 0.22, 1.0), metallic=0.0, roughness=0.55)
        leg_mat  = utils.create_material("StoolLeg",
            diffuse_color=(0.10, 0.10, 0.12, 1.0), metallic=0.9, roughness=0.2)
    else:  # wood
        seat_mat = utils.create_material("StoolSeat",
            diffuse_color=(0.48, 0.30, 0.14, 1.0), metallic=0.0, roughness=0.6)
        leg_mat  = seat_mat

    seat_thick = 0.035
    leg_h = height - seat_thick
    leg_r = 0.018 if material == "metal" else 0.022

    # ── Seat ──────────────────────────────────────────────────────────────────
    seat_z = height - seat_thick / 2.0

    if style == "round":
        bpy.ops.mesh.primitive_cylinder_add(
            radius=diam / 2.0, depth=seat_thick, location=(0, 0, seat_z))
        seat = bpy.context.active_object
        seat.name = "StoolSeat"
        utils.apply_smooth_by_angle(seat)

    elif style == "saddle":
        # Saddle = elongated oval — use cylinder scaled asymmetrically
        bpy.ops.mesh.primitive_cylinder_add(
            radius=diam / 2.0, depth=seat_thick, location=(0, 0, seat_z))
        seat = bpy.context.active_object
        seat.name = "StoolSeat"
        seat.scale = (1.0, 0.65, 1.0)   # narrower in Y = saddle shape
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_smooth_by_angle(seat)

    else:  # square
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, seat_z))
        seat = bpy.context.active_object
        seat.name = "StoolSeat"
        seat.scale = (diam, diam, seat_thick)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(seat, width=0.008)

    utils.apply_material(seat, seat_mat)
    parts.append(seat)

    # ── Legs (evenly spaced around a circle) ──────────────────────────────────
    leg_radius_offset = diam / 2.0 * 0.72   # how far from center each leg sits
    leg_z_center = leg_h / 2.0

    for i in range(num_legs):
        angle = (2 * math.pi / num_legs) * i + math.pi / num_legs
        lx = math.cos(angle) * leg_radius_offset
        ly = math.sin(angle) * leg_radius_offset

        bpy.ops.mesh.primitive_cylinder_add(
            radius=leg_r, depth=leg_h, location=(lx, ly, leg_z_center))
        leg = bpy.context.active_object
        leg.name = f"StoolLeg_{i}"

        # Slight outward splay (tilt away from center for stability look)
        splay = 0.07
        leg.rotation_euler = (
            math.sin(angle) * splay,
            -math.cos(angle) * splay,
            0
        )
        utils.apply_smooth_by_angle(leg)
        utils.apply_material(leg, leg_mat)
        parts.append(leg)

    # ── Footrest ring / rail ───────────────────────────────────────────────────
    if footrest:
        fr_z    = leg_h * 0.38   # about 1/3 up from the floor
        fr_r    = leg_radius_offset * 0.90
        fr_tube = leg_r * 0.8

        bpy.ops.mesh.primitive_torus_add(
            major_radius=fr_r,
            minor_radius=fr_tube,
            location=(0, 0, fr_z)
        )
        ring = bpy.context.active_object
        ring.name = "FootrestRing"
        utils.apply_smooth_by_angle(ring)
        utils.apply_material(ring, leg_mat)
        parts.append(ring)

    # ── Join ──────────────────────────────────────────────────────────────────
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = seat
    bpy.ops.object.join()
    seat.name = "StoolAsset"
    return seat


def main():
    parser = argparse.ArgumentParser(description="Procedural Stool Generator")
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
    obj = generate_stool(params)
    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
