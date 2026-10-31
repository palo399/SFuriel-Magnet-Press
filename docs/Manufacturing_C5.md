# C5 – výrobný návrh prototypu (NEUVOĽNENÉ)

Cieľ: rozpracovať schválenú C4 pri zachovaní troch valcov, priameho lisovania a priechodnej lišty. Potvrdený takt **10 ks/min = 6 s/cyklus**. Magnet **Ø14 × 5 mm**. V tejto revízii bol doplnený skutočný pružinový prvok, mechanický doraz a odstránená kolízia spojky vidličky. Zostava nie je schválená na výrobu ani skúšku pod tlakom, kým sa neuzavrú konkrétne body uvedené nižšie.

## Dodané podklady

V `models/manufacturing-C5/`:
- `Rohovnik_press_C5_prototype_DRAFT.step`: zostava.
- `parts/`: samostatné obrábané diely; rovinné diely aj DXF.
- `C5_Drawings_DRAFT.pdf`: 15 listov A3 – platne s rozmermi/operáciami, sústružené diely a listy rozmerových požiadaviek tvarových dielov. Pri tvarových dieloch nejde o kompletné GD&T výkresy.
- `drawing_data.json`, `Holes.csv`: súradnice otvorov šiestich základných platní; ďalšie operácie sú na výkresových listoch a v STEP. CSV nie je kompletný zoznam všetkých operácií celého stroja.
- `BOM.csv`: zoznam modelovaných komponentov; riadok je jeden kus, nie schválená nákupná objednávka.
- `vendor_manifest.json`: presne rozlišuje importovaný model a nedostupné originálne CAD.

Generovanie: `python3 -B cad/build_C5.py`, potom `python3 -B cad/draw_C5.py`. Potrebné CadQuery, reportlab, zdroje C3/C4 a pôvodný STEP rohovníka a KIPP v repozitári. Predchádzajúce STEP zostavy sa neprepisujú.

## Festo – stav originálnych modelov

