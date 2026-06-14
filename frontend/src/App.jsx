import React, { useState, useEffect, useRef } from 'react';
import RoomViewer from './RoomViewer';
import GameAssetStudio from './GameAssetStudio';
import MovieProductionPanel from './MovieProductionPanel';
import {
  buildLayoutPlan,
  DEFAULT_HOUSE_CONFIG,
  DEFAULT_WALL_COLORS,
  getEffectiveLayoutMode,
  getLayoutPresetAssetIds,
} from './roomLayoutUtils';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

// Custom inline SVG icons for zero external dependencies
const SparklesIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275Z"/>
    <path d="m5 3 1 2.5L8.5 6 6 7 5 9.5 4 7 1.5 6 4 5.5Z"/>
    <path d="m19 17 1 2.5 2.5.5-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1Z"/>
  </svg>
);

const SwordIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="14.5 17.5 3 6 3 3 6 3 17.5 14.5" />
    <line x1="13" y1="19" x2="19" y2="13" />
    <line x1="16" y1="16" x2="20" y2="20" />
    <line x1="19" y1="21" x2="21" y2="19" />
    <line x1="14.5" y1="14.5" x2="18.5" y2="10.5" />
    <line x1="10.5" y1="18.5" x2="14.5" y2="14.5" />
  </svg>
);

const TableIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="6" width="20" height="4" rx="1"/>
    <line x1="6" y1="10" x2="6" y2="20"/>
    <line x1="18" y1="10" x2="18" y2="20"/>
  </svg>
);

const DiningTableIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="1" y="7" width="22" height="4" rx="1"/>
    <line x1="4" y1="11" x2="4" y2="20"/>
    <line x1="20" y1="11" x2="20" y2="20"/>
    <line x1="7" y1="4" x2="7" y2="7"/>
    <line x1="17" y1="4" x2="17" y2="7"/>
    <line x1="12" y1="4" x2="12" y2="7"/>
  </svg>
);

const CoffeeTableIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="9" width="20" height="5" rx="2"/>
    <line x1="5" y1="14" x2="5" y2="19"/>
    <line x1="19" y1="14" x2="19" y2="19"/>
  </svg>
);

const BarrelIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M5 3h14M5 21h14M2 9h20M2 15h20M4 3c-1 3-1 15 0 18M20 3c1 3 1 15 0 18" />
  </svg>
);

const CrateIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
    <line x1="3" y1="3" x2="21" y2="21" />
    <line x1="21" y1="3" x2="3" y2="21" />
  </svg>
);

const ShieldIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
  </svg>
);

const ChairIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M7 18V5h10v13M5 12h14M7 12v6M17 12v6" />
  </svg>
);

const BenchIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M2 10h20M2 14h20M6 14v6M18 14v6M3 10V6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4"/>
  </svg>
);

const CouchIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 14V8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6M2 14h20v4a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2zM6 10h12M12 6v4"/>
  </svg>
);

const ArmchairIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M5 14V8a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v6M4 14h16v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zM6 10h12"/>
  </svg>
);

const BedIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M2 4v16M2 8h20M2 17h20M22 4v16M6 8v9M18 8v9"/>
  </svg>
);

const BunkBedIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M2 2v20M22 2v20M2 7h20M2 15h20M6 7v8M18 7v8M12 2v20M12 11h4M12 18h4"/>
  </svg>
);

const WardrobeIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="2" width="18" height="20" rx="2" ry="2" />
    <line x1="12" y1="2" x2="12" y2="22" />
    <circle cx="9" cy="12" r="1" />
    <circle cx="15" cy="12" r="1" />
  </svg>
);

const ClosetIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="2" width="18" height="20" rx="2" ry="2" />
    <line x1="9" y1="2" x2="9" y2="22" />
    <line x1="15" y1="2" x2="15" y2="22" />
    <path d="M6 12h2M16 12h2" />
  </svg>
);

const DresserIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="6" width="18" height="14" rx="2" ry="2" />
    <line x1="3" y1="11" x2="21" y2="11" />
    <line x1="3" y1="16" x2="21" y2="16" />
    <line x1="12" y1="6" x2="12" y2="20" />
    <circle cx="7.5" cy="8.5" r="1" />
    <circle cx="16.5" cy="8.5" r="1" />
    <circle cx="7.5" cy="13.5" r="1" />
    <circle cx="16.5" cy="13.5" r="1" />
    <circle cx="7.5" cy="18" r="1" />
    <circle cx="16.5" cy="18" r="1" />
  </svg>
);

const CabinetIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="4" y="3" width="16" height="18" rx="2" ry="2" />
    <line x1="4" y1="10" x2="20" y2="10" />
    <line x1="12" y1="3" x2="12" y2="21" />
    <circle cx="9" cy="12" r="1" />
    <circle cx="15" cy="12" r="1" />
  </svg>
);

const DeskIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="6" width="20" height="3" rx="1"/>
    <line x1="5" y1="9" x2="5" y2="20"/>
    <line x1="19" y1="9" x2="19" y2="20"/>
    <rect x="13" y="9" width="6" height="8" rx="1"/>
  </svg>
);

const StoolIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <ellipse cx="12" cy="7" rx="8" ry="3"/>
    <line x1="6" y1="10" x2="4" y2="20"/>
    <line x1="18" y1="10" x2="20" y2="20"/>
    <line x1="12" y1="10" x2="12" y2="20"/>
    <path d="M5 16h14"/>
  </svg>
);

const ChestIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
    <path d="M2 12h20M10 7V4c0-.5.5-1 1-1h2c.5 0 1 .5 1 1v3M10 12v3h4v-3" />
  </svg>
);

const AxeIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="m14 12-8.5 8.5a2.12 2.12 0 1 1-3-3L11 9" />
    <path d="M15 3v4a2 2 0 0 0 2 2h4" />
    <path d="M11 9c2-2 5-3 8-3v6c-3 0-6-1-8-3Z" />
  </svg>
);

const HammerIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M6 21 17 10" />
    <path d="M13 4h7v5h-3l-2 2-4-4 2-2Z" />
    <path d="M5 19 3 21" />
  </svg>
);

const BowIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M6 3c8 4 8 14 0 18" />
    <path d="M18 3c-8 4-8 14 0 18" opacity="0.15" />
    <line x1="17" y1="4" x2="17" y2="20" />
    <line x1="8" y1="8" x2="14" y2="12" />
  </svg>
);

const StaffIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="3" x2="12" y2="21" />
    <circle cx="12" cy="4.5" r="2.5" />
    <path d="M9.5 10h5" />
  </svg>
);

const OrbIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="9" r="5" />
    <path d="M8 18h8" />
    <path d="M10 14v4M14 14v4" />
  </svg>
);

const VehicleIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M5 16h14l-1-6H6l-1 6Z" />
    <path d="M7 10l2-3h6l2 3" />
    <circle cx="8" cy="18" r="2" />
    <circle cx="16" cy="18" r="2" />
  </svg>
);

const BoatIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 15h18l-2 4H5l-2-4Z" />
    <path d="M12 4v11" />
    <path d="M12 5l5 3-5 3Z" />
  </svg>
);

const PlaneAssetIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M2 12h20" />
    <path d="M10 12 6 5" />
    <path d="M14 12l4-7" />
    <path d="M12 12v8" />
  </svg>
);

const CharacterIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="6" r="3" />
    <path d="M12 9v6M7 21l2-6 3-2 3 2 2 6M8 13l-3 3M16 13l3 3" />
  </svg>
);

const AnimalIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="8" cy="7" r="2" />
    <circle cx="16" cy="7" r="2" />
    <circle cx="6" cy="12" r="2" />
    <circle cx="18" cy="12" r="2" />
    <path d="M8 18c1.5-1.5 6.5-1.5 8 0" />
  </svg>
);

const GemIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M7 4h10l4 5-9 11L3 9l4-5Z" />
    <path d="M9 4l3 16 3-16" />
  </svg>
);

const KeyAssetIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="8" cy="15" r="4" />
    <path d="M12 15h9M17 15v-3M20 15v-2" />
  </svg>
);

const TerrainIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 18h18" />
    <path d="m4 18 5-8 4 5 3-4 4 7" />
  </svg>
);

const HelmetIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M2 11c0-5 4-9 10-9s10 4 10 9v3a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-3z" />
    <path d="M8 11h8v4a4 4 0 0 1-8 0v-4z" />
    <path d="M12 2v3M12 11v4" />
  </svg>
);

const TorchIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 6c0 3-4 6-6 10-2-4-6-7-6-10a6 6 0 0 1 12 0Z" />
    <path d="M9 16h6v4a2 2 0 0 1-2 2h-2a2 2 0 0 1-2-2v-4Z" />
    <path d="M12 2v2M8 4l1.5 1.5M16 4l-1.5 1.5" />
  </svg>
);

const ShelfIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 10h18M5 10v4l4-4M19 10v4l-4-4" />
  </svg>
);

const BookcaseIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="4" y="2" width="16" height="20" rx="1" />
    <line x1="4" y1="7" x2="20" y2="7" />
    <line x1="4" y1="12" x2="20" y2="12" />
    <line x1="4" y1="17" x2="20" y2="17" />
  </svg>
);

const NightstandIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="4" y="6" width="16" height="12" rx="1" />
    <line x1="4" y1="12" x2="20" y2="12" />
    <circle cx="12" cy="9" r="0.75" />
    <circle cx="12" cy="15" r="0.75" />
    <line x1="7" y1="18" x2="5" y2="21" />
    <line x1="17" y1="18" x2="19" y2="21" />
  </svg>
);

const TVStandIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="8" width="20" height="9" rx="1" />
    <line x1="8" y1="8" x2="8" y2="17" />
    <line x1="16" y1="8" x2="16" y2="17" />
    <circle cx="5" cy="12.5" r="0.75" />
    <circle cx="19" cy="12.5" r="0.75" />
    <line x1="5" y1="17" x2="4" y2="20" />
    <line x1="19" y1="17" x2="20" y2="20" />
  </svg>
);

const FridgeIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="5" y="2" width="14" height="20" rx="2" ry="2" />
    <line x1="5" y1="9" x2="19" y2="9" />
    <line x1="9" y1="4" x2="9" y2="7" />
    <line x1="9" y1="11" x2="9" y2="16" />
  </svg>
);

const StoveIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="4" y="6" width="16" height="14" rx="2" ry="2" />
    <ellipse cx="9" cy="4" rx="3" ry="1.5" />
    <ellipse cx="15" cy="4" rx="3" ry="1.5" />
    <circle cx="8" cy="9" r="1" />
    <circle cx="12" cy="9" r="1" />
    <circle cx="16" cy="9" r="1" />
    <rect x="7" y="12" width="10" height="6" rx="1" />
  </svg>
);

const OvenIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
    <rect x="6" y="8" width="12" height="9" rx="1" ry="1" />
    <line x1="8" y1="10" x2="16" y2="10" />
    <circle cx="7" cy="5.5" r="1" />
    <circle cx="17" cy="5.5" r="1" />
    <rect x="10" y="4.5" width="4" height="2" rx="0.5" />
  </svg>
);

const MicrowaveIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="4" width="18" height="15" rx="2" ry="2" />
    <rect x="6" y="7" width="9" height="9" rx="1" ry="1" />
    <line x1="18" y1="8" x2="19" y2="8" />
    <line x1="18" y1="11" x2="19" y2="11" />
    <line x1="18" y1="14" x2="19" y2="14" />
  </svg>
);

const SinkIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="10" width="18" height="12" rx="2" ry="2" />
    <line x1="3" y1="13" x2="21" y2="13" />
    <path d="M6 13v4a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-4" />
    <path d="M12 10V6a2 2 0 0 1 2-2h1V5" />
  </svg>
);

const CountertopIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="5" width="20" height="3" rx="0.5" />
    <rect x="2" y="2" width="20" height="3" rx="0.5" />
    <rect x="3" y="8" width="18" height="13" rx="1" />
    <line x1="12" y1="8" x2="12" y2="21" />
    <line x1="3" y1="14" x2="21" y2="14" />
    <circle cx="7.5" cy="11" r="0.75" />
    <circle cx="16.5" cy="11" r="0.75" />
    <circle cx="7.5" cy="17.5" r="0.75" />
    <circle cx="16.5" cy="17.5" r="0.75" />
  </svg>
);

const ToiletIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="5" y="3" width="14" height="6" rx="1" />
    <ellipse cx="12" cy="14" rx="6" ry="5" />
    <path d="M7 14v2c0 3 2.5 5 5 5s5-2 5-5v-2" />
  </svg>
);

const BathtubIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M2 9h20M2 9c0 5 3 9 10 9s10-4 10-9M4 9v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9" />
    <line x1="6" y1="18" x2="5" y2="21" />
    <line x1="18" y1="18" x2="19" y2="21" />
    <path d="M19 5h-2v4" />
  </svg>
);

const ShowerIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M7 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2" />
    <path d="M16 7h3v1M17.5 8v2" />
    <line x1="16" y1="13" x2="16.01" y2="13" />
    <line x1="17.5" y1="13" x2="17.51" y2="13" />
    <line x1="19" y1="13" x2="19.01" y2="13" />
    <line x1="16" y1="16" x2="16.01" y2="16" />
    <line x1="17.5" y1="16" x2="17.51" y2="16" />
    <line x1="19" y1="16" x2="19.01" y2="16" />
    <rect x="5" y="20" width="14" height="2" rx="0.5" />
  </svg>
);

const MirrorIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <ellipse cx="12" cy="12" rx="7" ry="9" />
    <path d="M7.5 9.5a5.5 5.5 0 0 1 9 0" />
  </svg>
);

const TowelRackIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="5" width="20" height="3" rx="1" />
    <path d="M4 8v10a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V8" />
    <line x1="8" y1="12" x2="16" y2="12" />
  </svg>
);

const LampIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M8 3h8l2 6H6Z" />
    <line x1="12" y1="9" x2="12" y2="20" />
    <path d="M9 20h6" />
  </svg>
);

const ChandelierIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="2" x2="12" y2="8" />
    <path d="M5 10c0 3 3 5 7 5s7-2 7-5" />
    <line x1="12" y1="8" x2="12" y2="15" />
    <circle cx="5" cy="8" r="1" fill="currentColor" />
    <circle cx="12" cy="6" r="1" fill="currentColor" />
    <circle cx="19" cy="8" r="1" fill="currentColor" />
    <path d="M12 15l-2 3 2 3 2-3Z" />
  </svg>
);

const PaintingIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
    <path d="m3 16 5-5 6 6" />
    <path d="m12 13 3-3 6 6" />
    <circle cx="17" cy="8" r="1.5" />
  </svg>
);

const PictureFrameIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="1" />
    <rect x="6" y="6" width="12" height="12" rx="0.5" />
    <circle cx="12" cy="10" r="2" />
    <path d="M8 16c0-2 2-3 4-3s4 1 4 3" />
  </svg>
);

const TrashIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2M10 11v6M14 11v6" />
  </svg>
);

const DownloadIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" />
  </svg>
);

const ClockIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" />
    <polyline points="12 6 12 12 16 14" />
  </svg>
);

const VaseIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M8 2h8M9 2v4a3 3 0 0 1-1 2.24C6.4 9.6 5 11.63 5 14a7 7 0 0 0 14 0c0-2.37-1.4-4.4-3-5.76A3 3 0 0 1 15 6V2" />
  </svg>
);

const PlantIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M6 15h12l-1.5 6h-9z" />
    <path d="M5 12h14v3H5z" />
    <path d="M12 12V3M12 6c1.5-1.5 3.5-2 5-2s2 .5 2 2-1 3.5-2 5M12 8c-1.5-1.5-3.5-2-5-2s-2 .5-2 2 1 3.5 2 5" />
  </svg>
);

const TreeIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 3 6 11h3l-3 5h4l-2 5h8l-2-5h4l-3-5h3z" />
    <path d="M12 14v7" />
  </svg>
);

const RockIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M5 18 3 11l5-6h8l5 5-1 8H5Z" />
    <path d="M8 7h6l3 3" />
  </svg>
);

const WaterIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 16c2 2 4 2 6 0s4-2 6 0 4 2 6 0" />
    <path d="M3 11c2 2 4 2 6 0s4-2 6 0 4 2 6 0" />
    <path d="M3 6c2 2 4 2 6 0s4-2 6 0 4 2 6 0" />
  </svg>
);

const MushroomIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 11a8 8 0 0 1 16 0Z" />
    <path d="M10 11v6a2 2 0 0 0 4 0v-6" />
    <path d="M9 20h6" />
  </svg>
);

const RugIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="5" width="20" height="14" rx="2" />
    <line x1="2" y1="3" x2="2" y2="5" />
    <line x1="5" y1="3" x2="5" y2="5" />
    <line x1="8" y1="3" x2="8" y2="5" />
    <line x1="11" y1="3" x2="11" y2="5" />
    <line x1="14" y1="3" x2="14" y2="5" />
    <line x1="17" y1="3" x2="17" y2="5" />
    <line x1="20" y1="3" x2="20" y2="5" />
    <line x1="2" y1="19" x2="2" y2="21" />
    <line x1="5" y1="19" x2="5" y2="21" />
    <line x1="8" y1="19" x2="8" y2="21" />
    <line x1="11" y1="19" x2="11" y2="21" />
    <line x1="14" y1="19" x2="14" y2="21" />
    <line x1="17" y1="19" x2="17" y2="21" />
    <line x1="20" y1="19" x2="20" y2="21" />
    <rect x="6" y="9" width="12" height="6" rx="1" strokeDasharray="2" />
  </svg>
);

const WallIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="4" width="18" height="16" rx="1" />
    <path d="M9 4v16M15 4v16M3 10h18" />
  </svg>
);

const FloorIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 16 12 5l9 11-9 3Z" />
    <path d="M12 5v14M7.5 10.5l9 2.5" />
  </svg>
);

const CeilingIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 8 12 3l9 5-9 5Z" />
    <path d="M3 8v5l9 5 9-5V8" />
  </svg>
);

const RoofIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 13 12 4l9 9" />
    <path d="M5 13h14M7 13l2 7h6l2-7" />
  </svg>
);

const PillarIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M5 4h14M7 7h10M8 7v10M16 7v10M7 17h10M5 20h14" />
  </svg>
);

const BeamIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="8" width="20" height="8" rx="1" />
    <path d="M6 8v8M12 8v8M18 8v8" />
  </svg>
);

const FoundationIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 19h18" />
    <rect x="4" y="11" width="16" height="5" rx="1" />
    <path d="M7 16v3M12 16v3M17 16v3" />
  </svg>
);

const DoorAssetIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M5 3h12v18H5Z" />
    <path d="M17 3h2a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1h-2" />
    <circle cx="13" cy="12" r="1" />
  </svg>
);

const WindowAssetIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="4" y="4" width="16" height="16" rx="1" />
    <path d="M12 4v16M4 12h16" />
  </svg>
);

const ArchwayIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 20V10a8 8 0 0 1 16 0v10" />
    <path d="M8 20V11a4 4 0 0 1 8 0v9" />
  </svg>
);

const GateIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 20V5M21 20V5" />
    <rect x="5" y="7" width="14" height="11" rx="1" />
    <path d="M9 7v11M12 7v11M15 7v11" />
  </svg>
);

const StairsIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 20h16" />
    <path d="M6 20v-4h4v-4h4V8h4V4" />
  </svg>
);

const LadderIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M7 3v18M17 3v18" />
    <path d="M7 7h10M7 11h10M7 15h10M7 19h10" />
  </svg>
);

const RampIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 20h16" />
    <path d="M4 20 18 8h2v12" />
  </svg>
);

const BridgeIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 15h18" />
    <path d="M5 15V9M19 15V9M8 15v-3M16 15v-3" />
    <path d="M5 9c2-2 4-3 7-3s5 1 7 3" />
  </svg>
);

const BalconyIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 8h18" />
    <path d="M5 8v10M19 8v10M8 8v10M12 8v10M16 8v10" />
    <path d="M3 18h18" />
  </svg>
);

const FenceIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 18h18" />
    <path d="M5 18V6l2 2 2-2v12M11 18V5l2 2 2-2v13M17 18V6l2 2 2-2v12" />
  </svg>
);

const RailingIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 7h18" />
    <path d="M5 7v11M9 7v11M13 7v11M17 7v11M21 7v11" />
    <path d="M3 18h18" />
  </svg>
);

const ChimneyIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M8 20V7h8v13" />
    <path d="M6 7h12M7 4h10" />
    <path d="M10 10h1M13 13h1M11 16h1" />
  </svg>
);

const PorchIcon = ({ className = "" }) => (
  <svg className={className} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 10h16" />
    <path d="M6 10v9M18 10v9" />
    <path d="M3 19h18" />
    <path d="M12 5 4 10M12 5l8 5" />
  </svg>
);

const WarningIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" />
    <line x1="12" y1="9" x2="12" y2="13" />
    <line x1="12" y1="17" x2="12.01" y2="17" />
  </svg>
);

const CITY_GRID_SIZE = 20;
const CITY_LIGHT_MIN = 1;
const CITY_LIGHT_MAX = 50;
const CITY_CELL_SIZE_METERS = 4;

const CITY_TOOL_GROUPS = [
  {
    title: 'Roads',
    description: '3D street blocks.',
    tools: [
      { id: 'road_straight', label: 'Straight E-W' },
      { id: 'road_vertical', label: 'Straight N-S' },
      { id: 'road_intersection', label: 'Intersection' },
      { id: 'road_curve', label: 'Curve / Turn' },
    ],
  },
  {
    title: 'Buildings',
    description: 'Place 3D structures.',
    tools: [
      { id: 'building_house', label: 'Residential House' },
      { id: 'building_apartment', label: 'Apartment Block' },
      { id: 'building_office', label: 'Office Tower' },
      { id: 'building_shop', label: 'Shop' },
    ],
  },
  {
    title: 'Street Lights',
    description: 'Real light assets.',
    tools: [
      { id: 'light_classic', label: 'Classic Pole' },
      { id: 'light_modern', label: 'Modern LED' },
    ],
  },
  {
    title: 'Edit',
    description: 'Clean up cells.',
    tools: [
      { id: 'erase', label: 'Erase Cell' },
    ],
  },
];

const CITY_TOOL_LABELS = CITY_TOOL_GROUPS.reduce((labels, group) => {
  group.tools.forEach((tool) => {
    labels[tool.id] = tool.label;
  });
  return labels;
}, {});

const CITY_BUILDING_META = {
  house: {
    label: 'Residential House',
    floors: 2,
    height: 2.5,
    color: '#f8fafc',
    roof: '#dc2626',
    accent: '#78350f',
    description: 'Two-floor house with gabled roof, door, windows, and chimney.',
  },
  apartment: {
    label: 'Apartment Block',
    floors: 6,
    height: 5.6,
    color: '#64748b',
    roof: '#334155',
    accent: '#bae6fd',
    description: 'Stacked residential block with window rows and balconies.',
  },
  office: {
    label: 'Office Tower',
    floors: 10,
    height: 8.6,
    color: '#0f766e',
    roof: '#083344',
    accent: '#67e8f9',
    description: 'Tall glass office tower with panel bands and rooftop antenna.',
  },
  shop: {
    label: 'Shop',
    floors: 1,
    height: 1.7,
    color: '#92400e',
    roof: '#ef4444',
    accent: '#facc15',
    description: 'Street shop with awning, sign, display window, and glass door.',
  },
};

const CITY_ROAD_META = {
  straight: { label: 'Straight E-W', description: 'East-west asphalt road with lane stripe.' },
  vertical: { label: 'Straight N-S', description: 'North-south asphalt road with lane stripe.' },
  intersection: { label: 'Intersection', description: 'Four-way road crossing with crosswalk marks.' },
  curve: { label: 'Curve / Turn', description: 'Corner road tile for turning streets.' },
};

const CITY_LIGHT_META = {
  classic: {
    label: 'Classic Pole',
    color: '#fef3c7',
    description: 'Decorative warm lamp pole with actual Blender point light.',
  },
  modern: {
    label: 'Modern LED',
    color: '#67e8f9',
    description: 'Modern cool LED pole with actual Blender area light.',
  },
};

const createEmptyCityCell = () => ({
  road: null,
  building: null,
  light: null,
  elevation: 0,
  rotation: 0,
  heightScale: 1,
});

const createEmptyCityGrid = () =>
  Array.from({ length: CITY_GRID_SIZE }, () =>
    Array.from({ length: CITY_GRID_SIZE }, createEmptyCityCell)
  );

const clampCityLightCount = (value) => {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed)) return 1;
  return Math.max(CITY_LIGHT_MIN, Math.min(CITY_LIGHT_MAX, parsed));
};

const getCityToolKind = (toolId) => {
  if (!toolId) return null;
  if (toolId === 'erase') return 'erase';
  return toolId.split('_')[0];
};

const getCityToolVariant = (toolId) => {
  const kind = getCityToolKind(toolId);
  if (!kind || kind === 'erase') return null;
  return toolId.replace(`${kind}_`, '');
};

const getCityRoadCells = (grid) => {
  const cells = [];
  grid.forEach((row, rowIndex) => {
    row.forEach((cell, colIndex) => {
      if (cell.road) {
        cells.push({ row: rowIndex, col: colIndex });
      }
    });
  });
  return cells;
};

const pickEvenlySpacedCells = (cells, requestedCount) => {
  const count = Math.min(cells.length, clampCityLightCount(requestedCount));
  if (count <= 0) return [];
  if (count === 1) {
    return [cells[Math.floor((cells.length - 1) / 2)]];
  }

  return Array.from({ length: count }, (_, index) => {
    const sourceIndex = Math.round((index * (cells.length - 1)) / (count - 1));
    return cells[sourceIndex];
  });
};

const getCityGridStats = (grid) => {
  let roads = 0;
  let buildings = 0;
  let lights = 0;

  grid.forEach((row) => {
    row.forEach((cell) => {
      if (cell.road) roads += 1;
      if (cell.building) buildings += 1;
      if (cell.light) lights += 1;
    });
  });

  return { roads, buildings, lights };
};

const renderRoadTile = (variant) => {
  const road = '#252d3a';
  const roadEdge = '#111827';
  const lane = '#facc15';
  const roadLine = '#e5e7eb';

  if (variant === 'vertical') {
    return (
      <>
        <rect x="18" y="0" width="28" height="64" fill={road} />
        <rect x="16" y="0" width="2" height="64" fill={roadEdge} opacity="0.55" />
        <rect x="46" y="0" width="2" height="64" fill={roadEdge} opacity="0.55" />
        <line x1="32" y1="7" x2="32" y2="57" stroke={lane} strokeWidth="3" strokeLinecap="round" strokeDasharray="7 7" />
        <line x1="22" y1="0" x2="22" y2="64" stroke={roadLine} strokeWidth="1.2" opacity="0.25" />
        <line x1="42" y1="0" x2="42" y2="64" stroke={roadLine} strokeWidth="1.2" opacity="0.25" />
      </>
    );
  }

  if (variant === 'intersection') {
    return (
      <>
        <rect x="18" y="0" width="28" height="64" fill={road} />
        <rect x="0" y="18" width="64" height="28" fill={road} />
        <rect x="18" y="18" width="28" height="28" fill="#2f3948" />
        <line x1="32" y1="4" x2="32" y2="18" stroke={lane} strokeWidth="3" strokeLinecap="round" strokeDasharray="6 6" />
        <line x1="32" y1="46" x2="32" y2="60" stroke={lane} strokeWidth="3" strokeLinecap="round" strokeDasharray="6 6" />
        <line x1="4" y1="32" x2="18" y2="32" stroke={lane} strokeWidth="3" strokeLinecap="round" strokeDasharray="6 6" />
        <line x1="46" y1="32" x2="60" y2="32" stroke={lane} strokeWidth="3" strokeLinecap="round" strokeDasharray="6 6" />
        <rect x="16" y="16" width="32" height="32" fill="none" stroke="#94a3b8" strokeWidth="1" opacity="0.22" />
      </>
    );
  }

  if (variant === 'curve') {
    return (
      <>
        <path d="M0 32H32V64" fill="none" stroke={roadEdge} strokeWidth="34" strokeLinecap="square" strokeLinejoin="miter" opacity="0.65" />
        <path d="M0 32H32V64" fill="none" stroke={road} strokeWidth="28" strokeLinecap="square" strokeLinejoin="miter" />
        <path d="M5 32H32V59" fill="none" stroke={lane} strokeWidth="3" strokeLinecap="round" strokeDasharray="7 7" />
        <path d="M0 18H46V64" fill="none" stroke={roadLine} strokeWidth="1.2" opacity="0.24" />
        <path d="M0 46H18V64" fill="none" stroke={roadLine} strokeWidth="1.2" opacity="0.24" />
      </>
    );
  }

  return (
    <>
      <rect x="0" y="18" width="64" height="28" fill={road} />
      <rect x="0" y="16" width="64" height="2" fill={roadEdge} opacity="0.55" />
      <rect x="0" y="46" width="64" height="2" fill={roadEdge} opacity="0.55" />
      <line x1="7" y1="32" x2="57" y2="32" stroke={lane} strokeWidth="3" strokeLinecap="round" strokeDasharray="7 7" />
      <line x1="0" y1="22" x2="64" y2="22" stroke={roadLine} strokeWidth="1.2" opacity="0.25" />
      <line x1="0" y1="42" x2="64" y2="42" stroke={roadLine} strokeWidth="1.2" opacity="0.25" />
    </>
  );
};

const renderBuildingTile = (variant) => {
  if (variant === 'apartment') {
    return (
      <>
        <rect x="12" y="8" width="40" height="48" rx="4" fill="#64748b" stroke="#cbd5e1" strokeWidth="1.5" />
        <rect x="17" y="14" width="7" height="7" rx="1" fill="#bae6fd" />
        <rect x="29" y="14" width="7" height="7" rx="1" fill="#dbeafe" />
        <rect x="41" y="14" width="7" height="7" rx="1" fill="#bae6fd" />
        <rect x="17" y="27" width="7" height="7" rx="1" fill="#dbeafe" />
        <rect x="29" y="27" width="7" height="7" rx="1" fill="#bae6fd" />
        <rect x="41" y="27" width="7" height="7" rx="1" fill="#dbeafe" />
        <rect x="17" y="40" width="7" height="7" rx="1" fill="#bae6fd" />
        <rect x="29" y="40" width="7" height="7" rx="1" fill="#dbeafe" />
        <rect x="40" y="40" width="8" height="16" rx="1" fill="#334155" />
      </>
    );
  }

  if (variant === 'office') {
    return (
      <>
        <rect x="10" y="6" width="44" height="52" rx="3" fill="#0f766e" stroke="#67e8f9" strokeWidth="1.5" />
        <rect x="16" y="12" width="32" height="40" rx="2" fill="#155e75" opacity="0.9" />
        <line x1="24" y1="12" x2="24" y2="52" stroke="#a5f3fc" strokeWidth="1.5" opacity="0.75" />
        <line x1="32" y1="12" x2="32" y2="52" stroke="#a5f3fc" strokeWidth="1.5" opacity="0.75" />
        <line x1="40" y1="12" x2="40" y2="52" stroke="#a5f3fc" strokeWidth="1.5" opacity="0.75" />
        <line x1="16" y1="24" x2="48" y2="24" stroke="#a5f3fc" strokeWidth="1.5" opacity="0.55" />
        <line x1="16" y1="36" x2="48" y2="36" stroke="#a5f3fc" strokeWidth="1.5" opacity="0.55" />
        <rect x="28" y="50" width="8" height="8" rx="1" fill="#083344" />
      </>
    );
  }

  if (variant === 'shop') {
    return (
      <>
        <rect x="10" y="16" width="44" height="36" rx="4" fill="#92400e" stroke="#fbbf24" strokeWidth="1.5" />
        <rect x="10" y="12" width="44" height="12" rx="3" fill="#f8fafc" />
        <rect x="10" y="12" width="9" height="12" rx="2" fill="#ef4444" />
        <rect x="28" y="12" width="9" height="12" fill="#ef4444" />
        <rect x="45" y="12" width="9" height="12" rx="2" fill="#ef4444" />
        <rect x="16" y="31" width="13" height="12" rx="2" fill="#bae6fd" />
        <rect x="36" y="29" width="10" height="23" rx="2" fill="#451a03" />
        <circle cx="43" cy="41" r="1.2" fill="#fbbf24" />
      </>
    );
  }

  return (
    <>
      <rect x="14" y="25" width="36" height="27" rx="3" fill="#f8fafc" stroke="#fde68a" strokeWidth="1.5" />
      <polygon points="10,28 32,10 54,28" fill="#dc2626" stroke="#fecaca" strokeWidth="1.5" />
      <rect x="28" y="39" width="8" height="13" rx="1" fill="#7c2d12" />
      <rect x="18" y="33" width="8" height="7" rx="1" fill="#bfdbfe" />
      <rect x="39" y="33" width="8" height="7" rx="1" fill="#bfdbfe" />
      <rect x="43" y="13" width="5" height="9" rx="1" fill="#78350f" />
    </>
  );
};

const renderStreetLightTile = (variant) => {
  if (variant === 'modern') {
    return (
      <g>
        <circle cx="47" cy="16" r="12" fill="#67e8f9" opacity="0.16" />
        <path d="M36 48V22c0-3 2-5 5-5h11" fill="none" stroke="#cbd5e1" strokeWidth="4" strokeLinecap="round" />
        <rect x="46" y="12" width="13" height="8" rx="3" fill="#67e8f9" stroke="#e0f2fe" strokeWidth="1.5" />
        <circle cx="36" cy="51" r="5" fill="#334155" stroke="#e2e8f0" strokeWidth="1" />
      </g>
    );
  }

  return (
    <g>
      <circle cx="46" cy="18" r="13" fill="#fde68a" opacity="0.2" />
      <line x1="46" y1="50" x2="46" y2="22" stroke="#1f2937" strokeWidth="4" strokeLinecap="round" />
      <path d="M39 23h14l-3-8h-8z" fill="#fbbf24" stroke="#fff7ed" strokeWidth="1.4" />
      <circle cx="46" cy="18" r="4" fill="#fef3c7" />
      <circle cx="46" cy="52" r="5" fill="#374151" stroke="#e5e7eb" strokeWidth="1" />
    </g>
  );
};

