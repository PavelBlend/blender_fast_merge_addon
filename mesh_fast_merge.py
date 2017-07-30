
bl_info = {
    "name": "Fast Merge",
    "author": "Pavel_Blend",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "location": "Editmode > Q",
    "description": "Quick merge call",
    "category": "Mesh",
    "wiki_url": "https://github.com/PavelBlend/blender_fast_merge_addon",
    "tracker_url": "https://github.com/PavelBlend/blender_fast_merge_addon/issues"
    }


import bpy
from bpy.props import *


class MeshFastMerge(bpy.types.Operator):
    bl_idname = "mesh.fast_merge"
    bl_label = "Fast Merge"
    bl_description = "Quick call Merge Tool"
    bl_options = {'REGISTER', 'UNDO'}

    merge_type = EnumProperty(
        items=
            [
            ("FIRST", "First", ""),
            ("LAST", "Last", ""),
            ('CENTER', "Center", ""),
            ("CURSOR", "Cursor", ""),
            ("COLLAPSE", "Collapse", "")
            ],
        name="Merge Type",
        description="",
        default="CENTER"
        )

    uvs = BoolProperty(name="UVs", default=False)

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return (ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')

    def execute(self, context):
        try:
            bpy.ops.mesh.merge(type=self.merge_type, uvs=self.uvs)
        except TypeError:
            bpy.ops.mesh.merge(type='CENTER', uvs=self.uvs)
            self.merge_type = 'CENTER'
        return{'FINISHED'}


def draw_func(self, context):
    self.layout.operator("mesh.fast_merge")


addon_keymaps = []


def register():
    bpy.utils.register_class(MeshFastMerge)
    bpy.types.VIEW3D_PT_tools_meshedit.append(draw_func)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
        kmi = km.keymap_items.new('mesh.fast_merge', 'Q', 'PRESS')
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.types.VIEW3D_PT_tools_meshedit.remove(draw_func)
    bpy.utils.unregister_class(MeshFastMerge)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()
