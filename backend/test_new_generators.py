import os
import sys
import pytest

# Dynamic path resolution to find backend
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.blender_executor import BlenderExecutor

def test_blender_executor_shield():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "shield.py")
    
    # Shield params
    params = {
        "asset_type": "shield",
        "shield_style": "heater",
        "diameter": 60.0,
        "boss_material": "brass",
        "has_rim": True
    }
    
    export_path = os.path.join(project_root, "exports", "test_shield.glb")
    render_path = os.path.join(project_root, "renders", "test_shield.png")
    
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
    
    assert success, f"Shield generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Shield GLB export failed"
    assert os.path.exists(render_path), "Shield PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_chair():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "chair.py")
    
    # Chair params
    params = {
        "asset_type": "chair",
        "width": 50.0,
        "depth": 50.0,
        "seat_height": 45.0,
        "backrest_height": 50.0,
        "leg_style": "round"
    }
    
    export_path = os.path.join(project_root, "exports", "test_chair.glb")
    render_path = os.path.join(project_root, "renders", "test_chair.png")
    
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
    
    assert success, f"Chair generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Chair GLB export failed"
    assert os.path.exists(render_path), "Chair PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_chest():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "chest.py")
    
    # Chest params
    params = {
        "asset_type": "chest",
        "width": 80.0,
        "depth": 50.0,
        "height": 50.0,
        "lid_style": "arched",
        "has_lock": True
    }
    
    export_path = os.path.join(project_root, "exports", "test_chest.glb")
    render_path = os.path.join(project_root, "renders", "test_chest.png")
    
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
    
    assert success, f"Chest generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Chest GLB export failed"
    assert os.path.exists(render_path), "Chest PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_axe():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "axe.py")
    
    # Axe params
    params = {
        "asset_type": "axe",
        "shaft_length": 80.0,
        "axe_style": "double",
        "head_material": "steel",
        "shaft_material": "wood"
    }
    
    export_path = os.path.join(project_root, "exports", "test_axe.glb")
    render_path = os.path.join(project_root, "renders", "test_axe.png")
    
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
    
    assert success, f"Axe generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Axe GLB export failed"
    assert os.path.exists(render_path), "Axe PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_helmet():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "helmet.py")
    
    # Helmet params
    params = {
        "asset_type": "helmet",
        "style": "knight",
        "material": "steel",
        "has_crest": True
    }
    
    export_path = os.path.join(project_root, "exports", "test_helmet.glb")
    render_path = os.path.join(project_root, "renders", "test_helmet.png")
    
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
    
    assert success, f"Helmet generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Helmet GLB export failed"
    assert os.path.exists(render_path), "Helmet PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_torch():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "torch.py")
    
    # Torch params
    params = {
        "asset_type": "torch",
        "style": "wall_mounted",
        "shaft_length": 40.0,
        "flame_size": 15.0
    }
    
    export_path = os.path.join(project_root, "exports", "test_torch.glb")
    render_path = os.path.join(project_root, "renders", "test_torch.png")
    
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
    
    assert success, f"Torch generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Torch GLB export failed"
    assert os.path.exists(render_path), "Torch PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_sofa():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "sofa.py")
    
    # Sofa params
    params = {
        "asset_type": "sofa",
        "style": "couch",
        "width": 180.0,
        "depth": 90.0,
        "has_armrests": True
    }
    
    export_path = os.path.join(project_root, "exports", "test_sofa.glb")
    render_path = os.path.join(project_root, "renders", "test_sofa.png")
    
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
    
    assert success, f"Sofa generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Sofa GLB export failed"
    assert os.path.exists(render_path), "Sofa PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_bench():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "bench.py")
    
    params = {
        "asset_type": "bench",
        "width": 120.0,
        "depth": 40.0,
        "height": 45.0,
        "has_backrest": True,
        "leg_style": "x_frame",
        "material": "metal"
    }
    
    export_path = os.path.join(project_root, "exports", "test_bench.glb")
    render_path = os.path.join(project_root, "renders", "test_bench.png")
    
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
    
    assert success, f"Bench generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Bench GLB export failed"
    assert os.path.exists(render_path), "Bench PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_couch():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "couch.py")
    
    params = {
        "asset_type": "couch",
        "width": 200.0,
        "depth": 90.0,
        "height": 85.0,
        "has_chaise": True,
        "material": "leather"
    }
    
    export_path = os.path.join(project_root, "exports", "test_couch.glb")
    render_path = os.path.join(project_root, "renders", "test_couch.png")
    
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
    
    assert success, f"Couch generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Couch GLB export failed"
    assert os.path.exists(render_path), "Couch PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_armchair():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "armchair.py")
    
    params = {
        "asset_type": "armchair",
        "width": 85.0,
        "depth": 80.0,
        "height": 85.0,
        "style": "recliner",
        "material": "velvet"
    }
    
    export_path = os.path.join(project_root, "exports", "test_armchair.glb")
    render_path = os.path.join(project_root, "renders", "test_armchair.png")
    
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
    
    assert success, f"Armchair generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Armchair GLB export failed"
    assert os.path.exists(render_path), "Armchair PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_bed():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "bed.py")
    
    params = {
        "asset_type": "bed",
        "width": 160.0,
        "depth": 200.0,
        "height": 60.0,
        "has_headboard": True,
        "material": "wood"
    }
    
    export_path = os.path.join(project_root, "exports", "test_bed.glb")
    render_path = os.path.join(project_root, "renders", "test_bed.png")
    
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
    
    assert success, f"Bed generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Bed GLB export failed"
    assert os.path.exists(render_path), "Bed PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_bunk_bed():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "bunk_bed.py")
    
    params = {
        "asset_type": "bunk_bed",
        "width": 100.0,
        "depth": 200.0,
        "height": 180.0,
        "has_ladder": True,
        "material": "wood"
    }
    
    export_path = os.path.join(project_root, "exports", "test_bunk_bed.glb")
    render_path = os.path.join(project_root, "renders", "test_bunk_bed.png")
    
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
    
    assert success, f"Bunk bed generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Bunk bed GLB export failed"
    assert os.path.exists(render_path), "Bunk bed PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_wardrobe():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "wardrobe.py")
    
    params = {
        "asset_type": "wardrobe",
        "width": 120.0,
        "depth": 60.0,
        "height": 190.0,
        "style": "classic",
        "has_mirror": True
    }
    
    export_path = os.path.join(project_root, "exports", "test_wardrobe.glb")
    render_path = os.path.join(project_root, "renders", "test_wardrobe.png")
    
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
    
    assert success, f"Wardrobe generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Wardrobe GLB export failed"
    assert os.path.exists(render_path), "Wardrobe PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_storage():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "storage.py")
    
    # Storage params
    params = {
        "asset_type": "storage",
        "style": "bookcase",
        "width": 100.0,
        "depth": 40.0,
        "height": 160.0,
        "num_shelves": 4,
        "has_doors": False
    }
    
    export_path = os.path.join(project_root, "exports", "test_storage.glb")
    render_path = os.path.join(project_root, "renders", "test_storage.png")
    
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
    
    assert success, f"Storage generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Storage GLB export failed"
    assert os.path.exists(render_path), "Storage PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_lighting():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "lighting.py")
    
    # Lighting params
    params = {
        "asset_type": "lighting",
        "style": "lamp",
        "height": 120.0,
        "is_lit": True
    }
    
    export_path = os.path.join(project_root, "exports", "test_lighting.glb")
    render_path = os.path.join(project_root, "renders", "test_lighting.png")
    
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
    
    assert success, f"Lighting generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Lighting GLB export failed"
    assert os.path.exists(render_path), "Lighting PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_closet():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "closet.py")
    
    params = {
        "asset_type": "closet",
        "width": 150.0,
        "depth": 65.0,
        "height": 200.0,
        "door_style": "sliding",
        "doors": 2,
        "material": "dark_oak"
    }
    
    export_path = os.path.join(project_root, "exports", "test_closet.glb")
    render_path = os.path.join(project_root, "renders", "test_closet.png")
    
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
    
    assert success, f"Closet generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Closet GLB export failed"
    assert os.path.exists(render_path), "Closet PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_dresser():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "dresser.py")
    
    params = {
        "asset_type": "dresser",
        "width": 120.0,
        "depth": 50.0,
        "height": 90.0,
        "drawers_rows": 3,
        "drawers_cols": 2,
        "style": "classic"
    }
    
    export_path = os.path.join(project_root, "exports", "test_dresser.glb")
    render_path = os.path.join(project_root, "renders", "test_dresser.png")
    
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
    
    assert success, f"Dresser generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Dresser GLB export failed"
    assert os.path.exists(render_path), "Dresser PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_cabinet():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "cabinet.py")
    
    params = {
        "asset_type": "cabinet",
        "width": 80.0,
        "depth": 40.0,
        "height": 120.0,
        "has_glass": True,
        "shelves": 3,
        "style": "display"
    }
    
    export_path = os.path.join(project_root, "exports", "test_cabinet.glb")
    render_path = os.path.join(project_root, "renders", "test_cabinet.png")
    
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
    
    assert success, f"Cabinet generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Cabinet GLB export failed"
    assert os.path.exists(render_path), "Cabinet PNG render failed"
    
    # Clean up
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_shelf():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "shelf.py")
    params = {
        "asset_type": "shelf",
        "width": 80.0,
        "depth": 25.0,
        "height": 20.0,
        "material": "wood",
        "brackets": "floating"
    }
    export_path = os.path.join(project_root, "exports", "test_shelf.glb")
    render_path = os.path.join(project_root, "renders", "test_shelf.png")
    
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
    assert success, f"Shelf generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Shelf GLB export failed"
    assert os.path.exists(render_path), "Shelf PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_bookcase():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "bookcase.py")
    params = {
        "asset_type": "bookcase",
        "width": 90.0,
        "depth": 35.0,
        "height": 180.0,
        "shelves": 4,
        "has_back_panel": True,
        "material": "metal_frame"
    }
    export_path = os.path.join(project_root, "exports", "test_bookcase.glb")
    render_path = os.path.join(project_root, "renders", "test_bookcase.png")
    
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
    assert success, f"Bookcase generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Bookcase GLB export failed"
    assert os.path.exists(render_path), "Bookcase PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_nightstand():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "nightstand.py")
    params = {
        "asset_type": "nightstand",
        "width": 50.0,
        "depth": 40.0,
        "height": 60.0,
        "drawers": 2,
        "has_open_shelf": True,
        "style": "mid_century"
    }
    export_path = os.path.join(project_root, "exports", "test_nightstand.glb")
    render_path = os.path.join(project_root, "renders", "test_nightstand.png")
    
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
    assert success, f"Nightstand generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Nightstand GLB export failed"
    assert os.path.exists(render_path), "Nightstand PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_tv_stand():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "tv_stand.py")
    params = {
        "asset_type": "tv_stand",
        "width": 150.0,
        "depth": 45.0,
        "height": 50.0,
        "compartments": 3,
        "has_doors": True,
        "style": "modern"
    }
    export_path = os.path.join(project_root, "exports", "test_tv_stand.glb")
    render_path = os.path.join(project_root, "renders", "test_tv_stand.png")
    
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
    assert success, f"TV Stand generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "TV Stand GLB export failed"
    assert os.path.exists(render_path), "TV Stand PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_fridge():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "fridge.py")
    params = {
        "asset_type": "fridge",
        "width": 75.0,
        "depth": 70.0,
        "height": 180.0,
        "style": "double_door",
        "material": "stainless_steel",
        "has_dispenser": True
    }
    export_path = os.path.join(project_root, "exports", "test_fridge.glb")
    render_path = os.path.join(project_root, "renders", "test_fridge.png")
    
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
    assert success, f"Fridge generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Fridge GLB export failed"
    assert os.path.exists(render_path), "Fridge PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_stove():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "stove.py")
    params = {
        "asset_type": "stove",
        "width": 75.0,
        "depth": 60.0,
        "height": 90.0,
        "burners": 4,
        "style": "gas",
        "material": "stainless_steel"
    }
    export_path = os.path.join(project_root, "exports", "test_stove.glb")
    render_path = os.path.join(project_root, "renders", "test_stove.png")
    
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
    assert success, f"Stove generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Stove GLB export failed"
    assert os.path.exists(render_path), "Stove PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_oven():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "oven.py")
    params = {
        "asset_type": "oven",
        "width": 60.0,
        "depth": 55.0,
        "height": 60.0,
        "has_glass_window": True,
        "shelves": 2,
        "style": "built_in"
    }
    export_path = os.path.join(project_root, "exports", "test_oven.glb")
    render_path = os.path.join(project_root, "renders", "test_oven.png")
    
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
    assert success, f"Oven generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Oven GLB export failed"
    assert os.path.exists(render_path), "Oven PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_microwave():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "microwave.py")
    params = {
        "asset_type": "microwave",
        "width": 55.0,
        "depth": 40.0,
        "height": 35.0,
        "style": "countertop",
        "has_glass_door": True
    }
    export_path = os.path.join(project_root, "exports", "test_microwave.glb")
    render_path = os.path.join(project_root, "renders", "test_microwave.png")
    
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
    assert success, f"Microwave generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Microwave GLB export failed"
    assert os.path.exists(render_path), "Microwave PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_sink():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "sink.py")
    params = {
        "asset_type": "sink",
        "width": 80.0,
        "depth": 60.0,
        "height": 85.0,
        "style": "single_basin",
        "faucet_style": "goose_neck"
    }
    export_path = os.path.join(project_root, "exports", "test_sink.glb")
    render_path = os.path.join(project_root, "renders", "test_sink.png")
    
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
    assert success, f"Sink generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Sink GLB export failed"
    assert os.path.exists(render_path), "Sink PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_countertop():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "countertop.py")
    params = {
        "asset_type": "countertop",
        "width": 120.0,
        "depth": 60.0,
        "height": 90.0,
        "has_drawers": True,
        "has_backsplash": True,
        "material": "marble"
    }
    export_path = os.path.join(project_root, "exports", "test_countertop.glb")
    render_path = os.path.join(project_root, "renders", "test_countertop.png")
    
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
    assert success, f"Countertop generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Countertop GLB export failed"
    assert os.path.exists(render_path), "Countertop PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_cupboard():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "cupboard.py")
    params = {
        "asset_type": "cupboard",
        "width": 100.0,
        "depth": 45.0,
        "height": 180.0,
        "style": "hutch",
        "has_drawers": True,
        "shelves": 3
    }
    export_path = os.path.join(project_root, "exports", "test_cupboard.glb")
    render_path = os.path.join(project_root, "renders", "test_cupboard.png")
    
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
    assert success, f"Cupboard generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Cupboard GLB export failed"
    assert os.path.exists(render_path), "Cupboard PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_kitchen_island():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "kitchen_island.py")
    params = {
        "asset_type": "kitchen_island",
        "width": 160.0,
        "depth": 90.0,
        "height": 90.0,
        "overhang_depth": 25.0,
        "has_stools": True,
        "stools_count": 2,
        "material": "wood_marble"
    }
    export_path = os.path.join(project_root, "exports", "test_kitchen_island.glb")
    render_path = os.path.join(project_root, "renders", "test_kitchen_island.png")
    
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
    assert success, f"Kitchen Island generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Kitchen Island GLB export failed"
    assert os.path.exists(render_path), "Kitchen Island PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_dining_set():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "dining_set.py")
    params = {
        "asset_type": "dining_set",
        "table_width": 180.0,
        "table_depth": 90.0,
        "table_height": 75.0,
        "chair_count": 6,
        "chair_style": "classic",
        "material": "oak"
    }
    export_path = os.path.join(project_root, "exports", "test_dining_set.glb")
    render_path = os.path.join(project_root, "renders", "test_dining_set.png")
    
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
    assert success, f"Dining Set generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Dining Set GLB export failed"
    assert os.path.exists(render_path), "Dining Set PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_toilet():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "toilet.py")
    params = {
        "asset_type": "toilet",
        "width": 50.0,
        "depth": 70.0,
        "height": 80.0,
        "bowl_shape": "elongated",
        "has_lid_open": True,
        "tank_width": 45.0,
        "tank_depth": 20.0
    }
    export_path = os.path.join(project_root, "exports", "test_toilet.glb")
    render_path = os.path.join(project_root, "renders", "test_toilet.png")
    
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
    assert success, f"Toilet generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Toilet GLB export failed"
    assert os.path.exists(render_path), "Toilet PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_bathtub():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "bathtub.py")
    params = {
        "asset_type": "bathtub",
        "width": 160.0,
        "depth": 75.0,
        "height": 60.0,
        "style": "freestanding",
        "material": "ceramic",
        "has_faucet": True
    }
    export_path = os.path.join(project_root, "exports", "test_bathtub.glb")
    render_path = os.path.join(project_root, "renders", "test_bathtub.png")
    
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
    assert success, f"Bathtub generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Bathtub GLB export failed"
    assert os.path.exists(render_path), "Bathtub PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_shower():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "shower.py")
    params = {
        "asset_type": "shower",
        "width": 90.0,
        "depth": 90.0,
        "height": 210.0,
        "enclosure": "glass_door",
        "head_type": "standard",
        "material": "chrome"
    }
    export_path = os.path.join(project_root, "exports", "test_shower.glb")
    render_path = os.path.join(project_root, "renders", "test_shower.png")
    
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
    assert success, f"Shower generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Shower GLB export failed"
    assert os.path.exists(render_path), "Shower PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_mirror():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "mirror.py")
    params = {
        "asset_type": "mirror",
        "width": 60.0,
        "height": 80.0,
        "shape": "oval",
        "border_style": "metallic",
        "border_color": "gold"
    }
    export_path = os.path.join(project_root, "exports", "test_mirror.glb")
    render_path = os.path.join(project_root, "renders", "test_mirror.png")
    
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
    assert success, f"Mirror generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Mirror GLB export failed"
    assert os.path.exists(render_path), "Mirror PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_towel_rack():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "towel_rack.py")
    params = {
        "asset_type": "towel_rack",
        "width": 60.0,
        "depth": 15.0,
        "height": 20.0,
        "bar_style": "shelf_style",
        "material": "chrome",
        "has_towel": True,
        "towel_color": "blue"
    }
    export_path = os.path.join(project_root, "exports", "test_towel_rack.glb")
    render_path = os.path.join(project_root, "renders", "test_towel_rack.png")
    
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
    assert success, f"Towel rack generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Towel rack GLB export failed"
    assert os.path.exists(render_path), "Towel rack PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_sink_pedestal():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "sink.py")
    params = {
        "asset_type": "sink",
        "width": 70.0,
        "depth": 55.0,
        "height": 85.0,
        "style": "pedestal",
        "faucet_style": "standard"
    }
    export_path = os.path.join(project_root, "exports", "test_sink_ped.glb")
    render_path = os.path.join(project_root, "renders", "test_sink_ped.png")
    
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
    assert success, f"Pedestal Sink generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Pedestal Sink GLB export failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_sink_wall_mounted():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "sink.py")
    params = {
        "asset_type": "sink",
        "width": 70.0,
        "depth": 55.0,
        "height": 85.0,
        "style": "wall_mounted",
        "faucet_style": "goose_neck"
    }
    export_path = os.path.join(project_root, "exports", "test_sink_wall.glb")
    render_path = os.path.join(project_root, "renders", "test_sink_wall.png")
    
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
    assert success, f"Wall-mounted Sink generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Wall-mounted Sink GLB export failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_cabinet_bathroom():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "cabinet.py")
    params = {
        "asset_type": "cabinet",
        "width": 60.0,
        "depth": 35.0,
        "height": 100.0,
        "style": "bathroom",
        "shelves": 2,
        "has_glass": False
    }
    export_path = os.path.join(project_root, "exports", "test_cabinet_bath.glb")
    render_path = os.path.join(project_root, "renders", "test_cabinet_bath.png")
    
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
    assert success, f"Bathroom Cabinet generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Bathroom Cabinet GLB export failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_lamp():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "lamp.py")
    params = {
        "asset_type": "lamp",
        "height": 60.0,
        "style": "table",
        "shade_shape": "conical",
        "is_lit": True
    }
    export_path = os.path.join(project_root, "exports", "test_lamp.glb")
    render_path = os.path.join(project_root, "renders", "test_lamp.png")
    
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
    assert success, f"Lamp generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Lamp GLB export failed"
    assert os.path.exists(render_path), "Lamp PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_chandelier():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "chandelier.py")
    params = {
        "asset_type": "chandelier",
        "width": 80.0,
        "height": 70.0,
        "arms": 6,
        "style": "classic",
        "is_lit": True
    }
    export_path = os.path.join(project_root, "exports", "test_chandelier.glb")
    render_path = os.path.join(project_root, "renders", "test_chandelier.png")
    
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
    assert success, f"Chandelier generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Chandelier GLB export failed"
    assert os.path.exists(render_path), "Chandelier PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_painting():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "painting.py")
    params = {
        "asset_type": "painting",
        "width": 80.0,
        "height": 60.0,
        "frame_width": 3.0,
        "style": "landscape",
        "art_type": "abstract"
    }
    export_path = os.path.join(project_root, "exports", "test_painting.glb")
    render_path = os.path.join(project_root, "renders", "test_painting.png")
    
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
    assert success, f"Painting generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Painting GLB export failed"
    assert os.path.exists(render_path), "Painting PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_picture_frame():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "picture_frame.py")
    params = {
        "asset_type": "picture_frame",
        "width": 40.0,
        "height": 50.0,
        "border_thickness": 2.5,
        "style": "classic",
        "has_matting": True
    }
    export_path = os.path.join(project_root, "exports", "test_picture_frame.glb")
    render_path = os.path.join(project_root, "renders", "test_picture_frame.png")
    
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
    assert success, f"Picture Frame generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Picture Frame GLB export failed"
    assert os.path.exists(render_path), "Picture Frame PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_clock():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "clock.py")
    params = {
        "asset_type": "clock",
        "width": 40.0,
        "height": 40.0,
        "depth": 5.0,
        "shape": "circular",
        "style": "wall",
        "material": "wood"
    }
    export_path = os.path.join(project_root, "exports", "test_clock.glb")
    render_path = os.path.join(project_root, "renders", "test_clock.png")
    
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
    assert success, f"Clock generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Clock GLB export failed"
    assert os.path.exists(render_path), "Clock PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_vase():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "vase.py")
    params = {
        "asset_type": "vase",
        "height": 35.0,
        "diameter": 18.0,
        "neck_diameter": 6.0,
        "style": "classic",
        "material": "ceramic"
    }
    export_path = os.path.join(project_root, "exports", "test_vase.glb")
    render_path = os.path.join(project_root, "renders", "test_vase.png")
    
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
    assert success, f"Vase generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Vase GLB export failed"
    assert os.path.exists(render_path), "Vase PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_plant_pot():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "plant_pot.py")
    params = {
        "asset_type": "plant_pot",
        "width": 30.0,
        "depth": 30.0,
        "height": 30.0,
        "shape": "cylindrical",
        "material": "terracotta",
        "has_plant": True
    }
    export_path = os.path.join(project_root, "exports", "test_plant_pot.glb")
    render_path = os.path.join(project_root, "renders", "test_plant_pot.png")
    
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
    assert success, f"Plant Pot generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Plant Pot GLB export failed"
    assert os.path.exists(render_path), "Plant Pot PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

def test_blender_executor_rug():
    executor = BlenderExecutor()
    generator_script = os.path.join(project_root, "generators", "rug.py")
    params = {
        "asset_type": "rug",
        "width": 150.0,
        "depth": 100.0,
        "thickness": 1.2,
        "shape": "rectangular",
        "pattern": "geometric",
        "color": "cream"
    }
    export_path = os.path.join(project_root, "exports", "test_rug.glb")
    render_path = os.path.join(project_root, "renders", "test_rug.png")
    
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
    assert success, f"Rug generation failed with logs:\n{logs}"
    assert os.path.exists(export_path), "Rug GLB export failed"
    assert os.path.exists(render_path), "Rug PNG render failed"
    for path in [export_path, render_path]:
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    pytest.main([__file__])



