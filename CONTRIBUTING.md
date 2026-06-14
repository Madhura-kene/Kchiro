# Contributing

Thanks for helping improve kchiro. The project is still moving quickly, so small focused changes are easiest to review.

## Local Setup

1. Install Python, Node.js, Blender, and Ollama.
2. Install Python dependencies with `pip install -r requirements.txt`.
3. Install frontend dependencies with `cd frontend && npm install`.
4. Pull the default Ollama model with `ollama pull qwen2.5:7b`.
5. Run the backend with `uvicorn backend.app:app --reload`.
6. Run the frontend with `cd frontend && npm run dev`.

## Before Opening A Pull Request

Run:

```powershell
pytest backend/test_app.py backend/test_prompt_processor.py backend/test_room_layout.py database/test_db.py schemas/test_schemas.py -q
cd frontend
npm run build
```

If you changed Blender generator geometry, also run the relevant Blender-backed tests locally.

## Generated Files

Do not commit generated files from `exports/`, `renders/`, `outputs/`, `scratch/`, `frontend/dist/`, `frontend/node_modules/`, or `blender/bin/`.

## Adding A New Asset Type

1. Add or update the Pydantic schema in `schemas/asset_schemas.py`.
2. Teach the prompt parser about aliases in `backend/prompt_processor.py`.
3. Add the generator in `generators/`.
4. Add tests for schema validation and prompt repair.
5. Update the frontend asset list if it should appear as a button.
