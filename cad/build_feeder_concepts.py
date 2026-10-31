"""Three alternative feeder concepts; CadQuery, mm. V1 retained unchanged."""
from pathlib import Path
import cadquery as cq

R=Path(__file__).resolve().parents[1]
# Reuse common press components without altering original source or V1 output.
ns={'__file__':str(R/'cad/build_concept.py')}
exec(compile((R/'cad/build_concept.py').read_text().split('A.save(')[0], str(R/'cad/build_concept.py'), 'exec'), ns)
box,cyl=ns['box'],ns['cyl']
O=R/'models'/'feeder-concepts'; O.mkdir(parents=True,exist_ok=True)
steel=(.65,.68,.72); blue=(.2,.4,.7); gold=(.85,.65,.2)
common=[(n,s) for n,s in ns['parts'] if not (n.startswith(('Magnet_shuttle','Shuttle_guide','Magnet_magazine','Magazine_','Magnet_at_head')))]
for code in ['A_linear','B_rotary','C_fork']:
 a=cq.Assembly(name=code); feeder=[]
 for n,s in common: a.add(s,name=n,color=cq.Color(*steel))
 def add(n,s,col=steel):
  assert s.val().isValid(),n
  a.add(s,name=n,color=cq.Color(*col)); feeder.append(s.val())
 # Magnet rides at z17..20; tube starts above slide with one-layer exit below.
 tube=cyl(65,0,20.2,10,300).cut(cyl(65,0,20.1,7.2,300.2))
 add('Tube_300mm',tube)
 add('Pickup_magnet',cyl(0,0,17,7,3),gold)
 # No solid crosses the pickup axis above the magnet.
 if code=='A_linear':
  # Blind pocket at pickup, solid tongue supports column during transfer.
  slide=box(-11,-11,15,95,22,5).cut(cyl(0,0,16.9,7.15,3.2))
  add('Slide_with_blind_pocket_at_pickup',slide,blue)
  for y in [-17,11]: add('Slide_guide_'+str(y),box(20,y,14,65,6,7))
  add('Fixed_strip_plate',box(52,-11,20.2,26,22,2).cut(cyl(65,0,20,7.2,2.5)),gold)
  add('Actuator_envelope',box(100,-12,12,50,24,24),blue)
 elif code=='B_rotary':
  disc=cyl(32.5,0,15,43,5)
  for x in [0,65]: disc=disc.cut(cyl(x,0,16.9,7.15,3.2))
  add('Two_pocket_rotor_180deg',disc,blue)
  add('Axle',cyl(32.5,0,0,5,15))
  add('Strip_plate',box(52,-11,20.2,26,22,2).cut(cyl(65,0,20,7.2,2.5)),gold)
 else:
  # U slot opens toward -X; magnet seated at x0. Narrow prongs clear tube mouth.
  fork=box(-11,-11,15,95,22,5).cut(box(-12,-7.15,16.9,12,14.3,3.2)).cut(cyl(0,0,16.9,7.15,3.2))
  add('Open_fork',fork,blue)
  # Separate lower gate under the remaining column; timing must be developed.
  gate=box(54,-11,20.2,30,22,1.5)
  add('Independent_stack_gate_closed',gate,gold)
  # Tube lifted to accommodate separate gate rather than intersecting it.
  # The tube's bottom is locally open: gate occupies bore, tube wall clears gate via cut.
  # Replace tube assembly component with clearance cut at gate height.
  a.remove('Tube_300mm')
  tube=tube.cut(box(53,-12,20.1,32,24,1.8))
  a.add(tube,name='Tube_with_gate_slot',color=cq.Color(*steel))
  feeder[0]=tube.val()
  for y in [-17,11]: add('Fork_guide_'+str(y),box(20,y,14,65,6,7))
 # Show a few remaining magnets, not a full stack.
 for i in range(4): add('Stack_magnet_'+str(i),cyl(65,0,22+i*3,7,3),gold)
 path=O/(code+'.step'); a.save(str(path))
 re=cq.importers.importStep(str(path)); assert re.val().isValid()
 # Detail preview hides long tube and common frame for visibility of exit mechanism.
 detail=[s for s in feeder if s.BoundingBox().zlen<100]
 cq.exporters.export(cq.Compound.makeCompound(detail),str(O/(code+'.svg')),opt={'width':900,'height':600,'projectionDir':(-1,-1,1.4),'showHidden':False,'strokeWidth':.8})
 print(code,'STEP valid',len(re.solids().vals()),'solids')
