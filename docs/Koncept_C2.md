# C2 – priechodná lišta a zalomený vstup

Vybraný podávač magnetov C: vidlička a samostatná uzávierka. Nová zostava: `models/concept-C2/C_fork.step`. Predošlé verzie zostávajú zachované.

## Úpravy podľa zadania
- Odstránený diel `Rear_column`; rám má namiesto neho dva bočné stĺpy mimo dráhy rohovníkov a horný most.
- Lišta je priechodná cez lis až po výstup v zápornom smere Y. Odstránený aj pôvodný koncový doraz, ktorý by výstup blokoval.
- Pružinová skrutka M6 × 12 je v osi Z zdola na strede dielu (X=Y=0). Podpera má otvor pre závit a základňa prístupový otvor zdola. Bočný kolík bol odstránený. Gulička je iba geometrická obálka Ø5,5 mm, nie potvrdený katalógový diel. Dodaný model má na osi otvor približne Ø5 mm: menšia gulička by doň vošla bez zachytenia; pred výberom skrutky treba overiť skutočný priemer a zdvih guličky.
- Diely sú výškovo opravené na dosadnutie spodnou plochou na Z=0; predchádzajúca zostava mala nesprávny výškový posun +9,5 mm.
- Horné pridržovacie úkosy sú zachované. Pravá lišta má pri vstupe otvor pre rohovník.
- Vstup je zalomený o 90° v pôdoryse: sklz prichádza z boku (+X) do rovnej prijímacej zóny pri Y=90 mm. Za ňou sa diel posúva smerom -Y pod lis.
- V osi lišty je separačný valec s tlačnou pätkou. Pracovný predpoklad je krok 30 mm. Valec je zobrazený zasunutý; ide o geometrickú obálku bez výberu katalógového modelu.
- Samostatná vstupná závora zadrží ďalší diel počas posuvu. Zobrazená je zdvihnutá; jej ovládanie treba doladiť. Samotný tlačný valec by prítok z bočného sklzu nezadržal.

## Predbežný cyklus
1. Pätka je vzadu, vstupná závora otvorená; rohovník príde z boku do prijímacej zóny.
2. Závora sa zatvorí a zadrží nasledujúci diel na sklze.
3. Valec posunie rad rohovníkov o jeden krok smerom k lisu; hotový kus odchádza po pokračujúcej lište.
4. Pätka sa vráti. Podávač C odovzdá magnet hlave a ustúpi pred lisovaním.
5. Po lisovaní a návrate hlavy možno opakovať cyklus.

Krok 30 mm a tri polohy čakania sú koncept. Presnú polohu rohovníka pod lisom bude potrebné riešiť výsuvným dorazom alebo presným indexovaním; Zvislá M6 pružinová gulička sama nesmie byť jediným pozdĺžnym dorazom. Finálne ovládanie a snímanie zatiaľ nie sú navrhnuté.

## Overenie a hranice
Overená platnosť STEP spätným importom. Overený prienik dodaného rohovníka s pridržovacími lištami a bočnými stĺpmi/mostom v troch polohách na výstupe; bez objemových kolízií. Nie je to overenie celého cyklu, prechodu rohom, separácie ani pohonov. Hrúbka magnetu 3 mm a jeho priemer 14 mm sú stále pracovný predpoklad. Žiadna výrobná pripravenosť sa netvrdí.
