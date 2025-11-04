"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface Generator {
  id: string;
  name: string;
  emoji: string;
  description: string;
  category: 'mvp' | 'extended';
  path: string;
  implemented: boolean;
}

const generators: Generator[] = [
  // MVP Generators (5)
  {
    id: 'character',
    name: 'Character Generator',
    emoji: '🐭',
    description: 'Vygeneruj kompletní myší postavu se statistikami, inventářem a pozadím',
    category: 'mvp',
    path: '/generators/character',
    implemented: true,
  },
  {
    id: 'npc',
    name: 'NPC Generator',
    emoji: '👥',
    description: 'Rychlé vytvoření NPC s osobností, motivacemi a vztahy',
    category: 'mvp',
    path: '/generators/npc',
    implemented: true,
  },
  {
    id: 'weather',
    name: 'Weather Generator',
    emoji: '🌦️',
    description: 'Počasí a sezónní události pro všechna čtyři roční období',
    category: 'mvp',
    path: '/generators/weather',
    implemented: true,
  },
  {
    id: 'hex',
    name: 'Hex Generator',
    emoji: '🗺️',
    description: 'Generování hexů pro hexcrawl kampaně s detaily a háčky',
    category: 'mvp',
    path: '/generators/hex',
    implemented: true,
  },
  {
    id: 'settlement',
    name: 'Settlement Generator',
    emoji: '🏘️',
    description: 'Myší osady s velikostí, vládou, řemesly a hospodami',
    category: 'mvp',
    path: '/generators/settlement',
    implemented: true,
  },

  // Extended Generators (12)
  {
    id: 'hireling',
    name: 'Hireling Generator',
    emoji: '⚔️',
    description: 'Pronajímatelní pomocníci se statistikami a specializacemi',
    category: 'extended',
    path: '/generators/hireling',
    implemented: true,
  },
  {
    id: 'reaction',
    name: 'Reaction Roll',
    emoji: '🎲',
    description: 'Určení reakce tvora při setkání (2k6 mechanika)',
    category: 'extended',
    path: '/generators/reaction',
    implemented: true,
  },
  {
    id: 'spell',
    name: 'Spell Generator',
    emoji: '✨',
    description: 'Náhodná kouzla z tabulky (2k8 na 16 kouzel)',
    category: 'extended',
    path: '/generators/spell',
    implemented: true,
  },
  {
    id: 'treasure',
    name: 'Treasure Generator',
    emoji: '💰',
    description: 'Poklady s ďobky, kouzelné meče, kouzla a předměty',
    category: 'extended',
    path: '/generators/treasure',
    implemented: true,
  },
  {
    id: 'adventure',
    name: 'Adventure Seeds',
    emoji: '📖',
    description: 'Semínka dobrodružství (Tvor + Problém + Komplikace)',
    category: 'extended',
    path: '/generators/adventure',
    implemented: true,
  },
  {
    id: 'hook',
    name: 'Adventure Hooks',
    emoji: '🎣',
    description: 'Motivace pro začátek dobrodružství (k6 háčků)',
    category: 'extended',
    path: '/generators/hook',
    implemented: true,
  },
  {
    id: 'creature',
    name: 'Creature Variants',
    emoji: '🐉',
    description: 'Varianty stvoření (11 typů: ghost, snake, cat, atd.)',
    category: 'extended',
    path: '/generators/creature',
    implemented: true,
  },
  {
    id: 'tavern',
    name: 'Tavern Generator',
    emoji: '🏠',
    description: 'Názvy a speciality hospod pro osady',
    category: 'extended',
    path: '/generators/tavern',
    implemented: true,
  },
  {
    id: 'dungeon',
    name: 'Dungeon Generator',
    emoji: '🏛️',
    description: 'Dobrodružná místa s místnostmi, obyvateli a tajemstvími',
    category: 'extended',
    path: '/generators/dungeon',
    implemented: true,
  },
  {
    id: 'rumor',
    name: 'Rumor Generator',
    emoji: '📰',
    description: 'Zvěsti s pravdivostním systémem (k6 tabulka)',
    category: 'extended',
    path: '/generators/rumor',
    implemented: true,
  },
  {
    id: 'hexcrawl',
    name: 'Hexcrawl Generator',
    emoji: '🗺️',
    description: 'Kompletní hexcrawl kampaň (25 hexů + osady + dungeony)',
    category: 'extended',
    path: '/generators/hexcrawl',
    implemented: true,
  },
];

export default function GeneratorsPage() {
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState<'all' | 'mvp' | 'extended'>('all');

  const filteredGenerators = generators.filter((gen) => {
    const matchesSearch = gen.name.toLowerCase().includes(search.toLowerCase()) ||
      gen.description.toLowerCase().includes(search.toLowerCase());
    const matchesFilter = filter === 'all' || gen.category === filter;
    return matchesSearch && matchesFilter;
  });

  const mvpCount = generators.filter(g => g.category === 'mvp').length;
  const extendedCount = generators.filter(g => g.category === 'extended').length;

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">🎲 Generátory</h1>
          <p className="text-lg text-muted-foreground">
            Všech 17 nástrojů pro generování postav, NPC, hexů, dungeonů a dalších
          </p>
        </div>

        {/* Filters & Search */}
        <div className="mb-8 flex gap-4 flex-wrap">
          <Input
            type="text"
            placeholder="Hledat generátor..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="max-w-sm"
          />
          <div className="flex gap-2">
            <Button
              variant={filter === 'all' ? 'default' : 'outline'}
              onClick={() => setFilter('all')}
            >
              Všechny ({generators.length})
            </Button>
            <Button
              variant={filter === 'mvp' ? 'default' : 'outline'}
              onClick={() => setFilter('mvp')}
            >
              MVP ({mvpCount})
            </Button>
            <Button
              variant={filter === 'extended' ? 'default' : 'outline'}
              onClick={() => setFilter('extended')}
            >
              Extended ({extendedCount})
            </Button>
          </div>
        </div>

        {/* Generator Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredGenerators.map((generator) => (
            <Link key={generator.id} href={generator.path}>
              <Card className="h-full hover:border-primary transition-colors cursor-pointer">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="text-4xl mb-2">{generator.emoji}</div>
                    {!generator.implemented && (
                      <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                        Coming Soon
                      </span>
                    )}
                  </div>
                  <CardTitle className="text-xl">{generator.name}</CardTitle>
                  <CardDescription className="text-sm">
                    {generator.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <span className="capitalize">{generator.category}</span>
                    {generator.implemented ? (
                      <span className="text-green-600">✓ Available</span>
                    ) : (
                      <span className="text-gray-400">⏳ Pending</span>
                    )}
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>

        {/* No Results */}
        {filteredGenerators.length === 0 && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Žádné generátory nenalezeny</p>
          </div>
        )}
      </div>
    </main>
  );
}
