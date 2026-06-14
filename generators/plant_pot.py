import os
import sys
import json
import argparse
import math

# Setup path to import backend and utils
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

def generate_plant_pot(params):
    w = params.get("width", 30.0) / 100.0   # cm to m
    h = params.get("height", 30.0) / 100.0  # cm to m
    shape = params.get("shape", "cylindrical")
    mat_type = params.get("material", "terracotta")
    has_plant = params.get("has_plant", True)

    parts = []

    # 1. Materials
    if mat_type == "terracotta":
        pot_mat = utils.create_material("PotTerracotta", diffuse_color=(0.7, 0.35, 0.2, 1.0), metallic=0.0, roughness=0.85)
    elif mat_type == "ceramic":
        pot_mat = utils.create_material("PotCeramic", diffuse_color=(0.95, 0.95, 0.95, 1.0), metallic=0.0, roughness=0.1)
    elif mat_type == "wood":
        pot_mat = utils.create_material("PotWood", diffuse_color=(0.32, 0.2, 0.1, 1.0), metallic=0.0, roughness=0.7)
    else: # plastic
        pot_mat = utils.create_material("PotPlastic", diffuse_color=(0.18, 0.18, 0.18, 1.0), metallic=0.1, roughness=0.45)

    soil_mat = utils.create_material("PotSoil", diffuse_color=(0.15, 0.1, 0.07, 1.0), metallic=0.0, roughness=0.95)
    stem_mat = utils.create_material("PlantStem", diffuse_color=(0.28, 0.48, 0.18, 1.0), metallic=0.0, roughness=0.6)
    leaf_mat = utils.create_material("PlantLeaf", diffuse_color=(0.22, 0.58, 0.14, 1.0), metallic=0.0, roughness=0.4)

    # 2. Build Container
    pot_z = h / 2.0
    r_top = w / 2.0
    
    if shape == "cylindrical":
        # Tapered cylinder: upper radius = r_top, lower radius = r_top * 0.78
        # We can construct it via a cone or cylinder scaling
        bpy.ops.mesh.primitive_cone_add(
            vertices=32,
            radius1=r_top * 0.78,
            radius2=r_top,
            depth=h,
            location=(0, 0, pot_z)
        )
        pot = bpy.context.active_object
        pot.name = "PotContainer_Circ"
        utils.apply_smooth_by_angle(pot, angle=30.0)
        utils.apply_bevel(pot, width=0.005)
        utils.apply_material(pot, pot_mat)
        parts.append(pot)

    elif shape == "square":
        # Tapered box: we will construct a cube and scale the bottom face, or stack cube segments
        # Let's stack cube segments or just use a cube and taper it manually
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, pot_z))
        pot = bpy.context.active_object
        pot.name = "PotContainer_Square"
        pot.scale = (w, w, h)
        bpy.ops.object.transform_apply(scale=True)
        
        # Taper the bottom vertices
        # Enter edit mode, select bottom vertices (z <= 0.01), scale down by 0.8
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        for vert in pot.data.vertices:
            if vert.co.z < 0.01:
                vert.co.x *= 0.8
                vert.co.y *= 0.8
        
        utils.apply_bevel(pot, width=0.005)
        utils.apply_material(pot, pot_mat)
        parts.append(pot)

    else: # rounded / bulbous
        # Bulged cylinder
        # Create a sphere-like structure or cylinder scaled at center
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=32,
            radius=r_top,
            depth=h,
            location=(0, 0, pot_z)
        )
        pot = bpy.context.active_object
        pot.name = "PotContainer_Round"
        
        # Add slight bulge in center vertices
        for vert in pot.data.vertices:
            # Distance from center vertical height (center_z = h/2)
            dist_from_mid = abs(vert.co.z - pot_z)
            factor = 1.0 - (dist_from_mid / (h / 2.0)) # 1.0 in center, 0.0 at top/bottom
            # Bulge out by 15% in middle
            bulge_val = 1.0 + 0.15 * factor
            vert.co.x *= bulge_val
            vert.co.y *= bulge_val
            
        utils.apply_smooth_by_angle(pot, angle=30.0)
        utils.apply_bevel(pot, width=0.005)
        utils.apply_material(pot, pot_mat)
        parts.append(pot)

    # 3. Hollow out Pot (Solidify modifier)
    bpy.ops.object.select_all(action='DESELECT')
    pot.select_set(True)
    bpy.context.view_layer.objects.active = pot
    
    solidify = pot.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.015  # 1.5 cm thick walls
    bpy.ops.object.modifier_apply(modifier="Solidify")

    # 4. Fill Soil inside container (placed 3cm down from top rim)
    soil_z = h - 0.035
    soil_r = r_top - 0.02
    
    if shape == "square":
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, soil_z))
        soil = bpy.context.active_object
        soil.name = "PotSoil"
        soil.scale = (w - 0.035, w - 0.035, 0.01)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(soil, soil_mat)
        parts.append(soil)
    else:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=32,
            radius=soil_r,
            depth=0.01,
            location=(0, 0, soil_z),
            rotation=(0, 0, 0)
        )
        soil = bpy.context.active_object
        soil.name = "PotSoil"
        utils.apply_smooth_by_angle(soil, angle=30.0)
        utils.apply_material(soil, soil_mat)
        parts.append(soil)

    # 5. Sprout stylized houseplant (stem + leaves)
    if has_plant:
        # Stem starts at soil center, goes up and tilts slightly
        stem_h = h * 0.95
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.007,
            depth=stem_h,
            location=(0, 0, soil_z + stem_h / 2.0)
        )
        stem = bpy.context.active_object
        stem.name = "PlantStem"
        
        # Tilt and curve the stem slightly
        for vert in stem.data.vertices:
            # Curve Z coordinate: top tilts to the right/front
            factor = (vert.co.z - (soil_z)) / stem_h
            if factor > 0:
                vert.co.x += 0.03 * factor * factor
                vert.co.y += 0.02 * factor * factor
                
        utils.apply_smooth_by_angle(stem, angle=30.0)
        utils.apply_material(stem, stem_mat)
        parts.append(stem)

        # Sprout 8 leaves branching outwards
        num_leaves = 8
        for i in range(num_leaves):
            t = (i + 1) / (num_leaves + 1) # height factor along the stem: 0.1 to 0.9
            leaf_z = soil_z + t * stem_h
            
            # Find horizontal coordinates of the stem at this height
            stem_offset_x = 0.03 * t * t
            stem_offset_y = 0.02 * t * t
            
            # Radiate leaves in different directions
            angle = (i * 137.5) * math.pi / 180.0 # golden angle distribution
            
            leaf_len = w * 0.45 * (1.2 - t * 0.4) # leaf gets smaller near the top
            leaf_w = leaf_len * 0.4
            
            # Position leaf center slightly offset from the stem
            leaf_dist = leaf_len / 2.2
            lx = stem_offset_x + leaf_dist * math.cos(angle)
            ly = stem_offset_y + leaf_dist * math.sin(angle)
            
            # Spherical leaf segment
            bpy.ops.mesh.primitive_uv_sphere_add(
                segments=16,
                ring_count=12,
                radius=1.0,
                location=(lx, ly, leaf_z)
            )
            leaf = bpy.context.active_object
            leaf.name = f"PlantLeaf_{i}"
            
            # Flatten, stretch, and orient the leaf
            leaf.scale = (leaf_w, leaf_len, 0.003)
            # Tilt leaf upwards: rotation around local X/Y depending on angle
            # In Blender, we can apply rotation to align Y-axis of sphere with branch direction
            leaf.rotation_euler = (math.radians(20.0), 0, angle - math.pi / 2.0)
            bpy.ops.object.transform_apply(rotation=True, scale=True)
            
            utils.apply_smooth_by_angle(leaf, angle=30.0)
            utils.apply_material(leaf, leaf_mat)
            parts.append(leaf)

    # 6. Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    
    parts[0].name = "PlantPotAsset"
    
    # Bounding box base origin
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return parts[0]

def main():
    parser = argparse.ArgumentParser(description="Procedural Plant Pot Generator")
    parser.add_argument("--params", type=str, required=True, help="Path to JSON parameters file")
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
    pot_obj = generate_plant_pot(params)
    
    if args.render:
        utils.setup_lighting_and_camera(pot_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
