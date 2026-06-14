import json
import math
import os
import sys

import bpy
import mathutils


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    manifest_path = None
    output_path = None

    for index, arg in enumerate(argv):
        if arg == "--manifest" and index + 1 < len(argv):
            manifest_path = argv[index + 1]
        if arg == "--output" and index + 1 < len(argv):
            output_path = argv[index + 1]

    if not manifest_path or not output_path:
        raise ValueError("Missing --manifest or --output argument.")

    return os.path.abspath(manifest_path), os.path.abspath(output_path)


def cleanup_scene():
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    for mesh in list(bpy.data.meshes):
        bpy.data.meshes.remove(mesh)
    for material in list(bpy.data.materials):
        bpy.data.materials.remove(material)


def hex_to_rgba(hex_value, alpha=1.0):
    if not isinstance(hex_value, str) or not hex_value.startswith("#") or len(hex_value) != 7:
        return (0.8, 0.8, 0.8, alpha)
    return (
        int(hex_value[1:3], 16) / 255.0,
        int(hex_value[3:5], 16) / 255.0,
        int(hex_value[5:7], 16) / 255.0,
        alpha,
    )


def make_material(name, color, metallic=0.0, roughness=0.62, emission=None, emission_strength=0.0):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        rgba = hex_to_rgba(color) if isinstance(color, str) else color
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        if emission:
            bsdf.inputs["Emission Color"].default_value = hex_to_rgba(emission)
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return material


def collection(name):
    found = bpy.data.collections.get(name)
    if found:
        return found
    created = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(created)
    return created


def link_to_collection(obj, target_collection):
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    target_collection.objects.link(obj)


def mark_rotoscope(obj, category, label, enabled):
    obj["rotoscope_category"] = category
    obj["rotoscope_label"] = label
    obj.show_name = enabled
    obj.show_wire = enabled
    obj.show_in_front = enabled


def bevel(obj, width=0.025, segments=1):
    modifier = obj.modifiers.new("RotoscopeSafe_Bevel", "BEVEL")
    modifier.width = width
    modifier.segments = segments
    modifier.affect = "EDGES"
    obj.modifiers.new("WeightedNormals", "WEIGHTED_NORMAL")


def add_cube(name, location, size, material, target_collection, rotoscope=False, category="City"):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0] / 2.0, size[1] / 2.0, size[2] / 2.0)
    obj.data.materials.append(material)
    bevel(obj, width=min(size) * 0.025 if min(size) > 0 else 0.01)
    mark_rotoscope(obj, category, name, rotoscope)
    link_to_collection(obj, target_collection)
    return obj


def add_cylinder(name, location, radius, depth, material, target_collection, vertices=20, rotoscope=False, category="City"):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(material)
    bevel(obj, width=radius * 0.08, segments=2)
    mark_rotoscope(obj, category, name, rotoscope)
    link_to_collection(obj, target_collection)
    return obj


