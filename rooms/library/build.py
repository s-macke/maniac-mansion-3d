"""Room 005: book-lined library, reading corner and decorative spiral stair."""
from pathlib import Path
import sys,math,random,bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from blender_shared.layout_shell import build
from blender_shared.furnishings import panel,curved_line,source_patch


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
    # Clear the plant bay after generating books so all other book colors stay stable.
    for obj in list(bpy.data.objects):
        if obj.name.startswith(('Book_spine','Book_binding')) and obj.location.x>4.12 and 1.56<obj.location.z<2.31:
            bpy.data.objects.remove(obj,do_unlink=True)
    # Low red/yellow pot and spreading green leaves on the middle shelf.
    px,py=4.65,4.85
    geo.sphere('Shelf_plant_pot',(px,py,1.73),(.30,.18,.12),'yellow')
    geo.sphere('Shelf_pot_red_base',(px,py,1.64),(.24,.145,.035),'red')
    geo.cyl('Shelf_pot_rim',(px,py,1.84),.27,.045,'red')
    for side in [-1,1]:
        for k in range(3):
            tip=px+side*(.30+k*.09)
            curved_line(geo,'Shelf_plant_leaf',[(px+side*(.36*t*(1-t)+abs(tip-px)*t*t),py-.045*k*t,1.85*(1-t)**2+2*(2.15+k*.02)*t*(1-t)+(1.91-k*.035)*t*t) for t in [j/8 for j in range(9)]],.035,'green')
    box('Bookcase_crown',(0,4.81,3.065),(10.92,.74,.11),'brown')
    # Real ceiling aperture and a closed, black shaft conceal the stair destination.
    cx,cy=-.1,3.05
    ceiling=config['geometry']['height'];shaft_top=5.75
    hole=config['geometry']['ceilingHoles'][0]
    x0,x1,y0,y1=[hole[k] for k in ['x0','x1','y0','y1']]
    for x in [x0-.05,x1+.05]:
        box('Mystery_shaft_side',(x,cy,(ceiling+shaft_top)/2),(.10,y1-y0+.20,shaft_top-ceiling),'black')
        box('Stair_opening_side_trim',(x,cy,ceiling-.035),(.10,y1-y0+.20,.07),'brown')
    for y in [y0-.05,y1+.05]:
        box('Mystery_shaft_end',(cx,y,(ceiling+shaft_top)/2),(x1-x0,.10,shaft_top-ceiling),'black')
        box('Stair_opening_end_trim',(cx,y,ceiling-.035),(x1-x0,.10,.07),'brown')
    box('Mystery_shaft_dark_end',(cx,cy,shaft_top+.025),(x1-x0+.20,y1-y0+.20,.05),'black')
    def stair_shade(z,base='brown'):
        if z<ceiling:return base
        # Pre-shaded brown fades to black inside the shaft, with no runtime effect.
        key=f'Stair_dark_{base}_{z:.3f}'
        if key not in geo.mats:
            mat=geo.mats[base].copy();mat.name=key
            factor=max(0,1-(z-ceiling)/1.5)**3*.42
            mat.diffuse_color=tuple(v*factor for v in mat.diffuse_color[:3])+(1,)
            geo.mats[key]=mat
        return key
    def shaded(obj,z):
        if z>=ceiling:obj['bake_unlit']=True
        return obj
    geo.cyl('Spiral_central_column',(cx,cy,1.56),.26,3.12,'brown',20)
    for i in range(18):
        z=ceiling+(i+.5)*.143
        shaded(geo.cyl('Spiral_column_in_dark',(cx,cy,z),.26,.143,stair_shade(z),20),z)
    outer=[]
    for i in range(34):
        a=-math.pi/2+i*math.tau/25;b=a+math.tau/25;z=.12+i*.143
        vs=[(cx+r*math.cos(t),cy+r*math.sin(t),zz) for zz in [z-.08,z] for r,t in [(.2,a),(1.45,a),(1.45,b),(.2,b)]]
        shaded(geo.mesh('Spiral_tread',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],stair_shade(z)),z)
        shaded(geo.beam('Spiral_tread_edge',vs[5],vs[6],.035,stair_shade(z,'yellow')),z)
        band=[(cx+1.47*math.cos(t),cy+1.47*math.sin(t),h) for t,h in [(a,max(.02,z-.25)),(b,max(.02,z+.143-.25)),(b,z+.143),(a,z)]]
        shaded(geo.mesh('Spiral_outer_stringer',band,[(0,1,2,3)],stair_shade(z)),z)
        p=(cx+1.45*math.cos(a),cy+1.45*math.sin(a),z)
        # Split each baluster so it also disappears gradually above the ceiling.
        for j in range(4):
            za=z+j*.17;zb=za+.17
            shaded(geo.beam('Spiral_baluster',(p[0],p[1],za),(p[0],p[1],zb),.045,stair_shade((za+zb)/2)),(za+zb)/2)
        outer.append((p[0],p[1],z+.68))
    for a,b in zip(outer,outer[1:]):
        z=(a[2]+b[2])/2
        shaded(geo.beam('Spiral_handrail',a,b,.085,stair_shade(z)),z)
    # Small sign suspended from the lower rail in background 005.
    # Preserve its illegible lettering as original pixels rather than guessing text.
    anchor=Vector(outer[1]);sx,sy=anchor.x,anchor.y-.11
    sw,sh=.42,.252;sz=anchor.z-.34
    box('Stair_sign_board',(sx,sy,sz),(sw,.028,sh),'gray')
    box('Stair_sign_reverse',(sx,sy+.0145,sz),(sw-.018,.001,sh-.018),'white')
    source_patch(geo,ROOT/'source/room 005.png',(308,86,322,93),(sx,sy-.0145,sz),(sw,sh),'Original_stair_sign')
    curved_line(geo,'Stair_sign_hanger',[(sx-sw*.38,sy,sz+sh/2),(anchor.x,anchor.y-.075,anchor.z),(sx+sw*.38,sy,sz+sh/2)],.007,'gray')
    # Reading chair, phone table and slim standing lamps.
    def upholstered(name,loc,size,bevel):
        obj=box(name,loc,size,'black')
        modifier=obj.modifiers.new('Soft_upholstery_edges','BEVEL');modifier.width=bevel;modifier.segments=3
        bpy.context.view_layer.objects.active=obj;obj.select_set(True);bpy.ops.object.modifier_apply(modifier=modifier.name);obj.select_set(False)
        return obj
    upholstered('Armchair_seat',(4.85,2.1,.48),(1.25,1.05,.27),.10)
    back=upholstered('Armchair_back',(4.85,2.57,1.03),(1.1,.3,1.16),.10);back.rotation_euler.x=-.14
    for x in [4.23,5.47]:
        upholstered('Armchair_arm',(x,2.08,.72),(.22,1.18,.5),.10)
        # Thin gray piping outlines the rolled fronts, as in the black source chair.
        pts=[(x+.084*math.cos(t),1.486,.77+.145*math.sin(t)) for t in [i*math.pi/12 for i in range(13)]]
        curved_line(geo,'Armchair_arm_piping',pts,.010,'darkgray')
    bpy.context.view_layer.update()
    pts=[(-.40,-.152,-.40),(-.43,-.152,.36),(-.37,-.152,.47),(.37,-.152,.47),(.43,-.152,.36),(.40,-.152,-.40)]
    curved_line(geo,'Armchair_back_piping',[back.matrix_world@Vector(p) for p in pts],.010,'darkgray')
    curved_line(geo,'Armchair_seat_piping',[(4.32,1.58,.54),(4.40,1.568,.59),(5.30,1.568,.59),(5.38,1.58,.54)],.010,'darkgray')
    for x in [4.4,5.3]:
        for y in [1.72,2.47]:box('Armchair_foot',(x,y,.15),(.1,.1,.3),'brown')
    panel(geo,'Telephone_table_front',3.65,1.8,.3,.7,.38)
    box('Telephone_table_top',(3.65,2.1,.57),(.82,.68,.1),'brown')
    for x in [3.32,3.98]:
        for y in [1.86,2.34]:box('Telephone_table_leg',(x,y,.25),(.07,.07,.5),'brown')
    box('Telephone_base',(3.65,2.1,.68),(.48,.34,.13),'green')
    curved_line(geo,'Telephone_receiver',[(3.41,2.13,.79),(3.44,2.13,.84),(3.50,2.13,.86),(3.80,2.13,.86),(3.86,2.13,.84),(3.89,2.13,.79)],.065,'green')
    for x in [3.43,3.87]:geo.sphere('Telephone_earpiece',(x,2.13,.79),(.08,.08,.05),'green')
    geo.cyl('Telephone_rotary_plate',(3.65,2.02,.752),.093,.015,'cyan',20)
    for i in range(10):
        a=i*math.tau/10;geo.cyl('Telephone_dial_hole',(3.65+.066*math.cos(a),2.02+.066*math.sin(a),.762),.014,.006,'black',8)
    curved_line(geo,'Telephone_coiled_cord',[(3.91+.018*math.cos(i*math.pi/2),2.12+i*.007,.75-.24*math.sin(i/40*math.pi)+.018*math.sin(i*math.pi/2)) for i in range(41)],.009,'black')
    for x,y in [(-5.1,3.8),(5.55,3.6)]:
        geo.cyl('Floor_lamp_base',(x,y,.06),.22,.1,'brown')
        geo.cyl('Floor_lamp_stem',(x,y,1.03),.027,1.95,'black')
        geo.mesh('Floor_lamp_shade',[(x+r*math.cos(i*math.tau/12),y+r*math.sin(i*math.tau/12),z) for z,r in [(1.85,.06),(2.18,.23)] for i in range(12)],[(i,(i+1)%12,(i+1)%12+12,i+12) for i in range(12)],'white')
        glow=geo.sphere('Floor_lamp_glow',(x,y,2.13),(.12,.12,.08),'yellow');glow['bake_unlit']=True;glow['bake_no_shadow']=True

build(Path(__file__).with_name('room.json'),furnish)

# Reverse review camera stands in the clear right aisle, outside the bookcase.
camera=bpy.data.objects['03_Reverse'];camera.location=(5.95,1.0,1.62)
camera.rotation_euler=(Vector((3.9,4.7,1.4))-camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
