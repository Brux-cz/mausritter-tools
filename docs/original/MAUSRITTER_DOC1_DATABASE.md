# 📊 MAUSRITTER - DOKUMENT 1: DATABASE TABULEK

**Účel:** Referenční databáze všech tabulek, seznamů a hodnot z Mausritter
**Pro:** Generátory postav, NPC, světa, dobrodružství
**Formát:** Každá tabulka má ID, popis použití a cross-reference

---

# 🐭 SEKCE A: TVORBA POSTAV

## TAB-POV-01: Tabulka původů
**Účel:** Určení původu postavy podle BO a ďobků
**Použití:** Po hodu na BO (k6) a ďobky (k6)
**Kostka:** Lookup (porovnání hodnot)
**Vazby:** → TAB-VYB-01 (zbraně), TAB-KOU-01 (kouzla), TAB-POM-01 (pomocníci)

| BO | Ďobky | Původ | Předmět A | Předmět B |
|----|-------|-------|-----------|-----------|
| 1 | 1 | Pokusná myš | Kouzlo: Kouzelná střela [TAB-KOU-01 #4] | Olověný plášť (těžká zbroj) |
| 1 | 2 | Kuchyňský slídil | Štít a kabátec (lehká zbroj) | Hrnce |
| 1 | 3 | Uprchlík z klece | Kouzlo: Srozumitelnost [TAB-KOU-01 #8] | Láhev mléka |
| 1 | 4 | Čarodějnice | Kouzlo: Zahojení [TAB-KOU-01 #3] | Vonná tyčka |
| 1 | 5 | Kožešník | Štít a kabátec (lehká zbroj) | Silné nůžky |
| 1 | 6 | Pouliční rváč | Dýka (lehká, k6) | Láhev kávy |
| 2 | 1 | Žebravý kněz | Kouzlo: Zotavení [TAB-KOU-01 #7] | Svatý symbol |
| 2 | 2 | Honák brouků | Pomocník: věrný brouk [TAB-POM-01] | Tyč, 15 cm |
| 2 | 3 | Sládek | Pomocník: opilý světlonoš [TAB-POM-01] | Soudek piva |
| 2 | 4 | Rybář | Síť | Jehla (lehká, k6) |
| 2 | 5 | Kovář | Kladivo (střední, k6/k8) | Pilník na železo |
| 2 | 6 | Dráteník | Drát, klubko | Elektrická lampa |
| 3 | 1 | Dřevorubec | Sekera (střední, k6/k8) | Motouz, klubko |
| 3 | 2 | Člen netopýřího kultu | Kouzlo: Tma [TAB-KOU-01 #6] | Pytlík netopýřích zubů |
| 3 | 3 | Horník v cínovém dole | Krumpáč (střední, k6/k8) | Lucerna |
| 3 | 4 | Sběrač odpadků | Hák na odpadky (těžká, k10) | Zrcátko |
| 3 | 5 | Stěnolezec | Rybářský háček | Nit, cívka |
| 3 | 6 | Kupec | Pomocník: tažná krysa [TAB-POM-01] | Směnka od šlechtice na 20 ď |
| 4 | 1 | Vorař | Kladivo (střední, k6/k8) | Dřevěné klíny |
| 4 | 2 | Honák žížal | Tyč, 15 cm | Mýdlo |
| 4 | 3 | Vlaštovkář | Rybářský háček | Ochranné brýle |
| 4 | 4 | Kanálník | Pilník na železo | Nit, cívka |
| 4 | 5 | Žalářník | Řetěz, 15 cm | Kopí (těžká, k10) |
| 4 | 6 | Pěstitel hub | Sušené houby (zásoby) | Maska proti spórám |
| 5 | 1 | Stavitel hrází | Lopata | Dřevěné klíny |
| 5 | 2 | Kartograf | Brk a inkoust | Kompas |
| 5 | 3 | Vykradač pastiček | Kus sýra | Lepidlo |
| 5 | 4 | Tulák | Stan | Mapa k pokladu, pochybná |
| 5 | 5 | Pěstitel obilí | Kopí (těžká, k10) | Píšťalka |
| 5 | 6 | Poslíček | Deka | Dokumenty, zapečetěné |
| 6 | 1 | Trubadúr | Hudební nástroj | Maskovací sada |
| 6 | 2 | Hazardní hráč | Zatížené kostky | Zrcátko |
| 6 | 3 | Sběrač mízy | Vědro | Dřevěné klíny |
| 6 | 4 | Včelař | Sklenice medu | Síť |
| 6 | 5 | Knihovník | Útržek ze starodávné knihy | Brk a inkoust |
| 6 | 6 | Zchudlý šlechtic | Plstěný klobouk | Parfém |

---

## TAB-ZNA-01: Rodné znamení
**Účel:** Určení povahy postavy
**Použití:** Při tvorbě postavy nebo NPC
**Kostka:** k6

| k6 | Znamení | Povaha |
|----|---------|--------|
| 1 | Hvězda | Statečná/zbrklá |
| 2 | Kolo | Pracovitá/nenápaditá |
| 3 | Žalud | Zvědavá/paličatá |
| 4 | Bouřka | Štědrá/popudlivá |
| 5 | Měsíc | Moudrá/záhadná |
| 6 | Matka | Pečující/ustaraná |

---

## TAB-SRS-01: Srst - barva
**Účel:** Určení barvy srsti
**Použití:** Při tvorbě postavy nebo NPC
**Kostka:** k6

| k6 | Barva |
|----|-------|
| 1 | Čokoládová |
| 2 | Černá |
| 3 | Bílá |
| 4 | Světle hnědá |
| 5 | Šedá |
| 6 | Namodralá |

---

## TAB-SRS-02: Srst - vzor
**Účel:** Určení vzoru srsti
**Použití:** Při tvorbě postavy nebo NPC
**Kostka:** k6

| k6 | Vzor |
|----|------|
| 1 | Jednolitá |
| 2 | Mourovatá |
| 3 | Strakatá |
| 4 | Pruhovaná |
| 5 | Tečkovaná |
| 6 | Skvrnitá |

---

## TAB-RYS-01: Výrazný rys
**Účel:** Určení výrazného rysu postavy
**Použití:** Při tvorbě postavy nebo NPC
**Kostka:** k66 (k6 x 10 + k6)
**Poznámka:** První k6 = desítky, druhá k6 = jednotky

| k66 | Rys |
|-----|-----|
| 11 | Tělo plné jizev |
| 12 | Korpulentní tělo |
| 13 | Vychrtlé tělo |
| 14 | Klackovité tělo |
| 15 | Drobné tělíčko |
| 16 | Rozložité tělo |
| 21 | Válečné malování |
| 22 | Cizokrajné oblečení |
| 23 | Elegantní oblečení |
| 24 | Záplatované oblečení |
| 25 | Módní oblečení |
| 26 | Neprané oblečení |
| 31 | Useknuté ucho |
| 32 | Neforemný obličej |
| 33 | Krásný obličej |
| 34 | Baculatý obličej |
| 35 | Jemné rysy v obličeji |
| 36 | Protáhlý obličej |
| 41 | Načesaná srst |
| 42 | Dredy |
| 43 | Nabarvená srst |
| 44 | Oholená srst |
| 45 | Kudrnatá srst |
| 46 | Sametová srst |
| 51 | Oči temné jako noc |
| 52 | Páska přes oko |
| 53 | Krvavě rudé oči |
| 54 | Moudrý pohled |
| 55 | Pronikavý pohled |
| 56 | Blyštivé oči |
| 61 | Zastřižený ocásek |
| 62 | Ocásek jako bič |
| 63 | Chocholatý ocásek |
| 64 | Pahýl ocásku |
| 65 | Chápavý ocásek |
| 66 | Zakroucený ocásek |

---

## TAB-JME-01: Myší jména - vlastní jméno
**Účel:** Generování vlastního jména myši
**Použití:** Při tvorbě postavy nebo NPC (hoď 1-100)
**Kostka:** k100 nebo 2x k10 (první = desítky, druhá = jednotky)
**Vazby:** → Kombinuj s TAB-JME-02 (mateřské jméno)

| # | Jméno | # | Jméno | # | Jméno | # | Jméno |
|---|-------|---|-------|---|-------|---|-------|
| 1 | Ada | 26 | Fenykl | 51 | Krokus | 76 | Perla |
| 2 | Agáta | 27 | Fialka | 52 | Kuklík | 77 | Rípčíp |
| 3 | Akácie | 28 | Filip | 53 | Květa | 78 | Rokfór |
| 4 | Aloe | 29 | Františka | 54 | Levandule | 79 | Routa |
| 5 | Ambrož | 30 | Gouda | 55 | Lilie | 80 | Rozmarín |
| 6 | Anežka | 31 | Grácie | 56 | Líska | 81 | Rulík |
| 7 | Anýz | 32 | Gvendolína | 57 | Lorenz | 82 | Řebřík |
| 8 | Apríl | 33 | Habrovec | 58 | Magnolie | 83 | Sedmikráska |
| 9 | Astra | 34 | Háta | 59 | Majoránka | 84 | Slídie |
| 10 | Augustín | 35 | Hložek | 60 | Makovec | 85 | Smaragd |
| 11 | Azalka | 36 | Horácio | 61 | Máslena | 86 | Svízel |
| 12 | Bazalka | 37 | Hyacint | 62 | Meduňka | 87 | Šafrán |
| 13 | Berylie | 38 | Iris | 63 | Měsíček | 88 | Šimon |
| 14 | Bobek | 39 | Jalovec | 64 | Muškát | 89 | Šípek |
| 15 | Bodlák | 40 | Janek | 65 | Myrta | 90 | Šťavel |
| 16 | Bříz | 41 | Jasan | 66 | Niva | 91 | Tis |
| 17 | Čedar | 42 | Jaspis | 67 | Nora | 92 | Vavřinec |
| 18 | Čekanka | 43 | Jeřabinka | 68 | Okřál | 93 | Vilík |
| 19 | Devětsil | 44 | Jílovec | 69 | Oliver | 94 | Višňa |
| 20 | Edmund | 45 | Jiřička | 70 | Olivie | 95 | Vlnka |
| 21 | Eidam | 46 | Karmína | 71 | Olša | 96 | Vrbena |
| 22 | Elza | 47 | Klára | 72 | Opál | 97 | Vřesena |
| 23 | Emil | 48 | Kmínek | 73 | Otýlie | 98 | Vřesík |
| 24 | Erina | 49 | Konrád | 74 | Pelyňka | 99 | Zuzanka |
| 25 | Estragon | 50 | Kostřava | 75 | Pepřík | 100 | Žitmil |

---

## TAB-JME-02: Myší jména - mateřské jméno
**Účel:** Generování mateřského jména (příjmení)
**Použití:** Při tvorbě postavy nebo NPC
**Kostka:** k20
**Vazby:** → Kombinuj s TAB-JME-01 (vlastní jméno)

| k20 | Mateřské jméno (mužský rod) | Mateřské jméno (ženský rod) |
|-----|----------------------------|----------------------------|
| 1 | Bílý | Bílá |
| 2 | Černý | Černá |
| 3 | Čihař | Čihařová |
| 4 | Darček | Darčeková |
| 5 | Durman | Durmanová |
| 6 | Hrabal | Hrabalová |
| 7 | Chalva | Chalvová |
| 8 | Jařinka | Jařinková |
| 9 | Jeleňák | Jeleňáková |
| 10 | Jeseň | Jeseňová |
| 11 | Katzenreiser | Katzenreiserová |
| 12 | Máselník | Máselníková |
| 13 | Píp | Pípová |
| 14 | Řešetlák | Řešetláková |
| 15 | Semínko | Semínková |
| 16 | Sníh | Sněhová |
| 17 | Strážný | Strážná |
| 18 | Trnka | Trnková |
| 19 | Urobil | Urobílová |
| 20 | Žvanil | Žvanilová |

---

## TAB-CET-01: Cetky a drobnosti
**Účel:** Náhodný drobný předmět navíc
**Použití:** Při tvorbě postavy (volitelné)
**Kostka:** k6 + k8
**Poznámka:** První k6 určuje kategorii, druhá k8 konkrétní předmět

| k6 | k8 | Předmět |
|----|----|---------| 
| 1 | - | k8 ďobků |
| 2 | 1 | Sušený pětilístek, opatrně složený |
| 2 | 2 | Kamenný přívěsek Matky |
| 2 | 3 | Pahýl tužky |
| 2 | 4 | Sušené bylinky v nepromokavém pytlíku |
| 2 | 5 | Drát ohnutý do tvaru můry |
| 2 | 6 | Psaný rozkaz od myšího šlechtice |
| 2 | 7 | Vyleštěný kousek barevného sklíčka |
| 2 | 8 | Polosnězený kus sýra zabalený v papíru |
| 3 | 1 | Začouzený netopýří zub |
| 3 | 2 | Plecháček zdobený loveckými výjevy |
| 3 | 3 | Zvláštně třpytivý opál ve stříbrném opletení |
| 3 | 4 | Nůž vyrobený z plechovky |
| 3 | 5 | Keramický džbánek hutné medoviny |
| 3 | 6 | Včelí žihadlo přidrátované k dřevěné násadě |
| 3 | 7 | Kandovaná bobulka |
| 3 | 8 | Motýlí křídla vylisovaná mezi pergameny |
| 4 | 1 | Mapa k pokladu skrytému v osadě |
| 4 | 2 | Vzkaz hráčské myši od kočičího pána |
| 4 | 3 | Dřevěná modla stonožky požírající si ocas |
| 4 | 4 | Zub lidského dítěte |
| 4 | 5 | Plechovka svítivé barvy |
| 4 | 6 | Rozzuřená mravenčí královna ve sklenici |
| 4 | 7 | Srolovaná tapiserie s výjevem dávné bitvy |
| 4 | 8 | Hrouda vlhkého jílu, který nikdy nevyschne |
| 5 | 1 | Pramínek vílích vlasů |
| 5 | 2 | Lahvička červeného inkoustu |
| 5 | 3 | Slaměný košík s koženými popruhy |
| 5 | 4 | Úlomek destičky s kouzlem |
| 5 | 5 | Sušené jedovaté houby |
| 5 | 6 | Růžový plastový kartáč na srst |
| 5 | 7 | Hromádka sušeného listí omotaná motouzem |
| 5 | 8 | Dýmka vyřezaná z lastury |
| 6 | 1 | Útržek ovčího rouna |
| 6 | 2 | Toulec šípů se stříbrnými hroty |
| 6 | 3 | Klubko stříbrného drátu |
| 6 | 4 | Velice silný magnet |
| 6 | 5 | Hopík |
| 6 | 6 | Brašna z rybí kůže |
| 6 | 7 | Extrémně ostrá čili paprička |
| 6 | 8 | Moucha zachovaná v pryskyřici |

---

# 🗺️ SEKCE B: SVĚT A MAPA

## TAB-HEX-01: Typ hexu
**Účel:** Určení typu krajiny hexu
**Použití:** Při generování mapy hexcrawlu
**Kostka:** k6
**Vazby:** → Určuje, kterou tabulku výrazných prvků použít (TAB-HEX-02 až 05)

| k6 | Typ hexu |
|----|----------|
| 1-2 | Otevřená krajina → použij TAB-HEX-02 |
| 3-4 | Les → použij TAB-HEX-03 |
| 5 | Řeka → použij TAB-HEX-04 |
| 6 | Lidské město → použij TAB-HEX-05 |

---

## TAB-HEX-02: Výrazné prvky - Otevřená krajina
**Účel:** Určení výrazného prvku v otevřené krajině
**Použití:** Po hodu TAB-HEX-01 (výsledek 1-2)
**Kostka:** k20

| k20 | Výrazný prvek |
|-----|--------------|
| 1 | Mraveniště |
| 2 | Buk rozštípnutý bleskem |
| 3 | Strom bílý jako kost |
| 4 | Kostra krávy |
| 5 | Květnatá louka |
| 6 | Pšeničné pole |
| 7 | Zarostlá mez |
| 8 | Dutý pařez |
| 9 | Obrovský placatý kámen |
| 10 | Rybníček zarostlý lekníny |
| 11 | Kolosální padlý strom |
| 12 | Starý sukovitý dub |
| 13 | Starý statek |
| 14 | Tichá prašná cesta |
| 15 | Králičí nora |
| 16 | Vrabčí hnízdo |
| 17 | Borovicový hájek |
| 18 | Strmý kopec |
| 19 | Kamenná zeď |
| 20 | Změť vystouplých kořenů |

---

## TAB-HEX-03: Výrazné prvky - Les
**Účel:** Určení výrazného prvku v lese
**Použití:** Po hodu TAB-HEX-01 (výsledek 3-4)
**Kostka:** k20

| k20 | Výrazný prvek |
|-----|--------------|
| 1 | Opuštěná chýše |
| 2 | Slunečná mýtina |
| 3 | Kaskáda vodopádů |
| 4 | Útes |
| 5 | Studený, svěží pramen |
| 6 | Hustý podrost |
| 7 | Obličej v prastarém dubu |
| 8 | Liščí nora |
| 9 | Háj kapradí |
| 10 | Dutý pařez |
| 11 | Obrovská borovice |
| 12 | Lidská stezka |
| 13 | Lidská mýtina |
| 14 | Klikatící se potůček |
| 15 | Zarostlé rozvaliny |
| 16 | Kruh z kamenů |
| 17 | Skalní výběžek |
| 18 | Propadlina |
| 19 | Změť kořenů |
| 20 | Strom provrtaný termity |

---

## TAB-HEX-04: Výrazné prvky - Řeka
**Účel:** Určení výrazného prvku u řeky
**Použití:** Po hodu TAB-HEX-01 (výsledek 5)
**Kostka:** k20

| k20 | Výrazný prvek |
|-----|--------------|
| 1 | Zdymadlo |
| 2 | Soutok |
| 3 | Závoje vrbových větví |
| 4 | Podemletý břeh |
| 5 | Padlý strom přes řeku |
| 6 | Vysoký vodopád |
| 7 | Obří balvan |
| 8 | Obří betonová přehrada |
| 9 | Izolovaný ostrov |
| 10 | Blátivá mělčina |
| 11 | Skalnaté peřeje |
| 12 | Řada uschlých stromů |
| 13 | Bahnitá hráz |
| 14 | Nášlapné kameny |
| 15 | Kamenný most |
| 16 | Kamenitá mělčina |
| 17 | Ponořené odpadky |
| 18 | Potopená loďka |
| 19 | Propletené kořeny |
| 20 | Dřevěný most |

---

## TAB-HEX-05: Výrazné prvky - Lidské město
**Účel:** Určení výrazného prvku v lidském městě
**Použití:** Po hodu TAB-HEX-01 (výsledek 6)
**Kostka:** k20

| k20 | Výrazný prvek |
|-----|--------------|
| 1 | Opuštěné auto |
| 2 | Balkón bytu |
| 3 | Ostružinové houští |
| 4 | Rušná silnice |
| 5 | Výpust okapu |
| 6 | Naházený nábytek |
| 7 | Skleník |
| 8 | Myší trosky |
| 9 | Nově postavený dům |
| 10 | Zarostlý záhonek |
| 11 | Holubí hnízdo |
| 12 | Hromada odpadků |
| 13 | Nákupní vozík |
| 14 | Zatuchlé jezírko |
| 15 | Ocelový most |
| 16 | Kontejner plný odpadků |
| 17 | Pěšina lemovaná stromy |
| 18 | Podzemní parkoviště |
| 19 | Kůlna na dříví |
| 20 | (Hoď znovu nebo vymysli vlastní) |

---

## TAB-HEX-06: Detaily výrazných prvků
**Účel:** Přidání zajímavého detailu k výraznému prvku
**Použití:** Po určení výrazného prvku z TAB-HEX-02 až 05
**Kostka:** k6 + k8
**Poznámka:** První k6 určuje kategorii detailu, druhá k8 konkrétní detail

| k6 | k8 | Detail | Doplňující otázka |
|----|----|--------|------------------|
| 1 | - | Myší osada... | [TAB-OSA-01 a další tabulky osad] |
| 2 | 1 | Menší myší farma | Co se stalo s úrodou? |
| 2 | 2 | Hrad myšího šlechtice | Před čím chrání? |
| 2 | 3 | Vlídný myší zájezdní hostinec | Co je ve sklepě? |
| 2 | 4 | Myší lovecký srub | Co zdejší myši loví? |
| 2 | 5 | Hornická osada | Co vykopali? |
| 2 | 6 | Bouda myšího poustevníka | Proč se straní společnosti? |
| 2 | 7 | Přírodní jeskyně | Co v ní žije? |
| 2 | 8 | Věž potulného rytíře | Co je jeho posláním? |
| 3 | 1 | Hnízdo zpěvného ptáka | Jaké smutné příběhy pěje? |
| 3 | 2 | Kmen obřích, mírumilovných zvířat | Čeho se bojí? |
| 3 | 3 | Skrýš krysích loupežníků | Koho okrádají? |
| 3 | 4 | Věž vraních čarodějnic | Jaká kouzla krákají? |
| 3 | 5 | Hmyzí hnízdo | Na co mají chuť? |
| 3 | 6 | Doupě velké šelmy | Jaké poklady střeží? |
| 3 | 7 | Žabí pevnost | Co se skrývá v kobkách? |
| 3 | 8 | Věž myšího čaroděje | Jaké kouzlo má skoro připravené? |
| 4 | 1 | Nebezpečný přírodní prvek | Jak se mu vyhnout? |
| 4 | 2 | Osamělá svatyně | Kdo o ni pečuje? Koho uctívá? |
| 4 | 3 | Sídlo myšího šlechtice | Proč je opuštěné? |
| 4 | 4 | Opuštěná osada | Jaké po nich zůstaly stopy? |
| 4 | 5 | Pobořená strážní věž | Před čím chránila? |
| 4 | 6 | Přírodní prvek, klidný a bezpečný | Kdo se tu potkává? |
| 4 | 7 | Přírodní prvek, nepatřičný | Jak se utvořil? |
| 4 | 8 | Vachrlatý most | Přes co se klene? |
| 5 | 1 | Starý chrám netopýřího kultu | Co tu vyvolali? |
| 5 | 2 | Vílí kruh | O co se tu víly pokoušejí? |
| 5 | 3 | Broučí hřbitov | Co duchové chtějí? |
| 5 | 4 | Chýše myší čarodějnice | Co zrovna vaří? |
| 5 | 5 | Malé, ale hluboké jezírko | Co leží na dně? |
| 5 | 6 | Rostliny z jiného ročního období | Proč tu rostou? |
| 5 | 7 | Hnízdo soví čarodějky | Po čem pátrá? |
| 5 | 8 | Zvláštní magická anomálie | Proč se šíří? |
| 6 | 1 | Zřícená vzducholoď liliputů | Jak se dá opravit? |
| 6 | 2 | Hučící kámen | Co se stane, když se ho někdo dotkne? |
| 6 | 3 | Naprosté mrtvo | Jaká katastrofa se tu odehrála? |
| 6 | 4 | Pravidelně používáno lidmi | Co tu dělají? |
| 6 | 5 | Poškozeno lidmi | Co provedli? |
| 6 | 6 | Starodávné trosky zaniklé civilizace | Kdo je postavil? |
| 6 | 7 | Loviště kočičího pána | Jaké trofeje tu zůstávají? |
| 6 | 8 | Přestavěná lidská stavba | K čemu slouží teď? |

---

## TAB-OSA-01: Velikost osady
**Účel:** Určení velikosti myší osady
**Použití:** Při generování osady
**Kostka:** 2k6, použij NIŽŠÍ výsledek
**Vazby:** → Ovlivňuje TAB-OSA-02 (společenské zřízení)

| k6 | Velikost | Populace |
|----|----------|----------|
| 1 | Farma/zámeček | 1-3 rodiny |
| 2 | Křižovatka | 3-5 rodin |
| 3 | Víska | 50-150 myší |
| 4 | Vesnice | 150-300 myší |
| 5 | Město | 300-1000 myší |
| 6 | Velkoměsto | 1000+ myší |

---

## TAB-OSA-02: Společenské zřízení
**Účel:** Určení vlády/správy osady
**Použití:** Po určení velikosti z TAB-OSA-01
**Kostka:** k6 + velikost (1 u farmy, 6 u velkoměsta)
**Poznámka:** Sečti hod k6 + číslo velikosti z předchozí tabulky

| k6+ | Společenské zřízení |
|-----|-------------------|
| 2-3 | Vedená vesnickými stařešiny |
| 4-5 | Spravovaná rytířem nebo nižším šlechticem |
| 6-7 | Organizovaná cechovním výborem |
| 8-9 | Svobodná osada pod správou rady měšťanů |
| 10-11 | Domov významnějšího šlechtice |
| 12 | Hlavní sídlo šlechtické moci |

---

## TAB-OSA-03: Výrazný prvek osady
**Účel:** Určení, co osadu odlišuje
**Použití:** Při generování osady (velkoměsta mají 2 prvky)
**Kostka:** k20

| k20 | Výrazný prvek |
|-----|--------------|
| 1 | Bludiště obranných chodeb plných pastí |
| 2 | Mimořádně pohodlný a dobře zařízený hostinec |
| 3 | Svatyně vyřezaná z černého dřeva |
| 4 | Meditační houbová zahrádka |
| 5 | Kravská lebka sloužící jako cechovní síň |
| 6 | Nepřehledná změť těsně namačkaných chýší |
| 7 | Úhledné řady zavěšených dřevěných domků |
| 8 | Zdobená brána střežená sochami |
| 9 | Tajný chrám netopýřího kultu |
| 10 | Dráha na broučí závody |
| 11 | Spižírna napěchovaná trvanlivými zásobami |
| 12 | Skryté říční molo |
| 13 | Pobořený mramorový palác myších prapředků |
| 14 | Ukořistěný lidský stroj, funkční |
| 15 | Osada se nachází za dřevěným mostem |
| 16 | Znepokojivě vysoká pokroucená věž |
| 17 | Krásná květinová zahrádka |
| 18 | Hnízdo holubího jezdce |
| 19 | Zarostlá socha prastarého hrdiny |
| 20 | Točité schodiště vedoucí hluboko pod zem |

---

## TAB-OSA-04: Podrobnosti o obyvatelích
**Účel:** Určení zvyklostí a zvláštností obyvatel
**Použití:** Při generování osady
**Kostka:** k20

| k20 | Podrobnosti o obyvatelích |
|-----|--------------------------|
| 1 | Holí si v srsti složité vzory |
| 2 | Intoxikovaní zvláštními rostlinami |
| 3 | Zdráhají se jednat s cizími myšmi |
| 4 | Zvědaví na novinky z dalekých krajů |
| 5 | Věří, že česat si srst přináší smůlu |
| 6 | Nosí krásně vyšívané oblečení |
| 7 | Vaří medovinu ochucenou vonnými bylinami |
| 8 | Zakrývají si tváře dlouhými kápěmi |
| 9 | Jsou chudí kvůli placení daní kočičímu pánovi |
| 10 | Obřadně si zastřihují ocásky |
| 11 | Stateční lovci velkých zvířat |
| 12 | Všichni jsou potomci jedné matriarchy |
| 13 | Pečou lahodné koláče z lesních plodů |
| 14 | Utekli z laboratoře, o světě moc neví |
| 15 | Tráví dny lenošením u potoka |
| 16 | Dávný krevní spor s jinou osadou |
| 17 | Pod dohledem cechu kopou velkolepé chodby |
| 18 | Nosí velké klobouky s širokou krempou |
| 19 | Jejich zákony a zvyky jsou pro cizince matoucí |
| 20 | Jsou spřátelení s predátorem |

---

## TAB-OSA-05: Živnost
**Účel:** Určení, čím se osada živí
**Použití:** Při generování osady (města a velkoměsta = 2x)
**Kostka:** k20

| k20 | Živnost |
|-----|---------|
| 1 | Zemědělci pečující o tyčící se plodiny |
| 2 | Dřevorubci s pilami a potahy |
| 3 | Drsní a ošlehaní rybáři se sítěmi a vory |
| 4 | Tmavá a zatuchlá houbová farma |
| 5 | Na každém rovném povrchu se suší obilí |
| 6 | Aromatický sýr, několik let uleželý |
| 7 | Zahrádky vzácných bylin, střežené sušáky |
| 8 | Včelí úly a včelaři v ochranných oděvech |
| 9 | Kupci a obchodníci, často shánějí stráže |
| 10 | Kameníci pracující v nedalekém lomu |
| 11 | Mlýn poháněný velkým vodním kolem |
| 12 | Hlubinný důl na železo, stříbro nebo cín |
| 13 | Chovají bource a tkají jemné hedvábí |
| 14 | Zkušení průzkumníci jeskyní a chodeb |
| 15 | Keramika s pestrobarevnými glazurami |
| 16 | Přádelna vlny ověšená jasnými látkami |
| 17 | Vynikající škola s neukázněnými žáky |
| 18 | Rušná, dobře zásobená tržnice |
| 19 | Páchnoucí hora odpadků, pečlivě přebíraná |
| 20 | Krásně vyřezávaný nábytek z leštěného dřeva |

---

## TAB-OSA-06: Událost v osadě
**Účel:** Co se právě děje při příchodu hráčů
**Použití:** Při návštěvě osady
**Kostka:** k20

| k20 | Událost |
|-----|---------|
| 1 | Katastrofa, všichni se balí a odcházejí |
| 2 | Svatba, ulice vyzdobené květinami |
| 3 | Příprava na velkou sezónní hostinu |
| 4 | Udeřila nemoc |
| 5 | Hmyz spořádal obsah spižíren |
| 6 | Koná se trh, do osady se sjíždějí kupci |
| 7 | Myši si jdou po krku |
| 8 | Formuje se tlupa na boj s velkým zvířetem |
| 9 | Několik myší se ztratilo |
| 10 | Myší šlechtic vznesl svévolný požadavek |
| 11 | Dorazila potulná divadelní kumpanie |
| 12 | Pohřeb, ulice plné kouře |
| 13 | Podvodník spřádá vyšinuté plány |
| 14 | Domácí brouk se pomátl a napadá myši |
| 15 | Vílí velvyslanec s nemožným požadavkem |
| 16 | V okolí se šíří zvláštní, rychle rostoucí rostlina |
| 17 | Někdo ukradl drahocenné dědictví |
| 18 | Kočičí pán si žádá nehoráznou daň |
| 19 | Mladé myši slaví svátek dospělosti |
| 20 | Na želvím hřbetě přijela čarodějova věž |

---

## TAB-OSA-NAZ-01: Názvy osad - Začátek A
**Účel:** Generování názvu osady (1. část)
**Použití:** Hoď 2x k12 - první určí začátek
**Kostka:** k12

| k12 | Začátek A |
|-----|-----------|
| 1 | Dub |
| 2 | Bob |
| 3 | Vrba |
| 4 | Pařez |
| 5 | Smrk |
| 6 | Měsíc |
| 7 | Zelená |
| 8 | Černá |
| 9 | Kámen |
| 10 | Vysoký |
| 11 | Buk |
| 12 | Jablko |

---

## TAB-OSA-NAZ-02: Názvy osad - Konec B
**Účel:** Generování názvu osady (2. část)
**Použití:** Hoď 2x k12 - druhý určí konec (kombinuj s TAB-OSA-NAZ-01)
**Kostka:** k12
**Poznámka:** Mixuj začátek + konec, dokud to nezní dobře

| k12 | Konec B |
|-----|---------|
| 1 | Luh |
| 2 | Háj |
| 3 | Věž |
| 4 | Újezd |
| 5 | Most |
| 6 | Brod |
| 7 | Voda |
| 8 | Hora |
| 9 | Nora |
| 10 | Lhota |
| 11 | Hrob |
| 12 | Žďár |

---

## TAB-OSA-NAZ-03: Názvy osad - Začátek B (alternativa)
**Účel:** Alternativní začátky názvů osad
**Použití:** Pro větší rozmanitost kombinuj s TAB-OSA-NAZ-04 a 05
**Kostka:** k12

| k12 | Začátek B |
|-----|-----------|
| 1 | Bláto |
| 2 | Sova |
| 3 | Liška |
| 4 | Žalud |
| 5 | Měď |
| 6 | Lup |
| 7 | Sýr |
| 8 | Mokro |
| 9 | Růže |
| 10 | Cín |
| 11 | Dobro |
| 12 | Kmen |

---

## TAB-OSA-NAZ-04: Názvy osad - Konec A (alternativa)
**Účel:** Alternativní konce názvů osad
**Použití:** Pro větší rozmanitost
**Kostka:** k12

| k12 | Konec A |
|-----|---------|
| 1 | -ov |
| 2 | -ovec |
| 3 | -ová |
| 4 | -ice |
| 5 | -iny |
| 6 | -ín |
| 7 | -ec |
| 8 | -ník |
| 9 | -any |
| 10 | -ves |
| 11 | Hradec |
| 12 | Městec |

---

## TAB-OSA-NAZ-05: Názvy osad - 2. část
**Účel:** Druhá část složeného názvu
**Použití:** Pro kreativnější názvy (např. "U Bílého Brouka")
**Kostka:** k12

| k12 | 2. část |
|-----|---------|
| 1 | Brouk |
| 2 | Liška |
| 3 | Špalek |
| 4 | Semínko |
| 5 | Krysa |
| 6 | Sýr |
| 7 | Orel |
| 8 | Červ |
| 9 | Včela |
| 10 | Lucerna |
| 11 | Růže |
| 12 | Rytíř |

---

## TAB-HOS-01: Názvy hospod - 1. část
**Účel:** Generování názvu hospody (1. část)
**Použití:** U hospod - kombinuj s TAB-HOS-02
**Kostka:** k12
**Poznámka:** Hospoda se jmenuje "U..."

| k12 | 1. část |
|-----|---------|
| 1 | Bílý |
| 2 | Zelený |
| 3 | Černý |
| 4 | Červený |
| 5 | Stříbrný |
| 6 | Křivý |
| 7 | Přátelský |
| 8 | Schovaný |
| 9 | Lstivý |
| 10 | Skleněný |
| 11 | Trnitý |
| 12 | Rozbitý |

---

## TAB-HOS-02: Názvy hospod - 2. část
**Účel:** Generování názvu hospody (2. část)
**Použití:** U hospod - kombinuj s TAB-HOS-01
**Kostka:** k12
**Poznámka:** Např. "U Bílého Brouka", "U Zeleného Sýra"

| k12 | 2. část |
|-----|---------|
| 1 | Brouk |
| 2 | Liška |
| 3 | Špalek |
| 4 | Semínko |
| 5 | Krysa |
| 6 | Sýr |
| 7 | Orel |
| 8 | Červ |
| 9 | Včela |
| 10 | Lucerna |
| 11 | Růže |
| 12 | Rytíř |

---

## TAB-HOS-03: Specialita hospody
**Účel:** Určení speciality kuchyně
**Použití:** Při generování hospody
**Kostka:** k12

| k12 | Specialita |
|-----|------------|
| 1 | Pečená kořeněná mrkev |
| 2 | Žížalí vývar |
| 3 | Ostružinový koláč |
| 4 | Uleželý aromatický sýr |
| 5 | Ječmenná kaše |
| 6 | Tlustý rybí řízek |
| 7 | Pečené jablko |
| 8 | Smažené hmyzí nožičky |
| 9 | Čerstvý máslový chléb |
| 10 | Ukořistěné sladkosti |
| 11 | Semínka pražená v medu |
| 12 | Houbový guláš |

---

# 👥 SEKCE C: NPC A TVOROVÉ

## TAB-NPC-01: Nehráčské myši - Vzhled
**Účel:** Určení vzhledu nehráčské myši
**Použití:** Při generování NPC
**Kostka:** k20
**Vazby:** → Kombinuj s TAB-NPC-02, 03, 04, 05

| k20 | Vzhled |
|-----|--------|
| 1 | Zkroušený pohled |
| 2 | Záplatované oblečení |
| 3 | Věnec ze sedmikrásek |
| 4 | Upatlané oblečení |
| 5 | Velký plandající klobouk |
| 6 | Kapsy plné semínek |
| 7 | Hůlka z ohnuté větvičky |
| 8 | Má rezavý špendlomeč |
| 9 | Dlouhá zacuchaná srst |
| 10 | Hodně, hodně stará |
| 11 | Zafačovaný ocásek |
| 12 | Ocásek omotaný pentlí |
| 13 | Nemá ucho |
| 14 | Dlouhé fousky |
| 15 | Třpytivé oči |
| 16 | Obrovský černý plášť |
| 17 | Staré jizvy z boje |
| 18 | Velmi mladá |
| 19 | Oholená srst |
| 20 | Zaplétaná srst |

---

## TAB-NPC-02: Nehráčské myši - Zvláštnost
**Účel:** Určení charakterové zvláštnosti
**Použití:** Při generování NPC
**Kostka:** k20
**Vazby:** → Kombinuj s TAB-NPC-01, 03, 04, 05

| k20 | Zvláštnost |
|-----|------------|
| 1 | Neustále se upravuje |
| 2 | Vyvádí kvůli počasí |
| 3 | Silně nabuzená |
| 4 | Zcestovalá, světaznalá |
| 5 | Prokletá čarodějem |
| 6 | Snadno se vyleká |
| 7 | Stydí se za dřívější zločiny |
| 8 | Velice soutěživá |
| 9 | Hýřivý opilec |
| 10 | Extrémně zdvořilá |
| 11 | Bezelstně upřímná |
| 12 | Mluví pomalu a rozvážně |
| 13 | Mluví rychle a zbrkle |
| 14 | Utajený služebník kočky |
| 15 | Vychována krysami |
| 16 | Vyhnanec z domova |
| 17 | Spousta hmyzích mazlíčků |
| 18 | Nesnáší být venku |
| 19 | Místní hrdina |
| 20 | Velice neklidné fousky |

---

## TAB-NPC-03: Nehráčské myši - Po čem touží
**Účel:** Určení motivace NPC
**Použití:** Při generování NPC
**Kostka:** k20
**Vazby:** → Kombinuj s TAB-NPC-01, 02, 04, 05

| k20 | Po čem touží |
|-----|--------------|
| 1 | Svoboda |
| 2 | Bezpečí |
| 3 | Útěk |
| 4 | Vzrušení |
| 5 | Moc |
| 6 | Smysl |
| 7 | Zdraví |
| 8 | Bohatství |
| 9 | Ochrana |
| 10 | Láska |
| 11 | Někoho chránit |
| 12 | Jídlo |
| 13 | Přátelství |
| 14 | Odpočinek |
| 15 | Vědomosti |
| 16 | Krutost |
| 17 | Krása |
| 18 | Pomsta |
| 19 | Sloužit |
| 20 | Zábava |

---

## TAB-NPC-04: Nehráčské myši - Vztah k PC
**Účel:** Určení vztahu NPC k hráčské postavě
**Použití:** Při generování NPC s vazbou na PC
**Kostka:** k20
**Vazby:** → Kombinuj s TAB-NPC-01, 02, 03, 05

| k20 | Vztah |
|-----|-------|
| 1 | Rodič |
| 2 | Sourozenec |
| 3 | Bratránek/sestřenka |
| 4 | Vzdálený bratránek/sestřenka |
| 5 | Prarodič |
| 6 | Příbuzný, ale neví o tom |
| 7 | Manželé |
| 8 | Bývalí milenci |
| 9 | Neopětovaná láska |
| 10 | Kamarád z hospody |
| 11 | Dlužník nebo věřitel |
| 12 | Dlouhý a bouřlivý |
| 13 | Zapřísáhlí nepřátelé |
| 14 | Bratři nebo sestry z cechu |
| 15 | Přátelé z dětství |
| 16 | Jedna okradla druhou |
| 17 | Spolupracovník |
| 18 | Vyrůstaly spolu |
| 19 | Slouží stejnému pánovi |
| 20 | Nikdy dřív se nepotkaly |

---

## TAB-NPC-05: Nehráčské myši - Společenské postavení
**Účel:** Určení majetku a sociální vrstvy NPC
**Použití:** Při generování NPC
**Kostka:** k6
**Vazby:** → Kombinuj s TAB-NPC-01, 02, 03, 04

| k6 | Společenské postavení | Typická platba za služby |
|----|-----------------------|-------------------------|
| 1 | Chuďas | k6 ď |
| 2 | Prostá myš | k6 x 10 ď |
| 3 | Prostá myš | k6 x 10 ď |
| 4 | Měšťan | k6 x 50 ď |
| 5 | Člen cechu | k4 x 100 ď |
| 6 | Myší šlechtic | k4 x 1000 ď |

---

[POKRAČOVÁNÍ V DALŠÍM SOUBORU - toto je první část, obsahuje sekce A, B a začátek C]

---

**STAV DOKUMENTU 1:**
✅ Sekce A: TVORBA POSTAV - HOTOVO
✅ Sekce B: SVĚT A MAPA - HOTOVO  
✅ Sekce C: NPC A TVOROVÉ - ZAČATO (pokračuji v dalším souboru)

**CO ZBÝVÁ:**
⏳ Dokončit Sekci C (bestář, pomocníci)
⏳ Sekce D: DOBRODRUŽSTVÍ
⏳ Sekce E: FRAKCE A UDÁLOSTI
⏳ Sekce F: MAGIE
