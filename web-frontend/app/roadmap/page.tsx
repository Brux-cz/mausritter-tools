"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface Feature {
  id: string;
  emoji: string;
  name: string;
  simple: string;
  example: string;
  benefits: string[];
}

const phase2Features: Feature[] = [
  {
    id: "auth",
    emoji: "🔐",
    name: "Účty a přihlášení",
    simple: "Vytvoř si svůj vlastní účet! Přihlas se emailem a heslem, a všechny tvé vygenerované postavy, kampaně a poznámky zůstanou uložené navždy. Žádné ztracené papírky s poznámkami!",
    example: "Je pátek večer. Vygeneruješ si Pepříka Chrabrého (HP 5/6, Síla 9, s pochodní a sirkou v kapse). V pondělí se vrátíš na web - a Pepřík tu stále čeká, připravený na další dobrodružství! Všechno uložené, nic se neztratilo.",
    benefits: [
      "Neztrácíš vygenerované postavy",
      "Můžeš se přihlásit odkudkoliv (z mobilu, z počítače kamaráda)",
      "Tvoje kampaně budou tvoje - nikdo jiný je neuvidí"
    ]
  },
  {
    id: "campaigns",
    emoji: "🎭",
    name: "Správa kampaní",
    simple: "Jsi Game Master? Vytvoř si kampaň pro své hráče! Dej jí jméno (např. \"Stíny nad Ječmenovým Údolím\"), pozvi kamarády, a všechny vygenerované NPC, osady, hexy a dungeony uvidíš pohromadě na jednom místě.",
    example: "Máš kampaň s 4 hráči. Během přípravy vygeneruješ: 12 NPCček (od rybáře Josefa po záhadnou čarodějnici), 3 osady (Ječmenov, Farma u Potoka, Skryté doupě), 25 hexů s detaily, a 2 dungeony. Všechno se ti ukládá do kampaně na přehledný dashboard! Žádné hledání v poznámkách. Klikneš na \"Kampaň\" → vidíš vše.",
    benefits: [
      "Všechno na jednom místě",
      "Nemusíš nic opisovat do sešitu",
      "Hráči vidí své postavy online",
      "Můžeš kampaň sdílet s kamarády"
    ]
  },
  {
    id: "persistence",
    emoji: "💾",
    name: "Ukládání postav",
    simple: "Vygeneroval sis postavu? Klikneš \"Uložit\" → postava je tvoje navždy! Neztratíš ji, nezapomeneš na ni. Je uložená v databázi a čeká na tebe, až se vrátíš.",
    example: "Pepřík Chrabrý přežil 5 session. Má 3 HP, meč +1, 120 pence, a Condition \"Injured\". Všechno je uložené online. Příští session jen otevřeš web → Pepřík je tam, přesně jak jsi ho nechal!",
    benefits: [
      "Postavy přežijí restart počítače",
      "Můžeš mít 10+ postav najednou",
      "Historie všech postav (živé i mrtvé 💀)",
      "Backup - kdyby ti sešit spadl do potoka!"
    ]
  },
  {
    id: "hexmap",
    emoji: "🗺️",
    name: "Interaktivní Hexcrawl Mapa",
    simple: "Pamatuješ, jak sis vygeneroval 25 hexů? Teď je uvidíš jako 5×5 mapu! Každý hex je políčko - klikneš na něj a vidíš detail (co tam je, jaký hook, jestli je osada). Plus: Můžeš označovat hexy jako \"objevené\" - hráči vidí jen ty, kam už došli. Neodhalené hexy jsou šedé s \"???\".",
    example: "Tvoji hráči začínají v hexu (3,3) - vesnice Ječmenov. Postupně objevují sousední hexy. Ty jako GM klikneš na hex, označíš ho jako \"objevený\" → hráči ho teď vidí na své mapě! Hex (2,3): Les s hnízdem ptáka - objevený ✅. Hex (4,3): ??? - neobjevený ❓",
    benefits: [
      "Vidíš mapu vizuálně, ne jen jako text",
      "Hráči objevují svět postupně (jako ve hře!)",
      "Každý hex má detail na kliknutí",
      "Žádné kreslení map na papír"
    ]
  },
  {
    id: "players",
    emoji: "👥",
    name: "Player Management",
    simple: "Pozvi kamarády do kampaně! Zadáš jejich email/username → oni dostanou pozvánku → kliknou \"Přijmout\" → jsou součástí kampaně! Vidí společnou mapu, své postavy, a můžou komunikovat.",
    example: "Kampaň \"Stíny nad Ječmenovým Údolím\" má 4 hráče: Pepa (hraje Pepříka), Jana (hraje Kláru), Martin (hraje Josefa), a Lucka (hraje Marii). Všichni vidí stejnou hexcrawl mapu, ale každý vidí jen svou postavu. GM vidí všechny postavy najednou!",
    benefits: [
      "Hráči se můžou připojit odkudkoliv",
      "Každý vidí jen to, co má vidět",
      "Žádné sdílení hesla k účtu",
      "Můžeš přidat/odebrat hráče kdykoliv"
    ]
  },
  {
    id: "editing",
    emoji: "✏️",
    name: "Editovatelné Character Sheety",
    simple: "Pepřík dostal zásah od kočky? Klikni na jeho HP a sniž ho z 5 na 3. Našel novou pochodni? Přetáhni ji do inventáře (drag & drop). Utratil pence za sýr? Uprav číslo. Všechno se ukládá online - tvoje postava se mění během hry!",
    example: "Session v sobotu večer: Pepřík bere 2 damage → HP 5 → 3 ✅. Našel meč +1 → přidáš do inventáře ✅. Utratil 50 pence za sýr → 100p → 50p ✅. Získal Condition \"Injured\" → přidáš badge ✅. Vše online, hned viditelné! Příště jen otevřeš web a pokračuješ.",
    benefits: [
      "Nemusíš gumou mazat HP na papíře",
      "Inventory drag & drop (jako v počítačové hře!)",
      "Všichni hráči vidí své sheety online",
      "GM vidí všechny postavy najednou"
    ]
  }
];

