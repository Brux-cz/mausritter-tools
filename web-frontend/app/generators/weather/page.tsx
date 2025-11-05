"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { generateWeather, type WeatherRequest, type WeatherResponse } from "@/lib/api";
import { toast } from "sonner";

const seasonEmojis = {
  spring: "🌸",
  summer: "☀️",
  autumn: "🍂",
  winter: "❄️",
};

const seasonNames = {
  spring: "Jaro",
  summer: "Léto",
  autumn: "Podzim",
  winter: "Zima",
};

export default function WeatherGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [weather, setWeather] = useState<WeatherResponse | null>(null);
  const [season, setSeason] = useState<"spring" | "summer" | "autumn" | "winter">("spring");
  const [withEvent, setWithEvent] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const request: WeatherRequest = {
        season: season,
        with_event: withEvent,
      };
      const result = await generateWeather(request);
      setWeather(result);
      toast.success("Počasí vygenerováno!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (weather) {
      navigator.clipboard.writeText(JSON.stringify(weather, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setWeather(null);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            🌦️ Weather Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Počasí a sezónní události pro všechna čtyři roční období
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Column */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Možnosti</CardTitle>
                <CardDescription>
                  Vyber roční období a zda zahrnout sezónní událost
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="season">Roční období</Label>
                  <Select value={season} onValueChange={(value: any) => setSeason(value)}>
                    <SelectTrigger id="season" disabled={loading}>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="spring">🌸 Jaro</SelectItem>
                      <SelectItem value="summer">☀️ Léto</SelectItem>
                      <SelectItem value="autumn">🍂 Podzim</SelectItem>
                      <SelectItem value="winter">❄️ Zima</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="withEvent"
                    checked={withEvent}
                    onChange={(e) => setWithEvent(e.target.checked)}
                    disabled={loading}
                    className="h-4 w-4 rounded border-gray-300"
                  />
                  <Label htmlFor="withEvent" className="cursor-pointer">
                    Zahrnout sezónní událost
                  </Label>
                </div>

                <div className="flex gap-2 pt-4">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {weather && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Season Info */}
            <Card className="mt-4">
              <CardHeader>
                <CardTitle>Info o ročních obdobích</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <div>🌸 <strong>Jaro:</strong> Přívalové deště (2.78% nepříznivé)</div>
                <div>☀️ <strong>Léto:</strong> Úmorné vedro (27.78% nepříznivé)</div>
                <div>🍂 <strong>Podzim:</strong> Silný vítr (2.78% nepříznivé)</div>
                <div>❄️ <strong>Zima:</strong> Vánice, mráz (72% nepříznivé!)</div>
              </CardContent>
            </Card>

            {/* Actions */}
            {weather && (
              <Card className="mt-4">
                <CardHeader>
                  <CardTitle>Akce</CardTitle>
                </CardHeader>
                <CardContent className="flex gap-2">
                  <Button onClick={handleCopyJSON} variant="outline" className="flex-1">
                    📋 Copy JSON
                  </Button>
                  <Button variant="outline" className="flex-1" disabled>
                    💾 Save
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Result Column */}
          <div>
            {weather ? (
              <Card className={weather.unfavorable ? "border-red-500 border-2" : ""}>
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <div className="text-4xl">{seasonEmojis[weather.season as keyof typeof seasonEmojis]}</div>
                    <div>
                      <CardTitle className="text-2xl">
                        {seasonNames[weather.season as keyof typeof seasonNames]}
                      </CardTitle>
                      {weather.unfavorable && (
                        <span className="text-sm text-red-600 font-medium">
                          ⚠️ Nepříznivé počasí
                        </span>
                      )}
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Weather */}
                  <div className="p-4 bg-muted rounded">
                    <div className="text-xs text-muted-foreground mb-2">POČASÍ</div>
                    <div className="text-lg font-semibold mb-1">{weather.weather}</div>
                    {weather.notes && (
                      <div className="text-sm text-muted-foreground">{weather.notes}</div>
                    )}
                  </div>

                  {/* Event */}
                  {weather.event && (
                    <div className="p-4 bg-primary/10 rounded border border-primary/20">
                      <div className="text-xs text-muted-foreground mb-2">SEZÓNNÍ UDÁLOST</div>
                      <div className="text-sm font-medium">{weather.event}</div>
                    </div>
                  )}

                  {/* Warning for adverse weather */}
                  {weather.unfavorable && (
                    <div className="p-3 bg-red-50 border border-red-200 rounded text-sm text-red-800">
                      <strong>Pozor:</strong> Nepříznivé počasí může ztížit cestování nebo způsobit újmu.
                    </div>
                  )}
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">🌦️</div>
                  <p>Klikni na "Generovat" pro vytvoření počasí</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
