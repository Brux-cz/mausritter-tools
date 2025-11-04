"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { generateCharacter, type CharacterRequest, type CharacterResponse } from "@/lib/api";
import { toast } from "sonner";

export default function CharacterGeneratorPage() {
  const [loading, setLoading] = useState(false);
  const [character, setCharacter] = useState<CharacterResponse | null>(null);
  const [name, setName] = useState("");
  const [gender, setGender] = useState<"male" | "female" | undefined>(undefined);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const request: CharacterRequest = {
        name: name || undefined,
        gender: gender,
      };
      const result = await generateCharacter(request);
      setCharacter(result);
      toast.success("Postava vygenerována!");
    } catch (error: any) {
      toast.error(`Chyba: ${error.message}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyJSON = () => {
    if (character) {
      navigator.clipboard.writeText(JSON.stringify(character, null, 2));
      toast.success("JSON zkopírován do schránky!");
    }
  };

  const handleReset = () => {
    setCharacter(null);
    setName("");
    setGender(undefined);
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            🐭 Character Generator
          </h1>
          <p className="text-lg text-muted-foreground">
            Vygeneruj kompletní myší postavu se statistikami, inventářem a pozadím
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Column */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Možnosti</CardTitle>
                <CardDescription>
                  Volitelně zadej jméno a pohlaví, jinak se vygeneruje náhodně
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Jméno (volitelné)</Label>
                  <Input
                    id="name"
                    placeholder="např. Pepřík"
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
                  {character && (
                    <Button onClick={handleReset} variant="outline">
                      Reset
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Actions */}
            {character && (
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
            {character ? (
              <Card>
                <CardHeader>
                  <CardTitle className="text-2xl">{character.name}</CardTitle>
                  <CardDescription className="text-base">
                    ⭐ {character.background}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Stats */}
                  <div>
                    <h3 className="font-semibold mb-2">Vlastnosti</h3>
                    <div className="grid grid-cols-3 gap-4">
                      <div className="text-center p-3 bg-muted rounded">
                        <div className="text-xs text-muted-foreground">Síla</div>
                        <div className="text-2xl font-bold">{character.strength}</div>
                      </div>
                      <div className="text-center p-3 bg-muted rounded">
                        <div className="text-xs text-muted-foreground">Mrštnost</div>
                        <div className="text-2xl font-bold">{character.dexterity}</div>
                      </div>
                      <div className="text-center p-3 bg-muted rounded">
                        <div className="text-xs text-muted-foreground">Vůle</div>
                        <div className="text-2xl font-bold">{character.willpower}</div>
                      </div>
                    </div>
                  </div>

                  {/* HP */}
                  <div>
                    <h3 className="font-semibold mb-2">Zdraví</h3>
                    <div className="flex items-center gap-2">
                      <span className="text-sm">HP: {character.current_hp}/{character.max_hp}</span>
                      <div className="flex gap-1">
                        {Array.from({ length: character.max_hp }).map((_, i) => (
                          <span key={i} className="text-red-500">
                            {i < character.current_hp ? "❤️" : "🤍"}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Inventory */}
                  <div>
                    <h3 className="font-semibold mb-2">Inventář</h3>
                    <div className="grid grid-cols-2 gap-2">
                      {character.inventory.map((item, i) => (
                        <div
                          key={i}
                          className={`p-2 border rounded text-sm ${
                            item ? "bg-background" : "bg-muted/30"
                          }`}
                        >
                          {item || <span className="text-muted-foreground">Prázdné</span>}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Appearance & Details */}
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="font-semibold">Vzhled:</span> {character.appearance}
                    </div>
                    <div>
                      <span className="font-semibold">Rodné znamení:</span> {character.birthsign}
                    </div>
                    <div>
                      <span className="font-semibold">Barva srsti:</span> {character.coat}
                    </div>
                    {character.notes && (
                      <div>
                        <span className="font-semibold">Poznámky:</span> {character.notes}
                      </div>
                    )}
                  </div>

                  {/* Experience */}
                  <div className="text-sm text-muted-foreground">
                    Level {character.level} • {character.experience} XP
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="h-full flex items-center justify-center min-h-[400px]">
                <CardContent className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">🐭</div>
                  <p>Klikni na "Generovat" pro vytvoření postavy</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
