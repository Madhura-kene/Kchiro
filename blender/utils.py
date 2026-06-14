import os
import sys
try:
    import bpy
    import mathutils
except ImportError:
    pass

def cleanup_scene():
    """Removes all default objects (cube, camera, light) from the startup scene."""
    if 'bpy' not in sys.modules:
        return
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        obj.select_set(True)
    bpy.ops.object.delete()
    
    # Delete unused materials and meshes to keep files clean
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

def create_material(name, diffuse_color=(0.8, 0.8, 0.8, 1.0), metallic=0.0, roughness=0.5):
    """Creates a new PBR material with the specified parameters, checking for custom color overrides."""
    # Check if a custom color is defined in the params JSON
    custom_color_hex = None
    try:
        import sys
        import json
        if "--params" in sys.argv:
            idx = sys.argv.index("--params")
            params_path = sys.argv[idx + 1]
            with open(params_path, 'r') as f:
                params = json.load(f)
                custom_color_hex = params.get("custom_color")
    except Exception:
        pass

    # If custom color exists and is a valid hex, parse it
    if custom_color_hex and isinstance(custom_color_hex, str) and custom_color_hex.startswith("#"):
        # We only override the color if the material is a primary material
        # (e.g., skip glass, soil, plants, ticks, lighting emission materials)
        lower_name = name.lower()
        secondary_keywords = ["glass", "soil", "stem", "leaf", "plant", "water", "flame", "ticks", "mirror", "fringe", "glow", "hands", "pin"]
        is_secondary = any(kw in lower_name for kw in secondary_keywords)
        
        if not is_secondary:
            try:
                hex_str = custom_color_hex.lstrip("#")
                r = int(hex_str[0:2], 16) / 255.0
                g = int(hex_str[2:4], 16) / 255.0
                b = int(hex_str[4:6], 16) / 255.0
                diffuse_color = (r, g, b, 1.0)
            except Exception:
                pass

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # Get the Principled BSDF node (default for new materials)
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        # Base Color (RGBA)
        bsdf.inputs['Base Color'].default_value = diffuse_color
        # Metallic
        bsdf.inputs['Metallic'].default_value = metallic
        # Roughness
        bsdf.inputs['Roughness'].default_value = roughness
        
    return mat

def apply_material(obj, mat):
    """Applies a material to an object."""
    if not obj.data.materials:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

def setup_lighting_and_camera(target_obj=None):
    """Sets up a three-point lighting rig and positions a camera to frame the target object."""
    import math as _math
    # Calculate approximate target center and height
    target_center = (0.0, 0.0, 0.0)
    target_height = 1.0
    if target_obj:
        # Use dimensions to offset target tracking point to middle of height
        dims = target_obj.dimensions
        target_center = (0.0, 0.0, dims.z / 2.0)
        target_height = dims.z
        
    # Scale camera distance based on the largest dimension for tight framing
    if target_obj:
        dims = target_obj.dimensions
        max_dim = max(dims.x, dims.y, dims.z)
        cam_dist = max_dim * 1.8   # tight framing
    else:
        cam_dist = 3.0
    cam_z = target_center[2]   # eye-level with mirror centre

    # 1. Add Camera — position directly in front (-Y direction for front-facing assets)
    bpy.ops.object.camera_add(location=(0.4 * cam_dist, -cam_dist, cam_z + cam_dist * 0.25))
    camera = bpy.context.active_object
    camera.name = "RenderCamera"
    bpy.context.scene.camera = camera

    # Camera Constraint to track target center using an empty
    if target_obj:
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=target_center)
        tracker_empty = bpy.context.active_object
        tracker_empty.name = "CameraTrackerEmpty"

        constraint = camera.constraints.new(type='TRACK_TO')
        constraint.target = tracker_empty
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'
    
    # 2. Add Sun/Key Light
    bpy.ops.object.light_add(type='SUN', radius=1.0, location=(4, -4, 5))
    key_light = bpy.context.active_object
    key_light.name = "KeyLight"
    key_light.data.energy = 5.0
    key_light.data.color = (1.0, 0.95, 0.9)  # Warm key
    
    # 3. Add Fill Light
    bpy.ops.object.light_add(type='POINT', location=(-3, -3, 2))
    fill_light = bpy.context.active_object
    fill_light.name = "FillLight"
    fill_light.data.energy = 200.0
    fill_light.data.color = (0.9, 0.95, 1.0)  # Cool fill
    
    # 4. Add Rim Light (backlight)
    bpy.ops.object.light_add(type='POINT', location=(0, 4, 3))
    rim_light = bpy.context.active_object
    rim_light.name = "RimLight"
    rim_light.data.energy = 150.0
    rim_light.data.color = (1.0, 1.0, 1.0)  # White rim

    # 5. Add front accent light so glass/metallic surfaces have highlights from camera side
    bpy.ops.object.light_add(type='AREA', location=(0, -cam_dist * 0.8, target_center[2]))
    front_light = bpy.context.active_object
    front_light.name = "FrontLight"
    front_light.data.energy = 300.0
    front_light.data.size = 2.0
    front_light.data.color = (1.0, 0.98, 0.95)
    front_light.rotation_euler = (_math.radians(90.0), 0, 0)

    # 6. World / environment background for reflections on metallic/glass surfaces
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg_nodes = world.node_tree.nodes
    bg_links = world.node_tree.links
    bg_nodes.clear()
    bg_node = bg_nodes.new(type='ShaderNodeBackground')
    bg_node.inputs['Color'].default_value = (0.25, 0.27, 0.32, 1.0)  # Warm grey room
    bg_node.inputs['Strength'].default_value = 1.5
    output_node = bg_nodes.new(type='ShaderNodeOutputWorld')
    bg_links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])

