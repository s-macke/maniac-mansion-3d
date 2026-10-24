"""Distinctive door designs in natural metre dimensions, local X width / Z height."""
import bpy,math
from blender_shared.geometry import linear

def mechanical_depth(design,u,v,rgb):
 """Authored component profiles in source-image coordinates, depth in metres.

 Keep the EGA face colors, but give each bar, case, wheel and bolt a physical
 silhouette. Dark seams sit below the colored metal rather than being painted
 across a single flat slab. Profiles apply identically to both door faces.
 """
 def rect(a,b,c,d):return a<=u<c and b<=v<d
 def ellipse(x,y,rx,ry):return ((u-x)/rx)**2+((v-y)/ry)**2
 depth=0.
 if design=='security':
  if u<.12 or u>.88 or v<.045 or v>.95:depth=.018
  if .07<u<.94 and any(a<v<b for a,b in [(.18,.26),(.36,.44),(.63,.71),(.81,.90)]):depth=.085
  if rect(.35,.175,.65,.46):depth=.125
  if rect(.40,.20,.60,.30):depth=.145
  if rect(.38,.84,.45,.98):depth=.14
  if rect(.67,.53,.76,.68):depth=.10
  r=ellipse(.42,.60,.14,.10)
  if r<1:depth=.145+.035*math.sqrt(1-r)
  if rect(.44,.585,.72,.63):depth=.19
  for x,y in [(.075,.075),(.945,.075),(.075,.535),(.945,.535)]:
   r=ellipse(x,y,.052,.038)
   if r<1:depth=.04+.025*math.sqrt(1-r)
 elif design=='dungeon':
  if u<.10 or u>.91 or v<.06 or v>.94:depth=.025
  if rect(.18,.16,.84,.28):depth=.055
  if .445<v<.555:depth=.075
  if rect(.72,.43,.89,.575):depth=.12
  r=ellipse(.34,.50,.18,.092)
  if r<1:depth=.13+.025*math.sqrt(1-r)
 elif design=='lab':
  if u<.08 or u>.90 or v<.045 or v>.96:depth=.025
  if rect(.18,.085,.73,.26):depth=.085
  if rect(.30,.10,.68,.23):depth=.095
  r=ellipse(.465,.435,.25,.105)
  if r<1:depth=.115+.035*math.sqrt(1-r)
  if rect(.30,.425,.62,.45):depth=.165
  for x,y in [(.10,.69),(.68,.72),(.72,.06),(.16,.92)]:
   if ellipse(x,y,.055,.025)<1:depth=max(depth,.04)
 elif design=='metal':
  if rect(.02,.45,.27,.55):depth=.10
  elif u<.085:depth=.012
 elif design=='reinforced':
  if u<.14 and any(a<v<b for a,b in [(.065,.24),(.72,.91)]):depth=.07
  elif .24<u<.76 and .10<v<.94:depth=.025 if rgb[0]>50 else .008
  elif v<.06 or v>.95:depth=.015
 # Real recesses between raised colored metal parts; never extrude printed
 # black outlines as if they were metal. A little depth remains in housings.
 if max(rgb)<10:depth=max(0,depth-.035)
 return round(depth/.005)*.005

