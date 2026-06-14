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

def generate_vase(params):
    h = params.get("height", 35.0) / 100.0        # cm to m
    d = params.get("diameter", 18.0) / 100.0      # cm to m
    neck_d = params.get("neck_diameter", 6.0) / 100.0 # cm to m
    style = params.get("style", "classic")
    mat_type = params.get("material", "ceramic")

    parts = []

    # 1. Materials
    if mat_type == "ceramic":
        # Glazed glossy teal ceramic
        vase_mat = utils.create_material("VaseCeramic", diffuse_color=(0.08, 0.45, 0.42, 1.0), metallic=0.0, roughness=0.12)
    elif mat_type == "glass":
        # Translucent glass
        vase_mat = bpy.data.materials.new(name="VaseGlass")
        vase_mat.use_nodes = True
        bsdf = vase_mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (0.75, 0.9, 0.95, 0.2)
            bsdf.inputs['Roughness'].default_value = 0.05
            bsdf.inputs['Transmission Weight'].default_value = 0.95
            bsdf.inputs['IOR'].default_value = 1.5
    else: # clay / terracotta
        # Matte terracotta clay
        vase_mat = utils.create_material("VaseClay", diffuse_color=(0.72, 0.36, 0.22, 1.0), metallic=0.0, roughness=0.8)

    # 2. Define the Profile Curve points (Z-height, Radius multiplier of d/2)
    max_r = d / 2.0
    neck_r = neck_d / 2.0

    profile = []
    
    if style == "modern":
        # Sleek teardrop shape
        # 10 layers
        num_layers = 12
        for i in range(num_layers):
            t = i / (num_layers - 1) # 0.0 to 1.0
            z = t * h
            if t < 0.2:
                # Base flaring to belly
                r = max_r * (0.4 + 0.6 * (t / 0.2))
            else:
                # Tapering to neck
                r = max_r - (max_r - neck_r) * ((t - 0.2) / 0.8)
            profile.append((z, r))
            
    elif style == "geometric":
        # Low-poly segmented profile (fewer divisions)
        profile = [
            (0.0, max_r * 0.4),      # Base
            (h * 0.1, max_r * 0.5),  # Lower flare
            (h * 0.4, max_r * 1.0),  # Belly
            (h * 0.75, neck_r),      # Neck
            (h * 1.0, neck_r * 1.15) # Rim
        ]
        
    else: # classic
        # Curvy classic amphora/bulbous shape
        num_layers = 15
        for i in range(num_layers):
            t = i / (num_layers - 1)
            z = t * h
            if t == 0:
                r = max_r * 0.45
            elif t < 0.15:
                # Base flare
                r = max_r * (0.45 + 0.1 * (t / 0.15))
            elif t < 0.45:
                # Bulge to max belly
                r = max_r * (0.55 + 0.45 * ((t - 0.15) / 0.3))
            elif t < 0.8:
                # Taper in to neck
                r = max_r - (max_r - neck_r) * ((t - 0.45) / 0.35)
            else:
                # Flare out to rim
                r = neck_r + (neck_r * 0.25) * ((t - 0.8) / 0.2)
            profile.append((z, r))

    # 3. Construct the Mesh
    segments = 8 if style == "geometric" else 32
    
    verts = []
    faces = []

    for l_idx, (z, r) in enumerate(profile):
        for s in range(segments):
            angle = (s / segments) * 2.0 * math.pi
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            verts.append((x, y, z))

    # Connect vertices to form faces
    num_levels = len(profile)
    for l in range(num_levels - 1):
        for s in range(segments):
            # 4 vertices of a quad face
            v1 = l * segments + s
            v2 = l * segments + (s + 1) % segments
            v3 = (l + 1) * segments + (s + 1) % segments
            v4 = (l + 1) * segments + s
            faces.append((v1, v2, v3, v4))

    # Create Blender Object
    mesh_data = bpy.data.meshes.new("VaseMesh")
    mesh_data.from_pydata(verts, [], faces)
    mesh_data.update()

    vase = bpy.data.objects.new("VaseObject", mesh_data)
    bpy.context.collection.objects.link(vase)
    
    # 4. Refine Mesh Shape and Thickness
    if style != "geometric":
        utils.apply_smooth_by_angle(vase, angle=35.0)
    else:
        # For geometric style, keep flat shading and apply a small bevel to highlight facets
        utils.apply_bevel(vase, width=0.003)

    # Add Solidify modifier to make the vase hollow
    bpy.ops.object.select_all(action='DESELECT')
    vase.select_set(True)
    bpy.context.view_layer.objects.active = vase
    
    solidify = vase.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.012  # 1.2 cm wall thickness
    bpy.ops.object.modifier_apply(modifier="Solidify")

    # Add a Subdivision Surface modifier for classic/modern styles to smooth it out further
    if style != "geometric":
        subdiv = vase.modifiers.new(name="Subdivision", type='SUBSURF')
        subdiv.levels = 1
        subdiv.render_levels = 2
        bpy.ops.object.modifier_apply(modifier="Subdivision")

    utils.apply_material(vase, vase_mat)
    parts.append(vase)

    vase.name = "VaseAsset"
    
    # Center origin to the base center
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return vase

def main():
    parser = argparse.ArgumentParser(description="Procedural Vase Generator")
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
    vase_obj = generate_vase(params)
    
    if args.render:
        utils.setup_lighting_and_camera(vase_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
