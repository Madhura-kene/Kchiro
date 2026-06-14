export const ROOM_DIMENSIONS = {
  singleRoomSize: 3,
  roomWidth: 4.2,
  roomDepth: 3.6,
  ensuiteDepth: 2.2,
  hallwayDepth: 1.25,
  roomHeight: 2.35,
  wallThickness: 0.12,
};

export const DEFAULT_HOUSE_CONFIG = {
  bedrooms: 2,
  bathrooms: 2,
  kitchens: 1,
  livingRooms: 1,
  diningRooms: 1,
  attachBathroomToBedroom: true,
  ensuiteBathrooms: 1,
  roadLanes: 2,
  sidewalkWidth: 1.8,
  setbackWidth: 2.4,
  addCrosswalks: true,
};

export const DEFAULT_WALL_COLORS = {
  north: '#334155',
  south: '#475569',
  east: '#3b4257',
  west: '#516175',
  interior: '#64748b',
};

export const ROOM_TYPE_GROUPS = {
  bedroom: [
    'bed',
    'bunk_bed',
    'nightstand',
    'wardrobe',
    'closet',
    'dresser',
    'desk',
    'lamp',
    'rug',
    'clock',
    'painting',
    'picture_frame',
    'mirror',
  ],
  living: [
    'sofa',
    'couch',
    'armchair',
    'bench',
    'coffee_table',
    'tv_stand',
    'bookcase',
    'shelf',
    'lamp',
    'rug',
    'vase',
    'plant_pot',
    'clock',
    'painting',
    'picture_frame',
    'mirror',
  ],
  dining: [
    'table',
    'dining_table',
    'chair',
    'stool',
    'bench',
    'lamp',
    'clock',
    'painting',
    'picture_frame',
    'vase',
    'plant_pot',
  ],
  kitchen: [
    'fridge',
    'stove',
    'oven',
    'microwave',
    'sink',
    'countertop',
    'cupboard',
    'cabinet',
    'table',
    'dining_table',
    'chair',
    'stool',
    'clock',
    'plant_pot',
  ],
  bathroom: [
    'toilet',
    'bathtub',
    'shower',
    'sink',
    'mirror',
    'towel_rack',
    'cabinet',
    'clock',
  ],
};

const SINGLE_ROOM_LAYOUTS = new Set(['bedroom', 'living', 'dining', 'kitchen', 'bathroom']);
const COLOR_KEYS = ['north', 'south', 'east', 'west', 'interior'];

const ROOM_TYPE_PRIORITY = {
  living: 0,
  dining: 1,
  kitchen: 2,
  bedroom: 3,
  bathroom: 4,
  outdoor: 5,
  street: 6,
};

const PROMPT_ZONE_KEYWORDS = {
  bathroom: ['bath', 'bathroom', 'pedestal', 'shower', 'toilet', 'towel', 'vanity'],
  bedroom: ['bed', 'bedroom', 'blanket', 'closet', 'dresser', 'nightstand', 'pillow', 'wardrobe'],
  kitchen: ['bar stool', 'counter', 'cook', 'dining', 'fridge', 'island', 'kitchen', 'microwave', 'oven', 'sink cabinet', 'stove'],
  living: ['armchair', 'bookcase', 'coffee table', 'couch', 'living', 'lounge', 'sofa', 'tv'],
  dining: ['dining', 'dinner', 'banquette', 'buffet'],
};

const ROOM_TARGETS_BY_TYPE = {
  armchair: ['living'],
  bathtub: ['bathroom'],
  bed: ['bedroom'],
  bench: ['living', 'dining'],
  bookcase: ['living', 'bedroom', 'dining'],
  bunk_bed: ['bedroom'],
  chair: ['dining', 'kitchen'],
  closet: ['bedroom'],
  coffee_table: ['living'],
  countertop: ['kitchen'],
  couch: ['living'],
  cupboard: ['kitchen'],
  desk: ['bedroom'],
  dining_table: ['dining', 'kitchen'],
  dresser: ['bedroom'],
  fridge: ['kitchen'],
  microwave: ['kitchen'],
  nightstand: ['bedroom'],
  oven: ['kitchen'],
  shower: ['bathroom'],
  sofa: ['living'],
  stool: ['dining', 'kitchen'],
  stove: ['kitchen'],
  table: ['dining', 'kitchen'],
  toilet: ['bathroom'],
  towel_rack: ['bathroom'],
  tv_stand: ['living'],
  wardrobe: ['bedroom'],
};

const OUTDOOR_TARGETS_BY_TYPE = {
  street_lamp: ['outdoor'],
  traffic_light: ['street', 'outdoor'],
  road_sign: ['outdoor', 'street'],
  street_bench: ['outdoor'],
  mailbox: ['outdoor'],
  trash_can: ['outdoor'],
  bus_stop: ['outdoor'],
  phone_booth: ['outdoor'],
  car: ['street'],
  truck: ['street'],
  bike: ['outdoor', 'street'],
  motorcycle: ['street'],
  tractor: ['street'],
  battle_tank: ['street'],
  fence: ['outdoor'],
  gate: ['outdoor'],
  railing: ['outdoor'],
  bridge: ['outdoor'],
  oak_tree: ['outdoor'],
  pine_tree: ['outdoor'],
  birch_tree: ['outdoor'],
  palm_tree: ['outdoor'],
  dead_tree: ['outdoor'],
  sapling: ['outdoor'],
  grass: ['outdoor'],
  bush: ['outdoor'],
  shrub: ['outdoor'],
  fern: ['outdoor'],
  flower: ['outdoor'],
  moss: ['outdoor'],
  small_rock: ['outdoor'],
  boulder: ['outdoor'],
  rock_cluster: ['outdoor'],
  cliff_section: ['outdoor'],
  log: ['outdoor'],
  tree_stump: ['outdoor'],
  fallen_tree: ['outdoor'],
  mushroom: ['outdoor'],
  vine: ['outdoor'],
  root: ['outdoor'],
  pond: ['outdoor'],
  river_segment: ['outdoor'],
  waterfall: ['outdoor'],
  stream: ['outdoor'],
  terrain: ['outdoor'],
  hill: ['outdoor'],
  mountain: ['outdoor'],
  cliff: ['outdoor'],
  valley: ['outdoor'],
  cave: ['outdoor'],
  ground_tile: ['outdoor'],
  road_tile: ['street'],
  path_tile: ['outdoor'],
  river_tile: ['outdoor'],
  dungeon_tile: ['outdoor'],
};

