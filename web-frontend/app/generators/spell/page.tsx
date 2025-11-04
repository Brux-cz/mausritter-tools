"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { generateSpell, type SpellResponse } from "@/lib/api";
import { toast } from "sonner";

export default function SpellGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [spell, setSpell] = useState<SpellResponse | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateSpell({});
      setSpell(result);
      toast.success("Kouzlo vygenerováno!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (spell) {
      navigator.clipboard.writeText(JSON.stringify(spell, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setSpell(null);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            ✨ Spell Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor kouzel - magické schopnosti, efekty a podmínky pro dobití
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Generovat kouzlo</CardTitle>
                <CardDescription>
                  Vygeneruj náhodné kouzlo z Mausritter tabulek
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {spell && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {spell && (
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
            {spell ? (
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className="text-5xl">✨</div>
                    <div>
                      <CardTitle className="text-2xl">{spell.name}</CardTitle>
                      <div className="text-sm text-muted-foreground mt-1">
                        Hod: {spell.roll}
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-primary/10 rounded border border-primary/20">
                    <div className="text-xs text-muted-foreground mb-2">EFEKT</div>
                    <div className="text-sm">{spell.effect}</div>
                  </div>

                  <div className="p-4 bg-secondary/10 rounded border border-secondary/20">
                    <div className="text-xs text-muted-foreground mb-2">DOBITÍ</div>
                    <div className="text-sm">{spell.recharge}</div>
                  </div>

                  {spell.tags && spell.tags.length > 0 && (
                    <div className="flex gap-2 flex-wrap">
                      {spell.tags.map((tag, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-1 bg-muted rounded text-xs font-medium"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">✨</div>
                  <p>Klikni na "Generovat" pro vytvoření kouzla</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
