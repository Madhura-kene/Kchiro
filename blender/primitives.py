import sys
import os
import argparse

# Check if running inside Blender
try:
    import bpy
except ImportError:
    print("Error: This script must be run inside Blender's Python environment.")
    sys.exit(1)

def cleanup_scene():
    """Removes all default objects (cube, camera, light) from the startup scene."""
    # Ensure we are in object mode
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    
    # Select all meshes, cameras, and lights
    for obj in bpy.data.objects:
        obj.select_set(True)
        
    # Delete selected objects
    bpy.ops.object.delete()
    print("Scene cleaned up successfully.")

def generate_cube(size=2.0, location=(0, 0, 0)):
    """Generates a cube mesh."""
    print(f"Generating cube with size={size} at location={location}...")
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    # Get reference to the newly created object
    obj = bpy.context.active_object
    obj.name = "PrimitiveCube"
    return obj

def generate_cylinder(radius=1.0, depth=2.0, location=(0, 0, 0)):
    """Generates a cylinder mesh."""
    print(f"Generating cylinder with radius={radius}, depth={depth} at location={location}...")
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location)
    obj = bpy.context.active_object
    obj.name = "PrimitiveCylinder"
    return obj

def generate_plane(size=2.0, location=(0, 0, 0)):
    """Generates a plane mesh."""
    print(f"Generating plane with size={size} at location={location}...")
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = "PrimitivePlane"
    return obj

def export_glb(filepath):
    """Exports the current scene to a GLB file."""
    # Ensure export directory exists
    export_dir = os.path.dirname(filepath)
    if export_dir and not os.path.exists(export_dir):
        os.makedirs(export_dir, exist_ok=True)
        
    print(f"Exporting scene to glTF/GLB: {filepath} ...")
    # Call the export operator
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=False
    )
    print("Export complete.")

def main():
    # Find arguments after '--'
    try:
        args_idx = sys.argv.index("--")
        script_args = sys.argv[args_idx + 1:]
    except ValueError:
        script_args = []

    parser = argparse.ArgumentParser(description="Generate 3D primitives in Blender headlessly.")
    parser.add_argument("--type", type=str, required=True, choices=["cube", "cylinder", "plane"], help="Type of primitive to generate")
    parser.add_argument("--size", type=float, default=2.0, help="Size of cube or plane")
    parser.add_argument("--radius", type=float, default=1.0, help="Radius of cylinder")
    parser.add_argument("--depth", type=float, default=2.0, help="Depth/height of cylinder")
    parser.add_argument("--x", type=float, default=0.0, help="X position")
    parser.add_argument("--y", type=float, default=0.0, help="Y position")
    parser.add_argument("--z", type=float, default=0.0, help="Z position")
    parser.add_argument("--export", type=str, required=True, help="Filepath for the exported GLB file")

    args = parser.parse_args(script_args)

    # 1. Clean the default startup scene
    cleanup_scene()

    # 2. Generate geometry based on type
    location = (args.x, args.y, args.z)
    if args.type == "cube":
        generate_cube(size=args.size, location=location)
    elif args.type == "cylinder":
        generate_cylinder(radius=args.radius, depth=args.depth, location=location)
    elif args.type == "plane":
        generate_plane(size=args.size, location=location)

    # 3. Export to GLB
    export_glb(args.export)

if __name__ == "__main__":
    main()
