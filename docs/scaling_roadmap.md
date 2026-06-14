# kchiro Scaling and Expansion Roadmap

This document outlines the architecture and blueprint for taking the kchiro MVP to a scalable, production-ready SaaS platform.

---

## 1. Adding New Asset Categories

To expand kchiro's catalog (e.g., adding Shields, Chests, Chairs, or Torches), follow this structured workflow:

### Step 1: Define the Pydantic Schema
Add a new schema model to `schemas/asset_schemas.py` with strict field types, ranges, and defaults.
```python
class ShieldSchema(BaseModel):
    asset_type: Literal["shield"]
    style: Literal["heater", "kite", "round"] = "round"
    width: float = Field(default=60.0, ge=30.0, le=100.0) # in cm
    height: float = Field(default=60.0, ge=30.0, le=120.0) # in cm
    boss_material: Literal["steel", "brass", "wood"] = "steel"
```

### Step 2: Implement the Procedural Generator
Create a new generator script (e.g., `shield.py`) in the `generators/` directory. Use `blender/utils.py` primitives and styling functions.
```python
def generate_shield(params):
    # Retrieve parameters, create materials, build meshes, apply bevels, and join parts
    pass
```

### Step 3: Update LLM System Prompts
Update the prompt definition inside `backend/ollama_client.py` to include the new JSON schema structure and instruction presets.

---

## 2. Advanced Procedural Materials & Texturing

To go beyond flat PBR colors and add wood grains, metallic wear, or concrete patterns:
1. **Material Library (.blend)**: Keep a library of pre-configured PBR materials (with high-quality image textures for diffuse, roughness, and normal maps) in a base `.blend` file. Have generator scripts open/link these materials instead of generating them from code.
2. **Headless Texture Baking**: If using custom procedural shaders (like Wave and Noise nodes):
   - Switch the rendering engine to `CYCLES`.
   - Set up UV unwrapping on the joined mesh (`bpy.ops.uv.smart_project()`).
   - Create a blank image texture node inside the material, and call `bpy.ops.object.bake(type='DIFFUSE')`.
   - Save the baked texture image and pack it into the exported GLB.

---

## 3. Production Queue & Scale-out Architecture

The current FastAPI `BackgroundTasks` executes Blender runs sequentially in-memory. In production with concurrent users:
- **Redis Queue (Celery/RQ)**: Offload generation requests from the web thread into a distributed task queue.
- **Blender Worker Pool**: Spin up multiple Celery workers inside Docker containers. Each worker runs a headless Blender instance.
- **Dockerization**: Pack the application using a base Linux image containing Blender dependencies:
  ```dockerfile
  FROM nytimes/blender:3.6-gpu-ubuntu18.04
  # Install python, backend dependencies, and uvicorn
  ```

---

## 4. Cloud Integration & SaaS Hosting

- **Cloud File Storage**: Replace local filesystem paths with Cloud Storage. Upon generation success, upload the GLB and PNG renders to an **AWS S3** or **Google Cloud Storage** bucket and store the public URL in the SQLite/PostgreSQL database.
- **Database Scaling**: Migrate the local SQLite database to a managed PostgreSQL cluster (e.g., AWS RDS).
- **Authentication**: Add JWT-based user authentication using FastAPI security utilities to allow users to save, catalog, and purchase/download their custom generations.
