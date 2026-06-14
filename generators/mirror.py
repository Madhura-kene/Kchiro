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


# ---------------------------------------------------------------------------
# Helper: add a UV-sphere as a decorative rosette/stud
# ---------------------------------------------------------------------------
def _add_rosette(location, radius, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=24, ring_count=16, location=location)
    obj = bpy.context.active_object
    utils.apply_smooth_by_angle(obj, angle=30.0)
    utils.apply_material(obj, mat)
    return obj


# ---------------------------------------------------------------------------
# Helper: add a small torus for a ring ornament
# ---------------------------------------------------------------------------
def _add_ring(location, major_r, minor_r, rot_x_deg, mat):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_r,
        minor_radius=minor_r,
        major_segments=48,
        minor_segments=12,
        location=location
    )
    obj = bpy.context.active_object
    obj.rotation_euler = (math.radians(rot_x_deg), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    utils.apply_smooth_by_angle(obj, angle=30.0)
    utils.apply_material(obj, mat)
    return obj


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------
def generate_mirror(params):
    w = params.get("width",  60.0) / 100.0   # cm → m
    h = params.get("height", 80.0) / 100.0
    shape        = params.get("shape",        "rectangular")
    border_style = params.get("border_style", "metallic")
    border_color = params.get("border_color", "gold")

    # Circular mirrors are square in bounding-box
    if shape == "circular":
        h = w

    parts = []

    # ------------------------------------------------------------------
    # 1.  MATERIALS
    # ------------------------------------------------------------------
    # Frame  ────────────────────────────────────────────────────────────
    if border_color == "gold":
        frame_base  = (0.88, 0.67, 0.18, 1.0)
        frame_metal = 1.0
        frame_rough = 0.15
        accent_base = (0.95, 0.85, 0.40, 1.0)   # brighter gold for rosettes
        accent_metal= 1.0
        accent_rough= 0.08
    elif border_color == "chrome":
        frame_base  = (0.92, 0.92, 0.94, 1.0)
        frame_metal = 1.0
        frame_rough = 0.05
        accent_base = (1.00, 1.00, 1.00, 1.0)
        accent_metal= 1.0
        accent_rough= 0.02
    elif border_color == "wood":
        frame_base  = (0.38, 0.22, 0.10, 1.0)
        frame_metal = 0.0
        frame_rough = 0.70
        accent_base = (0.55, 0.35, 0.15, 1.0)
        accent_metal= 0.0
        accent_rough= 0.55
    elif border_color == "black":
        frame_base  = (0.04, 0.04, 0.05, 1.0)
        frame_metal = 0.85
        frame_rough = 0.20
        accent_base = (0.15, 0.15, 0.18, 1.0)
        accent_metal= 0.90
        accent_rough= 0.10
    else:  # white / default
        frame_base  = (0.90, 0.88, 0.84, 1.0)
        frame_metal = 0.05
        frame_rough = 0.45
        accent_base = (1.00, 0.98, 0.95, 1.0)
        accent_metal= 0.10
        accent_rough= 0.30

    frame_mat  = utils.create_material(f"MirrorFrame_{border_color}",
                                       diffuse_color=frame_base,
                                       metallic=frame_metal,
                                       roughness=frame_rough)
    accent_mat = utils.create_material(f"MirrorAccent_{border_color}",
                                       diffuse_color=accent_base,
                                       metallic=accent_metal,
                                       roughness=accent_rough)
    # Mirror glass  ─────────────────────────────────────────────────────
    glass_mat  = utils.create_material("MirrorGlass",
                                       diffuse_color=(0.78, 0.90, 0.96, 1.0),
                                       metallic=1.0,
                                       roughness=0.0)
    # Backing plate  ────────────────────────────────────────────────────
    back_mat   = utils.create_material("MirrorBacking",
                                       diffuse_color=(0.12, 0.10, 0.08, 1.0),
                                       metallic=0.0,
                                       roughness=0.9)

    # ------------------------------------------------------------------
    # 2.  GEOMETRY CONSTANTS
    # ------------------------------------------------------------------
    has_frame      = (border_style != "frameless")
    ft             = 0.055 if has_frame else 0.0   # frame thickness (width of border)
    fd             = 0.045                          # frame depth (how deep the frame protrudes)
    glass_d        = 0.012                          # glass slab depth
    lip_t          = 0.012                          # inner reveal lip thickness
    lip_d          = 0.018                          # inner reveal lip depth
    back_d         = 0.010                          # backing plate depth
    center_z       = h / 2.0

    # ------------------------------------------------------------------
    # 3.  RECTANGULAR MIRROR
    # ------------------------------------------------------------------
    if shape == "rectangular":

        if has_frame:
            # ── 3a. Outer frame slab  ──────────────────────────────────
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, center_z))
            frame_outer = bpy.context.active_object
            frame_outer.name = "MirrorFrameOuter"
            frame_outer.scale = (w, fd, h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(frame_outer, width=0.006, segments=3)
            utils.apply_material(frame_outer, frame_mat)
            parts.append(frame_outer)

            # ── 3b. Inner reveal lip  ──────────────────────────────────
            # Four thin bars forming the inner chamfer / step
            inner_w = w - ft * 2
            inner_h = h - ft * 2

            for side, loc, sz in [
                ("Top",    (0, -lip_d/2.0 + fd/2.0 - 0.001, center_z + inner_h/2.0 + lip_t/2.0),
                           (inner_w + lip_t * 2, lip_d, lip_t)),
                ("Bot",    (0, -lip_d/2.0 + fd/2.0 - 0.001, center_z - inner_h/2.0 - lip_t/2.0),
                           (inner_w + lip_t * 2, lip_d, lip_t)),
                ("Left",   (-inner_w/2.0 - lip_t/2.0, -lip_d/2.0 + fd/2.0 - 0.001, center_z),
                           (lip_t, lip_d, inner_h)),
                ("Right",  ( inner_w/2.0 + lip_t/2.0, -lip_d/2.0 + fd/2.0 - 0.001, center_z),
                           (lip_t, lip_d, inner_h)),
            ]:
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
                lip = bpy.context.active_object
                lip.name = f"MirrorLip_{side}"
                lip.scale = sz
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_material(lip, frame_mat)
                parts.append(lip)

            # ── 3c. Mirror glass inset  ────────────────────────────────
            bpy.ops.mesh.primitive_cube_add(size=1.0,
                location=(0, (fd/2.0 - glass_d/2.0 + 0.002), center_z))
            glass_obj = bpy.context.active_object
            glass_obj.name = "MirrorGlass"
            glass_obj.scale = (inner_w, glass_d, inner_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(glass_obj, glass_mat)
            parts.append(glass_obj)

            # ── 3d. Backing plate  ────────────────────────────────────
            bpy.ops.mesh.primitive_cube_add(size=1.0,
                location=(0, -(fd/2.0 + back_d/2.0), center_z))
            back = bpy.context.active_object
            back.name = "MirrorBacking"
            back.scale = (w * 0.98, back_d, h * 0.98)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(back, back_mat)
            parts.append(back)

            # ── 3e. Corner rosettes (4 spheres)  ──────────────────────
            r_off_x = w / 2.0
            r_off_z = h / 2.0
            rosette_r = ft * 0.70
            rosette_y  = fd / 2.0 + rosette_r * 0.3
            for sx, sz_off in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                p = _add_rosette(
                    location=(sx * r_off_x, rosette_y, center_z + sz_off * r_off_z),
                    radius=rosette_r,
                    mat=accent_mat
                )
                parts.append(p)

            # ── 3f. Mid-edge accent rings (top & bottom)  ─────────────
            ring_major = ft * 0.38
            ring_minor = ft * 0.10
            for z_pos in [center_z + h/2.0 - ft * 0.5, center_z - h/2.0 + ft * 0.5]:
                p = _add_ring(
                    location=(0, fd / 2.0 + ring_minor, z_pos),
                    major_r=ring_major, minor_r=ring_minor,
                    rot_x_deg=90.0, mat=accent_mat
                )
                parts.append(p)

        else:
            # Frameless — just a clean beveled glass slab
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -glass_d / 2.0, center_z))
            glass_obj = bpy.context.active_object
            glass_obj.name = "MirrorGlass"
            glass_obj.scale = (w, glass_d, h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(glass_obj, width=0.004, segments=4)
            utils.apply_material(glass_obj, glass_mat)
            parts.append(glass_obj)

    # ------------------------------------------------------------------
    # 4.  CIRCULAR / OVAL MIRROR
    # ------------------------------------------------------------------
    elif shape in ["circular", "oval"]:
        r_x = w / 2.0
        r_z = h / 2.0

        if has_frame:
            # ── 4a. Outer frame ring  ──────────────────────────────────
            # Cylinder default: axis along Z, flat caps face ±Z.
            # We rotate 90° on X so the axis becomes Y (depth into wall).
            # Scale BEFORE applying rotation so X/Y are the radii, Z is depth.
            bpy.ops.mesh.primitive_cylinder_add(
                radius=1.0, depth=1.0,
                vertices=64,
                location=(0, 0, center_z))
            frame_outer = bpy.context.active_object
            frame_outer.name = "MirrorFrameOuter"
            frame_outer.scale = (r_x + ft, r_z + ft, fd)     # X=width, Y=height, Z=depth
            frame_outer.rotation_euler = (math.radians(90.0), 0, 0)  # now Z→Y (depth)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            utils.apply_smooth_by_angle(frame_outer, angle=30.0)
            utils.apply_bevel(frame_outer, width=0.005, segments=3)
            utils.apply_material(frame_outer, frame_mat)
            parts.append(frame_outer)

            # ── 4b. Inner reveal lip  ──────────────────────────────────
            bpy.ops.mesh.primitive_cylinder_add(
                radius=1.0, depth=1.0,
                vertices=64,
                location=(0, (fd/2.0 - lip_d/2.0 - 0.002), center_z))
            lip = bpy.context.active_object
            lip.name = "MirrorLip"
            lip.scale = (r_x + lip_t, r_z + lip_t, lip_d)
            lip.rotation_euler = (math.radians(90.0), 0, 0)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            utils.apply_smooth_by_angle(lip, angle=30.0)
            utils.apply_material(lip, frame_mat)
            parts.append(lip)

            # ── 4c. Glass disc  ───────────────────────────────────────
            bpy.ops.mesh.primitive_cylinder_add(
                radius=1.0, depth=1.0,
                vertices=64,
                location=(0, (fd/2.0 - glass_d/2.0 + 0.002), center_z))
            glass_obj = bpy.context.active_object
            glass_obj.name = "MirrorGlass"
            glass_obj.scale = (r_x, r_z, glass_d)
            glass_obj.rotation_euler = (math.radians(90.0), 0, 0)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            utils.apply_smooth_by_angle(glass_obj, angle=30.0)
            utils.apply_material(glass_obj, glass_mat)
            parts.append(glass_obj)

            # ── 4d. Backing plate  ────────────────────────────────────
            bpy.ops.mesh.primitive_cylinder_add(
                radius=1.0, depth=1.0,
                vertices=64,
                location=(0, -(fd/2.0 + back_d/2.0), center_z))
            back = bpy.context.active_object
            back.name = "MirrorBacking"
            back.scale = (r_x * 0.97, r_z * 0.97, back_d)
            back.rotation_euler = (math.radians(90.0), 0, 0)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            utils.apply_smooth_by_angle(back, angle=30.0)
            utils.apply_material(back, back_mat)
            parts.append(back)

            # ── 4e. Decorative rosette ring around the border  ────────
            #        Place 8 small spheres evenly around the frame edge
            n_studs = 8
            stud_r  = ft * 0.42
            stud_orbit_x = r_x + ft * 0.45
            stud_orbit_z = r_z + ft * 0.45
            stud_y = fd / 2.0 + stud_r * 0.2
            for i in range(n_studs):
                angle = (2.0 * math.pi * i) / n_studs
                sx = math.cos(angle) * stud_orbit_x
                sz = math.sin(angle) * stud_orbit_z
                p = _add_rosette(
                    location=(sx, stud_y, center_z + sz),
                    radius=stud_r,
                    mat=accent_mat
                )
                parts.append(p)

            # ── 4f. Centre-top crown accent ring  ─────────────────────
            crown_y = fd / 2.0 + ft * 0.08
            p = _add_ring(
                location=(0, crown_y, center_z + r_z + ft * 0.55),
                major_r=ft * 0.35, minor_r=ft * 0.09,
                rot_x_deg=90.0, mat=accent_mat
            )
            parts.append(p)

        else:
            # Frameless oval/circle
            bpy.ops.mesh.primitive_cylinder_add(
                radius=1.0, depth=1.0,
                vertices=64,
                location=(0, -glass_d / 2.0, center_z))
            glass_obj = bpy.context.active_object
            glass_obj.name = "MirrorGlass"
            glass_obj.scale = (r_x, r_z, glass_d)
            glass_obj.rotation_euler = (math.radians(90.0), 0, 0)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            utils.apply_smooth_by_angle(glass_obj, angle=30.0)
            utils.apply_bevel(glass_obj, width=0.003, segments=3)
            utils.apply_material(glass_obj, glass_mat)
            parts.append(glass_obj)

    # ------------------------------------------------------------------
    # 5.  JOIN & FINALISE
    # ------------------------------------------------------------------
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)

    main_obj = parts[0]
    bpy.context.view_layer.objects.active = main_obj
    bpy.ops.object.join()

    main_obj.name = "MirrorAsset"
    # Place origin at world cursor (0,0,0) → bottom-center
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return main_obj


# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Procedural Mirror Generator")
    parser.add_argument("--params", type=str, required=True)
    parser.add_argument("--export", type=str, required=True)
    parser.add_argument("--render", type=str)

    try:
        args_idx = sys.argv.index("--")
        script_args = sys.argv[args_idx + 1:]
    except ValueError:
        script_args = []

    args = parser.parse_args(script_args)

    with open(args.params, 'r') as f:
        params = json.load(f)

    utils.cleanup_scene()
    obj = generate_mirror(params)

    if args.render:
        utils.setup_lighting_and_camera(obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)


if __name__ == "__main__":
    main()