def relief_artwork(geo,root,background,crop,width,height,left,bottom,center_y,base_depth,design):
 """Closed stepped relief, with merged color-run faces and side walls at steps.

 This is actual mesh geometry, not a normal map, transparent decal or texture.
 Each source pixel retains its original front color. Only depth discontinuities
 emit side walls; neighboring coplanar pixels do not duplicate vertical faces.
 """
 x0,y0,x1,y1=crop;w=x1-x0;h=y1-y0
 image=bpy.data.images.load(str(root/f'source/room {background}.png'),check_existing=False)
 image.colorspace_settings.name='Non-Color';pixels=list(image.pixels);iw,ih=image.size
 colors=[];depths=[];materials={}
 for row in range(h):
  cr=[];dr=[]
  for col in range(w):
   k=((ih-1-y0-row)*iw+x0+col)*4;rgb=tuple(round(pixels[k+i]*255) for i in range(3))
   # The slanted source door leaves five blue floor pixels in the lower-left
   # corner of this rectangular crop. Continue the cyan metal into that corner.
   if design=='lab' and rgb==(0,0,168):rgb=(0,168,168)
   cr.append(rgb);dr.append(base_depth+mechanical_depth(design,(col+.5)/w,(row+.5)/h,rgb))
   if rgb not in materials:
    m=bpy.data.materials.new(design+'_metal_'+'_'.join(map(str,rgb)));m.diffuse_color=(*[linear(v) for v in rgb],1);materials[rgb]=m
  colors.append(cr);depths.append(dr)
 palette=list(materials);verts=[];faces=[];indices=[]
 def emit(points,rgb,side):
  start=len(verts);verts.extend(points);face=tuple(range(start,start+len(points)))
  faces.append(face if side<0 else tuple(reversed(face)));indices.append(palette.index(rgb))
 for side in [-1,1]:
  for row in range(h):
   col=0
   while col<w:
    end=col+1;rgb=colors[row][col];depth=depths[row][col]
    while end<w and colors[row][end]==rgb and depths[row][end]==depth:end+=1
    a=left+col*width/w;b=left+end*width/w;lo=bottom+(h-row-1)*height/h;hi=lo+height/h;y=center_y+side*depth
    emit([(a,y,lo),(b,y,lo),(b,y,hi),(a,y,hi)],rgb,side);col=end
   for col in range(w):
    d=depths[row][col];rgb=colors[row][col];a=left+col*width/w;b=a+width/w;lo=bottom+(h-row-1)*height/h;hi=lo+height/h
    for dc,dr,p,q in [(-1,0,(a,lo),(a,hi)),(1,0,(b,hi),(b,lo)),(0,-1,(a,hi),(b,hi)),(0,1,(b,lo),(a,lo))]:
     nc,nr=col+dc,row+dr;nd=depths[nr][nc] if 0<=nc<w and 0<=nr<h else base_depth-(.015 if design=='security' else .001)
     if d<=nd+1e-7:continue
     emit([(p[0],center_y+side*d,p[1]),(q[0],center_y+side*d,q[1]),(q[0],center_y+side*nd,q[1]),(p[0],center_y+side*nd,p[1])],rgb,side)
 obj=geo.mesh('Mechanical_'+design,verts,faces,None)
 for material in materials.values():obj.data.materials.append(material)
 for face,index in zip(obj.data.polygons,indices):face.material_index=index
 bpy.data.images.remove(image)

def pool_door(geo):
 box=geo.box;cx=0;y=0
 before=set(bpy.data.objects)
 box('Pool_door_leaf',(cx,y,1.415),(1.3,.09,2.83),'blue')
 for x in [cx-.65,cx+.65]:box('Pool_door_jamb',(x,y-.07,1.44),(.07,.06,2.88),'blue')
 for z in [.04,1.26,2.82]:box('Pool_door_rail',(cx,y-.075,z),(1.3,.06,.07),'white')
 for z0,z1 in [(.14,1.17),(1.36,2.70)]:
  box('Pool_mesh_dark',(cx,y-.055,(z0+z1)/2),(1.10,.018,z1-z0),'darkgray')
  for i in range(19):box('Pool_mesh_vertical',(cx-.54+i*.06,y-.072,(z0+z1)/2),(.012,.014,z1-z0),'gray')
  for i in range(int((z1-z0)/.06)+1):box('Pool_mesh_horizontal',(cx,y-.077,z0+i*.06),(1.08,.014,.012),'gray')
 box('Pool_door_handle',(cx+.52,y-.13,1.35),(.05,.10,.14),'gray')
 # Same visible mesh pattern and handle on the outdoor face.
 for o in list(set(bpy.data.objects)-before):
  if 'jamb' in o.name or o.name=='Pool_door_leaf':continue
  back=o.copy();back.data=o.data.copy();o.users_collection[0].objects.link(back);back.name=o.name+'_back';back.location.y=-o.location.y


def security_door(geo,root):
 for x in [-.99,.99]:geo.box('Security_door_frame_side',(x,-.07,1.5),(.08,.20,3.10),'black')
 geo.box('Security_door_frame_top',(0,-.07,3.005),(1.90,.20,.09),'black')
 geo.box('Security_door_body',(0,-.20,1.48),(1.90,.20,2.96),'blue')
 relief_artwork(geo,root,'011',(273,8,339,97),1.8,89*(1.8/66)*1.2,-.9,.03,-.20,.115,'security')

