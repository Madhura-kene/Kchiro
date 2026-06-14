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
except ImportError:
    print("Failed to import Blender API (bpy) or utilities.")
    sys.exit(1)


OVERLAP = 0.004


def cm(value, fallback=0.0):
    try:
        return float(value) / 100.0
    except Exception:
        return float(fallback) / 100.0


def build_materials():
    return {
        "steel": utils.create_material("AdventureSteel", diffuse_color=(0.68, 0.72, 0.77, 1.0), metallic=0.88, roughness=0.24),
        "iron": utils.create_material("AdventureIron", diffuse_color=(0.33, 0.35, 0.39, 1.0), metallic=0.78, roughness=0.42),
        "bronze": utils.create_material("AdventureBronze", diffuse_color=(0.63, 0.45, 0.24, 1.0), metallic=0.78, roughness=0.28),
        "brass": utils.create_material("AdventureBrass", diffuse_color=(0.84, 0.68, 0.24, 1.0), metallic=0.9, roughness=0.18),
        "gold": utils.create_material("AdventureGold", diffuse_color=(0.91, 0.75, 0.22, 1.0), metallic=0.96, roughness=0.14),
        "copper": utils.create_material("AdventureCopper", diffuse_color=(0.76, 0.39, 0.22, 1.0), metallic=0.85, roughness=0.24),
        "wood": utils.create_material("AdventureWood", diffuse_color=(0.44, 0.29, 0.17, 1.0), roughness=0.68),
        "darkwood": utils.create_material("AdventureDarkWood", diffuse_color=(0.22, 0.14, 0.09, 1.0), roughness=0.76),
        "stone": utils.create_material("AdventureStone", diffuse_color=(0.56, 0.54, 0.5, 1.0), roughness=0.95),
        "brick": utils.create_material("AdventureBrick", diffuse_color=(0.56, 0.24, 0.18, 1.0), roughness=0.9),
        "leather": utils.create_material("AdventureLeather", diffuse_color=(0.28, 0.16, 0.1, 1.0), roughness=0.86),
        "cloth_red": utils.create_material("AdventureClothRed", diffuse_color=(0.66, 0.18, 0.18, 1.0), roughness=0.84),
        "cloth_blue": utils.create_material("AdventureClothBlue", diffuse_color=(0.2, 0.37, 0.66, 1.0), roughness=0.84),
        "cloth_green": utils.create_material("AdventureClothGreen", diffuse_color=(0.2, 0.46, 0.2, 1.0), roughness=0.84),
        "cloth_black": utils.create_material("AdventureClothBlack", diffuse_color=(0.09, 0.09, 0.12, 1.0), roughness=0.92),
        "cloth_brown": utils.create_material("AdventureClothBrown", diffuse_color=(0.33, 0.22, 0.15, 1.0), roughness=0.88),
        "cloth_gray": utils.create_material("AdventureClothGray", diffuse_color=(0.45, 0.47, 0.5, 1.0), roughness=0.86),
        "cloth_white": utils.create_material("AdventureClothWhite", diffuse_color=(0.91, 0.91, 0.88, 1.0), roughness=0.84),
        "cloth_gold": utils.create_material("AdventureClothGold", diffuse_color=(0.84, 0.71, 0.22, 1.0), roughness=0.8),
        "canvas": utils.create_material("AdventureCanvas", diffuse_color=(0.72, 0.66, 0.54, 1.0), roughness=0.9),
        "hide": utils.create_material("AdventureHide", diffuse_color=(0.44, 0.32, 0.2, 1.0), roughness=0.9),
        "rope": utils.create_material("AdventureRope", diffuse_color=(0.72, 0.63, 0.43, 1.0), roughness=0.95),
        "glass": utils.create_material("AdventureGlass", diffuse_color=(0.8, 0.92, 0.98, 1.0), metallic=0.04, roughness=0.08),
        "ember": utils.create_material("AdventureEmber", diffuse_color=(0.88, 0.28, 0.14, 1.0), roughness=0.36),
        "flame": utils.create_material("AdventureFlame", diffuse_color=(0.96, 0.58, 0.14, 1.0), roughness=0.28),
        "shadow": utils.create_material("AdventureShadow", diffuse_color=(0.16, 0.16, 0.18, 1.0), roughness=0.96),
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


def add_sphere(radius, location, name, material=None, scale=(1.0, 1.0, 1.0)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=max(radius, 0.005), location=location, segments=28, ring_count=14)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_smooth_by_angle(obj)
    if material:
        utils.apply_material(obj, material)
    return obj


def add_cone(radius, height, location, name, material=None, vertices=20, rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0)):
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
    obj.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_smooth_by_angle(obj)
    if material:
        utils.apply_material(obj, material)
    return obj


