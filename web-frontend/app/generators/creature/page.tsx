"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { generateCreature, type CreatureResponse } from "@/lib/api";
import { toast } from "sonner";

const creatureTypes = [
  { value: "ghost", label: "Duch (Ghost)" },
  { value: "snake", label: "Had (Snake)" },
  { value: "cat", label: "Kočka (Cat)" },
  { value: "rat", label: "Krysa (Rat)" },
  { value: "mouse", label: "Myš (Mouse)" },
  { value: "spider", label: "Pavouk (Spider)" },
  { value: "owl", label: "Sova (Owl)" },
  { value: "centipede", label: "Stonožka (Centipede)" },
  { value: "fairy", label: "Víla (Fairy)" },
  { value: "crow", label: "Vrána (Crow)" },
  { value: "frog", label: "Žába (Frog)" },
];

export default function CreatureGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [creature, setCreature] = useState<CreatureResponse | null>(null);
  const [selectedType, setSelectedType] = useState<string>("cat");

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateCreature(selectedType as any);
      setCreature(result);
      toast.success("Varianta tvora vygenerována!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (creature) {
      navigator.clipboard.writeText(JSON.stringify(creature, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setCreature(null);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            🐾 Creature Variant Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor variant tvorů - unikátní verze běžných nepřátel
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Možnosti</CardTitle>
                <CardDescription>
                  Vyber typ tvora
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="type">Typ tvora</Label>
                  <Select value={selectedType} onValueChange={setSelectedType}>
                    <SelectTrigger id="type" disabled={loading}>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {creatureTypes.map((type) => (
                        <SelectItem key={type.value} value={type.value}>
                          {type.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex gap-2 pt-4">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {creature && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {creature && (
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

          <div>
            {creature ? (
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className="text-5xl">🐾</div>
                    <div>
                      <CardTitle className="text-2xl">{creature.variant}</CardTitle>
                      <div className="text-sm text-muted-foreground mt-1">
                        {creature.creature_type} • Hod: {creature.roll}
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-primary/10 rounded border border-primary/20">
                    <div className="text-xs text-muted-foreground mb-2">POPIS</div>
                    <div className="text-sm">{creature.description}</div>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">🐾</div>
                  <p>Klikni na "Generovat" pro vytvoření varianty tvora</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
