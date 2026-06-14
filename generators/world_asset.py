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
        "steel": utils.create_material("WorldSteel", diffuse_color=(0.66, 0.71, 0.77, 1.0), metallic=0.88, roughness=0.24),
        "darksteel": utils.create_material("WorldDarkSteel", diffuse_color=(0.22, 0.25, 0.3, 1.0), metallic=0.82, roughness=0.32),
        "iron": utils.create_material("WorldIron", diffuse_color=(0.28, 0.3, 0.34, 1.0), metallic=0.74, roughness=0.44),
        "aluminum": utils.create_material("WorldAluminum", diffuse_color=(0.78, 0.82, 0.86, 1.0), metallic=0.86, roughness=0.2),
        "stone": utils.create_material("WorldStone", diffuse_color=(0.54, 0.56, 0.58, 1.0), roughness=0.94),
        "dirt": utils.create_material("WorldDirt", diffuse_color=(0.37, 0.26, 0.15, 1.0), roughness=0.98),
        "grass": utils.create_material("WorldGrass", diffuse_color=(0.22, 0.46, 0.16, 1.0), roughness=0.96),
        "water": utils.create_material("WorldWater", diffuse_color=(0.12, 0.38, 0.66, 1.0), metallic=0.06, roughness=0.08),
        "plastic_white": utils.create_material("WorldPlasticWhite", diffuse_color=(0.9, 0.92, 0.94, 1.0), roughness=0.42),
        "plastic_dark": utils.create_material("WorldPlasticDark", diffuse_color=(0.12, 0.13, 0.16, 1.0), roughness=0.6),
        "rubber": utils.create_material("WorldRubber", diffuse_color=(0.08, 0.08, 0.1, 1.0), roughness=0.92),
        "glass": utils.create_material("WorldGlass", diffuse_color=(0.78, 0.9, 0.98, 1.0), metallic=0.04, roughness=0.08),
        "concrete": utils.create_material("WorldConcrete", diffuse_color=(0.58, 0.6, 0.62, 1.0), roughness=0.94),
        "asphalt": utils.create_material("WorldAsphalt", diffuse_color=(0.16, 0.17, 0.19, 1.0), roughness=0.98),
        "wood": utils.create_material("WorldWood", diffuse_color=(0.45, 0.3, 0.18, 1.0), roughness=0.72),
        "darkwood": utils.create_material("WorldDarkWood", diffuse_color=(0.24, 0.15, 0.09, 1.0), roughness=0.78),
        "hazard_yellow": utils.create_material("WorldHazardYellow", diffuse_color=(0.88, 0.72, 0.12, 1.0), roughness=0.5),
        "safety_orange": utils.create_material("WorldSafetyOrange", diffuse_color=(0.9, 0.42, 0.14, 1.0), roughness=0.44),
        "mail_red": utils.create_material("WorldMailRed", diffuse_color=(0.74, 0.12, 0.12, 1.0), roughness=0.46),
        "city_green": utils.create_material("WorldCityGreen", diffuse_color=(0.18, 0.48, 0.28, 1.0), roughness=0.58),
        "red": utils.create_material("WorldRed", diffuse_color=(0.78, 0.16, 0.12, 1.0), roughness=0.38),
        "blue": utils.create_material("WorldBlue", diffuse_color=(0.16, 0.36, 0.78, 1.0), roughness=0.34),
        "green": utils.create_material("WorldGreen", diffuse_color=(0.18, 0.5, 0.22, 1.0), roughness=0.42),
        "yellow": utils.create_material("WorldYellow", diffuse_color=(0.92, 0.78, 0.2, 1.0), roughness=0.38),
        "purple": utils.create_material("WorldPurple", diffuse_color=(0.5, 0.26, 0.78, 1.0), roughness=0.38),
        "white_paint": utils.create_material("WorldWhitePaint", diffuse_color=(0.94, 0.95, 0.96, 1.0), roughness=0.3),
        "black_paint": utils.create_material("WorldBlackPaint", diffuse_color=(0.1, 0.1, 0.12, 1.0), roughness=0.4),
        "silver_paint": utils.create_material("WorldSilverPaint", diffuse_color=(0.72, 0.76, 0.8, 1.0), metallic=0.62, roughness=0.22),
        "orange_paint": utils.create_material("WorldOrangePaint", diffuse_color=(0.88, 0.42, 0.12, 1.0), roughness=0.38),
        "olive": utils.create_material("WorldOlive", diffuse_color=(0.33, 0.4, 0.16, 1.0), roughness=0.54),
        "sand": utils.create_material("WorldSand", diffuse_color=(0.76, 0.68, 0.44, 1.0), roughness=0.68),
        "gray_paint": utils.create_material("WorldGrayPaint", diffuse_color=(0.5, 0.52, 0.55, 1.0), roughness=0.34),
        "brown_fur": utils.create_material("WorldBrownFur", diffuse_color=(0.45, 0.28, 0.16, 1.0), roughness=0.86),
        "black_fur": utils.create_material("WorldBlackFur", diffuse_color=(0.12, 0.12, 0.14, 1.0), roughness=0.88),
        "white_fur": utils.create_material("WorldWhiteFur", diffuse_color=(0.93, 0.93, 0.91, 1.0), roughness=0.9),
        "golden_fur": utils.create_material("WorldGoldenFur", diffuse_color=(0.74, 0.58, 0.3, 1.0), roughness=0.84),
        "gray_fur": utils.create_material("WorldGrayFur", diffuse_color=(0.56, 0.58, 0.6, 1.0), roughness=0.86),
        "orange_fur": utils.create_material("WorldOrangeFur", diffuse_color=(0.78, 0.42, 0.18, 1.0), roughness=0.84),
        "tan_fur": utils.create_material("WorldTanFur", diffuse_color=(0.7, 0.6, 0.4, 1.0), roughness=0.84),
        "skin_light": utils.create_material("WorldSkinLight", diffuse_color=(0.84, 0.7, 0.6, 1.0), roughness=0.84),
        "skin_medium": utils.create_material("WorldSkinMedium", diffuse_color=(0.62, 0.42, 0.3, 1.0), roughness=0.84),
        "skin_dark": utils.create_material("WorldSkinDark", diffuse_color=(0.38, 0.25, 0.18, 1.0), roughness=0.84),
        "cloth_red": utils.create_material("WorldClothRed", diffuse_color=(0.72, 0.18, 0.18, 1.0), roughness=0.82),
        "cloth_blue": utils.create_material("WorldClothBlue", diffuse_color=(0.2, 0.3, 0.72, 1.0), roughness=0.82),
        "cloth_green": utils.create_material("WorldClothGreen", diffuse_color=(0.18, 0.44, 0.24, 1.0), roughness=0.82),
        "cloth_brown": utils.create_material("WorldClothBrown", diffuse_color=(0.42, 0.28, 0.18, 1.0), roughness=0.84),
        "leather": utils.create_material("WorldLeather", diffuse_color=(0.34, 0.2, 0.12, 1.0), roughness=0.9),
        "paper": utils.create_material("WorldPaper", diffuse_color=(0.9, 0.86, 0.76, 1.0), roughness=0.96),
        "gold": utils.create_material("WorldGold", diffuse_color=(0.9, 0.74, 0.18, 1.0), metallic=0.92, roughness=0.18),
        "bronze": utils.create_material("WorldBronze", diffuse_color=(0.62, 0.42, 0.2, 1.0), metallic=0.72, roughness=0.28),
        "crystal": utils.create_material("WorldCrystal", diffuse_color=(0.48, 0.86, 0.98, 1.0), metallic=0.08, roughness=0.08),
        "red_liquid": utils.create_material("WorldRedLiquid", diffuse_color=(0.76, 0.14, 0.18, 1.0), roughness=0.08),
        "blue_liquid": utils.create_material("WorldBlueLiquid", diffuse_color=(0.18, 0.42, 0.9, 1.0), roughness=0.08),
        "green_liquid": utils.create_material("WorldGreenLiquid", diffuse_color=(0.18, 0.72, 0.34, 1.0), roughness=0.08),
        "screen_blue": utils.create_material("WorldScreenBlue", diffuse_color=(0.2, 0.74, 0.98, 1.0), roughness=0.18),
        "screen_green": utils.create_material("WorldScreenGreen", diffuse_color=(0.24, 0.84, 0.48, 1.0), roughness=0.18),
        "screen_red": utils.create_material("WorldScreenRed", diffuse_color=(0.92, 0.28, 0.24, 1.0), roughness=0.18),
        "screen_yellow": utils.create_material("WorldScreenYellow", diffuse_color=(0.94, 0.78, 0.22, 1.0), roughness=0.18),
        "screen_purple": utils.create_material("WorldScreenPurple", diffuse_color=(0.66, 0.42, 0.96, 1.0), roughness=0.18),
        "screen_white": utils.create_material("WorldScreenWhite", diffuse_color=(0.9, 0.94, 0.98, 1.0), roughness=0.16),
        "shadow": utils.create_material("WorldShadow", diffuse_color=(0.14, 0.15, 0.17, 1.0), roughness=0.96),
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


def add_wedge(width, depth, height, location, name, material=None, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (max(width, 0.01) / 2.0, max(depth, 0.01) / 2.0, max(height, 0.01) / 2.0)
    bpy.ops.object.transform_apply(scale=True)

    min_z = -height / 2.0
    for vert in obj.data.vertices:
        if vert.co.y < 0 and vert.co.z > 0:
            vert.co.z = min_z

    obj.data.update()
    if bevel > 0:
        utils.apply_bevel(obj, width=bevel)
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
        "metal": "steel",
        "dark_metal": "darksteel",
        "dark metal": "darksteel",
        "composite": "plastic_dark",
        "plastic": "plastic_dark",
        "urban": "concrete",
        "crate": "steel",
        "fiberglass": "white_paint",
        "aluminium": "aluminum",
    }
    normalized = str(key or fallback).strip().lower().replace(" ", "_")
    return mats.get(aliases.get(normalized, normalized), mats[fallback])


def accent_material(color_name, mats):
    mapping = {
        "blue": "screen_blue",
        "cyan": "screen_blue",
        "green": "screen_green",
        "red": "screen_red",
        "orange": "screen_yellow",
        "yellow": "screen_yellow",
        "amber": "screen_yellow",
        "purple": "screen_purple",
        "white": "screen_white",
    }
    normalized = str(color_name or "blue").strip().lower()
    return mats[mapping.get(normalized, "screen_blue")]


def surface_color_material(color_name, mats, default_key="steel"):
    mapping = {
        "red": "red",
        "blue": "blue",
        "green": "green",
        "yellow": "yellow",
        "white": "white_paint",
        "black": "black_paint",
        "silver": "silver_paint",
        "gray": "gray_paint",
        "grey": "gray_paint",
        "orange": "orange_paint",
        "olive": "olive",
        "sand": "sand",
        "brown": "brown_fur",
        "golden": "golden_fur",
        "tan": "tan_fur",
        "purple": "purple",
        "crystal": "crystal",
        "gold": "gold",
        "bronze": "bronze",
        "light": "skin_light",
        "medium": "skin_medium",
        "dark": "skin_dark",
    }
    normalized = str(color_name or "").strip().lower().replace(" ", "_")
    key = mapping.get(normalized, normalized)
    return mats.get(key, mats[default_key])


def cloth_material(color_name, mats, default_key="cloth_brown"):
    mapping = {
        "red": "cloth_red",
        "blue": "cloth_blue",
        "green": "cloth_green",
        "brown": "cloth_brown",
        "black": "black_paint",
        "white": "white_paint",
        "gray": "gray_paint",
        "grey": "gray_paint",
        "gold": "gold",
        "purple": "purple",
    }
    normalized = str(color_name or "").strip().lower()
    key = mapping.get(normalized, default_key)
    return mats.get(key, mats[default_key])


def fur_material(color_name, mats, default_key="brown_fur"):
    mapping = {
        "brown": "brown_fur",
        "black": "black_fur",
        "white": "white_fur",
        "golden": "golden_fur",
        "gray": "gray_fur",
        "grey": "gray_fur",
        "orange": "orange_fur",
        "tan": "tan_fur",
    }
    normalized = str(color_name or "").strip().lower().replace(" ", "_")
    key = mapping.get(normalized, default_key)
    return mats.get(key, mats[default_key])


def mix_rgba(color_a, color_b, factor):
    t = max(0.0, min(float(factor), 1.0))
    return tuple(color_a[index] + (color_b[index] - color_a[index]) * t for index in range(4))


def make_flat_material(name, rgba, roughness=0.88, metallic=0.0):
    return utils.create_material(name, diffuse_color=rgba, metallic=metallic, roughness=roughness)


def build_background_palette(theme, time_of_day):
    palettes = {
        "forest": {
            "sky": {"day": (0.62, 0.8, 0.98, 1.0), "sunset": (0.96, 0.62, 0.38, 1.0), "night": (0.08, 0.12, 0.24, 1.0), "dawn": (0.74, 0.8, 0.94, 1.0)},
            "far": (0.21, 0.33, 0.28, 1.0),
            "mid": (0.14, 0.27, 0.19, 1.0),
            "near": (0.08, 0.2, 0.12, 1.0),
            "ground": (0.12, 0.24, 0.12, 1.0),
            "accent": (0.33, 0.22, 0.12, 1.0),
            "celestial_day": (0.98, 0.92, 0.54, 1.0),
            "celestial_night": (0.9, 0.94, 0.98, 1.0),
        },
        "desert": {
            "sky": {"day": (0.7, 0.86, 0.98, 1.0), "sunset": (0.98, 0.66, 0.42, 1.0), "night": (0.07, 0.1, 0.2, 1.0), "dawn": (0.88, 0.8, 0.72, 1.0)},
            "far": (0.66, 0.46, 0.26, 1.0),
            "mid": (0.78, 0.58, 0.32, 1.0),
            "near": (0.88, 0.74, 0.42, 1.0),
            "ground": (0.9, 0.72, 0.38, 1.0),
            "accent": (0.55, 0.34, 0.18, 1.0),
            "celestial_day": (1.0, 0.92, 0.56, 1.0),
            "celestial_night": (0.94, 0.96, 1.0, 1.0),
        },
        "city": {
            "sky": {"day": (0.68, 0.82, 0.96, 1.0), "sunset": (0.98, 0.55, 0.44, 1.0), "night": (0.05, 0.08, 0.18, 1.0), "dawn": (0.78, 0.74, 0.9, 1.0)},
            "far": (0.14, 0.18, 0.28, 1.0),
            "mid": (0.1, 0.14, 0.22, 1.0),
            "near": (0.08, 0.1, 0.16, 1.0),
            "ground": (0.1, 0.12, 0.18, 1.0),
            "accent": (0.96, 0.82, 0.28, 1.0),
            "celestial_day": (0.98, 0.9, 0.54, 1.0),
            "celestial_night": (0.94, 0.95, 1.0, 1.0),
        },
        "cave": {
            "sky": {"day": (0.22, 0.28, 0.34, 1.0), "sunset": (0.26, 0.22, 0.28, 1.0), "night": (0.04, 0.06, 0.1, 1.0), "dawn": (0.26, 0.3, 0.36, 1.0)},
            "far": (0.18, 0.2, 0.26, 1.0),
            "mid": (0.14, 0.16, 0.2, 1.0),
            "near": (0.1, 0.12, 0.16, 1.0),
            "ground": (0.16, 0.18, 0.22, 1.0),
            "accent": (0.28, 0.74, 0.88, 1.0),
            "celestial_day": (0.34, 0.84, 0.94, 1.0),
            "celestial_night": (0.34, 0.84, 0.94, 1.0),
        },
        "snow": {
            "sky": {"day": (0.76, 0.88, 0.98, 1.0), "sunset": (0.98, 0.72, 0.66, 1.0), "night": (0.08, 0.12, 0.24, 1.0), "dawn": (0.84, 0.88, 0.96, 1.0)},
            "far": (0.56, 0.66, 0.8, 1.0),
            "mid": (0.4, 0.5, 0.68, 1.0),
            "near": (0.26, 0.36, 0.54, 1.0),
            "ground": (0.92, 0.96, 1.0, 1.0),
            "accent": (0.96, 0.98, 1.0, 1.0),
            "celestial_day": (0.98, 0.92, 0.62, 1.0),
            "celestial_night": (0.96, 0.97, 1.0, 1.0),
        },
        "space": {
            "sky": {"day": (0.12, 0.1, 0.24, 1.0), "sunset": (0.2, 0.1, 0.24, 1.0), "night": (0.03, 0.03, 0.08, 1.0), "dawn": (0.14, 0.1, 0.22, 1.0)},
            "far": (0.14, 0.12, 0.28, 1.0),
            "mid": (0.2, 0.16, 0.38, 1.0),
            "near": (0.28, 0.22, 0.52, 1.0),
            "ground": (0.08, 0.06, 0.16, 1.0),
            "accent": (0.38, 0.82, 0.98, 1.0),
            "celestial_day": (0.88, 0.92, 0.98, 1.0),
            "celestial_night": (0.92, 0.96, 1.0, 1.0),
        },
        "volcanic": {
            "sky": {"day": (0.48, 0.28, 0.22, 1.0), "sunset": (0.78, 0.28, 0.18, 1.0), "night": (0.08, 0.04, 0.06, 1.0), "dawn": (0.54, 0.22, 0.18, 1.0)},
            "far": (0.2, 0.18, 0.22, 1.0),
            "mid": (0.14, 0.12, 0.16, 1.0),
            "near": (0.08, 0.08, 0.1, 1.0),
            "ground": (0.16, 0.12, 0.1, 1.0),
            "accent": (0.96, 0.38, 0.08, 1.0),
            "celestial_day": (1.0, 0.72, 0.36, 1.0),
            "celestial_night": (0.98, 0.38, 0.12, 1.0),
        },
    }
    palette = palettes.get(theme, palettes["forest"])
    sky = palette["sky"].get(time_of_day, palette["sky"]["day"])
    celestial = palette["celestial_night"] if time_of_day == "night" else palette["celestial_day"]
    return {
        "sky": sky,
        "far": palette["far"],
        "mid": palette["mid"],
        "near": palette["near"],
        "ground": palette["ground"],
        "accent": palette["accent"],
        "celestial": celestial,
    }


