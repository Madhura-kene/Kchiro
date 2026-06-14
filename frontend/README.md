# kchiro Frontend

This is the React/Vite frontend for kchiro. It talks to the FastAPI backend, previews generated GLB assets, and provides the room, city, game asset, and movie production panels.

## Setup

```powershell
npm install
copy .env.example .env
npm run dev
```

## Configuration

The frontend reads:

- `VITE_API_BASE_URL`: FastAPI backend URL. Default: `http://127.0.0.1:8000`

## Commands

```powershell
npm run dev
npm run build
npm run preview
```
