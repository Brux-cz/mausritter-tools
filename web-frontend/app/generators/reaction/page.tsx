"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { generateReaction, type ReactionRequest, type ReactionResponse } from "@/lib/api";
import { toast } from "sonner";

const modifierOptions = Array.from({ length: 13 }, (_, i) => i - 6);

export default function ReactionGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [reaction, setReaction] = useState<ReactionResponse | null>(null);
  const [modifier, setModifier] = useState(0);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const request: ReactionRequest = {
        modifier: modifier,
      };
      const result = await generateReaction(request);
      setReaction(result);
      toast.success("Reakce vygenerována!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (reaction) {
      navigator.clipboard.writeText(JSON.stringify(reaction, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setReaction(null);
    setModifier(0);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            🎭 Reaction Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Generátor reakcí NPC - zjisti, jak postava reaguje na setkání s hráči
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Column */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Možnosti</CardTitle>
                <CardDescription>
                  Nastav modifikátor reakce (-6 až +6)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="modifier">Modifikátor ({modifier >= 0 ? '+' : ''}{modifier})</Label>
                  <Select
                    value={modifier.toString()}
                    onValueChange={(value) => setModifier(parseInt(value))}
                  >
                    <SelectTrigger id="modifier" disabled={loading}>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {modifierOptions.map((mod) => (
                        <SelectItem key={mod} value={mod.toString()}>
                          {mod >= 0 ? '+' : ''}{mod}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex gap-2 pt-4">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {reaction && (
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
                <CardTitle>O Reaction Generatoru</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <p>Tento generátor určuje reakci NPC při setkání:</p>
                <ul className="list-disc list-inside space-y-1 ml-2">
                  <li><strong>Hod 2k6:</strong> + modifikátor</li>
                  <li><strong>Výsledky:</strong> Od nepřátelské až po přátelskou</li>
                  <li><strong>Modifikátory:</strong> Charisma, kontext, dar</li>
                  <li><strong>Otázka pro GM:</strong> Pomůcka pro roleplay</li>
                </ul>
                <div className="mt-3 p-3 bg-muted rounded text-xs">
                  <strong>Tipy:</strong>
                  <ul className="list-disc list-inside mt-1 space-y-1">
                    <li>Negativní modifikátor: Podezřelý vzhled, špatná pověst</li>
                    <li>Pozitivní modifikátor: Dar, společný zájem, doporučení</li>
                  </ul>
                </div>
              </CardContent>
            </Card>

            {/* Actions */}
            {reaction && (
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
            {reaction ? (
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <div className="text-5xl">🎭</div>
                    <div>
                      <CardTitle className="text-2xl">{reaction.reaction}</CardTitle>
                      <div className="text-sm text-muted-foreground mt-1">
                        Hod: {reaction.roll}
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Question */}
                  <div className="p-4 bg-primary/10 rounded border border-primary/20">
                    <div className="text-xs text-muted-foreground mb-2">❓ OTÁZKA PRO GM</div>
                    <div className="text-sm font-medium italic">"{reaction.question}"</div>
                  </div>

                  {/* Notes */}
                  {reaction.notes && reaction.notes.trim() !== "" && (
                    <div className="p-4 bg-secondary/10 rounded border border-secondary/20">
                      <div className="text-xs text-muted-foreground mb-2">📝 POZNÁMKY</div>
                      <div className="text-sm">{reaction.notes}</div>
                    </div>
                  )}

                  {/* Reaction Guide */}
                  <div className="p-4 bg-muted rounded">
                    <div className="text-xs text-muted-foreground mb-3">INTERPRETACE</div>
                    <div className="text-sm space-y-2">
                      {reaction.roll <= 3 && (
                        <p className="text-red-700"><strong>Nepřátelská:</strong> NPC je agresivní nebo výrazně negativní. Může zaútočit nebo odmítnout jakoukoliv spolupráci.</p>
                      )}
                      {reaction.roll >= 4 && reaction.roll <= 6 && (
                        <p className="text-orange-700"><strong>Opatrná:</strong> NPC je podezřívavý a chladný. Komunikuje, ale není ochotný pomoci bez důvodu.</p>
                      )}
                      {reaction.roll >= 7 && reaction.roll <= 9 && (
                        <p className="text-blue-700"><strong>Neutrální:</strong> NPC je otevřený rozhovoru. Standardní obchodní nebo společenská interakce.</p>
                      )}
                      {reaction.roll >= 10 && reaction.roll <= 11 && (
                        <p className="text-green-700"><strong>Povídavá:</strong> NPC je přátelský a ochotný pomoci. Může nabídnout informace nebo služby.</p>
                      )}
                      {reaction.roll >= 12 && (
                        <p className="text-emerald-700"><strong>Přátelská:</strong> NPC je velmi nakloněný postavám. Může nabídnout pomoc zdarma nebo výhody.</p>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">🎭</div>
                  <p>Klikni na "Generovat" pro určení reakce</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