const CITY_LANE_WIDTH = 2.6;
const CITY_PRESET_LIMITS = {
  street_lamp: 4,
  traffic_light: 4,
  road_sign: 4,
  street_bench: 4,
  mailbox: 2,
  trash_can: 4,
  bus_stop: 2,
  phone_booth: 2,
  car: 4,
  truck: 2,
  bike: 4,
  motorcycle: 2,
  tractor: 1,
  battle_tank: 1,
  fence: 2,
  gate: 1,
  railing: 2,
  oak_tree: 4,
  pine_tree: 4,
  birch_tree: 4,
  palm_tree: 4,
  dead_tree: 3,
  sapling: 6,
  grass: 6,
  bush: 6,
  shrub: 6,
  fern: 6,
  flower: 8,
  moss: 4,
  small_rock: 6,
  boulder: 3,
  rock_cluster: 4,
};

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
const toInt = (value, fallback) => {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) ? parsed : fallback;
};
const toFloat = (value, fallback) => {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : fallback;
};

const normalizeColor = (value, fallback) => {
  if (typeof value !== 'string') return fallback;
  const trimmed = value.trim();
  return /^#[0-9a-fA-F]{6}$/.test(trimmed) ? trimmed.toLowerCase() : fallback;
};

const sortByRoomPriority = (a, b) => {
  const priorityA = ROOM_TYPE_PRIORITY[a.type] ?? 99;
  const priorityB = ROOM_TYPE_PRIORITY[b.type] ?? 99;
  if (priorityA !== priorityB) {
    return priorityA - priorityB;
  }
  return a.id.localeCompare(b.id);
};

const buildCenteredPositions = (count, width) =>
  Array.from({ length: Math.max(count, 0) }, (_, index) =>
    -((count - 1) * width) / 2 + index * width
  );

const createRectSpace = ({
  id,
  type,
  label,
  centerX,
  centerZ,
  width,
  depth,
  row,
  attachedTo = null,
  materialKey = 'floor',
}) => ({
  id,
  type,
  label,
  row,
  attachedTo,
  materialKey,
  width,
  depth,
  center: [centerX, 0, centerZ],
  rect: {
    minX: centerX - width / 2,
    maxX: centerX + width / 2,
    minZ: centerZ - depth / 2,
    maxZ: centerZ + depth / 2,
  },
});

const createWallSegment = (id, orientation, length, centerX, centerZ, interior = false) => {
  const { roomHeight, wallThickness } = ROOM_DIMENSIONS;
  const horizontal = orientation === 'north' || orientation === 'south';
  return {
    id,
    orientation,
    interior,
    materialKey: interior ? 'interior' : orientation,
    size: horizontal
      ? [length, roomHeight, wallThickness]
      : [wallThickness, roomHeight, length],
    position: [centerX, roomHeight / 2, centerZ],
  };
};

const addRowWallSegments = (rooms, rowKind, segments) => {
  if (rooms.length === 0) return;

  const { wallThickness } = ROOM_DIMENSIONS;
  const sortedRooms = [...rooms].sort((a, b) => a.rect.minX - b.rect.minX);

  sortedRooms.forEach((room, index) => {
    if (index === 0) {
      segments.push(
        createWallSegment(
          `${room.id}_west_outer`,
          'west',
          room.depth,
          room.rect.minX - wallThickness / 2,
          room.center[2]
        )
      );
    } else {
      segments.push(
        createWallSegment(
          `${room.id}_west_partition`,
          'west',
          room.depth,
          room.rect.minX,
          room.center[2],
          true
        )
      );
    }

    if (index === sortedRooms.length - 1) {
      segments.push(
        createWallSegment(
          `${room.id}_east_outer`,
          'east',
          room.depth,
          room.rect.maxX + wallThickness / 2,
          room.center[2]
        )
      );
    }

    if (rowKind === 'public') {
      segments.push(
        createWallSegment(
          `${room.id}_north_outer`,
          'north',
          room.width,
          room.center[0],
          room.rect.minZ - wallThickness / 2
        )
      );
    }

    if (rowKind === 'private' && !room.hasEnsuite) {
      segments.push(
        createWallSegment(
          `${room.id}_south_outer`,
          'south',
          room.width,
          room.center[0],
          room.rect.maxZ + wallThickness / 2
        )
      );
    }

    if (rowKind === 'ensuite') {
      segments.push(
        createWallSegment(
          `${room.id}_south_outer`,
          'south',
          room.width,
          room.center[0],
          room.rect.maxZ + wallThickness / 2
        )
      );
    }
  });
};

const buildSingleRoomWalls = (room) => {
  const { wallThickness } = ROOM_DIMENSIONS;
  return [
    createWallSegment(
      `${room.id}_north_outer`,
      'north',
      room.width,
      room.center[0],
      room.rect.minZ - wallThickness / 2
    ),
    createWallSegment(
      `${room.id}_west_outer`,
      'west',
      room.depth,
      room.rect.minX - wallThickness / 2,
      room.center[2]
    ),
    createWallSegment(
      `${room.id}_east_outer`,
      'east',
      room.depth,
      room.rect.maxX + wallThickness / 2,
      room.center[2]
    ),
  ];
};

