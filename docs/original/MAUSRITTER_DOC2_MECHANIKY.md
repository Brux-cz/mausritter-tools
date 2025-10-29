# ⚙️ MAUSRITTER - DOKUMENT 2: HERNÍ MECHANIKY

**Účel:** Referenční příručka všech herních mechanik a pravidel
**Pro:** Validaci generátorů, rychlé řešení situací ve hře
**Vazby:** → DOKUMENT 1 (DATABASE) pro všechny tabulky

---

# 🎲 SEKCE A: ZÁKLADNÍ MECHANIKY

## MEC-ZAC-01: Záchrany - základy
**Účel:** Určit výsledek riskantních akcí
**Kdy použít:** Když hráč dělá něco riskantního s nejistým výsledkem
**Kostka:** k20

### Jak funguje:
1. Průvodce určí, která vlastnost se testuje (síla/mrštnost/vůle)
2. Hráč hodí k20
3. Pokud hodí **≤ hodnota vlastnosti** → **ÚSPĚCH** (bez následků)
4. Pokud hodí **> hodnota vlastnosti** → **NEÚSPĚCH** (následky)

### Typy záchrán:
- **Síla:** Fyzická síla a odolnost (tažení, zvedání, odolání jedu)
- **Mrštnost:** Rychlost a obratnost (vyhnutí se, rovnováha, tiché plížení)
- **Vůle:** Síla odhodlání a osobnost (odolání strachu, vyjednávání, kouzlení)

### Kdy NEZKOUŠET záchranu:
- Akce je rozumná a bezpečná → automatický úspěch
- Akce je zjevně nemožná → automatický neúspěch
- Není jasný následek neúspěchu → není potřeba hodit

**Vazby:** → MEC-ZAC-02 (výhoda/nevýhoda), MEC-ZAC-03 (následky)

---

## MEC-ZAC-02: Výhoda a nevýhoda
**Účel:** Modifikace záchrany podle okolností
**Kdy použít:** Když je pozice výhodná/nevýhodná

### Výhoda:
- **Když:** Myš má výhodnou pozici, perfektní vybavení nebo přípravu
- **Jak:** Hoď 2k20, **použij NIŽŠÍ výsledek**
- **Příklad:** Útok ze zálohy, excelentní nástroj na práci

### Nevýhoda:
- **Když:** Myš má nevýhodnou pozici, špatné vybavení nebo podmínky
- **Jak:** Hoď 2k20, **použij VYŠŠÍ výsledek**
- **Příklad:** Zatížený inventář, tma, zranění

**Vazby:** → MEC-ZAC-01 (základní záchrany)

---

## MEC-ZAC-03: Následky neúspěchu
**Účel:** Určení, co se stane při neúspěšné záchraně
**Kdy použít:** Před hodem - hráč musí vědět, co riskuje

### Typy následků:
1. **Zranění:** k4 (drobné) až k20 (smrtící)
   - k4 = škrábnutí
   - k6 = nebezpečné
   - k8 = vážné pro 1. úroveň
   - k10+ = velmi nebezpečné
   - k20 = téměř jistá smrt

2. **Stavy:** → TAB-STA-01 (seznam stavů)
   - Nejčastější: Vyčerpání, Vystrašení

3. **Ztráta času:** Každá akce = 1 směna
   - Čas = hořící pochodně + náhodná setkání

4. **Ztráta předmětu:** Hoď k6 na políčko inventáře

5. **Použití předmětu:** Zaškrtni 1-3 tečky použití

**Pravidlo:** Následky musí být **předem zjevné a signalizované**

**Vazby:** → MEC-CAS-01 (čas), TAB-STA-01 (stavy)

---

## MEC-ZAC-04: Vzdorované záchrany
**Účel:** Řešení konfliktu mezi dvěma postavami
**Kdy použít:** Když se dvě postavy aktivně snaží porazit jedna druhou
**Příklad:** Přetahování, odzbrojování, sociální manipulace

### Jak funguje:
1. Obě strany hodí záchranu na příslušnou vlastnost
2. **Vyhrává TEN, kdo hodil NIŽŠÍ úspěšný hod**
3. Pokud jeden uspěje a druhý ne → uspěšný vyhrává
4. Pokud oba neuspějí → nikdo nevyhrává, ale oba nesou následky

**Příklad:**
- Myš (síla 10) tlačí krysu (síla 12) do jezírka
- Myš hodí: 8 (úspěch)
- Krysa hodí: 11 (úspěch)
- Myš vyhrává (8 < 11)

**Vazby:** → MEC-ZAC-01 (základní záchrany)

---

## MEC-HODY-01: Hody na štěstí
**Účel:** Řešení nepředvídatelných situací mimo kontrolu hráčů
**Kdy použít:** Když situace není záchranou (není to test dovednosti)
**Kostka:** k6

### Jak funguje:
1. Průvodce určí pravděpodobnost: "X ze 6"
   - 1 ze 6 = velmi nepravděpodobné
   - 2 ze 6 = nepravděpodobné
   - 3 ze 6 = 50:50
   - 4 ze 6 = pravděpodobné
   - 5 ze 6 = velmi pravděpodobné

2. Hoď k6
3. Pokud hodíš **≤ X** → stane se to
4. Pokud hodíš **> X** → nestane se to

**Příklady použití:**
- Objeví se náhodné setkání? (1 ze 6)
- Je v budově někdo doma? (3 ze 6)
- Drží most váhu myší skupiny? (4 ze 6)
- Všimne si stráž hlídkující myši? (2 ze 6)

**Vazby:** → Žádné (samostatná mechanika)

---

# ⚔️ SEKCE B: BOJOVÉ MECHANIKY

## MEC-BJ-01: Boj - základní postup
**Účel:** Řešení bojových situací
**Kdy použít:** Když dojde na fyzický konflikt