def generate_game_background_2d(params, mats):
    width = cm(params.get("width", 1400.0))
    depth = cm(params.get("depth", 36.0))
    height = cm(params.get("height", 800.0))
    theme = str(params.get("theme", "forest")).strip().lower()
    time_of_day = str(params.get("time_of_day", "day")).strip().lower()
    layer_count = max(3, min(int(params.get("layer_count", 4)), 7))
    has_celestial = bool(params.get("has_celestial", True))
    palette = build_background_palette(theme, time_of_day)

    layer_gap = max(depth / max(layer_count + 1, 1), 0.01)
    layer_thickness = max(min(layer_gap * 0.45, depth * 0.18), 0.012)
    parts = []

    sky_mat = make_flat_material(f"BackdropSky_{theme}_{time_of_day}", palette["sky"], roughness=0.96)
    parts.append(add_prism(width, layer_thickness, height, (0.0, depth * 0.28, height / 2.0), "BackgroundSkyPanel", material=sky_mat, bevel=0.002))

    if has_celestial:
        if theme == "space":
            parts.append(add_sphere(width * 0.08, (width * 0.22, depth * 0.24, height * 0.78), "BackgroundPlanet", material=make_flat_material("BackgroundPlanet", palette["celestial"], roughness=0.34), scale=(1.0, 0.16, 1.0)))
            parts.append(add_sphere(width * 0.03, (-width * 0.26, depth * 0.2, height * 0.86), "BackgroundMoon", material=make_flat_material("BackgroundMoon", (0.9, 0.94, 1.0, 1.0), roughness=0.3), scale=(1.0, 0.12, 1.0)))
        else:
            parts.append(add_sphere(width * 0.055, (width * 0.28, depth * 0.24, height * 0.82), "BackgroundCelestial", material=make_flat_material("BackgroundCelestial", palette["celestial"], roughness=0.3), scale=(1.0, 0.12, 1.0)))

    for layer_index in range(layer_count):
        blend = layer_index / max(layer_count - 1, 1)
        layer_color = mix_rgba(palette["far"], palette["near"], blend)
        layer_mat = make_flat_material(f"BackgroundLayer_{layer_index}", layer_color, roughness=0.92)
        accent_mat = make_flat_material(f"BackgroundAccent_{layer_index}", palette["accent"], roughness=0.76)
        ground_mat = make_flat_material(f"BackgroundGround_{layer_index}", mix_rgba(palette["ground"], layer_color, 0.35), roughness=0.94)
        layer_y = depth * 0.2 - layer_gap * layer_index
        horizon_z = height * (0.12 + blend * 0.04)
        silhouette_scale = 0.7 + blend * 0.5

        parts.append(add_prism(width, layer_thickness, max(height * (0.12 + 0.02 * blend), 0.05), (0.0, layer_y, horizon_z / 2.0), f"BackgroundGroundStrip_{layer_index}", material=ground_mat, bevel=0.001))

        if theme == "forest":
            x_positions = (-0.42, -0.18, 0.08, 0.31)
            for tree_index, x_factor in enumerate(x_positions):
                x_pos = width * x_factor * (0.92 - layer_index * 0.06)
                trunk_h = height * (0.22 + 0.06 * ((tree_index + layer_index) % 3)) * silhouette_scale
                canopy_r = width * 0.05 * (0.92 - tree_index * 0.08) * silhouette_scale
                parts.append(add_prism(width * 0.02, layer_thickness * 0.9, trunk_h, (x_pos, layer_y, horizon_z + trunk_h / 2.0), f"ForestTrunk_{layer_index}_{tree_index}", material=accent_mat, bevel=0.001))
                parts.append(add_cone(canopy_r, height * 0.24 * silhouette_scale, (x_pos, layer_y, horizon_z + trunk_h + height * 0.1 * silhouette_scale), f"ForestCanopy_{layer_index}_{tree_index}", material=layer_mat, vertices=12, scale=(1.0, 0.24, 1.0)))
                parts.append(add_sphere(canopy_r * 0.82, (x_pos, layer_y, horizon_z + trunk_h + height * 0.17 * silhouette_scale), f"ForestCanopyCap_{layer_index}_{tree_index}", material=layer_mat, scale=(1.2, 0.22, 0.9)))
        elif theme == "desert":
            parts.append(add_sphere(width * 0.24 * silhouette_scale, (-width * 0.22, layer_y, height * 0.18), f"DesertDuneLeft_{layer_index}", material=layer_mat, scale=(1.0, 0.18, 0.22)))
            parts.append(add_sphere(width * 0.2 * silhouette_scale, (width * 0.1, layer_y, height * 0.16), f"DesertDuneMid_{layer_index}", material=ground_mat, scale=(1.1, 0.18, 0.18)))
            parts.append(add_prism(width * 0.18 * silhouette_scale, layer_thickness * 0.95, height * 0.18 * silhouette_scale, (-width * 0.3, layer_y, height * 0.28), f"DesertMesaLeft_{layer_index}", material=accent_mat, bevel=0.003))
            parts.append(add_prism(width * 0.24 * silhouette_scale, layer_thickness * 0.95, height * 0.26 * silhouette_scale, (width * 0.22, layer_y, height * 0.34), f"DesertMesaRight_{layer_index}", material=layer_mat, bevel=0.003))
            parts.append(add_prism(width * 0.1 * silhouette_scale, layer_thickness * 0.85, height * 0.1 * silhouette_scale, (width * 0.32, layer_y, height * 0.5), f"DesertMesaCap_{layer_index}", material=accent_mat, bevel=0.002))
        elif theme == "city":
            building_specs = [(-0.38, 0.12, 0.3), (-0.18, 0.1, 0.42), (0.02, 0.12, 0.34), (0.24, 0.08, 0.5), (0.4, 0.1, 0.28)]
            for building_index, (x_factor, width_factor, height_factor) in enumerate(building_specs):
                building_width = width * width_factor * silhouette_scale
                building_height = height * height_factor * silhouette_scale
                x_pos = width * x_factor
                parts.append(add_prism(building_width, layer_thickness, building_height, (x_pos, layer_y, horizon_z + building_height / 2.0), f"CityBuilding_{layer_index}_{building_index}", material=layer_mat, bevel=0.002))
                if layer_index >= layer_count - 2:
                    for window_row in range(3):
                        parts.append(add_prism(building_width * 0.08, layer_thickness * 0.9, height * 0.04, (x_pos, layer_y, horizon_z + building_height * (0.3 + window_row * 0.18)), f"CityWindow_{layer_index}_{building_index}_{window_row}", material=accent_mat, bevel=0.001))
                if building_index in {1, 3}:
                    parts.append(add_prism(building_width * 0.06, layer_thickness * 0.9, height * 0.08, (x_pos, layer_y, horizon_z + building_height + height * 0.04), f"CityAntenna_{layer_index}_{building_index}", material=accent_mat, bevel=0.001))
        elif theme == "cave":
            parts.append(add_prism(width, layer_thickness, height * 0.16, (0.0, layer_y, height * 0.92), f"CaveCeiling_{layer_index}", material=layer_mat, bevel=0.003))
            for spike_index, x_factor in enumerate((-0.36, -0.12, 0.16, 0.38)):
                parts.append(add_cone(width * 0.045 * silhouette_scale, height * (0.16 + 0.04 * (spike_index % 2)), (width * x_factor, layer_y, height * 0.76), f"CaveStalactite_{layer_index}_{spike_index}", material=layer_mat, vertices=8, rotation=(math.pi, 0.0, 0.0), scale=(1.0, 0.3, 1.0)))
                parts.append(add_cone(width * 0.05 * silhouette_scale, height * (0.12 + 0.03 * ((spike_index + 1) % 2)), (width * x_factor * 0.9, layer_y, height * 0.12), f"CaveStalagmite_{layer_index}_{spike_index}", material=ground_mat, vertices=8, scale=(1.0, 0.3, 1.0)))
            if layer_index >= layer_count - 2:
                parts.append(add_sphere(width * 0.035, (width * 0.24, layer_y, height * 0.48), f"CaveCrystal_{layer_index}", material=accent_mat, scale=(1.0, 0.2, 1.2)))
        elif theme == "snow":
            parts.append(add_cone(width * 0.24 * silhouette_scale, height * 0.42 * silhouette_scale, (-width * 0.2, layer_y, height * 0.28), f"SnowPeakLeft_{layer_index}", material=layer_mat, vertices=7, scale=(1.0, 0.2, 1.0)))
            parts.append(add_cone(width * 0.3 * silhouette_scale, height * 0.56 * silhouette_scale, (width * 0.16, layer_y, height * 0.34), f"SnowPeakRight_{layer_index}", material=ground_mat, vertices=7, scale=(1.0, 0.2, 1.0)))
            parts.append(add_cone(width * 0.11 * silhouette_scale, height * 0.12 * silhouette_scale, (-width * 0.2, layer_y, height * 0.48), f"SnowCapLeft_{layer_index}", material=accent_mat, vertices=7, scale=(1.0, 0.18, 1.0)))
            parts.append(add_cone(width * 0.14 * silhouette_scale, height * 0.14 * silhouette_scale, (width * 0.16, layer_y, height * 0.62), f"SnowCapRight_{layer_index}", material=accent_mat, vertices=7, scale=(1.0, 0.18, 1.0)))
            for tree_index, x_factor in enumerate((-0.34, 0.0, 0.28)):
                parts.append(add_cone(width * 0.045 * silhouette_scale, height * 0.18 * silhouette_scale, (width * x_factor, layer_y, height * 0.16), f"SnowPine_{layer_index}_{tree_index}", material=layer_mat, vertices=8, scale=(1.0, 0.22, 1.0)))
        elif theme == "space":
            parts.append(add_sphere(width * 0.18 * silhouette_scale, (-width * 0.18, layer_y, height * 0.5), f"SpaceNebulaLeft_{layer_index}", material=layer_mat, scale=(1.4, 0.18, 0.5)))
            parts.append(add_sphere(width * 0.14 * silhouette_scale, (width * 0.18, layer_y, height * 0.64), f"SpaceNebulaRight_{layer_index}", material=accent_mat, scale=(1.3, 0.16, 0.44)))
            for asteroid_index, x_factor in enumerate((-0.38, -0.08, 0.26)):
                parts.append(add_sphere(width * 0.028 * silhouette_scale, (width * x_factor, layer_y, height * (0.26 + asteroid_index * 0.08)), f"SpaceAsteroid_{layer_index}_{asteroid_index}", material=ground_mat, scale=(1.1, 0.24, 0.8)))
        else:
            parts.append(add_cone(width * 0.26 * silhouette_scale, height * 0.48 * silhouette_scale, (-width * 0.18, layer_y, height * 0.28), f"VolcanoPeak_{layer_index}", material=layer_mat, vertices=7, scale=(1.0, 0.22, 1.0)))
            parts.append(add_cone(width * 0.18 * silhouette_scale, height * 0.32 * silhouette_scale, (width * 0.2, layer_y, height * 0.22), f"VolcanoSpur_{layer_index}", material=ground_mat, vertices=7, scale=(1.0, 0.22, 1.0)))
            parts.append(add_prism(width * 0.18, layer_thickness * 0.9, height * 0.04, (-width * 0.1, layer_y, height * 0.3), f"VolcanoLava_{layer_index}", material=accent_mat, bevel=0.001))
            if layer_index >= layer_count - 2:
                parts.append(add_sphere(width * 0.06, (-width * 0.04, layer_y, height * 0.64), f"VolcanoSmoke_{layer_index}", material=make_flat_material(f"VolcanoSmokeMat_{layer_index}", (0.32, 0.28, 0.3, 1.0), roughness=0.96), scale=(1.2, 0.16, 0.8)))

    return join_parts(parts, "GameBackground2DAsset")


def generate_control_panel(params, mats):
    width = cm(params.get("width", 140.0))
    depth = cm(params.get("depth", 80.0))
    height = cm(params.get("height", 110.0))
    body_material = material_for(params.get("material", "darksteel"), mats, "darksteel")
    accent = accent_material(params.get("accent_color", "cyan"), mats)
    screen_count = max(2, min(int(params.get("screen_count", 4)), 8))
    parts = []

    parts.append(add_wedge(width, depth, height * 0.58, (0.0, 0.0, height * 0.29), "ControlPanelBody", material=body_material, bevel=0.006))
    parts.append(add_prism(width * 0.9, depth * 0.12, height * 0.12, (0.0, depth * 0.28, height * 0.64), "ControlPanelTop", material=mats["steel"], bevel=0.004))

    screen_w = width * 0.14
    start_x = -width * 0.34
    for index in range(screen_count):
        x = start_x + index * width * 0.18
        parts.append(add_prism(screen_w, depth * 0.03, height * 0.12, (x, depth * 0.26, height * 0.52), f"ControlScreen_{index}", material=accent, bevel=0.001))
        parts.append(add_prism(screen_w * 0.72, depth * 0.02, height * 0.04, (x, depth * 0.18, height * 0.36), f"ControlButtonRow_{index}", material=mats["screen_white"], bevel=0.001))

    parts.append(add_prism(width * 0.18, depth * 0.05, height * 0.1, (width * 0.34, depth * 0.24, height * 0.34), "ControlLeverBase", material=mats["steel"], bevel=0.002))
    parts.append(add_cylinder(width * 0.02, height * 0.18, (width * 0.36, depth * 0.18, height * 0.42), "ControlLever", material=mats["steel"], vertices=12, rotation=(math.radians(18.0), 0.0, 0.0)))
    parts.append(add_sphere(width * 0.03, (width * 0.38, depth * 0.16, height * 0.52), "ControlLeverKnob", material=mats["screen_red"]))
    return join_parts(parts, "ControlPanelAsset")


def generate_terminal(params, mats):
    width = cm(params.get("width", 90.0))
    depth = cm(params.get("depth", 70.0))
    height = cm(params.get("height", 185.0))
    body_material = material_for(params.get("material", "steel"), mats, "steel")
    accent = accent_material(params.get("accent_color", "green"), mats)
    terminal_style = str(params.get("terminal_style", "upright")).lower()
    parts = []

    if terminal_style == "wall":
        parts.append(add_prism(width, depth * 0.36, height * 0.66, (0.0, 0.0, height * 0.33), "TerminalBodyWall", material=body_material, bevel=0.005))
    else:
        parts.append(add_prism(width * 0.52, depth * 0.52, height * 0.7, (0.0, 0.0, height * 0.35), "TerminalPedestal", material=body_material, bevel=0.005))
        parts.append(add_wedge(width, depth * 0.74, height * 0.34, (0.0, 0.0, height * 0.87), "TerminalHead", material=body_material, bevel=0.004))

    parts.append(add_prism(width * 0.72, depth * 0.03, height * 0.24, (0.0, depth * 0.22, height * 0.9), "TerminalScreen", material=accent, bevel=0.001))
    parts.append(add_prism(width * 0.68, depth * 0.05, height * 0.08, (0.0, depth * 0.14, height * 0.68), "TerminalKeys", material=mats["screen_white"], bevel=0.001))
    parts.append(add_prism(width * 0.18, depth * 0.04, height * 0.04, (-width * 0.24, depth * 0.16, height * 0.58), "TerminalPadLeft", material=mats["screen_blue"], bevel=0.001))
    parts.append(add_prism(width * 0.18, depth * 0.04, height * 0.04, (width * 0.24, depth * 0.16, height * 0.58), "TerminalPadRight", material=mats["screen_yellow"], bevel=0.001))
    return join_parts(parts, "TerminalAsset")


def generate_computer(params, mats):
    width = cm(params.get("width", 95.0))
    depth = cm(params.get("depth", 60.0))
    height = cm(params.get("height", 70.0))
    body_material = material_for(params.get("material", "plastic_dark"), mats, "plastic_dark")
    accent = accent_material(params.get("accent_color", "blue"), mats)
    style = str(params.get("computer_style", "desktop")).lower()
    parts = []

    if style == "laptop":
        parts.append(add_prism(width * 0.68, depth, height * 0.08, (0.0, 0.0, height * 0.04), "LaptopBase", material=body_material, bevel=0.004))
        parts.append(add_prism(width * 0.62, depth * 0.9, height * 0.06, (0.0, 0.0, height * 0.1), "LaptopKeys", material=mats["screen_white"], bevel=0.001))
        parts.append(add_prism(width * 0.68, depth * 0.06, height * 0.6, (0.0, -depth * 0.46, height * 0.36), "LaptopScreen", material=accent, rotation=(math.radians(-18.0), 0.0, 0.0), bevel=0.002))
    else:
        parts.append(add_prism(width * 0.58, depth * 0.08, height * 0.42, (0.0, 0.0, height * 0.74), "ComputerMonitor", material=accent, bevel=0.002))
        parts.append(add_prism(width * 0.12, depth * 0.08, height * 0.22, (0.0, 0.0, height * 0.42), "ComputerStem", material=mats["steel"], bevel=0.002))
        parts.append(add_prism(width * 0.28, depth * 0.22, height * 0.06, (0.0, 0.0, height * 0.08), "ComputerBase", material=mats["steel"], bevel=0.002))
        parts.append(add_prism(width * 0.44, depth * 0.24, height * 0.06, (0.0, depth * 0.26, height * 0.04), "ComputerKeyboard", material=body_material, bevel=0.002))
        parts.append(add_prism(width * 0.18, depth * 0.12, height * 0.48, (width * 0.34, -depth * 0.1, height * 0.24), "ComputerTower", material=body_material, bevel=0.004))
        parts.append(add_prism(width * 0.12, depth * 0.02, height * 0.2, (width * 0.34, depth * 0.02, height * 0.26), "ComputerTowerLight", material=accent, bevel=0.001))
    return join_parts(parts, "ComputerAsset")


def generate_server_rack(params, mats):
    width = cm(params.get("width", 80.0))
    depth = cm(params.get("depth", 95.0))
    height = cm(params.get("height", 220.0))
    frame_material = material_for(params.get("material", "darksteel"), mats, "darksteel")
    accent = accent_material(params.get("accent_color", "green"), mats)
    rack_units = max(6, min(int(params.get("rack_units", 12)), 24))
    parts = []

    post_w = width * 0.08
    for x in (-width * 0.42, width * 0.42):
        for y in (-depth * 0.42, depth * 0.42):
            parts.append(add_prism(post_w, post_w, height, (x, y, height / 2.0), f"ServerPost_{x}_{y}", material=frame_material, bevel=0.002))

    parts.append(add_prism(width * 0.92, depth * 0.06, post_w, (0.0, depth * 0.42, post_w / 2.0), "ServerBaseFront", material=frame_material, bevel=0.002))
    parts.append(add_prism(width * 0.92, depth * 0.06, post_w, (0.0, -depth * 0.42, post_w / 2.0), "ServerBaseBack", material=frame_material, bevel=0.002))
    parts.append(add_prism(width * 0.92, depth * 0.86, post_w, (0.0, 0.0, height + post_w / 2.0 - OVERLAP), "ServerTop", material=frame_material, bevel=0.002))

    unit_h = height * 0.78 / rack_units
    for index in range(rack_units):
        z = height * 0.1 + unit_h * (index + 0.5)
        parts.append(add_prism(width * 0.82, depth * 0.78, unit_h * 0.82, (0.0, 0.0, z), f"ServerUnit_{index}", material=mats["plastic_dark"], bevel=0.002))
        light_material = accent if index % 3 == 0 else mats["screen_white"]
        parts.append(add_prism(width * 0.08, depth * 0.02, unit_h * 0.18, (width * 0.28, depth * 0.4, z), f"ServerLight_{index}", material=light_material, bevel=0.001))
    return join_parts(parts, "ServerRackAsset")


def generate_energy_cell(params, mats):
    diameter = cm(params.get("diameter", 26.0))
    height = cm(params.get("height", 60.0))
    shell_material = material_for(params.get("material", "steel"), mats, "steel")
    accent = accent_material(params.get("accent_color", "cyan"), mats)
    parts = []

    radius = diameter / 2.0
    parts.append(add_tapered_cylinder(radius * 0.84, radius * 0.84, height * 0.82, (0.0, 0.0, height * 0.41), "EnergyCore", material=accent, vertices=20))
    parts.append(add_cylinder(radius, height * 0.12, (0.0, 0.0, height * 0.06), "EnergyCapBottom", material=shell_material, vertices=20))
    parts.append(add_cylinder(radius, height * 0.12, (0.0, 0.0, height * 0.94), "EnergyCapTop", material=shell_material, vertices=20))
    for z_factor in (0.24, 0.5, 0.76):
        parts.append(add_cylinder(radius * 1.02, height * 0.04, (0.0, 0.0, height * z_factor), "EnergyRing", material=shell_material, vertices=20))
    return join_parts(parts, "EnergyCellAsset")


def generate_tech_crate(params, mats):
    width = cm(params.get("width", 100.0))
    depth = cm(params.get("depth", 70.0))
    height = cm(params.get("height", 70.0))
    body_material = material_for(params.get("material", "darksteel"), mats, "darksteel")
    accent = accent_material(params.get("accent_color", "cyan"), mats)
    parts = []

    parts.append(add_prism(width, depth, height, (0.0, 0.0, height / 2.0), "TechCrateBody", material=body_material, bevel=0.008))
    parts.append(add_prism(width * 0.86, depth * 0.08, height * 0.08, (0.0, depth * 0.44, height * 0.5), "TechCrateStripFront", material=accent, bevel=0.001))
    parts.append(add_prism(width * 0.86, depth * 0.08, height * 0.08, (0.0, -depth * 0.44, height * 0.5), "TechCrateStripBack", material=accent, bevel=0.001))
    parts.append(add_prism(width * 0.18, depth * 0.12, height * 0.18, (-width * 0.38, 0.0, height * 0.5), "TechCrateLatchLeft", material=mats["aluminum"], bevel=0.002))
    parts.append(add_prism(width * 0.18, depth * 0.12, height * 0.18, (width * 0.38, 0.0, height * 0.5), "TechCrateLatchRight", material=mats["aluminum"], bevel=0.002))
    parts.append(add_prism(width * 0.86, depth * 0.82, height * 0.1, (0.0, 0.0, height * 0.9), "TechCrateTopPanel", material=mats["steel"], bevel=0.004))
    return join_parts(parts, "TechCrateAsset")


def generate_space_door(params, mats):
    width = cm(params.get("width", 150.0))
    height = cm(params.get("height", 240.0))
    depth = cm(params.get("depth", 24.0))
    body_material = material_for(params.get("material", "steel"), mats, "steel")
    accent = accent_material(params.get("accent_color", "cyan"), mats)
    door_style = str(params.get("door_style", "sliding")).lower()
    parts = []

    frame_w = width * 0.12
    parts.append(add_prism(width, depth, frame_w, (0.0, 0.0, frame_w / 2.0), "SpaceDoorThreshold", material=body_material, bevel=0.003))
    parts.append(add_prism(frame_w, depth, height, (-width / 2.0 + frame_w / 2.0, 0.0, height / 2.0), "SpaceDoorFrameLeft", material=body_material, bevel=0.004))
    parts.append(add_prism(frame_w, depth, height, (width / 2.0 - frame_w / 2.0, 0.0, height / 2.0), "SpaceDoorFrameRight", material=body_material, bevel=0.004))
    parts.append(add_prism(width, depth, frame_w, (0.0, 0.0, height - frame_w / 2.0), "SpaceDoorFrameTop", material=body_material, bevel=0.004))

    if door_style == "iris":
        for index, angle in enumerate((-0.22, 0.22)):
            parts.append(add_prism(width * 0.34, depth * 0.82, height * 0.76, ((-1 if index == 0 else 1) * width * 0.18, 0.0, height * 0.44), f"SpaceDoorLeaf_{index}", material=mats["darksteel"], rotation=(0.0, angle, 0.0), bevel=0.004))
    else:
        parts.append(add_prism(width * 0.42, depth * 0.8, height * 0.82, (-width * 0.22, 0.0, height * 0.44), "SpaceDoorLeafLeft", material=mats["darksteel"], bevel=0.004))
        parts.append(add_prism(width * 0.42, depth * 0.8, height * 0.82, (width * 0.22, 0.0, height * 0.44), "SpaceDoorLeafRight", material=mats["darksteel"], bevel=0.004))

    parts.append(add_prism(width * 0.08, depth * 0.08, height * 0.22, (width * 0.38, depth * 0.4, height * 0.56), "SpaceDoorPanel", material=accent, bevel=0.001))
    return join_parts(parts, "SpaceDoorAsset")


