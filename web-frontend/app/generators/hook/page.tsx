"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { generateHook, type HookResponse } from "@/lib/api";
import { toast } from "sonner";

export default function HookGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [hook, setHook] = useState<HookResponse | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateHook({});
      setHook(result);
      toast.success("Hook vygenerován!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (hook) {
      navigator.clipboard.writeText(JSON.stringify(hook, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setHook(null);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            🎣 Hook Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor příběhových hooků - záchytné body pro kampaň
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Generovat Hook</CardTitle>
                <CardDescription>
                  Vygeneruj záchytný bod pro nové dobrodružství
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {hook && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {hook && (
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
            {hook ? (
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className="text-5xl">🎣</div>
                    <div>
                      <CardTitle className="text-2xl">{hook.category_name}</CardTitle>
                      <div className="text-sm text-muted-foreground mt-1">
                        Hod: {hook.roll}
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-primary/10 rounded border border-primary/20">
                    <div className="text-xs text-muted-foreground mb-2">HOOK</div>
                    <div className="text-sm font-medium">{hook.hook}</div>
                  </div>

                  {hook.questions && hook.questions.length > 0 && (
                    <div className="p-4 bg-secondary/10 rounded border border-secondary/20">
                      <div className="text-xs text-muted-foreground mb-3">❓ OTÁZKY PRO GM</div>
                      <ul className="space-y-2">
                        {hook.questions.map((q, idx) => (
                          <li key={idx} className="text-sm flex gap-2">
                            <span className="text-muted-foreground">•</span>
                            <span>{q}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">🎣</div>
                  <p>Klikni na "Generovat" pro vytvoření hooku</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
