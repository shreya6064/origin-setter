bl_info = {
    "name": "Origin Setter",
    "author": "Shreya Punjabi",
    "version": (1, 1, 0),
    "blender": (5, 2, 0),
    "doc_url" : "https://github.com/shreya6064/origin-setter",
    "location": "3D Viewport > Edit Mode > Ctrl+W",
    "description": "Set the origin to selected mesh geometry or curve points",
    "category": "Mesh",
}

import bpy


class OBJECT_OT_origin_setter(bpy.types.Operator):
    """Move the object origin to the Edit Mode selection"""

    bl_idname = "origin.set"
    bl_label = "Set Origin to Selection"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.edit_object
        return (
            context.area is not None
            and context.area.type == 'VIEW_3D'
            and obj is not None
            and obj.type in {'MESH', 'CURVE'}
        )

    def execute(self, context):
        viewport_region = next(
            region for region in context.area.regions if region.type == 'WINDOW'
        )
        edit_objects = list(context.objects_in_mode)
        cursor = context.scene.cursor
        saved_location = cursor.location.copy()

        try:
            with context.temp_override(region=viewport_region):
                snapped = bpy.ops.view3d.snap_cursor_to_selected()
            if 'FINISHED' not in snapped:
                self.report({'WARNING'}, "Select mesh geometry or curve points first")
                return {'CANCELLED'}

            if 'FINISHED' not in bpy.ops.object.mode_set(mode='OBJECT'):
                return {'CANCELLED'}

            with context.temp_override(selected_editable_objects=edit_objects):
                return bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        finally:
            cursor.location = saved_location
            if context.mode == 'OBJECT':
                bpy.ops.object.mode_set(mode='EDIT')


addon_keymaps = []


def register():
    bpy.utils.register_class(OBJECT_OT_origin_setter)

    keyconfig = bpy.context.window_manager.keyconfigs.addon
    if keyconfig is not None:
        keymap = keyconfig.keymaps.new(name="3D View", space_type='VIEW_3D')
        item = keymap.keymap_items.new(
            OBJECT_OT_origin_setter.bl_idname, type='W', value='PRESS', ctrl=True
        )
        addon_keymaps.append((keymap, item))


def unregister():
    for keymap, item in addon_keymaps:
        keymap.keymap_items.remove(item)
    addon_keymaps.clear()
    bpy.utils.unregister_class(OBJECT_OT_origin_setter)


if __name__ == "__main__":
    register()
