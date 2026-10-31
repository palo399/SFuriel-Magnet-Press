"""C4: direct ADN press, mechanical stripping and linked inlet shutter.
Concept only: see docs/Koncept_C4.md. Units mm, CadQuery.
"""
from pathlib import Path
import re,csv
import cadquery as cq
R=Path(__file__).resolve().parents[1];O=R/'models'/'concept-C4';O.mkdir(parents=True,exist_ok=True)
# Reuse validated geometry without exporting or overwriting C3.
src=(R/'cad/build_C3.py').read_text().split('# Export assembly, BOM and hole table.')[0]
src=re.sub(r'(?m)^(\s*)cq\.exporters\.export\(.*$',r'\1pass # no exports during reuse',src)
g={'__file__':str(R/'cad/build_C3.py')};exec(compile(src,str(R/'cad/build_C3.py'),'exec'),g)
old=g['components'];oldbom={r[0]:r for r in g['bom']};box,cyl=g['box'],g['cyl']
A=cq.Assembly(name='C4_simple_three_ADN');parts={};bom=[]
def add(n,s,mat='Steel',spec='',color=(.67,.7,.74)):
 assert s.val().isValid(),n
 A.add(s,name=n,color=cq.Color(*color));parts[n]=s;bom.append([n,mat,spec])
keep=('P02_Track','Left_through','Right_through','M4x16','Workpiece','Queue_','Part_on_','L_inlet','Chute_','Plunger_ball','M6_vertical','Head_pickup','Product_magnet','Festo_PART','P05_','P06_','Separator_rod','C_fork','Festo_FORK','P07_Fork_motor_face','Fork_link','Fork_extended','Fork_coupling','P09_')
for n,s in old.items():
 if n.startswith(keep):
  if n=='Right_through_retaining_rail':s=s.cut(box(12,74,-1,13,37,17))
  add(n,s,*oldbom.get(n,[n,'Reference',''])[1:3])
# Position next lateral part clear of the linked blade.
add('Next_rohovnik_on_inlet',old['Part_at_lateral_inlet'].translate((2,0,0)),'Workpiece','Next piece before separator')
# Clean base: no old guide, gate-actuator or mast holes.
base=box(-145,-155,-23,500,400,15)
base_holes=[(0,0,8),(-85,-42.5,13),(85,-42.5,13)]
base_holes += [(x,y,5) for x in [-22,22] for y in [155,193]]+[(x,y,5) for x in [180,290] for y in [-20,20]]
base_holes += [(x,y,6.6) for x in [-19,19] for y in [-100,50]]+[(x,y,9) for x in [-130,340] for y in [-140,230]]
for x,y,dia in base_holes:base=base.cut(cyl(x,y,-24,dia/2,17))
add('C4_Base_plate',base,'Aluminium','500x400x15; redundant C3 holes removed')
# Two short portal columns only, no magazine mast.
for n in ['BR_Left_column','BR_Right_column']:
 # Trim existing profile from -8 to60, retaining original footprint.
 short=old[n].intersect(box(-150,-100,-8,300,100,68))
 add(n+'_L68',short,'Bosch Rexroth','45x45 slot10 L68; cross-section schematic')
bridge=box(-110,-90,60,220,140,15)
bridge_holes=[(-85,-42.5,13),(85,-42.5,13),(0,0,20),(65,0,20.5)]
bridge_holes += [(x,y,9) for x in [-23.25,23.25] for y in [-23.25,23.25]]
bridge_holes += [(65+x,y,4.5) for x in [-13,13] for y in [-13,13]]
for x,y,dia in bridge_holes:bridge=bridge.cut(cyl(x,y,59,dia/2,17))
add('C4_Bridge',bridge,'Steel S355','220x140x15; press mount TG46.5; tube support')
# Cylinder lowers 132mm relative to C3. Short coaxial replaceable tool, no crosshead or guides.
add('Festo_PRESS_ADN50_25',old['Festo_PRESS_ADN50_25'].translate((0,0,-132)),'Festo','ADN-50-25-I-P-A #536324; provisional force selection',(.15,.38,.66))
tool=cyl(0,0,22,6.7,12).union(cyl(0,0,34,8,33.3)).cut(cyl(0,0,21.9,5.1,2.2))
add('Short_coaxial_press_tool',tool,'Tool steel','L45.3; D16 shank; annular D13.4 tip around recessed pickup magnet; connection thread to confirm')
# Threaded stop collar on moving tool; fixed bridge underside at60.
# At pickup collar spans34..36.7, and at final travel13.3 it spans20.7..23.4;
# adjustable lower stop is deliberately omitted until a suitable ADN travel-stop adapter is selected.
# The drawing must not imply that full 25mm travel is correct for a 13.3mm press motion.
# Stationary stripping shoe holds second magnet while first travels in fork.
strip=box(50,-15,22.2,30,30,3).cut(cyl(65,0,22.1,7.2,3.3))
for x in [53,77]:
 for y in [-12,12]:strip=strip.cut(cyl(x,y,22,1.7,4))
