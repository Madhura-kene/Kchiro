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

def generate_stove(params):
    w = params.get("width", 75.0) / 100.0  # convert cm to meters
    d = params.get("depth", 60.0) / 100.0
    h = params.get("height", 90.0) / 100.0
    burners = params.get("burners", 4)
    style = params.get("style", "gas")
    material_type = params.get("material", "stainless_steel")

    parts = []

    # 1. Setup Materials
    if material_type == "white":
        body_color = (0.95, 0.95, 0.95, 1.0)
        metallic_body = 0.0
        rough_body = 0.35
    elif material_type == "black":
        body_color = (0.12, 0.12, 0.13, 1.0)
        metallic_body = 0.0
        rough_body = 0.5
    else: # stainless_steel
        body_color = (0.85, 0.85, 0.87, 1.0)
        metallic_body = 0.9
        rough_body = 0.22

    body_mat = utils.create_material("StoveBody", diffuse_color=body_color, metallic=metallic_body, roughness=rough_body)
    cooktop_mat = utils.create_material("StoveCooktop", diffuse_color=(0.08, 0.08, 0.08, 1.0), metallic=0.1, roughness=0.15)
    burner_metal = utils.create_material("StoveBurnerMetal", diffuse_color=(0.15, 0.15, 0.15, 1.0), metallic=0.8, roughness=0.6)
    burner_glow = utils.create_material("StoveBurnerGlow", diffuse_color=(0.95, 0.25, 0.0, 1.0), metallic=0.0, roughness=0.1) # Glowing red-orange
    knob_mat = utils.create_material("StoveKnobs", diffuse_color=(0.8, 0.8, 0.82, 1.0), metallic=0.9, roughness=0.2)
    glass_mat = utils.create_material("StoveGlass", diffuse_color=(0.05, 0.05, 0.05, 1.0), metallic=0.2, roughness=0.05)
    handle_mat = utils.create_material("StoveHandle", diffuse_color=(0.8, 0.8, 0.82, 1.0), metallic=0.9, roughness=0.2)

    base_h = 0.06
    cooktop_thick = 0.03
    main_h = h - base_h
    center_z = base_h + main_h / 2.0

    # 2. Main Carcass Box
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, center_z))
    carcass = bpy.context.active_object
    carcass.name = "StoveCarcass"
    carcass.scale = (w, d, main_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(carcass, width=0.005)
    utils.apply_material(carcass, body_mat)
    parts.append(carcass)
    master_obj = carcass

    # Bottom support kickplate/feet
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.01, base_h / 2.0))
    kickplate = bpy.context.active_object
    kickplate.name = "StoveKickplate"
    kickplate.scale = (w - 0.01, d - 0.02, base_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(kickplate, cooktop_mat)
    parts.append(kickplate)

    # 3. Cooktop Surface (Black glass or metal tray)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h - cooktop_thick / 2.0))
    cooktop = bpy.context.active_object
    cooktop.name = "StoveCooktopSurface"
    cooktop.scale = (w - 0.002, d - 0.002, cooktop_thick)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(cooktop, width=0.003)
    utils.apply_material(cooktop, cooktop_mat)
    parts.append(cooktop)

    # Backsplash/backguard (standard on freestanding stoves)
    guard_h = 0.08
    guard_d = 0.03
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, d/2.0 - guard_d/2.0, h + guard_h/2.0))
    backguard = bpy.context.active_object
    backguard.name = "StoveBackguard"
    backguard.scale = (w - 0.002, guard_d, guard_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(backguard, width=0.003)
    utils.apply_material(backguard, body_mat)
    parts.append(backguard)

    # 4. Burners layout
    w_burn = w * 0.75
    d_burn = d * 0.7
    
    burner_coords = []
    if burners == 2:
        burner_coords = [(0.0, -d_burn * 0.25), (0.0, d_burn * 0.25)]
    elif burners == 3:
        burner_coords = [(-w_burn * 0.28, -d_burn * 0.25), (w_burn * 0.28, -d_burn * 0.25), (0.0, d_burn * 0.25)]
    elif burners == 5:
        bx = w_burn * 0.3
        by = d_burn * 0.3
        burner_coords = [(-bx, -by), (bx, -by), (-bx, by), (bx, by), (0.0, 0.0)]
    elif burners == 6:
        bx = w_burn * 0.35
        by = d_burn * 0.3
        burner_coords = [
            (-bx, -by), (0.0, -by), (bx, -by),
            (-bx, by), (0.0, by), (bx, by)
        ]
    else: # 4 burners (default)
        bx = w_burn * 0.3
        by = d_burn * 0.3
        burner_coords = [(-bx, -by), (bx, -by), (-bx, by), (bx, by)]

    # Place burners
    for idx, (bx, by) in enumerate(burner_coords):
        bz = h + 0.001  # resting just on top of cooktop
        
        if style == "electric_glass":
            # Outer Ring (thin flat cylinder)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.002, location=(bx, by, bz + 0.001))
            outer_ring = bpy.context.active_object
            outer_ring.name = f"ElectricBurnerOuter_{idx}"
            outer_ring.scale = (1, 1, 1)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(outer_ring, burner_metal)
            parts.append(outer_ring)

            # Inner Ring (glowing / hot visual indicator on some elements)
            is_hot = (idx in [0, 2] if len(burner_coords) > 2 else idx == 0)
            ring_mat = burner_glow if is_hot else burner_metal
            
            bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.0022, location=(bx, by, bz + 0.0011))
            inner_ring = bpy.context.active_object
            inner_ring.name = f"ElectricBurnerInner_{idx}"
            inner_ring.scale = (1, 1, 1)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(inner_ring, ring_mat)
            parts.append(inner_ring)
            
        else: # gas style
            # Burner base collar
            bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.015, location=(bx, by, bz + 0.0075))
            collar = bpy.context.active_object
            collar.name = f"GasBurnerBase_{idx}"
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(collar, burner_metal)
            parts.append(collar)
            
            # Central brass/black cap
            bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.01, location=(bx, by, bz + 0.015 + 0.005))
            cap = bpy.context.active_object
            cap.name = f"GasBurnerCap_{idx}"
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(cap, burner_metal)
            parts.append(cap)
            
            # Crossed grates
            grate_w = 0.17
            grate_t = 0.008
            grate_h = 0.016
            
            for angle in [0, 90]:
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, bz + grate_h/2.0 + 0.005))
                grate = bpy.context.active_object
                grate.name = f"GasGrate_{idx}_{angle}"
                grate.scale = (grate_w, grate_t, grate_h)
                
                # Rotate grate bar
                grate.rotation_euler.z = math.radians(angle)
                bpy.ops.object.transform_apply(scale=True, rotation=True)
                utils.apply_bevel(grate, width=0.0015)
                utils.apply_material(grate, burner_metal)
                parts.append(grate)

    # 5. Front Control Panel & Knobs
    panel_h = 0.09
    panel_z = h - cooktop_thick - panel_h / 2.0
    panel_y = -d / 2.0 - 0.005
    
    # Control panel bezel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, panel_y, panel_z))
    ctrl_panel = bpy.context.active_object
    ctrl_panel.name = "StoveControlPanel"
    ctrl_panel.scale = (w - 0.004, 0.01, panel_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(ctrl_panel, width=0.002)
    utils.apply_material(ctrl_panel, body_mat)
    parts.append(ctrl_panel)
    
    # Place knobs corresponding to burners + oven control
    num_knobs = len(burner_coords) + 1
    knob_spacing = (w - 0.14) / max(1, num_knobs - 1)
    knob_start_x = - (w - 0.14) / 2.0
    
    for k in range(num_knobs):
        kx = knob_start_x + k * knob_spacing
        ky = panel_y - 0.008
        
        # Knob cylinder
        bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.012, location=(kx, ky, panel_z))
        knob = bpy.context.active_object
        knob.name = f"StoveKnob_{k}"
        knob.rotation_euler.x = math.radians(90)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_bevel(knob, width=0.0015)
        utils.apply_material(knob, knob_mat)
        parts.append(knob)
        
        # Knob indicator ridge
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(kx, ky - 0.006, panel_z + 0.006))
        ridge = bpy.context.active_object
        ridge.name = f"StoveKnobRidge_{k}"
        ridge.scale = (0.004, 0.004, 0.014)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(ridge, burner_metal)
        parts.append(ridge)

    # 6. Oven Compartment below Control Panel
    # Oven Door Frame
    door_w = w - 0.01
    door_h = panel_z - panel_h/2.0 - base_h - 0.015
    door_z = base_h + door_h / 2.0 + 0.005
    door_y = -d / 2.0 - 0.01
    door_thick = 0.035
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, door_y, door_z))
    door = bpy.context.active_object
    door.name = "StoveOvenDoor"
    door.scale = (door_w, door_thick, door_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(door, width=0.004)
    utils.apply_material(door, body_mat)
    parts.append(door)
    
    # Glass Window in the door
    win_w = door_w * 0.72
    win_h = door_h * 0.58
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, door_y - 0.004, door_z))
    window = bpy.context.active_object
    window.name = "StoveOvenWindow"
    window.scale = (win_w, door_thick + 0.002, win_h)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(window, glass_mat)
    parts.append(window)
    
    # Oven Door Handle (horizontal)
    hnd_z = door_z + door_h * 0.38
    hnd_y = door_y - 0.02
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, hnd_y, hnd_z))
    handle = bpy.context.active_object
    handle.name = "StoveOvenHandle"
    handle.scale = (door_w * 0.7, 0.016, 0.016)
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_bevel(handle, width=0.002)
    utils.apply_material(handle, handle_mat)
    parts.append(handle)
    
    # Handle mounts
    for hx in [-door_w * 0.3, door_w * 0.3]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx, (door_y + hnd_y)/2.0, hnd_z))
        mount = bpy.context.active_object
        mount.name = f"StoveOvenHandleMount_{hx}"
        mount.scale = (0.016, abs(door_y - hnd_y), 0.016)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(mount, handle_mat)
        parts.append(mount)

    # 7. Join all parts into one mesh
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = master_obj
    bpy.ops.object.join()

    master_obj.name = "StoveAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return master_obj

def main():
    parser = argparse.ArgumentParser(description="Procedural Stove Generator")
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
    stove_obj = generate_stove(params)
    
    if args.render:
        utils.setup_lighting_and_camera(stove_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
