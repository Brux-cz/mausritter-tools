"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { generateNPC, type NPCRequest, type NPCResponse } from "@/lib/api";
import { toast } from "sonner";

export default function NPCGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [npc, setNpc] = useState<NPCResponse | null>(null);
  const [name, setName] = useState("");
  const [gender, setGender] = useState<"male" | "female" | undefined>(undefined);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const request: NPCRequest = {
        name: name || undefined,
        gender: gender,
      };
      const result = await generateNPC(request);
      setNpc(result);
      toast.success("NPC vygenerováno!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (npc) {
      navigator.clipboard.writeText(JSON.stringify(npc, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setNpc(null);
    setName("");
    setGender(undefined);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            👥 NPC Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Rychlé vytvoření NPC s osobností, motivacemi a vztahy
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Column */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Možnosti</CardTitle>
                <CardDescription>
                  Volitelně zadej jméno a pohlaví
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Jméno (volitelné)</Label>
                  <Input
                    id="name"
                    placeholder="např. Strážný"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    disabled={loading}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="gender">Pohlaví (volitelné)</Label>
                  <Select value={gender} onValueChange={(value: "male" | "female") => setGender(value)}>
                    <SelectTrigger id="gender" disabled={loading}>
                      <SelectValue placeholder="Náhodné" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="male">Samec</SelectItem>
                      <SelectItem value="female">Samice</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex gap-2 pt-4">
                  <Button onClick={handleGenerate} disabled={loading} className="flex-1">
                    {loading ? "Generuji..." : "🎲 Generovat"}
                  </Button>
                  {npc && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Actions */}
            {npc && (
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
            {npc ? (
              <Card>
                <CardHeader>
                  <CardTitle className="text-2xl">{npc.name}</CardTitle>
                  <CardDescription className="text-base">
                    {npc.gender === "male" ? "♂" : "♀"} {npc.social_status}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Basic Info */}
                  <div className="space-y-3">
                    <div className="p-3 bg-muted rounded">
                      <div className="text-xs text-muted-foreground mb-1">Rodné znamení</div>
                      <div className="font-medium">{npc.birthsign}</div>
                    </div>

                    <div className="p-3 bg-muted rounded">
                      <div className="text-xs text-muted-foreground mb-1">Vzhled</div>
                      <div className="font-medium">{npc.appearance}</div>
                    </div>

                    <div className="p-3 bg-muted rounded">
                      <div className="text-xs text-muted-foreground mb-1">Zvláštnost</div>
                      <div className="font-medium">{npc.quirk}</div>
                    </div>

                    <div className="p-3 bg-muted rounded">
                      <div className="text-xs text-muted-foreground mb-1">Po čem touží</div>
                      <div className="font-medium">{npc.desire}</div>
                    </div>

                    <div className="p-3 bg-muted rounded">
                      <div className="text-xs text-muted-foreground mb-1">Vztah k jiné myši</div>
                      <div className="font-medium">{npc.relationship}</div>
                    </div>

                    <div className="p-3 bg-muted rounded">
                      <div className="text-xs text-muted-foreground mb-1">Reakce při setkání</div>
                      <div className="font-medium">{npc.reaction}</div>
                      <div className="text-xs text-muted-foreground mt-1">
                        (Hod: {npc.roll_reaction})
                      </div>
                    </div>
                  </div>

                  {/* Dice Rolls Info */}
                  <div className="pt-4 border-t text-xs text-muted-foreground space-y-1">
                    <div className="font-semibold mb-2">Hody kostek:</div>
                    <div>Status: {npc.roll_social_status} • Znamení: {npc.roll_birthsign}</div>
                    <div>Vzhled: {npc.roll_appearance} • Quirk: {npc.roll_quirk}</div>
                    <div>Touha: {npc.roll_desire} • Vztah: {npc.roll_relationship}</div>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">👥</div>
                  <p>Klikni na "Generovat" pro vytvoření NPC</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
