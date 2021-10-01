bl_info = {
    "name": "Origin Setter",
    "author": "Shreya Punjabi",
    "version": (0,8),
    "blender": (2, 92, 0),
    "location": "Shortcut > Ctrl W",
    "description": "Set origin to selected geometry with a single shortcut",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}


import bpy

class OBJECT_ORIGIN_SETTER(bpy.types.Operator):
    "Set origin to selected geometry"
    bl_idname = "origin.set"
    bl_label = "Set Origin" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    
    
    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                cur = bpy.context.scene.cursor.location.copy()
                ctx = bpy.context.copy()
                
                ctx["area"] = area
                ctx["region"] = area.regions[-1]
                
                bpy.ops.view3d.snap_cursor_to_selected(ctx)
                
                bpy.ops.object.editmode_toggle()
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                
                bpy.context.scene.cursor.location = cur
                bpy.ops.object.editmode_toggle()
        
        return {"FINISHED"}
    
    
    @classmethod
    def poll(cls, context):
        obj = bpy.context.active_object
        if (obj.type=='MESH' and obj.mode=='EDIT'):
            return True
        return False
    
    
def test():
    obj = bpy.context.active_object
    if (obj.type=='MESH' and obj.mode=='EDIT'):
        print("bob")
        
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                cur = bpy.context.scene.cursor.location.copy()
                ctx = bpy.context.copy()
                
                ctx["area"] = area
                ctx["region"] = area.regions[-1]
                
                bpy.ops.view3d.snap_cursor_to_selected(ctx)

                
                bpy.ops.object.editmode_toggle()
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                
                bpy.context.scene.cursor.location = cur

        
        

addon_keymaps = []
    
        
def register():
    bpy.utils.register_class(OBJECT_ORIGIN_SETTER)
    
    global addon_keymaps
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc and (len(addon_keymaps)==0):
        km = wm.keyconfigs.addon.keymaps.new(name = "3D View", space_type = "VIEW_3D")
        kmi = km.keymap_items.new(OBJECT_ORIGIN_SETTER.bl_idname, type = 'W', value = 'PRESS', ctrl = True)
        
        
        
        addon_keymaps.append((km, kmi))
        
    
    
    
def unregister():
    bpy.utils.unregister_class(OBJECT_ORIGIN_SETTER)
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        
    addon_keymaps.clear()
    
    
    
    
if __name__ == "__main__":
    register()
    #unregister()