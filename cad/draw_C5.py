"""A3 PDF prototype drawings, mm coordinates. Inputs from build_C5.py.
All sheets remain DRAFT until the review items in docs/Manufacturing_C5.md close.
"""
from pathlib import Path
import json,math,textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1];O=R/'models/manufacturing-C5';O.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
c=canvas.Canvas(str(O/'C5_Drawings_DRAFT.pdf'),pagesize=landscape(A3));W,H=landscape(A3);page=0
c.setTitle('C5 Rohovnik magnet - prototype manufacturing draft')
def txt(x,y,s,size=9):c.setFont('DV',size);c.drawString(x,y,str(s))
def header(name,material,notes=''):
 global page
 page+=1;c.setStrokeColorRGB(0,0,0);c.setFillColorRGB(0,0,0);c.setLineWidth(.6);c.rect(20,20,W-40,H-40)
 txt(40,H-45,name,16);txt(40,H-65,'Materiál: '+material,10)
 c.setFillColorRGB(.7,.08,.08);txt(W-355,H-45,'NÁVRH PROTOTYPU — NEUVOĽNENÉ',11);c.setFillColorRGB(0,0,0)
 txt(40,55,'Jednotky mm | Netolerované rozmery ISO 2768-1 m | Hrany odhrotovať 0,2 | Závity sú schematické',8)
 txt(40,39,'C5 | Kontrola Festo CAD, tlaku a lisovacej sily otvorená | Výkres č. '+str(page),8)
 for i,l in enumerate(textwrap.wrap(notes,170)):txt(40,95+13*i,l,8)
def dim(x1,y1,x2,y2,label):
 c.setLineWidth(.4);c.line(x1,y1,x2,y2)
 angle=math.atan2(y2-y1,x2-x1)
 for x,y,a in [(x1,y1,angle),(x2,y2,angle+math.pi)]:
  for off in [-.45,.45]:c.line(x,y,x+6*math.cos(a+off),y+6*math.sin(a+off))
 c.saveState();c.translate((x1+x2)/2,(y1+y2)/2);c.rotate(angle*180/math.pi);c.setFont('DV',9);c.drawCentredString(0,5,str(label));c.restoreState()
def hole_table(rows,x=790,y=H-115):
 widths=[28,44,44,43,200];xs=[x]
 for w in widths:xs.append(xs[-1]+w)
 for j,v in enumerate(['Č.','X','Y','Ø','Operácia']):txt(xs[j]+3,y,v,8)
 y-=15
 for i,(xx,yy,dd,op) in enumerate(rows):
  lines=textwrap.wrap(op,35) or [''];rh=max(16,11*len(lines)+4)
  if y-rh<125:txt(x,y,'Úplné operácie: pozri Holes.csv a dokumentáciu.',7);break
  vals=[str(i+1),f'{xx:g}',f'{yy:g}',f'{dd:g}']
  for j,v in enumerate(vals):txt(xs[j]+3,y,v,7)
  for k,v in enumerate(lines):txt(xs[4]+3,y-k*11,v,7)
  c.line(x,y+10,xs[-1],y+10);y-=rh
