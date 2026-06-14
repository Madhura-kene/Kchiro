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

def generate_microwave(params):
    w = params.get("width", 55.0) / 100.0  # convert cm to meters
    d = params.get("depth", 40.0) / 100.0
    h = params.get("height", 35.0) / 100.0
    style = params.get("style", "countertop")
    has_glass_door = params.get("has_glass_door", True)

    parts = []

    # 1. Setup Materials
    body_mat = utils.create_material("MicrowaveBody", diffuse_color=(0.85, 0.85, 0.87, 1.0), metallic=0.9, roughness=0.22)
    glass_mat = utils.create_material("MicrowaveGlass", diffuse_color=(0.04, 0.04, 0.05, 1.0), metallic=0.2, roughness=0.05)
    keypad_mat = utils.create_material("MicrowaveKeypad", diffuse_color=(0.1, 0.1, 0.11, 1.0), metallic=0.0, roughness=0.55)
    display_mat = utils.create_material("MicrowaveDisplay", diffuse_color=(0.0, 0.85, 0.25, 1.0), metallic=0.0, roughness=0.1) # Glowing green
    interior_mat = utils.create_material("MicrowaveInterior", diffuse_color=(0.15, 0.15, 0.16, 1.0), metallic=0.4, roughness=0.45)
    handle_mat = utils.create_material("MicrowaveHandle", diffuse_color=(0.8, 0.8, 0.82, 1.0), metallic=0.95, roughness=0.15)
    feet_mat = utils.create_material("MicrowaveFeet", diffuse_color=(0.08, 0.08, 0.08, 1.0), metallic=0.0, roughness=0.6)

    door_thick = 0.02
    center_z = h / 2.0

    # 2. Main Carcass Box & Style Framing
    if style == "built_in":
        # Add outer flange bezel around the front face
        bezel_thick = 0.015
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -d / 2.0 + bezel_thick / 2.0, center_z))
        bezel = bpy.context.active_object
        bezel.name = "MicrowaveFrontBezel"
        bezel.scale = (w, bezel_thick, h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(bezel, width=0.003)
        utils.apply_material(bezel, body_mat)
        parts.append(bezel)
        master_obj = bezel

        # Smaller rear body housing box
        body_w = w - 0.03
        body_h = h - 0.03
        body_d = d - bezel_thick
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, bezel_thick / 2.0, center_z))
        housing = bpy.context.active_object
        housing.name = "MicrowaveHousing"
        housing.scale = (body_w, body_d, body_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(housing, body_mat)
        parts.append(housing)
    else:
        # Countertop style: standard beveled box with support feet
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, center_z))
        carcass = bpy.context.active_object
        carcass.name = "MicrowaveCarcass"
        carcass.scale = (w, d, h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(carcass, width=0.005)
        utils.apply_material(carcass, body_mat)
        parts.append(carcass)
        master_obj = carcass

        # Add 4 small feet at the corners
        foot_h = 0.015
        foot_r = 0.015
        for sx in [-w/2.0 + 0.04, w/2.0 - 0.04]:
            for sy in [-d/2.0 + 0.04, d/2.0 - 0.04]:
                bpy.ops.mesh.primitive_cylinder_add(radius=foot_r, depth=foot_h, location=(sx, sy, -foot_h/2.0))
                foot = bpy.context.active_object
                foot.name = "MicrowaveFoot"
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_material(foot, feet_mat)
                parts.append(foot)

    # 3. Control Panel Keypad (Right ~25% of front surface)
    door_w = w * 0.74 - 0.005
    ctrl_w = w - door_w - 0.01
    ctrl_x = w/2.0 - ctrl_w/2.0 - 0.004
    ctrl_y = -d/2.0 - 0.001
    
    # Keypad backing frame
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ctrl_x, ctrl_y, center_z))
    keypad_back = bpy.context.active_object
    keypad_back.name = "MicrowaveControlBack"
    keypad_back.scale = (ctrl_w, 0.006, h - 0.01)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(keypad_back, keypad_mat)
    parts.append(keypad_back)

    # Green glowing digital clock display
    disp_h = h * 0.15
    disp_z = center_z + h * 0.3
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ctrl_x, ctrl_y - 0.004, disp_z))
    display = bpy.context.active_object
    display.name = "MicrowaveClockDisplay"
    display.scale = (ctrl_w * 0.76, 0.002, disp_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(display, display_mat)
    parts.append(display)

    # Dial / Button Grid below display
    dial_z = disp_z - disp_h - 0.03
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.008, location=(ctrl_x, ctrl_y - 0.004, dial_z))
    dial = bpy.context.active_object
    dial.name = "MicrowaveControlDial"
    dial.rotation_euler.x = math.radians(90)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    utils.apply_material(dial, handle_mat)
    parts.append(dial)

    # Button rows
    button_rows = 4
    button_cols = 3
    start_z = dial_z - 0.035
    row_spacing = 0.02
    col_spacing = 0.015
    
    for r in range(button_rows):
        for c in range(button_cols):
            bx = ctrl_x - ((button_cols - 1) * col_spacing) / 2.0 + c * col_spacing
            bz = start_z - r * row_spacing
            
            # Simple button rectangle
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, ctrl_y - 0.004, bz))
            btn = bpy.context.active_object
            btn.name = f"MicrowaveButton_{r}_{c}"
            btn.scale = (0.01, 0.002, 0.008)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(btn, handle_mat)
            parts.append(btn)

    # 4. Microwave Door Panel (Left ~75%)
    door_x = -w/2.0 + door_w/2.0 + 0.004
    door_y = -d/2.0 - door_thick/2.0
    door_h = h - 0.01
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y, center_z))
    door = bpy.context.active_object
    door.name = "MicrowaveDoorFrame"
    door.scale = (door_w, door_thick, door_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(door, width=0.002)
    utils.apply_material(door, body_mat)
    parts.append(door)

    # Add Glass window if requested
    if has_glass_door:
        win_w = door_w * 0.72
        win_h = door_h * 0.65
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y - 0.002, center_z))
        window = bpy.context.active_object
        window.name = "MicrowaveDoorWindow"
        window.scale = (win_w, door_thick + 0.002, win_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(window, glass_mat)
        parts.append(window)

    # Door Handle
    if style == "countertop":
        # Pull Handle: Vertical bar on the right side of the door
        hnd_x = door_x + door_w / 2.0 - 0.03
        hnd_z = center_z
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hnd_x, door_y - 0.012, hnd_z))
        hnd = bpy.context.active_object
        hnd.name = "MicrowaveDoorHandle"
        hnd.scale = (0.01, 0.01, door_h * 0.65)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(hnd, width=0.001)
        utils.apply_material(hnd, handle_mat)
        parts.append(hnd)
        
        # Handle mounts
        for mz in [hnd_z - door_h * 0.28, hnd_z + door_h * 0.28]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hnd_x, door_y - 0.006, mz))
            mount = bpy.context.active_object
            mount.name = "MicrowaveHandleMount"
            mount.scale = (0.01, 0.012, 0.01)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(mount, handle_mat)
            parts.append(mount)
    else:
        # Built-in style: door release button at the bottom of control panel
        btn_z = start_z - button_rows * row_spacing - 0.02
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ctrl_x, ctrl_y - 0.004, btn_z))
        rel_btn = bpy.context.active_object
        rel_btn.name = "MicrowaveDoorReleaseBtn"
        rel_btn.scale = (ctrl_w * 0.7, 0.004, 0.025)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(rel_btn, width=0.001)
        utils.apply_material(rel_btn, handle_mat)
        parts.append(rel_btn)

    # 5. Internal Cavity (Turntable Visible)
    # We place a thin glass turntable tray centered inside the microwave cavity space
    cavity_w = door_w * 0.8
    cavity_h = door_h * 0.8
    cavity_d = d - door_thick - 0.06
    
    turntable_z = center_z - cavity_h/2.0 + 0.01
    turntable_r = min(cavity_w, cavity_d) * 0.45
    bpy.ops.mesh.primitive_cylinder_add(radius=turntable_r, depth=0.006, location=(door_x, 0.0, turntable_z))
    turntable = bpy.context.active_object
    turntable.name = "MicrowaveTurntablePlate"
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(turntable, glass_mat)
    parts.append(turntable)

    # Join all microwave parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = master_obj
    bpy.ops.object.join()

    master_obj.name = "MicrowaveAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return master_obj

def main():
    parser = argparse.ArgumentParser(description="Procedural Microwave Generator")
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
    micro_obj = generate_microwave(params)
    
    if args.render:
        utils.setup_lighting_and_camera(micro_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