def generate_airlock(params, mats):
    width = cm(params.get("width", 220.0))
    depth = cm(params.get("depth", 280.0))
    height = cm(params.get("height", 250.0))
    body_material = material_for(params.get("material", "steel"), mats, "steel")
    accent = accent_material(params.get("accent_color", "blue"), mats)
    door_count = max(1, min(int(params.get("door_count", 2)), 2))
    parts = []

    parts.append(add_prism(width, depth, height, (0.0, 0.0, height / 2.0), "AirlockShell", material=body_material, bevel=0.008))
    parts.append(add_prism(width * 0.72, depth * 0.72, height * 0.76, (0.0, 0.0, height * 0.44), "AirlockChamber", material=mats["glass"], bevel=0.001))

    door_y_positions = (-depth * 0.46, depth * 0.46) if door_count == 2 else (depth * 0.46,)
    for index, y in enumerate(door_y_positions):
        parts.append(add_prism(width * 0.54, depth * 0.06, height * 0.72, (0.0, y, height * 0.42), f"AirlockDoor_{index}", material=mats["darksteel"], bevel=0.003))

    if bool(params.get("has_control_panel", True)):
        parts.append(add_prism(width * 0.1, depth * 0.12, height * 0.3, (width * 0.42, depth * 0.22, height * 0.52), "AirlockControl", material=accent, bevel=0.001))
    return join_parts(parts, "AirlockAsset")


def generate_turret(params, mats):
    width = cm(params.get("width", 120.0))
    depth = cm(params.get("depth", 140.0))
    height = cm(params.get("height", 130.0))
    body_material = material_for(params.get("material", "darksteel"), mats, "darksteel")
    accent = accent_material(params.get("accent_color", "red"), mats)
    barrel_count = max(1, min(int(params.get("barrel_count", 2)), 4))
    parts = []

    parts.append(add_cylinder(width * 0.28, height * 0.22, (0.0, 0.0, height * 0.11), "TurretBase", material=body_material, vertices=20))
    parts.append(add_cylinder(width * 0.12, height * 0.34, (0.0, 0.0, height * 0.34), "TurretNeck", material=body_material, vertices=18))
    parts.append(add_prism(width * 0.52, depth * 0.38, height * 0.28, (0.0, 0.0, height * 0.62), "TurretHead", material=body_material, bevel=0.004))
    for index in range(barrel_count):
        x = (-barrel_count / 2.0 + index + 0.5) * width * 0.12
        parts.append(add_cylinder(width * 0.04, depth * 0.58, (x, depth * 0.34, height * 0.62), f"TurretBarrel_{index}", material=mats["steel"], vertices=14, rotation=(math.radians(90.0), 0.0, 0.0)))
    parts.append(add_prism(width * 0.14, depth * 0.08, height * 0.08, (0.0, -depth * 0.12, height * 0.72), "TurretSensor", material=accent, bevel=0.001))
    return join_parts(parts, "TurretAsset")


def generate_drone(params, mats):
    width = cm(params.get("width", 90.0))
    depth = cm(params.get("depth", 90.0))
    height = cm(params.get("height", 36.0))
    body_material = material_for(params.get("material", "plastic_dark"), mats, "plastic_dark")
    accent = accent_material(params.get("accent_color", "cyan"), mats)
    drone_style = str(params.get("drone_style", "quad")).lower()
    parts = []

    parts.append(add_prism(width * 0.28, depth * 0.28, height * 0.18, (0.0, 0.0, height * 0.34), "DroneCore", material=body_material, bevel=0.004))
    parts.append(add_sphere(width * 0.12, (0.0, 0.0, height * 0.48), "DroneDome", material=mats["plastic_dark"], scale=(1.0, 1.0, 0.55)))
    parts.append(add_prism(width * 0.18, depth * 0.08, height * 0.05, (0.0, depth * 0.08, height * 0.28), "DroneCameraBar", material=mats["steel"], bevel=0.001))
    parts.append(add_cylinder(width * 0.035, height * 0.12, (0.0, depth * 0.18, height * 0.24), "DroneCameraYoke", material=mats["steel"], vertices=12, rotation=(math.radians(90.0), 0.0, 0.0)))
    parts.append(add_sphere(width * 0.05, (0.0, depth * 0.22, height * 0.22), "DroneCamera", material=accent, scale=(1.0, 0.9, 0.8)))

    rotor_count = 4 if drone_style == "quad" else 6
    arm_radius = width * (0.34 if rotor_count == 4 else 0.3)
    for index in range(rotor_count):
        angle = (math.pi * 2.0 * index) / rotor_count
        arm_x = math.cos(angle) * arm_radius
        arm_y = math.sin(angle) * arm_radius
        motor_radius = width * (0.055 if rotor_count == 4 else 0.048)
        parts.append(add_prism(width * (0.34 if rotor_count == 4 else 0.28), depth * 0.05, height * 0.04, (arm_x * 0.48, arm_y * 0.48, height * 0.36), f"DroneArm_{index}", material=body_material, rotation=(0.0, 0.0, angle), bevel=0.002))
        parts.append(add_cylinder(motor_radius, height * 0.12, (arm_x, arm_y, height * 0.42), f"DroneMotor_{index}", material=mats["darksteel"], vertices=16))
        parts.append(add_cylinder(motor_radius * 0.42, height * 0.08, (arm_x, arm_y, height * 0.5), f"DroneRotorHub_{index}", material=mats["steel"], vertices=12))
        parts.append(add_prism(motor_radius * 3.6, motor_radius * 0.4, height * 0.016, (arm_x, arm_y, height * 0.56), f"DroneBladeA_{index}", material=mats["black_paint"], rotation=(0.0, 0.0, angle + math.radians(18.0)), bevel=0.001))
        parts.append(add_prism(motor_radius * 0.4, motor_radius * 3.6, height * 0.016, (arm_x, arm_y, height * 0.56), f"DroneBladeB_{index}", material=mats["black_paint"], rotation=(0.0, 0.0, angle + math.radians(18.0)), bevel=0.001))

    for x in (-width * 0.12, width * 0.12):
        for y in (-depth * 0.12, depth * 0.12):
            parts.append(add_cylinder(width * 0.016, height * 0.22, (x, y, height * 0.11), f"DroneLeg_{x}_{y}", material=mats["steel"], vertices=10))
    for y in (-depth * 0.14, depth * 0.14):
        parts.append(add_prism(width * 0.34, depth * 0.03, height * 0.03, (0.0, y, height * 0.02), f"DroneSkid_{y}", material=mats["darksteel"], bevel=0.001))
    return join_parts(parts, "DroneAsset")


def generate_pipe(params, mats):
    diameter = cm(params.get("diameter", 30.0))
    length = cm(params.get("length", 220.0))
    material = material_for(params.get("material", "steel"), mats, "steel")
    style = str(params.get("pipe_style", "straight")).lower()
    parts = []

    if style == "elbow":
        segment = length * 0.52
        parts.append(add_cylinder(diameter / 2.0, segment, (0.0, 0.0, segment / 2.0), "PipeVertical", material=material, vertices=18))
        parts.append(add_cylinder(diameter / 2.0, segment, (segment / 2.0, 0.0, segment), "PipeHorizontal", material=material, vertices=18, rotation=(0.0, math.radians(90.0), 0.0)))
        parts.append(add_sphere(diameter * 0.42, (0.0, 0.0, segment), "PipeElbow", material=material, scale=(1.0, 1.0, 1.0)))
    else:
        parts.append(add_cylinder(diameter / 2.0, length, (0.0, 0.0, length / 2.0), "PipeBody", material=material, vertices=18))

    for z in (length * 0.14, length * 0.86):
        parts.append(add_cylinder(diameter * 0.62, diameter * 0.16, (0.0, 0.0, z), "PipeFlange", material=mats["darksteel"], vertices=18))
    return join_parts(parts, "PipeAsset")


def generate_valve(params, mats):
    diameter = cm(params.get("diameter", 36.0))
    depth = cm(params.get("depth", 26.0))
    material = material_for(params.get("material", "steel"), mats, "steel")
    handle_style = str(params.get("handle_style", "wheel")).lower()
    parts = []

    parts.append(add_cylinder(diameter * 0.3, depth, (0.0, 0.0, depth / 2.0), "ValveBody", material=material, vertices=18))
    parts.append(add_cylinder(diameter * 0.48, depth * 0.22, (0.0, 0.0, depth * 0.62), "ValveFlange", material=mats["darksteel"], vertices=18))

    if handle_style == "lever":
        parts.append(add_cylinder(diameter * 0.05, diameter * 0.5, (0.0, 0.0, depth * 0.92), "ValveStem", material=mats["steel"], vertices=12))
        parts.append(add_prism(diameter * 0.58, diameter * 0.08, diameter * 0.08, (diameter * 0.24, 0.0, depth + diameter * 0.22), "ValveLever", material=mats["hazard_yellow"], bevel=0.002))
    else:
        parts.append(add_cylinder(diameter * 0.05, diameter * 0.46, (0.0, 0.0, depth * 0.92), "ValveStem", material=mats["steel"], vertices=12))
        parts.append(add_tapered_cylinder(diameter * 0.42, diameter * 0.42, diameter * 0.06, (0.0, 0.0, depth + diameter * 0.22), "ValveWheel", material=mats["hazard_yellow"], vertices=20))
    return join_parts(parts, "ValveAsset")


def generate_tank(params, mats):
    diameter = cm(params.get("diameter", 160.0))
    height = cm(params.get("height", 260.0))
    material = material_for(params.get("material", "steel"), mats, "steel")
    orientation = str(params.get("orientation", "vertical")).lower()
    parts = []

    if orientation == "horizontal":
        parts.append(add_cylinder(diameter / 2.0, height, (0.0, 0.0, diameter / 2.0 + diameter * 0.18), "TankBodyHorizontal", material=material, vertices=24, rotation=(0.0, math.radians(90.0), 0.0)))
        for x in (-height * 0.22, height * 0.22):
            parts.append(add_prism(diameter * 0.12, diameter * 0.32, diameter * 0.18, (x, 0.0, diameter * 0.1), "TankStand", material=mats["darksteel"], bevel=0.002))
    else:
        parts.append(add_cylinder(diameter / 2.0, height, (0.0, 0.0, height / 2.0), "TankBodyVertical", material=material, vertices=24))
        parts.append(add_cone(diameter * 0.44, diameter * 0.18, (0.0, 0.0, height + diameter * 0.09 - OVERLAP), "TankTopCap", material=material, vertices=24))
        parts.append(add_cone(diameter * 0.44, diameter * 0.18, (0.0, 0.0, diameter * 0.09), "TankBottomCap", material=material, vertices=24, rotation=(math.pi, 0.0, 0.0)))
        for x in (-diameter * 0.22, diameter * 0.22):
            parts.append(add_prism(diameter * 0.1, diameter * 0.1, height * 0.18, (x, 0.0, height * 0.09), "TankLeg", material=mats["darksteel"], bevel=0.002))
    return join_parts(parts, "TankAsset")


def generate_generator(params, mats):
    width = cm(params.get("width", 180.0))
    depth = cm(params.get("depth", 120.0))
    height = cm(params.get("height", 140.0))
    body_material = material_for(params.get("material", "darksteel"), mats, "darksteel")
    accent = accent_material(params.get("accent_color", "yellow"), mats)
    parts = []

    parts.append(add_prism(width, depth, height * 0.58, (0.0, 0.0, height * 0.29), "GeneratorBody", material=body_material, bevel=0.006))
    parts.append(add_prism(width * 0.74, depth * 0.12, height * 0.22, (0.0, depth * 0.34, height * 0.4), "GeneratorVentFront", material=mats["steel"], bevel=0.002))
    parts.append(add_prism(width * 0.18, depth * 0.24, height * 0.38, (-width * 0.3, 0.0, height * 0.5), "GeneratorCoilLeft", material=accent, bevel=0.002))
    parts.append(add_prism(width * 0.18, depth * 0.24, height * 0.38, (width * 0.3, 0.0, height * 0.5), "GeneratorCoilRight", material=accent, bevel=0.002))
    parts.append(add_cylinder(width * 0.06, height * 0.4, (-width * 0.34, -depth * 0.3, height * 0.78), "GeneratorPipeLeft", material=mats["steel"], vertices=14))
    parts.append(add_cylinder(width * 0.06, height * 0.4, (width * 0.34, -depth * 0.3, height * 0.78), "GeneratorPipeRight", material=mats["steel"], vertices=14))
    return join_parts(parts, "GeneratorAsset")


def generate_conveyor_belt(params, mats):
    width = cm(params.get("width", 90.0))
    length = cm(params.get("length", 320.0))
    height = cm(params.get("height", 90.0))
    frame_material = material_for(params.get("material", "steel"), mats, "steel")
    roller_count = max(3, min(int(params.get("roller_count", 6)), 12))
    parts = []

    parts.append(add_prism(width, length, height * 0.08, (0.0, 0.0, height * 0.74), "ConveyorBeltTop", material=mats["rubber"], bevel=0.002))
    parts.append(add_prism(width * 0.12, length, height * 0.08, (-width * 0.44, 0.0, height * 0.7), "ConveyorRailLeft", material=frame_material, bevel=0.002))
    parts.append(add_prism(width * 0.12, length, height * 0.08, (width * 0.44, 0.0, height * 0.7), "ConveyorRailRight", material=frame_material, bevel=0.002))

    for index in range(roller_count):
        y = -length * 0.42 + index * (length * 0.84 / max(roller_count - 1, 1))
        parts.append(add_cylinder(width * 0.16, width * 0.88, (0.0, y, height * 0.74), f"ConveyorRoller_{index}", material=mats["aluminum"], rotation=(0.0, math.radians(90.0), 0.0), vertices=14))

    for x in (-width * 0.34, width * 0.34):
        for y in (-length * 0.34, length * 0.34):
            parts.append(add_prism(width * 0.08, width * 0.08, height * 0.74, (x, y, height * 0.37), "ConveyorLeg", material=frame_material, bevel=0.002))
    return join_parts(parts, "ConveyorBeltAsset")


def generate_toolbox(params, mats):
    width = cm(params.get("width", 62.0))
    depth = cm(params.get("depth", 34.0))
    height = cm(params.get("height", 34.0))
    material = material_for(params.get("material", "steel"), mats, "steel")
    parts = []

    parts.append(add_prism(width, depth, height * 0.62, (0.0, 0.0, height * 0.31), "ToolboxBody", material=material, bevel=0.005))
    parts.append(add_prism(width * 0.96, depth * 0.96, height * 0.18, (0.0, 0.0, height * 0.72), "ToolboxLid", material=mats["safety_orange"], bevel=0.004))
    parts.append(add_prism(width * 0.2, depth * 0.08, height * 0.12, (0.0, 0.0, height * 0.84), "ToolboxHandleBlock", material=mats["darksteel"], bevel=0.002))
    parts.append(add_cylinder(height * 0.05, width * 0.28, (0.0, 0.0, height * 0.96), "ToolboxHandle", material=mats["darksteel"], rotation=(0.0, math.radians(90.0), 0.0), vertices=12))
    if bool(params.get("has_tray", True)):
        parts.append(add_prism(width * 0.78, depth * 0.24, height * 0.08, (0.0, 0.0, height * 0.52), "ToolboxTray", material=mats["plastic_dark"], bevel=0.002))
    return join_parts(parts, "ToolboxAsset")


def generate_forklift(params, mats):
    width = cm(params.get("width", 120.0))
    depth = cm(params.get("depth", 260.0))
    height = cm(params.get("height", 220.0))
    body_material = material_for(params.get("material", "hazard_yellow"), mats, "hazard_yellow")
    parts = []

    parts.append(add_prism(width * 0.68, depth * 0.44, height * 0.28, (0.0, -depth * 0.08, height * 0.24), "ForkliftBody", material=body_material, bevel=0.006))
    parts.append(add_prism(width * 0.42, depth * 0.22, height * 0.3, (0.0, depth * 0.04, height * 0.54), "ForkliftSeatBlock", material=mats["plastic_dark"], bevel=0.004))
    mast_x = width * 0.32
    parts.append(add_prism(width * 0.08, depth * 0.12, height * 0.98, (-mast_x, depth * 0.42, height * 0.49), "ForkliftMastLeft", material=mats["darksteel"], bevel=0.002))
    parts.append(add_prism(width * 0.08, depth * 0.12, height * 0.98, (mast_x, depth * 0.42, height * 0.49), "ForkliftMastRight", material=mats["darksteel"], bevel=0.002))
    parts.append(add_prism(width * 0.58, depth * 0.06, height * 0.08, (0.0, depth * 0.46, height * 0.38), "ForkliftCarriage", material=mats["steel"], bevel=0.002))
    parts.append(add_prism(width * 0.14, depth * 0.58, height * 0.04, (-width * 0.12, depth * 0.74, height * 0.06), "ForkliftForkLeft", material=mats["steel"], bevel=0.001))
    parts.append(add_prism(width * 0.14, depth * 0.58, height * 0.04, (width * 0.12, depth * 0.74, height * 0.06), "ForkliftForkRight", material=mats["steel"], bevel=0.001))

    wheel_positions = [
        (-width * 0.28, -depth * 0.34, height * 0.12),
        (width * 0.28, -depth * 0.34, height * 0.12),
        (-width * 0.22, depth * 0.08, height * 0.12),
        (width * 0.22, depth * 0.08, height * 0.12),
    ]
    for index, (x, y, z) in enumerate(wheel_positions):
        parts.append(add_cylinder(width * 0.14 if index < 2 else width * 0.12, width * 0.1, (x, y, z), f"ForkliftWheel_{index}", material=mats["rubber"], rotation=(0.0, math.radians(90.0), 0.0), vertices=16))

    if bool(params.get("has_load", False)):
        parts.append(add_prism(width * 0.38, width * 0.38, width * 0.38, (0.0, depth * 0.72, width * 0.19), "ForkliftLoad", material=mats["wood"], bevel=0.003))
    return join_parts(parts, "ForkliftAsset")


def generate_storage_rack(params, mats):
    width = cm(params.get("width", 180.0))
    depth = cm(params.get("depth", 60.0))
    height = cm(params.get("height", 240.0))
    frame_material = material_for(params.get("material", "steel"), mats, "steel")
    shelf_count = max(2, min(int(params.get("shelves", 4)), 8))
    parts = []

    post_w = width * 0.06
    for x in (-width * 0.42, width * 0.42):
        for y in (-depth * 0.42, depth * 0.42):
            parts.append(add_prism(post_w, post_w, height, (x, y, height / 2.0), "RackPost", material=frame_material, bevel=0.002))

    for index in range(shelf_count):
        z = height * (0.12 + index * 0.76 / max(shelf_count - 1, 1))
        shelf_material = mats["wood"] if index % 2 == 0 else mats["aluminum"]
        parts.append(add_prism(width * 0.88, depth * 0.88, height * 0.04, (0.0, 0.0, z), f"RackShelf_{index}", material=shelf_material, bevel=0.002))
    return join_parts(parts, "StorageRackAsset")


def generate_street_lamp(params, mats):
    width = cm(params.get("width", 26.0))
    depth = cm(params.get("depth", 30.0))
    height = cm(params.get("height", 340.0))
    material = material_for(params.get("material", "darksteel"), mats, "darksteel")
    parts = []

    pole_radius = width * 0.18
    parts.append(add_cylinder(pole_radius, height, (0.0, 0.0, height / 2.0), "StreetLampPole", material=material, vertices=18))
    parts.append(add_cylinder(width * 0.42, width * 0.18, (0.0, 0.0, width * 0.09), "StreetLampBase", material=mats["concrete"], vertices=18))
    parts.append(add_prism(width * 0.14, depth * 0.14, height * 0.16, (0.0, 0.0, height * 0.92), "StreetLampHeadStem", material=material, bevel=0.002))
    parts.append(add_prism(width * 0.74, depth * 0.44, height * 0.12, (width * 0.22, 0.0, height * 0.98), "StreetLampHead", material=mats["glass"], bevel=0.002))
    return join_parts(parts, "StreetLampAsset")


