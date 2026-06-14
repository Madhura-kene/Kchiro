import os
import sys
import pytest

# Dynamic path resolution to find backend
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.blender_executor import BlenderExecutor

def test_blender_executor_table():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "table.py")
    
    # Parameters for table.py (in centimeters)
    params = {
        "asset_type": "table",
        "width": 100.0,
        "depth": 80.0,
        "height": 75.0,
        "leg_style": "round"
    }
    
    export_path = os.path.join(project_root, "exports", "test_table.glb")
    render_path = os.path.join(project_root, "renders", "test_table.png")
    
    # Remove existing files if any
    for path in [export_path, render_path]:
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass
            
    success, logs = executor.execute_generator(
        generator_script=generator_script,
        params=params,
        export_path=export_path,
        render_path=render_path
    )
    
    assert success, f"Blender execution failed with logs:\n{logs}"
    assert os.path.exists(export_path), "GLB export file was not created"
    assert os.path.exists(render_path), "PNG preview render was not created"
    
    # Clean up test outputs
    if os.path.exists(export_path):
        os.remove(export_path)
    if os.path.exists(render_path):
        os.remove(render_path)

if __name__ == "__main__":
    pytest.main([__file__])
