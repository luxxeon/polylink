from polylink.Polylink import trigPolylink
import bpy
from bpy.props import EnumProperty, FloatProperty, IntProperty


def create_mesh_object(context, verts, edges, faces, name):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, edges, faces)
    me.update()

    from bpy_extras import object_utils
    return object_utils.object_data_add(context, me, operator=None)


class AddTorusPolylink(bpy.types.Operator):
    """Add a surface defined by torus-based polylinks"""
    bl_idname = "mesh.primitive_torus_polylink"
    bl_label = "Add Torus Polylink"
    bl_options = {"REGISTER", "UNDO"}

    source = EnumProperty(
        items=[("TETRAHEDRON", "Tetrahedron", "", 1),
               ("CUBE", "Cube", "", 2),
               ("OCTAHEDRON", "Octahedron", "", 3),
               ("DODECAHEDRON", "Dodecahedron", "", 4),
               ("ICOSAHEDRON", "Icosahedron", "", 5)],
        name="Source",
        description="Starting point of your polylink")

    rot = FloatProperty(
        name="Rotation",
        description="Rotation around the face normals",
        min=0.00, max=360,
        step=10,
        default=0.0,
        subtype="ANGLE",
        unit="ROTATION")

    faceDis = FloatProperty(
        name="Distance",
        description="Distance from the center to each face",
        min=0.00, max=10,
        default=1.0,
        unit="LENGTH")

    majorRadius = FloatProperty(
        name="Major Radius",
        description=("Max distance from the face " +
                     "center to the center of the tube"),
        min=0.01, max=10,
        default=3.0,
        unit="LENGTH")

    minorRadius = FloatProperty(
        name="Minor Radius",
        description="The radius of the tube",
        min=0.01, max=10,
        default=1,
        unit="LENGTH")

    amplitude = FloatProperty(
        name="Amplitude",
        description="Amplitude of the wave",
        min=0.01, max=10,
        default=1.0,
        unit="LENGTH")

    factor = IntProperty(
        name="Factor",
        description="Times of the frequency",
        min=1, max=10,
        default=1)

    initAng = FloatProperty(
        name="Initial Angle",
        description="Initial angle of tube segments",
        min=0.00, max=360,
        step=10,
        default=0.0,
        subtype="ANGLE")

    uSeg = IntProperty(
        name="u segments",
        description="Number of segments in radial direction",
        min=3, max=50,
        default=10)

    vSeg = IntProperty(
        name="v segments",
        description="Number of segments in axial direction",
        min=10, max=300,
        default=40)

    def execute(self, context):
        pmesh = trigPolylink(self.source, self.rot, self.faceDis,
                             self.majorRadius, self.amplitude,
                             self.minorRadius, self.factor,
                             self.initAng, self.vSeg, self.uSeg)
        create_mesh_object(context, pmesh.vertices, [],
                           pmesh.faces, "Polylink")
        return {'FINISHED'}