for d in json.loads((O/'drawing_data.json').read_text()):
 header(d['name'],d['material'],d.get('notes',''))
 w,h,t=d['w'],d['h'],d['t'];sc=min(575/w,490/h,8);ox=120;oy=160
 c.rect(ox,oy,w*sc,h*sc);txt(ox,oy+h*sc+18,'PÔDORYS — počiatok X0/Y0 v ľavom dolnom rohu',9)
 for i,(x,y,diam,op) in enumerate(d['holes']):
  xx=ox+x*sc;yy=oy+y*sc;c.circle(xx,yy,diam/2*sc);c.setLineWidth(.3)
  c.line(xx-5,yy,xx+5,yy);c.line(xx,yy-5,xx,yy+5);txt(xx+diam/2*sc+2,yy+2,'H'+str(i+1),6)
 if 'pocket' in d:
  x,y,pw,ph=d['pocket'];c.rect(ox+x*sc,oy+y*sc,pw*sc,ph*sc);txt(ox+x*sc,oy+(y+ph)*sc+5,'32 × 32 PRIECHOZÍ',7)
 if d['name']=='D03_Plunger_block':
  c.setDash(5,3);c.rect(ox+15*sc,oy+15*sc,30*sc,30*sc);c.setDash();txt(ox+15*sc,oy+45*sc+7,'Výstupok 30 × 30, výška15',8)
 if d['name']=='D05_Stop_plate':
  c.setDash(3,2)
  for x in [8,96]:c.circle(ox+x*sc,oy+15*sc,5.5*sc)
  c.setDash()
 dim(ox,oy-25,ox+w*sc,oy-25,f'{w:g}')
 dim(ox-30,oy,ox-30,oy+h*sc,f'{h:g}')
 txt(ox,oy-55,f'Hrúbka: {t:g} mm. Modelovaný priemer závitu je predvŕtanie.',9)
 hole_table(d['holes']);c.showPage()
# Turned and stepped parts: explicit axial stations and hole notes.
turned=[
 ('D06_Stop_spacer','Steel C45',26.3,[(0,12),(26.3,12)],['2 kusy','Dĺžka26,30 ±0,02; čelá rovnobežnosť0,02','Oba konce M6×1-6H, plný závit10; vrtákØ5 hĺbka11,5','Stred musí zostať plný; nekombinovať dva hlboké závity']),
 ('D07_Press_tool','Steel C45',60.3,[(0,13.4),(12,13.4),(12,16),(45.3,16),(45.3,10),(60.3,10)],['1 kus; súososť konca a upínacieho drieku0,03','Z0: Ø10,2 +0,03/0, hĺbka2,1 pre prídržný magnetØ10×2','Z18..34: vonkajší M16×1-6g pre dorazové krúžky','Z45,3..60,3: vonkajší M10×1,5-6g L15; overiť na originálnom ADN','Kovové medzikružie na Z0 prenáša lisovaciu silu; magnet je zapustený']),
 ('D08_Adjust_ring','Steel C45',5,[(0,28),(5,28)],['1 kus; vnútorný M16×1-6H priechozí','2×Ø3 priechozí na rozstupovej kružniciØ22 pre kolíkový kľúč','Nastavenie v zostave: dolné čelo Z47, horné Z52 pred lisovaním']),
 ('D09_Lock_ring','Steel C45',4,[(0,28),(4,28)],['1 kus; vnútorný M16×1-6H priechozí','2×Ø3 priechozí na rozstupovej kružniciØ22','Kontruje nastavovací krúžok; poloha Z52..56']),
]
for name,mat,L,stations,notes in turned:
 header(name,mat,'SÚSTRUŽENÝ DIEL; absolútne Z v poznámkach je poloha v zostave.')
 sc=min(650/L,10);ox=160;cy=420
 points=[(ox,cy)]+[(ox+z*sc,cy+dia/2*sc) for z,dia in stations]+[(ox+L*sc,cy)]+[(ox+z*sc,cy-dia/2*sc) for z,dia in reversed(stations)]
 p=c.beginPath();p.moveTo(*points[0])
 for xy in points[1:]:p.lineTo(*xy)
 p.close();c.drawPath(p)
 c.setDash(6,3);c.line(ox-30,cy,ox+L*sc+30,cy);c.setDash()
 dim(ox,cy-170,ox+L*sc,cy-170,f'{L:g}')
 for j,(z,di) in enumerate(stations):
  if j==0 or stations[j-1][1]!=di:txt(ox+z*sc+3,cy+di/2*sc+18,'Ø'+f'{di:g}',9)
 for i,t in enumerate(notes):txt(70,H-140-19*i,t,11)
 c.showPage()
