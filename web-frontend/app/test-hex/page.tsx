"use client";

import HexMap from "@/components/generators/HexMap";
import { HexcrawlResponse } from "@/lib/api";

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
  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-4">
          <h1 className="text-3xl font-bold">🧪 Hex Map Test</h1>
          <p className="text-muted-foreground">Testovací stránka pro ladění geometrie hex mapy</p>
        </div>

        <div className="border-2 border-yellow-500 rounded-lg p-4">
          <HexMap
            hexcrawl={mockHexcrawl}
            onHexSelect={(idx, hex) => {
              console.log(`Hex ${idx + 1} selected:`, hex);
            }}
          />
        </div>

        <div className="mt-4 p-4 bg-muted rounded text-sm">
          <p><strong>Debug info:</strong></p>
          <p>• Celkem hexů: 19</p>
          <p>• Pattern: Klasický hexagon (spiral z centra)</p>
          <p>• URL: <code>http://localhost:3001/test-hex</code></p>
        </div>
      </div>
    </main>
  );
}