### Pořadí akcí:
1. **Překvapení?**
   - Pokud jedna strana překvapila druhou → hraje první
   - Pokud obě strany vědí o sobě → hoď záchranu na mrštnost
   - Určené pořadí platí **všechna kola boje**

2. **Kolo boje:**
   - Pohyb: až 30 cm
   - Akce: 1x (útok, kouzlo, riskantní činnost)

3. **Opakuj** dokud boj neskončí

**Vazby:** → MEC-BJ-02 (útoky), MEC-BJ-03 (zranění), MEC-BJ-04 (kritické zranění)

---

## MEC-BJ-02: Útoky a zranění
**Účel:** Určení zranění z útoku
**Kdy použít:** V boji, při útoku

### Základní útok:
1. **Útoky VŽDY zasahují** (nehází se na zásah)
2. Hoď kostkou zbraně → TAB-VYB-01 (zbraně)
3. Odečti zbroj protivníka
4. Výsledek = způsobené zranění

### Modifikace útoků:

**ZESÍLENÝ útok (hoď k12):**
- Útok ze zálohy/překvapení
- Využití slabiny protivníka
- Dobrý taktický plán

**ZESLABENÝ útok (hoď k4):**
- Střelba po zakrytém cíli
- Útok s nevhodnou zbraní
- Útok v nevýhodné pozici

**Bojování dvěma zbraněmi (lehké):**
- Hoď oběma kostkami
- Použij LEPŠÍ výsledek

**Obouruční zbraně (střední/těžké):**
- Jednou packou: nižší kostka (např. k6)
- Oběma packama: vyšší kostka (např. k8)

**Vazby:** → TAB-VYB-01 (zbraně), MEC-BJ-03 (aplikace zranění)

---

## MEC-BJ-03: Aplikace zranění a BO
**Účel:** Určení dopadu zranění na tvora
**Kdy použít:** Po každém útoku

### Postup:
1. **Nejdřív od BO:**
   - Zranění se odečítá od bodů ochrany (BO)
   - BO = schopnost vyhnout se nebo odolat zranění
   - Když BO klesne na 0 → jsou vyčerpané

2. **Pak od síly:**
   - Když jsou BO vyčerpané, zranění jde do síly
   - Kdykoliv síla klesne → **hoď záchranu na sílu**
   - ÚSPĚCH → můžeš pokračovat v boji
   - NEÚSPĚCH → **KRITICKÉ ZRANĚNÍ** → MEC-BJ-04

3. **Smrt:**
   - Síla klesne na 0 → tvor je mrtvý
   - Vyřazený (kritické zranění) a neošetřený 6 směn → mrtvý

**Vazby:** → MEC-BJ-04 (kritické zranění), TAB-STA-01 (stav Poranění)

---

## MEC-BJ-04: Kritické zranění
**Účel:** Vyřazení tvora z boje
**Kdy použít:** Když tvor neuspěje v záchraně na sílu po zranění síly

### Standardní kritické zranění:
1. Tvor dostane **stav Poranění** → TAB-STA-01
2. Tvor je **vyřazený** (nemůže jednat)
3. Pokud není ošetřen do **6 směn** → umírá

### Speciální kritické zranění:
Některé útoky mají vlastní kritické zranění (přepisuje standardní):
- **Příklad - Had:** Spolkne zaživa, každé kolo k4 zranění síly
- **Příklad - Pavouk:** Odnese v kokonu
- **Příklad - Duch:** Ovládne zasaženého tvora

**Vazby:** → TAB-BEST-XX (bestář se speciálními kritickými zraněními), TAB-STA-01 (Poranění)

---

## MEC-BJ-05: Ztráta vlastností
**Účel:** Určení efektu ztráty vlastností na nulu
**Kdy použít:** Když vlastnost klesne na 0

### Efekty:
- **Síla = 0:** Tvor je **mrtvý**
- **Mrštnost = 0:** Tvor se **nedokáže pohybovat** (paralyzovaný)
- **Vůle = 0:** Tvor propadl **nepříčetnosti** (nelze jednat rozumně)

**Poznámka:** Mrštnost a vůle na 0 = není smrt, ale tvor je neakceschopný

**Vazby:** → MEC-ODL-01 (léčení vlastností)

---

## MEC-BJ-06: Morálka
**Účel:** Určení, kdy protivník utíká nebo se vzdává
**Kdy použít:** Při specifických spouštěčích v boji
**Kostka:** Záchrana na vůli

### Spouštěče:
Protivník musí uspět v záchraně na vůli, jinak utíká/se vzdává:
1. Na začátku boje je viditelně v nevýhodě
2. Poprvé dostane kritické zranění
3. Uvidí, jak spojenec padl nebo dal se na útěk

### Modifikace:
- **Výhoda:** Fanatičtí, zoufalí nebo mimořádně placení
- **Nevýhoda:** Zbabělí, přeplacení nebo demoralizovaní

**Poznámka pro pomocníky:** → MEC-POM-02 (morálka pomocníků)

**Vazby:** → MEC-ZAC-01 (záchrany), MEC-POM-02 (pomocníci)

---

## MEC-BJ-07: Tečky použití po boji
**Účel:** Opotřebení zbraní, zbroje a munice
**Kdy použít:** Po KAŽDÉM boji

### Postup:
Za **každý předmět použitý v boji** (zbraň/zbroj/munice):
1. Hoď k6
2. Pokud padne **4, 5 nebo 6** → zaškrtni 1 tečku použití
3. Když jsou všechny 3 tečky zaškrtnuté → předmět je zničený/spotřebovaný

### Co škrtnout:
- **Zbraně:** Které jsi použil k útoku
- **Zbroj:** Která ti zachránila život (zablokovala zranění)
- **Munice:** Šípy/kameny, které jsi vystřelil

### Oprava:
- Cena: 10 % původní ceny za každou tečku
- Nutný zbrojíř nebo kovář

**Vazby:** → TAB-VYB-01 (ceny oprav)

---