def generate_traffic_light(params, mats):
    width = cm(params.get("width", 46.0))
    depth = cm(params.get("depth", 36.0))
    height = cm(params.get("height", 320.0))
    material = material_for(params.get("material", "darksteel"), mats, "darksteel")
    active_light = str(params.get("active_light", "green")).lower()
    orientation = str(params.get("orientation", "vertical")).lower()
    parts = []

    parts.append(add_cylinder(width * 0.08, height, (0.0, 0.0, height / 2.0), "TrafficPole", material=material, vertices=16))
    housing_height = height * 0.34
    if orientation == "horizontal":
        parts.append(add_prism(width * 1.3, depth * 0.74, width * 0.42, (width * 0.42, 0.0, height * 0.82), "TrafficHousingHorizontal", material=material, bevel=0.003))
        light_positions = [(-width * 0.34, "red"), (0.0, "yellow"), (width * 0.34, "green")]
        for x, color_key in light_positions:
            mat = accent_material(color_key if color_key == active_light else "white", mats)
            parts.append(add_sphere(width * 0.14, (width * 0.42 + x, depth * 0.24, height * 0.82), f"TrafficLight_{color_key}", material=mat, scale=(1.0, 0.4, 1.0)))
    else:
        parts.append(add_prism(width * 0.56, depth * 0.74, housing_height, (0.0, 0.0, height * 0.72), "TrafficHousingVertical", material=material, bevel=0.003))
        light_positions = [(height * 0.82, "red"), (height * 0.72, "yellow"), (height * 0.62, "green")]
        for z, color_key in light_positions:
            mat = accent_material(color_key if color_key == active_light else "white", mats)
            parts.append(add_sphere(width * 0.14, (0.0, depth * 0.24, z), f"TrafficLight_{color_key}", material=mat, scale=(1.0, 0.4, 1.0)))
    return join_parts(parts, "TrafficLightAsset")


def generate_road_sign(params, mats):
    width = cm(params.get("width", 70.0))
    depth = cm(params.get("depth", 10.0))
    height = cm(params.get("height", 260.0))
    material = material_for(params.get("material", "aluminum"), mats, "aluminum")
    sign_shape = str(params.get("sign_shape", "rectangle")).lower()
    accent = accent_material(params.get("accent_color", "white"), mats)
    parts = []

    parts.append(add_cylinder(width * 0.06, height, (0.0, 0.0, height / 2.0), "RoadSignPole", material=mats["darksteel"], vertices=14))
    panel_h = height * 0.26
    if sign_shape == "circle":
        parts.append(add_cylinder(width * 0.32, depth, (0.0, 0.0, height * 0.78), "RoadSignPanelCircle", material=accent, vertices=24, rotation=(math.radians(90.0), 0.0, 0.0)))
    elif sign_shape == "triangle":
        parts.append(add_cone(width * 0.42, depth, (0.0, 0.0, height * 0.78), "RoadSignPanelTriangle", material=accent, vertices=3, rotation=(math.radians(90.0), 0.0, math.radians(180.0))))
    else:
        parts.append(add_prism(width, depth, panel_h, (0.0, 0.0, height * 0.78), "RoadSignPanelRect", material=accent, bevel=0.002))
    parts.append(add_prism(width * 0.82, depth * 0.24, panel_h * 0.12, (0.0, depth * 0.08, height * 0.78), "RoadSignStripe", material=material, bevel=0.001))
    return join_parts(parts, "RoadSignAsset")


def generate_street_bench(params, mats):
    width = cm(params.get("width", 140.0))
    depth = cm(params.get("depth", 52.0))
    height = cm(params.get("height", 88.0))
    frame_material = material_for(params.get("material", "darksteel"), mats, "darksteel")
    has_backrest = bool(params.get("has_backrest", True))
    parts = []

    seat_z = height * 0.46
    slat_w = width * 0.18
    for index in range(5):
        x = -width * 0.32 + index * width * 0.16
        parts.append(add_prism(slat_w, depth * 0.72, height * 0.05, (x, 0.0, seat_z), "BenchSeatSlat", material=mats["wood"], bevel=0.002))

    for x in (-width * 0.4, width * 0.4):
        parts.append(add_prism(width * 0.08, depth * 0.08, seat_z, (x, -depth * 0.12, seat_z / 2.0), "BenchLegFront", material=frame_material, bevel=0.002))
        parts.append(add_prism(width * 0.08, depth * 0.08, seat_z, (x, depth * 0.12, seat_z / 2.0), "BenchLegBack", material=frame_material, bevel=0.002))
        parts.append(add_prism(width * 0.08, depth * 0.12, height * 0.34, (x, -depth * 0.26, height * 0.66), "BenchArm", material=frame_material, bevel=0.002))
    parts.append(add_prism(width * 0.86, depth * 0.08, height * 0.06, (0.0, 0.0, height * 0.2), "BenchRunner", material=frame_material, bevel=0.002))

    if has_backrest:
        for index in range(4):
            x = -width * 0.24 + index * width * 0.16
            parts.append(add_prism(width * 0.14, depth * 0.08, height * 0.2, (x, -depth * 0.26, height * 0.72), "BenchBackSlat", material=mats["wood"], rotation=(math.radians(-10.0), 0.0, 0.0), bevel=0.002))
    return join_parts(parts, "StreetBenchAsset")


def generate_mailbox(params, mats):
    width = cm(params.get("width", 42.0))
    depth = cm(params.get("depth", 62.0))
    height = cm(params.get("height", 150.0))
    body_material = material_for(params.get("material", "mail_red"), mats, "mail_red")
    style = str(params.get("mailbox_style", "post")).lower()
    parts = []

    if style == "wall":
        parts.append(add_prism(width, depth * 0.5, height * 0.42, (0.0, 0.0, height * 0.72), "MailboxBodyWall", material=body_material, bevel=0.004))
    else:
        parts.append(add_prism(width * 0.14, width * 0.14, height * 0.72, (0.0, 0.0, height * 0.36), "MailboxPost", material=mats["darksteel"], bevel=0.002))
        parts.append(add_prism(width, depth * 0.72, height * 0.26, (0.0, 0.0, height * 0.76), "MailboxBody", material=body_material, bevel=0.004))
        parts.append(add_cone(width * 0.48, depth * 0.18, (0.0, 0.0, height * 0.88), "MailboxCap", material=body_material, vertices=4, rotation=(0.0, 0.0, math.radians(45.0))))
    parts.append(add_prism(width * 0.4, depth * 0.06, height * 0.08, (0.0, depth * 0.28, height * 0.76), "MailboxSlot", material=mats["aluminum"], bevel=0.001))
    parts.append(add_prism(width * 0.08, depth * 0.18, height * 0.16, (width * 0.42, 0.0, height * 0.8), "MailboxFlag", material=mats["hazard_yellow"], bevel=0.001))
    return join_parts(parts, "MailboxAsset")


def generate_trash_can(params, mats):
    diameter = cm(params.get("diameter", 48.0))
    height = cm(params.get("height", 82.0))
    material = material_for(params.get("material", "city_green"), mats, "city_green")
    parts = []

    parts.append(add_tapered_cylinder(diameter * 0.42, diameter * 0.34, height * 0.88, (0.0, 0.0, height * 0.44), "TrashCanBody", material=material, vertices=20))
    parts.append(add_cylinder(diameter * 0.44, height * 0.06, (0.0, 0.0, height * 0.88), "TrashCanRim", material=mats["darksteel"], vertices=20))
    if bool(params.get("has_lid", True)):
        parts.append(add_cone(diameter * 0.46, height * 0.14, (0.0, 0.0, height * 0.99), "TrashCanLid", material=mats["darksteel"], vertices=20))
    return join_parts(parts, "TrashCanAsset")


def generate_bus_stop(params, mats):
    width = cm(params.get("width", 280.0))
    depth = cm(params.get("depth", 120.0))
    height = cm(params.get("height", 240.0))
    frame_material = material_for(params.get("material", "steel"), mats, "steel")
    parts = []

    for x in (-width * 0.42, width * 0.42):
        for y in (-depth * 0.34, depth * 0.34):
            parts.append(add_prism(width * 0.05, width * 0.05, height, (x, y, height / 2.0), "BusStopPost", material=frame_material, bevel=0.002))
    parts.append(add_prism(width, depth * 0.92, height * 0.08, (0.0, 0.0, height * 0.96), "BusStopRoof", material=mats["plastic_white"], rotation=(math.radians(-4.0), 0.0, 0.0), bevel=0.002))
    parts.append(add_prism(width * 0.02, depth * 0.7, height * 0.72, (-width * 0.46, 0.0, height * 0.44), "BusStopPanelLeft", material=mats["glass"], bevel=0.001))
    parts.append(add_prism(width * 0.02, depth * 0.7, height * 0.72, (width * 0.46, 0.0, height * 0.44), "BusStopPanelRight", material=mats["glass"], bevel=0.001))
    parts.append(add_prism(width * 0.82, depth * 0.02, height * 0.72, (0.0, -depth * 0.38, height * 0.44), "BusStopBackPanel", material=mats["glass"], bevel=0.001))
    if bool(params.get("has_bench", True)):
        parts.append(add_prism(width * 0.56, depth * 0.18, height * 0.08, (0.0, depth * 0.08, height * 0.28), "BusStopBenchSeat", material=mats["wood"], bevel=0.002))
        parts.append(add_prism(width * 0.56, depth * 0.06, height * 0.18, (0.0, -depth * 0.02, height * 0.44), "BusStopBenchBack", material=mats["wood"], bevel=0.002))
    return join_parts(parts, "BusStopAsset")


def generate_phone_booth(params, mats):
    width = cm(params.get("width", 120.0))
    depth = cm(params.get("depth", 120.0))
    height = cm(params.get("height", 240.0))
    frame_material = material_for(params.get("material", "mail_red"), mats, "mail_red")
    booth_style = str(params.get("booth_style", "classic")).lower()
    accent = accent_material(params.get("accent_color", "white"), mats)
    parts = []

    post_w = width * 0.08
    for x in (-width * 0.42, width * 0.42):
        for y in (-depth * 0.42, depth * 0.42):
            parts.append(add_prism(post_w, post_w, height, (x, y, height / 2.0), "PhoneBoothPost", material=frame_material, bevel=0.002))

    parts.append(add_prism(width, depth, height * 0.08, (0.0, 0.0, height * 0.96), "PhoneBoothRoof", material=frame_material, bevel=0.003))
    parts.append(add_prism(width * 0.82, depth * 0.04, height * 0.18, (0.0, 0.0, height * 1.04), "PhoneBoothSign", material=accent, bevel=0.002))
    parts.append(add_prism(width * 0.02, depth * 0.76, height * 0.72, (-width * 0.46, 0.0, height * 0.44), "PhoneBoothPanelLeft", material=mats["glass"], bevel=0.001))
    parts.append(add_prism(width * 0.02, depth * 0.76, height * 0.72, (width * 0.46, 0.0, height * 0.44), "PhoneBoothPanelRight", material=mats["glass"], bevel=0.001))
    parts.append(add_prism(width * 0.76, depth * 0.02, height * 0.72, (0.0, -depth * 0.46, height * 0.44), "PhoneBoothBackPanel", material=mats["glass"], bevel=0.001))
    if booth_style == "enclosed":
        parts.append(add_prism(width * 0.28, depth * 0.06, height * 0.72, (width * 0.24, depth * 0.46, height * 0.44), "PhoneBoothDoor", material=frame_material, bevel=0.002))
    parts.append(add_prism(width * 0.16, depth * 0.12, height * 0.28, (-width * 0.18, -depth * 0.12, height * 0.56), "PhoneBoxConsole", material=mats["plastic_dark"], bevel=0.002))
    parts.append(add_prism(width * 0.08, depth * 0.06, height * 0.12, (-width * 0.18, -depth * 0.12, height * 0.72), "PhoneBoxScreen", material=accent, bevel=0.001))
    parts.append(add_cylinder(width * 0.03, height * 0.18, (-width * 0.04, -depth * 0.08, height * 0.56), "PhoneBoxHandset", material=mats["darksteel"], rotation=(math.radians(90.0), 0.0, 0.0), vertices=12))
    return join_parts(parts, "PhoneBoothAsset")


def generate_car(params, mats):
    width = cm(params.get("width", 180.0))
    depth = cm(params.get("depth", 420.0))
    height = cm(params.get("height", 155.0))
    style = str(params.get("body_style", "sedan")).lower()
    body = surface_color_material(params.get("body_color", "red"), mats, "red")
    accent = accent_material(params.get("accent_color", "white"), mats)
    parts = []

    wheel_r = width * 0.12
    wheel_t = width * 0.11
    axle_z = wheel_r
    wheel_x = width * 0.3
    front_y = -depth * 0.24
    rear_y = depth * 0.24

    parts.append(add_prism(width * 0.88, depth * 0.52, height * 0.16, (0.0, 0.0, height * 0.18), "CarChassis", material=body, bevel=0.008))
    parts.append(add_wedge(width * 0.78, depth * 0.22, height * 0.12, (0.0, -depth * 0.15, height * 0.3), "CarHood", material=body, bevel=0.004))
    parts.append(add_prism(width * 0.78, depth * 0.18, height * 0.12, (0.0, depth * 0.18, height * 0.28), "CarRearDeck", material=body, bevel=0.004))

    cabin_depth = depth * (0.34 if style == "sedan" else 0.3)
    cabin_height = height * (0.32 if style == "suv" else 0.26)
    parts.append(add_prism(width * 0.68, cabin_depth, cabin_height, (0.0, -depth * 0.02, height * 0.48), "CarCabin", material=body, bevel=0.008))
    parts.append(add_prism(width * 0.56, cabin_depth * 0.34, cabin_height * 0.72, (0.0, -depth * 0.16, height * 0.54), "CarWindshield", material=mats["glass"], rotation=(math.radians(-18.0), 0.0, 0.0), bevel=0.002))
    parts.append(add_prism(width * 0.56, cabin_depth * 0.42, cabin_height * 0.58, (0.0, depth * 0.05, height * 0.56), "CarRoofGlass", material=mats["glass"], bevel=0.002))
    parts.append(add_prism(width * 0.56, cabin_depth * 0.24, cabin_height * 0.54, (0.0, depth * 0.18, height * 0.52), "CarRearGlass", material=mats["glass"], rotation=(math.radians(14.0), 0.0, 0.0), bevel=0.002))
    parts.append(add_prism(width * 0.7, depth * 0.04, height * 0.025, (0.0, 0.0, height * 0.34), "CarSideStripe", material=accent, bevel=0.001))

    if style == "hatchback":
        parts.append(add_prism(width * 0.42, depth * 0.04, height * 0.03, (0.0, depth * 0.26, height * 0.66), "CarSpoiler", material=mats["black_paint"], bevel=0.002))
    elif style == "suv":
        parts.append(add_prism(width * 0.72, depth * 0.06, height * 0.04, (0.0, -depth * 0.02, height * 0.68), "CarRoofRail", material=mats["darksteel"], bevel=0.002))
        parts.append(add_prism(width * 0.12, depth * 0.06, height * 0.08, (0.0, depth * 0.26, height * 0.34), "CarSpareMount", material=body, bevel=0.002))
    else:
        parts.append(add_prism(width * 0.32, depth * 0.06, height * 0.03, (0.0, depth * 0.27, height * 0.42), "CarTrunkLip", material=body, bevel=0.002))

    parts.append(add_prism(width * 0.82, depth * 0.04, height * 0.04, (0.0, -depth * 0.31, height * 0.16), "CarFrontBumper", material=mats["black_paint"], bevel=0.002))
    parts.append(add_prism(width * 0.82, depth * 0.04, height * 0.04, (0.0, depth * 0.31, height * 0.16), "CarRearBumper", material=mats["black_paint"], bevel=0.002))
    for x, light_mat in [(-width * 0.24, mats["screen_white"]), (width * 0.24, mats["screen_white"])]:
        parts.append(add_prism(width * 0.1, depth * 0.02, height * 0.04, (x, -depth * 0.31, height * 0.24), "CarHeadlight", material=light_mat, bevel=0.001))
    for x, light_mat in [(-width * 0.22, mats["screen_red"]), (width * 0.22, mats["screen_red"])]:
        parts.append(add_prism(width * 0.09, depth * 0.02, height * 0.04, (x, depth * 0.31, height * 0.24), "CarTaillight", material=light_mat, bevel=0.001))
    parts.append(add_prism(width * 0.2, depth * 0.02, height * 0.06, (0.0, -depth * 0.31, height * 0.22), "CarGrille", material=mats["darksteel"], bevel=0.001))

    for y in (front_y, rear_y):
        parts.append(add_cylinder(width * 0.02, width * 0.66, (0.0, y, axle_z), f"CarAxle_{y}", material=mats["darksteel"], rotation=(0.0, math.radians(90.0), 0.0), vertices=12))
        parts.append(add_prism(width * 0.7, depth * 0.03, height * 0.05, (0.0, y, height * 0.24), f"CarFender_{y}", material=body, bevel=0.002))

    wheel_positions = [
        (-wheel_x, front_y, axle_z),
        (wheel_x, front_y, axle_z),
        (-wheel_x, rear_y, axle_z),
        (wheel_x, rear_y, axle_z),
    ]
    for index, (x, y, z) in enumerate(wheel_positions):
        parts.append(add_cylinder(wheel_r, wheel_t, (x, y, z), f"CarWheel_{index}", material=mats["rubber"], rotation=(0.0, math.radians(90.0), 0.0), vertices=18))
        parts.append(add_cylinder(wheel_r * 0.54, wheel_t * 1.08, (x, y, z), f"CarRim_{index}", material=mats["aluminum"], rotation=(0.0, math.radians(90.0), 0.0), vertices=14))
    return join_parts(parts, "CarAsset")


def generate_truck(params, mats):
    width = cm(params.get("width", 240.0))
    depth = cm(params.get("depth", 620.0))
    height = cm(params.get("height", 260.0))
    style = str(params.get("truck_style", "pickup")).lower()
    body = surface_color_material(params.get("body_color", "blue"), mats, "blue")
    accent = accent_material(params.get("accent_color", "white"), mats)
    parts = []

    wheel_r = width * 0.12
    wheel_t = width * 0.12
    cab_depth = depth * (0.28 if style == "semi" else 0.24)
    parts.append(add_prism(width * 0.84, depth * 0.18, height * 0.12, (0.0, 0.0, height * 0.18), "TruckFrame", material=mats["darksteel"], bevel=0.004))
    parts.append(add_prism(width * 0.78, cab_depth, height * 0.28, (0.0, -depth * 0.28, height * 0.28), "TruckCabLower", material=body, bevel=0.01))
    parts.append(add_wedge(width * 0.68, cab_depth * 0.38, height * 0.14, (0.0, -depth * 0.36, height * 0.44), "TruckHood", material=body, bevel=0.004))
    parts.append(add_prism(width * 0.62, cab_depth * 0.38, height * 0.18, (0.0, -depth * 0.18, height * 0.48), "TruckCabUpper", material=body, bevel=0.004))
    parts.append(add_prism(width * 0.56, cab_depth * 0.28, height * 0.14, (0.0, -depth * 0.24, height * 0.54), "TruckWindshield", material=mats["glass"], rotation=(math.radians(-18.0), 0.0, 0.0), bevel=0.002))
    parts.append(add_prism(width * 0.56, cab_depth * 0.18, height * 0.08, (0.0, -depth * 0.12, height * 0.56), "TruckSideGlass", material=mats["glass"], bevel=0.002))
    parts.append(add_prism(width * 0.28, depth * 0.02, height * 0.05, (0.0, -depth * 0.39, height * 0.24), "TruckGrille", material=mats["darksteel"], bevel=0.001))
    parts.append(add_prism(width * 0.74, depth * 0.03, height * 0.04, (0.0, -depth * 0.42, height * 0.18), "TruckFrontBumper", material=mats["black_paint"], bevel=0.002))
    parts.append(add_prism(width * 0.64, depth * 0.02, height * 0.03, (0.0, -depth * 0.12, height * 0.34), "TruckCabStripe", material=accent, bevel=0.001))

    if style == "box":
        parts.append(add_prism(width * 0.88, depth * 0.46, height * 0.42, (0.0, depth * 0.1, height * 0.4), "TruckBox", material=mats["white_paint"], bevel=0.008))
        parts.append(add_prism(width * 0.78, depth * 0.02, height * 0.34, (0.0, depth * 0.32, height * 0.42), "TruckBoxDoor", material=mats["white_paint"], bevel=0.002))
    elif style == "semi":
        parts.append(add_prism(width * 0.92, depth * 0.56, height * 0.44, (0.0, depth * 0.14, height * 0.38), "TruckTrailer", material=mats["silver_paint"], bevel=0.01))
        parts.append(add_prism(width * 0.18, depth * 0.08, height * 0.16, (0.0, -depth * 0.02, height * 0.26), "TruckFifthWheel", material=mats["darksteel"], bevel=0.002))
        parts.append(add_prism(width * 0.08, depth * 0.04, height * 0.36, (-width * 0.24, -depth * 0.18, height * 0.52), "TruckExhaust", material=mats["steel"], bevel=0.002))
    else:
        parts.append(add_prism(width * 0.84, depth * 0.34, height * 0.16, (0.0, depth * 0.16, height * 0.28), "TruckBed", material=body, bevel=0.008))
        for x in (-width * 0.4, width * 0.4):
            parts.append(add_prism(width * 0.04, depth * 0.3, height * 0.12, (x, depth * 0.16, height * 0.38), "TruckBedSide", material=body, bevel=0.002))
        if bool(params.get("has_cargo", False)):
            parts.append(add_prism(width * 0.52, depth * 0.22, height * 0.2, (0.0, depth * 0.18, height * 0.52), "TruckCargo", material=mats["wood"], bevel=0.004))

    axle_ys = (-depth * 0.26, 0.0, depth * (0.24 if style == "semi" else 0.2))
    for y in axle_ys:
        parts.append(add_cylinder(width * 0.022, width * 0.72, (0.0, y, wheel_r), f"TruckAxle_{y}", material=mats["darksteel"], rotation=(0.0, math.radians(90.0), 0.0), vertices=12))

    wheel_positions = []
    for y in axle_ys:
        wheel_positions.extend([(-width * 0.34, y, wheel_r), (width * 0.34, y, wheel_r)])
    for index, (x, y, z) in enumerate(wheel_positions):
        parts.append(add_cylinder(wheel_r, wheel_t, (x, y, z), f"TruckWheel_{index}", material=mats["rubber"], rotation=(0.0, math.radians(90.0), 0.0), vertices=18))
        parts.append(add_cylinder(wheel_r * 0.5, wheel_t * 1.04, (x, y, z), f"TruckRim_{index}", material=mats["aluminum"], rotation=(0.0, math.radians(90.0), 0.0), vertices=14))
    return join_parts(parts, "TruckAsset")


