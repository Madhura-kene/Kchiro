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
    import mathutils
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
        "bark": utils.create_material("NatureBark", diffuse_color=(0.36, 0.23, 0.13, 1.0), roughness=0.9),
        "dark_bark": utils.create_material("NatureDarkBark", diffuse_color=(0.2, 0.16, 0.13, 1.0), roughness=0.95),
        "birch": utils.create_material("BirchBark", diffuse_color=(0.92, 0.92, 0.89, 1.0), roughness=0.8),
        "leaf_oak": utils.create_material("OakLeaf", diffuse_color=(0.16, 0.42, 0.16, 1.0), roughness=0.7),
        "leaf_pine": utils.create_material("PineLeaf", diffuse_color=(0.08, 0.28, 0.1, 1.0), roughness=0.85),
        "leaf_light": utils.create_material("LightLeaf", diffuse_color=(0.44, 0.72, 0.36, 1.0), roughness=0.65),
        "leaf_palm": utils.create_material("PalmLeaf", diffuse_color=(0.2, 0.55, 0.2, 1.0), roughness=0.7),
        "stem": utils.create_material("NatureStem", diffuse_color=(0.28, 0.52, 0.18, 1.0), roughness=0.7),
        "petal_pink": utils.create_material("FlowerPetalPink", diffuse_color=(0.94, 0.42, 0.64, 1.0), roughness=0.45),
        "petal_yellow": utils.create_material("FlowerPetalYellow", diffuse_color=(0.94, 0.82, 0.18, 1.0), roughness=0.45),
        "flower_center": utils.create_material("FlowerCenter", diffuse_color=(0.45, 0.26, 0.08, 1.0), roughness=0.75),
        "mushroom_cap": utils.create_material("MushroomCap", diffuse_color=(0.76, 0.14, 0.12, 1.0), roughness=0.5),
        "mushroom_spot": utils.create_material("MushroomSpot", diffuse_color=(0.94, 0.93, 0.88, 1.0), roughness=0.55),
        "mushroom_stem": utils.create_material("MushroomStem", diffuse_color=(0.86, 0.82, 0.72, 1.0), roughness=0.75),
        "rock": utils.create_material("NatureRock", diffuse_color=(0.42, 0.44, 0.46, 1.0), roughness=0.98),
        "rock_dark": utils.create_material("NatureRockDark", diffuse_color=(0.28, 0.3, 0.32, 1.0), roughness=1.0),
        "moss": utils.create_material("NatureMoss", diffuse_color=(0.18, 0.42, 0.14, 1.0), roughness=0.95),
        "soil": utils.create_material("NatureSoil", diffuse_color=(0.2, 0.13, 0.08, 1.0), roughness=1.0),
        "sand": utils.create_material("NatureSand", diffuse_color=(0.56, 0.49, 0.34, 1.0), roughness=1.0),
        "water": utils.create_material("NatureWater", diffuse_color=(0.16, 0.42, 0.64, 1.0), metallic=0.0, roughness=0.08),
        "foam": utils.create_material("NatureFoam", diffuse_color=(0.86, 0.92, 0.97, 1.0), roughness=0.2),
    }


