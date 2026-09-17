"""Small solid furniture details, using the existing EGA geometry/bake pipeline."""
import math
import bpy
from .layout_shell import PALETTE


def panel(geo,name,x,y,z,w,h,base='brown'):
    for inset,depth,color in [(0,0,'black'),(.035,-.016,'yellow'),(.075,-.032,'red'),(.11,-.048,base)]:
        geo.box(name,(x,y+depth,z),(w-inset*2,.025,h-inset*2),color)


def curved_line(geo,name,points,width,color):
    for a,b in zip(points,points[1:]):geo.beam(name,a,b,width,color)


def source_patch(geo,path,crop,center,size,name,only=None):
    """Original pixels as coplanar color runs; no filtered/repainted artwork or texture dependency."""
    image=bpy.data.images.load(str(path),check_existing=False)
    image.colorspace_settings.name='Non-Color'
    pixels=list(image.pixels);iw,ih=image.size
    x0,y0,x1,y1=crop;w,h=x1-x0,y1-y0
    groups={};cache={}
    for row in range(h):
        line=[]
        for col in range(w):
            i=((ih-1-y0-row)*iw+x0+col)*4;rgb=tuple(round(v*255) for v in pixels[i:i+3])
            if rgb not in cache:cache[rgb]=min(PALETTE,key=lambda k:sum((rgb[j]-PALETTE[k][j])**2 for j in range(3)))
            line.append(cache[rgb])
        start=0
        while start<w:
            end=start+1;color=line[start]
            while end<w and line[end]==color:end+=1
            if only is None or color in only:
                vs,fs=groups.setdefault(color,([],[]));n=len(vs)
                xa=center[0]+(start/w-.5)*size[0];xb=center[0]+(end/w-.5)*size[0]
                za=center[2]+(.5-row/h)*size[1];zb=center[2]+(.5-(row+1)/h)*size[1]
                vs.extend([(xa,center[1],zb),(xb,center[1],zb),(xb,center[1],za),(xa,center[1],za)]);fs.append((n,n+1,n+2,n+3))
            start=end
    for color,(vs,fs) in groups.items():
        obj=geo.mesh(name+'_'+color,vs,fs,color);obj['bake_unlit']=True;obj['bake_no_shadow']=True
    bpy.data.images.remove(image)
