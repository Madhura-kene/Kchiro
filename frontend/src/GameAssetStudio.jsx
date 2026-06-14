import React, { useEffect, useRef, useState } from 'react';

const GRID_SIZE = 20;
const MAX_HISTORY = 20;
const LAYERS = ['Background', 'Midground', 'Foreground'];
const COLLISION_TYPES = ['Solid', 'Passthrough', 'Trigger'];
const ANIMATION_TYPES = [
  'Idle',
  'Walk',
  'Run',
  'Attack',
  'Jump',
  'Death',
  'Float',
  'Pulse',
  'Spin',
  'Flicker',
  'Bob',
  'Shake',
  'Collect',
  'Open Close',
];

const CATEGORY_COLORS = {
  Characters: '#38bdf8',
  Terrain: '#84cc16',
  Props: '#a16207',
  Collectibles: '#facc15',
  Hazards: '#f97316',
  Lighting: '#fde68a',
  VFX: '#c084fc',
  'Generated Assets': '#111111',
};

const ASSET_CATEGORIES = [
  {
    name: 'Characters',
    items: [
      { type: 'player', label: 'Player', color: '#38bdf8', layer: 'Midground', animated: true },
      { type: 'npc', label: 'NPC', color: '#22c55e', layer: 'Midground', animated: true },
      { type: 'enemy_grunt', label: 'Enemy Grunt', color: '#ef4444', layer: 'Midground', animated: true },
      { type: 'enemy_ranged', label: 'Enemy Ranged', color: '#fb7185', layer: 'Midground', animated: true },
      { type: 'enemy_boss', label: 'Enemy Boss', color: '#a855f7', layer: 'Midground', animated: true, size: 1.3 },
    ],
  },
  {
    name: 'Terrain',
    items: [
      { type: 'grass', label: 'Grass Tile', color: '#4ade80', layer: 'Background' },
      { type: 'dirt', label: 'Dirt Tile', color: '#a16207', layer: 'Background' },
      { type: 'stone', label: 'Stone Tile', color: '#94a3b8', layer: 'Background' },
      { type: 'water', label: 'Water Tile', color: '#38bdf8', layer: 'Background', animated: true },
      { type: 'lava', label: 'Lava Tile', color: '#fb923c', layer: 'Background', animated: true },
      { type: 'brick_wall', label: 'Brick Wall', color: '#b45309', layer: 'Midground' },
      { type: 'wood_wall', label: 'Wood Wall', color: '#92400e', layer: 'Midground' },
      { type: 'metal_wall', label: 'Metal Wall', color: '#64748b', layer: 'Midground' },
      { type: 'platform', label: 'Platform', color: '#d97706', layer: 'Midground' },
      { type: 'slope', label: 'Slope', color: '#78716c', layer: 'Midground' },
    ],
  },
  {
    name: 'Props',
    items: [
      { type: 'crate', label: 'Crate', color: '#b45309', layer: 'Midground' },
      { type: 'tree', label: 'Tree', color: '#22c55e', layer: 'Midground' },
      { type: 'rock', label: 'Rock', color: '#94a3b8', layer: 'Midground' },
      { type: 'door', label: 'Door', color: '#78350f', layer: 'Midground' },
      { type: 'chest', label: 'Chest', color: '#f59e0b', layer: 'Midground' },
      { type: 'torch_prop', label: 'Torch', color: '#fb923c', layer: 'Foreground', animated: true },
      { type: 'barrel', label: 'Barrel', color: '#92400e', layer: 'Midground' },
    ],
  },
  {
    name: 'Collectibles',
    items: [
      { type: 'coin', label: 'Coin', color: '#facc15', layer: 'Foreground', animated: true },
      { type: 'gem', label: 'Gem', color: '#a78bfa', layer: 'Foreground', animated: true },
      { type: 'health', label: 'Health Pickup', color: '#ef4444', layer: 'Foreground', animated: true },
      { type: 'sword_pickup', label: 'Sword', color: '#e5e7eb', layer: 'Foreground' },
      { type: 'gun_pickup', label: 'Gun', color: '#64748b', layer: 'Foreground' },
      { type: 'bow_pickup', label: 'Bow', color: '#a16207', layer: 'Foreground' },
    ],
  },
  {
    name: 'Hazards',
    items: [
      { type: 'spikes', label: 'Spikes', color: '#e5e7eb', layer: 'Midground' },
      { type: 'fire', label: 'Fire', color: '#f97316', layer: 'Midground', animated: true },
      { type: 'trap', label: 'Trap', color: '#dc2626', layer: 'Midground' },
      { type: 'electric_panel', label: 'Electric Panel', color: '#22d3ee', layer: 'Midground', animated: true },
    ],
  },
  {
    name: 'Lighting',
    items: [
      { type: 'point_light', label: 'Point Light', color: '#fde68a', layer: 'Foreground', animated: true },
      { type: 'torch_light', label: 'Torch Light', color: '#fb923c', layer: 'Foreground', animated: true },
      { type: 'lantern', label: 'Lantern', color: '#facc15', layer: 'Foreground', animated: true },
    ],
  },
  {
    name: 'VFX',
    items: [
      { type: 'explosion', label: 'Explosion', color: '#fb923c', layer: 'Foreground', animated: true },
      { type: 'dust_cloud', label: 'Dust Cloud', color: '#d6d3d1', layer: 'Foreground', animated: true },
      { type: 'magic_sparkle', label: 'Magic Sparkle', color: '#c084fc', layer: 'Foreground', animated: true },
      { type: 'smoke_puff', label: 'Smoke Puff', color: '#94a3b8', layer: 'Foreground', animated: true },
      { type: 'coin_pop', label: 'Coin Pop', color: '#facc15', layer: 'Foreground', animated: true },
    ],
  },
];

const ASSET_LOOKUP = ASSET_CATEGORIES.flatMap((category) =>
  category.items.map((item) => ({ ...item, category: category.name }))
).reduce((lookup, item) => {
  lookup[item.type] = item;
  return lookup;
}, {});

const makeId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `asset-${Date.now()}-${Math.random().toString(16).slice(2)}`;
};

const formatAssetTypeLabel = (value = '') =>
  String(value)
    .replace(/[_:-]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/\b\w/g, (letter) => letter.toUpperCase());

