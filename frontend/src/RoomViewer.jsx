import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import {
  detectMaterialRoleMetadata,
  findDetailRole,
  isPrimaryMaterialName,
  normalizeHexColor,
} from './roomMaterialUtils';
import {
  DEFAULT_WALL_COLORS,
  buildLayoutPlan,
  buildLayoutPlacements,
  normalizeWallColors,
} from './roomLayoutUtils';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const ROOM_PREVIEW_COLORS = {
  armchair: '#60a5fa',
  barrel: '#a16207',
  bathtub: '#93c5fd',
  bed: '#38bdf8',
  bench: '#f59e0b',
  bookcase: '#f59e0b',
  cabinet: '#eab308',
  chair: '#22c55e',
  clock: '#f8fafc',
  closet: '#eab308',
  coffee_table: '#f59e0b',
  couch: '#818cf8',
  countertop: '#d4d4d8',
  crate: '#b45309',
  desk: '#f97316',
  dining_table: '#f97316',
  dresser: '#f59e0b',
  fridge: '#e2e8f0',
  lamp: '#fde68a',
  mirror: '#bfdbfe',
  nightstand: '#fb923c',
  painting: '#f472b6',
  picture_frame: '#f9a8d4',
  plant_pot: '#34d399',
  rug: '#a78bfa',
  shelf: '#f59e0b',
  shower: '#7dd3fc',
  sink: '#93c5fd',
  sofa: '#6366f1',
  stool: '#22c55e',
  sword: '#cbd5e1',
  dagger: '#e2e8f0',
  table: '#fb923c',
  toilet: '#cbd5e1',
  torch: '#fb7185',
  axe: '#94a3b8',
  hammer: '#94a3b8',
  mace: '#64748b',
  spear: '#d4d4d8',
  halberd: '#94a3b8',
  staff: '#92400e',
  bow: '#b45309',
  crossbow: '#7c3aed',
  arrow: '#f8fafc',
  bolt: '#cbd5e1',
  magic_staff: '#60a5fa',
  wand: '#a78bfa',
  orb: '#22d3ee',
  chestplate: '#94a3b8',
  gauntlets: '#cbd5e1',
  boots: '#92400e',
  backpack: '#b45309',
  belt: '#7c2d12',
  pouch: '#a16207',
  cape: '#dc2626',
  tent: '#ca8a04',
  campfire: '#f97316',
  sleeping_bag: '#2563eb',
  lantern: '#facc15',
  cooking_pot: '#475569',
  supply_box: '#92400e',
  tv_stand: '#f59e0b',
  vase: '#2dd4bf',
  wardrobe: '#facc15',
  wall: '#c2410c',
  floor: '#a16207',
  ceiling: '#e5e7eb',
  roof: '#b91c1c',
  pillar: '#94a3b8',
  beam: '#92400e',
  foundation: '#64748b',
  door: '#b45309',
  window: '#93c5fd',
  archway: '#78716c',
  gate: '#475569',
  stairs: '#a16207',
  ladder: '#ca8a04',
  ramp: '#64748b',
  bridge: '#92400e',
  balcony: '#94a3b8',
  fence: '#b45309',
  railing: '#64748b',
  chimney: '#b91c1c',
  porch: '#a16207',
  castle_wall: '#78716c',
  tower: '#64748b',
  drawbridge: '#78350f',
  throne: '#d4af37',
  banner: '#dc2626',
  market_stall: '#ea580c',
  well: '#6b7280',
  cart: '#a16207',
  anvil: '#475569',
  forge: '#991b1b',
  control_panel: '#22d3ee',
  terminal: '#0ea5e9',
  computer: '#60a5fa',
  server_rack: '#475569',
  energy_cell: '#22d3ee',
  tech_crate: '#334155',
  space_door: '#94a3b8',
  airlock: '#64748b',
  turret: '#ef4444',
  drone: '#38bdf8',
  pipe: '#94a3b8',
  valve: '#eab308',
  tank: '#64748b',
  generator: '#f59e0b',
  conveyor_belt: '#475569',
  toolbox: '#f97316',
  forklift: '#eab308',
  storage_rack: '#94a3b8',
  street_lamp: '#f8fafc',
  traffic_light: '#22c55e',
  road_sign: '#f8fafc',
  street_bench: '#a16207',
  mailbox: '#dc2626',
  trash_can: '#15803d',
  bus_stop: '#93c5fd',
  phone_booth: '#dc2626',
  car: '#ef4444',
  truck: '#3b82f6',
  bike: '#22c55e',
  motorcycle: '#f97316',
  tractor: '#16a34a',
  battle_tank: '#4d7c0f',
  boat: '#38bdf8',
  canoe: '#a16207',
  ship: '#64748b',
  plane: '#e2e8f0',
  helicopter: '#94a3b8',
  male: '#60a5fa',
  female: '#f472b6',
  child: '#22c55e',
  elder: '#a78bfa',
  merchant: '#ca8a04',
  guard: '#2563eb',
  farmer: '#92400e',
  blacksmith: '#57534e',
  soldier: '#dc2626',
  elf: '#16a34a',
  orc: '#65a30d',
  goblin: '#84cc16',
  dwarf: '#f59e0b',
  dragon: '#15803d',
  dog: '#a16207',
  cat: '#f97316',
  horse: '#92400e',
  cow: '#f8fafc',
  deer: '#d97706',
  wolf: '#64748b',
  bird: '#0ea5e9',
  fish: '#94a3b8',
  coin: '#facc15',
  gem: '#a855f7',
  key: '#fbbf24',
  scroll: '#f5e6c8',
  potion: '#3b82f6',
  treasure_chest: '#b45309',
  artifact: '#22d3ee',
  terrain: '#65a30d',
  hill: '#84cc16',
  mountain: '#64748b',
  cliff: '#475569',
  valley: '#16a34a',
  cave: '#334155',
  ground_tile: '#65a30d',
  road_tile: '#475569',
  path_tile: '#92400e',
  river_tile: '#0284c7',
  dungeon_tile: '#78716c',
  oak_tree: '#166534',
  pine_tree: '#14532d',
  birch_tree: '#84cc16',
  palm_tree: '#22c55e',
  dead_tree: '#57534e',
  sapling: '#65a30d',
  grass: '#4ade80',
  bush: '#16a34a',
  shrub: '#65a30d',
  fern: '#15803d',
  flower: '#fb7185',
  moss: '#3f6212',
  small_rock: '#94a3b8',
  boulder: '#64748b',
  rock_cluster: '#475569',
  cliff_section: '#334155',
  log: '#92400e',
  tree_stump: '#78350f',
  fallen_tree: '#854d0e',
  mushroom: '#ef4444',
  vine: '#22c55e',
  root: '#7c2d12',
  pond: '#0ea5e9',
  river_segment: '#0284c7',
  waterfall: '#38bdf8',
  stream: '#06b6d4',
  game_background_2d: '#1d4ed8',
};

const SHELL_FLOOR_COLORS = {
  floor: '#10131e',
  lot: '#151922',
  sidewalk: '#7c8799',
  road: '#242833',
  crosswalk: '#e2e8f0',
};

const addFloorSpace = (scene, floorMaterials, floorSpace, wallThickness) => {
  const materialKey = floorSpace.materialKey || 'floor';
  const floorMaterial = floorMaterials[materialKey] || floorMaterials.floor;
  const floorMesh = new THREE.Mesh(
    new THREE.BoxGeometry(floorSpace.width, wallThickness, floorSpace.depth),
    floorMaterial
  );
  floorMesh.position.set(floorSpace.center[0], -wallThickness / 2, floorSpace.center[2]);
  floorMesh.receiveShadow = true;
  scene.add(floorMesh);
};

const addWallSegment = (scene, material, wallSegment) => {
  const mesh = new THREE.Mesh(
    new THREE.BoxGeometry(...wallSegment.size),
    material
  );
  mesh.position.set(...wallSegment.position);
  mesh.receiveShadow = true;
  mesh.castShadow = true;
  scene.add(mesh);
};

const createPreviewMaterial = (hex) =>
  new THREE.MeshStandardMaterial({
    color: new THREE.Color(hex),
    roughness: 0.65,
    metalness: 0.12,
  });