const CityTileSvg = ({ cell, toolId, compact = false }) => {
  const toolKind = getCityToolKind(toolId);
  const toolVariant = getCityToolVariant(toolId);
  const roadVariant = toolKind === 'road' ? toolVariant : cell?.road;
  const buildingVariant = toolKind === 'building' ? toolVariant : cell?.building;
  const lightVariant = toolKind === 'light' ? toolVariant : cell?.light;
  const isErase = toolKind === 'erase';

  return (
    <svg
      className={`city-tile-svg ${compact ? 'compact' : ''}`}
      viewBox="0 0 64 64"
      role="img"
      aria-hidden="true"
    >
      <rect x="0" y="0" width="64" height="64" rx="8" fill="#112d22" />
      <circle cx="12" cy="14" r="2" fill="#3f8f62" opacity="0.45" />
      <circle cx="52" cy="48" r="1.8" fill="#3f8f62" opacity="0.35" />
      {roadVariant && renderRoadTile(roadVariant)}
      {buildingVariant && renderBuildingTile(buildingVariant)}
      {lightVariant && renderStreetLightTile(lightVariant)}
      {isErase && (
        <>
          <rect x="18" y="24" width="28" height="18" rx="4" transform="rotate(-28 32 33)" fill="#f8fafc" />
          <rect x="31" y="24" width="14" height="18" rx="3" transform="rotate(-28 38 33)" fill="#f43f5e" />
          <line x1="18" y1="48" x2="48" y2="16" stroke="#f43f5e" strokeWidth="4" strokeLinecap="round" />
        </>
      )}
    </svg>
  );
};

const buildCityPreviewCell = (cell, toolId) => {
  if (!toolId) return cell || createEmptyCityCell();
  const toolKind = getCityToolKind(toolId);
  const toolVariant = getCityToolVariant(toolId);

  if (toolKind === 'road') {
    return { ...createEmptyCityCell(), road: toolVariant };
  }
  if (toolKind === 'building') {
    return { ...createEmptyCityCell(), building: toolVariant, heightScale: 1 };
  }
  if (toolKind === 'light') {
    return { ...createEmptyCityCell(), road: 'straight', light: toolVariant };
  }
  return createEmptyCityCell();
};

const getCityCellLabel = (cell) => {
  if (!cell) return 'Empty block';
  const parts = [];
  if (cell.road) parts.push(CITY_ROAD_META[cell.road]?.label || 'Road');
  if (cell.building) parts.push(CITY_BUILDING_META[cell.building]?.label || 'Building');
  if (cell.light) parts.push(CITY_LIGHT_META[cell.light]?.label || 'Street light');
  return parts.length ? parts.join(' + ') : 'Empty block';
};

const CityTile3D = ({ cell, toolId, compact = false, selected = false, rotoscope = false }) => {
  const previewCell = buildCityPreviewCell(cell, toolId);
  const buildingMeta = previewCell.building ? CITY_BUILDING_META[previewCell.building] : null;
  const lightMeta = previewCell.light ? CITY_LIGHT_META[previewCell.light] : null;
  const heightScale = previewCell.heightScale || 1;
  const floors = buildingMeta ? Math.max(1, Math.round(buildingMeta.floors * heightScale)) : 0;

  return (
    <div
      className={`city-tile-3d ${compact ? 'compact' : ''} ${selected ? 'selected' : ''} ${rotoscope ? 'rotoscope' : ''}`}
      style={{
        '--building-color': buildingMeta?.color || '#64748b',
        '--building-roof': buildingMeta?.roof || '#334155',
        '--building-accent': buildingMeta?.accent || '#bae6fd',
        '--building-height': `${Math.min(84, 22 + floors * (compact ? 3 : 7))}%`,
        '--city-elevation': `${Math.min(18, (previewCell.elevation || 0) * 8)}px`,
        '--city-rotation': `${previewCell.rotation || 0}deg`,
        '--light-color': lightMeta?.color || '#fde68a',
      }}
      aria-hidden="true"
    >
      <span className="city-ground-3d" />
      {previewCell.road && (
        <span className={`city-road-3d road-${previewCell.road}`}>
          <span className="city-road-lane" />
          {previewCell.road === 'intersection' && <span className="city-road-cross" />}
          {previewCell.road === 'curve' && <span className="city-road-turn" />}
        </span>
      )}
      {previewCell.building && (
        <span className={`city-building-3d building-${previewCell.building}`}>
          <span className="city-building-body">
            <span className="city-building-side" />
            <span className="city-building-front" />
            <span className="city-building-windows">
              {Array.from({ length: Math.min(10, floors) }).map((_, index) => (
                <i key={index} />
              ))}
            </span>
          </span>
          <span className="city-building-roof" />
          {previewCell.building === 'house' && <span className="city-building-chimney" />}
          {previewCell.building === 'shop' && <span className="city-shop-awning" />}
          {previewCell.building === 'office' && <span className="city-office-antenna" />}
        </span>
      )}
      {previewCell.light && (
        <span className={`city-light-3d light-${previewCell.light}`}>
          <span className="city-light-glow" />
          <span className="city-light-pole" />
          <span className="city-light-head" />
          {previewCell.light === 'modern' && <span className="city-light-arm" />}
        </span>
      )}
    </div>
  );
};

