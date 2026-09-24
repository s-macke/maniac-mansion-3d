"""Fixed kitchen furnishings from background 007; appliances are noninteractive."""
import math
from blender_shared.furnishings import panel,curved_line,source_patch


def furnish(geo,root):
    box=geo.box
    # Cabinet run, cyan cooker and thick dark worktop.
    box('Base_cabinet_body',(-.05,4.68,.47),(7.3,1.12,.94),'brown')
    for x,w in [(-3.05,1.15),(-.12,1.3),(1.3,1.35),(2.76,1.4)]:panel(geo,'Cabinet_front',x,4.09,.49,w,.82)
    box('Worktop_ink',(-.05,4.67,.99),(7.48,1.25,.12),'black')
    box('Worktop_red_edge',(-.05,4.02,.98),(7.48,.035,.065),'red')
    box('Cooker_body',(-1.83,4.63,.5),(1.35,1.16,.98),'cyan')
    box('Oven_trim',(-1.83,4.035,.49),(.98,.045,.54),'aqua')
    box('Oven_black_glass',(-1.83,4.005,.49),(.83,.035,.41),'black')
    box('Oven_handle',(-1.83,3.97,.77),(.7,.065,.045),'gray')
    geo.beam('Oven_glass_glint',(-2.13,3.978,.37),(-1.91,3.978,.6),.018,'gray')
    for x in [-2.15,-1.52]:
        for y in [4.38,4.91]:
            geo.cyl('Hob_ring',(x,y,1.07),.19,.025,'gray',16)
            geo.cyl('Hob_dark',(x,y,1.086),.145,.015,'black',16)
    # Upper cupboards and microwave in its open niche.
    box('Upper_cabinet',(-2.35,5.02,2.24),(2.7,.63,1.48),'brown')
    panel(geo,'Upper_tall_door',-3.1,4.675,2.23,1.16,1.38)
    panel(geo,'Upper_short_door',-1.75,4.675,2.68,1.45,.48)
    box('Microwave_case',(-1.7,4.59,2.03),(1.25,.65,.68),'gray')
    box('Microwave_face',(-1.7,4.247,2.03),(1.14,.035,.56),'black')
    box('Microwave_screen',(-1.84,4.218,2.03),(.78,.028,.43),'gray')
    box('Microwave_glass',(-1.84,4.198,2.03),(.68,.012,.34),'black')
    for i in range(3):
        for j in range(4):box('Microwave_key',(-1.23+i*.045,4.211,2.18-j*.055),(.028,.018,.026),'white')
    box('Microwave_display',(-1.18,4.213,1.85),(.17,.02,.06),'blue')
    # Both original blue night windows have real openings and recessed frames.
    from blender_shared.windows import cut_wall,outside_window
    cut_wall(geo,'Kitchen_back',[(-5.55,-4.25,1.70,2.66),(1.025,3.075,1.70,2.66)])
    for x,w,cols in [(-4.9,1.3,2),(2.05,2.05,3)]:
        outside_window(geo,'Kitchen_window_'+str(cols),(x,5.37,2.18),(0,1),w,.96,columns=cols,seed=7+cols,edge='red')
    # Sink inset and arched faucet.
    box('Sink_rim',(2.25,4.68,1.06),(1.03,.68,.025),'gray')
    box('Sink_bowl',(2.25,4.68,1.077),(.83,.49,.015),'black')
    curved_line(geo,'Tap',[(2.25,5.02,1.06),(2.25,5.02,1.38),(2.25,4.92,1.46),(2.25,4.73,1.46),(2.25,4.66,1.37)],.055,'gray')
    for x in [1.91,2.58]:box('Tap_handle',(x,4.97,1.12),(.18,.06,.05),'gray')
    # Knife rack, cleaver, chainsaw silhouette and wall stains sampled from the source.
    box('Knife_rack',(.05,5.02,1.82),(1.68,.25,.07),'black')
    for x in [-.18,.13]:
        box('Knife_handle',(x,4.92,1.98),(.07,.09,.27),'gray')
        geo.mesh('Knife_blade',[(x-.06,4.89,1.79),(x+.065,4.89,1.79),(x+.065,4.89,1.37)],[(0,1,2)],'white')
    box('Cleaver_blade',(-.48,4.87,1.57),(.27,.07,.35),'gray')
    box('Cleaver_handle',(-.48,4.9,1.94),(.08,.08,.27),'black')
    box('Cleaver_hole',(-.55,4.829,1.46),(.045,.012,.04),'darkgray')
    # The rightmost tool is the chainsaw: white guide bar with a toothed chain.
    box('Chainsaw_chain',(.48,4.87,1.56),(.26,.07,.41),'black')
    box('Chainsaw_guide',(.48,4.825,1.57),(.19,.025,.34),'white')
    for z in [1.39+i*.07 for i in range(5)]:
        for x in [.335,.625]:box('Chainsaw_tooth',(x,4.87,z),(.035,.075,.025),'gray')
    box('Red_appliance',(.5,4.96,2.04),(.45,.26,.32),'red')
    geo.sphere('Chainsaw_motor_rim',(.5,4.814,2.04),(.145,.018,.135),'black')
    geo.sphere('Chainsaw_motor_face',(.5,4.791,2.04),(.105,.013,.095),'red')
    curved_line(geo,'Appliance_handle',[(.27,4.95,2.2),(.33,4.95,2.35),(.67,4.95,2.35),(.73,4.95,2.2)],.045,'black')
    source_patch(geo,root/'source/room 007.png',(304,11,365,50),(.2,5.30,2.58),(1.5,.85),'Wall_stains',only={'red'})
    # Rounded white refrigerator with a recessed black outline and source stains.
    fridge=box('Fridge_body',(4.48,4.71,1.11),(1.36,1.27,2.22),'gray')
    bevel=fridge.modifiers.new('Rounded_enamel_edges','BEVEL');bevel.width=.14;bevel.segments=3
    import bpy
    bpy.context.view_layer.objects.active=fridge;fridge.select_set(True);bpy.ops.object.modifier_apply(modifier=bevel.name);fridge.select_set(False)
    box('Fridge_door_outline',(4.48,4.047,1.10),(1.18,.055,1.99),'black')
    box('Fridge_enamel',(4.48,4.007,1.10),(1.10,.035,1.92),'white')
    box('Fridge_handle',(4.06,3.956,1.14),(.055,.065,.42),'gray')
    source_patch(geo,root/'source/room 007.png',(493,40,535,110),(4.48,3.975,1.1),(1.06,1.87),'Fridge_stains',only={'red'})
    for i in range(4):geo.cyl('Fridge_top_dishes',(4.48,4.72,2.25+i*.065),.39-i*.035,.04,'gray',20)
    # EGA patterned skirting along the exposed rear wall.
    for i in range(30):
        x=-5.94+i*.405
        box('Tile_gold',(x,5.31,.18),(.37,.03,.3),'yellow')
        box('Tile_red',(x,5.287,.18),(.31,.02,.25),'red')
        geo.sphere('Tile_brown_motif',(x,5.26,.18),(.105,.015,.105),'brown')
