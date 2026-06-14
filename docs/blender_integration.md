# Blender Command Line Integration Guide

This guide explains how to install Blender, run it headlessly (in background mode), and execute Python scripts using Blender's internal Python interpreter and the `bpy` module.

---

## 1. Installing Blender

kchiro requires a standard installation of Blender (version 3.6 or 4.x is recommended).

### Windows
1. Download the installer or zip from the [Blender Official Website](https://www.blender.org/download/).
2. Install it. By default, it installs to:
   `C:\Program Files\Blender Foundation\Blender <version>\` (e.g., `C:\Program Files\Blender Foundation\Blender 4.1\`).
3. Add the installation folder to your User/System **PATH** environment variable:
   - Search for "Edit the system environment variables" in Windows.
   - Click "Environment Variables...".
   - Under "System variables" or "User variables", find `Path` and click "Edit".
   - Click "New" and paste the path to your Blender executable (e.g., `C:\Program Files\Blender Foundation\Blender 4.1`).
   - Click "OK" on all windows to save.

---

## 2. Running Blender from the Command Line

Once added to your `PATH`, you can verify the installation by running:
```powershell
blender --version
```

### Running Headless (Background Mode)
To run Blender without opening its GUI, use the `--background` (or `-b`) flag:
```powershell
blender --background
```

---

## 3. Running `bpy` Scripts

Blender embeds its own Python environment containing the `bpy` (Blender Python) module. You cannot import `bpy` from a standard system Python environment; you must run your script *inside* Blender.

Use the `--python` (or `-P`) flag to run a Python script:
```powershell
blender --background --python path/to/script.py
```

### Passing Custom Arguments to Scripts
To pass arguments to your Python script, append them after a double dash `--`. Blender ignores everything after `--`, allowing your script's `sys.argv` parser to read them:
```powershell
blender --background --python path/to/script.py -- --type cube --size 2.0
```

---

## 4. Basic `bpy` Concept: Scene Cleanup
When Blender starts up, it automatically loads a default startup file containing a default cube, camera, and light source. Before generating any procedural meshes, we must clean these up to avoid exporting them in our final model.

```python
import bpy

def cleanup_scene():
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    # Select all mesh objects
    for obj in bpy.data.objects:
        if obj.type in ['MESH', 'CAMERA', 'LIGHT']:
            obj.select_set(True)
    # Delete selected objects
    bpy.ops.object.delete()
```

---

## 5. Exporting to GLB
To export the generated scene or specific objects to a `.glb` (glTF binary) file, use the built-in glTF export operator:

```python
import bpy

def export_glb(export_path):
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB',
        use_selection=False  # Exports the entire scene
    )
```
