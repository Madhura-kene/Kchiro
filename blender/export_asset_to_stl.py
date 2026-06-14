import os
import sys

import bpy


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from blender import utils


def parse_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1 :]
    else:
        argv = []

    input_path = None
    output_path = None
    for index, arg in enumerate(argv):
        if arg == "--input" and index + 1 < len(argv):
            input_path = argv[index + 1]
        if arg == "--output" and index + 1 < len(argv):
            output_path = argv[index + 1]

    if not input_path or not output_path:
        raise ValueError("Missing --input or --output argument.")

    return os.path.abspath(input_path), os.path.abspath(output_path)


def main():
    input_path, output_path = parse_args()
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Asset GLB not found: {input_path}")

    utils.cleanup_scene()
    bpy.ops.import_scene.gltf(filepath=input_path)
    utils.export_stl(output_path)
    print(f"Saved STL asset file to: {output_path}")


if __name__ == "__main__":
    main()