## MEC-BJ-08: Boj v měřítku tlupy
**Účel:** Řešení bitev mezi armádami
**Kdy použít:** Když bojují tlupy (20+ myší) proti sobě nebo velkým zvířatům
**Vazby:** → MEC-TLU-01 (tvorba tlupy), TAB-BEST-03 (kočka - měřítko tlupy)

### Základní pravidla:
Funguje STEJNĚ jako normální boj, ale:

**Měřítko útoků:**
- Tlupa vs. jednotlivce → útoky tlupy jsou **zesílené** (k12)
- Jednotlivec vs. tlupu → zranění se **ignoruje** (kromě výjimečně ničivých)

**Ztráty a seskupení:**
- Tlupa dostane kritické zranění → **rozvrácená**, nemůže jednat
- Musí se **seskupit** (akce) než může znovu jednat
- Při síle 0 → tlupa je **pobitá**
- Při poloviční síle → záchrana na vůli nebo **panický útěk**

**Odpočinek:**
- Tlupy si obnovují BO i sílu stejně jako jednotlivci
- Krátký/dlouhý/úplný odpočinek → MEC-ODL-01

**Vazby:** → MEC-TLU-01 (vytvoření tlupy)

---

# 🔮 SEKCE C: MAGICKÉ MECHANIKY

## MEC-MAG-01: Sesílání kouzel
**Účel:** Použití kouzla
**Kdy použít:** Když myš sešle kouzlo
**Vazby:** → TAB-KOU-01 (seznam kouzel)

### Požadavky:
- Myš musí držet destičku s kouzlem v pacce
- Myš musí číst nahlas z destičky

### Postup:
1. **Rozhodni, kolik moci investuješ:**
   - Minimum: 1 bod moci
   - Maximum: Počet nevyškrtnutých teček použití kouzla (1-3)

2. **Hoď tolika k6, kolik máš moci:**
   - Za každou kostku, na které padne **4, 5 nebo 6** → zaškrtni 1 tečku

3. **Účinek kouzla:**
   - Závisí na **[POČTU]** kostek, kterými jsi házel
   - A na **[SOUČTU]** všech hodnot, které ti padly
   - Viz popis v TAB-KOU-01

4. **Kontrola vymknutí:** → MEC-MAG-02

**Příklad:**
- Kouzlo má 3 volné tečky → můžeš dát max. 3 moc
- Dáš 3 moc → hodíš 3k6 → padne ti 2, 5, 6
- Zaškrtneš 2 tečky (5 a 6)
- [POČET] = 3 (tři kostky)
- [SOUČET] = 13 (2+5+6)
- Pak se podíváš na účinek kouzla v TAB-KOU-01

**Vazby:** → MEC-MAG-02 (vymknutí), MEC-MAG-03 (dobíjení)

---

## MEC-MAG-02: Vymknutí kouzla
**Účel:** Riziko při sesílání kouzel
**Kdy použít:** Kdykoliv při sesílání padne šestka
**Vazby:** → TAB-STA-01 (Pomatení)

### Postup:
1. Za **každou hozenou šestku:**
   - Dostaneš **k6 zranění do vůle** (ne do síly!)
   
2. **Hoď záchranu na vůli:**
   - ÚSPĚCH → nic dalšího se neděje
   - NEÚSPĚCH → dostaneš **stav Pomatení** → TAB-STA-01

**Poznámka:** Můžeš dostat vícero zranění vůle za jedno sesílání (pokud padne víc šestek)

**Vazby:** → MEC-ZAC-01 (záchrany), TAB-STA-01 (Pomatení)

---

## MEC-MAG-03: Dobíjení kouzel
**Účel:** Obnovení vyčerpaných kouzel
**Kdy použít:** Když jsou všechny tečky zaškrtnuté (kouzlo vyčerpané)
**Vazby:** → TAB-KOU-01 (podmínky dobití u každého kouzla)

### Postup:
1. Najdi kouzlo v TAB-KOU-01
2. Přečti si podmínku dobití
3. Splň podmínku (obvykle rituál trvající několik dní)
4. Vygumuj VŠECHNY tečky použití

**Příklady podmínek:**
- Zahojení: Pořež se za k6 zranění a potřísni kouzlo krví
- Světlo: Po 3 dny vystavuj kouzlo rannímu i večernímu slunci
- Tma: Nech kouzlo 3 dny na tmavém místě

**Poznámka:** Vyčerpané kouzlo má poloviční prodejní hodnotu

**Vazby:** → TAB-KOU-01 (seznam kouzel)

---

## MEC-MAG-04: Stříbrné a kouzelné zbraně
**Účel:** Speciální zbraně proti určitým tvorům
**Kdy použít:** Při boji s duchy, přízraky a magickými tvory
**Vazby:** → TAB-VYB-01 (cena postříbření), TAB-POK-02 (kouzelné meče)

### Pravidlo:
Některé bytosti lze zranit **POUZE:**
- Stříbrnými zbraněmi
- Kouzelnými zbraněmi
- Kouzly

**Příklady tvorů:**
- Duchové → TAB-BEST-01
- Přízrační pavouci → TAB-BEST-06a

### Postříbření zbraně:
- Cena: **10x** původní cena zbraně
- Po každém boji: zaškrtni tečku použití (stříbro se opotřebuje)
- Oprava: 10 % postříbřené ceny za tečku

**Vazby:** → TAB-BEST-01 (duchové), TAB-BEST-06a (přízrační pavouk)

---

# 🕐 SEKCE D: ČAS A CESTOVÁNÍ

## MEC-CAS-01: Časová měřítka
**Účel:** Strukturování času ve hře
**Kdy použít:** Vždy - pro sledování efektů

### Tři měřítka:

**1. KOLO (combat rounds):**
- Délka: **necelá minuta**
- Použití: V boji
- Akce: Pohyb (30 cm) + 1 akce

