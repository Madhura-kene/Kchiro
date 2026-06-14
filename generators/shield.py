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

def generate_shield(params):
    diameter = params.get("diameter", 60.0) / 100.0  # convert cm to meters
    style = params.get("shield_style", "round")
    boss_mat_type = params.get("boss_material", "steel")
    has_rim = params.get("has_rim", True)
    
    parts = []
    
    # 1. Create Materials
    wood_mat = utils.create_material("ShieldWood", diffuse_color=(0.33, 0.20, 0.11, 1.0), metallic=0.0, roughness=0.8)
    steel_mat = utils.create_material("ShieldSteel", diffuse_color=(0.7, 0.7, 0.72, 1.0), metallic=0.9, roughness=0.25)
    brass_mat = utils.create_material("ShieldBrass", diffuse_color=(0.85, 0.65, 0.25, 1.0), metallic=0.95, roughness=0.2)
    
    # Select boss material
    if boss_mat_type == "brass":
        boss_mat = brass_mat
    elif boss_mat_type == "wood":
        boss_mat = wood_mat
    else:
        boss_mat = steel_mat
        
    radius = diameter / 2.0
    thickness = 0.03  # 3cm backing thickness
    
    if style == "round":
        # --- ROUND SHIELD ---
        # 1. Wooden Backing
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=32, 
            radius=radius, 
            depth=thickness, 
            location=(0, 0, radius),
            rotation=(math.pi / 2.0, 0, 0)
        )
        backing = bpy.context.active_object
        backing.name = "ShieldBacking"
        utils.apply_material(backing, wood_mat)
        parts.append(backing)
        
        # 2. Outer Rim Ring (Steel/Brass)
        if has_rim:
            rim_outer_r = radius + 0.012
            rim_inner_r = radius - 0.012
            rim_depth = thickness + 0.006
            
            # Create outer cylinder
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=32, 
                radius=rim_outer_r, 
                depth=rim_depth, 
                location=(0, 0, radius),
                rotation=(math.pi / 2.0, 0, 0)
            )
            outer_cyl = bpy.context.active_object
            outer_cyl.name = "RimOuter"
            
            # Create inner cutter cylinder
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=32, 
                radius=rim_inner_r, 
                depth=rim_depth * 1.5, 
                location=(0, 0, radius),
                rotation=(math.pi / 2.0, 0, 0)
            )
            inner_cyl = bpy.context.active_object
            inner_cyl.name = "RimCutter"
            
            # Perform Boolean difference
            bpy.ops.object.select_all(action='DESELECT')
            outer_cyl.select_set(True)
            bpy.context.view_layer.objects.active = outer_cyl
            
            bool_mod = outer_cyl.modifiers.new(name="RimCut", type='BOOLEAN')
            bool_mod.operation = 'DIFFERENCE'
            bool_mod.object = inner_cyl
            bpy.ops.object.modifier_apply(modifier="RimCut")
            
            # Delete cutter
            bpy.ops.object.select_all(action='DESELECT')
            inner_cyl.select_set(True)
            bpy.ops.object.delete()
            
            utils.apply_material(outer_cyl, steel_mat)
            utils.apply_bevel(outer_cyl, width=0.002)
            parts.append(outer_cyl)
            
        # 3. Center Boss Dome
        boss_radius = radius * 0.26
        boss_y = -thickness/2.0 - 0.002
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=boss_radius, 
            location=(0, boss_y, radius)
        )
        boss = bpy.context.active_object
        boss.name = "ShieldBoss"
        # Flatten dome slightly along Y
        boss.scale = (1.0, 0.5, 1.0)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_smooth_by_angle(boss, angle=35.0)
        utils.apply_material(boss, boss_mat)
        parts.append(boss)
        
    else:
        # --- HEATER SHIELD ---
        # 1. Create a grid representing shield dimensions
        height = diameter
        width = diameter * 0.8
        
        # Add a grid and align it with the XZ plane
        bpy.ops.mesh.primitive_grid_add(x_subdivisions=5, y_subdivisions=5, size=1.0, location=(0, 0, height/2.0))
        grid = bpy.context.active_object
        grid.name = "ShieldGrid"
        # Rotate to stand vertically
        grid.rotation_euler = (math.pi / 2.0, 0, 0)
        bpy.ops.object.transform_apply(rotation=True)
        
        # Scale to shield dimensions
        grid.scale = (width, 1.0, height)
        bpy.ops.object.transform_apply(scale=True)
        
        # Deform grid vertices to create heater shield outline
        for v in grid.data.vertices:
            vx, vy, vz = v.co.x, v.co.y, v.co.z
            # vz goes from 0 (bottom) to height (top)
            # Taper bottom half to a point
            taper_z_threshold = height * 0.6
            if vz < taper_z_threshold:
                taper_factor = vz / taper_z_threshold
                v.co.x = vx * taper_factor
                
            # Curve Y coordinate slightly to make shield curve forward
            curve_factor = 1.0 - (abs(vx) / (width/2.0))**2
            v.co.y = -0.06 * curve_factor * (vz / height)
            
        # Extrude/Solidify backing
        bpy.ops.object.select_all(action='DESELECT')
        grid.select_set(True)
        bpy.context.view_layer.objects.active = grid
        
        sol_mod = grid.modifiers.new(name="Solidify", type='SOLIDIFY')
        sol_mod.thickness = thickness
        sol_mod.offset = 0.0 # centered
        bpy.ops.object.modifier_apply(modifier="Solidify")
        
        utils.apply_bevel(grid, width=0.005)
        utils.apply_material(grid, wood_mat)
        parts.append(grid)
        
        # 2. Add metallic border/rim
        if has_rim:
            # We copy the grid mesh, scale it slightly, and carve it out or simplify.
            # For a reliable procedural shield rim, let's place a metallic trim lining
            # the heater shield. Alternatively, let's create a beautiful top crest.
            # Let's add a top horizontal trim beam and a central steel strip.
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -thickness/2.0 - 0.002, height - 0.015))
            top_trim = bpy.context.active_object
            top_trim.name = "TopTrim"
            top_trim.scale = (width, 0.005, 0.03)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(top_trim, steel_mat)
            utils.apply_bevel(top_trim, width=0.002)
            parts.append(top_trim)
            
        # 3. Add Steel Center Boss
        boss_radius = width * 0.18
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=boss_radius, 
            location=(0, -thickness/2.0 - 0.015, height * 0.6)
        )
        boss = bpy.context.active_object
        boss.name = "ShieldBoss"
        boss.scale = (1.0, 0.4, 1.0)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_smooth_by_angle(boss, angle=35.0)
        utils.apply_material(boss, boss_mat)
        parts.append(boss)
        
    # Join all shield parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    
    parts[0].name = "ShieldAsset"
    # Place pivot point at center ground level (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return parts[0]

def main():
    parser = argparse.ArgumentParser(description="Procedural Shield Generator")
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
    shield_obj = generate_shield(params)
    
    if args.render:
        utils.setup_lighting_and_camera(shield_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
