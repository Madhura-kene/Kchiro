export const DETAIL_ROLE_DEFINITIONS = [
  {
    key: 'pillows_sheets',
    label: 'Pillows / Sheets',
    keywords: ['pillow', 'sheet', 'sheets'],
  },
  {
    key: 'blankets',
    label: 'Blankets',
    keywords: ['blanket', 'duvet', 'comforter', 'quilt'],
  },
  {
    key: 'cushions',
    label: 'Cushions / Upholstery',
    keywords: ['cushion', 'upholstery'],
  },
  {
    key: 'frame',
    label: 'Frame / Wood',
    keywords: ['frame', 'wood', 'oak', 'board', 'carcass', 'shelf', 'door'],
  },
  {
    key: 'metal',
    label: 'Metal',
    keywords: ['metal', 'steel', 'iron', 'chrome', 'brass', 'handle', 'hoop'],
  },
  {
    key: 'glass_mirror',
    label: 'Glass / Mirror',
    keywords: ['glass', 'mirror'],
  },
  {
    key: 'accent',
    label: 'Accent Parts',
    keywords: ['canvas', 'shade', 'dial', 'face', 'trim'],
  },
];

const PRIMARY_EXCLUSION_KEYWORDS = [
  'glass',
  'soil',
  'stem',
  'leaf',
  'plant',
  'water',
  'flame',
  'ticks',
  'mirror',
  'fringe',
  'glow',
  'hands',
  'pin',
];

export const normalizeHexColor = (value, fallback = '#8b5cf6') => {
  if (typeof value !== 'string') return fallback;
  const normalized = value.trim().toLowerCase();
  return /^#[0-9a-f]{6}$/.test(normalized) ? normalized : fallback;
};

export const isPrimaryMaterialName = (materialName = '') => {
  const lowerName = materialName.toLowerCase();
  return !PRIMARY_EXCLUSION_KEYWORDS.some((keyword) => lowerName.includes(keyword));
};

export const findDetailRole = (materialName = '') => {
  const lowerName = materialName.toLowerCase();
  return DETAIL_ROLE_DEFINITIONS.find((role) =>
    role.keywords.some((keyword) => lowerName.includes(keyword))
  );
};

export const detectMaterialRoleMetadata = (materials = []) => {
  const grouped = new Map();
  let hasUnmappedPrimaryMaterials = false;

  materials.forEach((material) => {
    const role = findDetailRole(material.name || '');
    if (!role) {
      if (isPrimaryMaterialName(material.name || '')) {
        hasUnmappedPrimaryMaterials = true;
      }
      return;
    }

    const existing = grouped.get(role.key);
    if (existing) {
      existing.materialNames.push(material.name);
      if (!existing.defaultColor && material.color) {
        existing.defaultColor = normalizeHexColor(material.color, '#8b5cf6');
      }
      return;
    }

    grouped.set(role.key, {
      key: role.key,
      label: role.label,
      materialNames: [material.name],
      defaultColor: material.color ? normalizeHexColor(material.color, '#8b5cf6') : '#8b5cf6',
    });
  });

  return {
    materialRoles: DETAIL_ROLE_DEFINITIONS.map((role) => grouped.get(role.key)).filter(Boolean),
    hasUnmappedPrimaryMaterials,
  };
};
