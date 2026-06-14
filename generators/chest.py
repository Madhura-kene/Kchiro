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

def generate_chest(params):
    w = params.get("width", 80.0) / 100.0  # convert cm to meters
    d = params.get("depth", 50.0) / 100.0
    h = params.get("height", 50.0) / 100.0
    lid_style = params.get("lid_style", "flat")
    has_lock = params.get("has_lock", True)
    
    parts = []
    
    # 1. Create Materials
    wood_mat = utils.create_material("ChestWood", diffuse_color=(0.33, 0.20, 0.11, 1.0), metallic=0.0, roughness=0.75)
    steel_mat = utils.create_material("ChestSteel", diffuse_color=(0.22, 0.22, 0.22, 1.0), metallic=0.85, roughness=0.35)
    brass_mat = utils.create_material("ChestBrass", diffuse_color=(0.85, 0.65, 0.25, 1.0), metallic=0.95, roughness=0.2)
    
    # 2. Chest Base Box
    # Base occupies 60% of total height
    base_h = h * 0.6
    base_z = base_h / 2.0
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, base_z))
    base = bpy.context.active_object
    base.name = "ChestBase"
    base.scale = (w, d, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(base, width=0.006)
    utils.apply_material(base, wood_mat)
    parts.append(base)
    
    # 3. Chest Lid
    lid_h = h * 0.4
    if lid_style == "arched":
        # Arched Lid (half-cylinder along X-axis)
        lid_radius = d / 2.0
        
        # Create cylinder representing the lid
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=24,
            radius=lid_radius,
            depth=w,
            location=(0, 0, base_h),
            rotation=(0, math.pi / 2.0, 0)
        )
        lid = bpy.context.active_object
        lid.name = "ChestLidArched"
        
        # Scale Y to flatten the dome slightly
        lid.scale = (1.0, 1.0, lid_h / lid_radius)
        bpy.ops.object.transform_apply(scale=True)
        
        # Create cutter box to cut bottom half of cylinder
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, base_h - lid_radius))
        cutter = bpy.context.active_object
        cutter.name = "LidCutter"
        cutter.scale = (w * 1.5, d * 1.5, lid_radius * 2.0)
        bpy.ops.object.transform_apply(scale=True)
        
        # Cut cylinder in half
        bpy.ops.object.select_all(action='DESELECT')
        lid.select_set(True)
        bpy.context.view_layer.objects.active = lid
        
        bool_mod = lid.modifiers.new(name="LidCut", type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = cutter
        bpy.ops.object.modifier_apply(modifier="LidCut")
        
        # Delete cutter
        bpy.ops.object.select_all(action='DESELECT')
        cutter.select_set(True)
        bpy.ops.object.delete()
        
        utils.apply_smooth_by_angle(lid, angle=40.0)
        utils.apply_bevel(lid, width=0.005)
        utils.apply_material(lid, wood_mat)
        parts.append(lid)
        
    else:
        # Flat Lid (beveled wood panel)
        lid_thickness = 0.04
        lid_z = base_h + (lid_thickness / 2.0)
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, lid_z))
        lid = bpy.context.active_object
        lid.name = "ChestLidFlat"
        lid.scale = (w, d, lid_thickness)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(lid, width=0.005)
        utils.apply_material(lid, wood_mat)
        parts.append(lid)
        
    # 4. Metal Trim / Straps
    # Place two steel bands on the left and right sides
    band_x_positions = [-w * 0.35, w * 0.35]
    band_width = 0.035
    band_thick = 0.004
    
    for idx, bx in enumerate(band_x_positions):
        # Front band
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, -d/2.0 - band_thick/2.0, base_h/2.0))
        f_band = bpy.context.active_object
        f_band.name = f"FrontBand_{idx}"
        f_band.scale = (band_width, band_thick, base_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(f_band, width=0.001)
        utils.apply_material(f_band, steel_mat)
        parts.append(f_band)
        
        # Back band
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, d/2.0 + band_thick/2.0, base_h/2.0))
        b_band = bpy.context.active_object
        b_band.name = f"BackBand_{idx}"
        b_band.scale = (band_width, band_thick, base_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(b_band, width=0.001)
        utils.apply_material(b_band, steel_mat)
        parts.append(b_band)
        
        # Lid band
        if lid_style == "arched":
            lid_radius = d / 2.0
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=24,
                radius=lid_radius + band_thick,
                depth=band_width,
                location=(bx, 0, base_h),
                rotation=(0, math.pi / 2.0, 0)
            )
            l_band = bpy.context.active_object
            l_band.name = f"LidBand_{idx}"
            l_band.scale = (1.0, 1.0, lid_h / lid_radius)
            bpy.ops.object.transform_apply(scale=True)
            
            # Cutter for lid band bottom half
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0, base_h - lid_radius))
            l_cutter = bpy.context.active_object
            l_cutter.scale = (band_width * 1.5, d * 1.5, lid_radius * 2.0)
            bpy.ops.object.transform_apply(scale=True)
            
            bpy.ops.object.select_all(action='DESELECT')
            l_band.select_set(True)
            bpy.context.view_layer.objects.active = l_band
            
            b_mod = l_band.modifiers.new(name="LidBandCut", type='BOOLEAN')
            b_mod.operation = 'DIFFERENCE'
            b_mod.object = l_cutter
            bpy.ops.object.modifier_apply(modifier="LidBandCut")
            
            # Delete cutter
            bpy.ops.object.select_all(action='DESELECT')
            l_cutter.select_set(True)
            bpy.ops.object.delete()
            
            utils.apply_smooth_by_angle(l_band, angle=40.0)
            utils.apply_material(l_band, steel_mat)
            parts.append(l_band)
            
        else:
            # Flat top band
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0, base_h + 0.042))
            l_band = bpy.context.active_object
            l_band.name = f"LidBandFlat_{idx}"
            l_band.scale = (band_width, d, band_thick)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(l_band, width=0.001)
            utils.apply_material(l_band, steel_mat)
            parts.append(l_band)
            
    # 5. Front Lock Box
    if has_lock:
        lock_z = base_h - 0.03
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -d/2.0 - 0.01, lock_z))
        lock = bpy.context.active_object
        lock.name = "ChestLock"
        lock.scale = (0.07, 0.015, 0.07)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(lock, width=0.002)
        utils.apply_material(lock, brass_mat)
        parts.append(lock)
        
    # Join all chest parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    
    base.name = "ChestAsset"
    # Place pivot point at center ground level (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return base

def main():
    parser = argparse.ArgumentParser(description="Procedural Chest Generator")
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
    chest_obj = generate_chest(params)
    
    if args.render:
        utils.setup_lighting_and_camera(chest_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
