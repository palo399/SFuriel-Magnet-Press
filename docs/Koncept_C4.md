# C4 – zjednodušenie podľa pripomienok

Vybraná otvorená vidlička C zostáva zachovaná. Magnet Ø14 × 5 mm. Nový návrh používa **tri valce**, bez oboch valcov Gate ADN, bez horných vodiacich tyčí a bez samostatného stožiara zásobníka. C3 zostáva zachovaná pre porovnanie.

## Rozhodnutia

**Lis priamo na ADN.** Horné vedenie a priečnik pohyblivej hlavy boli odstránené. Krátky súosý nástroj je priamo na piestnici ADN-50-25-I-P-A. Kruhový magnet nevyžaduje zaistenie uhlovej polohy. Kruhovosť však neodstraňuje bočné sily: riešenie platí pre presne súosý kontakt, overenie bočného zaťaženia piestnice a lisovacej sily zostáva nutné. Kovové medzikružie konca nástroja prenáša tlak, prídržný magnet je zapustený v strede a nemá prenášať celú lisovaciu silu sám.

**Bez valca závory magnetov.** Pod rúrkou je pevná oddeľovacia doska s otvorom Ø14,4. Jej spodná rovina Z=22,2 spolu s dnom kapsy Z=16,9 vytvára medzeru 5,3 mm pre jeden magnet. Pri vysunutí otvorenej vidličky zostáva ďalší magnet v kruhovom otvore pevnej dosky; plná časť vidličky podopiera zostávajúci stĺpec. Rúrka začína nad doskou a nemá priečnu štrbinu pre samostatnú závoru. Dve bočné podpery oddeľovacej dosky zároveň vedú vidličku s nominálnou bočnou vôľou 0,2 mm.

**Bez valca závory rohovníkov.** Tlačná pätka má bočné rameno a clonku. Počas 30mm posuvu clonka postupne uzavrie bočný prítok; pri návrate ho otvorí. Je to jeden tuhý pohyblivý diel ovládaný existujúcim ADN-16-30. Pravá lišta má predĺžené vstupné okno, aby do nej clonka nenarážala. Kinematiku prítoku na sklze treba prakticky vyskúšať, nejde zatiaľ o overený dávkovač.

**Bez samostatného stožiara.** „Profil mst 35“ bol interpretovaný ako predchádzajúci `BR_Magazine_mast`. Odstránený je celý tento profil, police aj uholníky. Zásobník je vedený cez otvor mosta a držaný 40 mm dlhým deleným puzdrom priskrutkovaným priamo k mostu. Priečny sťahovací spoj puzdra treba dopracovať. Rúrka má stále 300 mm aktívnu výšku. Ohyb a chvenie voľného konca rúrky nie sú vypočítané.

**Nižší hlavný rám.** Zostali len dve hlavné profilové stojky Bosch 45 × 45, drážka 10; dĺžka skrátená na 68 mm. Most je v Z=60..75. Sú to schematické profily ako v C3, konkrétne objednávacie číslo a koncový spoj M12 treba potvrdiť. Priechodná lišta a zalomený vstup zostali zachované. Pružinová skrutka zostáva kolmo zdola na strede rohovníka.

## Pohony

| Funkcia | Festo | Objednávacie číslo |
|---|---|---|
| Lis | ADN-50-25-I-P-A | 536324 |
| Posun rohovníkov | ADN-16-30-I-P-A | 536231 |
| Vidlička | ADN-16-70-I-P-A | 8178767 |

Zdroj rozmerov a čísiel je [oficiálny katalóg Festo ADN 2026/09](https://www.festo.com/media/catalog/203981_documentation.pdf), rovnako ako pri C3. Modely sú katalógové obálky, nie originálne Festo CAD. Pracovný posuv vidličky je 65 mm; valec 70 mm potrebuje nastaviteľné dorazy.

## Predbežný cyklus
1. Posúvač rohovníkov vzadu: otvorený bočný vstup pustí jeden diel do rohu lišty.
2. Posúvač ide dopredu, uzavrie bočný vstup a posunie radu k lisu. Pružinová skrutka pod lisom pomáha usadiť diel.
3. Otvorená vidlička oddelí jeden magnet spod stĺpca; pevná doska zastaví ďalší magnet.
4. Vidlička dopraví magnet k hlave; hlava ho pritiahne. Vidlička sa musí vrátiť úplne mimo osi lisovania.
5. ADN zalisuje magnet. Hlava sa vráti; hotový diel sa pri ďalšom posuve posunie po výstupnej lište.

Nominálny krok 30 mm treba doladiť podľa vôlí v rade. Rozmery rohovníka sú približne 29 mm; tlak v rade a gulička nesmú byť bez skúšky považované za presné pozdĺžne polohovanie.

## Súbory a overenie

- `Rohovnik_press_C4_simple.step`: kompletná zostava.
- Samostatné STEP novej základne, mosta, nástroja, pevného oddeľovača, puzdra a prepojeného posúvača.
- `BOM_C4.csv`, `Mounting_holes_C4.csv`: položky a otvory novej základne/mosta v súradniciach zostavy; mm.
- `Assembly_C4.png`, `Plan_C4.png`: náhľady.
- `cad/build_C4.py`: parametrický zdroj využívajúci predchádzajúce zdroje bez prepisovania ich výstupov.

Overenie: platná geometria komponentov a spätný import STEP; päť polôh vidličky voči pevnému oddeľovaču a jeho podperám; tri polohy clonky voči lištám; tri polohy rohovníka na výstupe voči lištám a stĺpom. Tieto kontroly neznamenajú overenie všetkých kolízií alebo celého dynamického cyklu. Magnetické sily a podávanie stĺpca nie sú simulované.

## Otvorené pred výrobou

Lisovacia sila a tlak vzduchu sú stále neznáme. ADN-50 pri 6 bar teoreticky dáva 1,18 kN bez strát; nie je preukázané, že je to správna sila. Pri zvolenej výške hlavy vychádza pracovný pohyb k dosadacej rovine približne 13,3 mm, **nie celý zdvih 25 mm**. Nastaviteľné mechanické obmedzenie zdvihu treba doplniť pred skúškou lisu; v C4 nie je definitívny doraz vymodelovaný. Samotné škrtenie rýchlosti nenahrádza doraz.

Treba dopracovať závit a aretáciu vymeniteľného nástroja, sťahovací spoj puzdra rúrky, finálne závitové spoje, skrutky a prípojky. Pružinová skrutka M6 má stále predbežnú guličku Ø5,5 proti stredovému otvoru približne Ø5; výber katalógového dielu nie je potvrdený. Overiť vytrhnutie magnetu zo stĺpca, jeho odovzdanie hlave, polaritu a súčasne návrat vidličky pred lisovaním. Táto verzia je koncept na posúdenie jednoduchšej architektúry, nie podklad na okamžitú výrobu.
