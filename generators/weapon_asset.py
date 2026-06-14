import argparse
import json
import math
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    import bpy
    import blender.utils as utils
    from mathutils import Vector
except ImportError:
    print("Failed to import Blender API (bpy), mathutils, or utilities.")
    sys.exit(1)


OVERLAP = 0.004


def cm(value, fallback=0.0):
    try:
        return float(value) / 100.0
    except Exception:
        return float(fallback) / 100.0


def build_materials():
    return {
        "steel": utils.create_material("WeaponSteel", diffuse_color=(0.7, 0.74, 0.78, 1.0), metallic=0.9, roughness=0.24),
        "iron": utils.create_material("WeaponIron", diffuse_color=(0.34, 0.36, 0.39, 1.0), metallic=0.8, roughness=0.38),
        "brass": utils.create_material("WeaponBrass", diffuse_color=(0.84, 0.66, 0.23, 1.0), metallic=0.94, roughness=0.16),
        "bronze": utils.create_material("WeaponBronze", diffuse_color=(0.66, 0.45, 0.22, 1.0), metallic=0.82, roughness=0.28),
        "wood": utils.create_material("WeaponWood", diffuse_color=(0.43, 0.28, 0.16, 1.0), metallic=0.0, roughness=0.68),
        "darkwood": utils.create_material("WeaponDarkWood", diffuse_color=(0.22, 0.14, 0.09, 1.0), metallic=0.0, roughness=0.74),
        "leather": utils.create_material("WeaponLeather", diffuse_color=(0.27, 0.16, 0.1, 1.0), metallic=0.0, roughness=0.86),
        "bone": utils.create_material("WeaponBone", diffuse_color=(0.83, 0.79, 0.69, 1.0), metallic=0.0, roughness=0.58),
        "obsidian": utils.create_material("WeaponObsidian", diffuse_color=(0.08, 0.07, 0.11, 1.0), metallic=0.12, roughness=0.14),
        "stone": utils.create_material("WeaponStone", diffuse_color=(0.5, 0.5, 0.52, 1.0), metallic=0.0, roughness=0.93),
        "glass": utils.create_material("WeaponGlass", diffuse_color=(0.74, 0.9, 0.98, 1.0), metallic=0.06, roughness=0.06),
        "string": utils.create_material("WeaponString", diffuse_color=(0.77, 0.72, 0.62, 1.0), metallic=0.0, roughness=0.92),
        "feather_white": utils.create_material("WeaponFeatherWhite", diffuse_color=(0.93, 0.94, 0.96, 1.0), metallic=0.0, roughness=0.78),
        "feather_red": utils.create_material("WeaponFeatherRed", diffuse_color=(0.8, 0.24, 0.22, 1.0), metallic=0.0, roughness=0.72),
        "feather_black": utils.create_material("WeaponFeatherBlack", diffuse_color=(0.12, 0.12, 0.14, 1.0), metallic=0.0, roughness=0.88),
        "feather_green": utils.create_material("WeaponFeatherGreen", diffuse_color=(0.18, 0.46, 0.24, 1.0), metallic=0.0, roughness=0.74),
        "feather_blue": utils.create_material("WeaponFeatherBlue", diffuse_color=(0.22, 0.43, 0.76, 1.0), metallic=0.0, roughness=0.72),
        "crystal_blue": utils.create_material("WeaponCrystalBlue", diffuse_color=(0.33, 0.72, 0.96, 1.0), metallic=0.08, roughness=0.12),
        "crystal_green": utils.create_material("WeaponCrystalGreen", diffuse_color=(0.28, 0.78, 0.54, 1.0), metallic=0.08, roughness=0.14),
        "crystal_red": utils.create_material("WeaponCrystalRed", diffuse_color=(0.9, 0.28, 0.25, 1.0), metallic=0.1, roughness=0.14),
        "crystal_purple": utils.create_material("WeaponCrystalPurple", diffuse_color=(0.6, 0.36, 0.9, 1.0), metallic=0.1, roughness=0.14),
    }