**2. SMĚNA (turns):**
- Délka: **10 minut**
- Použití: Při průzkumu dobrodružných míst
- Akce: Průzkum 1 místnosti NEBO 1 delší akce
- **Každé 3 směny:** hoď na náhodné setkání (k6, na 1 = setkání)
- **Každých 6 směn:** zaškrtni tečku u světla (pochodeň/lucerna/lampa)

**3. HLÍDKA (watches):**
- Délka: **6 hodin** (36 směn)
- Použití: Při cestování divočinou
- Akce: Ujedeš 1 hex/míli (2 hexy v náročném terénu)
- 1 den = **4 hlídky**

**Vazby:** → MEC-CES-01 (cestování), MEC-CAS-02 (náhodná setkání)

---

## MEC-CAS-02: Náhodná setkání
**Účel:** Generování dynamických událostí
**Kdy použít:** Podle časového měřítka
**Kostka:** k6
**Vazby:** → Specifické tabulky setkání pro oblast

### Pravidla házení:

**V dobrodružném místě (směny):**
- Každé **3 směny** → hoď k6
- **NEBO** kdykoliv myši způsobí **randál/hluk**
- Na **1** → setkání (hoď na tabulku setkání místa)
- Na **2** → předzvěst (stopy, zvuky, náznak)

**V divočině (hlídky):**
- Na začátku **ranní hlídky** → hoď k6
- Na začátku **večerní hlídky** → hoď k6
- Na **1** → setkání (hoď na tabulku setkání regionu)
- Na **2** → předzvěst
- Pokud setkání → hoď k12 na hodinu (kdy během hlídky)

**Vazby:** → Specifické tabulky setkání v DATABASE

---

## MEC-CES-01: Cestování krajinou
**Účel:** Pohyb po mapě
**Kdy použít:** Při cestování mezi lokacemi
**Vazby:** → MEC-CAS-01 (čas), TAB-ROC-XX (počasí)

### Základní pravidlo:
**1 hex = 1 hlídka (6 hodin)**

### Náročný terén (2x pomalejší):
- Potoky a řeky
- Lidské silnice (velké vzdálenosti)
- Skály a útesy
- Kopce
**= 2 hlídky na hex**

### Denní program:
1 den = 4 hlídky:
- **Ranní hlídka:** Cestování
- **Polední hlídka:** Cestování
- **Odpolední hlídka:** Cestování
- **Noční hlídka:** Odpočinek (povinný)

**Bez odpočinku:** Stav Vyčerpání → TAB-STA-01

**Vazby:** → MEC-ODL-01 (odpočinek), TAB-STA-01 (Vyčerpání)

---

## MEC-CES-02: Hledání potravy
**Účel:** Získání zásob v divočině
**Kdy použít:** Když myši nemají zásoby
**Čas:** 1 hlídka
**Výsledek:** k3 použití zásob

### Postup:
1. Myš stráví **1 hlídku** hledáním potravy
2. Najde **k3 použití zásob**
3. Nepostoupí v cestování (nemůže ve stejné hlídce cestovat)

**Poznámka:** V nehostinném terénu může Průvodce snížit na k2 nebo vyžadovat záchranu

**Vazby:** → TAB-VYB-01 (zásoby)

---

## MEC-CES-03: Navigace a ztracení se
**Účel:** Určení, jestli se myši nezabloudily
**Kdy použít:** V neznámém terénu bez průvodce
**Kostka:** k6 (hod na štěstí)

### Pravidlo:
**Bez místního průvodce nebo mapy:**
- Hoď k6 každý den cestování v neznámé oblasti
- Šance **1 ze 6** → zabloudily (skončí v nesprávném hexu)

**S místním průvodcem nebo mapou:**
- Nezabloudíš (automatický úspěch)

**Vazby:** → TAB-POM-01 (místní průvodce), MEC-HODY-01 (štěstí)

---

## MEC-CES-04: Počasí a roční období
**Účel:** Generování počasí a jeho efektů
**Kdy použít:** Každý den cestování
**Kostka:** 2k6
**Vazby:** → TAB-ROC-01 až 04 (roční období)

### Postup:
1. Určit aktuální roční období
2. Hoď 2k6 na tabulce počasí pro dané období
3. Pokud je počasí **tučně** = nepříznivé

### Nepříznivé počasí:
Za každou **hlídku strávenou cestováním** v nepříznivém počasí:
- Hoď **záchranu na sílu**
- NEÚSPĚCH → stav **Vyčerpání** → TAB-STA-01

**Příklady nepříznivého počasí:**
- **Jaro:** Přívalové deště
- **Léto:** Úmorné vedro
- **Podzim:** Silný vítr, Slejvák
- **Zima:** Vánice, Mrznoucí déšť, Třeskutá zima

**Vazby:** → TAB-ROC-01 až 04 (počasí), TAB-STA-01 (Vyčerpání)

---

# 🛡️ SEKCE E: ODPOČINEK A LÉČENÍ

## MEC-ODL-01: Typy odpočinku
**Účel:** Obnovení BO a vlastností
**Kdy použít:** Když myš odpočívá v bezpečí
**Vazby:** → TAB-STA-01 (odstranění stavů)

### 1. KRÁTKÝ ODPOČINEK
**Trvání:** 1 směna (10 minut)
**Požadavky:** Doušek vody, bezpečné místo
**Efekt:**
- Obnoví **k6+1 BO**
- NEOBNOVUJE vlastnosti
- NEODSTRAŇUJE stavy

---

### 2. DLOUHÝ ODPOČINEK
**Trvání:** 1 hlídka (6 hodin)
**Požadavky:** Vydatné jídlo (zásoby) + spánek
**Efekt:**
- Obnoví **všechny BO**
- **NEBO** (pokud už máš plné BO): obnoví **k6 bodů** jedné poškozené vlastnosti
- Odstraní některé stavy (ty s podmínkou "po dlouhém odpočinku")

**Poznámka:** Zásoby se škrtají při dlouhém odpočinku

---

