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

def generate_coffee_table(params):
    """
    Generates a modern living-room coffee table — low, wide, with a thick
    slab top and distinctive low legs.

    Params:
      - width  (cm): long side width, default 110
      - depth  (cm): short side depth, default 60
      - height (cm): total table height, default 45  (much shorter than dining)
      - style: 'slab' (solid thick top), 'glass_frame' (thin top + visible frame), default 'slab'
      - leg_style: 'block', 'hairpin', default 'block'
    """
    width     = params.get("width",  110.0) / 100.0
    depth     = params.get("depth",   60.0) / 100.0
    height    = params.get("height",  45.0) / 100.0
    style     = params.get("style", "slab")
    leg_style = params.get("leg_style", "block")

    parts = []

    # ── Materials ─────────────────────────────────────────────────────────────
    wood_mat  = utils.create_material("CoffeeWood",
        diffuse_color=(0.38, 0.22, 0.10, 1.0), metallic=0.0, roughness=0.65)
    metal_mat = utils.create_material("CoffeeMetal",
        diffuse_color=(0.15, 0.15, 0.15, 1.0), metallic=0.85, roughness=0.3)

    if style == "glass_frame":
        top_thickness = 0.012   # thin glass slab
        top_mat = utils.create_material("GlassTop",
            diffuse_color=(0.7, 0.85, 0.9, 0.3), metallic=0.0, roughness=0.0)
    else:  # slab
        top_thickness = 0.07    # chunky solid-wood slab
        top_mat = wood_mat

    leg_h = height - top_thickness

    # ── Tabletop ─────────────────────────────────────────────────────────────
    top_z = height - top_thickness / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, top_z))
    top = bpy.context.active_object
    top.name = "CoffeeTop"
    top.scale = (width, depth, top_thickness)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(top, width=0.010)
    utils.apply_material(top, top_mat)
    parts.append(top)

    # ── Frame (glass_frame style adds a thin structural frame under the glass) ─
    if style == "glass_frame":
        frame_t = 0.025
        frame_h = 0.05
        frame_z = height - top_thickness - frame_h / 2.0
        # Long frame rails
        for sign in (-1, 1):
            bpy.ops.mesh.primitive_cube_add(size=1.0,
                location=(0, sign * (depth / 2.0 - frame_t / 2.0), frame_z))
            fr = bpy.context.active_object
            fr.scale = (width, frame_t, frame_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(fr, metal_mat)
            parts.append(fr)
        # Short frame rails
        for sign in (-1, 1):
            bpy.ops.mesh.primitive_cube_add(size=1.0,
                location=(sign * (width / 2.0 - frame_t / 2.0), 0, frame_z))
            fr = bpy.context.active_object
            fr.scale = (frame_t, depth, frame_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(fr, metal_mat)
            parts.append(fr)

    # ── Legs ─────────────────────────────────────────────────────────────────
    inset = 0.10
    px = width  / 2.0 - inset
    py = depth  / 2.0 - inset
    leg_z_center = leg_h / 2.0
    corners = [(-px, -py), (px, -py), (-px, py), (px, py)]

    if leg_style == "hairpin":
        # Each hairpin leg = two thin metal rods at an angle fanning outward
        rod_r  = 0.008
        for cx, cy in corners:
            for fan in (-0.04, 0.04):
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=rod_r, depth=leg_h,
                    location=(cx + fan, cy + fan, leg_z_center))
                rod = bpy.context.active_object
                # Slight forward tilt
                rod.rotation_euler = (0.08 * (1 if cy < 0 else -1),
                                      0.08 * (1 if cx < 0 else -1), 0)
                utils.apply_smooth_by_angle(rod)
                utils.apply_material(rod, metal_mat)
                parts.append(rod)
    else:  # block legs
        block_w = 0.06
        for lx, ly in corners:
            bpy.ops.mesh.primitive_cube_add(size=1.0,
                location=(lx, ly, leg_z_center))
            leg = bpy.context.active_object
            leg.name = f"CoffeeLeg_{lx:.2f}_{ly:.2f}"
            leg.scale = (block_w, block_w, leg_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(leg, width=0.005)
            utils.apply_material(leg, wood_mat)
            parts.append(leg)

    # ── Join all parts ────────────────────────────────────────────────────────
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = top
    bpy.ops.object.join()
    top.name = "CoffeeTableAsset"
    return top


def main():
    parser = argparse.ArgumentParser(description="Procedural Coffee Table Generator")
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
    obj = generate_coffee_table(params)

    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)


if __name__ == "__main__":
    main()
