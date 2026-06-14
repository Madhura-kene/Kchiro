# Kchiro — AI-Powered Procedural 3D Asset Studio

Kchiro is a local-first procedural 3D asset generator and layout studio. It turns natural language text prompts into validated asset parameters, generates Blender geometry programmatically, previews models interactively in the browser, and exports individual assets, complete rooms, houses, and city layouts for Blender or 3D printing.

## Design & UI Aesthetics

Kchiro features a professional, visually stunning, custom dark-mode interface:
- **Steel-Blue Midnight Theme**: Coordinated dark navy and steel-blue palette inspired by the Kchiro branding.
- **Elegant & Traditional Typography**: High-fidelity Google Fonts (`Playfair Display` for headers and `Lora` for body/values) replacing standard sans-serif/monospace for a classic, literary visual feel.
- **High-Contrast Input Fields**: Re-styled numerical input boxes featuring black letters on a clean white background for absolute legibility.
- **Collapsible Presets Control**: Collapsible, categorized prompt presets so you can quickly build presets or prompts without cluttering the screen.
- **Simplified Workflow**: Streamlined sidebar layouts, focusing entirely on the 3D Room Designer experience.

## What It Can Do

- **Text-to-3D Generation**: Enter natural prompts to generate fully detailed procedural Blender assets (e.g., *a modern kitchen island* or *an elegant wooden desk*).
- **Interactive 3D Viewport**: Rotate, position, scale, and color-customize models directly in the browser.
- **Asset Hierarchy & Checklists**: Easily pick, transform, and keep track of items across rooms.
- **Room & House Builder**: Build full houses or compact city blocks with customized sidewalk widths, lanes, and setbacks.
- **Blender & STL Export**: Save assets as standard `.glb` or `.stl` format, or export entire layout designs directly as native `.blend` files.
- **Local LLM Engine**: Use local Ollama and `qwen2.5:7b` to keep everything offline, private, and fast.

## Tech Stack

- **Frontend**: React, Vite, Three.js
- **Backend**: FastAPI (Python), Pydantic, SQLite
- **AI Engine**: Local Ollama Server (`qwen2.5:7b`)
- **3D Runner**: Blender Python API run headlessly in background mode

## How The Pipeline Works

1. The user enters a prompt in the frontend, such as `a wooden bunk bed with blue blankets`.
2. The frontend posts that prompt to `POST /api/generate`.
3. FastAPI sends the prompt to local Ollama.
4. Ollama returns a strict JSON spec, for example `{ "asset_type": "bunk_bed", "material": "wood" }`.
5. Pydantic validates and clamps the JSON against the matching schema.
6. The backend chooses the correct generator script in `generators/`.
7. Blender runs headlessly and exports a `.glb` plus a preview `.png`.
8. The browser displays the result and can export Blender or print files.

More detail: [docs/OLLAMA.md](docs/OLLAMA.md)

## Prerequisites

- Python 3.10 or newer
- Node.js 20 or newer
- Blender 3.6 or 4.x
- Ollama with the Qwen model pulled locally

Install the default Ollama model:

```powershell
ollama pull qwen2.5:7b
```

Blender can be installed normally and available as `blender` on your PATH, or configured with `BLENDER_EXECUTABLE`.

## Backend Setup

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn backend.app:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

## Frontend Setup

Open a second terminal:

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

The Vite app usually runs at:

```text
http://127.0.0.1:5173
```

If that port is busy, Vite may use another port such as `5174`.

## Configuration

Backend environment variables:

- `OLLAMA_HOST`: Ollama server URL. Default: `http://127.0.0.1:11434`
- `OLLAMA_MODEL`: Ollama model name. Default: `qwen2.5:7b`
- `BLENDER_EXECUTABLE`: Optional absolute path to Blender.
- `KCHIRO_DB_PATH`: Optional SQLite path. Default: `database/assets.db`

Frontend environment variables:

- `VITE_API_BASE_URL`: Backend URL. Default: `http://127.0.0.1:8000`

## Useful Commands

Run backend tests that do not require Blender:

```powershell
pytest backend/test_app.py backend/test_prompt_processor.py backend/test_room_layout.py database/test_db.py schemas/test_schemas.py -q
```

Run the frontend production build:

```powershell
cd frontend
npm run build
```

Run Blender-backed generator tests locally:

```powershell
pytest backend/test_blender_executor.py backend/test_new_generators.py -q
```

Those tests require a working Blender executable and can take longer.

Run the real Ollama integration test:

```powershell
$env:RUN_OLLAMA_INTEGRATION_TESTS="1"
pytest backend/test_prompt_processor.py::test_end_to_end_pipeline_integration -q
```

That test requires the Ollama server and configured model to be available locally.

## Repository Hygiene

Generated and bulky local files are intentionally ignored:

- `frontend/node_modules/`
- `frontend/dist/`
- `database/*.db`
- `exports/`
- `renders/`
- `outputs/`
- `scratch/`
- `blender/bin/`
- local `.blend` and `.stl` files

This keeps GitHub clean and avoids committing huge Blender/runtime/generated artifacts.

## Project Structure

```text
backend/      FastAPI API, prompt processing, export endpoints
blender/      Blender execution helpers and export scripts
database/     SQLite database wrapper
docs/         Project documentation
frontend/     React/Vite app
generators/   Procedural Blender asset generators
schemas/      Pydantic asset schemas
exports/      Generated GLB/Blend/STL output, ignored by git
renders/      Generated preview PNG output, ignored by git
```


