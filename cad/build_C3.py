"""C3 engineering layout. CadQuery; catalogue-based simplified Festo geometry.
Run from root. Sources and unverified interfaces: docs/Koncept_C3.md.
"""
from pathlib import Path
import cadquery as cq
import csv,math
R=Path(__file__).resolve().parents[1]; O=R/'models'/'concept-C3';P=O/'plates'
P.mkdir(parents=True,exist_ok=True)
# Evaluate prior construction without exporting or modifying any prior revision.
d={'__file__':str(R/'cad/build_revision_C2.py')}
exec(compile((R/'cad/build_revision_C2.py').read_text().rsplit('\nexec(',1)[0],str(R/'cad/build_revision_C2.py'),'exec'),d)
b={'__file__':str(R/'cad/build_feeder_concepts.py')}
exec(compile(d['source'].split(' path=O/')[0],str(R/'cad/build_feeder_concepts.py'),'exec'),b)
box,cyl=b['box'],b['cyl']; A=cq.Assembly(name='C3_Bosch_Festo_14x5');bom=[];holes=[];components={}
steel=(.66,.70,.74);blue=(.15,.38,.66);al=(.80,.82,.84);gold=(.75,.6,.2)
def add(n,s,material='Steel',spec='',color=steel):
 assert s.val().isValid(),n
 A.add(s,name=n,color=cq.Color(*color));components[n]=s
 bb=s.val().BoundingBox();bom.append([n,material,spec,round(bb.xlen,2),round(bb.ylen,2),round(bb.zlen,2)])
def panel(n,w,h,t,hs,pos=(0,0,0),rx=0,material='Aluminium 6082',slots=()):
 s=box(-w/2,-h/2,0,w,h,t)
 for x,y,dia,note in hs:
  assert abs(x)+dia/2<w/2 and abs(y)+dia/2<h/2,(n,x,y)
  s=s.cut(cyl(x,y,-1,dia/2,t+2));holes.append([n,x,y,dia,note,t])
 for x,y,l,dia in slots:
  cut=cq.Workplane('XY').center(x,y).slot2D(l,dia,90).extrude(t+2).translate((0,0,-1));s=s.cut(cut)
  holes.append([n,x,y,dia,'SLOT length '+str(l)+' along local Y',t])
 cq.exporters.export(s,str(P/(n+'.step')))
 cq.exporters.export(s.section(t/2),str(P/(n+'.dxf')))
 world=s.rotate((0,0,0),(1,0,0),rx).translate(pos)
 add(n,world,material,'Plate: local XY origin at centre, bottom Z=0');return world
# Retain only workpiece path and reference pieces from C2.
for n,s in b['common']:
 if n.startswith(('Workpiece_at','Queue_on','Part_at_lateral','Part_on_inlet','L_inlet','Chute_','Plunger_ball','M6_vertical')):
  add(n,s,'Reference workpiece' if 'part' in n.lower() else 'Concept hardware',color=(.1,.5,.4) if 'part' in n.lower() else steel)
# Base / track interfaces.
rail_y=[-125,-75,-25,25,65]
baseholes=[(0,0,8,'Plunger access'),(-85,-42.5,13,'M12 profile end bolt VERIFY'),(85,-42.5,13,'M12 profile end bolt VERIFY'),(120,40,13,'Magazine mast end bolt VERIFY')]
baseholes += [(x,y,5,'M6 TAP mounting foot') for x,y in [(x,y) for x in [-22,22] for y in [155,193]]+[(x,y) for x in [180,290] for y in [-20,20]]+[(x,y) for x in [35,95] for y in [-95,-45]]]
baseholes += [(x,20,9,'M8 stop pillar fixing') for x in [-48,48]]
baseholes += [(x,-32,12,'Guide shaft D12H7 seat') for x in [-40,40]]
baseholes += [(x,y,6.6,'M6 track attachment from below') for x in [-19,19] for y in [-100,50]]
baseholes += [(x,y,9,'M8 bench mounting') for x in [-130,340] for y in [-140,230]]
panel('P01_Base',500,400,15,[(x-105,y-45,di,n) for x,y,di,n in baseholes],(105,45,-23))
trackholes=[(0,0,5,'M6x1 TAP THROUGH plunger')]+[(x,y,3.3,'M4 TAP THROUGH rail') for x in [-19,19] for y in rail_y]+[(x,y,5,'M6 TAP THROUGH base') for x in [-19,19] for y in [-100,50]]
panel('P02_Track_bed',46,250,8,[(x,y+15,di,n) for x,y,di,n in trackholes],(0,-15,-8),'0' if False else 0)
# Through retaining rails, clearance and recessed M4 cap screw seats.
for n,s in b['common']:
 if n.startswith(('Left_through','Right_through')):
  x=-19 if n.startswith('Left') else 19
  for y in rail_y:
   s=s.cut(cyl(x,y,-1,2.25,16)).cut(cyl(x,y,9.5,3.75,5))
   holes.append([n,x,y,4.5,'Through + counterbore D7.5 from Z14 to9.5',14])
   bolt=cyl(x,y,-6.5,2,16).union(cyl(x,y,9.5,3.5,4))
   add('M4x16_'+n[:4]+'_'+str(y),bolt,'Fastener','ISO4762 M4x16 simplified')
  add(n,s,'Aluminium or nonmagnetic guide','Retaining bevel; holes at assembly XY')
  cq.exporters.export(s,str(P/(n+'.step')))
