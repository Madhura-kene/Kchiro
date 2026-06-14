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

def generate_fridge(params):
    w = params.get("width", 75.0) / 100.0  # convert cm to meters
    d = params.get("depth", 70.0) / 100.0
    h = params.get("height", 180.0) / 100.0
    style = params.get("style", "double_door")
    material_type = params.get("material", "stainless_steel")
    has_dispenser = params.get("has_dispenser", False)

    parts = []

    # 1. Setup Materials
    if material_type == "white":
        body_color = (0.95, 0.95, 0.95, 1.0)
        metallic_body = 0.0
        rough_body = 0.4
    elif material_type == "black_matte":
        body_color = (0.12, 0.12, 0.13, 1.0)
        metallic_body = 0.0
        rough_body = 0.6
    else: # stainless_steel
        body_color = (0.85, 0.85, 0.87, 1.0)
        metallic_body = 0.9
        rough_body = 0.2

    body_mat = utils.create_material("FridgeBody", diffuse_color=body_color, metallic=metallic_body, roughness=rough_body)
    handle_mat = utils.create_material("FridgeHandle", diffuse_color=(0.8, 0.8, 0.82, 1.0), metallic=0.9, roughness=0.2)
    accent_mat = utils.create_material("FridgeAccent", diffuse_color=(0.08, 0.08, 0.08, 1.0), metallic=0.0, roughness=0.45)

    base_h = 0.05
    box_h = h - base_h
    box_z = base_h + box_h / 2.0
    door_thick = 0.04
    gap = 0.005

    # 2. Refrigerator Carcass Box
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, door_thick / 2.0, box_z))
    carcass = bpy.context.active_object
    carcass.name = "FridgeCarcass"
    carcass.scale = (w, d - door_thick, box_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(carcass, width=0.006)
    utils.apply_material(carcass, body_mat)
    parts.append(carcass)
    master_obj = carcass

    # Bottom kicker plate
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.01, base_h / 2.0))
    kicker = bpy.context.active_object
    kicker.name = "FridgeKicker"
    kicker.scale = (w - 0.01, d - 0.02, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(kicker, accent_mat)
    parts.append(kicker)

    # 3. Doors & Handles
    door_y = -d / 2.0 + door_thick / 2.0
    
    if style == "single_door":
        # One large vertical door
        door_w = w - 0.004
        door_h = box_h - 0.01
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, door_y, base_h + door_h/2.0 + 0.005))
        door = bpy.context.active_object
        door.name = "FridgeDoor"
        door.scale = (door_w, door_thick, door_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(door, width=0.005)
        utils.apply_material(door, body_mat)
        parts.append(door)

        # Single long vertical handle (offset to the right for left-hand pull)
        handle_x = w / 2.0 - 0.06
        handle_z = base_h + door_h / 2.0
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(handle_x, door_y - 0.015, handle_z))
        hnd = bpy.context.active_object
        hnd.name = "FridgeDoorHandle"
        hnd.scale = (0.015, 0.015, door_h * 0.4)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(hnd, width=0.002)
        utils.apply_material(hnd, handle_mat)
        parts.append(hnd)

        # Handle mounts
        for hz in [handle_z - door_h * 0.2, handle_z + door_h * 0.2]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(handle_x, door_y - 0.007, hz))
            mnt = bpy.context.active_object
            mnt.name = "FridgeHandleMount"
            mnt.scale = (0.015, 0.015, 0.02)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(mnt, handle_mat)
            parts.append(mnt)

    elif style == "double_door":
        # Split top freezer, bottom fridge
        freezer_ratio = 0.35
        freezer_h = box_h * freezer_ratio - gap
        fridge_h = box_h * (1.0 - freezer_ratio) - gap

        fridge_z = base_h + fridge_h / 2.0
        freezer_z = base_h + fridge_h + gap + freezer_h / 2.0

        # Bottom Fridge Door
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, door_y, fridge_z))
        door_bot = bpy.context.active_object
        door_bot.name = "FridgeDoorBottom"
        door_bot.scale = (w - 0.004, door_thick, fridge_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(door_bot, width=0.005)
        utils.apply_material(door_bot, body_mat)
        parts.append(door_bot)

        # Top Freezer Door
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, door_y, freezer_z))
        door_top = bpy.context.active_object
        door_top.name = "FridgeDoorTop"
        door_top.scale = (w - 0.004, door_thick, freezer_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(door_top, width=0.005)
        utils.apply_material(door_top, body_mat)
        parts.append(door_top)

        # Bottom door vertical handle
        handle_x = w / 2.0 - 0.06
        handle_z = fridge_z
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(handle_x, door_y - 0.015, handle_z))
        hnd_bot = bpy.context.active_object
        hnd_bot.name = "FridgeHandleBottom"
        hnd_bot.scale = (0.015, 0.015, fridge_h * 0.45)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(hnd_bot, width=0.002)
        utils.apply_material(hnd_bot, handle_mat)
        parts.append(hnd_bot)

        # Bottom handle mounts
        for hz in [handle_z - fridge_h * 0.225, handle_z + fridge_h * 0.225]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(handle_x, door_y - 0.007, hz))
            mnt = bpy.context.active_object
            mnt.scale = (0.015, 0.015, 0.02)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(mnt, handle_mat)
            parts.append(mnt)

        # Top door vertical handle
        handle_z_top = freezer_z - freezer_h * 0.15
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(handle_x, door_y - 0.015, handle_z_top))
        hnd_top = bpy.context.active_object
        hnd_top.name = "FridgeHandleTop"
        hnd_top.scale = (0.015, 0.015, freezer_h * 0.5)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(hnd_top, width=0.002)
        utils.apply_material(hnd_top, handle_mat)
        parts.append(hnd_top)

        # Top handle mounts
        for hz in [handle_z_top - freezer_h * 0.25, handle_z_top + freezer_h * 0.25]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(handle_x, door_y - 0.007, hz))
            mnt = bpy.context.active_object
            mnt.scale = (0.015, 0.015, 0.02)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(mnt, handle_mat)
            parts.append(mnt)

    else: # french_door
        # Side-by-side upper doors, bottom pullout drawer
        drawer_ratio = 0.35
        drawer_h = box_h * drawer_ratio - gap
        upper_h = box_h * (1.0 - drawer_ratio) - gap

        drawer_z = base_h + drawer_h / 2.0
        upper_z = base_h + drawer_h + gap + upper_h / 2.0
        upper_door_w = w / 2.0 - 0.003

        # Bottom Drawer Door
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, door_y, drawer_z))
        drawer = bpy.context.active_object
        drawer.name = "FridgeDrawer"
        drawer.scale = (w - 0.004, door_thick, drawer_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(drawer, width=0.005)
        utils.apply_material(drawer, body_mat)
        parts.append(drawer)

        # Horizontal drawer handle
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, door_y - 0.015, drawer_z))
        hnd_draw = bpy.context.active_object
        hnd_draw.name = "FridgeDrawerHandle"
        hnd_draw.scale = (w * 0.6, 0.015, 0.015)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(hnd_draw, width=0.002)
        utils.apply_material(hnd_draw, handle_mat)
        parts.append(hnd_draw)

        # Drawer handle mounts
        for hx in [-w * 0.25, w * 0.25]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx, door_y - 0.007, drawer_z))
            mnt = bpy.context.active_object
            mnt.scale = (0.015, 0.015, 0.02)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(mnt, handle_mat)
            parts.append(mnt)

        # Left Upper Door
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-upper_door_w/2.0 - 0.001, door_y, upper_z))
        door_l = bpy.context.active_object
        door_l.name = "FridgeDoorL"
        door_l.scale = (upper_door_w, door_thick, upper_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(door_l, width=0.005)
        utils.apply_material(door_l, body_mat)
        parts.append(door_l)

        # Right Upper Door
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(upper_door_w/2.0 + 0.001, door_y, upper_z))
        door_r = bpy.context.active_object
        door_r.name = "FridgeDoorR"
        door_r.scale = (upper_door_w, door_thick, upper_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(door_r, width=0.005)
        utils.apply_material(door_r, body_mat)
        parts.append(door_r)

        # Left Vertical handle
        hx_l = -0.02
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx_l, door_y - 0.015, upper_z))
        hnd_l = bpy.context.active_object
        hnd_l.name = "FridgeHandleL"
        hnd_l.scale = (0.015, 0.015, upper_h * 0.5)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(hnd_l, width=0.002)
        utils.apply_material(hnd_l, handle_mat)
        parts.append(hnd_l)

        # Left handle mounts
        for hz in [upper_z - upper_h * 0.25, upper_z + upper_h * 0.25]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx_l, door_y - 0.007, hz))
            mnt = bpy.context.active_object
            mnt.scale = (0.015, 0.015, 0.02)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(mnt, handle_mat)
            parts.append(mnt)

        # Right Vertical handle
        hx_r = 0.02
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx_r, door_y - 0.015, upper_z))
        hnd_r = bpy.context.active_object
        hnd_r.name = "FridgeHandleR"
        hnd_r.scale = (0.015, 0.015, upper_h * 0.5)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(hnd_r, width=0.002)
        utils.apply_material(hnd_r, handle_mat)
        parts.append(hnd_r)

        # Right handle mounts
        for hz in [upper_z - upper_h * 0.25, upper_z + upper_h * 0.25]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx_r, door_y - 0.007, hz))
            mnt = bpy.context.active_object
            mnt.scale = (0.015, 0.015, 0.02)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(mnt, handle_mat)
            parts.append(mnt)

    # 4. Optional Dispenser
    if has_dispenser:
        # Position dispenser on the single door or left upper door
        disp_x = -w / 4.0 if style == "french_door" else 0.0
        disp_h = 0.24
        disp_w = 0.16
        disp_d = 0.03
        disp_z = h * 0.55
        
        # dispenser frame/niche (inset slightly)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(disp_x, door_y - door_thick/2.0 + 0.002, disp_z))
        disp_niche = bpy.context.active_object
        disp_niche.name = "FridgeDispenserNiche"
        disp_niche.scale = (disp_w, disp_d, disp_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(disp_niche, width=0.002)
        utils.apply_material(disp_niche, accent_mat)
        parts.append(disp_niche)

        # dispenser pad/lever
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(disp_x, door_y - door_thick/2.0 - 0.006, disp_z))
        disp_pad = bpy.context.active_object
        disp_pad.name = "FridgeDispenserPaddle"
        disp_pad.scale = (0.03, 0.006, 0.08)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(disp_pad, handle_mat)
        parts.append(disp_pad)

    # 5. Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = master_obj
    bpy.ops.object.join()

    master_obj.name = "FridgeAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return master_obj

def main():
    parser = argparse.ArgumentParser(description="Procedural Fridge Generator")
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
    fridge_obj = generate_fridge(params)
    
    if args.render:
        utils.setup_lighting_and_camera(fridge_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