const buildHouseWalls = (publicRooms, privateRooms, ensuiteRooms) => {
  const segments = [];
  addRowWallSegments(publicRooms, 'public', segments);
  addRowWallSegments(privateRooms, 'private', segments);
  addRowWallSegments(ensuiteRooms, 'ensuite', segments);
  return segments;
};

const inferPromptRoomType = (prompt = '') => {
  const normalized = String(prompt).toLowerCase();
  return Object.entries(PROMPT_ZONE_KEYWORDS).find(([, keywords]) =>
    keywords.some((keyword) => normalized.includes(keyword))
  )?.[0] || null;
};

export const normalizeWallColors = (wallColors = {}) =>
  COLOR_KEYS.reduce(
    (colors, key) => ({
      ...colors,
      [key]: normalizeColor(wallColors[key], DEFAULT_WALL_COLORS[key]),
    }),
    {}
  );

export const normalizeHouseConfig = (houseConfig = {}) => {
  const bedrooms = clamp(toInt(houseConfig.bedrooms, DEFAULT_HOUSE_CONFIG.bedrooms), 1, 6);
  const bathrooms = clamp(toInt(houseConfig.bathrooms, DEFAULT_HOUSE_CONFIG.bathrooms), 1, 6);
  const kitchens = clamp(toInt(houseConfig.kitchens, DEFAULT_HOUSE_CONFIG.kitchens), 1, 3);
  const livingRooms = clamp(toInt(houseConfig.livingRooms, DEFAULT_HOUSE_CONFIG.livingRooms), 1, 3);
  const diningRooms = clamp(toInt(houseConfig.diningRooms, DEFAULT_HOUSE_CONFIG.diningRooms), 0, 3);
  const roadLanes = clamp(toInt(houseConfig.roadLanes, DEFAULT_HOUSE_CONFIG.roadLanes), 1, 4);
  const sidewalkWidth = clamp(
    toFloat(houseConfig.sidewalkWidth, DEFAULT_HOUSE_CONFIG.sidewalkWidth),
    0.8,
    6
  );
  const setbackWidth = clamp(
    toFloat(houseConfig.setbackWidth, DEFAULT_HOUSE_CONFIG.setbackWidth),
    0.8,
    8
  );
  const attachBathroomToBedroom = houseConfig.attachBathroomToBedroom !== false;
  const addCrosswalks = houseConfig.addCrosswalks !== false;
  const requestedEnsuites = attachBathroomToBedroom
    ? clamp(
        toInt(houseConfig.ensuiteBathrooms, DEFAULT_HOUSE_CONFIG.ensuiteBathrooms),
        0,
        Math.min(bedrooms, bathrooms)
      )
    : 0;

  return {
    bedrooms,
    bathrooms,
    kitchens,
    livingRooms,
    diningRooms,
    attachBathroomToBedroom,
    ensuiteBathrooms: requestedEnsuites,
    roadLanes,
    sidewalkWidth: Number(sidewalkWidth.toFixed(2)),
    setbackWidth: Number(setbackWidth.toFixed(2)),
    addCrosswalks,
  };
};

export const getSingleRoomPlacement = (type, index) => {
  const offset = index * 0.25;
  switch (type) {
    case 'rug':
      return { pos: [0, 0.01 + index * 0.005, 0], rot: [0, 0, 0], scale: 1.2 };
    case 'coffee_table':
      return { pos: [0, 0, 0.1 + offset], rot: [0, 0, 0], scale: 1.0 };
    case 'table':
    case 'dining_table':
      return { pos: [0, 0, 0.3 + offset], rot: [0, 0, 0], scale: 1.0 };
    case 'desk':
      return { pos: [-0.6, 0, -1.0 + offset], rot: [0, 0, 0], scale: 1.0 };
    case 'chair':
    case 'stool':
      if (index === 0) return { pos: [-0.6, 0, -0.6], rot: [0, 0, 0], scale: 1.0 };
      if (index === 1) return { pos: [-0.5, 0, 0.3], rot: [0, Math.PI / 2, 0], scale: 1.0 };
      if (index === 2) return { pos: [0.5, 0, 0.3], rot: [0, -Math.PI / 2, 0], scale: 1.0 };
      return { pos: [0, 0, 0.8 + offset], rot: [0, Math.PI, 0], scale: 1.0 };
    case 'sofa':
    case 'couch':
      return { pos: [-1.2, 0, 0.4 + offset], rot: [0, Math.PI / 2, 0], scale: 1.0 };
    case 'armchair':
      return { pos: [1.1, 0, 0.8 + offset], rot: [0, -Math.PI / 4, 0], scale: 1.0 };
    case 'bench':
      return { pos: [0.7, 0, 1.0 + offset], rot: [0, Math.PI, 0], scale: 1.0 };
    case 'bed':
    case 'bunk_bed':
      return { pos: [0.4, 0, -1.1 + offset], rot: [0, Math.PI, 0], scale: 1.0 };
    case 'nightstand':
      return { pos: [-0.4 + offset, 0, -1.3], rot: [0, Math.PI, 0], scale: 1.0 };
    case 'wardrobe':
    case 'closet':
    case 'dresser':
    case 'cabinet':
    case 'cupboard':
      return { pos: [1.2, 0, -0.6 + offset], rot: [0, -Math.PI / 2, 0], scale: 1.0 };
    case 'bookcase':
    case 'shelf':
      return { pos: [1.2, 0, 0.3 + offset], rot: [0, -Math.PI / 2, 0], scale: 1.0 };
    case 'tv_stand':
      return { pos: [-1.2, 0, -0.4 + offset], rot: [0, Math.PI / 2, 0], scale: 1.0 };
    case 'lamp':
      return { pos: [1.2, 0, -1.2 + offset], rot: [0, 0, 0], scale: 1.0 };
    case 'clock':
      return { pos: [0.8 - offset * 0.5, 1.4, -1.46], rot: [0, 0, 0], scale: 1.0 };
    case 'painting':
    case 'picture_frame':
      return { pos: [-0.6 + offset, 1.3, -1.46], rot: [0, 0, 0], scale: 1.0 };
    case 'mirror':
      return { pos: [-1.46, 1.3, 0 + offset], rot: [0, Math.PI / 2, 0], scale: 1.0 };
    case 'vase':
      return { pos: [0, 0.75, 0.3 + offset], rot: [0, 0, 0], scale: 0.6 };
    case 'plant_pot':
      return { pos: [-1.1 + offset * 0.3, 0, 1.2 + offset], rot: [0, 0, 0], scale: 0.9 };
    case 'fridge':
      return { pos: [-1.2, 0, -1.1 + offset], rot: [0, Math.PI, 0], scale: 1.0 };
    case 'stove':
    case 'oven':
      return { pos: [-0.6, 0, -1.25 + offset], rot: [0, Math.PI, 0], scale: 1.0 };
    case 'sink':
    case 'countertop':
      return { pos: [0.1 + offset, 0, -1.25], rot: [0, Math.PI, 0], scale: 1.0 };
    case 'microwave':
      return { pos: [0.45 + offset * 0.2, 0.95, -1.18], rot: [0, Math.PI, 0], scale: 0.7 };
    case 'toilet':
      return { pos: [1.2, 0, -1.1 + offset], rot: [0, Math.PI, 0], scale: 1.0 };
    case 'bathtub':
      return { pos: [0.5, 0, -1.25 + offset], rot: [0, Math.PI, 0], scale: 1.0 };
    case 'shower':
      return { pos: [-1.2, 0, -1.1 + offset], rot: [0, Math.PI, 0], scale: 1.0 };
    case 'towel_rack':
      return { pos: [1.46, 1.2, 0.3 + offset], rot: [0, -Math.PI / 2, 0], scale: 1.0 };
    default:
      return { pos: [-1.0 + index * 0.4, 0, 1.0], rot: [0, 0, 0], scale: 1.0 };
  }
};