def entrance_transom(geo):
 verts=[(-.925,-.19,0),(0,-.19,.32),(.925,-.19,0)]
 geo.mesh('Transom_face',verts,[(0,1,2)],'blue')
 for i in range(3):geo.beam('Entrance_transom_border',verts[i],verts[(i+1)%3],.035,'yellow')


def concealed_panel(geo,root):
 # Unit panel, matching the Standard_leaf placement convention. No handle or frame.
 geo.box('Painted_panel',(0,0,0),(1,.06,1),'red')
 image=bpy.data.images.load(str(root/'source/room 027.png'));pixels=list(image.pixels[:]);W,H=image.size
 # Keep the original jagged EGA paint blotch, using horizontal pixel runs.
 for v in range(18,115):
  u=315
  def is_paint(x):
   off=((H-1-v)*W+x)*4
   return pixels[off]>.8 and .15<pixels[off+1]<.5 and .15<pixels[off+2]<.5
  while u<381:
   if not is_paint(u):u+=1;continue
   end=u+1
   while end<381 and is_paint(end):end+=1
   x0=(u-315)/66-.5;x1=(end-315)/66-.5;z0=.5-(v-18+1)/97;z1=.5-(v-18)/97
   geo.box('Paint_blotch',((x0+x1)/2,-.033,(z0+z1)/2),(x1-x0,.006,z1-z0),'lightred');u=end


def grating_leaf(geo):
 for x in [-.5,.5]:geo.box('Grate_rail',(x,0,0),(.035,.045,1),'gray')
 for z in [-.5,.5]:geo.box('Grate_rail',(0,0,z),(1,.045,.04),'gray')
 for i in range(1,8):geo.box('Grate_bar',(-.5+i/8,0,0),(.034,.045,1),'darkgray')
 for z in [-.22,.22]:geo.box('Grate_cross',(0,-.024,z),(1,.035,.048),'gray')


def artwork_leaf(geo,root,background,crop):
 """Unit leaf with solid mechanical profiles and original EGA face colors."""
 # Match the exposed core to each door's artwork, including its top/bottom edges.
 body_color={'031':'darkgray','030':(0,168,168)}.get(background,'blue')
 if isinstance(body_color,tuple):
  material=bpy.data.materials.new('Lab_door_cyan_core');material.diffuse_color=(*[linear(v) for v in body_color],1)
  body_color=material
 geo.box('Metal_leaf_body',(0,0,0),(1,.08,1),body_color)
 design={'030':'lab','031':'metal'}.get(background,'reinforced' if crop[0]==109 else 'dungeon')
 relief_artwork(geo,root,background,crop,1,1,-.5,-.5,0,.041,design)


def dungeon_reinforced_leaf(geo,root):
 """Source 004 left door: nested panels, two crossbars and padlocks."""
 before=set(bpy.data.objects)
 artwork_leaf(geo,root,'004',(109,17,184,102))
 for side in [-1,1]:
  y=side*.08
  for z in [-.20,.20]:
   geo.box('Dungeon_crossbar',(0,y,z),(.98,.065,.048),'blue')
   geo.box('Dungeon_bar_highlight',(0,y+side*.034,z+.014),(.96,.012,.014),'gray')
   for x in [-.31,.31]:geo.box('Dungeon_bar_keeper',(x,y+side*.02,z),(.063,.09,.12),'blue')
   # Match the source padlock centers so the relief covers its painted detail.
   x=.347;lock_z=-.008 if z>0 else -.368
   shackle_h=z-lock_z-.055
   for dx in [-.045,.045]:geo.box('Padlock_shackle',(x+dx,y+side*.07,(z+lock_z)/2),(.015,.018,shackle_h),'gray')
   geo.box('Padlock_shackle_top',(x,y+side*.07,z-.033),(.105,.018,.014),'gray')
   geo.box('Padlock_body',(x,y+side*.07,lock_z),(.17,.045,.115),'gray')
   geo.box('Padlock_keyhole',(x,y+side*.098,lock_z+.005),(.018,.008,.025),'black')
 # The shell mirrors unit leaves; compensate to keep the source's hinge/lock sides.
 for obj in set(bpy.data.objects)-before:
  obj.scale.x*=-1;obj.location.x*=-1