def add_gabled_roof(name, location, width, depth, height, material, target_collection, rotoscope=False):
    half_w = width / 2.0
    half_d = depth / 2.0
    verts = [
        (-half_w, -half_d, 0),
        (half_w, -half_d, 0),
        (0, -half_d, height),
        (-half_w, half_d, 0),
        (half_w, half_d, 0),
        (0, half_d, height),
    ]
    faces = [
        (0, 1, 2),
        (3, 5, 4),
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (2, 5, 3, 0),
    ]
    mesh = bpy.data.meshes.new(f"{name}Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.data.materials.append(material)
    target_collection.objects.link(obj)
    bevel(obj, width=0.02)
    mark_rotoscope(obj, "Buildings", name, rotoscope)
    return obj


def look_at(obj, target):
    direction = mathutils.Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def road_rotation(variant):
    return math.radians(90.0) if variant == "vertical" else 0.0


def cell_center(cell, grid_size, cell_size):
    x = (cell["col"] - (grid_size / 2.0) + 0.5) * cell_size
    y = ((grid_size / 2.0) - cell["row"] - 0.5) * cell_size
    return x, y


def create_materials():
    return {
        "terrain": make_material("City_Terrain_AsphaltBase", "#1f2937", roughness=0.8),
        "lot": make_material("City_Lot_Grass", "#21442f", roughness=0.75),
        "road": make_material("Road_Dark_Asphalt", "#2b3039", roughness=0.7),
        "lane": make_material("Road_Yellow_Lane_Marks", "#facc15", roughness=0.45),
        "crosswalk": make_material("Road_Crosswalk_White", "#f8fafc", roughness=0.35),
        "sidewalk": make_material("Concrete_Sidewalk", "#7c8491", roughness=0.8),
        "house_wall": make_material("House_Warm_Plaster", "#f8fafc", roughness=0.68),
        "house_roof": make_material("House_Red_Gabled_Roof", "#b91c1c", roughness=0.55),
        "apartment": make_material("Apartment_Concrete", "#64748b", roughness=0.72),
        "office": make_material("Office_Teal_Glass", "#0f766e", metallic=0.1, roughness=0.28),
        "shop": make_material("Shop_Brick", "#92400e", roughness=0.7),
        "awning_red": make_material("Shop_Red_Awning", "#ef4444", roughness=0.5),
        "glass": make_material("Window_Cool_Glass", "#bae6fd", metallic=0.0, roughness=0.18),
        "door": make_material("Door_Dark_Wood", "#78350f", roughness=0.55),
        "metal": make_material("StreetLight_Dark_Metal", "#334155", metallic=0.55, roughness=0.34),
        "glow_warm": make_material("Lamp_Warm_Glow", "#fef3c7", roughness=0.2, emission="#fde68a", emission_strength=2.8),
        "glow_cool": make_material("Modern_LED_Cool_Glow", "#cffafe", roughness=0.2, emission="#67e8f9", emission_strength=3.2),
    }


def add_road_tile(cell, manifest, materials, roads_collection):
    grid_size = manifest["grid_size"]
    cell_size = manifest["cell_size"]
    variant = cell.get("road")
    if not variant:
        return

    x, y = cell_center(cell, grid_size, cell_size)
    z = 0.045
    prefix = f"Road_{variant}_r{cell['row'] + 1}_c{cell['col'] + 1}"
    lane_h = 0.035

    if variant == "intersection":
        add_cube(f"{prefix}_north_south", (x, y, z), (cell_size * 0.42, cell_size, 0.09), materials["road"], roads_collection, manifest["rotoscope"], "Roads")
        add_cube(f"{prefix}_east_west", (x, y, z + 0.003), (cell_size, cell_size * 0.42, 0.095), materials["road"], roads_collection, manifest["rotoscope"], "Roads")
        add_cube(f"{prefix}_crosswalk_a", (x, y - cell_size * 0.24, z + 0.06), (cell_size * 0.48, 0.08, lane_h), materials["crosswalk"], roads_collection, manifest["rotoscope"], "Roads")
        add_cube(f"{prefix}_crosswalk_b", (x - cell_size * 0.24, y, z + 0.06), (0.08, cell_size * 0.48, lane_h), materials["crosswalk"], roads_collection, manifest["rotoscope"], "Roads")
        return

    if variant == "curve":
        add_cube(f"{prefix}_west_leg", (x - cell_size * 0.14, y, z), (cell_size * 0.72, cell_size * 0.42, 0.09), materials["road"], roads_collection, manifest["rotoscope"], "Roads")
        add_cube(f"{prefix}_south_leg", (x, y - cell_size * 0.14, z + 0.003), (cell_size * 0.42, cell_size * 0.72, 0.095), materials["road"], roads_collection, manifest["rotoscope"], "Roads")
        add_cube(f"{prefix}_lane_west", (x - cell_size * 0.2, y, z + 0.06), (cell_size * 0.36, 0.045, lane_h), materials["lane"], roads_collection, manifest["rotoscope"], "Roads")
        add_cube(f"{prefix}_lane_south", (x, y - cell_size * 0.2, z + 0.06), (0.045, cell_size * 0.36, lane_h), materials["lane"], roads_collection, manifest["rotoscope"], "Roads")
        return

    is_vertical = variant == "vertical"
    size = (cell_size * 0.42, cell_size, 0.09) if is_vertical else (cell_size, cell_size * 0.42, 0.09)
    lane_size = (0.05, cell_size * 0.72, lane_h) if is_vertical else (cell_size * 0.72, 0.05, lane_h)
    add_cube(prefix, (x, y, z), size, materials["road"], roads_collection, manifest["rotoscope"], "Roads")
    add_cube(f"{prefix}_center_lane", (x, y, z + 0.06), lane_size, materials["lane"], roads_collection, manifest["rotoscope"], "Roads")


def add_house(cell, manifest, materials, buildings_collection):
    x, y = cell_center(cell, manifest["grid_size"], manifest["cell_size"])
    elevation = cell.get("elevation", 0.0)
    scale = cell.get("height_scale", 1.0)
    base_name = f"House_r{cell['row'] + 1}_c{cell['col'] + 1}"
    body_h = 1.65 * scale
    body = add_cube(f"{base_name}_body", (x, y, elevation + body_h / 2.0), (2.35, 2.05, body_h), materials["house_wall"], buildings_collection, manifest["rotoscope"], "Buildings")
    body.rotation_euler.z = math.radians(cell.get("rotation", 0.0))
    roof = add_gabled_roof(f"{base_name}_red_roof", (x, y, elevation + body_h), 2.65, 2.35, 0.85, materials["house_roof"], buildings_collection, manifest["rotoscope"])
    roof.rotation_euler.z = body.rotation_euler.z
    add_cube(f"{base_name}_front_door", (x, y - 1.04, elevation + 0.45), (0.38, 0.08, 0.9), materials["door"], buildings_collection, manifest["rotoscope"], "Buildings")
    add_cube(f"{base_name}_left_window", (x - 0.58, y - 1.05, elevation + 1.05), (0.36, 0.07, 0.34), materials["glass"], buildings_collection, manifest["rotoscope"], "Buildings")
    add_cube(f"{base_name}_right_window", (x + 0.58, y - 1.05, elevation + 1.05), (0.36, 0.07, 0.34), materials["glass"], buildings_collection, manifest["rotoscope"], "Buildings")
    add_cube(f"{base_name}_chimney", (x + 0.72, y + 0.25, elevation + body_h + 0.68), (0.22, 0.24, 0.8), materials["door"], buildings_collection, manifest["rotoscope"], "Buildings")


def add_apartment(cell, manifest, materials, buildings_collection):
    x, y = cell_center(cell, manifest["grid_size"], manifest["cell_size"])
    elevation = cell.get("elevation", 0.0)
    scale = cell.get("height_scale", 1.0)
    floors = max(3, round(5 * scale))
    height = floors * 0.72
    base_name = f"Apartment_r{cell['row'] + 1}_c{cell['col'] + 1}"
    add_cube(f"{base_name}_tower_body", (x, y, elevation + height / 2.0), (2.45, 2.25, height), materials["apartment"], buildings_collection, manifest["rotoscope"], "Buildings")
    for floor in range(floors):
        z = elevation + 0.34 + floor * 0.72
        for idx, offset_x in enumerate((-0.72, 0, 0.72)):
            add_cube(f"{base_name}_front_window_f{floor + 1}_{idx + 1}", (x + offset_x, y - 1.15, z), (0.34, 0.06, 0.3), materials["glass"], buildings_collection, manifest["rotoscope"], "Buildings")
        if floor % 2 == 1:
            add_cube(f"{base_name}_balcony_f{floor + 1}", (x + 1.25, y, z - 0.05), (0.12, 0.72, 0.08), materials["sidewalk"], buildings_collection, manifest["rotoscope"], "Buildings")


def add_office(cell, manifest, materials, buildings_collection):
    x, y = cell_center(cell, manifest["grid_size"], manifest["cell_size"])
    elevation = cell.get("elevation", 0.0)
    scale = cell.get("height_scale", 1.0)
    floors = max(6, round(8 * scale))
    height = floors * 0.74
    base_name = f"OfficeTower_r{cell['row'] + 1}_c{cell['col'] + 1}"
    add_cube(f"{base_name}_glass_core", (x, y, elevation + height / 2.0), (2.15, 2.15, height), materials["office"], buildings_collection, manifest["rotoscope"], "Buildings")
    for floor in range(floors):
        z = elevation + 0.38 + floor * 0.74
        add_cube(f"{base_name}_window_band_front_{floor + 1}", (x, y - 1.09, z), (1.72, 0.045, 0.28), materials["glass"], buildings_collection, manifest["rotoscope"], "Buildings")
        add_cube(f"{base_name}_window_band_right_{floor + 1}", (x + 1.09, y, z), (0.045, 1.72, 0.28), materials["glass"], buildings_collection, manifest["rotoscope"], "Buildings")
    add_cylinder(f"{base_name}_antenna", (x, y, elevation + height + 0.55), 0.035, 1.1, materials["metal"], buildings_collection, vertices=10, rotoscope=manifest["rotoscope"], category="Buildings")


def add_shop(cell, manifest, materials, buildings_collection):
    x, y = cell_center(cell, manifest["grid_size"], manifest["cell_size"])
    elevation = cell.get("elevation", 0.0)
    scale = cell.get("height_scale", 1.0)
    base_name = f"Shop_r{cell['row'] + 1}_c{cell['col'] + 1}"
    height = 1.15 * scale
    add_cube(f"{base_name}_brick_body", (x, y, elevation + height / 2.0), (2.7, 1.95, height), materials["shop"], buildings_collection, manifest["rotoscope"], "Buildings")
    add_cube(f"{base_name}_striped_awning", (x, y - 1.08, elevation + height + 0.06), (2.95, 0.42, 0.18), materials["awning_red"], buildings_collection, manifest["rotoscope"], "Buildings")
    add_cube(f"{base_name}_shop_sign", (x, y - 1.02, elevation + height + 0.42), (1.55, 0.09, 0.36), materials["lane"], buildings_collection, manifest["rotoscope"], "Buildings")
    add_cube(f"{base_name}_display_window_left", (x - 0.55, y - 1.01, elevation + 0.52), (0.62, 0.07, 0.48), materials["glass"], buildings_collection, manifest["rotoscope"], "Buildings")
    add_cube(f"{base_name}_glass_door", (x + 0.56, y - 1.01, elevation + 0.48), (0.42, 0.07, 0.82), materials["glass"], buildings_collection, manifest["rotoscope"], "Buildings")


def add_building(cell, manifest, materials, buildings_collection):
    variant = cell.get("building")
    if variant == "house":
        add_house(cell, manifest, materials, buildings_collection)
    elif variant == "apartment":
        add_apartment(cell, manifest, materials, buildings_collection)
    elif variant == "office":
        add_office(cell, manifest, materials, buildings_collection)
    elif variant == "shop":
        add_shop(cell, manifest, materials, buildings_collection)


def add_street_light(cell, manifest, materials, lights_collection):
    if not cell.get("light"):
        return
    x, y = cell_center(cell, manifest["grid_size"], manifest["cell_size"])
    variant = cell.get("light")
    base_name = f"{'ModernLED' if variant == 'modern' else 'ClassicLamp'}_r{cell['row'] + 1}_c{cell['col'] + 1}"
    offset = manifest["cell_size"] * 0.28
    lx, ly = x + offset, y + offset
    pole_h = 2.25 if variant == "modern" else 2.05
    add_cylinder(f"{base_name}_pole", (lx, ly, pole_h / 2.0), 0.045, pole_h, materials["metal"], lights_collection, rotoscope=manifest["rotoscope"], category="Lights")
    if variant == "modern":
        add_cube(f"{base_name}_horizontal_arm", (lx + 0.38, ly, pole_h - 0.08), (0.78, 0.07, 0.08), materials["metal"], lights_collection, manifest["rotoscope"], "Lights")
        add_cube(f"{base_name}_cool_led_head", (lx + 0.78, ly, pole_h - 0.18), (0.42, 0.22, 0.12), materials["glow_cool"], lights_collection, manifest["rotoscope"], "Lights")
        bpy.ops.object.light_add(type="AREA", location=(lx + 0.78, ly, pole_h - 0.35))
        light = bpy.context.active_object
        light.name = f"{base_name}_actual_area_light"
        light.data.energy = 280
        light.data.size = 1.1
    else:
        add_cube(f"{base_name}_lantern_cap", (lx, ly, pole_h + 0.05), (0.34, 0.34, 0.2), materials["metal"], lights_collection, manifest["rotoscope"], "Lights")
        add_cube(f"{base_name}_warm_glass", (lx, ly, pole_h - 0.12), (0.24, 0.24, 0.28), materials["glow_warm"], lights_collection, manifest["rotoscope"], "Lights")
        bpy.ops.object.light_add(type="POINT", location=(lx, ly, pole_h - 0.08))
        light = bpy.context.active_object
        light.name = f"{base_name}_actual_point_light"
        light.data.energy = 120
        light.data.shadow_soft_size = 4.0
    mark_rotoscope(light, "Lights", light.name, manifest["rotoscope"])
    link_to_collection(light, lights_collection)


def setup_scene_for_rotoscope(manifest):
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 96
    scene.render.use_freestyle = bool(manifest.get("rotoscope", True))

    try:
        view_layer = scene.view_layers[0]
        view_layer.use_freestyle = bool(manifest.get("rotoscope", True))
        lineset = view_layer.freestyle_settings.linesets[0]
        lineset.name = "Rotoscope_Object_Outlines"
        lineset.linestyle.thickness = 1.8
    except Exception:
        pass

    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.02, 0.035, 0.055, 1.0)
        bg.inputs["Strength"].default_value = 0.8


