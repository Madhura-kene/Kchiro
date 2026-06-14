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

def generate_helmet(params):
    style = params.get("style", "knight")
    mat_type = params.get("material", "steel")
    has_crest = params.get("has_crest", True)
    
    parts = []
    
    # 1. Create Materials
    steel_mat = utils.create_material("HelmetSteel", diffuse_color=(0.7, 0.7, 0.72, 1.0), metallic=0.9, roughness=0.25)
    brass_mat = utils.create_material("HelmetBrass", diffuse_color=(0.85, 0.65, 0.25, 1.0), metallic=0.95, roughness=0.2)
    bronze_mat = utils.create_material("HelmetBronze", diffuse_color=(0.6, 0.43, 0.25, 1.0), metallic=0.9, roughness=0.3)
    crest_mat = utils.create_material("HelmetCrest", diffuse_color=(0.8, 0.05, 0.05, 1.0), metallic=0.0, roughness=0.8) # Red plume
    horn_mat = utils.create_material("HelmetHorn", diffuse_color=(0.95, 0.90, 0.80, 1.0), metallic=0.0, roughness=0.7) # Bone/Horn
    
    # Select main material
    if mat_type == "brass":
        main_mat = brass_mat
    elif mat_type == "bronze":
        main_mat = bronze_mat
    else:
        main_mat = steel_mat
        
    # 2. Main Helmet Dome (UV Sphere cut in half)
    dome_radius = 0.14
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=32,
        ring_count=16,
        radius=dome_radius,
        location=(0, 0, 0.15)
    )
    dome = bpy.context.active_object
    dome.name = "HelmetDome"
    
    # Squash slightly to make it head-shaped (longer in Y, taller in Z)
    dome.scale = (1.0, 1.08, 1.12)
    bpy.ops.object.transform_apply(scale=True)
    
    # Cut bottom off to hollow the dome
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.32))
    cutter = bpy.context.active_object
    cutter.name = "DomeCutter"
    cutter.scale = (dome_radius * 3.0, dome_radius * 3.0, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    
    # Perform Boolean difference
    bpy.ops.object.select_all(action='DESELECT')
    dome.select_set(True)
    bpy.context.view_layer.objects.active = dome
    
    bool_mod = dome.modifiers.new(name="HollowCut", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cutter
    bpy.ops.object.modifier_apply(modifier="HollowCut")
    
    # Delete cutter
    bpy.ops.object.select_all(action='DESELECT')
    cutter.select_set(True)
    bpy.ops.object.delete()
    
    utils.apply_smooth_by_angle(dome, angle=35.0)
    utils.apply_material(dome, main_mat)
    parts.append(dome)
    
    # Re-select dome to make sure operations focus correctly
    bpy.ops.object.select_all(action='DESELECT')
    dome.select_set(True)
    bpy.context.view_layer.objects.active = dome

    # 3. Add Details Based on Style
    if style == "knight":
        # --- KNIGHT HELMET ---
        # Add a pointed/wedged faceplate visor
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -dome_radius * 0.8, 0.14))
        visor = bpy.context.active_object
        visor.name = "KnightVisor"
        visor.scale = (0.16, 0.08, 0.12)
        bpy.ops.object.transform_apply(scale=True)
        
        # Deform the front of the visor to make it wedge-shaped
        for v in visor.data.vertices:
            # Shift front vertices (y < 0) inwards in X to taper/point the front
            if v.co.y < 0:
                # Make the point sharper the further forward it is
                taper = 1.0 + (v.co.y * 3.5) # y goes from 0 to -0.04
                taper = max(0.2, taper)
                v.co.x = v.co.x * taper
                
        # Cut viewport slits (slanted small cubes)
        slit_cutters = []
        for side in [-1.0, 1.0]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 0.038, -dome_radius * 1.15, 0.17))
            slit_c = bpy.context.active_object
            slit_c.scale = (0.04, 0.015, 0.008)
            slit_c.rotation_euler = (0, side * 0.12, 0)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            slit_cutters.append(slit_c)
            
        # Cut the slits from visor
        for slit in slit_cutters:
            bpy.ops.object.select_all(action='DESELECT')
            visor.select_set(True)
            bpy.context.view_layer.objects.active = visor
            
            b_mod = visor.modifiers.new(name="SlitCut", type='BOOLEAN')
            b_mod.operation = 'DIFFERENCE'
            b_mod.object = slit
            bpy.ops.object.modifier_apply(modifier="SlitCut")
            
            # Delete slit cutter
            bpy.ops.object.select_all(action='DESELECT')
            slit.select_set(True)
            bpy.ops.object.delete()
            
        utils.apply_smooth_by_angle(visor, angle=35.0)
        utils.apply_bevel(visor, width=0.003)
        utils.apply_material(visor, brass_mat) # Brass visor on steel dome
        parts.append(visor)
        
        # Plume Crest
        if has_crest:
            # Arched plume on top center
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=24,
                radius=0.08,
                depth=0.024,
                location=(0, 0.02, 0.28),
                rotation=(0, math.pi / 2.0, 0)
            )
            plume = bpy.context.active_object
            plume.name = "KnightPlume"
            plume.scale = (1.0, 1.8, 0.4) # Make it oval mohawk
            bpy.ops.object.transform_apply(scale=True)
            
            # Cut lower half of cylinder plume
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.2))
            plume_cutter = bpy.context.active_object
            plume_cutter.scale = (0.1, 0.3, 0.1)
            bpy.ops.object.transform_apply(scale=True)
            
            bpy.ops.object.select_all(action='DESELECT')
            plume.select_set(True)
            bpy.context.view_layer.objects.active = plume
            
            b_mod = plume.modifiers.new(name="PlumeCut", type='BOOLEAN')
            b_mod.operation = 'DIFFERENCE'
            b_mod.object = plume_cutter
            bpy.ops.object.modifier_apply(modifier="PlumeCut")
            
            bpy.ops.object.select_all(action='DESELECT')
            plume_cutter.select_set(True)
            bpy.ops.object.delete()
            
            utils.apply_smooth_by_angle(plume, angle=40.0)
            utils.apply_material(plume, crest_mat)
            parts.append(plume)
            
    elif style == "spartan":
        # --- SPARTAN HELMET ---
        # Corinthian styled T-slit faceplate wrap
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -dome_radius * 0.72, 0.10))
        faceplate = bpy.context.active_object
        faceplate.name = "SpartanFaceplate"
        faceplate.scale = (0.17, 0.10, 0.18)
        bpy.ops.object.transform_apply(scale=True)
        
        # T-Cutout cutters
        # Center vertical slit
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -dome_radius * 1.2, 0.08))
        vert_c = bpy.context.active_object
        vert_c.scale = (0.024, 0.08, 0.16)
        bpy.ops.object.transform_apply(scale=True)
        
        # Left eye cutout
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.04, -dome_radius * 1.2, 0.13))
        l_eye_c = bpy.context.active_object
        l_eye_c.scale = (0.05, 0.08, 0.03)
        bpy.ops.object.transform_apply(scale=True)
        
        # Right eye cutout
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.04, -dome_radius * 1.2, 0.13))
        r_eye_c = bpy.context.active_object
        r_eye_c.scale = (0.05, 0.08, 0.03)
        bpy.ops.object.transform_apply(scale=True)
        
        # Apply cuts
        for cutter in [vert_c, l_eye_c, r_eye_c]:
            bpy.ops.object.select_all(action='DESELECT')
            faceplate.select_set(True)
            bpy.context.view_layer.objects.active = faceplate
            
            b_mod = faceplate.modifiers.new(name="SpartanCut", type='BOOLEAN')
            b_mod.operation = 'DIFFERENCE'
            b_mod.object = cutter
            bpy.ops.object.modifier_apply(modifier="SpartanCut")
            
            bpy.ops.object.select_all(action='DESELECT')
            cutter.select_set(True)
            bpy.ops.object.delete()
            
        utils.apply_smooth_by_angle(faceplate, angle=35.0)
        utils.apply_bevel(faceplate, width=0.002)
        utils.apply_material(faceplate, main_mat)
        parts.append(faceplate)
        
        # High Crest
        if has_crest:
            # Tall vertical crest holder (bronze/brass)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.02, 0.28))
            holder = bpy.context.active_object
            holder.name = "SpartanCrestHolder"
            holder.scale = (0.016, 0.22, 0.04)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(holder, main_mat)
            parts.append(holder)
            
            # Massive red plume mohawk
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.04, 0.34))
            plume = bpy.context.active_object
            plume.name = "SpartanPlume"
            plume.scale = (0.022, 0.26, 0.09)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(plume, crest_mat)
            parts.append(plume)
            
    elif style == "viking":
        # --- VIKING HELMET ---
        # Spectacle eyeguard mask
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -dome_radius * 0.8, 0.14))
        mask = bpy.context.active_object
        mask.name = "VikingMask"
        mask.scale = (0.18, 0.04, 0.08)
        bpy.ops.object.transform_apply(scale=True)
        
        # Eye holes cutouts
        l_eye = bpy.ops.mesh.primitive_cylinder_add(
            radius=0.024,
            depth=0.1,
            location=(-0.038, -dome_radius * 1.1, 0.14),
            rotation=(math.pi / 2.0, 0, 0)
        )
        l_eye_c = bpy.context.active_object
        
        r_eye = bpy.ops.mesh.primitive_cylinder_add(
            radius=0.024,
            depth=0.1,
            location=(0.038, -dome_radius * 1.1, 0.14),
            rotation=(math.pi / 2.0, 0, 0)
        )
        r_eye_c = bpy.context.active_object
        
        for cutter in [l_eye_c, r_eye_c]:
            bpy.ops.object.select_all(action='DESELECT')
            mask.select_set(True)
            bpy.context.view_layer.objects.active = mask
            
            b_mod = mask.modifiers.new(name="EyeCut", type='BOOLEAN')
            b_mod.operation = 'DIFFERENCE'
            b_mod.object = cutter
            bpy.ops.object.modifier_apply(modifier="EyeCut")
            
            bpy.ops.object.select_all(action='DESELECT')
            cutter.select_set(True)
            bpy.ops.object.delete()
            
        utils.apply_smooth_by_angle(mask, angle=35.0)
        utils.apply_bevel(mask, width=0.002)
        utils.apply_material(mask, steel_mat if mat_type != "steel" else brass_mat) # Accent color
        parts.append(mask)
        
        # Viking Horns
        if has_crest:
            for side in [-1.0, 1.0]:
                # Horn base/socket
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=12,
                    radius=0.018,
                    depth=0.025,
                    location=(side * 0.11, 0.0, 0.22),
                    rotation=(0, side * 0.5, 0)
                )
                socket = bpy.context.active_object
                socket.name = f"HornSocket_{'R' if side > 0 else 'L'}"
                utils.apply_material(socket, main_mat)
                parts.append(socket)
                
                # Horn curve (extruded/slanted cylinder)
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=12,
                    radius=0.014,
                    depth=0.12,
                    location=(side * 0.15, 0.0, 0.27),
                    rotation=(0, side * 0.8, 0)
                )
                horn = bpy.context.active_object
                horn.name = f"VikingHorn_{'R' if side > 0 else 'L'}"
                
                # Deform horn to taper to a point
                for v in horn.data.vertices:
                    # Taper the end (z > 0 in local space)
                    if v.co.z > 0:
                        t = 1.0 - (v.co.z / 0.06)
                        t = max(0.1, t)
                        v.co.x = v.co.x * t
                        v.co.y = v.co.y * t
                        
                utils.apply_smooth_by_angle(horn, angle=30.0)
                utils.apply_material(horn, horn_mat)
                parts.append(horn)
                
    # Join all helmet parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = dome
    bpy.ops.object.join()
    
    dome.name = "HelmetAsset"
    # Place pivot point at bottom center (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return dome

def main():
    parser = argparse.ArgumentParser(description="Procedural Helmet Generator")
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
    helmet_obj = generate_helmet(params)
    
    if args.render:
        utils.setup_lighting_and_camera(helmet_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