def generate_bike(params, mats):
    width = cm(params.get("width", 60.0))
    depth = cm(params.get("depth", 180.0))
    height = cm(params.get("height", 115.0))
    frame = surface_color_material(params.get("frame_color", "green"), mats, "green")
    style = str(params.get("bike_style", "road")).lower()
    parts = []

    for index, y in enumerate((-depth * 0.34, depth * 0.34)):
        parts.append(add_cylinder(width * 0.24, width * 0.06, (0.0, y, width * 0.24), f"BikeWheel_{index}", material=mats["rubber"], rotation=(0.0, math.radians(90.0), 0.0), vertices=22))
        parts.append(add_cylinder(width * 0.18, width * 0.03, (0.0, y, width * 0.24), f"BikeRim_{index}", material=mats["aluminum"], rotation=(0.0, math.radians(90.0), 0.0), vertices=18))
    parts.append(add_prism(width * 0.06, depth * 0.5, height * 0.06, (0.0, 0.0, height * 0.34), "BikeTopTube", material=frame, rotation=(math.radians(24.0), 0.0, 0.0), bevel=0.002))
    parts.append(add_prism(width * 0.06, depth * 0.34, height * 0.06, (-width * 0.16, -depth * 0.08, height * 0.28), "BikeDownTube", material=frame, rotation=(math.radians(-38.0), 0.0, 0.0), bevel=0.002))
    parts.append(add_prism(width * 0.06, depth * 0.3, height * 0.06, (width * 0.16, -depth * 0.12, height * 0.3), "BikeSeatTube", material=frame, rotation=(math.radians(-24.0), 0.0, 0.0), bevel=0.002))
    parts.append(add_prism(width * 0.34, depth * 0.06, height * 0.05, (0.0, -depth * 0.38, height * 0.68), "BikeHandlebar", material=mats["darksteel"], bevel=0.002))
    parts.append(add_prism(width * 0.2, depth * 0.1, height * 0.04, (0.0, 0.0, height * 0.56), "BikeSeat", material=mats["black_paint"], bevel=0.002))
    if bool(params.get("has_basket", style == "city")):
        parts.append(add_prism(width * 0.34, depth * 0.16, height * 0.12, (0.0, -depth * 0.48, height * 0.54), "BikeBasket", material=mats["wood"], bevel=0.003))
    return join_parts(parts, "BikeAsset")


def generate_motorcycle(params, mats):
    width = cm(params.get("width", 80.0))
    depth = cm(params.get("depth", 220.0))
    height = cm(params.get("height", 130.0))
    style = str(params.get("motorcycle_style", "sport")).lower()
    body = surface_color_material(params.get("body_color", "orange"), mats, "orange_paint")
    parts = []

    for index, y in enumerate((-depth * 0.34, depth * 0.34)):
        parts.append(add_cylinder(width * 0.22, width * 0.12, (0.0, y, width * 0.22), f"MotorcycleWheel_{index}", material=mats["rubber"], rotation=(0.0, math.radians(90.0), 0.0), vertices=22))
    parts.append(add_prism(width * 0.36, depth * 0.4, height * 0.16, (0.0, 0.0, height * 0.34), "MotorcycleFrame", material=mats["darksteel"], bevel=0.004))
    parts.append(add_prism(width * 0.42, depth * 0.18, height * 0.22, (0.0, -depth * 0.06, height * 0.52), "MotorcycleTank", material=body, bevel=0.006))
    parts.append(add_prism(width * 0.22, depth * 0.2, height * 0.06, (0.0, depth * 0.12, height * 0.46), "MotorcycleSeat", material=mats["black_paint"], bevel=0.002))
    parts.append(add_prism(width * 0.3, depth * 0.04, height * 0.05, (0.0, -depth * 0.44, height * 0.78), "MotorcycleHandlebar", material=mats["steel"], bevel=0.002))
    if bool(params.get("has_windshield", style == "sport")):
        parts.append(add_prism(width * 0.24, depth * 0.02, height * 0.18, (0.0, -depth * 0.3, height * 0.78), "MotorcycleShield", material=mats["glass"], rotation=(math.radians(-18.0), 0.0, 0.0), bevel=0.001))
    return join_parts(parts, "MotorcycleAsset")


def generate_tractor(params, mats):
    width = cm(params.get("width", 180.0))
    depth = cm(params.get("depth", 360.0))
    height = cm(params.get("height", 240.0))
    body = surface_color_material(params.get("body_color", "green"), mats, "green")
    parts = []

    parts.append(add_prism(width * 0.82, depth * 0.44, height * 0.28, (0.0, 0.0, height * 0.28), "TractorBody", material=body, bevel=0.008))
    if bool(params.get("has_cab", True)):
        parts.append(add_prism(width * 0.44, depth * 0.24, height * 0.34, (0.0, -depth * 0.08, height * 0.62), "TractorCab", material=mats["glass"], bevel=0.003))
        parts.append(add_prism(width * 0.48, depth * 0.28, height * 0.06, (0.0, -depth * 0.08, height * 0.82), "TractorCabRoof", material=body, bevel=0.003))
    parts.append(add_prism(width * 0.32, depth * 0.22, height * 0.12, (0.0, depth * 0.28, height * 0.34), "TractorHood", material=body, bevel=0.004))
    rear_radius = width * 0.22
    front_radius = width * 0.14
    wheel_specs = [
        (-width * 0.32, -depth * 0.2, rear_radius),
        (width * 0.32, -depth * 0.2, rear_radius),
        (-width * 0.28, depth * 0.26, front_radius),
        (width * 0.28, depth * 0.26, front_radius),
    ]
    for index, (x, y, radius) in enumerate(wheel_specs):
        parts.append(add_cylinder(radius, width * 0.12, (x, y, radius), f"TractorWheel_{index}", material=mats["rubber"], rotation=(0.0, math.radians(90.0), 0.0), vertices=20))
    return join_parts(parts, "TractorAsset")


def generate_battle_tank(params, mats):
    width = cm(params.get("width", 320.0))
    depth = cm(params.get("depth", 640.0))
    height = cm(params.get("height", 220.0))
    body = surface_color_material(params.get("body_color", "olive"), mats, "olive")
    turret_style = str(params.get("turret_style", "angular")).lower()
    parts = []

    parts.append(add_prism(width * 0.92, depth * 0.72, height * 0.16, (0.0, 0.0, height * 0.12), "TankHullLower", material=body, bevel=0.01))
    parts.append(add_wedge(width * 0.8, depth * 0.22, height * 0.12, (0.0, -depth * 0.18, height * 0.24), "TankGlacis", material=body, bevel=0.004))
    parts.append(add_prism(width * 0.78, depth * 0.34, height * 0.14, (0.0, depth * 0.08, height * 0.24), "TankEngineDeck", material=body, bevel=0.006))
    turret_h = height * (0.16 if turret_style == "angular" else 0.14)
    parts.append(add_prism(width * 0.42, depth * 0.24, turret_h, (0.0, -depth * 0.02, height * 0.42), "TankTurretBase", material=body, bevel=0.008))
    parts.append(add_wedge(width * 0.34, depth * 0.16, turret_h * 0.7, (0.0, -depth * 0.08, height * 0.5), "TankTurretTop", material=body, bevel=0.004))
    parts.append(add_cylinder(width * 0.05, depth * 0.08, (0.0, -depth * 0.14, height * 0.44), "TankMantlet", material=mats["darksteel"], rotation=(math.radians(90.0), 0.0, 0.0), vertices=16))
    parts.append(add_cylinder(width * 0.034, depth * 0.52, (0.0, -depth * 0.34, height * 0.44), "TankBarrel", material=mats["steel"], rotation=(math.radians(90.0), 0.0, 0.0), vertices=14))
    parts.append(add_cylinder(width * 0.042, depth * 0.04, (0.0, -depth * 0.58, height * 0.44), "TankMuzzle", material=mats["darksteel"], rotation=(math.radians(90.0), 0.0, 0.0), vertices=14))
    parts.append(add_prism(width * 0.16, depth * 0.12, height * 0.04, (-width * 0.1, depth * 0.02, height * 0.52), "TankHatch", material=mats["darksteel"], bevel=0.002))
    parts.append(add_prism(width * 0.08, depth * 0.08, height * 0.08, (width * 0.12, depth * 0.02, height * 0.56), "TankCupola", material=mats["darksteel"], bevel=0.002))
    for x in (-width * 0.44, width * 0.44):
        parts.append(add_prism(width * 0.12, depth * 0.74, height * 0.14, (x, 0.0, height * 0.12), "TankTrack", material=mats["darksteel"], bevel=0.004))
        parts.append(add_prism(width * 0.08, depth * 0.68, height * 0.04, (x, 0.0, height * 0.24), "TankSideSkirt", material=body, bevel=0.002))
        for y in (-depth * 0.28, -depth * 0.12, depth * 0.04, depth * 0.2):
            parts.append(add_cylinder(width * 0.08, width * 0.09, (x, y, height * 0.1), f"TankRoadWheel_{x}_{y}", material=mats["rubber"], rotation=(0.0, math.radians(90.0), 0.0), vertices=16))
        parts.append(add_cylinder(width * 0.09, width * 0.1, (x, -depth * 0.34, height * 0.12), f"TankIdler_{x}", material=mats["darksteel"], rotation=(0.0, math.radians(90.0), 0.0), vertices=16))
        parts.append(add_cylinder(width * 0.1, width * 0.1, (x, depth * 0.28, height * 0.12), f"TankSprocket_{x}", material=mats["darksteel"], rotation=(0.0, math.radians(90.0), 0.0), vertices=16))
    return join_parts(parts, "BattleTankAsset")


def generate_boat(params, mats):
    width = cm(params.get("width", 180.0))
    depth = cm(params.get("depth", 460.0))
    height = cm(params.get("height", 160.0))
    style = str(params.get("boat_style", "motorboat")).lower()
    hull = material_for(params.get("hull_material", "fiberglass"), mats, "white_paint")
    parts = []

    parts.append(add_tapered_cylinder(width * 0.42, width * 0.28, depth * 0.9, (0.0, 0.0, width * 0.28), "BoatHull", material=hull, vertices=18, rotation=(0.0, math.radians(90.0), 0.0)))
    parts.append(add_prism(width * 0.72, depth * 0.62, height * 0.08, (0.0, 0.0, height * 0.24), "BoatDeck", material=mats["wood"], bevel=0.003))
    if style == "sailboat":
        parts.append(add_cylinder(width * 0.03, height * 0.9, (0.0, 0.0, height * 0.6), "BoatMast", material=mats["steel"], vertices=12))
        parts.append(add_prism(width * 0.02, depth * 0.34, height * 0.44, (width * 0.18, 0.0, height * 0.62), "BoatSail", material=mats["white_paint"], bevel=0.001))
    elif style == "rowboat":
        parts.append(add_prism(width * 0.16, depth * 0.18, height * 0.06, (0.0, 0.0, height * 0.36), "BoatSeat", material=mats["wood"], bevel=0.002))
    else:
        parts.append(add_prism(width * 0.32, depth * 0.16, height * 0.18, (0.0, -depth * 0.12, height * 0.42), "BoatConsole", material=mats["glass"], bevel=0.003))
        if bool(params.get("has_canopy", False)):
            parts.append(add_prism(width * 0.52, depth * 0.24, height * 0.06, (0.0, -depth * 0.04, height * 0.76), "BoatCanopy", material=mats["cloth_blue"], bevel=0.002))
    return join_parts(parts, "BoatAsset")


def generate_canoe(params, mats):
    width = cm(params.get("width", 90.0))
    depth = cm(params.get("depth", 420.0))
    height = cm(params.get("height", 90.0))
    hull = material_for(params.get("material", "wood"), mats, "wood")
    seat_count = max(1, min(int(params.get("seat_count", 2)), 3))
    parts = []

    parts.append(add_tapered_cylinder(width * 0.42, width * 0.24, depth, (0.0, 0.0, width * 0.24), "CanoeHull", material=hull, vertices=16, rotation=(0.0, math.radians(90.0), 0.0)))
    for index in range(seat_count):
        y = -depth * 0.22 + index * depth * 0.22
        parts.append(add_prism(width * 0.46, depth * 0.04, height * 0.06, (0.0, y, height * 0.34), f"CanoeSeat_{index}", material=mats["wood"], bevel=0.001))
    return join_parts(parts, "CanoeAsset")


def generate_ship(params, mats):
    width = cm(params.get("width", 320.0))
    depth = cm(params.get("depth", 1200.0))
    height = cm(params.get("height", 340.0))
    style = str(params.get("ship_style", "cargo")).lower()
    hull = material_for(params.get("hull_material", "steel"), mats, "steel")
    parts = []

    parts.append(add_tapered_cylinder(width * 0.44, width * 0.22, depth * 0.94, (0.0, 0.0, width * 0.3), "ShipHull", material=hull, vertices=20, rotation=(0.0, math.radians(90.0), 0.0)))
    parts.append(add_prism(width * 0.78, depth * 0.78, height * 0.06, (0.0, 0.0, height * 0.22), "ShipDeck", material=mats["wood"], bevel=0.003))
    parts.append(add_prism(width * 0.14, depth * 0.2, height * 0.04, (0.0, -depth * 0.36, height * 0.28), "ShipForeDeck", material=mats["wood"], bevel=0.002))
    parts.append(add_prism(width * 0.16, depth * 0.14, height * 0.04, (0.0, depth * 0.34, height * 0.28), "ShipAftDeck", material=mats["wood"], bevel=0.002))
    parts.append(add_prism(width * 0.12, depth * 0.84, height * 0.02, (0.0, 0.0, height * 0.26), "ShipCenterStripe", material=mats["white_paint"], bevel=0.001))
    if style == "sailing":
        parts.append(add_cylinder(width * 0.03, height * 0.96, (0.0, -depth * 0.04, height * 0.7), "ShipMast", material=mats["steel"], vertices=12))
        parts.append(add_prism(width * 0.02, depth * 0.24, height * 0.42, (width * 0.16, -depth * 0.04, height * 0.74), "ShipSailMain", material=mats["paper"], bevel=0.001))
        parts.append(add_prism(width * 0.02, depth * 0.16, height * 0.28, (-width * 0.12, depth * 0.08, height * 0.6), "ShipSailRear", material=mats["paper"], bevel=0.001))
    elif style == "warship":
        parts.append(add_prism(width * 0.3, depth * 0.16, height * 0.16, (0.0, -depth * 0.04, height * 0.42), "ShipBridge", material=mats["darksteel"], bevel=0.004))
        parts.append(add_prism(width * 0.22, depth * 0.1, height * 0.12, (0.0, depth * 0.16, height * 0.52), "ShipBridgeUpper", material=mats["darksteel"], bevel=0.003))
        for y in (-depth * 0.24, depth * 0.12):
            parts.append(add_cylinder(width * 0.04, depth * 0.08, (0.0, y, height * 0.4), "ShipTurret", material=mats["darksteel"], rotation=(math.radians(90.0), 0.0, 0.0), vertices=12))
            parts.append(add_cylinder(width * 0.018, depth * 0.16, (0.0, y - depth * 0.08, height * 0.42), "ShipGun", material=mats["steel"], rotation=(math.radians(90.0), 0.0, 0.0), vertices=12))
    else:
        container_colors = [mats["red"], mats["blue"], mats["hazard_yellow"], mats["city_green"]]
        for row, y in enumerate((-depth * 0.06, depth * 0.12)):
            for col, x in enumerate((-width * 0.18, width * 0.02)):
                parts.append(add_prism(width * 0.24, depth * 0.14, height * 0.14, (x, y, height * (0.36 + row * 0.14)), f"ShipContainer_{row}_{col}", material=container_colors[(row * 2 + col) % len(container_colors)], bevel=0.003))
        parts.append(add_prism(width * 0.22, depth * 0.14, height * 0.14, (width * 0.14, depth * 0.06, height * 0.36), "ShipContainerSingle", material=mats["silver_paint"], bevel=0.003))
        parts.append(add_prism(width * 0.26, depth * 0.12, height * 0.18, (0.0, -depth * 0.28, height * 0.56), "ShipBridgeBase", material=mats["plastic_white"], bevel=0.003))
        parts.append(add_prism(width * 0.22, depth * 0.1, height * 0.12, (0.0, -depth * 0.2, height * 0.68), "ShipBridgeTop", material=mats["plastic_white"], bevel=0.003))
        parts.append(add_prism(width * 0.18, depth * 0.02, height * 0.08, (0.0, -depth * 0.14, height * 0.7), "ShipBridgeWindows", material=mats["glass"], bevel=0.001))
        parts.append(add_cylinder(width * 0.04, height * 0.24, (-width * 0.14, -depth * 0.12, height * 0.64), "ShipStack", material=mats["darksteel"], vertices=16))
        parts.append(add_cylinder(width * 0.024, height * 0.3, (width * 0.14, -depth * 0.08, height * 0.7), "ShipMast", material=mats["steel"], vertices=10))
    return join_parts(parts, "ShipAsset")


