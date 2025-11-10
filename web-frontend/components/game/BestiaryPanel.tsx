"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import type { Creature } from "@/lib/types/campaign";

export default function BestiaryPanel() {
  const [creatures, setCreatures] = useState<Creature[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [sourceFilter, setSourceFilter] = useState<string>("");
  const [selectedCreature, setSelectedCreature] = useState<Creature | null>(null);
  const [sheetOpen, setSheetOpen] = useState(false);

  // Mock creatures data (later: fetch from API)
  useEffect(() => {
    const mockCreatures: Creature[] = [
      {
        id: "1",
        name: "Giant Rat",
        hp: 6,
        attack: "Bite (d6)",
        wants: "Food, shelter",
        source: "rulebook",
        description: "A large, aggressive rodent.",
      },
      {
        id: "2",
        name: "Owl",
        hp: 4,
        attack: "Talons (d6)",
        wants: "Prey, territory",
        source: "rulebook",
        description: "Silent hunter of the night.",
      },
      {
        id: "3",
        name: "Cat",
        hp: 8,
        attack: "Claws (d6+1)",
        wants: "Play, food",
        source: "rulebook",
        description: "Deadly predator to mice.",
      },
      {
        id: "4",
        name: "Snake",
        hp: 5,
        attack: "Bite (d6), poison",
        wants: "Warmth, prey",
        source: "rulebook",
        description: "Venomous serpent.",
        special: ["Poison: Save or take d6 damage"],
      },
      {
        id: "5",
        name: "Spider",
        hp: 3,
        attack: "Bite (d4)",
        wants: "Dark corners, insects",
        source: "rulebook",
        description: "Eight-legged terror.",
      },
      {
        id: "6",
        name: "Bee Swarm",
        hp: 10,
        attack: "Sting (2d6)",
        wants: "Protect hive",
        source: "rulebook",
        description: "Angry swarm of bees.",
      },
    ];
    setCreatures(mockCreatures);
  }, []);

  // Filter creatures by search query and source
  const filteredCreatures = creatures.filter((creature) => {
    const matchesSearch = creature.name
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    const matchesSource = sourceFilter === "" || creature.source === sourceFilter;
    return matchesSearch && matchesSource;
  });

  const getCreatureEmoji = (name: string): string => {
    if (name.toLowerCase().includes("rat")) return "🐀";
    if (name.toLowerCase().includes("owl")) return "🦉";
    if (name.toLowerCase().includes("cat")) return "🐱";
    if (name.toLowerCase().includes("snake")) return "🐍";
    if (name.toLowerCase().includes("spider")) return "🕷️";
    if (name.toLowerCase().includes("bee")) return "🐝";
    return "🐾";
  };

  const getSourceColor = (source: string): string => {
    switch (source) {
      case "rulebook":
        return "bg-blue-100 text-blue-800";
      case "generated":
        return "bg-green-100 text-green-800";
      case "custom":
        return "bg-purple-100 text-purple-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="flex flex-col h-full space-y-2">
      {/* Search and Filter Row */}
      <div className="flex gap-2">
        <Input
          type="text"
          placeholder="Search..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="text-xs h-8 flex-1"
        />
        <select
          value={sourceFilter}
          onChange={(e) => setSourceFilter(e.target.value)}
          className="text-xs h-8 px-2 rounded-md border border-gray-300 bg-white hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-400"
        >
          <option value="">All</option>
          <option value="rulebook">Rulebook</option>
          <option value="generated">Generated</option>
          <option value="custom">Custom</option>
        </select>
      </div>

      {/* Icon Grid */}
      <div className="flex-1 overflow-y-auto overflow-x-hidden">
        {filteredCreatures.length === 0 ? (
          <div className="text-xs text-gray-500 text-center py-4">
            No creatures found
          </div>
        ) : (
          <TooltipProvider delayDuration={300}>
            <div className="grid grid-cols-2 gap-2">
              {filteredCreatures.map((creature) => (
                <Tooltip key={creature.id}>
                  <TooltipTrigger asChild>
                    <button
                      onClick={() => {
                        setSelectedCreature(creature);
                        setSheetOpen(true);
                      }}
                      className="w-full h-10 bg-gradient-to-br from-amber-100 to-orange-100 rounded-md flex items-center justify-center text-xs font-medium hover:shadow-md hover:scale-105 transition-all border border-amber-200 hover:border-amber-400 px-2 overflow-hidden"
                    >
                      <span className="truncate">{creature.name}</span>
                    </button>
                  </TooltipTrigger>

                  {/* Tooltip: Quick Preview (hover) */}
                  <TooltipContent side="right" className="max-w-[200px]">
                    <div className="space-y-1">
                      <div className="font-bold text-sm">{creature.name}</div>
                      <div className="text-xs text-gray-600">
                        HP: {creature.hp}
                      </div>
                      <div className="text-xs text-gray-600">
                        Attack: {creature.attack}
                      </div>
                    </div>
                  </TooltipContent>
                </Tooltip>
              ))}
            </div>
          </TooltipProvider>
        )}
      </div>

      {/* Creature Detail Sheet */}
      {selectedCreature && (
        <Sheet open={sheetOpen} onOpenChange={setSheetOpen}>
          <SheetContent className="w-[400px] sm:w-[540px] overflow-y-auto">
            <SheetHeader>
              <SheetTitle className="flex items-center gap-2">
                <span className="text-2xl">{getCreatureEmoji(selectedCreature.name)}</span>
                {selectedCreature.name}
              </SheetTitle>
            </SheetHeader>

            <div className="mt-6 space-y-4">
              {/* Stats */}
              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 bg-amber-50 rounded-lg">
                  <div className="text-xs text-gray-600">Hit Points</div>
                  <div className="text-2xl font-bold text-amber-900">
                    {selectedCreature.hp}
                  </div>
                </div>
                <div className="p-3 bg-amber-50 rounded-lg">
                  <div className="text-xs text-gray-600">Attack</div>
                  <div className="text-sm font-semibold text-amber-900">
                    {selectedCreature.attack}
                  </div>
                </div>
              </div>

              {/* Wants */}
              <div>
                <div className="text-sm font-semibold text-gray-700 mb-1">Wants</div>
                <div className="text-sm text-gray-600">{selectedCreature.wants}</div>
              </div>

              {/* Description */}
              {selectedCreature.description && (
                <div>
                  <div className="text-sm font-semibold text-gray-700 mb-1">
                    Description
                  </div>
                  <div className="text-sm text-gray-600">
                    {selectedCreature.description}
                  </div>
                </div>
              )}

              {/* Special Abilities */}
              {selectedCreature.special && selectedCreature.special.length > 0 && (
                <div>
                  <div className="text-sm font-semibold text-gray-700 mb-1">
                    Special Abilities
                  </div>
                  <ul className="list-disc list-inside space-y-1">
                    {selectedCreature.special.map((ability, index) => (
                      <li key={index} className="text-sm text-gray-600">
                        {ability}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Source Badge */}
              <div>
                <Badge className={getSourceColor(selectedCreature.source)}>
                  {selectedCreature.source}
                </Badge>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      )}
    </div>
  );
}
