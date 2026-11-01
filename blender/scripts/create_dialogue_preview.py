import bpy, math, os
from mathutils import Vector

# Short, title-free 3D conversation proof-of-pipeline.
# Run: blender -b -noaudio --python blender/scripts/create_dialogue_preview.py

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.materials, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    pass

def material(name, color, metallic=0.0, roughness=0.55):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value=(*color,1)
    bs.inputs["Metallic"].default_value=metallic
    bs.inputs["Roughness"].default_value=roughness
    return m

navy=material("Midnight blue", (0.025,0.055,0.10))
wall=material("Deep blue wall", (0.035,0.075,0.13))
panel=material("Window glass", (0.08,0.20,0.29), metallic=0.25)
skin=material("Warm skin", (0.63,0.34,0.22))
hair=material("Dark hair", (0.025,0.018,0.025))
jacket=material("Slate jacket", (0.09,0.19,0.29))
shirt=material("Light shirt", (0.72,0.78,0.82))
orange=material("Claude amber", (0.92,0.31,0.08), metallic=0.08)
dark=material("Face details", (0.035,0.025,0.025))
floor_mat=material("Floor", (0.018,0.035,0.06))

def smooth(obj):
    if obj.type=="MESH":
        for p in obj.data.polygons: p.use_smooth=True
    return obj

