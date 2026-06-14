import os
import sys
import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, Dict, List

# Path resolution to find other packages
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.prompt_processor import PromptProcessor
from backend.blender_executor import BlenderExecutor
from backend.room_exporter import RoomExporter
from backend.print_exporter import PrintExporter
from backend.city_exporter import CityExporter
from database.db import DatabaseManager

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KchiroApp")

app = FastAPI(title="kchiro API", version="1.0.0")

# CORS configuration to allow connections from local frontend server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure exports and renders directories exist
exports_dir = os.path.join(project_root, "exports")
renders_dir = os.path.join(project_root, "renders")
os.makedirs(exports_dir, exist_ok=True)
os.makedirs(renders_dir, exist_ok=True)

# Mount Static Files for direct asset retrieval
app.mount("/exports", StaticFiles(directory=exports_dir), name="exports")
app.mount("/renders", StaticFiles(directory=renders_dir), name="renders")

db = DatabaseManager()
prompt_processor = PromptProcessor()
executor = BlenderExecutor()
room_exporter = RoomExporter(executor=executor, exports_dir=exports_dir)
print_exporter = PrintExporter(executor=executor, exports_dir=exports_dir)
city_exporter = CityExporter(executor=executor, exports_dir=exports_dir)

class GenerateRequest(BaseModel):
    prompt: str
    custom_color: Optional[str] = None


class RoomAssetExportRequest(BaseModel):
    asset_id: int
    pos_x: float = 0.0
    pos_y: float = 0.0
    pos_z: float = 0.0
    rot_y: float = 0.0
    scale: float = 1.0
    custom_color: Optional[str] = None
    detail_colors: Dict[str, str] = Field(default_factory=dict)


class HouseConfigRequest(BaseModel):
    bedrooms: int = 2
    bathrooms: int = 2
    kitchens: int = 1
    livingRooms: int = 1
    diningRooms: int = 1
    attachBathroomToBedroom: bool = True
    ensuiteBathrooms: int = 1
    roadLanes: int = 2
    sidewalkWidth: float = 1.8
    setbackWidth: float = 2.4
    addCrosswalks: bool = True


class RoomExportRequest(BaseModel):
    wall_color: str = "#334155"
    wall_colors: Dict[str, str] = Field(default_factory=dict)
    layout_mode: str = "living"
    house_config: HouseConfigRequest = Field(default_factory=HouseConfigRequest)
    assets: List[RoomAssetExportRequest] = Field(default_factory=list)


class CityCellExportRequest(BaseModel):
    row: int
    col: int
    road: Optional[str] = None
    building: Optional[str] = None
    light: Optional[str] = None
    elevation: float = 0.0
    rotation: float = 0.0
    height_scale: float = 1.0


class CityExportRequest(BaseModel):
    grid_size: int = 20
    cell_size: float = 4.0
    rotoscope: bool = True
    cells: List[CityCellExportRequest] = Field(default_factory=list)

def run_blender_generation(asset_id: int, generator_path: str, params: dict):
    """Worker function executed in the background to generate files using Blender."""
    logger.info(f"Starting background generation for asset {asset_id}")
    
    # Define file names
    glb_filename = f"asset_{asset_id}.glb"
    png_filename = f"asset_{asset_id}.png"
    
    glb_path = os.path.join(exports_dir, glb_filename)
    png_path = os.path.join(renders_dir, png_filename)
    
    # Run the generator
    success, logs = executor.execute_generator(
        generator_script=generator_path,
        params=params,
        export_path=glb_path,
        render_path=png_path
    )
    
    if success:
        # Update database with file URLs relative to server root
        db.update_asset_success(
            asset_id=asset_id,
            glb_path=f"/exports/{glb_filename}",
            render_path=f"/renders/{png_filename}"
        )
        logger.info(f"Generation succeeded for asset {asset_id}")
    else:
        db.update_asset_failed(
            asset_id=asset_id,
            error_message=f"Blender failed: {logs}"
        )
        logger.error(f"Generation failed for asset {asset_id}: {logs}")


def get_completed_asset_with_glb(asset_id: int):
    asset = db.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail=f"Asset {asset_id} not found")
    if asset.get("status") != "completed" or not asset.get("glb_path"):
        raise HTTPException(status_code=400, detail=f"Asset {asset_id} is not ready for export")

    glb_file = os.path.abspath(os.path.join(project_root, asset["glb_path"].lstrip("/")))
    if not os.path.exists(glb_file):
        raise HTTPException(status_code=400, detail=f"GLB file missing for asset {asset_id}")

    return asset, glb_file