# 45x45 profile schematic, four 10mm slots; not factory extrusion contour.
def profile(n,x,y,z,length):
 s=box(-22.5,-22.5,0,45,45,length).cut(cyl(0,0,-1,5.1,length+2))
 for angle in [0,90,180,270]:
  cut=box(17.5,-5,-1,6,10,length+2).union(box(12,-8,-1,6,16,length+2)).rotate((0,0,0),(0,0,1),angle)
  s=s.cut(cut)
 add(n,s.translate((x,y,z)),'Bosch Rexroth profile','45x45 slot10, cut '+str(length)+'; contour schematic',al)
profile('BR_Left_column',-85,-42.5,-8,200);profile('BR_Right_column',85,-42.5,-8,200)
profile('BR_Magazine_mast',120,40,-8,340)
# Structural bridge: cylinder mount and two guide rods.
topholes=[(-85,-42.5,13,'M12 profile end bolt VERIFY'),(85,-42.5,13,'M12 profile end bolt VERIFY'),(0,0,20,'Press rod clearance')]
topholes += [(x,y,9,'Festo ADN50 M8 face mount TG46.5') for x in [-23.25,23.25] for y in [-23.25,23.25]]
topholes += [(x,-32,12,'Guide shaft seat D12H7 to finish') for x in [-40,40]]
panel('P03_Top_bridge',220,140,15,[(x,y+20,di,n) for x,y,di,n in topholes],(0,-20,192),material='Steel S355')
# Guided ram kept clear of the strip and feed fork. Precision fit needs final linear bush selection.
crossholes=[(-48,20,9,'M8 depth stop clearance'),(48,20,9,'M8 depth stop clearance'),(0,0,10,'M12 TAP coupling pilot'),(-40,-32,18,'Linear bushing seat VERIFY'),(40,-32,18,'Linear bushing seat VERIFY')]
panel('P04_Moving_head',110,80,12,[(x,y+10,di,n) for x,y,di,n in crossholes],(0,-10,96),material='Steel S355')
for x in [-40,40]:
 add('Guide_D12_'+str(x),cyl(x,-32,-14,6,221),'Hardened guide shaft','D12 x221')
 add('Guide_bushing_'+str(x),cyl(x,-32,90,9,24).cut(cyl(x,-32,89,6,26)),'Linear bearing','D12 bore, D18 body provisional')
add('Punch_shaft',cyl(0,0,24,6.7,72),'Steel tool','D13.4 punch; length96-24')
add('Head_pickup_magnet',cyl(0,0,22,5,2),'Magnet','Head retention magnet concept',gold)
add('Product_magnet_14x5',cyl(0,0,17,7,5),'Magnet','USER CONFIRMED D14x5',gold)
# Adjustable travel stop prevents the cylinder using its full stroke against the workpiece.
for x in [-48,48]:
 add('Stop_support_'+str(x),cyl(x,20,-8,8,78.7).cut(cyl(x,20,60,3.4,12)).cut(cyl(x,20,-9,3.4,20)),'Steel','M8 tapped depth stop pillar')
 add('Adjustable_stop_M8_'+str(x),cyl(x,20,70.7,4,42).union(cyl(x,20,76.7,7,6)).union(cyl(x,20,70.7,7,6)),'Fastener','Adjust travel after press-fit test')
# Festo ADN dimensions from official 2026/09 p17: E, TG, ZA, ZB, rodMM, RT.
CAT={12:(27.5,16,35,39.2,6,4),16:(29,18,35,39.7,8,4),50:(65.5,46.5,45,52.7,16,8)}
def festo(n,bore,stroke,partno,front,axis):
 E,TG,ZA,ZB,rod,rt=CAT[bore];L=ZA+stroke
 # Local +Z is extension direction, front mounting plane at local Z0.
 body=box(-E/2,-E/2,-L,E,E,L)
 for x in [-TG/2,TG/2]:
  for y in [-TG/2,TG/2]:body=body.cut(cyl(x,y,-7,rt/2,8))
 # Pipe port representations on one side; threads not modelled.
 for z in [-8,-L+8]:
  port=cq.Workplane('YZ').circle(2.5 if bore<20 else 4.3).extrude(7).translate((E/2-6,0,z));body=body.cut(port)
 shape=body.union(cyl(0,0,0,rod/2,ZB-ZA))
 def orient(s):
  if axis=='-Z':s=s.rotate((0,0,0),(1,0,0),180)
  elif axis=='-Y':s=s.rotate((0,0,0),(1,0,0),90)
  elif axis=='+Y':s=s.rotate((0,0,0),(1,0,0),-90)
  elif axis=='-X':s=s.rotate((0,0,0),(0,1,0),-90)
  return s.translate(front)
 add(n,orient(shape),'Festo','ADN-'+str(bore)+'-'+str(stroke)+'-I-P-A #'+str(partno)+'; simplified catalogue envelope',blue)
 return E,TG,rt
