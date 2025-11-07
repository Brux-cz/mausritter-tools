"use client";

import React, { useState } from "react";
import { HexcrawlResponse, HexcrawlHex } from "@/lib/api";
import {
  offsetToScreen,
  getGridViewBox,
  hexagonPoints,
} from "@/lib/hexMath";

interface HexMapProps {
  hexcrawl: HexcrawlResponse;
  onHexSelect?: (hexIndex: number, hex: HexcrawlHex) => void;
}

interface HexState {
  revealed: boolean;
  selected: boolean;
}

export default function HexMap({ hexcrawl, onHexSelect }: HexMapProps) {
  // State: Fog of War - initially all hexes unrevealed
  const [hexStates, setHexStates] = useState<HexState[]>(
    hexcrawl.hexes.map(() => ({ revealed: false, selected: false }))
  );

  const viewBox = getGridViewBox(5, 5);

  // Click handler: toggle revealed state
  const handleHexClick = (index: number, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    setHexStates((prev) => {
      const newStates = prev.map((state, idx) => ({
        ...state,
        selected: idx === index, // Only clicked hex is selected
      }));
      // Toggle revealed for clicked hex
      newStates[index].revealed = !newStates[index].revealed;
      return newStates;
    });

    onHexSelect?.(index, hexcrawl.hexes[index]);
  };

  return (
    <div className="flex flex-col items-center gap-4 p-4">
      {/* SVG Hex Grid */}
      <svg
        viewBox={viewBox.viewBox}
        className="w-full max-w-4xl border-2 border-slate-700 rounded-lg bg-slate-950"
        style={{ aspectRatio: `${viewBox.width} / ${viewBox.height}` }}
      >
        {/* Render 25 hexes in 5x5 grid */}
        {hexcrawl.hexes.map((hex, idx) => {
          const col = idx % 5;
          const row = Math.floor(idx / 5);
          const { x, y } = offsetToScreen(col, row);
          const points = hexagonPoints(x, y);
          const state = hexStates[idx];

          return (
            <g
              key={idx}
              onClick={(e) => handleHexClick(idx, e)}
              className="cursor-pointer"
            >
              {/* Hex polygon */}
              <polygon
                points={points}
                className={`
                  transition-all duration-200
                  ${
                    state.revealed
                      ? "fill-slate-700 stroke-blue-400"
                      : "fill-slate-800 stroke-gray-600"
                  }
                  ${state.selected ? "stroke-yellow-400" : ""}
                  hover:fill-slate-600
                `}
                strokeWidth={state.selected ? "3" : "2"}
              />

              {/* Hex number (1-25) - always visible */}
              <text
                x={x}
                y={y + 8}
                textAnchor="middle"
                className="select-none font-bold text-2xl fill-white pointer-events-none"
                style={{ userSelect: "none" }}
              >
                {idx + 1}
              </text>

              {/* Type indicator (only when revealed) */}
              {state.revealed && (
                <text
                  x={x}
                  y={y - 25}
                  textAnchor="middle"
                  className="select-none text-xs fill-gray-300 pointer-events-none"
                  style={{ userSelect: "none" }}
                >
                  {hex.type}
                </text>
              )}

              {/* Settlement icon (only when revealed and has settlement) */}
              {state.revealed && hex.settlement && (
                <text
                  x={x}
                  y={y + 35}
                  textAnchor="middle"
                  className="select-none text-2xl pointer-events-none"
                  style={{ userSelect: "none" }}
                >
                  🏘️
                </text>
              )}
            </g>
          );
        })}
      </svg>

      {/* Legend */}
      <div className="flex flex-wrap gap-6 text-sm text-muted-foreground">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 border-2 border-gray-600 bg-slate-800 rounded"></div>
          <span>Neobjeveno (klikni pro odhalení)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 border-2 border-blue-400 bg-slate-700 rounded"></div>
          <span>Objeveno</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 border-2 border-yellow-400 bg-slate-700 rounded"></div>
          <span>Vybráno</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-2xl">🏘️</span>
          <span>Osada</span>
        </div>
      </div>
    </div>
  );
}
