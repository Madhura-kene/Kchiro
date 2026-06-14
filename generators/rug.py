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

def generate_rug(params):
    w = params.get("width", 150.0) / 100.0   # cm to m
    d = params.get("depth", 100.0) / 100.0   # cm to m
    thickness = params.get("thickness", 1.2) / 100.0 # cm to m
    shape = params.get("shape", "rectangular")
    pattern = params.get("pattern", "geometric")
    color_choice = params.get("color", "cream")

    parts = []

    # 1. Color Palettes (Curated, harmonious HSL based colors)
    palettes = {
        "cream": {"primary": (0.94, 0.92, 0.86, 1.0), "accent": (0.2, 0.22, 0.25, 1.0)},  # Cream & Charcoal
        "red": {"primary": (0.68, 0.12, 0.14, 1.0), "accent": (0.92, 0.88, 0.8, 1.0)},   # Ruby Red & Cream
        "blue": {"primary": (0.12, 0.25, 0.45, 1.0), "accent": (0.92, 0.88, 0.8, 1.0)},  # Navy Blue & Cream
        "grey": {"primary": (0.35, 0.36, 0.38, 1.0), "accent": (0.88, 0.85, 0.8, 1.0)},  # Slate Grey & Light Cream
        "green": {"primary": (0.18, 0.35, 0.22, 1.0), "accent": (0.92, 0.88, 0.8, 1.0)}  # Sage Green & Cream
    }

    colors = palettes.get(color_choice, palettes["cream"])
    
    # Create PBR materials with velvet-like rough soft surface (roughness = 0.95)
    primary_mat = utils.create_material("RugPrimary", diffuse_color=colors["primary"], metallic=0.0, roughness=0.95)
    accent_mat = utils.create_material("RugAccent", diffuse_color=colors["accent"], metallic=0.0, roughness=0.95)
    fringe_mat = utils.create_material("RugFringe", diffuse_color=(0.9, 0.87, 0.8, 1.0), metallic=0.0, roughness=0.9)

    # Height offset to place rug resting flat on floor (Z = thickness / 2)
    rug_z = thickness / 2.0

    if shape == "rectangular":
        # Base/Backing plate
        if pattern == "solid":
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, rug_z))
            base = bpy.context.active_object
            base.name = "RugBase"
            base.scale = (w, d, thickness)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(base, width=0.002)
            utils.apply_material(base, primary_mat)
            parts.append(base)

        elif pattern == "striped":
            # Form rug by alternating rows of geometry along depth (Y axis)
            num_stripes = 7
            stripe_d = d / num_stripes
            for i in range(num_stripes):
                stripe_y = -d / 2.0 + (i * stripe_d) + (stripe_d / 2.0)
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, stripe_y, rug_z))
                stripe = bpy.context.active_object
                stripe.name = f"RugStripe_{i}"
                stripe.scale = (w, stripe_d, thickness)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_bevel(stripe, width=0.001)
                
                # Alternate materials
                mat = primary_mat if i % 2 == 0 else accent_mat
                utils.apply_material(stripe, mat)
                parts.append(stripe)

        elif pattern == "oriental":
            # Primary backing plate
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, rug_z))
            base = bpy.context.active_object
            base.name = "RugBase"
            base.scale = (w, d, thickness)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(base, width=0.002)
            utils.apply_material(base, primary_mat)
            parts.append(base)

            # Inset Accent Borders: 4 thin border plates slightly elevated (1mm)
            border_w = 0.06  # 6cm border
            inset = 0.08     # 8cm from edge
            
            # Left & Right borders
            for sign in [-1, 1]:
                bx = sign * (w / 2.0 - inset)
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0, rug_z + 0.0005))
                border = bpy.context.active_object
                border.name = f"RugBorderSide_{sign}"
                border.scale = (border_w, d - 2 * inset, thickness)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_material(border, accent_mat)
                parts.append(border)
                
            # Top & Bottom borders
            for sign in [-1, 1]:
                by = sign * (d / 2.0 - inset)
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, by, rug_z + 0.0005))
                border = bpy.context.active_object
                border.name = f"RugBorderEnd_{sign}"
                border.scale = (w - 2 * inset - 2 * border_w, border_w, thickness)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_material(border, accent_mat)
                parts.append(border)

            # Center medallion (Accent Diamond)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, rug_z + 0.001))
            medallion = bpy.context.active_object
            medallion.name = "RugMedallion"
            med_size = min(w, d) * 0.3
            medallion.scale = (med_size, med_size, thickness)
            medallion.rotation_euler = (0, 0, math.radians(45.0))
            bpy.ops.object.transform_apply(rotation=True, scale=True)
            utils.apply_material(medallion, accent_mat)
            parts.append(medallion)

        else: # geometric pattern (center diamond and corner diamonds)
            # Primary backing plate
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, rug_z))
            base = bpy.context.active_object
            base.name = "RugBase"
            base.scale = (w, d, thickness)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(base, width=0.002)
            utils.apply_material(base, primary_mat)
            parts.append(base)

            # Add multiple diamond elements on top
            diamond_coords = [
                (0, 0),                       # center
                (-w * 0.25, -d * 0.25),      # bottom left
                (-w * 0.25, d * 0.25),       # top left
                (w * 0.25, -d * 0.25),       # bottom right
                (w * 0.25, d * 0.25)         # top right
            ]
            
            dia_size = min(w, d) * 0.18
            for idx, (dx, dy) in enumerate(diamond_coords):
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, dy, rug_z + 0.0005))
                dia = bpy.context.active_object
                dia.name = f"RugGeoDiamond_{idx}"
                dia.scale = (dia_size, dia_size, thickness)
                dia.rotation_euler = (0, 0, math.radians(45.0))
                bpy.ops.object.transform_apply(rotation=True, scale=True)
                utils.apply_material(dia, accent_mat)
                parts.append(dia)

        # Add Edge Tassel Fringes on Left (-X) and Right (+X) sides
        num_tassels = 18
        tassel_l = 0.04  # 4cm tassel length
        tassel_spacing = d / (num_tassels - 1)
        for sign in [-1, 1]: # left and right
            tx = sign * (w / 2.0 + tassel_l / 2.0)
            for j in range(num_tassels):
                ty = -d / 2.0 + j * tassel_spacing
                # Create a thin box segment for each tassel
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(tx, ty, rug_z))
                tassel = bpy.context.active_object
                tassel.name = f"RugTassel_{sign}_{j}"
                tassel.scale = (tassel_l, 0.005, thickness * 0.6)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_material(tassel, fringe_mat)
                parts.append(tassel)

    else: # circular rug
        radius = w / 2.0
        if pattern == "solid":
            # Single circular plate
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=64,
                radius=radius,
                depth=thickness,
                location=(0, 0, rug_z),
                rotation=(0, 0, 0)
            )
            base = bpy.context.active_object
            base.name = "RugBase_Circ"
            utils.apply_smooth_by_angle(base, angle=30.0)
            utils.apply_bevel(base, width=0.002)
            utils.apply_material(base, primary_mat)
            parts.append(base)
            
        elif pattern == "striped" or pattern == "oriental" or pattern == "geometric":
            # Concentric rings of alternating materials
            # 3 rings (outer, middle, center)
            rings = [
                {"name": "RugOuterRing", "r_outer": radius, "r_inner": radius * 0.72, "mat": primary_mat},
                {"name": "RugMidRing", "r_outer": radius * 0.72, "r_inner": radius * 0.38, "mat": accent_mat},
                {"name": "RugCenterCircle", "r_outer": radius * 0.38, "r_inner": 0.0, "mat": primary_mat}
            ]
            
            for ring in rings:
                r_out = ring["r_outer"]
                r_in = ring["r_inner"]
                
                if r_in > 0:
                    # Create an outer ring using a thin cylinder and Boolean diff, or extruding a circle
                    # Simplest robust way is to create a cylinder of outer radius, and a slightly taller cylinder of inner radius, and run Boolean subtraction.
                    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r_out, depth=thickness, location=(0, 0, rug_z))
                    outer_cyl = bpy.context.active_object
                    outer_cyl.name = ring["name"]
                    utils.apply_smooth_by_angle(outer_cyl, angle=30.0)
                    
                    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r_in, depth=thickness * 2.0, location=(0, 0, rug_z))
                    inner_cyl = bpy.context.active_object
                    inner_cyl.name = f"{ring['name']}_Hole"
                    
                    # Boolean Modifier
                    bpy.ops.object.select_all(action='DESELECT')
                    outer_cyl.select_set(True)
                    bpy.context.view_layer.objects.active = outer_cyl
                    
                    bool_mod = outer_cyl.modifiers.new(name="HoleMod", type='BOOLEAN')
                    bool_mod.operation = 'DIFFERENCE'
                    bool_mod.object = inner_cyl
                    bpy.ops.object.modifier_apply(modifier="HoleMod")
                    
                    # Delete inner cutter cylinder
                    bpy.ops.object.select_all(action='DESELECT')
                    inner_cyl.select_set(True)
                    bpy.ops.object.delete()
                    
                    utils.apply_material(outer_cyl, ring["mat"])
                    parts.append(outer_cyl)
                else:
                    # Solid center circle
                    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r_out, depth=thickness, location=(0, 0, rug_z))
                    center_cyl = bpy.context.active_object
                    center_cyl.name = ring["name"]
                    utils.apply_smooth_by_angle(center_cyl, angle=30.0)
                    utils.apply_material(center_cyl, ring["mat"])
                    parts.append(center_cyl)

    # 2. Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    
    parts[0].name = "RugAsset"
    
    # Set origin to the center on floor level (Z = 0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return parts[0]

def main():
    parser = argparse.ArgumentParser(description="Procedural Rug Generator")
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
    rug_obj = generate_rug(params)
    
    if args.render:
        utils.setup_lighting_and_camera(rug_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