const scalePlacementToRoom = (placement, room) => {
  const xScale = room.width / ROOM_DIMENSIONS.singleRoomSize;
  const zScale = room.depth / ROOM_DIMENSIONS.singleRoomSize;
  return {
    pos: [placement.pos[0] * xScale, placement.pos[1], placement.pos[2] * zScale],
    rot: placement.rot,
    scale: placement.scale,
  };
};

const buildHousePresetLimits = (houseConfig) => {
  const normalized = normalizeHouseConfig(houseConfig);
  return {
    armchair: normalized.livingRooms * 2,
    bathtub: normalized.bathrooms,
    bed: normalized.bedrooms,
    bench: normalized.livingRooms + Math.max(normalized.diningRooms, 1) - 1,
    bookcase: normalized.livingRooms + normalized.bedrooms,
    bunk_bed: normalized.bedrooms,
    cabinet: normalized.bathrooms + normalized.kitchens,
    chair: Math.max(normalized.diningRooms, 1) * 4,
    clock: normalized.livingRooms + normalized.bedrooms + normalized.kitchens,
    closet: normalized.bedrooms,
    couch: normalized.livingRooms,
    coffee_table: normalized.livingRooms,
    countertop: normalized.kitchens * 2,
    cupboard: normalized.kitchens,
    desk: normalized.bedrooms,
    dining_table: Math.max(normalized.diningRooms, 1),
    dresser: normalized.bedrooms,
    fridge: normalized.kitchens,
    lamp: normalized.livingRooms + normalized.bedrooms + Math.max(normalized.diningRooms, 1),
    microwave: normalized.kitchens,
    mirror: normalized.bathrooms + normalized.bedrooms,
    nightstand: normalized.bedrooms * 2,
    oven: normalized.kitchens,
    painting: normalized.livingRooms + normalized.bedrooms + Math.max(normalized.diningRooms, 1),
    picture_frame: normalized.livingRooms + normalized.bedrooms + Math.max(normalized.diningRooms, 1),
    plant_pot: normalized.livingRooms + normalized.kitchens + Math.max(normalized.diningRooms - 1, 0),
    rug: normalized.livingRooms + normalized.bedrooms,
    shelf: normalized.livingRooms + normalized.bedrooms + normalized.kitchens,
    shower: normalized.bathrooms,
    sink: normalized.kitchens + normalized.bathrooms,
    sofa: normalized.livingRooms,
    stool: Math.max(normalized.kitchens * 2, normalized.diningRooms * 2),
    stove: normalized.kitchens,
    table: Math.max(normalized.diningRooms, 1),
    toilet: normalized.bathrooms,
    towel_rack: normalized.bathrooms,
    tv_stand: normalized.livingRooms,
    vase: normalized.livingRooms + normalized.diningRooms,
    wardrobe: normalized.bedrooms,
  };
};

const buildCityPresetLimits = (houseConfig) => ({
  ...buildHousePresetLimits(houseConfig),
  ...CITY_PRESET_LIMITS,
});

