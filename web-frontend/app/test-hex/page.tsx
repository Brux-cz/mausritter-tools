"use client";

import React, { useState, useMemo } from "react";
import { HexcrawlResponse } from "@/lib/api";
import { get19HexLayout, hexagonPoints } from "@/lib/hexMath";

// Mock data pro testování hex mapy (19 hexů)
const mockHexcrawl: HexcrawlResponse = {
  hexes: Array.from({ length: 19 }, (_, i) => ({
    type: ["Otevřená krajina", "Les", "Řeka", "Lidské město"][i % 4],
    type_roll: (i % 6) + 1,
    detail_category: (i % 6) + 1,
    detail_subtype: null,
    detail_name: `Detail ${i + 1}`,
    detail_hook: `Hook pro hex ${i + 1}`,
    settlement: i % 5 === 0 ? {
      name: `Osada ${i + 1}`,
      size: 3,
      size_name: "Village",
      population: 50 + i * 10,
      government: "Democracy",
      detail: "Test detail",
      trades: ["Baker", "Smith"],
      features: ["River", "Walls"],
      event: "Festival",
      tavern: null,
    } : null,
    description: `Popis hexa ${i + 1}`,
  })),
  settlements: [],
  dungeons: [],
  rumors: [],
  metadata: {
    preset: "test",
    total_hexes: 25,
    total_settlements: 0,
    total_dungeons: 0,
  },
};

export default function TestHexPage() {
  const [selectedHex, setSelectedHex] = useState<number | null>(null);

  // Get 19-hex layout
  const hexLayout = useMemo(() => get19HexLayout(), []);

  // Calculate viewBox
  const viewBox = useMemo(() => {
    const padding = 80;
    const xCoords = hexLayout.map((h) => h.x);
    const yCoords = hexLayout.map((h) => h.y);
    const minX = Math.min(...xCoords) - 70;
    const maxX = Math.max(...xCoords) + 70;
    const minY = Math.min(...yCoords) - 70;
    const maxY = Math.max(...yCoords) + 70;
    const width = maxX - minX + padding;
    const height = maxY - minY + padding;
    return `${minX - padding / 2} ${minY - padding / 2} ${width} ${height}`;
  }, [hexLayout]);

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-4">
          <h1 className="text-3xl font-bold">🧪 Hex Map Test (19-hex)</h1>
          <p className="text-muted-foreground">Testovací stránka pro ladění geometrie hex mapy</p>
        </div>

        <div className="border-2 border-yellow-500 rounded-lg p-4">
          <div className="flex flex-col items-center gap-4">
            <svg
              viewBox={viewBox}
              className="w-full max-w-4xl border-2 border-slate-700 rounded-lg bg-slate-950"
            >
              {mockHexcrawl.hexes.map((hex, idx) => {
                const layout = hexLayout[idx];
                if (!layout) return null;
                const { x, y } = layout;
                const points = hexagonPoints(x, y);

                return (
                  <g
                    key={idx}
                    onClick={() => setSelectedHex(idx)}
                    className="cursor-pointer"
                  >
                    <polygon
                      points={points}
                      className={`
                        transition-all duration-200
                        fill-slate-700 stroke-blue-400
                        ${selectedHex === idx ? "stroke-yellow-400" : ""}
                        hover:fill-slate-600
                      `}
                      strokeWidth={selectedHex === idx ? "3" : "2"}
                    />
                    <text
                      x={x}
                      y={y + 8}
                      textAnchor="middle"
                      className="select-none font-bold text-2xl fill-white pointer-events-none"
                    >
                      {idx + 1}
                    </text>
                    <text
                      x={x}
                      y={y - 25}
                      textAnchor="middle"
                      className="select-none text-xs fill-gray-300 pointer-events-none"
                    >
                      {hex.type}
                    </text>
                    {hex.settlement && (
                      <text
                        x={x}
                        y={y + 35}
                        textAnchor="middle"
                        className="select-none text-2xl pointer-events-none"
                      >
                        🏘️
                      </text>
                    )}
                  </g>
                );
              })}
            </svg>
          </div>
        </div>

        <div className="mt-4 p-4 bg-muted rounded text-sm">
          <p><strong>Debug info:</strong></p>
          <p>• Celkem hexů: 19</p>
          <p>• Pattern: Klasický hexagon (spiral z centra)</p>
          <p>• Layout: get19HexLayout()</p>
          <p>• URL: <code>http://localhost:3001/test-hex</code></p>
          {selectedHex !== null && (
            <p className="mt-2 text-yellow-500">• Vybraný hex: #{selectedHex + 1}</p>
          )}
        </div>
      </div>
    </main>
  );
}
