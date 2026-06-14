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

def generate_kitchen_island(params):
    w = params.get("width", 160.0) / 100.0  # cm to meters
    d = params.get("depth", 90.0) / 100.0
    h = params.get("height", 90.0) / 100.0
    overhang = params.get("overhang_depth", 25.0) / 100.0
    has_stools = params.get("has_stools", True)
    stools_count = params.get("stools_count", 2)
    material_style = params.get("material", "wood_marble")

    parts = []

    # 1. Setup Materials
    if material_style == "industrial_metal":
        # Steel / Dark iron frame with wood top
        top_color = (0.45, 0.3, 0.18, 1.0) # wood top
        top_rough = 0.5
        top_metal = 0.0
        base_color = (0.15, 0.15, 0.15, 1.0) # dark steel base
        base_rough = 0.3
        base_metal = 0.9
        accent_color = (0.75, 0.55, 0.15, 1.0) # brass knobs
    else:
        # wood_marble
        top_color = (0.95, 0.95, 0.95, 1.0) # marble top
        top_rough = 0.1 # glossy marble
        top_metal = 0.0
        base_color = (0.85, 0.85, 0.85, 1.0) # white painted wood base
        base_rough = 0.4
        base_metal = 0.0
        accent_color = (0.8, 0.8, 0.8, 1.0) # chrome handles

    top_mat = utils.create_material("IslandTop", diffuse_color=top_color, metallic=top_metal, roughness=top_rough)
    base_mat = utils.create_material("IslandBase", diffuse_color=base_color, metallic=base_metal, roughness=base_rough)
    accent_mat = utils.create_material("IslandAccent", diffuse_color=accent_color, metallic=0.9, roughness=0.15)
    stool_cushion_mat = utils.create_material("StoolCushion", diffuse_color=(0.25, 0.25, 0.25, 1.0), metallic=0.0, roughness=0.7)

    top_thick = 0.04
    base_h = h - top_thick

    # Carcass depth is total depth minus overhang
    carcass_d = d - overhang
    # Offset carcass so overhang extends on positive Y
    carcass_y_offset = -overhang / 2.0

    # ── CARCASS BASE BLOCK ──────────────────────────────────────────────────
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, carcass_y_offset, base_h / 2.0))
    carcass = bpy.context.active_object
    carcass.name = "IslandBaseCarcass"
    carcass.scale = (w - 0.04, carcass_d, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(carcass, width=0.005)
    utils.apply_material(carcass, base_mat)
    parts.append(carcass)

    # Base kicker recess at bottom front/sides
    kicker_h = 0.08
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, carcass_y_offset - 0.01, kicker_h / 2.0))
    kicker = bpy.context.active_object
    kicker.name = "IslandBaseKicker"
    kicker.scale = (w - 0.08, carcass_d - 0.02, kicker_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(kicker, base_mat)
    parts.append(kicker)

    # ── DRAWERS/DOORS (Facing Negative Y - Front side of island) ───────────
    # We will build drawer/door panels along the front
    front_y = carcass_y_offset - carcass_d / 2.0 - 0.01
    panel_w = (w - 0.1) / 3.0
    panel_h = base_h - kicker_h - 0.04
    panel_z = kicker_h + panel_h / 2.0 + 0.02

    for col in [-1, 0, 1]:
        panel_x = col * (panel_w + 0.015)
        # Center column is drawers, sides are doors
        if col == 0:
            # 3 Stacked drawers
            row_h = panel_h / 3.0
            for r in range(3):
                rz = kicker_h + 0.02 + r * row_h + row_h / 2.0
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(panel_x, front_y, rz))
                dr_front = bpy.context.active_object
                dr_front.name = f"IslandDrawer_{r}"
                dr_front.scale = (panel_w, 0.015, row_h - 0.005)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(dr_front, width=0.002)
                utils.apply_material(dr_front, base_mat)
                parts.append(dr_front)

                # Modern bar handle
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(panel_x, front_y - 0.01, rz))
                handle = bpy.context.active_object
                handle.name = f"IslandHandle_{col}_{r}"
                handle.scale = (panel_w * 0.5, 0.01, 0.012)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(handle, width=0.002)
                utils.apply_material(handle, accent_mat)
                parts.append(handle)
        else:
            # Side Cabinet Door
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(panel_x, front_y, panel_z))
            door = bpy.context.active_object
            door.name = f"IslandDoor_{col}"
            door.scale = (panel_w, 0.015, panel_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(door, width=0.003)
            utils.apply_material(door, base_mat)
            parts.append(door)

            # Round knob handle
            knob_x_offset = panel_x + (panel_w / 2.0 - 0.03) if col < 0 else panel_x - (panel_w / 2.0 - 0.03)
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=0.01,
                subdivisions=2,
                location=(knob_x_offset, front_y - 0.01, panel_z)
            )
            knob = bpy.context.active_object
            knob.name = f"IslandKnob_{col}"
            utils.apply_smooth_by_angle(knob)
            utils.apply_material(knob, accent_mat)
            parts.append(knob)

    # ── COUNTERTOP SLAB ─────────────────────────────────────────────────────
    # Slab sits on top, Y goes from -d/2 to d/2
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h - top_thick / 2.0))
    slab = bpy.context.active_object
    slab.name = "IslandSlab"
    slab.scale = (w, d, top_thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(slab, width=0.008)
    utils.apply_material(slab, top_mat)
    parts.append(slab)

    # Support legs or corbels under the overhang (on positive Y side)
    overhang_y = d / 2.0 - overhang / 2.0
    for side in [-1.0, 1.0]:
        post_x = side * (w / 2.0 - 0.05)
        # support post
        bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=base_h, location=(post_x, d/2.0 - 0.03, base_h/2.0))
        post = bpy.context.active_object
        post.name = f"IslandSupportPost_{'L' if side < 0 else 'R'}"
        utils.apply_smooth_by_angle(post)
        utils.apply_material(post, base_mat)
        parts.append(post)

    # ── procedurally generate STOOLS UNDER OVERHANG ─────────────────────────
    if has_stools and stools_count > 0:
        stool_seat_h = h - 0.25 # Stool seat is 25cm below island countertop (65cm)
        stool_d = 0.32
        stool_z = stool_seat_h

        # Stools position in Y is under overhang
        stool_y = d / 2.0 - overhang / 2.0 - 0.05

        # Space stools out along width
        # Spacing depends on stools_count
        if stools_count == 1:
            stool_xs = [0.0]
        elif stools_count == 2:
            stool_xs = [-w / 4.0, w / 4.0]
        elif stools_count == 3:
            stool_xs = [-w / 3.0, 0.0, w / 3.0]
        else: # 4
            stool_xs = [-3.0 * w / 8.0, -w / 8.0, w / 8.0, 3.0 * w / 8.0]

        for s_idx, sx in enumerate(stool_xs):
            # Model simple bar stool
            # Seat Cushion (thick cylinder)
            bpy.ops.mesh.primitive_cylinder_add(radius=stool_d / 2.0, depth=0.06, location=(sx, stool_y, stool_z - 0.03))
            s_seat = bpy.context.active_object
            s_seat.name = f"StoolSeat_{s_idx}"
            utils.apply_smooth_by_angle(s_seat)
            utils.apply_material(s_seat, stool_cushion_mat)
            parts.append(s_seat)

            # Stool legs
            stool_leg_h = stool_z - 0.06
            stool_leg_z = stool_leg_h / 2.0
            leg_spread = stool_d / 2.0 - 0.03
            
            for leg_angle in [0, 90, 180, 270]:
                rad = math.radians(leg_angle)
                lx = sx + leg_spread * math.cos(rad)
                ly = stool_y + leg_spread * math.sin(rad)
                bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=stool_leg_h, location=(lx, ly, stool_leg_z))
                s_leg = bpy.context.active_object
                s_leg.name = f"StoolLeg_{s_idx}_{leg_angle}"
                utils.apply_smooth_by_angle(s_leg)
                utils.apply_material(s_leg, base_mat)
                parts.append(s_leg)

            # Footrest ring
            bpy.ops.mesh.primitive_torus_add(
                align='WORLD',
                location=(sx, stool_y, stool_leg_h * 0.35),
                major_radius=leg_spread - 0.01,
                minor_radius=0.008
            )
            s_ring = bpy.context.active_object
            s_ring.name = f"StoolRing_{s_idx}"
            utils.apply_smooth_by_angle(s_ring)
            utils.apply_material(s_ring, base_mat)
            parts.append(s_ring)

    # ── Join all parts ────────────────────────────────────────────────────────
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = slab
    bpy.ops.object.join()
    slab.name = "KitchenIslandAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    return slab

def main():
    parser = argparse.ArgumentParser(description="Procedural Kitchen Island Generator")
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
    obj = generate_kitchen_island(params)

    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
