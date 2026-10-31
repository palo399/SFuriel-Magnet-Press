"""Revision C2: open through-track, lateral inlet and indexing cylinder. mm."""
from pathlib import Path
import cadquery as cq
R=Path(__file__).resolve().parents[1]
# Reuse C feeder geometry while replacing common frame and workpiece handling.
source=(R/'cad/build_feeder_concepts.py').read_text()
source=source.replace("O=R/'models'/'feeder-concepts'", "O=R/'models'/'concept-C2'")
start=source.index('common=[')
end=source.index("for code in ['A_linear','B_rotary','C_fork']:")
replacement='''
ns['part']=ns['part'].translate((0,0,-9.5))
removed=('M6_ball_plunger','Plunger_ball','Workpiece_at_press','Base_plate','Rear_column','Top_crossmember','Track_support','Left_retaining','Right_retaining','Gravity_chute','Chute_','Queued_part','Part_index','Escapement_stop','Station_end_stop')
common=[(n,s) for n,s in ns['parts'] if not n.startswith(removed+('Magnet_shuttle','Shuttle_guide','Magnet_magazine','Magazine_','Magnet_at_head'))]
track=[]
def shared(n,s):
 assert s.val().isValid(),n
 common.append((n,s)); track.append(s.val())
shared('Workpiece_at_press_C2',ns['part'])
shared('M6_vertical_plunger_body_envelope',cyl(0,0,-15,3,12))
shared('Plunger_ball_concept',cq.Workplane('XY').sphere(2.75).translate((0,0,-1.15)))
shared('Base_C2',box(-110,-155,-20,310,355,12).cut(cyl(0,0,-21,4,22)))
# Two lateral columns replace the obstructing rear column. Passage at X +/-23 is open.
for x in [-66,54]: shared('Side_frame_column_'+str(x),box(x,-65,-8,12,25,128))
shared('Top_bridge_C2',box(-72,-68,120,144,103,14))
shared('Through_track_bed',box(-23,-140,-8,46,250,8).cut(cyl(0,0,-9,3,10)))
for sign,label in [(-1,'Left'),(1,'Right')]:
 profile=[(14.8,0),(23,0),(23,14),(13.2,14),(13.2,11.4),(14.8,9.8)]
 if sign<0: profile=[(-x,z) for x,z in profile]
 rail=cq.Workplane('XZ').polyline(profile).close().extrude(250).translate((0,110,0))
 if sign>0: rail=rail.cut(box(12,75,-1,13,30,17))
 shared(label+'_through_retaining_rail',rail)
# 90-degree inlet. Level receiving zone, then gravity chute rising towards +X.
shared('L_inlet_level_bed',box(14.8,75,-4,35.2,30,4))
for y in [71,105]: shared('L_inlet_level_side_'+str(y),box(23,y,0,27,4,14))
angle=-25
for n,s in [('Chute_bed',box(0,75,-4,130,30,4)),('Chute_wall_front',box(0,71,0,130,4,14)),('Chute_wall_back',box(0,105,0,130,4,14))]:
 shared(n,s.rotate((0,0,0),(0,1,0),angle).translate((50,0,0)))
part=ns['part']
for i,y in enumerate([30,60,90]): shared('Queue_on_track_'+str(i),part.translate((0,y,0)))
shared('Part_at_lateral_inlet',part.translate((32,90,0)))
for i,x in enumerate([25,60,95]):
 shared('Part_on_inlet_slope_'+str(i),part.translate((x,90,0)).rotate((0,0,0),(0,1,0),angle).translate((50,0,0)))
# Inline actuator moves towards -Y, indexing 30 mm per cycle. Shown retracted.
shared('Separator_cylinder_body_envelope',box(-12,140,0,24,45,24))
shared('Separator_cylinder_mount',box(-18,132,-8,36,8,38).cut(cq.Workplane('XZ').circle(4).extrude(10).translate((0,141,10))))
shared('Separator_rod_retracted',cq.Workplane('XZ').circle(3).extrude(30).translate((0,140,10)))
shared('Separator_pusher_retracted',box(-12,106,1,24,4,8))
# Gate closes across lateral inlet while indexing; shown raised (open).
shared('Inlet_gate_blade_open',box(15.5,75,17,3,30,4))
shared('Inlet_gate_actuator_envelope',box(12,78,28,12,24,25))
'''
source=source[:start]+replacement+source[end:]
source=source.replace("for code in ['A_linear','B_rotary','C_fork']:","for code in ['C_fork']:")
# Export overview of part handling as well as existing feeder detail.
source += '''
cq.exporters.export(cq.Compound.makeCompound([s.val() for n,s in common if n.startswith(('Through_track','Left_through','Right_through','L_inlet','Chute','Queue','Part_at','Part_on','Separator','Inlet_gate','Workpiece_at_press_C2'))]),str(O/'Track_C2.svg'),opt={'width':1200,'height':850,'projectionDir':(0,0,1),'showHidden':False,'strokeWidth':.7})
# Validate that the supplied workpiece can leave along the straight open exit.
obstacles=[(n,s) for n,s in common if n.startswith(('Left_through','Right_through','Side_frame','Top_bridge'))]
for y in [-35,-70,-110]:
 moving=part.translate((0,y,0)).val()
 for name,obstacle in obstacles:
  assert moving.intersect(obstacle.val()).Volume()<1e-5,('Exit interference',name,y,moving.intersect(obstacle.val()).Volume())
print('PASS: exit clearance at three downstream positions')
'''
exec(compile(source,str(R/'cad/build_feeder_concepts.py'),'exec'),{'__file__':str(R/'cad/build_feeder_concepts.py')})