# Remaining stepped parts: controlled dimensions plus neutral 3D reference.
items=[
 ('D11_Carrier_support','POM-C', ['2 zrkadlové kusy; dĺžka136, výška30,20 ±0,02; kompletný profil v STEP','Zostava: X24..160; vonkajšie boky Y±18; základný pás šírky6','Spodná oporná polica: Z12..15; vnútorný okraj Y±6','Bočné vedenie: vnútorné plochy Y±11,2, výška Z15..22,2','Zo spodku 3×M5, hĺbka10, polohy X35/100/150, Y±15','Zhora 2×M4, hĺbka10, polohy X53/77, Y±15','Nominálna bočná vôľa vidličky0,2 na stranu; doladiť po skúške']),
 ('D12_Carrier_14x5','POM-C',['Obálka95×22×7; začiatok zostavy X−11,Y−11,Z15','KapsaØ14,30 +0,05/0, hĺbka5,10 +0,03/0 otvorená smerom−X','Dno kapsy Z16,9; celková horná plochaZ22','2×M3×0,5 priechozí; osi zostavy X72/79,Y0','Otvorená štrbina šírky14,3; ostré hrany zraziť0,15','Presný tvar otvorenia a prechody v samostatnom STEP']),
 ('D13_Under_carrier_link','Aluminium6082-T6',['Spodná platňa26×10×6 v zostave X68..94,Y−5..5,Z9..15','Výstupok10×10×14, X84..94,Y−5..5,Z9..23','2×Ø3,4 priechozí zospodu; osi zostavyX72/79,Y0','Os piestniceZ18,5,Y0; otvor pozdĺžX: M6×1, predvŕtanieØ5','Spoj vidličky:2×M3×10 zospodu; závit v POM vidličke','Závit a dĺžku spojovacej tyčky potvrdiť s originálnym Festo modelom']),
 ('D14_Tube_collar','Aluminium6082-T6',['Príruba34×34×8, dolné čeloZ75; stredX65,Y0','Vodiace puzdroØ26×40, vnútornýØ20,30 +0,05/0','4×Ø4,5 v štvorci26×26 okolo osi zásobníka','Deliaca štrbina šírky1; dve ušká pre zvieraciu M4 skrutku','Ľavé uškoØ4,5, pravé M4×0,7; os X, zostavaY16,Z95','Presný tvar ušiek v STEP; skrutku doťahovať po skúške rúrky']),
]
for name,mat,notes in items:
 header(name,mat,'TVAROVÝ DIEL — súradnice v poznámkach sú v zostave, nie v rohu polotovaru.')
 for i,t in enumerate(notes):txt(60,H-130-28*i,t,12)
 txt(60,220,'Podklad: samostatný STEP v parts/. Táto stránka nie je úplný GD&T výkres.',11)
 txt(60,195,'Pred obrábaním overiť všetky pohľady a prístup nástroja; stav zostáva DRAFT.',11)
 c.showPage()
header('Montáž a kontrola — 10 ks/min','Zostava C5','Nominálny cyklus6s. Časy sú návrhový rozpočet, nie výsledok skúšky.')
notes=['1. Zmontovať základňu, lištu a dve profilové stojky; overiť voľný priechod dielu.',
'2. KIPP zospodu nastaviť na dotyk s otvorom; nesmie dvíhať diel proti úkosu.',
'3. Zmontovať pevný oddeľovač a podávač; vyskúšať ručne so stĺpcom magnetov.',
'4. Originálne Festo STEP ešte chýbajú. Neuvoľniť montážne otvory bez overenia.',
'5. Lis najprv bez tlaku ručne nastaviť: krúžok Z47 -> doraz Z33,7, pohyb13,3.',
'6. Overiť na reálnom dielci dosadnutie magnetu; nenastavovať plný zdvih25.',
'7. Skúšku s tlakom vykonať až po meraní sily a kontrole mechanického dorazu.',
'8. Overiť, že vidlička je mimo osi pred lisovaním; snímače a riadenie ešte dopracovať.',
'9. Až potom merať takt a doladiť rozpočet6s; cieľ10ks/min nie je overený výkon.']
for i,t in enumerate(notes):txt(55,H-140-35*i,t,12)
c.showPage();c.save();print('PDF sheets',page)
