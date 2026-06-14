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

def generate_bookcase(params):
    w = params.get("width", 90.0) / 100.0  # convert cm to meters
    d = params.get("depth", 35.0) / 100.0
    h = params.get("height", 180.0) / 100.0
    shelves_count = params.get("shelves", 4)
    has_back = params.get("has_back_panel", True)
    material_type = params.get("material", "wood")

    parts = []

    # 1. Setup Materials
    if material_type == "painted_mdf":
        # Off-white / Cream paint
        carcass_color = (0.92, 0.9, 0.85, 1.0)
        rough_carcass = 0.5
        metallic_carcass = 0.0
        carcass_mat = utils.create_material("BookcaseMDF", diffuse_color=carcass_color, metallic=metallic_carcass, roughness=rough_carcass)
        shelf_mat = carcass_mat
        back_mat = carcass_mat
    elif material_type == "metal_frame":
        # Dark industrial frame + wooden shelves
        frame_color = (0.08, 0.08, 0.09, 1.0) # black steel
        frame_mat = utils.create_material("BookcaseMetalFrame", diffuse_color=frame_color, metallic=0.9, roughness=0.35)
        
        shelf_color = (0.6, 0.4, 0.22, 1.0) # honey pine wood
        shelf_mat = utils.create_material("BookcaseWoodShelf", diffuse_color=shelf_color, metallic=0.0, roughness=0.6)
        back_mat = shelf_mat
    else: # wood
        # Classic Dark Oak wood
        carcass_color = (0.32, 0.18, 0.1, 1.0)
        rough_carcass = 0.7
        metallic_carcass = 0.0
        carcass_mat = utils.create_material("BookcaseWood", diffuse_color=carcass_color, metallic=metallic_carcass, roughness=rough_carcass)
        shelf_mat = carcass_mat
        back_mat = carcass_mat

    # 2. Build Geometry
    if material_type != "metal_frame":
        # Solid wood / MDF carcass style
        carcass_thick = 0.03
        base_h = 0.08
        
        # Left Panel
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-w/2.0 + carcass_thick/2.0, 0.0, h/2.0))
        left_panel = bpy.context.active_object
        left_panel.name = "BookcaseSideL"
        left_panel.scale = (carcass_thick, d, h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(left_panel, width=0.004)
        utils.apply_material(left_panel, carcass_mat)
        parts.append(left_panel)
        master_obj = left_panel
        
        # Right Panel
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(w/2.0 - carcass_thick/2.0, 0.0, h/2.0))
        right_panel = bpy.context.active_object
        right_panel.name = "BookcaseSideR"
        right_panel.scale = (carcass_thick, d, h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(right_panel, width=0.004)
        utils.apply_material(right_panel, carcass_mat)
        parts.append(right_panel)

        # Top Panel
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, h - carcass_thick/2.0))
        top_panel = bpy.context.active_object
        top_panel.name = "BookcaseTop"
        top_panel.scale = (w - carcass_thick*2.0, d, carcass_thick)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(top_panel, width=0.004)
        utils.apply_material(top_panel, carcass_mat)
        parts.append(top_panel)

        # Bottom Panel
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, base_h + carcass_thick/2.0))
        bottom_panel = bpy.context.active_object
        bottom_panel.name = "BookcaseBottom"
        bottom_panel.scale = (w - carcass_thick*2.0, d, carcass_thick)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(bottom_panel, width=0.004)
        utils.apply_material(bottom_panel, carcass_mat)
        parts.append(bottom_panel)

        # Kickboard Base Trim (at front)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -d/2.0 + 0.015, base_h/2.0))
        kickboard = bpy.context.active_object
        kickboard.name = "BookcaseKickboard"
        kickboard.scale = (w, 0.03, base_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(kickboard, width=0.003)
        utils.apply_material(kickboard, carcass_mat)
        parts.append(kickboard)

        # Back panel
        if has_back:
            back_thick = 0.01
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, d/2.0 - back_thick/2.0, base_h + (h - base_h)/2.0))
            back = bpy.context.active_object
            back.name = "BookcaseBack"
            back.scale = (w - carcass_thick*2.0, back_thick, h - base_h - carcass_thick)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(back, back_mat)
            parts.append(back)

        # Shelves inside
        interior_h = h - base_h - carcass_thick * 2.0
        shelf_thick = 0.02
        for s in range(shelves_count):
            sz = base_h + carcass_thick + (s + 1) * (interior_h / (shelves_count + 1))
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, sz))
            shelf = bpy.context.active_object
            shelf.name = f"BookcaseShelf_{s}"
            shelf.scale = (w - carcass_thick*2.0 - 0.002, d - 0.02, shelf_thick)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(shelf, width=0.002)
            utils.apply_material(shelf, shelf_mat)
            parts.append(shelf)

    else:
        # Metal frame bookcase style
        frame_w = 0.025
        px = w/2.0 - frame_w/2.0
        py = d/2.0 - frame_w/2.0
        
        # 4 Corner posts
        corner_posts = []
        for lx in [-px, px]:
            for ly in [-py, py]:
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, h/2.0))
                post = bpy.context.active_object
                post.name = f"BookcasePost_{lx}_{ly}"
                post.scale = (frame_w, frame_w, h)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(post, width=0.002)
                utils.apply_material(post, frame_mat)
                parts.append(post)
                corner_posts.append(post)
                
        master_obj = corner_posts[0]

        # Horizontal support bars at bottom, mid-heights, and top
        num_support_levels = shelves_count + 2
        for l in range(num_support_levels):
            # height levels
            if l == 0:
                sz = 0.08
            elif l == num_support_levels - 1:
                sz = h - frame_w/2.0
            else:
                sz = 0.08 + (l) * ((h - 0.16) / (num_support_levels - 1))
                
            # Left side connector bar
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-px, 0.0, sz))
            lbar = bpy.context.active_object
            lbar.name = f"BookcaseSideBarL_{l}"
            lbar.scale = (frame_w, d - frame_w, frame_w)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(lbar, width=0.002)
            utils.apply_material(lbar, frame_mat)
            parts.append(lbar)

            # Right side connector bar
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, 0.0, sz))
            rbar = bpy.context.active_object
            rbar.name = f"BookcaseSideBarR_{l}"
            rbar.scale = (frame_w, d - frame_w, frame_w)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(rbar, width=0.002)
            utils.apply_material(rbar, frame_mat)
            parts.append(rbar)

            # Front connector bar
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -py, sz))
            fbar = bpy.context.active_object
            fbar.name = f"BookcaseFrontBar_{l}"
            fbar.scale = (w - frame_w, frame_w, frame_w)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(fbar, width=0.002)
            utils.apply_material(fbar, frame_mat)
            parts.append(fbar)

            # Back connector bar
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, py, sz))
            bbar = bpy.context.active_object
            bbar.name = f"BookcaseBackBar_{l}"
            bbar.scale = (w - frame_w, frame_w, frame_w)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(bbar, width=0.002)
            utils.apply_material(bbar, frame_mat)
            parts.append(bbar)

        # Back diagonal structural metal braces (X shape on back frame)
        # From (-px, py, 0.08) to (px, py, h)
        # Just simple cylinders / slim cubes
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, py, h / 2.0 + 0.04))
        brace1 = bpy.context.active_object
        brace1.name = "BookcaseBrace1"
        brace1.scale = (0.008, 0.008, h * 1.1)
        # Rotated slightly around Y to form diagonal
        angle = math.atan2(w, h)
        brace1.rotation_euler = (0.0, angle, 0.0)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        utils.apply_material(brace1, frame_mat)
        parts.append(brace1)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, py, h / 2.0 + 0.04))
        brace2 = bpy.context.active_object
        brace2.name = "BookcaseBrace2"
        brace2.scale = (0.008, 0.008, h * 1.1)
        brace2.rotation_euler = (0.0, -angle, 0.0)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        utils.apply_material(brace2, frame_mat)
        parts.append(brace2)

        # Shelves resting on the horizontal sidebars
        shelf_thick = 0.025
        # Shelves distributed between bottom level and top level
        for s in range(shelves_count):
            sz = 0.08 + (s + 1) * ((h - 0.16) / (shelves_count + 1)) + shelf_thick / 2.0 + frame_w / 2.0
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, sz))
            shelf = bpy.context.active_object
            shelf.name = f"BookcaseShelf_{s}"
            # Fit inside frame posts
            shelf.scale = (w - frame_w * 2.0 - 0.002, d - frame_w * 2.0 - 0.002, shelf_thick)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(shelf, width=0.003)
            utils.apply_material(shelf, shelf_mat)
            parts.append(shelf)

        # Back panel if requested (wooden backing sheet)
        if has_back:
            back_thick = 0.01
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, py - frame_w/2.0 - back_thick/2.0, h/2.0))
            back = bpy.context.active_object
            back.name = "BookcaseBackSheet"
            back.scale = (w - frame_w * 2.0, back_thick, h - 0.16)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(back, back_mat)
            parts.append(back)

    # 3. Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = master_obj
    bpy.ops.object.join()

    master_obj.name = "BookcaseAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return master_obj

def main():
    parser = argparse.ArgumentParser(description="Procedural Bookcase Generator")
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
    bookcase_obj = generate_bookcase(params)
    
    if args.render:
        utils.setup_lighting_and_camera(bookcase_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