def add_cube(size, location, name, material=None, rotation=(0.0, 0.0, 0.0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel > 0:
        utils.apply_bevel(obj, width=bevel)
    if material:
        utils.apply_material(obj, material)
    return obj


def add_uv_sphere(radius, location, name, material=None, scale=(1.0, 1.0, 1.0), smooth=True):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=radius, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    if smooth:
        utils.apply_smooth_by_angle(obj)
    if material:
        utils.apply_material(obj, material)
    return obj


def add_ico_sphere(radius, location, name, material=None, scale=(1.0, 1.0, 1.0)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=radius, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_smooth_by_angle(obj)
    if material:
        utils.apply_material(obj, material)
    return obj


def add_cylinder(radius, depth, location, name, material=None, rotation=(0.0, 0.0, 0.0), vertices=16):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=vertices, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    utils.apply_smooth_by_angle(obj)
    if material:
        utils.apply_material(obj, material)
    return obj


def add_tapered_cylinder(radius_bottom, radius_top, depth, location, name, material=None, rotation=(0.0, 0.0, 0.0), vertices=16):
    bpy.ops.mesh.primitive_cone_add(
        radius1=radius_bottom,
        radius2=radius_top,
        depth=depth,
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


def cylinder_between(start, end, radius_start, radius_end, name, material=None, vertices=12):
    start_vec = mathutils.Vector(start)
    end_vec = mathutils.Vector(end)
    direction = end_vec - start_vec
    depth = max(direction.length, 0.01)
    mid = (start_vec + end_vec) / 2.0
    bpy.ops.mesh.primitive_cone_add(
        radius1=max(radius_start, 0.002),
        radius2=max(radius_end, 0.001),
        depth=depth,
        vertices=vertices,
        location=mid,
    )
    obj = bpy.context.active_object
    obj.name = name
    quat = direction.normalized().to_track_quat("Z", "Y")
    obj.rotation_euler = quat.to_euler()
    bpy.ops.object.transform_apply(rotation=True)
    utils.apply_smooth_by_angle(obj)
    if material:
        utils.apply_material(obj, material)
    return obj


def deform_rock(obj, rng, amount_xy=0.22, amount_z=0.18):
    for vert in obj.data.vertices:
        scale_xy = 1.0 + rng.uniform(-amount_xy, amount_xy)
        scale_z = 1.0 + rng.uniform(-amount_z, amount_z)
        vert.co.x *= scale_xy
        vert.co.y *= scale_xy
        vert.co.z *= scale_z


def add_canopy_blob(center, radius, material, name, rng, squash=1.0):
    obj = add_ico_sphere(radius, center, name, material=material, scale=(
        1.0 + rng.uniform(-0.18, 0.18),
        1.0 + rng.uniform(-0.18, 0.18),
        squash + rng.uniform(-0.08, 0.12),
    ))
    deform_rock(obj, rng, amount_xy=0.08, amount_z=0.08)
    return obj


def add_rock_blob(center, radius, scale, material, name, rng, deform_xy=0.22, deform_z=0.18):
    rock = add_ico_sphere(radius, center, name, material=material, scale=scale)
    deform_rock(rock, rng, amount_xy=deform_xy, amount_z=deform_z)
    return rock


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


def generate_oak_tree(params, mats, rng):
    height = cm(params.get("height", 540.0))
    canopy_width = cm(params.get("canopy_width", 420.0))
    trunk_radius = cm(params.get("trunk_radius", 22.0))
    parts = [
        add_tapered_cylinder(
            trunk_radius * 1.18,
            trunk_radius * 0.75,
            height * 0.62,
            (0.0, 0.0, height * 0.31),
            "OakTrunk",
            material=mats["bark"],
        )
    ]

    branch_base_z = height * 0.48
    for index, angle in enumerate((0.2, 1.6, 3.2, 4.8)):
        start = (0.0, 0.0, branch_base_z + index * height * 0.025)
        end = (
            math.cos(angle) * canopy_width * 0.22,
            math.sin(angle) * canopy_width * 0.22,
            height * (0.68 + 0.04 * rng.random()),
        )
        parts.append(cylinder_between(start, end, trunk_radius * 0.34, trunk_radius * 0.12, f"OakBranch_{index}", material=mats["bark"]))

    canopy_points = [
        (0.0, 0.0, height * 0.8),
        (-canopy_width * 0.16, canopy_width * 0.1, height * 0.77),
        (canopy_width * 0.18, canopy_width * 0.04, height * 0.79),
        (-canopy_width * 0.08, -canopy_width * 0.18, height * 0.76),
        (canopy_width * 0.1, -canopy_width * 0.16, height * 0.81),
        (0.0, canopy_width * 0.2, height * 0.82),
    ]
    for index, point in enumerate(canopy_points):
        parts.append(add_canopy_blob(point, canopy_width * (0.16 + rng.uniform(-0.02, 0.04)), mats["leaf_oak"], f"OakCanopy_{index}", rng))

    return join_parts(parts, "OakTreeAsset")


def generate_pine_tree(params, mats, rng):
    height = cm(params.get("height", 680.0))
    canopy_width = cm(params.get("canopy_width", 260.0))
    trunk_radius = cm(params.get("trunk_radius", 16.0))
    layers = int(params.get("layers", 5))
    parts = [
        add_tapered_cylinder(
            trunk_radius * 1.1,
            trunk_radius * 0.55,
            height * 0.82,
            (0.0, 0.0, height * 0.41),
            "PineTrunk",
            material=mats["bark"],
        )
    ]
    for index in range(max(3, layers)):
        factor = index / max(layers - 1, 1)
        layer_width = canopy_width * (1.0 - factor * 0.65)
        layer_depth = height * 0.18
        z = height * (0.26 + factor * 0.16)
        parts.append(
            add_tapered_cylinder(
                layer_width * 0.55,
                0.02,
                layer_depth,
                (0.0, 0.0, z),
                f"PineLayer_{index}",
                material=mats["leaf_pine"],
                vertices=18,
            )
        )
    parts.append(
        add_tapered_cylinder(
            canopy_width * 0.18,
            0.0,
            height * 0.16,
            (0.0, 0.0, height * 0.88),
            "PineTop",
            material=mats["leaf_pine"],
            vertices=16,
        )
    )
    return join_parts(parts, "PineTreeAsset")


def generate_birch_tree(params, mats, rng):
    height = cm(params.get("height", 560.0))
    canopy_width = cm(params.get("canopy_width", 280.0))
    trunk_radius = cm(params.get("trunk_radius", 12.0))
    parts = [
        add_tapered_cylinder(
            trunk_radius * 1.08,
            trunk_radius * 0.52,
            height * 0.72,
            (0.0, 0.0, height * 0.36),
            "BirchTrunk",
            material=mats["birch"],
        )
    ]
    for index in range(6):
        stripe_z = height * (0.12 + index * 0.1)
        parts.append(
            add_cube(
                (trunk_radius * 1.9, trunk_radius * 1.45, 0.01),
                (0.0, 0.0, stripe_z),
                f"BirchStripe_{index}",
                material=mats["dark_bark"],
                rotation=(0.0, 0.0, rng.uniform(-0.35, 0.35)),
            )
        )
    for index, angle in enumerate((0.0, 2.15, 4.2)):
        start = (0.0, 0.0, height * (0.48 + index * 0.05))
        end = (
            math.cos(angle) * canopy_width * 0.16,
            math.sin(angle) * canopy_width * 0.16,
            height * (0.64 + 0.04 * index),
        )
        parts.append(cylinder_between(start, end, trunk_radius * 0.22, trunk_radius * 0.08, f"BirchBranch_{index}", material=mats["birch"]))
    for index, point in enumerate((
        (0.0, 0.0, height * 0.78),
        (canopy_width * 0.12, 0.0, height * 0.76),
        (-canopy_width * 0.1, canopy_width * 0.06, height * 0.74),
        (0.05, -canopy_width * 0.1, height * 0.8),
    )):
        parts.append(add_canopy_blob(point, canopy_width * 0.13, mats["leaf_light"], f"BirchCanopy_{index}", rng, squash=1.15))
    return join_parts(parts, "BirchTreeAsset")


def generate_palm_tree(params, mats, rng):
    height = cm(params.get("height", 620.0))
    frond_span = cm(params.get("frond_span", 260.0))
    trunk_radius = cm(params.get("trunk_radius", 14.0))
    segments = 7
    parts = []
    points = []
    for index in range(segments + 1):
        t = index / segments
        points.append((math.sin(t * 1.2) * height * 0.08, 0.0, height * t))
    for index in range(segments):
        start = points[index]
        end = points[index + 1]
        parts.append(
            cylinder_between(
                start,
                end,
                trunk_radius * (1.08 - index * 0.06),
                trunk_radius * (0.98 - index * 0.06),
                f"PalmSegment_{index}",
                material=mats["bark"],
                vertices=14,
            )
        )
    crown = mathutils.Vector(points[-1])
    parts.append(add_uv_sphere(trunk_radius * 0.9, crown, "PalmCrown", material=mats["bark"], scale=(1.0, 1.0, 0.8)))
    for index in range(7):
        angle = (math.tau / 7.0) * index
        length = frond_span * (0.42 + rng.uniform(-0.04, 0.07))
        frond = add_cube(
            (0.02, length, 0.01),
            (
                crown.x + math.cos(angle) * length * 0.28,
                crown.y + math.sin(angle) * length * 0.28,
                crown.z + rng.uniform(-0.03, 0.04),
            ),
            f"PalmFrond_{index}",
            material=mats["leaf_palm"],
            rotation=(math.radians(68), 0.0, angle),
        )
        parts.append(frond)
    return join_parts(parts, "PalmTreeAsset")


def generate_dead_tree(params, mats, rng):
    height = cm(params.get("height", 520.0))
    branch_count = int(params.get("branch_count", 7))
    trunk_radius = cm(params.get("trunk_radius", 16.0))
    parts = [
        add_tapered_cylinder(
            trunk_radius * 1.15,
            trunk_radius * 0.45,
            height * 0.78,
            (0.0, 0.0, height * 0.39),
            "DeadTrunk",
            material=mats["dark_bark"],
        )
    ]
    for index in range(max(4, branch_count)):
        angle = (math.tau / max(branch_count, 1)) * index + rng.uniform(-0.2, 0.2)
        start = (0.0, 0.0, height * (0.4 + 0.05 * (index % 4)))
        end = (
            math.cos(angle) * height * (0.12 + rng.uniform(0.02, 0.08)),
            math.sin(angle) * height * (0.12 + rng.uniform(0.02, 0.08)),
            height * (0.66 + rng.uniform(-0.02, 0.12)),
        )
        parts.append(cylinder_between(start, end, trunk_radius * 0.26, trunk_radius * 0.03, f"DeadBranch_{index}", material=mats["dark_bark"]))
    return join_parts(parts, "DeadTreeAsset")


def generate_sapling(params, mats, rng):
    height = cm(params.get("height", 180.0))
    canopy_width = cm(params.get("canopy_width", 90.0))
    parts = [
        add_tapered_cylinder(0.018, 0.01, height * 0.82, (0.0, 0.0, height * 0.41), "SaplingTrunk", material=mats["bark"])
    ]
    top = height * 0.68
    for index, angle in enumerate((0.6, 2.4, 4.5)):
        start = (0.0, 0.0, top - 0.03 * index)
        end = (
            math.cos(angle) * canopy_width * 0.18,
            math.sin(angle) * canopy_width * 0.18,
            top + canopy_width * 0.06,
        )
        parts.append(cylinder_between(start, end, 0.008, 0.004, f"SaplingBranch_{index}", material=mats["bark"]))
    for index, point in enumerate((
        (0.0, 0.0, height * 0.86),
        (canopy_width * 0.09, 0.0, height * 0.76),
        (-canopy_width * 0.08, canopy_width * 0.04, height * 0.72),
    )):
        parts.append(add_canopy_blob(point, canopy_width * 0.12, mats["leaf_light"], f"SaplingLeaves_{index}", rng))
    return join_parts(parts, "SaplingAsset")


def generate_grass(params, mats, rng):
    width = cm(params.get("width", 110.0))
    height = cm(params.get("height", 34.0))
    density = int(params.get("density", 28))
    parts = []
    clump_radius = width * 0.32
    for index in range(max(12, density)):
        angle = rng.uniform(0.0, math.tau)
        dist = rng.uniform(0.0, clump_radius)
        x = math.cos(angle) * dist
        y = math.sin(angle) * dist
        blade_height = height * rng.uniform(0.7, 1.2)
        blade = add_cube(
            (0.01, 0.03, blade_height),
            (x, y, blade_height / 2.0),
            f"GrassBlade_{index}",
            material=mats["leaf_light"],
            rotation=(rng.uniform(-0.4, 0.4), rng.uniform(-0.25, 0.25), angle),
        )
        parts.append(blade)
    return join_parts(parts, "GrassAsset")


def generate_bush(params, mats, rng):
    width = cm(params.get("width", 160.0))
    height = cm(params.get("height", 95.0))
    density = int(params.get("density", 8))
    parts = []
    for index in range(max(5, density)):
        x = rng.uniform(-width * 0.18, width * 0.18)
        y = rng.uniform(-width * 0.18, width * 0.18)
        z = height * rng.uniform(0.28, 0.7)
        radius = width * rng.uniform(0.12, 0.18)
        parts.append(add_canopy_blob((x, y, z), radius, mats["leaf_oak"], f"BushBlob_{index}", rng, squash=0.92))
    for index in range(4):
        parts.append(cylinder_between((0.0, 0.0, 0.02), (rng.uniform(-0.08, 0.08), rng.uniform(-0.08, 0.08), height * 0.25), 0.02, 0.01, f"BushStem_{index}", material=mats["bark"]))
    return join_parts(parts, "BushAsset")


def generate_shrub(params, mats, rng):
    width = cm(params.get("width", 150.0))
    height = cm(params.get("height", 130.0))
    stems = int(params.get("stems", 5))
    parts = []
    for index in range(max(3, stems)):
        angle = (math.tau / max(stems, 1)) * index
        end = (math.cos(angle) * width * 0.12, math.sin(angle) * width * 0.12, height * rng.uniform(0.45, 0.7))
        parts.append(cylinder_between((0.0, 0.0, 0.02), end, 0.026, 0.01, f"ShrubStem_{index}", material=mats["bark"]))
    for index in range(max(6, stems + 2)):
        point = (
            rng.uniform(-width * 0.2, width * 0.2),
            rng.uniform(-width * 0.2, width * 0.2),
            height * rng.uniform(0.35, 0.82),
        )
        parts.append(add_canopy_blob(point, width * rng.uniform(0.09, 0.14), mats["leaf_light"], f"ShrubBlob_{index}", rng, squash=1.1))
    return join_parts(parts, "ShrubAsset")


def generate_fern(params, mats, rng):
    width = cm(params.get("width", 120.0))
    height = cm(params.get("height", 75.0))
    fronds = int(params.get("fronds", 6))
    parts = []
    for index in range(max(4, fronds)):
        angle = (math.tau / max(fronds, 1)) * index
        length = width * rng.uniform(0.28, 0.42)
        end = (
            math.cos(angle) * length,
            math.sin(angle) * length,
            height * rng.uniform(0.5, 0.85),
        )
        parts.append(cylinder_between((0.0, 0.0, 0.02), end, 0.015, 0.005, f"FernFrond_{index}", material=mats["stem"]))
        for leaf_index in range(6):
            t = (leaf_index + 1) / 7.0
            base = mathutils.Vector((0.0, 0.0, 0.02)).lerp(mathutils.Vector(end), t)
            side = 1 if leaf_index % 2 == 0 else -1
            offset = mathutils.Vector((math.cos(angle + math.pi / 2.0) * side * width * 0.06, math.sin(angle + math.pi / 2.0) * side * width * 0.06, 0.0))
            leaflet = add_cube(
                (0.015, width * 0.08 * (1.0 - t * 0.3), 0.008),
                tuple(base + offset),
                f"FernLeaf_{index}_{leaf_index}",
                material=mats["leaf_light"],
                rotation=(math.radians(55), 0.0, angle),
            )
            parts.append(leaflet)
    return join_parts(parts, "FernAsset")


def generate_flower(params, mats, rng):
    height = cm(params.get("height", 45.0))
    petals = int(params.get("petals", 6))
    bloom_color = params.get("bloom_color", "pink")
    petal_mat = mats["petal_yellow"] if bloom_color == "yellow" else mats["petal_pink"]
    parts = [
        add_cylinder(0.01, height, (0.0, 0.0, height / 2.0), "FlowerStem", material=mats["stem"], vertices=10)
    ]
    parts.append(add_cube((0.01, 0.09, 0.01), (0.05, 0.0, height * 0.42), "FlowerLeafA", material=mats["leaf_light"], rotation=(math.radians(25), 0.0, 0.6)))
    parts.append(add_cube((0.01, 0.08, 0.01), (-0.05, 0.0, height * 0.55), "FlowerLeafB", material=mats["leaf_light"], rotation=(math.radians(-20), 0.0, -0.8)))
    center = (0.0, 0.0, height)
    parts.append(add_uv_sphere(0.03, center, "FlowerCenter", material=mats["flower_center"]))
    for index in range(max(5, petals)):
        angle = (math.tau / max(petals, 1)) * index
        parts.append(
            add_uv_sphere(
                0.035,
                (math.cos(angle) * 0.055, math.sin(angle) * 0.055, height),
                f"FlowerPetal_{index}",
                material=petal_mat,
                scale=(1.2, 0.8, 0.35),
            )
        )
    return join_parts(parts, "FlowerAsset")


def generate_moss(params, mats, rng):
    width = cm(params.get("width", 130.0))
    depth = cm(params.get("depth", 100.0))
    thickness = cm(params.get("thickness", 18.0))
    parts = [add_cube((width * 0.45, depth * 0.45, 0.02), (0.0, 0.0, 0.01), "MossBase", material=mats["soil"])]
    for index in range(8):
        parts.append(
            add_uv_sphere(
                width * rng.uniform(0.06, 0.11),
                (
                    rng.uniform(-width * 0.24, width * 0.24),
                    rng.uniform(-depth * 0.24, depth * 0.24),
                    thickness * rng.uniform(0.35, 0.7),
                ),
                f"MossLump_{index}",
                material=mats["moss"],
                scale=(1.0, 1.0, 0.45),
            )
        )
    return join_parts(parts, "MossAsset")


def generate_small_rock(params, mats, rng):
    width = cm(params.get("width", 55.0))
    depth = cm(params.get("depth", 45.0))
    height = cm(params.get("height", 32.0))
    rock = add_ico_sphere(0.3, (0.0, 0.0, height * 0.5), "SmallRock", material=mats["rock"], scale=(width, depth, height))
    deform_rock(rock, rng)
    return join_parts([rock], "SmallRockAsset")


def generate_boulder(params, mats, rng):
    width = cm(params.get("width", 180.0))
    depth = cm(params.get("depth", 140.0))
    height = cm(params.get("height", 120.0))
    parts = []
    for index, point in enumerate(((0.0, 0.0, height * 0.45), (-0.24, 0.08, height * 0.32), (0.22, -0.12, height * 0.35))):
        rock = add_ico_sphere(
            0.35 if index == 0 else 0.24,
            point,
            f"BoulderPart_{index}",
            material=mats["rock_dark" if index == 0 else "rock"],
            scale=(width * (0.7 if index == 0 else 0.4), depth * (0.7 if index == 0 else 0.36), height * (0.8 if index == 0 else 0.42)),
        )
        deform_rock(rock, rng)
        parts.append(rock)
    return join_parts(parts, "BoulderAsset")


def generate_rock_cluster(params, mats, rng):
    width = cm(params.get("width", 180.0))
    depth = cm(params.get("depth", 120.0))
    rocks = int(params.get("rocks", 5))
    cluster_height = max(min(width, depth) * 0.42, 0.34)
    parts = [
        add_uv_sphere(
            0.24,
            (0.0, 0.0, cluster_height * 0.08),
            "ClusterBase",
            material=mats["soil"],
            scale=(width * 0.48, depth * 0.38, cluster_height * 0.2),
            smooth=False,
        )
    ]

    layout = [
        (-width * 0.18, depth * 0.06, cluster_height * 0.28, 0.34, (width * 0.34, depth * 0.22, cluster_height * 0.7), mats["rock_dark"]),
        (width * 0.16, -depth * 0.08, cluster_height * 0.24, 0.28, (width * 0.28, depth * 0.24, cluster_height * 0.54), mats["rock"]),
        (0.0, depth * 0.12, cluster_height * 0.18, 0.22, (width * 0.2, depth * 0.16, cluster_height * 0.42), mats["rock"]),
        (-width * 0.02, -depth * 0.2, cluster_height * 0.12, 0.18, (width * 0.16, depth * 0.14, cluster_height * 0.28), mats["rock_dark"]),
    ]
    pebble_count = max(0, rocks - len(layout))
    for index, (x, y, z, radius, scale, material) in enumerate(layout[: max(3, min(rocks, len(layout)))]):
        parts.append(add_rock_blob((x, y, z), radius, scale, material, f"ClusterRock_{index}", rng))

    for pebble_index in range(pebble_count + 2):
        radius = rng.uniform(0.08, 0.14)
        x = rng.uniform(-width * 0.26, width * 0.26)
        y = rng.uniform(-depth * 0.24, depth * 0.24)
        scale = (
            width * rng.uniform(0.08, 0.14),
            depth * rng.uniform(0.07, 0.12),
            cluster_height * rng.uniform(0.12, 0.2),
        )
        parts.append(
            add_rock_blob(
                (x, y, cluster_height * rng.uniform(0.06, 0.12)),
                radius,
                scale,
                mats["rock" if pebble_index % 2 == 0 else "rock_dark"],
                f"ClusterPebble_{pebble_index}",
                rng,
                deform_xy=0.18,
                deform_z=0.14,
            )
        )

    moss_patch_count = 2 if max(rocks, 3) >= 4 else 1
    for moss_index in range(moss_patch_count):
        parts.append(
            add_uv_sphere(
                0.08,
                (
                    (-1 if moss_index == 0 else 1) * width * 0.1,
                    depth * (0.04 if moss_index == 0 else -0.1),
                    cluster_height * 0.12,
                ),
                f"ClusterMoss_{moss_index}",
                material=mats["moss"],
                scale=(width * 0.12, depth * 0.08, cluster_height * 0.08),
            )
        )
    return join_parts(parts, "RockClusterAsset")


def generate_cliff_section(params, mats, rng):
    width = cm(params.get("width", 280.0))
    depth = cm(params.get("depth", 140.0))
    height = cm(params.get("height", 300.0))
    parts = [
        add_cube((width * 0.5, depth * 0.28, height * 0.5), (0.0, 0.0, height * 0.5), "CliffMain", material=mats["rock_dark"], bevel=0.01),
        add_cube((width * 0.42, depth * 0.18, height * 0.14), (-width * 0.06, depth * 0.18, height * 0.42), "CliffLedgeA", material=mats["rock"], bevel=0.008),
        add_cube((width * 0.3, depth * 0.16, height * 0.12), (width * 0.12, depth * 0.16, height * 0.7), "CliffLedgeB", material=mats["rock"], bevel=0.008),
    ]
    for index in range(4):
        parts.append(
            add_cube(
                (0.03, depth * 0.14, height * 0.12),
                (rng.uniform(-width * 0.3, width * 0.3), depth * 0.28, height * (0.18 + index * 0.18)),
                f"CliffCrack_{index}",
                material=mats["rock_dark"],
            )
        )
    return join_parts(parts, "CliffSectionAsset")


def generate_log(params, mats, rng):
    length = cm(params.get("length", 220.0))
    radius = cm(params.get("radius", 24.0))
    parts = [
        add_cylinder(radius, length, (0.0, 0.0, radius), "LogBody", material=mats["bark"], rotation=(math.pi / 2.0, 0.0, 0.0)),
        add_cylinder(radius * 0.92, 0.02, (0.0, -length / 2.0, radius), "LogEndA", material=mats["sand"], rotation=(math.pi / 2.0, 0.0, 0.0)),
        add_cylinder(radius * 0.92, 0.02, (0.0, length / 2.0, radius), "LogEndB", material=mats["sand"], rotation=(math.pi / 2.0, 0.0, 0.0)),
    ]
    parts.append(cylinder_between((0.0, 0.0, radius * 1.2), (radius * 0.8, length * 0.15, radius * 1.85), radius * 0.18, radius * 0.06, "LogBranchNub", material=mats["bark"]))
    return join_parts(parts, "LogAsset")


def generate_tree_stump(params, mats, rng):
    radius = cm(params.get("radius", 38.0))
    height = cm(params.get("height", 48.0))
    parts = [
        add_cylinder(radius, height, (0.0, 0.0, height / 2.0), "StumpBody", material=mats["bark"], vertices=18),
        add_cylinder(radius * 0.92, 0.02, (0.0, 0.0, height), "StumpTop", material=mats["sand"], vertices=18),
    ]
    for index in range(4):
        angle = (math.tau / 4.0) * index
        end = (math.cos(angle) * radius * 1.15, math.sin(angle) * radius * 1.15, 0.05)
        parts.append(cylinder_between((0.0, 0.0, 0.08), end, radius * 0.16, 0.03, f"StumpRoot_{index}", material=mats["dark_bark"]))
    return join_parts(parts, "TreeStumpAsset")


def generate_fallen_tree(params, mats, rng):
    length = cm(params.get("length", 360.0))
    trunk_radius = cm(params.get("trunk_radius", 20.0))
    has_leaves = params.get("has_leaves", True)
    parts = [
        add_cylinder(trunk_radius, length, (0.0, 0.0, trunk_radius), "FallenTreeBody", material=mats["bark"], rotation=(math.pi / 2.0, 0.0, 0.0))
    ]
    branch_a = cylinder_between((0.0, -length * 0.1, trunk_radius * 1.1), (length * 0.08, -length * 0.02, trunk_radius * 2.3), trunk_radius * 0.22, 0.035, "FallenBranchA", material=mats["bark"])
    branch_b = cylinder_between((0.0, length * 0.18, trunk_radius * 1.1), (-length * 0.06, length * 0.28, trunk_radius * 2.0), trunk_radius * 0.2, 0.03, "FallenBranchB", material=mats["bark"])
    parts.extend([branch_a, branch_b])
    if has_leaves:
        parts.append(add_canopy_blob((length * 0.11, -length * 0.01, trunk_radius * 2.7), length * 0.07, mats["leaf_oak"], "FallenLeavesA", rng))
        parts.append(add_canopy_blob((-length * 0.08, length * 0.31, trunk_radius * 2.35), length * 0.06, mats["leaf_light"], "FallenLeavesB", rng))
    return join_parts(parts, "FallenTreeAsset")


def generate_mushroom(params, mats, rng):
    cap_diameter = cm(params.get("cap_diameter", 36.0))
    height = cm(params.get("height", 34.0))
    parts = [
        add_cylinder(cap_diameter * 0.16, height * 0.72, (0.0, 0.0, height * 0.36), "MushroomStem", material=mats["mushroom_stem"], vertices=14)
    ]
    cap = add_uv_sphere(cap_diameter * 0.22, (0.0, 0.0, height * 0.78), "MushroomCap", material=mats["mushroom_cap"], scale=(1.4, 1.4, 0.55))
    parts.append(cap)
    for index in range(6):
        angle = (math.tau / 6.0) * index
        parts.append(add_uv_sphere(0.018, (math.cos(angle) * cap_diameter * 0.11, math.sin(angle) * cap_diameter * 0.11, height * 0.82), f"MushroomSpot_{index}", material=mats["mushroom_spot"], scale=(1.0, 1.0, 0.4)))
    return join_parts(parts, "MushroomAsset")


def generate_vine(params, mats, rng):
    length = cm(params.get("length", 260.0))
    leaf_density = int(params.get("leaf_density", 9))
    points = []
    segments = 8
    for index in range(segments + 1):
        t = index / segments
        points.append((math.sin(t * math.pi * 1.2) * 0.18, 0.0, t * length))
    parts = []
    for index in range(segments):
        parts.append(cylinder_between(points[index], points[index + 1], 0.02, 0.012, f"VineSegment_{index}", material=mats["stem"], vertices=10))
    for index in range(max(5, leaf_density)):
        t = (index + 1) / (leaf_density + 1)
        base = mathutils.Vector((math.sin(t * math.pi * 1.2) * 0.18, 0.0, t * length))
        angle = t * math.tau * 2.0
        offset = mathutils.Vector((math.cos(angle) * 0.08, math.sin(angle) * 0.03, 0.0))
        parts.append(add_cube((0.012, 0.08, 0.008), tuple(base + offset), f"VineLeaf_{index}", material=mats["leaf_light"], rotation=(math.radians(50), 0.0, angle)))
    return join_parts(parts, "VineAsset")


def generate_root(params, mats, rng):
    width = cm(params.get("width", 180.0))
    depth = cm(params.get("depth", 120.0))
    height = cm(params.get("height", 50.0))
    parts = [add_uv_sphere(0.1, (0.0, 0.0, height * 0.35), "RootCore", material=mats["dark_bark"], scale=(1.6, 1.2, 0.7))]
    root_targets = [
        (width * 0.36, 0.0, 0.05),
        (-width * 0.28, depth * 0.18, 0.04),
        (-width * 0.12, -depth * 0.32, 0.05),
        (width * 0.14, -depth * 0.26, 0.03),
    ]
    for index, target in enumerate(root_targets):
        parts.append(cylinder_between((0.0, 0.0, height * 0.3), target, 0.06, 0.018, f"RootArm_{index}", material=mats["dark_bark"], vertices=12))
    return join_parts(parts, "RootAsset")


def generate_pond(params, mats, rng):
    width = cm(params.get("width", 240.0))
    depth = cm(params.get("depth", 180.0))
    bank_height = cm(params.get("bank_height", 22.0))
    parts = [
        add_uv_sphere(0.4, (0.0, 0.0, bank_height * 0.6), "PondBank", material=mats["sand"], scale=(width * 0.95, depth * 0.85, bank_height * 1.1)),
        add_uv_sphere(0.3, (0.0, 0.0, bank_height * 0.36), "PondWater", material=mats["water"], scale=(width * 0.72, depth * 0.58, bank_height * 0.24)),
    ]
    for index in range(5):
        rock = add_ico_sphere(
            0.12,
            (
                rng.uniform(-width * 0.28, width * 0.28),
                rng.uniform(-depth * 0.24, depth * 0.24),
                bank_height * 0.48,
            ),
            f"PondRock_{index}",
            material=mats["rock"],
            scale=(0.12, 0.1, 0.06),
        )
        deform_rock(rock, rng, amount_xy=0.16, amount_z=0.12)
        parts.append(rock)
    return join_parts(parts, "PondAsset")


def generate_river_segment(params, mats, rng):
    width = cm(params.get("width", 160.0))
    length = cm(params.get("length", 340.0))
    curve = cm(params.get("curve", 60.0))
    parts = []
    z = 0.05
    water_points = []
    for index in range(6):
        t = index / 5.0
        water_points.append((math.sin(t * math.pi) * curve * 0.45, (t - 0.5) * length, z))
    for index in range(5):
        start = mathutils.Vector(water_points[index])
        end = mathutils.Vector(water_points[index + 1])
        mid = (start + end) / 2.0
        segment_len = max((end - start).length, 0.01)
        angle = math.atan2(end.x - start.x, end.y - start.y)
        parts.append(add_cube((width * 0.46, segment_len * 0.52, 0.025), tuple(mid), f"RiverWater_{index}", material=mats["water"], rotation=(0.0, 0.0, -angle)))
        parts.append(add_cube((width * 0.62, segment_len * 0.56, 0.05), (mid.x - width * 0.12, mid.y, 0.025), f"RiverBankL_{index}", material=mats["sand"], rotation=(0.0, 0.0, -angle)))
        parts.append(add_cube((width * 0.62, segment_len * 0.56, 0.05), (mid.x + width * 0.12, mid.y, 0.025), f"RiverBankR_{index}", material=mats["sand"], rotation=(0.0, 0.0, -angle)))
    return join_parts(parts, "RiverSegmentAsset")


def generate_waterfall(params, mats, rng):
    width = cm(params.get("width", 140.0))
    height = cm(params.get("height", 260.0))
    pool_radius = cm(params.get("pool_radius", 110.0))
    cliff_height = height * 0.94
    parts = [
        add_rock_blob((0.0, width * 0.02, cliff_height * 0.48), 0.42, (width * 0.9, width * 0.42, cliff_height * 0.86), mats["rock_dark"], "WaterfallCliffCore", rng),
        add_rock_blob((-width * 0.24, 0.0, height * 0.58), 0.24, (width * 0.34, width * 0.24, height * 0.44), mats["rock"], "WaterfallShoulderLeft", rng),
        add_rock_blob((width * 0.24, width * 0.02, height * 0.56), 0.24, (width * 0.32, width * 0.22, height * 0.42), mats["rock"], "WaterfallShoulderRight", rng),
        add_rock_blob((0.0, width * 0.12, height * 0.92), 0.18, (width * 0.46, width * 0.2, height * 0.14), mats["rock_dark"], "WaterfallTopLedge", rng, deform_xy=0.16, deform_z=0.12),
    ]

    sheet_y = -width * 0.06
    parts.append(add_cube((width * 0.13, width * 0.08, height * 0.46), (0.0, sheet_y, height * 0.48), "WaterfallSheetOuter", material=mats["water"], rotation=(math.radians(3.0), 0.0, 0.0)))
    parts.append(add_cube((width * 0.09, width * 0.05, height * 0.42), (0.0, sheet_y - width * 0.02, height * 0.46), "WaterfallSheetInner", material=mats["foam"], rotation=(math.radians(5.0), 0.0, 0.0)))
    parts.append(add_cube((width * 0.32, width * 0.16, 0.03), (0.0, width * 0.08, height * 0.92), "WaterfallCreek", material=mats["water"]))

    parts.append(
        add_uv_sphere(
            0.34,
            (0.0, -pool_radius * 0.08, 0.09),
            "WaterfallPool",
            material=mats["water"],
            scale=(pool_radius * 0.9, pool_radius * 0.64, 0.18),
        )
    )
    parts.append(
        add_uv_sphere(
            0.18,
            (0.0, -width * 0.12, 0.12),
            "WaterfallSplash",
            material=mats["foam"],
            scale=(width * 0.34, width * 0.2, 0.12),
        )
    )
    parts.append(add_cube((width * 0.26, width * 0.08, 0.02), (0.0, -width * 0.1, 0.18), "WaterfallFoamBand", material=mats["foam"]))

    for index, (x, y, radius, scale) in enumerate([
        (-pool_radius * 0.42, pool_radius * 0.02, 0.16, (pool_radius * 0.3, pool_radius * 0.18, height * 0.14)),
        (pool_radius * 0.38, -pool_radius * 0.08, 0.15, (pool_radius * 0.28, pool_radius * 0.18, height * 0.13)),
        (-pool_radius * 0.12, -pool_radius * 0.18, 0.12, (pool_radius * 0.18, pool_radius * 0.14, height * 0.1)),
        (pool_radius * 0.1, pool_radius * 0.2, 0.11, (pool_radius * 0.16, pool_radius * 0.12, height * 0.08)),
    ]):
        parts.append(add_rock_blob((x, y, height * 0.06), radius, scale, mats["rock"], f"WaterfallBaseRock_{index}", rng, deform_xy=0.18, deform_z=0.12))

    for bank_index, x in enumerate((-pool_radius * 0.3, pool_radius * 0.3)):
        parts.append(
            add_uv_sphere(
                0.12,
                (x, pool_radius * 0.18, height * 0.05),
                f"WaterfallBankMoss_{bank_index}",
                material=mats["moss"],
                scale=(pool_radius * 0.16, pool_radius * 0.1, height * 0.06),
            )
        )
    return join_parts(parts, "WaterfallAsset")


def generate_stream(params, mats, rng):
    width = cm(params.get("width", 75.0))
    length = cm(params.get("length", 260.0))
    curve = cm(params.get("curve", 36.0))
    parts = []
    points = []
    for index in range(5):
        t = index / 4.0
        points.append((math.sin(t * math.pi * 1.5) * curve * 0.45, (t - 0.5) * length, 0.03))
    for index in range(4):
        start = mathutils.Vector(points[index])
        end = mathutils.Vector(points[index + 1])
        mid = (start + end) / 2.0
        segment_len = max((end - start).length, 0.01)
        angle = math.atan2(end.x - start.x, end.y - start.y)
        parts.append(add_cube((width * 0.4, segment_len * 0.52, 0.018), tuple(mid), f"StreamWater_{index}", material=mats["water"], rotation=(0.0, 0.0, -angle)))
        parts.append(add_cube((width * 0.5, segment_len * 0.52, 0.035), (mid.x - width * 0.09, mid.y, 0.018), f"StreamBankL_{index}", material=mats["moss"], rotation=(0.0, 0.0, -angle)))
        parts.append(add_cube((width * 0.5, segment_len * 0.52, 0.035), (mid.x + width * 0.09, mid.y, 0.018), f"StreamBankR_{index}", material=mats["moss"], rotation=(0.0, 0.0, -angle)))
    return join_parts(parts, "StreamAsset")


GENERATORS = {
    "oak_tree": generate_oak_tree,
    "pine_tree": generate_pine_tree,
    "birch_tree": generate_birch_tree,
    "palm_tree": generate_palm_tree,
    "dead_tree": generate_dead_tree,
    "sapling": generate_sapling,
    "grass": generate_grass,
    "bush": generate_bush,
    "shrub": generate_shrub,
    "fern": generate_fern,
    "flower": generate_flower,
    "moss": generate_moss,
    "small_rock": generate_small_rock,
    "boulder": generate_boulder,
    "rock_cluster": generate_rock_cluster,
    "cliff_section": generate_cliff_section,
    "log": generate_log,
    "tree_stump": generate_tree_stump,
    "fallen_tree": generate_fallen_tree,
    "mushroom": generate_mushroom,
    "vine": generate_vine,
    "root": generate_root,
    "pond": generate_pond,
    "river_segment": generate_river_segment,
    "waterfall": generate_waterfall,
    "stream": generate_stream,
}


def generate_nature_asset(params):
    asset_type = params.get("asset_type")
    if asset_type not in GENERATORS:
        raise ValueError(f"Unsupported nature asset type: {asset_type}")
    rng = random.Random(seed_for(asset_type, params))
    mats = build_materials()
    return GENERATORS[asset_type](params, mats, rng)


def main():
    parser = argparse.ArgumentParser(description="Procedural Nature Asset Generator")
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
    asset_obj = generate_nature_asset(params)

    if args.render:
        utils.setup_lighting_and_camera(asset_obj)
        utils.render_preview(args.render)

    utils.export_glb(args.export)


if __name__ == "__main__":
    main()
