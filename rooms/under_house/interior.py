"""029: long supported crawl-space gallery with blue plumbing and damp timber."""
import random
from blender_shared.lab_furniture import pipe
from blender_shared.bedroom_furniture import finish

def furnish(g,c):
 b=g.box
 for row in range(9):b('Underhouse_back_board',(0,3.295,.22+row*.20),(23.55,.04,.18),'darkgray')
 rng=random.Random(29);vs=[];fs=[]
 for i in range(1500):
  x=rng.uniform(-11.7,11.7);z=rng.uniform(.15,1.98);n=len(vs);w=.022;h=.013
  vs.extend([(x,3.266,z),(x+w,3.266,z),(x+w,3.266,z+h),(x,3.266,z+h)]);fs.append((n,n+1,n+2,n+3))
 g.mesh('Damp_timber_flecks',vs,fs,'cyan')
 b('Rear_timber_sill',(0,2.94,.045),(23.4,.72,.09),'brown')
 for z in [.58,.94,1.30]:pipe(g,'Long_blue_pipe',[(-11.4,3.10,z),(11.4,3.10,z)],.051,'blue')
 for x in [-10.0,-7.2,-4.4,-1.6,1.2,4.0,6.8,9.6]:
  b('Foundation_post_foot',(x,2.73,.15),(.30,.36,.30),'white');b('Yellow_support_post',(x,2.73,1.14),(.105,.125,1.83),'yellow')
  b('Post_red_cap',(x,2.73,1.95),(.14,.16,.28),'red')
  for s in [-1,1]:g.beam('Red_diagonal_brace',(x,2.73,1.66),(x+s*.62,2.73,2.13),.092,'lightred')
  for z in [1.87,2.02]:b('Support_bolt',(x,2.64,z),(.035,.023,.035),'gray')
  pipe(g,'Pipe_riser',[(x+.52,3.10,.59),(x+.52,3.10,1.32),(x+1.13,3.10,1.32)],.054,'blue')
 b('Red_upper_beam',(0,2.76,2.13),(23.7,.22,.12),'red')
 for x in [-9.4,-6.6,-3.8,-1.,1.8,4.6,7.4,10.2]:
  for z in [.58,.94,1.30]:b('Pipe_joint',(x,3.08,z),(.15,.16,.15),'blue');b('Pipe_joint_glint',(x,2.994,z+.035),(.11,.018,.025),'aqua')
 finish(c)
