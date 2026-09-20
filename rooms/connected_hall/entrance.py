"""Generate entrance geometry in memory as the first stage of the combined hall."""
import bpy, math
from pathlib import Path
from mathutils import Vector


def build_entrance():
    """Start a clean scene and create the original EGA entrance, without file outputs."""
    ROOT = Path(__file__).resolve().parents[2]
    bpy.ops.wm.read_factory_settings(use_empty=False)
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    for m in list(bpy.data.materials):bpy.data.materials.remove(m)
    bpy.context.preferences.filepaths.save_version=0
    scene=bpy.context.scene
    scene.unit_settings.system='METRIC'
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32
    scene.cycles.use_denoising=False
    scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
    scene.view_settings.exposure=0;scene.view_settings.gamma=1
    scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
    scene.render.resolution_percentage=100
    scene.render.image_settings.color_mode='RGB'
    scene.render.fps=30
    
    def linear(v):
     v=v/255;return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
    colors={'black':(0,0,0),'red':(168,0,0),'brown':(168,84,0),'yellow':(252,252,84),
    'cyan':(0,168,168),'aqua':(84,252,252),'gray':(168,168,168),'darkgray':(84,84,84),
    'white':(252,252,252),'pink':(252,84,252),'purple':(168,0,168),'green':(0,168,0),
    'lime':(84,252,84),'blue':(0,0,168),'salmon':(252,84,84)}
    mats={}
    for name,rgb in colors.items():
     m=bpy.data.materials.new('EGA_'+name);m.diffuse_color=(*[linear(c) for c in rgb],1)
     m.use_nodes=True;n=m.node_tree.nodes;n.clear();s=n.new('ShaderNodeEmission');s.inputs['Color'].default_value=m.diffuse_color
     o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(s.outputs[0],o.inputs['Surface']);mats[name]=m
    atlas=bpy.data.images.load(str(ROOT/'source/room 010.png'));atlas.pack()
    atlasmat=bpy.data.materials.new('Original_room010_pixels_UNLIT');atlasmat.use_nodes=True
    n=atlasmat.node_tree.nodes;n.clear();tex=n.new('ShaderNodeTexImage');tex.image=atlas;tex.interpolation='Closest';tex.extension='EXTEND'
    e=n.new('ShaderNodeEmission');o=n.new('ShaderNodeOutputMaterial');atlasmat.node_tree.links.new(tex.outputs['Color'],e.inputs['Color']);atlasmat.node_tree.links.new(e.outputs[0],o.inputs['Surface'])
    collections={}
    for name in ['Architecture','Doors','Staircase','Clock','Plants','Pixel_ornaments','Cameras','Collision','Reference']:
     c=bpy.data.collections.new(name);scene.collection.children.link(c);collections[name]=c
    active='Architecture'
    def put(obj,name,mat):
     obj.name=name
     for c in list(obj.users_collection):c.objects.unlink(obj)
     collections[active].objects.link(obj)
     if mat:obj.data.materials.append(mats[mat] if isinstance(mat,str) else mat)
     return obj
    
    def box(name,loc,size,mat):
     w,d,h=[v/2 for v in size]
     verts=[(x,y,z) for z in [-h,h] for y in [-d,d] for x in [-w,w]]
     o=mesh(name,verts,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat);o.location=loc;return o
    
    def mesh(name,verts,faces,mat):
     me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);collections[active].objects.link(o)
     if mat:me.materials.append(mats[mat] if isinstance(mat,str) else mat)
     return o
    
    def beam(name,a,b,width,mat):
     a,b=Vector(a),Vector(b);o=box(name,(a+b)/2,(width,width,(b-a).length),mat);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
    
    def cyl(name,loc,radius,depth,mat,vertices=12):
     bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc);return put(bpy.context.object,name,mat)
    
    def sphere(name,loc,scale,mat):
     bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=1,location=loc);o=put(bpy.context.object,name,mat);o.scale=scale;return o
    
    # Wall-local coordinates: x horizontal along wall, y inward offset, z vertical.
    # Wall-local positive y is behind the surface, so detail is placed at negative y.
    def localbox(name,u,y,z,w,d,h,mat,origin=(0,6.5),rot=0):
     o=box(name,(origin[0]+u*math.cos(rot)-y*math.sin(rot),origin[1]+u*math.sin(rot)+y*math.cos(rot),z),(w,d,h),mat)
     o.rotation_euler.z=rot;return o
    
    def wall(name,width,origin,rot,doors):
     # Fill above/between door openings, leaving actual apertures behind separate leaves.
     H=3.65
     cuts=sorted([(-width/2,-width/2,0)]+[(x-w/2,x+w/2,h) for x,w,h in doors]+[(width/2,width/2,0)])
     for i in range(len(cuts)-1):
      a,b=cuts[i][1],cuts[i+1][0]
      if b>a:localbox(name+'_shell', (a+b)/2,.11,H/2,b-a,.22,H,'cyan',origin,rot)
     for x,w,h in doors:localbox(name+'_header',x,.11,(H+h)/2,w,.22,H-h,'cyan',origin,rot)
     # Narrow alternating stripes stay geometric and retain exact palette from all angles.
     for i in range(int(width/.12)):
      u=-width/2+(i+.5)*.12
      z0=.92
      for x,w,h in doors:
       if abs(u-x)<w/2+.02:z0=max(z0,h)
      if z0<H:
       localbox(name+'_stripe',u,-.007,(z0+H)/2,.045,.016,H-z0,'aqua',origin,rot)
       localbox(name+'_stripe_ink',u-.036,-.009,(z0+H)/2,.017,.02,H-z0,'black',origin,rot)
     # Continuous wooden backing and clipped panels fill the wall beside jambs.
     spans=[(cuts[i][1],cuts[i+1][0]) for i in range(len(cuts)-1) if cuts[i+1][0]>cuts[i][1]]
     for a,b in spans:
      localbox(name+'_panel_backing',(a+b)/2,-.018,.43,b-a,.025,.84,'brown',origin,rot)
     count=int(width/.85);step=width/count
     for i in range(count):
      centre=-width/2+(i+.5)*step;nominal=step-.06
      for a,b in spans:
       left=max(centre-nominal/2,a+.025);right=min(centre+nominal/2,b-.025)
       w=right-left
       if w<.35:continue
       u=(left+right)/2
       localbox(name+'_panel_black',u,-.025,.43,w,.07,.84,'black',origin,rot)
       localbox(name+'_panel_red',u,-.065,.43,w-.035,.025,.80,'red',origin,rot)
       localbox(name+'_panel_gold',u,-.084,.43,w-.09,.018,.68,'yellow',origin,rot)
       localbox(name+'_panel_wood',u,-.097,.43,w-.14,.016,.62,'brown',origin,rot)
       localbox(name+'_panel_inset',u,-.107,.43,w-.27,.013,.44,'red',origin,rot)
       localbox(name+'_panel_center',u,-.12,.43,w-.32,.016,.39,'brown',origin,rot)
     for z,h,mat in [(.07,.13,'red'),(.84,.07,'black'),(.91,.06,'yellow'),(.97,.06,'brown'),(3.61,.07,'brown')]:
      for i in range(len(cuts)-1):
       a,b=cuts[i][1],cuts[i+1][0]
       if b>a:localbox(name+'_trim',(a+b)/2,-.08,z,b-a,.12,h,mat,origin,rot)
    
    wall('Back',12.8,(0,6.5),0,[(-3.72,1.30,2.83),(3.12,1.30,2.83)])
    wall('Left',6.5,(-6.4,3.25),math.pi/2,[(-.9,1.85,3.18)])
    wall('Right',6.5,(6.4,3.25),-math.pi/2,[(.1,1.05,2.75)])
    # Inferred fourth wall and ceiling close the room for interior exploration.
    wall('Front_inferred',12.8,(0,0),math.pi,[])
    front=[o for o in collections['Architecture'].objects if o.name.startswith('Front_inferred')]
    for o in front:o.hide_render=True;o['inferred_surface']=True
    floor=box('Red_floor',(0,3.25,-.1),(13.0,6.7,.2),'red')
    ceilings=[box('Ceiling_front_inferred',(0,1.9,3.78),(13,3.8,.2),'cyan'),
     box('Ceiling_left_inferred',(-4.0,5.15,3.78),(4.8,2.7,.2),'cyan'),
     box('Ceiling_right_inferred',(4.5,5.15,3.78),(3.8,2.7,.2),'cyan')]
    for ceiling in ceilings:ceiling.hide_render=True;ceiling['inferred_surface']=True
    # Tall enclosed stairwell above the cut ceiling; exit landing remains a placeholder.
    box('Stairwell_left',(-1.65,5.3,4.8),(.18,3.1,2.4),'cyan')
    box('Stairwell_right',(2.65,5.3,4.8),(.18,3.1,2.4),'cyan')
    box('Stairwell_back',(0.5,6.85,4.8),(4.48,.18,2.4),'cyan')
    box('Stairwell_top',(0.5,5.3,6.0),(4.48,3.1,.18),'cyan')
    upper_shell=[o for o in collections['Architecture'].objects if o.name.startswith('Stairwell_')]
    for o in upper_shell:o.hide_render=True
    
    print('Architecture built',flush=True)
    active='Doors'
    def door(name,u,width,height,origin,rot=0,double=False):
     for j,(extra,mat) in enumerate([(.21,'black'),(.13,'yellow'),(.06,'red')]):
      w=width+extra;thick=.038;y=-.10-j*.021
      for side in [-1,1]:
       o=localbox(name+'_jamb',u+side*(w/2-thick/2),y,height/2,thick,.025,height+.10,mat,origin,rot)
       o['destination']='Unresolved placeholder'
      localbox(name+'_lintel',u,y,height+.045-j*.027,w,.025,.035,mat,origin,rot)
     # Door leaves sit in front of the frame backing. Separate named mesh for later animation.
     leaves=2 if double else 1
     for k in range(leaves):
      lw=width/leaves-.035;lu=u+(k-(leaves-1)/2)*width/leaves
      leaf=localbox(name+'_leaf',lu,-.18,height/2,lw,.13,height-.10,'brown',origin,rot);leaf['is_door_leaf']=True
      for z,h in [(height*.68,height*.47),(height*.22,height*.29)]:
       for delta,inset,mat in [(0,0,'black'),(.012,.035,'yellow'),(.024,.075,'red'),(.036,.12,'brown')]:
        localbox(name+'_raised_panel',lu,-.255-delta,z,lw-.18-inset,.02,h-inset,mat,origin,rot)
      # Square pixel-like metal knob in real geometry.
      ku=lu+(lw*.34 if double and k==0 else -lw*.34)
      localbox(name+'_knob_ink',ku,-.32,height*.49,.11,.09,.11,'black',origin,rot)
      localbox(name+'_knob',ku-.013,-.38,height*.50,.06,.035,.06,'gray',origin,rot)
    door('Rear_left',-3.72,1.30,2.83,(0,6.5))
    door('Rear_right',3.12,1.30,2.83,(0,6.5))
    door('Front_double',-.9,1.85,3.18,(-6.4,3.25),math.pi/2,True)
    door('Right_side',.1,1.05,2.75,(6.4,3.25),-math.pi/2)
    
    active='Staircase'
    # A broad staircase sweeps to the right toward the implied upstairs landing.
    # Back wall ends at ceiling height; upper steps extend into the next room placeholder.
    N=21;rise=3.36/N
    centers=[]
    for i in range(N+1):
     t=i/N
     centers.append(Vector((-.55+1.30*math.sin(t*math.pi*.80),2.15+4.13*t,0)))
    widths=[2.10-.45*i/N for i in range(N+1)]
    left=[];right=[]
    for i,p in enumerate(centers):
     tangent=(centers[min(i+1,N)]-centers[max(i-1,0)]).normalized();across=Vector((tangent.y,-tangent.x,0))
     left.append(p-across*widths[i]/2);right.append(p+across*widths[i]/2)
    for i in range(N):
     z=(i+1)*rise
     a,b,c,d=left[i],right[i],right[i+1],left[i+1]
     verts=[(p.x,p.y,h) for h in [0,z] for p in [a,b,c,d]]
     mesh(f'Step_{i+1:02}',verts,[(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'brown')
     # Palette-defined riser shadow and thin gold tread edge.
     beam('Tread_ink',(a.x,a.y-.015,z+.012),(b.x,b.y-.015,z+.012),.047,'black')
     beam('Tread_gold',(a.x,a.y-.04,z+.033),(b.x,b.y-.04,z+.033),.022,'yellow')
     # Red runner across the middle, retaining brown edges.
     ac=a.lerp(b,.18);bc=a.lerp(b,.82);dc=d.lerp(c,.18);cc=d.lerp(c,.82)
     mesh('Red_carpet_tread',[(p.x,p.y,z+.01) for p in [ac,bc,cc,dc]],[(0,1,2,3)],'red')
     mesh('Red_carpet_riser',[(ac.x,ac.y-.005,z-rise),(bc.x,bc.y-.005,z-rise),(bc.x,bc.y-.005,z),(ac.x,ac.y-.005,z)],[(0,1,2,3)],'red')
    # Solid curved wooden side panels, as in the illustration; gold edges and dark outlines.
    for side in [left,right]:
     for i in range(N):
      a,b=side[i],side[i+1];z0=i*rise+.68;z1=(i+1)*rise+.68
      mesh('Curved_wood_balustrade',[(a.x,a.y,i*rise),(b.x,b.y,(i+1)*rise),(b.x,b.y,z1),(a.x,a.y,z0)],[(0,1,2,3)],'brown')
      beam('Rail_ink',(a.x,a.y,z0),(b.x,b.y,z1),.10,'black')
      beam('Rail_gold',(a.x,a.y,z0+.04),(b.x,b.y,z1+.04),.06,'yellow')
    for p in [left[0],right[0]]:
     box('Newel_base',(p.x,p.y,.11),(.46,.46,.22),'black')
     box('Newel_gold_base',(p.x,p.y,.19),(.41,.41,.10),'yellow')
     box('Newel_wood',(p.x,p.y,.51),(.32,.32,.58),'brown')
     box('Newel_cap',(p.x,p.y,.82),(.48,.46,.12),'yellow')
     sphere('Newel_gargoyle_body',(p.x,p.y,.98),(.16,.13,.16),'brown')
     for dx in [-.13,0,.13]:
      bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.065,radius2=0,depth=.24,location=(p.x+dx,p.y,1.15));put(bpy.context.object,'Newel_gargoyle_crown','yellow')
     # Black pixel-like eyes on 3D finial.
     for dx in [-.055,.055]:box('Finial_eye',(p.x+dx,p.y-.126,1.02),(.035,.02,.035),'black')
    box('Upper_landing_placeholder',(.74,6.35,3.28),(1.9,.55,.16),'brown')['destination']='011 landing, not modeled'
    
    # Pixel UV surface helper. Uses the packed, unchanged original image as an atlas.
    def pixel_face(name,rect,x,y,z,w,h):
     u0,v0,u1,v1=rect
     obj=mesh(name,[(x-w/2,y,z),(x+w/2,y,z),(x+w/2,y,z+h),(x-w/2,y,z+h)],[(0,1,2,3)],atlasmat)
     uv=obj.data.uv_layers.new();coords=[(u0/640,1-v1/128),(u1/640,1-v1/128),(u1/640,1-v0/128),(u0/640,1-v0/128)]
     for i,loop in enumerate(uv.data):loop.uv=coords[i]
     return obj
    
    print('Staircase built',flush=True)
    active='Clock'
    # Freestanding clock case, geometric side faces and original illustrated front.
    cx=-5.12;cy=5.96
    box('Clock_plinth',(cx,cy,.09),(.69,.40,.18),'black')
    box('Clock_foot_gold',(cx,cy-.01,.17),(.62,.40,.13),'yellow')
    box('Clock_case',(cx,cy,1.18),(.56,.35,2.05),'brown')
    box('Clock_case_ink',(cx,cy-.187,1.18),(.45,.02,1.96),'black')
    box('Clock_case_gold',(cx,cy-.206,1.18),(.37,.02,1.88),'yellow')
    box('Clock_case_red',(cx,cy-.22,1.18),(.30,.02,1.81),'red')
    box('Clock_pendulum_slot',(cx,cy-.236,1.09),(.20,.02,1.39),'black')
    beam('Clock_pendulum_rod',(cx,cy-.26,.49),(cx,cy-.26,1.60),.025,'yellow')
    sphere('Clock_pendulum',(cx,cy-.27,.46),(.075,.025,.09),'yellow')
    box('Clock_head',(cx,cy,2.32),(.70,.45,.67),'brown')
    box('Clock_head_ink',(cx,cy-.24,2.33),(.57,.02,.55),'black')
    sphere('Clock_face',(cx,cy-.27,2.34),(.235,.024,.235),'yellow')
    for i in range(12):
     t=i*math.tau/12
     box('Clock_hour',(cx+math.sin(t)*.175,cy-.303,2.34+math.cos(t)*.175),(.025,.014,.025),'black')
    beam('Clock_minute',(cx,cy-.32,2.34),(cx-.08,cy-.32,2.48),.027,'black')
    beam('Clock_hour_hand',(cx,cy-.325,2.34),(cx+.11,cy-.325,2.34),.03,'black')
    roof=[(cx-.40,cy-.25,2.66),(cx,cy-.25,2.98),(cx+.40,cy-.25,2.66)]
    mesh('Clock_pediment',roof,[(0,1,2)],'brown')
    for i in range(2):beam('Clock_pediment_trim',roof[i],roof[i+1],.045,'yellow')
    # Authentic pixel dial texture, kept as optional reference until its UV crop is verified.
    
    active='Plants'
    def plant(x,y):
     cyl('Pot_foot',(x,y,.08),.24,.12,'purple')
     sphere('Purple_pot',(x,y,.37),(.40,.36,.38),'pink')
     cyl('Pot_rim',(x,y,.65),.30,.14,'purple')
     cyl('Pot_soil',(x,y,.726),.24,.01,'black')
     # A source-like belt around the pot.
     cyl('Pot_belt',(x,y,.34),.39,.06,'purple')
     for j in range(9):
      t=j*math.tau/9;reach=.52+(j%3)*.11;top=1.15+(j%2)*.18
      start=Vector((x,y,.72));middle=Vector((x+math.cos(t)*reach*.5,y+math.sin(t)*reach*.5,top));end=Vector((x+math.cos(t)*reach,y+math.sin(t)*reach,top-.22))
      across=Vector((-math.sin(t),math.cos(t),0))*.10
      verts=[start,middle-across,end,middle+across,middle+Vector((0,0,.045))]
      obj=mesh('Angular_leaf',[tuple(v) for v in verts],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],'green')
      obj.data.materials.append(mats['lime']);obj.data.polygons[2].material_index=1
    plant(-2.25,4.99);plant(2.10,5.05)
    
    active='Pixel_ornaments'
    # Extract gray source gargoyles as opaque pixel relief. No rectangle/billboard background.
    # Runs of equal RGB form tiny extruded blocks; source pixels remain exact.
    pixels=list(atlas.pixels[:]);aw,ah=atlas.size
    reverse={tuple(rgb):name for name,rgb in colors.items()}
    def getpixel(x,y):
     k=((ah-1-y)*aw+x)*4
     return tuple(round(pixels[k+i]*255) for i in range(3))
    def relief(name,rect,cx,y,z,pitch=.026,allowed=None):
     u0,v0,u1,v1=rect
     if allowed is None:allowed={(84,84,84),(168,168,168),(252,252,252)}
     for v in range(v0,v1):
      u=u0
      while u<u1:
       color=getpixel(u,v);end=u+1
       while end<u1 and getpixel(end,v)==color:end+=1
       if color in allowed:
        box(name,(cx+((u+end)/2-(u0+u1)/2)*pitch,y,z+(v1-v-.5)*pitch*1.2),((end-u)*pitch,.075,pitch*1.2),reverse[color])
       u=end
    # Wall sconces visible between clock and doors. Gray-only segmentation excludes wallpaper.
    for cx,rect in [(-4.62,(140,5,154,43)),(-2.67,(210,5,226,43)),(2.18,(412,5,430,43)),(4.05,(481,5,499,43))]:
     relief('Original_pixel_sconce',rect,cx,6.30,2.42,.023)
    
    relief('Original_plaster_patch',(250,10,288,40),-1.65,6.28,2.45,.025,{(252,84,84),(168,0,0)})
    
    active='Collision'
    # Separate non-rendered proxies for a future viewer. Not exported in the visible GLB.
    box('COL_floor',(0,3.25,-.15),(12.8,6.5,.3),None)
    for name,loc,size in [('back',(0,6.62,1.8),(13,.2,3.6)),('left',(-6.52,3.25,1.8),(.2,6.5,3.6)),('right',(6.52,3.25,1.8),(.2,6.5,3.6)),('front',(0,-.12,1.8),(13,.2,3.6))]:
     box('COL_'+name,loc,size,None)
    for i in range(N):
     a,b,c,d=left[i],right[i],right[i+1],left[i+1]
     mesh('COL_stair_ramp',[(a.x,a.y,i*rise),(b.x,b.y,i*rise),(c.x,c.y,(i+1)*rise),(d.x,d.y,(i+1)*rise)],[(0,1,2,3)],None)
    for o in collections['Collision'].objects:o.hide_render=True;o.hide_set(True);o.display_type='WIRE'
    
    print('Geometry complete',flush=True)
    active='Cameras'
    def camera(name,loc,target,lens=26,ortho=None):
     bpy.ops.object.camera_add(location=loc);o=put(bpy.context.object,name,None);o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;o.data.clip_start=.05;o.data.clip_end=150
     if ortho:o.data.type='ORTHO';o.data.ortho_scale=ortho
     return o
    ref=camera('01_Reference',(0,-14,4.8),(0,4.6,1.65),lens=44)
    inside=camera('02_Inside',(-4.9,.6,1.62),(.0,5.0,1.85),lens=20)
    reversecam=camera('03_Reverse',(4.7,5.6,1.62),(-4.5,2.3,1.9),lens=20)
    detail=camera('04_Stair_detail',(-3.6,1.9,1.62),(.2,4.8,1.9),lens=23)
    scene.camera=ref
    # Source image as a hidden reference object, packed into the blend.
    active='Reference'
    refplane=pixel_face('Original_640x128_reference',(0,0,640,128),0,8,0,12.8,3.072)
    refplane.hide_render=True;refplane.hide_set(True)
    scene['room_id']='010';scene['version']='v1';scene['style']='Source EGA palette, unlit, geometric reconstruction'
    scene['limitations']='Unseen front/ceiling inferred. Door destinations unresolved. Stair landing is a placeholder. No gameplay.'
    # Open the file in a useful material preview camera view.
    for screen in bpy.data.screens:
     for area in screen.areas:
      if area.type=='VIEW_3D':
       area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL'
    scene.render.resolution_x=1480;scene.render.resolution_y=600
    bpy.context.view_layer.update()