const getAnimationClassName = (type = 'Idle') =>
  `studio-anim-${String(type).toLowerCase().replace(/[^a-z0-9]+/g, '-') || 'idle'}`;

const getAssetRenderSrc = (asset, apiBaseUrl = '') => {
  const path = asset?.renderPath || asset?.render_path;
  if (!path) return null;
  if (/^(https?:|data:|blob:)/i.test(path)) return path;
  return `${apiBaseUrl}${path}`;
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

const layerZIndex = (layer) => LAYERS.indexOf(layer) + 1;

const getCategoryCounts = (assets, categories = ASSET_CATEGORIES) =>
  categories.reduce((counts, category) => {
    counts[category.name] = assets.filter((asset) => asset.category === category.name).length;
    return counts;
  }, {});

const createPlacedAsset = (definition, x, y, overrides = {}) => ({
  id: makeId(),
  type: definition.type,
  category: definition.category,
  name: definition.label,
  label: definition.label,
  x,
  y,
  color: definition.color,
  size: definition.size || 1,
  facing: 'Down',
  opacity: 1,
  layer: definition.layer || 'Midground',
  collision: definition.category === 'Terrain' ? 'Solid' : 'Passthrough',
  tags: '',
  notes: '',
  animation: {
    type: definition.animated ? 'Idle' : 'Idle',
    speed: 1,
    loop: true,
    enabled: Boolean(definition.animated || definition.category === 'Characters'),
  },
  animated: Boolean(definition.animated || definition.category === 'Characters'),
  backendAssetId: definition.backendAssetId,
  glbPath: definition.glbPath,
  renderPath: definition.renderPath,
  sourcePrompt: definition.prompt,
  ...overrides,
});

const getAssetsAtCell = (assets, x, y, layers) =>
  assets
    .filter((asset) => asset.x === x && asset.y === y && layers[asset.layer]?.visible)
    .sort((a, b) => layerZIndex(a.layer) - layerZIndex(b.layer));

const getTopAssetAtCell = (assets, x, y, layers) => {
  const cellAssets = getAssetsAtCell(assets, x, y, layers);
  return cellAssets[cellAssets.length - 1] || null;
};

const buildBlenderScript = (layout) => {
  const encoded = encodeBase64(JSON.stringify(layout));
  return `# Game Asset Studio Blender scene builder
# Run this script inside Blender. It creates the scene and saves a .blend file next to the current file.
import base64
import json
import math
import bpy

LAYOUT_JSON = json.loads(base64.b64decode("${encoded}").decode("utf-8"))

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

materials = {}

def hex_to_rgba(hex_color, alpha=1.0):
    value = (hex_color or "#ffffff").lstrip("#")
    if len(value) != 6:
        value = "ffffff"
    return tuple(int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (alpha,)

def get_mat(name, color, alpha=1.0):
    key = f"{name}_{color}_{alpha}"
    if key in materials:
        return materials[key]
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = hex_to_rgba(color, alpha)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = hex_to_rgba(color, alpha)
        bsdf.inputs["Alpha"].default_value = alpha
    if alpha < 1:
        mat.blend_method = "BLEND"
    materials[key] = mat
    return mat

def cube(name, x, y, z, sx, sy, sz, color, alpha=1.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(get_mat(name + "_mat", color, alpha))
    return obj

layer_heights = {"Background": 0.03, "Midground": 0.22, "Foreground": 0.42}
category_heights = {
    "Terrain": 0.08,
    "Characters": 0.9,
    "Props": 0.55,
    "Collectibles": 0.25,
    "Hazards": 0.35,
    "Lighting": 0.75,
    "VFX": 0.35,
}

for asset in LAYOUT_JSON.get("assets", []):
    x = asset.get("x", 0) - 10
    y = 10 - asset.get("y", 0)
    size = asset.get("size", 1)
    category = asset.get("category", "Props")
    layer = asset.get("layer", "Midground")
    color = asset.get("color", "#ffffff")
    opacity = asset.get("opacity", 1)
    height = category_heights.get(category, 0.45) * size
    base_z = layer_heights.get(layer, 0.2)
    animation = asset.get("animation") or {}
    if category == "Terrain":
        created = [cube(asset.get("name", "terrain"), x, y, base_z, size, size, height, color, opacity)]
    elif category == "Characters":
        created = [
            cube(asset.get("name", "character") + "_body", x, y, base_z + height / 2, 0.42 * size, 0.42 * size, height, color, opacity),
            cube(asset.get("name", "character") + "_head", x, y, base_z + height + 0.16 * size, 0.32 * size, 0.32 * size, 0.28 * size, color, opacity),
        ]
    elif category == "Lighting":
        created = [
            cube(asset.get("name", "light") + "_pole", x, y, base_z + 0.34 * size, 0.12 * size, 0.12 * size, 0.68 * size, "#1f2937", opacity),
            cube(asset.get("name", "light") + "_lamp", x, y, base_z + 0.76 * size, 0.34 * size, 0.34 * size, 0.16 * size, color, 0.85),
        ]
    else:
        created = [cube(asset.get("name", "asset"), x, y, base_z + height / 2, 0.7 * size, 0.7 * size, height, color, opacity)]

    anim_enabled = bool(animation.get("enabled", asset.get("animated", False)))
    anim_type = str(animation.get("type", "Idle")).lower().replace(" ", "_")
    speed = max(0.25, float(animation.get("speed", 1) or 1))
    frame_span = max(8, int(48 / speed))
    if anim_enabled:
        for obj in created:
            obj["kchiro_animation_type"] = anim_type
            obj["kchiro_animation_speed"] = speed
            start_loc = obj.location.copy()
            start_rot = obj.rotation_euler.copy()
            start_scale = obj.scale.copy()
            obj.keyframe_insert(data_path="location", frame=1)
            obj.keyframe_insert(data_path="rotation_euler", frame=1)
            obj.keyframe_insert(data_path="scale", frame=1)
            if anim_type in {"walk", "run"}:
                obj.location.x += (0.45 if anim_type == "run" else 0.25) * size
            elif anim_type in {"jump", "float", "bob", "collect"}:
                obj.location.z += (0.55 if anim_type == "jump" else 0.22) * size
            elif anim_type in {"attack", "shake"}:
                obj.rotation_euler.z += math.radians(18 if anim_type == "attack" else 7)
            elif anim_type == "death":
                obj.rotation_euler.z += math.radians(85)
            elif anim_type == "spin":
                obj.rotation_euler.z += math.radians(360)
            elif anim_type in {"pulse", "flicker"}:
                obj.scale = (start_scale.x * 1.18, start_scale.y * 1.18, start_scale.z * 1.18)
            elif anim_type == "open_close":
                obj.rotation_euler.x += math.radians(28)
            obj.keyframe_insert(data_path="location", frame=frame_span // 2)
            obj.keyframe_insert(data_path="rotation_euler", frame=frame_span // 2)
            obj.keyframe_insert(data_path="scale", frame=frame_span // 2)
            obj.location = start_loc
            obj.rotation_euler = start_rot
            obj.scale = start_scale
            obj.keyframe_insert(data_path="location", frame=frame_span)
            obj.keyframe_insert(data_path="rotation_euler", frame=frame_span)
            obj.keyframe_insert(data_path="scale", frame=frame_span)
            if animation.get("loop", True) and obj.animation_data and obj.animation_data.action:
                for curve in obj.animation_data.action.fcurves:
                    curve.modifiers.new(type="CYCLES")

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 96

bpy.ops.object.light_add(type="SUN", location=(0, -5, 9))
bpy.context.object.name = "Studio Sun"
bpy.context.object.data.energy = 2.2
bpy.ops.object.camera_add(location=(9, -12, 11), rotation=(math.radians(60), 0, math.radians(42)))
bpy.context.scene.camera = bpy.context.object
bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath("//game_asset_studio_scene.blend"))
`;
};

const GameAssetIcon = ({ asset, mode = '2d', compact = false, apiBaseUrl = '' }) => {
  const color = asset.color || ASSET_LOOKUP[asset.type]?.color || '#cbd5e1';
  const type = asset.type;
  const category = asset.category || ASSET_LOOKUP[type]?.category || 'Props';
  const is3D = mode === '3d';
  const stroke = '#0f172a';
  const renderSrc = getAssetRenderSrc(asset, apiBaseUrl);

  if (renderSrc) {
    return (
      <span className={`studio-generated-preview ${compact ? 'compact' : ''}`}>
        <img src={renderSrc} alt="" loading="lazy" />
      </span>
    );
  }

  if (is3D && category === 'Terrain') {
    return (
      <svg className={`studio-icon ${compact ? 'compact' : ''}`} viewBox="0 0 80 80" aria-hidden="true">
        <polygon points="40,10 72,28 40,46 8,28" fill={color} stroke={stroke} strokeWidth="3" />
        <polygon points="8,28 40,46 40,68 8,50" fill="#475569" opacity="0.85" stroke={stroke} strokeWidth="2" />
        <polygon points="72,28 40,46 40,68 72,50" fill="#1f2937" opacity="0.85" stroke={stroke} strokeWidth="2" />
        {type.includes('water') && <path d="M21 29c8-5 13 5 21 0s12 4 18 0" fill="none" stroke="#e0f2fe" strokeWidth="3" opacity="0.75" />}
        {type.includes('lava') && <path d="M20 29c7-4 12 4 19 0s13 4 21 0" fill="none" stroke="#fef3c7" strokeWidth="3" opacity="0.9" />}
      </svg>
    );
  }

  if (category === 'Characters') {
    return (
      <svg className={`studio-icon ${compact ? 'compact' : ''}`} viewBox="0 0 80 80" aria-hidden="true">
        {is3D && <ellipse cx="40" cy="62" rx="21" ry="7" fill="#020617" opacity="0.35" />}
        <circle cx="40" cy="24" r={type === 'enemy_boss' ? 14 : 11} fill={color} stroke={stroke} strokeWidth="3" />
        <path d="M28 56c2-18 22-18 24 0Z" fill={color} stroke={stroke} strokeWidth="3" />
        <circle cx="36" cy="23" r="2" fill="#020617" />
        <circle cx="44" cy="23" r="2" fill="#020617" />
        {type.includes('ranged') && <path d="M54 40h16M65 35l5 5-5 5" stroke="#f8fafc" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />}
        {type.includes('boss') && <path d="M27 13l-8-8M53 13l8-8" stroke="#facc15" strokeWidth="4" strokeLinecap="round" />}
      </svg>
    );
  }

  if (category === 'Collectibles') {
    return (
      <svg className={`studio-icon ${compact ? 'compact' : ''}`} viewBox="0 0 80 80" aria-hidden="true">
        {type === 'coin' && <circle cx="40" cy="40" r="22" fill={color} stroke={stroke} strokeWidth="4" />}
        {type === 'coin' && <circle cx="40" cy="40" r="12" fill="none" stroke="#fef3c7" strokeWidth="4" />}
        {type === 'gem' && <polygon points="40,12 61,31 51,62 29,62 19,31" fill={color} stroke={stroke} strokeWidth="4" />}
        {type === 'health' && <path d="M40 64C13 41 20 18 36 26c2 1 3 3 4 5 1-2 2-4 4-5 16-8 23 15-4 38Z" fill={color} stroke={stroke} strokeWidth="4" />}
        {type.includes('sword') && <path d="M23 61 58 18l5-1-1 5-35 43ZM24 45l12 12" stroke={color} strokeWidth="8" strokeLinecap="round" />}
        {type.includes('gun') && <path d="M17 35h43v13H44l-8 15H26l5-15H17Z" fill={color} stroke={stroke} strokeWidth="4" />}
        {type.includes('bow') && <path d="M52 13c-22 12-22 42 0 54M53 13v54M20 40h36" fill="none" stroke={color} strokeWidth="5" strokeLinecap="round" />}
      </svg>
    );
  }

  if (category === 'Hazards') {
    return (
      <svg className={`studio-icon ${compact ? 'compact' : ''}`} viewBox="0 0 80 80" aria-hidden="true">
        {type === 'spikes' && <path d="M8 61 20 26l12 35 12-35 12 35 12-35 8 35Z" fill={color} stroke={stroke} strokeWidth="4" />}
        {type === 'fire' && <path d="M40 67c-15-8-18-24-7-36 4-4 5-10 4-18 17 13 27 34 3 54Z" fill={color} stroke={stroke} strokeWidth="4" />}
        {type === 'trap' && <rect x="16" y="23" width="48" height="36" rx="6" fill={color} stroke={stroke} strokeWidth="4" />}
        {type === 'trap' && <path d="M22 32h36M22 43h36M22 54h36" stroke="#fecaca" strokeWidth="3" />}
        {type === 'electric_panel' && <rect x="18" y="15" width="44" height="50" rx="7" fill="#1f2937" stroke="#22d3ee" strokeWidth="4" />}
        {type === 'electric_panel' && <path d="m43 22-13 20h10l-5 17 15-23H40Z" fill={color} />}
      </svg>
    );
  }

  if (category === 'Lighting' || type.includes('torch')) {
    return (
      <svg className={`studio-icon ${compact ? 'compact' : ''}`} viewBox="0 0 80 80" aria-hidden="true">
        <circle cx="42" cy="25" r="21" fill={color} opacity="0.22" />
        <path d="M40 65V30" stroke="#1f2937" strokeWidth="7" strokeLinecap="round" />
        <path d="M31 29h18l-4-11H35Z" fill={color} stroke={stroke} strokeWidth="3" />
        <circle cx="40" cy="24" r="6" fill="#fff7ed" />
      </svg>
    );
  }

  if (category === 'VFX') {
    return (
      <svg className={`studio-icon ${compact ? 'compact' : ''}`} viewBox="0 0 80 80" aria-hidden="true">
        <path d="M40 8 47 30l23-8-16 19 18 16-24-3-8 20-8-20-24 3 18-16-16-19 23 8Z" fill={color} stroke={stroke} strokeWidth="3" opacity="0.9" />
        <circle cx="40" cy="41" r="11" fill="#fff7ed" opacity="0.55" />
      </svg>
    );
  }

  if (type === 'tree') {
    return (
      <svg className={`studio-icon ${compact ? 'compact' : ''}`} viewBox="0 0 80 80" aria-hidden="true">
        <rect x="35" y="43" width="10" height="24" rx="3" fill="#78350f" />
        <circle cx="31" cy="35" r="16" fill={color} stroke={stroke} strokeWidth="3" />
        <circle cx="48" cy="33" r="18" fill={color} stroke={stroke} strokeWidth="3" />
        <circle cx="40" cy="22" r="16" fill="#16a34a" stroke={stroke} strokeWidth="3" />
      </svg>
    );
  }

  if (type === 'rock') {
    return (
      <svg className={`studio-icon ${compact ? 'compact' : ''}`} viewBox="0 0 80 80" aria-hidden="true">
        <path d="M13 59 24 31l22-13 20 17 3 24Z" fill={color} stroke={stroke} strokeWidth="4" />
        <path d="M24 31 39 40l7-22M39 40l30 19" stroke="#cbd5e1" strokeWidth="3" opacity="0.55" />
      </svg>
    );
  }

  return (
    <svg className={`studio-icon ${compact ? 'compact' : ''}`} viewBox="0 0 80 80" aria-hidden="true">
      <rect x="18" y="22" width="44" height="39" rx="7" fill={color} stroke={stroke} strokeWidth="4" />
      {type === 'crate' && <path d="M18 22 62 61M62 22 18 61M18 42h44" stroke="#fef3c7" strokeWidth="4" opacity="0.75" />}
      {type === 'barrel' && <path d="M23 26h34M23 57h34M19 39h42" stroke="#fef3c7" strokeWidth="4" opacity="0.75" />}
      {type === 'door' && <circle cx="50" cy="42" r="3" fill="#facc15" />}
      {type === 'chest' && <path d="M18 39h44M35 39v10h10V39" stroke="#facc15" strokeWidth="4" />}
    </svg>
  );
};

function GameAssetStudio({ generatedAssets = [], apiBaseUrl = '' }) {
  const [gameMode, setGameMode] = useState(null);
  const [studioMode, setStudioMode] = useState('Place');
  const [selectedTool, setSelectedTool] = useState('player');
  const [openCategories, setOpenCategories] = useState(() =>
    ASSET_CATEGORIES.reduce((state, category) => ({ ...state, [category.name]: true }), {})
  );
  const [assets, setAssets] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [gridlines, setGridlines] = useState(true);
  const [layers, setLayers] = useState({
    Background: { visible: true, locked: false },
    Midground: { visible: true, locked: false },
    Foreground: { visible: true, locked: false },
  });
  const [dayMode, setDayMode] = useState('Day');
  const [fogOpacity, setFogOpacity] = useState(0);
  const [history, setHistory] = useState({ past: [], future: [] });
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [spaceDown, setSpaceDown] = useState(false);
  const [isPanning, setIsPanning] = useState(false);
  const [panStart, setPanStart] = useState(null);
  const [contextMenu, setContextMenu] = useState(null);
  const [status, setStatus] = useState('Pick 2D or 3D to begin.');
  const importRef = useRef(null);

  const completedGeneratedAssets = generatedAssets.filter((asset) => asset.status === 'completed' && asset.glb_path);
  const generatedCategory = {
    name: 'Generated Assets',
    items: completedGeneratedAssets.map((asset) => ({
      type: `generated-${asset.id}`,
      label: `${formatAssetTypeLabel(asset.asset_type)} #${asset.id}`,
      color: asset.parameters?.custom_color || '#111111',
      layer: 'Midground',
      animated: false,
      backendAssetId: asset.id,
      glbPath: asset.glb_path,
      renderPath: asset.render_path,
      prompt: asset.prompt,
      size: 1,
    })),
  };
  const studioCategories = generatedCategory.items.length > 0
    ? [...ASSET_CATEGORIES, generatedCategory]
    : ASSET_CATEGORIES;
  const studioLookup = studioCategories.flatMap((category) =>
    category.items.map((item) => ({ ...item, category: category.name }))
  ).reduce((lookup, item) => {
    lookup[item.type] = item;
    return lookup;
  }, {});
  const selectedAsset = selectedIds.length === 1 ? assets.find((asset) => asset.id === selectedIds[0]) : null;
  const selectedDefinition = studioLookup[selectedTool] || studioLookup.player || ASSET_LOOKUP.player;
  const categoryCounts = getCategoryCounts(assets, studioCategories);

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.code === 'Space') {
        event.preventDefault();
        setSpaceDown(true);
      }
    };
    const handleKeyUp = (event) => {
      if (event.code === 'Space') {
        setSpaceDown(false);
        setIsPanning(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  const commitAssets = (nextAssets, nextSelected = selectedIds) => {
    setHistory((prev) => ({
      past: [...prev.past.slice(-(MAX_HISTORY - 1)), assets],
      future: [],
    }));
    setAssets(nextAssets);
    setSelectedIds(nextSelected);
  };

  const resetStudio = (nextMode = gameMode) => {
    setAssets([]);
    setSelectedIds([]);
    setHistory({ past: [], future: [] });
    setZoom(1);
    setPan({ x: 0, y: 0 });
    setContextMenu(null);
    setGameMode(nextMode);
    setStatus(`${nextMode === '3d' ? '3D' : '2D'} Game Studio ready. Select a built-in piece or generated asset, then click the grid.`);
  };

  const handlePickMode = (mode) => {
    resetStudio(mode);
  };

  const handleSwitchMode = () => {
    const nextMode = gameMode === '2d' ? '3d' : '2d';
    if (assets.length > 0 && !window.confirm('Switching mode resets the current canvas. Continue?')) {
      return;
    }
    resetStudio(nextMode);
  };

  const handleUndo = () => {
    setHistory((prev) => {
      if (prev.past.length === 0) return prev;
      const previous = prev.past[prev.past.length - 1];
      setAssets(previous);
      setSelectedIds([]);
      setStatus('Undo applied.');
      return {
        past: prev.past.slice(0, -1),
        future: [assets, ...prev.future].slice(0, MAX_HISTORY),
      };
    });
  };

  const handleRedo = () => {
    setHistory((prev) => {
      if (prev.future.length === 0) return prev;
      const next = prev.future[0];
      setAssets(next);
      setSelectedIds([]);
      setStatus('Redo applied.');
      return {
        past: [...prev.past.slice(-(MAX_HISTORY - 1)), assets],
        future: prev.future.slice(1),
      };
    });
  };

  const isLayerLocked = (layer) => Boolean(layers[layer]?.locked);

  const handleCellClick = (x, y, event) => {
    setContextMenu(null);
    if (spaceDown) return;

    const topAsset = getTopAssetAtCell(assets, x, y, layers);

    if (studioMode === 'Select') {
      if (!topAsset) {
        if (!event.shiftKey) setSelectedIds([]);
        return;
      }
      setSelectedIds((prev) =>
        event.shiftKey
          ? prev.includes(topAsset.id) ? prev.filter((id) => id !== topAsset.id) : [...prev, topAsset.id]
          : [topAsset.id]
      );
      setStatus(`Selected ${topAsset.name}.`);
      return;
    }

    if (studioMode === 'Erase') {
      if (!topAsset || isLayerLocked(topAsset.layer)) return;
      commitAssets(assets.filter((asset) => asset.id !== topAsset.id), selectedIds.filter((id) => id !== topAsset.id));
      setStatus(`Deleted ${topAsset.name}.`);
      return;
    }

    if (studioMode === 'Fill') {
      if (isLayerLocked(selectedDefinition.layer || 'Midground')) {
        setStatus(`${selectedDefinition.layer} is locked.`);
        return;
      }
      const occupied = new Set(assets.map((asset) => `${asset.x}:${asset.y}:${asset.layer}`));
      const filled = [];
      for (let row = 0; row < GRID_SIZE; row += 1) {
        for (let col = 0; col < GRID_SIZE; col += 1) {
          const key = `${col}:${row}:${selectedDefinition.layer || 'Midground'}`;
          if (!occupied.has(key)) {
            filled.push(createPlacedAsset(selectedDefinition, col, row));
          }
        }
      }
      commitAssets([...assets, ...filled]);
      setStatus(`Filled ${filled.length} empty ${selectedDefinition.layer || 'Midground'} cells.`);
      return;
    }

    if (isLayerLocked(selectedDefinition.layer || 'Midground')) {
      setStatus(`${selectedDefinition.layer} is locked.`);
      return;
    }

    const placed = createPlacedAsset(selectedDefinition, x, y);
    commitAssets([...assets, placed], [placed.id]);
    setStatus(`Placed ${placed.name} at row ${y + 1}, column ${x + 1}.`);
  };

  const handleContextMenu = (x, y, event) => {
    event.preventDefault();
    const topAsset = getTopAssetAtCell(assets, x, y, layers);
    if (!topAsset) return;
    setSelectedIds([topAsset.id]);
    setContextMenu({
      x: event.clientX,
      y: event.clientY,
      assetId: topAsset.id,
    });
  };

  const duplicateAsset = (assetId) => {
    const source = assets.find((asset) => asset.id === assetId);
    if (!source || isLayerLocked(source.layer)) return;
    const duplicate = {
      ...source,
      id: makeId(),
      name: `${source.name} Copy`,
      x: Math.min(GRID_SIZE - 1, source.x + 1),
      y: Math.min(GRID_SIZE - 1, source.y + 1),
    };
    commitAssets([...assets, duplicate], [duplicate.id]);
    setContextMenu(null);
    setStatus(`Duplicated ${source.name}.`);
  };

  const deleteAsset = (assetId) => {
    const source = assets.find((asset) => asset.id === assetId);
    if (!source || isLayerLocked(source.layer)) return;
    commitAssets(assets.filter((asset) => asset.id !== assetId), selectedIds.filter((id) => id !== assetId));
    setContextMenu(null);
    setStatus(`Deleted ${source.name}.`);
  };

  const updateSelectedAsset = (field, value) => {
    if (!selectedAsset) return;
    setAssets((prev) => prev.map((asset) => (asset.id === selectedAsset.id ? { ...asset, [field]: value } : asset)));
  };

  const updateSelectedAnimation = (field, value) => {
    if (!selectedAsset) return;
    setAssets((prev) =>
      prev.map((asset) =>
        asset.id === selectedAsset.id
          ? {
              ...asset,
              animation: {
                type: 'Idle',
                speed: 1,
                loop: true,
                enabled: Boolean(asset.animated),
                ...asset.animation,
                [field]: value,
                ...(field === 'type' || field === 'speed' ? { enabled: true } : {}),
              },
              animated: field === 'enabled' ? Boolean(value) : true,
            }
          : asset
      )
    );
  };

  const handleWheel = (event) => {
    event.preventDefault();
    setZoom((current) => {
      const next = current + (event.deltaY < 0 ? 0.08 : -0.08);
      return Math.max(0.55, Math.min(2.5, Number(next.toFixed(2))));
    });
  };

  const handleCanvasMouseDown = (event) => {
    if (!spaceDown) return;
    setIsPanning(true);
    setPanStart({ x: event.clientX - pan.x, y: event.clientY - pan.y });
  };

  const handleCanvasMouseMove = (event) => {
    if (!isPanning || !panStart) return;
    setPan({ x: event.clientX - panStart.x, y: event.clientY - panStart.y });
  };

  const handleExportJson = () => {
    const layout = {
      version: 1,
      source: 'kchiro Game Asset Studio',
      gameMode,
      gridSize: GRID_SIZE,
      gridlines,
      dayMode,
      fogOpacity,
      layers,
      assets,
    };
    downloadTextFile('game_asset_studio_layout.json', JSON.stringify(layout, null, 2));
    setStatus('Exported JSON layout.');
  };

  const handleDownloadBlender = () => {
    const layout = {
      version: 1,
      source: 'kchiro Game Asset Studio',
      gameMode,
      gridSize: GRID_SIZE,
      assets,
    };
    downloadTextFile('game_asset_studio_blender_builder.py', buildBlenderScript(layout), 'text/x-python');
    setStatus('Downloaded Blender scene builder script. Run it in Blender to create the .blend file.');
  };

  const handleImportJson = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const data = JSON.parse(await file.text());
      if (!Array.isArray(data.assets)) {
        throw new Error('JSON does not contain an assets array.');
      }
      setAssets(data.assets.map((asset) => ({
        ...asset,
        animation: {
          type: 'Idle',
          speed: 1,
          loop: true,
          enabled: Boolean(asset.animated),
          ...asset.animation,
        },
      })));
      setGameMode(data.gameMode === '3d' ? '3d' : '2d');
      setGridlines(data.gridlines ?? true);
      setDayMode(data.dayMode || 'Day');
      setFogOpacity(Number(data.fogOpacity || 0));
      setLayers(data.layers || layers);
      setSelectedIds([]);
      setHistory({ past: [], future: [] });
      setStatus(`Imported ${data.assets.length} assets.`);
    } catch (error) {
      setStatus(`Import failed: ${error.message}`);
    } finally {
      event.target.value = '';
    }
  };

  const handleClear = () => {
    if (assets.length > 0 && !window.confirm('Clear the entire Game Asset Studio canvas?')) {
      return;
    }
    commitAssets([], []);
    setStatus('Canvas cleared.');
  };

  const handleRandomLevel = () => {
    const next = [];
    const terrainTypes = ['grass', 'dirt', 'stone'];
    for (let y = 0; y < GRID_SIZE; y += 1) {
      for (let x = 0; x < GRID_SIZE; x += 1) {
        const type = terrainTypes[(x + y) % terrainTypes.length];
        next.push(createPlacedAsset(ASSET_LOOKUP[type], x, y));
      }
    }
    for (let i = 0; i < GRID_SIZE; i += 1) {
      next.push(createPlacedAsset(ASSET_LOOKUP.brick_wall, i, 0));
      next.push(createPlacedAsset(ASSET_LOOKUP.brick_wall, i, GRID_SIZE - 1));
      next.push(createPlacedAsset(ASSET_LOOKUP.brick_wall, 0, i));
      next.push(createPlacedAsset(ASSET_LOOKUP.brick_wall, GRID_SIZE - 1, i));
    }
    next.push(createPlacedAsset(ASSET_LOOKUP.player, 2, 2));
    next.push(createPlacedAsset(ASSET_LOOKUP.enemy_grunt, 14, 7));
    next.push(createPlacedAsset(ASSET_LOOKUP.enemy_ranged, 17, 12));
    next.push(createPlacedAsset(ASSET_LOOKUP.chest, 10, 10));
    next.push(createPlacedAsset(ASSET_LOOKUP.coin, 6, 5));
    next.push(createPlacedAsset(ASSET_LOOKUP.gem, 15, 15));
    next.push(createPlacedAsset(ASSET_LOOKUP.spikes, 9, 12));
    next.push(createPlacedAsset(ASSET_LOOKUP.fire, 12, 13));
    next.push(createPlacedAsset(ASSET_LOOKUP.tree, 4, 14));
    next.push(createPlacedAsset(ASSET_LOOKUP.rock, 7, 16));
    next.push(createPlacedAsset(ASSET_LOOKUP.lantern, 3, 3));
    commitAssets(next, []);
    setStatus('Random level generated with terrain, borders, enemies, pickups, props, and hazards.');
  };

  const toggleLayer = (layer, field) => {
    setLayers((prev) => ({
      ...prev,
      [layer]: {
        ...prev[layer],
        [field]: !prev[layer][field],
      },
    }));
  };

  const renderGridCells = () => {
    const cells = [];
    for (let y = 0; y < GRID_SIZE; y += 1) {
      for (let x = 0; x < GRID_SIZE; x += 1) {
        const cellAssets = getAssetsAtCell(assets, x, y, layers);
        cells.push(
          <button
            key={`${x}-${y}`}
            type="button"
            className={`studio-cell ${gridlines ? 'show-grid' : ''}`}
            onClick={(event) => handleCellClick(x, y, event)}
            onContextMenu={(event) => handleContextMenu(x, y, event)}
            aria-label={`Game grid row ${y + 1}, column ${x + 1}`}
          >
            {cellAssets.map((asset) => {
              const isSelected = selectedIds.includes(asset.id);
              const animation = {
                type: 'Idle',
                speed: 1,
                loop: true,
                enabled: Boolean(asset.animated),
                ...asset.animation,
              };
              return (
                <span
                  key={asset.id}
                  className={`studio-asset-chip ${isSelected ? 'selected' : ''} studio-layer-${asset.layer.toLowerCase()} ${animation.enabled ? 'is-animated' : ''}`}
                  style={{
                    '--asset-scale': asset.size,
                    '--asset-opacity': asset.opacity,
                    '--asset-speed': `${1 / Math.max(0.25, animation.speed || 1)}s`,
                    '--asset-iteration-count': animation.loop ? 'infinite' : '1',
                    zIndex: layerZIndex(asset.layer) * 10,
                  }}
                >
                  <span className={`studio-asset-icon-wrap ${getAnimationClassName(animation.type)}`}>
                    <GameAssetIcon asset={asset} mode={gameMode} apiBaseUrl={apiBaseUrl} />
                  </span>
                </span>
              );
            })}
          </button>
        );
      }
    }
    return cells;
  };

  if (!gameMode) {
    return (
      <div className="game-studio-picker">
        <div className="game-studio-picker-inner">
          <span className="city-panel-kicker">Game Asset Studio</span>
          <h2>Choose Your Game Type</h2>
          <p>Pick a rendering style first. You can place built-in game pieces or your generated kchiro assets, then animate them.</p>
          <div className="game-mode-cards">
            <button type="button" className="game-mode-card two-d" onClick={() => handlePickMode('2d')}>
              <GameAssetIcon asset={{ type: 'player', category: 'Characters', color: '#38bdf8' }} mode="2d" apiBaseUrl={apiBaseUrl} />
              <strong>2D Game</strong>
              <span>Flat sprite-based, top-down or side-scrolling.</span>
            </button>
            <button type="button" className="game-mode-card three-d" onClick={() => handlePickMode('3d')}>
              <GameAssetIcon asset={{ type: 'grass', category: 'Terrain', color: '#4ade80' }} mode="3d" apiBaseUrl={apiBaseUrl} />
              <strong>3D Game</strong>
              <span>Isometric perspective with depth using CSS and SVG transforms.</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`game-studio game-studio-${gameMode} ${dayMode === 'Night' ? 'night' : 'day'}`}>
      <aside className="game-studio-sidebar">
        <div className="game-studio-title">
          <span className="city-panel-kicker">{gameMode === '3d' ? 'Isometric 3D' : 'Flat 2D'}</span>
          <h2>Game Asset Studio</h2>
          <button type="button" className="secondary-action-btn" onClick={handleSwitchMode}>
            Switch Mode
          </button>
        </div>

        <div className="studio-category-list">
          {studioCategories.map((category) => (
            <section className="studio-category" key={category.name}>
              <button
                type="button"
                className="studio-category-toggle"
                onClick={() => setOpenCategories((prev) => {
                  const isOpen = prev[category.name] !== false;
                  return { ...prev, [category.name]: !isOpen };
                })}
              >
                <span style={{ color: CATEGORY_COLORS[category.name] }}>{category.name}</span>
                <strong>{categoryCounts[category.name] || 0}</strong>
              </button>
              {openCategories[category.name] !== false && (
                <div className="studio-tool-grid">
                  {category.items.map((item) => (
                    <button
                      type="button"
                      key={item.type}
                      className={`studio-tool ${selectedTool === item.type ? 'active' : ''}`}
                      onClick={() => {
                        setSelectedTool(item.type);
                        setStudioMode('Place');
                        setStatus(`${item.label} selected.`);
                      }}
                    >
                      <GameAssetIcon asset={{ ...item, category: category.name }} mode={gameMode} compact apiBaseUrl={apiBaseUrl} />
                      <span>{item.label}</span>
                      <span className="studio-tooltip">
                        <GameAssetIcon asset={{ ...item, category: category.name }} mode={gameMode} compact apiBaseUrl={apiBaseUrl} />
                        {item.label}
                      </span>
                    </button>
                  ))}
                </div>
              )}
            </section>
          ))}
        </div>
      </aside>

      <main className="game-studio-main">
        <div className="game-studio-toolbar">
          <div className="studio-mode-buttons">
            {['Place', 'Select', 'Erase', 'Fill'].map((mode) => (
              <button
                key={mode}
                type="button"
                className={`preset-pill ${studioMode === mode ? 'active' : ''}`}
                onClick={() => setStudioMode(mode)}
              >
                {mode}
              </button>
            ))}
          </div>
          <div className="studio-toolbar-actions">
            <button type="button" className="secondary-action-btn" onClick={handleUndo} disabled={history.past.length === 0}>Undo</button>
            <button type="button" className="secondary-action-btn" onClick={handleRedo} disabled={history.future.length === 0}>Redo</button>
            <button type="button" className="secondary-action-btn" onClick={() => setGridlines((value) => !value)}>
              Gridlines {gridlines ? 'On' : 'Off'}
            </button>
            <button type="button" className="secondary-action-btn" onClick={handleRandomLevel}>Random Level</button>
            <button type="button" className="secondary-action-btn" onClick={() => importRef.current?.click()}>Import JSON</button>
            <button type="button" className="secondary-action-btn" onClick={handleExportJson}>Export JSON</button>
            <button type="button" className="secondary-action-btn" onClick={handleDownloadBlender}>Blender Builder</button>
            <button type="button" className="secondary-action-btn delete" onClick={handleClear}>Clear Canvas</button>
            <input ref={importRef} type="file" accept="application/json,.json" onChange={handleImportJson} hidden />
          </div>
        </div>

        <div className="studio-count-strip">
          {studioCategories.map((category) => (
            <span key={category.name} style={{ '--count-color': CATEGORY_COLORS[category.name] }}>
              {category.name}: {categoryCounts[category.name] || 0}
            </span>
          ))}
        </div>

        <div
          className="studio-canvas-viewport"
          onWheel={handleWheel}
          onMouseDown={handleCanvasMouseDown}
          onMouseMove={handleCanvasMouseMove}
          onMouseUp={() => setIsPanning(false)}
          onMouseLeave={() => setIsPanning(false)}
        >
          <div className="studio-canvas-hud">
            <span>{status}</span>
            <strong>Zoom {Math.round(zoom * 100)}%</strong>
          </div>
          <div
            className="studio-grid"
            style={{
              gridTemplateColumns: `repeat(${GRID_SIZE}, minmax(0, 1fr))`,
              transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
            }}
          >
            {renderGridCells()}
          </div>
          <div className="studio-fog" style={{ opacity: fogOpacity }} />
        </div>

        {contextMenu && (
          <div className="studio-context-menu" style={{ left: contextMenu.x, top: contextMenu.y }}>
            <button type="button" onClick={() => { setSelectedIds([contextMenu.assetId]); setContextMenu(null); }}>Edit</button>
            <button type="button" onClick={() => duplicateAsset(contextMenu.assetId)}>Duplicate</button>
            <button type="button" onClick={() => deleteAsset(contextMenu.assetId)}>Delete</button>
          </div>
        )}
      </main>

      <aside className="game-studio-properties">
        <div className="studio-panel-block">
          <h3>Lighting</h3>
          <label className="studio-property-row">
            <span>Day / Night</span>
            <select value={dayMode} onChange={(event) => setDayMode(event.target.value)}>
              <option>Day</option>
              <option>Night</option>
            </select>
          </label>
          <label className="studio-property-row">
            <span>Fog Opacity</span>
            <input type="range" min="0" max="0.85" step="0.05" value={fogOpacity} onChange={(event) => setFogOpacity(Number(event.target.value))} />
          </label>
        </div>

        <div className="studio-panel-block">
          <h3>Layer Manager</h3>
          {LAYERS.map((layer) => (
            <div className="studio-layer-row" key={layer}>
              <strong>{layer}</strong>
              <label><input type="checkbox" checked={layers[layer].visible} onChange={() => toggleLayer(layer, 'visible')} /> Visible</label>
              <label><input type="checkbox" checked={layers[layer].locked} onChange={() => toggleLayer(layer, 'locked')} /> Locked</label>
            </div>
          ))}
        </div>

        {selectedIds.length > 1 && (
          <div className="studio-panel-block">
            <h3>{selectedIds.length} assets selected</h3>
            <button type="button" className="secondary-action-btn delete" onClick={() => commitAssets(assets.filter((asset) => !selectedIds.includes(asset.id)), [])}>
              Delete Selected
            </button>
          </div>
        )}

        {selectedAsset ? (
          <>
            {(() => {
              const animation = {
                type: 'Idle',
                speed: 1,
                loop: true,
                enabled: Boolean(selectedAsset.animated),
                ...selectedAsset.animation,
              };
              return (
                <div className="studio-panel-block">
                  <h3>Animation Panel</h3>
                  <div
                    className={`studio-animation-preview ${animation.enabled ? 'is-animated' : ''}`}
                    style={{
                      '--asset-speed': `${1 / Math.max(0.25, animation.speed || 1)}s`,
                      '--asset-iteration-count': animation.loop ? 'infinite' : '1',
                    }}
                  >
                    <span className={`studio-asset-icon-wrap ${getAnimationClassName(animation.type)}`}>
                      <GameAssetIcon asset={selectedAsset} mode={gameMode} apiBaseUrl={apiBaseUrl} />
                    </span>
                  </div>
                  <label className="studio-inline-check">
                    <input
                      type="checkbox"
                      checked={animation.enabled}
                      onChange={(event) => updateSelectedAnimation('enabled', event.target.checked)}
                    />
                    Enable animation on this asset
                  </label>
                  <label className="studio-property-row">
                    <span>Animation Type</span>
                    <select value={animation.type} onChange={(event) => updateSelectedAnimation('type', event.target.value)}>
                      {ANIMATION_TYPES.map((type) => <option key={type}>{type}</option>)}
                    </select>
                  </label>
                  <label className="studio-property-row">
                    <span>Speed {Number(animation.speed || 1).toFixed(2)}x</span>
                    <input
                      type="range"
                      min="0.25"
                      max="3"
                      step="0.25"
                      value={animation.speed || 1}
                      onChange={(event) => updateSelectedAnimation('speed', Number(event.target.value))}
                    />
                  </label>
                  <label className="studio-inline-check">
                    <input type="checkbox" checked={animation.loop} onChange={(event) => updateSelectedAnimation('loop', event.target.checked)} />
                    Loop animation
                  </label>
                </div>
              );
            })()}

            <div className="studio-panel-block">
              <h3>Properties</h3>
              <label className="studio-property-row">
                <span>Name</span>
                <input value={selectedAsset.name} onChange={(event) => updateSelectedAsset('name', event.target.value)} />
              </label>
              <label className="studio-property-row">
                <span>Color / Tint</span>
                <input type="color" value={selectedAsset.color} onChange={(event) => updateSelectedAsset('color', event.target.value)} />
              </label>
              <label className="studio-property-row">
                <span>Size {selectedAsset.size}x</span>
                <input type="range" min="0.5" max="3" step="0.1" value={selectedAsset.size} onChange={(event) => updateSelectedAsset('size', Number(event.target.value))} />
              </label>
              <label className="studio-property-row">
                <span>Opacity {Math.round(selectedAsset.opacity * 100)}%</span>
                <input type="range" min="0.1" max="1" step="0.05" value={selectedAsset.opacity} onChange={(event) => updateSelectedAsset('opacity', Number(event.target.value))} />
              </label>
              <label className="studio-property-row">
                <span>Facing</span>
                <select value={selectedAsset.facing} onChange={(event) => updateSelectedAsset('facing', event.target.value)}>
                  {['Up', 'Down', 'Left', 'Right'].map((direction) => <option key={direction}>{direction}</option>)}
                </select>
              </label>
              <label className="studio-property-row">
                <span>Layer</span>
                <select value={selectedAsset.layer} onChange={(event) => updateSelectedAsset('layer', event.target.value)}>
                  {LAYERS.map((layer) => <option key={layer}>{layer}</option>)}
                </select>
              </label>
              <label className="studio-property-row">
                <span>Collision</span>
                <select value={selectedAsset.collision} onChange={(event) => updateSelectedAsset('collision', event.target.value)}>
                  {COLLISION_TYPES.map((type) => <option key={type}>{type}</option>)}
                </select>
              </label>
              <label className="studio-property-row">
                <span>Tags</span>
                <input value={selectedAsset.tags} onChange={(event) => updateSelectedAsset('tags', event.target.value)} placeholder="enemy, loot, spawn" />
              </label>
              <label className="studio-property-row notes">
                <span>Dev Notes</span>
                <textarea value={selectedAsset.notes} onChange={(event) => updateSelectedAsset('notes', event.target.value)} placeholder="Behavior, trigger, quest note..." />
              </label>
            </div>
          </>
        ) : (
          <div className="studio-panel-block muted">
            <h3>No Asset Selected</h3>
            <p>Click an asset on the canvas to edit animation, collision, layer, tags, and notes.</p>
          </div>
        )}
      </aside>
    </div>
  );
}

export default GameAssetStudio;