def build_city_scene(manifest):
    cleanup_scene()
    manifest["grid_size"] = int(manifest.get("grid_size") or 20)
    manifest["cell_size"] = float(manifest.get("cell_size") or 4.0)
    manifest["rotoscope"] = bool(manifest.get("rotoscope", True))

    setup_scene_for_rotoscope(manifest)
    materials = create_materials()
    roads_collection = collection("City_Roads_RotoscopeLayer")
    buildings_collection = collection("City_Buildings_RotoscopeLayer")
    lights_collection = collection("City_Lights_RotoscopeLayer")
    ground_collection = collection("City_Ground_RotoscopeLayer")

    grid_width = manifest["grid_size"] * manifest["cell_size"]
    add_cube(
        "Whole_City_Base_Block",
        (0, 0, -0.06),
        (grid_width + 2.0, grid_width + 2.0, 0.12),
        materials["terrain"],
        ground_collection,
        manifest["rotoscope"],
        "Ground",
    )

    for cell in manifest.get("cells", []):
        x, y = cell_center(cell, manifest["grid_size"], manifest["cell_size"])
        if cell.get("building") and not cell.get("road"):
            add_cube(
                f"Green_Lot_r{cell['row'] + 1}_c{cell['col'] + 1}",
                (x, y, 0.015),
                (manifest["cell_size"] * 0.9, manifest["cell_size"] * 0.9, 0.03),
                materials["lot"],
                ground_collection,
                manifest["rotoscope"],
                "Ground",
            )
        add_road_tile(cell, manifest, materials, roads_collection)
        add_building(cell, manifest, materials, buildings_collection)
        add_street_light(cell, manifest, materials, lights_collection)

    bpy.ops.object.light_add(type="SUN", location=(0, 0, 12))
    sun = bpy.context.active_object
    sun.name = "City_Sun_KeyLight"
    sun.data.energy = 2.2
    sun.rotation_euler = (math.radians(46), math.radians(0), math.radians(38))

    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    target = bpy.context.active_object
    target.name = "Rotoscope_City_Target"

    camera_distance = grid_width * 0.72
    bpy.ops.object.camera_add(location=(camera_distance, -camera_distance, camera_distance * 0.82))
    camera = bpy.context.active_object
    camera.name = "Rotoscope_City_Camera"
    look_at(camera, (0, 0, 0))
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = grid_width * 1.16
    bpy.context.scene.camera = camera


def save_output(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if os.path.splitext(output_path)[1].lower() != ".blend":
        raise ValueError("City export only supports .blend output.")
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    print(f"Saved Blender city file to: {output_path}")


def main():
    manifest_path, output_path = parse_args()
    with open(manifest_path, "r", encoding="utf-8") as manifest_file:
        manifest = json.load(manifest_file)
    build_city_scene(manifest)
    save_output(output_path)


if __name__ == "__main__":
    main()
