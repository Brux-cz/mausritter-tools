"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { generateRumor, type RumorResponse } from "@/lib/api";
import { toast } from "sonner";

export default function RumorGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [rumor, setRumor] = useState<RumorResponse | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateRumor({});
      setRumor(result);
      toast.success("Zvěsti vygenerovány!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (rumor) {
      navigator.clipboard.writeText(JSON.stringify(rumor, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setRumor(null);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            📜 Rumor Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor zvěstí a pomluv - informace z hospod a tržišť
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Generovat zvěsti</CardTitle>
                <CardDescription>
                  Vygeneruj sadu pomluv a drb
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {rumor && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {rumor && (
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
            {rumor ? (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <span className="text-3xl">📜</span>
                    Zvěsti ({rumor.rumors.length})
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {rumor.rumors.map((r, idx) => (
                    <div key={idx} className="p-4 bg-muted rounded border">
                      <div className="text-sm mb-2">{r.rumor}</div>
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <span className="font-medium">{r.truthfulness}</span>
                        <span>Hod: {r.roll}</span>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">📜</div>
                  <p>Klikni na "Generovat" pro vytvoření zvěstí</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