def generate_plane(params, mats):
    width = cm(params.get("width", 1200.0))
    depth = cm(params.get("depth", 900.0))
    height = cm(params.get("height", 260.0))
    style = str(params.get("plane_style", "jet")).lower()
    body = surface_color_material(params.get("body_color", "white"), mats, "white_paint")
    accent = accent_material(params.get("accent_color", "blue"), mats)
    parts = []

    fuselage_radius = height * 0.14
    fuselage_z = height * 0.44
    parts.append(add_cylinder(fuselage_radius, depth * 0.72, (0.0, -depth * 0.02, fuselage_z), "PlaneFuselage", material=body, vertices=20, rotation=(math.radians(90.0), 0.0, 0.0)))
    parts.append(add_cone(fuselage_radius, depth * 0.18, (0.0, -depth * 0.46, fuselage_z), "PlaneNose", material=body, vertices=20, rotation=(math.radians(90.0), 0.0, 0.0)))
    parts.append(add_tapered_cylinder(fuselage_radius * 0.92, fuselage_radius * 0.28, depth * 0.22, (0.0, depth * 0.45, fuselage_z + height * 0.02), "PlaneTailCone", material=body, vertices=18, rotation=(math.radians(90.0), 0.0, 0.0)))
    parts.append(add_prism(width * 0.18, depth * 0.18, height * 0.02, (0.0, -depth * 0.02, height * 0.56), "PlaneStripe", material=accent, bevel=0.001))
    parts.append(add_prism(width * 0.2, depth * 0.14, height * 0.12, (0.0, -depth * 0.26, height * 0.58), "PlaneCockpit", material=mats["glass"], rotation=(math.radians(-10.0), 0.0, 0.0), bevel=0.002))
    parts.append(add_prism(width * 0.96, depth * 0.18, height * 0.03, (0.0, 0.0, height * 0.4), "PlaneWing", material=body, bevel=0.003))
    parts.append(add_prism(width * 0.74, depth * 0.08, height * 0.025, (0.0, -depth * 0.06, height * 0.37), "PlaneWingRoot", material=body, bevel=0.003))
    parts.append(add_prism(width * 0.34, depth * 0.09, height * 0.028, (0.0, depth * 0.3, height * 0.56), "PlaneTailPlane", material=body, bevel=0.003))
    parts.append(add_prism(width * 0.05, depth * 0.14, height * 0.24, (0.0, depth * 0.36, height * 0.7), "PlaneTailFin", material=body, bevel=0.003))
    if style == "prop":
        parts.append(add_cylinder(width * 0.02, width * 0.18, (0.0, -depth * 0.56, fuselage_z), "PlanePropHub", material=mats["steel"], rotation=(0.0, math.radians(90.0), 0.0), vertices=12))
        parts.append(add_prism(width * 0.04, width * 0.02, height * 0.28, (0.0, -depth * 0.58, fuselage_z), "PlanePropBladeA", material=mats["black_paint"], bevel=0.001))
        parts.append(add_prism(width * 0.28, width * 0.02, height * 0.04, (0.0, -depth * 0.58, fuselage_z), "PlanePropBladeB", material=mats["black_paint"], bevel=0.001))
    else:
        for x in (-width * 0.24, width * 0.24):
            parts.append(add_prism(width * 0.06, depth * 0.08, height * 0.08, (x, -depth * 0.02, height * 0.32), f"PlaneEnginePylon_{x}", material=body, bevel=0.002))
            parts.append(add_tapered_cylinder(width * 0.06, width * 0.04, depth * 0.18, (x, 0.02, height * 0.26), f"PlaneJetEngine_{x}", material=mats["steel"], vertices=18, rotation=(math.radians(90.0), 0.0, 0.0)))

    gear_wheel_r = width * 0.05
    gear_leg_h = height * 0.18
    for x in (-width * 0.18, width * 0.18):
        parts.append(add_cylinder(width * 0.012, gear_leg_h, (x, depth * 0.08, gear_wheel_r + gear_leg_h / 2.0), f"PlaneMainGearLeg_{x}", material=mats["darksteel"], vertices=10))
        parts.append(add_cylinder(gear_wheel_r, width * 0.04, (x, depth * 0.08, gear_wheel_r), f"PlaneMainGearWheel_{x}", material=mats["rubber"], rotation=(0.0, math.radians(90.0), 0.0), vertices=16))
    parts.append(add_cylinder(width * 0.01, gear_leg_h * 0.8, (0.0, -depth * 0.18, gear_wheel_r + gear_leg_h * 0.4), "PlaneNoseGearLeg", material=mats["darksteel"], vertices=10))
    parts.append(add_cylinder(gear_wheel_r * 0.7, width * 0.03, (0.0, -depth * 0.18, gear_wheel_r * 0.7), "PlaneNoseGearWheel", material=mats["rubber"], rotation=(0.0, math.radians(90.0), 0.0), vertices=16))

    for x, material in [(-width * 0.46, mats["screen_red"]), (width * 0.46, mats["screen_green"])]:
        parts.append(add_sphere(width * 0.018, (x, -depth * 0.04, height * 0.42), "PlaneWingLight", material=material))
    return join_parts(parts, "PlaneAsset")


def generate_helicopter(params, mats):
    width = cm(params.get("width", 320.0))
    depth = cm(params.get("depth", 820.0))
    height = cm(params.get("height", 300.0))
    body = surface_color_material(params.get("body_color", "gray"), mats, "gray_paint")
    accent = accent_material(params.get("accent_color", "blue"), mats)
    parts = []

    parts.append(add_prism(width * 0.34, depth * 0.28, height * 0.22, (0.0, -depth * 0.12, height * 0.38), "HeliCabinLower", material=body, bevel=0.008))
    parts.append(add_prism(width * 0.28, depth * 0.18, height * 0.16, (0.0, -depth * 0.18, height * 0.52), "HeliCanopy", material=mats["glass"], rotation=(math.radians(-12.0), 0.0, 0.0), bevel=0.002))
    parts.append(add_cone(width * 0.12, depth * 0.18, (0.0, -depth * 0.34, height * 0.4), "HeliNose", material=body, vertices=18, rotation=(math.radians(90.0), 0.0, 0.0)))
    parts.append(add_prism(width * 0.22, depth * 0.06, height * 0.03, (0.0, -depth * 0.1, height * 0.6), "HeliStripe", material=accent, bevel=0.001))
    parts.append(add_tapered_cylinder(width * 0.06, width * 0.03, depth * 0.56, (0.0, depth * 0.18, height * 0.42), "HeliTailBoom", material=body, vertices=16, rotation=(math.radians(90.0), 0.0, 0.0)))
    parts.append(add_prism(width * 0.08, depth * 0.14, height * 0.24, (0.0, depth * 0.48, height * 0.56), "HeliTailFin", material=body, bevel=0.003))
    parts.append(add_prism(width * 0.22, depth * 0.04, height * 0.03, (0.0, depth * 0.44, height * 0.46), "HeliTailPlane", material=body, bevel=0.002))
    parts.append(add_cylinder(width * 0.03, height * 0.18, (0.0, -depth * 0.06, height * 0.68), "HeliRotorMast", material=mats["darksteel"], vertices=12))
    parts.append(add_cylinder(width * 0.06, height * 0.04, (0.0, -depth * 0.06, height * 0.78), "HeliRotorHub", material=mats["steel"], vertices=12))
    parts.append(add_prism(width * 1.04, depth * 0.04, height * 0.02, (0.0, -depth * 0.06, height * 0.84), "HeliMainBladeA", material=mats["black_paint"], bevel=0.001))
    parts.append(add_prism(width * 0.04, depth * 1.04, height * 0.02, (0.0, -depth * 0.06, height * 0.84), "HeliMainBladeB", material=mats["black_paint"], bevel=0.001))
    parts.append(add_cylinder(width * 0.02, width * 0.06, (0.0, depth * 0.58, height * 0.56), "HeliTailRotorHub", material=mats["steel"], vertices=10, rotation=(math.radians(90.0), 0.0, 0.0)))
    parts.append(add_prism(width * 0.18, depth * 0.02, height * 0.02, (0.0, depth * 0.58, height * 0.56), "HeliTailBladeA", material=mats["black_paint"], bevel=0.001))
    parts.append(add_prism(width * 0.02, depth * 0.12, height * 0.12, (0.0, depth * 0.58, height * 0.56), "HeliTailBladeB", material=mats["black_paint"], bevel=0.001))
    if bool(params.get("has_skids", True)):
        for x in (-width * 0.18, width * 0.18):
            parts.append(add_prism(width * 0.04, depth * 0.56, height * 0.03, (x, 0.0, height * 0.08), f"HeliSkid_{x}", material=mats["darksteel"], bevel=0.002))
            parts.append(add_cylinder(width * 0.012, height * 0.24, (x, -depth * 0.12, height * 0.2), f"HeliSkidStrutFront_{x}", material=mats["steel"], vertices=10))
            parts.append(add_cylinder(width * 0.012, height * 0.24, (x, depth * 0.08, height * 0.2), f"HeliSkidStrutRear_{x}", material=mats["steel"], vertices=10))
        parts.append(add_prism(width * 0.36, depth * 0.02, height * 0.02, (0.0, -depth * 0.12, height * 0.08), "HeliSkidBraceFront", material=mats["steel"], bevel=0.001))
        parts.append(add_prism(width * 0.32, depth * 0.02, height * 0.02, (0.0, depth * 0.08, height * 0.08), "HeliSkidBraceRear", material=mats["steel"], bevel=0.001))
    return join_parts(parts, "HelicopterAsset")


def generate_humanoid(params, mats, label, defaults):
    width = cm(params.get("width", defaults.get("width", 56.0)))
    depth = cm(params.get("depth", defaults.get("depth", 38.0)))
    height = cm(params.get("height", defaults.get("height", 178.0)))
    skin = surface_color_material(params.get("skin_tone", defaults.get("skin_tone", "medium")), mats, f"skin_{defaults.get('skin_tone', 'medium')}")
    outfit = cloth_material(params.get("outfit_color", defaults.get("outfit_color", "brown")), mats)
    hair = fur_material(defaults.get("hair_color", "brown"), mats)
    boot_material = mats.get(defaults.get("boot_material", "leather"), mats["leather"])
    parts = []

    torso_h = height * defaults.get("torso_ratio", 0.3)
    pelvis_h = height * defaults.get("pelvis_ratio", 0.12)
    leg_h = height * defaults.get("leg_ratio", 0.44)
    arm_h = height * 0.34
    head_r = width * defaults.get("head_ratio", 0.18)
    chest_w = width * defaults.get("torso_width", 0.42)
    hip_w = chest_w * 0.84
    shoulder_w = chest_w * 1.24
    foot_h = height * 0.045
    lower_leg_h = leg_h * 0.4
    upper_leg_h = max(leg_h - lower_leg_h - foot_h, height * 0.12)
    upper_arm_h = arm_h * 0.46
    lower_arm_h = arm_h * 0.42
    hip_z = leg_h + pelvis_h / 2.0
    waist_z = leg_h + pelvis_h + torso_h * 0.22
    chest_z = leg_h + pelvis_h + torso_h * 0.62
    shoulder_z = leg_h + pelvis_h + torso_h * 0.94
    head_z = leg_h + pelvis_h + torso_h + height * 0.02 + head_r * 1.02

    parts.append(add_prism(hip_w, depth * 0.32, pelvis_h, (0.0, 0.0, hip_z), f"{label}Hips", material=outfit, bevel=0.004))
    parts.append(add_prism(chest_w * 0.92, depth * 0.26, torso_h * 0.34, (0.0, 0.0, waist_z), f"{label}Abdomen", material=outfit, bevel=0.004))
    parts.append(add_sphere(chest_w * 0.28, (0.0, 0.0, chest_z), f"{label}Chest", material=outfit, scale=(1.0, 1.04, 1.26)))
    parts.append(add_prism(chest_w * 0.9, depth * 0.18, height * 0.055, (0.0, 0.0, shoulder_z), f"{label}ShoulderBar", material=outfit, bevel=0.003))
    parts.append(add_prism(chest_w * 0.76, depth * 0.24, torso_h * 0.2, (0.0, 0.0, leg_h + pelvis_h + torso_h * 0.04), f"{label}TunicSkirt", material=outfit, bevel=0.003))
    parts.append(add_prism(chest_w * 0.86, depth * 0.14, height * 0.034, (0.0, 0.0, leg_h + pelvis_h * 0.58), f"{label}Belt", material=mats["leather"], bevel=0.002))
    parts.append(add_cylinder(width * 0.045, height * 0.05, (0.0, 0.0, leg_h + pelvis_h + torso_h + height * 0.018), f"{label}Neck", material=skin, vertices=12))
    parts.append(add_sphere(head_r, (0.0, 0.0, head_z), f"{label}Head", material=skin, scale=(1.0, 1.0, 1.06)))
    parts.append(add_prism(head_r * 0.9, head_r * 0.66, head_r * 0.46, (0.0, -head_r * 0.26, head_z - head_r * 0.26), f"{label}Jaw", material=skin, bevel=0.002))
    parts.append(add_prism(head_r * 0.18, head_r * 0.18, head_r * 0.24, (0.0, -head_r * 0.72, head_z - head_r * 0.08), f"{label}Nose", material=skin, bevel=0.001))
    for x in (-head_r * 0.28, head_r * 0.28):
        parts.append(add_sphere(head_r * 0.07, (x, -head_r * 0.58, head_z + head_r * 0.04), f"{label}Eye_{x}", material=mats["shadow"], scale=(1.0, 1.0, 0.6)))
    if not defaults.get("bald", False):
        parts.append(add_sphere(head_r * 0.92, (0.0, head_r * 0.04, head_z + head_r * 0.12), f"{label}Hair", material=hair, scale=(1.0, 1.0, 0.72)))

    for x in (-hip_w * 0.24, hip_w * 0.24):
        parts.append(add_sphere(width * 0.05, (x, 0.0, leg_h + pelvis_h * 0.14), f"{label}HipJoint_{x}", material=outfit, scale=(1.0, 0.9, 1.0)))
        parts.append(add_cylinder(width * 0.05, upper_leg_h, (x, 0.0, foot_h + lower_leg_h + upper_leg_h / 2.0), f"{label}UpperLeg_{x}", material=outfit, vertices=12))
        parts.append(add_sphere(width * 0.042, (x, 0.0, foot_h + lower_leg_h), f"{label}Knee_{x}", material=outfit, scale=(1.0, 0.9, 1.0)))
        parts.append(add_cylinder(width * 0.038, lower_leg_h, (x, 0.0, foot_h + lower_leg_h / 2.0), f"{label}LowerLeg_{x}", material=outfit, vertices=12))
        parts.append(add_prism(width * 0.12, depth * 0.19, foot_h, (x, depth * 0.04, foot_h / 2.0), f"{label}Foot_{x}", material=boot_material, bevel=0.002))
        parts.append(add_prism(width * 0.1, depth * 0.08, foot_h * 0.4, (x, 0.0, foot_h + foot_h * 0.2), f"{label}BootCuff_{x}", material=boot_material, bevel=0.001))

    arm_material = skin if defaults.get("bare_arms", False) else outfit
    for x in (-shoulder_w * 0.42, shoulder_w * 0.42):
        parts.append(add_sphere(width * 0.05, (x, 0.0, shoulder_z + height * 0.01), f"{label}Shoulder_{x}", material=outfit))
        parts.append(add_cylinder(width * 0.04, upper_arm_h, (x, 0.0, shoulder_z - upper_arm_h / 2.0 + height * 0.02), f"{label}UpperArm_{x}", material=arm_material, vertices=12))
        parts.append(add_sphere(width * 0.034, (x, 0.0, shoulder_z - upper_arm_h + height * 0.02), f"{label}Elbow_{x}", material=arm_material, scale=(1.0, 0.9, 1.0)))
        parts.append(add_cylinder(width * 0.034, lower_arm_h, (x, -depth * 0.02, shoulder_z - upper_arm_h - lower_arm_h / 2.0 + height * 0.04), f"{label}LowerArm_{x}", material=arm_material, vertices=12))
        parts.append(add_sphere(width * 0.03, (x, -depth * 0.02, shoulder_z - arm_h + height * 0.01), f"{label}Hand_{x}", material=skin))

    if defaults.get("has_hat"):
        parts.append(add_prism(head_r * 1.9, head_r * 1.9, head_r * 0.1, (0.0, 0.0, head_z + head_r * 0.92), f"{label}HatBrim", material=outfit, bevel=0.001))
        parts.append(add_cone(head_r * 0.92, head_r * 0.72, (0.0, 0.0, head_z + head_r * 1.22), f"{label}Hat", material=outfit, vertices=16))
    if defaults.get("has_beard"):
        parts.append(add_prism(width * 0.18, depth * 0.12, height * 0.14, (0.0, -depth * 0.08, head_z - head_r * 0.26), f"{label}Beard", material=fur_material("brown", mats), bevel=0.002))
    if defaults.get("has_staff"):
        parts.append(add_cylinder(width * 0.02, height * 0.82, (width * 0.26, 0.0, height * 0.42), f"{label}Staff", material=mats["wood"], vertices=10))
    if defaults.get("has_shield"):
        parts.append(add_cylinder(width * 0.14, depth * 0.06, (-width * 0.34, -depth * 0.08, leg_h + pelvis_h + torso_h * 0.48), f"{label}Shield", material=mats["steel"], vertices=20, rotation=(math.radians(90.0), 0.0, 0.0)))
    if defaults.get("has_spear"):
        parts.append(add_cylinder(width * 0.02, height * 0.88, (width * 0.28, 0.0, height * 0.44), f"{label}Spear", material=mats["wood"], vertices=10))
        parts.append(add_cone(width * 0.05, height * 0.1, (width * 0.28, 0.0, height * 0.92), f"{label}SpearTip", material=mats["steel"], vertices=10))
    if defaults.get("has_hammer"):
        parts.append(add_cylinder(width * 0.018, height * 0.34, (width * 0.26, 0.0, height * 0.34), f"{label}HammerHandle", material=mats["wood"], vertices=10))
        parts.append(add_prism(width * 0.12, depth * 0.08, height * 0.08, (width * 0.26, 0.0, height * 0.48), f"{label}HammerHead", material=mats["steel"], bevel=0.002))
    if defaults.get("has_pouch"):
        parts.append(add_prism(width * 0.12, depth * 0.12, height * 0.12, (width * 0.24, -depth * 0.04, leg_h + pelvis_h * 0.32), f"{label}Pouch", material=mats["leather"], bevel=0.002))
    if defaults.get("has_sword"):
        parts.append(add_prism(width * 0.028, depth * 0.028, height * 0.34, (width * 0.3, 0.0, height * 0.26), f"{label}SwordBlade", material=mats["steel"], bevel=0.001))
        parts.append(add_prism(width * 0.08, depth * 0.02, height * 0.016, (width * 0.3, 0.0, height * 0.1), f"{label}SwordGuard", material=mats["gold"], bevel=0.001))
        parts.append(add_prism(width * 0.02, depth * 0.02, height * 0.08, (width * 0.3, 0.0, height * 0.06), f"{label}SwordGrip", material=mats["leather"], bevel=0.001))
    if defaults.get("has_ears"):
        for x in (-head_r * 0.84, head_r * 0.84):
            parts.append(add_cone(head_r * 0.18, head_r * 0.36, (x, 0.0, head_z + head_r * 0.58), f"{label}Ear_{x}", material=skin, vertices=6))
    if defaults.get("has_tusks"):
        for x in (-head_r * 0.22, head_r * 0.22):
            parts.append(add_cone(head_r * 0.08, head_r * 0.28, (x, depth * 0.12, head_z - head_r * 0.18), f"{label}Tusk_{x}", material=mats["white_paint"], vertices=8, rotation=(math.radians(110.0), 0.0, 0.0)))
    return join_parts(parts, f"{label}Asset")