def add_tapered_cylinder(radius_bottom, radius_top, height, location, name, material=None, vertices=24, rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cone_add(
        radius1=max(radius_bottom, 0.003),
        radius2=max(radius_top, 0.001),
        depth=max(height, 0.01),
        vertices=vertices,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.active_object
    obj.name = name
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


def material_for(key, mats, fallback):
    aliases = {
        "plate": "steel",
        "metal": "iron",
        "cloth": "canvas",
        "travel": "leather",
        "riding": "leather",
        "breastplate": "steel",
        "knight": "steel",
        "fantasy": "bronze",
        "a_frame": "canvas",
        "ridge": "canvas",
        "pup": "canvas",
        "cuirass": "steel",
    }
    normalized = str(key or fallback).strip().lower().replace(" ", "_")
    return mats.get(aliases.get(normalized, normalized), mats[fallback])


def cloth_material(color_key, mats):
    mapping = {
        "red": "cloth_red",
        "blue": "cloth_blue",
        "green": "cloth_green",
        "black": "cloth_black",
        "brown": "cloth_brown",
        "gray": "cloth_gray",
        "grey": "cloth_gray",
        "white": "cloth_white",
        "gold": "cloth_gold",
        "striped": "cloth_red",
    }
    normalized = str(color_key or "red").strip().lower().replace(" ", "_")
    return mats[mapping.get(normalized, "cloth_red")]


def generate_chestplate(params, mats):
    width = cm(params.get("width", 58.0))
    height = cm(params.get("height", 72.0))
    depth = cm(params.get("depth", 28.0))
    material = material_for(params.get("material", "steel"), mats, "steel")
    style = str(params.get("style", "knight")).lower()
    accent = mats["bronze"] if style == "fantasy" else mats["brass"]
    parts = []

    parts.append(add_prism(width * 0.72, depth * 0.64, height * 0.46, (0.0, 0.0, height * 0.36), "ChestplateTorso", material=material, bevel=0.006))
    parts.append(add_prism(width * 0.9, depth * 0.72, height * 0.22, (0.0, 0.0, height * 0.72), "ChestplateUpper", material=material, bevel=0.006))
    parts.append(add_prism(width * 0.56, depth * 0.52, height * 0.12, (0.0, 0.0, height * 0.1), "ChestplateFauld", material=material, bevel=0.005))
    parts.append(add_prism(width * 0.24, depth * 0.56, height * 0.08, (0.0, 0.0, height * 0.83), "ChestplateNeck", material=accent, bevel=0.004))

    shoulder_z = height * 0.76
    shoulder_offset = width * 0.4
    parts.append(add_sphere(width * 0.14, (-shoulder_offset, 0.0, shoulder_z), "ChestplateShoulderLeft", material=material, scale=(1.4, 1.0, 0.7)))
    parts.append(add_sphere(width * 0.14, (shoulder_offset, 0.0, shoulder_z), "ChestplateShoulderRight", material=material, scale=(1.4, 1.0, 0.7)))
    parts.append(add_prism(width * 0.12, depth * 0.68, height * 0.26, (-width * 0.32, 0.0, height * 0.5), "ChestplateSideLeft", material=material, bevel=0.004))
    parts.append(add_prism(width * 0.12, depth * 0.68, height * 0.26, (width * 0.32, 0.0, height * 0.5), "ChestplateSideRight", material=material, bevel=0.004))
    return join_parts(parts, "ChestplateAsset")


def generate_gauntlets(params, mats):
    width = cm(params.get("width", 34.0))
    depth = cm(params.get("depth", 20.0))
    height = cm(params.get("height", 28.0))
    material_name = str(params.get("material", "steel")).lower()
    style = str(params.get("style", "plate")).lower()
    shell_material = material_for(material_name if style != "leather" else "leather", mats, "steel")
    strap_material = mats["leather"]
    parts = []

    gauntlet_width = width * 0.36
    spacing = width * 0.28
    for side, x in (("Left", -spacing), ("Right", spacing)):
        parts.append(add_tapered_cylinder(gauntlet_width * 0.32, gauntlet_width * 0.22, height * 0.58, (x, 0.0, height * 0.54), f"GauntletCuff{side}", material=shell_material, vertices=18))
        parts.append(add_prism(gauntlet_width * 0.82, depth * 0.68, height * 0.2, (x, depth * 0.12, height * 0.18), f"GauntletHand{side}", material=shell_material, bevel=0.003))
        parts.append(add_prism(gauntlet_width * 0.68, depth * 0.26, height * 0.08, (x, -depth * 0.14, height * 0.44), f"GauntletBand{side}", material=strap_material, bevel=0.002))
        if style == "spiked":
            parts.append(add_cone(gauntlet_width * 0.11, height * 0.16, (x, depth * 0.08, height * 0.84), f"GauntletSpike{side}", material=mats["iron"]))
    return join_parts(parts, "GauntletsAsset")


def generate_boots(params, mats):
    width = cm(params.get("width", 30.0))
    depth = cm(params.get("depth", 40.0))
    height = cm(params.get("height", 46.0))
    material_name = str(params.get("material", "leather")).lower()
    style = str(params.get("style", "travel")).lower()
    shell_material = material_for(material_name if style != "travel" else "leather", mats, "leather")
    sole_material = mats["shadow"] if material_name == "leather" else mats["iron"]
    parts = []

    boot_width = width * 0.38
    x_offset = width * 0.28
    for side, x in (("Left", -x_offset), ("Right", x_offset)):
        parts.append(add_prism(boot_width, depth * 0.62, height * 0.14, (x, 0.0, height * 0.07), f"BootSole{side}", material=sole_material, bevel=0.003))
        parts.append(add_prism(boot_width * 0.9, depth * 0.58, height * 0.4, (x, -depth * 0.08, height * 0.32), f"BootShaft{side}", material=shell_material, bevel=0.004))
        parts.append(add_prism(boot_width * 0.94, depth * 0.42, height * 0.18, (x, depth * 0.26, height * 0.13), f"BootToe{side}", material=shell_material, bevel=0.003))
        if style == "plate":
            parts.append(add_prism(boot_width * 0.84, depth * 0.12, height * 0.08, (x, -depth * 0.18, height * 0.42), f"BootRidge{side}", material=mats["steel"], bevel=0.002))
    return join_parts(parts, "BootsAsset")


def generate_backpack(params, mats):
    width = cm(params.get("width", 42.0))
    depth = cm(params.get("depth", 22.0))
    height = cm(params.get("height", 56.0))
    material_name = str(params.get("material", "canvas")).lower()
    body_material = material_for(material_name, mats, "canvas")
    strap_material = mats["leather"]
    parts = []

    parts.append(add_prism(width * 0.82, depth * 0.78, height * 0.74, (0.0, 0.0, height * 0.42), "BackpackBody", material=body_material, bevel=0.006))
    parts.append(add_prism(width * 0.86, depth * 0.82, height * 0.2, (0.0, depth * 0.04, height * 0.78), "BackpackFlap", material=body_material, rotation=(math.radians(10.0), 0.0, 0.0), bevel=0.004))
    parts.append(add_prism(width * 0.2, depth * 0.18, height * 0.46, (-width * 0.42, 0.0, height * 0.34), "BackpackSidePocketLeft", material=body_material, bevel=0.003))
    parts.append(add_prism(width * 0.2, depth * 0.18, height * 0.46, (width * 0.42, 0.0, height * 0.34), "BackpackSidePocketRight", material=body_material, bevel=0.003))
    parts.append(add_prism(width * 0.12, depth * 0.12, height * 0.72, (-width * 0.22, -depth * 0.24, height * 0.44), "BackpackStrapLeft", material=strap_material, bevel=0.002))
    parts.append(add_prism(width * 0.12, depth * 0.12, height * 0.72, (width * 0.22, -depth * 0.24, height * 0.44), "BackpackStrapRight", material=strap_material, bevel=0.002))

    if bool(params.get("has_bedroll", False)):
        parts.append(add_cylinder(depth * 0.22, width * 0.78, (0.0, 0.0, height * 0.96), "BackpackBedroll", material=mats["cloth_brown"], rotation=(0.0, math.radians(90.0), 0.0), vertices=18))
    return join_parts(parts, "BackpackAsset")


def generate_belt(params, mats):
    length = cm(params.get("width", 110.0))
    thickness = cm(params.get("depth", 4.0))
    strap_height = cm(params.get("height", 10.0))
    strap_material = material_for(params.get("material", "leather"), mats, "leather")
    buckle_material = material_for(params.get("buckle_material", "brass"), mats, "brass")
    parts = []

    parts.append(add_prism(length * 0.62, thickness, strap_height, (-length * 0.08, 0.0, strap_height / 2.0), "BeltMain", material=strap_material, bevel=0.002))
    parts.append(add_prism(length * 0.24, thickness, strap_height, (length * 0.34, 0.0, strap_height / 2.0), "BeltTail", material=strap_material, rotation=(0.0, 0.0, math.radians(8.0)), bevel=0.002))
    parts.append(add_prism(strap_height * 1.1, thickness * 1.4, strap_height * 1.24, (-length * 0.42, 0.0, strap_height * 0.62), "BeltBuckleFrame", material=buckle_material, bevel=0.002))
    parts.append(add_prism(strap_height * 0.16, thickness * 1.1, strap_height * 0.9, (-length * 0.42, 0.0, strap_height * 0.6), "BeltTongue", material=buckle_material, bevel=0.001))
    return join_parts(parts, "BeltAsset")


def generate_pouch(params, mats):
    width = cm(params.get("width", 20.0))
    depth = cm(params.get("depth", 12.0))
    height = cm(params.get("height", 22.0))
    material = material_for(params.get("material", "leather"), mats, "leather")
    clasp_material = material_for(params.get("clasp_material", "brass"), mats, "brass")
    parts = []

    parts.append(add_prism(width * 0.82, depth * 0.72, height * 0.72, (0.0, 0.0, height * 0.36), "PouchBody", material=material, bevel=0.004))
    parts.append(add_prism(width * 0.88, depth * 0.74, height * 0.2, (0.0, depth * 0.06, height * 0.72), "PouchFlap", material=material, rotation=(math.radians(12.0), 0.0, 0.0), bevel=0.003))
    parts.append(add_prism(width * 0.18, depth * 0.1, height * 0.22, (0.0, depth * 0.18, height * 0.54), "PouchClasp", material=clasp_material, bevel=0.002))
    return join_parts(parts, "PouchAsset")


def generate_cape(params, mats):
    width = cm(params.get("width", 120.0))
    height = cm(params.get("height", 170.0))
    thickness = cm(params.get("thickness", 1.5))
    fabric_material = cloth_material(params.get("fabric", "red"), mats)
    clasp_material = material_for(params.get("clasp_material", "brass"), mats, "brass")
    parts = []

    panel_width = width / 3.0
    for index, offset in enumerate((-panel_width * 0.9, 0.0, panel_width * 0.9)):
        rotation = math.radians(-8.0 if index == 0 else 8.0 if index == 2 else 0.0)
        parts.append(
            add_prism(
                panel_width * 1.08,
                max(thickness, 0.02),
                height * (0.94 if index == 1 else 0.88),
                (offset, 0.0, height * (0.47 if index == 1 else 0.44)),
                f"CapePanel_{index}",
                material=fabric_material,
                rotation=(0.0, rotation, 0.0),
                bevel=0.0015,
            )
        )
    parts.append(add_prism(width * 0.28, thickness * 2.6, height * 0.05, (0.0, 0.0, height * 0.95), "CapeCollar", material=clasp_material, bevel=0.002))
    return join_parts(parts, "CapeAsset")


def generate_tent(params, mats):
    width = cm(params.get("width", 240.0))
    depth = cm(params.get("depth", 280.0))
    height = cm(params.get("height", 165.0))
    fabric_material = material_for(params.get("material", "canvas"), mats, "canvas")
    style = str(params.get("tent_style", "ridge")).lower()
    parts = []

    side_length = math.sqrt((width / 2.0) ** 2 + height ** 2)
    panel_thickness = max(width * 0.02, 0.03)
    angle = math.atan2(height, width / 2.0)
    left_center = (-width * 0.22, 0.0, height * 0.5)
    right_center = (width * 0.22, 0.0, height * 0.5)

    parts.append(add_prism(side_length, depth, panel_thickness, left_center, "TentPanelLeft", material=fabric_material, rotation=(0.0, angle, 0.0), bevel=0.002))
    parts.append(add_prism(side_length, depth, panel_thickness, right_center, "TentPanelRight", material=fabric_material, rotation=(0.0, -angle, 0.0), bevel=0.002))
    parts.append(add_cylinder(panel_thickness * 0.42, depth * 0.98, (0.0, 0.0, height - panel_thickness * 0.3), "TentRidgePole", material=mats["wood"], rotation=(math.radians(90.0), 0.0, 0.0), vertices=12))
    parts.append(add_prism(width * 0.82, depth * 0.92, panel_thickness * 0.4, (0.0, 0.0, panel_thickness * 0.2), "TentGroundsheet", material=mats["shadow"], bevel=0.001))

    if style in {"pup", "a_frame"}:
        parts.append(add_prism(width * 0.18, panel_thickness, height * 0.48, (0.0, depth * 0.46, height * 0.24), "TentDoorFlap", material=cloth_material("brown", mats), rotation=(math.radians(-14.0), 0.0, 0.0), bevel=0.0015))
    return join_parts(parts, "TentAsset")


def generate_campfire(params, mats):
    width = cm(params.get("width", 90.0))
    depth = cm(params.get("depth", 90.0))
    height = cm(params.get("height", 34.0))
    log_count = max(3, min(int(params.get("log_count", 5)), 10))
    is_lit = bool(params.get("is_lit", True))
    parts = []

    ring_radius = min(width, depth) * 0.34
    for index in range(7):
        angle = (math.pi * 2.0 * index) / 7.0
        parts.append(add_sphere(width * 0.08, (math.cos(angle) * ring_radius, math.sin(angle) * ring_radius, width * 0.06), f"CampfireStone_{index}", material=mats["stone"], scale=(1.15, 0.9, 0.7)))

    log_length = min(width, depth) * 0.58
    log_radius = max(width * 0.05, 0.03)
    for index in range(log_count):
        angle = (math.pi * index) / max(log_count, 1)
        z = log_radius + (index % 2) * log_radius * 0.22
        parts.append(
            add_cylinder(
                log_radius,
                log_length,
                (0.0, 0.0, z),
                f"CampfireLog_{index}",
                material=mats["wood"],
                rotation=(math.radians(90.0), 0.0, angle),
                vertices=14,
            )
        )

    parts.append(add_prism(width * 0.24, depth * 0.24, height * 0.08, (0.0, 0.0, height * 0.04), "CampfireCoalBed", material=mats["ember"], bevel=0.002))
    if is_lit:
        parts.append(add_cone(width * 0.16, height * 0.7, (0.0, 0.0, height * 0.4), "CampfireFlame", material=mats["flame"], scale=(1.0, 0.8, 1.0)))
        parts.append(add_sphere(width * 0.08, (0.0, 0.0, height * 0.22), "CampfireGlow", material=mats["ember"], scale=(1.0, 0.8, 0.7)))
    return join_parts(parts, "CampfireAsset")


def generate_sleeping_bag(params, mats):
    width = cm(params.get("width", 78.0))
    depth = cm(params.get("depth", 190.0))
    thickness = cm(params.get("thickness", 14.0))
    fabric_material = cloth_material(params.get("fabric", "blue"), mats)
    parts = []

    parts.append(add_prism(width * 0.78, depth * 0.84, thickness * 0.86, (0.0, 0.0, thickness * 0.43), "SleepingBagBody", material=fabric_material, bevel=0.006))
    parts.append(add_sphere(width * 0.32, (0.0, -depth * 0.3, thickness * 0.54), "SleepingBagHood", material=fabric_material, scale=(1.18, 1.0, 0.48)))
    parts.append(add_prism(width * 0.72, depth * 0.04, thickness * 0.1, (0.0, 0.0, thickness * 0.9), "SleepingBagSeam", material=mats["shadow"], bevel=0.001))
    return join_parts(parts, "SleepingBagAsset")


def generate_lantern(params, mats):
    width = cm(params.get("width", 24.0))
    depth = cm(params.get("depth", 18.0))
    height = cm(params.get("height", 42.0))
    shell_material = material_for(params.get("material", "iron"), mats, "iron")
    is_lit = bool(params.get("is_lit", True))
    parts = []

    base_height = height * 0.16
    chamber_height = height * 0.48
    top_height = height * 0.18
    post_width = width * 0.09
    parts.append(add_prism(width * 0.62, depth * 0.62, base_height, (0.0, 0.0, base_height / 2.0), "LanternBase", material=shell_material, bevel=0.003))
    parts.append(add_prism(width * 0.46, depth * 0.46, chamber_height, (0.0, 0.0, base_height + chamber_height / 2.0), "LanternGlass", material=mats["glass"], bevel=0.001))

    for x in (-width * 0.22, width * 0.22):
        for y in (-depth * 0.22, depth * 0.22):
            parts.append(add_prism(post_width, post_width, chamber_height + top_height * 0.35, (x, y, base_height + (chamber_height + top_height * 0.35) / 2.0), f"LanternPost_{x}_{y}", material=shell_material, bevel=0.001))

    parts.append(add_prism(width * 0.56, depth * 0.56, top_height, (0.0, 0.0, base_height + chamber_height + top_height / 2.0), "LanternTop", material=shell_material, bevel=0.003))
    parts.append(add_prism(width * 0.22, depth * 0.16, top_height * 0.5, (0.0, 0.0, height - top_height * 0.04), "LanternCap", material=shell_material, bevel=0.002))
    parts.append(add_cylinder(post_width * 0.46, width * 0.48, (0.0, 0.0, height + width * 0.12), "LanternHandle", material=shell_material, rotation=(0.0, math.radians(90.0), 0.0), vertices=14))
    if is_lit:
        parts.append(add_sphere(width * 0.11, (0.0, 0.0, base_height + chamber_height * 0.52), "LanternFlame", material=mats["flame"], scale=(0.8, 0.8, 1.3)))
    return join_parts(parts, "LanternAsset")


def generate_cooking_pot(params, mats):
    diameter = cm(params.get("diameter", 38.0))
    height = cm(params.get("height", 28.0))
    body_material = material_for(params.get("material", "iron"), mats, "iron")
    has_lid = bool(params.get("has_lid", True))
    parts = []

    radius = diameter / 2.0
    parts.append(add_tapered_cylinder(radius * 0.92, radius * 0.74, height * 0.7, (0.0, 0.0, height * 0.35), "CookingPotBody", material=body_material, vertices=22))
    parts.append(add_cylinder(radius * 0.92, height * 0.08, (0.0, 0.0, height * 0.7), "CookingPotRim", material=body_material, vertices=22))
    parts.append(add_prism(radius * 0.3, radius * 0.1, height * 0.14, (-radius * 1.02, 0.0, height * 0.42), "CookingPotHandleLeft", material=body_material, bevel=0.001))
    parts.append(add_prism(radius * 0.3, radius * 0.1, height * 0.14, (radius * 1.02, 0.0, height * 0.42), "CookingPotHandleRight", material=body_material, bevel=0.001))
    if has_lid:
        parts.append(add_tapered_cylinder(radius * 0.86, radius * 0.24, height * 0.14, (0.0, 0.0, height * 0.82), "CookingPotLid", material=body_material, vertices=20))
        parts.append(add_sphere(radius * 0.12, (0.0, 0.0, height * 0.94), "CookingPotKnob", material=mats["wood"], scale=(1.0, 1.0, 0.8)))
    return join_parts(parts, "CookingPotAsset")


def generate_supply_box(params, mats):
    width = cm(params.get("width", 76.0))
    depth = cm(params.get("depth", 46.0))
    height = cm(params.get("height", 48.0))
    material_name = str(params.get("material", "wood")).lower()
    body_material = material_for(material_name, mats, "wood")
    trim_material = mats["iron"] if material_name == "metal" else mats["rope"]
    parts = []

    parts.append(add_prism(width, depth, height * 0.72, (0.0, 0.0, height * 0.36), "SupplyBoxBody", material=body_material, bevel=0.005))
    parts.append(add_prism(width * 0.96, depth * 0.96, height * 0.18, (0.0, 0.0, height * 0.81), "SupplyBoxLid", material=body_material, bevel=0.004))
    parts.append(add_prism(width * 0.94, depth * 0.06, height * 0.08, (0.0, -depth * 0.36, height * 0.46), "SupplyBoxBandFront", material=trim_material, bevel=0.001))
    parts.append(add_prism(width * 0.94, depth * 0.06, height * 0.08, (0.0, depth * 0.36, height * 0.46), "SupplyBoxBandBack", material=trim_material, bevel=0.001))
    if bool(params.get("has_rope", True)):
        parts.append(add_cylinder(height * 0.08, depth * 0.32, (-width * 0.48, 0.0, height * 0.5), "SupplyBoxHandleLeft", material=mats["rope"], rotation=(math.radians(90.0), 0.0, 0.0), vertices=12))
        parts.append(add_cylinder(height * 0.08, depth * 0.32, (width * 0.48, 0.0, height * 0.5), "SupplyBoxHandleRight", material=mats["rope"], rotation=(math.radians(90.0), 0.0, 0.0), vertices=12))
    return join_parts(parts, "SupplyBoxAsset")


def generate_castle_wall(params, mats):
    width = cm(params.get("width", 420.0))
    thickness = cm(params.get("thickness", 70.0))
    height = cm(params.get("height", 320.0))
    material = material_for(params.get("material", "stone"), mats, "stone")
    has_crenellations = bool(params.get("has_crenellations", True))
    parts = [add_prism(width, thickness, height, (0.0, 0.0, height / 2.0), "CastleWallMain", material=material, bevel=0.008)]

    if has_crenellations:
        crenel_count = max(4, min(int(width / 0.7), 8))
        crenel_width = width / (crenel_count * 1.45)
        for index in range(crenel_count):
            x = -width / 2.0 + (index + 0.5) * (width / crenel_count)
            parts.append(add_prism(crenel_width, thickness * 0.9, height * 0.14, (x, 0.0, height + height * 0.07), f"CastleWallCrenel_{index}", material=material, bevel=0.003))
    parts.append(add_prism(width * 0.96, thickness * 0.08, height * 0.05, (0.0, 0.0, height * 0.5), "CastleWallBand", material=mats["shadow"], bevel=0.001))
    return join_parts(parts, "CastleWallAsset")


def generate_tower(params, mats):
    diameter = cm(params.get("diameter", 320.0))
    height = cm(params.get("height", 620.0))
    material = material_for(params.get("material", "stone"), mats, "stone")
    roof_style = str(params.get("roof_style", "battlement")).lower()
    parts = [add_cylinder(diameter * 0.5, height, (0.0, 0.0, height / 2.0), "TowerMain", material=material, vertices=28)]

    band_height = height * 0.05
    parts.append(add_cylinder(diameter * 0.52, band_height, (0.0, 0.0, height * 0.62), "TowerBand", material=mats["shadow"], vertices=28))
    if roof_style == "cone":
        parts.append(add_cone(diameter * 0.54, height * 0.28, (0.0, 0.0, height + height * 0.14 - OVERLAP), "TowerRoof", material=mats["darkwood"], vertices=24))
    else:
        crown_height = height * 0.1
        parts.append(add_cylinder(diameter * 0.54, crown_height, (0.0, 0.0, height + crown_height / 2.0 - OVERLAP), "TowerCrown", material=material, vertices=28))
        if roof_style == "battlement":
            crenel_count = 8
            crenel_radius = diameter * 0.52
            for index in range(crenel_count):
                angle = (math.pi * 2.0 * index) / crenel_count
                parts.append(add_prism(diameter * 0.12, diameter * 0.12, crown_height * 0.72, (math.cos(angle) * crenel_radius * 0.82, math.sin(angle) * crenel_radius * 0.82, height + crown_height * 0.86), f"TowerCrenel_{index}", material=material, rotation=(0.0, 0.0, angle), bevel=0.002))
    return join_parts(parts, "TowerAsset")


def generate_drawbridge(params, mats):
    width = cm(params.get("width", 260.0))
    length = cm(params.get("length", 420.0))
    thickness = cm(params.get("thickness", 24.0))
    material = material_for(params.get("material", "wood"), mats, "wood")
    chain_count = max(2, min(int(params.get("chain_count", 2)), 4))
    chain_material = mats["iron"]
    parts = [add_prism(width, length, thickness, (0.0, 0.0, thickness / 2.0), "DrawbridgeDeck", material=material, bevel=0.004)]

    for index in range(4):
        y = -length * 0.34 + index * (length * 0.22)
        parts.append(add_prism(width * 0.9, length * 0.02, thickness * 0.12, (0.0, y, thickness * 0.94), f"DrawbridgePlank_{index}", material=mats["shadow"], bevel=0.001))

    hinge_y = -length * 0.47
    parts.append(add_cylinder(thickness * 0.24, width * 0.94, (0.0, hinge_y, thickness * 0.58), "DrawbridgeHinge", material=chain_material, rotation=(0.0, math.radians(90.0), 0.0), vertices=14))

    anchor_positions = [(-width * 0.34, length * 0.42), (width * 0.34, length * 0.42)]
    if chain_count == 4:
        anchor_positions = [(-width * 0.38, length * 0.42), (-width * 0.15, length * 0.42), (width * 0.15, length * 0.42), (width * 0.38, length * 0.42)]
    for index, (x, y) in enumerate(anchor_positions):
        chain_height = length * 0.24
        parts.append(add_cylinder(thickness * 0.08, chain_height, (x, y, thickness + chain_height / 2.0), f"DrawbridgeChain_{index}", material=chain_material, vertices=10))
    return join_parts(parts, "DrawbridgeAsset")


def generate_throne(params, mats):
    width = cm(params.get("width", 105.0))
    depth = cm(params.get("depth", 90.0))
    height = cm(params.get("height", 190.0))
    material_name = str(params.get("material", "wood")).lower()
    body_material = material_for(material_name, mats, "wood")
    trim_material = mats["gold"] if material_name == "gold" else mats["brass"]
    parts = []

    parts.append(add_prism(width * 0.62, depth * 0.58, height * 0.12, (0.0, 0.0, height * 0.3), "ThroneSeat", material=body_material, bevel=0.004))
    parts.append(add_prism(width * 0.7, depth * 0.16, height * 0.64, (0.0, -depth * 0.22, height * 0.68), "ThroneBack", material=body_material, bevel=0.005))
    parts.append(add_prism(width * 0.14, depth * 0.5, height * 0.32, (-width * 0.32, 0.0, height * 0.4), "ThroneArmLeft", material=body_material, bevel=0.004))
    parts.append(add_prism(width * 0.14, depth * 0.5, height * 0.32, (width * 0.32, 0.0, height * 0.4), "ThroneArmRight", material=body_material, bevel=0.004))
    parts.append(add_prism(width * 0.82, depth * 0.2, height * 0.08, (0.0, -depth * 0.22, height * 0.94), "ThroneCrest", material=trim_material, bevel=0.003))
    if bool(params.get("has_cushion", True)):
        parts.append(add_prism(width * 0.52, depth * 0.42, height * 0.08, (0.0, 0.0, height * 0.39), "ThroneCushion", material=cloth_material("red", mats), bevel=0.003))
    return join_parts(parts, "ThroneAsset")


def generate_banner(params, mats):
    width = cm(params.get("width", 70.0))
    height = cm(params.get("height", 180.0))
    fabric_material = cloth_material(params.get("fabric", "red"), mats)
    pole_material = material_for(params.get("pole_material", "wood"), mats, "wood")
    parts = []

    parts.append(add_cylinder(width * 0.04, height * 1.08, (0.0, 0.0, height * 0.54), "BannerPole", material=pole_material, vertices=14))
    parts.append(add_cylinder(width * 0.03, width * 0.92, (width * 0.42, 0.0, height * 0.92), "BannerCrossbar", material=pole_material, rotation=(0.0, math.radians(90.0), 0.0), vertices=12))
    parts.append(add_prism(width * 0.72, width * 0.04, height * 0.74, (width * 0.36, 0.0, height * 0.54), "BannerCloth", material=fabric_material, bevel=0.001))
    parts.append(add_prism(width * 0.14, width * 0.04, height * 0.14, (width * 0.64, 0.0, height * 0.18), "BannerTailRight", material=fabric_material, rotation=(0.0, math.radians(12.0), 0.0), bevel=0.001))
    return join_parts(parts, "BannerAsset")


def generate_market_stall(params, mats):
    width = cm(params.get("width", 260.0))
    depth = cm(params.get("depth", 180.0))
    height = cm(params.get("height", 250.0))
    frame_material = material_for(params.get("frame_material", "wood"), mats, "wood")
    canopy_color = str(params.get("canopy_color", "striped")).lower()
    canopy_material = cloth_material("red" if canopy_color == "striped" else canopy_color, mats)
    parts = []

    counter_height = height * 0.42
    parts.append(add_prism(width * 0.9, depth * 0.58, counter_height * 0.18, (0.0, 0.0, counter_height), "MarketCounterTop", material=frame_material, bevel=0.004))
    parts.append(add_prism(width * 0.84, depth * 0.4, counter_height * 0.46, (0.0, 0.0, counter_height * 0.44), "MarketCounterBase", material=frame_material, bevel=0.004))
    for x in (-width * 0.38, width * 0.38):
        for y in (-depth * 0.28, depth * 0.28):
            parts.append(add_prism(width * 0.06, depth * 0.06, height * 0.72, (x, y, height * 0.36), f"MarketPost_{x}_{y}", material=frame_material, bevel=0.002))

    parts.append(add_prism(width, depth * 0.92, height * 0.08, (0.0, 0.0, height * 0.82), "MarketCanopy", material=canopy_material, rotation=(math.radians(-6.0), 0.0, 0.0), bevel=0.002))
    if canopy_color == "striped":
        for index, x in enumerate((-width * 0.3, 0.0, width * 0.3)):
            stripe_material = cloth_material("white" if index == 1 else "blue", mats)
            parts.append(add_prism(width * 0.18, depth * 0.96, height * 0.02, (x, 0.0, height * 0.86), f"MarketStripe_{index}", material=stripe_material, rotation=(math.radians(-6.0), 0.0, 0.0), bevel=0.001))
    return join_parts(parts, "MarketStallAsset")


def generate_well(params, mats):
    diameter = cm(params.get("diameter", 150.0))
    height = cm(params.get("height", 160.0))
    body_material = material_for(params.get("material", "stone"), mats, "stone")
    roof_style = str(params.get("roof_style", "gable")).lower()
    parts = []

    ring_radius = diameter * 0.5
    wall_thickness = ring_radius * 0.18
    ring_height = height * 0.34
    segment_count = 12
    for index in range(segment_count):
        angle = (math.pi * 2.0 * index) / segment_count
        segment_length = (math.pi * diameter) / segment_count * 0.75
        parts.append(add_prism(segment_length, wall_thickness, ring_height, (math.cos(angle) * (ring_radius - wall_thickness * 0.4), math.sin(angle) * (ring_radius - wall_thickness * 0.4), ring_height / 2.0), f"WellSegment_{index}", material=body_material, rotation=(0.0, 0.0, angle), bevel=0.002))

    parts.append(add_prism(diameter * 0.5, diameter * 0.5, ring_height * 0.08, (0.0, 0.0, ring_height * 0.06), "WellWaterShadow", material=mats["shadow"], bevel=0.001))
    post_height = height * 0.64
    for x in (-diameter * 0.22, diameter * 0.22):
        parts.append(add_prism(diameter * 0.08, diameter * 0.08, post_height, (x, 0.0, ring_height + post_height / 2.0), f"WellPost_{x}", material=mats["wood"], bevel=0.002))

    if roof_style != "none":
        if roof_style == "flat":
            parts.append(add_prism(diameter * 0.72, diameter * 0.46, height * 0.08, (0.0, 0.0, ring_height + post_height + height * 0.04), "WellRoofFlat", material=mats["wood"], bevel=0.002))
        else:
            roof_height = height * 0.28
            parts.append(add_prism(diameter * 0.54, diameter * 0.54, height * 0.06, (-diameter * 0.14, 0.0, ring_height + post_height + roof_height * 0.44), "WellRoofLeft", material=mats["darkwood"], rotation=(0.0, math.radians(34.0), 0.0), bevel=0.002))
            parts.append(add_prism(diameter * 0.54, diameter * 0.54, height * 0.06, (diameter * 0.14, 0.0, ring_height + post_height + roof_height * 0.44), "WellRoofRight", material=mats["darkwood"], rotation=(0.0, math.radians(-34.0), 0.0), bevel=0.002))
    return join_parts(parts, "WellAsset")


def generate_cart(params, mats):
    width = cm(params.get("width", 170.0))
    depth = cm(params.get("depth", 260.0))
    height = cm(params.get("height", 150.0))
    material = material_for(params.get("material", "wood"), mats, "wood")
    has_canopy = bool(params.get("has_canopy", False))
    parts = []

    bed_height = height * 0.18
    parts.append(add_prism(width, depth * 0.56, bed_height, (0.0, 0.0, height * 0.42), "CartBed", material=material, bevel=0.004))
    parts.append(add_prism(width * 0.08, depth * 0.56, height * 0.26, (-width * 0.46, 0.0, height * 0.55), "CartRailLeft", material=material, bevel=0.003))
    parts.append(add_prism(width * 0.08, depth * 0.56, height * 0.26, (width * 0.46, 0.0, height * 0.55), "CartRailRight", material=material, bevel=0.003))
    parts.append(add_prism(width * 0.84, depth * 0.08, height * 0.24, (0.0, -depth * 0.24, height * 0.54), "CartTailgate", material=material, bevel=0.003))
    parts.append(add_prism(width * 0.84, depth * 0.08, height * 0.24, (0.0, depth * 0.24, height * 0.54), "CartFrontgate", material=material, bevel=0.003))

    axle_z = height * 0.18
    wheel_radius = min(width, depth) * 0.18
    wheel_thickness = width * 0.08
    wheel_y = depth * 0.22
    wheel_x = width * 0.56
    for x in (-wheel_x, wheel_x):
        for y in (-wheel_y, wheel_y):
            parts.append(add_cylinder(wheel_radius, wheel_thickness, (x, y, axle_z), f"CartWheel_{x}_{y}", material=mats["darkwood"], rotation=(math.radians(90.0), 0.0, 0.0), vertices=18))
    parts.append(add_cylinder(wheel_thickness * 0.42, width * 1.18, (0.0, wheel_y, axle_z), "CartAxleFront", material=mats["iron"], rotation=(0.0, math.radians(90.0), 0.0), vertices=12))
    parts.append(add_cylinder(wheel_thickness * 0.42, width * 1.18, (0.0, -wheel_y, axle_z), "CartAxleBack", material=mats["iron"], rotation=(0.0, math.radians(90.0), 0.0), vertices=12))
    parts.append(add_prism(width * 0.08, depth * 0.56, height * 0.08, (0.0, depth * 0.48, height * 0.34), "CartTongue", material=material, rotation=(math.radians(-6.0), 0.0, 0.0), bevel=0.002))

    if has_canopy:
        post_height = height * 0.44
        for x in (-width * 0.3, width * 0.3):
            for y in (-depth * 0.16, depth * 0.16):
                parts.append(add_prism(width * 0.05, width * 0.05, post_height, (x, y, height * 0.72), f"CartCanopyPost_{x}_{y}", material=material, bevel=0.001))
        parts.append(add_prism(width * 0.78, depth * 0.5, height * 0.06, (0.0, 0.0, height * 1.02), "CartCanopy", material=cloth_material("brown", mats), rotation=(math.radians(-8.0), 0.0, 0.0), bevel=0.001))
    return join_parts(parts, "CartAsset")


def generate_anvil(params, mats):
    width = cm(params.get("width", 62.0))
    depth = cm(params.get("depth", 28.0))
    height = cm(params.get("height", 42.0))
    material = material_for(params.get("material", "iron"), mats, "iron")
    parts = []

    parts.append(add_prism(width * 0.72, depth, height * 0.22, (0.0, 0.0, height * 0.7), "AnvilTop", material=material, bevel=0.003))
    parts.append(add_prism(width * 0.3, depth * 0.72, height * 0.38, (-width * 0.05, 0.0, height * 0.42), "AnvilWaist", material=material, bevel=0.003))
    parts.append(add_prism(width * 0.44, depth * 0.82, height * 0.18, (-width * 0.02, 0.0, height * 0.12), "AnvilBase", material=material, bevel=0.003))
    parts.append(add_cone(depth * 0.34, width * 0.34, (width * 0.4, 0.0, height * 0.68), "AnvilHorn", material=material, rotation=(0.0, math.radians(90.0), 0.0), scale=(1.0, 0.7, 1.0)))
    parts.append(add_prism(width * 0.18, depth * 0.5, height * 0.16, (-width * 0.42, 0.0, height * 0.68), "AnvilTail", material=material, rotation=(0.0, 0.0, math.radians(45.0)), bevel=0.002))
    return join_parts(parts, "AnvilAsset")


def generate_forge(params, mats):
    width = cm(params.get("width", 220.0))
    depth = cm(params.get("depth", 150.0))
    height = cm(params.get("height", 130.0))
    material_name = str(params.get("material", "stone")).lower()
    body_material = material_for(material_name, mats, "stone")
    fire_material = mats["flame"] if bool(params.get("is_lit", True)) else mats["shadow"]
    parts = []

    base_height = height * 0.36
    side_height = height * 0.34
    wall_thickness = width * 0.08
    parts.append(add_prism(width, depth, base_height, (0.0, 0.0, base_height / 2.0), "ForgeBase", material=body_material, bevel=0.005))
    parts.append(add_prism(wall_thickness, depth, side_height, (-width * 0.46, 0.0, base_height + side_height / 2.0), "ForgeSideLeft", material=body_material, bevel=0.004))
    parts.append(add_prism(wall_thickness, depth, side_height, (width * 0.46, 0.0, base_height + side_height / 2.0), "ForgeSideRight", material=body_material, bevel=0.004))
    parts.append(add_prism(width * 0.86, wall_thickness, side_height, (0.0, -depth * 0.46, base_height + side_height / 2.0), "ForgeBack", material=body_material, bevel=0.004))
    parts.append(add_prism(width * 0.66, depth * 0.66, height * 0.08, (0.0, 0.0, base_height + height * 0.06), "ForgeCoalBed", material=mats["shadow"], bevel=0.002))
    parts.append(add_prism(width * 0.4, depth * 0.34, height * 0.06, (0.0, 0.0, base_height + height * 0.1), "ForgeEmberBed", material=fire_material, bevel=0.002))
    if bool(params.get("is_lit", True)):
        parts.append(add_cone(width * 0.12, height * 0.32, (0.0, 0.0, base_height + height * 0.28), "ForgeFlame", material=mats["flame"], scale=(1.0, 0.8, 1.0)))
    parts.append(add_prism(width * 0.38, depth * 0.36, height * 0.14, (0.0, 0.0, base_height + side_height + height * 0.05), "ForgeHood", material=body_material, bevel=0.004))
    parts.append(add_prism(width * 0.18, depth * 0.18, height * 0.7, (0.0, 0.0, base_height + side_height + height * 0.42), "ForgeChimney", material=body_material, bevel=0.004))
    return join_parts(parts, "ForgeAsset")


GENERATOR_MAP = {
    "chestplate": generate_chestplate,
    "gauntlets": generate_gauntlets,
    "boots": generate_boots,
    "backpack": generate_backpack,
    "belt": generate_belt,
    "pouch": generate_pouch,
    "cape": generate_cape,
    "tent": generate_tent,
    "campfire": generate_campfire,
    "sleeping_bag": generate_sleeping_bag,
    "lantern": generate_lantern,
    "cooking_pot": generate_cooking_pot,
    "supply_box": generate_supply_box,
    "castle_wall": generate_castle_wall,
    "tower": generate_tower,
    "drawbridge": generate_drawbridge,
    "throne": generate_throne,
    "banner": generate_banner,
    "market_stall": generate_market_stall,
    "well": generate_well,
    "cart": generate_cart,
    "anvil": generate_anvil,
    "forge": generate_forge,
}


def generate_adventure_asset(params):
    mats = build_materials()
    asset_type = params.get("asset_type")
    if asset_type not in GENERATOR_MAP:
        raise ValueError(f"Unsupported adventure asset_type: {asset_type}")
    return GENERATOR_MAP[asset_type](params, mats)


def main():
    parser = argparse.ArgumentParser(description="Procedural Adventure Asset Generator")
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
    asset_obj = generate_adventure_asset(params)

    if args.render:
        utils.setup_lighting_and_camera(asset_obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)


if __name__ == "__main__":
    main()
