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

def generate_bathtub(params):
    w = params.get("width", 160.0) / 100.0  # cm to meters
    d = params.get("depth", 75.0) / 100.0
    h = params.get("height", 60.0) / 100.0
    style = params.get("style", "freestanding")
    material_style = params.get("material", "ceramic")
    has_faucet = params.get("has_faucet", True)

    parts = []

    # 1. Setup Materials
    if material_style == "copper":
        tub_color = (0.80, 0.45, 0.30, 1.0)
        rough = 0.2
        metal = 0.9
    elif material_style == "stone":
        tub_color = (0.4, 0.4, 0.4, 1.0)
        rough = 0.8
        metal = 0.0
    else: # ceramic default
        tub_color = (0.95, 0.95, 0.95, 1.0)
        rough = 0.05
        metal = 0.0

    tub_mat = utils.create_material("TubBody", diffuse_color=tub_color, metallic=metal, roughness=rough)
    chrome_mat = utils.create_material("TubChrome", diffuse_color=(0.85, 0.85, 0.85, 1.0), metallic=0.9, roughness=0.1)
    drain_mat = utils.create_material("TubDrain", diffuse_color=(0.1, 0.1, 0.1, 1.0), metallic=0.9, roughness=0.2)

    # Offset tub height if it's clawfoot (legs lift it up by 12cm)
    lift = 0.12 if style == "clawfoot" else 0.0
    tub_z = lift + h / 2.0
    tub_top_z = lift + h

    # ── TUB OUTER BODY ──────────────────────────────────────────────────────
    if style == "alcove":
        # Alcove style is built into a rectangular surround block
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, tub_z))
        tub_outer = bpy.context.active_object
        tub_outer.name = "AlcoveSurround"
        tub_outer.scale = (w, d, h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(tub_outer, width=0.01, segments=3)
        utils.apply_material(tub_outer, tub_mat)
    else:
        # Freestanding or Clawfoot capsule oval shape
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, tub_z))
        tub_outer = bpy.context.active_object
        tub_outer.name = "TubOuter"
        tub_outer.scale = (w, d, h)
        bpy.ops.object.transform_apply(scale=True)
        # Apply heavy bevel to round out the box sides
        utils.apply_bevel(tub_outer, width=min(d/2.0 - 0.04, 0.15), segments=5)
        utils.apply_material(tub_outer, tub_mat)

    parts.append(tub_outer)

    # ── TUB INNER HOLLOWING (Boolean) ───────────────────────────────────────
    # Create the cutter object
    cutter_h = h + 0.04
    cutter_z = tub_z + 0.04
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, cutter_z))
    tub_inner = bpy.context.active_object
    tub_inner.name = "TubInnerCutter"
    tub_inner.scale = (w - 0.08, d - 0.08, cutter_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(tub_inner, width=min((d-0.08)/2.0 - 0.02, 0.12), segments=5)

    # Run boolean difference modifier
    bool_mod = tub_outer.modifiers.new(name="Hollow", type='BOOLEAN')
    bool_mod.object = tub_inner
    bool_mod.operation = 'DIFFERENCE'
    bpy.context.view_layer.objects.active = tub_outer
    bpy.ops.object.modifier_apply(modifier="Hollow")

    # Delete the cutter object
    bpy.ops.object.select_all(action='DESELECT')
    tub_inner.select_set(True)
    bpy.ops.object.delete()

    # ── DRAIN HOLE ──────────────────────────────────────────────────────────
    # Place a small drain disc at the bottom of the tub basin
    drain_z = lift + 0.045
    drain_x = -w / 2.0 + 0.25
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.005, location=(drain_x, 0.0, drain_z))
    drain = bpy.context.active_object
    drain.name = "TubDrainMesh"
    utils.apply_smooth_by_angle(drain)
    utils.apply_material(drain, drain_mat)
    parts.append(drain)

    # ── CLAWFOOT LEGS ───────────────────────────────────────────────────────
    if style == "clawfoot":
        leg_r = 0.03
        leg_h = lift
        leg_z = leg_h / 2.0
        
        # Space out legs under corners of the tub
        px = w / 2.0 - 0.15
        py = d / 2.0 - 0.10
        
        for lx in [-px, px]:
            for ly in [-py, py]:
                # Model claw legs using tapered cones/cylinders
                bpy.ops.mesh.primitive_cone_add(radius1=leg_r, radius2=leg_r*0.6, depth=leg_h, location=(lx, ly, leg_z))
                leg = bpy.context.active_object
                leg.name = f"ClawLeg_{lx:.2f}_{ly:.2f}"
                # Rotate legs slightly outwards
                leg.rotation_euler = (0.15 * (1.0 if ly < 0 else -1.0), 0.15 * (-1.0 if lx < 0 else 1.0), 0.0)
                utils.apply_smooth_by_angle(leg)
                utils.apply_material(leg, chrome_mat) # claw feet are metallic chrome
                parts.append(leg)

    # ── FAUCET ASSEMBLY ─────────────────────────────────────────────────────
    if has_faucet:
        # Faucet base and spout located at one end of the tub
        faucet_x = -w / 2.0 + 0.06
        faucet_y = 0.0
        
        # Spout riser column
        bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.20, location=(faucet_x, faucet_y, tub_top_z + 0.05))
        spout_base = bpy.context.active_object
        spout_base.name = "FaucetRiser"
        utils.apply_smooth_by_angle(spout_base)
        utils.apply_material(spout_base, chrome_mat)
        parts.append(spout_base)

        # Curved faucet neck
        bpy.ops.mesh.primitive_torus_add(
            align='WORLD',
            location=(faucet_x + 0.04, faucet_y, tub_top_z + 0.14),
            major_radius=0.04,
            minor_radius=0.012
        )
        neck = bpy.context.active_object
        neck.name = "FaucetNeck"
        neck.rotation_euler = (0.0, math.radians(90.0), 0.0)
        utils.apply_smooth_by_angle(neck)
        utils.apply_material(neck, chrome_mat)
        parts.append(neck)

        # Hot/Cold knobs
        for side_y in [-0.06, 0.06]:
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=0.02,
                subdivisions=2,
                location=(faucet_x, side_y, tub_top_z + 0.08)
            )
            knob = bpy.context.active_object
            knob.name = f"FaucetKnob_{'H' if side_y < 0 else 'C'}"
            utils.apply_smooth_by_angle(knob)
            utils.apply_material(knob, chrome_mat)
            parts.append(knob)

    # ── Join all parts ────────────────────────────────────────────────────────
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = tub_outer
    bpy.ops.object.join()
    
    tub_outer.name = "BathtubAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    return tub_outer

def main():
    parser = argparse.ArgumentParser(description="Procedural Bathtub Generator")
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
    obj = generate_bathtub(params)

    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
