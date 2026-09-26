"""Continue reference wall finishes onto inferred front walls, without copying props.

Runs after furnishing/rear anchoring. Repeated joinery uses linked mesh data;
new wallpaper is batched by material. Front door apertures remain clear.
"""
import math
import random
import bpy
from mathutils import Matrix

# Only seamless architectural finishes: no openings, lights, furniture or decals.
COPIES = {
    'heart_bedroom': ('Staggered_heart_wallpaper', 'Rear_ceiling_cornice', 'Rear_wall_base_rail'),
    'tentacle_room': ('Music_wall_stripes', 'Music_wainscot', 'Wainscot_stile', 'Wainscot_panel_edge', 'Wainscot_rail'),
    'mummy_room': ('Exercise_wainscot', 'Exercise_wall_rail'),
    'music_room': ('Pilaster', 'Column_flute', 'Column_capital', 'Pink_wall_panel', 'White_dado', 'Dado_rail', 'Dado_panel_outline', 'Dado_panel_inset'),
    'dining_room': ('Wall_panel', 'Wainscot_groove', 'Wainscot_highlight', 'Wall_rail'),
    'kitchen': ('Tile_gold', 'Tile_red', 'Tile_brown_motif'),
}
PROCEDURAL = {'living_room', 'cellar', 'security_hall', 'windowed_hall', 'upper_corridor',
              'typewriter_room', 'wire_attic', 'under_house', 'pantry', 'mummy_bathroom'}
ROOMS = set(COPIES) | PROCEDURAL