const getRoomTypeCandidates = (asset, houseConfig) => {
  const type = asset?.asset_type;
  const promptType = inferPromptRoomType(asset?.prompt);

  if (OUTDOOR_TARGETS_BY_TYPE[type]) {
    return OUTDOOR_TARGETS_BY_TYPE[type];
  }

  if (type === 'sink') {
    return promptType === 'bathroom' ? ['bathroom', 'kitchen'] : ['kitchen', 'bathroom'];
  }

  if (type === 'cabinet') {
    if (promptType === 'bathroom') return ['bathroom', 'kitchen', 'dining'];
    if (promptType === 'kitchen') return ['kitchen', 'bathroom', 'dining'];
    return ['kitchen', 'bathroom', 'dining'];
  }

  if (type === 'mirror') {
    if (promptType === 'bathroom') return ['bathroom', 'bedroom', 'living'];
    return ['bedroom', 'bathroom', 'living'];
  }

  if (type === 'painting' || type === 'picture_frame') {
    return ['living', 'bedroom', houseConfig.diningRooms > 0 ? 'dining' : 'kitchen'];
  }

  if (type === 'clock') {
    return ['living', houseConfig.diningRooms > 0 ? 'dining' : 'kitchen', 'bedroom', 'bathroom'];
  }

  if (type === 'rug') {
    return ['living', 'bedroom', houseConfig.diningRooms > 0 ? 'dining' : 'kitchen'];
  }

  if (type === 'lamp') {
    return ['living', 'bedroom', houseConfig.diningRooms > 0 ? 'dining' : 'kitchen'];
  }

  if (type === 'vase' || type === 'plant_pot') {
    return ['living', houseConfig.diningRooms > 0 ? 'dining' : 'kitchen', 'bedroom'];
  }

  if (type === 'shelf' || type === 'bookcase') {
    return ['living', 'bedroom', 'kitchen'];
  }

  if (ROOM_TARGETS_BY_TYPE[type]) {
    return ROOM_TARGETS_BY_TYPE[type];
  }

  if (promptType && SINGLE_ROOM_LAYOUTS.has(promptType)) {
    return [promptType];
  }

  return ['living'];
};

const chooseRoomForAsset = (asset, plan, houseConfig, roomLoads) => {
  const roomsByType = plan.rooms.reduce((acc, room) => {
    if (!room.assignable) return acc;
    acc[room.type] = acc[room.type] || [];
    acc[room.type].push(room);
    return acc;
  }, {});

  const candidateTypes = getRoomTypeCandidates(asset, houseConfig);
  const candidateRooms = candidateTypes.flatMap((type) => roomsByType[type] || []);

  if (candidateRooms.length === 0) {
    const fallbackRooms = [...plan.rooms].filter((room) => room.assignable).sort(sortByRoomPriority);
    return fallbackRooms[0] || null;
  }

  return [...candidateRooms].sort((roomA, roomB) => {
    const loadA = roomLoads[roomA.id] || 0;
    const loadB = roomLoads[roomB.id] || 0;
    if (loadA !== loadB) {
      return loadA - loadB;
    }
    return sortByRoomPriority(roomA, roomB);
  })[0];
};

export const buildHousePlan = (houseConfig = DEFAULT_HOUSE_CONFIG) => {
  const normalized = normalizeHouseConfig(houseConfig);
  const {
    roomWidth,
    roomDepth,
    ensuiteDepth,
    hallwayDepth,
    roomHeight,
    wallThickness,
  } = ROOM_DIMENSIONS;

  const publicDefinitions = [
    ...Array.from({ length: normalized.livingRooms }, (_, index) => ({
      id: `living_${index + 1}`,
      type: 'living',
      label: normalized.livingRooms > 1 ? `Living Room ${index + 1}` : 'Living Room',
    })),
    ...Array.from({ length: normalized.diningRooms }, (_, index) => ({
      id: `dining_${index + 1}`,
      type: 'dining',
      label: normalized.diningRooms > 1 ? `Dining Room ${index + 1}` : 'Dining Room',
    })),
    ...Array.from({ length: normalized.kitchens }, (_, index) => ({
      id: `kitchen_${index + 1}`,
      type: 'kitchen',
      label: normalized.kitchens > 1 ? `Kitchen ${index + 1}` : 'Kitchen',
    })),
  ];

  const sharedBathrooms = Math.max(normalized.bathrooms - normalized.ensuiteBathrooms, 0);
  const privateDefinitions = [
    ...Array.from({ length: normalized.bedrooms }, (_, index) => ({
      id: `bedroom_${index + 1}`,
      type: 'bedroom',
      label: normalized.bedrooms > 1 ? `Bedroom ${index + 1}` : 'Bedroom',
      bedroomIndex: index,
    })),
    ...Array.from({ length: sharedBathrooms }, (_, index) => ({
      id: `bathroom_shared_${index + 1}`,
      type: 'bathroom',
      label: sharedBathrooms > 1 ? `Bathroom ${index + 1}` : 'Bathroom',
    })),
  ];

  const publicRowWidth = publicDefinitions.length * roomWidth;
  const privateRowWidth = privateDefinitions.length * roomWidth;
  const houseWidth = Math.max(publicRowWidth, privateRowWidth, roomWidth);

  const publicCenterZ = -(hallwayDepth / 2 + roomDepth / 2);
  const privateCenterZ = hallwayDepth / 2 + roomDepth / 2;
  const ensuiteCenterZ = privateCenterZ + roomDepth / 2 + ensuiteDepth / 2;

  const publicPositions = buildCenteredPositions(publicDefinitions.length, roomWidth);
  const privatePositions = buildCenteredPositions(privateDefinitions.length, roomWidth);

  const publicRooms = publicDefinitions.map((definition, index) =>
    createRectSpace({
      ...definition,
      centerX: publicPositions[index],
      centerZ: publicCenterZ,
      width: roomWidth,
      depth: roomDepth,
      row: 'public',
    })
  );

  const privateRooms = privateDefinitions.map((definition, index) =>
    createRectSpace({
      ...definition,
      centerX: privatePositions[index],
      centerZ: privateCenterZ,
      width: roomWidth,
      depth: roomDepth,
      row: 'private',
    })
  );

  const bedroomRooms = privateRooms.filter((room) => room.type === 'bedroom');
  const ensuiteRooms = bedroomRooms.slice(0, normalized.ensuiteBathrooms).map((bedroom, index) => {
    bedroom.hasEnsuite = true;
    return createRectSpace({
      id: `bathroom_ensuite_${index + 1}`,
      type: 'bathroom',
      label: `Ensuite ${index + 1}`,
      centerX: bedroom.center[0],
      centerZ: ensuiteCenterZ,
      width: roomWidth,
      depth: ensuiteDepth,
      row: 'ensuite',
      attachedTo: bedroom.id,
    });
  });

  const corridor = createRectSpace({
    id: 'hallway_main',
    type: 'hallway',
    label: 'Hallway',
    centerX: 0,
    centerZ: 0,
    width: houseWidth,
    depth: hallwayDepth,
    row: 'corridor',
  });
  corridor.assignable = false;

  privateRooms.forEach((room) => {
    room.assignable = true;
  });
  publicRooms.forEach((room) => {
    room.assignable = true;
  });
  ensuiteRooms.forEach((room) => {
    room.assignable = true;
  });

  const allSpaces = [...publicRooms, ...privateRooms, ...ensuiteRooms, corridor];
  const minX = Math.min(...allSpaces.map((space) => space.rect.minX)) - wallThickness;
  const maxX = Math.max(...allSpaces.map((space) => space.rect.maxX)) + wallThickness;
  const minZ = Math.min(...allSpaces.map((space) => space.rect.minZ)) - wallThickness;
  const maxZ = Math.max(...allSpaces.map((space) => space.rect.maxZ)) + wallThickness;

  return {
    mode: 'house',
    houseConfig: normalized,
    rooms: [...publicRooms, ...privateRooms, ...ensuiteRooms],
    floors: [...publicRooms, ...privateRooms, ...ensuiteRooms, corridor],
    corridor,
    walls: buildHouseWalls(publicRooms, privateRooms, ensuiteRooms),
    bounds: {
      minX,
      maxX,
      minZ,
      maxZ,
      width: maxX - minX,
      depth: maxZ - minZ,
      centerX: (minX + maxX) / 2,
      centerZ: (minZ + maxZ) / 2,
    },
    dimensions: {
      roomHeight,
      wallThickness,
    },
  };
};

