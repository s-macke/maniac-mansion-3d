"""Room 005: book-lined library, reading corner and decorative spiral stair."""
from pathlib import Path
import sys,math,random,bpy
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from blender_shared.layout_shell import build
from blender_shared.furnishings import panel,curved_line


def furnish(geo,config):
    box=geo.box;rng=random.Random(5)
    bpy.data.objects['Wall_front'].name='Front_inferred_library'
    # Full-width rear bookcase: raised cupboards and three shelf rows.
    box('Bookcase_dark_back',(0,5.13,1.82),(10.7,.34,2.6),'black')
    for x in [-5.4,5.4]:box('Bookcase_end',(x,4.87,1.56),(.12,.65,3.12),'brown')
    for i in range(14):panel(geo,'Bookcase_cupboard',-5.04+i*.775,4.77,.39,.74,.68)
    colors=['white','gray','red','blue','lightblue','green','cyan','yellow','purple','pink']
    for row,z in enumerate([.78,1.56,2.34]):
        box('Shelf_gold_edge',(0,4.82,z),(10.8,.65,.065),'yellow')
        box('Shelf_wood',(0,4.8,z+.035),(10.8,.66,.055),'brown')
        x=-5.26
        while x<5.2:
            w=rng.uniform(.065,.14);h=rng.uniform(.42,.68);color=rng.choice(colors)
            box('Book_spine',(x+w/2,4.85,z+.075+h/2),(w,.34,h),color)
            if rng.random()<.68:
                for zz in [z+.13,z+h-.015]:box('Book_binding',(x+w/2,4.669,zz),(w*.78,.014,.018),'white' if color!='white' else 'gray')
            x+=w+.025
    # Brown helical flight as drawn, ending at the ceiling; no invented destination.
    cx,cy=-.1,3.3
    geo.cyl('Spiral_central_column',(cx,cy,1.56),.20,3.12,'brown',20)
    outer=[]
    for i in range(21):
        a=-math.pi/2+i*math.tau/25;b=a+math.tau/25;z=.12+i*.143
        vs=[(cx+r*math.cos(t),cy+r*math.sin(t),zz) for zz in [z-.08,z] for r,t in [(.2,a),(1.18,a),(1.18,b),(.2,b)]]
        geo.mesh('Spiral_tread',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'brown')
        geo.beam('Spiral_tread_edge',vs[5],vs[6],.035,'yellow')
        p=(cx+1.18*math.cos(a),cy+1.18*math.sin(a),z)
        if z+.68<3.12:geo.beam('Spiral_baluster',p,(p[0],p[1],z+.68),.045,'brown')
        outer.append((p[0],p[1],min(z+.68,3.09)))
    curved_line(geo,'Spiral_handrail',outer,.085,'brown')
    # Reading chair, phone table and slim standing lamps.
    box('Armchair_seat',(4.85,2.1,.48),(1.25,1.05,.27),'black')
    back=box('Armchair_back',(4.85,2.57,1.03),(1.1,.3,1.16),'black');back.rotation_euler.x=-.14
    for x in [4.23,5.47]:box('Armchair_arm',(x,2.08,.72),(.22,1.18,.5),'black')
    for x in [4.4,5.3]:
        for y in [1.72,2.47]:box('Armchair_foot',(x,y,.15),(.1,.1,.3),'brown')
    panel(geo,'Telephone_table_front',3.65,1.8,.3,.7,.38)
    box('Telephone_table_top',(3.65,2.1,.57),(.82,.68,.1),'brown')
    for x in [3.32,3.98]:
        for y in [1.86,2.34]:box('Telephone_table_leg',(x,y,.25),(.07,.07,.5),'brown')
    box('Telephone_base',(3.65,2.1,.68),(.48,.34,.13),'green')
    box('Telephone_receiver',(3.65,2.13,.80),(.53,.13,.09),'black')
    box('Telephone_dial',(3.65,1.92,.72),(.16,.025,.1),'cyan')
    for x,y in [(-5.1,3.8),(5.55,3.6)]:
        geo.cyl('Floor_lamp_base',(x,y,.06),.22,.1,'brown')
        geo.cyl('Floor_lamp_stem',(x,y,1.03),.027,1.95,'yellow')
        geo.mesh('Floor_lamp_shade',[(x+r*math.cos(i*math.tau/12),y+r*math.sin(i*math.tau/12),z) for z,r in [(1.85,.06),(2.18,.23)] for i in range(12)],[(i,(i+1)%12,(i+1)%12+12,i+12) for i in range(12)],'white')
        geo.sphere('Floor_lamp_glow',(x,y,2.13),(.12,.12,.08),'yellow')

build(Path(__file__).with_name('room.json'),furnish)
