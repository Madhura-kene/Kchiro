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

def generate_dining_set(params):
    w_t = params.get("table_width", 180.0) / 100.0  # cm to meters
    d_t = params.get("table_depth", 90.0) / 100.0
    h_t = params.get("table_height", 75.0) / 100.0
    chair_count = params.get("chair_count", 6)
    chair_style = params.get("chair_style", "classic")
    mat_style = params.get("material", "oak")

    parts = []

    # 1. Setup Materials
    if mat_style == "walnut":
        wood_color = (0.32, 0.22, 0.14, 1.0) # rich dark walnut
        roughness = 0.5
    else:
        wood_color = (0.58, 0.42, 0.24, 1.0) # golden oak
        roughness = 0.55

    wood_mat = utils.create_material("DiningSetWood", diffuse_color=wood_color, metallic=0.0, roughness=roughness)
    cushion_color = (0.85, 0.82, 0.76, 1.0) # off-white fabric cushion
    cushion_mat = utils.create_material("ChairCushion", diffuse_color=cushion_color, metallic=0.0, roughness=0.8)
    metal_mat = utils.create_material("ChairMetal", diffuse_color=(0.15, 0.15, 0.15, 1.0), metallic=0.9, roughness=0.3)

    # ── GENERATE TABLE ──────────────────────────────────────────────────────
    top_thick = 0.04
    table_top_z = h_t - top_thick / 2.0

    # Table Top
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, table_top_z))
    top = bpy.context.active_object
    top.name = "TableTop"
    top.scale = (w_t, d_t, top_thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(top, width=0.008)
    utils.apply_material(top, wood_mat)
    parts.append(top)

    # Table Apron Frame
    apron_h = 0.06
    apron_thick = 0.025
    apron_z = h_t - top_thick - apron_h / 2.0
    apron_inset = 0.08

    # Long sides apron
    for sign in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, sign * (d_t/2.0 - apron_inset), apron_z))
        ap = bpy.context.active_object
        ap.name = f"TableApronLong_{sign}"
        ap.scale = (w_t - apron_inset * 2.0, apron_thick, apron_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(ap, wood_mat)
        parts.append(ap)

    # Short sides apron
    for sign in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sign * (w_t/2.0 - apron_inset), 0, apron_z))
        ap = bpy.context.active_object
        ap.name = f"TableApronShort_{sign}"
        ap.scale = (apron_thick, d_t - apron_inset * 2.0, apron_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(ap, wood_mat)
        parts.append(ap)

    # Table Legs
    leg_size = 0.07
    leg_h = h_t - top_thick
    leg_z = leg_h / 2.0
    lx_offset = w_t / 2.0 - apron_inset
    ly_offset = d_t / 2.0 - apron_inset

    for lx in [-lx_offset, lx_offset]:
        for ly in [-ly_offset, ly_offset]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, leg_z))
            leg = bpy.context.active_object
            leg.name = f"TableLeg_{lx:.2f}_{ly:.2f}"
            leg.scale = (leg_size, leg_size, leg_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(leg, width=0.005)
            utils.apply_material(leg, wood_mat)
            parts.append(leg)

    # ── PROCEDURAL CHAIR GENERATOR INLINE ───────────────────────────────────
    def make_chair_mesh(style, x, y, rot_z):
        chair_parts = []
        c_w = 0.44
        c_d = 0.44
        c_h_seat = 0.45
        c_h_back = 0.45

        # Create localized chair seat
        seat_z = c_h_seat - 0.02

        # Base Seat
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, seat_z))
        c_seat = bpy.context.active_object
        c_seat.name = "ChairSeatMesh"
        c_seat.scale = (c_w, c_d, 0.04)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(c_seat, width=0.005)
        utils.apply_material(c_seat, cushion_mat if style == "classic" else wood_mat)
        chair_parts.append(c_seat)

        # Legs and Backrest depending on style
        if style == "modern":
            # Modern scoop seat with metal legs
            # Backrest - curved shell panel
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, c_d / 2.0 - 0.02, seat_z + c_h_back / 2.0))
            c_back = bpy.context.active_object
            c_back.name = "ChairBackMesh"
            c_back.scale = (c_w, 0.02, c_h_back)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(c_back, width=0.004)
            utils.apply_material(c_back, wood_mat)
            chair_parts.append(c_back)

            # Slim metal hairpin legs
            leg_spread_x = c_w / 2.0 - 0.04
            leg_spread_y = c_d / 2.0 - 0.04
            for l_idx, (lx, ly) in enumerate([
                (-leg_spread_x, -leg_spread_y), (leg_spread_x, -leg_spread_y),
                (-leg_spread_x, leg_spread_y), (leg_spread_x, leg_spread_y)
            ]):
                bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=c_h_seat - 0.02, location=(lx, ly, (c_h_seat - 0.02) / 2.0))
                c_leg = bpy.context.active_object
                c_leg.name = f"ChairLeg_{l_idx}"
                # Angle the legs slightly outward for modern look
                c_leg.rotation_euler = (0.08 * (1.0 if ly < 0 else -1.0), 0.08 * (1.0 if lx < 0 else -1.0), 0.0)
                utils.apply_smooth_by_angle(c_leg)
                utils.apply_material(c_leg, metal_mat)
                chair_parts.append(c_leg)
        else:
            # Classic wood slats
            # 4 square wood legs
            leg_spread_x = c_w / 2.0 - 0.03
            leg_spread_y = c_d / 2.0 - 0.03
            leg_size = 0.035
            leg_len = c_h_seat - 0.04
            for l_idx, (lx, ly) in enumerate([
                (-leg_spread_x, -leg_spread_y), (leg_spread_x, -leg_spread_y),
                (-leg_spread_x, leg_spread_y), (leg_spread_x, leg_spread_y)
            ]):
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, leg_len / 2.0))
                c_leg = bpy.context.active_object
                c_leg.name = f"ChairLeg_{l_idx}"
                c_leg.scale = (leg_size, leg_size, leg_len)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(c_leg, width=0.003)
                utils.apply_material(c_leg, wood_mat)
                chair_parts.append(c_leg)

            # Backrest posts extending from back legs
            for side_sign in [-1, 1]:
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_sign * leg_spread_x, leg_spread_y, c_h_seat + c_h_back / 2.0))
                post = bpy.context.active_object
                post.name = f"ChairBackPost_{side_sign}"
                post.scale = (0.03, 0.03, c_h_back)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(post, width=0.003)
                utils.apply_material(post, wood_mat)
                chair_parts.append(post)

            # Slats connecting posts
            slat_w = c_w - 0.06
            for s_idx in range(3):
                slat_z = c_h_seat + 0.1 + s_idx * 0.12
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, leg_spread_y, slat_z))
                slat = bpy.context.active_object
                slat.name = f"ChairBackSlat_{s_idx}"
                slat.scale = (slat_w, 0.015, 0.04)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(slat, width=0.002)
                utils.apply_material(slat, wood_mat)
                chair_parts.append(slat)

        # Join the chair meshes
        bpy.ops.object.select_all(action='DESELECT')
        for cp in chair_parts:
            cp.select_set(True)
        bpy.context.view_layer.objects.active = c_seat
        bpy.ops.object.join()
        c_seat.name = "TempChair"

        # Apply position and rotation
        c_seat.location = (x, y, 0)
        c_seat.rotation_euler = (0, 0, rot_z)
        bpy.ops.object.transform_apply(location=True, rotation=True)
        
        return c_seat

    # ── LAYOUT CHAIRS AROUND TABLE ──────────────────────────────────────────
    tuck_in = 0.12 # tuck chairs slightly under table edge
    offset_y = d_t / 2.0 - tuck_in + 0.22 # distance to chair center
    offset_x = w_t / 2.0 - tuck_in + 0.22

    # Calculate coordinates
    chair_positions = [] # tuples of (x, y, rot_z)

    if chair_count <= 4:
        # 2 on each side if space permits, or 1 on each long side
        half_chairs = chair_count // 2
        if half_chairs == 1:
            chair_positions.append((0.0, -offset_y, 0.0))
            chair_positions.append((0.0, offset_y, math.pi))
        else: # 2 on each side
            for x_sign in [-1, 1]:
                cx = x_sign * w_t * 0.22
                chair_positions.append((cx, -offset_y, 0.0))
                chair_positions.append((cx, offset_y, math.pi))
    elif chair_count == 6:
        # 3 on each side
        for col in [-1, 0, 1]:
            cx = col * w_t * 0.28
            chair_positions.append((cx, -offset_y, 0.0))
            chair_positions.append((cx, offset_y, math.pi))
    elif chair_count == 8:
        # 3 on each long side + 1 on each end
        for col in [-1, 0, 1]:
            cx = col * w_t * 0.28
            chair_positions.append((cx, -offset_y, 0.0))
            chair_positions.append((cx, offset_y, math.pi))
        # ends
        chair_positions.append((-offset_x, 0.0, math.pi / 2.0))
        chair_positions.append((offset_x, 0.0, -math.pi / 2.0))
    else: # 10 or more
        # 4 on each long side + 1 on each end
        for col in [-1.5, -0.5, 0.5, 1.5]:
            cx = col * w_t * 0.22
            chair_positions.append((cx, -offset_y, 0.0))
            chair_positions.append((cx, offset_y, math.pi))
        # ends
        chair_positions.append((-offset_x, 0.0, math.pi / 2.0))
        chair_positions.append((offset_x, 0.0, -math.pi / 2.0))

    # Generate each chair
    for idx, (cx, cy, rot_z) in enumerate(chair_positions[:chair_count]):
        c_obj = make_chair_mesh(chair_style, cx, cy, rot_z)
        parts.append(c_obj)

    # ── Join table and all chairs into one final Dining Set asset ───────────
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = top
    bpy.ops.object.join()
    top.name = "DiningSetAsset"
    
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    return top

def main():
    parser = argparse.ArgumentParser(description="Procedural Dining Set Generator")
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
    obj = generate_dining_set(params)

    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