export const buildCityPlan = (houseConfig = DEFAULT_HOUSE_CONFIG) => {
  const normalized = normalizeHouseConfig(houseConfig);
  const basePlan = buildHousePlan(normalized);
  const { wallThickness } = ROOM_DIMENSIONS;

  const lotMinX = basePlan.bounds.minX - normalized.setbackWidth;
  const lotMaxX = basePlan.bounds.maxX + normalized.setbackWidth;
  const lotMinZ = basePlan.bounds.minZ - normalized.setbackWidth;
  const lotMaxZ = basePlan.bounds.maxZ + normalized.setbackWidth;

  const sidewalkMinX = lotMinX - normalized.sidewalkWidth;
  const sidewalkMaxX = lotMaxX + normalized.sidewalkWidth;
  const sidewalkMinZ = lotMinZ - normalized.sidewalkWidth;
  const sidewalkMaxZ = lotMaxZ + normalized.sidewalkWidth;

  const roadWidth = normalized.roadLanes * CITY_LANE_WIDTH;
  const roadMinX = sidewalkMinX - roadWidth;
  const roadMaxX = sidewalkMaxX + roadWidth;
  const roadMinZ = sidewalkMinZ - roadWidth;
  const roadMaxZ = sidewalkMaxZ + roadWidth;

  const centerX = (roadMinX + roadMaxX) / 2;
  const centerZ = (roadMinZ + roadMaxZ) / 2;
  const lotWidth = lotMaxX - lotMinX;
  const lotDepth = lotMaxZ - lotMinZ;

  const outdoorRooms = [
    createRectSpace({
      id: 'city_outdoor_north',
      type: 'outdoor',
      label: 'Front Court',
      centerX: basePlan.bounds.centerX,
      centerZ: (lotMinZ + basePlan.bounds.minZ) / 2,
      width: basePlan.bounds.width,
      depth: normalized.setbackWidth,
      row: 'outdoor',
      materialKey: 'lot',
    }),
    createRectSpace({
      id: 'city_outdoor_south',
      type: 'outdoor',
      label: 'Back Court',
      centerX: basePlan.bounds.centerX,
      centerZ: (basePlan.bounds.maxZ + lotMaxZ) / 2,
      width: basePlan.bounds.width,
      depth: normalized.setbackWidth,
      row: 'outdoor',
      materialKey: 'lot',
    }),
    createRectSpace({
      id: 'city_outdoor_west',
      type: 'outdoor',
      label: 'West Court',
      centerX: (lotMinX + basePlan.bounds.minX) / 2,
      centerZ: basePlan.bounds.centerZ,
      width: normalized.setbackWidth,
      depth: basePlan.bounds.depth,
      row: 'outdoor',
      materialKey: 'lot',
    }),
    createRectSpace({
      id: 'city_outdoor_east',
      type: 'outdoor',
      label: 'East Court',
      centerX: (basePlan.bounds.maxX + lotMaxX) / 2,
      centerZ: basePlan.bounds.centerZ,
      width: normalized.setbackWidth,
      depth: basePlan.bounds.depth,
      row: 'outdoor',
      materialKey: 'lot',
    }),
  ];
  outdoorRooms.forEach((room) => {
    room.assignable = true;
  });

  const streetRooms = [
    createRectSpace({
      id: 'city_street_north',
      type: 'street',
      label: 'North Street',
      centerX,
      centerZ: (roadMinZ + sidewalkMinZ) / 2,
      width: roadMaxX - roadMinX,
      depth: roadWidth,
      row: 'street',
      materialKey: 'road',
    }),
    createRectSpace({
      id: 'city_street_south',
      type: 'street',
      label: 'South Street',
      centerX,
      centerZ: (sidewalkMaxZ + roadMaxZ) / 2,
      width: roadMaxX - roadMinX,
      depth: roadWidth,
      row: 'street',
      materialKey: 'road',
    }),
    createRectSpace({
      id: 'city_street_west',
      type: 'street',
      label: 'West Street',
      centerX: (roadMinX + sidewalkMinX) / 2,
      centerZ,
      width: roadWidth,
      depth: sidewalkMaxZ - sidewalkMinZ,
      row: 'street',
      materialKey: 'road',
    }),
    createRectSpace({
      id: 'city_street_east',
      type: 'street',
      label: 'East Street',
      centerX: (sidewalkMaxX + roadMaxX) / 2,
      centerZ,
      width: roadWidth,
      depth: sidewalkMaxZ - sidewalkMinZ,
      row: 'street',
      materialKey: 'road',
    }),
  ];
  streetRooms.forEach((room) => {
    room.assignable = true;
  });

  const floorSpaces = [
    ...basePlan.floors.map((space) => ({ ...space, materialKey: space.materialKey || 'floor' })),
    createRectSpace({
      id: 'city_lot',
      type: 'lot',
      label: 'Lot',
      centerX: (lotMinX + lotMaxX) / 2,
      centerZ: (lotMinZ + lotMaxZ) / 2,
      width: lotWidth,
      depth: lotDepth,
      row: 'lot',
      materialKey: 'lot',
    }),
    createRectSpace({
      id: 'city_sidewalk_north',
      type: 'sidewalk',
      label: 'North Sidewalk',
      centerX,
      centerZ: (sidewalkMinZ + lotMinZ) / 2,
      width: sidewalkMaxX - sidewalkMinX,
      depth: normalized.sidewalkWidth,
      row: 'sidewalk',
      materialKey: 'sidewalk',
    }),
    createRectSpace({
      id: 'city_sidewalk_south',
      type: 'sidewalk',
      label: 'South Sidewalk',
      centerX,
      centerZ: (lotMaxZ + sidewalkMaxZ) / 2,
      width: sidewalkMaxX - sidewalkMinX,
      depth: normalized.sidewalkWidth,
      row: 'sidewalk',
      materialKey: 'sidewalk',
    }),
    createRectSpace({
      id: 'city_sidewalk_west',
      type: 'sidewalk',
      label: 'West Sidewalk',
      centerX: (sidewalkMinX + lotMinX) / 2,
      centerZ,
      width: normalized.sidewalkWidth,
      depth: lotDepth,
      row: 'sidewalk',
      materialKey: 'sidewalk',
    }),
    createRectSpace({
      id: 'city_sidewalk_east',
      type: 'sidewalk',
      label: 'East Sidewalk',
      centerX: (lotMaxX + sidewalkMaxX) / 2,
      centerZ,
      width: normalized.sidewalkWidth,
      depth: lotDepth,
      row: 'sidewalk',
      materialKey: 'sidewalk',
    }),
    ...streetRooms,
  ];

  if (normalized.addCrosswalks) {
    floorSpaces.push(
      createRectSpace({
        id: 'city_crosswalk_north',
        type: 'crosswalk',
        label: 'North Crosswalk',
        centerX,
        centerZ: (roadMinZ + sidewalkMinZ) / 2,
        width: Math.max(3, Math.min(basePlan.bounds.width * 0.72, sidewalkMaxX - sidewalkMinX - 0.4)),
        depth: Math.max(1.2, roadWidth * 0.72),
        row: 'crosswalk',
        materialKey: 'crosswalk',
      }),
      createRectSpace({
        id: 'city_crosswalk_south',
        type: 'crosswalk',
        label: 'South Crosswalk',
        centerX,
        centerZ: (sidewalkMaxZ + roadMaxZ) / 2,
        width: Math.max(3, Math.min(basePlan.bounds.width * 0.72, sidewalkMaxX - sidewalkMinX - 0.4)),
        depth: Math.max(1.2, roadWidth * 0.72),
        row: 'crosswalk',
        materialKey: 'crosswalk',
      }),
      createRectSpace({
        id: 'city_crosswalk_west',
        type: 'crosswalk',
        label: 'West Crosswalk',
        centerX: (roadMinX + sidewalkMinX) / 2,
        centerZ,
        width: Math.max(1.2, roadWidth * 0.72),
        depth: Math.max(3, Math.min(basePlan.bounds.depth * 0.72, sidewalkMaxZ - sidewalkMinZ - 0.4)),
        row: 'crosswalk',
        materialKey: 'crosswalk',
      }),
      createRectSpace({
        id: 'city_crosswalk_east',
        type: 'crosswalk',
        label: 'East Crosswalk',
        centerX: (sidewalkMaxX + roadMaxX) / 2,
        centerZ,
        width: Math.max(1.2, roadWidth * 0.72),
        depth: Math.max(3, Math.min(basePlan.bounds.depth * 0.72, sidewalkMaxZ - sidewalkMinZ - 0.4)),
        row: 'crosswalk',
        materialKey: 'crosswalk',
      })
    );
  }

  return {
    ...basePlan,
    mode: 'city',
    houseConfig: normalized,
    rooms: [...basePlan.rooms, ...outdoorRooms, ...streetRooms],
    floors: floorSpaces,
    bounds: {
      minX: roadMinX - wallThickness,
      maxX: roadMaxX + wallThickness,
      minZ: roadMinZ - wallThickness,
      maxZ: roadMaxZ + wallThickness,
      width: roadMaxX - roadMinX + wallThickness * 2,
      depth: roadMaxZ - roadMinZ + wallThickness * 2,
      centerX,
      centerZ,
    },
  };
};

