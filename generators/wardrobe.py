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

def generate_wardrobe(params):
    w = params.get("width", 120.0) / 100.0  # convert cm to meters
    d = params.get("depth", 60.0) / 100.0
    h = params.get("height", 190.0) / 100.0
    style = params.get("style", "classic")
    has_mirror = params.get("has_mirror", False)

    parts = []

    # 1. Create Materials
    wood_mat = utils.create_material("WardrobeWood", diffuse_color=(0.28, 0.16, 0.08, 1.0), metallic=0.0, roughness=0.8)
    handle_mat = utils.create_material("WardrobeHandle", diffuse_color=(0.7, 0.55, 0.2, 1.0), metallic=0.9, roughness=0.2) # Gold/Brass
    mirror_mat = utils.create_material("WardrobeMirror", diffuse_color=(0.85, 0.85, 0.9, 1.0), metallic=0.95, roughness=0.05) # Reflective Chrome

    carcass_thick = 0.04
    base_h = 0.08

    # 2. Main Carcass Box
    carcass_z = h / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, carcass_z))
    carcass = bpy.context.active_object
    carcass.name = "WardrobeCarcass"
    carcass.scale = (w, d, h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(carcass, width=0.008)
    utils.apply_material(carcass, wood_mat)
    parts.append(carcass)

    # 3. Kicker Base Trim
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.01, base_h / 2.0))
    kicker = bpy.context.active_object
    kicker.name = "WardrobeBase"
    kicker.scale = (w - 0.02, d - 0.02, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(kicker, width=0.003)
    utils.apply_material(kicker, wood_mat)
    parts.append(kicker)

    # 4. Top Crown Trim (classic flared top molding)
    if style == "classic":
        crown_h = 0.06
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h - crown_h / 2.0))
        crown = bpy.context.active_object
        crown.name = "WardrobeCrown"
        crown.scale = (w + 0.06, d + 0.04, crown_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(crown, width=0.01)
        utils.apply_material(crown, wood_mat)
        parts.append(crown)

    # 5. Front Doors or Open Shelves
    if style == "open":
        # Create an open front inset cutout
        # We model this by building inner partitions to give the "wardrobe" visual depth without boolean cuts.
        # Vertical divider panel
        div_w = 0.02
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h/2.0 + base_h/2.0))
        divider = bpy.context.active_object
        divider.name = "WardrobeOpenDivider"
        divider.scale = (div_w, d - carcass_thick * 2.0, h - base_h - carcass_thick * 2.0)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(divider, wood_mat)
        parts.append(divider)

        # Horizontal shelves (e.g. 3 shelves on the left side)
        shelf_thick = 0.02
        shelf_w = (w - div_w - carcass_thick * 2.0) / 2.0
        shelf_x = -w / 4.0
        
        for s_idx in range(3):
            sz = base_h + (h - base_h) * (s_idx + 1) / 4.0
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(shelf_x, 0.0, sz))
            shelf = bpy.context.active_object
            shelf.name = f"WardrobeShelf_{s_idx}"
            shelf.scale = (shelf_w, d - carcass_thick * 2.0, shelf_thick)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(shelf, wood_mat)
            parts.append(shelf)

        # Clothes hanging rod on the right side
        rod_x = w / 4.0
        rod_z = h - carcass_thick - 0.15
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.012,
            depth=shelf_w,
            location=(rod_x, 0.0, rod_z)
        )
        rod = bpy.context.active_object
        rod.name = "WardrobeHangingRod"
        # Rotate along Y axis
        rod.rotation_euler = (0, math.pi/2.0, 0)
        bpy.ops.object.transform_apply(rotation=True)
        utils.apply_smooth_by_angle(rod, angle=40.0)
        # Silver steel rod
        rod_steel = utils.create_material("RodSteel", diffuse_color=(0.8, 0.8, 0.8, 1.0), metallic=0.9, roughness=0.15)
        utils.apply_material(rod, rod_steel)
        parts.append(rod)

    else:
        # Doors (Classic or Modern)
        door_w = w / 2.0 - 0.005
        door_h = h - base_h - 0.02
        door_thick = 0.025
        door_z = base_h + door_h / 2.0
        door_y = -d / 2.0 - door_thick / 2.0

        for side in [-1.0, 1.0]:
            door_x = side * (door_w / 2.0 + 0.002)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y, door_z))
            door = bpy.context.active_object
            door.name = f"WardrobeDoor_{'L' if side < 0 else 'R'}"
            door.scale = (door_w, door_thick, door_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(door, width=0.005)
            utils.apply_material(door, wood_mat)
            parts.append(door)

            # Classic style raised door panels
            if style == "classic" and not (has_mirror and side == 1.0):
                # 2 raised inset panels per door
                for panel_idx in [0, 1]:
                    panel_h = (door_h - 0.16) / 2.0
                    p_z = door_z - door_h/4.0 + (panel_idx * door_h/2.0)
                    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y - 0.006, p_z))
                    panel = bpy.context.active_object
                    panel.name = f"ClassicPanel_{'L' if side < 0 else 'R'}_{panel_idx}"
                    panel.scale = (door_w - 0.06, 0.008, panel_h)
                    bpy.ops.object.transform_apply(scale=True)
                    utils.apply_bevel(panel, width=0.002)
                    utils.apply_material(panel, wood_mat)
                    parts.append(panel)

            # Modern style vertical accent line
            elif style == "modern":
                pass

            # Center/right mirror door pane
            if has_mirror and side == 1.0:
                mirror_w = door_w - 0.08
                mirror_h = door_h - 0.12
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y - 0.004, door_z))
                mirror = bpy.context.active_object
                mirror.name = "WardrobeMirrorPane"
                mirror.scale = (mirror_w, 0.005, mirror_h)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(mirror, width=0.001)
                utils.apply_material(mirror, mirror_mat)
                parts.append(mirror)

            # Door Handles
            handle_offset_x = side * (door_w / 2.0 - 0.04)
            handle_z = door_z
            handle_y = door_y - 0.02

            if style == "classic":
                # Ornate curve handle
                # Small cylinder with beveled curve
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=0.008,
                    depth=0.12,
                    location=(handle_offset_x, handle_y, handle_z)
                )
                hnd = bpy.context.active_object
                hnd.name = f"WardrobeHandle_{'L' if side < 0 else 'R'}"
                utils.apply_smooth_by_angle(hnd, angle=40.0)
                utils.apply_material(hnd, handle_mat)
                parts.append(hnd)
                
                # Small cylinder standoffs
                for sy in [-0.05, 0.05]:
                    bpy.ops.mesh.primitive_cylinder_add(
                        radius=0.006,
                        depth=0.02,
                        location=(handle_offset_x, handle_y + 0.01, handle_z + sy)
                    )
                    stand = bpy.context.active_object
                    stand.rotation_euler = (math.pi/2.0, 0, 0)
                    bpy.ops.object.transform_apply(rotation=True)
                    utils.apply_smooth_by_angle(stand, angle=40.0)
                    utils.apply_material(stand, handle_mat)
                    parts.append(stand)

            else:
                # Modern style pull bar: long thin vertical cube
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(handle_offset_x, handle_y, handle_z))
                hnd = bpy.context.active_object
                hnd.name = f"WardrobeHandle_{'L' if side < 0 else 'R'}"
                hnd.scale = (0.015, 0.015, 0.5)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(hnd, width=0.002)
                # Modern metal handle
                utils.apply_material(hnd, handle_mat)
                parts.append(hnd)

    # Join all wardrobe parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = carcass
    bpy.ops.object.join()
    
    carcass.name = "WardrobeAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return carcass

def main():
    parser = argparse.ArgumentParser(description="Procedural Wardrobe Generator")
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
    wardrobe_obj = generate_wardrobe(params)
    
    if args.render:
        utils.setup_lighting_and_camera(wardrobe_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
