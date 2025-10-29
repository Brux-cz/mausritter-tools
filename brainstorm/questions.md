# Otázky k Řešení

## Architektura

### Jak strukturovat datové modely?
- Pydantic models?
- Dataclasses?
- Plain dicts?
- SQLite databáze?

### Jak ukládat pravidla a tabulky?
- JSON?
- YAML?
- Python moduly?
- Databáze?

### CLI nebo GUI?
- První verze CLI (jednodušší)
- Později web app?
- Desktop GUI?

---

## Data a Pravidla

### Jak nejlépe strukturovat dokumentaci pro AI?
- Jeden velký soubor vs. mnoho malých?
- Jaké značky/tagy použít pro snadné vyhledávání?
- Jak linkovat související pravidla?

### Jak řešit české znaky?
- UTF-8 všude
- Konzistence v názvech

---

## Generátory

### Jak zajistit konzistenci generování?
- Seedy pro reprodukovatelnost?
- Váhování pravděpodobností?

### Jak řešit závislosti mezi generovanými daty?
- Např. povolání určuje výbavu
- Pozadí ovlivňuje vlastnosti?

---

## Export/Import

### Jaké formáty podporovat?
- JSON (určitě)
- YAML
- Markdown
- PDF (těžší)
- Kartičky pro tisk?

---

## Testování

### Jak testovat náhodné generátory?
- Property-based testing?
- Snapshot testing?
- Manuální review?

---

## Řešené otázky
<!-- Sem přesuň otázky, které už byly vyřešeny, včetně odpovědí -->