def add_prism(width, depth, height, location, name, material=None, rotation=(0.0, 0.0, 0.0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (
        max(width, 0.01) / 2.0,
        max(depth, 0.01) / 2.0,
        max(height, 0.01) / 2.0,
    )
    bpy.ops.object.transform_apply(scale=True)
    if bevel > 0:
        utils.apply_bevel(obj, width=bevel)
    if material:
        utils.apply_material(obj, material)
    return obj


def add_cylinder(radius, height, location, name, material=None, vertices=24, rotation=(0.0, 0.0, 0.0), smooth=True):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=max(radius, 0.003),
        depth=max(height, 0.01),
        vertices=vertices,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.active_object
    obj.name = name
    if smooth:
        utils.apply_smooth_by_angle(obj)
    if material:
        utils.apply_material(obj, material)
    return obj


def add_sphere(radius, location, name, material=None, smooth=True):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=max(radius, 0.005), location=location, segments=32, ring_count=16)
    obj = bpy.context.active_object
    obj.name = name
    if smooth:
        utils.apply_smooth_by_angle(obj)
    if material:
        utils.apply_material(obj, material)
    return obj


def add_cone(radius, height, location, name, material=None, vertices=24, rotation=(0.0, 0.0, 0.0), scale_y=None):
    bpy.ops.mesh.primitive_cone_add(
        radius1=max(radius, 0.004),
        radius2=0.0,
        depth=max(height, 0.01),
        vertices=vertices,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.active_object
    obj.name = name
    if scale_y is not None:
        obj.scale = (1.0, max(scale_y, 0.08), 1.0)
        bpy.ops.object.transform_apply(scale=True)
    utils.apply_smooth_by_angle(obj)
    if material:
        utils.apply_material(obj, material)
    return obj


def add_segment_between(start, end, radius, name, material=None, vertices=16):
    start_vec = Vector(start)
    end_vec = Vector(end)
    direction = end_vec - start_vec
    length = direction.length
    if length < 0.0001:
        return None

    midpoint = (start_vec + end_vec) / 2.0
    bpy.ops.mesh.primitive_cylinder_add(
        radius=max(radius, 0.003),
        depth=max(length, 0.01),
        vertices=vertices,
        location=midpoint,
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = Vector((0.0, 0.0, 1.0)).rotation_difference(direction.normalized())
    utils.apply_smooth_by_angle(obj)
    if material:
        utils.apply_material(obj, material)
    return obj


def join_parts(parts, name):
    valid_parts = [part for part in parts if part is not None]
    bpy.ops.object.select_all(action="DESELECT")
    for part in valid_parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = valid_parts[0]
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = name
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
    utils.apply_smooth_by_angle(obj)
    return obj


def pick_material(material_key, mats, fallback):
    aliases = {
        "metal": "steel",
        "wood": "wood",
        "dark_wood": "darkwood",
        "darkwood": "darkwood",
        "composite": "darkwood",
        "horn": "bone",
        "crystal": "crystal_blue",
    }
    normalized = str(material_key or fallback).strip().lower().replace(" ", "_")
    return mats.get(aliases.get(normalized, normalized), mats[fallback])


def pick_fletching_material(color_name, mats):
    color_map = {
        "white": "feather_white",
        "red": "feather_red",
        "black": "feather_black",
        "green": "feather_green",
        "blue": "feather_blue",
    }
    normalized = str(color_name or "white").strip().lower()
    return mats[color_map.get(normalized, "feather_white")]


def pick_gem_material(color_name, mats):
    color_map = {
        "blue": "crystal_blue",
        "green": "crystal_green",
        "red": "crystal_red",
        "purple": "crystal_purple",
    }
    normalized = str(color_name or "blue").strip().lower()
    return mats[color_map.get(normalized, "crystal_blue")]


def add_leaf_tip(width, thickness, height, location, name, material):
    tip = add_cone(
        radius=width / 2.0,
        height=height,
        location=location,
        name=name,
        material=material,
        vertices=8,
        scale_y=max(thickness / max(width, 0.01), 0.16),
    )
    return tip


def add_fletching(parts, tail_z, shaft_radius, fin_height, fin_length, material):
    fin_width = max(shaft_radius * 0.55, 0.004)
    for index, angle in enumerate((0.0, math.radians(120.0), math.radians(240.0))):
        fin = add_prism(
            fin_width,
            max(fin_length, 0.008),
            max(fin_height, 0.015),
            (0.0, 0.0, tail_z + fin_height / 2.0),
            f"Fletching_{index}",
            material=material,
            rotation=(0.0, 0.0, angle),
            bevel=0.001,
        )
        fin.location.x += math.cos(angle) * shaft_radius * 0.9
        fin.location.y += math.sin(angle) * shaft_radius * 0.9
        parts.append(fin)


def add_axe_blade(span, height, thickness, location, direction, name, material):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    blade = bpy.context.active_object
    blade.name = name
    blade.scale = (max(span, 0.02) / 2.0, max(thickness, 0.006) / 2.0, max(height, 0.02) / 2.0)
    bpy.ops.object.transform_apply(scale=True)

    for vertex in blade.data.vertices:
        edge_side = vertex.co.x > 0 if direction > 0 else vertex.co.x < 0
        if edge_side:
            vertex.co.x += direction * span * 0.22
            vertex.co.z *= 1.18
            vertex.co.y *= 0.18
        else:
            vertex.co.x *= 0.52

    blade.data.update()
    utils.apply_bevel(blade, width=0.0018)
    utils.apply_material(blade, material)
    return blade


def generate_sword(params, mats, asset_type="sword"):
    blade_length = cm(params.get("blade_length", 90.0 if asset_type == "sword" else 38.0))
    blade_width = cm(params.get("blade_width", 5.0 if asset_type == "sword" else 3.8))
    grip_length = cm(params.get("grip_length", 15.0 if asset_type == "sword" else 11.0))
    crossguard_type = params.get("crossguard_type", "simple")
    grip_material = pick_material(params.get("grip_material", "leather"), mats, "leather")
    pommel_material = mats["brass"]
    blade_material = mats["steel"]

    blade_thickness = max(blade_width * 0.16, 0.008)
    pommel_radius = max(blade_width * (0.55 if asset_type == "dagger" else 0.48), 0.022 if asset_type == "dagger" else 0.026)
    grip_radius = max(blade_width * 0.26, 0.010 if asset_type == "dagger" else 0.012)
    guard_height = max(blade_width * 0.28, 0.016)
    guard_depth = max(blade_thickness * 1.6, 0.012)
    guard_span = blade_width * (2.6 if asset_type == "dagger" else 3.6)
    tip_length = max(blade_length * 0.18, 0.08 if asset_type == "sword" else 0.055)
    main_blade_length = max(blade_length - tip_length + OVERLAP, blade_length * 0.72)
    parts = []

    pommel = add_sphere(pommel_radius, (0.0, 0.0, pommel_radius), "Pommel", material=pommel_material)
    parts.append(pommel)

    grip_center_z = pommel_radius * 2.0 + grip_length / 2.0 - OVERLAP
    grip = add_cylinder(grip_radius, grip_length, (0.0, 0.0, grip_center_z), "Grip", material=grip_material, vertices=20)
    grip.scale = (1.0, 0.82, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    parts.append(grip)

    guard_z = grip_center_z + grip_length / 2.0 + guard_height / 2.0 - OVERLAP
    if crossguard_type == "curved":
        left_guard = add_prism(
            guard_span * 0.54,
            guard_depth,
            guard_height,
            (-guard_span * 0.24, 0.0, guard_z + guard_height * 0.08),
            "CrossguardLeft",
            material=pommel_material,
            rotation=(0.0, math.radians(-18.0), 0.0),
            bevel=0.002,
        )
        right_guard = add_prism(
            guard_span * 0.54,
            guard_depth,
            guard_height,
            (guard_span * 0.24, 0.0, guard_z + guard_height * 0.08),
            "CrossguardRight",
            material=pommel_material,
            rotation=(0.0, math.radians(18.0), 0.0),
            bevel=0.002,
        )
        parts.extend([left_guard, right_guard])
    elif crossguard_type == "none":
        parts.append(add_cylinder(blade_width * 0.45, guard_height, (0.0, 0.0, guard_z), "GuardRing", material=pommel_material, vertices=18))
    else:
        parts.append(add_prism(guard_span, guard_depth, guard_height, (0.0, 0.0, guard_z), "Crossguard", material=pommel_material, bevel=0.002))

    blade_start_z = guard_z + guard_height / 2.0 - OVERLAP
    blade_center_z = blade_start_z + main_blade_length / 2.0
    parts.append(
        add_prism(
            blade_width,
            blade_thickness,
            main_blade_length,
            (0.0, 0.0, blade_center_z),
            "Blade",
            material=blade_material,
            bevel=0.0012,
        )
    )
    parts.append(
        add_leaf_tip(
            blade_width,
            blade_thickness,
            tip_length,
            (0.0, 0.0, blade_start_z + main_blade_length + tip_length / 2.0 - OVERLAP),
            "BladeTip",
            blade_material,
        )
    )
    parts.append(
        add_prism(
            blade_width * 0.18,
            blade_thickness * 0.6,
            main_blade_length * 0.84,
            (0.0, 0.0, blade_start_z + main_blade_length * 0.44),
            "BladeRidge",
            material=mats["iron"],
            bevel=0.0008,
        )
    )

    return join_parts(parts, "SwordAsset" if asset_type == "sword" else "DaggerAsset")


def generate_axe(params, mats):
    shaft_length = cm(params.get("shaft_length", 80.0))
    axe_style = params.get("axe_style", "single")
    head_material = pick_material(params.get("head_material", "steel"), mats, "steel")
    shaft_material = pick_material(params.get("shaft_material", "wood"), mats, "wood")
    parts = []

    shaft_radius = max(shaft_length * 0.018, 0.016)
    shaft = add_cylinder(shaft_radius, shaft_length, (0.0, 0.0, shaft_length / 2.0), "AxeShaft", material=shaft_material, vertices=18)
    shaft.scale = (1.0, 0.78, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    parts.append(shaft)

    grip_length = shaft_length * 0.32
    parts.append(add_cylinder(shaft_radius + 0.0035, grip_length, (0.0, 0.0, grip_length / 2.0 + 0.04), "AxeGrip", material=mats["leather"], vertices=16))
    parts.append(add_sphere(shaft_radius * 1.3, (0.0, 0.0, shaft_radius * 1.3), "AxePommel", material=head_material))

    socket_height = max(shaft_length * 0.14, 0.11)
    socket_z = shaft_length - socket_height / 2.0 - shaft_radius * 0.2
    parts.append(add_prism(shaft_radius * 2.8, shaft_radius * 2.6, socket_height, (0.0, 0.0, socket_z), "AxeSocket", material=head_material, bevel=0.002))

    blade_span = max(shaft_length * 0.22, 0.18)
    blade_height = max(shaft_length * 0.16, 0.13)
    blade_thickness = max(shaft_radius * 0.75, 0.008)
    blade_offset = shaft_radius * 0.55
    parts.append(
        add_axe_blade(
            blade_span,
            blade_height,
            blade_thickness,
            (blade_span * 0.22 + blade_offset, 0.0, socket_z + blade_height * 0.02),
            1,
            "AxeBladeRight",
            head_material,
        )
    )
    if axe_style == "double":
        parts.append(
            add_axe_blade(
                blade_span,
                blade_height,
                blade_thickness,
                (-blade_span * 0.22 - blade_offset, 0.0, socket_z + blade_height * 0.02),
                -1,
                "AxeBladeLeft",
                head_material,
            )
        )

    top_spike_height = max(blade_height * 0.55, 0.08)
    parts.append(
        add_leaf_tip(
            shaft_radius * 2.1,
            blade_thickness,
            top_spike_height,
            (0.0, 0.0, socket_z + socket_height / 2.0 + top_spike_height / 2.0 - OVERLAP),
            "AxeTopSpike",
            head_material,
        )
    )

    return join_parts(parts, "AxeAsset")


def generate_hammer(params, mats):
    handle_length = cm(params.get("handle_length", 90.0))
    head_width = cm(params.get("head_width", 24.0))
    head_height = cm(params.get("head_height", 14.0))
    head_material = pick_material(params.get("head_material", "steel"), mats, "steel")
    handle_material = pick_material(params.get("handle_material", "wood"), mats, "wood")
    parts = []

    handle_radius = max(handle_length * 0.016, 0.014)
    parts.append(add_cylinder(handle_radius, handle_length, (0.0, 0.0, handle_length / 2.0), "HammerHandle", material=handle_material, vertices=18))
    parts.append(add_cylinder(handle_radius + 0.003, handle_length * 0.26, (0.0, 0.0, handle_length * 0.18), "HammerGrip", material=mats["leather"], vertices=16))
    parts.append(add_sphere(handle_radius * 1.2, (0.0, 0.0, handle_radius * 1.2), "HammerButtCap", material=head_material))

    collar_height = max(head_height * 0.6, 0.08)
    collar_z = handle_length - collar_height / 2.0 - handle_radius * 0.4
    parts.append(add_prism(handle_radius * 2.5, handle_radius * 2.3, collar_height, (0.0, 0.0, collar_z), "HammerCollar", material=head_material, bevel=0.002))

    head_depth = max(head_height * 0.62, 0.07)
    head_z = handle_length - head_height * 0.15
    parts.append(add_prism(head_width, head_depth, head_height, (0.0, 0.0, head_z), "HammerHead", material=head_material, bevel=0.0025))
    parts.append(add_prism(head_height * 0.4, head_depth * 0.84, head_height * 0.84, (head_width / 2.0 + head_height * 0.18, 0.0, head_z), "HammerFaceRight", material=head_material, bevel=0.0018))
    parts.append(add_prism(head_height * 0.4, head_depth * 0.78, head_height * 0.68, (-head_width / 2.0 - head_height * 0.16, 0.0, head_z), "HammerFaceLeft", material=head_material, bevel=0.0018))

    return join_parts(parts, "HammerAsset")


def generate_mace(params, mats):
    shaft_length = cm(params.get("shaft_length", 88.0))
    head_radius = cm(params.get("head_radius", 11.0))
    flange_count = int(params.get("flange_count", 6))
    shaft_material = pick_material(params.get("shaft_material", "wood"), mats, "wood")
    head_material = pick_material(params.get("head_material", "iron"), mats, "iron")
    parts = []

    shaft_radius = max(shaft_length * 0.015, 0.013)
    parts.append(add_cylinder(shaft_radius, shaft_length, (0.0, 0.0, shaft_length / 2.0), "MaceShaft", material=shaft_material, vertices=18))
    parts.append(add_cylinder(shaft_radius + 0.003, shaft_length * 0.26, (0.0, 0.0, shaft_length * 0.18), "MaceGrip", material=mats["leather"], vertices=16))
    parts.append(add_sphere(shaft_radius * 1.25, (0.0, 0.0, shaft_radius * 1.25), "MaceButtCap", material=head_material))

    head_center_z = shaft_length - head_radius * 0.15
    parts.append(add_sphere(head_radius * 0.72, (0.0, 0.0, head_center_z), "MaceCore", material=head_material))

    flange_total = max(4, min(flange_count, 10))
    for index in range(flange_total):
        angle = (math.pi * 2.0 * index) / flange_total
        flange = add_prism(
            head_radius * 1.4,
            max(head_radius * 0.22, 0.012),
            head_radius * 1.5,
            (0.0, 0.0, head_center_z),
            f"MaceFlange_{index}",
            material=head_material,
            rotation=(0.0, 0.0, angle),
            bevel=0.0016,
        )
        parts.append(flange)

    spike_height = max(head_radius * 0.7, 0.05)
    parts.append(add_leaf_tip(head_radius * 0.44, head_radius * 0.18, spike_height, (0.0, 0.0, head_center_z + head_radius * 0.8), "MaceSpike", head_material))
    return join_parts(parts, "MaceAsset")


def generate_spear(params, mats):
    shaft_length = cm(params.get("shaft_length", 240.0))
    tip_length = cm(params.get("tip_length", 42.0))
    shaft_material = pick_material(params.get("shaft_material", "wood"), mats, "wood")
    tip_material = pick_material(params.get("tip_material", "steel"), mats, "steel")
    parts = []

    shaft_radius = max(shaft_length * 0.006, 0.012)
    parts.append(add_cylinder(shaft_radius, shaft_length, (0.0, 0.0, shaft_length / 2.0), "SpearShaft", material=shaft_material, vertices=16))

    collar_height = max(tip_length * 0.18, 0.035)
    collar_z = shaft_length - collar_height / 2.0 + OVERLAP
    parts.append(add_cylinder(shaft_radius * 1.5, collar_height, (0.0, 0.0, collar_z), "SpearCollar", material=tip_material, vertices=16))

    tip_width = max(shaft_radius * 3.8, 0.03)
    tip_thickness = max(shaft_radius * 1.1, 0.01)
    tip_z = shaft_length + tip_length / 2.0 - OVERLAP
    parts.append(add_leaf_tip(tip_width, tip_thickness, tip_length, (0.0, 0.0, tip_z), "SpearTip", tip_material))
    return join_parts(parts, "SpearAsset")


def generate_halberd(params, mats):
    shaft_length = cm(params.get("shaft_length", 260.0))
    blade_size = cm(params.get("blade_size", 48.0))
    hook_size = cm(params.get("hook_size", 22.0))
    shaft_material = pick_material(params.get("shaft_material", "wood"), mats, "wood")
    head_material = pick_material(params.get("head_material", "steel"), mats, "steel")
    parts = []

    shaft_radius = max(shaft_length * 0.0065, 0.013)
    parts.append(add_cylinder(shaft_radius, shaft_length, (0.0, 0.0, shaft_length / 2.0), "HalberdShaft", material=shaft_material, vertices=18))

    head_anchor_z = shaft_length - blade_size * 0.12
    spear_tip_length = blade_size * 0.8
    parts.append(add_leaf_tip(shaft_radius * 4.2, shaft_radius * 1.2, spear_tip_length, (0.0, 0.0, shaft_length + spear_tip_length / 2.0 - OVERLAP), "HalberdTopTip", head_material))
    parts.append(add_prism(shaft_radius * 3.0, shaft_radius * 2.4, blade_size * 0.42, (0.0, 0.0, head_anchor_z), "HalberdSocket", material=head_material, bevel=0.0018))

    blade = add_axe_blade(
        blade_size * 0.68,
        blade_size * 0.72,
        max(shaft_radius * 0.9, 0.008),
        (blade_size * 0.14 + shaft_radius * 0.8, 0.0, head_anchor_z + blade_size * 0.04),
        1,
        "HalberdBlade",
        head_material,
    )
    parts.append(blade)

    hook = add_prism(
        hook_size * 0.7,
        max(shaft_radius * 0.8, 0.008),
        hook_size * 0.24,
        (-hook_size * 0.18 - shaft_radius, 0.0, head_anchor_z + hook_size * 0.18),
        "HalberdHook",
        material=head_material,
        rotation=(0.0, math.radians(-35.0), 0.0),
        bevel=0.0015,
    )
    parts.append(hook)
    return join_parts(parts, "HalberdAsset")


def generate_staff(params, mats):
    height = cm(params.get("height", 190.0))
    shaft_radius = cm(params.get("shaft_radius", 2.5))
    shaft_material = pick_material(params.get("material", "wood"), mats, "wood")
    tip_style = params.get("tip_style", "plain")
    parts = []

    parts.append(add_cylinder(shaft_radius, height, (0.0, 0.0, height / 2.0), "StaffShaft", material=shaft_material, vertices=18))

    if tip_style in {"ring", "carved"}:
        band_height = max(height * 0.035, 0.04)
        parts.append(add_cylinder(shaft_radius * 1.35, band_height, (0.0, 0.0, height - band_height / 2.0), "StaffBandTop", material=mats["brass"], vertices=18))
        parts.append(add_cylinder(shaft_radius * 1.25, band_height, (0.0, 0.0, band_height / 2.0 + 0.05), "StaffBandBottom", material=mats["brass"], vertices=18))
    if tip_style == "ring":
        parts.append(add_sphere(shaft_radius * 1.1, (0.0, 0.0, height + shaft_radius * 0.9), "StaffTopper", material=mats["brass"]))
    elif tip_style == "carved":
        parts.append(add_sphere(shaft_radius * 1.35, (0.0, 0.0, height + shaft_radius), "StaffTopper", material=shaft_material))
    return join_parts(parts, "StaffAsset")


def generate_bow(params, mats):
    height = cm(params.get("height", 170.0))
    width = cm(params.get("width", 56.0))
    material = pick_material(params.get("material", "wood"), mats, "wood")
    bow_style = params.get("bow_style", "longbow")
    parts = []

    thickness = max(width * 0.05, 0.012)
    handle_height = max(height * 0.18, 0.24)
    handle_radius = max(thickness * 1.2, 0.015)

    if bow_style == "recurve":
        points = [
            (0.0, 0.0, 0.0),
            (-width * 0.08, 0.0, height * 0.14),
            (width * 0.16, 0.0, height * 0.36),
            (width * 0.25, 0.0, height * 0.5),
            (width * 0.16, 0.0, height * 0.64),
            (-width * 0.08, 0.0, height * 0.86),
            (0.0, 0.0, height),
        ]
    elif bow_style == "shortbow":
        points = [
            (0.0, 0.0, 0.0),
            (width * 0.1, 0.0, height * 0.2),
            (width * 0.18, 0.0, height * 0.5),
            (width * 0.1, 0.0, height * 0.8),
            (0.0, 0.0, height),
        ]
    else:
        points = [
            (0.0, 0.0, 0.0),
            (width * 0.08, 0.0, height * 0.18),
            (width * 0.17, 0.0, height * 0.36),
            (width * 0.23, 0.0, height * 0.5),
            (width * 0.17, 0.0, height * 0.64),
            (width * 0.08, 0.0, height * 0.82),
            (0.0, 0.0, height),
        ]

    for index in range(len(points) - 1):
        parts.append(add_segment_between(points[index], points[index + 1], thickness / 2.0, f"BowLimb_{index}", material=material))

    handle_z = height * 0.5
    handle_x = max(point[0] for point in points) * 0.98
    parts.append(add_cylinder(handle_radius, handle_height, (handle_x, 0.0, handle_z), "BowGrip", material=mats["leather"], vertices=18))
    parts.append(add_segment_between(points[0], points[-1], thickness * 0.18, "BowString", material=mats["string"], vertices=10))
    return join_parts(parts, "BowAsset")


def generate_crossbow(params, mats):
    width = cm(params.get("width", 82.0))
    stock_length = cm(params.get("stock_length", 96.0))
    material = pick_material(params.get("material", "wood"), mats, "wood")
    has_bolt = bool(params.get("has_bolt", True))
    parts = []

    stock_width = max(width * 0.12, 0.06)
    stock_depth = max(stock_width * 0.55, 0.026)
    parts.append(add_prism(stock_width, stock_depth, stock_length, (0.0, 0.0, stock_length / 2.0), "CrossbowStock", material=material, bevel=0.0018))

    limb_z = stock_length * 0.8
    limb_points = [(-width / 2.0, 0.0, limb_z - width * 0.06), (0.0, 0.0, limb_z), (width / 2.0, 0.0, limb_z - width * 0.06)]
    parts.append(add_segment_between(limb_points[0], limb_points[1], stock_depth * 0.46, "CrossbowLimbLeft", material=mats["steel"]))
    parts.append(add_segment_between(limb_points[1], limb_points[2], stock_depth * 0.46, "CrossbowLimbRight", material=mats["steel"]))
    parts.append(add_segment_between(limb_points[0], limb_points[2], stock_depth * 0.1, "CrossbowString", material=mats["string"], vertices=10))

    stirrup_radius = max(stock_width * 0.36, 0.03)
    parts.append(add_cylinder(stirrup_radius, stock_depth * 0.75, (0.0, 0.0, stock_length - stock_depth * 0.35), "CrossbowStirrup", material=mats["steel"], rotation=(math.radians(90.0), 0.0, 0.0), vertices=18))
    parts.append(add_prism(stock_width * 0.48, stock_depth * 1.2, stock_width * 0.9, (0.0, 0.0, stock_length * 0.36), "CrossbowGrip", material=material, rotation=(math.radians(-18.0), 0.0, 0.0), bevel=0.0014))

    if has_bolt:
        bolt_length = stock_length * 0.72
        bolt_radius = max(stock_depth * 0.14, 0.005)
        bolt_center_z = stock_length * 0.62
        parts.append(add_cylinder(bolt_radius, bolt_length, (0.0, 0.0, bolt_center_z), "CrossbowBoltShaft", material=mats["darkwood"], vertices=12))
        parts.append(add_leaf_tip(stock_width * 0.18, stock_depth * 0.18, bolt_length * 0.18, (0.0, 0.0, bolt_center_z + bolt_length / 2.0 - OVERLAP), "CrossbowBoltTip", mats["steel"]))
    return join_parts(parts, "CrossbowAsset")


def generate_arrow_like(params, mats, asset_type="arrow"):
    default_length = 78.0 if asset_type == "arrow" else 34.0
    length = cm(params.get("length", default_length))
    shaft_radius = cm(params.get("shaft_radius", 1.0 if asset_type == "arrow" else 1.3))
    shaft_material = pick_material(params.get("shaft_material", "wood"), mats, "wood")
    tip_material = pick_material(params.get("tip_material", "steel"), mats, "steel")
    fletching_material = pick_fletching_material(params.get("fletching_color", "white"), mats)
    parts = []

    parts.append(add_cylinder(shaft_radius, length, (0.0, 0.0, length / 2.0), f"{asset_type.title()}Shaft", material=shaft_material, vertices=12))
    tip_length = max(length * (0.16 if asset_type == "arrow" else 0.2), 0.04)
    parts.append(add_leaf_tip(shaft_radius * 5.0, shaft_radius * 1.4, tip_length, (0.0, 0.0, length + tip_length / 2.0 - OVERLAP), f"{asset_type.title()}Tip", tip_material))
    add_fletching(
        parts,
        tail_z=max(length * 0.08, 0.04),
        shaft_radius=shaft_radius,
        fin_height=max(length * (0.12 if asset_type == "arrow" else 0.09), 0.05),
        fin_length=max(shaft_radius * 2.8, 0.012),
        material=fletching_material,
    )
    return join_parts(parts, "ArrowAsset" if asset_type == "arrow" else "BoltAsset")


def generate_magic_staff(params, mats):
    height = cm(params.get("height", 210.0))
    shaft_material = pick_material(params.get("shaft_material", "darkwood"), mats, "darkwood")
    head_style = params.get("head_style", "orb")
    gem_material = pick_gem_material(params.get("gem_color", "blue"), mats)
    parts = []

    shaft_radius = max(height * 0.012, 0.018)
    parts.append(add_cylinder(shaft_radius, height, (0.0, 0.0, height / 2.0), "MagicStaffShaft", material=shaft_material, vertices=18))
    parts.append(add_cylinder(shaft_radius * 1.18, height * 0.18, (0.0, 0.0, height * 0.18), "MagicStaffGrip", material=mats["leather"], vertices=18))
    crown_z = height
    parts.append(add_cylinder(shaft_radius * 1.5, height * 0.06, (0.0, 0.0, crown_z - height * 0.03), "MagicStaffCrownBand", material=mats["brass"], vertices=18))

    if head_style == "crystal":
        parts.append(add_leaf_tip(shaft_radius * 4.4, shaft_radius * 1.2, height * 0.18, (0.0, 0.0, crown_z + height * 0.09), "MagicStaffCrystal", gem_material))
        parts.append(add_prism(shaft_radius * 0.52, shaft_radius * 0.52, height * 0.11, (-shaft_radius * 1.2, 0.0, crown_z + height * 0.04), "MagicStaffClawLeft", material=mats["brass"], rotation=(0.0, math.radians(-22.0), 0.0), bevel=0.001))
        parts.append(add_prism(shaft_radius * 0.52, shaft_radius * 0.52, height * 0.11, (shaft_radius * 1.2, 0.0, crown_z + height * 0.04), "MagicStaffClawRight", material=mats["brass"], rotation=(0.0, math.radians(22.0), 0.0), bevel=0.001))
    elif head_style == "crescent":
        parts.append(add_prism(shaft_radius * 0.56, shaft_radius * 0.56, height * 0.16, (-shaft_radius * 1.5, 0.0, crown_z + height * 0.09), "MagicStaffHornLeft", material=mats["brass"], rotation=(0.0, math.radians(-35.0), 0.0), bevel=0.001))
        parts.append(add_prism(shaft_radius * 0.56, shaft_radius * 0.56, height * 0.16, (shaft_radius * 1.5, 0.0, crown_z + height * 0.09), "MagicStaffHornRight", material=mats["brass"], rotation=(0.0, math.radians(35.0), 0.0), bevel=0.001))
        parts.append(add_sphere(shaft_radius * 1.15, (0.0, 0.0, crown_z + height * 0.08), "MagicStaffGem", material=gem_material))
    else:
        parts.append(add_sphere(shaft_radius * 1.55, (0.0, 0.0, crown_z + height * 0.08), "MagicStaffOrb", material=gem_material))
        parts.append(add_prism(shaft_radius * 0.5, shaft_radius * 0.5, height * 0.12, (-shaft_radius * 1.05, 0.0, crown_z + height * 0.03), "MagicStaffProngLeft", material=mats["brass"], rotation=(0.0, math.radians(-18.0), 0.0), bevel=0.001))
        parts.append(add_prism(shaft_radius * 0.5, shaft_radius * 0.5, height * 0.12, (shaft_radius * 1.05, 0.0, crown_z + height * 0.03), "MagicStaffProngRight", material=mats["brass"], rotation=(0.0, math.radians(18.0), 0.0), bevel=0.001))
    return join_parts(parts, "MagicStaffAsset")


def generate_wand(params, mats):
    length = cm(params.get("length", 32.0))
    shaft_material = pick_material(params.get("shaft_material", "wood"), mats, "wood")
    tip_style = params.get("tip_style", "gem")
    gem_material = pick_gem_material(params.get("gem_color", "purple"), mats)
    parts = []

    shaft_radius = max(length * 0.04, 0.008)
    parts.append(add_cylinder(shaft_radius, length, (0.0, 0.0, length / 2.0), "WandShaft", material=shaft_material, vertices=16))
    parts.append(add_cylinder(shaft_radius * 1.18, length * 0.26, (0.0, 0.0, length * 0.14), "WandGrip", material=mats["leather"], vertices=16))

    if tip_style == "forked":
        parts.append(add_prism(shaft_radius * 0.5, shaft_radius * 0.5, length * 0.18, (-shaft_radius * 0.9, 0.0, length + length * 0.08), "WandForkLeft", material=mats["brass"], rotation=(0.0, math.radians(-18.0), 0.0), bevel=0.0008))
        parts.append(add_prism(shaft_radius * 0.5, shaft_radius * 0.5, length * 0.18, (shaft_radius * 0.9, 0.0, length + length * 0.08), "WandForkRight", material=mats["brass"], rotation=(0.0, math.radians(18.0), 0.0), bevel=0.0008))
    elif tip_style == "gem":
        parts.append(add_sphere(shaft_radius * 1.2, (0.0, 0.0, length + shaft_radius * 1.05), "WandGem", material=gem_material))
    else:
        parts.append(add_sphere(shaft_radius * 0.8, (0.0, 0.0, length + shaft_radius * 0.6), "WandCap", material=mats["brass"]))
    return join_parts(parts, "WandAsset")


def generate_orb(params, mats):
    diameter = cm(params.get("diameter", 24.0))
    orb_material = pick_material(params.get("orb_material", "crystal"), mats, "crystal_blue")
    stand_material = mats["brass"] if orb_material != mats["obsidian"] else mats["steel"]
    has_stand = bool(params.get("has_stand", True))
    parts = []

    orb_radius = max(diameter / 2.0, 0.04)
    orb_center_z = orb_radius + (orb_radius * 0.45 if has_stand else 0.0)
    parts.append(add_sphere(orb_radius, (0.0, 0.0, orb_center_z), "OrbCore", material=orb_material))

    if has_stand:
        base_height = max(orb_radius * 0.32, 0.025)
        parts.append(add_cylinder(orb_radius * 0.7, base_height, (0.0, 0.0, base_height / 2.0), "OrbBase", material=stand_material, vertices=18))
        parts.append(add_cylinder(orb_radius * 0.28, orb_radius * 0.55, (0.0, 0.0, base_height + orb_radius * 0.28), "OrbStem", material=stand_material, vertices=14))
        for index, angle in enumerate((0.0, math.radians(120.0), math.radians(240.0))):
            claw = add_prism(
                orb_radius * 0.18,
                orb_radius * 0.14,
                orb_radius * 0.66,
                (math.cos(angle) * orb_radius * 0.46, math.sin(angle) * orb_radius * 0.46, base_height + orb_radius * 0.56),
                f"OrbClaw_{index}",
                material=stand_material,
                rotation=(0.0, math.radians(18.0), angle),
                bevel=0.001,
            )
            parts.append(claw)
    return join_parts(parts, "OrbAsset")


GENERATOR_MAP = {
    "sword": lambda params, mats: generate_sword(params, mats, "sword"),
    "dagger": lambda params, mats: generate_sword(params, mats, "dagger"),
    "axe": generate_axe,
    "hammer": generate_hammer,
    "mace": generate_mace,
    "spear": generate_spear,
    "halberd": generate_halberd,
    "staff": generate_staff,
    "bow": generate_bow,
    "crossbow": generate_crossbow,
    "arrow": lambda params, mats: generate_arrow_like(params, mats, "arrow"),
    "bolt": lambda params, mats: generate_arrow_like(params, mats, "bolt"),
    "magic_staff": generate_magic_staff,
    "wand": generate_wand,
    "orb": generate_orb,
}


def generate_weapon(params):
    mats = build_materials()
    asset_type = params.get("asset_type")
    if asset_type not in GENERATOR_MAP:
        raise ValueError(f"Unsupported weapon asset_type: {asset_type}")
    return GENERATOR_MAP[asset_type](params, mats)


def main():
    parser = argparse.ArgumentParser(description="Procedural Weapon Asset Generator")
    parser.add_argument("--params", type=str, required=True, help="Path to JSON parameter file")
    parser.add_argument("--export", type=str, required=True, help="Path to export GLB")
    parser.add_argument("--render", type=str, help="Path to render preview PNG")

    try:
        args_idx = sys.argv.index("--")
        script_args = sys.argv[args_idx + 1:]
    except ValueError:
        script_args = []

    args = parser.parse_args(script_args)

    with open(args.params, "r") as file_handle:
        params = json.load(file_handle)

    utils.cleanup_scene()
    asset_obj = generate_weapon(params)

    if args.render:
        utils.setup_lighting_and_camera(asset_obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)


if __name__ == "__main__":
    main()