festo('Festo_PRESS_ADN50_25',50,25,536324,(0,0,207),'-Z')
# Extension adapter joins retracted rod end at199.3 to guided head at108.
add('Press_rod_adapter',cyl(0,0,108,6,91.3),'Steel','Female piston rod coupling; confirm thread and floating coupling')
# Separator mount, cylinder face towards -Y and pusher indexes 30 mm.
festo('Festo_PART_INDEX_ADN16_30',16,30,536231,(0,145,18),'-Y')
sep=[(x,y,4.5,'Festo ADN16 M4 TG18') for x in [-9,9] for y in [-9,9]]+[(0,0,10,'Rod clearance')]
panel('P05_Separator_face',48,36,6,sep,(0,145,18),rx=90)
add('Separator_rod_extension',cq.Workplane('XZ').circle(3).extrude(30.3).translate((0,140.3,18)),'Steel','Links cylinder to pusher')
add('Separator_pusher',box(-12,106,1,24,4,22),'POM','Removable pushing shoe')
# Mount feet for P05: slotted for setup, vertical plate fasteners need final corner bracket detailing.
panel('P06_Separator_foot',60,75,8,[(-22,-20,6.6,'M6 base bolt'),(22,-20,6.6,'M6 base bolt')],(0,175,-8),slots=[(-22,18,20,6.6),(22,18,20,6.6)])
# Magnet fork: 5mm magnet, 5.1 pocket depth, solid bottom 1.9mm.
fork=box(-11,-11,15,95,22,7).cut(box(-12,-7.15,16.9,12,14.3,5.3)).cut(cyl(0,0,16.9,7.15,5.3))
for x in [72,79]:
 fork=fork.cut(cyl(x,0,14,1.65,9));holes.append(['C_fork_14x5',x,0,1.65,'M2 TAP linkage',7])