def render_preview(filepath):
    """Renders the current camera view and saves it as a PNG preview."""
    # Ensure absolute path for Blender's internal engine
    filepath = os.path.abspath(filepath)
    
    # Ensure folder exists
    render_dir = os.path.dirname(filepath)
    if render_dir and not os.path.exists(render_dir):
        os.makedirs(render_dir, exist_ok=True)
        
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = filepath
    
    # Use Cycles for accurate metallic / mirror reflections
    scene.render.engine = 'CYCLES'
    # CPU rendering (no GPU assumed in headless)
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True

    # Transparent background for clean asset previews
    scene.render.film_transparent = True
    
    # Render resolution
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    
    # Render the scene
    print(f"Rendering preview to: {filepath}...")
    bpy.ops.render.render(write_still=True)
    print("Render complete.")

def export_glb(filepath):
    """Exports the entire scene to a GLB file."""
    # Ensure absolute path
    filepath = os.path.abspath(filepath)
    
    export_dir = os.path.dirname(filepath)
    if export_dir and not os.path.exists(export_dir):
        os.makedirs(export_dir, exist_ok=True)
        
    print(f"Exporting GLB to: {filepath}...")
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=False
    )
    print("GLB export complete.")

def export_stl(filepath, objects=None):
    """Exports mesh objects to a binary STL file for 3D printing workflows."""
    filepath = os.path.abspath(filepath)

    export_dir = os.path.dirname(filepath)
    if export_dir and not os.path.exists(export_dir):
        os.makedirs(export_dir, exist_ok=True)

    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    mesh_objects = [obj for obj in (objects or bpy.data.objects) if obj and obj.type == 'MESH']
    if not mesh_objects:
        raise ValueError("No mesh objects available for STL export.")

    bpy.ops.object.select_all(action='DESELECT')
    for obj in mesh_objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = mesh_objects[0]

    print(f"Exporting STL to: {filepath}...")
    try:
        if hasattr(bpy.ops.wm, "stl_export"):
            bpy.ops.wm.stl_export(
                filepath=filepath,
                export_selected_objects=True,
                ascii_format=False,
            )
        else:
            raise AttributeError("wm.stl_export not available")
    except Exception:
        bpy.ops.export_mesh.stl(
            filepath=filepath,
            use_selection=True,
            ascii=False,
        )
    print("STL export complete.")

def apply_bevel(obj, width=0.01, segments=3):
    """Applies a bevel modifier to clean up sharp edges and catch light highlights."""
    if 'bpy' not in sys.modules:
        return
    # Deselect all and select target object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    # Add bevel modifier
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = width
    mod.segments = segments
    
    # Apply modifier (recommended for GLTF compatibility and clean hierarchy)
    bpy.ops.object.modifier_apply(modifier="Bevel")

def apply_smooth_by_angle(obj, angle=30.0):
    """Applies smooth shading and adds a Smooth By Angle modifier for clean smooth curves."""
    if 'bpy' not in sys.modules:
        return
    # Deselect all and select target object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    # Enable smooth shading on all polygons
    for poly in obj.data.polygons:
        poly.use_smooth = True
        
    # Add modifier
    try:
        import math
        mod = obj.modifiers.new(name="SmoothByAngle", type='SMOOTH_BY_ANGLE')
        mod.angle = math.radians(angle)
        bpy.ops.object.modifier_apply(modifier="SmoothByAngle")
    except Exception:
        # Fallback for older Blender versions
        if hasattr(obj.data, "use_auto_smooth"):
            obj.data.use_auto_smooth = True
            import math
            obj.data.auto_smooth_angle = math.radians(angle)