def generate_quadruped(params, mats, label, defaults):
    width = cm(params.get("width", defaults.get("width", 60.0)))
    depth = cm(params.get("depth", defaults.get("depth", 120.0)))
    height = cm(params.get("height", defaults.get("height", 90.0)))
    fur = fur_material(params.get("fur_color", defaults.get("fur_color", "brown")), mats)
    parts = []

    body_w = width * defaults.get("body_width", 0.48)
    body_d = depth * defaults.get("body_depth", 0.52)
    body_h = height * defaults.get("body_height", 0.32)
    shoulder_z = height * defaults.get("shoulder_height", 0.54)
    parts.append(add_sphere(body_w * 0.34, (0.0, -body_d * 0.18, shoulder_z + body_h * 0.04), f"{label}Chest", material=fur, scale=(1.0, 1.12, 1.04)))
    parts.append(add_sphere(body_w * 0.34, (0.0, body_d * 0.18, shoulder_z - body_h * 0.02), f"{label}Haunch", material=fur, scale=(1.0, 1.04, 0.98)))
    parts.append(add_prism(body_w * 0.96, body_d * 0.56, body_h * 0.72, (0.0, 0.0, shoulder_z), f"{label}BodyBridge", material=fur, bevel=0.006))
    parts.append(add_prism(body_w * 0.78, body_d * 0.3, body_h * 0.16, (0.0, 0.0, shoulder_z - body_h * 0.28), f"{label}Belly", material=fur, bevel=0.003))
    neck_len = depth * defaults.get("neck_len", 0.16)
    head_w = width * defaults.get("head_width", 0.24)
    head_d = depth * defaults.get("head_depth", 0.18)
    head_h = height * defaults.get("head_height", 0.18)
    head_z = shoulder_z + height * defaults.get("head_lift", 0.14)
    head_y = -body_d * 0.74
    muzzle_depth = head_d * defaults.get("muzzle_ratio", 0.54)
    parts.append(add_prism(width * 0.12, neck_len, height * 0.18, (0.0, -body_d * 0.46, shoulder_z + height * 0.08), f"{label}Neck", material=fur, rotation=(math.radians(-18.0), 0.0, 0.0), bevel=0.003))
    parts.append(add_prism(head_w, head_d * 0.86, head_h, (0.0, head_y, head_z), f"{label}Head", material=fur, bevel=0.004))
    parts.append(add_prism(head_w * 0.68, muzzle_depth, head_h * 0.46, (0.0, head_y - head_d * 0.42, head_z - head_h * 0.1), f"{label}Muzzle", material=fur, bevel=0.003))
    parts.append(add_prism(head_w * 0.14, head_d * 0.12, head_h * 0.1, (0.0, head_y - head_d * 0.72, head_z - head_h * 0.14), f"{label}Nose", material=mats["black_paint"], bevel=0.001))
    for x in (-head_w * 0.22, head_w * 0.22):
        parts.append(add_sphere(head_w * 0.05, (x, head_y - head_d * 0.42, head_z + head_h * 0.06), f"{label}Eye_{x}", material=mats["shadow"], scale=(1.0, 1.0, 0.6)))
    ear_height = head_h * defaults.get("ear_height", 0.44)
    for x in (-head_w * 0.22, head_w * 0.22):
        parts.append(add_cone(head_w * 0.12, ear_height, (x, head_y - head_d * 0.04, head_z + head_h * 0.42), f"{label}Ear_{x}", material=fur, vertices=8))
    front_leg_z = shoulder_z - body_h * 0.18
    rear_leg_z = shoulder_z - body_h * 0.24
    for x in (-body_w * 0.32, body_w * 0.32):
        for y, base_z, tag in [(-body_d * 0.16, front_leg_z, "Front"), (body_d * 0.2, rear_leg_z, "Rear")]:
            foot_h = height * 0.05
            lower_leg_h = max((base_z - foot_h) * 0.5, height * 0.14)
            upper_leg_h = max(base_z - lower_leg_h - foot_h, height * 0.12)
            leg_radius = width * defaults.get("leg_radius", 0.05)
            parts.append(add_sphere(leg_radius * 1.1, (x, y, base_z), f"{label}Hip_{tag}_{x}_{y}", material=fur, scale=(1.0, 0.9, 1.0)))
            parts.append(add_cylinder(leg_radius * 1.06, upper_leg_h, (x, y, foot_h + lower_leg_h + upper_leg_h / 2.0), f"{label}UpperLeg_{tag}_{x}_{y}", material=fur, vertices=12))
            parts.append(add_sphere(leg_radius * 0.9, (x, y, foot_h + lower_leg_h), f"{label}Knee_{tag}_{x}_{y}", material=fur, scale=(1.0, 0.9, 1.0)))
            parts.append(add_cylinder(leg_radius * 0.84, lower_leg_h, (x, y, foot_h + lower_leg_h / 2.0), f"{label}LowerLeg_{tag}_{x}_{y}", material=fur, vertices=12))
            foot_material = mats["black_paint"] if defaults.get("hooves", False) else fur
            parts.append(add_prism(leg_radius * 2.4, leg_radius * 3.2, foot_h, (x, y + depth * 0.01, foot_h / 2.0), f"{label}Foot_{tag}_{x}_{y}", material=foot_material, bevel=0.001))
    tail_len = depth * defaults.get("tail_len", 0.2)
    parts.append(add_prism(width * 0.06, tail_len, height * 0.06, (0.0, body_d * 0.54, shoulder_z + height * defaults.get("tail_height", 0.02)), f"{label}Tail", material=fur, rotation=(math.radians(defaults.get("tail_pitch", 42.0)), 0.0, 0.0), bevel=0.002))
    if defaults.get("mane"):
        parts.append(add_prism(width * 0.08, depth * 0.28, height * 0.2, (0.0, -body_d * 0.34, shoulder_z + height * 0.18), f"{label}Mane", material=fur_material("black", mats), bevel=0.002))
    if defaults.get("horns"):
        for x in (-head_w * 0.24, head_w * 0.24):
            parts.append(add_cone(head_w * 0.08, head_h * 0.44, (x, head_y - head_d * 0.02, head_z + head_h * 0.34), f"{label}Horn_{x}", material=mats["white_paint"], vertices=8))
    if defaults.get("antlers"):
        for x in (-head_w * 0.24, head_w * 0.24):
            parts.append(add_prism(head_w * 0.06, head_d * 0.06, head_h * 0.6, (x, head_y - head_d * 0.04, head_z + head_h * 0.36), f"{label}AntlerStem_{x}", material=mats["brown_fur"], bevel=0.001))
            parts.append(add_prism(head_w * 0.24, head_d * 0.04, head_h * 0.04, (x, head_y - head_d * 0.02, head_z + head_h * 0.5), f"{label}AntlerBranch_{x}", material=mats["brown_fur"], bevel=0.001))
    return join_parts(parts, f"{label}Asset")


def generate_bird(params, mats):
    width = cm(params.get("width", 42.0))
    depth = cm(params.get("depth", 60.0))
    height = cm(params.get("height", 46.0))
    color = surface_color_material(params.get("body_color", "blue"), mats, "blue")
    style = str(params.get("bird_style", "perched")).lower()
    parts = []

    parts.append(add_sphere(width * 0.18, (0.0, 0.0, height * 0.38), "BirdBody", material=color, scale=(1.0, 1.5, 1.0)))
    parts.append(add_sphere(width * 0.1, (0.0, -depth * 0.26, height * 0.5), "BirdHead", material=color))
    parts.append(add_cone(width * 0.05, width * 0.12, (0.0, -depth * 0.38, height * 0.5), "BirdBeak", material=mats["yellow"], vertices=8, rotation=(math.radians(90.0), 0.0, 0.0)))
    wing_rot = math.radians(-12.0 if style == "perched" else -38.0)
    for x in (-width * 0.16, width * 0.16):
        parts.append(add_prism(width * 0.08, depth * 0.24, height * 0.18, (x, 0.0, height * 0.4), "BirdWing", material=color, rotation=(wing_rot, 0.0, 0.0), bevel=0.002))
    if style == "perched":
        for x in (-width * 0.05, width * 0.05):
            parts.append(add_cylinder(width * 0.015, height * 0.24, (x, depth * 0.1, height * 0.12), "BirdLeg", material=mats["bronze"], vertices=8))
    return join_parts(parts, "BirdAsset")


def generate_fish(params, mats):
    width = cm(params.get("width", 24.0))
    depth = cm(params.get("depth", 72.0))
    height = cm(params.get("height", 26.0))
    color = surface_color_material(params.get("body_color", "silver"), mats, "silver_paint")
    style = str(params.get("fish_style", "stream")).lower()
    parts = []

    parts.append(add_tapered_cylinder(height * 0.42, height * 0.14, depth * 0.62, (0.0, 0.0, height * 0.3), "FishBody", material=color, vertices=18, rotation=(0.0, math.radians(90.0), 0.0)))
    parts.append(add_prism(width * 0.08, depth * 0.18, height * 0.14, (0.0, 0.0, height * 0.5), "FishDorsalFin", material=color, rotation=(math.radians(12.0), 0.0, 0.0), bevel=0.001))
    parts.append(add_prism(width * 0.06, depth * 0.16, height * 0.08, (-width * 0.12, -depth * 0.02, height * 0.22), "FishPectoralFinLeft", material=color, rotation=(0.0, 0.0, math.radians(22.0)), bevel=0.001))
    parts.append(add_prism(width * 0.06, depth * 0.16, height * 0.08, (width * 0.12, -depth * 0.02, height * 0.22), "FishPectoralFinRight", material=color, rotation=(0.0, 0.0, math.radians(-22.0)), bevel=0.001))
    parts.append(add_prism(width * 0.08, depth * 0.12, height * 0.08, (0.0, depth * 0.14, height * 0.12), "FishLowerFin", material=color, rotation=(math.radians(-10.0), 0.0, 0.0), bevel=0.001))
    parts.append(add_prism(width * 0.04, depth * 0.12, height * 0.18, (-width * 0.08, depth * 0.34, height * 0.3), "FishTailLeft", material=color, rotation=(0.0, 0.0, math.radians(26.0)), bevel=0.001))
    parts.append(add_prism(width * 0.04, depth * 0.12, height * 0.18, (width * 0.08, depth * 0.34, height * 0.3), "FishTailRight", material=color, rotation=(0.0, 0.0, math.radians(-26.0)), bevel=0.001))
    parts.append(add_sphere(width * 0.03, (-width * 0.08, -depth * 0.22, height * 0.34), "FishEyeLeft", material=mats["screen_white"], scale=(1.0, 1.0, 0.8)))
    parts.append(add_sphere(width * 0.03, (width * 0.08, -depth * 0.22, height * 0.34), "FishEyeRight", material=mats["screen_white"], scale=(1.0, 1.0, 0.8)))
    if style == "shark":
        parts.append(add_prism(width * 0.16, depth * 0.16, height * 0.22, (0.0, -depth * 0.08, height * 0.58), "FishDorsal", material=mats["gray_paint"], bevel=0.001))
    return join_parts(parts, "FishAsset")


def generate_dragon(params, mats):
    width = cm(params.get("width", 260.0))
    depth = cm(params.get("depth", 520.0))
    height = cm(params.get("height", 240.0))
    color = surface_color_material(params.get("scale_color", "green"), mats, "green")
    membrane = cloth_material(params.get("membrane_color", params.get("scale_color", "red")), mats, "cloth_red")
    pose = str(params.get("pose", "standing")).lower()
    parts = []

    body_z = height * (0.66 if pose == "flying" else 0.56)
    parts.append(add_sphere(width * 0.18, (0.0, -depth * 0.04, body_z), "DragonChest", material=color, scale=(1.0, 1.28, 0.9)))
    parts.append(add_sphere(width * 0.15, (0.0, depth * 0.14, body_z - height * 0.02), "DragonHaunch", material=color, scale=(1.0, 1.14, 0.82)))
    parts.append(add_prism(width * 0.18, depth * 0.24, height * 0.16, (0.0, depth * 0.04, body_z), "DragonBodyBridge", material=color, bevel=0.005))
    parts.append(add_prism(width * 0.12, depth * 0.14, height * 0.08, (0.0, -depth * 0.2, body_z + height * 0.08), "DragonNeckBase", material=color, rotation=(math.radians(-20.0), 0.0, 0.0), bevel=0.004))
    parts.append(add_prism(width * 0.08, depth * 0.12, height * 0.07, (0.0, -depth * 0.3, body_z + height * 0.16), "DragonNeckUpper", material=color, rotation=(math.radians(-24.0), 0.0, 0.0), bevel=0.003))
    parts.append(add_prism(width * 0.18, depth * 0.16, height * 0.12, (0.0, -depth * 0.42, body_z + height * 0.2), "DragonHead", material=color, bevel=0.004))
    parts.append(add_prism(width * 0.14, depth * 0.08, height * 0.05, (0.0, -depth * 0.5, body_z + height * 0.14), "DragonJaw", material=color, bevel=0.003))
    for x in (-width * 0.05, width * 0.05):
        parts.append(add_cone(width * 0.03, height * 0.14, (x, -depth * 0.42, body_z + height * 0.3), f"DragonHorn_{x}", material=mats["white_paint"], vertices=8))
    for z, y in [(body_z + height * 0.14, -depth * 0.08), (body_z + height * 0.18, depth * 0.04), (body_z + height * 0.14, depth * 0.18)]:
        parts.append(add_cone(width * 0.03, height * 0.1, (0.0, y, z), "DragonSpine", material=mats["darksteel"], vertices=8))
    for x in (-width * 0.14, width * 0.14):
        for y in (-depth * 0.08, depth * 0.14):
            foot_h = height * 0.05
            lower_leg_h = height * 0.2
            upper_leg_h = max(body_z - lower_leg_h - foot_h, height * 0.16)
            parts.append(add_cylinder(width * 0.05, upper_leg_h, (x, y, foot_h + lower_leg_h + upper_leg_h / 2.0), f"DragonUpperLeg_{x}_{y}", material=color, vertices=12))
            parts.append(add_cylinder(width * 0.042, lower_leg_h, (x, y, foot_h + lower_leg_h / 2.0), f"DragonLowerLeg_{x}_{y}", material=color, vertices=12))
            parts.append(add_prism(width * 0.11, depth * 0.16, foot_h, (x, y + depth * 0.02, foot_h / 2.0), f"DragonFoot_{x}_{y}", material=mats["darksteel"], bevel=0.001))
    tail_rot = math.radians(60.0 if pose == "flying" else 34.0)
    parts.append(add_prism(width * 0.08, depth * 0.18, height * 0.08, (0.0, depth * 0.28, body_z - height * 0.02), "DragonTailBase", material=color, rotation=(math.radians(26.0), 0.0, 0.0), bevel=0.003))
    parts.append(add_prism(width * 0.06, depth * 0.18, height * 0.06, (0.0, depth * 0.42, body_z + height * 0.06), "DragonTailMid", material=color, rotation=(tail_rot, 0.0, 0.0), bevel=0.003))
    parts.append(add_prism(width * 0.04, depth * 0.14, height * 0.04, (0.0, depth * 0.54, body_z + height * 0.18), "DragonTailTip", material=color, rotation=(math.radians(72.0), 0.0, 0.0), bevel=0.002))
    for x in (-width * 0.28, width * 0.28):
        wing_roll = math.radians(-18.0 if x < 0 else 18.0)
        wing_pitch = math.radians(12.0 if pose == "flying" else 22.0)
        parts.append(add_prism(width * 0.34, depth * 0.05, height * 0.03, (x, 0.0, body_z + height * 0.12), "DragonWingBone", material=color, rotation=(wing_pitch, 0.0, wing_roll), bevel=0.002))
        parts.append(add_prism(width * 0.24, depth * 0.28, height * 0.02, (x * 1.22, depth * 0.02, body_z + height * 0.08), "DragonWingMembrane", material=membrane, rotation=(math.radians(8.0 if pose == "flying" else 18.0), 0.0, wing_roll), bevel=0.001))
    return join_parts(parts, "DragonAsset")


def generate_coin(params, mats):
    width = cm(params.get("width", 4.0))
    depth = cm(params.get("depth", 4.0))
    height = cm(params.get("height", 0.4))
    parts = [
        add_cylinder(width * 0.5, height, (0.0, 0.0, height / 2.0), "CoinBody", material=mats["gold"], vertices=24),
        add_cylinder(width * 0.38, height * 0.1, (0.0, 0.0, height * 0.58), "CoinStamp", material=mats["bronze"], vertices=20),
    ]
    return join_parts(parts, "CoinAsset")


def generate_gem(params, mats):
    width = cm(params.get("width", 12.0))
    depth = cm(params.get("depth", 12.0))
    height = cm(params.get("height", 18.0))
    color = surface_color_material(params.get("gem_color", "purple"), mats, "purple")
    parts = [
        add_cone(width * 0.34, height * 0.56, (0.0, 0.0, height * 0.72), "GemTop", material=color, vertices=6),
        add_cone(width * 0.34, height * 0.56, (0.0, 0.0, height * 0.28), "GemBottom", material=color, vertices=6, rotation=(math.pi, 0.0, 0.0)),
    ]
    return join_parts(parts, "GemAsset")


def generate_key(params, mats):
    width = cm(params.get("width", 4.0))
    depth = cm(params.get("depth", 16.0))
    height = cm(params.get("height", 2.0))
    material = material_for(params.get("material", "gold"), mats, "gold")
    parts = [
        add_cylinder(width * 0.38, height * 0.22, (0.0, -depth * 0.22, height * 0.5), "KeyRing", material=material, vertices=20, rotation=(math.radians(90.0), 0.0, 0.0)),
        add_prism(width * 0.18, depth * 0.7, height * 0.12, (0.0, depth * 0.12, height * 0.5), "KeyShaft", material=material, bevel=0.001),
        add_prism(width * 0.4, depth * 0.1, height * 0.12, (0.0, depth * 0.42, height * 0.5), "KeyBitTop", material=material, bevel=0.001),
        add_prism(width * 0.18, depth * 0.1, height * 0.12, (-width * 0.12, depth * 0.5, height * 0.5), "KeyBitBottom", material=material, bevel=0.001),
    ]
    return join_parts(parts, "KeyAsset")


def generate_scroll(params, mats):
    width = cm(params.get("width", 16.0))
    depth = cm(params.get("depth", 34.0))
    height = cm(params.get("height", 6.0))
    parts = [
        add_prism(width * 0.92, depth * 0.56, height * 0.1, (0.0, 0.0, height * 0.42), "ScrollSheet", material=mats["paper"], bevel=0.001),
        add_cylinder(height * 0.18, width, (0.0, -depth * 0.24, height * 0.46), "ScrollRollTop", material=mats["paper"], rotation=(0.0, math.radians(90.0), 0.0), vertices=12),
        add_cylinder(height * 0.18, width, (0.0, depth * 0.24, height * 0.46), "ScrollRollBottom", material=mats["paper"], rotation=(0.0, math.radians(90.0), 0.0), vertices=12),
    ]
    if bool(params.get("tied", True)):
        parts.append(add_prism(width * 0.12, depth * 0.1, height * 0.18, (0.0, 0.0, height * 0.54), "ScrollRibbon", material=mats["cloth_red"], bevel=0.001))
    return join_parts(parts, "ScrollAsset")


def generate_potion(params, mats):
    width = cm(params.get("width", 12.0))
    depth = cm(params.get("depth", 12.0))
    height = cm(params.get("height", 28.0))
    liquid = surface_color_material(params.get("liquid_color", "blue"), mats, "blue_liquid")
    parts = [
        add_tapered_cylinder(width * 0.28, width * 0.18, height * 0.56, (0.0, 0.0, height * 0.3), "PotionBottle", material=mats["glass"], vertices=18),
        add_cylinder(width * 0.14, height * 0.16, (0.0, 0.0, height * 0.68), "PotionNeck", material=mats["glass"], vertices=16),
        add_tapered_cylinder(width * 0.22, width * 0.14, height * 0.34, (0.0, 0.0, height * 0.2), "PotionLiquid", material=liquid, vertices=18),
        add_prism(width * 0.12, depth * 0.12, height * 0.1, (0.0, 0.0, height * 0.82), "PotionCork", material=mats["wood"], bevel=0.001),
    ]
    return join_parts(parts, "PotionAsset")


def generate_treasure_chest(params, mats):
    width = cm(params.get("width", 90.0))
    depth = cm(params.get("depth", 56.0))
    height = cm(params.get("height", 62.0))
    material = material_for(params.get("material", "wood"), mats, "wood")
    base_h = height * 0.46
    lid_base_h = height * 0.14
    arch_radius = depth * 0.26
    lid_arch_z = base_h + lid_base_h + arch_radius * 0.56
    parts = [
        add_prism(width * 0.98, depth, base_h, (0.0, 0.0, base_h / 2.0), "TreasureChestBase", material=material, bevel=0.006),
        add_prism(width * 0.92, depth * 0.84, lid_base_h, (0.0, 0.0, base_h + lid_base_h / 2.0), "TreasureChestLidBase", material=material, bevel=0.004),
        add_tapered_cylinder(arch_radius, arch_radius, width * 0.92, (0.0, 0.0, lid_arch_z), "TreasureChestLidArch", material=material, vertices=20, rotation=(0.0, math.radians(90.0), 0.0)),
        add_prism(width * 0.1, depth * 0.96, base_h * 0.92, (0.0, 0.0, base_h * 0.5), "TreasureBandCenter", material=mats["gold"], bevel=0.002),
        add_prism(width * 0.08, depth * 0.88, lid_base_h * 1.2, (0.0, 0.0, base_h + lid_base_h * 0.66), "TreasureLidBand", material=mats["gold"], bevel=0.001),
    ]
    for x in (-width * 0.36, width * 0.36):
        parts.append(add_prism(width * 0.07, depth * 0.94, base_h * 0.9, (x, 0.0, base_h * 0.5), f"TreasureBandSide_{x}", material=mats["gold"], bevel=0.002))
    for x, y in [(-width * 0.38, -depth * 0.34), (width * 0.38, -depth * 0.34), (-width * 0.38, depth * 0.34), (width * 0.38, depth * 0.34)]:
        parts.append(add_prism(width * 0.08, depth * 0.08, height * 0.08, (x, y, height * 0.04), "TreasureFoot", material=material, bevel=0.002))
    parts.append(add_prism(width * 0.16, depth * 0.08, height * 0.14, (0.0, -depth * 0.46, base_h * 0.58), "TreasureLatchPlate", material=mats["gold"], bevel=0.002))
    parts.append(add_prism(width * 0.08, depth * 0.06, height * 0.18, (0.0, -depth * 0.5, base_h * 0.54), "TreasureLock", material=mats["bronze"], bevel=0.002))
    for x in (-width * 0.48, width * 0.48):
        parts.append(add_cylinder(height * 0.06, depth * 0.04, (x, 0.0, base_h * 0.56), f"TreasureSideHandle_{x}", material=mats["gold"], vertices=16, rotation=(math.radians(90.0), 0.0, 0.0)))
    if bool(params.get("has_gems", True)):
        parts.append(add_sphere(width * 0.06, (0.0, 0.0, lid_arch_z + arch_radius * 0.62), "TreasureGem", material=mats["crystal"]))
    return join_parts(parts, "TreasureChestAsset")


