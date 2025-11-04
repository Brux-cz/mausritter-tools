"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { generateSettlement, type SettlementRequest, type SettlementResponse } from "@/lib/api";
import { toast } from "sonner";

export default function SettlementGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [settlement, setSettlement] = useState<SettlementResponse | null>(null);
  const [withName, setWithName] = useState(false);
  const [noTavern, setNoTavern] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const request: SettlementRequest = {
        with_name: withName,
        no_tavern: noTavern,
      };
      const result = await generateSettlement(request);
      setSettlement(result);
      toast.success("Osada vygenerována!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (settlement) {
      navigator.clipboard.writeText(JSON.stringify(settlement, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setSettlement(null);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            🏘️ Settlement Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor osad - vesnice, města, tržiště a jejich charakteristiky
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Column */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Možnosti</CardTitle>
                <CardDescription>
                  Nastav parametry pro generování osady
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="withName"
                    checked={withName}
                    onChange={(e) => setWithName(e.target.checked)}
                    disabled={loading}
                    className="h-4 w-4 rounded border-gray-300"
                  />
                  <Label htmlFor="withName" className="cursor-pointer">
                    Generovat název osady
                  </Label>
                </div>

                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="noTavern"
                    checked={noTavern}
                    onChange={(e) => setNoTavern(e.target.checked)}
                    disabled={loading}
                    className="h-4 w-4 rounded border-gray-300"
                  />
                  <Label htmlFor="noTavern" className="cursor-pointer">
                    Bez hospody/taverny
                  </Label>
                </div>

                <div className="flex gap-2 pt-4">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {settlement && (
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
                <CardTitle>O Settlement Generatoru</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <p>Tento generátor vytváří osady s následujícími vlastnostmi:</p>
                <ul className="list-disc list-inside space-y-1 ml-2">
                  <li><strong>Velikost:</strong> Od samoty až po velkoměsto (2k6)</li>
                  <li><strong>Vláda:</strong> Způsob správy osady</li>
                  <li><strong>Zajímavost:</strong> Unikátní charakteristika</li>
                  <li><strong>Řemesla:</strong> Dostupné služby a produkty</li>
                  <li><strong>Prvky:</strong> Architektonické zajímavosti</li>
                  <li><strong>Událost:</strong> Co se právě děje v osadě</li>
                </ul>
              </CardContent>
            </Card>

            {/* Actions */}
            {settlement && (
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
            {settlement ? (
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className="text-5xl">🏘️</div>
                    <div>
                      {settlement.name && (
                        <CardTitle className="text-2xl mb-1">{settlement.name}</CardTitle>
                      )}
                      <div className="text-lg font-semibold text-muted-foreground">
                        {settlement.size.name}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Populace: {settlement.size.population}
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Government */}
                  <div className="p-4 bg-muted rounded">
                    <div className="text-xs text-muted-foreground mb-2">VLÁDA</div>
                    <div className="text-sm font-semibold">{settlement.government}</div>
                  </div>

                  {/* Detail */}
                  <div className="p-4 bg-primary/10 rounded border border-primary/20">
                    <div className="text-xs text-muted-foreground mb-2">ZAJÍMAVOST</div>
                    <div className="text-sm font-medium">{settlement.detail}</div>
                  </div>

                  {/* Trades */}
                  {settlement.trades && settlement.trades.length > 0 && (
                    <div className="p-4 bg-secondary/10 rounded border border-secondary/20">
                      <div className="text-xs text-muted-foreground mb-2">ŘEMESLA & SLUŽBY</div>
                      <ul className="text-sm space-y-1">
                        {settlement.trades.map((trade, idx) => (
                          <li key={idx}>• {trade}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Features */}
                  {settlement.features && settlement.features.length > 0 && (
                    <div className="p-4 bg-green-50 rounded border border-green-200">
                      <div className="text-xs text-muted-foreground mb-2">ARCHITEKTONICKÉ PRVKY</div>
                      <ul className="text-sm space-y-1">
                        {settlement.features.map((feature, idx) => (
                          <li key={idx}>• {feature}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Event */}
                  <div className="p-4 bg-yellow-50 rounded border border-yellow-200">
                    <div className="text-xs text-muted-foreground mb-2">🎭 AKTUÁLNÍ UDÁLOST</div>
                    <div className="text-sm font-medium">{settlement.event}</div>
                  </div>

                  {/* Tavern */}
                  {settlement.tavern && (
                    <div className="p-4 bg-orange-50 rounded border border-orange-200">
                      <div className="text-xs text-muted-foreground mb-2">🍺 HOSPODA</div>
                      <div className="text-sm font-semibold mb-1">{settlement.tavern.name}</div>
                      <div className="text-sm text-muted-foreground">
                        Specialita: {settlement.tavern.specialty}
                      </div>
                    </div>
                  )}

                  {/* Technical info */}
                  {settlement.rolls && (
                    <div className="text-xs text-muted-foreground border-t pt-3">
                      Velikost (hody): {settlement.rolls.size_die1} + {settlement.rolls.size_die2} = {settlement.size.value}
                    </div>
                  )}
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">🏘️</div>
                  <p>Klikni na "Generovat" pro vytvoření osady</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
