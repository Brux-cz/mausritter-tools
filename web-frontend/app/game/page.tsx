"use client";

import { useState, useEffect } from 'react';
import { createMockCampaign } from '@/lib/types/campaign';
import type { CampaignState, Mouse } from '@/lib/types/campaign';
import PartyPanel from '@/components/game/PartyPanel';
import MouseDetailSidebar from '@/components/game/MouseDetailSidebar';
import TimeWeatherPanel from '@/components/game/TimeWeatherPanel';

export default function GamePage() {
  const [campaign, setCampaign] = useState<CampaignState | null>(null);
  const [selectedMouse, setSelectedMouse] = useState<Mouse | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Load campaign from localStorage or create mock
  useEffect(() => {
    const savedCampaign = localStorage.getItem('mausritter-campaign');
    if (savedCampaign) {
      setCampaign(JSON.parse(savedCampaign));
    } else {
      const mockCampaign = createMockCampaign();
      setCampaign(mockCampaign);
      localStorage.setItem('mausritter-campaign', JSON.stringify(mockCampaign));
    }
  }, []);

  // Save campaign to localStorage whenever it changes
  useEffect(() => {
    if (campaign) {
      campaign.lastModified = new Date();
      localStorage.setItem('mausritter-campaign', JSON.stringify(campaign));
    }
  }, [campaign]);

  const handleMouseClick = (mouse: Mouse) => {
    setSelectedMouse(mouse);
    setSidebarOpen(true);
  };

  const handleCloseSidebar = () => {
    setSidebarOpen(false);
    setSelectedMouse(null);
  };

  if (!campaign) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading campaign...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-50 p-4">
      {/* Header */}
      <header className="mb-6">
        <h1 className="text-3xl font-bold text-amber-900 mb-2">
          🎲 {campaign.name}
        </h1>
        <p className="text-amber-700">GM Dashboard</p>
      </header>

      {/* Party Panel */}
      <PartyPanel
        party={campaign.party}
        onMouseClick={handleMouseClick}
      />

      {/* Time & Weather Widgets */}
      <TimeWeatherPanel
        campaign={campaign}
        onUpdateCampaign={setCampaign}
      />

      {/* Main Content Area - Placeholder for now */}
      <div className="mt-6 bg-white rounded-lg shadow-lg p-6 min-h-[400px]">
        <div className="text-center text-gray-500">
          <p className="text-xl mb-2">🗺️ Hex Map</p>
          <p>Coming soon: Interactive hex map will appear here</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-6 bg-white rounded-lg shadow-lg p-4">
        <h3 className="text-lg font-semibold text-amber-900 mb-3">
          🔗 Quick Actions
        </h3>
        <div className="flex flex-wrap gap-2">
          <button className="px-4 py-2 bg-amber-600 text-white rounded hover:bg-amber-700 transition">
            Generate NPC
          </button>
          <button className="px-4 py-2 bg-amber-600 text-white rounded hover:bg-amber-700 transition">
            Roll Encounter
          </button>
          <button className="px-4 py-2 bg-amber-600 text-white rounded hover:bg-amber-700 transition">
            Random Table
          </button>
          <button className="px-4 py-2 bg-amber-600 text-white rounded hover:bg-amber-700 transition">
            Add Settlement
          </button>
        </div>
      </div>

      {/* Quick Rolls Panel */}
      <div className="mt-4 bg-white rounded-lg shadow-lg p-4">
        <h3 className="text-lg font-semibold text-amber-900 mb-3">
          🎲 Quick Rolls
        </h3>
        <div className="flex gap-2">
          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            d6
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            2d6
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            d20
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            d100
          </button>
        </div>
        <div className="mt-2 text-sm text-gray-600">
          Last roll: --
        </div>
      </div>

      {/* Mouse Detail Sidebar */}
      <MouseDetailSidebar
        mouse={selectedMouse}
        isOpen={sidebarOpen}
        onClose={handleCloseSidebar}
      />
    </div>
  );
}