### 3. ÚPLNÝ ODPOČINEK
**Trvání:** 1 týden
**Požadavky:** Bezpečné místo (osada), strava + ubytování
**Cena:** ~20 ď za týden (strava + bydlení)
**Efekt:**
- Obnoví **všechny BO**
- Obnoví **všechny vlastnosti** na maximum
- Odstraní **většinu dlouhodobých stavů**

**Vazby:** → TAB-VYB-01 (ceny ubytování)

---

## MEC-ODL-02: Hlad
**Účel:** Penalizace za nedostatek jídla
**Kdy použít:** Když myš nejí celý den
**Vazby:** → TAB-STA-01 (Hlad)

### Pravidlo:
Pokud se myš **nenají po celý den** (4 hlídky):
- Dostane **stav Hlad** → TAB-STA-01

**Odstranění:**
- Sní jídlo (zásoby) a odpočívá si 1 směnu

**Vazby:** → TAB-STA-01 (Hlad), TAB-VYB-01 (ceny jídla)

---

## MEC-ODL-03: Léčení kritického zranění
**Účel:** Vrácení vyřazené myši do hry
**Kdy použít:** Po kritickém zranění
**Vazby:** → MEC-BJ-04 (kritické zranění), TAB-STA-01 (Poranění)

### Postup:
1. **Ošetření:**
   - Jiný tvor musí vyřazenou myš ošetřit (akce)
   - Nevyžaduje žádný speciální nástroj (jen péče)

2. **Krátký odpočinek:**
   - Ošetřená myš musí provést krátký odpočinek (1 směna)
   - Po odpočinku: obnoví k6+1 BO

3. **Stav Poranění:**
   - Stav **Poranění zůstává**
   - Odstraní se až po úplném odpočinku (týden)

**Smrt:**
Pokud vyřazenou myš nikdo neošetří do **6 směn** → umírá

**Vazby:** → MEC-ODL-01 (odpočinek), TAB-STA-01 (Poranění)

---

# 📦 SEKCE F: INVENTÁŘ A STAVY

## MEC-INV-01: Struktura inventáře
**Účel:** Organizace předmětů
**Kdy použít:** Vždy
**Vazby:** → Deník postavy (vizuální)

### Políčka inventáře:

**1. Silnější packa (1 políčko):**
- Zbraň nebo nástroj v dominantní ruce
- Volná akce k prohození s tělem

**2. Slabší packa (1 políčko):**
- Štít, pochodeň nebo druhá zbraň
- Volná akce k prohození s tělem

**3. Tělo (2 políčka):**
- Nošené na těle (plášť, zbroj, toulec)
- Volná akce k prohození s packama

**4. Batoh (6 políček):**
- Uloženo v batohu
- **AKCE** k vytažení v krizové situaci (místo útoku v boji)

**Celkem:** 10 políček inventáře

**Vazby:** → MEC-INV-02 (zatížení)

---

## MEC-INV-02: Zatížení
**Účel:** Penalizace za příliš mnoho předmětů
**Kdy použít:** Když myš nese víc než 10 políček
**Vazby:** → TAB-STA-01 (stavy mohou zabírat políčka)

### Pravidlo:
Když myš nese **víc předmětů nebo stavů než má políček:**
- Je **zatížená**
- **Nemůže běhat**
- **Všechny záchrany s nevýhodou**

### Speciální předměty:

**Ďobky:**
- Prvních **250 ď** = nezabírá políčka (kapsy)
- Každých dalších načatých **250 ď** = 1 políčko

**Stavy:**
- Každý stav **musí** být umístěn do políčka inventáře
- Zabírají místo stejně jako předměty

**Vazby:** → MEC-ZAC-02 (nevýhoda), TAB-STA-01 (stavy)

---

## MEC-INV-03: Použití předmětů
**Účel:** Sledování opotřebení
**Kdy použít:** Při použití předmětů
**Vazby:** → TAB-VYB-01 (ceny oprav)

### Tečky použití (3 tečky):
Většina předmětů má **3 tečky použití** (☐☐☐)

**Kdy škrtnout:**

1. **Zbraně/zbroje/munice:**
   - Po boji hoď k6 za každý použitý předmět
   - Na **4-6** → zaškrtni tečku
   - → MEC-BJ-07

2. **Pochodně/lucerny/lampy:**
   - Po **6 směnách** → zaškrtni tečku
   - Elektrická lampa má **6 teček** (místo 3)

3. **Zásoby:**
   - Po **každém jídle** → zaškrtni tečku

4. **Jiné vybavení:**
   - Když použití může předmět vyčerpat/poškodit
   - Průvodce rozhodne

**Všechny tečky zaškrtnuté** = předmět je **zničený/spotřebovaný**

**Oprava:**
- Cena: **10 % původní ceny** za každou tečku
- Nutný zbrojíř/kovář (u zbraní/zbroje)

**Vazby:** → TAB-VYB-01 (ceny)

---

## MEC-STA-01: Systém stavů
**Účel:** Sledování negativních efektů
**Kdy použít:** Když myš utrpí stav
**Vazby:** → TAB-STA-01 (seznam stavů v DATABASE)

### Jak fungují stavy:

1. **Zabírají políčko inventáře:**
   - Každý stav = 1 políčko
   - Myš může mít vícero kopií stejného stavu
   - Přispívají k zatížení → MEC-INV-02

2. **Mají dodatečné efekty:**
   - Vyčerpání: Nevýhoda při síle/mrštnosti
   - Hlad: Musíš sníst
   - Poranění: Nevýhoda při síle/mrštnosti
   - atd.

3. **Odstranění podle podmínky:**
   - Každý stav má podmínku odstranění
   - Např.: "Po dlouhém odpočinku", "Po jídle"

### Hlavní stavy:

