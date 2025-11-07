# Oprava Hex Layout Geometrie

**Datum:** 2025-11-07
**Branch:** `feature/hex-map-generator`
**Commit:** `a60885f`

## 📋 Problém

19-hexový pattern se zobrazoval špatně:
- ❌ Hexy se **překrývaly**
- ❌ Geometrie neodpovídala správnému plástev patternu
- ❌ Číslování bylo správné, ale pozice špatné

### Vizuální příklad problému:
```
Před opravou: Hexy se překrývaly, nerovnoměrné mezery
Po opravě: Pravidelný hexagon, hexy se dotýkají hranami
```

---

## 🔍 Root Cause Analysis

### 1. HEX_RADIUS byl 2× příliš velký
```typescript
// ❌ ŠPATNĚ
const HEX_RADIUS = 60; // px

// ✅ SPRÁVNĚ
const HEX_RADIUS = 30; // px
```

**Vysvětlení:**
- Pro pointy-top hexy s `RADIUS=30` je šířka hexa `√3 × 30 ≈ 51.96px`
- Horizontální vzdálenost mezi centry sousedních hexů je také `51.96px`
- Výsledek: hexy se **dotýkají hranami** (ideální!)
- S `RADIUS=60` byly hexy široké ~104px → překrývání

---

### 2. Axiální koordináty byly špatné

**Problém v get19HexLayout():**
```typescript
// ❌ ŠPATNĚ - tyto souřadnice nejsou sousedé centra!
{ q: -1, r: -1, label: 3 }, // NW - není přímý soused!
{ q: 1, r: 1, label: 6 },   // SE - není přímý soused!
```

**Pro pointy-top hexagony**, přímí sousedé `(0,0)` jsou:
```typescript
{ q: -1, r: 0 },  // W (západ)
{ q: 0, r: -1 },  // NW (severozápad)
{ q: 1, r: -1 },  // NE (severovýchod)
{ q: 1, r: 0 },   // E (východ)
{ q: 0, r: 1 },   // SW (jihozápad)
{ q: -1, r: 1 },  // SE (jihovýchod)
```

---

## ✅ Řešení

### 1. Oprava HEX_RADIUS
```typescript
// web-frontend/lib/hexMath.ts:7
const HEX_RADIUS = 30; // px (distance from center to corner)
```

### 2. Oprava hexagonPoints()
```typescript
// web-frontend/lib/hexMath.ts:89
const angle = (Math.PI / 3) * i - Math.PI / 6; // Posun pro Pointy-Top
```

### 3. Oprava axiálních souřadnic v get19HexLayout()
```typescript
export function get19HexLayout(): HexLayout[] {
  const axialCoords = [
    // Střed (1 hex)
    { q: 0, r: 0, label: 1 },

    // Vnitřní prstenec (6 hexů) - přímí sousedé centra
    { q: -1, r: 0, label: 2 },
    { q: 0, r: -1, label: 3 },
    { q: 1, r: -1, label: 4 },
    { q: 1, r: 0, label: 5 },
    { q: 0, r: 1, label: 6 },
    { q: -1, r: 1, label: 7 },

    // Vnější prstenec (12 hexů) - vzdálenost 2 od centra
    { q: -2, r: 0, label: 8 },
    { q: -1, r: -1, label: 9 },
    { q: 0, r: -2, label: 10 },
    { q: 1, r: -2, label: 11 },
    { q: 2, r: -2, label: 12 },
    { q: 2, r: -1, label: 13 },
    { q: 2, r: 0, label: 14 },
    { q: 1, r: 1, label: 15 },
    { q: 0, r: 2, label: 16 },
    { q: -1, r: 2, label: 17 },
    { q: -2, r: 2, label: 18 },
    { q: -2, r: 1, label: 19 },
  ];

  return axialCoords.map(({ q, r, label }) => {
    const { x, y } = axialToScreen(q, r);
    return { col: q, row: r, x, y, label };
  });
}
```

---

## 📊 Výsledek

✅ **Hexy se dotýkají hranami** (žádné překryvy ani mezery)
✅ **Pravidelný hexagon pattern** (tvar plástve)
✅ **Správné číslování**: 1 střed + 6 vnitřní + 12 vnější
✅ **Připraveno k tisku** na `/generators/map`

### Finální mapa:
```
     10  11  12
   9   3   4  13
 8   2   1   5  14
  19  7   6  15
    18 17 16
```

---

## 🤖 Technické detaily

### Axiální souřadnicový systém
- Používáme **axial coordinates** (q, r) pro pointy-top hexagony
- Konverze na pixel souřadnice: `axialToScreen(q, r)`
- Vzorce:
  ```typescript
  x = HEX_RADIUS * (√3 * q + (√3/2) * r)
  y = HEX_RADIUS * (3/2 * r)
  ```

### Reference
- [Red Blob Games - Hexagonal Grids](https://www.redblobgames.com/grids/hexagons/)
- Gemini AI asistence při ladění axiálních souřadnic

---

## 📝 Testování

**URL pro testování:**
- Prázdná mapa: http://localhost:3001/generators/map
- Test mapa: http://localhost:3001/test-hex

**Ověření:**
1. Hexy se dotýkají hranami ✅
2. Číslování 1-19 odpovídá patternu ✅
3. Žádné překryvy ani mezery ✅
4. Tisk funguje správně ✅

---

## 💾 Backup

**Pokud se v budoucnu něco rozbije, vrať se k tomuto commitu:**
```bash
git checkout a60885f -- web-frontend/lib/hexMath.ts
```

**Nebo vytáhni celou branch:**
```bash
git checkout feature/hex-map-generator
```