add('Fixed_magnet_stripper',strip,'POM / nonmagnetic','Bore14.4; exit gap5.3 above floor16.9; NO actuator',(.78,.62,.2))
# Two supports lie outside moving carrier (carrier Y +/-11).
for y in [-15,12]:
 support=box(50,y,-8,30,3,30.2)
 wear=box(50,-12 if y<0 else 11.2,15,30,.8,7.2)
 add('Stripper_side_support_'+str(y),support.union(wear),'Aluminium / POM liner','Combined fixed shoe support and fork guide; lateral clearance0.2')
tube=cyl(65,0,25.2,10,300).cut(cyl(65,0,25.1,7.2,300.2))
add('Magnet_tube_300',tube,'Nonmagnetic tube','ID14.4 OD20 L300; no gate slot')
# Long split collar directly bolted to the press bridge; no dedicated mast.
collar=cyl(65,0,75,13,40).union(box(48,-17,75,34,34,8)).cut(cyl(65,0,74,10.15,42))
collar=collar.cut(box(64.5,0,74,1,18,42))
for x in [-13,13]:
 for y in [-13,13]:collar=collar.cut(cyl(65+x,y,74,2.25,10))
add('Tube_split_collar_on_bridge',collar,'Aluminium','40mm guide sleeve; OD20.3 bore; clamping screw to finish')
# Remaining stack sits against the solid carrier tongue in pickup position.
for i in range(4):add('Stack_14x5_'+str(i),cyl(65,0,22+i*5,7,5),'Magnet','D14x5 reference only',(.7,.55,.2))
# One actuator indexes parts and simultaneously closes side inlet.
shoe=box(-12,104.5,1,24,5.5,22)
blade=box(16,104.5,1,2,40,12)
arm=box(10,108,9,8,7,5)
linked=shoe.union(blade).union(arm)
assert len(linked.solids().vals())==1, 'Pusher must be one connected solid'
add('Linked_pusher_and_inlet_shutter',linked,'POM / aluminium','One rigid moving part, 30mm stroke; NO gate ADN',(.15,.4,.65))
# Export STEP and tabular design data.
A.save(str(O/'Rohovnik_press_C4_simple.step'))
with (O/'BOM_C4.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Component','Material_supplier','Description']);w.writerows(bom)
with (O/'Mounting_holes_C4.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Part','Assembly_X','Assembly_Y','Diameter','Units']);w.writerows([['Base',x,y,di,'mm'] for x,y,di in base_holes]+[['Bridge',x,y,di,'mm'] for x,y,di in bridge_holes])
for n in ['C4_Base_plate','C4_Bridge','Short_coaxial_press_tool','Fixed_magnet_stripper','Tube_split_collar_on_bridge','Linked_pusher_and_inlet_shutter']:
 cq.exporters.export(parts[n],str(O/(n+'.step')))
read=cq.importers.importStep(str(O/'Rohovnik_press_C4_simple.step'));assert read.val().isValid()
# Focused checks: exit, stationary stripper versus moving fork across transfer,
# and inlet shutter versus retained rails in sampled index positions.
for dy in [0,-15,-30]:
 moving=parts['Linked_pusher_and_inlet_shutter'].translate((0,dy,0)).val()
 for n in ['Left_through_retaining_rail','Right_through_retaining_rail']:
  assert moving.intersect(parts[n].val()).Volume()<1e-5,(n,dy)
for dx in [0,16.25,32.5,48.75,65]:
 fork=parts['C_fork_14x5'].translate((dx,0,0)).val()
 for n in ['Fixed_magnet_stripper','Stripper_side_support_-15','Stripper_side_support_12']:
  assert fork.intersect(parts[n].val()).Volume()<1e-5,(n,dx)
for dy in [-35,-70,-110]:
 piece=parts['Workpiece_at_press_C2'].translate((0,dy,0)).val()
 for n in ['Left_through_retaining_rail','Right_through_retaining_rail','BR_Left_column_L68','BR_Right_column_L68']:
  assert piece.intersect(parts[n].val()).Volume()<1e-5,(n,dy)
print('PASS C4',len(parts),'components; STEP readback; sampled fork, shutter and exit checks')
from cadquery.occ_impl.exporters import svg
from OCP.gp import gp_Dir
original=svg.gp_Ax2;svg.gp_Ax2=lambda p,d:original(p,d,gp_Dir(1,1,0))
try:cq.exporters.export(read,str(O/'Assembly_C4.svg'),opt={'width':1400,'height':1000,'projectionDir':(1,-1,1.3),'showHidden':False,'strokeWidth':.5})
finally:svg.gp_Ax2=original
select=[s.val() for n,s in parts.items() if n.startswith(('P02','Left_through','Right_through','Workpiece','Queue','Next_rohovnik','Part_on','L_inlet','Chute','Festo_PART','P05','Linked_pusher'))]
cq.exporters.export(cq.Compound.makeCompound(select),str(O/'Plan_C4.svg'),opt={'width':1200,'height':900,'projectionDir':(0,0,1),'showHidden':False,'strokeWidth':.7})
