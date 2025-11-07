"use client";

import { HexcrawlHex } from "@/lib/api";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface HexDetailProps {
  hex: HexcrawlHex;
  hexNumber: number;
  onClose?: () => void;
}

export default function HexDetail({
  hex,
  hexNumber,
  onClose,
}: HexDetailProps) {
  return (
    <Card className="w-full h-fit sticky top-4">
      <CardHeader className="flex flex-row items-center justify-between pb-3">
        <CardTitle className="text-xl">Hex #{hexNumber}</CardTitle>
        {onClose && (
          <button
            onClick={onClose}
            className="text-3xl leading-none text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
            aria-label="Zavřít"
          >
            ×
          </button>
        )}
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Type & Category Grid */}
        <div className="grid grid-cols-2 gap-3">
          <div className="p-3 bg-muted rounded-md">
            <div className="text-xs text-muted-foreground font-medium mb-1">
              TYP TERÉNU
            </div>
            <div className="font-semibold text-sm">{hex.type}</div>
          </div>
          <div className="p-3 bg-muted rounded-md">
            <div className="text-xs text-muted-foreground font-medium mb-1">
              KATEGORIE
            </div>
            <div className="font-semibold text-sm">{hex.detail_category}</div>
          </div>
        </div>

        {/* Detail Name */}
        <div className="p-4 bg-primary/10 rounded-md border border-primary/20">
          <div className="text-xs text-muted-foreground font-medium mb-2">
            📍 DETAIL
          </div>
          <div className="font-semibold text-base">{hex.detail_name}</div>
        </div>

        {/* Hook */}
        <div className="p-4 bg-secondary/50 rounded-md border border-secondary">
          <div className="text-xs text-muted-foreground font-medium mb-2">
            🎣 HÁČEK
          </div>
          <div className="italic text-sm leading-relaxed">
            "{hex.detail_hook}"
          </div>
        </div>

        {/* Settlement info (if exists) */}
        {hex.settlement && (
          <div className="p-4 bg-green-500/10 rounded-md border border-green-500/30">
            <div className="text-xs text-muted-foreground font-medium mb-3 flex items-center gap-2">
              🏘️ OSADA
            </div>
            <div className="space-y-2">
              <div className="font-bold text-base">{hex.settlement.name}</div>
              <div className="text-sm">
                <span className="font-medium">Velikost:</span>{" "}
                {hex.settlement.size_name || `Level ${hex.settlement.size}`}
              </div>
              <div className="text-sm">
                <span className="font-medium">Populace:</span>{" "}
                {hex.settlement.population}
              </div>
              {hex.settlement.government && (
                <div className="text-sm">
                  <span className="font-medium">Vláda:</span>{" "}
                  {hex.settlement.government}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Description */}
        {hex.description && (
          <div className="p-4 bg-muted/50 rounded-md">
            <div className="text-xs text-muted-foreground font-medium mb-2">
              📖 POPIS
            </div>
            <div className="text-sm leading-relaxed">{hex.description}</div>
          </div>
        )}

        {/* Quick Stats */}
        <div className="pt-2 border-t border-border">
          <div className="grid grid-cols-2 gap-2 text-xs text-muted-foreground">
            <div>
              <span className="font-medium">Type roll:</span> {hex.type_roll}
            </div>
            {hex.detail_subtype && (
              <div>
                <span className="font-medium">Subtype:</span>{" "}
                {hex.detail_subtype}
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
