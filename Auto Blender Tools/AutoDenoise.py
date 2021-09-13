import bpy
import os

from bpy.props import BoolProperty, FloatProperty, IntProperty, PointerProperty,StringProperty
from bpy.types import Operator, Panel, PropertyGroup

class REAL_PT_DenoisePanel(Panel):
    bl_space_type = "IMAGE_EDITOR"
    bl_context = ""
    bl_region_type = "UI"
    bl_label = "贴图降噪"
    bl_category = u"贴图降噪"
    
    def draw(self, context):
        scn = context.scene
        settings = scn.AutoMateToolsSet
        layout = self.layout
        
        col = layout.column(align = True)
        
        bl_label = "AutoDenoise Tool"
        #layout.prop(context.scene, "directory")
        
        # display the properties
        layout.prop(settings, "replaceOld", text="覆盖原图")
        row1 = layout.row(align = False)
        row1.scale_y = 1.5
        op1 = row1.operator("rabichora.denoisenodes", text = "贴图降噪（已导入图片）", icon = "IMAGE_ZDEPTH")


class REAL_OT_Denoise( Operator ):
    bl_idname = "rabichora.denoisenodes"
    bl_label = "Auto Denoise Nodes"
    bl_description = "为当前导入的图片降噪(必须使用本地PNG或者缓存中的图片，不支持Viewer Node直出)"
    bl_options = {'REGISTER', 'UNDO'}
    
    #directory: bpy.props.StringProperty() 

    
    def execute(self, context):        
        replaceOld = context.scene.AutoMateToolsSet.replaceOld
     
        for a in bpy.context.screen.areas:
            if a.type == 'IMAGE_EDITOR':
                image_area = a.spaces[0]
                img = image_area.image
                break
        
        #rename img
        newImgName = img.name
        for s in range(0, len(newImgName)):
            if newImgName[s] == '.':
                newImgName = newImgName[:s]
                break
        
        # Call user prefs window
        area = bpy.ops.wm.window_new()
        # Change area type
        area = bpy.context.window_manager.windows[-1].screen.areas[0]
        area.type = 'NODE_EDITOR'
        area.ui_type = 'CompositorNodeTree'
        
        # switch on nodes and get reference
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        
        # clear default nodes
        #for node in tree.nodes:
        #    tree.nodes.remove(node)
        
        # create input image node
        image_node = tree.nodes.new(type='CompositorNodeImage')
        image_node.image = img
        image_node.location = 0,0
        
        # create denoise node
        denoise_node = tree.nodes.new(type = 'CompositorNodeDenoise')
        denoise_node.use_hdr = True
        denoise_node.location = 300, 0
        
        #create image output
        output_node = tree.nodes.new('CompositorNodeOutputFile')   
        output_node.base_path = 'C:\\tmp\\'
        img_path = img.filepath
        output_node.file_slots[0].path = newImgName + "_baked.png"
        output_node.file_slots[0].save_as_render = False
        output_node.file_slots[0].use_node_format = False
        output_node.location = 600,0
        
        #Create viewer node
        #view_node = tree.nodes.new('CompositorNodeViewer')
        #view_node.name = 'baked viewer'
        #view_node.location = 600, 300
        
        #link
        links = tree.links
        linkImageDenoise = links.new(image_node.outputs[0], denoise_node.inputs[0])
        linkDenoiseOutput = links.new(denoise_node.outputs[0], output_node.inputs[0])
        #linkDenoiseOutput = links.new(denoise_node.outputs[0], view_node.inputs[0])
        
        context = bpy.context
        scene = bpy.context.scene
        coll = bpy.data.collections
        render_layers = bpy.context.scene.view_layers
        hasDummy = False
        for layer in render_layers:
            if layer.name == 'dummy': 
                hasDummy = True
                break
        if not hasDummy:
            dummy_layer = scene.view_layers.new('dummy')
        else:
            dummy_layer = scene.view_layers['dummy']

        original = context.window.view_layer
        context.window.view_layer = dummy_layer

        for c in coll:
            c.hide_render=True

        for layer in render_layers:
            if layer.name == 'dummy':
                layer.use = True
            else:
                layer.use = False

        bpy.ops.render.render(layer = 'dummy')
        
        tree.nodes.remove(image_node)
        tree.nodes.remove(denoise_node)
        tree.nodes.remove(output_node)
        
        #change file name
        imgPath = 'C:\\tmp\\'
        targetName = newImgName + '_baked.png'
        if replaceOld:
            targetName = newImgName + '.png'
        file_exist = False
        for (root, dir, files) in os.walk(imgPath, topdown = True):
            for f in files:
                fileName = os.path.basename(f)
                if fileName == targetName:
                    file_exist = True
                isTarget = fileName[:len(targetName)] == targetName
                if isTarget and len(fileName) > len(targetName):
                    if replaceOld or file_exist:
                        os.remove(root + targetName)
                    os.rename(root + fileName, root + targetName)
                    break
        
        bpy.ops.wm.window_close()
        
        for layer in render_layers:
            layer.use = True
            
        for c in coll:
            c.hide_render=False
        
        #context.window.view_layer = original
        scene.view_layers.remove(dummy_layer)

        #replace image
        for (root, dir, files) in os.walk(imgPath, topdown = True):
            for f in files:
                fileName = os.path.basename(f)
                if fileName == 'Scene_Background.png0000.png':
                    os.remove(root + fileName)

        #replace image
        
        path = 'C:\\tmp\\' + targetName
        bpy.ops.image.open(filepath = path)
        new_img = bpy.data.images[targetName]
        image_area.image = new_img
        
        return {'FINISHED'}


# Properties
class AutoMateToolsSettings(PropertyGroup):
    replaceOld : BoolProperty(
        name = "replaceOld",
        description = "replace the old noised picture",
        default = False
    )


#############################################################################################
classes = (
    AutoMateToolsSettings,
    
    REAL_PT_DenoisePanel,
    REAL_OT_Denoise,
    )


#denoise_register, denoise_unregister = bpy.utils.register_classes_factory(classes)


# Register
def denoise_register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_custom_save = bpy.props.BoolProperty(name="My Custom Save Property")
    bpy.types.Scene.AutoMateToolsSet =  PointerProperty(type=AutoMateToolsSettings)
    #bpy.types.Scene.directory = StringProperty(name = "Saving Directory", description="Choose a directory:", default="", maxlen=1024, subtype='FILE_PATH')
    
# Unregister
def denoise_unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.AutoMateToolsSet
    #del(bpy.types.Scene.directory)


if __name__ == "__main__":
    denoise_register()

    # test call
    bpy.ops.better_export.fbx('INVOKE_DEFAULT')