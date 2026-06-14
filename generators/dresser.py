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

def generate_dresser(params):
    w = params.get("width", 120.0) / 100.0  # convert cm to meters
    d = params.get("depth", 50.0) / 100.0
    h = params.get("height", 90.0) / 100.0
    rows = params.get("drawers_rows", 3)
    cols = params.get("drawers_cols", 2)
    style = params.get("style", "classic")

    parts = []

    # 1. Setup Materials
    if style == "rustic":
        wood_color = (0.22, 0.14, 0.08, 1.0)
        knob_color = (0.15, 0.15, 0.15, 1.0) # Iron
        metallic_knob = 0.8
        rough_wood = 0.9
    elif style == "modern":
        wood_color = (0.8, 0.75, 0.7, 1.0) # Bleached Oak / White Wood
        knob_color = (0.85, 0.85, 0.9, 1.0) # Silver chrome
        metallic_knob = 0.95
        rough_wood = 0.55
    else: # classic
        wood_color = (0.35, 0.18, 0.08, 1.0) # Mahogany/Cherry Wood
        knob_color = (0.7, 0.55, 0.2, 1.0) # Brass/Gold
        metallic_knob = 0.9
        rough_wood = 0.7

    wood_mat = utils.create_material("DresserWood", diffuse_color=wood_color, metallic=0.0, roughness=rough_wood)
    knob_mat = utils.create_material("DresserKnob", diffuse_color=knob_color, metallic=metallic_knob, roughness=0.2)

    carcass_thick = 0.03
    base_h = 0.08

    # 2. Main Carcass Box
    carcass_z = h / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, carcass_z))
    carcass = bpy.context.active_object
    carcass.name = "DresserCarcass"
    carcass.scale = (w, d, h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(carcass, width=0.006)
    utils.apply_material(carcass, wood_mat)
    parts.append(carcass)

    # 3. Base or Legs
    if style in ["classic", "rustic"]:
        # Four block/post corner legs
        leg_w = 0.06
        leg_h = base_h
        leg_offset_x = w / 2.0 - leg_w / 2.0 - 0.01
        leg_offset_y = d / 2.0 - leg_w / 2.0 - 0.01
        
        for sx in [-1.0, 1.0]:
            for sy in [-1.0, 1.0]:
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0, 
                    location=(sx * leg_offset_x, sy * leg_offset_y, leg_h / 2.0)
                )
                leg = bpy.context.active_object
                leg.name = f"DresserLeg_{sx}_{sy}"
                leg.scale = (leg_w, leg_w, leg_h)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(leg, width=0.003)
                utils.apply_material(leg, wood_mat)
                parts.append(leg)
    else:
        # Modern kicker base trim
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.01, base_h / 2.0))
        kicker = bpy.context.active_object
        kicker.name = "DresserBase"
        kicker.scale = (w - 0.02, d - 0.02, base_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(kicker, width=0.003)
        utils.apply_material(kicker, wood_mat)
        parts.append(kicker)

    # 4. Top Molded Edge (Classic/Rustic detail)
    if style in ["classic", "rustic"]:
        top_h = 0.04
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h - top_h / 2.0))
        top_panel = bpy.context.active_object
        top_panel.name = "DresserTopMold"
        top_panel.scale = (w + 0.04, d + 0.02, top_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(top_panel, width=0.008)
        utils.apply_material(top_panel, wood_mat)
        parts.append(top_panel)

    # 5. Drawers Grid
    drawers_h = h - base_h - carcass_thick * 2.0
    drawers_w = w - carcass_thick * 2.0
    gap = 0.006
    
    dh = (drawers_h - gap * (rows - 1)) / rows
    dw = (drawers_w - gap * (cols - 1)) / cols
    drawer_thick = 0.02
    drawer_y = -d / 2.0 - drawer_thick / 2.0

    for r in range(rows):
        for c in range(cols):
            # Calculate drawer cell coordinates
            dz = base_h + carcass_thick + r * (dh + gap) + dh / 2.0
            dx = -drawers_w / 2.0 + c * (dw + gap) + dw / 2.0

            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, drawer_y, dz))
            drawer = bpy.context.active_object
            drawer.name = f"DresserDrawerFront_{r}_{c}"
            drawer.scale = (dw, drawer_thick, dh)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(drawer, width=0.003)
            utils.apply_material(drawer, wood_mat)
            parts.append(drawer)

            # Drawers Knobs/Handles
            if style == "modern":
                # Sleek long horizontal handle bar
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, drawer_y - 0.015, dz))
                hnd = bpy.context.active_object
                hnd.name = f"DresserHandle_{r}_{c}"
                hnd.scale = (dw * 0.4, 0.015, 0.01)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(hnd, width=0.002)
                utils.apply_material(hnd, knob_mat)
                parts.append(hnd)
            else:
                # Classic or Rustic knobs (two knobs per drawer if wide, else one)
                knob_count = 2 if dw > 0.6 else 1
                knob_offsets = [-dw / 4.0, dw / 4.0] if knob_count == 2 else [0.0]

                for offset_x in knob_offsets:
                    bpy.ops.mesh.primitive_ico_sphere_add(
                        radius=0.015,
                        subdivisions=2,
                        location=(dx + offset_x, drawer_y - 0.012, dz)
                    )
                    knob = bpy.context.active_object
                    knob.name = f"DresserKnob_{r}_{c}_{offset_x}"
                    utils.apply_smooth_by_angle(knob, angle=40.0)
                    utils.apply_material(knob, knob_mat)
                    parts.append(knob)

    # Join dresser components
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = carcass
    bpy.ops.object.join()
    
    carcass.name = "DresserAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return carcass

def main():
    parser = argparse.ArgumentParser(description="Procedural Dresser Generator")
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
    dresser_obj = generate_dresser(params)
    
    if args.render:
        utils.setup_lighting_and_camera(dresser_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
