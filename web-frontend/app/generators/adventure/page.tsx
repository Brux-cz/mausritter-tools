"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { generateAdventure, type AdventureResponse } from "@/lib/api";
import { toast } from "sonner";

export default function AdventureGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [adventure, setAdventure] = useState<AdventureResponse | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateAdventure({});
      setAdventure(result);
      toast.success("Dobrodružství vygenerováno!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (adventure) {
      navigator.clipboard.writeText(JSON.stringify(adventure, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setAdventure(null);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            🗺️ Adventure Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor dobrodružství - stvoření, problémy a komplikace
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Generovat dobrodružství</CardTitle>
                <CardDescription>
                  Vygeneruj základ pro novou quest nebo vedlejší úkol
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {adventure && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {adventure && (
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
            {adventure ? (
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className="text-5xl">🗺️</div>
                    <div>
                      <CardTitle className="text-2xl">Dobrodružství</CardTitle>
                      <div className="text-sm text-muted-foreground mt-1">
                        Hod: {adventure.roll}
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-primary/10 rounded border border-primary/20">
                    <div className="text-xs text-muted-foreground mb-2">STVOŘENÍ</div>
                    <div className="text-lg font-semibold">{adventure.creature}</div>
                  </div>

                  <div className="p-4 bg-secondary/10 rounded border border-secondary/20">
                    <div className="text-xs text-muted-foreground mb-2">PROBLÉM</div>
                    <div className="text-sm">{adventure.problem}</div>
                  </div>

                  <div className="p-4 bg-yellow-50 rounded border border-yellow-200">
                    <div className="text-xs text-muted-foreground mb-2">⚠️ KOMPLIKACE</div>
                    <div className="text-sm font-medium">{adventure.complication}</div>
                  </div>

                  {adventure.notes && adventure.notes.trim() !== "" && (
                    <div className="p-3 bg-muted rounded text-sm">
                      <strong>Poznámky:</strong> {adventure.notes}
                    </div>
                  )}
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">🗺️</div>
                  <p>Klikni na "Generovat" pro vytvoření dobrodružství</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
