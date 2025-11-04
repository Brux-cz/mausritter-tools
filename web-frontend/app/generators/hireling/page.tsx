"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { generateHireling, type HirelingRequest, type HirelingResponse } from "@/lib/api";
import { toast } from "sonner";

const hirelingTypes = [
  { value: 1, label: "Průvodce" },
  { value: 2, label: "Překladatel" },
  { value: 3, label: "Učenec" },
  { value: 4, label: "Pomocník" },
  { value: 5, label: "Továrník" },
  { value: 6, label: "Válečník" },
  { value: 7, label: "Specialista" },
  { value: 8, label: "Strážný" },
  { value: 9, label: "Průzkumník" },
];

export default function HirelingGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [hireling, setHireling] = useState<HirelingResponse | null>(null);
  const [customName, setCustomName] = useState("");
  const [hirelingType, setHirelingType] = useState<number | undefined>(undefined);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const request: HirelingRequest = {};
      if (customName.trim()) request.name = customName.trim();
      if (hirelingType) request.type = hirelingType;

      const result = await generateHireling(request);
      setHireling(result);
      toast.success("Žoldnéř vygenerován!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (hireling) {
      navigator.clipboard.writeText(JSON.stringify(hireling, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setHireling(null);
    setCustomName("");
    setHirelingType(undefined);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            ⚔️ Hireling Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor žoldnéřů a pomocníků - průvodci, válečníci, specialisté a další
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Column */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Možnosti</CardTitle>
                <CardDescription>
                  Nastav parametry pro generování žoldnéře
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Vlastní jméno (volitelné)</Label>
                  <Input
                    id="name"
                    type="text"
                    value={customName}
                    onChange={(e) => setCustomName(e.target.value)}
                    placeholder="Např: Hroch Statečný"
                    disabled={loading}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="type">Typ žoldnéře (volitelný)</Label>
                  <Select
                    value={hirelingType?.toString()}
                    onValueChange={(value) => setHirelingType(value ? parseInt(value) : undefined)}
                  >
                    <SelectTrigger id="type" disabled={loading}>
                      <SelectValue placeholder="Náhodný typ" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0">Náhodný typ</SelectItem>
                      {hirelingTypes.map((type) => (
                        <SelectItem key={type.value} value={type.value.toString()}>
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
                  {hireling && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Info Card */}
            <Card className="mt-4">
              <CardHeader>
                <CardTitle>O Hireling Generatoru</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <p>Tento generátor vytváří žoldnéře s následujícími vlastnostmi:</p>
                <ul className="list-disc list-inside space-y-1 ml-2">
                  <li><strong>9 typů:</strong> Průvodce, Překladatel, Učenec, atd.</li>
                  <li><strong>Stats:</strong> STR, DEX, WIL, HP</li>
                  <li><strong>Denní mzda:</strong> Cena za den práce</li>
                  <li><strong>Morálka:</strong> Jak je spolehlivý</li>
                  <li><strong>Dostupnost:</strong> Jak snadné je ho najít</li>
                </ul>
              </CardContent>
            </Card>

            {/* Actions */}
            {hireling && (
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
            {hireling ? (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-2xl">{hireling.name}</CardTitle>
                      <div className="text-sm text-muted-foreground mt-1">
                        {hireling.type} • {hireling.daily_wage}p/den
                      </div>
                    </div>
                    <div className="text-5xl">⚔️</div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Stats */}
                  <div className="grid grid-cols-4 gap-3">
                    <div className="p-3 bg-muted rounded text-center">
                      <div className="text-xs text-muted-foreground mb-1">HP</div>
                      <div className="text-2xl font-bold">{hireling.hp}</div>
                    </div>
                    <div className="p-3 bg-muted rounded text-center">
                      <div className="text-xs text-muted-foreground mb-1">STR</div>
                      <div className="text-2xl font-bold">{hireling.strength}</div>
                    </div>
                    <div className="p-3 bg-muted rounded text-center">
                      <div className="text-xs text-muted-foreground mb-1">DEX</div>
                      <div className="text-2xl font-bold">{hireling.dexterity}</div>
                    </div>
                    <div className="p-3 bg-muted rounded text-center">
                      <div className="text-xs text-muted-foreground mb-1">WIL</div>
                      <div className="text-2xl font-bold">{hireling.willpower}</div>
                    </div>
                  </div>

                  {/* Notes */}
                  <div className="p-4 bg-primary/10 rounded border border-primary/20">
                    <div className="text-xs text-muted-foreground mb-2">POPIS</div>
                    <div className="text-sm">{hireling.notes}</div>
                  </div>

                  {/* Morale & Availability */}
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-3 bg-secondary/10 rounded border border-secondary/20">
                      <div className="text-xs text-muted-foreground mb-1">MORÁLKA</div>
                      <div className="text-sm font-medium capitalize">{hireling.morale}</div>
                    </div>
                    <div className="p-3 bg-green-50 rounded border border-green-200">
                      <div className="text-xs text-muted-foreground mb-1">DOSTUPNOST</div>
                      <div className="text-sm font-medium">Hod: {hireling.availability}</div>
                    </div>
                  </div>

                  {/* Level & Experience */}
                  <div className="p-3 bg-yellow-50 rounded border border-yellow-200">
                    <div className="text-xs text-muted-foreground mb-1">ÚROVEŇ & ZKUŠENOSTI</div>
                    <div className="text-sm">
                      Úroveň {hireling.level} • {hireling.experience} XP
                    </div>
                  </div>

                  {/* Inventory */}
                  <div className="p-4 bg-muted rounded">
                    <div className="text-xs text-muted-foreground mb-3">INVENTÁŘ ({hireling.inventory.filter(i => i !== null).length}/{hireling.inventory.length})</div>
                    <div className="grid grid-cols-3 gap-2">
                      {hireling.inventory.map((item, idx) => (
                        <div
                          key={idx}
                          className={`p-2 rounded border text-center text-xs ${
                            item
                              ? "bg-primary/10 border-primary/30"
                              : "bg-background border-border"
                          }`}
                        >
                          {item || `Slot ${idx + 1}`}
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">⚔️</div>
                  <p>Klikni na "Generovat" pro vytvoření žoldnéře</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