def build_room_export_manifest(req: RoomExportRequest):
    manifest_assets = []

    for placement in req.assets:
        asset, glb_file = get_completed_asset_with_glb(placement.asset_id)
        manifest_assets.append({
            "asset_id": placement.asset_id,
            "asset_type": asset["asset_type"],
            "prompt": asset.get("prompt", ""),
            "glb_file": glb_file,
            "pos_x": placement.pos_x,
            "pos_y": placement.pos_y,
            "pos_z": placement.pos_z,
            "rot_y": placement.rot_y,
            "scale": placement.scale,
            "custom_color": placement.custom_color,
            "detail_colors": placement.detail_colors,
        })

    return {
        "wall_color": req.wall_color,
        "wall_colors": req.wall_colors,
        "layout_mode": req.layout_mode,
        "house_config": req.house_config.model_dump(),
        "room_size": 3.0,
        "room_height": 2.0,
        "wall_thickness": 0.1,
        "assets": manifest_assets,
    }

@app.post("/api/generate")
async def generate_asset(req: GenerateRequest, background_tasks: BackgroundTasks):
    """Starts the asset generation pipeline.
    Validates parameters synchronously and initiates Blender execution asynchronously.
    """
    try:
        # 1. Process prompt using LLM & auto-repair units
        validated_params, generator_path = prompt_processor.process_prompt(req.prompt)
        params_dict = validated_params.model_dump()
        if req.custom_color:
            params_dict["custom_color"] = req.custom_color
        asset_type = validated_params.asset_type
        
        # 2. Create pending database entry
        asset_id = db.create_asset(
            prompt=req.prompt,
            asset_type=asset_type,
            parameters=params_dict
        )
        
        # 3. Queue headless Blender execution task
        background_tasks.add_task(
            run_blender_generation,
            asset_id=asset_id,
            generator_path=generator_path,
            params=params_dict
        )
        
        # Return current generation state
        return db.get_asset(asset_id)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during asset generation request")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/assets")
async def list_assets():
    """Lists all previously created/requested assets."""
    return db.get_assets()

@app.get("/api/assets/{asset_id}")
async def get_asset(asset_id: int):
    """Retrieves metadata of a specific asset."""
    asset = db.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@app.delete("/api/assets/{asset_id}")
async def delete_asset(asset_id: int):
    """Deletes an asset record and its generated GLB and render PNG files."""
    asset = db.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    # Delete GLB file
    if asset.get("glb_path"):
        glb_file = os.path.join(project_root, asset["glb_path"].lstrip("/"))
        if os.path.exists(glb_file):
            try:
                os.remove(glb_file)
            except Exception as e:
                logger.warning(f"Failed to delete {glb_file}: {e}")
                
    # Delete PNG preview file
    if asset.get("render_path"):
        render_file = os.path.join(project_root, asset["render_path"].lstrip("/"))
        if os.path.exists(render_file):
            try:
                os.remove(render_file)
            except Exception as e:
                logger.warning(f"Failed to delete {render_file}: {e}")
                
    deleted = db.delete_asset(asset_id)
    return {"success": deleted}


@app.post("/api/assets/{asset_id}/export-print")
async def export_asset_print(asset_id: int):
    """Builds a printable STL file for a previously generated asset."""
    _, glb_file = get_completed_asset_with_glb(asset_id)

    try:
        return print_exporter.export_asset_to_stl(asset_id=asset_id, glb_path=glb_file)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during asset STL export")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rooms/export-blend")
async def export_room_blend(req: RoomExportRequest):
    """Builds a Blender .blend file for the current room layout."""
    try:
        return room_exporter.export_room_to_blend(build_room_export_manifest(req))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during room export")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rooms/export-print")
async def export_room_print(req: RoomExportRequest):
    """Builds a printable STL file for the current room or house layout."""
    try:
        return room_exporter.export_room_to_stl(build_room_export_manifest(req))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during room export")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/city/export-blend")
async def export_city_blend(req: CityExportRequest):
    """Builds a Blender .blend file for the current 3D city planner layout."""
    try:
        return city_exporter.export_city_to_blend(req.model_dump())
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during city export")
        raise HTTPException(status_code=500, detail=str(e))
