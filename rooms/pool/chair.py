"""One EGA pool-chair design shared by the floating and drained states."""

def build_chair(g, name, x, y, base):
    g.box(name+'_seat',(x,y,base+.065),(.72,.72,.13),'pink')
    g.box(name+'_back',(x,y+.32,base+.445),(.65,.12,.78),'pink')
    g.box(name+'_side',(x-.35,y,base+.155),(.10,.70,.20),'purple')
