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

def generate_lamp(params):
    height = params.get("height", 60.0) / 100.0  # cm to meters
    style = params.get("style", "table")
    shade_shape = params.get("shade_shape", "conical")
    is_lit = params.get("is_lit", True)

    parts = []

    # 1. Create Materials
    brass_mat = utils.create_material("LampBrass", diffuse_color=(0.85, 0.65, 0.25, 1.0), metallic=0.9, roughness=0.2)
    chrome_mat = utils.create_material("LampChrome", diffuse_color=(0.9, 0.9, 0.9, 1.0), metallic=0.95, roughness=0.1)
    fabric_mat = utils.create_material("LampShadeFabric", diffuse_color=(0.95, 0.93, 0.88, 1.0), metallic=0.0, roughness=0.9)
    ceramic_mat = utils.create_material("LampCeramic", diffuse_color=(0.15, 0.35, 0.45, 1.0), metallic=0.0, roughness=0.15)  # Elegant teal-blue glaze
    cord_mat = utils.create_material("LampCord", diffuse_color=(0.1, 0.1, 0.1, 1.0), metallic=0.0, roughness=0.7)

    # Glowing bulb emission material
    glow_mat = utils.create_material("LampGlow", diffuse_color=(1.0, 0.85, 0.4, 1.0), metallic=0.0, roughness=0.1)
    glow_mat.use_nodes = True
    nodes = glow_mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (1.0, 0.8, 0.3, 1.0)
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = (1.0, 0.8, 0.3, 1.0)
        
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 4.0 if is_lit else 0.0

    # 2. Build Base
    if style == "table":
        # Table lamp base (bulbous ceramic vase shape with metal trim)
        base_h = height * 0.45
        base_radius_max = height * 0.18
        
        # Bottom metal disk rim
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=32,
            radius=base_radius_max,
            depth=0.012,
            location=(0, 0, 0.006)
        )
        bottom_rim = bpy.context.active_object
        bottom_rim.name = "LampBaseRim"
        utils.apply_smooth_by_angle(bottom_rim, angle=35.0)
        utils.apply_material(bottom_rim, brass_mat)
        parts.append(bottom_rim)

        # Bulbous ceramic body
        # Let's model a gourd-like base by combining a sphere and cylinder, or scaling layers
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=32,
            ring_count=16,
            radius=base_radius_max * 0.95,
            location=(0, 0, 0.012 + base_h * 0.4)
        )
        ceramic_body = bpy.context.active_object
        ceramic_body.name = "LampBaseCeramic"
        ceramic_body.scale = (1.0, 1.0, 1.3)  # Stretch vertically
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_smooth_by_angle(ceramic_body, angle=30.0)
        utils.apply_material(ceramic_body, ceramic_mat)
        parts.append(ceramic_body)

        # Neck connector (top metal cap of the base)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=24,
            radius=base_radius_max * 0.35,
            depth=0.02,
            location=(0, 0, 0.012 + base_h - 0.01)
        )
        top_cap = bpy.context.active_object
        top_cap.name = "LampBaseCap"
        utils.apply_smooth_by_angle(top_cap, angle=35.0)
        utils.apply_material(top_cap, brass_mat)
        parts.append(top_cap)

        # Base center Z is around the top cap
        stem_start_z = 0.012 + base_h
    else:
        # Floor lamp base (heavy cast brass base plate + long rod)
        base_h = 0.03
        base_radius = height * 0.12

        bpy.ops.mesh.primitive_cylinder_add(
            vertices=32,
            radius=base_radius,
            depth=base_h,
            location=(0, 0, base_h / 2.0)
        )
        base = bpy.context.active_object
        base.name = "LampBasePlate"
        utils.apply_smooth_by_angle(base, angle=35.0)
        utils.apply_bevel(base, width=0.005)
        utils.apply_material(base, brass_mat)
        parts.append(base)
        
        # Elegant small neck collar just above base
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=24,
            radius=base_radius * 0.3,
            depth=0.02,
            location=(0, 0, base_h + 0.01)
        )
        collar = bpy.context.active_object
        collar.name = "LampBaseCollar"
        utils.apply_smooth_by_angle(collar, angle=35.0)
        utils.apply_material(collar, brass_mat)
        parts.append(collar)

        stem_start_z = base_h + 0.02

    # 3. Stem/Neck
    shade_h = height * 0.32
    shade_z = height - (shade_h / 2.0)
    stem_h = height - stem_start_z - (shade_h * 0.7)  # stem goes up inside the shade

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.012 if style == "floor" else 0.008,
        depth=stem_h,
        location=(0, 0, stem_start_z + stem_h / 2.0)
    )
    stem = bpy.context.active_object
    stem.name = "LampStem"
    utils.apply_smooth_by_angle(stem, angle=35.0)
    utils.apply_material(stem, brass_mat)
    parts.append(stem)

    # 4. Shade
    shade_center_z = height - (shade_h / 2.0)
    shade_r1 = height * 0.24  # bottom radius
    shade_r2 = height * 0.18 if shade_shape == "conical" else shade_r1  # top radius

    # Create the shade using a cone or cylinder
    if shade_shape == "conical":
        bpy.ops.mesh.primitive_cone_add(
            vertices=32,
            radius1=shade_r1,
            radius2=shade_r2,
            depth=shade_h,
            location=(0, 0, shade_center_z)
        )
    else:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=32,
            radius=shade_r1,
            depth=shade_h,
            location=(0, 0, shade_center_z)
        )
    shade = bpy.context.active_object
    shade.name = "LampShade"
    utils.apply_smooth_by_angle(shade, angle=35.0)
    utils.apply_material(shade, fabric_mat)
    parts.append(shade)

    # Add a thin metal top rim/spokes for premium detail
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=24,
        radius=shade_r2,
        depth=0.005,
        location=(0, 0, shade_center_z + shade_h / 2.0)
    )
    top_rim = bpy.context.active_object
    top_rim.name = "LampShadeTopRim"
    # scale it down to make it look like a wire frame
    top_rim.scale = (1.002, 1.002, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_smooth_by_angle(top_rim, angle=40.0)
    utils.apply_material(top_rim, brass_mat)
    parts.append(top_rim)

    # 5. Glowing bulb
    bulb_z = shade_center_z - (shade_h * 0.15)
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16,
        ring_count=12,
        radius=shade_r1 * 0.28,
        location=(0, 0, bulb_z)
    )
    bulb = bpy.context.active_object
    bulb.name = "LampBulb"
    utils.apply_smooth_by_angle(bulb, angle=30.0)
    utils.apply_material(bulb, glow_mat)
    parts.append(bulb)

    # 6. Join parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()

    # Rename asset and center origin to ground level (0, 0, 0)
    parts[0].name = "LampAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return parts[0]

def main():
    parser = argparse.ArgumentParser(description="Procedural Lamp Generator")
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
    lamp_obj = generate_lamp(params)
    
    if args.render:
        utils.setup_lighting_and_camera(lamp_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
