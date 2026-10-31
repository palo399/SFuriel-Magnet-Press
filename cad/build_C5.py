"""C5 prototype manufacturing development. Not released for production.
Run from repository root. Original KIPP STEP is preserved; Festo CAD unavailable.
"""
from pathlib import Path
import cadquery as cq
import csv,re,json,hashlib,math
R=Path(__file__).resolve().parents[1];O=R/'models'/'manufacturing-C5';P=O/'parts';P.mkdir(parents=True,exist_ok=True)
g={'__file__':str(R/'cad/build_C4.py')}
src=(R/'cad/build_C4.py').read_text().split('# Export STEP and tabular design data.')[0]
exec(compile(src,str(R/'cad/build_C4.py'),'exec'),g)
old=g['parts'];box,cyl=g['box'],g['cyl']; A=cq.Assembly(name='C5_prototype_draft');parts={};bom=[];holes=[];drawings=[]
def add(n,s,material='Steel',note='',color=(.65,.69,.73)):
 assert s.val().isValid(),n
 A.add(s,name=n,color=cq.Color(*color));parts[n]=s;bom.append([n,material,note])
remove=('C4_Base','C4_Bridge','Short_coaxial','M6_vertical','Plunger_ball','Stripper_side','Fixed_magnet_stripper','C_fork','Fork_coupling','P02_Track','Tube_split')
for n,s in old.items():
 if not n.startswith(remove):add(n,s,'Reused C4','Dimensioned interfaces pending original vendor CAD' if n.startswith('Festo') else '')
# Drilled flat parts: drawing coordinates are local lower-left XY, bottom Z0.
def plate(n,w,h,t,hs,pos,material,slots=(),notes=''):
 s=box(0,0,0,w,h,t)
 for x,y,diam,op in hs:
  assert 0<x-diam/2 and x+diam/2<w and 0<y-diam/2 and y+diam/2<h,(n,x,y)
  s=s.cut(cyl(x,y,-1,diam/2,t+2));holes.append([n,x,y,diam,op,t])
 for x,y,l,di in slots:
  s=s.cut(cq.Workplane('XY').center(x,y).slot2D(l,di,90).extrude(t+2).translate((0,0,-1)))
  holes.append([n,x,y,di,'SLOT Y L'+str(l),t])
 cq.exporters.export(s,str(P/(n+'.step')));cq.exporters.export(s.section(t/2),str(P/(n+'.dxf')))
 drawings.append(dict(name=n,w=w,h=h,t=t,holes=hs,material=material,notes=notes))
 add(n,s.translate(pos),material,notes);return s
# Exact supplied KIPP geometry, vertical from below. Set nominal seating on hole rim.
raw=cq.importers.importStep(str(R/'models/vendor/kipp/k0309_212.stp'))
contact_center=-math.sqrt(4**2-2.5**2)
shift=contact_center-20.5
kipp=raw.rotate((0,0,0),(1,0,0),90).translate((0,0,shift))
add('KIPP_K0309_212_ORIGINAL',kipp,'User supplied TraceParts STEP','Body D12 L22; ball D8; nominal free sphere tangent to D5 mouth',(.74,.6,.25))
# Base includes access pocket for flange-mounted plunger block and remaining mounts.
bh=[(x+145,y+155,di,'M6 TAP THROUGH' if di==5 else 'CLEAR') for x,y,di in g['base_holes'] if not (x==0 and y==0)]
bh += [(x+145,y+155,5,'M6 TAP THROUGH plunger flange') for x in [-22,22] for y in [-22,22]]
bh += [(x+145,y+155,5.5,'M5 guide fixing from below') for x in [35,100,150] for y in [-15,15]]
plate('D01_Base',500,400,15,bh,(-145,-155,-23),'Aluminium 6082-T6',notes='Central32x32 through pocket; flatness0.10 datum top; deburr0.2')
base=parts['D01_Base'].cut(box(-16,-16,-24,32,32,17));A.remove('D01_Base');parts.pop('D01_Base');add('D01_Base',base,'Aluminium6082-T6','Central pocket32x32 assembly XY[-16,+16]')
# Update individual STEP and drawing pocket.
cq.exporters.export(base.translate((145,155,23)),str(P/'D01_Base.step'))
cq.exporters.export(base.translate((145,155,23)).section(7.5),str(P/'D01_Base.dxf'))
drawings[-1]['pocket']=(129,139,32,32)
# Track: M12 hardware needs clearance, not old M6 thread.
th=[(23,140,12.5,'KIPP body clearance')]
th += [(x+23,y+140,3.3,'M4 TAP THROUGH') for x in [-19,19] for y in [-125,-75,-25,25,65]]
th += [(x+23,y+140,5,'M6 TAP THROUGH from underside') for x in [-19,19] for y in [-100,50]]
plate('D02_Track_bed',46,250,8,th,(-23,-140,-8),'Aluminium6082-T6',notes='Top Z0; flatness0.05; no thread in central hole')
# Actual plunger block: flange fits under base; boss in square base pocket.
block=box(-30,-30,-33,60,60,10).union(box(-15,-15,-23,30,30,15)).cut(cyl(0,0,-34,5.1,27))
for x in [-22,22]:
 for y in [-22,22]:block=block.cut(cyl(x,y,-34,3.3,12))