const addBox = (group, width, height, depth, material, yOffset = height / 2) => {
  const mesh = new THREE.Mesh(
    new THREE.BoxGeometry(Math.max(width, 0.05), Math.max(height, 0.05), Math.max(depth, 0.05)),
    material
  );
  mesh.position.y = yOffset;
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  group.add(mesh);
};

const addCylinder = (group, radiusTop, radiusBottom, height, material) => {
  const mesh = new THREE.Mesh(
    new THREE.CylinderGeometry(
      Math.max(radiusTop, 0.03),
      Math.max(radiusBottom, 0.03),
      Math.max(height, 0.05),
      24
    ),
    material
  );
  mesh.position.y = Math.max(height, 0.05) / 2;
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  group.add(mesh);
};

const addSphere = (group, radius, material, yOffset = radius) => {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(Math.max(radius, 0.04), 18, 14),
    material
  );
  mesh.position.y = yOffset;
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  group.add(mesh);
};

const applyObjectColor = (root, hex) => {
  if (!root || !hex || !hex.startsWith('#')) return;

  root.traverse((child) => {
    if (!child.isMesh || !child.material) return;
    const materials = Array.isArray(child.material) ? child.material : [child.material];
    materials.forEach((material) => {
      if (material?.color) {
        material.color.set(hex);
      }
    });
  });
};

const getMaterialHex = (material) => {
  if (!material?.color) return null;
  return `#${material.color.getHexString()}`;
};

const captureOriginalMaterialColors = (root) => {
  root.traverse((child) => {
    if (!child.isMesh || !child.material) return;
    const materials = Array.isArray(child.material) ? child.material : [child.material];
    materials.forEach((material) => {
      if (material?.color && !material.userData?.kchiroOriginalHex) {
        material.userData = material.userData || {};
        material.userData.kchiroOriginalHex = getMaterialHex(material);
      }
    });
  });
};

const resetObjectMaterialColors = (root) => {
  root.traverse((child) => {
    if (!child.isMesh || !child.material) return;
    const materials = Array.isArray(child.material) ? child.material : [child.material];
    materials.forEach((material) => {
      const originalHex = material?.userData?.kchiroOriginalHex;
      if (originalHex && material?.color) {
        material.color.set(originalHex);
      }
    });
  });
};

const collectMaterialMetadata = (root) => {
  const seen = new Map();

  root.traverse((child) => {
    if (!child.isMesh || !child.material) return;
    const materials = Array.isArray(child.material) ? child.material : [child.material];
    materials.forEach((material) => {
      if (!material?.name || seen.has(material.name)) return;
      seen.set(material.name, {
        name: material.name,
        color: normalizeHexColor(getMaterialHex(material) || '#8b5cf6'),
      });
    });
  });

  return {
    materialNames: Array.from(seen.keys()),
    ...detectMaterialRoleMetadata(Array.from(seen.values())),
  };
};

const applyObjectColorOverrides = (root, baseColor, detailColors = {}) => {
  if (!root) return;

  resetObjectMaterialColors(root);

  root.traverse((child) => {
    if (!child.isMesh || !child.material) return;
    const materials = Array.isArray(child.material) ? child.material : [child.material];

    materials.forEach((material) => {
      if (!material?.color) return;

      const materialName = material.name || '';
      const role = findDetailRole(materialName);
      const detailColor = role ? normalizeHexColor(detailColors?.[role.key] || '', '') : '';

      if (baseColor && isPrimaryMaterialName(materialName)) {
        material.color.set(baseColor);
      }

      if (detailColor) {
        material.color.set(detailColor);
      }
    });
  });
};