const phase3Features: Feature[] = [
  {
    id: "dice",
    emoji: "🎲",
    name: "Real-time Dice Roller",
    simple: "Hodíš si k20 na webu → VŠICHNI v kampani to vidí live! Je to jako Discord, ale pro kostky. Vidíš, kdo hodil, jaké číslo padlo, a proč (např. \"Pepřík - STR test\").",
    example: "Hráč: \"Házím na STR, abych vyšplhal na strom\" → Klikne na k20 → padne 14 → Všichni vidí: \"🐭 Pepřík hodil 14 (STR test) - Úspěch!\" GM: \"Kočka hází útok\" → Klikne na k6 → padne 6 → Všichni vidí: \"🐱 Kočka hodila 6 (Attack) - Critical!\"",
    benefits: [
      "Všichni vidí všechny hody (transparentní)",
      "Historie hodů (můžeš se vrátit)",
      "Atmosphere! Vidíš hody live během session",
      "Žádné \"já jsem hodil 20, věř mi!\""
    ]
  },
  {
    id: "sessions",
    emoji: "📝",
    name: "Session Tracking",
    simple: "Před každou session vytvoříš záznam - datum, kteří hráči jsou, co se stalo. Píšeš si poznámky během hry (kdo co řekl, co objevili). Na konci session = automatický souhrn!",
    example: "Session #5 - 5. listopadu 2025. Hráči: Pepřík, Klárka, Josef, Marie. Poznámky během hry: \"Objevili osadu U Mlýna\", \"NPC Rybář jim dal quest\", \"Boj s kočkou - Pepřík -2 HP\", \"Našli poklad: 50p + meč\". → Konec session → automatický souhrn ✅ → XP rozděleno, poznámky uloženy ✅",
    benefits: [
      "Pamatuješ si, co se stalo minule",
      "Hráči můžou číst recap",
      "Historie celé kampaně",
      "Automatický souhrn (nemusíš psát esej)"
    ]
  },
  {
    id: "pdf",
    emoji: "📄",
    name: "PDF Export",
    simple: "Klikneš \"Export PDF\" → stáhneš si krásně naformátovaný character sheet / hexcrawl mapu / session souhrn jako PDF. Můžeš si ho vytisknout, poslat kamarádovi, nebo uložit.",
    example: "Chceš vytisknout Pepříkův character sheet na papír? → Klikneš \"Export PDF\" → Stáhne se peprik_character_sheet.pdf → Vytiskneš → máš fyzickou kopii! Nebo: Chceš poslat hráčům souhrn session? → Export session summary → session_5_souhrn.pdf → Pošleš přes Discord ✅",
    benefits: [
      "Fyzické kopie (pro hru bez počítače)",
      "Zálohování (kdyby web spadl)",
      "Krásně naformátované (vypadá to profesionálně)",
      "Sdílení s kamarády"
    ]
  },
  {
    id: "files",
    emoji: "🖼️",
    name: "File Uploads",
    simple: "Nahraj obrázek své postavy! Nebo banner pro kampaň. Nebo fotku tvého fyzického character sheetu. Všechno se uloží online a vidí to ostatní hráči.",
    example: "Pepřík má avatara - nakreslila ho Lucka. Nahraješ ho → všichni vidí Pepříkův obrázek v kampani! Nebo: Kampaň \"Stíny nad Ječmenovým Údolím\" má cool banner s lesem → nastavíš ho jako cover image → každý, kdo otevře kampaň, vidí ten banner!",
    benefits: [
      "Personalizace postav (každá má avatara)",
      "Kampaně vypadají cool (s bannery)",
      "Můžeš uploadovat fotky mapek z papíru",
      "Sdílená galerie (hráči vidí tvé obrázky)"
    ]
  }
];