add('D03_Plunger_block',block,'Steel C45','M12x1.75-6H through; flange M6 clearance6.6; setting access from below')
cq.exporters.export(block.translate((30,30,33)),str(P/'D03_Plunger_block.step'))
drawings.append(dict(name='D03_Plunger_block',w=60,h=60,t=25,holes=[(30,30,10.2,'M12x1.75 TAP THROUGH')]+[(x+30,y+30,6.6,'M6 clearance') for x in [-22,22] for y in [-22,22]],material='Steel C45',notes='Flange10; boss30x30x15 centred; drawing shows plan; use STEP for steps. Low-strength thread locking after adjustment.'))
# Bridge with two support screws for non-guiding travel stop.
bridgeholes=g['bridge_holes']+[(44,0,6.6),(-44,0,6.6)]
plate('D04_Bridge',220,140,15,[(x+110,y+90,di,'CLEAR; ADN face TG46.5 where applicable') for x,y,di in bridgeholes],(-110,-90,60),'Steel S355',notes='Top Z75; flatness0.05 cylinder seat')
# End stop structure, no guidance fit. Top at Z33.7; punch collar reaches it after13.3mm.
plate('D05_Stop_plate',104,30,10,[(52,15,18,'TOOL clearance; NO guide fit'),(8,15,6.6,'M6 clearance'),(96,15,6.6,'M6 clearance')],(-52,-15,23.7),'Steel S355',notes='D11 counterbores depth6 FROM BOTTOM at X8,96 Y15; top Z33.7')
stop=parts['D05_Stop_plate']
for x in [-44,44]:stop=stop.cut(cyl(x,0,23.6,5.5,6.1))
A.remove('D05_Stop_plate');parts.pop('D05_Stop_plate');add('D05_Stop_plate',stop,'SteelS355','Counterbore from bottom; top Z33.7')
cq.exporters.export(stop.translate((52,15,-23.7)),str(P/'D05_Stop_plate.step'))
cq.exporters.export(stop.translate((52,15,-23.7)).section(5),str(P/'D05_Stop_plate.dxf'))
# Custom spacers, both ends tapped M6 10mm, fixed stop suspended from bridge.
for x in [-44,44]:
 spacer=cyl(x,0,33.7,6,26.3).cut(cyl(x,0,33.6,2.5,10.1)).cut(cyl(x,0,50,2.5,10.1))
 add('D06_Stop_spacer_'+str(x),spacer,'SteelC45','D12 L26.30 +/-0.02; M6x1-6H depth10 each end')
