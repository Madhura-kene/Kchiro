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

def generate_torch(params):
    style = params.get("style", "handheld")
    shaft_len = params.get("shaft_length", 40.0) / 100.0  # convert cm to meters
    flame_sz = params.get("flame_size", 15.0) / 100.0
    
    parts = []
    
    # 1. Create Materials
    wood_mat = utils.create_material("TorchWood", diffuse_color=(0.35, 0.22, 0.12, 1.0), metallic=0.0, roughness=0.8)
    steel_mat = utils.create_material("TorchSteel", diffuse_color=(0.28, 0.28, 0.3, 1.0), metallic=0.85, roughness=0.35)
    
    # Flame material with glowing yellow-orange emission
    flame_mat = utils.create_material("TorchFlame", diffuse_color=(1.0, 0.45, 0.05, 1.0), metallic=0.0, roughness=0.2)
    flame_mat.use_nodes = True
    nodes = flame_mat.node_tree.nodes
    # Find Principal BSDF node
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        # Set emission color and strength
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (1.0, 0.5, 0.05, 1.0)
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = (1.0, 0.5, 0.05, 1.0)
            
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 2.0
            
    # 2. Wood Shaft Handle
    shaft_radius = 0.016
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12,
        radius=shaft_radius,
        depth=shaft_len,
        location=(0, 0, shaft_len / 2.0)
    )
    shaft = bpy.context.active_object
    shaft.name = "TorchShaft"
    utils.apply_smooth_by_angle(shaft, angle=40.0)
    utils.apply_material(shaft, wood_mat)
    parts.append(shaft)
    
    # 3. Metal Collars (Steel bands around wood shaft)
    # Lower band
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12,
        radius=shaft_radius + 0.003,
        depth=0.02,
        location=(0, 0, shaft_len * 0.15)
    )
    lower_band = bpy.context.active_object
    lower_band.name = "LowerBand"
    utils.apply_smooth_by_angle(lower_band, angle=40.0)
    utils.apply_material(lower_band, steel_mat)
    parts.append(lower_band)
    
    # Top collar holding the brackets
    collar_z = shaft_len - 0.03
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12,
        radius=shaft_radius + 0.004,
        depth=0.03,
        location=(0, 0, collar_z)
    )
    top_band = bpy.context.active_object
    top_band.name = "TopCollar"
    utils.apply_smooth_by_angle(top_band, angle=40.0)
    utils.apply_material(top_band, steel_mat)
    parts.append(top_band)
    
    # 4. Metal Bracket Cage (Outward flared steel straps at the top)
    cage_r = 0.04
    cage_h = 0.08
    cage_top_z = shaft_len + cage_h
    
    # Top rim ring
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=cage_r,
        depth=0.012,
        location=(0, 0, cage_top_z)
    )
    top_ring = bpy.context.active_object
    top_ring.name = "CageTopRing"
    
    # Cut center out of top ring cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=cage_r - 0.005,
        depth=0.02,
        location=(0, 0, cage_top_z)
    )
    ring_cutter = bpy.context.active_object
    ring_cutter.name = "RingCutter"
    
    bpy.ops.object.select_all(action='DESELECT')
    top_ring.select_set(True)
    bpy.context.view_layer.objects.active = top_ring
    
    b_mod = top_ring.modifiers.new(name="RingCut", type='BOOLEAN')
    b_mod.operation = 'DIFFERENCE'
    b_mod.object = ring_cutter
    bpy.ops.object.modifier_apply(modifier="RingCut")
    
    bpy.ops.object.select_all(action='DESELECT')
    ring_cutter.select_set(True)
    bpy.ops.object.delete()
    
    utils.apply_smooth_by_angle(top_ring, angle=40.0)
    utils.apply_material(top_ring, steel_mat)
    parts.append(top_ring)
    
    # 4 Vertical Rib Straps linking collar to top rim
    for i in range(4):
        angle = i * (math.pi / 2.0)
        rib_x = math.cos(angle) * (shaft_radius + cage_r) / 2.0
        rib_y = math.sin(angle) * (shaft_radius + cage_r) / 2.0
        rib_z = collar_z + (cage_h + 0.03) / 2.0
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(rib_x, rib_y, rib_z))
        rib = bpy.context.active_object
        rib.name = f"CageRib_{i}"
        
        # Scale strap
        rib.scale = (0.008, 0.005, cage_h + 0.03)
        # Rotate to match cylinder curvature
        rib.rotation_euler = (0, 0, angle)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        
        # Bend rib outward slightly at the top
        for v in rib.data.vertices:
            # Local Z goes from -h/2 to h/2
            if v.co.z > 0:
                bend_factor = v.co.z / (cage_h / 2.0)
                # push outwards radially
                rad_angle = angle
                v.co.x += math.cos(rad_angle) * 0.012 * bend_factor
                v.co.y += math.sin(rad_angle) * 0.012 * bend_factor
                
        utils.apply_bevel(rib, width=0.001)
        utils.apply_material(rib, steel_mat)
        parts.append(rib)
        
    # 5. Stylized Flame (Deformed UV sphere)
    flame_base_z = shaft_len + 0.01
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16,
        ring_count=12,
        radius=flame_sz * 0.7,
        location=(0, 0, flame_base_z + flame_sz * 0.5)
    )
    flame = bpy.context.active_object
    flame.name = "TorchFlame"
    
    # Stretched vertically
    flame.scale = (1.0, 1.0, 1.5)
    bpy.ops.object.transform_apply(scale=True)
    
    # Shape the flame to taper into a point at the top and flicker slightly
    center_z = flame_base_z + flame_sz * 0.5
    for v in flame.data.vertices:
        # Taper top vertices
        if v.co.z > center_z:
            height_t = (v.co.z - center_z) / (flame_sz * 1.5)
            taper = 1.0 - height_t
            taper = max(0.05, taper)
            v.co.x = v.co.x * taper
            v.co.y = v.co.y * taper
            
            # Add small noise/flicker warp in X/Y
            flicker_amp = 0.018 * math.sin(v.co.z * 15.0)
            v.co.x += flicker_amp * height_t
            v.co.y += flicker_amp * 0.5 * height_t
            
    utils.apply_smooth_by_angle(flame, angle=35.0)
    utils.apply_material(flame, flame_mat)
    parts.append(flame)
    
    # 6. Wall Mount Bracket (if style == wall_mounted)
    if style == "wall_mounted":
        # Wall backing plate
        plate_y = cage_r * 2.5
        plate_z = shaft_len / 2.0
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, plate_y, plate_z))
        plate = bpy.context.active_object
        plate.name = "WallPlate"
        plate.scale = (0.08, 0.008, 0.12)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(plate, width=0.002)
        utils.apply_material(plate, steel_mat)
        parts.append(plate)
        
        # Angled steel rod arm connecting plate to shaft
        arm_start = (0, plate_y, plate_z)
        arm_end = (0, shaft_radius, plate_z - 0.04)
        
        # Calculate distance and angle
        dx = arm_end[0] - arm_start[0]
        dy = arm_end[1] - arm_start[1]
        dz = arm_end[2] - arm_start[2]
        dist = math.sqrt(dx**2 + dy**2 + dz**2)
        
        rot_x = math.atan2(dy, dz)
        
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.008,
            depth=dist,
            location=(0, (arm_start[1] + arm_end[1]) / 2.0, (arm_start[2] + arm_end[2]) / 2.0),
            rotation=(rot_x, 0, 0)
        )
        arm = bpy.context.active_object
        arm.name = "BracketArm"
        utils.apply_smooth_by_angle(arm, angle=40.0)
        utils.apply_material(arm, steel_mat)
        parts.append(arm)
        
    # Join all torch parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = shaft
    bpy.ops.object.join()
    
    shaft.name = "TorchAsset"
    # Place pivot point at bottom center (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return shaft

def main():
    parser = argparse.ArgumentParser(description="Procedural Torch Generator")
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
    torch_obj = generate_torch(params)
    
    if args.render:
        utils.setup_lighting_and_camera(torch_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
