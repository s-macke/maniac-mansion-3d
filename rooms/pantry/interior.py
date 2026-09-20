"""Room 036: stocked shelf and damaged plaster, preserving doorway clearances."""
from blender_shared.furnishings import curved_line,source_patch


def furnish(geo,root):
    box=geo.box
    for x in [.63,2.16]:
        box('Pantry_shelf_post',(x,4.94,1.40),(.11,.64,2.8),'brown')
        box('Pantry_shelf_post_highlight',(x-.025,4.61,1.40),(.025,.015,2.8),'yellow')
    for z in [.18,.88,1.52,2.15,2.68]:
        box('Pantry_shelf',(1.395,4.94,z),(1.58,.68,.09),'brown')
        box('Pantry_shelf_red_edge',(1.395,4.582,z),(1.58,.025,.065),'red')
    # Tall preserves, cyan tins, packets and the bottle on top follow the reference rows.
    def jar(name,x,z,r,h,color):
        geo.cyl(name,(x,4.83,z+h/2),r,h,color,16)
        geo.cyl(name+'_lid',(x,4.83,z+h+.018),r*1.04,.035,'gray',16)
        box(name+'_label',(x,4.83-r-.005,z+h*.53),(r*1.55,.018,h*.27),'white')
    for x,col in [(.88,'purple'),(1.18,'pink'),(1.52,'green'),(1.87,'cyan')]:jar('Preserve_jar',x,.925,.11,.33,col)
    for x,col in [(.93,'cyan'),(1.42,'gray'),(1.83,'green')]:jar('Food_tin',x,1.565,.105,.23,col)
    for x,w,h,col in [(1.08,.22,.31,'blue'),(1.55,.30,.34,'gray'),(1.88,.17,.3,'blue')]:
        box('Pantry_packet',(x,4.87,2.20+h/2),(w,.27,h),col)
        box('Packet_label',(x,4.724,2.20+h/2),(w*.62,.012,.10),'white')
    geo.cyl('Top_bottle',(1.0,4.91,2.86),.075,.23,'gray',12)
    geo.cyl('Top_bottle_neck',(1.0,4.91,3.025),.037,.1,'white',12)
    # Exact exposed-brick pixels are mounted flush on the rear wall, with irregular silhouettes.
    source_patch(geo,root/'source/room 036.png',(47,0,88,52),(-2.29,5.354,2.49),(1.02,1.27),'Left_exposed_brick',only={'red','brown','yellow','black'})
    source_patch(geo,root/'source/room 036.png',(224,66,257,103),(2.6,5.354,.61),(.78,.86),'Right_exposed_brick',only={'red','brown','yellow','black'})
    for points in [[(-2.50,1.80),(-2.57,1.55),(-2.39,1.28),(-2.52,.83),(-2.34,.40)],[(2.58,2.45),(2.40,2.16),(2.55,1.87),(2.33,1.48),(2.51,1.21)]]:
        curved_line(geo,'Plaster_crack',[(x,5.35,z) for x,z in points],.016,'darkgray')
    # Blue patterned mat from the source, immediately in front of the rack.
    box('Pantry_mat',(1.4,4.13,.012),(1.43,.50,.018),'black')
    for i in range(18):
        for j in range(5):
            if (i+j)%2:box('Mat_weave',(.75+i*.075,3.95+j*.077,.024),(.047,.032,.003),'cyan')