def apply(g, c):
    room = c['id']
    if room not in ROOMS:
        return
    cfg = c['geometry']; W = cfg['halfWidth']; D = cfg['depth']
    T = cfg.get('wallThickness', 0); H = cfg.get('height', 3.5)
    y = T + c.get('shell', {}).get('frontOffset', 0)
    ports = {p['id']: p for p in c['ports']}
    holes = [ports[e['port']] for e in c.get('shell', {}).get('entries', []) if e['wall'] == 'front']
    before = set(bpy.data.objects)
    g.active = 'Architecture'
    # Existing generic skirting would hide the original lower panels/tiles.
    for obj in list(bpy.data.objects):
        if room != 'windowed_hall' and obj.name.startswith(('Skirting', 'Front_skirting')) and obj.location.y < y + .08:
            bpy.data.objects.remove(obj, do_unlink=True)
    bpy.context.view_layer.update()
    if room in COPIES:
        if holes:
            raise ValueError('Copied wall finish requires an aperture-aware style: ' + room)
        transform = Matrix.Translation((0, D + c.get('shell', {}).get('frontOffset', 0), 0)) @ Matrix.Rotation(math.pi, 4, 'Z')
        originals = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith(COPIES[room])]
        if not originals:
            raise ValueError('Missing reference wall finish: ' + room)
        for obj in originals:
            duplicate = obj.copy()
            duplicate.name = 'Front_inferred_' + obj.name
            duplicate['opposite_wall_finish'] = True
            obj.users_collection[0].objects.link(duplicate)
            duplicate.matrix_world = transform @ obj.matrix_world
        return

    batches = {}
    def rect(name, x0, x1, z0, z1, color, offset=.008):
        """Clip flat finish rectangles to room bounds and exact front door holes."""
        x0=max(-W+T,x0); x1=min(W-T,x1); z0=max(0,z0); z1=min(H,z1)
        if x1<=x0 or z1<=z0:return
        xs=sorted({x0,x1,*[max(x0,min(x1,p['position'][0]+s*(p['width']/2+.015))) for p in holes for s in [-1,1]]})
        zs=sorted({z0,z1,*[max(z0,min(z1,p['position'][2]+h)) for p in holes for h in [0,p['height']+.015]]})
        vs,fs=batches.setdefault((name,color,offset),([],[]))
        for a,b in zip(xs,xs[1:]):
            for low,high in zip(zs,zs[1:]):
                if any(abs((a+b)/2-p['position'][0])<p['width']/2+.015 and p['position'][2]<=(low+high)/2<p['position'][2]+p['height']+.015 for p in holes):continue
                n=len(vs);vs.extend([(a,y+offset,low),(a,y+offset,high),(b,y+offset,high),(b,y+offset,low)]);fs.append((n,n+1,n+2,n+3))
    def rail(z, color, height=.04):
        rect('Rail',-W,W,z-height/2,z+height/2,color,.018)
    def panels(top, color='brown', spacing=1.5):
        rect('Wainscot',-W,W,.04,top,color,.01)
        rail(.10,'red');rail(top-.05,'red');rail(top+.02,'yellow',.025)
        for i in range(math.ceil(2*(W-T)/spacing)):
            a=-W+T+i*spacing+.06;b=min(a+spacing-.12,W-T-.06)
            for z in [.20,top-.15]:rect('Panel_border',a,b,z,z+.023,'red',.025)
            for x in [a,b]:rect('Panel_stile',x,x+.023,.20,top-.127,'red',.025)
    rng=random.Random(731)
    if room=='living_room':
        for i in range(83):
            x=-6.35+i*.155
            rect('Wallpaper_ink',x-.025,x+.025,.40,3.48,'black',.021)
            rect('Wallpaper_gold',x+.031,x+.047,.40,3.48,'brown',.037)
        for z,h,col in [(.10,.16,'red'),(.23,.045,'black'),(.28,.035,'yellow'),(3.45,.06,'brown')]:rail(z,col,h)
    elif room=='cellar':
        rect('Plaster',-W,W,0,H,'gray')
        for x in [-7.4,-5.3,-2.4,.2,2.8,4.95]:rect('Plaster_seam',x,x+.018,0,H,'darkgray',.013)
        for z in [.35,1.05]:rail(z,'darkgray',.018)
    elif room=='mummy_bathroom':
        for row in range(5):
            z=.18+row*.22
            for i in range(math.ceil((2*W-2*T)/.36)):
                x=-W+T+.18+i*.36
                rect('Wall_tile',x-.17,x+.17,z-.1,z+.1,'aqua',.024)
                for dx,dz in [(-.08,.04),(.05,-.045),(.09,.055)]:rect('Tile_speck',x+dx-.013,x+dx+.013,z+dz-.0155,z+dz+.0155,'cyan',.026)
    elif room in {'security_hall','windowed_hall','upper_corridor'}:
        if room=='upper_corridor':
            rect('Wainscot',-W,W,.04,.92,'brown',.01)
            for z,col in [(.08,'red'),(.83,'red'),(.94,'yellow')]:rail(z,col)
            for i in range(math.ceil((2*W-2*T)/2.04)+1):
                x=-W+T+.07+i*2.04
                rect('Panel_stile',x-.019,x+.019,.085,.855,'yellow',.025)
            # Same fine diamond lattice as the rear, without its lamp-light patches.
            vs=[];fs=[]
            for i in range(int((2*W-2*T)/.166)):
                x=-W+T+.08+i*.166
                for j in range(13):
                    z=1.05+j*.162
                    for s in [-1,1]:
                        n=len(vs);vs.extend([(x-.075,y+.008,z-s*.08),(x-.067,y+.008,z-s*.08),(x+.075,y+.008,z+s*.08),(x+.067,y+.008,z+s*.08)]);fs.append((n,n+1,n+2,n+3))
            g.mesh('Front_inferred_Diamond_lattice',vs,[tuple(reversed(f)) for f in fs],'lightblue')
        elif room=='security_hall':
            for i in range(math.ceil((2*W-2*T)/.091)):
                x=-W+T+.045+i*.091
                for j in range(30):
                    z=.35+j*.089
                    rect('Wallpaper',x-.0215,x+.0215,z-.0225,z+.0225,'blue')
                    rect('Wallpaper_highlight',x-.006,x+.006,z-.0065,z+.0065,'gray',.010)
            for z,col in [(.21,'red'),(.30,'yellow'),(3.03,'red')]:rail(z,col,.07)
        else:
            for i in range(math.ceil((2*W-2*T)/.225)):
                x=-W+T+.112+i*.225
                for j in range(12):
                    z=.37+j*.225
                    rect('Wallpaper_cross',x-.016,x+.016,z-.09,z+.09,'aqua')
                    rect('Wallpaper_cross',x-.09,x+.09,z-.016,z+.016,'aqua')
                    for dx in [-.052,.052]:
                        for dz in [-.052,.052]:rect('Wallpaper_dots',x+dx-.018,x+dx+.018,z+dz-.018,z+dz+.018,'aqua')
    elif room=='typewriter_room':
        from pathlib import Path
        from .furnishings import source_patch
        # Repeat the unobstructed original paper at its authored pixel scale.
        # Its horizontal repeat is nine pixels; 135 keeps tile joins seamless.
        pitch=5.55/137; x=-W+T
        while x<W-T-.001:
            pixels=min(135,max(1,int((W-T-x)/pitch)))
            width=min(pixels*pitch,W-T-x)
            patch_before=set(bpy.data.objects)
            source_patch(g,Path(__file__).resolve().parents[2]/'source/room 027.png',(176,8,176+pixels,64),(0,0,2.14),(width,1.87),'Front_inferred_Den_wallpaper')
            for obj in set(bpy.data.objects)-patch_before:obj.matrix_world=Matrix.Translation((x+width/2,y+.013,0))@Matrix.Rotation(math.pi,4,'Z')@obj.matrix_world
            x+=width
        panels(1.10)
    elif room=='under_house':
        rect('Board_backing',-W,W,0,2.20,'black')
        for row in range(10):rect('Timber_board',-W,W,row*.22+.006,row*.22+.213,'darkgray',.012)
        for i in range(2300):
            x=rng.uniform(-W+T,W-T);z=rng.uniform(.06,2.17)
            rect('Timber_grain',x,x+rng.uniform(.015,.12),z,z+rng.uniform(.006,.016),rng.choice(['gray','cyan','black']),.016)
        rail(.045,'brown',.09)
    elif room in {'pantry','wire_attic'}:
        # New irregular plaster loss, not the same source damage mirrored twice.
        base='gray' if room=='pantry' else 'cyan'
        rect('Plaster',-W,W,0,H,base)
        def polygon(name, points, color, offset):
            step=.025
            low=max(0,min(z for x,z in points)); high=min(H,max(z for x,z in points))
            for row in range(math.ceil((high-low)/step)):
                z=low+(row+.5)*step
                cuts=[]
                for (ax,az),(bx,bz) in zip(points,points[1:]+points[:1]):
                    if min(az,bz)<=z<max(az,bz):cuts.append(ax+(bx-ax)*(z-az)/(bz-az))
                cuts.sort()
                for left,right in zip(cuts[::2],cuts[1::2]):rect(name,left,right,z-step/2,z+step/2,color,offset)
        def crack(points):
            for (ax,az),(bx,bz) in zip(points,points[1:]):
                count=max(1,math.ceil(math.hypot(bx-ax,bz-az)/.018))
                for i in range(count):
                    t=(i+.5)/count;x=ax+(bx-ax)*t;z=az+(bz-az)*t
                    rect('Plaster_crack',x-.008,x+.008,z-.012,z+.012,'black',.021)
        if room=='wire_attic':
            polygon('Peeling_gray_plaster',[(-W,H),(-.8,H),(-1.4,2.61),(-.63,2.28),(-1.7,1.86),(-2.42,1.97),(-W,1.29)],'darkgray',.011)
            patches=[(-W*.56,.66,1.2,.59),(W*.40,1.31,.90,.74),(W*.83,2.76,.69,.57)]
            crack([(-.44,3.12),(-.12,2.48),(-.48,2.1),(.10,1.67),(-.19,1.30)])
            crack([(W,1.14),(W-.55,1.47),(W-.79,2.09),(W-1.22,2.3)])
        else:
            patches=[(-W*.67,2.73,.72,.58),(W*.52,.59,.65,.51)]
            crack([(-.8,2.65),(-1.03,2.30),(-.66,1.95),(-.84,1.55)])
            crack([(1.39,1.09),(1.1,1.44),(1.41,1.80),(1.20,2.07)])
        # Angular, torn outlines; do not turn plaster loss into round spots.
        outlines=[
            [(-1,-1),(-.56,-.50),(-.73,-.20),(-.26,.13),(-.49,.56),(-.18,1),(1,1),(.76,.50),(.90,.15),(.47,-.23),(.68,-.65),(.34,-1)],
            [(-1,-.73),(-.73,-.31),(-.81,.08),(-.44,.34),(-.56,.78),(-.12,1),(.18,.53),(.65,.65),(.44,.15),(1,-.12),(.69,-.50),(.86,-1),(-.38,-1)],
            [(-1,-1),(-.72,-.59),(-.9,-.14),(-.45,.06),(-.51,.44),(.04,.39),(.14,1),(.60,.83),(.39,.30),(1,.14),(1,-1)],
        ]
        for index,(cx,cz,rx,rz) in enumerate(patches):
            points=[(cx+(x+rng.uniform(-.09,.09))*rx,cz+(z+rng.uniform(-.06,.06))*rz) for x,z in outlines[index]]
            polygon('Plaster_edge',[(cx+(x-cx)*1.06,cz+(z-cz)*1.06) for x,z in points],'darkgray',.012)
            step=.025
            for row in range(math.ceil(2*rz/step)):
                z=cz-rz+(row+.5)*step;cuts=[]
                for (ax,az),(bx,bz) in zip(points,points[1:]+points[:1]):
                    if min(az,bz)<=z<max(az,bz):cuts.append(ax+(bx-ax)*(z-az)/(bz-az))
                if len(cuts)<2:continue
                left=min(cuts);right=max(cuts)
                rect('Exposed_joints',left,right,z-step/2,z+step/2,'black',.014)
                if room=='pantry':
                    course=int(z/.14);joint=(course%2)*.18
                    for i in range(-30,31):
                        a=max(left,i*.36+joint+.013);b=min(right,(i+1)*.36+joint-.013)
                        if b>a and z%.14>.025:rect('Exposed_brick',a,b,z-step/2,z+step/2,'brown' if (i+course)%3 else 'red',.017)
                elif z%.14>.020:
                    rect('Exposed_laths',left,right,z-step/2,z+step/2,'brown' if int(z/.14)%2 else 'red',.017)
        if room=='wire_attic':
            # Dampness hangs from the ceiling in uneven clusters, rather than
            # scattering identical bright streaks across the whole plaster face.
            for center,span in [(-W*.80,.32),(W*.12,.18),(W*.74,.43)]:
                for i in range(14):
                    x=center+rng.uniform(-span,span);top=H-rng.uniform(.01,.09)
                    rect('Damp_streak',x,x+rng.uniform(.012,.025),top-rng.uniform(.035,.27),top,rng.choice(['green','lime']),.019)
    for (name,color,offset),(vs,fs) in batches.items():
        if fs:g.mesh('Front_inferred_'+name,vs,fs,color)

    for obj in set(bpy.data.objects) - before:
        obj['opposite_wall_finish'] = True
