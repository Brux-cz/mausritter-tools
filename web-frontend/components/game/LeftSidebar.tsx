"use client";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import type { CampaignState, Mouse } from "@/lib/types/campaign";

interface LeftSidebarProps {
  campaign: CampaignState;
  onMouseClick: (mouse: Mouse) => void;
  onUpdateCampaign: (campaign: CampaignState) => void;
}

export default function LeftSidebar({
  campaign,
  onMouseClick,
  onUpdateCampaign,
}: LeftSidebarProps) {
  const watchOrder = ["morning", "afternoon", "evening", "night"] as const;

  const handleNextWatch = () => {
    const currentIndex = watchOrder.indexOf(campaign.currentWatch);
    const nextIndex = (currentIndex + 1) % watchOrder.length;
    const nextWatch = watchOrder[nextIndex];

    const updatedCampaign = {
      ...campaign,
      currentWatch: nextWatch,
      currentDay:
        nextWatch === "morning" ? campaign.currentDay + 1 : campaign.currentDay,
    };

    onUpdateCampaign(updatedCampaign);
  };

  const handleRollWeather = () => {
    const die1 = Math.floor(Math.random() * 6) + 1;
    const die2 = Math.floor(Math.random() * 6) + 1;
    const total = die1 + die2;

    let weatherResult = "Normal";
    let effects: string[] = [];

    if (total <= 3) {
      weatherResult = "Harsh Weather";
      effects = ["Movement stopped"];
    } else if (total >= 10 && total <= 11) {
      weatherResult = "Favourable";
      effects = ["Comfortable"];
    } else if (total === 12) {
      weatherResult = "Extreme!";
      effects = ["Roll seasonal table"];
    }

    const updatedCampaign = {
      ...campaign,
      weather: {
        ...campaign.weather,
        current: weatherResult,
        roll: total,
        effects,
      },
      weatherLog: [
        ...campaign.weatherLog,
        {
          current: weatherResult,
          roll: total,
          season: campaign.weather.season,
          effects,
        },
      ],
    };

    onUpdateCampaign(updatedCampaign);
  };

  const getWatchEmoji = (watch: string) => {
    switch (watch) {
      case "morning":
        return "🌅";
      case "afternoon":
        return "☀️";
      case "evening":
        return "🌆";
      case "night":
        return "🌙";
      default:
        return "⏰";
    }
  };

  const getWeatherEmoji = (weather: string) => {
    if (weather.includes("Harsh")) return "⛈️";
    if (weather.includes("Favourable")) return "☀️";
    if (weather.includes("Extreme")) return "🌪️";
    return "🌤️";
  };

  return (
    <div className="h-full bg-gradient-to-b from-amber-50 to-orange-50 border-r border-amber-200 overflow-y-auto">
      <Accordion
        type="multiple"
        defaultValue={["party", "time", "actions"]}
        className="w-full"
      >
        {/* Party Section */}
        <AccordionItem value="party" className="border-b border-amber-200">
          <AccordionTrigger className="px-3 py-2 text-sm font-semibold text-amber-900 hover:bg-amber-100 hover:no-underline">
            🐭 Party ({campaign.party.length})
          </AccordionTrigger>
          <AccordionContent className="px-2 pb-2">
            <div className="space-y-1">
              {campaign.party.length === 0 ? (
                <div className="text-xs text-gray-500 text-center py-4">
                  No mice yet
                </div>
              ) : (
                campaign.party.map((mouse) => (
                  <button
                    key={mouse.id}
                    onClick={() => onMouseClick(mouse)}
                    className="w-full p-2 bg-white hover:bg-amber-50 rounded border border-amber-200 hover:border-amber-400 transition text-left group"
                  >
                    {/* Mouse name + icon */}
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-semibold text-amber-900 flex items-center gap-1">
                        🐭 {mouse.name}
                      </span>
                      {mouse.conditions && mouse.conditions.length > 0 && (
                        <Badge
                          variant="destructive"
                          className="text-[10px] px-1 py-0 h-4"
                        >
                          ⚠️
                        </Badge>
                      )}
                    </div>

                    {/* HP bar - inline */}
                    <div className="flex items-center gap-2 text-xs">
                      <span className="text-gray-600">HP</span>
                      <div className="flex-1 bg-gray-200 rounded-full h-1.5">
                        <div
                          className={`h-1.5 rounded-full transition-all ${
                            mouse.hp > mouse.maxHp * 0.5
                              ? "bg-green-500"
                              : mouse.hp > mouse.maxHp * 0.25
                              ? "bg-yellow-500"
                              : "bg-red-500"
                          }`}
                          style={{ width: `${(mouse.hp / mouse.maxHp) * 100}%` }}
                        />
                      </div>
                      <span className="text-gray-600 tabular-nums">
                        {mouse.hp}/{mouse.maxHp}
                      </span>
                    </div>
                  </button>
                ))
              )}

              {/* Add Mouse Button */}
              <button className="w-full py-1.5 text-xs bg-green-600 text-white rounded hover:bg-green-700 transition mt-2">
                + Add Mouse
              </button>
            </div>
          </AccordionContent>
        </AccordionItem>

        {/* Time & Weather Section */}
        <AccordionItem value="time" className="border-b border-amber-200">
          <AccordionTrigger className="px-3 py-2 text-sm font-semibold text-amber-900 hover:bg-amber-100 hover:no-underline">
            📅 Time & Weather
          </AccordionTrigger>
          <AccordionContent className="px-3 pb-3">
            <div className="space-y-3">
              {/* Time */}
              <div className="bg-white rounded border border-amber-200 p-2">
                <div className="text-xs text-gray-600 mb-1">Time</div>
                <div className="text-sm font-bold text-amber-900">
                  Day {campaign.currentDay}
                </div>
                <div className="text-sm text-amber-800">
                  {getWatchEmoji(campaign.currentWatch)}{" "}
                  {campaign.currentWatch.charAt(0).toUpperCase() +
                    campaign.currentWatch.slice(1)}
                </div>
                <button
                  onClick={handleNextWatch}
                  className="w-full mt-2 py-1 text-xs bg-amber-600 text-white rounded hover:bg-amber-700 transition"
                >
                  Next Watch →
                </button>
              </div>

              {/* Weather */}
              <div className="bg-white rounded border border-amber-200 p-2">
                <div className="text-xs text-gray-600 mb-1">Weather</div>
                <div className="text-sm font-bold text-amber-900">
                  {getWeatherEmoji(campaign.weather.current)}{" "}
                  {campaign.weather.current}
                </div>
                <div className="text-xs text-gray-500">
                  Roll: {campaign.weather.roll} (2d6)
                </div>
                {campaign.weather.effects &&
                  campaign.weather.effects.length > 0 && (
                    <div className="text-xs text-blue-600 mt-1">
                      {campaign.weather.effects[0]}
                    </div>
                  )}
                <button
                  onClick={handleRollWeather}
                  className="w-full mt-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition"
                >
                  Roll Weather
                </button>
              </div>
            </div>
          </AccordionContent>
        </AccordionItem>

        {/* Quick Actions Section */}
        <AccordionItem value="actions" className="border-b border-amber-200">
          <AccordionTrigger className="px-3 py-2 text-sm font-semibold text-amber-900 hover:bg-amber-100 hover:no-underline">
            ⚡ Quick Actions
          </AccordionTrigger>
          <AccordionContent className="px-2 pb-2">
            <div className="space-y-1">
              <button className="w-full py-1.5 px-3 text-xs bg-amber-600 text-white rounded hover:bg-amber-700 transition text-left">
                🎲 Generate NPC
              </button>
              <button className="w-full py-1.5 px-3 text-xs bg-amber-600 text-white rounded hover:bg-amber-700 transition text-left">
                ⚔️ Roll Encounter
              </button>
              <button className="w-full py-1.5 px-3 text-xs bg-amber-600 text-white rounded hover:bg-amber-700 transition text-left">
                📜 Random Table
              </button>
              <button className="w-full py-1.5 px-3 text-xs bg-amber-600 text-white rounded hover:bg-amber-700 transition text-left">
                🏘️ Add Settlement
              </button>
            </div>
          </AccordionContent>
        </AccordionItem>

        {/* Encounters Section */}
        <AccordionItem value="encounters">
          <AccordionTrigger className="px-3 py-2 text-sm font-semibold text-amber-900 hover:bg-amber-100 hover:no-underline">
            ⚔️ Encounters (
            {campaign.encounters.filter((e) => e.active).length})
          </AccordionTrigger>
          <AccordionContent className="px-3 pb-3">
            <div className="bg-white rounded border border-amber-200 p-2">
              <div className="text-xs text-gray-600 mb-1">Active</div>
              <div className="text-sm font-bold text-amber-900">
                {campaign.encounters.filter((e) => e.active).length}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                Next roll:{" "}
                {campaign.currentWatch === "morning" ||
                campaign.currentWatch === "evening"
                  ? "Now!"
                  : "Morning/Evening"}
              </div>
              <button className="w-full mt-2 py-1 text-xs bg-red-600 text-white rounded hover:bg-red-700 transition">
                Roll Encounter
              </button>
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  );
}