function FeatureCollapsible({ feature }: { feature: Feature }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border-2 border-border rounded-lg mb-3 overflow-hidden hover:border-primary/50 transition-colors">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-4 flex items-center justify-between bg-card hover:bg-accent transition-colors text-left"
      >
        <div className="flex items-center gap-3">
          <span className="text-3xl">{feature.emoji}</span>
          <span className="font-semibold text-lg">{feature.name}</span>
        </div>
        <span className="text-2xl text-muted-foreground">{isOpen ? "▲" : "▼"}</span>
      </button>

      {isOpen && (
        <div className="p-6 bg-card/50 space-y-4 border-t-2 border-border">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xl">🐭</span>
              <h4 className="font-semibold text-foreground">Jednoduše řečeno:</h4>
            </div>
            <p className="text-muted-foreground leading-relaxed">{feature.simple}</p>
          </div>

          <div className="bg-primary/5 border-l-4 border-primary p-4 rounded">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xl">💡</span>
              <h4 className="font-semibold text-foreground">Představ si:</h4>
            </div>
            <p className="text-muted-foreground leading-relaxed italic">{feature.example}</p>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xl">✨</span>
              <h4 className="font-semibold text-foreground">Proč je to super:</h4>
            </div>
            <ul className="space-y-2">
              {feature.benefits.map((benefit, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">•</span>
                  <span className="text-muted-foreground">{benefit}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default function RoadmapPage() {
  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-foreground mb-4">
            🗺️ Co připravujeme
          </h1>
          <p className="text-xl text-muted-foreground mb-6">
            Náš plán na budoucnost Mausritter Tools
          </p>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Všech 16 generátorů už máš! 🎉 Teď chystáme vylepšení, díky kterým
            si budeš moci ukládat postavy, spravovat kampaně s kamarády, a hrát
            online jako profesionál. Tady je náš plán (psaný srozumitelně, bez tech žargonu)!
          </p>
        </div>

        {/* Phase 2 */}
        <Card className="mb-8 border-2 border-primary/30">
          <CardHeader>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-4xl">📅</span>
              <CardTitle className="text-3xl">Fáze 2 (V2)</CardTitle>
            </div>
            <CardDescription className="text-lg">
              Campaign Management - Ukládání, sdílení, a správa kampaní
            </CardDescription>
            <div className="flex gap-4 mt-4 text-sm">
              <div className="flex items-center gap-2">
                <span className="text-muted-foreground">⏱️ Časový odhad:</span>
                <span className="font-semibold">3-4 týdny</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-muted-foreground">🎯 Status:</span>
                <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs font-semibold">
                  ⏳ Plánováno
                </span>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-2">
            {phase2Features.map((feature) => (
              <FeatureCollapsible key={feature.id} feature={feature} />
            ))}
          </CardContent>
        </Card>

        {/* Timeline connector */}
        <div className="flex justify-center my-6">
          <div className="h-12 w-1 bg-border"></div>
        </div>

        {/* Phase 3 */}
        <Card className="mb-8 border-2 border-border">
          <CardHeader>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-4xl">📅</span>
              <CardTitle className="text-3xl">Fáze 3 (V3)</CardTitle>
            </div>
            <CardDescription className="text-lg">
              Advanced Features - Real-time funkce, session tracking, a export
            </CardDescription>
            <div className="flex gap-4 mt-4 text-sm">
              <div className="flex items-center gap-2">
                <span className="text-muted-foreground">⏱️ Časový odhad:</span>
                <span className="font-semibold">4 týdny</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-muted-foreground">🎯 Status:</span>
                <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs font-semibold">
                  📅 Budoucnost
                </span>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-2">
            {phase3Features.map((feature) => (
              <FeatureCollapsible key={feature.id} feature={feature} />
            ))}
          </CardContent>
        </Card>

        {/* Footer CTA */}
        <div className="text-center mt-12 p-8 bg-card/50 border-2 border-dashed border-primary/30 rounded-lg">
          <p className="text-lg text-muted-foreground mb-4">
            Těšíš se na některou z těchto funkcí? My taky! 🐭
          </p>
          <p className="text-sm text-muted-foreground mb-6">
            Zatím si užij všech 16 generátorů a generuj postavy, NPC, dungeony a hexy do sytosti!
          </p>
          <Link href="/generators">
            <Button size="lg" className="text-lg px-8">
              Zpět na Generátory →
            </Button>
          </Link>
        </div>
      </div>
    </main>
  );
}