| Stav | Efekt | Odstranění |
|------|-------|------------|
| Vyčerpání | Nevýhoda při síle/mrštnosti | Po dlouhém odpočinku |
| Vystrašení | ? (specifikováno v situaci) | Podle zdroje strachu |
| Hlad | Musíš jíst | Po jídle |
| Poranění | Nevýhoda při síle/mrštnosti | Po úplném odpočinku |
| Pomatení | ? (magické zmatení) | Specifická pro zdroj |

**Vazby:** → TAB-STA-01 (úplný seznam), MEC-INV-02 (zatížení)

---

# 📈 SEKCE G: ZLEPŠOVÁNÍ

## MEC-ZLE-01: Získávání zkušeností (zk.)
**Účel:** Systém postupu postav
**Kdy použít:** Po úspěšném dobrodružství

### Způsoby získání zk.:

**1. Přinesení pokladu do bezpečí:**
- Hodnota v ďobcích se **rozdělí rovným dílem** mezi všechny členy skupiny
- Za každý **1 ďobek** = **1 zk.**

**Příklad:**
- Skupina 3 myší najde poklad v hodnotě 600 ď
- 600 ď ÷ 3 = 200 ď na myš
- Každá myš dostane **200 zk.**

**2. Nezištné utrácení na prospěch společenství:**
- Myš utratí ďobky na vylepšení prospívající celé komunitě
- (Ne na sebe - na veřejné stavby, dary osadě, atd.)
- Za každých **10 ďobků** = **1 zk.**

**Poznámka:** Ďobky utracené na pomoc komunitě dávají **méně zk.** než ďobky z pokladů

**Vazby:** → MEC-ZLE-02 (postup na úrovně)

---

## MEC-ZLE-02: Postup na úrovně
**Účel:** Zvyšování síly postavy
**Kdy použít:** Když myš nasbírá dost zk.
**Vazby:** → Tabulka úrovní níže

### Tabulka úrovní:

| Úroveň | Kostky ochrany | Kuráž | Zkušenostní body |
|--------|----------------|-------|------------------|
| 1 | 1k6 | 0 | 0 |
| 2 | 2k6 | 1 | 1 000 |
| 3 | 3k6 | 2 | 3 000 |
| 4 | 4k6 | 2 | 6 000 |
| 5+ | 4k6 | 3 | +5 000 za úroveň |

---

### Postup při zvýšení úrovně:

**1. Hoď na zvýšení vlastností:**
Za **každou vlastnost** (síla, mrštnost, vůle):
- Hoď k20
- Pokud hodíš **VÍCE než aktuální hodnota** → zvyš vlastnost o **+1**
- Pokud hodíš stejně nebo méně → vlastnost zůstává

**2. Hoď kostkami ochrany:**
- Hoď kostkami podle tvojí nové úrovně
- Pokud hodíš **VÍCE než aktuální BO** → přepiš BO na nový hod
- Pokud hodíš stejně nebo méně → zvyš BO o **+1**

**3. Získej kuráž:**
- Od 2. úrovně získáš **kuráž** → MEC-ZLE-03

**Vazby:** → MEC-ZLE-03 (kuráž)

---

## MEC-ZLE-03: Kuráž
**Účel:** Ignorování stavů
**Kdy použít:** Od 2. úrovně
**Vazby:** → MEC-STA-01 (stavy)

### Jak funguje kuráž:

**Úrovně 1:** 0 kurážZe
**Úrovně 2-3:** 1-2 kuráže
**Úrovně 4+:** 2-3 kuráže

### Použití:
Za každý **bod kuráže** můžeš:
- Umístit **1 stav** do prostoru "Kuráž" na deníku postavy
- Stav tam **stále je** (pořád zabírá políčko)
- ALE jeho **negativní efekt** se **NEAPLIKUJE**

**Odstranění:**
- Stav v Kuráži se odstraní **pouze splněním podmínky odstranění**
- Nemůžeš ho jen vyndat a vrátit do normálního inventáře

**Příklad:**
- Máš 2 kuráže a dostaneš stav Vyčerpání
- Dáš ho do Kuráže → nemáš nevýhodu na sílu/mrštnost
- Ale stále zabírá políčko
- Musíš si odpočinout (dlouhý odpočinek), abys ho odstranil

**Vazby:** → Tabulka úrovní v MEC-ZLE-02

---

# 👥 SEKCE H: POMOCNÍCI A TLUPY

## MEC-POM-01: Verbování pomocníků
**Účel:** Najímání NPC
**Kdy použít:** V myší osadě
**Čas:** 1 den
**Vazby:** → TAB-POM-01 (typy a ceny), TAB-OSA-01 (velikost osady)

### Postup:
1. **Stráv 1 den** sháněním pomocníků v osadě
2. **Zvol typ** pomocníka (světlonoš, zbrojmyš, učenec...)
3. **Uspěj v záchraně na vůli NEBO zaplať 20 ď**
4. Pokud uspěješ/zaplatíš → **hoď** na počet dostupných:
   - Viz sloupec "Počet" v TAB-POM-01

**Dostupnost podle velikosti osady:**
- Menší osady = méně typů pomocníků
- Větší města = všechny typy

**Typický pomocník:**
- k6 BO
- Vlastnosti: 2k6 (síla), 2k6 (mrštnost), 2k6 (vůle)
- 6 políček inventáře (2 packy, 2 tělo, 2 batoh)

**Vazby:** → TAB-POM-01 (typy), MEC-POM-02 (morálka)

---

## MEC-POM-02: Morálka pomocníků
**Účel:** Určení, kdy pomocník uteče/se vzbouří
**Kdy použít:** Ve stresujících situacích
**Kostka:** Záchrana na vůli
**Vazby:** → MEC-BJ-06 (bojová morálka)

### Spouštěče testu morálky:
Pomocník musí uspět v záchraně na vůli, jinak **uteče/vzbouří se**:

1. **Stresující situace:**
   - Vidí něco děsivého
   - Je v přímém nebezpečí
   - Skupina je v bezvýchodné situaci

2. **Špatné zacházení:**
   - Nedostává mzdu
   - Nedostává stravu
   - Skupina ho využívá

