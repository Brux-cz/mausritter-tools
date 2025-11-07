"use client";

import { useState } from "react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";

interface DiceRoll {
  id: string;
  dice: string;
  result: number;
  timestamp: Date;
}

export default function RightSidebar() {
  const [notes, setNotes] = useState("");
  const [rollHistory, setRollHistory] = useState<DiceRoll[]>([]);
  const [lastRoll, setLastRoll] = useState<DiceRoll | null>(null);

  const rollDice = (diceType: string) => {
    let result = 0;

    switch (diceType) {
      case "d6":
        result = Math.floor(Math.random() * 6) + 1;
        break;
      case "2d6":
        result =
          Math.floor(Math.random() * 6) +
          1 +
          Math.floor(Math.random() * 6) +
          1;
        break;
      case "d20":
        result = Math.floor(Math.random() * 20) + 1;
        break;
      case "d100":
        result = Math.floor(Math.random() * 100) + 1;
        break;
    }

    const roll: DiceRoll = {
      id: Date.now().toString(),
      dice: diceType,
      result,
      timestamp: new Date(),
    };

    setLastRoll(roll);
    setRollHistory([roll, ...rollHistory].slice(0, 20)); // Keep last 20 rolls
  };

  const clearHistory = () => {
    setRollHistory([]);
    setLastRoll(null);
  };

  return (
    <div className="h-full bg-gradient-to-b from-amber-50 to-orange-50 border-l border-amber-200 overflow-y-auto">
      <Accordion
        type="multiple"
        defaultValue={["notes", "dice"]}
        className="w-full"
      >
        {/* Quick Notes Section */}
        <AccordionItem value="notes" className="border-b border-amber-200">
          <AccordionTrigger className="px-3 py-2 text-sm font-semibold text-amber-900 hover:bg-amber-100 hover:no-underline">
            📝 Quick Notes
          </AccordionTrigger>
          <AccordionContent className="px-2 pb-2">
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Quick GM notes..."
              className="w-full h-32 p-2 text-xs border border-amber-200 rounded focus:outline-none focus:ring-2 focus:ring-amber-400 resize-none"
            />
            <div className="text-[10px] text-gray-500 mt-1 text-right">
              Auto-saved
            </div>
          </AccordionContent>
        </AccordionItem>

        {/* Dice Roller Section */}
        <AccordionItem value="dice" className="border-b border-amber-200">
          <AccordionTrigger className="px-3 py-2 text-sm font-semibold text-amber-900 hover:bg-amber-100 hover:no-underline">
            🎲 Dice Roller
          </AccordionTrigger>
          <AccordionContent className="px-3 pb-3">
            <div className="space-y-2">
              {/* Dice buttons - 2x2 grid */}
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={() => rollDice("d6")}
                  className="py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition font-semibold"
                >
                  d6
                </button>
                <button
                  onClick={() => rollDice("2d6")}
                  className="py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition font-semibold"
                >
                  2d6
                </button>
                <button
                  onClick={() => rollDice("d20")}
                  className="py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition font-semibold"
                >
                  d20
                </button>
                <button
                  onClick={() => rollDice("d100")}
                  className="py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition font-semibold"
                >
                  d100
                </button>
              </div>

              {/* Last roll display */}
              {lastRoll && (
                <div className="bg-white rounded border border-blue-300 p-2 text-center">
                  <div className="text-xs text-gray-600">Last roll</div>
                  <div className="text-2xl font-bold text-blue-700 tabular-nums">
                    {lastRoll.result}
                  </div>
                  <div className="text-xs text-gray-500">({lastRoll.dice})</div>
                </div>
              )}
            </div>
          </AccordionContent>
        </AccordionItem>

        {/* Roll History Section */}
        <AccordionItem value="history" className="border-b border-amber-200">
          <AccordionTrigger className="px-3 py-2 text-sm font-semibold text-amber-900 hover:bg-amber-100 hover:no-underline">
            📋 Roll History ({rollHistory.length})
          </AccordionTrigger>
          <AccordionContent className="px-2 pb-2">
            {rollHistory.length === 0 ? (
              <div className="text-xs text-gray-500 text-center py-4">
                No rolls yet
              </div>
            ) : (
              <div className="space-y-1 max-h-48 overflow-y-auto">
                {rollHistory.map((roll) => (
                  <div
                    key={roll.id}
                    className="flex items-center justify-between bg-white rounded border border-amber-200 px-2 py-1 text-xs"
                  >
                    <span className="text-gray-600">{roll.dice}</span>
                    <Badge variant="outline" className="text-xs tabular-nums">
                      {roll.result}
                    </Badge>
                  </div>
                ))}
              </div>
            )}
            {rollHistory.length > 0 && (
              <button
                onClick={clearHistory}
                className="w-full mt-2 py-1 text-xs bg-gray-300 text-gray-700 rounded hover:bg-gray-400 transition"
              >
                Clear History
              </button>
            )}
          </AccordionContent>
        </AccordionItem>

        {/* GM Log Section */}
        <AccordionItem value="log">
          <AccordionTrigger className="px-3 py-2 text-sm font-semibold text-amber-900 hover:bg-amber-100 hover:no-underline">
            📖 GM Log
          </AccordionTrigger>
          <AccordionContent className="px-3 pb-3">
            <div className="bg-white rounded border border-amber-200 p-2 text-xs text-gray-600 max-h-48 overflow-y-auto">
              <div className="mb-2">
                <div className="font-semibold text-amber-900">Day 1, Morning</div>
                <div className="text-[11px] text-gray-500">
                  - Campaign started
                </div>
              </div>
              {/* More log entries will be auto-generated */}
            </div>
            <button className="w-full mt-2 py-1 text-xs bg-amber-600 text-white rounded hover:bg-amber-700 transition">
              Export Log
            </button>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  );
}
