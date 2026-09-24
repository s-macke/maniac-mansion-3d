"""Room 016: static EGA car, shelving and raised shutter hardware."""
import math
from blender_shared.furnishings import source_patch,curved_line


def furnish(geo,root):
    box=geo.box
    # Rear faces the open forecourt (-X), as in 016; the nose points into the bay.
    # u runs across the car, v along it.
    cx,cy=8.45,4.6
    def b(name,u,v,z,w,l,h,color):return box(name,(cx+v,cy+u,z),(l,w,h),color)
    def mesh(name,vertices,faces,color):return geo.mesh(name,[(cx+v,cy+u,z) for u,v,z in vertices],faces,color)
    def wheel(name,u,v):
        # Axle along Y; black tire with gray inset hub.
        for radius,width,offset,color in [(.43,.26,0,'black'),(.25,.025,.145,'gray'),(.11,.03,.163,'darkgray')]:
            verts=[(cx+v+radius*math.cos(i*math.tau/20),cy+u+s*width/2+math.copysign(offset,u),.45+radius*math.sin(i*math.tau/20)) for s in [-1,1] for i in range(20)]
            geo.mesh(name,verts,[tuple(reversed(range(20))),tuple(range(20,40))]+[(i,(i+1)%20,(i+1)%20+20,i+20) for i in range(20)],color)
    b('Car_chassis',0,0,.44,2.3,4.7,.20,'black')
    # Tapered red shell, with the trunk towards the forecourt and hood inside.
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
    cabin=[(u,-v,z) for u,v,z in cabin]
    mesh('Car_windows',cabin,[(4,5,1,0),(5,6,2,1),(7,4,0,3)],'black')
    mesh('Car_rear_glass',cabin,[(6,7,3,2)],'darkgray')
    before=set(geo.collections[geo.active].objects)
    source_patch(geo,root/'source/room 016.png',(237,49,295,68),(0,0,1.31),(1.50,.38),'Rear_window_detail',only={'cyan','aqua','yellow','white','black','gray'})
    for obj in set(geo.collections[geo.active].objects)-before:
        for vert in obj.data.vertices:
            u,z=vert.co.x,vert.co.z
            vert.co=(cx-1.33+.39*(z-1)/.62-.001,cy-u,z)

    mesh('Car_roof',cabin,[(7,6,5,4)],'red')
    for a,bb in [(0,4),(1,5),(2,6),(3,7),(4,5),(6,7),(0,1),(2,3)]:
        u,v,z=cabin[a];uu,vv,zz=cabin[bb];geo.beam('Car_window_trim',(cx+v,cy+u,z),(cx+vv,cy+uu,zz),.04,'cyan')
    for u in [-1.035,1.035]:
        geo.beam('Car_window_pillar',(cx-.5,cy+u,1.02),(cx-.5,cy+math.copysign(.82,u),1.62),.055,'red')
        b('Car_door_handle',u,-.2,.93,.025,.25,.045,'gray')
        b('Car_side_chrome',u*1.24,0,.73,.035,3.9,.045,'aqua')
    # The visible red panel is the trunk, not a grille. Cyan round taillight
    # housings and tall rear fins preserve the unusual silhouette in the artwork.
    b('Trunk_rear_outline',0,-2.47,.78,1.90,.065,.34,'black')
    b('Trunk_rear_panel',0,-2.51,.79,1.80,.035,.27,'red')
    b('Trunk_handle',0,-2.54,.86,.34,.04,.035,'gray')
    for side in [-1,1]:
        pts=[(side*u,-2.534,z) for u,z in [(.16,.87),(.28,.90),(.56,.915),(.83,.90)]]
        curved_line(geo,'Rear_shoulder_chrome',[(cx+v,cy+u,z) for u,v,z in pts],.022,'aqua')
    mesh('Trunk_wing_badge',[(-.39,-2.550,.825),(.39,-2.550,.825),(.12,-2.550,.795),(0,-2.550,.765),(-.12,-2.550,.795)],[(0,1,2,3,4)],'aqua')
    b('Trunk_lid_seam',0,-1.81,1.032,1.92,1.10,.012,'black')
    b('Trunk_lid',0,-1.81,1.043,1.86,1.04,.015,'red')
    b('Rear_bumper',0,-2.56,.52,2.65,.18,.14,'cyan')
    b('Rear_bumper_highlight',0,-2.651,.57,2.61,.002,.035,'aqua')
    for u in [-1.2,1.2]:
        geo.sphere('Taillight_pod',(cx-2.18,cy+u,.99),(.53,.29,.24),'cyan')
        for radius,xx,color in [(.23,cx-2.63,'aqua'),(.16,cx-2.66,'black'),(.095,cx-2.68,'gray')]:
            geo.mesh('Taillight_disc',[(xx,cy+u+radius*math.cos(i*math.tau/24),.99+radius*math.sin(i*math.tau/24)) for i in range(24)],[tuple(reversed(range(24)))],color)
        mesh('Car_rear_fin',[(u,-1.1,.92),(u,-2.24,.92),(u,-2.18,1.52),(u*.93,-1.1,.92),(u*.93,-2.24,.92),(u*.93,-2.18,1.52)],[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],'cyan')
        # Unseen nose stays simple; its lamps point into the garage.
        b('Front_headlamp',u,2.27,.83,.22,.035,.14,'gray')
    b('Front_bumper',0,2.33,.56,2.45,.13,.12,'cyan')
    # Bumper guards and a solid plate bracket attach to the rear body.
    for u in [-.54,.54]:
        b('Rear_bumper_guard',u,-2.64,.63,.055,.15,.28,'cyan')
        b('Bumper_guard_glint',u+.010,-2.717,.64,.016,.005,.26,'aqua')
    b('Rear_plate_bracket',0,-2.60,.70,.58,.18,.20,'cyan')
    # Original EDSEL plate belongs on the rear, facing the forecourt.
    before=set(geo.collections[geo.active].objects)
    source_patch(geo,root/'source/room 016.png',(293,88,314,96),(0,0,.70),(.54,.18),'Car_source_plate')
    for o in set(geo.collections[geo.active].objects)-before:
        o.rotation_euler.z=-math.pi/2;o.location=(cx-2.691,cy,0)
    # Small original white/red bumper sticker beside the rear plate.
    before=set(geo.collections[geo.active].objects)
    source_patch(geo,root/'source/room 016.png',(250,96,271,104),(0,0,.54),(.46,.175),'Car_bumper_sticker')
    for o in set(geo.collections[geo.active].objects)-before:
        o.rotation_euler.z=-math.pi/2;o.location=(cx-2.653,cy+.82,0)
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
