# C3 – Bosch Rexroth / Festo, magnet Ø14 × 5 mm

Konštrukčne rozpracovaná revízia konceptu C2. **Nie je uvoľnená do výroby.** Montážne platne a otvory sú navrhnuté; nakupované diely sú zjednodušené geometrie. Zostava je uložená v polohe pred odberom magnetu hlavou, vidlička pri lise. Predošlé verzie sa nemenia.

## Súbory
- `models/concept-C3/Rohovnik_press_C3_Bosch_Festo.step`: zostava v mm.
- `models/concept-C3/plates/`: samostatné STEP platní a DXF priečne rezy v mierke 1:1. Lišty majú samostatné STEP.
- `BOM.csv`: položky zostavy, materiál/dodávateľ, špecifikácia a rozmery obálky. Jedna položka je jeden diel; nie nákupná objednávka.
- `Holes.csv`: súradnice otvorov, modelovaný priemer a zamýšľaná operácia.
- `cad/build_C3.py`: reprodukovateľný CAD zdroj; vyžaduje CadQuery a zdroje predchádzajúcich verzií v repozitári.

## Potvrdené zadanie
Magnet Ø14 × 5 mm. Vstupný sklz zalomený o 90° v pôdoryse, separátor posúva rohovníky ku lisu, pridržanie dielu úkosmi, priechodný výstup. Pružinová skrutka M6 × 12 kolmo zdola na stred dielu. Podávač magnetov C s nezávislou uzávierkou. Zásobník s aktívnou výškou 300 mm. Tlak a lisovacia sila nie sú potvrdené; výpočet je predbežne pre 6 bar.

## Rám Bosch Rexroth
Predbežne 45 × 45, drážka 10: dve stojky dĺžky 200 mm a stožiar zásobníka 340 mm. Zobrazený je zjednodušený štvorcový prierez s drážkami, **nie prevzatý výrobný CAD Bosch**. Stojky sú mimo priechodného vedenia. Základňa má 500 × 400 × 15 mm, most 220 × 140 × 15 mm.

Presné objednávacie číslo profilu a nosnosť spojov neboli potvrdené. Koncové M12 spoje a centrálny pilot Ø10,2 sú predbežné: podľa konkrétneho profilu treba potvrdiť možnosť závitovania, prípadne nahradiť koncový spoj katalógovými uholníkmi. Drážkové M8 spoje stožiara sú rozmerový zámer; konečné matice a uholníky treba vybrať. Nepoužívať prierez z modelu ako výrobný výkres extrúzie.

