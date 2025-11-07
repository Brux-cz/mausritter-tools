"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function TabSystem() {
  return (
    <Tabs defaultValue="hexmap" className="h-full flex flex-col">
      {/* Tab Headers */}
      <TabsList className="flex-shrink-0 h-10 bg-amber-100 border-b border-amber-200">
        <TabsTrigger
          value="hexmap"
          className="text-sm px-4 data-[state=active]:bg-white"
        >
          🗺️ Hex Map
        </TabsTrigger>
        <TabsTrigger
          value="tactical"
          className="text-sm px-4 data-[state=active]:bg-white"
        >
          🎨 Tactical
        </TabsTrigger>
        <TabsTrigger
          value="bestiary"
          className="text-sm px-4 data-[state=active]:bg-white"
        >
          📚 Bestiary
        </TabsTrigger>
      </TabsList>

      {/* Tab Content Areas */}
      <TabsContent value="hexmap" className="flex-1 m-0 p-4 data-[state=active]:flex data-[state=active]:flex-col">
        <div className="flex-1 bg-white rounded-lg border border-amber-200 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <p className="text-xl mb-2">🗺️ Hex Map</p>
            <p className="text-sm">Interactive hex map coming soon</p>
            <p className="text-xs text-gray-400 mt-2">
              Phase 1B - Hex grid visualization
            </p>
          </div>
        </div>
      </TabsContent>

      <TabsContent value="tactical" className="flex-1 m-0 p-4 data-[state=active]:flex data-[state=active]:flex-col">
        <div className="flex-1 bg-white rounded-lg border border-amber-200 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <p className="text-xl mb-2">🎨 Tactical Map</p>
            <p className="text-sm">Drawing canvas for combat encounters</p>
            <p className="text-xs text-gray-400 mt-2">
              Phase 1B - Canvas with drawing tools
            </p>
          </div>
        </div>
      </TabsContent>

      <TabsContent value="bestiary" className="flex-1 m-0 p-4 data-[state=active]:flex data-[state=active]:flex-col">
        <div className="flex-1 bg-white rounded-lg border border-amber-200 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <p className="text-xl mb-2">📚 Bestiary</p>
            <p className="text-sm">Creature database + generator</p>
            <p className="text-xs text-gray-400 mt-2">
              Phase 1B - Creature list with filters
            </p>
          </div>
        </div>
      </TabsContent>
    </Tabs>
  );
}
