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

def generate_storage(params):
    style = params.get("style", "shelf")
    w = params.get("width", 100.0) / 100.0  # convert cm to meters
    d = params.get("depth", 40.0) / 100.0
    h = params.get("height", 160.0) / 100.0
    num_shelves = params.get("num_shelves", 3)
    has_doors = params.get("has_doors", False)
    
    # Auto-adjust doors for wardrobe/cabinet if not specified
    if style in ["wardrobe", "cabinet"] and "has_doors" not in params:
        has_doors = True
        
    parts = []
    
    # 1. Create Materials
    wood_mat = utils.create_material("StorageWood", diffuse_color=(0.33, 0.22, 0.13, 1.0), metallic=0.0, roughness=0.7) # Cherry wood
    metal_mat = utils.create_material("StorageMetal", diffuse_color=(0.7, 0.7, 0.72, 1.0), metallic=0.9, roughness=0.25) # Steel
    
    # Thickness specifications
    thick = 0.024 # 2.4cm panel thickness
    leg_h = 0.08
    body_h = h - leg_h
    body_z = leg_h + (body_h / 2.0)
    
    # 2. Left and Right Side Panels
    side_panel_w = thick
    side_panel_d = d
    side_panel_h = body_h
    
    for side in [-1.0, 1.0]:
        px = side * ((w / 2.0) - (thick / 2.0))
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, 0, body_z))
        panel = bpy.context.active_object
        panel.name = f"StorageSidePanel_{'L' if side < 0 else 'R'}"
        panel.scale = (side_panel_w, side_panel_d, side_panel_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(panel, width=0.003)
        utils.apply_material(panel, wood_mat)
        parts.append(panel)
        
    # 3. Top and Bottom Panels
    top_bottom_w = w - (2.0 * thick)
    top_bottom_d = d
    top_bottom_h = thick
    
    for level in [leg_h + (thick / 2.0), h - (thick / 2.0)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, level))
        panel = bpy.context.active_object
        panel.name = f"StorageHorizontalPanel_{'Top' if level > h/2 else 'Bottom'}"
        panel.scale = (top_bottom_w, top_bottom_d, top_bottom_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(panel, width=0.003)
        utils.apply_material(panel, wood_mat)
        parts.append(panel)
        
    # 4. Backing Board (thin wood sheet covering the rear)
    back_thick = 0.006
    back_y = (d / 2.0) - (back_thick / 2.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, back_y, body_z))
    backing = bpy.context.active_object
    backing.name = "StorageBacking"
    backing.scale = (w, back_thick, body_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(backing, wood_mat)
    parts.append(backing)
    
    # 5. Shelves
    # Space between bottom panel and top panel
    inner_h = body_h - (2.0 * thick)
    inner_bottom = leg_h + thick
    
    for i in range(num_shelves):
        # Evenly distribute shelves inside cabinet
        shelf_z = inner_bottom + ((i + 1) * (inner_h / (num_shelves + 1)))
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -back_thick, shelf_z))
        shelf = bpy.context.active_object
        shelf.name = f"StorageShelf_{i}"
        # Slightly cut back in Y so doors can close flush
        shelf.scale = (top_bottom_w - 0.004, d - (thick * 1.5), thick)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(shelf, width=0.002)
        utils.apply_material(shelf, wood_mat)
        parts.append(shelf)
        
    # 6. Doors & Handles (Cabinet / Wardrobe styles)
    if has_doors:
        door_w = (w / 2.0) - 0.004
        door_thick = 0.018
        door_y = -(d / 2.0) - (door_thick / 2.0)
        
        for side in [-1.0, 1.0]:
            door_x = side * (door_w / 2.0 + 0.002)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_x, door_y, body_z))
            door = bpy.context.active_object
            door.name = f"StorageDoor_{'L' if side < 0 else 'R'}"
            door.scale = (door_w, door_thick, body_h - 0.008)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(door, width=0.002)
            utils.apply_material(door, wood_mat)
            parts.append(door)
            
            # Steel door handles
            handle_x = side * 0.025 # Near center split
            handle_y = door_y - door_thick/2.0 - 0.012
            handle_z = body_z # Mid height
            
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8,
                radius=0.006,
                depth=0.12,
                location=(handle_x, handle_y, handle_z)
            )
            handle = bpy.context.active_object
            handle.name = f"StorageDoorHandle_{'L' if side < 0 else 'R'}"
            utils.apply_smooth_by_angle(handle, angle=40.0)
            utils.apply_material(handle, metal_mat)
            parts.append(handle)
            
    # 7. Corner Legs
    leg_offset_x = (w / 2.0) - 0.04
    leg_offset_y = (d / 2.0) - 0.04
    
    for lx in [-leg_offset_x, leg_offset_x]:
        for ly in [-leg_offset_y, leg_offset_y]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, leg_h / 2.0))
            leg = bpy.context.active_object
            leg.name = f"StorageLeg_{'L' if lx < 0 else 'R'}_{'F' if ly < 0 else 'B'}"
            leg.scale = (0.04, 0.04, leg_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(leg, width=0.002)
            utils.apply_material(leg, wood_mat)
            parts.append(leg)
            
    # Join all storage parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = backing
    bpy.ops.object.join()
    
    backing.name = "StorageAsset"
    # Place pivot point at bottom center (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return backing

def main():
    parser = argparse.ArgumentParser(description="Procedural Storage Unit Generator")
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
    storage_obj = generate_storage(params)
    
    if args.render:
        utils.setup_lighting_and_camera(storage_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
