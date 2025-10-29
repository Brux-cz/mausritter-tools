# Session Notes - Udržení Kontextu

Tento adresář slouží k ukládání poznámek z jednotlivých konverzací s AI. Když dojde kontext nebo skončí session, je důležité zachytit:

## Co ukládat do session notes:

1. **Načtené soubory a dokumentace** - seznam všech souborů, které byly načteny do kontextu
2. **Řešené problémy** - co jsme právě řešili
3. **Rozpracované úkoly** - co je nedokončené a je třeba na to navázat
4. **Důležitá rozhodnutí** - jaké designové a strukturální rozhodnutí byla učiněna
5. **Kontext projektu** - aktuální stav projektu a co bylo změněno

## Formát session notes:

Každý session note má formát: `session_XXX_YYYY-MM-DD.md`

## Template:

```markdown
# Session XXX - YYYY-MM-DD

## Shrnutí
Krátký popis co jsme dělali v této session.

## Načtené soubory
- path/to/file1.md
- path/to/file2.py

## Provedené změny
- [ ] Co bylo dokončeno
- [x] Co je hotové

## Rozpracované úkoly
- Co je třeba dodělat
- Na co navázat v příští session

## Důležitá rozhodnutí
- Jaká rozhodnutí byla učiněna

## Poznámky pro příští session
Co je důležité načíst do kontextu příště.
```

## Použití:

Na konci každé session:
1. Vytvoř nový session note s aktuálním datem
2. Vyplň všechny sekce
3. Na začátku nové session si načti poslední session note
