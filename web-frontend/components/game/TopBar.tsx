"use client";

import { Badge } from "@/components/ui/badge";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import type { CampaignState } from "@/lib/types/campaign";

interface TopBarProps {
  campaign: CampaignState;
  onOpenCommandMenu?: () => void;
}

export default function TopBar({ campaign, onOpenCommandMenu }: TopBarProps) {
  const watchIcon = {
    morning: "🌅",
    afternoon: "☀️",
    evening: "🌆",
    night: "🌙",
  }[campaign.currentWatch];

  // Use currentWeather if available, fallback to weather.current
  const weatherCondition = campaign.currentWeather?.condition || campaign.weather.current;
  const weatherRoll = campaign.currentWeather?.roll || campaign.weather.roll;

  // Get weather icon
  const getWeatherIcon = (condition: string) => {
    if (condition.includes("Harsh")) return "⛈️";
    if (condition.includes("Favourable")) return "☀️";
    if (condition.includes("Extreme")) return "🌪️";
    return "🌤️";
  };
  const weatherIcon = campaign.currentWeather?.icon || getWeatherIcon(weatherCondition);

  // Count active encounters
  const activeEncounters = campaign.encounters?.filter(e => e.active).length || 0;

  return (
    <TooltipProvider>
      <header className="h-10 bg-gradient-to-r from-amber-100 to-orange-100 border-b border-amber-200 flex items-center justify-between px-4">
        {/* Left side: Campaign name */}
        <div className="flex items-center gap-3">
          <h1 className="text-base font-bold text-amber-900 flex items-center gap-2">
            🎲 {campaign.name}
          </h1>
        </div>

        {/* Right side: Key stats */}
        <div className="flex items-center gap-3 text-sm">
          {/* Time */}
          <Tooltip>
            <TooltipTrigger asChild>
              <Badge variant="outline" className="cursor-pointer hover:bg-amber-50">
                {watchIcon} Day {campaign.currentDay}, {campaign.currentWatch}
              </Badge>
            </TooltipTrigger>
            <TooltipContent>
              <p>Current time: Day {campaign.currentDay}</p>
              <p>Watch: {campaign.currentWatch}</p>
            </TooltipContent>
          </Tooltip>

          {/* Weather */}
          <Tooltip>
            <TooltipTrigger asChild>
              <Badge variant="outline" className="cursor-pointer hover:bg-amber-50">
                {weatherIcon} {weatherCondition}
              </Badge>
            </TooltipTrigger>
            <TooltipContent>
              <p>Weather: {weatherCondition}</p>
              <p>Roll: {weatherRoll} (2d6)</p>
            </TooltipContent>
          </Tooltip>

          {/* Encounters */}
          <Tooltip>
            <TooltipTrigger asChild>
              <Badge
                variant={activeEncounters > 0 ? "destructive" : "outline"}
                className="cursor-pointer"
              >
                ⚔️ {activeEncounters} Active
              </Badge>
            </TooltipTrigger>
            <TooltipContent>
              <p>Active encounters: {activeEncounters}</p>
            </TooltipContent>
          </Tooltip>

          {/* Command Menu trigger (optional) */}
          {onOpenCommandMenu && (
            <Tooltip>
              <TooltipTrigger asChild>
                <button
                  onClick={onOpenCommandMenu}
                  className="px-2 py-1 text-xs bg-amber-200 hover:bg-amber-300 rounded border border-amber-300 text-amber-900 font-mono transition"
                >
                  ⌘K
                </button>
              </TooltipTrigger>
              <TooltipContent>
                <p>Open command menu</p>
              </TooltipContent>
            </Tooltip>
          )}
        </div>
      </header>
    </TooltipProvider>
  );
}
