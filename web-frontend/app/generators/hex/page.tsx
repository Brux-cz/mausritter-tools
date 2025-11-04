"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { generateHex, type HexRequest, type HexResponse } from "@/lib/api";
import { toast } from "sonner";

export default function HexGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [hex, setHex] = useState<HexResponse | null>(null);
  const [withSettlement, setWithSettlement] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const request: HexRequest = {
        with_settlement: withSettlement,
      };
      const result = await generateHex(request);
      setHex(result);
      toast.success("Hex vygenerován!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (hex) {
      navigator.clipboard.writeText(JSON.stringify(hex, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setHex(null);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            🗺️ Hex Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor hexů pro průzkum světa - lokace, nebezpečí a zajímavosti
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Column */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Možnosti</CardTitle>
                <CardDescription>
                  Nastav parametry pro generování hexu
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="withSettlement"
                    checked={withSettlement}
                    onChange={(e) => setWithSettlement(e.target.checked)}
                    disabled={loading}
                    className="h-4 w-4 rounded border-gray-300"
                  />
                  <Label htmlFor="withSettlement" className="cursor-pointer">
                    Zahrnout osadu (pokud je to lidský hex)
                  </Label>
                </div>

                <div className="flex gap-2 pt-4">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {hex && (
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
                <CardTitle>O Hex Generatoru</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <p>Tento generátor vytváří náhodné hexy pro průzkum světa:</p>
                <ul className="list-disc list-inside space-y-1 ml-2">
                  <li><strong>6 typů hexů:</strong> Pole, Les, Pustina, Lidská oblast, Hory, Voda</li>
                  <li><strong>Unikátní detaily:</strong> Každý typ má vlastní tabulku zajímavostí</li>
                  <li><strong>Hooks:</strong> Otázky pro GM k rozvíjení příběhu</li>
                  <li><strong>Osady:</strong> Lidské hexy mohou obsahovat města a vesnice</li>
                </ul>
              </CardContent>
            </Card>

            {/* Actions */}
            {hex && (
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
            {hex ? (
              <Card className={hex.is_settlement ? "border-blue-500 border-2" : ""}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className="text-5xl">{hex.type_emoji}</div>
                    <div>
                      <CardTitle className="text-2xl">{hex.type}</CardTitle>
                      <div className="text-sm text-muted-foreground mt-1">
                        Hod: {hex.type_roll}
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Detail Name */}
                  <div className="p-4 bg-muted rounded">
                    <div className="text-xs text-muted-foreground mb-2">DETAIL</div>
                    <div className="text-xl font-semibold mb-2">{hex.detail.name}</div>
                    <div className="text-sm text-muted-foreground">
                      {hex.detail.category_name}
                    </div>
                  </div>

                  {/* Hook */}
                  <div className="p-4 bg-primary/10 rounded border border-primary/20">
                    <div className="text-xs text-muted-foreground mb-2">🎣 HOOK (OTÁZKA PRO GM)</div>
                    <div className="text-sm font-medium italic">"{hex.detail.hook}"</div>
                  </div>

                  {/* Description */}
                  {hex.description && hex.description.trim() !== "" && (
                    <div className="p-4 bg-secondary/10 rounded border border-secondary/20">
                      <div className="text-xs text-muted-foreground mb-2">POPIS</div>
                      <div className="text-sm">{hex.description}</div>
                    </div>
                  )}

                  {/* Settlement indicator */}
                  {hex.is_settlement && (
                    <div className="p-3 bg-blue-50 border border-blue-200 rounded text-sm text-blue-800">
                      <strong>🏘️ Obsahuje osadu!</strong> Tento hex obsahuje lidské sídliště.
                      <div className="text-xs mt-1 text-blue-600">
                        (Detaily osady zatím nejsou implementovány - použij Settlement Generator)
                      </div>
                    </div>
                  )}

                  {/* Technical info */}
                  <div className="text-xs text-muted-foreground border-t pt-3 space-y-1">
                    <div>Kategorie: {hex.detail.category}</div>
                    <div>Subtype: {hex.detail.subtype}</div>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">🗺️</div>
                  <p>Klikni na "Generovat" pro vytvoření hexu</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
