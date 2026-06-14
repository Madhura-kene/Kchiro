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

def generate_countertop(params):
    w = params.get("width", 120.0) / 100.0  # convert cm to meters
    d = params.get("depth", 60.0) / 100.0
    h = params.get("height", 90.0) / 100.0
    has_drawers = params.get("has_drawers", True)
    has_backsplash = params.get("has_backsplash", True)
    material_type = params.get("material", "marble")

    parts = []

    # 1. Setup Materials
    # Countertop slab surface material
    if material_type == "granite":
        counter_color = (0.15, 0.15, 0.16, 1.0) # Dark Charcoal
        counter_metallic = 0.2
        counter_roughness = 0.12
        carcass_color = (0.92, 0.92, 0.92, 1.0) # White cabinet body
    elif material_type == "wood":
        counter_color = (0.45, 0.25, 0.12, 1.0) # Oak Butcher Block
        counter_metallic = 0.0
        counter_roughness = 0.55
        carcass_color = (0.15, 0.15, 0.16, 1.0) # Dark Charcoal cabinet body
    else: # marble
        counter_color = (0.92, 0.92, 0.94, 1.0) # Polished White Marble
        counter_metallic = 0.1
        counter_roughness = 0.08
        carcass_color = (0.18, 0.18, 0.2, 1.0) # Modern Slate Gray cabinet body

    counter_mat = utils.create_material("CounterTopSlab", diffuse_color=counter_color, metallic=counter_metallic, roughness=counter_roughness)
    carcass_mat = utils.create_material("CounterCabinetBody", diffuse_color=carcass_color, metallic=0.0, roughness=0.5)
    handle_mat = utils.create_material("CounterHandle", diffuse_color=(0.82, 0.82, 0.84, 1.0), metallic=0.95, roughness=0.15)
    kick_mat = utils.create_material("CounterBase", diffuse_color=(0.08, 0.08, 0.08, 1.0), metallic=0.1, roughness=0.55)

    counter_thick = 0.04
    cabinet_h = h - counter_thick
    cabinet_z = cabinet_h / 2.0
    kicker_h = 0.08
    gap = 0.005

    # 2. Base Cabinet Carcass
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, cabinet_z))
    carcass = bpy.context.active_object
    carcass.name = "CountertopCabinet"
    carcass.scale = (w, d, cabinet_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(carcass, width=0.005)
    utils.apply_material(carcass, carcass_mat)
    parts.append(carcass)
    master_obj = carcass

    # Bottom recessed kickplate
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.015, kicker_h / 2.0))
    kickplate = bpy.context.active_object
    kickplate.name = "CountertopKickplate"
    kickplate.scale = (w - 0.02, d - 0.03, kicker_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(kickplate, kick_mat)
    parts.append(kickplate)

    # 3. Top Countertop Slab
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h - counter_thick/2.0))
    slab = bpy.context.active_object
    slab.name = "CountertopSlab"
    slab.scale = (w + 0.008, d + 0.008, counter_thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(slab, width=0.004)
    utils.apply_material(slab, counter_mat)
    parts.append(slab)

    # Backsplash
    if has_backsplash:
        splash_h = 0.1
        splash_t = 0.02
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, d/2.0 + 0.004 - splash_t/2.0, h + splash_h/2.0))
        splash = bpy.context.active_object
        splash.name = "CountertopBacksplash"
        splash.scale = (w + 0.008, splash_t, splash_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(splash, width=0.002)
        utils.apply_material(splash, counter_mat)
        parts.append(splash)

    # 4. Drawers or Doors Panels Grid
    face_y = -d/2.0 - 0.008
    panel_thick = 0.018
    grid_h = cabinet_h - kicker_h - 0.02
    grid_w = w - 0.02
    grid_z = kicker_h + grid_h / 2.0 + 0.01

    if has_drawers:
        # Determine columns count (1 or 2 based on width)
        cols = 2 if w > 1.2 else 1
        rows = 3
        
        ph = (grid_h - gap * (rows - 1)) / rows
        pw = (grid_w - gap * (cols - 1)) / cols
        
        for r in range(rows):
            for c in range(cols):
                # Calculate coordinates
                dx = -grid_w/2.0 + c * (pw + gap) + pw/2.0
                dz = kicker_h + 0.01 + r * (ph + gap) + ph/2.0
                
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, face_y, dz))
                panel = bpy.context.active_object
                panel.name = f"CountertopDrawer_{r}_{c}"
                panel.scale = (pw, panel_thick, ph)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(panel, width=0.002)
                utils.apply_material(panel, carcass_mat)
                parts.append(panel)
                
                # Horizontal drawer handles
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, face_y - 0.01, dz))
                hnd = bpy.context.active_object
                hnd.name = f"CountertopDrawerHandle_{r}_{c}"
                hnd.scale = (pw * 0.45, 0.01, 0.012)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(hnd, width=0.001)
                utils.apply_material(hnd, handle_mat)
                parts.append(hnd)
                
                # Handle mounts
                for hx in [dx - pw * 0.2, dx + pw * 0.2]:
                    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx, (face_y + face_y - 0.01)/2.0, dz))
                    mnt = bpy.context.active_object
                    mnt.scale = (0.01, abs(face_y - (face_y - 0.01)), 0.012)
                    bpy.ops.object.transform_apply(scale=True)
                    utils.apply_material(mnt, handle_mat)
                    parts.append(mnt)
    else:
        # Standard double cabinet doors
        door_w = grid_w / 2.0 - 0.002
        door_h = grid_h
        
        # Left Door
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-door_w/2.0 - 0.001, face_y, grid_z))
        door_l = bpy.context.active_object
        door_l.name = "CountertopDoorL"
        door_l.scale = (door_w, panel_thick, door_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(door_l, width=0.002)
        utils.apply_material(door_l, carcass_mat)
        parts.append(door_l)

        # Right Door
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_w/2.0 + 0.001, face_y, grid_z))
        door_r = bpy.context.active_object
        door_r.name = "CountertopDoorR"
        door_r.scale = (door_w, panel_thick, door_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(door_r, width=0.002)
        utils.apply_material(door_r, carcass_mat)
        parts.append(door_r)

        # Vertical bar handles near center split
        h_y = face_y - 0.01
        for dx in [-0.02, 0.02]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, h_y, grid_z))
            hnd = bpy.context.active_object
            hnd.name = "CountertopDoorHandle"
            hnd.scale = (0.012, 0.01, door_h * 0.35)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(hnd, width=0.0015)
            utils.apply_material(hnd, handle_mat)
            parts.append(hnd)
            
            # Mounts
            for mz in [grid_z - door_h * 0.12, grid_z + door_h * 0.12]:
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, (face_y + h_y)/2.0, mz))
                mnt = bpy.context.active_object
                mnt.scale = (0.012, abs(face_y - h_y), 0.01)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_material(mnt, handle_mat)
                parts.append(mnt)

    # 5. Join all parts into one countertop asset
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = master_obj
    bpy.ops.object.join()

    master_obj.name = "CountertopAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return master_obj

def main():
    parser = argparse.ArgumentParser(description="Procedural Countertop Generator")
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
    counter_obj = generate_countertop(params)
    
    if args.render:
        utils.setup_lighting_and_camera(counter_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
