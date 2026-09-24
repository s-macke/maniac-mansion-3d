"""Open, non-traversable windows with recessed frames and static distant skies."""
import bpy, random
from mathutils import Vector


def cut_wall(g,prefix,holes,axis='x',author_offset_y=0):
    """Split existing axis-aligned wall slabs, preserving other door openings.

    Holes are (horizontal minimum, maximum, bottom, top) in the furnishing's
    authored coordinates. Compensate rear_anchored with author_offset_y.
    """
    bpy.context.view_layer.update()
    index=0 if axis=='x' else 1
    for obj in list(bpy.data.objects):
        if not obj.name.startswith(prefix):continue
        corners=[obj.matrix_world@Vector(p) for p in obj.bound_box]
        lo=[min(p[i] for p in corners) for i in range(3)]
        hi=[max(p[i] for p in corners) for i in range(3)]
        lo[1]+=author_offset_y;hi[1]+=author_offset_y
        cuts=sorted(set([lo[index],hi[index]]+[max(lo[index],min(hi[index],h[i])) for h in holes for i in [0,1]]))
        zs=sorted(set([lo[2],hi[2]]+[max(lo[2],min(hi[2],h[i])) for h in holes for i in [2,3]]))
        mat=obj.data.materials[0]
        for a,b in zip(cuts,cuts[1:]):
            for bottom,top in zip(zs,zs[1:]):
                if b-a<1e-6 or top-bottom<1e-6:continue
                if any(h[0]<(a+b)/2<h[1] and h[2]<(bottom+top)/2<h[3] for h in holes):continue
                center=[(a+b)/2 if i==index else (lo[i]+hi[i])/2 for i in range(3)]
                size=[b-a if i==index else hi[i]-lo[i] for i in range(3)]
                center[2]=(bottom+top)/2;size[2]=top-bottom
                g.box(prefix+'_window_surround',center,size,mat)
        bpy.data.objects.remove(obj,do_unlink=True)


def outside_window(g,name,center,outward,width,height,*,sky='blue',frame='brown',columns=2,rows=2,seed=1,edge=None,rail=None):
    """Frame and distant sky in the same independent room; no transparent pane."""
    n=Vector((*outward,0));u=Vector((n.y,-n.x,0));origin=Vector(center)
    def box(label,x,d,z,w,depth,h,color,unlit=False):
        p=origin+u*x+n*d+Vector((0,0,z))
        size=(abs(u.x)*w+abs(n.x)*depth,abs(u.y)*w+abs(n.y)*depth,h)
        obj=g.box(name+'_'+label,p,size,color)
        if unlit:obj['bake_unlit']=True;obj['bake_no_shadow']=True;obj['bake_group']=name+'_sky'
        return obj
    for x in [-width/2,width/2]:
        box('frame',x,-.045,0,.095,.075,height+.16,frame)
        box('reveal',x,.075,0,.03,.30,height,frame)
    for z in [-height/2,height/2]:
        box('frame',0,-.045,z,width+.16,.075,.095,frame)
        box('reveal',0,.075,z,width,.30,.03,frame)
    if edge:
        for x in [-width/2,width/2]:box('frame_edge',x,-.087,0,.022,.012,height,edge)
        for z in [-height/2,height/2]:box('frame_edge',0,-.087,z,width,.012,.022,rail or edge)
    for i in range(1,columns):box('mullion',-width/2+width*i/columns,-.09,0,.04,.04,height,frame)
    for i in range(1,rows):box('crossbar',0,-.09,-height/2+height*i/rows,width,.04,.04,frame)
    box('sill',0,-.10,-height/2-.07,width+.22,.32,.055,frame)
    box('night',0,28,0,36,.02,36,sky,True)
    for x in [-18,18]:box('sky_side',x,14.1,0,.02,27.8,36,sky,True)
    for z in [-18,18]:box('sky_edge',0,14.1,z,36,27.8,.02,sky,True)
    rng=random.Random(seed)
    for i in range(65):
        box('star',rng.uniform(-14,14),rng.uniform(12,26),rng.uniform(-12,12),.05,.007,.05,'white' if i%3 else 'yellow',True)
    for x,z in [(-1.4,2.1),(1.2,-1.6),(.3,.7)]:box('reference_star',x,17,z,.065,.007,.065,'white',True)
