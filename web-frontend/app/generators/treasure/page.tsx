"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { generateTreasure, type TreasureRequest, type TreasureResponse } from "@/lib/api";
import { toast } from "sonner";

export default function TreasureGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [treasure, setTreasure] = useState<TreasureResponse | null>(null);
  const [bonus, setBonus] = useState(0);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateTreasure({ bonus });
      setTreasure(result);
      toast.success("Poklad vygenerován!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (treasure) {
      navigator.clipboard.writeText(JSON.stringify(treasure, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setTreasure(null);
    setBonus(0);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            💎 Treasure Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor pokladů - peníze, magické předměty, zbraně a další
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Možnosti</CardTitle>
                <CardDescription>
                  Nastav bonus hodů (0-4)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="bonus">Bonus hodů (+{bonus})</Label>
                  <Select value={bonus.toString()} onValueChange={(value) => setBonus(parseInt(value))}>
                    <SelectTrigger id="bonus" disabled={loading}>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {[0, 1, 2, 3, 4].map((val) => (
                        <SelectItem key={val} value={val.toString()}>
                          +{val}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex gap-2 pt-4">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {treasure && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {treasure && (
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

          <div>
            {treasure ? (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-2xl">Poklad</CardTitle>
                      <div className="text-sm text-muted-foreground mt-1">
                        {treasure.total_rolls} položek • Celkem {treasure.total_value}p
                      </div>
                    </div>
                    <div className="text-5xl">💎</div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  {treasure.items.map((item, idx) => (
                    <div key={idx} className="p-4 bg-muted rounded border">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <div className="font-semibold">{item.name}</div>
                          <div className="text-xs text-muted-foreground mt-1">{item.type}</div>
                        </div>
                        {item.value !== null && (
                          <div className="text-sm font-medium text-green-700">
                            {item.value}p
                          </div>
                        )}
                      </div>
                      <div className="text-sm text-muted-foreground">{item.description}</div>
                      <div className="flex gap-3 mt-2 text-xs text-muted-foreground">
                        <span>Sloty: {item.slots}</span>
                        {item.quantity > 1 && <span>× {item.quantity}</span>}
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">💎</div>
                  <p>Klikni na "Generovat" pro vytvoření pokladu</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
