"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { generateDungeon, type DungeonRequest, type DungeonResponse } from "@/lib/api";
import { toast } from "sonner";

export default function DungeonGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [dungeon, setDungeon] = useState<DungeonResponse | null>(null);
  const [rooms, setRooms] = useState(5);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateDungeon({ rooms });
      setDungeon(result);
      toast.success("Dungeon vygenerován!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (dungeon) {
      navigator.clipboard.writeText(JSON.stringify(dungeon, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setDungeon(null);
    setRooms(5);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            ⚔️ Dungeon Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor dungeonů - jeskyně, podzemí, ruiny
          </p>
        </div>

        <div className="grid grid-cols-1 gap-8">
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Možnosti</CardTitle>
                <CardDescription>
                  Nastav počet místností (1-20)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="rooms">Počet místností: {rooms}</Label>
                  <Select value={rooms.toString()} onValueChange={(val) => setRooms(parseInt(val))}>
                    <SelectTrigger id="rooms" disabled={loading}>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {Array.from({ length: 20 }, (_, i) => i + 1).map((val) => (
                        <SelectItem key={val} value={val.toString()}>
                          {val} místností
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex gap-2">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {dungeon && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {dungeon && (
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

          {dungeon && (
            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <span className="text-3xl">⚔️</span>
                    Dungeon ({dungeon.room_count} místností)
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-3 bg-muted rounded">
                      <div className="text-xs text-muted-foreground">MINULOST</div>
                      <div className="text-sm font-medium">{dungeon.past.name}</div>
                    </div>
                    <div className="p-3 bg-muted rounded">
                      <div className="text-xs text-muted-foreground">ÚPADEK</div>
                      <div className="text-sm font-medium">{dungeon.decay.name}</div>
                    </div>
                    <div className="p-3 bg-muted rounded">
                      <div className="text-xs text-muted-foreground">OBYVATELÉ</div>
                      <div className="text-sm font-medium">{dungeon.inhabitants.name}</div>
                    </div>
                    <div className="p-3 bg-muted rounded">
                      <div className="text-xs text-muted-foreground">CÍL</div>
                      <div className="text-sm font-medium">{dungeon.goal.name}</div>
                    </div>
                  </div>
                  <div className="p-4 bg-primary/10 rounded border border-primary/20">
                    <div className="text-xs text-muted-foreground mb-2">🔒 TAJEMSTVÍ</div>
                    <div className="text-sm font-medium">{dungeon.secret.name}</div>
                  </div>
                </CardContent>
              </Card>

              {dungeon.rooms.map((room) => (
                <Card key={room.number}>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <span className="text-2xl">{room.type.emoji}</span>
                        Místnost #{room.number}: {room.type.name}
                      </span>
                      <div className="flex gap-2 text-sm">
                        {room.has_creature && <span>👹</span>}
                        {room.has_treasure && <span>💎</span>}
                      </div>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-sm">{room.feature.name}</div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