3. **Mimo dohodnuté služby:**
   - Po pomocníkovi chceš něco nebezpečnějšího, než bylo domluveno

### Modifikace:

**Výhoda:**
- Mimořádně dobře placený
- Věrný (osobní pouto k hráčské myši)

**Nevýhoda:**
- Špatně placený nebo hladový
- Hrubě zneužívaný

**Vazby:** → TAB-POM-01 (denní mzdy), MEC-ZAC-01 (záchrany)

---

## MEC-POM-03: Zlepšování pomocníků
**Účel:** Postup pomocníků na úrovně
**Kdy použít:** Když pomocník dostane zk.
**Vazby:** → MEC-ZLE-01 (získávání zk.)

### Pravidla:
Pomocníci se zlepšují **STEJNĚ** jako hráčské postavy:

**Získávání zk.:**
- Když dostane **podíl na pokladu** (nad rámec denní mzdy)
- Za každý **1 ďobek** nad rámec mzdy = **1 zk.**

**Postup:**
- Stejná tabulka jako u hráčských myší → MEC-ZLE-02
- 1000 zk. = 2. úroveň
- 3000 zk. = 3. úroveň
- atd.

**Poznámka pro tlupy:**
- Tlupy dostávají **1 zk. za každých 10 ďobků** nad rámec týdenní mzdy

**Vazby:** → MEC-ZLE-02 (postup), MEC-TLU-02 (zlepšování tlup)

---

## MEC-TLU-01: Tvorba tlupy
**Účel:** Vytvoření vojenské jednotky
**Kdy použít:** Když chceš vytvořit tlupu pod svým velením
**Čas:** 1 týden
**Vazby:** → MEC-BJ-08 (boj v měřítku tlupy)

### Požadavky:
- **20+ bojeschopných myší**
- **+ 1 následovník** (nosič, kuchař, zbrojíř) za každého bojovníka
- **= Celkem 40+ myší**

### Postup:
1. Stráv **1 týden** verbováním v městě
2. **Uspěj v záchraně na vůli NEBO zaplať 1000 ď**
3. Vytvoř tlupu

### Statistiky nové tlupy:
- **BO:** k6
- **Síla:** 10
- **Mrštnost:** 10
- **Vůle:** 10
- **Zranění:** k6 (klacky a sekery)

### Údržba:
- **1000 ď za týden** (mzdy + údržba)
- Nezaplacení → **riziko vzpoury**

**Vazby:** → MEC-BJ-08 (bojové pravidla), MEC-TLU-02 (vybavení)

---

## MEC-TLU-02: Vybavení tlupy
**Účel:** Vylepšení schopností tlupy
**Kdy použít:** Při vybavování tlupy
**Vazby:** → TAB-VYB-01 (ceny vybavení)

### Pravidlo:
Vybavení funguje **STEJNĚ** jako u jednotlivců, ale:

**Cena vybavení:**
- **20x** nákupní cena (pro 20 bojovníků)
- Např.: Střední zbraně (20 ď) x 20 = **400 ď**

**Příklady:**
- Lehká zbroj pro tlupu: 150 ď x 20 = **3000 ď**
- Těžké zbraně: 40 ď x 20 = **800 ď**

**Efekt:**
- Tlupa s těžkými zbraněmi → zranění k10 (místo k6)
- Tlupa s lehkou zbrojí → zbroj 1

**Vazby:** → TAB-VYB-01 (základní ceny)

---

# 🏰 SEKCE I: FRAKCE A BUDOVY

## MEC-FRAK-01: Systém frakcí
**Účel:** Simulace živého světa s mocenskými silami
**Kdy použít:** Mezi sezeními, pro vývoj světa
**Vazby:** → TAB-FRAK-01 až 02 (příklady frakcí)

### Struktura frakce:

**1. ZDROJE:**
- Mocnosti, které frakce ovládá
- Každý zdroj = +1 k hodu na plnění cílů
- Příklady: Hrůzostrašnost, Armáda, Bohatství, Magie

**2. CÍLE:**
- Co frakce chce dosáhnout
- Každý cíl má **2-5 políček pokroku** (☐☐☐)
- Po dokončení cíle → frakce získá nový zdroj

### Plnění cílů (mezi sezeními):

**Hoď k6 za každou frakci:**

1. **+1 za každý relevantní zdroj** frakce
2. **-1 za každý relevantní zdroj** konkurenční frakce (pokud jde cíl proti ní)

**Výsledek:**
- **4-5:** Zaškrtni **1 políčko pokroku** ☐
- **6+:** Zaškrtni **2 políčka pokroku** ☐☐

**Po dokončení cíle:**
- Přidej frakci **nový zdroj**
- Konkurenční frakci **odeber nebo změň zdroj**
- Aktualizuj mapu světa

### Zásahy hráčů:
- Hráči pomůžou cíli → zaškrtni **1-3 políčka** (podle dopadu)
- Hráči zbrzdí cíl → vymaž **1-3 políčka**
- Hráči ničí zdroj frakce → odeber/změň zdroj

**Vazby:** → TAB-FRAK-01 až 02 (hotové frakce)

---

## MEC-BUD-01: Stavba budov
**Účel:** Vlastnictví a výstavba sídel
**Kdy použít:** Když myši chtějí stavět
**Vazby:** → Tabulka cen níže

### Pozemková práva:
- **NELZE koupit** (jen získat darem nebo silou)
- Musíš právo **bránit**

### Kopání:
- **3 kopáči** vykopou za den: **krychle 15x15x15 cm v hlíně**
- **Jiné materiály:** 2x déle (kámen, kořeny, atd.)

### Ceny za 15cm krychli:

| Typ místnosti | Cena (materiál + zařízení) |
|---------------|---------------------------|
| Chodba (15 cm) | 10 ď |
| Prostá místnost | 100 ď |
| Běžná místnost | 500 ď |
| Honosná místnost | 2000 ď |

