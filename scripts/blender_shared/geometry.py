"""Shared EGA geometry helpers. Each builder owns its materials and collections."""
import bpy, math
from mathutils import Vector

def linear(v):
 v=v/255
 return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4

class Geometry:

    def __init__(self, collections, materials):
        self.collections = collections
        self.mats = materials
        self.active = "Architecture"

    def put(self, obj, name, mat):
        obj.name = name
        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        self.collections[self.active].objects.link(obj)
        if mat:
            obj.data.materials.append(self.mats[mat] if isinstance(mat, str) else mat)
        return obj

    def box(self, name, loc, size, mat):
        w, d, h = [v / 2 for v in size]
        verts = [(x, y, z) for z in [-h, h] for y in [-d, d] for x in [-w, w]]
        o = self.mesh(name, verts, [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)], mat)
        o.location = loc
        return o

    def mesh(self, name, verts, faces, mat):
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], faces)
        me.update()
        o = bpy.data.objects.new(name, me)
        self.collections[self.active].objects.link(o)
        if mat:
            me.materials.append(self.mats[mat] if isinstance(mat, str) else mat)
        return o

    def beam(self, name, a, b, width, mat):
        a, b = (Vector(a), Vector(b))
        o = self.box(name, (a + b) / 2, (width, width, (b - a).length), mat)
        o.rotation_euler = (b - a).to_track_quat('Z', 'Y').to_euler()
        return o

    def cyl(self, name, loc, radius, depth, mat, vertices=12):
        verts = [(loc[0] + radius * math.cos(i * math.tau / vertices), loc[1] + radius * math.sin(i * math.tau / vertices), loc[2] + z) for z in [-depth / 2, depth / 2] for i in range(vertices)]
        faces = [tuple(reversed(range(vertices))), tuple(range(vertices, 2 * vertices))] + [(i, (i + 1) % vertices, (i + 1) % vertices + vertices, i + vertices) for i in range(vertices)]
        return self.mesh(name, verts, faces, mat)

    def sphere(self, name, loc, scale, mat):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=1, location=loc)
        o = self.put(bpy.context.object, name, mat)
        o.scale = scale
        return o

    def localbox(self, name, u, y, z, w, d, h, mat, origin=(0, 6.5), rot=0):
        o = self.box(name, (origin[0] + u * math.cos(rot) - y * math.sin(rot), origin[1] + u * math.sin(rot) + y * math.cos(rot), z), (w, d, h), mat)
        o.rotation_euler.z = rot
        return o

    def wall(self, name, width, origin, rot, doors):
        H = 3.65
        cuts = sorted([(-width / 2, -width / 2, 0)] + [(x - w / 2, x + w / 2, h) for x, w, h in doors] + [(width / 2, width / 2, 0)])
        for i in range(len(cuts) - 1):
            a, b = (cuts[i][1], cuts[i + 1][0])
            if b > a:
                self.localbox(name + '_shell', (a + b) / 2, 0.11, H / 2, b - a, 0.22, H, 'cyan', origin, rot)
        for x, w, h in doors:
            self.localbox(name + '_header', x, 0.11, (H + h) / 2, w, 0.22, H - h, 'cyan', origin, rot)

        def visible(u, z):
            return not any((abs(u - x) < w / 2 + 0.005 and z < h for x, w, h in doors))
        for i in range(int(width / 0.12)):
            u = -width / 2 + (i + 0.5) * 0.12
            z0 = 0.92
            for x, w, h in doors:
                if abs(u - x) < w / 2 + 0.02:
                    z0 = max(z0, h)
            if z0 < H:
                self.localbox(name + '_stripe', u, -0.007, (z0 + H) / 2, 0.045, 0.016, H - z0, 'aqua', origin, rot)
                self.localbox(name + '_stripe_ink', u - 0.036, -0.009, (z0 + H) / 2, 0.017, 0.02, H - z0, 'black', origin, rot)
        for i in range(int(width / 0.85)):
            u = -width / 2 + (i + 0.5) * width / int(width / 0.85)
            w = width / int(width / 0.85) - 0.06
            if not all((visible(t, 0.4) for t in [u - w / 2, u, u + w / 2])):
                continue
            self.localbox(name + '_panel_black', u, -0.025, 0.43, w, 0.07, 0.84, 'black', origin, rot)
            self.localbox(name + '_panel_red', u, -0.065, 0.43, w - 0.035, 0.025, 0.8, 'red', origin, rot)
            self.localbox(name + '_panel_gold', u, -0.084, 0.43, w - 0.09, 0.018, 0.68, 'yellow', origin, rot)
            self.localbox(name + '_panel_wood', u, -0.097, 0.43, w - 0.14, 0.016, 0.62, 'brown', origin, rot)
            self.localbox(name + '_panel_inset', u, -0.107, 0.43, w - 0.27, 0.013, 0.44, 'red', origin, rot)
            self.localbox(name + '_panel_center', u, -0.12, 0.43, w - 0.32, 0.016, 0.39, 'brown', origin, rot)
        for z, h, mat in [(0.07, 0.13, 'red'), (0.84, 0.07, 'black'), (0.91, 0.06, 'yellow'), (0.97, 0.06, 'brown'), (3.61, 0.07, 'brown')]:
            for i in range(len(cuts) - 1):
                a, b = (cuts[i][1], cuts[i + 1][0])
                if b > a:
                    self.localbox(name + '_trim', (a + b) / 2, -0.08, z, b - a, 0.12, h, mat, origin, rot)

    def door(self, name, u, width, height, origin, rot=0, double=False):
        for j, (extra, mat) in enumerate([(0.21, 'black'), (0.13, 'yellow'), (0.06, 'red')]):
            w = width + extra
            thick = 0.038
            y = -0.1 - j * 0.021
            for side in [-1, 1]:
                o = self.localbox(name + '_jamb', u + side * (w / 2 - thick / 2), y, height / 2, thick, 0.025, height + 0.1, mat, origin, rot)
                o['destination'] = 'Unresolved placeholder'
            self.localbox(name + '_lintel', u, y, height + 0.045 - j * 0.027, w, 0.025, 0.035, mat, origin, rot)
        leaves = 2 if double else 1
        for k in range(leaves):
            lw = width / leaves - 0.035
            lu = u + (k - (leaves - 1) / 2) * width / leaves
            leaf = self.localbox(name + '_leaf', lu, -0.18, height / 2, lw, 0.13, height - 0.1, 'brown', origin, rot)
            leaf['is_door_leaf'] = True
            for z, h in [(height * 0.68, height * 0.47), (height * 0.22, height * 0.29)]:
                for delta, inset, mat in [(0, 0, 'black'), (0.012, 0.035, 'yellow'), (0.024, 0.075, 'red'), (0.036, 0.12, 'brown')]:
                    self.localbox(name + '_raised_panel', lu, -0.255 - delta, z, lw - 0.18 - inset, 0.02, h - inset, mat, origin, rot)
            ku = lu + (lw * 0.34 if double and k == 0 else -lw * 0.34)
            self.localbox(name + '_knob_ink', ku, -0.32, height * 0.49, 0.11, 0.09, 0.11, 'black', origin, rot)
            self.localbox(name + '_knob', ku - 0.013, -0.38, height * 0.5, 0.06, 0.035, 0.06, 'gray', origin, rot)
        if double:
            pts = [(-width / 2, 0), (0, 0.32), (width / 2, 0)]
            verts = [(origin[0] + (u + x) * math.cos(rot) + 0.19 * math.sin(rot), origin[1] + (u + x) * math.sin(rot) - 0.19 * math.cos(rot), height + z) for x, z in pts]
            self.mesh(name + '_transom', verts, [(0, 1, 2)], 'blue')
            for i in range(3):
                self.beam(name + '_transom_border', verts[i], verts[(i + 1) % 3], 0.035, 'yellow')

    def camera(self, name, loc, target, lens=26, ortho=None):
        bpy.ops.object.camera_add(location=loc)
        o = self.put(bpy.context.object, name, None)
        o.rotation_euler = (Vector(target) - o.location).to_track_quat('-Z', 'Y').to_euler()
        o.data.lens = lens
        o.data.clip_start = 0.05
        o.data.clip_end = 150
        if ortho:
            o.data.type = 'ORTHO'
            o.data.ortho_scale = ortho
        return o