export const buildSingleRoomPlan = (layoutMode = 'living') => {
  const roomType = SINGLE_ROOM_LAYOUTS.has(layoutMode) ? layoutMode : 'living';
  const size = ROOM_DIMENSIONS.singleRoomSize;
  const room = createRectSpace({
    id: `${roomType}_single`,
    type: roomType,
    label: 'Room',
    centerX: 0,
    centerZ: 0,
    width: size,
    depth: size,
    row: 'single',
  });
  room.assignable = true;

  return {
    mode: roomType,
    houseConfig: normalizeHouseConfig(DEFAULT_HOUSE_CONFIG),
    rooms: [room],
    floors: [room],
    corridor: null,
    walls: buildSingleRoomWalls(room),
    bounds: {
      minX: room.rect.minX - ROOM_DIMENSIONS.wallThickness,
      maxX: room.rect.maxX + ROOM_DIMENSIONS.wallThickness,
      minZ: room.rect.minZ - ROOM_DIMENSIONS.wallThickness,
      maxZ: room.rect.maxZ,
      width: size + ROOM_DIMENSIONS.wallThickness * 2,
      depth: size + ROOM_DIMENSIONS.wallThickness,
      centerX: 0,
      centerZ: 0,
    },
    dimensions: {
      roomHeight: ROOM_DIMENSIONS.roomHeight,
      wallThickness: ROOM_DIMENSIONS.wallThickness,
    },
  };
};

