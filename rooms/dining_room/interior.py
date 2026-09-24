"""Room 037 furniture and original wall painting."""
import math
from blender_shared.furnishings import panel,curved_line,source_patch


def furnish(geo,root):
    box=geo.box
    # Red panelled rear wall, gold mouldings and narrow lower vertical slats.
    for x in [-8.4,-5.6,-2.8,0,2.8,5.6,8.4]:panel(geo,'Wall_panel',x,5.29,2.17,2.62,1.43)
    for i in range(105):
        x=-9.25+i*.178
        box('Wainscot_groove',(x,5.295,.6),(.025,.03,1.12),'black')
        box('Wainscot_highlight',(x+.027,5.272,.6),(.015,.026,1.12),'lightred')
    for z in [.10,1.2,3.05]:box('Wall_rail',(0,5.22,z),(18.8,.16,.075),'brown')
    # Preserve the painting itself, including all original pixel colors.
    panel(geo,'Painting_frame',0,5.13,2.42,3.35,1.32)
    source_patch(geo,root/'source/room 037.png',(427,0,549,46),(0,5.05,2.43),(3.05,1.1),'Original_painting')
    # Long rounded table with a draped turquoise cloth.
    geo.box('Table_top',(0,2.8,.94),(13.3,1.55,.15),'brown')
    for x in [-6.3,6.3]:
        for y in [2.25,3.35]:box('Table_leg',(x,y,.46),(.14,.14,.92),'brown')
    # Capsule top and scalloped hanging edge, avoiding a rectangular billboard.
    outline=[]
    for cx,start in [(6.3,-math.pi/2),(-6.3,math.pi/2)]:
        for i in range(17):
            a=start+i*math.pi/16;outline.append((cx+.78*math.cos(a),2.8+.78*math.sin(a),1.035))
    geo.mesh('Turquoise_tablecloth_top',outline,[tuple(range(len(outline)))],'aqua')
    n=len(outline);vs=outline+[(x,y,.69) for x,y,z in outline]
    geo.mesh('Turquoise_tablecloth_drop',vs,[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],'cyan')
    for side in [-1,1]:
        for i in range(6):
            x0=-6.3+i*2.1
            for zoff,col in [(0,'aqua'),(-.10,'white')]:
                curved_line(geo,'Cloth_scallop',[(x0+t*2.1,2.8+side*.79,.94-.17*math.sin(t*math.pi)+zoff) for t in [j/12 for j in range(13)]],.022,col)
    # Turquoise high-backed chairs at both ends, oriented towards the table.
    for side in [-1,1]:
        x=side*7.65
        box('Chair_seat',(x,2.8,.51),(.73,.79,.14),'cyan')
        box('Chair_seat_piping',(x,2.8,.595),(.73,.79,.025),'aqua')
        for dx in [-.28,.28]:
            for dy in [-.30,.30]:
                box('Chair_leg',(x+dx,2.8+dy,.25),(.075,.075,.5),'brown')
                geo.sphere('Chair_turned_foot',(x+dx,2.8+dy,.14),(.065,.065,.065),'brown')
        box('Chair_back',(x+side*.32,2.8,1.04),(.11,.71,1.02),'cyan')
        for dy in [-.33,.33]:box('Chair_back_post',(x+side*.32,2.8+dy,1.05),(.09,.075,1.07),'brown')
        geo.sphere('Chair_oval_finial',(x+side*.32,2.8,1.65),(.09,.20,.28),'aqua')
    # Three silver candelabra and the two roast platters seen in the art.
    for x in [-5.8,1.45,5.8]:
        geo.cyl('Candle_base',(x,2.8,1.075),.19,.055,'gray')
        geo.cyl('Candle_stem',(x,2.8,1.34),.035,.52,'gray')
        curved_line(geo,'Candle_arms',[(x-.24,2.8,1.55),(x-.24,2.8,1.34),(x,2.8,1.24),(x+.24,2.8,1.34),(x+.24,2.8,1.55)],.04,'gray')
        for dx in [-.24,0,.24]:
            geo.cyl('Candle_wax',(x+dx,2.8,1.68 if dx else 1.78),.035,.3,'aqua')
            geo.cyl('Candle_wick',(x+dx,2.8,1.85 if dx else 1.95),.009,.04,'black')
    for x in [-2.35,-.55]:
        geo.sphere('Serving_platter',(x,2.8,1.075),(.53,.34,.035),'gray')
        geo.sphere('Roast',(x,2.8,1.22),(.40,.26,.16),'brown' if x<-1 else 'red')
        geo.sphere('Roast_highlight',(x+.21,2.61,1.22),(.13,.04,.10),'lightred')
        if x<-1:
            geo.beam('Roast_bone',(x+.26,2.8,1.28),(x+.51,2.8,1.38),.055,'white')
        else:
            # The second platter carries a sliced ham, not another bone-in bird.
            geo.sphere('Ham_cut_fat_rim',(x+.21,2.568,1.23),(.16,.030,.135),'white')
            geo.sphere('Ham_cut_meat',(x+.21,2.540,1.23),(.127,.018,.104),'red')
            geo.sphere('Ham_cut_center',(x+.21,2.521,1.23),(.040,.008,.034),'white')
            for offset in [-.16,-.02]:
                curved_line(geo,'Ham_marbling',[(x+offset+.035*math.sin(t*math.pi),2.8-.255*math.sin(t*math.pi),1.22+.163*math.cos(t*math.pi)) for t in [j/16 for j in range(9)]],.012,'white')
    # Twin three-globe chandeliers; baked color rather than runtime lights.
    for x in [-5.6,5.6]:
        geo.cyl('Chandelier_chain',(x,3.95,2.86),.022,.52,'yellow')
        for dx in [-.56,0,.56]:
            curved_line(geo,'Chandelier_arm',[(x,3.95,2.55),(x+dx,3.95,2.45),(x+dx,3.95,2.62)],.045,'yellow')
            geo.sphere('Chandelier_globe',(x+dx,3.95,2.73),(.18,.18,.21),'white')
            geo.sphere('Chandelier_glow',(x+dx,3.93,2.73),(.145,.17,.175),'yellow')
