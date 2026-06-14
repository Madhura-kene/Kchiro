import React, { useRef, useState } from 'react';

const MAX_HISTORY = 20;
const MOVIE_LAYERS = ['Background', 'Midground', 'Foreground', 'Overlay'];
const ASPECTS = {
  '16:9': '16 / 9',
  '4:3': '4 / 3',
  '2.39:1': '2.39 / 1',
};

const STYLE_CARDS = [
  {
    id: 'live_action',
    label: 'Live Action',
    description: 'Real-world scenes, actors, locations.',
    defaultGrade: 'cinematic',
  },
  {
    id: 'animated',
    label: 'Animated',
    description: 'Cartoon or stylized animation, 2D or 3D.',
    defaultGrade: 'warm',
  },
  {
    id: 'documentary',
    label: 'Documentary',
    description: 'Interview setups, b-roll, narration-driven.',
    defaultGrade: 'cold',
  },
];

const CATEGORY_COLORS = {
  'Characters / Cast': '#38bdf8',
  'Locations / Sets': '#22c55e',
  Props: '#f59e0b',
  'Lighting Rigs': '#fde68a',
  Camera: '#c084fc',
  'VFX / Overlays': '#fb7185',
  'Audio Stubs': '#94a3b8',
};

const MOVIE_ASSET_CATEGORIES = [
  {
    name: 'Characters / Cast',
    items: [
      { type: 'lead', label: 'Lead', color: '#38bdf8', layer: 'Midground', motionTarget: 'character' },
      { type: 'supporting', label: 'Supporting', color: '#22c55e', layer: 'Midground', motionTarget: 'character' },
      { type: 'extra', label: 'Extra', color: '#a78bfa', layer: 'Midground', motionTarget: 'character' },
      { type: 'villain', label: 'Villain', color: '#ef4444', layer: 'Midground', motionTarget: 'character' },
    ],
  },
  {
    name: 'Locations / Sets',
    items: [
      { type: 'indoor_room', label: 'Indoor Room', color: '#92400e', layer: 'Background', scale: 2.2 },
      { type: 'office_set', label: 'Office', color: '#64748b', layer: 'Background', scale: 2.2 },
      { type: 'studio_set', label: 'Studio', color: '#312e81', layer: 'Background', scale: 2.2 },
      { type: 'street_set', label: 'Street', color: '#475569', layer: 'Background', scale: 2.2 },
      { type: 'forest_set', label: 'Forest', color: '#166534', layer: 'Background', scale: 2.2 },
      { type: 'rooftop_set', label: 'Rooftop', color: '#475569', layer: 'Background', scale: 2.2 },
      { type: 'desert_set', label: 'Desert', color: '#d97706', layer: 'Background', scale: 2.2 },
      { type: 'fantasy_set', label: 'Fantasy Env', color: '#7c3aed', layer: 'Background', scale: 2.2 },
      { type: 'sci_fi_set', label: 'Sci-Fi Env', color: '#0891b2', layer: 'Background', scale: 2.2 },
    ],
  },
  {
    name: 'Props',
    items: [
      { type: 'furniture', label: 'Furniture', color: '#b45309', layer: 'Midground' },
      { type: 'vehicle', label: 'Vehicle', color: '#ef4444', layer: 'Midground' },
      { type: 'weapon', label: 'Weapon', color: '#e5e7eb', layer: 'Foreground' },
      { type: 'food', label: 'Food Item', color: '#fb923c', layer: 'Foreground' },
      { type: 'electronics', label: 'Electronics', color: '#38bdf8', layer: 'Midground' },
      { type: 'book', label: 'Book', color: '#7c2d12', layer: 'Foreground' },
      { type: 'sign', label: 'Sign', color: '#facc15', layer: 'Foreground' },
    ],
  },
  {
    name: 'Lighting Rigs',
    items: [
      { type: 'key_light', label: 'Key Light', color: '#fde68a', layer: 'Overlay' },
      { type: 'fill_light', label: 'Fill Light', color: '#bfdbfe', layer: 'Overlay' },
      { type: 'backlight', label: 'Backlight', color: '#f0abfc', layer: 'Overlay' },
      { type: 'practical_lamp', label: 'Practical Lamp', color: '#fbbf24', layer: 'Foreground' },
      { type: 'neon_light', label: 'Neon', color: '#22d3ee', layer: 'Overlay' },
      { type: 'candle_light', label: 'Candle', color: '#fb923c', layer: 'Foreground' },
      { type: 'colored_gel', label: 'Colored Gel', color: '#a78bfa', layer: 'Overlay' },
      { type: 'strobe', label: 'Strobe', color: '#f8fafc', layer: 'Overlay', strobe: true },
    ],
  },
  {
    name: 'Camera',
    items: [
      { type: 'handheld_camera', label: 'Handheld', color: '#c084fc', layer: 'Overlay', motionTarget: 'camera' },
      { type: 'tripod_camera', label: 'Tripod', color: '#a78bfa', layer: 'Overlay', motionTarget: 'camera' },
      { type: 'crane_camera', label: 'Crane', color: '#818cf8', layer: 'Overlay', motionTarget: 'camera' },
      { type: 'drone_camera', label: 'Drone', color: '#38bdf8', layer: 'Overlay', motionTarget: 'camera' },
      { type: 'wide_shot', label: 'Wide Shot', color: '#f8fafc', layer: 'Overlay', shotType: 'Wide' },
      { type: 'medium_shot', label: 'Medium Shot', color: '#f8fafc', layer: 'Overlay', shotType: 'Medium' },
      { type: 'close_up', label: 'Close-Up', color: '#f8fafc', layer: 'Overlay', shotType: 'Close-Up' },
      { type: 'extreme_close_up', label: 'Extreme CU', color: '#f8fafc', layer: 'Overlay', shotType: 'Extreme Close-Up' },
      { type: 'eye_level', label: 'Eye Level', color: '#e0f2fe', layer: 'Overlay' },
      { type: 'low_angle', label: 'Low Angle', color: '#e0f2fe', layer: 'Overlay' },
      { type: 'high_angle', label: 'High Angle', color: '#e0f2fe', layer: 'Overlay' },
      { type: 'birds_eye', label: "Bird's Eye", color: '#e0f2fe', layer: 'Overlay' },
    ],
  },
  {
    name: 'VFX / Overlays',
    items: [
      { type: 'rain', label: 'Rain', color: '#93c5fd', layer: 'Overlay', motionTarget: 'vfx' },
      { type: 'snow', label: 'Snow', color: '#f8fafc', layer: 'Overlay', motionTarget: 'vfx' },
      { type: 'fire_vfx', label: 'Fire', color: '#fb923c', layer: 'Overlay', motionTarget: 'vfx' },
      { type: 'smoke', label: 'Smoke', color: '#94a3b8', layer: 'Overlay', motionTarget: 'vfx' },
      { type: 'lens_flare', label: 'Lens Flare', color: '#fde68a', layer: 'Overlay', motionTarget: 'vfx' },
      { type: 'motion_blur', label: 'Motion Blur', color: '#cbd5e1', layer: 'Overlay', motionTarget: 'vfx' },
      { type: 'cinematic_grade', label: 'Cinematic', color: '#fb923c', layer: 'Overlay', colorGrade: 'cinematic' },
      { type: 'noir_grade', label: 'Noir', color: '#9ca3af', layer: 'Overlay', colorGrade: 'noir' },
      { type: 'warm_grade', label: 'Warm', color: '#f97316', layer: 'Overlay', colorGrade: 'warm' },
      { type: 'cold_grade', label: 'Cold', color: '#38bdf8', layer: 'Overlay', colorGrade: 'cold' },
      { type: 'horror_grade', label: 'Horror', color: '#dc2626', layer: 'Overlay', colorGrade: 'horror' },
    ],
  },
  {
    name: 'Audio Stubs',
    items: [
      { type: 'dialogue_track', label: 'Dialogue Track', color: '#94a3b8', layer: 'Overlay' },
      { type: 'ambient_sound', label: 'Ambient Sound', color: '#64748b', layer: 'Overlay' },
      { type: 'score_music', label: 'Score / Music', color: '#a78bfa', layer: 'Overlay' },
      { type: 'foley_sfx', label: 'Foley SFX', color: '#f59e0b', layer: 'Overlay' },
    ],
  },
];

