import argparse
import json
import math
import os
import random
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


def cm(value):
    return float(value) / 100.0


def seed_for(asset_type, params):
    total = 0
    source = f"{asset_type}:{json.dumps(params, sort_keys=True)}"
    for index, char in enumerate(source):
        total += (index + 1) * ord(char)
    return total


def build_materials():
    return {
        "brick": utils.create_material("ArchitectureBrick", diffuse_color=(0.58, 0.24, 0.18, 1.0), roughness=0.88),
        "concrete": utils.create_material("ArchitectureConcrete", diffuse_color=(0.61, 0.62, 0.64, 1.0), roughness=0.92),
        "stone": utils.create_material("ArchitectureStone", diffuse_color=(0.56, 0.53, 0.5, 1.0), roughness=0.94),
        "wood": utils.create_material("ArchitectureWood", diffuse_color=(0.44, 0.29, 0.17, 1.0), roughness=0.68),
        "plaster": utils.create_material("ArchitecturePlaster", diffuse_color=(0.87, 0.84, 0.78, 1.0), roughness=0.8),
        "tile": utils.create_material("ArchitectureTile", diffuse_color=(0.69, 0.71, 0.75, 1.0), roughness=0.48),
        "clay_tiles": utils.create_material("ArchitectureClayRoof", diffuse_color=(0.63, 0.26, 0.16, 1.0), roughness=0.8),
        "wood_shingles": utils.create_material("ArchitectureShingles", diffuse_color=(0.35, 0.24, 0.14, 1.0), roughness=0.84),
        "metal_sheets": utils.create_material("ArchitectureRoofMetal", diffuse_color=(0.56, 0.62, 0.72, 1.0), metallic=0.72, roughness=0.28),
        "marble": utils.create_material("ArchitectureMarble", diffuse_color=(0.91, 0.92, 0.94, 1.0), roughness=0.22),
        "steel": utils.create_material("ArchitectureSteel", diffuse_color=(0.49, 0.54, 0.61, 1.0), metallic=0.86, roughness=0.24),
        "iron": utils.create_material("ArchitectureIron", diffuse_color=(0.24, 0.27, 0.3, 1.0), metallic=0.74, roughness=0.42),
        "aluminum": utils.create_material("ArchitectureAluminum", diffuse_color=(0.72, 0.76, 0.8, 1.0), metallic=0.84, roughness=0.24),
        "glass": utils.create_material("ArchitectureGlass", diffuse_color=(0.78, 0.9, 0.98, 1.0), metallic=0.05, roughness=0.08),
        "trim": utils.create_material("ArchitectureTrim", diffuse_color=(0.95, 0.93, 0.89, 1.0), roughness=0.45),
        "shadow": utils.create_material("ArchitectureShadow", diffuse_color=(0.25, 0.25, 0.27, 1.0), roughness=0.96),
    }