const createAssetPreview = (assetType, size, customColor) => {
  const safeSize = {
    x: Math.max(size.x || 0.6, 0.08),
    y: Math.max(size.y || 0.6, 0.08),
    z: Math.max(size.z || 0.6, 0.08),
  };

  const primary = createPreviewMaterial(customColor || ROOM_PREVIEW_COLORS[assetType] || '#94a3b8');
  const secondary = createPreviewMaterial('#e2e8f0');
  const dark = createPreviewMaterial('#334155');
  const green = createPreviewMaterial('#22c55e');
  const group = new THREE.Group();

  switch (assetType) {
    case 'sword':
    case 'dagger': {
      const bladeHeight = safeSize.y * (assetType === 'dagger' ? 0.5 : 0.64);
      const gripHeight = safeSize.y * (assetType === 'dagger' ? 0.24 : 0.2);
      const guardHeight = safeSize.y * 0.05;
      addSphere(group, safeSize.x * 0.08, primary, safeSize.x * 0.08);
      addBox(group, safeSize.x * 0.12, gripHeight, Math.max(safeSize.z * 0.12, 0.06), dark, safeSize.x * 0.16 + gripHeight / 2);
      addBox(group, safeSize.x * 0.48, guardHeight, Math.max(safeSize.z * 0.16, 0.08), primary, safeSize.x * 0.16 + gripHeight + guardHeight / 2);
      addBox(group, safeSize.x * 0.16, bladeHeight, Math.max(safeSize.z * 0.08, 0.05), secondary, safeSize.x * 0.16 + gripHeight + guardHeight + bladeHeight / 2);
      const tip = new THREE.Mesh(
        new THREE.ConeGeometry(Math.max(safeSize.x * 0.08, 0.04), Math.max(safeSize.y * 0.12, 0.08), 6),
        secondary
      );
      tip.position.y = safeSize.x * 0.16 + gripHeight + guardHeight + bladeHeight + Math.max(safeSize.y * 0.06, 0.04);
      tip.castShadow = true;
      tip.receiveShadow = true;
      group.add(tip);
      break;
    }
    case 'axe':
    case 'hammer':
    case 'mace':
    case 'spear':
    case 'halberd':
    case 'staff':
    case 'bow':
    case 'crossbow':
    case 'arrow':
    case 'bolt':
    case 'magic_staff':
    case 'wand':
    case 'orb': {
      if (assetType === 'orb') {
        addCylinder(group, safeSize.x * 0.14, safeSize.x * 0.16, safeSize.y * 0.12, dark);
        addCylinder(group, safeSize.x * 0.06, safeSize.x * 0.06, safeSize.y * 0.12, dark);
        group.children[group.children.length - 1].position.y = safeSize.y * 0.18;
        addSphere(group, safeSize.x * 0.24, primary, safeSize.y * 0.44);
        break;
      }

      if (assetType === 'bow') {
        const segments = [
          { x: 0.02, y: safeSize.y * 0.14, rot: -0.32 },
          { x: safeSize.x * 0.08, y: safeSize.y * 0.34, rot: -0.18 },
          { x: safeSize.x * 0.12, y: safeSize.y * 0.54, rot: 0.0 },
          { x: safeSize.x * 0.08, y: safeSize.y * 0.74, rot: 0.18 },
          { x: 0.02, y: safeSize.y * 0.9, rot: 0.32 },
        ];
        segments.forEach((segment, index) => {
          const limb = new THREE.Mesh(
            new THREE.BoxGeometry(Math.max(safeSize.x * 0.08, 0.05), Math.max(safeSize.y * 0.22, 0.12), Math.max(safeSize.z * 0.1, 0.05)),
            primary
          );
          limb.position.set(segment.x, segment.y, 0);
          limb.rotation.z = segment.rot;
          limb.castShadow = true;
          limb.receiveShadow = true;
          group.add(limb);
        });
        addBox(group, Math.max(safeSize.x * 0.04, 0.03), safeSize.y, Math.max(safeSize.z * 0.05, 0.03), secondary, safeSize.y / 2);
        addBox(group, Math.max(safeSize.x * 0.1, 0.05), safeSize.y * 0.18, Math.max(safeSize.z * 0.12, 0.06), dark, safeSize.y * 0.5);
        break;
      }

      const shaftHeight = assetType === 'wand' ? safeSize.y * 0.6 : safeSize.y * 0.82;
      const shaftWidth = assetType === 'crossbow' ? safeSize.x * 0.16 : safeSize.x * 0.1;
      addBox(group, Math.max(shaftWidth, 0.05), Math.max(shaftHeight, 0.18), Math.max(safeSize.z * 0.1, 0.05), dark, shaftHeight / 2);

      if (assetType === 'axe' || assetType === 'halberd') {
        addBox(group, safeSize.x * 0.48, safeSize.y * 0.18, Math.max(safeSize.z * 0.12, 0.07), primary, shaftHeight * 0.78);
        addBox(group, safeSize.x * 0.22, safeSize.y * 0.26, Math.max(safeSize.z * 0.08, 0.05), secondary, shaftHeight * 0.8);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.28;
        if (assetType === 'halberd') {
          addBox(group, safeSize.x * 0.18, safeSize.y * 0.22, Math.max(safeSize.z * 0.08, 0.05), secondary, shaftHeight * 0.84);
          group.children[group.children.length - 1].position.x = -safeSize.x * 0.18;
          const topTip = new THREE.Mesh(
            new THREE.ConeGeometry(Math.max(safeSize.x * 0.08, 0.04), Math.max(safeSize.y * 0.16, 0.08), 6),
            secondary
          );
          topTip.position.y = shaftHeight + safeSize.y * 0.08;
          topTip.castShadow = true;
          topTip.receiveShadow = true;
          group.add(topTip);
        }
      } else if (assetType === 'hammer') {
        addBox(group, safeSize.x * 0.58, safeSize.y * 0.18, Math.max(safeSize.z * 0.16, 0.08), primary, shaftHeight * 0.78);
      } else if (assetType === 'mace') {
        addSphere(group, safeSize.x * 0.18, primary, shaftHeight * 0.82);
        addBox(group, safeSize.x * 0.08, safeSize.y * 0.14, Math.max(safeSize.z * 0.06, 0.04), secondary, shaftHeight * 0.96);
      } else if (assetType === 'spear' || assetType === 'staff' || assetType === 'magic_staff' || assetType === 'wand' || assetType === 'arrow' || assetType === 'bolt') {
        const tip = new THREE.Mesh(
          new THREE.ConeGeometry(Math.max(safeSize.x * (assetType === 'wand' ? 0.06 : 0.08), 0.04), Math.max(safeSize.y * (assetType === 'wand' ? 0.12 : 0.18), 0.08), 6),
          assetType === 'staff' ? primary : secondary
        );
        tip.position.y = shaftHeight + tip.geometry.parameters.height / 2 - 0.01;
        tip.castShadow = true;
        tip.receiveShadow = true;
        group.add(tip);
        if (assetType === 'magic_staff' || assetType === 'wand') {
          addSphere(group, safeSize.x * (assetType === 'wand' ? 0.08 : 0.14), primary, shaftHeight + safeSize.y * 0.12);
        }
        if (assetType === 'arrow' || assetType === 'bolt') {
          addBox(group, safeSize.x * 0.22, safeSize.y * 0.12, Math.max(safeSize.z * 0.04, 0.03), primary, safeSize.y * 0.16);
        }
      } else if (assetType === 'crossbow') {
        addBox(group, safeSize.x * 0.62, safeSize.y * 0.12, Math.max(safeSize.z * 0.12, 0.06), primary, shaftHeight * 0.76);
        addBox(group, safeSize.x * 0.12, safeSize.y * 0.32, Math.max(safeSize.z * 0.08, 0.05), secondary, shaftHeight * 0.48);
        addBox(group, safeSize.x * 0.08, safeSize.y * 0.4, Math.max(safeSize.z * 0.05, 0.03), dark, shaftHeight * 0.74);
      }
      break;
    }
    case 'chestplate':
    case 'gauntlets':
    case 'boots':
    case 'backpack':
    case 'belt':
    case 'pouch':
    case 'cape':
    case 'tent':
    case 'campfire':
    case 'sleeping_bag':
    case 'lantern':
    case 'cooking_pot':
    case 'supply_box':
    case 'castle_wall':
    case 'tower':
    case 'drawbridge':
    case 'throne':
    case 'banner':
    case 'market_stall':
    case 'well':
    case 'cart':
    case 'anvil':
    case 'forge': {
      if (assetType === 'chestplate') {
        addBox(group, safeSize.x * 0.7, safeSize.y * 0.48, safeSize.z * 0.52, primary, safeSize.y * 0.36);
        addBox(group, safeSize.x * 0.88, safeSize.y * 0.24, safeSize.z * 0.58, primary, safeSize.y * 0.72);
        addBox(group, safeSize.x * 0.2, safeSize.y * 0.12, safeSize.z * 0.26, secondary, safeSize.y * 0.84);
        addSphere(group, safeSize.x * 0.12, primary, safeSize.y * 0.78);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.36;
        addSphere(group, safeSize.x * 0.12, primary, safeSize.y * 0.78);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.36;
        break;
      }

      if (assetType === 'gauntlets') {
        addBox(group, safeSize.x * 0.24, safeSize.y * 0.52, safeSize.z * 0.32, primary, safeSize.y * 0.46);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.22;
        addBox(group, safeSize.x * 0.24, safeSize.y * 0.52, safeSize.z * 0.32, primary, safeSize.y * 0.46);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.22;
        addBox(group, safeSize.x * 0.22, safeSize.y * 0.18, safeSize.z * 0.3, dark, safeSize.y * 0.18);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.22;
        addBox(group, safeSize.x * 0.22, safeSize.y * 0.18, safeSize.z * 0.3, dark, safeSize.y * 0.18);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.22;
        break;
      }

      if (assetType === 'boots') {
        addBox(group, safeSize.x * 0.24, safeSize.y * 0.56, safeSize.z * 0.28, primary, safeSize.y * 0.34);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.2;
        group.children[group.children.length - 1].position.z = -safeSize.z * 0.08;
        addBox(group, safeSize.x * 0.24, safeSize.y * 0.56, safeSize.z * 0.28, primary, safeSize.y * 0.34);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.2;
        group.children[group.children.length - 1].position.z = -safeSize.z * 0.08;
        addBox(group, safeSize.x * 0.24, safeSize.y * 0.18, safeSize.z * 0.34, dark, safeSize.y * 0.1);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.2;
        group.children[group.children.length - 1].position.z = safeSize.z * 0.16;
        addBox(group, safeSize.x * 0.24, safeSize.y * 0.18, safeSize.z * 0.34, dark, safeSize.y * 0.1);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.2;
        group.children[group.children.length - 1].position.z = safeSize.z * 0.16;
        break;
      }

      if (assetType === 'backpack') {
        addBox(group, safeSize.x * 0.72, safeSize.y * 0.76, safeSize.z * 0.54, primary, safeSize.y * 0.42);
        addBox(group, safeSize.x * 0.78, safeSize.y * 0.18, safeSize.z * 0.58, primary, safeSize.y * 0.78);
        addBox(group, safeSize.x * 0.12, safeSize.y * 0.72, safeSize.z * 0.12, dark, safeSize.y * 0.42);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.2;
        group.children[group.children.length - 1].position.z = -safeSize.z * 0.22;
        addBox(group, safeSize.x * 0.12, safeSize.y * 0.72, safeSize.z * 0.12, dark, safeSize.y * 0.42);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.2;
        group.children[group.children.length - 1].position.z = -safeSize.z * 0.22;
        break;
      }

      if (assetType === 'belt') {
        addBox(group, safeSize.x, safeSize.y * 0.12, safeSize.z * 0.12, primary, safeSize.y * 0.12);
        addBox(group, safeSize.x * 0.16, safeSize.y * 0.18, safeSize.z * 0.18, secondary, safeSize.y * 0.18);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.42;
        break;
      }

      if (assetType === 'pouch') {
        addBox(group, safeSize.x * 0.62, safeSize.y * 0.62, safeSize.z * 0.5, primary, safeSize.y * 0.32);
        addBox(group, safeSize.x * 0.66, safeSize.y * 0.18, safeSize.z * 0.52, primary, safeSize.y * 0.66);
        addBox(group, safeSize.x * 0.12, safeSize.y * 0.14, safeSize.z * 0.08, secondary, safeSize.y * 0.5);
        group.children[group.children.length - 1].position.z = safeSize.z * 0.26;
        break;
      }

      if (assetType === 'cape') {
        addBox(group, safeSize.x * 0.82, safeSize.y * 0.92, Math.max(safeSize.z * 0.06, 0.03), primary, safeSize.y * 0.46);
        addBox(group, safeSize.x * 0.22, safeSize.y * 0.08, Math.max(safeSize.z * 0.08, 0.04), secondary, safeSize.y * 0.94);
        break;
      }

      if (assetType === 'tent') {
        const leftPanel = new THREE.Mesh(
          new THREE.BoxGeometry(Math.max(safeSize.x * 0.1, 0.05), safeSize.y * 0.9, Math.max(safeSize.z, 0.08)),
          primary
        );
        leftPanel.position.set(-safeSize.x * 0.22, safeSize.y * 0.5, 0);
        leftPanel.rotation.z = Math.PI / 2;
        leftPanel.rotation.y = -0.52;
        leftPanel.castShadow = true;
        leftPanel.receiveShadow = true;
        group.add(leftPanel);
        const rightPanel = leftPanel.clone();
        rightPanel.position.x = safeSize.x * 0.22;
        rightPanel.rotation.y = 0.52;
        group.add(rightPanel);
        addBox(group, safeSize.x * 0.84, Math.max(safeSize.y * 0.06, 0.03), safeSize.z * 0.78, dark, safeSize.y * 0.03);
        break;
      }

      if (assetType === 'campfire') {
        for (let i = 0; i < 3; i += 1) {
          const log = new THREE.Mesh(
            new THREE.CylinderGeometry(Math.max(safeSize.x * 0.06, 0.03), Math.max(safeSize.x * 0.06, 0.03), safeSize.x * 0.56, 12),
            dark
          );
          log.rotation.z = Math.PI / 2;
          log.rotation.y = i * 1.05;
          log.position.y = safeSize.y * 0.08 + i * safeSize.y * 0.03;
          log.castShadow = true;
          log.receiveShadow = true;
          group.add(log);
        }
        const flame = new THREE.Mesh(
          new THREE.ConeGeometry(Math.max(safeSize.x * 0.14, 0.06), Math.max(safeSize.y * 0.46, 0.14), 8),
          primary
        );
        flame.position.y = safeSize.y * 0.34;
        flame.castShadow = true;
        flame.receiveShadow = true;
        group.add(flame);
        break;
      }

      if (assetType === 'sleeping_bag') {
        addBox(group, safeSize.x * 0.72, safeSize.y * 0.24, safeSize.z, primary, safeSize.y * 0.12);
        addSphere(group, safeSize.x * 0.22, primary, safeSize.y * 0.18);
        group.children[group.children.length - 1].position.z = -safeSize.z * 0.3;
        break;
      }

      if (assetType === 'lantern') {
        addBox(group, safeSize.x * 0.52, safeSize.y * 0.16, safeSize.z * 0.52, dark, safeSize.y * 0.08);
        addBox(group, safeSize.x * 0.42, safeSize.y * 0.5, safeSize.z * 0.42, secondary, safeSize.y * 0.4);
        addBox(group, safeSize.x * 0.52, safeSize.y * 0.14, safeSize.z * 0.52, dark, safeSize.y * 0.72);
        addSphere(group, safeSize.x * 0.08, primary, safeSize.y * 0.42);
        break;
      }

      if (assetType === 'cooking_pot') {
        addCylinder(group, safeSize.x * 0.3, safeSize.x * 0.24, safeSize.y * 0.54, primary);
        addBox(group, safeSize.x * 0.18, safeSize.y * 0.08, safeSize.z * 0.08, dark, safeSize.y * 0.32);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.34;
        addBox(group, safeSize.x * 0.18, safeSize.y * 0.08, safeSize.z * 0.08, dark, safeSize.y * 0.32);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.34;
        addBox(group, safeSize.x * 0.38, safeSize.y * 0.06, safeSize.z * 0.38, secondary, safeSize.y * 0.58);
        break;
      }

      if (assetType === 'supply_box') {
        addBox(group, safeSize.x, safeSize.y * 0.62, safeSize.z * 0.72, primary, safeSize.y * 0.31);
        addBox(group, safeSize.x * 0.96, safeSize.y * 0.18, safeSize.z * 0.76, dark, safeSize.y * 0.72);
        break;
      }

      if (assetType === 'castle_wall') {
        addBox(group, safeSize.x, safeSize.y, safeSize.z * 0.36, primary, safeSize.y * 0.5);
        for (let i = 0; i < 5; i += 1) {
          addBox(group, safeSize.x * 0.12, safeSize.y * 0.16, safeSize.z * 0.28, secondary, safeSize.y * 1.02);
          group.children[group.children.length - 1].position.x = -safeSize.x * 0.4 + i * safeSize.x * 0.2;
        }
        break;
      }

      if (assetType === 'tower') {
        addCylinder(group, safeSize.x * 0.38, safeSize.x * 0.38, safeSize.y, primary);
        for (let i = 0; i < 6; i += 1) {
          addBox(group, safeSize.x * 0.12, safeSize.y * 0.16, safeSize.z * 0.14, secondary, safeSize.y * 1.02);
          const angle = (Math.PI * 2 * i) / 6;
          group.children[group.children.length - 1].position.x = Math.cos(angle) * safeSize.x * 0.34;
          group.children[group.children.length - 1].position.z = Math.sin(angle) * safeSize.z * 0.34;
        }
        break;
      }

      if (assetType === 'drawbridge') {
        addBox(group, safeSize.x * 0.82, safeSize.y * 0.14, safeSize.z, primary, safeSize.y * 0.12);
        addBox(group, safeSize.x * 0.06, safeSize.y * 0.66, safeSize.z * 0.08, secondary, safeSize.y * 0.54);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.34;
        group.children[group.children.length - 1].position.z = safeSize.z * 0.42;
        addBox(group, safeSize.x * 0.06, safeSize.y * 0.66, safeSize.z * 0.08, secondary, safeSize.y * 0.54);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.34;
        group.children[group.children.length - 1].position.z = safeSize.z * 0.42;
        break;
      }

      if (assetType === 'throne') {
        addBox(group, safeSize.x * 0.58, safeSize.y * 0.14, safeSize.z * 0.48, primary, safeSize.y * 0.38);
        addBox(group, safeSize.x * 0.68, safeSize.y * 0.62, safeSize.z * 0.14, primary, safeSize.y * 0.72);
        addBox(group, safeSize.x * 0.14, safeSize.y * 0.34, safeSize.z * 0.48, secondary, safeSize.y * 0.42);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.34;
        addBox(group, safeSize.x * 0.14, safeSize.y * 0.34, safeSize.z * 0.48, secondary, safeSize.y * 0.42);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.34;
        break;
      }

      if (assetType === 'banner') {
        addBox(group, safeSize.x * 0.08, safeSize.y, safeSize.z * 0.08, dark, safeSize.y * 0.5);
        addBox(group, safeSize.x * 0.08, safeSize.y * 0.56, safeSize.z * 0.66, primary, safeSize.y * 0.62);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.24;
        break;
      }

      if (assetType === 'market_stall') {
        addBox(group, safeSize.x * 0.78, safeSize.y * 0.12, safeSize.z * 0.52, dark, safeSize.y * 0.36);
        addBox(group, safeSize.x, safeSize.y * 0.14, safeSize.z * 0.72, primary, safeSize.y * 0.86);
        addBox(group, safeSize.x * 0.08, safeSize.y * 0.74, safeSize.z * 0.08, dark, safeSize.y * 0.38);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.34;
        group.children[group.children.length - 1].position.z = -safeSize.z * 0.22;
        addBox(group, safeSize.x * 0.08, safeSize.y * 0.74, safeSize.z * 0.08, dark, safeSize.y * 0.38);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.34;
        group.children[group.children.length - 1].position.z = -safeSize.z * 0.22;
        break;
      }

      if (assetType === 'well') {
        addCylinder(group, safeSize.x * 0.34, safeSize.x * 0.34, safeSize.y * 0.28, primary);
        addBox(group, safeSize.x * 0.08, safeSize.y * 0.68, safeSize.z * 0.08, dark, safeSize.y * 0.62);
        group.children[group.children.length - 1].position.x = -safeSize.x * 0.18;
        addBox(group, safeSize.x * 0.08, safeSize.y * 0.68, safeSize.z * 0.08, dark, safeSize.y * 0.62);
        group.children[group.children.length - 1].position.x = safeSize.x * 0.18;
        addBox(group, safeSize.x * 0.56, safeSize.y * 0.08, safeSize.z * 0.48, secondary, safeSize.y * 1.02);
        break;
      }

      if (assetType === 'cart') {
        addBox(group, safeSize.x * 0.72, safeSize.y * 0.18, safeSize.z * 0.56, primary, safeSize.y * 0.46);
        for (const x of [-safeSize.x * 0.34, safeSize.x * 0.34]) {
          for (const z of [-safeSize.z * 0.22, safeSize.z * 0.22]) {
            const wheel = new THREE.Mesh(
              new THREE.CylinderGeometry(Math.max(safeSize.x * 0.14, 0.06), Math.max(safeSize.x * 0.14, 0.06), Math.max(safeSize.y * 0.08, 0.04), 16),
              dark
            );
            wheel.rotation.z = Math.PI / 2;
            wheel.position.set(x, safeSize.y * 0.18, z);
            wheel.castShadow = true;
            wheel.receiveShadow = true;
            group.add(wheel);
          }
        }
        break;
      }

      if (assetType === 'anvil') {
        addBox(group, safeSize.x * 0.68, safeSize.y * 0.16, safeSize.z * 0.34, primary, safeSize.y * 0.72);
        addBox(group, safeSize.x * 0.28, safeSize.y * 0.34, safeSize.z * 0.22, primary, safeSize.y * 0.42);
        const horn = new THREE.Mesh(
          new THREE.ConeGeometry(Math.max(safeSize.z * 0.12, 0.05), Math.max(safeSize.x * 0.32, 0.12), 8),
          primary
        );
        horn.rotation.z = -Math.PI / 2;
        horn.position.set(safeSize.x * 0.42, safeSize.y * 0.72, 0);
        horn.castShadow = true;
        horn.receiveShadow = true;
        group.add(horn);
        break;
      }

      if (assetType === 'forge') {
        addBox(group, safeSize.x, safeSize.y * 0.34, safeSize.z * 0.72, primary, safeSize.y * 0.17);
        addBox(group, safeSize.x * 0.62, safeSize.y * 0.16, safeSize.z * 0.42, dark, safeSize.y * 0.34);
        addBox(group, safeSize.x * 0.22, safeSize.y * 0.54, safeSize.z * 0.22, secondary, safeSize.y * 0.72);
        group.children[group.children.length - 1].position.z = -safeSize.z * 0.18;
        const flame = new THREE.Mesh(
          new THREE.ConeGeometry(Math.max(safeSize.x * 0.12, 0.05), Math.max(safeSize.y * 0.26, 0.1), 8),
          createPreviewMaterial('#fb7185')
        );
        flame.position.set(0, safeSize.y * 0.48, 0);
        flame.castShadow = true;
        flame.receiveShadow = true;
        group.add(flame);
        break;
      }
      break;
    }
    case 'rug':
      addBox(group, safeSize.x, Math.max(safeSize.y, 0.02), safeSize.z, primary);
      break;
    case 'clock':
    case 'mirror':
    case 'picture_frame':
    case 'painting':
    case 'towel_rack':
      addBox(group, safeSize.x, safeSize.y, Math.max(safeSize.z, 0.05), primary);
      break;
    case 'foundation':
      addBox(group, safeSize.x, safeSize.y * 0.35, safeSize.z, primary, safeSize.y * 0.175);
      addBox(group, safeSize.x * 0.22, safeSize.y * 0.65, safeSize.z * 0.22, dark, safeSize.y * 0.325);
      break;
    case 'door':
      addBox(group, safeSize.x, safeSize.y, Math.max(safeSize.z * 0.18, 0.08), primary);
      addBox(group, safeSize.x * 0.1, safeSize.y * 1.04, Math.max(safeSize.z * 0.08, 0.04), secondary);
      break;
    case 'window':
      addBox(group, safeSize.x, safeSize.y, Math.max(safeSize.z * 0.14, 0.08), secondary);
      addBox(group, safeSize.x * 0.14, safeSize.y, Math.max(safeSize.z * 0.16, 0.08), primary);
      addBox(group, safeSize.x, safeSize.y * 0.14, Math.max(safeSize.z * 0.16, 0.08), primary);
      break;
    case 'archway':
      addBox(group, safeSize.x * 0.18, safeSize.y, Math.max(safeSize.z, 0.12), primary);
      addBox(group, safeSize.x * 0.18, safeSize.y, Math.max(safeSize.z, 0.12), primary);
      group.children[group.children.length - 2].position.x = -safeSize.x * 0.36;
      group.children[group.children.length - 1].position.x = safeSize.x * 0.36;
      addBox(group, safeSize.x * 0.8, safeSize.y * 0.2, Math.max(safeSize.z, 0.12), secondary, safeSize.y * 0.9);
      break;
    case 'gate':
      addBox(group, safeSize.x, safeSize.y, Math.max(safeSize.z * 0.14, 0.08), primary);
      addBox(group, safeSize.x * 0.1, safeSize.y, Math.max(safeSize.z * 0.16, 0.08), dark);
      break;
    case 'stairs': {
      const steps = 4;
      for (let stepIndex = 0; stepIndex < steps; stepIndex += 1) {
        const stepHeight = safeSize.y * ((stepIndex + 1) / steps);
        const stepDepth = safeSize.z / steps;
        const step = new THREE.Mesh(
          new THREE.BoxGeometry(safeSize.x, stepHeight, Math.max(stepDepth, 0.06)),
          primary
        );
        step.position.set(0, stepHeight / 2, -safeSize.z / 2 + stepDepth * stepIndex + stepDepth / 2);
        step.castShadow = true;
        step.receiveShadow = true;
        group.add(step);
      }
      break;
    }
    case 'ladder':
      addBox(group, safeSize.x * 0.12, safeSize.y, Math.max(safeSize.z * 0.12, 0.06), primary);
      addBox(group, safeSize.x * 0.12, safeSize.y, Math.max(safeSize.z * 0.12, 0.06), primary);
      group.children[group.children.length - 2].position.x = -safeSize.x * 0.28;
      group.children[group.children.length - 1].position.x = safeSize.x * 0.28;
      for (let rungIndex = 0; rungIndex < 4; rungIndex += 1) {
        const rung = new THREE.Mesh(
          new THREE.BoxGeometry(safeSize.x * 0.56, Math.max(safeSize.y * 0.06, 0.05), Math.max(safeSize.z * 0.1, 0.05)),
          secondary
        );
        rung.position.set(0, safeSize.y * (0.18 + rungIndex * 0.2), 0);
        rung.castShadow = true;
        rung.receiveShadow = true;
        group.add(rung);
      }
      break;
    case 'ramp': {
      const ramp = new THREE.Mesh(
        new THREE.BufferGeometry(),
        primary
      );
      const vertices = new Float32Array([
        -safeSize.x / 2, 0, -safeSize.z / 2,
        safeSize.x / 2, 0, -safeSize.z / 2,
        safeSize.x / 2, 0, safeSize.z / 2,
        -safeSize.x / 2, 0, safeSize.z / 2,
        -safeSize.x / 2, 0, -safeSize.z / 2,
        safeSize.x / 2, 0, -safeSize.z / 2,
        safeSize.x / 2, safeSize.y, safeSize.z / 2,
        -safeSize.x / 2, safeSize.y, safeSize.z / 2,
      ]);
      const indices = [
        0, 1, 2, 0, 2, 3,
        4, 5, 6, 4, 6, 7,
        0, 1, 5, 0, 5, 4,
        1, 2, 6, 1, 6, 5,
        2, 3, 7, 2, 7, 6,
        3, 0, 4, 3, 4, 7,
      ];
      ramp.geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
      ramp.geometry.setIndex(indices);
      ramp.geometry.computeVertexNormals();
      ramp.castShadow = true;
      ramp.receiveShadow = true;
      group.add(ramp);
      break;
    }
    case 'bridge':
      addBox(group, safeSize.x, safeSize.y * 0.18, safeSize.z, primary, safeSize.y * 0.72);
      addBox(group, safeSize.x * 0.12, safeSize.y * 0.72, safeSize.z * 0.12, dark, safeSize.y * 0.36);
      addBox(group, safeSize.x * 0.12, safeSize.y * 0.72, safeSize.z * 0.12, dark, safeSize.y * 0.36);
      group.children[group.children.length - 2].position.z = -safeSize.z * 0.28;
      group.children[group.children.length - 1].position.z = safeSize.z * 0.28;
      break;
    case 'balcony':
      addBox(group, safeSize.x, safeSize.y * 0.18, safeSize.z, primary, safeSize.y * 0.1);
      addBox(group, safeSize.x, safeSize.y * 0.1, Math.max(safeSize.z * 0.08, 0.05), secondary, safeSize.y * 0.92);
      addBox(group, Math.max(safeSize.x * 0.08, 0.05), safeSize.y, Math.max(safeSize.z * 0.08, 0.05), secondary);
      addBox(group, Math.max(safeSize.x * 0.08, 0.05), safeSize.y, Math.max(safeSize.z * 0.08, 0.05), secondary);
      group.children[group.children.length - 2].position.x = -safeSize.x * 0.42;
      group.children[group.children.length - 1].position.x = safeSize.x * 0.42;
      break;
    case 'fence':
      addBox(group, safeSize.x, safeSize.y * 0.08, Math.max(safeSize.z * 0.12, 0.05), dark, safeSize.y * 0.66);
      addBox(group, safeSize.x, safeSize.y * 0.08, Math.max(safeSize.z * 0.12, 0.05), dark, safeSize.y * 0.34);
      for (let fenceIndex = 0; fenceIndex < 4; fenceIndex += 1) {
        const slat = new THREE.Mesh(
          new THREE.BoxGeometry(Math.max(safeSize.x * 0.12, 0.05), safeSize.y, Math.max(safeSize.z * 0.08, 0.05)),
          primary
        );
        slat.position.set(-safeSize.x * 0.36 + fenceIndex * safeSize.x * 0.24, safeSize.y / 2, 0);
        slat.castShadow = true;
        slat.receiveShadow = true;
        group.add(slat);
      }
      break;
    case 'railing':
      addBox(group, safeSize.x, Math.max(safeSize.y * 0.08, 0.05), Math.max(safeSize.z, 0.05), secondary, safeSize.y * 0.96);
      for (let railIndex = 0; railIndex < 5; railIndex += 1) {
        const baluster = new THREE.Mesh(
          new THREE.BoxGeometry(Math.max(safeSize.x * 0.06, 0.04), safeSize.y * 0.86, Math.max(safeSize.z * 0.3, 0.05)),
          primary
        );
        baluster.position.set(-safeSize.x * 0.42 + railIndex * safeSize.x * 0.21, safeSize.y * 0.43, 0);
        baluster.castShadow = true;
        baluster.receiveShadow = true;
        group.add(baluster);
      }
      break;
    case 'chimney':
      addBox(group, safeSize.x * 0.7, safeSize.y, safeSize.z * 0.7, primary);
      addBox(group, safeSize.x, safeSize.y * 0.08, safeSize.z, dark, safeSize.y * 1.02);
      break;
    case 'porch':
      addBox(group, safeSize.x, safeSize.y * 0.16, safeSize.z, primary, safeSize.y * 0.08);
      addBox(group, safeSize.x * 1.04, safeSize.y * 0.12, safeSize.z * 1.04, secondary, safeSize.y * 0.94);
      addBox(group, Math.max(safeSize.x * 0.08, 0.05), safeSize.y * 0.82, Math.max(safeSize.z * 0.08, 0.05), dark, safeSize.y * 0.49);
      addBox(group, Math.max(safeSize.x * 0.08, 0.05), safeSize.y * 0.82, Math.max(safeSize.z * 0.08, 0.05), dark, safeSize.y * 0.49);
      group.children[group.children.length - 2].position.x = -safeSize.x * 0.34;
      group.children[group.children.length - 1].position.x = safeSize.x * 0.34;
      break;
    case 'vase':
      addCylinder(group, safeSize.x * 0.22, safeSize.x * 0.38, safeSize.y, primary);
      break;
    case 'plant_pot':
      addCylinder(group, safeSize.x * 0.35, safeSize.x * 0.42, safeSize.y * 0.45, primary);
      addCylinder(group, safeSize.x * 0.14, safeSize.x * 0.08, safeSize.y * 0.55, green);
      break;
    case 'lamp':
      addCylinder(group, safeSize.x * 0.14, safeSize.x * 0.14, safeSize.y * 0.55, dark);
      addCylinder(group, safeSize.x * 0.35, safeSize.x * 0.22, safeSize.y * 0.45, primary);
      break;
    case 'barrel':
      addCylinder(group, safeSize.x * 0.45, safeSize.x * 0.45, safeSize.y, primary);
      break;
    case 'sofa':
    case 'couch':
    case 'armchair':
      addBox(group, safeSize.x, safeSize.y * 0.45, safeSize.z * 0.6, primary, safeSize.y * 0.225);
      addBox(group, safeSize.x, safeSize.y * 0.45, safeSize.z * 0.18, primary, safeSize.y * 0.675);
      break;
    case 'chair':
    case 'stool':
    case 'bench':
      addBox(group, safeSize.x, safeSize.y * 0.18, safeSize.z, primary, safeSize.y * 0.6);
      addBox(group, safeSize.x * 0.15, safeSize.y * 0.6, safeSize.z * 0.15, dark, safeSize.y * 0.3);
      break;
    case 'table':
    case 'coffee_table':
    case 'dining_table':
    case 'desk':
    case 'tv_stand':
    case 'nightstand':
      addBox(group, safeSize.x, safeSize.y * 0.12, safeSize.z, primary, safeSize.y * 0.88);
      addBox(group, safeSize.x * 0.12, safeSize.y * 0.88, safeSize.z * 0.12, dark, safeSize.y * 0.44);
      break;
    case 'bed':
    case 'bunk_bed':
      addBox(group, safeSize.x, safeSize.y * 0.28, safeSize.z, primary, safeSize.y * 0.2);
      addBox(group, safeSize.x, safeSize.y * 0.5, safeSize.z * 0.12, secondary, safeSize.y * 0.65);
      break;
    default:
      addBox(group, safeSize.x, safeSize.y, safeSize.z, primary);
      break;
  }

  return group;
};