function App() {
  const [assets, setAssets] = useState([]);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');
  const [toast, setToast] = useState('');
  
  // Track if we need to poll for updates
  const [shouldPoll, setShouldPoll] = useState(false);

  // Customizer / Color wheel states
  const [generationColor, setGenerationColor] = useState('#8b5cf6');
  const [useGenerationColor, setUseGenerationColor] = useState(false);
  const [customColor, setCustomColor] = useState('');
  const [showPresets, setShowPresets] = useState(false);
  const modelViewerRef = useRef(null);
  const modelViewerOriginalColorRef = useRef(new WeakMap());

  // Workspace states
  const [activeTab, setActiveTab] = useState('single'); // 'single' | 'room' | 'city' | 'game' | 'movie'
  const [roomWallColors, setRoomWallColors] = useState(DEFAULT_WALL_COLORS);
  const [houseConfig, setHouseConfig] = useState(DEFAULT_HOUSE_CONFIG);
  const [activeRoomAssets, setActiveRoomAssets] = useState([]);
  const [roomLayout, setRoomLayout] = useState('all');
  const [selectedRoomAssetId, setSelectedRoomAssetId] = useState(null);
  const [roomAssetTransforms, setRoomAssetTransforms] = useState({});
  const [roomAssetMaterialInfo, setRoomAssetMaterialInfo] = useState({});
  const [isSavingRoom, setIsSavingRoom] = useState(false);
  const [isExportingPrintAsset, setIsExportingPrintAsset] = useState(false);
  const [isExportingRoomPrint, setIsExportingRoomPrint] = useState(false);
  const [citySelectedTool, setCitySelectedTool] = useState('road_straight');
  const [cityGrid, setCityGrid] = useState(createEmptyCityGrid);
  const cityGridRef = useRef(cityGrid);
  const [cityLightCount, setCityLightCount] = useState(12);
  const [cityLightStyle, setCityLightStyle] = useState('mixed');
  const [citySelectedCell, setCitySelectedCell] = useState(null);
  const [cityRotoscopeMode, setCityRotoscopeMode] = useState(true);
  const [isExportingCityBlend, setIsExportingCityBlend] = useState(false);
  const [cityPlannerMessage, setCityPlannerMessage] = useState('Select a tool, then click any grid cell to place it.');
  const activeRoomAssetDetails = assets.filter((asset) => activeRoomAssets.includes(asset.id));
  const effectiveRoomLayoutMode = getEffectiveLayoutMode(roomLayout, activeRoomAssetDetails);
  const isHouseLayout = effectiveRoomLayoutMode === 'house';
  const isCityLayout = effectiveRoomLayoutMode === 'city';
  const layoutDisplayName = isCityLayout ? 'City Block' : isHouseLayout ? 'House' : 'Room';
  const layoutDisplayNameLower = isCityLayout ? 'city block' : isHouseLayout ? 'house' : 'room';
  const layoutPlan = buildLayoutPlan(effectiveRoomLayoutMode, houseConfig);
  const roomPositionRangeX = Math.max(1.4, layoutPlan.bounds.width / 2);
  const roomPositionRangeZ = Math.max(1.4, layoutPlan.bounds.depth / 2);
  const roomPositionRangeY = Math.max(2.5, layoutPlan.dimensions.roomHeight + 0.6);
  const cityStats = getCityGridStats(cityGrid);
  const selectedCityCellData = citySelectedCell
    ? cityGrid[citySelectedCell.row]?.[citySelectedCell.col]
    : null;

  const createRoomTransformMap = (selectedIds, availableAssets) => {
    const transformMap = {};
    selectedIds.forEach((id) => {
      const asset = availableAssets.find((entry) => entry.id === id);
      const existingTransform = roomAssetTransforms[id] || {};
      transformMap[id] = {
        posX: existingTransform.posX || 0,
        posY: existingTransform.posY || 0,
        posZ: existingTransform.posZ || 0,
        rotY: existingTransform.rotY || 0,
        scale: existingTransform.scale ?? 1,
        customColor:
          existingTransform.customColor ?? asset?.parameters?.custom_color ?? null,
        detailColors: existingTransform.detailColors || {},
      };
    });
    return transformMap;
  };

  // Dynamically load/unload model-viewer script to prevent Three.js conflicts with RoomViewer
  const modelViewerLoadedRef = useRef(false);
  useEffect(() => {
    if (activeTab === 'single' && !modelViewerLoadedRef.current) {
      // Load model-viewer CDN script dynamically
      if (!document.querySelector('script[data-model-viewer]')) {
        const script = document.createElement('script');
        script.type = 'module';
        script.src = 'https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js';
        script.setAttribute('data-model-viewer', 'true');
        document.head.appendChild(script);
        modelViewerLoadedRef.current = true;
      }
    }
  }, [activeTab]);

  useEffect(() => {
    cityGridRef.current = cityGrid;
  }, [cityGrid]);

  const applyRoomLayoutPreset = (layoutName) => {
    setRoomLayout(layoutName);
    setSelectedRoomAssetId(null); // Deselect on preset change
    const completedAssets = assets.filter((asset) => asset.status === 'completed');
    if (layoutName === 'clear') {
      setActiveRoomAssets([]);
      setRoomAssetTransforms({});
      return;
    }
    const selectedIds = getLayoutPresetAssetIds(layoutName, completedAssets, houseConfig);
    setRoomAssetTransforms(createRoomTransformMap(selectedIds, completedAssets));
    setActiveRoomAssets(selectedIds);
  };

  // Auto-initialize active room assets once completed assets are loaded
  useEffect(() => {
    if (assets.length > 0 && activeRoomAssets.length === 0) {
      const completed = assets.filter((asset) => asset.status === 'completed');
      if (completed.length > 0) {
        const defaultHouseIds = getLayoutPresetAssetIds('house', completed, houseConfig);
        const defaultLayout = defaultHouseIds.length > 0 ? 'house' : 'all';
        const selectedIds =
          defaultLayout === 'house'
            ? defaultHouseIds
            : completed.map((asset) => asset.id).slice(0, 8);

        setRoomAssetTransforms(createRoomTransformMap(selectedIds, completed));
        setActiveRoomAssets(selectedIds);
        setRoomLayout(defaultLayout);
      }
    }
  }, [assets]);

  // Sync customColor state when selected asset changes
  useEffect(() => {
    if (selectedAsset && selectedAsset.parameters && selectedAsset.parameters.custom_color) {
      setCustomColor(selectedAsset.parameters.custom_color);
    } else {
      setCustomColor('');
    }
  }, [selectedAsset]);

  // Apply customColor to the model-viewer materials in real-time
  useEffect(() => {
    if (!selectedAsset || selectedAsset.status !== 'completed') return;
    
    const modelViewer = modelViewerRef.current;
    if (!modelViewer) return;
    const activeCustomColor = customColor || selectedAsset.parameters?.custom_color || null;

    const applyColor = () => {
      if (!modelViewer.model) return;
      const materials = modelViewer.model.materials;
      if (!materials) return;

      materials.forEach(material => {
        if (!material?.pbrMetallicRoughness) {
          return;
        }

        if (!modelViewerOriginalColorRef.current.has(material)) {
          const originalFactor = material.pbrMetallicRoughness.baseColorFactor || [1, 1, 1, 1];
          modelViewerOriginalColorRef.current.set(material, [...originalFactor]);
        }

        const lowerName = (material.name || '').toLowerCase();
        // Skip secondary parts
        const secondaryKeywords = [
          "glass", "soil", "stem", "leaf", "plant", "water", 
          "flame", "ticks", "mirror", "fringe", "glow", "hands", "pin"
        ];
        const isSecondary = secondaryKeywords.some(kw => lowerName.includes(kw));

        if (!activeCustomColor || isSecondary) {
          const originalFactor = modelViewerOriginalColorRef.current.get(material);
          if (originalFactor) {
            material.pbrMetallicRoughness.setBaseColorFactor(originalFactor);
          }
          return;
        }

        const hex = activeCustomColor.replace('#', '');
        if (hex.length === 6) {
          const r = parseInt(hex.substring(0, 2), 16) / 255;
          const g = parseInt(hex.substring(2, 4), 16) / 255;
          const b = parseInt(hex.substring(4, 6), 16) / 255;
          
          material.pbrMetallicRoughness.setBaseColorFactor([r, g, b, 1.0]);
        }
      });
    };

    applyColor();

    const handleLoad = () => {
      applyColor();
    };

    modelViewer.addEventListener('load', handleLoad);
    return () => {
      modelViewer.removeEventListener('load', handleLoad);
    };
  }, [customColor, selectedAsset]);

  const handleBakeColor = async () => {
    if (!selectedAsset) return;
    setIsGenerating(true);
    setError('');
    const colorToBake = customColor || selectedAsset.parameters?.custom_color || '#cbd5e1';
    
    try {
      const res = await fetch(`${API_BASE_URL}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          prompt: selectedAsset.prompt,
          custom_color: colorToBake
        })
      });
      
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Generation failed.');
      }
      
      const newAsset = await res.json();
      setAssets(prev => [newAsset, ...prev]);
      setSelectedAsset(newAsset);
      setPrompt('');
      setShouldPoll(true);
      showToast('Asset queued with new custom color!');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsGenerating(false);
    }
  };

  // Load assets on mount
  useEffect(() => {
    fetchAssets();
  }, []);

  // Poll for generating assets
  useEffect(() => {
    if (!shouldPoll) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/assets`);
        const data = await res.json();
        setAssets(data);

        // Check if any asset is still generating
        const generating = data.some(asset => asset.status === 'generating');
        if (!generating) {
          setShouldPoll(false);
        }

        // Update selected asset reference in real-time
        if (selectedAsset) {
          const updated = data.find(a => a.id === selectedAsset.id);
          if (updated) {
            setSelectedAsset(updated);
          }
        }
      } catch (err) {
        console.error('Error polling assets:', err);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [shouldPoll, selectedAsset]);

  const fetchAssets = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/assets`);
      const data = await res.json();
      setAssets(data);
      if (data.length > 0 && !selectedAsset) {
        setSelectedAsset(data[0]);
      }
      
      const generating = data.some(asset => asset.status === 'generating');
      if (generating) {
        setShouldPoll(true);
      }
    } catch (err) {
      console.error('Failed to fetch assets:', err);
      setError('Cannot connect to kchiro backend server.');
    }
  };

  const handleGenerate = async (e) => {
    if (e) e.preventDefault();
    if (!prompt.trim()) return;

    setIsGenerating(true);
    setError('');
    
    try {
      const payload = { prompt };
      if (useGenerationColor) {
        payload.custom_color = generationColor;
      }
      const res = await fetch(`${API_BASE_URL}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Generation failed.');
      }
      
      const newAsset = await res.json();
      setAssets(prev => [newAsset, ...prev]);
      setSelectedAsset(newAsset);
      setPrompt('');
      setShouldPoll(true);
      showToast('Asset queued for generation!');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDelete = async (id, e) => {
    if (e) e.stopPropagation();
    
    try {
      const res = await fetch(`${API_BASE_URL}/api/assets/${id}`, {
        method: 'DELETE'
      });
      
      if (res.ok) {
        setAssets(prev => prev.filter(a => a.id !== id));
        if (selectedAsset && selectedAsset.id === id) {
          setSelectedAsset(null);
        }
        showToast('Asset deleted successfully.');
      }
    } catch (err) {
      console.error('Failed to delete asset:', err);
    }
  };

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(''), 3000);
  };

  const triggerDownload = (downloadUrl, filename) => {
    const link = document.createElement('a');
    link.href = `${API_BASE_URL}${downloadUrl}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const buildRoomExportPayload = () => ({
    wall_color: roomWallColors.interior,
    wall_colors: roomWallColors,
    layout_mode: effectiveRoomLayoutMode,
    house_config: houseConfig,
    assets: activeRoomAssets.map((assetId) => {
      const asset = assets.find((entry) => entry.id === assetId);
      const transform = roomAssetTransforms[assetId] || {};
      return {
        asset_id: assetId,
        pos_x: transform.posX || 0,
        pos_y: transform.posY || 0,
        pos_z: transform.posZ || 0,
        rot_y: transform.rotY || 0,
        scale: transform.scale ?? 1,
        custom_color: transform.customColor || asset?.parameters?.custom_color || null,
        detail_colors: transform.detailColors || {},
      };
    }),
  });

  const buildCityExportPayload = () => ({
    grid_size: CITY_GRID_SIZE,
    cell_size: CITY_CELL_SIZE_METERS,
    rotoscope: cityRotoscopeMode,
    cells: cityGrid.flatMap((row, rowIndex) =>
      row.map((cell, colIndex) => ({
        row: rowIndex,
        col: colIndex,
        road: cell.road,
        building: cell.building,
        light: cell.light,
        elevation: cell.elevation || 0,
        rotation: cell.rotation || 0,
        height_scale: cell.heightScale || 1,
      })).filter((cell) => cell.road || cell.building || cell.light)
    ),
  });

  const handleSaveCityToBlender = async () => {
    const payload = buildCityExportPayload();
    if (payload.cells.length === 0) {
      setCityPlannerMessage('Place at least one road, building, or light before exporting the Blender city.');
      return;
    }

    setIsExportingCityBlend(true);
    setError('');

    try {
      const res = await fetch(`${API_BASE_URL}/api/city/export-blend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'City export failed.');
      }

      const data = await res.json();
      triggerDownload(data.download_url, data.filename || 'kchiro_city.blend');
      setCityPlannerMessage('Blender city file downloaded with separate rotoscope-ready roads, buildings, and lights.');
      showToast('3D Blender city downloaded!');
    } catch (err) {
      setError(err.message);
      setCityPlannerMessage(`City export failed: ${err.message}`);
    } finally {
      setIsExportingCityBlend(false);
    }
  };

  const handleRoomAssetMaterialInfo = (assetId, materialInfo) => {
    setRoomAssetMaterialInfo(prev => {
      const nextInfo = materialInfo || { materialRoles: [], hasUnmappedPrimaryMaterials: true };
      const currentInfo = prev[assetId];
      if (currentInfo && JSON.stringify(currentInfo) === JSON.stringify(nextInfo)) {
        return prev;
      }
      return { ...prev, [assetId]: nextInfo };
    });
  };

  const handleSaveRoomToBlender = async () => {
    setIsSavingRoom(true);
    setError('');

    try {
      const res = await fetch(`${API_BASE_URL}/api/rooms/export-blend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(buildRoomExportPayload())
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Room export failed.');
      }

      const data = await res.json();
      triggerDownload(data.download_url, data.filename || 'kchiro_room.blend');
      showToast(`${layoutDisplayName} .blend saved for Blender!`);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSavingRoom(false);
    }
  };

  const handleExportSelectedAssetToPrint = async () => {
    if (!selectedAsset || selectedAsset.status !== 'completed') return;

    setIsExportingPrintAsset(true);
    setError('');

    try {
      const res = await fetch(`${API_BASE_URL}/api/assets/${selectedAsset.id}/export-print`, {
        method: 'POST',
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'STL export failed.');
      }

      const data = await res.json();
      triggerDownload(data.download_url, data.filename || `asset_${selectedAsset.id}.stl`);
      showToast('Printable STL downloaded for the selected asset.');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsExportingPrintAsset(false);
    }
  };

  const handleSaveRoomToPrint = async () => {
    setIsExportingRoomPrint(true);
    setError('');

    try {
      const res = await fetch(`${API_BASE_URL}/api/rooms/export-print`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(buildRoomExportPayload())
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Room STL export failed.');
      }

      const data = await res.json();
      triggerDownload(data.download_url, data.filename || 'kchiro_room.stl');
      showToast(`Printable ${layoutDisplayNameLower} STL downloaded.`);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsExportingRoomPrint(false);
    }
  };

  const selectPreset = (presetText) => {
    setPrompt(presetText);
  };

  const handleHouseConfigChange = (field, value) => {
    setHouseConfig((prev) => {
      const next = {
        ...prev,
        [field]: value,
      };

      if (field === 'attachBathroomToBedroom' && value === false) {
        next.ensuiteBathrooms = 0;
      }

      if (field === 'ensuiteBathrooms' && value > 0) {
        next.attachBathroomToBedroom = true;
      }

      const maxEnsuites = Math.min(
        field === 'bedrooms' ? value : next.bedrooms,
        field === 'bathrooms' ? value : next.bathrooms
      );
      next.ensuiteBathrooms = Math.max(
        0,
        Math.min(next.ensuiteBathrooms, Number.isFinite(maxEnsuites) ? maxEnsuites : 0)
      );

      return next;
    });
  };

  const handleWallColorChange = (wallKey, value) => {
    setRoomWallColors((prev) => ({
      ...prev,
      [wallKey]: value,
    }));
  };

  const handleCityToolSelect = (toolId) => {
    setCitySelectedTool(toolId);
    setCityPlannerMessage(`${CITY_TOOL_LABELS[toolId]} selected. Click a grid cell to place it.`);
  };

  const handleCityCellClick = (rowIndex, colIndex) => {
    const toolKind = getCityToolKind(citySelectedTool);
    const toolVariant = getCityToolVariant(citySelectedTool);

    const nextGrid = cityGridRef.current.map((row, currentRow) =>
        row.map((cell, currentCol) => {
          if (currentRow !== rowIndex || currentCol !== colIndex) {
            return cell;
          }

          if (toolKind === 'erase') {
            return createEmptyCityCell();
          }

          if (toolKind === 'road') {
            return {
              ...cell,
              road: toolVariant,
              building: null,
              elevation: 0,
              heightScale: 1,
            };
          }

          if (toolKind === 'building') {
            return {
              road: null,
              building: toolVariant,
              light: null,
              elevation: cell.elevation || 0,
              rotation: cell.rotation || 0,
              heightScale: cell.heightScale || 1,
            };
          }

          if (toolKind === 'light') {
            return {
              ...cell,
              light: toolVariant,
              elevation: cell.elevation || 0,
              rotation: cell.rotation || 0,
              heightScale: cell.heightScale || 1,
            };
          }

          return cell;
        })
      );

    cityGridRef.current = nextGrid;
    setCityGrid(nextGrid);
    setCitySelectedCell({ row: rowIndex, col: colIndex });

    setCityPlannerMessage(
      `${CITY_TOOL_LABELS[citySelectedTool]} placed at row ${rowIndex + 1}, column ${colIndex + 1}.`
    );
  };

  const handleSelectedCityCellChange = (field, value) => {
    if (!citySelectedCell) return;
    const nextGrid = cityGridRef.current.map((row, rowIndex) =>
      row.map((cell, colIndex) => {
        if (rowIndex !== citySelectedCell.row || colIndex !== citySelectedCell.col) {
          return cell;
        }
        return {
          ...cell,
          [field]: value,
        };
      })
    );
    cityGridRef.current = nextGrid;
    setCityGrid(nextGrid);
    setCityPlannerMessage(`Updated ${getCityCellLabel(nextGrid[citySelectedCell.row][citySelectedCell.col])} block controls.`);
  };

  const handleClearCityGrid = () => {
    const nextGrid = createEmptyCityGrid();
    cityGridRef.current = nextGrid;
    setCityGrid(nextGrid);
    setCitySelectedCell(null);
    setCityPlannerMessage('City canvas cleared. Fresh grid, fresh chaos, but the organized kind.');
  };

  const handleAutoPlaceCityLights = () => {
    const roadCells = getCityRoadCells(cityGridRef.current);

    if (roadCells.length === 0) {
      setCityPlannerMessage('Add some road tiles first, then Auto-Place Lights can distribute them.');
      return;
    }

    const selectedRoadCells = pickEvenlySpacedCells(roadCells, cityLightCount);
    const selectedKeys = new Set(selectedRoadCells.map((cell) => `${cell.row}:${cell.col}`));
    const placedCount = selectedRoadCells.length;

    const nextGrid = cityGridRef.current.map((row, rowIndex) =>
        row.map((cell, colIndex) => {
          const shouldPlaceLight = selectedKeys.has(`${rowIndex}:${colIndex}`);
          const nextLight =
            cityLightStyle === 'mixed'
              ? (rowIndex + colIndex) % 2 === 0 ? 'classic' : 'modern'
              : cityLightStyle;

          return {
            ...cell,
            light: shouldPlaceLight ? nextLight : null,
          };
        })
      );

    cityGridRef.current = nextGrid;
    setCityGrid(nextGrid);

    setCityPlannerMessage(
      `Auto-placed ${placedCount} street light${placedCount === 1 ? '' : 's'} evenly across ${roadCells.length} road tile${roadCells.length === 1 ? '' : 's'}.`
    );
  };

  const getAssetIcon = (type) => {
    switch (type) {
      case 'sword': return <SwordIcon />;
      case 'dagger': return <SwordIcon />;
      case 'table': return <TableIcon />;
      case 'dining_table': return <DiningTableIcon />;
      case 'coffee_table': return <CoffeeTableIcon />;
      case 'desk': return <DeskIcon />;
      case 'barrel': return <BarrelIcon />;
      case 'crate': return <CrateIcon />;
      case 'shield': return <ShieldIcon />;
      case 'chair': return <ChairIcon />;
      case 'stool': return <StoolIcon />;
      case 'chest': return <ChestIcon />;
      case 'axe': return <AxeIcon />;
      case 'hammer': return <HammerIcon />;
      case 'mace': return <HammerIcon />;
      case 'spear': return <StaffIcon />;
      case 'halberd': return <StaffIcon />;
      case 'staff': return <StaffIcon />;
      case 'bow': return <BowIcon />;
      case 'crossbow': return <BowIcon />;
      case 'arrow': return <SwordIcon />;
      case 'bolt': return <SwordIcon />;
      case 'magic_staff': return <StaffIcon />;
      case 'wand': return <StaffIcon />;
      case 'orb': return <OrbIcon />;
      case 'helmet': return <HelmetIcon />;
      case 'chestplate': return <ShieldIcon />;
      case 'gauntlets': return <ShieldIcon />;
      case 'boots': return <BedIcon />;
      case 'backpack': return <CrateIcon />;
      case 'belt': return <ChestIcon />;
      case 'pouch': return <ChestIcon />;
      case 'cape': return <PaintingIcon />;
      case 'torch': return <TorchIcon />;
      case 'tent': return <RoofIcon />;
      case 'campfire': return <TorchIcon />;
      case 'sleeping_bag': return <BedIcon />;
      case 'lantern': return <LampIcon />;
      case 'cooking_pot': return <BarrelIcon />;
      case 'supply_box': return <ChestIcon />;
      case 'sofa': return <CouchIcon />;
      case 'bench': return <BenchIcon />;
      case 'couch': return <CouchIcon />;
      case 'armchair': return <ArmchairIcon />;
      case 'bed': return <BedIcon />;
      case 'bunk_bed': return <BunkBedIcon />;
      case 'wardrobe': return <WardrobeIcon />;
      case 'closet': return <ClosetIcon />;
      case 'dresser': return <DresserIcon />;
      case 'cabinet': return <CabinetIcon />;
      case 'shelf': return <ShelfIcon />;
      case 'bookcase': return <BookcaseIcon />;
      case 'nightstand': return <NightstandIcon />;
      case 'tv_stand': return <TVStandIcon />;
      case 'storage': return <CrateIcon />;
      case 'lighting': return <TorchIcon />;
      case 'lamp': return <LampIcon />;
      case 'chandelier': return <ChandelierIcon />;
      case 'painting': return <PaintingIcon />;
      case 'picture_frame': return <PictureFrameIcon />;
      case 'fridge': return <FridgeIcon />;
      case 'stove': return <StoveIcon />;
      case 'oven': return <OvenIcon />;
      case 'microwave': return <MicrowaveIcon />;
      case 'sink': return <SinkIcon />;
      case 'countertop': return <CountertopIcon />;
      case 'toilet': return <ToiletIcon />;
      case 'bathtub': return <BathtubIcon />;
      case 'shower': return <ShowerIcon />;
      case 'mirror': return <MirrorIcon />;
      case 'towel_rack': return <TowelRackIcon />;
      case 'clock': return <ClockIcon />;
      case 'vase': return <VaseIcon />;
      case 'plant_pot': return <PlantIcon />;
      case 'rug': return <RugIcon />;
      case 'wall': return <WallIcon />;
      case 'floor': return <FloorIcon />;
      case 'ceiling': return <CeilingIcon />;
      case 'roof': return <RoofIcon />;
      case 'pillar': return <PillarIcon />;
      case 'beam': return <BeamIcon />;
      case 'foundation': return <FoundationIcon />;
      case 'door': return <DoorAssetIcon />;
      case 'window': return <WindowAssetIcon />;
      case 'archway': return <ArchwayIcon />;
      case 'gate': return <GateIcon />;
      case 'stairs': return <StairsIcon />;
      case 'ladder': return <LadderIcon />;
      case 'ramp': return <RampIcon />;
      case 'bridge': return <BridgeIcon />;
      case 'balcony': return <BalconyIcon />;
      case 'fence': return <FenceIcon />;
      case 'railing': return <RailingIcon />;
      case 'chimney': return <ChimneyIcon />;
      case 'porch': return <PorchIcon />;
      case 'castle_wall': return <WallIcon />;
      case 'tower': return <PillarIcon />;
      case 'drawbridge': return <BridgeIcon />;
      case 'throne': return <ChairIcon />;
      case 'banner': return <PaintingIcon />;
      case 'market_stall': return <TableIcon />;
      case 'well': return <BarrelIcon />;
      case 'cart': return <CrateIcon />;
      case 'anvil': return <HammerIcon />;
      case 'forge': return <ChimneyIcon />;
      case 'control_panel': return <MicrowaveIcon />;
      case 'terminal': return <TVStandIcon />;
      case 'computer': return <MicrowaveIcon />;
      case 'server_rack': return <WardrobeIcon />;
      case 'energy_cell': return <OrbIcon />;
      case 'tech_crate': return <CrateIcon />;
      case 'space_door': return <DoorAssetIcon />;
      case 'airlock': return <DoorAssetIcon />;
      case 'turret': return <HammerIcon />;
      case 'drone': return <PlaneAssetIcon />;
      case 'pipe': return <RailingIcon />;
      case 'valve': return <HammerIcon />;
      case 'tank': return <BarrelIcon />;
      case 'generator': return <HammerIcon />;
      case 'conveyor_belt': return <BridgeIcon />;
      case 'toolbox': return <ChestIcon />;
      case 'forklift': return <VehicleIcon />;
      case 'storage_rack': return <ShelfIcon />;
      case 'street_lamp': return <LampIcon />;
      case 'traffic_light': return <LampIcon />;
      case 'road_sign': return <PictureFrameIcon />;
      case 'street_bench': return <BenchIcon />;
      case 'mailbox': return <CabinetIcon />;
      case 'trash_can': return <BarrelIcon />;
      case 'bus_stop': return <PorchIcon />;
      case 'phone_booth': return <DoorAssetIcon />;
      case 'car':
      case 'truck':
      case 'bike':
      case 'motorcycle':
      case 'tractor':
      case 'battle_tank':
        return <VehicleIcon />;
      case 'boat':
      case 'canoe':
      case 'ship':
        return <BoatIcon />;
      case 'plane':
      case 'helicopter':
        return <PlaneAssetIcon />;
      case 'male':
      case 'female':
      case 'child':
      case 'elder':
      case 'merchant':
      case 'guard':
      case 'farmer':
      case 'blacksmith':
      case 'soldier':
      case 'elf':
      case 'orc':
      case 'goblin':
      case 'dwarf':
      case 'dragon':
        return <CharacterIcon />;
      case 'dog':
      case 'cat':
      case 'horse':
      case 'cow':
      case 'deer':
      case 'wolf':
      case 'bird':
      case 'fish':
        return <AnimalIcon />;
      case 'coin':
      case 'gem':
      case 'artifact':
        return <GemIcon />;
      case 'key':
        return <KeyAssetIcon />;
      case 'scroll':
      case 'potion':
      case 'treasure_chest':
        return <ChestIcon />;
      case 'terrain':
      case 'hill':
      case 'mountain':
      case 'cliff':
      case 'valley':
      case 'cave':
      case 'ground_tile':
      case 'road_tile':
      case 'path_tile':
      case 'river_tile':
      case 'dungeon_tile':
      case 'game_background_2d':
        return <TerrainIcon />;
      case 'oak_tree':
      case 'pine_tree':
      case 'birch_tree':
      case 'palm_tree':
      case 'dead_tree':
      case 'sapling':
      case 'log':
      case 'tree_stump':
      case 'fallen_tree':
      case 'root':
        return <TreeIcon />;
      case 'grass':
      case 'bush':
      case 'shrub':
      case 'fern':
      case 'flower':
      case 'moss':
      case 'vine':
        return <PlantIcon />;
      case 'small_rock':
      case 'boulder':
      case 'rock_cluster':
      case 'cliff_section':
        return <RockIcon />;
      case 'mushroom':
        return <MushroomIcon />;
      case 'pond':
      case 'river_segment':
      case 'waterfall':
      case 'stream':
        return <WaterIcon />;
      default: return <CrateIcon />;
    }
  };

  const formatAssetType = (type) => {
    return (type || '').replace(/_/g, ' ');
  };

  const formatTime = (timeString) => {
    try {
      const date = new Date(timeString);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' ' + date.toLocaleDateString();
    } catch (e) {
      return timeString;
    }
  };

  return (
    <div className="app-container">
      {/* Toast Notification */}
      {toast && (
        <div className="notification-toast">
          <SparklesIcon />
          <span>{toast}</span>
        </div>
      )}

      {/* Sidebar - Recent Generations */}
      <aside className="sidebar">
        <div className="sidebar-header" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <img src="/logo.png" alt="KCHIRO Logo" style={{ width: '38px', height: '38px', borderRadius: '4px', objectFit: 'contain' }} />
          <span className="logo-text" style={{ fontSize: '20px', letterSpacing: '0.05em' }}>KCHIRO</span>
        </div>
        
        <div className="sidebar-title-row">
          <span className="sidebar-title">My Assets</span>
          <span className="asset-count-badge">{assets.length}</span>
        </div>

        <div className="asset-list">
          {assets.length === 0 ? (
            <div className="empty-sidebar">
              <CrateIcon className="empty-sidebar-icon" />
              <p>No assets yet. Generate one below!</p>
            </div>
          ) : (
            assets.map(asset => (
              <div
                key={asset.id}
                className={`asset-row ${selectedAsset && selectedAsset.id === asset.id ? 'active' : ''}`}
                onClick={() => setSelectedAsset(asset)}
                title={asset.prompt}
              >
                <span className="asset-row-icon">{getAssetIcon(asset.asset_type)}</span>
                <span className="asset-row-name">{formatAssetType(asset.asset_type)}</span>
                <span className={`asset-row-dot ${asset.status}`} />
                <button
                  className="asset-row-delete"
                  title="Delete"
                  onClick={(e) => handleDelete(asset.id, e)}
                >
                  <TrashIcon />
                </button>
              </div>
            ))
          )}
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        {/* Top Prompting Panel — hidden in Room Designer mode for maximum canvas space */}
        {activeTab === 'single' && (
        <section className="prompt-section">
          <h1 className="prompt-section-title">Procedural Asset Generator</h1>
          <p className="prompt-section-subtitle">
            Translate text prompts into parameters using Qwen2.5, then procedurally generate, texture, render, and export GLBs inside Blender.
          </p>

          <form onSubmit={handleGenerate} className="prompt-input-container">
            <textarea
              className="prompt-textarea"
              placeholder="Describe a 3D asset (e.g. A heavy medieval longsword with a golden hilt and blue grip...)"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleGenerate();
                }
              }}
              disabled={isGenerating}
            />
            
            <button 
              type="submit" 
              className="generate-btn" 
              disabled={isGenerating || !prompt.trim()}
            >
              {isGenerating ? (
                <>
                  <span className="pulse-dot"></span>
                  Processing...
                </>
              ) : (
                <>
                  <SparklesIcon />
                  Generate
                </>
              )}
            </button>
          </form>

          {/* Color generator config */}
          <div className="prompt-controls-row">
            <label className="color-toggle-label">
              <input 
                type="checkbox" 
                checked={useGenerationColor} 
                onChange={(e) => setUseGenerationColor(e.target.checked)}
                className="color-checkbox"
              />
              <span>Bake custom color:</span>
            </label>
            <div className="color-picker-wrapper" style={{ opacity: useGenerationColor ? 1 : 0.5 }}>
              <input 
                type="color" 
                value={generationColor} 
                onChange={(e) => {
                  setGenerationColor(e.target.value);
                  if (!useGenerationColor) setUseGenerationColor(true);
                }}
                disabled={isGenerating}
                className="custom-color-input"
              />
              <span className="color-value-text">{generationColor.toUpperCase()}</span>
            </div>

            <button
              type="button"
              className="secondary-action-btn presets-toggle-btn"
              onClick={() => setShowPresets(!showPresets)}
              style={{ marginLeft: 'auto', padding: '6px 12px', fontSize: '12px', height: '28px', minHeight: 'unset', display: 'flex', alignItems: 'center' }}
            >
              <span>{showPresets ? 'Hide Presets 📂' : 'Show Presets 📁'}</span>
            </button>
          </div>

          {/* Categorized Quick Presets */}
          {showPresets && (
            <div className="presets-container">
            <div className="presets-group">
              <span className="presets-group-label">🪑 Seating & Beds</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Simple wooden dining chair with round legs and tall backrest")}>Chair</button>
                <button className="preset-pill" onClick={() => selectPreset("Round bar stool with metal hairpin legs, counter height, with footrest")}>Stool</button>
                <button className="preset-pill" onClick={() => selectPreset("Comfortable 3-seater fabric sofa with wooden legs")}>Sofa</button>
                <button className="preset-pill" onClick={() => selectPreset("Rustic wooden garden bench without backrest, 140cm wide")}>Bench</button>
                <button className="preset-pill" onClick={() => selectPreset("Luxury leather sectional couch with L-shaped chaise lounge")}>Couch</button>
                <button className="preset-pill" onClick={() => selectPreset("Cozy velvet classic armchair in deep blue")}>Armchair</button>
                <button className="preset-pill" onClick={() => selectPreset("King size wooden bed with large headboard and two soft pillows")}>Bed</button>
                <button className="preset-pill" onClick={() => selectPreset("Wooden double decker bunk bed with side safety ladder")}>Bunk Bed</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">🪵 Tables & Desks</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Rustic wooden work table, 120cm width 75cm height with square legs")}>Table</button>
                <button className="preset-pill" onClick={() => selectPreset("Large formal oak dining table that seats 8 people, with turned legs")}>Dining Table</button>
                <button className="preset-pill" onClick={() => selectPreset("Modern low wooden coffee table with hairpin metal legs, 110cm wide")}>Coffee Table</button>
                <button className="preset-pill" onClick={() => selectPreset("Office desk with drawer pedestal, metal frame and wood top")}>Desk</button>
                <button className="preset-pill" onClick={() => selectPreset("Elegant mahogany dining set with a large rectangular table and 6 matching cushioned chairs")}>Dining Set</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">📦 Storage & Decor</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Classic armoire wardrobe with decorative double doors and center mirror")}>Wardrobe</button>
                <button className="preset-pill" onClick={() => selectPreset("Walk-in open closet with side shoe cubbies and two clothes rods, dark oak")}>Closet</button>
                <button className="preset-pill" onClick={() => selectPreset("Rustic wood dresser with 3 rows of drawers, classic brass knobs")}>Dresser</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall glass display cabinet with 4 shelves and kitchen style handles")}>Cabinet</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall rustic wooden cupboard with double doors, open hutch shelving, and 3 storage drawers")}>Cupboard</button>
                <button className="preset-pill" onClick={() => selectPreset("Rustic floating oak shelf with industrial pipe brackets, 80cm wide")}>Shelf</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall wooden bookcase with 5 shelves")}>Bookcase</button>
                <button className="preset-pill" onClick={() => selectPreset("Mid century wooden nightstand with two drawers and tapered legs")}>Nightstand</button>
                <button className="preset-pill" onClick={() => selectPreset("Modern low-profile tv stand console in honey oak with 3 compartments and sliding doors")}>TV Stand</button>
                <button className="preset-pill" onClick={() => selectPreset("Old weathered whiskey barrel, 0.5m radius and 1.2m height")}>Barrel</button>
                <button className="preset-pill" onClick={() => selectPreset("Industrial cargo storage crate, 1.5m width and metal frame")}>Crate</button>
                <button className="preset-pill" onClick={() => selectPreset("Floor lamp with warm rounded shade, 150cm tall")}>Lamp</button>
                <button className="preset-pill" onClick={() => selectPreset("Wall clock with dark mahogany wood frame, 40cm wide")}>Clock</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall ceramic vase in glazed emerald green, geometric style")}>Vase</button>
                <button className="preset-pill" onClick={() => selectPreset("Rounded terracotta plant pot with a lush green houseplant")}>Plant Pot</button>
                <button className="preset-pill" onClick={() => selectPreset("Large circular grey rug with a soft geometric pattern")}>Rug</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">🍳 Kitchen Appliances</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Stainless steel double door refrigerator with ice dispenser, 80cm width")}>Fridge</button>
                <button className="preset-pill" onClick={() => selectPreset("Sleek black electric glass cooktop stove with 4 burners, 75cm wide")}>Stove</button>
                <button className="preset-pill" onClick={() => selectPreset("Built-in oven with black glass viewing door and two wire racks")}>Oven</button>
                <button className="preset-pill" onClick={() => selectPreset("Built-in stainless steel microwave oven with glass viewing window")}>Microwave</button>
                <button className="preset-pill" onClick={() => selectPreset("Double basin undermount kitchen sink cabinet with tall gooseneck faucet")}>Sink</button>
                <button className="preset-pill" onClick={() => selectPreset("White marble kitchen countertop cabinet island with 3 rows of drawers")}>Countertop</button>
                <button className="preset-pill" onClick={() => selectPreset("Large marble-top kitchen island with a breakfast bar overhang and 3 matching bar stools")}>Kitchen Island</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">⚔️ Weapons</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Medieval broadsword with crossguard, 100cm blade and wooden grip")}>Sword</button>
                <button className="preset-pill" onClick={() => selectPreset("Slim steel dagger with a short leather grip and compact crossguard")}>Dagger</button>
                <button className="preset-pill" onClick={() => selectPreset("Double-headed battle axe with leather grip and steel blades")}>Axe</button>
                <button className="preset-pill" onClick={() => selectPreset("Heavy war hammer with a long wooden handle and forged steel head")}>Hammer</button>
                <button className="preset-pill" onClick={() => selectPreset("Spiked iron mace with a leather-wrapped wooden shaft")}>Mace</button>
                <button className="preset-pill" onClick={() => selectPreset("Long spear with a wood shaft and leaf-shaped steel tip")}>Spear</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall halberd polearm with an axe blade, rear hook, and steel spear tip")}>Halberd</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall carved wooden staff with metal bands and a plain top")}>Staff</button>
                <button className="preset-pill" onClick={() => selectPreset("Classic longbow with curved wooden limbs and a taut bowstring")}>Bow</button>
                <button className="preset-pill" onClick={() => selectPreset("Heavy crossbow with steel limbs, wood stock, and a loaded bolt")}>Crossbow</button>
                <button className="preset-pill" onClick={() => selectPreset("Straight hunting arrow with white fletching and a steel tip")}>Arrow</button>
                <button className="preset-pill" onClick={() => selectPreset("Short crossbow bolt with black fletching and a sharp steel tip")}>Bolt</button>
                <button className="preset-pill" onClick={() => selectPreset("Arcane magic staff with an orb head, darkwood shaft, and glowing blue crystal")}>Magic Staff</button>
                <button className="preset-pill" onClick={() => selectPreset("Wizard wand with a purple gem tip and polished wood shaft")}>Wand</button>
                <button className="preset-pill" onClick={() => selectPreset("Magical crystal orb on a brass stand with a blue glow")}>Orb</button>
              </div>
            </div>

            <div className="presets-group">
              <span className="presets-group-label">🛡️ Armor & Equipment</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Ornate knight heater shield with brass rim, steel center boss")}>Shield</button>
                <button className="preset-pill" onClick={() => selectPreset("Ornate knight steel helmet with a red top crest plume")}>Helmet</button>
                <button className="preset-pill" onClick={() => selectPreset("Polished steel knight chestplate with layered faulds and broad shoulder guards")}>Chestplate</button>
                <button className="preset-pill" onClick={() => selectPreset("Pair of heavy steel gauntlets with layered plate fingers and leather straps")}>Gauntlets</button>
                <button className="preset-pill" onClick={() => selectPreset("Pair of rugged leather travel boots with reinforced soles and tall cuffs")}>Boots</button>
                <button className="preset-pill" onClick={() => selectPreset("Canvas adventurer backpack with leather straps and a rolled bedroll on top")}>Backpack</button>
                <button className="preset-pill" onClick={() => selectPreset("Wide brown leather belt with a polished brass buckle")}>Belt</button>
                <button className="preset-pill" onClick={() => selectPreset("Small leather belt pouch with a brass clasp flap")}>Pouch</button>
                <button className="preset-pill" onClick={() => selectPreset("Long royal red cape with a decorative brass clasp at the neck")}>Cape</button>
              </div>
            </div>

            <div className="presets-group">
              <span className="presets-group-label">🏕️ Survival / Camping</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("A-frame canvas tent with a wooden ridge pole and open front flap")}>Tent</button>
                <button className="preset-pill" onClick={() => selectPreset("Lit campfire with stacked logs, stone ring, and bright orange flames")}>Campfire</button>
                <button className="preset-pill" onClick={() => selectPreset("Padded blue sleeping bag with a rounded hood and soft lofted body")}>Sleeping Bag</button>
                <button className="preset-pill" onClick={() => selectPreset("Black iron camping lantern with glass panels and a warm flame inside")}>Lantern</button>
                <button className="preset-pill" onClick={() => selectPreset("Medieval iron-bound wall torch with a large burning flame")}>Torch</button>
                <button className="preset-pill" onClick={() => selectPreset("Heavy iron cooking pot with side handles and a fitted lid")}>Cooking Pot</button>
                <button className="preset-pill" onClick={() => selectPreset("Industrial cargo storage crate, 1.5m width and metal frame")}>Crate</button>
                <button className="preset-pill" onClick={() => selectPreset("Old weathered whiskey barrel, 0.5m radius and 1.2m height")}>Barrel</button>
                <button className="preset-pill" onClick={() => selectPreset("Large wooden supply box with rope handles and reinforced lid")}>Supply Box</button>
              </div>
            </div>

            <div className="presets-group">
              <span className="presets-group-label">🏰 Medieval</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Stone castle wall section with crenellated battlements and heavy masonry blocks")}>Castle Wall</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall round stone tower with a battlement crown and narrow medieval silhouette")}>Tower</button>
                <button className="preset-pill" onClick={() => selectPreset("Massive wooden drawbridge with iron chains and heavy plank decking")}>Drawbridge</button>
                <button className="preset-pill" onClick={() => selectPreset("Grand carved wooden throne with tall backrest, gold trim, and red cushion")}>Throne</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall royal banner with deep blue cloth hanging from a wooden pole")}>Banner</button>
                <button className="preset-pill" onClick={() => selectPreset("Wooden medieval market stall with striped canopy and sturdy merchant counter")}>Market Stall</button>
                <button className="preset-pill" onClick={() => selectPreset("Old stone village well with a gabled wooden roof")}>Well</button>
                <button className="preset-pill" onClick={() => selectPreset("Rustic wooden cart with tall side rails and large spoked wheels")}>Cart</button>
                <button className="preset-pill" onClick={() => selectPreset("Blacksmith anvil made of heavy forged iron with a clear horn and base")}>Anvil</button>
                <button className="preset-pill" onClick={() => selectPreset("Stone blacksmith forge with a chimney hood and a hot burning coal bed")}>Forge</button>
                <button className="preset-pill" onClick={() => selectPreset("Heavy iron-bound treasure chest with arched lid and brass lock")}>Chest</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Sci-Fi & Tech</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Futuristic control panel with angled console body and cyan screens")}>Control Panel</button>
                <button className="preset-pill" onClick={() => selectPreset("Wall mounted sci-fi terminal with green display panels and keypad")}>Terminal</button>
                <button className="preset-pill" onClick={() => selectPreset("Desktop computer setup with glowing blue monitor and tower")}>Computer</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall darksteel server rack with stacked units and green indicator lights")}>Server Rack</button>
                <button className="preset-pill" onClick={() => selectPreset("Compact energy cell canister with bright cyan glowing core")}>Energy Cell</button>
                <button className="preset-pill" onClick={() => selectPreset("Futuristic tech crate with armored panels and blue light strips")}>Tech Crate</button>
                <button className="preset-pill" onClick={() => selectPreset("Sliding space door with steel frame and blue side panel light")}>Space Door</button>
                <button className="preset-pill" onClick={() => selectPreset("Space station airlock chamber with two doors and control panel")}>Airlock</button>
                <button className="preset-pill" onClick={() => selectPreset("Automated defense turret with twin barrels and red sensor light")}>Turret</button>
                <button className="preset-pill" onClick={() => selectPreset("Compact quad drone with glowing cyan front sensor")}>Drone</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Industrial & City</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Long industrial steel pipe with heavy end flanges")}>Pipe</button>
                <button className="preset-pill" onClick={() => selectPreset("Industrial wheel valve with steel body and yellow handle")}>Valve</button>
                <button className="preset-pill" onClick={() => selectPreset("Large vertical industrial steel storage tank")}>Tank</button>
                <button className="preset-pill" onClick={() => selectPreset("Heavy power generator with exposed coils and yellow warning details")}>Generator</button>
                <button className="preset-pill" onClick={() => selectPreset("Warehouse conveyor belt with six rollers and steel frame")}>Conveyor Belt</button>
                <button className="preset-pill" onClick={() => selectPreset("Steel toolbox with lift handle and removable tray")}>Toolbox</button>
                <button className="preset-pill" onClick={() => selectPreset("Yellow warehouse forklift with raised forks and operator seat")}>Forklift</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall warehouse storage rack with four shelves")}>Storage Rack</button>
                <button className="preset-pill" onClick={() => selectPreset("Modern street lamp with dark steel pole and glass head")}>Street Lamp</button>
                <button className="preset-pill" onClick={() => selectPreset("Vertical traffic light with green active signal")}>Traffic Light</button>
                <button className="preset-pill" onClick={() => selectPreset("Rectangular white road sign on a metal pole")}>Road Sign</button>
                <button className="preset-pill" onClick={() => selectPreset("Urban street bench with wood slats and dark steel frame")}>Street Bench</button>
                <button className="preset-pill" onClick={() => selectPreset("Classic red post mailbox with a side flag")}>Mailbox</button>
                <button className="preset-pill" onClick={() => selectPreset("Green city trash can with lid and dark rim")}>Trash Can</button>
                <button className="preset-pill" onClick={() => selectPreset("Glass bus stop shelter with bench and steel frame")}>Bus Stop</button>
                <button className="preset-pill" onClick={() => selectPreset("Classic red phone booth with glass side panels")}>Phone Booth</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Vehicles</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Modern red sedan car with glass windows and four wheels")}>Car</button>
                <button className="preset-pill" onClick={() => selectPreset("Blue box truck with tall cargo body and heavy wheels")}>Truck</button>
                <button className="preset-pill" onClick={() => selectPreset("City bicycle with green frame and front basket")}>Bike</button>
                <button className="preset-pill" onClick={() => selectPreset("Orange sport motorcycle with windshield and exposed frame")}>Motorcycle</button>
                <button className="preset-pill" onClick={() => selectPreset("Green farm tractor with large rear wheels and enclosed cab")}>Tractor</button>
                <button className="preset-pill" onClick={() => selectPreset("Armored military battle tank with olive body and angular turret")}>Battle Tank</button>
                <button className="preset-pill" onClick={() => selectPreset("White motorboat with steering console and clean fiberglass hull")}>Boat</button>
                <button className="preset-pill" onClick={() => selectPreset("Wooden canoe with two seats and narrow hull")}>Canoe</button>
                <button className="preset-pill" onClick={() => selectPreset("Large cargo ship with raised bridge and long steel hull")}>Ship</button>
                <button className="preset-pill" onClick={() => selectPreset("White jet plane with wide wings and twin engines")}>Plane</button>
                <button className="preset-pill" onClick={() => selectPreset("Gray helicopter with main rotor, tail boom, and landing skids")}>Helicopter</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Animals</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Brown dog with sturdy body, tail, and clear muzzle")}>Dog</button>
                <button className="preset-pill" onClick={() => selectPreset("Orange cat with long tail and pointed ears")}>Cat</button>
                <button className="preset-pill" onClick={() => selectPreset("Brown horse with long legs and dark mane")}>Horse</button>
                <button className="preset-pill" onClick={() => selectPreset("White cow with sturdy body and short horns")}>Cow</button>
                <button className="preset-pill" onClick={() => selectPreset("Tan deer with slim legs and tall antlers")}>Deer</button>
                <button className="preset-pill" onClick={() => selectPreset("Gray wolf with long tail and alert head")}>Wolf</button>
                <button className="preset-pill" onClick={() => selectPreset("Blue bird perched with folded wings and small beak")}>Bird</button>
                <button className="preset-pill" onClick={() => selectPreset("Silver fish with top fin and forked tail")}>Fish</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Characters</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Stylized male character with blue outfit")}>Male</button>
                <button className="preset-pill" onClick={() => selectPreset("Stylized female character with red outfit")}>Female</button>
                <button className="preset-pill" onClick={() => selectPreset("Small child character with green outfit")}>Child</button>
                <button className="preset-pill" onClick={() => selectPreset("Elder character with staff and brown robe")}>Elder</button>
                <button className="preset-pill" onClick={() => selectPreset("Merchant character with green clothes, hat, and pouch")}>Merchant</button>
                <button className="preset-pill" onClick={() => selectPreset("Town guard with blue uniform, spear, and shield")}>Guard</button>
                <button className="preset-pill" onClick={() => selectPreset("Farmer character with brown clothes and hat")}>Farmer</button>
                <button className="preset-pill" onClick={() => selectPreset("Blacksmith with brown apron, beard, and hammer")}>Blacksmith</button>
                <button className="preset-pill" onClick={() => selectPreset("Soldier with red uniform, shield, and sword")}>Soldier</button>
                <button className="preset-pill" onClick={() => selectPreset("Fantasy elf with green outfit, tall ears, and staff")}>Elf</button>
                <button className="preset-pill" onClick={() => selectPreset("Fantasy orc warrior with broad shoulders and tusks")}>Orc</button>
                <button className="preset-pill" onClick={() => selectPreset("Small goblin with pointed ears and rough clothes")}>Goblin</button>
                <button className="preset-pill" onClick={() => selectPreset("Stout dwarf with beard, hammer, and blue clothing")}>Dwarf</button>
                <button className="preset-pill" onClick={() => selectPreset("Large green dragon with wings and long tail")}>Dragon</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Loot & Collectibles</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Gold coin with raised center stamp")}>Coin</button>
                <button className="preset-pill" onClick={() => selectPreset("Purple crystal gem with faceted shape")}>Gem</button>
                <button className="preset-pill" onClick={() => selectPreset("Golden key with ring handle and toothed bit")}>Key</button>
                <button className="preset-pill" onClick={() => selectPreset("Ancient tied scroll with rolled paper ends")}>Scroll</button>
                <button className="preset-pill" onClick={() => selectPreset("Blue potion bottle with glass body and cork stopper")}>Potion</button>
                <button className="preset-pill" onClick={() => selectPreset("Treasure chest with wooden body, gold bands, and jewel on top")}>Treasure Chest</button>
                <button className="preset-pill" onClick={() => selectPreset("Mystic artifact obelisk on a stone base")}>Artifact</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Environment Pieces</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Terrain patch with grassy ground, dirt base, and raised mounds")}>Terrain</button>
                <button className="preset-pill" onClick={() => selectPreset("Rounded grassy hill with dirt base")}>Hill</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall rocky mountain with sharp central peak")}>Mountain</button>
                <button className="preset-pill" onClick={() => selectPreset("Rock cliff face with layered ledges")}>Cliff</button>
                <button className="preset-pill" onClick={() => selectPreset("Wide valley with two grassy slopes and lower center floor")}>Valley</button>
                <button className="preset-pill" onClick={() => selectPreset("Rock cave entrance with dark opening and stone sides")}>Cave</button>
                <button className="preset-pill" onClick={() => selectPreset("Square ground tile with dirt base and grass top")}>Ground Tile</button>
                <button className="preset-pill" onClick={() => selectPreset("Road tile with asphalt surface and yellow center line")}>Road Tile</button>
                <button className="preset-pill" onClick={() => selectPreset("Path tile with dirt walking strip through grass")}>Path Tile</button>
                <button className="preset-pill" onClick={() => selectPreset("River tile with grassy banks and a water channel through the middle")}>River Tile</button>
                <button className="preset-pill" onClick={() => selectPreset("Dungeon tile made of stone blocks with dark grooves")}>Dungeon Tile</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">2D Game Backgrounds</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("2D game background with layered forest silhouettes, mist, and a warm sunset sky for a side scrolling platformer")}>Forest Sunset</button>
                <button className="preset-pill" onClick={() => selectPreset("2D game background with a neon city skyline, glowing windows, rooftop antennas, and a moonlit night sky")}>Night City</button>
                <button className="preset-pill" onClick={() => selectPreset("2D desert game background with sandstone mesas, rolling dunes, and a bright daytime sky")}>Desert</button>
                <button className="preset-pill" onClick={() => selectPreset("2D cave platformer background with layered stalactites, glowing crystals, and deep shadowy rock forms")}>Cave</button>
                <button className="preset-pill" onClick={() => selectPreset("2D snowy mountain background with layered pine ridges, icy peaks, and a pale dawn sky")}>Snow Peaks</button>
                <button className="preset-pill" onClick={() => selectPreset("2D space shooter background with distant planets, nebula clouds, stars, and drifting asteroid silhouettes")}>Space</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">🛁 Bathroom Fixtures</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Ceramic toilet with elongated bowl, water tank, white finish, lid closed")}>Toilet</button>
                <button className="preset-pill" onClick={() => selectPreset("Elegant freestanding oval bathtub with faucet, glossy white ceramic, 160cm length")}>Bathtub</button>
                <button className="preset-pill" onClick={() => selectPreset("Corner shower enclosure with glass doors, fixture column, rain showerhead")}>Shower</button>
                <button className="preset-pill" onClick={() => selectPreset("Freestanding pedestal sink vanity bowl with standard chrome faucet, 70cm width")}>Pedestal Sink</button>
                <button className="preset-pill" onClick={() => selectPreset("Wall mounted bathroom vanity basin with exposed chrome P-trap pipe and faucet")}>Wall-mounted Sink</button>
                <button className="preset-pill" onClick={() => selectPreset("Oval bathroom wall mirror with gold metallic border frame, 60cm wide")}>Oval Wall Mirror</button>
                <button className="preset-pill" onClick={() => selectPreset("Double bar chrome towel rack with hanging blue towels draped over it")}>Towel Rack</button>
                <button className="preset-pill" onClick={() => selectPreset("White lacquer bathroom storage cabinet with door handles and an open towel rack shelf underneath")}>Bathroom Cabinet</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Forest / Trees</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Oak tree with a thick trunk, spreading branches, and a dense rounded canopy")}>Oak Tree</button>
                <button className="preset-pill" onClick={() => selectPreset("Pine tree with a straight trunk and layered cone-shaped needle foliage")}>Pine Tree</button>
                <button className="preset-pill" onClick={() => selectPreset("Birch tree with white bark, thin branches, and a light leafy canopy")}>Birch Tree</button>
                <button className="preset-pill" onClick={() => selectPreset("Palm tree with a curved trunk and wide feather-like leaves at the top")}>Palm Tree</button>
                <button className="preset-pill" onClick={() => selectPreset("Dead tree with a rough trunk and twisted bare branches")}>Dead Tree</button>
                <button className="preset-pill" onClick={() => selectPreset("Young sapling with a thin trunk and a few leaves")}>Sapling</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Ground Cover</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Dense patch of grass with thin green blades growing from the ground")}>Grass</button>
                <button className="preset-pill" onClick={() => selectPreset("Rounded bush with dense leaves and short branching stems")}>Bush</button>
                <button className="preset-pill" onClick={() => selectPreset("Woody shrub with multiple stems and compact leafy growth")}>Shrub</button>
                <button className="preset-pill" onClick={() => selectPreset("Fern plant with long arching fronds and repeating leaf segments")}>Fern</button>
                <button className="preset-pill" onClick={() => selectPreset("Small flower with a stem, leaves, and a bright bloom")}>Flower</button>
                <button className="preset-pill" onClick={() => selectPreset("Soft green moss patch covering the ground like a cushion")}>Moss</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Rocks & Cliffs</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Small irregular rock with rough natural edges")}>Small Rock</button>
                <button className="preset-pill" onClick={() => selectPreset("Large boulder with a rounded jagged shape and heavy stone mass")}>Boulder</button>
                <button className="preset-pill" onClick={() => selectPreset("Rock cluster made of multiple stones grouped in a natural formation")}>Rock Cluster</button>
                <button className="preset-pill" onClick={() => selectPreset("Cliff section with a tall fractured rock face and layered geological edges")}>Cliff Section</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Natural Props</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Fallen log made from a horizontal tree trunk with visible cut ends")}>Log</button>
                <button className="preset-pill" onClick={() => selectPreset("Tree stump showing the cut base of a broken tree trunk")}>Tree Stump</button>
                <button className="preset-pill" onClick={() => selectPreset("Fallen tree lying on its side with branches and some remaining foliage")}>Fallen Tree</button>
                <button className="preset-pill" onClick={() => selectPreset("Mushroom with a stem and umbrella-shaped cap")}>Mushroom</button>
                <button className="preset-pill" onClick={() => selectPreset("Climbing vine with a long flexible stem and leaves")}>Vine</button>
                <button className="preset-pill" onClick={() => selectPreset("Exposed tree root with thick branching forms above the soil")}>Root</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Water Features</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Small pond with still water surrounded by natural banks")}>Pond</button>
                <button className="preset-pill" onClick={() => selectPreset("River segment with flowing water and visible banks along its sides")}>River Segment</button>
                <button className="preset-pill" onClick={() => selectPreset("Waterfall dropping over a rocky cliff into a pool below")}>Waterfall</button>
                <button className="preset-pill" onClick={() => selectPreset("Narrow winding stream with shallow flowing water")}>Stream</button>
              </div>
            </div>
            <div className="presets-group">
              <span className="presets-group-label">Architecture</span>
              <div className="presets-row">
                <button className="preset-pill" onClick={() => selectPreset("Brick wall section with plaster trim and a centered window opening")}>Wall</button>
                <button className="preset-pill" onClick={() => selectPreset("Large wood floor slab with visible plank divisions and solid structure")}>Floor</button>
                <button className="preset-pill" onClick={() => selectPreset("Flat plaster ceiling panel with neat perimeter trim")}>Ceiling</button>
                <button className="preset-pill" onClick={() => selectPreset("Gabled roof with clay tiles, balanced slope, and visible overhang")}>Roof</button>
                <button className="preset-pill" onClick={() => selectPreset("Stone pillar with a cylindrical shaft, wide base, and decorative capital")}>Pillar</button>
                <button className="preset-pill" onClick={() => selectPreset("Long structural wood beam with a sturdy rectangular profile")}>Beam</button>
                <button className="preset-pill" onClick={() => selectPreset("Concrete foundation slab with embedded footings for a house base")}>Foundation</button>
                <button className="preset-pill" onClick={() => selectPreset("Wood entry door with inset panels, frame, and metal handle")}>Door</button>
                <button className="preset-pill" onClick={() => selectPreset("Rectangular window with aluminum frame, clear glass, mullions, and a sill")}>Window</button>
                <button className="preset-pill" onClick={() => selectPreset("Stone archway with sturdy side supports and a curved upper arch")}>Archway</button>
                <button className="preset-pill" onClick={() => selectPreset("Iron gate with vertical bars inside a strong framed opening")}>Gate</button>
                <button className="preset-pill" onClick={() => selectPreset("Wide staircase with even steps and a side railing")}>Stairs</button>
                <button className="preset-pill" onClick={() => selectPreset("Tall wooden ladder with evenly spaced rungs")}>Ladder</button>
                <button className="preset-pill" onClick={() => selectPreset("Concrete access ramp with a gentle incline and side curbs")}>Ramp</button>
                <button className="preset-pill" onClick={() => selectPreset("Long wooden bridge with support pillars and side railings")}>Bridge</button>
                <button className="preset-pill" onClick={() => selectPreset("Projected balcony with a concrete slab and protective railings")}>Balcony</button>
                <button className="preset-pill" onClick={() => selectPreset("Wood picket fence with repeated vertical sections and posts")}>Fence</button>
                <button className="preset-pill" onClick={() => selectPreset("Steel safety railing with evenly spaced balusters and a top rail")}>Railing</button>
                <button className="preset-pill" onClick={() => selectPreset("Brick chimney shaft with a protective cap on top")}>Chimney</button>
                <button className="preset-pill" onClick={() => selectPreset("Covered front porch with a platform, support pillars, roof, and entry steps")}>Porch</button>
              </div>
            </div>
          </div>
        )}

          {/* Error Message Box */}
          {error && (
            <div className="error-box">
              <strong>Error:</strong> {error}
            </div>
          )}
        </section>
        )}

        {/* Workspace Mode Tabs */}
        <div className="view-tabs">
          <button 
            type="button"
            className={`view-tab-btn ${activeTab === 'single' ? 'active' : ''}`}
            onClick={() => setActiveTab('single')}
          >
            <span>Single Asset View</span>
          </button>
          <button 
            type="button"
            className={`view-tab-btn ${activeTab === 'room' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('room');
              // Auto initialize active assets with all completed assets if none are active yet
              if (activeRoomAssets.length === 0) {
                const completed = assets.filter(a => a.status === 'completed');
                setActiveRoomAssets(completed.map(a => a.id));
              }
            }}
          >
            <SparklesIcon />
            <span>3D Room Designer</span>
          </button>
        </div>

        {/* Dynamic Viewport and Parameters Section */}
        <section className="viewport-section">
          {activeTab === 'single' ? (
            selectedAsset ? (
              <>
                {/* Left Viewport - 3D Viewer or Status */}
                <div className="viewport-3d">
                  {selectedAsset.status === 'completed' ? (
                    // Model-viewer web component for 3D navigation
                    <model-viewer
                      ref={modelViewerRef}
                      src={`${API_BASE_URL}${selectedAsset.glb_path}`}
                      poster={`${API_BASE_URL}${selectedAsset.render_path}`}
                      alt={selectedAsset.prompt}
                      auto-rotate
                      camera-controls
                      shadow-intensity="1"
                      shadow-softness="0.5"
                      style={{ width: '100%', height: '100%', outline: 'none' }}
                    />
                  ) : selectedAsset.status === 'generating' ? (
                    <div className="status-overlay">
                      <div className="loading-spinner-ring"></div>
                      <h2>Generating Procedural Geometry...</h2>
                      <p style={{ color: 'var(--text-secondary)' }}>
                        Blender is running headlessly to construct the meshes, apply materials, frame the camera, and render preview image.
                      </p>
                      <div className="generation-step-list">
                        <div className="generation-step done">✓ Translated prompt into parameters</div>
                        <div className="generation-step active"><span className="pulse-dot"></span> Headless Blender executing...</div>
                        <div className="generation-step">○ Exporting GLB model</div>
                        <div className="generation-step">○ Rendering preview PNG</div>
                      </div>
                    </div>
                  ) : (
                    <div className="status-overlay" style={{ color: 'var(--error)' }}>
                      <WarningIcon />
                      <h2 style={{ marginTop: '10px' }}>Generation Failed</h2>
                      <p style={{ color: 'var(--text-secondary)', maxWidth: '400px' }}>
                        Blender script encountered a runtime error during procedural execution. See details in the right sidebar.
                      </p>
                    </div>
                  )}
                </div>

                {/* Right Sidebar - Details and Specs */}
                <div className="details-panel">
                  <div className="details-header">
                    <span className="details-title">Asset Specifications</span>
                  </div>
                  
                  <div className="params-details">
                    <h4 style={{ marginBottom: '14px', fontSize: '14px', fontWeight: '600' }}>
                      Type: <span className="param-tag">{selectedAsset.asset_type}</span>
                    </h4>
                    
                    {selectedAsset.status === 'failed' && selectedAsset.error_message && (
                      <div>
                        <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--error)', marginBottom: '4px' }}>
                          Error Log:
                        </div>
                        <div className="error-box" style={{ marginTop: 0 }}>
                          {selectedAsset.error_message}
                        </div>
                      </div>
                    )}

                    {selectedAsset.parameters && (
                      <div className="params-grid">
                        <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                          Parameters Extracted:
                        </div>
                        {Object.entries(selectedAsset.parameters).map(([key, val]) => {
                          if (key === 'asset_type') return null;
                          if (key === 'custom_color') {
                            return (
                              <div key={key} className="param-row">
                                <span className="param-name">custom color</span>
                                <span className="param-value" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                  <span style={{
                                    display: 'inline-block',
                                    width: '12px',
                                    height: '12px',
                                    borderRadius: '50%',
                                    backgroundColor: String(val),
                                    border: '1px solid rgba(255,255,255,0.2)'
                                  }}></span>
                                  {String(val).toUpperCase()}
                                </span>
                              </div>
                            );
                          }
                          const keysWithoutUnits = [
                            'arms', 'seats', 'drawers', 'shelves', 'burners', 
                            'stools_count', 'chair_count', 'doors', 'drawers_rows', 
                            'drawers_cols', 'num_shelves', 'num_legs', 'compartments'
                          ];
                          return (
                            <div key={key} className="param-row">
                              <span className="param-name">{key.replace('_', ' ')}</span>
                              <span className="param-value">
                                {typeof val === 'number' 
                                  ? keysWithoutUnits.includes(key)
                                    ? String(val)
                                    : selectedAsset.asset_type === 'barrel' || selectedAsset.asset_type === 'crate'
                                      ? `${val} m`
                                      : `${val} cm`
                                  : String(val)
                                }
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    )}

                    {/* Real-time Color Customizer */}
                    {selectedAsset.status === 'completed' && (
                      <div className="color-customizer-panel" style={{ borderTop: 'none', padding: '16px 0 0 0' }}>
                        <div className="section-divider"></div>
                        <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                          Real-time Color Picker:
                        </div>
                        <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '12px' }}>
                          Adjust the primary color instantly, or leave it alone to keep the asset's original materials.
                        </p>
                        <div className="realtime-color-row">
                          <input 
                            type="color" 
                            value={customColor || selectedAsset.parameters?.custom_color || '#cbd5e1'} 
                            onChange={(e) => setCustomColor(e.target.value)}
                            className="realtime-color-input"
                          />
                          <span className="color-hex-label">
                            {(customColor || selectedAsset.parameters?.custom_color || '#CBD5E1').toUpperCase()}
                          </span>
                          <button
                            type="button"
                            className="secondary-action-btn"
                            onClick={() => setCustomColor('')}
                            style={{ padding: '8px 10px', minWidth: 'fit-content' }}
                          >
                            Original
                          </button>
                          <button 
                            type="button"
                            className="bake-now-btn"
                            title="Bake this color into a new model"
                            onClick={handleBakeColor}
                            disabled={isGenerating}
                          >
                            Bake Color
                          </button>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Footer Download / Action Buttons */}
                  <div className="actions-footer">
                    {selectedAsset.status === 'completed' && (
                      <>
                        <a 
                          href={`${API_BASE_URL}${selectedAsset.glb_path}`} 
                          download={`asset_${selectedAsset.id}.glb`} 
                          style={{ textDecoration: 'none' }}
                        >
                          <button className="download-btn" style={{ width: '100%' }}>
                            <DownloadIcon />
                            Download GLB
                          </button>
                        </a>
                        <button
                          type="button"
                          className="secondary-action-btn"
                          onClick={handleExportSelectedAssetToPrint}
                          disabled={isExportingPrintAsset}
                          style={{ width: '100%' }}
                        >
                          <DownloadIcon />
                          {isExportingPrintAsset ? 'Preparing STL...' : 'Download STL for 3D Print'}
                        </button>
                      </>
                    )}
                    
                    <button 
                      type="button"
                      className="secondary-action-btn delete"
                      onClick={() => handleDelete(selectedAsset.id)}
                    >
                      <TrashIcon />
                      Delete Record
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <div className="empty-viewport">
                <div className="empty-viewport-icon">
                  <CrateIcon />
                </div>
                <h2>No Asset Selected</h2>
                <p style={{ maxWidth: '300px' }}>
                  Select an asset from the sidebar list or type a prompt above to generate a new one.
                </p>
              </div>
            )
          ) : activeTab === 'movie' ? (
            <MovieProductionPanel />
          ) : activeTab === 'game' ? (
            <GameAssetStudio generatedAssets={assets} apiBaseUrl={API_BASE_URL} />
          ) : activeTab === 'city' ? (
            <div className={`city-planner-container city-planner-3d ${cityRotoscopeMode ? 'rotoscope-mode' : ''}`}>
              <aside className="city-tool-panel">
                <div className="city-panel-header">
                  <span className="city-panel-kicker">3D Blender city grid</span>
                  <h2>City Planner</h2>
                  <p>
                    Select a 3D road, building, house, or street light asset, then click any block on the 20 by 20 city grid.
                  </p>
                </div>

                <div className="city-tool-groups">
                  {CITY_TOOL_GROUPS.map((group) => (
                    <div className="city-tool-group" key={group.title}>
                      <div className="city-tool-group-title">
                        <span>{group.title}</span>
                        <small>{group.description}</small>
                      </div>
                      <div className="city-tool-list">
                        {group.tools.map((tool) => (
                          <button
                            key={tool.id}
                            type="button"
                            className={`city-tool-button ${citySelectedTool === tool.id ? 'active' : ''}`}
                            onClick={() => handleCityToolSelect(tool.id)}
                          >
                            <CityTile3D toolId={tool.id} compact rotoscope={cityRotoscopeMode} />
                            <span>{tool.label}</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>

                <button
                  type="button"
                  className="secondary-action-btn city-reset-btn"
                  onClick={handleClearCityGrid}
                >
                  <TrashIcon />
                  Clear / Reset Canvas
                </button>
              </aside>

              <section className="city-canvas-panel">
                <div className="city-canvas-toolbar">
                  <div>
                    <span className="city-panel-kicker">3D placement blocks</span>
                    <h3>Rotoscope-Ready City Layout</h3>
                  </div>
                  <div className="city-stat-row">
                    <span>{cityStats.roads} road tiles</span>
                    <span>{cityStats.buildings} buildings</span>
                    <span>{cityStats.lights} lights</span>
                    <span>{cityRotoscopeMode ? 'Rotoscope outlines on' : 'Rotoscope outlines off'}</span>
                  </div>
                </div>

                <div className="city-grid-shell city-grid-shell-3d">
                  <div
                    className="city-grid city-grid-3d"
                    style={{ gridTemplateColumns: `repeat(${CITY_GRID_SIZE}, minmax(0, 1fr))` }}
                    aria-label="20 by 20 3D city layout grid"
                  >
                    {cityGrid.map((row, rowIndex) =>
                      row.map((cell, colIndex) => {
                        const hasContent = cell.road || cell.building || cell.light;
                        const isSelected = citySelectedCell?.row === rowIndex && citySelectedCell?.col === colIndex;
                        return (
                          <button
                            key={`${rowIndex}-${colIndex}`}
                            type="button"
                            className={`city-grid-cell ${hasContent ? 'filled' : ''} ${isSelected ? 'selected' : ''}`}
                            onClick={() => handleCityCellClick(rowIndex, colIndex)}
                            aria-label={`3D city cell row ${rowIndex + 1}, column ${colIndex + 1}: ${getCityCellLabel(cell)}`}
                            title={`Row ${rowIndex + 1}, Column ${colIndex + 1}: ${getCityCellLabel(cell)}`}
                          >
                            <CityTile3D cell={cell} selected={isSelected} rotoscope={cityRotoscopeMode} />
                          </button>
                        );
                      })
                    )}
                  </div>
                </div>

                <div className="city-status-bar">
                  <span>{cityPlannerMessage}</span>
                  <strong>Selected: {CITY_TOOL_LABELS[citySelectedTool]}</strong>
                </div>
              </section>

              <aside className="city-auto-panel">
                <div className="details-header">
                  <span className="details-title">3D City Controls</span>
                </div>
                <div className="city-auto-body">
                  <p>
                    Export downloads a real Blender `.blend` city with separate named roads, buildings, houses, shops, towers, and street lights.
                  </p>

                  <label className="city-inline-toggle">
                    <input
                      type="checkbox"
                      checked={cityRotoscopeMode}
                      onChange={(e) => setCityRotoscopeMode(e.target.checked)}
                    />
                    <span>Rotoscope outlines for whole city</span>
                  </label>

                  <button
                    type="button"
                    className="download-btn city-export-btn"
                    onClick={handleSaveCityToBlender}
                    disabled={isExportingCityBlend}
                  >
                    <SparklesIcon />
                    {isExportingCityBlend ? 'Building .blend...' : 'Download Blender City File'}
                  </button>

                  <div className="city-selected-card">
                    <strong>Selected Block</strong>
                    {selectedCityCellData ? (
                      <>
                        <span>
                          Row {citySelectedCell.row + 1}, Column {citySelectedCell.col + 1}: {getCityCellLabel(selectedCityCellData)}
                        </span>
                        <label className="city-control-label">
                          <span>Lift Up / Elevation {Number(selectedCityCellData.elevation || 0).toFixed(1)} m</span>
                          <input
                            type="range"
                            min="0"
                            max="4"
                            step="0.1"
                            value={selectedCityCellData.elevation || 0}
                            onChange={(e) => handleSelectedCityCellChange('elevation', Number(e.target.value))}
                          />
                        </label>
                        <label className="city-control-label">
                          <span>Rotation {Math.round(selectedCityCellData.rotation || 0)}°</span>
                          <input
                            type="range"
                            min="0"
                            max="270"
                            step="90"
                            value={selectedCityCellData.rotation || 0}
                            onChange={(e) => handleSelectedCityCellChange('rotation', Number(e.target.value))}
                          />
                        </label>
                        <label className="city-control-label">
                          <span>Building Height Scale {Number(selectedCityCellData.heightScale || 1).toFixed(1)}x</span>
                          <input
                            type="range"
                            min="0.5"
                            max="2"
                            step="0.1"
                            value={selectedCityCellData.heightScale || 1}
                            onChange={(e) => handleSelectedCityCellChange('heightScale', Number(e.target.value))}
                            disabled={!selectedCityCellData.building}
                          />
                        </label>
                      </>
                    ) : (
                      <span>Click a city block to edit its lift, rotation, and building height.</span>
                    )}
                  </div>

                  <div className="city-auto-note">
                    <strong>Rotoscope-friendly export:</strong>
                    <span>
                      The `.blend` uses named collections for roads, buildings, lights, and ground, with Freestyle outlines enabled.
                    </span>
                  </div>

                  <div className="city-control-divider" />

                  <p>
                    Set how many street lights you want, then let the planner find every road tile and spread them out evenly.
                  </p>

                  <label className="city-control-label">
                    <span>Street Light Count</span>
                    <div className="city-light-count-row">
                      <input
                        type="range"
                        min={CITY_LIGHT_MIN}
                        max={CITY_LIGHT_MAX}
                        value={cityLightCount}
                        onChange={(e) => setCityLightCount(clampCityLightCount(e.target.value))}
                      />
                      <input
                        type="number"
                        min={CITY_LIGHT_MIN}
                        max={CITY_LIGHT_MAX}
                        value={cityLightCount}
                        onChange={(e) => setCityLightCount(clampCityLightCount(e.target.value))}
                      />
                    </div>
                  </label>

                  <label className="city-control-label">
                    <span>Light Style</span>
                    <select
                      value={cityLightStyle}
                      onChange={(e) => setCityLightStyle(e.target.value)}
                      className="city-select"
                    >
                      <option value="mixed">Mixed Classic + Modern</option>
                      <option value="classic">Classic Pole</option>
                      <option value="modern">Modern LED</option>
                    </select>
                  </label>

                  <button
                    type="button"
                    className="download-btn"
                    onClick={handleAutoPlaceCityLights}
                    style={{ width: '100%' }}
                  >
                    <SparklesIcon />
                    Auto-Place Lights
                  </button>

                  <div className="city-auto-note">
                    <strong>How it works:</strong>
                    <span>
                      Roads are detected from the canvas. Existing lights are replaced so the requested count stays accurate.
                    </span>
                  </div>

                  <div className="city-mini-preview">
                    <CityTile3D toolId="road_intersection" rotoscope={cityRotoscopeMode} />
                    <CityTile3D toolId="building_house" rotoscope={cityRotoscopeMode} />
                    <CityTile3D toolId="building_office" rotoscope={cityRotoscopeMode} />
                    <CityTile3D toolId="light_modern" rotoscope={cityRotoscopeMode} />
                  </div>
                </div>
              </aside>
            </div>
          ) : (
            /* Room Designer View */
            <div className="room-designer-container" style={{ display: 'flex', width: '100%', height: '100%', overflow: 'hidden' }}>
              {/* Left Canvas Panel */}
              <div className="room-canvas-container" style={{ flex: 1, height: '100%', position: 'relative' }}>
                <RoomViewer 
                  assets={assets} 
                  activeAssets={activeRoomAssets} 
                  wallColors={roomWallColors}
                  houseConfig={houseConfig}
                  layoutMode={effectiveRoomLayoutMode}
                  selectedAssetId={selectedRoomAssetId}
                  onSelectAsset={setSelectedRoomAssetId}
                  transforms={roomAssetTransforms}
                  onAssetMetadataChange={handleRoomAssetMaterialInfo}
                />
              </div>

              {/* Right Controls Panel */}
              <div className="details-panel" style={{ borderLeft: '1px solid var(--border-light)' }}>
                <div className="details-header">
                  <span className="details-title">
                    {isCityLayout ? 'City Planner' : isHouseLayout ? 'House Planner' : 'Room Settings'}
                  </span>
                </div>
                
                <div className="params-details room-details-scroll" style={{ display: 'flex', flexDirection: 'column', gap: '20px', flex: 1, overflowY: 'auto', padding: '20px', minHeight: 0 }}>
                  {/* Selected Object Customizer */}
                  {selectedRoomAssetId && (() => {
                    const selectedAssetDetail = assets.find(a => a.id === selectedRoomAssetId);
                    if (!selectedAssetDetail) return null;
                    const transform = roomAssetTransforms[selectedRoomAssetId] || {
                      posX: 0,
                      posY: 0,
                      posZ: 0,
                      rotY: 0,
                      scale: 1,
                      customColor: selectedAssetDetail.parameters?.custom_color || null,
                      detailColors: {}
                    };
                    const materialInfo = roomAssetMaterialInfo[selectedRoomAssetId] || {
                      materialRoles: [],
                      hasUnmappedPrimaryMaterials: true
                    };
                    const detailRoles = materialInfo.materialRoles || [];
                    const showBaseColorControl = detailRoles.length === 0 || materialInfo.hasUnmappedPrimaryMaterials;
                    
                    const handleTransformChange = (field, val) => {
                      setRoomAssetTransforms(prev => ({
                        ...prev,
                        [selectedRoomAssetId]: {
                          ...transform,
                          [field]: val
                        }
                      }));
                    };

                    const handleDetailColorChange = (roleKey, value) => {
                      setRoomAssetTransforms(prev => ({
                        ...prev,
                        [selectedRoomAssetId]: {
                          ...transform,
                          detailColors: {
                            ...(transform.detailColors || {}),
                            [roleKey]: value
                          }
                        }
                      }));
                    };

                    const handleBakeSelectedColor = async () => {
                      const bakedColor =
                        transform.customColor ||
                        selectedAssetDetail.parameters?.custom_color ||
                        '#cbd5e1';
                      setIsGenerating(true);
                      setError('');
                      try {
                        const res = await fetch(`${API_BASE_URL}/api/generate`, {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({ 
                            prompt: selectedAssetDetail.prompt,
                            custom_color: bakedColor
                          })
                        });
                        if (!res.ok) {
                          const errData = await res.json();
                          throw new Error(errData.detail || 'Generation failed.');
                        }
                        const newAsset = await res.json();
                        setAssets(prev => [newAsset, ...prev]);
                        setSelectedAsset(newAsset);
                        setShouldPoll(true);
                        showToast('Asset queued with new custom color!');
                      } catch (err) {
                        setError(err.message);
                      } finally {
                        setIsGenerating(false);
                      }
                    };

                    return (
                      <div className="selected-object-controls" style={{ backgroundColor: 'rgba(139, 92, 246, 0.04)', border: '1px solid rgba(139, 92, 246, 0.15)', borderRadius: '12px', padding: '14px', marginBottom: '10px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                          <span style={{ color: 'var(--primary-hover)' }}>{getAssetIcon(selectedAssetDetail.asset_type)}</span>
                          <span style={{ fontSize: '13px', fontWeight: '600', textTransform: 'capitalize', color: 'white' }}>
                            Selected: {formatAssetType(selectedAssetDetail.asset_type)}
                          </span>
                          <button 
                            type="button" 
                            style={{ marginLeft: 'auto', background: 'transparent', border: 'none', color: 'var(--text-muted)', fontSize: '11px', cursor: 'pointer' }}
                            onClick={() => setSelectedRoomAssetId(null)}
                          >
                            Deselect
                          </button>
                        </div>

                        {/* Position X Offset */}
                        <div style={{ marginBottom: '10px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                            <span>Position X (Left/Right)</span>
                            <span style={{ fontFamily: 'monospace' }}>{((transform.posX || 0)).toFixed(2)} m</span>
                          </div>
                          <input 
                            type="range" 
                            min={-roomPositionRangeX} 
                            max={roomPositionRangeX} 
                            step="0.05"
                            value={transform.posX || 0}
                            onChange={(e) => handleTransformChange('posX', parseFloat(e.target.value))}
                            style={{ width: '100%', accentColor: 'var(--primary)', height: '4px', cursor: 'pointer' }}
                          />
                        </div>

                        <div style={{ marginBottom: '10px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                            <span>Position Y (Up/Down)</span>
                            <span style={{ fontFamily: 'monospace' }}>{((transform.posY || 0)).toFixed(2)} m</span>
                          </div>
                          <input
                            type="range"
                            min="-0.5"
                            max={roomPositionRangeY}
                            step="0.05"
                            value={transform.posY || 0}
                            onChange={(e) => handleTransformChange('posY', parseFloat(e.target.value))}
                            style={{ width: '100%', accentColor: 'var(--primary)', height: '4px', cursor: 'pointer' }}
                          />
                        </div>

                        {/* Position Z Offset */}
                        <div style={{ marginBottom: '10px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                            <span>Position Z (Forward/Back)</span>
                            <span style={{ fontFamily: 'monospace' }}>{((transform.posZ || 0)).toFixed(2)} m</span>
                          </div>
                          <input 
                            type="range" 
                            min={-roomPositionRangeZ} 
                            max={roomPositionRangeZ} 
                            step="0.05"
                            value={transform.posZ || 0}
                            onChange={(e) => handleTransformChange('posZ', parseFloat(e.target.value))}
                            style={{ width: '100%', accentColor: 'var(--primary)', height: '4px', cursor: 'pointer' }}
                          />
                        </div>

                        {/* Rotation Y Offset */}
                        <div style={{ marginBottom: '12px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                            <span>Rotation Y</span>
                            <span style={{ fontFamily: 'monospace' }}>{Math.round(transform.rotY || 0)}°</span>
                          </div>
                          <input 
                            type="range" 
                            min="0" 
                            max="360" 
                            step="5"
                            value={transform.rotY || 0}
                            onChange={(e) => handleTransformChange('rotY', parseInt(e.target.value, 10))}
                            style={{ width: '100%', accentColor: 'var(--primary)', height: '4px', cursor: 'pointer' }}
                          />
                        </div>

                        {/* Scale */}
                        <div style={{ marginBottom: '12px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                            <span>Scale</span>
                            <span style={{ fontFamily: 'monospace' }}>{(transform.scale ?? 1).toFixed(2)}x</span>
                          </div>
                          <input 
                            type="range" 
                            min="0.1" 
                            max="3" 
                            step="0.05"
                            value={transform.scale ?? 1}
                            onChange={(e) => handleTransformChange('scale', parseFloat(e.target.value))}
                            style={{ width: '100%', accentColor: 'var(--primary)', height: '4px', cursor: 'pointer' }}
                          />
                        </div>

                        {showBaseColorControl && (
                          <div style={{ borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '10px' }}>
                            <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '6px' }}>Base Color:</div>
                            <div className="realtime-color-row" style={{ marginTop: 0 }}>
                              <input 
                                type="color" 
                                value={transform.customColor || selectedAssetDetail.parameters?.custom_color || '#cbd5e1'} 
                                onChange={(e) => handleTransformChange('customColor', e.target.value)}
                                className="realtime-color-input"
                              />
                              <span className="color-hex-label">
                                {(transform.customColor || selectedAssetDetail.parameters?.custom_color || '#CBD5E1').toUpperCase()}
                              </span>
                              <button 
                                type="button"
                                className="bake-now-btn"
                                title="Bake this color into a new model"
                                onClick={handleBakeSelectedColor}
                                disabled={isGenerating}
                                style={{ padding: '4px 10px', fontSize: '11px' }}
                              >
                                Bake Color
                              </button>
                            </div>
                            {detailRoles.length > 0 && (
                              <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '8px' }}>
                                This only affects any remaining main surfaces that are not already listed below as detail colors.
                              </p>
                            )}
                          </div>
                        )}

                        {detailRoles.length > 0 && (
                          <div style={{ borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '10px', marginTop: '12px' }}>
                            <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                              Detail Colors:
                            </div>
                            <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '10px' }}>
                              Fine-tune specific parts like pillows, blankets, cushions, frames, or metal accents when the model exposes them.
                            </p>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                              {detailRoles.map(role => {
                                const roleColor = (transform.detailColors && transform.detailColors[role.key]) || role.defaultColor || '#8b5cf6';
                                return (
                                  <div key={role.key} style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                    <div style={{ flex: 1, fontSize: '11px', color: 'var(--text-secondary)' }}>{role.label}</div>
                                    <input
                                      type="color"
                                      value={roleColor}
                                      onChange={(e) => handleDetailColorChange(role.key, e.target.value)}
                                      className="realtime-color-input"
                                    />
                                    <span className="color-hex-label" style={{ minWidth: '72px', textAlign: 'right' }}>
                                      {roleColor.toUpperCase()}
                                    </span>
                                  </div>
                                );
                              })}
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })()}
                  <div className="control-group">
                    <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                      Building Questions:
                    </div>
                    <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '12px' }}>
                      Tell the planner how many bedrooms, bathrooms, kitchens, and shared spaces you want, then choose whether you want a pure house layout or a city block with roads around it.
                    </p>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: '10px' }}>
                      {[
                        ['bedrooms', 'Bedrooms', 1, 6],
                        ['bathrooms', 'Bathrooms', 1, 6],
                        ['kitchens', 'Kitchens', 1, 3],
                        ['livingRooms', 'Living Rooms', 1, 3],
                        ['diningRooms', 'Dining Rooms', 0, 3],
                        ['ensuiteBathrooms', 'Attached Baths', 0, Math.min(houseConfig.bedrooms, houseConfig.bathrooms)],
                      ].map(([key, label, min, max]) => (
                        <label key={key} style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '11px', color: 'var(--text-secondary)' }}>
                          <span>{label}</span>
                          <input
                            type="number"
                            min={min}
                            max={max}
                            value={key === 'ensuiteBathrooms' && !houseConfig.attachBathroomToBedroom ? 0 : houseConfig[key]}
                            disabled={key === 'ensuiteBathrooms' && !houseConfig.attachBathroomToBedroom}
                            onChange={(e) => handleHouseConfigChange(key, parseInt(e.target.value, 10) || 0)}
                            style={{
                              backgroundColor: '#ffffff',
                              color: '#000000',
                              border: '1px solid var(--border-light)',
                              borderRadius: '8px',
                              padding: '8px 10px',
                              fontSize: '12px',
                            }}
                          />
                        </label>
                      ))}
                    </div>
                    <label style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '12px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                      <input
                        type="checkbox"
                        checked={houseConfig.attachBathroomToBedroom}
                        onChange={(e) => handleHouseConfigChange('attachBathroomToBedroom', e.target.checked)}
                        style={{ accentColor: 'var(--primary)' }}
                      />
                      Connect a bathroom directly to a bedroom
                    </label>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: '10px', marginTop: '12px' }}>
                      <button
                        type="button"
                        className={`preset-pill ${roomLayout === 'house' ? 'active' : ''}`}
                        style={{ width: '100%', justifyContent: 'center' }}
                        onClick={() => applyRoomLayoutPreset('house')}
                      >
                        Build House
                      </button>
                      <button
                        type="button"
                        className={`preset-pill ${roomLayout === 'city' ? 'active' : ''}`}
                        style={{ width: '100%', justifyContent: 'center' }}
                        onClick={() => applyRoomLayoutPreset('city')}
                      >
                        Build City Block
                      </button>
                    </div>
                  </div>

                  <div className="control-group">
                    <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                      City Block Roads:
                    </div>
                    <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '12px' }}>
                      Wrap the building with sidewalks and roads so the layout behaves more like a compact city plan.
                    </p>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: '10px' }}>
                      <label style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '11px', color: 'var(--text-secondary)' }}>
                        <span>Road Lanes</span>
                        <input
                          type="number"
                          min="1"
                          max="4"
                          value={houseConfig.roadLanes}
                          onChange={(e) => handleHouseConfigChange('roadLanes', parseInt(e.target.value, 10) || 1)}
                          style={{
                            backgroundColor: '#ffffff',
                            color: '#000000',
                            border: '1px solid var(--border-light)',
                            borderRadius: '8px',
                            padding: '8px 10px',
                            fontSize: '12px',
                          }}
                        />
                      </label>
                      <label style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '11px', color: 'var(--text-secondary)' }}>
                        <span>Sidewalk Width (m)</span>
                        <input
                          type="number"
                          min="0.8"
                          max="6"
                          step="0.1"
                          value={houseConfig.sidewalkWidth}
                          onChange={(e) => handleHouseConfigChange('sidewalkWidth', parseFloat(e.target.value) || 0.8)}
                          style={{
                            backgroundColor: '#ffffff',
                            color: '#000000',
                            border: '1px solid var(--border-light)',
                            borderRadius: '8px',
                            padding: '8px 10px',
                            fontSize: '12px',
                          }}
                        />
                      </label>
                      <label style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '11px', color: 'var(--text-secondary)' }}>
                        <span>Building Setback (m)</span>
                        <input
                          type="number"
                          min="0.8"
                          max="8"
                          step="0.1"
                          value={houseConfig.setbackWidth}
                          onChange={(e) => handleHouseConfigChange('setbackWidth', parseFloat(e.target.value) || 0.8)}
                          style={{
                            backgroundColor: '#ffffff',
                            color: '#000000',
                            border: '1px solid var(--border-light)',
                            borderRadius: '8px',
                            padding: '8px 10px',
                            fontSize: '12px',
                          }}
                        />
                      </label>
                      <label style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '22px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                        <input
                          type="checkbox"
                          checked={houseConfig.addCrosswalks}
                          onChange={(e) => handleHouseConfigChange('addCrosswalks', e.target.checked)}
                          style={{ accentColor: 'var(--primary)' }}
                        />
                        Add crosswalks
                      </label>
                    </div>
                    <button
                      type="button"
                      className={`preset-pill ${roomLayout === 'city' ? 'active' : ''}`}
                      style={{ width: '100%', marginTop: '12px', justifyContent: 'center' }}
                      onClick={() => applyRoomLayoutPreset('city')}
                    >
                      Apply City Roads
                    </button>
                  </div>

                  <div className="control-group">
                    <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                      Wall Colors:
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      {[
                        ['north', 'North / Front'],
                        ['south', 'South / Back'],
                        ['east', 'East / Right'],
                        ['west', 'West / Left'],
                        ['interior', 'Interior Walls'],
                      ].map(([wallKey, label]) => (
                        <div key={wallKey} className="realtime-color-row" style={{ marginTop: 0 }}>
                          <div style={{ flex: 1, fontSize: '11px', color: 'var(--text-secondary)' }}>{label}</div>
                          <input
                            type="color"
                            value={roomWallColors[wallKey]}
                            onChange={(e) => handleWallColorChange(wallKey, e.target.value)}
                            className="realtime-color-input"
                          />
                          <span className="color-hex-label" style={{ minWidth: '72px', textAlign: 'right' }}>
                            {roomWallColors[wallKey].toUpperCase()}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Layout Presets */}
                  <div className="control-group">
                    <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                      Layout Presets:
                    </div>
                    <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '10px' }}>
                      Whole House keeps everything indoors. City Block uses the same building plan, then wraps it with sidewalks, streets, and optional crosswalks.
                    </p>
                    <div className="presets-row" style={{ marginTop: '6px' }}>
                      <button 
                        type="button"
                        className={`preset-pill ${roomLayout === 'house' ? 'active' : ''}`}
                        onClick={() => applyRoomLayoutPreset('house')}
                      >
                        Whole House
                      </button>
                      <button 
                        type="button"
                        className={`preset-pill ${roomLayout === 'city' ? 'active' : ''}`}
                        onClick={() => applyRoomLayoutPreset('city')}
                      >
                        City Block
                      </button>
                      <button 
                        type="button"
                        className={`preset-pill ${roomLayout === 'all' ? 'active' : ''}`}
                        onClick={() => applyRoomLayoutPreset('all')}
                      >
                        Load All
                      </button>
                      <button 
                        type="button"
                        className={`preset-pill ${roomLayout === 'bedroom' ? 'active' : ''}`}
                        onClick={() => applyRoomLayoutPreset('bedroom')}
                      >
                        Bedroom
                      </button>
                      <button 
                        type="button"
                        className={`preset-pill ${roomLayout === 'living' ? 'active' : ''}`}
                        onClick={() => applyRoomLayoutPreset('living')}
                      >
                        Living Room
                      </button>
                      <button 
                        type="button"
                        className={`preset-pill ${roomLayout === 'kitchen' ? 'active' : ''}`}
                        onClick={() => applyRoomLayoutPreset('kitchen')}
                      >
                        Kitchen
                      </button>
                      <button 
                        type="button"
                        className={`preset-pill ${roomLayout === 'bathroom' ? 'active' : ''}`}
                        onClick={() => applyRoomLayoutPreset('bathroom')}
                      >
                        Bathroom
                      </button>
                      <button 
                        type="button"
                        className="preset-pill"
                        style={{ borderColor: 'rgba(244,63,94,0.3)', color: 'var(--error)' }}
                        onClick={() => applyRoomLayoutPreset('clear')}
                      >
                        Clear All
                      </button>
                    </div>
                  </div>

                  <div className="control-group">
                    <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                      Export Files:
                    </div>
                    <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '10px' }}>
                      Save this {layoutDisplayNameLower} layout as a `.blend` file with the placed assets, shell geometry, and your live color overrides.
                    </p>
                    <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '10px' }}>
                      Use STL when you want a 3D-printable file. STL keeps the geometry, but not the material colors.
                    </p>
                    <button
                      type="button"
                      className="download-btn"
                      onClick={handleSaveRoomToBlender}
                      disabled={isSavingRoom}
                      style={{ width: '100%' }}
                    >
                      <DownloadIcon />
                      {isSavingRoom
                        ? `Saving ${layoutDisplayName}...`
                        : `Save ${layoutDisplayName} for Blender`}
                    </button>
                    <button
                      type="button"
                      className="secondary-action-btn"
                      onClick={handleSaveRoomToPrint}
                      disabled={isExportingRoomPrint}
                      style={{ width: '100%', marginTop: '10px' }}
                    >
                      <DownloadIcon />
                      {isExportingRoomPrint
                        ? `Preparing ${layoutDisplayName} STL...`
                        : `Download ${layoutDisplayName} STL for 3D Print`}
                    </button>
                  </div>

                  {/* Asset checklist */}
                  <div className="control-group room-asset-picker" style={{ display: 'flex', flexDirection: 'column' }}>
                    <div style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                      {isCityLayout ? 'Place Assets in City Block:' : isHouseLayout ? 'Place Assets in House:' : 'Place Assets in Room:'}
                    </div>
                    <div className="asset-list room-asset-checklist" style={{ overflowY: 'auto', border: '1px solid var(--border-light)', borderRadius: '8px', padding: '8px', backgroundColor: 'rgba(0,0,0,0.2)' }}>
                      {assets.filter(a => a.status === 'completed').length === 0 ? (
                        <div style={{ color: 'var(--text-muted)', fontSize: '12px', textAlign: 'center', padding: '20px' }}>
                          No completed assets found. Generate assets above to place them!
                        </div>
                      ) : (
                        assets.filter(a => a.status === 'completed').map(asset => {
                          const isChecked = activeRoomAssets.includes(asset.id);
                          return (
                            <label 
                              key={asset.id} 
                              style={{ 
                                display: 'flex', 
                                alignItems: 'center', 
                                gap: '10px', 
                                padding: '6px 8px', 
                                borderRadius: '6px', 
                                cursor: 'pointer',
                                transition: 'all var(--transition-fast)',
                                backgroundColor: isChecked ? 'rgba(139, 92, 246, 0.08)' : 'transparent',
                                border: isChecked ? '1px solid rgba(139, 92, 246, 0.2)' : '1px solid transparent',
                                marginBottom: '4px'
                              }}
                              className="asset-checklist-item"
                            >
                              <input 
                                type="checkbox" 
                                checked={isChecked}
                                onChange={() => {
                                  if (isChecked) {
                                    setActiveRoomAssets(prev => prev.filter(id => id !== asset.id));
                                  } else {
                                    setActiveRoomAssets(prev => [...prev, asset.id]);
                                    setRoomAssetTransforms(prev => ({
                                      ...prev,
                                      [asset.id]: prev[asset.id] || {
                                        posX: 0,
                                        posY: 0,
                                        posZ: 0,
                                        rotY: 0,
                                        scale: 1,
                                        customColor: asset.parameters?.custom_color || null,
                                        detailColors: {}
                                      }
                                    }));
                                  }
                                  setRoomLayout('custom');
                                }}
                                style={{ accentColor: 'var(--primary)', cursor: 'pointer' }}
                              />
                              <span style={{ color: isChecked ? 'var(--primary-hover)' : 'var(--text-muted)' }}>{getAssetIcon(asset.asset_type)}</span>
                              <span style={{ fontSize: '13px', color: 'var(--text-primary)', textTransform: 'capitalize' }}>
                                {formatAssetType(asset.asset_type)}
                              </span>
                            </label>
                          );
                        })
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
