"use client";

import { useState } from "react";
import type { HexData } from "@/lib/types/campaign";

// Hex geometry constants
const HEX_SIZE = 40; // radius of hexagon
const HEX_WIDTH = Math.sqrt(3) * HEX_SIZE;
const HEX_HEIGHT = 2 * HEX_SIZE;

// 19-hex honeycomb pattern (axial coordinates)
const HEX_COORDINATES = [
  // Center
  { q: 0, r: 0 },
  // First ring (6 hexes)
  { q: 1, r: 0 },
  { q: 1, r: -1 },
  { q: 0, r: -1 },
  { q: -1, r: 0 },
  { q: -1, r: 1 },
  { q: 0, r: 1 },
  // Second ring (12 hexes)
  { q: 2, r: 0 },
  { q: 2, r: -1 },
  { q: 2, r: -2 },
  { q: 1, r: -2 },
  { q: 0, r: -2 },
  { q: -1, r: -1 },
  { q: -2, r: 0 },
  { q: -2, r: 1 },
  { q: -2, r: 2 },
  { q: -1, r: 2 },
  { q: 0, r: 2 },
  { q: 1, r: 1 },
];

// Convert axial coordinates to pixel coordinates
function axialToPixel(q: number, r: number): { x: number; y: number } {
  const x = HEX_SIZE * (Math.sqrt(3) * q + (Math.sqrt(3) / 2) * r);
  const y = HEX_SIZE * ((3 / 2) * r);
  return { x, y };
}

// Generate hexagon SVG path
function hexagonPath(centerX: number, centerY: number, size: number): string {
  const angles = [0, 60, 120, 180, 240, 300];
  const points = angles.map((angle) => {
    const rad = (Math.PI / 180) * angle;
    const x = centerX + size * Math.cos(rad);
    const y = centerY + size * Math.sin(rad);
    return `${x},${y}`;
  });
  return `M${points.join("L")}Z`;
}

// Get terrain emoji
function getTerrainEmoji(terrain: string): string {
  const emojiMap: Record<string, string> = {
    forest: "🌲",
    plains: "🌾",
    water: "🌊",
    mountains: "⛰️",
    settlement: "🏘️",
    dungeon: "🏰",
    unknown: "❓",
  };
  return emojiMap[terrain] || "🗺️";
}

export default function HexMapViewer() {
  // Initialize mock hexes
  const [hexes, setHexes] = useState<HexData[]>(() =>
    HEX_COORDINATES.map((coord, index) => ({
      id: `hex-${index}`,
      q: coord.q,
      r: coord.r,
      terrain: index === 0 ? "settlement" : "unknown",
      explored: index === 0, // Only center hex explored by default
      notes: "",
    }))
  );

  const [selectedHex, setSelectedHex] = useState<HexData | null>(null);

  const handleHexClick = (hex: HexData) => {
    setSelectedHex(hex);
    // Toggle explored status
    setHexes((prevHexes) =>
      prevHexes.map((h) =>
        h.id === hex.id ? { ...h, explored: !h.explored } : h
      )
    );
  };

  const handleGenerateWorld = () => {
    // TODO: Call backend API /generate/hexcrawl
    alert("Generate World - připojení na backend bude přidáno!");
  };

  // Calculate SVG viewBox
  const padding = HEX_SIZE * 3;
  const minX = -padding;
  const minY = -padding;
  const width = HEX_SIZE * 10;
  const height = HEX_SIZE * 10;

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header with actions */}
      <div className="flex items-center justify-between p-3 border-b border-amber-200 bg-amber-50">
        <h3 className="text-sm font-semibold text-amber-900">
          🗺️ Hexcrawl Map
        </h3>
        <button
          onClick={handleGenerateWorld}
          className="px-3 py-1 text-xs bg-amber-600 text-white rounded hover:bg-amber-700 transition"
        >
          Generate World
        </button>
      </div>

      {/* SVG Hex Grid */}
      <div className="flex-1 overflow-auto p-4 bg-gradient-to-br from-green-50 to-blue-50">
        <svg
          viewBox={`${minX} ${minY} ${width} ${height}`}
          className="w-full h-full"
          style={{ maxWidth: "800px", margin: "0 auto" }}
        >
          {hexes.map((hex) => {
            const { x, y } = axialToPixel(hex.q, hex.r);
            const path = hexagonPath(x, y, HEX_SIZE);
            const isExplored = hex.explored;

            return (
              <g
                key={hex.id}
                onClick={() => handleHexClick(hex)}
                className="cursor-pointer transition-all hover:opacity-80"
              >
                {/* Hex background */}
                <path
                  d={path}
                  fill={isExplored ? "#fef3c7" : "#d1d5db"}
                  stroke={selectedHex?.id === hex.id ? "#f59e0b" : "#6b7280"}
                  strokeWidth={selectedHex?.id === hex.id ? 3 : 1.5}
                  className="transition-all"
                />

                {/* Terrain emoji */}
                {isExplored && (
                  <text
                    x={x}
                    y={y}
                    fontSize="24"
                    textAnchor="middle"
                    dominantBaseline="middle"
                  >
                    {getTerrainEmoji(hex.terrain)}
                  </text>
                )}

                {/* Fog of war */}
                {!isExplored && (
                  <text
                    x={x}
                    y={y}
                    fontSize="20"
                    textAnchor="middle"
                    dominantBaseline="middle"
                    fill="#9ca3af"
                  >
                    ?
                  </text>
                )}

                {/* Coordinates (debug) */}
                <text
                  x={x}
                  y={y + HEX_SIZE * 0.6}
                  fontSize="8"
                  textAnchor="middle"
                  fill="#6b7280"
                  className="select-none"
                >
                  {hex.q},{hex.r}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Selected hex info */}
      {selectedHex && (
        <div className="p-3 border-t border-amber-200 bg-amber-50">
          <div className="text-xs space-y-1">
            <div className="font-semibold text-amber-900">
              Hex ({selectedHex.q}, {selectedHex.r})
            </div>
            <div className="text-gray-700">
              Terrain: {selectedHex.terrain} {getTerrainEmoji(selectedHex.terrain)}
            </div>
            <div className="text-gray-700">
              Status: {selectedHex.explored ? "✅ Explored" : "🔒 Unexplored"}
            </div>
            {selectedHex.settlement && (
              <div className="text-gray-700">
                Settlement: {selectedHex.settlement.name}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