## Festo – katalógový výber
Zdroj: [oficiálna stránka ADN](https://www.festo.com/us/en/p/compact-cylinder-id_ADN/) a [oficiálny katalóg ADN 2026/09](https://www.festo.com/media/catalog/203981_documentation.pdf), str. 17 (rozmery), 26–28 (objednávacie údaje). Verzia I má vnútorný závit piestnice.

| Funkcia | Typ | Číslo Festo | Rozteč TG | Čelný závit | Teoretická sila pri 6 bar |
|---|---|---|---|---|---|
| Lis | ADN-50-25-I-P-A | 536324 | 46,5 × 46,5 | M8 | 1178 N |
| Rohovníky | ADN-16-30-I-P-A | 536231 | 18 × 18 | M4 | 121 N |
| Vidlička | ADN-16-70-I-P-A | 8178767 | 18 × 18 | M4 | 121 N |
| Uzávierka magnetov | ADN-12-10-I-P-A | 536212 | 16 × 16 | M4 | 68 N |
| Závora vstupu | ADN-12-10-I-P-A | 536212 | 16 × 16 | M4 | 68 N |

Sily sú p×plocha piesta bez trenia/protitlaku. Konečný priemer lisu určiť zo skúšky lisovania. ADN sú bez vedenia: lis má samostatné tyče Ø12 a koncepčné puzdrá, vidlička klzné vedenie. Tvar drážok valca, prípojky, závity a spojky sú zjednodušené, nie oficiálne importované modely. Overené z katalógu sú E/TG/ZA/ZB/MM/RT použité v skripte; fitingy a senzorové drážky nie sú detailne modelované.

Vidlička potrebuje presun 65 mm. Valec so zdvihom 70 mm je v zostave zobrazený vysunutý o 65 mm. Treba nastaviť mechanické dorazy na pracovný presun 65 mm; nesmie sa predpokladať, že voľný koncový zdvih 70 mm správne vystredí magnet. Pohon bol odsunutý ďalej doprava, aby pri návrate vidlička nevchádzala do telesa valca. Od toho sa odvíja väčšia základňa.

## Platne a otvory
P01 základňa: priechody pre skrutky profilov, otvory podpery, uloženie tyčí, upevnenie pohonov, prístup k pružinovej skrutke a montáž na stôl.
P02 podpera lišty: závit M6 pre pružinovú skrutku, M4 pre lišty a M6 pre spoj so základňou.
P03 most: štyri priechodzie Ø9 pre ADN50 podľa TG46,5, otvor Ø20 pre piestnicu, tyče Ø12 a koncové spoje profilov.
P04 pohyblivá hlava: predbežné uloženie puzdier Ø18, závitová spojka a priechody nastaviteľných dorazov.
P05/P06: čelná doska a nastaviteľná pätka separátora.
P07/P09: čelná doska a pätka pohonu vidličky.
P08: police zásobníka s otvorom Ø20,5 pre rúrku a pripevnením objímok.
P10/P12: čelná doska a pätka uzávierky magnetov.
P11: konzola pohonu vstupnej závory.
Lišty: Ø4,5 a valcové zapustenie Ø7,5 hĺbky 4,5 mm pre M4×16. Spodná plocha rohovníka je v Z=0.

**Výklad exportov:** DXF zobrazuje prierez v polovici hrúbky, preto nezobrazuje každé zapustenie; rozhodujúci pre 3D tvar je STEP a tabuľka operácií. Súradnice panelov sú lokálne XY s počiatkom v strede obdĺžnika a spodkom v Z=0. Po umiestnení môžu byť dosky otočené. Lišty sú výnimka: otvory sú uvedené v súradniciach zostavy. P07 je v samostatnom STEP lokálne vodorovná, v zostave otočená na čelo valca.

Závity nie sú špirálovo modelované: tabuľka uvádza pilot (napr. Ø5 pre M6, Ø3,3 pre M4) a operáciu TAP. Priechody pre valce sú modelované voľné pre skrutku; závit je v nakupovanom valci. H7 a ostatné presné uloženia treba vyrobiť dokončovacou operáciou, nie vyrezať podľa DXF bez tolerancií.

## Nastavenie a čo dokončiť
- Overiť lisovaciu silu, skutočný tlak, lícovanie magnetu a tvrdosť/poddajnosť rohovníka.
- Vybrať presný Bosch profil a katalógové spoje; overiť tuhosť mosta a vedenia podľa nameranej sily.
- Zvoliť konkrétne lineárne puzdrá, ich uloženie, poistky a mazanie. Ø18 sedlá sú predbežné.
- Dokončiť rohové spoje držiakov pohonov, spojky piestnic, skrutky/matice a nastavenie dorazov. Nie každý spoj je v tejto revízii kompletne oskrutkovaný.
- Uzávierka stĺpca magnetov musí preukázateľne držať zvyšok stĺpca pri odoberaní jedného kusu; zasunutie medzi priťahujúce sa magnety treba skúsiť na vzorke. Stĺpec v modeli má iba štyri referenčné magnety.
- Skutočná gulička M6 skrutky musí zodpovedať stredovému otvoru Ø5; obálka Ø5,5 je stále predbežná.
- Dopracovať výsuvný polohovací doraz rohovníka pri lise. Gulička zdola nemá sama zadržiavať celú tlačenú radu dielov.
- Doplniť rozvádzače, redukciu tlaku lisu, škrtenie, hadice, snímače, pneumatickú schému a riadenie. Lis nesmie ísť dole pred odchodom vidličky a návratom separátora.

## Overenie
Skript kontroluje platnosť komponentov, spätný import STEP, umiestnenie otvorov v platniach a voľný výstup dielu v troch polohách voči lištám a stojkám. Nie je to kontrola všetkých statických prienikov ani simulácia celého cyklu. Výrobné tolerancie, všetky závitové hĺbky, pevnosť a celková bezkolíznosť nie sú schválené. Táto revízia je určená na konštrukčnú diskusiu a ďalšie detailovanie.