def generate_artifact(params, mats):
    width = cm(params.get("width", 34.0))
    depth = cm(params.get("depth", 34.0))
    height = cm(params.get("height", 72.0))
    style = str(params.get("artifact_style", "obelisk")).lower()
    parts = [
        add_prism(width * 0.58, depth * 0.58, height * 0.1, (0.0, 0.0, height * 0.05), "ArtifactBaseLower", material=mats["stone"], bevel=0.003),
        add_prism(width * 0.44, depth * 0.44, height * 0.08, (0.0, 0.0, height * 0.14), "ArtifactBaseUpper", material=mats["bronze"], bevel=0.002),
    ]
    if style == "orb":
        for angle in (0.0, math.radians(120.0), math.radians(240.0)):
            x = math.cos(angle) * width * 0.12
            y = math.sin(angle) * depth * 0.12
            parts.append(add_prism(width * 0.08, depth * 0.04, height * 0.24, (x, y, height * 0.28), "ArtifactClaw", material=mats["bronze"], rotation=(math.radians(-18.0), 0.0, angle), bevel=0.002))
        parts.append(add_cylinder(width * 0.08, height * 0.14, (0.0, 0.0, height * 0.24), "ArtifactStem", material=mats["bronze"], vertices=12))
        parts.append(add_sphere(width * 0.2, (0.0, 0.0, height * 0.48), "ArtifactOrb", material=mats["crystal"]))
        parts.append(add_tapered_cylinder(width * 0.24, width * 0.24, height * 0.04, (0.0, 0.0, height * 0.42), "ArtifactRing", material=mats["gold"], vertices=18))
    else:
        parts.append(add_tapered_cylinder(width * 0.22, width * 0.08, height * 0.62, (0.0, 0.0, height * 0.42), "ArtifactObelisk", material=mats["gold"], vertices=6))
        parts.append(add_tapered_cylinder(width * 0.16, width * 0.16, height * 0.04, (0.0, 0.0, height * 0.24), "ArtifactRing", material=mats["bronze"], vertices=18))
        parts.append(add_sphere(width * 0.08, (0.0, 0.0, height * 0.72), "ArtifactTipGem", material=mats["crystal"], scale=(1.0, 1.0, 1.2)))
    return join_parts(parts, "ArtifactAsset")


def generate_terrain(params, mats):
    width = cm(params.get("width", 500.0))
    depth = cm(params.get("depth", 500.0))
    height = cm(params.get("height", 90.0))
    material = material_for(params.get("material", "grass"), mats, "grass")
    parts = [add_prism(width, depth, height * 0.22, (0.0, 0.0, height * 0.11), "TerrainBase", material=mats["dirt"], bevel=0.003)]
    for x, y, scale, z_scale in [
        (-width * 0.22, -depth * 0.14, 0.32, 0.34),
        (width * 0.18, depth * 0.02, 0.26, 0.28),
        (0.0, depth * 0.2, 0.2, 0.24),
        (width * 0.04, -depth * 0.22, 0.18, 0.2),
    ]:
        parts.append(add_sphere(width * scale, (x, y, height * 0.24), "TerrainMound", material=material, scale=(1.0, 1.0, z_scale)))
    parts.append(add_prism(width * 0.16, depth * 0.82, height * 0.04, (-width * 0.04, 0.0, height * 0.18), "TerrainPath", material=mats["dirt"], rotation=(0.0, 0.0, math.radians(16.0)), bevel=0.001))
    for x, y, rock_w, rock_d, rock_h in [
        (-width * 0.14, depth * 0.08, width * 0.08, depth * 0.06, height * 0.12),
        (width * 0.2, -depth * 0.1, width * 0.06, depth * 0.05, height * 0.1),
        (width * 0.08, depth * 0.2, width * 0.05, depth * 0.04, height * 0.08),
    ]:
        parts.append(add_prism(rock_w, rock_d, rock_h, (x, y, height * 0.18 + rock_h / 2.0), "TerrainRock", material=mats["stone"], bevel=0.003))
    return join_parts(parts, "TerrainAsset")


def generate_hill(params, mats):
    width = cm(params.get("width", 340.0))
    depth = cm(params.get("depth", 340.0))
    height = cm(params.get("height", 180.0))
    return join_parts([
        add_prism(width, depth, height * 0.16, (0.0, 0.0, height * 0.08), "HillBase", material=mats["dirt"], bevel=0.003),
        add_sphere(width * 0.42, (0.0, 0.0, height * 0.28), "HillDome", material=mats["grass"], scale=(1.0, 1.0, 0.46)),
    ], "HillAsset")


def generate_mountain(params, mats):
    width = cm(params.get("width", 420.0))
    depth = cm(params.get("depth", 420.0))
    height = cm(params.get("height", 520.0))
    return join_parts([
        add_cone(width * 0.42, height, (0.0, 0.0, height * 0.5), "MountainPeak", material=mats["stone"], vertices=6),
        add_cone(width * 0.26, height * 0.48, (-width * 0.18, depth * 0.12, height * 0.26), "MountainSpurLeft", material=mats["stone"], vertices=6),
        add_cone(width * 0.22, height * 0.36, (width * 0.2, -depth * 0.08, height * 0.2), "MountainSpurRight", material=mats["stone"], vertices=6),
    ], "MountainAsset")


def generate_cliff(params, mats):
    width = cm(params.get("width", 420.0))
    depth = cm(params.get("depth", 180.0))
    height = cm(params.get("height", 320.0))
    parts = [
        add_prism(width, depth, height * 0.62, (0.0, 0.0, height * 0.31), "CliffBody", material=mats["stone"], bevel=0.01),
        add_prism(width * 0.82, depth * 0.32, height * 0.18, (-width * 0.08, depth * 0.24, height * 0.72), "CliffShelfUpper", material=mats["stone"], bevel=0.006),
        add_prism(width * 0.62, depth * 0.28, height * 0.12, (width * 0.12, depth * 0.12, height * 0.5), "CliffShelfMid", material=mats["stone"], bevel=0.006),
    ]
    return join_parts(parts, "CliffAsset")


def generate_valley(params, mats):
    width = cm(params.get("width", 520.0))
    depth = cm(params.get("depth", 420.0))
    height = cm(params.get("height", 180.0))
    parts = [
        add_prism(width, depth, height * 0.12, (0.0, 0.0, height * 0.06), "ValleyFloor", material=mats["grass"], bevel=0.003),
        add_sphere(width * 0.3, (-width * 0.3, 0.0, height * 0.16), "ValleyLeftRise", material=mats["grass"], scale=(1.0, 1.0, 0.44)),
        add_sphere(width * 0.3, (width * 0.3, 0.0, height * 0.16), "ValleyRightRise", material=mats["grass"], scale=(1.0, 1.0, 0.44)),
    ]
    return join_parts(parts, "ValleyAsset")


def generate_cave(params, mats):
    width = cm(params.get("width", 320.0))
    depth = cm(params.get("depth", 260.0))
    height = cm(params.get("height", 220.0))
    parts = [
        add_prism(width, depth, height * 0.14, (0.0, 0.0, height * 0.07), "CaveFloor", material=mats["stone"], bevel=0.006),
        add_sphere(width * 0.42, (0.0, 0.0, height * 0.34), "CaveRoofMass", material=mats["stone"], scale=(1.0, depth / width * 0.86, 0.62)),
        add_prism(width * 0.22, depth * 0.18, height * 0.34, (-width * 0.26, depth * 0.04, height * 0.22), "CaveButtressLeft", material=mats["stone"], bevel=0.004),
        add_prism(width * 0.22, depth * 0.18, height * 0.34, (width * 0.26, depth * 0.04, height * 0.22), "CaveButtressRight", material=mats["stone"], bevel=0.004),
        add_prism(width * 0.48, depth * 0.34, height * 0.34, (0.0, depth * 0.1, height * 0.18), "CaveOpeningInner", material=mats["shadow"], bevel=0.003),
        add_prism(width * 0.54, depth * 0.08, height * 0.08, (0.0, -depth * 0.14, height * 0.18), "CaveEntryLip", material=mats["stone"], bevel=0.003),
    ]
    for x, y, h_scale in [(-width * 0.16, depth * 0.04, 0.18), (0.0, depth * 0.1, 0.14), (width * 0.18, depth * 0.02, 0.12)]:
        parts.append(add_cone(width * 0.05, height * h_scale, (x, y, height * h_scale / 2.0), "CaveStalagmite", material=mats["stone"], vertices=8))
    for x, y, h_scale in [(-width * 0.12, -depth * 0.02, 0.12), (width * 0.14, -depth * 0.04, 0.1)]:
        parts.append(add_cone(width * 0.04, height * h_scale, (x, y, height * 0.42), "CaveStalactite", material=mats["stone"], vertices=8, rotation=(math.pi, 0.0, 0.0)))
    return join_parts(parts, "CaveAsset")


def generate_ground_tile(params, mats):
    width = cm(params.get("width", 200.0))
    depth = cm(params.get("depth", 200.0))
    height = cm(params.get("height", 20.0))
    return join_parts([
        add_prism(width, depth, height, (0.0, 0.0, height / 2.0), "GroundTile", material=mats["dirt"], bevel=0.002),
        add_prism(width * 0.92, depth * 0.92, height * 0.18, (0.0, 0.0, height * 1.04), "GroundGrassCap", material=mats["grass"], bevel=0.001),
    ], "GroundTileAsset")


def generate_road_tile(params, mats):
    width = cm(params.get("width", 220.0))
    depth = cm(params.get("depth", 220.0))
    height = cm(params.get("height", 18.0))
    parts = [
        add_prism(width, depth, height, (0.0, 0.0, height / 2.0), "RoadTile", material=mats["asphalt"], bevel=0.002),
        add_prism(width * 0.08, depth * 0.7, height * 0.08, (0.0, 0.0, height * 1.02), "RoadLine", material=mats["yellow"], bevel=0.001),
    ]
    return join_parts(parts, "RoadTileAsset")


def generate_path_tile(params, mats):
    width = cm(params.get("width", 200.0))
    depth = cm(params.get("depth", 200.0))
    height = cm(params.get("height", 16.0))
    parts = [
        add_prism(width, depth, height, (0.0, 0.0, height / 2.0), "PathTile", material=mats["grass"], bevel=0.002),
        add_prism(width * 0.46, depth * 0.92, height * 0.08, (0.0, 0.0, height * 1.02), "PathStrip", material=mats["dirt"], bevel=0.001),
    ]
    return join_parts(parts, "PathTileAsset")


def generate_river_tile(params, mats):
    width = cm(params.get("width", 220.0))
    depth = cm(params.get("depth", 220.0))
    height = cm(params.get("height", 20.0))
    parts = [
        add_prism(width, depth, height, (0.0, 0.0, height / 2.0), "RiverTileBase", material=mats["grass"], bevel=0.002),
        add_prism(width * 0.36, depth * 0.96, height * 0.18, (0.0, 0.0, height * 0.5), "RiverChannel", material=mats["water"], bevel=0.001),
    ]
    return join_parts(parts, "RiverTileAsset")


def generate_dungeon_tile(params, mats):
    width = cm(params.get("width", 200.0))
    depth = cm(params.get("depth", 200.0))
    height = cm(params.get("height", 18.0))
    parts = [add_prism(width, depth, height, (0.0, 0.0, height / 2.0), "DungeonTileBase", material=mats["stone"], bevel=0.002)]
    for x in (-width * 0.24, 0.0, width * 0.24):
        parts.append(add_prism(width * 0.28, depth * 0.04, height * 0.08, (x, 0.0, height * 1.02), "DungeonGrooveX", material=mats["darksteel"], bevel=0.001))
    for y in (-depth * 0.24, 0.0, depth * 0.24):
        parts.append(add_prism(width * 0.04, depth * 0.28, height * 0.08, (0.0, y, height * 1.02), "DungeonGrooveY", material=mats["darksteel"], bevel=0.001))
    return join_parts(parts, "DungeonTileAsset")


def generate_male(params, mats):
    return generate_humanoid(params, mats, "Male", {"width": 58.0, "depth": 40.0, "height": 178.0, "skin_tone": "medium", "outfit_color": "blue", "hair_color": "brown"})


def generate_female(params, mats):
    return generate_humanoid(params, mats, "Female", {"width": 54.0, "depth": 36.0, "height": 168.0, "skin_tone": "light", "outfit_color": "red", "torso_width": 0.36, "hair_color": "black"})


def generate_child(params, mats):
    return generate_humanoid(params, mats, "Child", {"width": 42.0, "depth": 28.0, "height": 118.0, "skin_tone": "light", "outfit_color": "green", "torso_width": 0.36, "head_ratio": 0.22, "leg_ratio": 0.4, "hair_color": "brown"})


def generate_elder(params, mats):
    return generate_humanoid(params, mats, "Elder", {"width": 56.0, "depth": 38.0, "height": 166.0, "skin_tone": "light", "outfit_color": "brown", "hair_color": "gray", "has_staff": True, "has_beard": True})


def generate_merchant(params, mats):
    return generate_humanoid(params, mats, "Merchant", {"width": 58.0, "depth": 40.0, "height": 176.0, "skin_tone": "medium", "outfit_color": "green", "hair_color": "brown", "torso_width": 0.46, "has_pouch": True, "has_hat": True})


def generate_guard(params, mats):
    return generate_humanoid(params, mats, "Guard", {"width": 62.0, "depth": 42.0, "height": 184.0, "skin_tone": "medium", "outfit_color": "blue", "hair_color": "black", "has_shield": True, "has_spear": True})


def generate_farmer(params, mats):
    return generate_humanoid(params, mats, "Farmer", {"width": 58.0, "depth": 40.0, "height": 172.0, "skin_tone": "medium", "outfit_color": "brown", "hair_color": "brown", "has_hat": True, "has_staff": True})


def generate_blacksmith(params, mats):
    return generate_humanoid(params, mats, "Blacksmith", {"width": 64.0, "depth": 42.0, "height": 176.0, "skin_tone": "medium", "outfit_color": "brown", "hair_color": "black", "has_hammer": True, "has_beard": True})


def generate_soldier(params, mats):
    return generate_humanoid(params, mats, "Soldier", {"width": 62.0, "depth": 42.0, "height": 182.0, "skin_tone": "medium", "outfit_color": "red", "hair_color": "black", "has_shield": True, "has_sword": True})


def generate_elf(params, mats):
    return generate_humanoid(params, mats, "Elf", {"width": 54.0, "depth": 36.0, "height": 186.0, "skin_tone": "light", "outfit_color": "green", "hair_color": "golden", "has_ears": True, "has_staff": True})


def generate_orc(params, mats):
    return generate_humanoid(params, mats, "Orc", {"width": 72.0, "depth": 48.0, "height": 198.0, "skin_tone": "medium", "outfit_color": "brown", "hair_color": "black", "has_tusks": True, "torso_width": 0.5})


def generate_goblin(params, mats):
    return generate_humanoid(params, mats, "Goblin", {"width": 42.0, "depth": 28.0, "height": 112.0, "skin_tone": "medium", "outfit_color": "brown", "hair_color": "black", "has_ears": True, "head_ratio": 0.2, "leg_ratio": 0.38})


def generate_dwarf(params, mats):
    return generate_humanoid(params, mats, "Dwarf", {"width": 64.0, "depth": 42.0, "height": 132.0, "skin_tone": "light", "outfit_color": "blue", "hair_color": "brown", "has_beard": True, "has_hammer": True, "leg_ratio": 0.34})


def generate_dog(params, mats):
    return generate_quadruped(params, mats, "Dog", {"width": 46.0, "depth": 90.0, "height": 62.0, "fur_color": "brown", "body_width": 0.54, "body_depth": 0.5, "body_height": 0.34, "shoulder_height": 0.48, "head_lift": 0.08, "tail_len": 0.18, "tail_pitch": 34.0, "head_width": 0.22, "head_depth": 0.2, "muzzle_ratio": 0.62, "ear_height": 0.34})


def generate_cat(params, mats):
    return generate_quadruped(params, mats, "Cat", {"width": 30.0, "depth": 54.0, "height": 36.0, "fur_color": "orange", "body_width": 0.48, "body_depth": 0.5, "body_height": 0.26, "shoulder_height": 0.4, "head_lift": 0.12, "tail_len": 0.3, "tail_pitch": 58.0, "head_width": 0.24, "head_depth": 0.18, "leg_radius": 0.035, "muzzle_ratio": 0.42, "ear_height": 0.56})


def generate_horse(params, mats):
    return generate_quadruped(params, mats, "Horse", {"width": 80.0, "depth": 180.0, "height": 160.0, "fur_color": "brown", "tail_len": 0.24, "tail_pitch": 28.0, "head_width": 0.2, "head_depth": 0.22, "head_lift": 0.18, "leg_radius": 0.04, "mane": True, "hooves": True, "body_width": 0.44, "body_depth": 0.56, "body_height": 0.34, "shoulder_height": 0.62, "ear_height": 0.34})


def generate_cow(params, mats):
    return generate_quadruped(params, mats, "Cow", {"width": 84.0, "depth": 170.0, "height": 138.0, "fur_color": "white", "tail_len": 0.2, "tail_pitch": 20.0, "head_width": 0.24, "head_depth": 0.22, "head_lift": 0.12, "horns": True, "hooves": True, "body_width": 0.48, "body_depth": 0.58, "body_height": 0.36, "shoulder_height": 0.56, "muzzle_ratio": 0.64, "ear_height": 0.22})


def generate_deer(params, mats):
    return generate_quadruped(params, mats, "Deer", {"width": 66.0, "depth": 132.0, "height": 122.0, "fur_color": "tan", "tail_len": 0.12, "tail_pitch": 26.0, "head_width": 0.2, "head_depth": 0.18, "head_lift": 0.18, "leg_radius": 0.035, "antlers": True, "hooves": True, "body_width": 0.42, "body_depth": 0.5, "body_height": 0.28, "shoulder_height": 0.58, "ear_height": 0.32})


def generate_wolf(params, mats):
    return generate_quadruped(params, mats, "Wolf", {"width": 50.0, "depth": 110.0, "height": 72.0, "fur_color": "gray", "body_width": 0.5, "body_depth": 0.54, "body_height": 0.32, "shoulder_height": 0.52, "head_lift": 0.12, "tail_len": 0.26, "tail_pitch": 36.0, "head_width": 0.22, "head_depth": 0.22, "muzzle_ratio": 0.66, "ear_height": 0.42})


GENERATOR_MAP = {
    "control_panel": generate_control_panel,
    "terminal": generate_terminal,
    "computer": generate_computer,
    "server_rack": generate_server_rack,
    "energy_cell": generate_energy_cell,
    "tech_crate": generate_tech_crate,
    "space_door": generate_space_door,
    "airlock": generate_airlock,
    "turret": generate_turret,
    "drone": generate_drone,
    "pipe": generate_pipe,
    "valve": generate_valve,
    "tank": generate_tank,
    "generator": generate_generator,
    "conveyor_belt": generate_conveyor_belt,
    "toolbox": generate_toolbox,
    "forklift": generate_forklift,
    "storage_rack": generate_storage_rack,
    "street_lamp": generate_street_lamp,
    "traffic_light": generate_traffic_light,
    "road_sign": generate_road_sign,
    "street_bench": generate_street_bench,
    "mailbox": generate_mailbox,
    "trash_can": generate_trash_can,
    "bus_stop": generate_bus_stop,
    "phone_booth": generate_phone_booth,
    "car": generate_car,
    "truck": generate_truck,
    "bike": generate_bike,
    "motorcycle": generate_motorcycle,
    "tractor": generate_tractor,
    "battle_tank": generate_battle_tank,
    "boat": generate_boat,
    "canoe": generate_canoe,
    "ship": generate_ship,
    "plane": generate_plane,
    "helicopter": generate_helicopter,
    "male": generate_male,
    "female": generate_female,
    "child": generate_child,
    "elder": generate_elder,
    "merchant": generate_merchant,
    "guard": generate_guard,
    "farmer": generate_farmer,
    "blacksmith": generate_blacksmith,
    "soldier": generate_soldier,
    "elf": generate_elf,
    "orc": generate_orc,
    "goblin": generate_goblin,
    "dwarf": generate_dwarf,
    "dragon": generate_dragon,
    "dog": generate_dog,
    "cat": generate_cat,
    "horse": generate_horse,
    "cow": generate_cow,
    "deer": generate_deer,
    "wolf": generate_wolf,
    "bird": generate_bird,
    "fish": generate_fish,
    "coin": generate_coin,
    "gem": generate_gem,
    "key": generate_key,
    "scroll": generate_scroll,
    "potion": generate_potion,
    "treasure_chest": generate_treasure_chest,
    "artifact": generate_artifact,
    "terrain": generate_terrain,
    "hill": generate_hill,
    "mountain": generate_mountain,
    "cliff": generate_cliff,
    "valley": generate_valley,
    "cave": generate_cave,
    "ground_tile": generate_ground_tile,
    "road_tile": generate_road_tile,
    "path_tile": generate_path_tile,
    "river_tile": generate_river_tile,
    "dungeon_tile": generate_dungeon_tile,
    "game_background_2d": generate_game_background_2d,
}


def generate_world_asset(params):
    mats = build_materials()
    asset_type = params.get("asset_type")
    if asset_type not in GENERATOR_MAP:
        raise ValueError(f"Unsupported world asset_type: {asset_type}")
    return GENERATOR_MAP[asset_type](params, mats)


def main():
    parser = argparse.ArgumentParser(description="Procedural World Prop Generator")
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
    asset_obj = generate_world_asset(params)

    if args.render:
        utils.setup_lighting_and_camera(asset_obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)


if __name__ == "__main__":
    main()
