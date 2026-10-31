"""Concept V1. Dimensions in mm. Run from repository root with cadquery 2.6+."""
from pathlib import Path
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'models'/'concept-v1'; OUT.mkdir(parents=True,exist_ok=True)
MAGNET_D=14.0; MAGNET_H=3.0; STACK_H=300.0
A=cq.Assembly(name='Rohovnik_magnet_press_V1')
parts=[]
def add(name,shape,color):
    assert shape.val().isValid(),name
    A.add(shape,name=name,color=cq.Color(*color)); parts.append((name,shape))
def box(x,y,z,dx,dy,dz):
    return cq.Workplane('XY').box(dx,dy,dz,centered=False).translate((x,y,z))
def cyl(x,y,z,r,h):
    return cq.Workplane('XY').circle(r).extrude(h).translate((x,y,z))
steel=(.62,.66,.70); blue=(.20,.32,.48); green=(.10,.52,.43); brass=(.76,.60,.25)
base=box(-110,-85,-20,250,210,12)
for x in [-95,125]:
 for y in [-70,110]: base=base.cut(cyl(x,y,-21,4.5,14))
add('Base_plate',base,steel)
add('Track_support',box(-23,-45,-8,46,165,8),steel)
# Inverted supplied component: magnet cavity faces upwards.
part=cq.importers.importStep(str(ROOT/'models'/'Rohovnik magnet.stp')).rotate((0,0,0),(1,0,0),180).translate((-15,-15,9.5))
add('Workpiece_at_press',part,green)
# Rails retain the narrow outer edge of the top flange; 0.3 mm vertical clearance.
for sign,label in [(-1,'Left'),(1,'Right')]:
    profile=[(14.8,0),(23,0),(23,14),(13.2,14),(13.2,11.4),(14.8,9.8)]
    if sign<0: profile=[(-x,z) for x,z in profile]
    rail=cq.Workplane('XZ').polyline(profile).close().extrude(150).translate((0,110,0))
    add(label+'_retaining_bevel_rail',rail,steel)
# Inclined upstream chute with example workpieces (existing hopper is not redesigned).
angle=25
chute=box(-23,0,-4,46,145,4).rotate((0,0,0),(1,0,0),angle).translate((0,110,0))
add('Gravity_chute_25deg',chute,steel)
for sign,label in [(-1,'L'),(1,'R')]:
    wall=box(19*sign-2,0,0,4,145,14).rotate((0,0,0),(1,0,0),angle).translate((0,110,0))
    add('Chute_side_'+label,wall,steel)
for i,y in enumerate([30,62,94]): add('Queued_part_'+str(i+1),part.translate((0,y,0)),green)
for i,y in enumerate([20,55,90]):
    add('Chute_part_'+str(i+1),part.translate((0,y,0)).rotate((0,0,0),(1,0,0),angle).translate((0,110,0)),green)
# Side indexing actuator and pusher, shown retracted; two-stop escapement placeholders.
add('Part_index_cylinder_envelope',box(30,20,0,55,24,24),blue)
add('Part_index_slide',box(20,24,3,25,16,5),steel)
for y in [35,67]: add('Escapement_stop_'+str(y),box(14.8,y,4,8,5,12),brass)
add('Station_end_stop',box(-14,-23,0,28,7,8),steel)
add('M6_ball_plunger_envelope',cq.Workplane('YZ').circle(3).extrude(12).translate((-27,0,5)),brass)
add('Plunger_ball',cq.Workplane('XY').sphere(2).translate((-14.8,0,5)),brass)
# C-frame, guided press head raised at pickup position.
add('Rear_column',box(-45,-68,-8,90,25,140),blue)
add('Top_crossmember',box(-45,-68,120,90,103,14),steel)
for x in [-32,32]: add('Guide_post_'+str(x),cyl(x,10,14,5,106),steel)
add('Moving_crosshead',box(-40,-12,62,80,42,12),blue)
add('Press_ram_envelope',cyl(0,0,74,12,46),steel)
add('Press_punch',cyl(0,0,25,6.7,37),steel)
add('Head_pickup_magnet',cyl(0,0,23,5,2),brass)
add('Magnet_at_head',cyl(0,0,20,MAGNET_D/2,MAGNET_H),(.30,.30,.32))
# Shuttle moves from x=65 to x=0; pocket shown at magazine, head shown loaded.
shuttle=box(-10,-10,15,90,20,5).cut(cyl(65,0,16.9,7.15,4))
add('Magnet_shuttle_at_magazine',shuttle,blue)
add('Magnet_shuttle_actuator_envelope',box(82,-17,8,48,34,28),blue)
add('Shuttle_guide',box(26,-16,10,54,32,5),steel)
# Tube bottom gap allows one 3mm magnet to be sheared into the pocket.
add('Magnet_magazine_300mm',cyl(65,0,20.2,10,STACK_H).cut(cyl(65,0,20.1,7.2,STACK_H+.2)),(.72,.72,.76))
for i in range(5): add('Magazine_magnet_'+str(i+1),cyl(65,0,17+i*MAGNET_H,7,MAGNET_H),(.35,.35,.37))
add('Magazine_support_post',box(90,30,-8,15,15,220),steel)
for z in [45,190]:
    clamp=box(53,-13,z,52,58,8).cut(cyl(65,0,z-1,10.15,10))
    add('Magazine_clamp_'+str(z),clamp,blue)
A.save(str(OUT/'Rohovnik_magnet_press_V1.step'))
# Independent STEP readback, including all named assembly solids.
s=cq.importers.importStep(str(OUT/'Rohovnik_magnet_press_V1.step'))
assert s.val().isValid()
assert len(s.solids().vals())>=len(parts)
print('PASS: STEP readback,',len(parts),'components,',len(s.solids().vals()),'solids')