export default function RoomViewer({
  assets,
  activeAssets,
  wallColors = DEFAULT_WALL_COLORS,
  houseConfig,
  layoutMode = 'living',
  selectedAssetId,
  onSelectAsset,
  transforms,
  onAssetMetadataChange,
}) {
  const containerRef = useRef(null);
  const sceneRef = useRef(null);
  const rendererRef = useRef(null);
  const cameraRef = useRef(null);
  const controlsRef = useRef(null);
  const renderSceneRef = useRef(() => {});
  const wallMaterialsRef = useRef({});
  const loadedObjectsRef = useRef({});
  const boxHelperRef = useRef(null);
  const loadingIdsRef = useRef(new Set());
  const activeAssetsRef = useRef(activeAssets);
  const layoutPlanRef = useRef(buildLayoutPlan(layoutMode, houseConfig));
  const [loadingProgress, setLoadingProgress] = useState({});

  activeAssetsRef.current = activeAssets;
  layoutPlanRef.current = buildLayoutPlan(layoutMode, houseConfig);

  const frameLayoutBounds = (planOverride = layoutPlanRef.current) => {
    const camera = cameraRef.current;
    const controls = controlsRef.current;
    if (!camera || !controls || !planOverride?.bounds) return;

    const { bounds } = planOverride;
    const width = Math.max(bounds.width, 1);
    const depth = Math.max(bounds.depth, 1);
    const maxDim = Math.max(width, depth, 3);
    const target = new THREE.Vector3(bounds.centerX, 0.8, bounds.centerZ);
    const offset = new THREE.Vector3(maxDim * 0.35, maxDim * 0.58, maxDim * 1.1);

    camera.position.copy(target.clone().add(offset));
    camera.lookAt(target);
    camera.updateProjectionMatrix();
    controls.target.copy(target);
    controls.update();
  };

  const frameVisibleAssets = () => {
    const scene = sceneRef.current;
    const camera = cameraRef.current;
    const controls = controlsRef.current;
    if (!scene || !camera || !controls) return;

    const visibleObjects = activeAssetsRef.current
      .map((id) => loadedObjectsRef.current[id])
      .filter((obj) => obj && scene.children.includes(obj));

    if (visibleObjects.length === 0) {
      frameLayoutBounds();
      return;
    }

    const bounds = new THREE.Box3();
    let hasBounds = false;

    visibleObjects.forEach((obj) => {
      const objBounds = new THREE.Box3().setFromObject(obj);
      if (!objBounds.isEmpty()) {
        if (!hasBounds) {
          bounds.copy(objBounds);
          hasBounds = true;
        } else {
          bounds.union(objBounds);
        }
      }
    });

    if (!hasBounds) return;

    const center = new THREE.Vector3();
    const size = new THREE.Vector3();
    bounds.getCenter(center);
    bounds.getSize(size);

    const maxDim = Math.max(size.x, size.y, size.z, 1);
    const target = new THREE.Vector3(center.x, Math.max(0.55, center.y * 0.5), center.z);
    const offset = new THREE.Vector3(maxDim * 0.75, maxDim * 0.42, maxDim * 1.5);

    camera.position.copy(target.clone().add(offset));
    camera.lookAt(target);
    camera.updateProjectionMatrix();
    controls.target.copy(target);
    controls.update();
  };

  useEffect(() => {
    if (!containerRef.current) return;
    const mountEl = containerRef.current;
    mountEl.replaceChildren();
    const layoutPlan = buildLayoutPlan(layoutMode, houseConfig);
    const normalizedWallColors = normalizeWallColors(wallColors);

    const scene = new THREE.Scene();
    scene.background = new THREE.Color('#090a0f');
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(
      50,
      Math.max(mountEl.clientWidth, 1) / Math.max(mountEl.clientHeight, 1),
      0.1,
      100
    );
    camera.position.set(2.6, 1.5, 4.8);
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(Math.max(mountEl.clientWidth, 1), Math.max(mountEl.clientHeight, 1));
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    mountEl.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = false;
    controls.maxPolarAngle = Math.PI / 2 - 0.05;
    controls.minDistance = 2;
    controls.maxDistance = Math.max(layoutPlan.bounds.width, layoutPlan.bounds.depth) * 2.4;
    controls.target.set(layoutPlan.bounds.centerX, 0.8, layoutPlan.bounds.centerZ);
    controls.update();
    controlsRef.current = controls;

    const renderScene = () => {
      if (boxHelperRef.current) {
        boxHelperRef.current.update();
      }
      renderer.render(scene, camera);
    };

    renderSceneRef.current = renderScene;
    controls.addEventListener('change', renderScene);

    const gridSize = Math.ceil(Math.max(layoutPlan.bounds.width, layoutPlan.bounds.depth) + 4);
    const gridDivisions = Math.max(12, Math.ceil(gridSize * 2));
    const gridHelper = new THREE.GridHelper(gridSize, gridDivisions, '#8b5cf6', '#1e293b');
    gridHelper.position.y = 0.001;
    scene.add(gridHelper);

    wallMaterialsRef.current = Object.entries(normalizedWallColors).reduce((materials, [key, hex]) => {
      materials[key] = new THREE.MeshStandardMaterial({
        color: new THREE.Color(hex),
        roughness: 0.7,
        metalness: 0.1,
        transparent: true,
        opacity: 0.72,
      });
      return materials;
    }, {});

    const floorMaterials = Object.entries(SHELL_FLOOR_COLORS).reduce((materials, [key, hex]) => {
      materials[key] = new THREE.MeshStandardMaterial({
        color: new THREE.Color(hex),
        roughness: key === 'crosswalk' ? 0.38 : 0.56,
        metalness: key === 'road' ? 0.12 : 0.08,
      });
      return materials;
    }, {});

    layoutPlan.floors.forEach((floorSpace) => {
      addFloorSpace(scene, floorMaterials, floorSpace, layoutPlan.dimensions.wallThickness);
    });
    layoutPlan.walls.forEach((wallSegment) => {
      addWallSegment(
        scene,
        wallMaterialsRef.current[wallSegment.materialKey] || wallMaterialsRef.current.interior,
        wallSegment
      );
    });

    scene.add(new THREE.AmbientLight('#ffffff', 1.05));

    const dirLight = new THREE.DirectionalLight('#ffffff', 1.2);
    dirLight.position.set(
      layoutPlan.bounds.centerX + 4,
      6,
      layoutPlan.bounds.centerZ + 4
    );
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 1024;
    dirLight.shadow.mapSize.height = 1024;
    dirLight.shadow.camera.near = 0.5;
    dirLight.shadow.camera.far = 15;
    const d = 3;
    dirLight.shadow.camera.left = -d;
    dirLight.shadow.camera.right = d;
    dirLight.shadow.camera.top = d;
    dirLight.shadow.camera.bottom = -d;
    dirLight.shadow.bias = -0.0005;
    scene.add(dirLight);

    const fillLight = new THREE.DirectionalLight('#cbd5e1', 0.55);
    fillLight.position.set(
      layoutPlan.bounds.centerX - 4,
      3,
      layoutPlan.bounds.centerZ - 4
    );
    scene.add(fillLight);
    frameLayoutBounds(layoutPlan);

    const raycaster = new THREE.Raycaster();
    let startX = 0;
    let startY = 0;

    const handlePointerDown = (event) => {
      startX = event.clientX;
      startY = event.clientY;
    };

    const handlePointerUp = (event) => {
      const diffX = Math.abs(event.clientX - startX);
      const diffY = Math.abs(event.clientY - startY);
      if (diffX > 5 || diffY > 5) return;

      const rect = renderer.domElement.getBoundingClientRect();
      const mouse = new THREE.Vector2(
        ((event.clientX - rect.left) / rect.width) * 2 - 1,
        -((event.clientY - rect.top) / rect.height) * 2 + 1
      );

      raycaster.setFromCamera(mouse, camera);

      const targets = [];
      Object.values(loadedObjectsRef.current).forEach((obj) => {
        if (obj && scene.children.includes(obj)) {
          obj.traverse((child) => {
            if (child.isMesh) {
              targets.push(child);
            }
          });
        }
      });

      const intersects = raycaster.intersectObjects(targets);
      if (intersects.length > 0) {
        let current = intersects[0].object;
        while (current && current.parent) {
          if (current.userData?.assetId) {
            onSelectAsset(current.userData.assetId);
            return;
          }
          current = current.parent;
        }
      } else {
        onSelectAsset(null);
      }
    };

    renderer.domElement.addEventListener('pointerdown', handlePointerDown);
    renderer.domElement.addEventListener('pointerup', handlePointerUp);

    const resizeRenderer = () => {
      if (!rendererRef.current) return;
      const width = mountEl.clientWidth;
      const height = mountEl.clientHeight;
      if (!width || !height) return;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      rendererRef.current.setSize(width, height, false);
      renderScene();
    };

    resizeRenderer();

    const resizeObserver = new ResizeObserver(resizeRenderer);
    resizeObserver.observe(mountEl);
    window.addEventListener('resize', resizeRenderer);

    return () => {
      resizeObserver.disconnect();
      window.removeEventListener('resize', resizeRenderer);
      controls.removeEventListener('change', renderScene);
      renderer.domElement.removeEventListener('pointerdown', handlePointerDown);
      renderer.domElement.removeEventListener('pointerup', handlePointerUp);
      if (mountEl.contains(renderer.domElement)) {
        mountEl.removeChild(renderer.domElement);
      }
      mountEl.replaceChildren();
      sceneRef.current = null;
      cameraRef.current = null;
      rendererRef.current = null;
      controlsRef.current = null;
      wallMaterialsRef.current = {};
      renderSceneRef.current = () => {};
      controls.dispose();
      renderer.dispose();
    };
  }, [layoutMode, houseConfig, onSelectAsset]);

  useEffect(() => {
    const normalizedWallColors = normalizeWallColors(wallColors);
    Object.entries(normalizedWallColors).forEach(([key, hex]) => {
      if (wallMaterialsRef.current[key]) {
        wallMaterialsRef.current[key].color.set(hex);
      }
    });
    if (Object.keys(wallMaterialsRef.current).length > 0) {
      renderSceneRef.current();
    }
  }, [wallColors]);

  useEffect(() => {
    const scene = sceneRef.current;
    if (!scene) return;

    if (boxHelperRef.current) {
      scene.remove(boxHelperRef.current);
      boxHelperRef.current = null;
    }

    if (selectedAssetId) {
      const selectedObj = loadedObjectsRef.current[selectedAssetId];
      if (selectedObj && scene.children.includes(selectedObj)) {
        const helper = new THREE.BoxHelper(selectedObj, '#a78bfa');
        scene.add(helper);
        boxHelperRef.current = helper;
      }
    }

    renderSceneRef.current();
  }, [selectedAssetId, activeAssets]);

  useEffect(() => {
    const scene = sceneRef.current;
    if (!scene) return;

    const loader = new GLTFLoader();
    const activeAssetDetails = assets.filter((asset) => activeAssets.includes(asset.id));
    const placementMap = buildLayoutPlacements(activeAssetDetails, layoutMode, houseConfig);

    activeAssetDetails.forEach((asset) => {
      const modelId = asset.id;
      const cached = loadedObjectsRef.current[modelId];
      const placement = placementMap[modelId];

      if (!placement) {
        return;
      }

      if (cached) {
        const currentScene = sceneRef.current;
        if (!currentScene) return;
        const normalizeScale = cached.userData?.normalizeScale ?? 1;
        const finalScale = placement.scale * normalizeScale;
        cached.position.set(...placement.pos);
        cached.rotation.set(...placement.rot);
        cached.scale.set(finalScale, finalScale, finalScale);
        applyObjectColorOverrides(
          cached,
          transforms?.[modelId]?.customColor || asset.parameters?.custom_color,
          transforms?.[modelId]?.detailColors
        );
        if (!currentScene.children.includes(cached)) {
          currentScene.add(cached);
        }
        onAssetMetadataChange?.(
          modelId,
          cached.userData?.materialMetadata || { materialRoles: [], hasUnmappedPrimaryMaterials: true }
        );
        frameVisibleAssets();
        renderSceneRef.current();
        return;
      }

      if (loadingIdsRef.current.has(modelId) || !asset.glb_path) {
        return;
      }

      loadingIdsRef.current.add(modelId);
      setLoadingProgress((prev) => ({ ...prev, [modelId]: 0 }));

      loader.load(
        `${API_BASE_URL}${asset.glb_path}`,
        (gltf) => {
          loadingIdsRef.current.delete(modelId);

          const sourceScene = gltf.scene;
          sourceScene.traverse((child) => {
            if (child.isMesh) {
              child.castShadow = true;
              child.receiveShadow = true;
            }
          });

          const box = new THREE.Box3().setFromObject(sourceScene);
          const size = new THREE.Vector3();
          box.getSize(size);
          const maxDim = Math.max(size.x, size.y, size.z);

          let normalizeScale = 1;
          if (maxDim > 0.001) {
            normalizeScale = 1.0 / maxDim;
          }

          const finalScale = placement.scale * normalizeScale;
          const assetRoot = new THREE.Group();

          if (!box.isEmpty()) {
            const center = box.getCenter(new THREE.Vector3());
            sourceScene.position.set(-center.x, -box.min.y, -center.z);
          }

          assetRoot.add(sourceScene);
          assetRoot.position.set(...placement.pos);
          assetRoot.rotation.set(...placement.rot);
          assetRoot.scale.set(finalScale, finalScale, finalScale);
          assetRoot.userData = { assetId: modelId, normalizeScale };

          captureOriginalMaterialColors(assetRoot);
          const materialMetadata = collectMaterialMetadata(assetRoot);
          assetRoot.userData.materialMetadata = materialMetadata;

          applyObjectColorOverrides(
            assetRoot,
            transforms?.[modelId]?.customColor || asset.parameters?.custom_color,
            transforms?.[modelId]?.detailColors
          );

          loadedObjectsRef.current[modelId] = assetRoot;
          onAssetMetadataChange?.(modelId, materialMetadata);

          const currentScene = sceneRef.current;
          if (currentScene && activeAssetsRef.current.includes(modelId)) {
            currentScene.add(assetRoot);
            frameVisibleAssets();
            renderSceneRef.current();
          }

          setLoadingProgress((prev) => {
            const updated = { ...prev };
            delete updated[modelId];
            return updated;
          });
        },
        (progress) => {
          if (progress.total > 0) {
            const pct = Math.round((progress.loaded / progress.total) * 100);
            setLoadingProgress((prev) => ({ ...prev, [modelId]: pct }));
          }
        },
        (error) => {
          loadingIdsRef.current.delete(modelId);
          console.error(`Error loading model for asset ${modelId}:`, error);
          setLoadingProgress((prev) => {
            const updated = { ...prev };
            delete updated[modelId];
            return updated;
          });
        }
      );
    });

    Object.keys(loadedObjectsRef.current).forEach((idKey) => {
      const id = parseInt(idKey, 10);
      if (!activeAssets.includes(id)) {
        const obj = loadedObjectsRef.current[id];
        if (obj && scene.children.includes(obj)) {
          scene.remove(obj);
        }
      }
    });

    frameVisibleAssets();
    renderSceneRef.current();
  }, [activeAssets, assets, layoutMode, houseConfig]);

  useEffect(() => {
    if (!transforms) return;
    const activeAssetDetails = assets.filter((asset) => activeAssets.includes(asset.id));
    const placementMap = buildLayoutPlacements(activeAssetDetails, layoutMode, houseConfig);

    Object.keys(loadedObjectsRef.current).forEach((idKey) => {
      const id = parseInt(idKey, 10);
      const obj = loadedObjectsRef.current[id];
      if (!obj) return;

      const basePlacement = placementMap[id];
      const override = transforms[id];
      const asset = assets.find((entry) => entry.id === id);
      if (!asset || !basePlacement) return;
      const posX = basePlacement.pos[0] + (override?.posX || 0);
      const posY = basePlacement.pos[1] + (override?.posY || 0);
      const posZ = basePlacement.pos[2] + (override?.posZ || 0);
      obj.position.set(posX, posY, posZ);

      const rotY = basePlacement.rot[1] + ((override?.rotY || 0) * Math.PI) / 180;
      obj.rotation.set(basePlacement.rot[0], rotY, basePlacement.rot[2]);

      const scaleFactor = override?.scale ?? 1;
      const normalizeScale = obj.userData?.normalizeScale ?? 1;
      const finalScale = basePlacement.scale * normalizeScale * scaleFactor;
      obj.scale.set(finalScale, finalScale, finalScale);

      applyObjectColorOverrides(
        obj,
        override?.customColor || asset.parameters?.custom_color,
        override?.detailColors
      );
    });

    renderSceneRef.current();
  }, [transforms, activeAssets, assets, layoutMode, houseConfig]);

  const loadingCount = Object.keys(loadingProgress).length;

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <div ref={containerRef} style={{ width: '100%', height: '100%' }} />

      {loadingCount > 0 && (
        <div
          style={{
            position: 'absolute',
            bottom: '20px',
            left: '20px',
            backgroundColor: 'rgba(14, 17, 23, 0.95)',
            border: '1px solid var(--border-light)',
            padding: '10px 16px',
            borderRadius: '10px',
            color: 'white',
            fontSize: '12px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            boxShadow: 'var(--shadow-lg)',
            zIndex: 10,
          }}
        >
          <div className="pulse-dot"></div>
          <span>
            Loading {loadingCount} model{loadingCount > 1 ? 's' : ''}...
          </span>
        </div>
      )}
    </div>
  );
}