**Poznámky:**
- Cena = **JENOM materiál** (kopáče a dělníky platíš zvlášť)
- Kopáč: 5 ď/den → TAB-POM-01
- Dělník: 2 ď/den → TAB-POM-01

### Údržba:
**1 % celkové ceny měsíčně**

**Příklad:**
- Místnost 15x15x15 cm (běžná) = 500 ď
- Údržba = 5 ď/měsíc

**Vazby:** → TAB-POM-01 (ceny kopáčů/dělníků)

---

# 📋 SEKCE J: PRAVIDLA PRO PRŮVODCE

## MEC-PRU-01: Kdy házet na záchranu
**Účel:** Rozhodování, kdy vyžadovat hod
**Kdy použít:** Vždy, když hráč popisuje akci

### Rozhodovací strom:

**Je akce bezpečná a rozumná?**
→ ANO: **Automatický úspěch** (nehází se)
→ NE: Pokračuj ↓

**Je akce zjevně nemožná?**
→ ANO: **Automatický neúspěch** (nehází se)
→ NE: Pokračuj ↓

**Má neúspěch jasné následky?**
→ NE: **Automatický úspěch** (nebo to přeformuluj)
→ ANO: **HOĎ ZÁCHRANU**

### Pravidlo zlaté:
**Záchrany říkej JEN v reakci na akce hráčů**

**Špatně:** "Hoď si záchranu, jestli se nevyděsíš"
**Dobře:** "Rozběhneš se po úzkém trámu? Hoď mrštnost, při neúspěchu spadneš"

**Vazby:** → MEC-ZAC-01 (záchrany), MEC-ZAC-03 (následky)

---

## MEC-PRU-02: Signalizování nebezpečí
**Účel:** Férové varování před smrtí
**Kdy použít:** Vždy před velké nebezpečím

### Pravidlo:
**Hráči musí dostat JASNÉ varování před smrtelným nebezpečím**

**Špatně:**
- "Tlačíš na kliku. Past tě zabije."

**Dobře:**
- "Vidíš, že za dveřmi je napnutý drát. Pokud zmáčkneš kliku, něco se spustí."
- Hráči: "Ještě předtím přetnu drát"
- "OK, jak se ohýbáš k drátu, slyšíš cinkání mechanismu..."

### Pasti:
- **Zjevné a smrtící**
- Dávej hráčům příležitost řešit je chytře
- Pokud jdou na to hlava nehlava → nech je nést následky

**Vazby:** → TAB-DOB-12 (příklady pastí)

---

## MEC-PRU-03: Hraní nehráčských postav
**Účel:** Pravidla pro reakce NPC a tvorů
**Kdy použít:** Při setkání s NPC
**Vazby:** → TAB-REAK-01 (tabulka reakcí)

### Když není jasné, jak NPC zareaguje:

**1. Hoď na reakci (2k6):** → TAB-REAK-01
- 2 = Agresivní
- 3-5 = Nepřátelská
- 6-8 = Nejistá
- 9-11 = Povídavá
- 12 = Nápomocná

**2. Doplň otázkou:**
- Agresivní: "Jak ho myši rozzlobily?"
- Nepřátelská: "Jak se dá uchlácholit?"
- Nejistá: "Jak si ho můžou naklonit?"
- atd.

### Pravidlo:
**NPC mají vlastní motivace a cíle**
- Nejsou příběhoví roboti
- Reagují logicky podle své povahy
- Používej TAB-NPC-01 až 05 pro generování

**Vazby:** → TAB-REAK-01 (reakce), TAB-NPC-01 až 05 (generátor NPC)

---

## MEC-PRU-04: Náhodné vs. připravené obsah
**Účel:** Kdy improvizovat, kdy připravovat
**Kdy použít:** Při přípravě hry

### Připrav předem:
- **Mapu oblasti** (hexy, osady, důležité body)
- **Frakce** (cíle, zdroje, vztahy)
- **1-2 hlavní dobrodružná místa** (detailně)
- **Tabulky setkání** pro oblast

### Improvizuj během hry:
- **Detaily NPC** (použij generátory z DATABASE)
- **Obsah hexů** (hoď na tabulky během hry)
- **Reakce a dialogy** (použij tabulku reakcí)

### Zlaté pravidlo:
**Připravuj SITUACE, ne DĚJ**
- Nediktuj hráčům, co mají dělat
- Vytvoř místa a NPC s motivacemi
- Nech hráče, ať sami vyberou, co prozkoumají

**Vazby:** → Všechny tabulky v DATABASE (pro improvizaci)

---

**KONEC DOKUMENTU 2 - MECHANIKY**

---

**✅ DOKUMENT 2: MECHANIKY - DOKONČENO!**

**Shrnutí obsahu:**
- ✅ Sekce A: Základní mechaniky (záchrany, štěstí)
- ✅ Sekce B: Bojové mechaniky (útoky, zranění, morálka)
- ✅ Sekce C: Magické mechaniky (sesílání, vymknutí, dobíjení)
- ✅ Sekce D: Čas a cestování (směny, hlídky, navigace)
- ✅ Sekce E: Odpočinek a léčení (typy odpočinku, hlad)
- ✅ Sekce F: Inventář a stavy (zatížení, použití, stavy)
- ✅ Sekce G: Zlepšování (zk., úrovně, kuráž)
- ✅ Sekce H: Pomocníci a tlupy (verbování, morálka, boj)
- ✅ Sekce I: Frakce a budovy (systém frakcí, stavba)
- ✅ Sekce J: Pravidla pro Průvodce (kdy házet, signalizace)

**Celkem mechanik: 40+**
**Systém ID: MEC-XX-XX**
**Cross-reference: Funguje**

---

**CO DĚLAT DÁLE:**
→ Stáhni si DOKUMENT 2
→ Zkontroluj mechaniky
→ Pak udělám DOKUMENT 3: ŠABLONY (prázdné formuláře pro generátory)