export const buildLayoutPlan = (layoutMode, houseConfig = DEFAULT_HOUSE_CONFIG) =>
  layoutMode === 'city'
    ? buildCityPlan(houseConfig)
    : layoutMode === 'house'
      ? buildHousePlan(houseConfig)
      : buildSingleRoomPlan(layoutMode);

export const getLayoutPresetAssetIds = (
  layoutName,
  completedAssets,
  houseConfig = DEFAULT_HOUSE_CONFIG
) => {
  if (layoutName === 'clear') {
    return [];
  }

  if (layoutName === 'all') {
    return completedAssets.map((asset) => asset.id);
  }

  const limits =
    layoutName === 'city'
      ? buildCityPresetLimits(houseConfig)
      : layoutName === 'house'
        ? buildHousePresetLimits(houseConfig)
      : Object.entries(ROOM_TYPE_GROUPS).reduce((acc, [roomType, assetTypes]) => {
          if (roomType !== layoutName) {
            return acc;
          }
          assetTypes.forEach((type) => {
            if (type === 'lamp') acc[type] = 2;
            else if (type === 'nightstand') acc[type] = 2;
            else if (type === 'chair' || type === 'stool') acc[type] = 4;
            else if (type === 'painting' || type === 'picture_frame') acc[type] = 2;
            else acc[type] = 1;
          });
          return acc;
        }, {});

  const counts = {};
  return completedAssets.reduce((selectedIds, asset) => {
    const limit = limits[asset.asset_type];
    if (!limit) {
      return selectedIds;
    }

    const currentCount = counts[asset.asset_type] || 0;
    if (currentCount >= limit) {
      return selectedIds;
    }

    counts[asset.asset_type] = currentCount + 1;
    selectedIds.push(asset.id);
    return selectedIds;
  }, []);
};

export const buildLayoutPlacements = (
  assetList,
  layoutMode,
  houseConfig = DEFAULT_HOUSE_CONFIG
) => {
  const plan = buildLayoutPlan(layoutMode, houseConfig);
  const placements = {};

  if (plan.mode !== 'house' && plan.mode !== 'city') {
    const room = plan.rooms[0];
    const typeCounts = {};

    assetList.forEach((asset) => {
      const typeIndex = typeCounts[asset.asset_type] || 0;
      typeCounts[asset.asset_type] = typeIndex + 1;

      const localPlacement = scalePlacementToRoom(
        getSingleRoomPlacement(asset.asset_type, typeIndex),
        room
      );

      placements[asset.id] = {
        roomId: room.id,
        roomType: room.type,
        pos: [
          localPlacement.pos[0] + room.center[0],
          localPlacement.pos[1],
          localPlacement.pos[2] + room.center[2],
        ],
        rot: localPlacement.rot,
        scale: localPlacement.scale,
      };
    });

    return placements;
  }

  const normalized = normalizeHouseConfig(houseConfig);
  const roomLoads = {};
  const roomTypeCounts = {};

  assetList.forEach((asset) => {
    const room = chooseRoomForAsset(asset, plan, normalized, roomLoads);
    if (!room) {
      return;
    }

    roomLoads[room.id] = (roomLoads[room.id] || 0) + 1;

    const roomTypeKey = `${room.id}:${asset.asset_type}`;
    const localIndex = roomTypeCounts[roomTypeKey] || 0;
    roomTypeCounts[roomTypeKey] = localIndex + 1;

    const localPlacement = scalePlacementToRoom(
      getSingleRoomPlacement(asset.asset_type, localIndex),
      room
    );

    placements[asset.id] = {
      roomId: room.id,
      roomType: room.type,
      pos: [
        localPlacement.pos[0] + room.center[0],
        localPlacement.pos[1],
        localPlacement.pos[2] + room.center[2],
      ],
      rot: localPlacement.rot,
      scale: localPlacement.scale,
    };
  });

  return placements;
};

export const getEffectiveLayoutMode = (layoutName, assetList = []) => {
  if (layoutName === 'city') {
    return 'city';
  }

  if (layoutName === 'house' || layoutName === 'all') {
    return 'house';
  }

  if (SINGLE_ROOM_LAYOUTS.has(layoutName)) {
    return layoutName;
  }

  if (assetList.length === 0) {
    return 'living';
  }

  const discoveredTypes = new Set(
    assetList.flatMap((asset) => getRoomTypeCandidates(asset, DEFAULT_HOUSE_CONFIG))
  );
  if (discoveredTypes.size > 1) {
    return 'house';
  }

  return Array.from(discoveredTypes)[0] || 'living';
};
