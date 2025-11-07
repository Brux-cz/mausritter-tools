"use client";

import { useState, useEffect } from "react";
import { createMockCampaign } from "@/lib/types/campaign";
import type { CampaignState, Mouse } from "@/lib/types/campaign";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import TopBar from "@/components/game/TopBar";
import LeftSidebar from "@/components/game/LeftSidebar";
import RightSidebar from "@/components/game/RightSidebar";
import TabSystem from "@/components/game/TabSystem";
import MouseDetailSheet from "@/components/game/MouseDetailSidebar";

export default function GamePage() {
  const [campaign, setCampaign] = useState<CampaignState | null>(null);
  const [selectedMouse, setSelectedMouse] = useState<Mouse | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Load campaign from localStorage or create mock
  useEffect(() => {
    const savedCampaign = localStorage.getItem("mausritter-campaign");
    if (savedCampaign) {
      setCampaign(JSON.parse(savedCampaign));
    } else {
      const mockCampaign = createMockCampaign();
      setCampaign(mockCampaign);
      localStorage.setItem("mausritter-campaign", JSON.stringify(mockCampaign));
    }
  }, []);

  // Save campaign to localStorage whenever it changes
  useEffect(() => {
    if (campaign) {
      campaign.lastModified = new Date();
      localStorage.setItem("mausritter-campaign", JSON.stringify(campaign));
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
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-amber-50 to-orange-50">
        <div className="text-lg text-amber-900">Loading campaign...</div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-amber-50 to-orange-50">
      {/* Top Bar - 40px */}
      <TopBar campaign={campaign} />

      {/* Main Layout - Resizable Panels */}
      <ResizablePanelGroup
        direction="horizontal"
        className="flex-1 overflow-hidden"
      >
        {/* Left Sidebar */}
        <ResizablePanel defaultSize={15} minSize={10} maxSize={25}>
          <LeftSidebar
            campaign={campaign}
            onMouseClick={handleMouseClick}
            onUpdateCampaign={setCampaign}
          />
        </ResizablePanel>

        <ResizableHandle withHandle />

        {/* Main Content Area */}
        <ResizablePanel defaultSize={70} minSize={50}>
          <TabSystem />
        </ResizablePanel>

        <ResizableHandle withHandle />

        {/* Right Sidebar */}
        <ResizablePanel defaultSize={15} minSize={10} maxSize={25}>
          <RightSidebar />
        </ResizablePanel>
      </ResizablePanelGroup>

      {/* Mouse Detail Sheet Modal */}
      <MouseDetailSheet
        mouse={selectedMouse}
        isOpen={sidebarOpen}
        onClose={handleCloseSidebar}
      />
    </div>
  );
}
