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

def generate_sink(params):
    w = params.get("width", 80.0) / 100.0  # convert cm to meters
    d = params.get("depth", 60.0) / 100.0
    h = params.get("height", 85.0) / 100.0
    style = params.get("style", "single_basin")
    faucet_style = params.get("faucet_style", "goose_neck")

    parts = []

    # 1. Setup Materials
    counter_mat = utils.create_material("SinkCounter", diffuse_color=(0.9, 0.9, 0.9, 1.0), metallic=0.1, roughness=0.1) # Light Stone
    wood_mat = utils.create_material("SinkCabinetWood", diffuse_color=(0.35, 0.18, 0.08, 1.0), metallic=0.0, roughness=0.7) # Mahogany cabinet
    chrome_mat = utils.create_material("SinkChrome", diffuse_color=(0.8, 0.8, 0.82, 1.0), metallic=0.95, roughness=0.15) # Faucet/Basin
    drain_mat = utils.create_material("SinkDrain", diffuse_color=(0.15, 0.15, 0.16, 1.0), metallic=0.8, roughness=0.4)
    interior_basin_mat = utils.create_material("SinkInteriorBasin", diffuse_color=(0.4, 0.4, 0.42, 1.0), metallic=0.9, roughness=0.25)

    porcelain_mat = utils.create_material("SinkPorcelain", diffuse_color=(0.95, 0.95, 0.95, 1.0), metallic=0.0, roughness=0.1)

    if style in ["pedestal", "wall_mounted"]:
        # PORCELAIN BATHROOM BASIN (Freestanding / Wall-mounted)
        basin_h = 0.22
        basin_z = h - basin_h / 2.0
        
        # Main Basin Block (with rounded corners via bevel)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, basin_z))
        basin = bpy.context.active_object
        basin.name = "BathroomBasin"
        basin.scale = (w, d, basin_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(basin, width=0.03, segments=5) # nice rounded basin edges
        utils.apply_material(basin, porcelain_mat)
        parts.append(basin)
        master_obj = basin

        # Basin Inner Cavity
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.02, basin_z + 0.01))
        inner = bpy.context.active_object
        inner.name = "BathroomBasinInner"
        inner.scale = (w - 0.06, d - 0.10, basin_h - 0.02)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(inner, width=0.02, segments=3)
        utils.apply_material(inner, interior_basin_mat)
        parts.append(inner)

        # Drain
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.002, location=(0, -0.02, basin_z - basin_h/2.0 + 0.012))
        drain = bpy.context.active_object
        drain.name = "BathroomSinkDrain"
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(drain, drain_mat)
        parts.append(drain)

        # Plug
        bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.003, location=(0, -0.02, basin_z - basin_h/2.0 + 0.013))
        plug = bpy.context.active_object
        plug.name = "BathroomSinkPlug"
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(plug, chrome_mat)
        parts.append(plug)

        if style == "pedestal":
            # Pedestal column support
            ped_h = h - basin_h
            bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.0, location=(0, -0.02, ped_h / 2.0))
            ped = bpy.context.active_object
            ped.name = "SinkPedestal"
            ped.scale = (0.12, 0.12, ped_h) # cylindrical column
            
            # Apply a manual taper to the vertices of the column
            for v in ped.data.vertices:
                local_z = v.co.z
                # factor ranges from 1.0 in middle to 1.3 at ends
                factor = 1.0 + 0.3 * (local_z ** 2)
                v.co.x *= factor
                v.co.y *= factor
                
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_smooth_by_angle(ped)
            utils.apply_material(ped, porcelain_mat)
            parts.append(ped)
            
        elif style == "wall_mounted":
            # Wall mount support brackets underneath
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-w/4.0, d/4.0, basin_z - basin_h/2.0 - 0.02))
            bracket_l = bpy.context.active_object
            bracket_l.name = "BracketL"
            bracket_l.scale = (0.04, d/2.0, 0.04)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(bracket_l, chrome_mat)
            parts.append(bracket_l)

            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(w/4.0, d/4.0, basin_z - basin_h/2.0 - 0.02))
            bracket_r = bpy.context.active_object
            bracket_r.name = "BracketR"
            bracket_r.scale = (0.04, d/2.0, 0.04)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(bracket_r, chrome_mat)
            parts.append(bracket_r)

            # Exposed Chrome Pipes (P-Trap drain)
            # Vertical down-pipe
            pipe_v_h = 0.25
            bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=pipe_v_h, location=(0, -0.02, basin_z - basin_h/2.0 - pipe_v_h/2.0))
            pipe_v = bpy.context.active_object
            pipe_v.name = "ExposedPipeV"
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_smooth_by_angle(pipe_v)
            utils.apply_material(pipe_v, chrome_mat)
            parts.append(pipe_v)

            # Trap curve (horizontal connection to wall)
            trap_y = (-0.02 + d/2.0) / 2.0
            trap_len = d/2.0 + 0.02
            bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=trap_len, location=(0, trap_y, basin_z - basin_h/2.0 - pipe_v_h))
            pipe_h_obj = bpy.context.active_object
            pipe_h_obj.name = "ExposedPipeH"
            pipe_h_obj.rotation_euler.x = math.radians(90.0)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            utils.apply_smooth_by_angle(pipe_h_obj)
            utils.apply_material(pipe_h_obj, chrome_mat)
            parts.append(pipe_h_obj)

    else:
        # COUNTERTOP CABINET STYLE (Existing Code, Single/Double Basin)
        counter_thick = 0.04
        cabinet_h = h - counter_thick
        cabinet_z = cabinet_h / 2.0
        kicker_h = 0.08

        # 2. Base Cabinet Carcass
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, cabinet_z))
        carcass = bpy.context.active_object
        carcass.name = "SinkCabinet"
        carcass.scale = (w, d, cabinet_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(carcass, width=0.005)
        utils.apply_material(carcass, wood_mat)
        parts.append(carcass)
        master_obj = carcass

        # Bottom recessed kickplate
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.015, kicker_h / 2.0))
        kickplate = bpy.context.active_object
        kickplate.name = "SinkKickplate"
        kickplate.scale = (w - 0.02, d - 0.03, kicker_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(kickplate, drain_mat)
        parts.append(kickplate)

        # Cabinet double doors (Front face cupboard doors)
        door_w = w / 2.0 - 0.004
        door_h = cabinet_h - kicker_h - 0.02
        door_z = kicker_h + door_h / 2.0 + 0.01
        door_y = -d / 2.0 - 0.008
        door_thick = 0.018

        # Left Door
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-door_w/2.0 - 0.001, door_y, door_z))
        door_l = bpy.context.active_object
        door_l.name = "SinkDoorL"
        door_l.scale = (door_w, door_thick, door_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(door_l, width=0.002)
        utils.apply_material(door_l, wood_mat)
        parts.append(door_l)

        # Right Door
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(door_w/2.0 + 0.001, door_y, door_z))
        door_r = bpy.context.active_object
        door_r.name = "SinkDoorR"
        door_r.scale = (door_w, door_thick, door_h)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(door_r, width=0.002)
        utils.apply_material(door_r, wood_mat)
        parts.append(door_r)

        # Silver door handles
        handle_y = door_y - 0.01
        for dx in [-0.02, 0.02]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, handle_y, door_z + door_h*0.2))
            hnd = bpy.context.active_object
            hnd.name = "SinkDoorHandle"
            hnd.scale = (0.012, 0.01, 0.12)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_bevel(hnd, width=0.001)
            utils.apply_material(hnd, chrome_mat)
            parts.append(hnd)
            
            # Mounts
            for mz in [door_z + door_h*0.25, door_z + door_h*0.15]:
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, (door_y + handle_y)/2.0, mz))
                mnt = bpy.context.active_object
                mnt.scale = (0.012, abs(door_y - handle_y), 0.01)
                bpy.ops.object.transform_apply(scale=True)
                utils.apply_material(mnt, chrome_mat)
                parts.append(mnt)

        # 3. Top Countertop Slab
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, h - counter_thick/2.0))
        countertop = bpy.context.active_object
        countertop.name = "SinkCountertop"
        countertop.scale = (w, d, counter_thick)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(countertop, width=0.004)
        utils.apply_material(countertop, counter_mat)
        parts.append(countertop)

        # 4. Undermount Basin Bowl(s)
        basin_h = 0.22
        basin_z = h - counter_thick - basin_h/2.0 + 0.002
        basin_d = d * 0.72
        basin_y = 0.0  # Centered in depth
        
        basins = []
        if style == "double_basin":
            basin_w = (w * 0.76 - 0.025) / 2.0
            basins = [
                (-basin_w/2.0 - 0.012, basin_w),
                (basin_w/2.0 + 0.012, basin_w)
            ]
        else: # single_basin
            basin_w = w * 0.76
            basins = [(0.0, basin_w)]

        for idx, (bx, bw) in enumerate(basins):
            # Outer Basin Frame
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, basin_y, basin_z))
            basin_outer = bpy.context.active_object
            basin_outer.name = f"SinkBasinOuter_{idx}"
            basin_outer.scale = (bw, basin_d, basin_h)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(basin_outer, chrome_mat)
            parts.append(basin_outer)
            
            # Inner Cavity (Hollowed interior dark box)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, basin_y, basin_z + 0.005))
            basin_inner = bpy.context.active_object
            basin_inner.name = f"SinkBasinInner_{idx}"
            basin_inner.scale = (bw - 0.016, basin_d - 0.016, basin_h - 0.005)
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(basin_inner, interior_basin_mat)
            parts.append(basin_inner)
            
            # Drain flange at bottom
            bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.002, location=(bx, basin_y, basin_z - basin_h/2.0 + 0.006))
            drain = bpy.context.active_object
            drain.name = f"SinkDrain_{idx}"
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(drain, drain_mat)
            parts.append(drain)

            # Chrome center plug
            bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.003, location=(bx, basin_y, basin_z - basin_h/2.0 + 0.007))
            plug = bpy.context.active_object
            plug.name = f"SinkPlug_{idx}"
            bpy.ops.object.transform_apply(scale=True)
            utils.apply_material(plug, chrome_mat)
            parts.append(plug)

    # 5. Faucet System (Centered at the back rim)
    faucet_y = d/2.0 - 0.05
    faucet_z = h  # resting on countertop

    # Faucet base collar
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.012, location=(0.0, faucet_y, faucet_z + 0.006))
    faucet_base = bpy.context.active_object
    faucet_base.name = "FaucetBase"
    bpy.ops.object.transform_apply(scale=True)
    utils.apply_material(faucet_base, chrome_mat)
    parts.append(faucet_base)

    if faucet_style == "goose_neck":
        # Tall curved goose neck spout
        # Vertical pipe
        v_h = 0.2
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=v_h, location=(0.0, faucet_y, faucet_z + 0.01 + v_h/2.0))
        f_vert = bpy.context.active_object
        f_vert.name = "FaucetGooseVert"
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(f_vert, chrome_mat)
        parts.append(f_vert)

        # Curved elbow / horizontal curve (extending forward)
        c_w = 0.12
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=c_w, location=(0.0, faucet_y - c_w/2.0, faucet_z + 0.01 + v_h + 0.006))
        f_horiz = bpy.context.active_object
        f_horiz.name = "FaucetGooseHoriz"
        f_horiz.rotation_euler.x = math.radians(90)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_material(f_horiz, chrome_mat)
        parts.append(f_horiz)

        # Downward spout nozzle
        n_h = 0.05
        bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=n_h, location=(0.0, faucet_y - c_w, faucet_z + 0.01 + v_h - n_h/2.0))
        f_nozzle = bpy.context.active_object
        f_nozzle.name = "FaucetGooseNozzle"
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(f_nozzle, chrome_mat)
        parts.append(f_nozzle)
    else:
        # Standard faucet: boxy angled lever faucet spout
        f_w = 0.025
        f_h = 0.14
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, faucet_y - 0.03, faucet_z + 0.04))
        spout = bpy.context.active_object
        spout.name = "FaucetStandardSpout"
        spout.scale = (f_w, 0.08, f_h)
        spout.rotation_euler.x = math.radians(20) # Angled slightly forward
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        utils.apply_bevel(spout, width=0.002)
        utils.apply_material(spout, chrome_mat)
        parts.append(spout)

    # Left & Right faucet levers/valves
    for sx in [-0.06, 0.06]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.015, location=(sx, faucet_y, faucet_z + 0.0075))
        valve = bpy.context.active_object
        valve.name = "FaucetValveBase"
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_material(valve, chrome_mat)
        parts.append(valve)

        # Small lever handles
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sx, faucet_y - 0.015, faucet_z + 0.015))
        lever = bpy.context.active_object
        lever.name = "FaucetValveLever"
        lever.scale = (0.008, 0.035, 0.008)
        bpy.ops.object.transform_apply(scale=True)
        utils.apply_bevel(lever, width=0.001)
        utils.apply_material(lever, chrome_mat)
        parts.append(lever)

    # Join all sink parts into a single mesh
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = master_obj
    bpy.ops.object.join()

    master_obj.name = "SinkAsset"
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    return master_obj

def main():
    parser = argparse.ArgumentParser(description="Procedural Sink Generator")
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
    sink_obj = generate_sink(params)
    
    if args.render:
        utils.setup_lighting_and_camera(sink_obj)
        utils.render_preview(args.render)
        
    utils.export_glb(args.export)

if __name__ == "__main__":
    main()
