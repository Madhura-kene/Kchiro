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

def generate_lighting(params):
    style = params.get("style", "lamp")
    h = params.get("height", 120.0) / 100.0  # convert cm to meters
    is_lit = params.get("is_lit", True)
    
    parts = []
    
    # 1. Create Materials
    brass_mat = utils.create_material("LightBrass", diffuse_color=(0.85, 0.65, 0.25, 1.0), metallic=0.9, roughness=0.2)
    wax_mat = utils.create_material("LightWax", diffuse_color=(0.92, 0.9, 0.84, 1.0), metallic=0.0, roughness=0.75)
    fabric_mat = utils.create_material("LightShade", diffuse_color=(0.95, 0.93, 0.88, 1.0), metallic=0.0, roughness=0.9)
    steel_mat = utils.create_material("LightSteel", diffuse_color=(0.3, 0.3, 0.32, 1.0), metallic=0.85, roughness=0.35)
    
    # Glowing bulb/flame emission material
    glow_mat = utils.create_material("LightGlow", diffuse_color=(1.0, 0.8, 0.3, 1.0), metallic=0.0, roughness=0.1)
    glow_mat.use_nodes = True
    nodes = glow_mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (1.0, 0.75, 0.2, 1.0)
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = (1.0, 0.75, 0.2, 1.0)
            
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 3.0 if is_lit else 0.0
            
    if style == "candle":
        # --- CANDLE ---
        # Adjust height to sensible candle range if too high
        h = max(0.08, min(0.35, h))
        
        # Holder plate/saucer
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.06,
            depth=0.01,
            location=(0, 0, 0.005)
        )
        plate = bpy.context.active_object
        plate.name = "CandlePlate"
        utils.apply_smooth_by_angle(plate, angle=40.0)
        utils.apply_material(plate, brass_mat)
        parts.append(plate)
        
        # Wax body
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.018,
            depth=h,
            location=(0, 0, 0.01 + h/2.0)
        )
        wax = bpy.context.active_object
        wax.name = "CandleWax"
        utils.apply_smooth_by_angle(wax, angle=35.0)
        utils.apply_material(wax, wax_mat)
        parts.append(wax)
        
        # Wick
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.002,
            depth=0.012,
            location=(0, 0, 0.01 + h + 0.006)
        )
        wick = bpy.context.active_object
        wick.name = "CandleWick"
        utils.apply_material(wick, steel_mat)
        parts.append(wick)
        
        # Flame
        if is_lit:
            bpy.ops.mesh.primitive_uv_sphere_add(
                segments=8,
                ring_count=8,
                radius=0.008,
                location=(0, 0, 0.01 + h + 0.018)
            )
            flame = bpy.context.active_object
            flame.name = "CandleFlame"
            # Deform flame to taper
            flame.scale = (0.7, 0.7, 1.4)
            bpy.ops.object.transform_apply(scale=True)
            for v in flame.data.vertices:
                if v.co.z > 0:
                    v.co.x = v.co.x * 0.4
                    v.co.y = v.co.y * 0.4
            utils.apply_smooth_by_angle(flame, angle=35.0)
            utils.apply_material(flame, glow_mat)
            parts.append(flame)
            
    elif style == "lamp":
        # --- STANDING FLOOR LAMP ---
        # Base plate
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=20,
            radius=0.15,
            depth=0.024,
            location=(0, 0, 0.012)
        )
        base = bpy.context.active_object
        base.name = "LampBase"
        utils.apply_smooth_by_angle(base, angle=40.0)
        utils.apply_material(base, steel_mat)
        parts.append(base)
        
        # Long central rod
        rod_h = h - 0.28
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=12,
            radius=0.012,
            depth=rod_h,
            location=(0, 0, 0.024 + rod_h/2.0)
        )
        rod = bpy.context.active_object
        rod.name = "LampRod"
        utils.apply_smooth_by_angle(rod, angle=40.0)
        utils.apply_material(rod, steel_mat)
        parts.append(rod)
        
        # Shade (cone style)
        shade_h = 0.25
        shade_z = h - (shade_h / 2.0)
        bpy.ops.mesh.primitive_cone_add(
            vertices=16,
            radius1=0.16, # bottom
            radius2=0.11, # top
            depth=shade_h,
            location=(0, 0, shade_z)
        )
        shade = bpy.context.active_object
        shade.name = "LampShade"
        utils.apply_smooth_by_angle(shade, angle=40.0)
        utils.apply_material(shade, fabric_mat)
        parts.append(shade)
        
        # Glowing bulb
        if is_lit:
            bpy.ops.mesh.primitive_uv_sphere_add(
                segments=12,
                ring_count=8,
                radius=0.045,
                location=(0, 0, h - 0.16)
            )
            bulb = bpy.context.active_object
            bulb.name = "LampBulb"
            utils.apply_smooth_by_angle(bulb, angle=35.0)
            utils.apply_material(bulb, glow_mat)
            parts.append(bulb)
            
    elif style == "chandelier":
        # --- CHANDELIER ---
        # Hanging chain/rod down from the ceiling level h
        chain_h = 0.35
        chain_z = h - (chain_h / 2.0)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.008,
            depth=chain_h,
            location=(0, 0, chain_z)
        )
        chain = bpy.context.active_object
        chain.name = "ChandelierChain"
        utils.apply_smooth_by_angle(chain, angle=40.0)
        utils.apply_material(chain, brass_mat)
        parts.append(chain)
        
        # Central ring/core
        core_z = h - chain_h
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.07,
            depth=0.04,
            location=(0, 0, core_z)
        )
        core = bpy.context.active_object
        core.name = "ChandelierCore"
        utils.apply_smooth_by_angle(core, angle=40.0)
        utils.apply_material(core, brass_mat)
        parts.append(core)
        
        # 4 light-holding arms
        num_arms = 4
        arm_len = 0.22
        for i in range(num_arms):
            angle = i * (math.pi / 2.0)
            # Arm rod
            arm_x = math.cos(angle) * (arm_len / 2.0)
            arm_y = math.sin(angle) * (arm_len / 2.0)
            
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8,
                radius=0.006,
                depth=arm_len,
                location=(arm_x, arm_y, core_z),
                rotation=(0, math.pi / 2.0, angle)
            )
            arm = bpy.context.active_object
            arm.name = f"ChandelierArm_{i}"
            utils.apply_smooth_by_angle(arm, angle=40.0)
            utils.apply_material(arm, brass_mat)
            parts.append(arm)
            
            # Candle holder at the end of the arm
            end_x = math.cos(angle) * arm_len
            end_y = math.sin(angle) * arm_len
            holder_z = core_z + 0.02
            
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8,
                radius=0.016,
                depth=0.03,
                location=(end_x, end_y, holder_z)
            )
            holder = bpy.context.active_object
            holder.name = f"ChandelierSocket_{i}"
            utils.apply_smooth_by_angle(holder, angle=40.0)
            utils.apply_material(holder, brass_mat)
            parts.append(holder)
            
            # Little wax candle
            candle_z = holder_z + 0.03
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8,
                radius=0.008,
                depth=0.04,
                location=(end_x, end_y, candle_z)
            )
            candle = bpy.context.active_object
            candle.name = f"ChandelierCandle_{i}"
            utils.apply_smooth_by_angle(candle, angle=35.0)
            utils.apply_material(candle, wax_mat)
            parts.append(candle)
            
            # Flame
            if is_lit:
                bpy.ops.mesh.primitive_uv_sphere_add(
                    segments=8,
                    ring_count=6,
                    radius=0.006,
                    location=(end_x, end_y, candle_z + 0.028)
                )
                flame = bpy.context.active_object
                flame.name = f"ChandelierFlame_{i}"
                flame.scale = (0.7, 0.7, 1.3)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_smooth_by_angle(flame, angle=35.0)
                utils.apply_material(flame, glow_mat)
                parts.append(flame)
                
    # Join all lighting parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    
    parts[0].name = "LightingAsset"
    # Place pivot point at bottom center (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return parts[0]

def main():
    parser = argparse.ArgumentParser(description="Procedural Lighting Generator")
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
    light_obj = generate_lighting(params)
    
    if args.render:
        utils.setup_lighting_and_camera(light_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
