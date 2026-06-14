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

def generate_clock(params):
    w = params.get("width", 40.0) / 100.0  # cm to m
    h = params.get("height", 40.0) / 100.0 # cm to m
    d = params.get("depth", 5.0) / 100.0   # cm to m
    shape = params.get("shape", "circular")
    style = params.get("style", "wall")
    mat_type = params.get("material", "wood")

    parts = []

    # Helper to apply boolean difference
    def apply_boolean_difference(target, cutter):
        bpy.ops.object.select_all(action='DESELECT')
        target.select_set(True)
        bpy.context.view_layer.objects.active = target
        bool_mod = target.modifiers.new(name="Boolean", type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = cutter
        bpy.ops.object.modifier_apply(modifier="Boolean")
        # Delete cutter
        bpy.ops.object.select_all(action='DESELECT')
        cutter.select_set(True)
        bpy.ops.object.delete()

    # 1. Create Materials
    if mat_type == "wood":
        frame_mat = utils.create_material("ClockFrameWood", diffuse_color=(0.26, 0.15, 0.08, 1.0), metallic=0.0, roughness=0.7)
    elif mat_type == "metal":
        frame_mat = utils.create_material("ClockFrameMetal", diffuse_color=(0.85, 0.65, 0.18, 1.0), metallic=0.9, roughness=0.25) # gold/brass
    else: # plastic
        frame_mat = utils.create_material("ClockFramePlastic", diffuse_color=(0.1, 0.1, 0.1, 1.0), metallic=0.1, roughness=0.4)

    dial_mat = utils.create_material("ClockDialFace", diffuse_color=(0.96, 0.96, 0.94, 1.0), metallic=0.0, roughness=0.9)
    hands_mat = utils.create_material("ClockHands", diffuse_color=(0.05, 0.05, 0.05, 1.0), metallic=0.1, roughness=0.5)
    tick_mat = utils.create_material("ClockTicks", diffuse_color=(0.12, 0.12, 0.12, 1.0), metallic=0.1, roughness=0.6)
    
    # Glass material: high transmission, low roughness
    glass_mat = bpy.data.materials.new(name="ClockGlassFace")
    glass_mat.use_nodes = True
    bsdf = glass_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 0.1)
        bsdf.inputs['Roughness'].default_value = 0.05
        bsdf.inputs['Transmission Weight'].default_value = 0.95
        bsdf.inputs['IOR'].default_value = 1.45

    # Center position
    center_z = h / 2.0
    if style == "tabletop":
        center_z += 0.05  # raise slightly for tabletop stand

    # 2. Build Clock Frame & Dial Backing
    if shape == "circular":
        radius = w / 2.0
        # Frame Outer
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=64,
            radius=radius,
            depth=d,
            location=(0, 0, center_z),
            rotation=(math.pi / 2.0, 0, 0)
        )
        frame = bpy.context.active_object
        frame.name = "ClockFrame_Circ"
        
        # Frame Inner Cutter (shifted forward to hollow out front face, leaving 1cm back wall)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=64,
            radius=radius - 0.02,
            depth=d,
            location=(0, -0.01, center_z),
            rotation=(math.pi / 2.0, 0, 0)
        )
        cutter = bpy.context.active_object
        
        # Apply boolean to hollow it
        apply_boolean_difference(frame, cutter)
        utils.apply_smooth_by_angle(frame, angle=30.0)
        utils.apply_bevel(frame, width=0.005)
        utils.apply_material(frame, frame_mat)
        parts.append(frame)

        # Dial Face (placed inside the hollowed out cup, flat against back wall)
        dial_radius = radius - 0.02
        dial_y = d / 2.0 - 0.012  # flat against the 1cm back wall
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=64,
            radius=dial_radius,
            depth=0.002,
            location=(0, dial_y, center_z),
            rotation=(math.pi / 2.0, 0, 0)
        )
        dial = bpy.context.active_object
        dial.name = "ClockDial_Circ"
        utils.apply_smooth_by_angle(dial, angle=30.0)
        utils.apply_material(dial, dial_mat)
        parts.append(dial)
        
    else: # rectangular
        # Frame Outer
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, center_z))
        frame = bpy.context.active_object
        frame.name = "ClockFrame_Rect"
        frame.scale = (w, d, h)
        bpy.ops.object.transform_apply(scale=True)
        
        # Frame Inner Cutter
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.01, center_z))
        cutter = bpy.context.active_object
        cutter.scale = (w - 0.04, d, h - 0.04)
        bpy.ops.object.transform_apply(scale=True)
        
        # Apply boolean to hollow it
        apply_boolean_difference(frame, cutter)
        utils.apply_bevel(frame, width=0.005)
        utils.apply_material(frame, frame_mat)
        parts.append(frame)

        # Dial Face
        dial_w = w - 0.04
        dial_h = h - 0.04
        dial_y = d / 2.0 - 0.012
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, dial_y, center_z))
        dial = bpy.context.active_object
        dial.name = "ClockDial_Rect"
        dial.scale = (dial_w, 0.002, dial_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(dial, dial_mat)
        parts.append(dial)
        
        dial_radius = min(dial_w, dial_h) / 2.0

    # 3. Dial Tick Marks (placed on dial surface)
    tick_y = dial_y - 0.002
    for i in range(12):
        angle = math.radians(i * 30.0)
        tick_r = dial_radius * 0.85
        tx = tick_r * math.sin(angle)
        tz = center_z + tick_r * math.cos(angle)
        
        is_cardinal = (i % 3 == 0)
        t_width = 0.004 if not is_cardinal else 0.008
        t_length = 0.015 if not is_cardinal else 0.025
        t_depth = 0.002
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(tx, tick_y, tz))
        tick = bpy.context.active_object
        tick.name = f"ClockTick_{i}"
        tick.scale = (t_width, t_depth, t_length)
        tick.rotation_euler = (0, -angle, 0)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        utils.apply_material(tick, tick_mat)
        parts.append(tick)

    # 4. Clock Hands (with proper origin rotation and offset)
    hour_angle = math.radians(300.0) # 10 o'clock
    hour_length = dial_radius * 0.55
    hour_y = tick_y - 0.003
    
    # Hour hand
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, hour_y, center_z + hour_length / 2.0))
    hour_hand = bpy.context.active_object
    hour_hand.name = "ClockHourHand"
    hour_hand.scale = (0.006, 0.0015, hour_length)
    bpy.ops.object.transform_apply(scale=True)
    
    bpy.context.scene.cursor.location = (0, hour_y, center_z)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    hour_hand.rotation_euler = (0, -hour_angle, 0)
    bpy.ops.object.transform_apply(rotation=True)
    utils.apply_material(hour_hand, hands_mat)
    parts.append(hour_hand)

    # Minute hand (2 o'clock)
    minute_angle = math.radians(60.0)
    minute_length = dial_radius * 0.78
    minute_y = hour_y - 0.0025
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, minute_y, center_z + minute_length / 2.0))
    minute_hand = bpy.context.active_object
    minute_hand.name = "ClockMinuteHand"
    minute_hand.scale = (0.0045, 0.0012, minute_length)
    bpy.ops.object.transform_apply(scale=True)
    
    bpy.context.scene.cursor.location = (0, minute_y, center_z)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    minute_hand.rotation_euler = (0, -minute_angle, 0)
    bpy.ops.object.transform_apply(rotation=True)
    utils.apply_material(minute_hand, hands_mat)
    parts.append(minute_hand)

    # Center Pin/Cap
    pin_y = minute_y - 0.002
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.008,
        depth=0.006,
        location=(0, pin_y, center_z),
        rotation=(math.pi / 2.0, 0, 0)
    )
    pin = bpy.context.active_object
    pin.name = "ClockCenterPin"
    utils.apply_material(pin, hands_mat)
    parts.append(pin)

    # 5. Front Glass Face plate (caps the inset near front edge)
    glass_y = -d / 2.0 + 0.003
    if shape == "circular":
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=64,
            radius=radius - 0.005,
            depth=0.0015,
            location=(0, glass_y, center_z),
            rotation=(math.pi / 2.0, 0, 0)
        )
        glass = bpy.context.active_object
        glass.name = "ClockGlass_Circ"
        utils.apply_smooth_by_angle(glass, angle=30.0)
        utils.apply_material(glass, glass_mat)
        parts.append(glass)
    else:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, glass_y, center_z))
        glass = bpy.context.active_object
        glass.name = "ClockGlass_Rect"
        glass.scale = (w - 0.01, 0.0015, h - 0.01)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(glass, glass_mat)
        parts.append(glass)

    # 6. Tabletop Stand (only if tabletop style)
    if style == "tabletop":
        # Base plate at Z = 0
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.01))
        stand_base = bpy.context.active_object
        stand_base.name = "ClockStandBase"
        stand_base.scale = (w * 0.7, d * 1.8, 0.02)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(stand_base, width=0.003)
        utils.apply_material(stand_base, frame_mat)
        parts.append(stand_base)

        # Support bracket behind the frame
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, d / 2.0 + 0.01, center_z / 2.0))
        bracket = bpy.context.active_object
        bracket.name = "ClockStandBracket"
        bracket.scale = (w * 0.15, d, center_z * 0.9)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(bracket, width=0.003)
        utils.apply_material(bracket, frame_mat)
        parts.append(bracket)

    # 7. Join and set origin
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    
    parts[0].name = "ClockAsset"
    
    # Adjust origin to base center of the bounding box
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return parts[0]

def main():
    parser = argparse.ArgumentParser(description="Procedural Clock Generator")
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
    clock_obj = generate_clock(params)
    
    if args.render:
        utils.setup_lighting_and_camera(clock_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
