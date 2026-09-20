"""Room 016: static EGA car, shelving and raised shutter hardware."""
import math
from blender_shared.furnishings import source_patch


def furnish(geo,root):
    box=geo.box
    # Car faces the open forecourt (-X). u runs across the car, v along it.
    cx,cy=8.45,4.6
    def b(name,u,v,z,w,l,h,color):return box(name,(cx+v,cy+u,z),(l,w,h),color)
    def mesh(name,vertices,faces,color):return geo.mesh(name,[(cx+v,cy+u,z) for u,v,z in vertices],faces,color)
    def wheel(name,u,v):
        # Axle along Y; black tire with gray inset hub.
        for radius,width,offset,color in [(.43,.26,0,'black'),(.25,.025,.145,'gray'),(.11,.03,.163,'darkgray')]:
            verts=[(cx+v+radius*math.cos(i*math.tau/20),cy+u+s*width/2+math.copysign(offset,u),.45+radius*math.sin(i*math.tau/20)) for s in [-1,1] for i in range(20)]
            geo.mesh(name,verts,[tuple(reversed(range(20))),tuple(range(20,40))]+[(i,(i+1)%20,(i+1)%20+20,i+20) for i in range(20)],color)
    b('Car_chassis',0,0,.44,2.3,4.7,.20,'black')
    # Tapered red shell and sloping hood, with complete sides and rear.
    sections=[(-2.45,1.18,.64,.92),(-1.55,1.3,.56,1.02),(.9,1.28,.58,1.03),(2.25,1.15,.62,.96)]
    verts=[(u,v,z) for v,w,low,high in sections for u,z in [(-w,low),(w,low),(w,high),(-w,high)]]
    faces=[(3,2,1,0),(12,13,14,15)]
    for j in range(3):
        for k in range(4):faces.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
    mesh('Car_red_body',verts,faces,'red')
    # Four real wheels, visible from either side.
    for u in [-1.22,1.22]:
        for v in [-1.48,1.48]:wheel('Car_wheel',u,v)
    # Low black cabin with red roof and cyan window surrounds.
    cabin=[(-1.05,-.83,1),(1.05,-.83,1),(1.02,1.33,1),(-1.02,1.33,1),(-.82,-.28,1.62),(.82,-.28,1.62),(.82,.94,1.62),(-.82,.94,1.62)]
    mesh('Car_windows',cabin,[(4,5,1,0),(5,6,2,1),(6,7,3,2),(7,4,0,3)],'black')
    mesh('Car_roof',cabin,[(7,6,5,4)],'red')
    for a,bb in [(0,4),(1,5),(2,6),(3,7),(4,5),(6,7),(0,1),(2,3)]:
        u,v,z=cabin[a];uu,vv,zz=cabin[bb];geo.beam('Car_window_trim',(cx+v,cy+u,z),(cx+vv,cy+uu,zz),.04,'cyan')
    for u in [-1.035,1.035]:
        geo.beam('Car_window_pillar',(cx+.5,cy+u,1.02),(cx+.5,cy+math.copysign(.82,u),1.62),.055,'red')
        b('Car_door_handle',u,.2,.93,.025,.25,.045,'gray')
        b('Car_side_chrome',u*1.24,0,.73,.035,3.9,.045,'aqua')
    # Turquoise grille, bumper and broad circular headlight pods: the source silhouette.
    b('Car_grille_black',0,-2.47,.77,1.9,.065,.33,'black')
    for z in [.68,.76,.84]:b('Car_grille_bar',0,-2.51,z,1.87,.04,.025,'gray')
    b('Car_bumper',0,-2.56,.52,2.65,.18,.14,'cyan')
    b('Car_bumper_highlight',0,-2.67,.57,2.61,.025,.035,'aqua')
    for u in [-1.2,1.2]:
        geo.sphere('Headlight_pod',(cx-2.18,cy+u,.99),(.53,.29,.24),'cyan')
        # Disc faces point along the car length.
        for radius,xx,color in [(.23,cx-2.63,'aqua'),(.16,cx-2.66,'black'),(.095,cx-2.68,'gray')]:
            geo.mesh('Headlight_disc',[(xx,cy+u+radius*math.cos(i*math.tau/24),.99+radius*math.sin(i*math.tau/24)) for i in range(24)],[tuple(reversed(range(24)))],color)
        # High rear fins and horizontal cyan rear bumper.
        mesh('Car_tail_fin',[(u,1.1,.92),(u,2.24,.92),(u,2.18,1.52),(u*.93,1.1,.92),(u*.93,2.24,.92),(u*.93,2.18,1.52)],[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],'cyan')
        b('Tail_light',u,2.27,.83,.22,.035,.14,'lightred')
    b('Rear_bumper',0,2.33,.56,2.45,.13,.12,'cyan')
    # Original small front plate, kept as pixel colors.
    before=set(geo.collections[geo.active].objects)
    source_patch(geo,root/'source/room 016.png',(293,88,314,96),(0,0,.70),(.54,.18),'Car_source_plate')
    for o in set(geo.collections[geo.active].objects)-before:
        o.rotation_euler.z=-math.pi/2;o.location=(cx-2.69,cy,0)
    # Slim red/brown storage rack along the far side, outside the hatch landing.
    for x in [6.05,9.75]:box('Garage_shelf_upright',(x,7.0,1.28),(.09,.5,2.56),'red')
    for z in [.2,.86,1.52,2.18,2.55]:box('Garage_shelf',(7.9,7.0,z),(3.8,.62,.065),'brown')
    for x in [6.45,6.9,8.75]:
        geo.cyl('Garage_tin',(x,6.99,.99),.12,.2,'gray')
        geo.cyl('Garage_tin_lid',(x,6.99,1.10),.125,.025,'cyan')
    box('Garage_tool_case',(8.1,7,1.68),(.65,.34,.25),'darkgray')
    # Open shutter tracks and overhead stacked slats, never an invisible closed door.
    for y in [1.67,6.33]:box('Shutter_track',(4.22,y,1.48),(.1,.08,2.9),'gray')
    for i in range(10):box('Raised_shutter_slat',(4.3+i*.17,4,3.16),(.13,4.65,.045),'gray')
    for i in range(7):box('Facade_vertical_flute',(4.0,.64+i*.13,1.5),(.025,.035,2.98),'black')
