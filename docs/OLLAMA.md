# What Ollama Does In kchiro

Ollama is used as the local AI parser for asset prompts. It does not directly create meshes, draw the preview, export Blender files, or run the frontend. Its job is to read a natural-language prompt and return a strict JSON object that the rest of the app can validate and generate from.

## In One Sentence

Ollama turns text like `make a pine tree with layered foliage` into machine-readable parameters like `asset_type`, `height`, `canopy_width`, and `layers`.

## Exact Flow

1. The React app sends the prompt to `POST /api/generate`.
2. `backend/app.py` calls `PromptProcessor.process_prompt()`.
3. `PromptProcessor` calls `OllamaClient.generate_json_spec()`.
4. `backend/ollama_client.py` sends the prompt to the local Ollama server.
5. Ollama uses the configured model, `qwen2.5:7b` by default.
6. The model returns JSON only.
7. The backend repairs common unit mistakes, such as meters vs centimeters.
8. Pydantic validates the JSON against `schemas/asset_schemas.py`.
9. The selected Blender generator script builds the actual mesh.

## Why It Exists

The Blender generators need exact structured values. A human writes messy text; Blender code needs exact parameters. Ollama is the bridge between those two worlds.

For example:

```text
Prompt:
make a dense grass patch
```

Ollama should return something like:

```json
{
  "asset_type": "grass",
  "width": 120.0,
  "height": 35.0,
  "density": 45
}
```

Then Pydantic checks that `density` is an integer in the allowed range. If Ollama returns `"dense"` instead of `45`, validation fails, which is why the system prompt strongly tells it to output integers and concrete numbers.

## What Ollama Does Not Do

- It does not render models.
- It does not create `.blend`, `.glb`, or `.stl` files.
- It does not run inside Blender.
- It does not store project data.
- It does not control the city planner, room planner, or game/movie panels directly.

## Configuration

Defaults:

```text
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:7b
```

You can override those values with environment variables before starting the backend.

PowerShell example:

```powershell
$env:OLLAMA_HOST="http://127.0.0.1:11434"
$env:OLLAMA_MODEL="qwen2.5:7b"
uvicorn backend.app:app --reload
```

## Troubleshooting

If generation fails before Blender starts, check Ollama first:

```powershell
ollama list
ollama pull qwen2.5:7b
ollama run qwen2.5:7b
```

If the backend says schema validation failed, Ollama returned JSON that did not match the asset schema. The backend has repair logic for common mistakes, but not every bad output can be safely guessed.