Oficiálna verejná stránka poskytla katalóg [ADN 2026/09](https://www.festo.com/media/catalog/203981_documentation.pdf). Oficiálna CAD cesta pre položku536324 však po štandardnom anonymnom presmerovaní vrátila:

> CAD data is one of the benefits for our registered customers. Please login or create an account.

Agent nemá Festo prihlásenie. Originálne modely **neboli stiahnuté ani vložené**. Existujúce zjednodušené katalógové obálky nie sú premenované na originálne STEP. Na pokračovanie sa prihlásený používateľ môže dostať na export cez tieto oficiálne odkazy a poskytnúť STEP:

| Funkcia | Typ a číslo | Oficiálny CAD export |
|---|---|---|
| Lis | ADN-50-25-I-P-A, 536324 | [CAD536324](https://www.festo.com/eap/en_us/DKI3CAD2Fox/start.do?part=536324) |
| Rohovníky | ADN-16-30-I-P-A, 536231 | [CAD536231](https://www.festo.com/eap/en_us/DKI3CAD2Fox/start.do?part=536231) |
| Vidlička | ADN-16-70-I-P-A, 8178767 | [CAD8178767](https://www.festo.com/eap/en_us/DKI3CAD2Fox/start.do?part=8178767) |

Heslá ani tokeny sa nemajú posielať do četu. Potrebné sú exportované súbory, nie prihlasovacie údaje. Montážne rozteče a závity v podkladoch vychádzajú z katalógu str.17–19. Originálne STEP ešte musia potvrdiť piestnice, čelné osadenia, drážky, prípojky a montážne spoje.

## Pružinový prvok zo súboru používateľa

`models/vendor/kipp/k0309_212.stp` je nezmenený súbor používateľa (hlavička TraceParts); kontrolný súčet je v manifeste. Geometria má telo Ø12, osovú dĺžku tela22 a guličkuØ8. **Nebol to pôvodne uvažovaný M6×12.**

Model je otočený osou nahor zdola na stred rohovníka. Voľná guľa je nominálne dotyková na hrane otvoruØ5: stred guľôčky je Z=−3,1225, vrchol Z=+0,8775. Je to geometrické nastavenie bez predpätia; v skutočnosti treba nastaviť pružinu tak, aby gulička diel nezodvihla proti lište. Stav pružiny a sila sa zo STEP nedajú určiť.

D02 má Ø12,5 priechod. D03 je samostatný oceľový držiak so závitom **M12×1,75**, zatiaľ odvodeným z Ø12 a predpokladu štandardného metrického závitu; stúpanie a pružinová sila musia byť potvrdené katalógovým listom K0309.212. Overenie na stránke KIPP sa nepodarilo (HTTP503). D03 má spodnú prírubu60×60×10, horný výstupok30×30×15; základňa otvor32×32. Nastavenie je dostupné zdola. Zaistenie nízkopevnostným poistným prípravkom až po potvrdení závitu a výšky.

## Dokončené konštrukčné úpravy

1. **Mechanický doraz lisu bez vodiacich tyčí.** D05 je oceľová doska104×30×10 s voľným otvoromØ18 a dvoma dištanciamiD06 Ø12×26,30. D08 na nástroji má M16×1 a kontruje sa D09. V nominálnej polohe je spodné čelo D08 v Z47; dosadne na Z33,7 po pohybe13,3mm. OtvorØ18 nevedie driekØ16; sú to iba dorazové diely. Valec nesmie používať celý zdvih25mm proti dielu.
2. **Súosý nástroj.** Kovové medzikružieØ13,4 prenáša tlak na magnet. Prídržný magnetØ10×2 je v osadeníØ10,2 hĺbky2,1; nenesie sám celú lisovaciu silu. Spoj ADN50 je predbežne M10×1,5 L15 podľa KF/AF katalógu. Konečné osadenie a aretáciu potvrdiť s originálnym modelom; lepenie a polaritu prídržného magnetu zvoliť podľa skúšky.
3. **Vidlička aj spojka sú kontrolované spolu.** V C4 prechádzala horná časť spojky do pevnej oddeľovacej dosky. D13 sa preto upevňuje **zdola** dvoma M3×10. Stredový kanál šírky12 v podperách ju prepustí. Pod vidličkou sú oporné police; bočné klzné plochy majú vôľu0,2mm na stranu.
4. **Podpery D11 sú z jedného obrábateľného POM-C dielu**, nie fiktívny zlepenec dvoch materiálov. Základné rozmery136×12×30,2; presný profil v STEP. Horné M4 upevňujú oddeľovač, spodné M5 podpery k základni.
5. **Pevný oddeľovač D10:** Ø14,4, hrúbka3, spodná rovinaZ22,2. Kapsa vidličky má dnoZ16,9, teda priechod5,3mm pre magnet5mm. Skutočná tolerancia magnetov a povrch sa musia potvrdiť pred uzamknutím tejto medzery.
6. **Puzdro zásobníka:** doplnené dve ušká pre tangenciálne zvieraciu skrutkuM4. Samostatný stožiar sa nevrátil.
7. **Skrutky:** doplnené skrutky valca lisu, dorazu, pružinového držiaka, oddeľovača a spojky. Nie všetky skrutky starších podsústav sú dokončené; ich kontrola je otvorená.

## Rozmerové a povrchové požiadavky

- Všeobecné dĺžkové tolerancie: ISO2768-1m, ak nie je uvedené inak. Nejde o určenie všetkých geometrických tolerancií.
- Kovové dosadacie plochy Ra3,2, čelo lisovacieho nástroja Ra1,6; konečné spracovanie podľa dodávateľa.
- Rovinnosť stolaD02 a plochy pod valcomD04:0,05mm; základňa0,10mm. DištancieD06 dĺžka26,30±0,02 a rovnobežnosť čiel0,02.
- Hrany0,2, pri vedení magnetu0,15; bez otrepov a feromagnetických pilín.
- Závity v STEP sú valcové obálky alebo predvŕtania. Závitová operácia na výkrese je rozhodujúca; pilot nie je hotový priemer závitu.
- DXF je prierez v strede hrúbky. Neslúži sám na zhotovenie zapustení, závitov a stupňov. D01 má priechodnú kapsu32×32, prípustný vnútorný rádius doR3 pri vôli voči30×30 výstupku.
- Bežné skrutky predbežne trieda8.8, dotiahnutie podľa skutočného materiálu, mazania a výrobcu. Závity v POM overiť na vzorke; nevkladať všeobecné oceľové uťahovacie momenty.

## Orientačná kontrola dorazu – nenahrádza výpočet stroja

Pri predpokladaných6bar a Ø50 je sila1178N bez strát. Pre doskuD05 hrúbky10, rozpätie88 a konzervatívnu čistú šírku12 pri stredovom otvore vychádza jednoduchý nosníkový odhad I=1000mm4, M=25,9Nm, napätie≈130MPa. MateriálS355 má nominálnu medzu klzu355MPa pri tejto hrúbke. Odhad nezahŕňa koncentrácie napätí, kontakty, únavu, skrutkové spoje ani most/profily. **Nie je to schválenie nosnosti.** Pri inom tlaku alebo sile sa musí preveriť celý silový reťazec.

## Rozpočet taktu – cieľ10ks/min, nie overený výkon

| Čas s | Navrhnutá udalosť |
|---|---|
| 0–0,8 | Posun rohovníkov a mechanické zavretie bočného vstupu |
| 0,8–1,2 | Návrat posúvača, prítok ďalšieho dielu |
| 1,2–2,0 | Vidlička s magnetom k hlave |
| 2,0–2,2 | Prevzatie magnetu a potrebné uvoľnenie pre návrat vidličky |
| 2,2–3,0 | Vidlička späť pod zásobník |
| 3,0–3,6 | Lisovanie po nastaviteľný doraz |
| 3,6–4,0 | Výdrž podľa skúšky |
| 4,0–4,6 | Návrat hlavy |
| 4,6–6,0 | Rezerva, kontrola polôh a príprava nového cyklu |

Časy nie sú namerané. Predbežný výber prípojok: ADN50 G1/8, ADN16 M5 podľa katalógu. Prietoky, hadice, ventily a škrtenie určiť po potvrdení tlaku a reálnych časov. Riadenie musí čakať na potvrdenie odchodu vidličky a pripravenosti dielu pred pohybom lisu; časovač sám nie je potvrdenie polohy.

## Overené touto revíziou

- Platnosť vytvorených tvarov a spätné načítanie STEP.
- Šesť polôh **vidličky aj spodnej spojky** voči novej základni, pevnému oddeľovaču, podperám, mostu, stĺpom a dorazu.
- Nominálne dosadnutie nastavovacieho krúžku na mechanický doraz po13,3mm.
- Vloženie skutočného KIPP modelu bez prieniku s podperou, základňou a rohovníkom v referenčnej polohe.
- Výkresový PDF a DXF sú digitálne podklady; bez fyzického obrábania alebo montážnej skúšky.

## Otvorené body pre uvoľnenie do výroby

| ID | Bod | Prečo je potrebný |
|---|---|---|
| V01 | Originálne STEP troch Festo valcov | Overiť závitové spoje, priestor prípojok, osadenia, senzory a dodatočné kolízie |
| V02 | Skutočný tlak vzduchu a meranie lisovacej sily | Potvrdiť priemer valca, reguláciu a pevnosť rámu/spojov |
| V03 | Katalóg KIPP K0309.212 | Potvrdiť závit, pružinu, zdvih a prípustné nastavenie |
| V04 | Presný Bosch profil a katalógové spoje | Geometria je stále schematická45×45; M12 koncové spoje nie sú potvrdené |
| V05 | Magnet – tolerancie, materiál, polarita | Rozmer14×5 je potvrdený, výrobné tolerancie a sila pri oddeľovaní nie |
| V06 | Montážne spoje podsústav zoC4 | Dokončiť zvyšné uholníky, zaisťovanie a upevnenia valcov po vložení originálnych modelov |
| V07 | Reálna skúška gravitačného vstupu a oddelenia magnetu | Overiť spoľahlivé dávkovanie a takt10ks/min |
| V08 | Pneumatická schéma, snímače a riadenie | Nie sú implementované; treba definovať pred zhotovením ovládania |

Až po uzavretí bodov má zmysel odstrániť stavDRAFT a vystaviť kontrolované výrobné revízie. Táto revízia dáva konkrétne diely a výkresy na kontrolu; netvrdí, že všetky spoje a celý stroj sú už schválené na výrobu.