add('C_fork_14x5',fork,'POM / nonmagnetic','Open pickup pocket D14.3 depth5.1',blue)
for y in [-17,11]:add('Fork_slide_guide_'+str(y),box(24,y,14,64,6,9),'POM','0.2mm running clearance to be tuned')
festo('Festo_FORK_ADN16_70',16,70,8178767,(200,0,18.5),'-X')
# Vertical YZ cylinder plate; custom local rotation for axial X.
fg=[(x,y,4.5,'Festo ADN16 M4 TG18') for x in [-9,9] for y in [-9,9]]+[(0,0,10,'Rod clearance')]
local=panel('P07_Fork_motor_face_local',44,44,6,fg,(0,0,0))
# Replace temporary local placement with YZ plate at actuator face.
A.remove('P07_Fork_motor_face_local');components.pop('P07_Fork_motor_face_local')
world=local.rotate((0,0,0),(0,1,0),-90).translate((200,0,18.5));A.add(world,name='P07_Fork_motor_face',color=cq.Color(*steel));components['P07_Fork_motor_face']=world
add('Fork_link_extension',cq.Workplane('YZ').circle(3).extrude(41.3).translate((89,0,18.5)),'Steel','Link to fork, articulation to develop')
add('Fork_extended_rod_65',cq.Workplane('YZ').circle(4).extrude(65).translate((130.3,0,18.5)),'Festo rod representation','ADN16-70 shown extended65; adjustable stops required')
add('Fork_coupling_block',box(78,-5,15,12,10,8),'Aluminium','Coupling to open fork')
panel('P09_Fork_motor_foot',140,60,4.5,[(-55,-20,6.6,'M6 base fixing'),(55,-20,6.6,'M6 base fixing'),(-55,20,6.6,'M6 base fixing'),(55,20,6.6,'M6 base fixing')],(235,0,-8))
# Magazine raised from 20.2 to22.2 to accommodate 5mm magnet.
tube=cyl(65,0,22.2,10,300).cut(cyl(65,0,22.1,7.2,300.2)).cut(box(53,-12,22.1,32,24,1.8))
add('Magnet_tube_300',tube,'Nonmagnetic tube','ID14.4 OD20; gate slot1.8')
for i in range(4):add('Stack_14x5_'+str(i),cyl(65,0,24+i*5,7,5),'Magnet','D14x5 reference stack',gold)
add('Independent_stack_gate',box(54,-11,22.2,30,22,1.5),'Nonmagnetic steel','Sequencing / inter-magnet insertion to validate',gold)
festo('Festo_MAGNET_GATE_ADN12_10',12,10,536212,(65,-50,22.95),'+Y')
gateholes=[(x,y,4.5,'Festo ADN12 M4 TG16') for x in [-8,8] for y in [-8,8]]+[(0,0,8,'Rod clearance')]
panel('P10_Magnet_gate_face',44,40,6,gateholes,(65,-50,22.95),rx=-90)
panel('P12_Magnet_gate_foot',80,70,10.95,[(-30,-25,6.6,'M6 base bolt'),(30,-25,6.6,'M6 base bolt'),(-30,25,6.6,'M6 base bolt'),(30,25,6.6,'M6 base bolt')],(65,-70,-8))
add('Magnet_gate_rod_extension',cq.Workplane('XZ').circle(2).extrude(34.8).translate((65,-11,22.95)),'Steel','Gate linkage')
festo('Festo_INLET_GATE_ADN12_10',12,10,536212,(17,90,40),'-Z')
panel('P11_Inlet_gate_motor_shelf',80,50,6,[(x+17,y,di,n) for x,y,di,n in gateholes],(0,90,34))
add('Inlet_gate_support',box(-40,68,0,8,44,34),'Aluminium','Cantilever support; M6 fixings to finish')
add('Inlet_gate_rod_extension',cyl(17,90,21,2,14.8),'Steel','Gate link')
add('Inlet_gate_blade',box(15.5,75,17,3,30,4),'Nonmagnetic steel','Blade open; 10mm travel',gold)
for z in [50,230]:
 clamp=box(50,-15,z,30,30,8).cut(cyl(65,0,z-1,10.15,10)).cut(box(64.5,-16,z-1,1,17,10))
 for x in [52.5,77.5]:clamp=clamp.cut(cyl(x,10,z-1,1.65,10))
 add('Split_tube_clamp_'+str(z),clamp,'Aluminium','OD20.3 clamp; pinch fastener layout to finish')
 panel('P08_Mast_shelf_'+str(z),47.5,60,6,[(-8.75,-15,20.5,'Tube clearance'),(-21.25,-5,3.3,'M3 clamp attachment'),(3.75,-5,3.3,'M3 clamp attachment')],(73.75,15,z-6))
 add('Mast_angle_'+str(z),box(91.5,15,z-6,6,35,28).cut(cq.Workplane('YZ').circle(4.5).extrude(8).translate((90.5,40,z+8))),'Aluminium','M8 slot10 T-nut mounting, verify Bosch connector')
# Export assembly, BOM and hole table.
A.save(str(O/'Rohovnik_press_C3_Bosch_Festo.step'))
with (O/'BOM.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Component','Material_or_supplier','Specification','BBoxX_mm','BBoxY_mm','BBoxZ_mm']);w.writerows(bom)
with (O/'Holes.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Part','LocalX_mm','LocalY_mm','ModelDiameter_mm','Operation','Thickness_mm']);w.writerows(holes)
read=cq.importers.importStep(str(O/'Rohovnik_press_C3_Bosch_Festo.step'));assert read.val().isValid()
for y in [-35,-70,-110]:
 part=b['ns']['part'].translate((0,y,0)).val()
 for n,s in components.items():
  if n.startswith(('Left_through','Right_through','BR_Left','BR_Right')):assert part.intersect(s.val()).Volume()<1e-5,(n,y)
print('PASS',len(components),'components',len(read.solids().vals()),'STEP solids;',len(holes),'hole operations; exit checks passed')
# Plan layout, excluding tall structures for legibility.
selected=[s.val() for n,s in components.items() if n.startswith(('Through','P02','Left_through','Right_through','Separator','Workpiece','Queue','Part_at','Part_on','L_inlet','Chute','Festo_PART','Inlet_gate'))]
cq.exporters.export(cq.Compound.makeCompound(selected),str(O/'Plan_C3.svg'),opt={'width':1200,'height':900,'projectionDir':(0,0,1),'showHidden':False,'strokeWidth':.6})
# Keep world Z vertical in the isometric preview.
from cadquery.occ_impl.exporters import svg
from OCP.gp import gp_Dir
original_frame=svg.gp_Ax2
svg.gp_Ax2=lambda p,d:original_frame(p,d,gp_Dir(1,1,0))
try:
 cq.exporters.export(read,str(O/'Assembly_C3.svg'),opt={'width':1400,'height':1000,'projectionDir':(1,-1,1.3),'showHidden':False,'strokeWidth':.4})
finally: svg.gp_Ax2=original_frame
