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
    if parent: o.parent=parent; o.matrix_parent_inverse=parent.matrix_world.inverted()
    return o

def cube(name, loc, scale, mat, bevel=0.08, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    if bevel:
        mod=o.modifiers.new("Soft rounded edges","BEVEL"); mod.width=bevel; mod.segments=4
        o.modifiers.new("Weighted corner normals","WEIGHTED_NORMAL")
    if parent: o.parent=parent; o.matrix_parent_inverse=parent.matrix_world.inverted()
    return o

def cyl(name, loc, radius, depth, mat, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=radius, depth=depth, location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(mat); smooth(o)
    if parent: o.parent=parent; o.matrix_parent_inverse=parent.matrix_world.inverted()
    return o

# Environment
cube("Room back wall",(0,1.2,3.1),(12,0.25,7),wall,0)
cube("Floor",(0,0,-0.16),(12,12,0.3),floor_mat,0)
cube("Window panel",(-3.3,1.0,3.5),(2.7,0.08,2.4),panel,0.12)
for x in (-4.65,-3.3,-1.95): cube("Window mullion",(x,0.91,3.5),(0.045,0.08,2.4),shirt,0.01)
cube("Window crossbar",(-3.3,0.91,3.5),(2.7,0.08,0.045),shirt,0.01)
# Desk and small monitor in the background
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

claude=bpy.data.objects.new("CLAUDE_ROOT",None); bpy.context.collection.objects.link(claude); claude.location=(1.65,-0.55,0)
# Friendly compact orange AI character, deliberately distinct silhouette.
uv("Claude body",(0,0,1.75),(0.78,0.58,0.82),orange,claude)
uv("Claude head",(0,-0.02,2.78),(0.78,0.57,0.72),orange,claude)
# Small top crest and side details
uv("Claude crest",(0,0.0,3.48),(0.18,0.18,0.22),orange,claude)
for x in (-0.28,0.28):
    uv("Claude eye",(x,-0.54,2.88),(0.07,0.035,0.09),dark,claude)
uv("Claude mouth",(0,-0.575,2.59),(0.16,0.03,0.045),dark,claude)
for side in (-1,1):
    arm=cyl("Claude arm",(side*0.82,-0.02,1.85),0.13,0.75,orange,claude)
    arm.rotation_euler[1]=side*0.5
    uv("Claude hand",(side*1.0,-0.05,1.48),(0.16,0.15,0.16),orange,claude)
for x in (-0.32,0.32):
    cyl("Claude foot",(x,-0.05,0.32),0.18,0.5,orange,claude)

# Camera and lighting
bpy.ops.object.camera_add(location=(0,-11,4.0))
cam=bpy.context.object; cam.name="Conversation Camera"
target=Vector((0,0,1.95)); cam.rotation_euler=(target-cam.location).to_track_quat("-Z","Y").to_euler()
cam.data.type="ORTHO"; cam.data.ortho_scale=8.6
bpy.context.scene.camera=cam

def area(name, loc, power, color, size, target=(0,0,2)):
    bpy.ops.object.light_add(type="AREA", location=loc)
    l=bpy.context.object; l.name=name; l.data.energy=power; l.data.color=color; l.data.shape="DISK"; l.data.size=size
    l.rotation_euler=(Vector(target)-l.location).to_track_quat("-Z","Y").to_euler()
area("Warm key",(-4,-5,7),950,(1.0,0.78,0.62),5)
area("Cool fill",(4,-4,5),800,(0.55,0.72,1.0),4)
area("Top rim",(0,2,6),1100,(1.0,0.48,0.22),3)

scene=bpy.context.scene
scene.render.engine="BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items.keys() else "BLENDER_EEVEE"
scene.eevee.taa_render_samples=32 if hasattr(scene,"eevee") else 16
scene.render.resolution_x=720; scene.render.resolution_y=1280; scene.render.resolution_percentage=100
scene.render.fps=24; scene.frame_start=1; scene.frame_end=120
scene.render.image_settings.file_format="FFMPEG"
scene.render.ffmpeg.format="MPEG4"; scene.render.ffmpeg.codec="H264"; scene.render.ffmpeg.constant_rate_factor="MEDIUM"
out_dir=os.path.abspath(os.path.join(os.getcwd(), "out"))
os.makedirs(out_dir, exist_ok=True)
blend_path=os.path.join(out_dir, "blender-dialogue-preview.blend")
video_path=os.path.join(out_dir, "blender-dialogue-preview.mp4")
scene.render.filepath=video_path
scene.view_settings.view_transform="Standard"
scene.view_settings.look="Medium High Contrast"
scene.world.color=(0.025,0.025,0.025)

# Gentle idle motion; no title card or on-screen title.
for root, phase in ((human,0.0),(claude,1.2)):
    for frame in (1,30,60,90,120):
        root.location.z=0.035*math.sin(frame/12+phase)
        root.rotation_euler[1]=0.025*math.sin(frame/18+phase)
        root.keyframe_insert(data_path="location",frame=frame)
        root.keyframe_insert(data_path="rotation_euler",frame=frame)

# Slightly vary camera framing over the shot.
for frame, z in ((1,4.0),(120,3.92)):
    cam.location.z=z; cam.keyframe_insert(data_path="location",frame=frame)
scene.render.image_settings.color_mode="RGB"
scene.render.ffmpeg.audio_codec="NONE"
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
bpy.ops.render.render(animation=True)
print("BLENDER_DIALOGUE_PREVIEW_RENDERED")