# Short coaxial tool with M10 connection and M16x1 adjustment section (threads schematic).
tool=cyl(0,0,22,6.7,12).union(cyl(0,0,34,8,33.3)).union(cyl(0,0,67.3,5,15)).cut(cyl(0,0,21.9,5.1,2.2))
add('D07_Press_tool',tool,'SteelC45','Tip D13.4; pickup bore10.2 depth2.1; M16x1 from Z40..56; M10x1.5 male L15 at Z67.3; thread geometry schematic')
for n,z,t in [('D08_Adjust_ring',47,5),('D09_Lock_ring',52,4)]:
 ring=cyl(0,0,z,14,t).cut(cyl(0,0,z-1,7.5,t+2))
 for x in [-11,11]:ring=ring.cut(cyl(x,0,z-1,1.5,t+2))
 add(n,ring,'SteelC45','D28; M16x1-6H; pin-spanner2xD3 PCD22')
# Improve fixed stripper support + combined running guides with a centre slot for linkage.
stripholes=[(x-50,y+18,4.5,'M4 clearance') for x in [53,77] for y in [-15,15]]+[(15,18,14.4,'Magazine bore +0.02 /0')]
plate('D10_Fixed_stripper',30,36,3,stripholes,(50,-18,22.2),'POM-C',notes='Underside22.2; carrier pocket floor16.9 => gap5.3; magnet tolerance unknown')
for y in [-18,12]:
 side=box(24,y,-8,136,6,30.2)
 # Inward lower shelf supports carrier, leaving central12mm linkage channel.
 side=side.union(box(24,-12 if y<0 else 6,12,136,6,3))
 side=side.union(box(24,-12 if y<0 else 11.2,15,136,.8,7.2))
 yc=-15 if y<0 else 15
 for x in [35,100,150]:side=side.cut(cyl(x,yc,-9,2.1,11))
 for x in [53,77]:side=side.cut(cyl(x,yc,12.2,1.65,11))
 add('D11_Carrier_support_'+str(y),side,'POM-C','Base M5 depth10; stripper M4 depth10; guide gap22.4; runner top15.0')
# Carrier and UNDER-mounted link. Avoid the C4 upper coupling colliding with stripper.
fork=old['C_fork_14x5']
for x in [72,79]:fork=fork.cut(cyl(x,0,14,1.25,9)) # M3 pilot D2.5
add('D12_Carrier_14x5',fork,'POM-C','Open pocket D14.3 +0.05; floor16.9; 2xM3 TAP through at72,79 Y0')
link=box(68,-5,9,26,10,6).union(box(84,-5,9,10,10,14))
for x in [72,79]:link=link.cut(cyl(x,0,8,1.7,8))
link=link.cut(cq.Workplane('YZ').circle(2.5).extrude(11).translate((83.5,0,18.5)))
add('D13_Under_carrier_link',link,'Aluminium6082','M3x10 from below to carrier; M6 threaded linkage bore alongX; link below carrier')
# Tube split collar with tangential pinch screw in two lugs.
collar=old['Tube_split_collar_on_bridge']
lugs=box(60,10,91,4.5,12,8).union(box(65.5,10,91,4.5,12,8))
# Horizontal pinch bore alongX. M4 clearance left, M4 tap pilot right; no stem changes.
lugs=lugs.cut(cq.Workplane('YZ').circle(2.25).extrude(5.5).translate((59,16,95)))
lugs=lugs.cut(cq.Workplane('YZ').circle(1.65).extrude(5.5).translate((65,16,95)))
add('D14_Tube_collar',collar.union(lugs),'Aluminium6082','M4 pinch clamp across split; D20.3 bore; fourM4 mounting holes')
# Bolts at completed critical interfaces, simplified envelope no helical threads.
def bolt(n,x,y,z,d,L,axis='Z'):
 s=cyl(0,0,0,d/2,L).union(cyl(0,0,-d,.85*d,d))
 if axis=='-Z':s=s.rotate((0,0,0),(1,0,0),180)
 if axis=='X':s=s.rotate((0,0,0),(0,1,0),90)
 add(n,s.translate((x,y,z)),'Fastener','ISO4762 M'+str(d)+'x'+str(L)+'; schematic')
for x in [-23.25,23.25]:
 for y in [-23.25,23.25]:bolt('B_PRESS_'+str(x)+'_'+str(y),x,y,60,8,25)
for x in [-44,44]:
 bolt('B_STOP_upper_'+str(x),x,0,75,6,25,'-Z')
 bolt('B_STOP_lower_'+str(x),x,0,29.7,6,12)
