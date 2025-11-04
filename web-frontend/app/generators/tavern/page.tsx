"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { generateTavern, type TavernResponse } from "@/lib/api";
import { toast } from "sonner";

export default function TavernGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [tavern, setTavern] = useState<TavernResponse | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateTavern({});
      setTavern(result);
      toast.success("Hospoda vygenerována!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (tavern) {
      navigator.clipboard.writeText(JSON.stringify(tavern, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setTavern(null);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            🍺 Tavern Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor hospod a taveren - název a specialita
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Generovat hospodu</CardTitle>
                <CardDescription>
                  Vygeneruj název a specialitu pro tavernu
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {tavern && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {tavern && (
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
            {tavern ? (
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className="text-5xl">🍺</div>
                    <div>
                      <CardTitle className="text-2xl">{tavern.full_name}</CardTitle>
                      <div className="text-sm text-muted-foreground mt-1">
                        Hody: {tavern.roll_part1} + {tavern.roll_part2}
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-primary/10 rounded border border-primary/20">
                    <div className="text-xs text-muted-foreground mb-2">SPECIALITA</div>
                    <div className="text-sm font-medium">{tavern.specialty}</div>
                    <div className="text-xs text-muted-foreground mt-2">
                      Hod: {tavern.roll_specialty}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">🍺</div>
                  <p>Klikni na "Generovat" pro vytvoření hospody</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