const ASSET_LOOKUP = MOVIE_ASSET_CATEGORIES.flatMap((category) =>
  category.items.map((item) => ({ ...item, category: category.name }))
).reduce((lookup, item) => {
  lookup[item.type] = item;
  return lookup;
}, {});

const CHARACTER_MOTIONS = ['Idle', 'Walking', 'Running', 'Talking', 'Fighting', 'Sitting', 'Reacting'];
const CAMERA_MOTIONS = ['Static', 'Pan left-right', 'Tilt up-down', 'Zoom in-out', 'Dolly', 'Handheld shake'];
const VFX_MOTIONS = ['Static', 'Falling', 'Flicker', 'Drift', 'Pulse'];
const SHOT_TYPES = ['Wide', 'Medium', 'Close-Up', 'Extreme Close-Up'];
const COLOR_GRADES = ['none', 'cinematic', 'noir', 'warm', 'cold', 'horror'];

const makeId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) return crypto.randomUUID();
  return `movie-${Date.now()}-${Math.random().toString(16).slice(2)}`;
};

const downloadTextFile = (filename, text, type = 'application/json') => {
  const blob = new Blob([text], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

const encodeBase64 = (value) => {
  const bytes = new TextEncoder().encode(value);
  let binary = '';
  bytes.forEach((byte) => {
    binary += String.fromCharCode(byte);
  });
  return btoa(binary);
};

const layerZIndex = (layer) => MOVIE_LAYERS.indexOf(layer) + 1;

const createScene = (index = 0, overrides = {}) => ({
  id: makeId(),
  locationName: overrides.locationName || 'Studio Set',
  shotType: overrides.shotType || 'Wide',
  duration: overrides.duration || 6,
  intExt: overrides.intExt || 'INT',
  dayNight: overrides.dayNight || 'Day',
  description: overrides.description || '',
  script: overrides.script || '',
  aspectRatio: overrides.aspectRatio || '16:9',
  colorGrade: overrides.colorGrade || 'none',
  assets: overrides.assets || [],
  sceneNumber: index + 1,
});

const createPlacedAsset = (definition, x, y, overrides = {}) => ({
  id: makeId(),
  type: definition.type,
  category: definition.category,
  name: definition.label,
  color: definition.color,
  scale: definition.scale || 1,
  opacity: 1,
  layer: definition.layer || 'Midground',
  facing: 'Right',
  emotion: 'neutral',
  notes: '',
  x,
  y,
  motion: {
    type: definition.motionTarget === 'camera' ? 'Static' : 'Idle',
    speed: 1,
    loop: true,
  },
  motionTarget: definition.motionTarget || null,
  strobe: Boolean(definition.strobe),
  ...overrides,
});

const normalizeSceneNumbers = (scenes) => scenes.map((scene, index) => ({ ...scene, sceneNumber: index + 1 }));

const getSceneAssetCounts = (scene) =>
  MOVIE_ASSET_CATEGORIES.reduce((counts, category) => {
    counts[category.name] = scene.assets.filter((asset) => asset.category === category.name).length;
    return counts;
  }, {});

const getVisibleAssets = (scene, layers) =>
  scene.assets
    .filter((asset) => layers[asset.layer]?.visible)
    .sort((a, b) => layerZIndex(a.layer) - layerZIndex(b.layer));

const getShotInset = (shotType) => {
  switch (shotType) {
    case 'Medium':
      return '10% 18%';
    case 'Close-Up':
      return '18% 30%';
    case 'Extreme Close-Up':
      return '28% 38%';
    default:
      return '5% 6%';
  }
};

const buildBlenderScript = (project) => {
  const encoded = encodeBase64(JSON.stringify(project));
  return `# Movie Production Panel Blender scene builder
# Run this in Blender. It creates storyboard scene markers as 3D blocks and saves a .blend file.
import base64
import json
import math
import bpy

PROJECT = json.loads(base64.b64decode("${encoded}").decode("utf-8"))

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

materials = {}

def hex_to_rgba(hex_color, alpha=1.0):
    value = (hex_color or "#ffffff").lstrip("#")
    if len(value) != 6:
        value = "ffffff"
    return tuple(int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (alpha,)

def mat(name, color, alpha=1.0):
    key = f"{name}_{color}_{alpha}"
    if key in materials:
        return materials[key]
    m = bpy.data.materials.new(name)
    m.diffuse_color = hex_to_rgba(color, alpha)
    materials[key] = m
    return m

def cube(name, loc, scale, color, alpha=1.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat(name + "_mat", color, alpha))
    return obj

layer_z = {"Background": 0.05, "Midground": 0.55, "Foreground": 1.1, "Overlay": 1.65}
category_size = {
    "Characters / Cast": (0.45, 0.45, 1.4),
    "Locations / Sets": (3.8, 0.18, 1.9),
    "Props": (0.8, 0.8, 0.65),
    "Lighting Rigs": (0.35, 0.35, 1.8),
    "Camera": (0.7, 0.45, 0.45),
    "VFX / Overlays": (1.1, 0.08, 0.6),
    "Audio Stubs": (0.9, 0.25, 0.35),
}

for scene_index, scene in enumerate(PROJECT.get("scenes", [])):
    offset_x = scene_index * 12
    cube(f"Scene {scene_index + 1} frame", (offset_x, 0, -0.04), (9.6, 5.4, 0.05), "#111827", 1)
    for asset in scene.get("assets", []):
        x = offset_x + (asset.get("x", 50) - 50) / 10
        y = (50 - asset.get("y", 50)) / 10
        category = asset.get("category", "Props")
        sx, sy, sz = category_size.get(category, (0.7, 0.7, 0.7))
        scale = asset.get("scale", 1)
        z = layer_z.get(asset.get("layer", "Midground"), 0.5) + sz * scale / 2
        cube(asset.get("name", "asset"), (x, y, z), (sx * scale, sy * scale, sz * scale), asset.get("color", "#ffffff"), asset.get("opacity", 1))

bpy.ops.object.light_add(type="SUN", location=(0, -6, 10))
bpy.context.object.name = "Production Sun"
bpy.context.object.data.energy = 2.4
bpy.ops.object.camera_add(location=(8, -12, 8), rotation=(math.radians(58), 0, math.radians(35)))
bpy.context.scene.camera = bpy.context.object
bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath("//movie_production_storyboard.blend"))
`;
};

const MovieAssetIcon = ({ asset, compact = false }) => {
  const color = asset.color || ASSET_LOOKUP[asset.type]?.color || '#e5e7eb';
  const category = asset.category || ASSET_LOOKUP[asset.type]?.category || 'Props';
  const type = asset.type || '';

  if (category === 'Characters / Cast') {
    const angry = asset.emotion === 'angry';
    const scared = asset.emotion === 'scared';
    const happy = asset.emotion === 'happy';
    return (
      <svg className={`movie-icon ${compact ? 'compact' : ''}`} viewBox="0 0 100 100" aria-hidden="true">
        <ellipse cx="50" cy="84" rx="24" ry="6" fill="#020617" opacity="0.32" />
        <path d="M34 78c2-27 30-27 32 0Z" fill={color} stroke="#0f172a" strokeWidth="4" />
        <circle cx="50" cy="32" r="18" fill="#f8d8b5" stroke="#0f172a" strokeWidth="4" />
        <path d="M34 19c12-14 30-6 34 5-15-3-22 1-34-5Z" fill="#1f2937" />
        <circle cx="43" cy="31" r="2.5" fill="#111827" />
        <circle cx="57" cy="31" r="2.5" fill="#111827" />
        {happy && <path d="M42 42c5 6 12 6 17 0" fill="none" stroke="#111827" strokeWidth="3" strokeLinecap="round" />}
        {angry && <path d="M40 25l7 3M60 25l-7 3M42 44h16" stroke="#111827" strokeWidth="3" strokeLinecap="round" />}
        {scared && <ellipse cx="50" cy="44" rx="6" ry="8" fill="#111827" />}
        {!happy && !angry && !scared && <path d="M43 43h14" stroke="#111827" strokeWidth="3" strokeLinecap="round" />}
        {type === 'villain' && <path d="M32 16 24 6M68 16l8-10" stroke="#ef4444" strokeWidth="5" strokeLinecap="round" />}
      </svg>
    );
  }

  if (category === 'Locations / Sets') {
    return (
      <svg className={`movie-icon ${compact ? 'compact' : ''}`} viewBox="0 0 100 100" aria-hidden="true">
        <rect x="8" y="18" width="84" height="58" rx="8" fill={color} stroke="#0f172a" strokeWidth="4" />
        <path d="M8 76 32 54h36l24 22Z" fill="#020617" opacity="0.22" />
        {type.includes('forest') && <path d="M24 67 35 35l11 32M49 67l14-38 14 38" fill="#16a34a" stroke="#0f172a" strokeWidth="3" />}
        {type.includes('street') && <path d="M37 76 50 20 63 76M50 31v34" stroke="#facc15" strokeWidth="4" strokeDasharray="6 6" />}
        {type.includes('office') && <path d="M22 28h56M22 42h56M22 56h56M36 22v50M64 22v50" stroke="#dbeafe" strokeWidth="3" opacity="0.8" />}
      </svg>
    );
  }

  if (category === 'Lighting Rigs') {
    return (
      <svg className={`movie-icon ${compact ? 'compact' : ''}`} viewBox="0 0 100 100" aria-hidden="true">
        <path d="M50 18 86 82H14Z" fill={color} opacity="0.28" />
        <rect x="42" y="13" width="16" height="18" rx="4" fill={color} stroke="#0f172a" strokeWidth="4" />
        <path d="M50 31v47M35 78h30" stroke="#0f172a" strokeWidth="5" strokeLinecap="round" />
        {asset.strobe && <path d="M25 20h10M66 20h10M50 4v9" stroke="#f8fafc" strokeWidth="4" strokeLinecap="round" />}
      </svg>
    );
  }

  if (category === 'Camera') {
    return (
      <svg className={`movie-icon ${compact ? 'compact' : ''}`} viewBox="0 0 100 100" aria-hidden="true">
        <rect x="16" y="33" width="48" height="30" rx="6" fill={color} stroke="#0f172a" strokeWidth="4" />
        <path d="M64 42 86 31v34L64 54Z" fill="#312e81" stroke="#0f172a" strokeWidth="4" />
        <circle cx="37" cy="48" r="10" fill="#020617" />
        <path d="M30 75h40M50 63v12" stroke="#0f172a" strokeWidth="5" strokeLinecap="round" />
      </svg>
    );
  }

  if (category === 'VFX / Overlays') {
    return (
      <svg className={`movie-icon ${compact ? 'compact' : ''}`} viewBox="0 0 100 100" aria-hidden="true">
        <path d="M50 10 59 37l29-9-20 23 22 20-30-4-10 25-10-25-30 4 22-20-20-23 29 9Z" fill={color} stroke="#0f172a" strokeWidth="4" opacity="0.9" />
        <circle cx="50" cy="51" r="13" fill="#fff7ed" opacity="0.55" />
      </svg>
    );
  }

  if (category === 'Audio Stubs') {
    return (
      <svg className={`movie-icon ${compact ? 'compact' : ''}`} viewBox="0 0 100 100" aria-hidden="true">
        <rect x="18" y="24" width="64" height="52" rx="10" fill={color} stroke="#0f172a" strokeWidth="4" />
        <path d="M35 58V42l13 8 13-8v16" fill="none" stroke="#f8fafc" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }

  return (
    <svg className={`movie-icon ${compact ? 'compact' : ''}`} viewBox="0 0 100 100" aria-hidden="true">
      <rect x="22" y="28" width="56" height="44" rx="8" fill={color} stroke="#0f172a" strokeWidth="4" />
      {type === 'vehicle' && <><circle cx="34" cy="73" r="8" fill="#111827" /><circle cx="66" cy="73" r="8" fill="#111827" /><path d="M30 28l10-12h22l10 12" fill="none" stroke="#0f172a" strokeWidth="4" /></>}
      {type === 'weapon' && <path d="M28 72 70 25M63 23h9v9M31 61l9 9" stroke="#f8fafc" strokeWidth="6" strokeLinecap="round" />}
      {type === 'sign' && <path d="M30 42h40M50 72v17" stroke="#f8fafc" strokeWidth="5" strokeLinecap="round" />}
    </svg>
  );
};

function MovieProductionPanel() {
  const [projectStyle, setProjectStyle] = useState(null);
  const [scenes, setScenes] = useState([]);
  const [activeSceneId, setActiveSceneId] = useState(null);
  const [selectedTool, setSelectedTool] = useState('lead');
  const [mode, setMode] = useState('Place');
  const [openCategories, setOpenCategories] = useState(() =>
    MOVIE_ASSET_CATEGORIES.reduce((state, category) => ({ ...state, [category.name]: true }), {})
  );
  const [scriptOpen, setScriptOpen] = useState(true);
  const [selectedAssetId, setSelectedAssetId] = useState(null);
  const [contextMenu, setContextMenu] = useState(null);
  const [layers, setLayers] = useState({
    Background: { visible: true, locked: false },
    Midground: { visible: true, locked: false },
    Foreground: { visible: true, locked: false },
    Overlay: { visible: true, locked: false },
  });
  const [history, setHistory] = useState({ past: [], future: [] });
  const [isPlaying, setIsPlaying] = useState(false);
  const [status, setStatus] = useState('Pick a production style to begin.');
  const importRef = useRef(null);

  const activeScene = scenes.find((scene) => scene.id === activeSceneId) || null;
  const selectedAsset = activeScene?.assets.find((asset) => asset.id === selectedAssetId) || null;
  const selectedDefinition = ASSET_LOOKUP[selectedTool] || ASSET_LOOKUP.lead;
  const counts = activeScene ? getSceneAssetCounts(activeScene) : {};

  const commitScenes = (nextScenes, nextActiveId = activeSceneId, nextSelectedAssetId = selectedAssetId) => {
    setHistory((prev) => ({
      past: [...prev.past.slice(-(MAX_HISTORY - 1)), scenes],
      future: [],
    }));
    setScenes(normalizeSceneNumbers(nextScenes));
    setActiveSceneId(nextActiveId);
    setSelectedAssetId(nextSelectedAssetId);
  };

  const updateActiveScene = (updater, shouldCommit = false) => {
    const nextScenes = scenes.map((scene) => {
      if (scene.id !== activeSceneId) return scene;
      return typeof updater === 'function' ? updater(scene) : { ...scene, ...updater };
    });
    if (shouldCommit) {
      commitScenes(nextScenes);
    } else {
      setScenes(normalizeSceneNumbers(nextScenes));
    }
  };

  const resetProject = (styleId) => {
    const style = STYLE_CARDS.find((card) => card.id === styleId) || STYLE_CARDS[0];
    const firstScene = createScene(0, {
      locationName: style.id === 'documentary' ? 'Interview Studio' : 'Studio Set',
      shotType: style.id === 'documentary' ? 'Medium' : 'Wide',
      colorGrade: style.defaultGrade,
      description: `${style.label} opening scene`,
    });
    setProjectStyle(styleId);
    setScenes([firstScene]);
    setActiveSceneId(firstScene.id);
    setSelectedAssetId(null);
    setHistory({ past: [], future: [] });
    setStatus(`${style.label} project ready. Select an asset and click the storyboard frame.`);
  };

  const handlePickStyle = (styleId) => {
    resetProject(styleId);
  };

  const handleSwitchStyle = () => {
    const currentIndex = STYLE_CARDS.findIndex((card) => card.id === projectStyle);
    const nextStyle = STYLE_CARDS[(currentIndex + 1) % STYLE_CARDS.length];
    if (scenes.some((scene) => scene.assets.length > 0) && !window.confirm('Switching style resets the movie project. Continue?')) {
      return;
    }
    resetProject(nextStyle.id);
  };

  const handleUndo = () => {
    setHistory((prev) => {
      if (prev.past.length === 0) return prev;
      const previous = prev.past[prev.past.length - 1];
      setScenes(previous);
      setActiveSceneId(previous[0]?.id || null);
      setSelectedAssetId(null);
      setStatus('Undo applied.');
      return {
        past: prev.past.slice(0, -1),
        future: [scenes, ...prev.future].slice(0, MAX_HISTORY),
      };
    });
  };

  const handleRedo = () => {
    setHistory((prev) => {
      if (prev.future.length === 0) return prev;
      const next = prev.future[0];
      setScenes(next);
      setActiveSceneId(next[0]?.id || null);
      setSelectedAssetId(null);
      setStatus('Redo applied.');
      return {
        past: [...prev.past.slice(-(MAX_HISTORY - 1)), scenes],
        future: prev.future.slice(1),
      };
    });
  };

  const handleAddScene = () => {
    const nextScene = createScene(scenes.length, {
      locationName: activeScene?.locationName || 'New Location',
      shotType: activeScene?.shotType || 'Wide',
      colorGrade: activeScene?.colorGrade || 'none',
    });
    commitScenes([...scenes, nextScene], nextScene.id, null);
    setStatus(`Scene ${scenes.length + 1} added.`);
  };

  const handleSceneDrop = (sourceId, targetId) => {
    if (!sourceId || sourceId === targetId) return;
    const sourceIndex = scenes.findIndex((scene) => scene.id === sourceId);
    const targetIndex = scenes.findIndex((scene) => scene.id === targetId);
    if (sourceIndex < 0 || targetIndex < 0) return;
    const nextScenes = [...scenes];
    const [moved] = nextScenes.splice(sourceIndex, 1);
    nextScenes.splice(targetIndex, 0, moved);
    commitScenes(nextScenes, activeSceneId, selectedAssetId);
    setStatus('Scene order updated.');
  };

  const handleCanvasClick = (event) => {
    if (!activeScene || mode !== 'Place') {
      if (mode === 'Select') setSelectedAssetId(null);
      return;
    }
    const layer = selectedDefinition.layer || 'Midground';
    if (layers[layer]?.locked) {
      setStatus(`${layer} is locked.`);
      return;
    }
    const rect = event.currentTarget.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
    const placed = createPlacedAsset(selectedDefinition, Number(x.toFixed(2)), Number(y.toFixed(2)));
    const nextScene = {
      ...activeScene,
      assets: [...activeScene.assets, placed],
      locationName: selectedDefinition.category === 'Locations / Sets' ? selectedDefinition.label : activeScene.locationName,
      shotType: selectedDefinition.shotType || activeScene.shotType,
      colorGrade: selectedDefinition.colorGrade || activeScene.colorGrade,
    };
    commitScenes(scenes.map((scene) => (scene.id === activeScene.id ? nextScene : scene)), activeScene.id, placed.id);
    setStatus(`Placed ${placed.name}.`);
  };

  const handleAssetClick = (asset, event) => {
    event.stopPropagation();
    if (mode === 'Erase') {
      deleteAsset(asset.id);
      return;
    }
    setSelectedAssetId(asset.id);
    setStatus(`Selected ${asset.name}.`);
  };

  const handleAssetContextMenu = (asset, event) => {
    event.preventDefault();
    event.stopPropagation();
    setSelectedAssetId(asset.id);
    setContextMenu({ x: event.clientX, y: event.clientY, assetId: asset.id });
  };

  const duplicateAsset = (assetId) => {
    if (!activeScene) return;
    const source = activeScene.assets.find((asset) => asset.id === assetId);
    if (!source || layers[source.layer]?.locked) return;
    const duplicate = {
      ...source,
      id: makeId(),
      name: `${source.name} Copy`,
      x: Math.min(96, source.x + 4),
      y: Math.min(92, source.y + 4),
    };
    const nextScene = { ...activeScene, assets: [...activeScene.assets, duplicate] };
    commitScenes(scenes.map((scene) => (scene.id === activeScene.id ? nextScene : scene)), activeScene.id, duplicate.id);
    setContextMenu(null);
    setStatus(`Duplicated ${source.name}.`);
  };

  const deleteAsset = (assetId) => {
    if (!activeScene) return;
    const source = activeScene.assets.find((asset) => asset.id === assetId);
    if (!source || layers[source.layer]?.locked) return;
    const nextScene = { ...activeScene, assets: activeScene.assets.filter((asset) => asset.id !== assetId) };
    commitScenes(scenes.map((scene) => (scene.id === activeScene.id ? nextScene : scene)), activeScene.id, null);
    setContextMenu(null);
    setStatus(`Deleted ${source.name}.`);
  };

  const updateSelectedAsset = (field, value) => {
    if (!activeScene || !selectedAsset) return;
    updateActiveScene((scene) => ({
      ...scene,
      assets: scene.assets.map((asset) => (asset.id === selectedAsset.id ? { ...asset, [field]: value } : asset)),
    }));
  };

  const updateSelectedMotion = (field, value) => {
    if (!activeScene || !selectedAsset) return;
    updateActiveScene((scene) => ({
      ...scene,
      assets: scene.assets.map((asset) =>
        asset.id === selectedAsset.id ? { ...asset, motion: { ...asset.motion, [field]: value } } : asset
      ),
    }));
  };

  const handleClear = () => {
    if (!activeScene) return;
    if (activeScene.assets.length > 0 && !window.confirm('Clear the active storyboard canvas?')) return;
    const nextScene = { ...activeScene, assets: [] };
    commitScenes(scenes.map((scene) => (scene.id === activeScene.id ? nextScene : scene)), activeScene.id, null);
    setStatus('Active scene canvas cleared.');
  };

  const handleRandomScene = () => {
    if (!activeScene) return;
    const picks = ['street_set', 'lead', 'supporting', 'villain', 'vehicle', 'furniture', 'key_light', 'backlight', 'rain', 'lens_flare'];
    const randomAssets = picks.map((type, index) => {
      const definition = ASSET_LOOKUP[type];
      return createPlacedAsset(definition, 16 + ((index * 17) % 70), 24 + ((index * 19) % 52), {
        scale: definition.category === 'Locations / Sets' ? 2.4 : 1,
      });
    });
    const nextScene = {
      ...activeScene,
      locationName: 'Rainy Street',
      shotType: 'Wide',
      colorGrade: 'cinematic',
      assets: randomAssets,
      description: 'Randomly blocked ideation scene with cast, props, lighting, and atmosphere.',
    };
    commitScenes(scenes.map((scene) => (scene.id === activeScene.id ? nextScene : scene)), activeScene.id, null);
    setStatus('Random scene generated.');
  };

  const handlePlayScene = () => {
    setIsPlaying(true);
    setStatus('Playing rough motion preview.');
    window.setTimeout(() => setIsPlaying(false), Math.max(1600, (activeScene?.duration || 4) * 500));
  };

  const exportProject = () => {
    const project = { version: 1, source: 'kchiro Movie Production Panel', projectStyle, layers, scenes };
    downloadTextFile('movie_production_project.json', JSON.stringify(project, null, 2));
    setStatus('Storyboard project JSON exported.');
  };

  const importProject = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const data = JSON.parse(await file.text());
      if (!Array.isArray(data.scenes)) throw new Error('JSON does not contain scenes.');
      setProjectStyle(data.projectStyle || 'live_action');
      setScenes(normalizeSceneNumbers(data.scenes));
      setLayers(data.layers || layers);
      setActiveSceneId(data.scenes[0]?.id || null);
      setSelectedAssetId(null);
      setHistory({ past: [], future: [] });
      setStatus(`Imported ${data.scenes.length} scenes.`);
    } catch (error) {
      setStatus(`Import failed: ${error.message}`);
    } finally {
      event.target.value = '';
    }
  };

  const exportShotList = () => {
    const lines = scenes.map((scene, index) => [
      `Scene ${index + 1}`,
      `${scene.intExt}. ${scene.locationName} - ${scene.dayNight}`,
      `Shot: ${scene.shotType}`,
      `Duration: ${scene.duration}s`,
      `Description: ${scene.description || 'No description'}`,
    ].join('\n'));
    downloadTextFile('movie_shot_list.txt', lines.join('\n\n'), 'text/plain');
    setStatus('Shot list exported.');
  };

  const downloadBlenderBuilder = () => {
    const project = { version: 1, source: 'kchiro Movie Production Panel', projectStyle, scenes };
    downloadTextFile('movie_production_blender_builder.py', buildBlenderScript(project), 'text/x-python');
    setStatus('Downloaded Blender scene builder script. Run it in Blender to create a .blend file.');
  };

  const toggleLayer = (layer, field) => {
    setLayers((prev) => ({ ...prev, [layer]: { ...prev[layer], [field]: !prev[layer][field] } }));
  };

  const motionTypes = selectedAsset?.motionTarget === 'camera'
    ? CAMERA_MOTIONS
    : selectedAsset?.motionTarget === 'vfx'
      ? VFX_MOTIONS
      : CHARACTER_MOTIONS;

  if (!projectStyle) {
    return (
      <div className="movie-setup-screen">
        <div className="movie-setup-inner">
          <span className="city-panel-kicker">Movie Production Panel</span>
          <h2>Choose Production Style</h2>
          <p>Start with the visual language of the project. You can switch later, but switching resets this panel.</p>
          <div className="movie-style-cards">
            {STYLE_CARDS.map((style) => (
              <button type="button" className={`movie-style-card ${style.id}`} key={style.id} onClick={() => handlePickStyle(style.id)}>
                <MovieAssetIcon asset={{ type: style.id === 'documentary' ? 'tripod_camera' : style.id === 'animated' ? 'lead' : 'street_set', category: style.id === 'documentary' ? 'Camera' : style.id === 'animated' ? 'Characters / Cast' : 'Locations / Sets', color: style.id === 'documentary' ? '#c084fc' : style.id === 'animated' ? '#38bdf8' : '#22c55e' }} />
                <strong>{style.label}</strong>
                <span>{style.description}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`movie-panel movie-grade-${activeScene?.colorGrade || 'none'} ${isPlaying ? 'playing' : ''}`}>
      <aside className="movie-sidebar">
        <div className="movie-sidebar-header">
          <span className="city-panel-kicker">{STYLE_CARDS.find((card) => card.id === projectStyle)?.label}</span>
          <h2>Production Panel</h2>
          <button type="button" className="secondary-action-btn" onClick={handleSwitchStyle}>Switch Style</button>
        </div>

        <section className={`movie-script-panel ${scriptOpen ? 'open' : ''}`}>
          <button type="button" className="movie-section-toggle" onClick={() => setScriptOpen((value) => !value)}>
            <span>Script Sidebar</span>
            <strong>{scriptOpen ? 'Hide' : 'Show'}</strong>
          </button>
          {scriptOpen && activeScene && (
            <textarea
              value={activeScene.script}
              onChange={(event) => updateActiveScene({ script: event.target.value })}
              placeholder="Paste dialogue, action lines, narration, or beat notes for this scene..."
            />
          )}
        </section>

        <div className="movie-asset-categories">
          {MOVIE_ASSET_CATEGORIES.map((category) => (
            <section className="movie-category" key={category.name}>
              <button
                type="button"
                className="movie-section-toggle"
                onClick={() => setOpenCategories((prev) => ({ ...prev, [category.name]: !prev[category.name] }))}
              >
                <span style={{ color: CATEGORY_COLORS[category.name] }}>{category.name}</span>
                <strong>{activeScene ? counts[category.name] || 0 : 0}</strong>
              </button>
              {openCategories[category.name] && (
                <div className="movie-tool-grid">
                  {category.items.map((item) => (
                    <button
                      type="button"
                      className={`movie-tool ${selectedTool === item.type ? 'active' : ''}`}
                      key={item.type}
                      onClick={() => {
                        setSelectedTool(item.type);
                        setMode('Place');
                        setStatus(`${item.label} selected.`);
                      }}
                    >
                      <MovieAssetIcon asset={{ ...item, category: category.name }} compact />
                      <span>{item.label}</span>
                    </button>
                  ))}
                </div>
              )}
            </section>
          ))}
        </div>
      </aside>

      <main className="movie-main">
        <div className="movie-toolbar">
          <div className="studio-mode-buttons">
            {['Place', 'Select', 'Erase'].map((item) => (
              <button type="button" className={`preset-pill ${mode === item ? 'active' : ''}`} key={item} onClick={() => setMode(item)}>
                {item}
              </button>
            ))}
          </div>
          <div className="movie-toolbar-actions">
            <button type="button" className="secondary-action-btn" onClick={handleUndo} disabled={history.past.length === 0}>Undo</button>
            <button type="button" className="secondary-action-btn" onClick={handleRedo} disabled={history.future.length === 0}>Redo</button>
            <button type="button" className="secondary-action-btn" onClick={() => updateActiveScene({ showGrid: !activeScene?.showGrid })}>Grid {activeScene?.showGrid === false ? 'Off' : 'On'}</button>
            <button type="button" className="secondary-action-btn" onClick={handleRandomScene}>Random Scene</button>
            <button type="button" className="secondary-action-btn" onClick={handlePlayScene}>Play Scene</button>
            <button type="button" className="secondary-action-btn" onClick={() => importRef.current?.click()}>Import JSON</button>
            <button type="button" className="secondary-action-btn" onClick={exportProject}>Export JSON</button>
            <button type="button" className="secondary-action-btn" onClick={exportShotList}>Shot List</button>
            <button type="button" className="secondary-action-btn" onClick={downloadBlenderBuilder}>Blender Builder</button>
            <button type="button" className="secondary-action-btn delete" onClick={handleClear}>Clear Canvas</button>
            <input ref={importRef} type="file" accept="application/json,.json" hidden onChange={importProject} />
          </div>
        </div>

        {activeScene && (
          <div className="movie-scene-controls">
            <label><span>Scene</span><input value={activeScene.description} onChange={(event) => updateActiveScene({ description: event.target.value })} placeholder="Scene description" /></label>
            <label><span>Location</span><input value={activeScene.locationName} onChange={(event) => updateActiveScene({ locationName: event.target.value })} /></label>
            <label><span>Duration</span><input type="number" min="1" max="240" value={activeScene.duration} onChange={(event) => updateActiveScene({ duration: Number(event.target.value) || 1 })} /></label>
            <label><span>Shot</span><select value={activeScene.shotType} onChange={(event) => updateActiveScene({ shotType: event.target.value })}>{SHOT_TYPES.map((shot) => <option key={shot}>{shot}</option>)}</select></label>
            <label><span>Aspect</span><select value={activeScene.aspectRatio} onChange={(event) => updateActiveScene({ aspectRatio: event.target.value })}>{Object.keys(ASPECTS).map((aspect) => <option key={aspect}>{aspect}</option>)}</select></label>
            <label><span>Grade</span><select value={activeScene.colorGrade} onChange={(event) => updateActiveScene({ colorGrade: event.target.value })}>{COLOR_GRADES.map((grade) => <option key={grade}>{grade}</option>)}</select></label>
            <div className="movie-toggle-pair">
              <button type="button" className="preset-pill active" onClick={() => updateActiveScene({ intExt: activeScene.intExt === 'INT' ? 'EXT' : 'INT' })}>{activeScene.intExt}</button>
              <button type="button" className="preset-pill active" onClick={() => updateActiveScene({ dayNight: activeScene.dayNight === 'Day' ? 'Night' : 'Day' })}>{activeScene.dayNight}</button>
            </div>
          </div>
        )}

        <div className="movie-count-strip">
          {MOVIE_ASSET_CATEGORIES.map((category) => (
            <span key={category.name} style={{ '--count-color': CATEGORY_COLORS[category.name] }}>
              {category.name}: {counts[category.name] || 0}
            </span>
          ))}
        </div>

        <div className="movie-storyboard-shell">
          <div
            className="movie-storyboard"
            style={{ aspectRatio: ASPECTS[activeScene?.aspectRatio || '16:9'] }}
            onClick={handleCanvasClick}
          >
            {activeScene?.showGrid !== false && (
              <div className="movie-rule-grid" aria-hidden="true">
                <span /><span /><span /><span />
              </div>
            )}
            <div className="movie-camera-frame" style={{ inset: getShotInset(activeScene?.shotType || 'Wide') }} />
            <div className="movie-grade-overlay" />
            {activeScene && getVisibleAssets(activeScene, layers).map((asset) => (
              <button
                key={asset.id}
                type="button"
                className={`movie-placed-asset layer-${asset.layer.toLowerCase()} motion-${(asset.motion?.type || 'Idle').toLowerCase().replace(/[^a-z0-9]+/g, '-')} ${selectedAssetId === asset.id ? 'selected' : ''}`}
                style={{
                  left: `${asset.x}%`,
                  top: `${asset.y}%`,
                  opacity: asset.opacity,
                  transform: `translate(-50%, -50%) scale(${asset.scale})`,
                  zIndex: layerZIndex(asset.layer) * 10,
                  '--motion-speed': `${1 / Math.max(0.25, asset.motion?.speed || 1)}s`,
                  '--asset-scale': asset.scale,
                }}
                onClick={(event) => handleAssetClick(asset, event)}
                onContextMenu={(event) => handleAssetContextMenu(asset, event)}
              >
                <MovieAssetIcon asset={asset} />
              </button>
            ))}
          </div>
          <div className="movie-status-bar">
            <span>{status}</span>
            <strong>{activeScene ? `Scene ${activeScene.sceneNumber} ${activeScene.intExt}. ${activeScene.locationName} - ${activeScene.dayNight}` : ''}</strong>
          </div>
        </div>

        <div className="movie-timeline">
          <button type="button" className="download-btn movie-add-scene" onClick={handleAddScene}>+ Add Scene</button>
          <div className="movie-scene-track">
            {scenes.map((scene) => (
              <button
                key={scene.id}
                type="button"
                draggable
                className={`movie-scene-card ${scene.id === activeSceneId ? 'active' : ''}`}
                onClick={() => { setActiveSceneId(scene.id); setSelectedAssetId(null); }}
                onDragStart={(event) => event.dataTransfer.setData('text/plain', scene.id)}
                onDragOver={(event) => event.preventDefault()}
                onDrop={(event) => handleSceneDrop(event.dataTransfer.getData('text/plain'), scene.id)}
              >
                <strong>Scene {scene.sceneNumber}</strong>
                <span>{scene.locationName}</span>
                <small>{scene.shotType} - {scene.duration}s</small>
              </button>
            ))}
          </div>
        </div>

        {contextMenu && (
          <div className="studio-context-menu" style={{ left: contextMenu.x, top: contextMenu.y }}>
            <button type="button" onClick={() => { setSelectedAssetId(contextMenu.assetId); setContextMenu(null); }}>Edit</button>
            <button type="button" onClick={() => duplicateAsset(contextMenu.assetId)}>Duplicate</button>
            <button type="button" onClick={() => deleteAsset(contextMenu.assetId)}>Delete</button>
          </div>
        )}
      </main>

      <aside className="movie-properties">
        <div className="studio-panel-block">
          <h3>Layer Manager</h3>
          {MOVIE_LAYERS.map((layer) => (
            <div className="studio-layer-row" key={layer}>
              <strong>{layer}</strong>
              <label><input type="checkbox" checked={layers[layer].visible} onChange={() => toggleLayer(layer, 'visible')} /> Visible</label>
              <label><input type="checkbox" checked={layers[layer].locked} onChange={() => toggleLayer(layer, 'locked')} /> Locked</label>
            </div>
          ))}
        </div>

        {selectedAsset && (selectedAsset.motionTarget === 'character' || selectedAsset.motionTarget === 'camera' || selectedAsset.motionTarget === 'vfx') && (
          <div className="studio-panel-block">
            <h3>Animation & Motion</h3>
            <label className="studio-property-row">
              <span>Motion Type</span>
              <select value={selectedAsset.motion?.type || motionTypes[0]} onChange={(event) => updateSelectedMotion('type', event.target.value)}>
                {motionTypes.map((motion) => <option key={motion}>{motion}</option>)}
              </select>
            </label>
            <label className="studio-property-row">
              <span>Speed {selectedAsset.motion?.speed || 1}x</span>
              <input type="range" min="0.25" max="3" step="0.25" value={selectedAsset.motion?.speed || 1} onChange={(event) => updateSelectedMotion('speed', Number(event.target.value))} />
            </label>
            <label className="studio-inline-check">
              <input type="checkbox" checked={selectedAsset.motion?.loop ?? true} onChange={(event) => updateSelectedMotion('loop', event.target.checked)} />
              Loop motion
            </label>
          </div>
        )}

        {selectedAsset ? (
          <div className="studio-panel-block">
            <h3>Properties</h3>
            <label className="studio-property-row"><span>Name</span><input value={selectedAsset.name} onChange={(event) => updateSelectedAsset('name', event.target.value)} /></label>
            <label className="studio-property-row"><span>Color / Costume Tint</span><input type="color" value={selectedAsset.color} onChange={(event) => updateSelectedAsset('color', event.target.value)} /></label>
            <label className="studio-property-row"><span>Scale {selectedAsset.scale}x</span><input type="range" min="0.5" max="3" step="0.1" value={selectedAsset.scale} onChange={(event) => updateSelectedAsset('scale', Number(event.target.value))} /></label>
            <label className="studio-property-row"><span>Opacity {Math.round(selectedAsset.opacity * 100)}%</span><input type="range" min="0.1" max="1" step="0.05" value={selectedAsset.opacity} onChange={(event) => updateSelectedAsset('opacity', Number(event.target.value))} /></label>
            <label className="studio-property-row"><span>Layer</span><select value={selectedAsset.layer} onChange={(event) => updateSelectedAsset('layer', event.target.value)}>{MOVIE_LAYERS.map((layer) => <option key={layer}>{layer}</option>)}</select></label>
            <label className="studio-property-row"><span>Facing Direction</span><select value={selectedAsset.facing} onChange={(event) => updateSelectedAsset('facing', event.target.value)}>{['Left', 'Right', 'Camera', 'Away'].map((direction) => <option key={direction}>{direction}</option>)}</select></label>
            <label className="studio-property-row"><span>Emotion / Expression</span><select value={selectedAsset.emotion} onChange={(event) => updateSelectedAsset('emotion', event.target.value)}>{['happy', 'angry', 'scared', 'neutral'].map((emotion) => <option key={emotion}>{emotion}</option>)}</select></label>
            <label className="studio-property-row notes"><span>Dev / Director Notes</span><textarea value={selectedAsset.notes} onChange={(event) => updateSelectedAsset('notes', event.target.value)} placeholder="Blocking, performance, camera notes..." /></label>
          </div>
        ) : (
          <div className="studio-panel-block muted">
            <h3>No Asset Selected</h3>
            <p>Select a cast member, prop, light, VFX overlay, or camera item to edit its properties and motion.</p>
          </div>
        )}
      </aside>
    </div>
  );
}

export default MovieProductionPanel;
