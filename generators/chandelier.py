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

def generate_chandelier(params):
    w = params.get("width", 80.0) / 100.0  # cm to meters
    h = params.get("height", 70.0) / 100.0 # cm to meters (this is the vertical span from ceiling)
    arms = params.get("arms", 5)
    style = params.get("style", "classic")
    is_lit = params.get("is_lit", True)

    parts = []

    # 1. Create Materials
    brass_mat = utils.create_material("ChandelierBrass", diffuse_color=(0.82, 0.62, 0.2, 1.0), metallic=0.95, roughness=0.18)
    wax_mat = utils.create_material("ChandelierCandleWax", diffuse_color=(0.95, 0.94, 0.9, 1.0), metallic=0.0, roughness=0.7)
    chrome_mat = utils.create_material("ChandelierChrome", diffuse_color=(0.9, 0.9, 0.9, 1.0), metallic=0.95, roughness=0.1)
    crystal_mat = utils.create_material("ChandelierCrystal", diffuse_color=(0.95, 0.98, 1.0, 0.4), metallic=0.1, roughness=0.05)
    crystal_mat.blend_method = 'BLEND'

    # Glowing bulb/flame emission material
    glow_mat = utils.create_material("ChandelierGlow", diffuse_color=(1.0, 0.82, 0.35, 1.0), metallic=0.0, roughness=0.1)
    glow_mat.use_nodes = True
    nodes = glow_mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (1.0, 0.78, 0.25, 1.0)
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = (1.0, 0.78, 0.25, 1.0)
        
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 3.5 if is_lit else 0.0

    # 2. Ceiling Canopy (at Z = h, the ceiling attachment)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=24,
        radius=0.08,
        depth=0.02,
        location=(0, 0, h - 0.01)
    )
    canopy = bpy.context.active_object
    canopy.name = "ChandelierCanopy"
    utils.apply_smooth_by_angle(canopy, angle=40.0)
    utils.apply_bevel(canopy, width=0.003)
    utils.apply_material(canopy, brass_mat)
    parts.append(canopy)

    # 3. Central Hanging Rod/Chain
    chain_h = h * 0.4
    rod_z = h - 0.02 - (chain_h / 2.0)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12,
        radius=0.01,
        depth=chain_h,
        location=(0, 0, rod_z)
    )
    rod = bpy.context.active_object
    rod.name = "ChandelierHangingRod"
    utils.apply_smooth_by_angle(rod, angle=35.0)
    utils.apply_material(rod, brass_mat)
    parts.append(rod)

    # Accent decorative collar along the rod
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.02,
        depth=0.03,
        location=(0, 0, rod_z)
    )
    collar = bpy.context.active_object
    collar.name = "ChandelierRodCollar"
    utils.apply_smooth_by_angle(collar, angle=35.0)
    utils.apply_material(collar, brass_mat)
    parts.append(collar)

    # 4. Central Hub/Core (body at bottom of the rod)
    hub_h = h * 0.16
    hub_z = h - 0.02 - chain_h - (hub_h / 2.0)
    hub_radius = w * 0.12

    if style == "classic":
        # Bowl-shaped ornamental hub
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=32,
            ring_count=16,
            radius=hub_radius,
            location=(0, 0, hub_z)
        )
        hub = bpy.context.active_object
        hub.name = "ChandelierHubClassic"
        hub.scale = (1.0, 1.0, 0.7)  # Flatten sphere
        bpy.ops.object.transform_apply(scale=True)
    else:
        # Sleek modern cylindrical hub
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=24,
            radius=hub_radius,
            depth=hub_h,
            location=(0, 0, hub_z)
        )
        hub = bpy.context.active_object
        hub.name = "ChandelierHubModern"
        utils.apply_bevel(hub, width=0.005)

    utils.apply_smooth_by_angle(hub, angle=30.0)
    utils.apply_material(hub, brass_mat)
    parts.append(hub)

    # Bottom finial tip
    bpy.ops.mesh.primitive_cone_add(
        vertices=12,
        radius1=0.015,
        radius2=0.0,
        depth=0.04,
        location=(0, 0, hub_z - hub_h * 0.5 - 0.02)
    )
    finial = bpy.context.active_object
    finial.name = "ChandelierFinial"
    # Flip it upside down
    finial.rotation_euler = (math.radians(180), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    utils.apply_smooth_by_angle(finial, angle=35.0)
    utils.apply_material(finial, brass_mat)
    parts.append(finial)

    # 5. Radiating Arms
    arm_radius = w * 0.42
    arm_thick = 0.008

    for i in range(arms):
        angle = i * (2.0 * math.pi / arms)
        
        # We will create curved arms using multiple cylinder segments:
        # Segment 1: Extending horizontally from the hub
        seg1_len = arm_radius * 0.5
        seg1_x = math.cos(angle) * (hub_radius + seg1_len / 2.0)
        seg1_y = math.sin(angle) * (hub_radius + seg1_len / 2.0)
        seg1_z = hub_z
        
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=arm_thick,
            depth=seg1_len,
            location=(seg1_x, seg1_y, seg1_z),
            rotation=(0, math.pi / 2.0, angle)
        )
        arm_seg1 = bpy.context.active_object
        arm_seg1.name = f"ChandelierArmSeg1_{i}"
        utils.apply_smooth_by_angle(arm_seg1, angle=40.0)
        utils.apply_material(arm_seg1, brass_mat)
        parts.append(arm_seg1)

        # Segment 2: Angled upward sweep
        seg2_len = arm_radius * 0.6
        # Start at end of seg1
        start_x = math.cos(angle) * (hub_radius + seg1_len)
        start_y = math.sin(angle) * (hub_radius + seg1_len)
        
        # End point of sweep (curving up and out)
        end_x = math.cos(angle) * arm_radius
        end_y = math.sin(angle) * arm_radius
        end_z = hub_z + h * 0.15
        
        mid_x = (start_x + end_x) / 2.0
        mid_y = (start_y + end_y) / 2.0
        mid_z = (hub_z + end_z) / 2.0
        
        # Compute angles for cylinder aligning
        dx = end_x - start_x
        dy = end_y - start_y
        dz = end_z - hub_z
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        phi = math.atan2(dy, dx)
        theta = math.acos(dz / dist)
        
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=arm_thick * 0.9,
            depth=dist,
            location=(mid_x, mid_y, mid_z),
            rotation=(0, theta, phi)
        )
        arm_seg2 = bpy.context.active_object
        arm_seg2.name = f"ChandelierArmSeg2_{i}"
        utils.apply_smooth_by_angle(arm_seg2, angle=40.0)
        utils.apply_material(arm_seg2, brass_mat)
        parts.append(arm_seg2)

        # 6. Sockets, Candle/Bulb, and Flame
        # Socket Cup
        cup_z = end_z + 0.015
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.024,
            depth=0.03,
            location=(end_x, end_y, cup_z)
        )
        cup = bpy.context.active_object
        cup.name = f"ChandelierSocket_{i}"
        utils.apply_smooth_by_angle(cup, angle=35.0)
        utils.apply_bevel(cup, width=0.003)
        utils.apply_material(cup, brass_mat)
        parts.append(cup)

        # Wax candle sleeve
        candle_h = 0.06
        candle_z = cup_z + 0.015 + (candle_h / 2.0)
        
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=12,
            radius=0.012,
            depth=candle_h,
            location=(end_x, end_y, candle_z)
        )
        candle = bpy.context.active_object
        candle.name = f"ChandelierCandle_{i}"
        utils.apply_smooth_by_angle(candle, angle=30.0)
        utils.apply_material(candle, wax_mat)
        parts.append(candle)

        # Bulb flame
        if is_lit:
            flame_z = candle_z + (candle_h / 2.0) + 0.014
            bpy.ops.mesh.primitive_uv_sphere_add(
                segments=12,
                ring_count=8,
                radius=0.009,
                location=(end_x, end_y, flame_z)
            )
            flame = bpy.context.active_object
            flame.name = f"ChandelierFlame_{i}"
            flame.scale = (0.7, 0.7, 1.5)  # Stretch into flame shape
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_smooth_by_angle(flame, angle=35.0)
            utils.apply_material(flame, glow_mat)
            parts.append(flame)

        # 7. Crystals (hang under cups if style is classic)
        if style == "classic":
            crystal_z = end_z - 0.03
            bpy.ops.mesh.primitive_cone_add(
                vertices=6,
                radius1=0.008,
                radius2=0.0,
                depth=0.03,
                location=(end_x, end_y, crystal_z)
            )
            crystal = bpy.context.active_object
            crystal.name = f"ChandelierCrystal_{i}"
            crystal.rotation_euler = (math.radians(180), 0, 0)
            bpy.ops.object.transform_apply(rotation=True)
            utils.apply_smooth_by_angle(crystal, angle=30.0)
            utils.apply_material(crystal, crystal_mat)
            parts.append(crystal)

    # 8. Join all components
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()

    # Center origin to ground level (ceiling height alignment)
    parts[0].name = "ChandelierAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return parts[0]

def main():
    parser = argparse.ArgumentParser(description="Procedural Chandelier Generator")
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
    chandelier_obj = generate_chandelier(params)
    
    if args.render:
        utils.setup_lighting_and_camera(chandelier_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
