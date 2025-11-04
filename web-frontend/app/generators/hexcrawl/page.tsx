"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { generateHexcrawl, type HexcrawlResponse } from "@/lib/api";
import { toast } from "sonner";

export default function HexcrawlGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [hexcrawl, setHexcrawl] = useState<HexcrawlResponse | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateHexcrawl({});
      setHexcrawl(result);
      toast.success("Hexcrawl vygenerován!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (hexcrawl) {
      navigator.clipboard.writeText(JSON.stringify(hexcrawl, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setHexcrawl(null);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            🗺️ Hexcrawl Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor hexcrawl kampaní - kompletní svět k průzkumu
          </p>
        </div>

        <div className="grid grid-cols-1 gap-8">
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Generovat Hexcrawl</CardTitle>
                <CardDescription>
                  Vygeneruj kompletní hexcrawl s hexy, osadami, dungeony a zvěstmi
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {hexcrawl && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {hexcrawl && (
              <Card className="mt-4">
                <CardHeader>
                  <CardTitle>Akce</CardTitle>
                </CardHeader>
                <CardContent className="flex gap-2">
                  <Button onClick={handleCopyJSON} variant="outline" className="flex-1">
                    📋 Copy JSON
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>

          {hexcrawl && (
            <div className="space-y-4">
              {/* Summary Card */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <span className="text-3xl">🗺️</span>
                    Hexcrawl - {hexcrawl.metadata.preset}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-4 gap-3">
                    <div className="p-3 bg-muted rounded text-center">
                      <div className="text-2xl font-bold">{hexcrawl.hexes.length}</div>
                      <div className="text-xs text-muted-foreground">Hexů</div>
                    </div>
                    <div className="p-3 bg-muted rounded text-center">
                      <div className="text-2xl font-bold">{hexcrawl.settlements.length}</div>
                      <div className="text-xs text-muted-foreground">Osad</div>
                    </div>
                    <div className="p-3 bg-muted rounded text-center">
                      <div className="text-2xl font-bold">{hexcrawl.dungeons.length}</div>
                      <div className="text-xs text-muted-foreground">Dungeonů</div>
                    </div>
                    <div className="p-3 bg-muted rounded text-center">
                      <div className="text-2xl font-bold">{hexcrawl.rumors.length}</div>
                      <div className="text-xs text-muted-foreground">Zvěstí</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Tabs for detailed content */}
              <Tabs defaultValue="hexes" className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="hexes">Hexy ({hexcrawl.hexes.length})</TabsTrigger>
                  <TabsTrigger value="settlements">Osady ({hexcrawl.settlements.length})</TabsTrigger>
                  <TabsTrigger value="dungeons">Dungeony ({hexcrawl.dungeons.length})</TabsTrigger>
                  <TabsTrigger value="rumors">Zvěsti ({hexcrawl.rumors.length})</TabsTrigger>
                </TabsList>

                {/* HEXES TAB */}
                <TabsContent value="hexes" className="space-y-3">
                  {hexcrawl.hexes.map((hex, idx) => (
                    <Card key={idx}>
                      <CardHeader>
                        <CardTitle className="flex items-center gap-3">
                          <span className="text-3xl">🗺️</span>
                          <div>
                            <div className="text-xl">Hex #{idx + 1}: {hex.type}</div>
                            <div className="text-sm text-muted-foreground font-normal">
                              Kategorie: {hex.detail_category}
                            </div>
                          </div>
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <div className="p-3 bg-muted rounded">
                          <div className="text-xs text-muted-foreground mb-1">DETAIL</div>
                          <div className="text-sm font-semibold">{hex.detail_name}</div>
                        </div>
                        <div className="p-3 bg-primary/10 rounded border border-primary/20">
                          <div className="text-xs text-muted-foreground mb-1">🎣 HOOK</div>
                          <div className="text-sm italic">"{hex.detail_hook}"</div>
                        </div>
                        {hex.settlement && (
                          <div className="p-3 bg-blue-50 rounded border border-blue-200">
                            <div className="text-xs text-muted-foreground mb-1">🏘️ OSADA</div>
                            <div className="text-sm font-medium">{hex.settlement.size_name}</div>
                            <div className="text-xs text-muted-foreground">{hex.settlement.population}</div>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </TabsContent>

                {/* SETTLEMENTS TAB */}
                <TabsContent value="settlements" className="space-y-3">
                  {hexcrawl.settlements.map((settlement, idx) => (
                    <Card key={idx}>
                      <CardHeader>
                        <div className="flex items-center gap-3">
                          <div className="text-5xl">🏘️</div>
                          <div>
                            {settlement.name && settlement.name.trim() !== "" && (
                              <CardTitle className="text-2xl mb-1">{settlement.name}</CardTitle>
                            )}
                            <div className="text-lg font-semibold text-muted-foreground">
                              {settlement.size_name}
                            </div>
                            <div className="text-sm text-muted-foreground">
                              Populace: {settlement.population}
                            </div>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <div className="p-3 bg-muted rounded">
                          <div className="text-xs text-muted-foreground mb-1">VLÁDA</div>
                          <div className="text-sm font-semibold">{settlement.government}</div>
                        </div>
                        <div className="p-3 bg-primary/10 rounded border border-primary/20">
                          <div className="text-xs text-muted-foreground mb-1">ZAJÍMAVOST</div>
                          <div className="text-sm font-medium">{settlement.detail}</div>
                        </div>
                        {settlement.trades && settlement.trades.length > 0 && (
                          <div className="p-3 bg-secondary/10 rounded border border-secondary/20">
                            <div className="text-xs text-muted-foreground mb-2">ŘEMESLA & SLUŽBY</div>
                            <ul className="text-sm space-y-1">
                              {settlement.trades.map((trade, i) => (
                                <li key={i}>• {trade}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {settlement.features && settlement.features.length > 0 && (
                          <div className="p-3 bg-green-50 rounded border border-green-200">
                            <div className="text-xs text-muted-foreground mb-2">PRVKY</div>
                            <ul className="text-sm space-y-1">
                              {settlement.features.map((feature, i) => (
                                <li key={i}>• {feature}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        <div className="p-3 bg-yellow-50 rounded border border-yellow-200">
                          <div className="text-xs text-muted-foreground mb-1">🎭 UDÁLOST</div>
                          <div className="text-sm font-medium">{settlement.event}</div>
                        </div>
                        {settlement.tavern && (
                          <div className="p-3 bg-orange-50 rounded border border-orange-200">
                            <div className="text-xs text-muted-foreground mb-1">🍺 HOSPODA</div>
                            <div className="text-sm font-semibold">
                              {settlement.tavern.name_part1} {settlement.tavern.name_part2}
                            </div>
                            <div className="text-xs text-muted-foreground mt-1">
                              Specialita: {settlement.tavern.specialty}
                            </div>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </TabsContent>

                {/* DUNGEONS TAB */}
                <TabsContent value="dungeons" className="space-y-4">
                  {hexcrawl.dungeons.map((dungeon, idx) => (
                    <div key={idx} className="space-y-3">
                      <Card>
                        <CardHeader>
                          <CardTitle className="flex items-center gap-2">
                            <span className="text-3xl">⚔️</span>
                            Dungeon #{idx + 1} ({dungeon.rooms.length} místností)
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          <div className="grid grid-cols-2 gap-3">
                            <div className="p-3 bg-muted rounded">
                              <div className="text-xs text-muted-foreground">MINULOST</div>
                              <div className="text-sm font-medium">{dungeon.past}</div>
                            </div>
                            <div className="p-3 bg-muted rounded">
                              <div className="text-xs text-muted-foreground">ÚPADEK</div>
                              <div className="text-sm font-medium">{dungeon.decay}</div>
                            </div>
                            <div className="p-3 bg-muted rounded">
                              <div className="text-xs text-muted-foreground">OBYVATELÉ</div>
                              <div className="text-sm font-medium">{dungeon.inhabitants}</div>
                            </div>
                            <div className="p-3 bg-muted rounded">
                              <div className="text-xs text-muted-foreground">CÍL</div>
                              <div className="text-sm font-medium">{dungeon.goal}</div>
                            </div>
                          </div>
                          <div className="p-3 bg-primary/10 rounded border border-primary/20">
                            <div className="text-xs text-muted-foreground mb-1">🔒 TAJEMSTVÍ</div>
                            <div className="text-sm font-medium">{dungeon.secret}</div>
                          </div>
                        </CardContent>
                      </Card>

                      {dungeon.rooms.map((room) => (
                        <Card key={room.room_number}>
                          <CardHeader>
                            <CardTitle className="flex items-center justify-between text-base">
                              <span className="flex items-center gap-2">
                                <span className="text-2xl">🚪</span>
                                Místnost #{room.room_number}: {room.room_type}
                              </span>
                              <div className="flex gap-2 text-sm">
                                {room.has_creature && <span>👹</span>}
                                {room.has_treasure && <span>💎</span>}
                              </div>
                            </CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="text-sm">{room.feature}</div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  ))}
                </TabsContent>

                {/* RUMORS TAB */}
                <TabsContent value="rumors" className="space-y-3">
                  {hexcrawl.rumors.map((rumor: any, idx) => (
                    <Card key={idx}>
                      <CardHeader>
                        <CardTitle className="flex items-center justify-between">
                          <span className="flex items-center gap-2">
                            <span className="text-2xl">📜</span>
                            Zvěst #{idx + 1}
                          </span>
                          <span className={`text-xs px-2 py-1 rounded ${
                            rumor.truthfulness === 'true'
                              ? 'bg-green-100 text-green-800'
                              : rumor.truthfulness === 'false'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {rumor.truthfulness === 'true' ? '✓ Pravda' : rumor.truthfulness === 'false' ? '✗ Lež' : '~ Částečně'}
                          </span>
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <div className="p-3 bg-muted rounded">
                          <div className="text-sm italic">"{rumor.rumor_text}"</div>
                        </div>
                        {rumor.gm_notes && (
                          <div className="p-3 bg-primary/10 rounded border border-primary/20">
                            <div className="text-xs text-muted-foreground mb-1">GM POZNÁMKY</div>
                            <div className="text-xs">{rumor.gm_notes}</div>
                          </div>
                        )}
                        <div className="flex gap-2 text-xs text-muted-foreground">
                          <span>Kategorie: {rumor.category}</span>
                          <span>•</span>
                          <span>Hod: {rumor.roll}</span>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </TabsContent>
              </Tabs>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
