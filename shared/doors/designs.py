"""Distinctive door designs in natural metre dimensions, local X width / Z height."""
import bpy
from blender_shared.geometry import linear

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
 image=bpy.data.images.load(str(root/'source/room 011.png'));image.pack();pixels=list(image.pixels[:]);W,H=image.size
 verts=[];faces=[];indices=[];materials=[];palette={};pitch=1.8/66
 for v in range(8,97):
  u=273
  def color(k):
   off=((H-1-v)*W+k)*4;return tuple(round(pixels[off+i]*255) for i in range(3))
  while u<339:
   c=color(u);end=u+1
   while end<339 and color(end)==c:end+=1
   if c not in palette:
    m=bpy.data.materials.new('Security_pixel_'+'_'.join(map(str,c)));m.diffuse_color=(*[linear(k) for k in c],1);palette[c]=len(materials);materials.append(m)
   a=-.9+(u-273)*pitch;b=-.9+(end-273)*pitch;lo=.03+(97-v-1)*pitch*1.2;hi=lo+pitch*1.2
   start=len(verts);verts.extend([(a,-.315,lo),(b,-.315,lo),(b,-.315,hi),(a,-.315,hi)]);faces.append((start,start+1,start+2,start+3));indices.append(palette[c]);u=end
 obj=geo.mesh('Original_security_door',verts,faces,None)
 for m in materials:obj.data.materials.append(m)
 for face,i in zip(obj.data.polygons,indices):face.material_index=i
 back=obj.copy();back.data=obj.data.copy();obj.users_collection[0].objects.link(back);back.name='Security_reverse_art'
 for v in back.data.vertices:v.co.y=-.4-v.co.y
 for poly in back.data.polygons:poly.flip()

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
