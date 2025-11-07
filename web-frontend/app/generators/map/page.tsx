"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import EmptyHexMap from "@/components/generators/EmptyHexMap";
import { toast } from "sonner";

export default function MapGeneratorPage() {
  const [showNumbers, setShowNumbers] = useState(true);
  const mapRef = useRef<HTMLDivElement>(null);

  const handlePrint = () => {
    window.print();
    toast.success("Otevřeno v režimu tisku");
  };

  const handleExportPNG = async () => {
    try {
      // This will be implemented in Phase 2
      toast.info("Export PNG bude přidán v další verzi");
    } catch (error) {
      toast.error("Chyba při exportu PNG");
    }
  };

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 print:hidden">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            🗺️ Generátor prázdné mapy
          </h1>
          <p className="text-lg text-muted-foreground">
            Klasický 19-hexový pattern pro Mausritter - připravený k tisku
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Control Panel */}
          <div className="lg:col-span-1 print:hidden">
            <Card>
              <CardHeader>
                <CardTitle>Nastavení</CardTitle>
                <CardDescription>
                  Přizpůsob si mapu podle potřeby
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Show numbers toggle */}
                <div className="flex items-center justify-between">
                  <Label htmlFor="show-numbers" className="cursor-pointer">
                    Zobrazit čísla hexů
                  </Label>
                  <Switch
                    id="show-numbers"
                    checked={showNumbers}
                    onCheckedChange={setShowNumbers}
                  />
                </div>

                {/* Divider */}
                <div className="border-t pt-6">
                  <h3 className="font-semibold mb-3">Export</h3>
                  <div className="space-y-2">
                    <Button
                      onClick={handlePrint}
                      variant="outline"
                      className="w-full"
                    >
                      🖨️ Vytisknout
                    </Button>
                    <Button
                      onClick={handleExportPNG}
                      variant="outline"
                      className="w-full"
                      disabled
                    >
                      📷 Uložit jako PNG
                    </Button>
                  </div>
                </div>

                {/* Info */}
                <div className="border-t pt-6">
                  <h3 className="font-semibold mb-2">ℹ️ O mapě</h3>
                  <div className="text-sm text-muted-foreground space-y-2">
                    <p>
                      <strong>Pattern:</strong> 19 hexů (klasický hexagon)
                    </p>
                    <p>
                      <strong>Formát:</strong> Pointy-top hexagony
                    </p>
                    <p>
                      <strong>Použití:</strong> Prázdná mapa k vyplnění vlastními poznámkami
                    </p>
                  </div>
                </div>

                {/* Tips */}
                <div className="border-t pt-6">
                  <h3 className="font-semibold mb-2">💡 Tipy</h3>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Vytiskni mapu na A4 papír</li>
                    <li>• Vyplň hexy poznámkami dle pravidel</li>
                    <li>• Použij jako šablonu pro kampaň</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Map Display */}
          <div className="lg:col-span-3" ref={mapRef}>
            <Card className="print:border-0 print:shadow-none">
              <CardHeader className="print:hidden">
                <CardTitle>Mapa hexcrawlu</CardTitle>
                <CardDescription>
                  19-hexový pattern připravený k použití
                </CardDescription>
              </CardHeader>
              <CardContent>
                <EmptyHexMap showNumbers={showNumbers} />
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Print-only title */}
        <div className="hidden print:block text-center mb-4">
          <h1 className="text-2xl font-bold">Mausritter Hexcrawl Map</h1>
          <p className="text-sm text-gray-600">19-hex pattern</p>
        </div>
      </div>

      {/* Print styles */}
      <style jsx global>{`
        @media print {
          body {
            background: white;
          }
          @page {
            size: A4 portrait;
            margin: 1cm;
          }
        }
      `}</style>
    </main>
  );
}