for x in [-22,22]:
 for y in [-22,22]:bolt('B_PLUNGER_'+str(x)+'_'+str(y),x,y,-33,6,20)
for x in [53,77]:
 for y in [-15,15]:bolt('B_STRIP_'+str(x)+'_'+str(y),x,y,25.2,4,12,'-Z')
for x in [35,100,150]:
 for y in [-15,15]:bolt('B_CARRIER_BASE_'+str(x)+'_'+str(y),x,y,-23,5,25)
for x in [72,79]:bolt('B_CARRIER_LINK_'+str(x),x,0,9,3,10)
# Data and neutral exports.
for n in parts:
 if n.startswith('D') and n not in ['D01_Base','D02_Track_bed','D03_Plunger_block','D04_Bridge','D05_Stop_plate','D10_Fixed_stripper']:cq.exporters.export(parts[n],str(P/(n+'.step')))
A.save(str(O/'Rohovnik_press_C5_prototype_DRAFT.step'))
with (O/'BOM.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Item','Material','Specification']);w.writerows(bom)
with (O/'Holes.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Part','LocalX','LocalY','Diameter','Operation','Thickness']);w.writerows(holes)
(O/'drawing_data.json').write_text(json.dumps(drawings,indent=2))
# Verify carrier + under-link, not just fork, against fixed structures throughout transfer.
obstacles=[s.val() for n,s in parts.items() if n.startswith(('D10','D11','D01','D04','D05','D06','BR_'))]
for dx in [0,13,26,39,52,65]:
 for name in ['D12_Carrier_14x5','D13_Under_carrier_link']:
  moving=parts[name].translate((dx,0,0)).val()
  for obstacle in obstacles:assert moving.intersect(obstacle).Volume()<1e-5,(name,dx)
# At 13.3mm the adjustable collar seats on stop without penetrating it.
ring=parts['D08_Adjust_ring'].translate((0,0,-13.3)).val()
assert ring.intersect(parts['D05_Stop_plate'].val()).Volume()<1e-5
assert abs(ring.BoundingBox().zmin-33.7)<1e-5
assert kipp.val().intersect(parts['Workpiece_at_press_C2'].val()).Volume()<1e-5, 'KIPP workpiece seating'
# KIPP reference model must not significantly penetrate workpiece or surrounding support.
for n in ['D02_Track_bed','D01_Base']:
 assert kipp.val().intersect(parts[n].val()).Volume()<1e-5,('KIPP clearance',n)
read=cq.importers.importStep(str(O/'Rohovnik_press_C5_prototype_DRAFT.step'));assert read.val().isValid()
print('PASS C5',len(parts),'components; STEP readback; 6 carrier+link positions; stop seating; KIPP mounting clearance')
from cadquery.occ_impl.exporters import svg
from OCP.gp import gp_Dir
frame=svg.gp_Ax2;svg.gp_Ax2=lambda p,d:frame(p,d,gp_Dir(1,1,0))
try:cq.exporters.export(read,str(O/'Assembly_C5.svg'),opt={'width':1400,'height':1000,'projectionDir':(1,-1,1.3),'showHidden':False,'strokeWidth':.4})
finally:svg.gp_Ax2=frame
manifest=[]
for number,type_ in [(536324,'ADN-50-25-I-P-A'),(536231,'ADN-16-30-I-P-A'),(8178767,'ADN-16-70-I-P-A')]:
 manifest.append(dict(vendor='Festo',part=number,type=type_,status='ORIGINAL_CAD_NOT_DOWNLOADED_LOGIN_REQUIRED',official_cad_url=f'https://www.festo.com/eap/en_us/DKI3CAD2Fox/start.do?part={number}',installed_geometry='catalogue-based simplified envelope inherited from C4'))
f=R/'models/vendor/kipp/k0309_212.stp'
manifest.append(dict(vendor='KIPP',filename=str(f.relative_to(R)),source='user upload, TraceParts STEP header',sha256=hashlib.sha256(f.read_bytes()).hexdigest(),status='ORIGINAL_UPLOADED_STEP_IMPORTED'))
(O/'vendor_manifest.json').write_text(json.dumps(manifest,indent=2))