def uv(name, loc, scale, mat, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(mat); smooth(o)
    if parent:
        # Assign the parent first, then set explicit local coordinates.
        # This avoids Blender's implicit keep-transform parenting offset.
        o.parent=parent
        o.matrix_parent_inverse.identity()
        # All supplied character-part coordinates are already root-local.
        o.location = Vector(loc)
    return o

def cube(name, loc, scale, mat, bevel=0.08, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    if bevel:
        mod=o.modifiers.new("Soft rounded edges","BEVEL"); mod.width=bevel; mod.segments=4
        o.modifiers.new("Weighted corner normals","WEIGHTED_NORMAL")
    if parent:
        # Assign the parent first, then set explicit local coordinates.
        # This avoids Blender's implicit keep-transform parenting offset.
        o.parent=parent
        o.matrix_parent_inverse.identity()
        # All supplied character-part coordinates are already root-local.
        o.location = Vector(loc)
    return o


def text_obj(name, body, loc, size, mat, rotation=(math.pi/2,0,0), parent=None, align="CENTER"):
    data=bpy.data.curves.new(name, type="FONT")
    data.body=body; data.size=size; data.align_x=align
    data.extrude=0.004; data.bevel_depth=0.001
    obj=bpy.data.objects.new(name,data); bpy.context.collection.objects.link(obj)
    obj.location=loc; obj.rotation_euler=rotation; obj.data.materials.append(mat)
    if parent:
        obj.parent=parent; obj.matrix_parent_inverse.identity(); obj.location=Vector(loc)
    return obj

def starburst(name, center, radius, mat, parent=None, plane="front"):
    # Eight rounded rays, built as small beveled bars.
    for i in range(8):
        a=math.tau*i/8
        if plane=="front":  # front faces toward camera (-Y), radial plane X/Z
            x=center[0]+math.cos(a)*radius*0.48
            z=center[2]+math.sin(a)*radius*0.48
            bar=cube(name+" ray", (x,center[1],z), (radius*0.72,0.055,0.12), mat, 0.055, parent)
            bar.rotation_euler[1]=-a
        else:  # right side, radial plane Y/Z
            y=center[1]+math.cos(a)*radius*0.48
            z=center[2]+math.sin(a)*radius*0.48
            bar=cube(name+" ray", (center[0],y,z), (0.055,radius*0.72,0.12), mat, 0.055, parent)
            bar.rotation_euler[0]=a
def cyl(name, loc, radius, depth, mat, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=radius, depth=depth, location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(mat); smooth(o)
    if parent:
        # Assign the parent first, then set explicit local coordinates.
        # This avoids Blender's implicit keep-transform parenting offset.
        o.parent=parent
        o.matrix_parent_inverse.identity()
        # All supplied character-part coordinates are already root-local.
        o.location = Vector(loc)
    return o

# Environment
cube("Room back wall",(0,1.2,3.1),(12,0.25,7),wall,0)
cube("Floor",(0,0,-0.16),(12,12,0.3),floor_mat,0)
cube("Window panel",(-3.3,1.0,3.5),(2.7,0.08,2.4),panel,0.12)
for x in (-4.65,-3.3,-1.95): cube("Window mullion",(x,0.91,3.5),(0.045,0.08,2.4),shirt,0.01)
cube("Window crossbar",(-3.3,0.91,3.5),(2.7,0.08,0.045),shirt,0.01)

# Warm window blinds, wall art and shelves establish the reference-room setting.
for z in (2.65,2.92,3.19,3.46,3.73,4.0):
    cube("Window blind",(-3.3,0.82,z),(2.65,0.045,0.055),shirt,0.02)
# Large dark wall plaque with the orange Claude-inspired burst.
cube("Claude wall plaque",(0.15,0.98,4.55),(3.15,0.12,2.35),dark,0.12)
starburst("Wall Claude burst",(0.15,0.90,4.92),0.92,orange)
text_obj("Wall Claude Code lettering","Claude Code",(0.15,0.895,4.02),0.38,shirt)
# Floating shelf and a few books on the right.
cube("Floating shelf",(4.15,0.55,4.55),(2.4,0.42,0.14),navy,0.05)
for i, col in enumerate((orange,shirt,panel)):
    book=cube("Shelf book",(3.45+i*0.27,0.28,4.88),(0.19,0.28,0.58),col,0.025)
    book.rotation_euler[1]=(i-1)*0.08
# Simple leafy plant silhouette.
cyl("Plant pot",(4.55,0.12,3.35),0.28,0.48,navy)
for i in range(7):
    a=math.tau*i/7
    leaf=uv("Plant leaf",(4.55+math.cos(a)*0.34,0.12,3.82+math.sin(a)*0.10),(0.13,0.10,0.42),panel)
    leaf.rotation_euler[1]=math.cos(a)*0.55
\n# Desk and small monitor in the background
cube("Desk top",(0,-0.25,1.0),(5.8,1.2,0.16),navy,0.08)
cube("Monitor",(-0.05,0.45,2.15),(1.5,0.14,0.95),dark,0.09)
cube("Monitor screen",(-0.05,0.36,2.16),(1.34,0.035,0.78),panel,0.025)
cyl("Monitor stand",(-0.05,0.43,1.57),0.09,0.55,shirt)

# Character roots keep all parts independently animatable as a single group.
human=bpy.data.objects.new("HUMAN_ROOT",None); bpy.context.collection.objects.link(human); human.location=(-1.65,-0.65,0)
# Torso, neck, head
cube("Human torso",(0,0,1.55),(1.12,0.62,1.45),jacket,0.25,human)
cube("Human shirt",(0,-0.325,1.57),(0.43,0.06,1.18),shirt,0.07,human)
cyl("Human neck",(0,-0.02,2.43),0.19,0.34,skin,human)
uv("Human head",(0,-0.04,2.95),(0.56,0.49,0.66),skin,human)
uv("Hair cap",(0,0.01,3.34),(0.57,0.48,0.32),hair,human)
uv("Left hair side",(-0.48,0.0,3.08),(0.13,0.4,0.38),hair,human)
uv("Right hair side",(0.48,0.0,3.08),(0.13,0.4,0.38),hair,human)
for x in (-0.2,0.2):
    uv("Human eye",(x,-0.49,3.0),(0.055,0.035,0.07),dark,human)
uv("Human smile",(0,-0.505,2.76),(0.13,0.025,0.035),dark,human)
# Arms
for side in (-1,1):
    arm=cyl("Human arm",(side*0.72,-0.04,1.67),0.16,0.95,jacket,human)
    arm.rotation_euler[1]=side*0.22
    uv("Human hand",(side*0.82,-0.05,1.18),(0.17,0.16,0.17),skin,human)
# Legs
for x in (-0.28,0.28):
    cube("Human leg",(x,0.02,0.45),(0.37,0.48,0.95),navy,0.12,human)
    cube("Human shoe",(x,-0.18,0.08),(0.43,0.68,0.18),dark,0.08,human)

claude=bpy.data.objects.new("CLAUDE_ROOT",None); bpy.context.collection.objects.link(claude); claude.location=(1.55,-0.72,0)
# Claude is a compact seated box-bot: a soft-edged charcoal cube, terminal face,
# orange side burst, articulated arms, short legs and sneakers.
cube("Claude lower body",(0,0,1.42),(1.12,0.72,0.72),dark,0.16,claude)
cube("Claude box head",(0,-0.02,2.58),(1.72,1.34,1.68),dark,0.19,claude)
# Front terminal prompt: bright, simple and readable in the camera-facing plane.
text_obj("Claude terminal prompt",">_", (0,-0.705,2.43),0.66,shirt,parent=claude)
# Orange eight-ray mark on the visible right side of the cube.
starburst("Claude side burst",(0.875,-0.02,2.58),0.74,orange,parent=claude,plane="side")
# Small inset orange edge accents.
cube("Claude top accent",(0,-0.02,3.43),(0.9,0.025,0.035),orange,0.015,claude)
# Flexible arms and expressive hands.
for side in (-1,1):
    upper=cyl("Claude arm",(side*1.02,-0.02,1.83),0.105,0.68,dark,claude)
    upper.rotation_euler[1]=side*0.48
    uv("Claude hand",(side*1.20,-0.22,1.48),(0.19,0.14,0.17),shirt,claude)
# Short legs and rounded light sneakers.
for x in (-0.34,0.34):
    leg=cyl("Claude leg",(x,0.0,0.84),0.10,0.55,dark,claude)
    cube("Claude sneaker",(x,-0.18,0.48),(0.42,0.62,0.25),shirt,0.11,claude)
    cube("Sneaker sole",(x,-0.19,0.36),(0.44,0.64,0.07),navy,0.025,claude)

