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

def generate_toilet(params):
    w = params.get("width", 50.0) / 100.0  # cm to meters
    d = params.get("depth", 70.0) / 100.0
    h = params.get("height", 80.0) / 100.0
    bowl_shape = params.get("bowl_shape", "elongated")
    has_lid_open = params.get("has_lid_open", False)
    tank_w = params.get("tank_width", 45.0) / 100.0
    tank_d = params.get("tank_depth", 20.0) / 100.0

    parts = []

    # 1. Setup Materials
    # Glossy white ceramic PBR material
    ceramic_mat = utils.create_material("ToiletCeramic", diffuse_color=(0.95, 0.95, 0.95, 1.0), metallic=0.0, roughness=0.05)
    # Chrome metal for flush button
    chrome_mat = utils.create_material("ToiletChrome", diffuse_color=(0.8, 0.8, 0.8, 1.0), metallic=0.9, roughness=0.1)

    # ── FLOOR BASE ─────────────────────────────────────────────────────────
    # A tapered floor-mounted base
    base_h = 0.15
    base_w = w * 0.6
    base_d = d * 0.7
    
    # We model it as a cylinder stretched on Y axis (depth)
    # Using depth=1.0 to avoid double-scaling on Z axis
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0, depth=1.0, location=(0, -0.05, base_h / 2.0)
    )
    base_obj = bpy.context.active_object
    base_obj.name = "ToiletBase"
    base_obj.scale = (base_w / 2.0, base_d / 2.0, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_smooth_by_angle(base_obj)
    utils.apply_material(base_obj, ceramic_mat)
    parts.append(base_obj)

    # ── BOWL ───────────────────────────────────────────────────────────────
    # Toilet bowl extends above the base
    bowl_h = 0.27
    bowl_z = base_h + bowl_h / 2.0
    bowl_top_r_x = w * 0.8 / 2.0
    # Elongated vs round bowl shape
    bowl_top_r_y = (d * 0.7 if bowl_shape == "elongated" else w * 0.8) / 2.0

    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0, depth=1.0, location=(0, -0.08, bowl_z)
    )
    bowl = bpy.context.active_object
    bowl.name = "ToiletBowl"
    bowl.scale = (bowl_top_r_x, bowl_top_r_y, bowl_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_smooth_by_angle(bowl)
    utils.apply_material(bowl, ceramic_mat)

    # Hollow out bowl
    cutter_w = bowl_top_r_x - 0.02
    cutter_d = bowl_top_r_y - 0.02
    cutter_h = bowl_h
    # Cutter bottom is at base_h + 0.05 to leave bottom thickness
    cutter_z = base_h + 0.05 + cutter_h / 2.0

    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0, depth=1.0, location=(0, -0.08, cutter_z)
    )
    bowl_cutter = bpy.context.active_object
    bowl_cutter.name = "BowlCutter"
    bowl_cutter.scale = (cutter_w, cutter_d, cutter_h)
    bpy.ops.object.transform_apply(scale=True)

    # Run boolean difference
    bool_mod = bowl.modifiers.new(name="HollowBowl", type='BOOLEAN')
    bool_mod.object = bowl_cutter
    bool_mod.operation = 'DIFFERENCE'
    bpy.context.view_layer.objects.active = bowl
    bpy.ops.object.modifier_apply(modifier="HollowBowl")

    # Delete cutter
    bpy.ops.object.select_all(action='DESELECT')
    bowl_cutter.select_set(True)
    bpy.ops.object.delete()

    # Rim bevel / lip (overlaps top of the bowl)
    rim_h = 0.04
    rim_z = base_h + bowl_h  # bottom is at base_h+bowl_h-0.02, top is at base_h+bowl_h+0.02
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0, depth=1.0, location=(0, -0.08, rim_z)
    )
    rim = bpy.context.active_object
    rim.name = "ToiletRim"
    rim.scale = (bowl_top_r_x + 0.01, bowl_top_r_y + 0.01, rim_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_smooth_by_angle(rim)
    utils.apply_material(rim, ceramic_mat)

    # Hollow out rim
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0, depth=1.0, location=(0, -0.08, rim_z)
    )
    rim_cutter = bpy.context.active_object
    rim_cutter.scale = (cutter_w, cutter_d, rim_h + 0.01)
    bpy.ops.object.transform_apply(scale=True)

    bool_mod_rim = rim.modifiers.new(name="HollowRim", type='BOOLEAN')
    bool_mod_rim.object = rim_cutter
    bool_mod_rim.operation = 'DIFFERENCE'
    bpy.context.view_layer.objects.active = rim
    bpy.ops.object.modifier_apply(modifier="HollowRim")

    # Delete cutter
    bpy.ops.object.select_all(action='DESELECT')
    rim_cutter.select_set(True)
    bpy.ops.object.delete()

    # Join bowl and rim after hollowing
    bpy.ops.object.select_all(action='DESELECT')
    bowl.select_set(True)
    rim.select_set(True)
    bpy.context.view_layer.objects.active = bowl
    bpy.ops.object.join()

    parts.append(bowl)

    # ── WATER TANK ─────────────────────────────────────────────────────────
    # Rectangular tank at the rear
    tank_h = h - base_h - bowl_h  # Remaining height for tank
    tank_z = base_h + bowl_h + tank_h / 2.0
    # Placed at the very back of the toilet
    tank_y = d / 2.0 - tank_d / 2.0 - 0.02

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, tank_y, tank_z))
    tank = bpy.context.active_object
    tank.name = "ToiletTank"
    tank.scale = (tank_w, tank_d, tank_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(tank, width=0.008)
    utils.apply_material(tank, ceramic_mat)
    parts.append(tank)

    # Flush button on top of the tank lid
    btn_h = 0.01
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.02, depth=1.0, location=(0, tank_y, tank_z + tank_h / 2.0 + btn_h / 2.0)
    )
    btn = bpy.context.active_object
    btn.name = "FlushButton"
    btn.scale = (1.0, 1.0, btn_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_smooth_by_angle(btn)
    utils.apply_material(btn, chrome_mat)
    parts.append(btn)

    # ── SEAT AND LID ───────────────────────────────────────────────────────
    # Placed on top of the rim (top of rim is at base_h + bowl_h + rim_h/2.0)
    rim_top_z = base_h + bowl_h + rim_h / 2.0
    seat_w = (bowl_top_r_x + 0.005) * 2.0
    seat_d = (bowl_top_r_y + 0.005) * 2.0
    seat_thick = 0.02
    seat_z = rim_top_z + seat_thick / 2.0
    seat_y = -0.08

    # Hinge is at the back of the seat
    hinge_y = tank_y - tank_d / 2.0 - 0.02

    # Model Seat Ring (hollowed cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0, depth=1.0, location=(0, seat_y, seat_z)
    )
    seat = bpy.context.active_object
    seat.name = "ToiletSeat"
    seat.scale = (seat_w / 2.0, seat_d / 2.0, seat_thick)
    bpy.ops.object.transform_apply(scale=True)

    # Create seat cutter to hollow it out
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0, depth=1.0, location=(0, seat_y, seat_z)
    )
    seat_cutter = bpy.context.active_object
    seat_cutter.name = "SeatCutter"
    seat_cutter.scale = (seat_w / 2.0 - 0.04, seat_d / 2.0 - 0.04, seat_thick + 0.01)
    bpy.ops.object.transform_apply(scale=True)

    # Run boolean difference
    bool_mod_seat = seat.modifiers.new(name="HollowSeat", type='BOOLEAN')
    bool_mod_seat.object = seat_cutter
    bool_mod_seat.operation = 'DIFFERENCE'
    bpy.context.view_layer.objects.active = seat
    bpy.ops.object.modifier_apply(modifier="HollowSeat")

    # Delete cutter
    bpy.ops.object.select_all(action='DESELECT')
    seat_cutter.select_set(True)
    bpy.ops.object.delete()

    utils.apply_smooth_by_angle(seat)
    utils.apply_material(seat, ceramic_mat)
    parts.append(seat)

    # Lid (should be a rounded cylinder shape too, matching seat)
    lid_thick = 0.015
    lid_z = seat_z + seat_thick / 2.0 + lid_thick / 2.0
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.0, depth=1.0, location=(0, seat_y, lid_z)
    )
    lid = bpy.context.active_object
    lid.name = "ToiletLid"
    lid.scale = (seat_w / 2.0, seat_d / 2.0, lid_thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_smooth_by_angle(lid)
    utils.apply_material(lid, ceramic_mat)

    if has_lid_open:
        # If open, rotate around the hinge point at the back
        bpy.ops.object.select_all(action='DESELECT')
        lid.select_set(True)
        bpy.context.view_layer.objects.active = lid
        # Pivot point offset relative to lid center
        y_offset = hinge_y - seat_y
        z_offset = lid_thick / 2.0  # Move pivot to the bottom of the lid
        
        # Translate object origin to hinge
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(0, -y_offset, -z_offset))
        bpy.ops.object.mode_set(mode='OBJECT')
        lid.location = (0, hinge_y, lid_z - z_offset)
        # Rotate the lid 85 degrees (open)
        lid.rotation_euler = (math.radians(-85.0), 0.0, 0.0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    parts.append(lid)

    # ── Join all parts ────────────────────────────────────────────────────────
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = base_obj
    bpy.ops.object.join()
    base_obj.name = "ToiletAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    return base_obj

def main():
    parser = argparse.ArgumentParser(description="Procedural Toilet Generator")
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
    obj = generate_toilet(params)

    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
