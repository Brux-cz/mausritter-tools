"use client";

import React, { useMemo } from "react";
import {
  get19HexLayout,
  hexagonPoints,
} from "@/lib/hexMath";

interface EmptyHexMapProps {
  showNumbers?: boolean;
  hexSize?: number;
}

export default function EmptyHexMap({
  showNumbers = true,
}: EmptyHexMapProps) {
  // Get 19-hex layout (classic hexagon pattern)
  const hexLayout = useMemo(() => get19HexLayout(), []);

  // Calculate viewBox to fit the hexagon shape
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
    <div className="flex flex-col items-center gap-4 p-4">
      {/* SVG Hex Grid */}
      <svg
        viewBox={viewBox}
        className="w-full max-w-4xl border-2 border-slate-700 rounded-lg bg-white print:border-black"
        style={{ aspectRatio: "auto" }}
      >
        {/* Render 19 hexes in hexagon layout */}
        {hexLayout.map((layout, idx) => {
          const { x, y } = layout;
          const points = hexagonPoints(x, y);

          return (
            <g key={idx}>
              {/* Hex polygon */}
              <polygon
                points={points}
                className="fill-white stroke-slate-800 print:stroke-black"
                strokeWidth="2"
              />

              {/* Hex number (1-19) */}
              {showNumbers && (
                <text
                  x={x}
                  y={y + 8}
                  textAnchor="middle"
                  className="select-none font-bold text-2xl fill-slate-800 print:fill-black"
                  style={{ userSelect: "none" }}
                >
                  {idx + 1}
                </text>
              )}
            </g>
          );
        })}
      </svg>

      {/* Info panel */}
      <div className="text-sm text-muted-foreground print:hidden">
        <p>
          Klasický 19-hexový pattern pro Mausritter.
          Použij jako prázdnou mapu pro vlastní poznámky.
        </p>
      </div>
    </div>
  );
}