def add_prism(width, depth, height, location, name, material=None, rotation=(0.0, 0.0, 0.0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (max(width, 0.01) / 2.0, max(depth, 0.01) / 2.0, max(height, 0.01) / 2.0)
    bpy.ops.object.transform_apply(scale=True)
    if bevel > 0:
        utils.apply_bevel(obj, width=bevel)
    if material:
        utils.apply_material(obj, material)
    return obj


def add_cylinder(radius, height, location, name, material=None, vertices=24, rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=max(radius, 0.01),
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
    bpy.ops.object.select_all(action="DESELECT")
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = name
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
    utils.apply_smooth_by_angle(obj)
    return obj


def material_for(key, mats):
    return mats.get(key, mats["concrete"])


def generate_wall(params, mats, rng):
    width = cm(params.get("width", 320.0))
    height = cm(params.get("height", 280.0))
    thickness = cm(params.get("thickness", 18.0))
    material_key = params.get("material", "plaster")
    opening_type = params.get("opening_type", "none")
    opening_width = min(cm(params.get("opening_width", 110.0)), width * 0.72)
    opening_height = min(cm(params.get("opening_height", 190.0)), height * 0.86)
    has_trim = bool(params.get("has_trim", False))
    main_material = material_for(material_key, mats)
    parts = []
    pilaster_width = min(max(thickness * 1.05, 0.06), width * 0.12)
    cap_height = min(max(height * 0.035, 0.06), 0.14)
    frame_depth = thickness * 1.04
    frame_thickness = min(0.07, max(thickness * 0.18, 0.03))

    if opening_type == "door":
        side_width = max((width - opening_width) / 2.0, pilaster_width)
        header_height = max(height - opening_height, 0.2)
        parts.extend([
            add_prism(side_width, thickness, height, (-width / 2.0 + side_width / 2.0, 0.0, height / 2.0), "WallSideLeft", material=main_material, bevel=0.008),
            add_prism(side_width, thickness, height, (width / 2.0 - side_width / 2.0, 0.0, height / 2.0), "WallSideRight", material=main_material, bevel=0.008),
            add_prism(opening_width, thickness, header_height, (0.0, 0.0, opening_height + header_height / 2.0), "WallHeader", material=main_material, bevel=0.008),
            add_prism(opening_width * 0.98, thickness * 0.14, opening_height * 0.96, (0.0, thickness * 0.36, opening_height * 0.5), "DoorOpeningShadow", material=mats["shadow"], bevel=0.001),
        ])
    elif opening_type == "window":
        side_width = max((width - opening_width) / 2.0, pilaster_width)
        sill_height = min(max(height * 0.28, 0.6), max(height - opening_height - 0.35, 0.45))
        header_height = max(height - opening_height - sill_height, 0.25)
        parts.extend([
            add_prism(side_width, thickness, height, (-width / 2.0 + side_width / 2.0, 0.0, height / 2.0), "WallWindowLeft", material=main_material, bevel=0.008),
            add_prism(side_width, thickness, height, (width / 2.0 - side_width / 2.0, 0.0, height / 2.0), "WallWindowRight", material=main_material, bevel=0.008),
            add_prism(opening_width, thickness, sill_height, (0.0, 0.0, sill_height / 2.0), "WallWindowSill", material=main_material, bevel=0.008),
            add_prism(opening_width, thickness, header_height, (0.0, 0.0, sill_height + opening_height + header_height / 2.0), "WallWindowHeader", material=main_material, bevel=0.008),
            add_prism(opening_width * 0.94, thickness * 0.14, opening_height * 0.92, (0.0, thickness * 0.34, sill_height + opening_height / 2.0), "WindowShadowInset", material=mats["shadow"], bevel=0.001),
            add_prism(opening_width * 0.9, thickness * 0.08, opening_height * 0.86, (0.0, thickness * 0.24, sill_height + opening_height / 2.0), "WindowGlass", material=mats["glass"], bevel=0.001),
        ])
        if has_trim:
            frame_bottom_z = sill_height + opening_height / 2.0
            parts.extend([
                add_prism(opening_width + frame_thickness * 2.0, frame_depth, frame_thickness, (0.0, 0.0, sill_height + frame_thickness / 2.0), "WindowTrimBottom", material=mats["trim"], bevel=0.004),
                add_prism(frame_thickness, frame_depth, opening_height, (-opening_width / 2.0 - frame_thickness / 2.0, 0.0, frame_bottom_z), "WindowTrimLeft", material=mats["trim"], bevel=0.004),
                add_prism(frame_thickness, frame_depth, opening_height, (opening_width / 2.0 + frame_thickness / 2.0, 0.0, frame_bottom_z), "WindowTrimRight", material=mats["trim"], bevel=0.004),
                add_prism(opening_width + frame_thickness * 2.0, frame_depth, frame_thickness, (0.0, 0.0, sill_height + opening_height - frame_thickness / 2.0), "WindowTrimTop", material=mats["trim"], bevel=0.004),
            ])
    else:
        parts.append(add_prism(width, thickness, height, (0.0, 0.0, height / 2.0), "WallMain", material=main_material, bevel=0.008))

    parts.extend([
        add_prism(pilaster_width, thickness * 1.08, height, (-width / 2.0 + pilaster_width / 2.0, 0.0, height / 2.0), "WallPilasterLeft", material=mats["trim"] if has_trim else main_material, bevel=0.004),
        add_prism(pilaster_width, thickness * 1.08, height, (width / 2.0 - pilaster_width / 2.0, 0.0, height / 2.0), "WallPilasterRight", material=mats["trim"] if has_trim else main_material, bevel=0.004),
    ])

    if has_trim:
        trim_height = cap_height
        trim_depth = thickness * 1.06
        parts.append(add_prism(width, trim_depth, trim_height, (0.0, 0.0, trim_height / 2.0), "WallBaseTrim", material=mats["trim"], bevel=0.003))
        parts.append(add_prism(width, trim_depth, trim_height * 0.7, (0.0, 0.0, height - trim_height * 0.35), "WallTopTrim", material=mats["trim"], bevel=0.003))

        if opening_type == "door":
            frame_mid_z = opening_height / 2.0
            parts.extend([
                add_prism(frame_thickness, frame_depth, opening_height, (-opening_width / 2.0 - frame_thickness / 2.0, 0.0, frame_mid_z), "DoorTrimLeft", material=mats["trim"], bevel=0.004),
                add_prism(frame_thickness, frame_depth, opening_height, (opening_width / 2.0 + frame_thickness / 2.0, 0.0, frame_mid_z), "DoorTrimRight", material=mats["trim"], bevel=0.004),
                add_prism(opening_width + frame_thickness * 2.0, frame_depth, frame_thickness, (0.0, 0.0, opening_height - frame_thickness / 2.0), "DoorTrimTop", material=mats["trim"], bevel=0.004),
            ])

    if material_key in {"brick", "stone"}:
        accent_material = mats["shadow"] if material_key == "stone" else mats["trim"]
        band_zs = [height * 0.24, height * 0.54, height * 0.82]
        for band_index, band_z in enumerate(band_zs):
            if opening_type == "window" and height * 0.3 < band_z < height * 0.72:
                left_span = width / 2.0 - opening_width / 2.0 - pilaster_width
                if left_span > 0.08:
                    band_width = left_span
                    parts.append(add_prism(band_width, thickness * 0.08, cap_height * 0.24, (-opening_width / 4.0 - band_width / 2.0, thickness * 0.48, band_z), f"WallBandLeft_{band_index}", material=accent_material, bevel=0.001))
                    parts.append(add_prism(band_width, thickness * 0.08, cap_height * 0.24, (opening_width / 4.0 + band_width / 2.0, thickness * 0.48, band_z), f"WallBandRight_{band_index}", material=accent_material, bevel=0.001))
            else:
                parts.append(add_prism(width * 0.92, thickness * 0.08, cap_height * 0.24, (0.0, thickness * 0.48, band_z), f"WallBand_{band_index}", material=accent_material, bevel=0.001))

    return join_parts(parts, "WallAsset")


def generate_floor(params, mats, rng):
    width = cm(params.get("width", 420.0))
    depth = cm(params.get("depth", 420.0))
    thickness = cm(params.get("thickness", 20.0))
    divisions = int(params.get("tile_divisions", 6))
    material_key = params.get("material", "wood")
    main_material = material_for(material_key, mats)
    parts = [add_prism(width, depth, thickness, (0.0, 0.0, thickness / 2.0), "FloorSlab", material=main_material, bevel=0.005)]

    if material_key == "wood":
        plank_count = max(4, min(16, divisions if divisions > 0 else 8))
        plank_width = width / plank_count
        for index in range(plank_count - 1):
            x = -width / 2.0 + plank_width * (index + 1)
            parts.append(add_prism(0.01, depth * 0.98, thickness * 0.14, (x, 0.0, thickness + thickness * 0.07), f"WoodSeam_{index}", material=mats["shadow"]))
    else:
        grid = max(2, min(12, divisions if divisions > 0 else 6))
        cell_x = width / grid
        cell_y = depth / grid
        for index in range(grid - 1):
            x = -width / 2.0 + cell_x * (index + 1)
            y = -depth / 2.0 + cell_y * (index + 1)
            parts.append(add_prism(0.012, depth * 0.98, thickness * 0.16, (x, 0.0, thickness + thickness * 0.08), f"FloorGridX_{index}", material=mats["shadow"]))
            parts.append(add_prism(width * 0.98, 0.012, thickness * 0.16, (0.0, y, thickness + thickness * 0.08), f"FloorGridY_{index}", material=mats["shadow"]))

    return join_parts(parts, "FloorAsset")


def generate_ceiling(params, mats, rng):
    width = cm(params.get("width", 420.0))
    depth = cm(params.get("depth", 420.0))
    thickness = cm(params.get("thickness", 12.0))
    has_trim = bool(params.get("has_trim", True))
    main_material = material_for(params.get("material", "plaster"), mats)
    parts = [add_prism(width, depth, thickness, (0.0, 0.0, thickness / 2.0), "CeilingPanel", material=main_material, bevel=0.004)]

    if has_trim:
        trim_width = min(0.12, max(width * 0.03, 0.05))
        trim_depth = min(0.12, max(depth * 0.03, 0.05))
        trim_height = min(0.05, max(thickness * 0.4, 0.02))
        z = trim_height / 2.0
        parts.extend([
            add_prism(width, trim_depth, trim_height, (0.0, -depth / 2.0 + trim_depth / 2.0, z), "CeilingTrimNorth", material=mats["trim"], bevel=0.003),
            add_prism(width, trim_depth, trim_height, (0.0, depth / 2.0 - trim_depth / 2.0, z), "CeilingTrimSouth", material=mats["trim"], bevel=0.003),
            add_prism(trim_width, depth - trim_depth * 2.0, trim_height, (-width / 2.0 + trim_width / 2.0, 0.0, z), "CeilingTrimWest", material=mats["trim"], bevel=0.003),
            add_prism(trim_width, depth - trim_depth * 2.0, trim_height, (width / 2.0 - trim_width / 2.0, 0.0, z), "CeilingTrimEast", material=mats["trim"], bevel=0.003),
        ])

    return join_parts(parts, "CeilingAsset")


def add_roof_panel(parts, span, length, thickness, slope_radians, location, rotation, name, material):
    panel_length = span / max(math.cos(slope_radians), 0.05)
    parts.append(
        add_prism(
            panel_length,
            length,
            thickness,
            location,
            name,
            material=material,
            rotation=rotation,
            bevel=0.004,
        )
    )


def generate_roof(params, mats, rng):
    width = cm(params.get("width", 520.0))
    depth = cm(params.get("depth", 420.0))
    thickness = cm(params.get("thickness", 18.0))
    slope = math.radians(float(params.get("slope", 32.0)))
    overhang = cm(params.get("overhang", 35.0))
    roof_style = params.get("roof_style", "gabled")
    roof_material = material_for(params.get("material", "clay_tiles"), mats)
    total_width = width + overhang * 2.0
    total_depth = depth + overhang * 2.0
    parts = []

    if roof_style == "flat":
        parts.append(add_prism(total_width, total_depth, thickness, (0.0, 0.0, thickness / 2.0), "RoofFlatDeck", material=roof_material, bevel=0.005))
        lip_height = thickness * 0.45
        lip_depth = max(thickness * 0.5, 0.05)
        parts.extend([
            add_prism(total_width, lip_depth, lip_height, (0.0, -total_depth / 2.0 + lip_depth / 2.0, thickness + lip_height / 2.0), "RoofLipNorth", material=mats["trim"], bevel=0.003),
            add_prism(total_width, lip_depth, lip_height, (0.0, total_depth / 2.0 - lip_depth / 2.0, thickness + lip_height / 2.0), "RoofLipSouth", material=mats["trim"], bevel=0.003),
            add_prism(lip_depth, total_depth, lip_height, (-total_width / 2.0 + lip_depth / 2.0, 0.0, thickness + lip_height / 2.0), "RoofLipWest", material=mats["trim"], bevel=0.003),
            add_prism(lip_depth, total_depth, lip_height, (total_width / 2.0 - lip_depth / 2.0, 0.0, thickness + lip_height / 2.0), "RoofLipEast", material=mats["trim"], bevel=0.003),
        ])
    elif roof_style == "mansard":
        lower_slope = math.radians(min(math.degrees(slope) + 18.0, 62.0))
        top_width = total_width * 0.42
        top_depth = total_depth * 0.42
        rise_x = math.tan(lower_slope) * ((total_width - top_width) / 2.0)
        rise_y = math.tan(lower_slope) * ((total_depth - top_depth) / 2.0)
        z_x = rise_x / 2.0 + thickness / 2.0
        z_y = rise_y / 2.0 + thickness / 2.0
        add_roof_panel(parts, (total_width - top_width) / 2.0, total_depth, thickness, lower_slope, (-top_width / 2.0 - (total_width - top_width) / 4.0, 0.0, z_x), (0.0, lower_slope, 0.0), "RoofMansardWest", roof_material)
        add_roof_panel(parts, (total_width - top_width) / 2.0, total_depth, thickness, lower_slope, (top_width / 2.0 + (total_width - top_width) / 4.0, 0.0, z_x), (0.0, -lower_slope, 0.0), "RoofMansardEast", roof_material)
        add_roof_panel(parts, (total_depth - top_depth) / 2.0, top_width, thickness, lower_slope, (0.0, -top_depth / 2.0 - (total_depth - top_depth) / 4.0, z_y), (-lower_slope, 0.0, 0.0), "RoofMansardNorth", roof_material)
        add_roof_panel(parts, (total_depth - top_depth) / 2.0, top_width, thickness, lower_slope, (0.0, top_depth / 2.0 + (total_depth - top_depth) / 4.0, z_y), (lower_slope, 0.0, 0.0), "RoofMansardSouth", roof_material)
        top_height = max(rise_x, rise_y) + thickness
        parts.append(add_prism(top_width, top_depth, thickness * 0.8, (0.0, 0.0, top_height), "RoofMansardTop", material=roof_material, bevel=0.004))
    else:
        span_x = total_width / 2.0
        rise_x = math.tan(slope) * span_x
        z_center = rise_x / 2.0 + thickness / 2.0
        add_roof_panel(parts, span_x, total_depth, thickness, slope, (-span_x / 2.0, 0.0, z_center), (0.0, slope, 0.0), "RoofWest", roof_material)
        add_roof_panel(parts, span_x, total_depth, thickness, slope, (span_x / 2.0, 0.0, z_center), (0.0, -slope, 0.0), "RoofEast", roof_material)
        ridge_length = total_depth if roof_style == "gabled" else total_depth * 0.82
        ridge_z = rise_x + thickness * 0.55
        parts.append(add_prism(max(total_width * 0.03, 0.08), ridge_length, thickness * 0.7, (0.0, 0.0, ridge_z), "RoofRidge", material=mats["trim"], bevel=0.003))

        if roof_style == "hip":
            span_y = total_depth / 2.0
            rise_y = math.tan(slope) * span_y
            z_y = rise_y / 2.0 + thickness / 2.0
            add_roof_panel(parts, span_y, total_width * 0.86, thickness, slope, (0.0, -span_y / 2.0, z_y), (-slope, 0.0, 0.0), "RoofNorth", roof_material)
            add_roof_panel(parts, span_y, total_width * 0.86, thickness, slope, (0.0, span_y / 2.0, z_y), (slope, 0.0, 0.0), "RoofSouth", roof_material)

    soffit_z = thickness * 0.12
    parts.append(add_prism(total_width * 0.92, total_depth * 0.92, thickness * 0.22, (0.0, 0.0, soffit_z), "RoofSoffit", material=mats["trim"], bevel=0.002))
    fascia_height = max(thickness * 0.5, 0.05)
    fascia_depth = max(thickness * 0.3, 0.03)
    parts.extend([
        add_prism(total_width * 0.98, fascia_depth, fascia_height, (0.0, -total_depth / 2.0 + fascia_depth / 2.0, fascia_height / 2.0), "RoofFasciaNorth", material=mats["trim"], bevel=0.002),
        add_prism(total_width * 0.98, fascia_depth, fascia_height, (0.0, total_depth / 2.0 - fascia_depth / 2.0, fascia_height / 2.0), "RoofFasciaSouth", material=mats["trim"], bevel=0.002),
        add_prism(fascia_depth, total_depth * 0.98, fascia_height, (-total_width / 2.0 + fascia_depth / 2.0, 0.0, fascia_height / 2.0), "RoofFasciaWest", material=mats["trim"], bevel=0.002),
        add_prism(fascia_depth, total_depth * 0.98, fascia_height, (total_width / 2.0 - fascia_depth / 2.0, 0.0, fascia_height / 2.0), "RoofFasciaEast", material=mats["trim"], bevel=0.002),
    ])

    return join_parts(parts, "RoofAsset")


def generate_pillar(params, mats, rng):
    height = cm(params.get("height", 320.0))
    width = cm(params.get("width", 40.0))
    shape = params.get("shape", "cylindrical")
    material_key = params.get("material", "stone")
    has_capital = bool(params.get("has_capital", True))
    main_material = material_for(material_key, mats)
    parts = []

    if shape == "square":
        shaft_width = width * 0.72 if has_capital else width
        parts.append(add_prism(shaft_width, shaft_width, height * 0.78 if has_capital else height, (0.0, 0.0, (height * 0.78 if has_capital else height) / 2.0 + (height * 0.11 if has_capital else 0.0)), "PillarShaft", material=main_material, bevel=0.006))
    else:
        shaft_radius = width * (0.28 if has_capital else 0.5)
        parts.append(add_cylinder(shaft_radius, height * 0.78 if has_capital else height, (0.0, 0.0, (height * 0.78 if has_capital else height) / 2.0 + (height * 0.11 if has_capital else 0.0)), "PillarShaft", material=main_material, vertices=28))

    if has_capital:
        base_height = height * 0.12
        cap_height = height * 0.1
        base_width = width * 1.12
        cap_width = width * 1.2
        if shape == "square":
            parts.extend([
                add_prism(base_width, base_width, base_height, (0.0, 0.0, base_height / 2.0), "PillarBase", material=mats["trim"], bevel=0.005),
                add_prism(cap_width, cap_width, cap_height, (0.0, 0.0, height - cap_height / 2.0), "PillarCapital", material=mats["trim"], bevel=0.005),
            ])
        else:
            parts.extend([
                add_cylinder(base_width / 2.0, base_height, (0.0, 0.0, base_height / 2.0), "PillarBase", material=mats["trim"], vertices=28),
                add_cylinder(cap_width / 2.0, cap_height, (0.0, 0.0, height - cap_height / 2.0), "PillarCapital", material=mats["trim"], vertices=28),
            ])

    return join_parts(parts, "PillarAsset")


def generate_beam(params, mats, rng):
    length = cm(params.get("length", 420.0))
    width = cm(params.get("width", 24.0))
    height = cm(params.get("height", 32.0))
    material_key = params.get("material", "wood")
    main_material = material_for(material_key, mats)
    parts = [add_prism(length, width, height, (0.0, 0.0, height / 2.0), "BeamBody", material=main_material, bevel=0.006)]

    if material_key == "steel":
        band_width = max(length * 0.05, 0.08)
        offset = length * 0.34
        for index, x in enumerate((-offset, offset)):
            parts.append(add_prism(band_width, width * 1.02, height * 1.03, (x, 0.0, height / 2.0), f"BeamBand_{index}", material=mats["shadow"], bevel=0.003))
    elif material_key == "concrete":
        cap_width = max(length * 0.06, 0.08)
        parts.extend([
            add_prism(cap_width, width * 0.96, height * 0.94, (-length / 2.0 + cap_width / 2.0, 0.0, height / 2.0), "BeamCapLeft", material=mats["shadow"], bevel=0.002),
            add_prism(cap_width, width * 0.96, height * 0.94, (length / 2.0 - cap_width / 2.0, 0.0, height / 2.0), "BeamCapRight", material=mats["shadow"], bevel=0.002),
        ])
    else:
        notch_width = max(length * 0.04, 0.06)
        for index, x in enumerate((-length * 0.25, length * 0.1)):
            parts.append(add_prism(notch_width, width * 1.01, height * 0.18, (x, 0.0, height - height * 0.09), f"BeamDetail_{index}", material=mats["shadow"], bevel=0.002))

    return join_parts(parts, "BeamAsset")


def generate_foundation(params, mats, rng):
    width = cm(params.get("width", 720.0))
    depth = cm(params.get("depth", 560.0))
    height = cm(params.get("height", 70.0))
    footing_depth = cm(params.get("footing_depth", 120.0))
    material_key = params.get("material", "concrete")
    has_footings = bool(params.get("has_footings", True))
    main_material = material_for(material_key, mats)
    parts = []

    embed_offset = min(height * 0.18, 0.12)
    slab_z = height / 2.0 - embed_offset
    parts.append(add_prism(width, depth, height, (0.0, 0.0, slab_z), "FoundationSlab", material=main_material, bevel=0.006))

    if has_footings:
        footing_width = min(max(width * 0.2, 0.36), 0.9)
        footing_depth_size = min(max(depth * 0.2, 0.36), 0.9)
        x_offset = width / 2.0 - footing_width / 2.0 - max(width * 0.06, 0.08)
        y_offset = depth / 2.0 - footing_depth_size / 2.0 - max(depth * 0.06, 0.08)
        footing_z = slab_z - height / 2.0 - footing_depth / 2.0 + max(height * 0.08, 0.03)
        for index, (x, y) in enumerate(((-x_offset, -y_offset), (x_offset, -y_offset), (-x_offset, y_offset), (x_offset, y_offset))):
            parts.append(
                add_prism(
                    footing_width,
                    footing_depth_size,
                    footing_depth,
                    (x, y, footing_z),
                    f"FoundationFooting_{index}",
                    material=mats["shadow"] if material_key == "concrete" else main_material,
                    bevel=0.004,
                )
            )

    return join_parts(parts, "FoundationAsset")


def generate_door(params, mats, rng):
    width = cm(params.get("width", 92.0))
    height = cm(params.get("height", 210.0))
    thickness = cm(params.get("thickness", 4.5))
    material_key = params.get("material", "wood")
    panel_style = params.get("panel_style", "inset")
    has_frame = bool(params.get("has_frame", True))
    has_handle = bool(params.get("has_handle", True))
    door_material = mats["steel"] if material_key == "metal" else mats["wood"]
    frame_material = mats["aluminum"] if material_key == "metal" else mats["trim"]
    parts = []

    panel_depth = thickness * 0.86
    panel_y = 0.0
    if has_frame:
        frame_width = min(max(width * 0.08, 0.05), 0.1)
        frame_depth = thickness * 1.25
        parts.extend([
            add_prism(frame_width, frame_depth, height, (-width / 2.0 - frame_width / 2.0, 0.0, height / 2.0), "DoorFrameLeft", material=frame_material, bevel=0.004),
            add_prism(frame_width, frame_depth, height, (width / 2.0 + frame_width / 2.0, 0.0, height / 2.0), "DoorFrameRight", material=frame_material, bevel=0.004),
            add_prism(width + frame_width * 2.0, frame_depth, frame_width * 0.9, (0.0, 0.0, height - frame_width * 0.45), "DoorFrameTop", material=frame_material, bevel=0.004),
        ])
        panel_y = -thickness * 0.04

    parts.append(add_prism(width, panel_depth, height, (0.0, panel_y, height / 2.0), "DoorPanel", material=door_material, bevel=0.006))

    inset_depth = max(thickness * 0.14, 0.008)
    detail_y = panel_y + panel_depth / 2.0 - inset_depth / 2.0
    if panel_style == "double":
        pane_width = width * 0.34
        pane_height = height * 0.28
        for col, x in enumerate((-width * 0.21, width * 0.21)):
            for row, z in enumerate((height * 0.3, height * 0.7)):
                parts.append(add_prism(pane_width, inset_depth, pane_height, (x, detail_y, z), f"DoorPanelInset_{col}_{row}", material=mats["shadow"], bevel=0.002))
    elif panel_style == "inset":
        parts.extend([
            add_prism(width * 0.62, inset_depth, height * 0.26, (0.0, detail_y, height * 0.33), "DoorInsetLower", material=mats["shadow"], bevel=0.002),
            add_prism(width * 0.52, inset_depth, height * 0.2, (0.0, detail_y, height * 0.7), "DoorInsetUpper", material=mats["shadow"], bevel=0.002),
        ])

    hinge_x = -width / 2.0 + max(width * 0.04, 0.02)
    for index, z in enumerate((height * 0.22, height * 0.5, height * 0.78)):
        parts.append(add_cylinder(thickness * 0.08, height=max(thickness * 0.46, 0.015), location=(hinge_x, -thickness * 0.48, z), name=f"DoorHinge_{index}", material=mats["steel"], vertices=14, rotation=(math.radians(90.0), 0.0, 0.0)))

    if has_handle:
        handle_x = width * 0.31
        handle_z = height * 0.48
        stem_depth = thickness * 0.16
        parts.extend([
            add_prism(0.02, stem_depth, 0.06, (handle_x, thickness * 0.35, handle_z), "DoorHandleStem", material=mats["steel"], bevel=0.002),
            add_prism(0.1, stem_depth * 0.78, 0.025, (handle_x + 0.04, thickness * 0.41, handle_z), "DoorHandleBar", material=mats["steel"], bevel=0.002),
        ])

    return join_parts(parts, "DoorAsset")


def generate_window(params, mats, rng):
    width = cm(params.get("width", 140.0))
    height = cm(params.get("height", 120.0))
    thickness = cm(params.get("thickness", 12.0))
    frame_key = params.get("frame_material", "wood")
    has_mullions = bool(params.get("has_mullions", True))
    has_sill = bool(params.get("has_sill", True))
    frame_material = mats["aluminum"] if frame_key == "aluminum" else mats["wood"]
    parts = []

    frame_width = min(max(width * 0.08, 0.04), 0.1)
    glass_depth = max(thickness * 0.2, 0.02)
    parts.extend([
        add_prism(frame_width, thickness, height, (-width / 2.0 + frame_width / 2.0, 0.0, height / 2.0), "WindowFrameLeft", material=frame_material, bevel=0.004),
        add_prism(frame_width, thickness, height, (width / 2.0 - frame_width / 2.0, 0.0, height / 2.0), "WindowFrameRight", material=frame_material, bevel=0.004),
        add_prism(width - frame_width * 2.0, thickness, frame_width, (0.0, 0.0, height - frame_width / 2.0), "WindowFrameTop", material=frame_material, bevel=0.004),
        add_prism(width - frame_width * 2.0, thickness, frame_width, (0.0, 0.0, frame_width / 2.0), "WindowFrameBottom", material=frame_material, bevel=0.004),
        add_prism(width - frame_width * 2.0, glass_depth, height - frame_width * 2.0, (0.0, 0.0, height / 2.0), "WindowGlass", material=mats["glass"], bevel=0.001),
    ])

    if has_mullions:
        mullion_width = max(frame_width * 0.58, 0.025)
        parts.extend([
            add_prism(mullion_width, glass_depth * 1.4, height - frame_width * 2.0, (0.0, 0.0, height / 2.0), "WindowMullionVertical", material=frame_material, bevel=0.002),
            add_prism(width - frame_width * 2.0, glass_depth * 1.4, mullion_width, (0.0, 0.0, height / 2.0), "WindowMullionHorizontal", material=frame_material, bevel=0.002),
        ])

    if has_sill:
        sill_depth = thickness * 1.25
        sill_height = max(frame_width * 0.45, 0.025)
        parts.append(add_prism(width + frame_width * 0.8, sill_depth, sill_height, (0.0, 0.0, -sill_height / 2.0), "WindowSill", material=frame_material, bevel=0.003))

    return join_parts(parts, "WindowAsset")


def generate_archway(params, mats, rng):
    opening_width = cm(params.get("width", 220.0))
    height = cm(params.get("height", 280.0))
    thickness = cm(params.get("thickness", 28.0))
    support_width = cm(params.get("support_width", 34.0))
    material_key = params.get("material", "stone")
    main_material = material_for(material_key, mats)
    parts = []

    arch_rise = min(opening_width * 0.42, height * 0.42)
    spring_height = max(height - arch_rise, height * 0.5)
    spring_height = min(spring_height, height - max(arch_rise * 0.75, 0.35))
    parts.extend([
        add_prism(support_width, thickness, spring_height, (-opening_width / 2.0 - support_width / 2.0, 0.0, spring_height / 2.0), "ArchSupportLeft", material=main_material, bevel=0.006),
        add_prism(support_width, thickness, spring_height, (opening_width / 2.0 + support_width / 2.0, 0.0, spring_height / 2.0), "ArchSupportRight", material=main_material, bevel=0.006),
    ])

    segment_count = 7
    block_width = opening_width / segment_count * 1.04
    block_height = max(arch_rise * 0.22, 0.12)
    for index in range(segment_count):
        theta = math.pi - (math.pi * (index + 0.5) / segment_count)
        x = math.cos(theta) * opening_width / 2.0
        z = spring_height + math.sin(theta) * arch_rise
        rotation_y = (math.pi / 2.0 - theta) * 0.48
        material = mats["trim"] if index == segment_count // 2 else main_material
        parts.append(
            add_prism(
                block_width,
                thickness,
                block_height,
                (x, 0.0, z),
                f"ArchVoussoir_{index}",
                material=material,
                rotation=(0.0, rotation_y, 0.0),
                bevel=0.004,
            )
        )

    return join_parts(parts, "ArchwayAsset")


def generate_gate(params, mats, rng):
    width = cm(params.get("width", 220.0))
    height = cm(params.get("height", 180.0))
    thickness = cm(params.get("thickness", 8.0))
    material_key = params.get("material", "iron")
    gate_style = params.get("gate_style", "barred")
    bar_count = int(params.get("bar_count", 8))
    main_material = mats["iron"] if material_key == "iron" else mats["wood"]
    accent_material = mats["steel"] if material_key == "iron" else mats["shadow"]
    parts = []

    frame_width = min(max(width * 0.06, 0.05), 0.12)
    parts.extend([
        add_prism(frame_width, thickness, height, (-width / 2.0 + frame_width / 2.0, 0.0, height / 2.0), "GateFrameLeft", material=main_material, bevel=0.004),
        add_prism(frame_width, thickness, height, (width / 2.0 - frame_width / 2.0, 0.0, height / 2.0), "GateFrameRight", material=main_material, bevel=0.004),
        add_prism(width, thickness, frame_width, (0.0, 0.0, height - frame_width / 2.0), "GateFrameTop", material=main_material, bevel=0.004),
        add_prism(width, thickness, frame_width, (0.0, 0.0, frame_width / 2.0), "GateFrameBottom", material=main_material, bevel=0.004),
    ])

    if gate_style == "solid":
        parts.append(add_prism(width - frame_width * 2.2, thickness * 0.65, height - frame_width * 2.2, (0.0, 0.0, height / 2.0), "GatePanelSolid", material=main_material, bevel=0.003))
        if material_key == "wood":
            parts.append(add_prism(width - frame_width * 3.0, thickness * 0.18, 0.08, (0.0, thickness * 0.32, height * 0.58), "GateBrace", material=accent_material, rotation=(0.0, math.radians(32.0), 0.0), bevel=0.002))
    else:
        clear_width = width - frame_width * 2.6
        spacing = clear_width / max(bar_count, 2)
        bar_width = min(max(spacing * 0.28, 0.025), 0.09)
        for index in range(bar_count):
            x = -clear_width / 2.0 + spacing * index + spacing / 2.0
            parts.append(add_prism(bar_width, thickness * 0.52, height - frame_width * 2.4, (x, 0.0, height / 2.0), f"GateBar_{index}", material=main_material, bevel=0.002))
        if material_key == "iron":
            ring_radius = max(width * 0.035, 0.05)
            parts.append(add_cylinder(ring_radius, max(thickness * 0.3, 0.02), (0.0, thickness * 0.36, height * 0.52), "GateRing", material=accent_material, vertices=18, rotation=(math.radians(90.0), 0.0, 0.0)))

    hinge_x = -width / 2.0 + frame_width * 0.55
    for index, z in enumerate((height * 0.24, height * 0.5, height * 0.76)):
        parts.append(add_cylinder(frame_width * 0.18, max(thickness * 0.34, 0.02), (hinge_x, -thickness * 0.46, z), f"GateHinge_{index}", material=accent_material, vertices=14, rotation=(math.radians(90.0), 0.0, 0.0)))

    return join_parts(parts, "GateAsset")


def generate_stairs(params, mats, rng):
    width = cm(params.get("width", 120.0))
    step_count = int(params.get("step_count", 8))
    step_height = cm(params.get("step_height", 17.0))
    step_depth = cm(params.get("step_depth", 28.0))
    material_key = params.get("material", "wood")
    has_railing = bool(params.get("has_railing", True))
    main_material = material_for(material_key, mats)
    rail_material = mats["steel"] if material_key != "wood" else mats["trim"]
    parts = []

    total_depth = step_count * step_depth
    total_height = step_count * step_height
    for step_index in range(step_count):
        current_height = step_height * (step_index + 1)
        y = -total_depth / 2.0 + step_depth * step_index + step_depth / 2.0
        parts.append(add_prism(width, step_depth, current_height, (0.0, y, current_height / 2.0), f"StairStep_{step_index}", material=main_material, bevel=0.003))

    stringer_width = max(width * 0.08, 0.06)
    stringer_length = math.sqrt(total_depth ** 2 + total_height ** 2)
    stringer_angle = math.atan2(total_height, total_depth)
    stringer_height = max(step_height * 1.2, 0.06)
    stringer_z = total_height * 0.42
    for side in (-1, 1):
        x = side * (width / 2.0 - stringer_width / 2.0)
        parts.append(
            add_prism(
                stringer_width,
                stringer_length * 1.02,
                stringer_height,
                (x, 0.0, stringer_z),
                f"StairStringer_{side}",
                material=main_material,
                rotation=(stringer_angle, 0.0, 0.0),
                bevel=0.002,
            )
        )

    if has_railing:
        post_width = max(width * 0.035, 0.03)
        rail_height = max(total_height * 0.22, 0.9)
        post_positions = sorted(set([0, max(1, step_count // 3), max(1, (step_count * 2) // 3), step_count - 1]))
        rail_length = math.sqrt(total_depth ** 2 + total_height ** 2)
        rail_angle = math.atan2(total_height, total_depth)
        for side in (-1, 1):
            side_x = side * (width / 2.0 - post_width / 2.0)
            for index, step_index in enumerate(post_positions):
                y = -total_depth / 2.0 + step_depth * step_index + step_depth / 2.0
                tread_z = step_height * (step_index + 1)
                post_height = rail_height if step_index != step_count - 1 else rail_height * 1.06
                parts.append(add_prism(post_width, post_width, post_height, (side_x, y, tread_z + post_height / 2.0), f"StairPost_{side}_{index}", material=rail_material, bevel=0.002))
            top_rail_z = total_height + rail_height * 0.72
            mid_rail_z = total_height + rail_height * 0.34
            parts.append(add_prism(post_width * 1.2, rail_length, post_width, (side_x, 0.0, top_rail_z), f"StairHandrail_{side}", material=rail_material, rotation=(rail_angle, 0.0, 0.0), bevel=0.002))
            parts.append(add_prism(post_width * 0.8, rail_length, post_width * 0.6, (side_x, 0.0, mid_rail_z), f"StairMidRail_{side}", material=rail_material, rotation=(rail_angle, 0.0, 0.0), bevel=0.001))

    return join_parts(parts, "StairsAsset")


def generate_ladder(params, mats, rng):
    width = cm(params.get("width", 50.0))
    height = cm(params.get("height", 260.0))
    rung_count = int(params.get("rung_count", 8))
    material_key = params.get("material", "wood")
    rail_material = mats["steel"] if material_key == "metal" else mats["wood"]
    rung_material = mats["aluminum"] if material_key == "metal" else mats["trim"]
    parts = []

    rail_radius = max(width * 0.06, 0.02)
    side_x = width / 2.0 - rail_radius
    parts.extend([
        add_cylinder(rail_radius, height, (-side_x, 0.0, height / 2.0), "LadderRailLeft", material=rail_material, vertices=18),
        add_cylinder(rail_radius, height, (side_x, 0.0, height / 2.0), "LadderRailRight", material=rail_material, vertices=18),
    ])

    usable_height = height - rail_radius * 4.0
    rung_spacing = usable_height / max(rung_count - 1, 1)
    rung_radius = max(rail_radius * 0.75, 0.015)
    rung_length = max(width - rail_radius * 3.2, 0.12)
    for rung_index in range(rung_count):
        z = rail_radius * 2.0 + rung_spacing * rung_index
        parts.append(
            add_cylinder(
                rung_radius,
                rung_length,
                (0.0, 0.0, z),
                f"LadderRung_{rung_index}",
                material=rung_material,
                vertices=16,
                rotation=(0.0, math.radians(90.0), 0.0),
            )
        )

    return join_parts(parts, "LadderAsset")


def generate_ramp(params, mats, rng):
    width = cm(params.get("width", 140.0))
    depth = cm(params.get("depth", 320.0))
    input_height = cm(params.get("height", 55.0))
    slope = float(params.get("slope", 12.0))
    slope_height = depth * math.tan(math.radians(slope))
    height = max(0.15, (input_height + slope_height) / 2.0)
    material_key = params.get("material", "concrete")
    has_side_curbs = bool(params.get("has_side_curbs", True))
    main_material = material_for(material_key, mats)
    parts = [add_wedge(width, depth, height, (0.0, 0.0, height / 2.0), "RampBody", material=main_material, bevel=0.005)]

    if has_side_curbs:
        curb_width = max(width * 0.05, 0.04)
        curb_height = max(height * 0.18, 0.04)
        curb_z = curb_height / 2.0
        x_offset = width / 2.0 - curb_width / 2.0
        parts.extend([
            add_prism(curb_width, depth, curb_height, (-x_offset, 0.0, curb_z), "RampCurbLeft", material=mats["trim"], bevel=0.002),
            add_prism(curb_width, depth, curb_height, (x_offset, 0.0, curb_z), "RampCurbRight", material=mats["trim"], bevel=0.002),
        ])

    return join_parts(parts, "RampAsset")


def generate_bridge(params, mats, rng):
    length = cm(params.get("length", 900.0))
    width = cm(params.get("width", 220.0))
    height = cm(params.get("height", 180.0))
    deck_thickness = cm(params.get("deck_thickness", 24.0))
    material_key = params.get("material", "wood")
    support_count = int(params.get("support_count", 4))
    has_railings = bool(params.get("has_railings", True))
    main_material = mats["steel"] if material_key == "steel" else material_for(material_key, mats)
    accent_material = mats["shadow"] if material_key == "stone" else mats["trim"]
    deck_z = height + deck_thickness / 2.0
    parts = []

    if material_key == "wood":
        plank_count = max(6, min(18, int(length / 0.55)))
        plank_depth = length / plank_count
        for index in range(plank_count):
            y = -length / 2.0 + plank_depth * index + plank_depth / 2.0
            plank_width = width * (0.95 if index % 2 == 0 else 0.92)
            parts.append(add_prism(plank_width, plank_depth * 0.92, deck_thickness, (0.0, y, deck_z), f"BridgePlank_{index}", material=main_material, bevel=0.002))
    else:
        parts.append(add_prism(width, length, deck_thickness, (0.0, 0.0, deck_z), "BridgeDeck", material=main_material, bevel=0.004))

    support_span = max(length - width * 0.1, 0.2)
    pillar_width = min(max(width * 0.14, 0.12), 0.32)
    beam_x = width * 0.3
    beam_height = max(deck_thickness * 0.6, 0.06)
    parts.extend([
        add_prism(pillar_width * 0.7, length * 0.96, beam_height, (-beam_x, 0.0, height + beam_height / 2.0), "BridgeBeamLeft", material=accent_material, bevel=0.003),
        add_prism(pillar_width * 0.7, length * 0.96, beam_height, (beam_x, 0.0, height + beam_height / 2.0), "BridgeBeamRight", material=accent_material, bevel=0.003),
    ])

    for index in range(max(2, support_count)):
        y = -support_span / 2.0 + (support_span / max(support_count - 1, 1)) * index
        parts.append(add_prism(width * 0.86, pillar_width * 0.36, beam_height, (0.0, y, height + beam_height / 2.0), f"BridgeCrossBeam_{index}", material=accent_material, bevel=0.002))
        for side in (-1, 1):
            x = side * beam_x
            parts.append(add_prism(pillar_width, pillar_width, height, (x, y, height / 2.0), f"BridgeSupport_{side}_{index}", material=accent_material, bevel=0.003))
            brace_height = max(height * 0.42, 0.24)
            brace_length = math.sqrt((pillar_width * 1.2) ** 2 + brace_height ** 2)
            parts.append(
                add_prism(
                    pillar_width * 0.24,
                    pillar_width * 0.24,
                    brace_length,
                    (x, y, height * 0.42),
                    f"BridgeBrace_{side}_{index}",
                    material=accent_material,
                    rotation=(0.0, math.radians(45.0 * side), math.radians(90.0)),
                    bevel=0.001,
                )
            )

    if has_railings:
        rail_height = max(height * 0.18, 0.85)
        side_x = width / 2.0 - pillar_width * 0.35
        post_count = max(4, min(12, support_count + 2))
        for side in (-1, 1):
            for index in range(post_count):
                y = -length / 2.0 + (length / max(post_count - 1, 1)) * index
                parts.append(add_prism(pillar_width * 0.45, pillar_width * 0.45, rail_height, (side * side_x, y, height + deck_thickness + rail_height / 2.0), f"BridgeRailPost_{side}_{index}", material=accent_material, bevel=0.002))
            parts.append(add_prism(pillar_width * 0.6, length, pillar_width * 0.45, (side * side_x, 0.0, height + deck_thickness + rail_height), f"BridgeTopRail_{side}", material=accent_material, bevel=0.002))
            parts.append(add_prism(pillar_width * 0.42, length, pillar_width * 0.24, (side * side_x, 0.0, height + deck_thickness + rail_height * 0.54), f"BridgeMidRail_{side}", material=accent_material, bevel=0.001))

    return join_parts(parts, "BridgeAsset")


def generate_balcony(params, mats, rng):
    width = cm(params.get("width", 320.0))
    depth = cm(params.get("depth", 160.0))
    railing_height = cm(params.get("height", 105.0))
    thickness = cm(params.get("thickness", 18.0))
    material_key = params.get("material", "concrete")
    has_railings = bool(params.get("has_railings", True))
    main_material = material_for(material_key, mats)
    rail_material = mats["steel"] if material_key != "wood" else mats["trim"]
    parts = [add_prism(width, depth, thickness, (0.0, 0.0, thickness / 2.0), "BalconySlab", material=main_material, bevel=0.005)]

    bracket_size = min(max(depth * 0.18, 0.16), 0.32)
    bracket_z = thickness + bracket_size / 2.0
    bracket_y = depth * 0.14
    for side in (-1, 1):
        parts.append(add_prism(bracket_size, bracket_size, bracket_size, (side * (width * 0.26), bracket_y, bracket_z), f"BalconyBracket_{side}", material=mats["shadow"], rotation=(math.radians(45.0), 0.0, 0.0), bevel=0.002))

    if has_railings:
        post_width = max(width * 0.03, 0.03)
        z_center = thickness + railing_height / 2.0
        rail_z = thickness + railing_height
        post_count = max(4, min(10, int(width / 0.6)))
        for index in range(post_count):
            x = -width / 2.0 + (width / max(post_count - 1, 1)) * index
            parts.append(add_prism(post_width, post_width, railing_height, (x, depth / 2.0 - post_width / 2.0, z_center), f"BalconyFrontPost_{index}", material=rail_material, bevel=0.002))
        parts.append(add_prism(width, post_width, post_width * 1.2, (0.0, depth / 2.0 - post_width / 2.0, rail_z), "BalconyFrontRail", material=rail_material, bevel=0.002))
        side_depth = depth - post_width
        for side in (-1, 1):
            parts.append(add_prism(post_width, side_depth, post_width * 1.2, (side * (width / 2.0 - post_width / 2.0), 0.0, rail_z), f"BalconySideRail_{side}", material=rail_material, bevel=0.002))

    return join_parts(parts, "BalconyAsset")


def generate_fence(params, mats, rng):
    width = cm(params.get("width", 420.0))
    height = cm(params.get("height", 160.0))
    thickness = cm(params.get("thickness", 10.0))
    material_key = params.get("material", "wood")
    fence_style = params.get("fence_style", "picket")
    section_count = int(params.get("section_count", 10))
    main_material = mats["iron"] if material_key == "iron" else mats["wood"]
    accent_material = mats["steel"] if material_key == "iron" else mats["trim"]
    parts = []

    post_width = min(max(width * 0.03, 0.05), 0.12)
    rail_height = max(thickness * 0.5, 0.03)
    post_count = max(2, min(10, int(width / 1.2) + 1))
    for index in range(post_count):
        x = -width / 2.0 + (width / max(post_count - 1, 1)) * index
        parts.append(add_prism(post_width, thickness, height, (x, 0.0, height / 2.0), f"FencePost_{index}", material=accent_material, bevel=0.002))

    parts.extend([
        add_prism(width, thickness * 0.5, rail_height, (0.0, 0.0, height * 0.68), "FenceRailUpper", material=accent_material, bevel=0.002),
        add_prism(width, thickness * 0.5, rail_height, (0.0, 0.0, height * 0.34), "FenceRailLower", material=accent_material, bevel=0.002),
    ])

    if fence_style == "panel":
        panel_height = height * 0.72
        parts.append(add_prism(width - post_width * 1.6, thickness * 0.55, panel_height, (0.0, 0.0, panel_height / 2.0 + height * 0.08), "FencePanel", material=main_material, bevel=0.003))
    else:
        slat_count = max(3, min(24, section_count))
        slat_width = min(max(width / (slat_count * 1.5), 0.03), 0.1)
        clear_width = width - post_width * 2.0
        for index in range(slat_count):
            x = -clear_width / 2.0 + (clear_width / max(slat_count - 1, 1)) * index
            slat_height = height * (0.82 if index % 2 == 0 else 0.76)
            parts.append(add_prism(slat_width, thickness * 0.36, slat_height, (x, 0.0, slat_height / 2.0), f"FenceSlat_{index}", material=main_material, bevel=0.002))

    return join_parts(parts, "FenceAsset")


def generate_railing(params, mats, rng):
    width = cm(params.get("width", 280.0))
    height = cm(params.get("height", 105.0))
    depth = cm(params.get("depth", 14.0))
    material_key = params.get("material", "steel")
    baluster_count = int(params.get("baluster_count", 8))
    main_material = mats["steel"] if material_key == "steel" else mats["wood"]
    accent_material = mats["aluminum"] if material_key == "steel" else mats["trim"]
    parts = []

    post_width = max(depth * 0.28, 0.03)
    rail_width = max(depth * 0.22, 0.025)
    end_x = width / 2.0 - post_width / 2.0
    parts.extend([
        add_prism(post_width, depth, height, (-end_x, 0.0, height / 2.0), "RailingPostLeft", material=main_material, bevel=0.002),
        add_prism(post_width, depth, height, (end_x, 0.0, height / 2.0), "RailingPostRight", material=main_material, bevel=0.002),
        add_prism(width, depth, rail_width, (0.0, 0.0, height), "RailingTopRail", material=accent_material, bevel=0.002),
    ])

    clear_width = width - post_width * 2.0
    for index in range(max(3, min(24, baluster_count))):
        x = -clear_width / 2.0 + (clear_width / max(baluster_count - 1, 1)) * index
        parts.append(add_prism(post_width * 0.6, depth * 0.65, height * 0.74, (x, 0.0, height * 0.37), f"RailingBaluster_{index}", material=main_material, bevel=0.001))

    return join_parts(parts, "RailingAsset")


def generate_chimney(params, mats, rng):
    width = cm(params.get("width", 90.0))
    depth = cm(params.get("depth", 90.0))
    height = cm(params.get("height", 240.0))
    material_key = params.get("material", "brick")
    has_cap = bool(params.get("has_cap", True))
    main_material = material_for(material_key, mats)
    parts = [add_prism(width, depth, height, (0.0, 0.0, height / 2.0), "ChimneyShaft", material=main_material, bevel=0.005)]

    flue_width = width * 0.42
    flue_depth = depth * 0.42
    parts.append(add_prism(flue_width, flue_depth, max(height * 0.04, 0.05), (0.0, 0.0, height + max(height * 0.02, 0.02)), "ChimneyFlueShadow", material=mats["shadow"], bevel=0.002))

    if has_cap:
        cap_overhang = max(width * 0.12, 0.04)
        cap_height = max(height * 0.07, 0.08)
        parts.append(add_prism(width + cap_overhang * 2.0, depth + cap_overhang * 2.0, cap_height, (0.0, 0.0, height + cap_height / 2.0), "ChimneyCap", material=mats["trim"], bevel=0.003))
        parts.append(add_prism(flue_width, flue_depth, cap_height * 0.4, (0.0, 0.0, height + cap_height * 0.2), "ChimneyFlue", material=mats["shadow"], bevel=0.001))

    return join_parts(parts, "ChimneyAsset")


def generate_porch(params, mats, rng):
    width = cm(params.get("width", 360.0))
    depth = cm(params.get("depth", 220.0))
    height = cm(params.get("height", 260.0))
    material_key = params.get("material", "wood")
    pillar_count = int(params.get("pillar_count", 4))
    has_steps = bool(params.get("has_steps", True))
    main_material = material_for(material_key, mats)
    pillar_material = mats["trim"] if material_key == "wood" else mats["stone"]
    roof_material = mats["wood_shingles"] if material_key == "wood" else mats["concrete"]
    parts = []

    platform_height = max(height * 0.08, 0.16)
    parts.append(add_prism(width, depth, platform_height, (0.0, 0.0, platform_height / 2.0), "PorchPlatform", material=main_material, bevel=0.004))
    skirt_height = max(platform_height * 0.55, 0.08)
    parts.append(add_prism(width * 0.98, depth * 0.08, skirt_height, (0.0, depth / 2.0 - depth * 0.04, skirt_height / 2.0), "PorchFrontSkirt", material=pillar_material, bevel=0.002))

    board_count = max(3, min(8, int(width / 0.55)))
    board_width = width / board_count
    for index in range(board_count - 1):
        x = -width / 2.0 + board_width * (index + 1)
        parts.append(add_prism(board_width * 0.04, depth * 0.94, platform_height * 0.1, (x, 0.0, platform_height + platform_height * 0.05), f"PorchBoardGap_{index}", material=mats["shadow"], bevel=0.001))

    roof_thickness = max(height * 0.06, 0.12)
    porch_slope = math.radians(18.0)
    roof_span = width * 0.56
    roof_panel_length = roof_span / max(math.cos(porch_slope), 0.06)
    roof_rise = math.tan(porch_slope) * roof_span
    roof_z = height + roof_rise / 2.0 + roof_thickness / 2.0
    parts.append(add_prism(roof_panel_length, depth * 1.08, roof_thickness, (-roof_span / 2.0, 0.0, roof_z), "PorchRoofLeft", material=roof_material, rotation=(0.0, porch_slope, 0.0), bevel=0.004))
    parts.append(add_prism(roof_panel_length, depth * 1.08, roof_thickness, (roof_span / 2.0, 0.0, roof_z), "PorchRoofRight", material=roof_material, rotation=(0.0, -porch_slope, 0.0), bevel=0.004))
    parts.append(add_prism(max(width * 0.04, 0.08), depth * 1.02, roof_thickness * 0.75, (0.0, 0.0, height + roof_rise + roof_thickness * 0.4), "PorchRoofRidge", material=mats["trim"], bevel=0.002))

    usable_front = width - max(width * 0.12, 0.3)
    pillar_width = min(max(width * 0.05, 0.08), 0.18)
    front_y = depth / 2.0 - pillar_width / 2.0
    back_y = -depth / 2.0 + pillar_width / 2.0
    columns_per_row = max(1, min(3, math.ceil(pillar_count / 2)))
    front_positions = []
    for index in range(columns_per_row):
        x = 0.0 if columns_per_row == 1 else -usable_front / 2.0 + (usable_front / max(columns_per_row - 1, 1)) * index
        front_positions.append(x)
        parts.append(add_prism(pillar_width, pillar_width, height, (x, front_y, height / 2.0), f"PorchFrontPillar_{index}", material=pillar_material, bevel=0.003))

    remaining = max(0, pillar_count - columns_per_row)
    back_count = min(columns_per_row, remaining)
    for index in range(back_count):
        x = front_positions[index]
        parts.append(add_prism(pillar_width, pillar_width, height, (x, back_y, height / 2.0), f"PorchBackPillar_{index}", material=pillar_material, bevel=0.003))

    parts.append(add_prism(width, pillar_width * 0.7, pillar_width * 0.7, (0.0, front_y, height - pillar_width * 0.2), "PorchFrontBeam", material=pillar_material, bevel=0.002))
    parts.append(add_prism(width, pillar_width * 0.6, pillar_width * 0.6, (0.0, back_y, height - pillar_width * 0.2), "PorchBackBeam", material=pillar_material, bevel=0.002))
    parts.append(add_prism(pillar_width * 0.6, depth, pillar_width * 0.55, (-width / 2.0 + pillar_width * 0.6, 0.0, height - pillar_width * 0.24), "PorchSideBeamLeft", material=pillar_material, bevel=0.002))
    parts.append(add_prism(pillar_width * 0.6, depth, pillar_width * 0.55, (width / 2.0 - pillar_width * 0.6, 0.0, height - pillar_width * 0.24), "PorchSideBeamRight", material=pillar_material, bevel=0.002))

    if has_steps:
        step_count = 3
        step_depth = depth * 0.18
        for step_index in range(step_count):
            step_height = platform_height * ((step_index + 1) / step_count)
            y = depth / 2.0 + step_depth * (step_count - step_index - 0.5)
            step_width = width * (0.46 + step_index * 0.08)
            parts.append(add_prism(step_width, step_depth, step_height, (0.0, y, step_height / 2.0), f"PorchStep_{step_index}", material=main_material, bevel=0.002))
        rail_post_width = pillar_width * 0.42
        rail_height = max(height * 0.28, 0.85)
        for side in (-1, 1):
            x = side * width * 0.22
            parts.append(add_prism(rail_post_width, rail_post_width, rail_height, (x, depth / 2.0 + step_depth * 1.1, rail_height / 2.0), f"PorchRailPostFront_{side}", material=pillar_material, bevel=0.002))
            parts.append(add_prism(rail_post_width, rail_post_width, rail_height * 0.78, (x, front_y - step_depth * 0.1, platform_height + rail_height * 0.39), f"PorchRailPostTop_{side}", material=pillar_material, bevel=0.002))
            rail_length = math.sqrt((step_depth * 1.7) ** 2 + platform_height ** 2)
            rail_angle = math.atan2(platform_height, step_depth * 1.7)
            parts.append(add_prism(rail_post_width * 1.1, rail_length, rail_post_width * 0.9, (x, depth / 2.0 + step_depth * 0.35, platform_height * 0.72 + rail_height * 0.16), f"PorchStepRail_{side}", material=pillar_material, rotation=(rail_angle, 0.0, 0.0), bevel=0.002))

    return join_parts(parts, "PorchAsset")


GENERATORS = {
    "wall": generate_wall,
    "floor": generate_floor,
    "ceiling": generate_ceiling,
    "roof": generate_roof,
    "pillar": generate_pillar,
    "beam": generate_beam,
    "foundation": generate_foundation,
    "door": generate_door,
    "window": generate_window,
    "archway": generate_archway,
    "gate": generate_gate,
    "stairs": generate_stairs,
    "ladder": generate_ladder,
    "ramp": generate_ramp,
    "bridge": generate_bridge,
    "balcony": generate_balcony,
    "fence": generate_fence,
    "railing": generate_railing,
    "chimney": generate_chimney,
    "porch": generate_porch,
}


def generate_architecture_asset(params):
    asset_type = params.get("asset_type")
    if asset_type not in GENERATORS:
        raise ValueError(f"Unsupported architecture asset type: {asset_type}")
    rng = random.Random(seed_for(asset_type, params))
    mats = build_materials()
    return GENERATORS[asset_type](params, mats, rng)


def main():
    parser = argparse.ArgumentParser(description="Procedural Architecture Asset Generator")
    parser.add_argument("--params", type=str, required=True, help="Path to JSON parameter file")
    parser.add_argument("--export", type=str, required=True, help="Path to export GLB")
    parser.add_argument("--render", type=str, help="Path to render preview PNG")

    try:
        args_idx = sys.argv.index("--")
        script_args = sys.argv[args_idx + 1:]
    except ValueError:
        script_args = []

    args = parser.parse_args(script_args)

    with open(args.params, "r") as fh:
        params = json.load(fh)

    utils.cleanup_scene()
    asset_obj = generate_architecture_asset(params)

    if args.render:
        utils.setup_lighting_and_camera(asset_obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)


if __name__ == "__main__":
    main()
