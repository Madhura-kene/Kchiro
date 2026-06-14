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

def generate_bunk_bed(params):
    w = params.get("width", 100.0) / 100.0  # convert cm to meters
    d = params.get("depth", 200.0) / 100.0
    h = params.get("height", 180.0) / 100.0
    has_ladder = params.get("has_ladder", True)
    material = params.get("material", "wood")

    parts = []

    # 1. Create Materials
    wood_mat = utils.create_material("BunkWood", diffuse_color=(0.28, 0.16, 0.08, 1.0), metallic=0.0, roughness=0.75)
    metal_mat = utils.create_material("BunkMetal", diffuse_color=(0.22, 0.22, 0.24, 1.0), metallic=0.9, roughness=0.3)
    sheet_mat = utils.create_material("BunkSheets", diffuse_color=(0.9, 0.9, 0.95, 1.0), metallic=0.0, roughness=0.95)
    blanket1_mat = utils.create_material("BunkBlanket1", diffuse_color=(0.12, 0.28, 0.45, 1.0), metallic=0.0, roughness=0.85) # Navy blue
    blanket2_mat = utils.create_material("BunkBlanket2", diffuse_color=(0.65, 0.35, 0.12, 1.0), metallic=0.0, roughness=0.8)  # Orange/Yellow

    frame_mat = wood_mat if material == "wood" else metal_mat

    # Dimensions
    post_w = 0.06
    frame_h = 0.12
    mattress_h = 0.18

    # 2. Four Tall Corner Posts
    px = (w / 2.0) - post_w / 2.0
    py = (d / 2.0) - post_w / 2.0
    
    for lx in [-px, px]:
        for ly in [-py, py]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, h / 2.0))
            post = bpy.context.active_object
            post.name = f"BunkPost_{lx}_{ly}"
            post.scale = (post_w, post_w, h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(post, width=0.005)
            utils.apply_material(post, frame_mat)
            parts.append(post)

    # Helper function to generate a single bunk bed floor/mattress/pillow
    def create_single_bunk(z_base, name_prefix, b_mat):
        bunk_parts = []
        
        # Bed Frame Box
        frame_z = z_base + (frame_h / 2.0)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, frame_z))
        bf = bpy.context.active_object
        bf.name = f"{name_prefix}Frame"
        bf.scale = (w - 0.01, d, frame_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(bf, width=0.006)
        utils.apply_material(bf, frame_mat)
        bunk_parts.append(bf)

        # Mattress
        mat_z = z_base + frame_h + (mattress_h / 2.0) - 0.03
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, mat_z))
        bm = bpy.context.active_object
        bm.name = f"{name_prefix}Mattress"
        bm.scale = (w - post_w - 0.02, d - post_w - 0.02, mattress_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(bm, width=0.015)
        utils.apply_material(bm, sheet_mat)
        bunk_parts.append(bm)

        # Pillow
        pillow_w = w * 0.65
        pillow_d = 0.32
        pillow_h = 0.08
        pillow_z = mat_z + (mattress_h / 2.0) + 0.01
        pillow_y = (d / 2.0) - 0.22
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, pillow_y, pillow_z))
        bp = bpy.context.active_object
        bp.name = f"{name_prefix}Pillow"
        bp.scale = (pillow_w, pillow_d, pillow_h)
        bp.rotation_euler = (0.1, 0, 0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_bevel(bp, width=0.015)
        utils.apply_material(bp, sheet_mat)
        bunk_parts.append(bp)

        # Blanket Sheet
        blanket_d = d * 0.6
        blanket_y = -d/2.0 + blanket_d/2.0 + 0.04
        blanket_z = mat_z + (mattress_h / 2.0) + 0.005
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, blanket_y, blanket_z))
        bb = bpy.context.active_object
        bb.name = f"{name_prefix}Blanket"
        bb.scale = (w - post_w - 0.01, blanket_d, 0.02)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(bb, width=0.005)
        utils.apply_material(bb, b_mat)
        bunk_parts.append(bb)
        
        return bunk_parts

    # 3. Create Bottom Bunk Bed
    bottom_parts = create_single_bunk(0.25, "BottomBunk", blanket1_mat)
    parts.extend(bottom_parts)
    master_object = bottom_parts[0] # frame base

    # 4. Create Top Bunk Bed
    top_z_base = h - frame_h - mattress_h - 0.15 # lower than top posts
    top_parts = create_single_bunk(top_z_base, "TopBunk", blanket2_mat)
    parts.extend(top_parts)

    # 5. Guard Rails for Top Bunk
    rail_y = 0.0
    rail_z = top_z_base + frame_h + 0.18
    rail_h = 0.18
    rail_thick = 0.025
    
    # Left and Right guard rails
    for side_x in [-(w / 2.0 - rail_thick/2.0), (w / 2.0 - rail_thick/2.0)]:
        # Create horizontal bar
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, 0, rail_z))
        rail = bpy.context.active_object
        rail.name = f"BunkGuardRail_{side_x}"
        rail.scale = (rail_thick, d - post_w*2.0, rail_thick)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(rail, width=0.003)
        utils.apply_material(rail, frame_mat)
        parts.append(rail)
        
        # Vertical connectors for the rail
        for step_y in [-d/3.0, 0, d/3.0]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, step_y, rail_z - rail_h/2.0))
            con = bpy.context.active_object
            con.name = f"BunkGuardCon_{side_x}_{step_y}"
            con.scale = (rail_thick, rail_thick, rail_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(con, width=0.002)
            utils.apply_material(con, frame_mat)
            parts.append(con)

    # 6. Ladder
    if has_ladder:
        ladder_x = w/2.0 + 0.02
        ladder_z = h / 2.0
        # Double side rails of the ladder
        ladder_post_w = 0.03
        for ladder_y in [-0.25, 0.25]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ladder_x, ladder_y, ladder_z))
            lad_post = bpy.context.active_object
            lad_post.name = f"LadderPost_{ladder_y}"
            lad_post.scale = (ladder_post_w, ladder_post_w, h * 0.95)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(lad_post, width=0.002)
            utils.apply_material(lad_post, frame_mat)
            parts.append(lad_post)
            
        # Horizontal ladder rungs (steps)
        step_count = 5
        for s in range(step_count):
            sz = (h / step_count) * (s + 0.5)
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.012,
                depth=0.5,
                location=(ladder_x, 0.0, sz)
            )
            rung = bpy.context.active_object
            rung.name = f"LadderRung_{s}"
            rung.rotation_euler = (math.pi/2.0, 0.0, 0.0) # rotate along Y-axis
            bpy.ops.object.transform_apply(rotation=True)
            utils.apply_smooth_by_angle(rung, angle=40.0)
            utils.apply_material(rung, frame_mat)
            parts.append(rung)

    # Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
        
    bpy.context.view_layer.objects.active = master_object
    bpy.ops.object.join()
    
    master_object.name = "BunkBedAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    return master_object

def main():
    parser = argparse.ArgumentParser(description="Procedural Bunk Bed Generator")
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
    bunk_bed_obj = generate_bunk_bed(params)
    
    if args.render:
        utils.setup_lighting_and_camera(bunk_bed_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
