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

def generate_oven(params):
    w = params.get("width", 60.0) / 100.0  # convert cm to meters
    d = params.get("depth", 55.0) / 100.0
    h = params.get("height", 60.0) / 100.0
    has_glass_window = params.get("has_glass_window", True)
    shelves_count = params.get("shelves", 2)
    style = params.get("style", "built_in")

    parts = []

    # 1. Setup Materials
    # Oven standard is stainless steel with black glass accents
    body_mat = utils.create_material("OvenBody", diffuse_color=(0.85, 0.85, 0.87, 1.0), metallic=0.9, roughness=0.22)
    glass_mat = utils.create_material("OvenGlass", diffuse_color=(0.05, 0.05, 0.05, 1.0), metallic=0.1, roughness=0.05)
    interior_mat = utils.create_material("OvenInterior", diffuse_color=(0.12, 0.12, 0.13, 1.0), metallic=0.2, roughness=0.45)
    rack_mat = utils.create_material("OvenRack", diffuse_color=(0.8, 0.8, 0.82, 1.0), metallic=0.9, roughness=0.15)
    knob_mat = utils.create_material("OvenKnobs", diffuse_color=(0.8, 0.8, 0.82, 1.0), metallic=0.9, roughness=0.2)
    display_mat = utils.create_material("OvenDisplay", diffuse_color=(0.03, 0.05, 0.04, 1.0), metallic=0.0, roughness=0.1)

    door_thick = 0.035
    control_h = h * 0.18
    door_h = h - control_h - 0.01

    # 2. Carcass & Built-in vs Freestanding setup
    if style == "built_in":
        # Built-in ovens have a front bezel/flange that sits flush, and a slightly smaller rear body
        bezel_thick = 0.02
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -d / 2.0 + bezel_thick / 2.0, h / 2.0))
        bezel = bpy.context.active_object
        bezel.name = "OvenFrontBezel"
        bezel.scale = (w, bezel_thick, h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(bezel, width=0.003)
        utils.apply_material(bezel, body_mat)
        parts.append(bezel)
        master_obj = bezel

        # Main housing box behind the bezel
        body_w = w - 0.04
        body_h = h - 0.04
        body_d = d - bezel_thick
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, bezel_thick / 2.0, h / 2.0))
        housing = bpy.context.active_object
        housing.name = "OvenHousing"
        housing.scale = (body_w, body_d, body_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(housing, interior_mat)
        parts.append(housing)
    else:
        # Freestanding style: simple clean outer carcass, fits on the floor, has small feet
        base_h = 0.04
        carcass_h = h - base_h
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, base_h + carcass_h / 2.0))
        carcass = bpy.context.active_object
        carcass.name = "OvenCarcass"
        carcass.scale = (w, d, carcass_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(carcass, width=0.005)
        utils.apply_material(carcass, body_mat)
        parts.append(carcass)
        master_obj = carcass

        # Add 4 feet
        foot_r = 0.02
        foot_h = base_h
        for sx in [-w/2.0 + 0.04, w/2.0 - 0.04]:
            for sy in [-d/2.0 + 0.04, d/2.0 - 0.04]:
                bpy.ops.mesh.primitive_cylinder_add(radius=foot_r, depth=foot_h, location=(sx, sy, foot_h/2.0))
                foot = bpy.context.active_object
                foot.name = "OvenFoot"
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_material(foot, interior_mat)
                parts.append(foot)

    # 3. Control Panel (Top Section)
    panel_z = h - control_h / 2.0
    panel_y = -d / 2.0 - 0.002
    
    # Dark glass control banner
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, panel_y, panel_z))
    ctrl_banner = bpy.context.active_object
    ctrl_banner.name = "OvenControlBanner"
    ctrl_banner.scale = (w - 0.004, 0.01, control_h - 0.004)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(ctrl_banner, glass_mat)
    parts.append(ctrl_banner)

    # Center digital display screen
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, panel_y - 0.006, panel_z))
    display = bpy.context.active_object
    display.name = "OvenDigitalDisplay"
    display.scale = (w * 0.18, 0.002, control_h * 0.45)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(display, display_mat)
    parts.append(display)

    # Dial Knobs (left and right of screen)
    knob_offsets = [-w * 0.22, w * 0.22]
    for idx, kx in enumerate(knob_offsets):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.012, location=(kx, panel_y - 0.006, panel_z))
        knob = bpy.context.active_object
        knob.name = f"OvenControlKnob_{idx}"
        knob.rotation_euler.x = math.radians(90)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_bevel(knob, width=0.001)
        utils.apply_material(knob, knob_mat)
        parts.append(knob)

    # 4. Oven Door (Bottom Section)
    door_z = door_h / 2.0 + 0.005
    door_y = -d / 2.0 - door_thick / 2.0
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, door_y, door_z))
    door = bpy.context.active_object
    door.name = "OvenDoor"
    door.scale = (w - 0.004, door_thick, door_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(door, width=0.004)
    utils.apply_material(door, body_mat)
    parts.append(door)

    # Glass Window (If requested, else solid front panel)
    if has_glass_window:
        win_w = w * 0.76
        win_h = door_h * 0.65
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, door_y - 0.002, door_z))
        window = bpy.context.active_object
        window.name = "OvenWindow"
        window.scale = (win_w, door_thick + 0.004, win_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(window, glass_mat)
        parts.append(window)

    # Horizontal Pull-Down Handle
    hnd_z = door_z + door_h * 0.4
    hnd_y = door_y - 0.022
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, hnd_y, hnd_z))
    handle = bpy.context.active_object
    handle.name = "OvenDoorHandle"
    handle.scale = (w * 0.74, 0.016, 0.016)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(handle, width=0.002)
    utils.apply_material(handle, rack_mat)
    parts.append(handle)

    # Handle mounts
    for hx in [-w * 0.32, w * 0.32]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx, (door_y + hnd_y)/2.0, hnd_z))
        mount = bpy.context.active_object
        mount.name = f"OvenHandleMount_{hx}"
        mount.scale = (0.016, abs(door_y - hnd_y), 0.016)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(mount, rack_mat)
        parts.append(mount)

    # 5. Internal Cavity and Wire Racks
    # We position the wire racks slightly inside behind the glass door (so they are visible through it)
    cavity_w = w - 0.12
    cavity_d = d - door_thick - 0.04
    cavity_h = door_h - 0.08
    
    # Internal wire shelves/racks
    if shelves_count > 0:
        shelf_spacing = cavity_h / (shelves_count + 1)
        shelf_start_z = door_z - cavity_h/2.0 + shelf_spacing
        
        for s in range(shelves_count):
            sz = shelf_start_z + s * shelf_spacing
            sy = 0.0 # centered in depth
            
            # Rack frame border
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, sy, sz))
            frame = bpy.context.active_object
            frame.name = f"OvenShelfFrame_{s}"
            frame.scale = (cavity_w, cavity_d, 0.008)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(frame, width=0.002)
            utils.apply_material(frame, rack_mat)
            parts.append(frame)
            
            # Wire bars (3-5 bars spanning left-to-right)
            bars_count = 4
            bar_spacing = cavity_d / (bars_count + 1)
            bar_start_y = sy - cavity_d/2.0 + bar_spacing
            
            for b in range(bars_count):
                by = bar_start_y + b * bar_spacing
                bpy.ops.mesh.primitive_cylinder_add(radius=0.003, depth=cavity_w - 0.004, location=(0, by, sz))
                bar = bpy.context.active_object
                bar.name = f"OvenShelfWire_{s}_{b}"
                bar.rotation_euler.y = math.radians(90)
                bpy.ops.object.transform_apply(scale=True, rotation=True)
                utils.apply_material(bar, rack_mat)
                parts.append(bar)

    # 6. Join all parts into one mesh
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = master_obj
    bpy.ops.object.join()

    master_obj.name = "OvenAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return master_obj

def main():
    parser = argparse.ArgumentParser(description="Procedural Oven Generator")
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
    oven_obj = generate_oven(params)
    
    if args.render:
        utils.setup_lighting_and_camera(oven_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
