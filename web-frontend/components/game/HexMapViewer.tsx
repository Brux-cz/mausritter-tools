"use client";

import { useState } from "react";
import type { HexData } from "@/lib/types/campaign";
import { get19HexLayout, hexagonPoints } from "@/lib/hexMath";
import type { HexLayout } from "@/lib/hexMath";

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
  // Get hex layout from library
  const hexLayout = get19HexLayout();

  // Initialize mock hexes
  const [hexes, setHexes] = useState<HexData[]>(() =>
    hexLayout.map((layout, index) => ({
      id: `hex-${index}`,
      q: layout.col, // Axial q coordinate
      r: layout.row, // Axial r coordinate
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

  // Calculate SVG viewBox (HEX_RADIUS = 30)
  const padding = 120; // Extra space around hex grid
  const minX = -200;
  const minY = -200;
  const width = 400;
  const height = 400;

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
          {hexes.map((hex, index) => {
            const layout = hexLayout[index];
            const { x, y } = layout;
            const points = hexagonPoints(x, y);
            const isExplored = hex.explored;

            return (
              <g
                key={hex.id}
                onClick={() => handleHexClick(hex)}
                className="cursor-pointer transition-all hover:opacity-80"
              >
                {/* Hex background */}
                <polygon
                  points={points}
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
                  y={y + 18}
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
