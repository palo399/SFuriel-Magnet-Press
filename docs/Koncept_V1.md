# Rohovnik magnet – koncept lisu V1

STEP: `models/concept-v1/Rohovnik_magnet_press_V1.step`
Zdroj: `cad/build_concept.py` (Python + CadQuery; spustiť z koreňa repozitára).
Jednotky: mm. Os Z je zvislá; diely postupujú po Y smerom k nule. Lis je na X=Y=0.

## Zahrnuté
- Originálny dodaný rohovník 29 × 29 × 9,5 mm otočený dutinou nahor.
- Vodiace lišty s horným úkosom a predbežnou vôľou 0,3 mm nad okrajom dielu.
- Sklz so sklonom 25°, čakanie dielov, obálky separátora a posúvača.
- Pevný doraz, obálka pružinového kolíka M6 × 12 a gulička.
- Rám lisu, vodiace stĺpiky, zdvihnutá hlava s prídržným magnetom.
- Bočný podávač magnetov, kapsa a rúrkový zásobník s aktívnou výškou 300 mm.

## Pracovné predpoklady
Magnet Ø14 × 3 mm; priemer vychádza z kruhovej dutiny dodaného dielu, hrúbka nie je potvrdená. Vnútorný priemer zásobníka 14,4 mm, kapsa 14,3 mm. Zdvih podávača 65 mm. Uvedené vôle a zdvihy sú východiskové hodnoty, nie výrobné tolerancie.

Zostava zobrazuje koncepčné polohy: hlava drží magnet a podávač je pri zásobníku. Päť magnetov v zásobníku ilustruje stĺpec; nejde o plnú náplň. Existujúci schodíkový zásobník nie je súčasťou návrhu, iba jeho nadväzujúci sklz.

## Ďalšie rozpracovanie
Separátor, pohony, kolík a úchyt hlavy sú geometrické obálky, nie presné katalógové súčiastky. Dopracovať kinematiku dvojitého dorazu, polohu zachytenia magnetu, výstup hotového dielu, upevňovacie otvory, snímače a blokovanie pohybov. Návrat podávača musí byť dokončený pred lisovaním. Pružinová gulička pritláča diel k pevnému vedeniu, neurčuje sama jeho presnú polohu.

Toto je rozvojový 3D koncept, nie výrobná dokumentácia. Platnosť STEP geometrie a spätný import boli overené; kolízna kontrola celého cyklu, sily lisu, tuhosť a bezpečnostné krytovanie zatiaľ nie.
