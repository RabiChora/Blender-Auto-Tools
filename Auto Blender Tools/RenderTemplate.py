#=============================================================
#  INFO
#=============================================================

import bpy
from bpy.types import Operator, Panel, PropertyGroup, Menu
from bpy.props import BoolProperty, FloatProperty, IntProperty, PointerProperty,StringProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

import bpy
import os
import importlib
import time



         
#=============================================================
#  FUNCTIONS
#=============================================================
def selectTitle(title):
    coll = bpy.data.collections['Titles']
    for i in range(len(coll.all_objects)):
        obj = coll.all_objects[i]
        if obj.name != title:
            print(obj.hide_render)
            obj.hide_render = True
            obj.hide_viewport = True
            obj.hide_select = True
        else:
            print(obj.name)
            obj.hide_render = False
            obj.hide_viewport = False
            obj.hide_select = False
            
def selectName(name):
    coll = bpy.data.collections['Names']
    for i in range(len(coll.all_objects)):
        obj = coll.all_objects[i]
        if obj.name != name:
            print(obj.hide_render)
            obj.hide_render = True
            obj.hide_viewport = True
            obj.hide_select = True
        else:
            print(obj.name)
            obj.hide_render = False
            obj.hide_viewport = False
            obj.hide_select = False
            
def changeBackground(color):
    #changeMaterial
    for obj in bpy.data.objects:
        if obj.name != 'BackgroundColor':
            obj.select_set(False)
        else:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
    # BackgroundColor is selected, so must have a material
    
    mat=bpy.context.active_object.active_material # mat never null
    tree=mat.node_tree.nodes
    backgroundNode = tree.get("Background Image")
    
    addonPath = bpy.utils.user_resource('SCRIPTS', "addons")
    if color == 'Red':
        bpy.ops.image.open(filepath = addonPath + '\\Background Colors\\Background_Red.png')
        bgImage = bpy.data.images['Background_Red.png']
    elif color == 'Orange':
        bpy.ops.image.open(filepath = addonPath + '\\Background Colors\\Background_Orange.png')
        bgImage = bpy.data.images['Background_Orange.png']
    elif color == 'Blue':
        bpy.ops.image.open(filepath = addonPath + '\\Background Colors\\Background_Blue.png')
        bgImage = bpy.data.images['Background_Blue.png']
    elif color == 'Purple':
        bpy.ops.image.open(filepath = addonPath + '\\Background Colors\\Background_Purple.png')
        bgImage = bpy.data.images['Background_Purple.png']
    
    print(bgImage)    
    backgroundNode.image = bgImage
    
    #changeShadow        
    shadow_red = [0.068381, 0.009078, 0.034835, 1.0]
    shadow_orange = [0.068380, 0.016252, 0.010204, 1.0]
    shadow_blue = [0.007923, 0.01253, 0.06838, 1.0]
    shadow_purple = [0.0248607, 0.005285, 0.068379, 1.0]

    for a in bpy.context.screen.areas:
        if a.type == 'NODE_EDITOR' and a.ui_type == 'CompositorNodeTree':
            area = a
    bpy.context.scene.use_nodes = True
    composeTree = bpy.context.scene.node_tree
    for node in composeTree.nodes:
        if node.name == 'Shadow Color':
            if color == 'Red':
                node.outputs[0].default_value = shadow_red
            elif color == 'Orange':
                node.outputs[0].default_value = shadow_orange
            elif color == 'Blue':
                node.outputs[0].default_value = shadow_blue
            elif color == 'Purple':
                node.outputs[0].default_value = shadow_purple
    
def showExplorer():
    path = "C:/tmp"
    path = os.path.realpath(path)
    os.startfile(path)
    

                
#=============================================================
#  MENUS
#=============================================================          
def execute_bgcolor(self, context):
    changeBackground(self.bg_color_enum)
        
        
class BG_Color_Enum(PropertyGroup):
    bgcolor_options = [
        #(idname, name, description, icon, id_number)
        ('Red',      'Red',    '',  'COLORSET_01_VEC', 0),
        ('Orange',   'Orange', '',  'COLORSET_02_VEC', 1),
        ('Blue',     'Blue',   '',  'COLORSET_04_VEC', 2),
        ('Purple',   'Purple', '',  'COLORSET_06_VEC', 3)
    ]
    
    bg_color_enum : bpy.props.EnumProperty(
        items = bgcolor_options,
        description = '选择背景颜色',
        default = 'Blue',
        update = execute_bgcolor
    )
        
        
def execute_title(self, context):
    selectTitle(self.title_enum)

def title_option(self, context):
    enum_titles = []
    title_obj = bpy.data.collections['Titles'].all_objects
    count = 0
    for obj in title_obj:
        enum_titles.append((obj.name, obj.name, '', 'TOPBAR', count))
        count += 1
    return enum_titles

def update_title_option(self, context):
    enum_titles = title_option(self, context)
    print(enum_titles)
    return None
   
   
def execute_name(self, context):
    selectName(self.name_enum)

def name_option(self, context):
    enum_names = []
    name_obj = bpy.data.collections['Names'].all_objects
    count = 0
    for obj in name_obj:
        enum_names.append((obj.name, obj.name, '', 'USER', count))
        count += 1
    return enum_names
        
def update_name_option(self, context):
    enum_names = name_option(self, context)
    print(enum_names)
    return None
        
        
   
   
   

#=============================================================
#  MAIN OPERATOR
#=============================================================  
class REAL_OT_AutoRenderer(Operator):
    bl_idname = "rabichora.autorender"
    bl_label = "Auto Renderer"
    bl_description = "自动渲染模型展示图片"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        
        start = time.time()
        #render the images
        for scn in bpy.data.scenes:
            bpy.context.window.scene = scn
            bpy.ops.render.render()
            
        #change pic names
        #C:\Users\rabichorali\Pictures\StandardRenderer\
        imgPath = 'C:\\tmp\\'

        targetName_models = 'Scene_Models.png'
        targetName_background = 'Scene_Background.png'
        file_exist = False
        for (root, dir, files) in os.walk(imgPath, topdown = True):
            for f in files:
                fileName = os.path.basename(f)
                
                isTarget_models = fileName[:len(targetName_models)] == targetName_models
                if fileName == targetName_models:
                    file_exist = True
                if isTarget_models and len(fileName) > len(targetName_models):
                    if file_exist:
                        os.remove(root + targetName_models)
                    os.rename(root + fileName, root + targetName_models)
                    file_exist = False
                    
                isTarget_background = fileName[:len(targetName_background)] == targetName_background
                if fileName == targetName_background:
                    file_exist = True
                if isTarget_background and len(fileName) > len(targetName_background):
                    if file_exist:
                        os.remove(root + targetName_background)
                    os.rename(root + fileName, root + targetName_background)
                    file_exist = False
                    
        
        os.system("start Photoshop.exe " + bpy.utils.user_resource('SCRIPTS', "addons") + "\\Auto Blender Tools\\Combine2.jsx")
        
        time.sleep(35)
        
        for a in bpy.context.screen.areas:
            if a.type == 'IMAGE_EDITOR':
                image_area = a.spaces[0]
                break
        
        #bpy.data.scenes[0] = Background
        #bpy.data.scenes[1] = Models
        if bpy.context.window.scene.name == 'Models':
            bpy.context.window.scene = bpy.data.scenes[0]
        # #process with the result pixels
        path = imgPath + 'RenderedImage.png'
        bpy.ops.image.open(filepath = path)
        img = bpy.data.images['RenderedImage.png']
        image_area.image = img
        newImgName = 'RenderedImage'

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
        output_node.base_path = imgPath
        img_path = img.filepath
        output_node.file_slots[0].path = newImgName + ".png"
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
        targetName = newImgName + '.png'
        file_exist = False
        for (root, dir, files) in os.walk(imgPath, topdown = True):
            for f in files:
                fileName = os.path.basename(f)
                if fileName == targetName:
                    file_exist = True
                isTarget = fileName[:len(targetName)] == targetName
                if isTarget and len(fileName) > len(targetName):
                    if file_exist:
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

        bpy.ops.image.open(filepath = path)
        new_img = bpy.data.images[targetName]
        image_area.image = new_img
        
        elapsed_time_fl = (time.time() - start)
        print('Rendering took ' + str(elapsed_time_fl) + ' second')
                
        bpy.context.window.scene = bpy.data.scenes[1]
        
        return {'FINISHED'}
    
    
    




#=============================================================
#  APPEND FILE OPERATOR
#=============================================================
class Appen_OT_File(Operator):
    bl_idname = 'operator.appendtemplate'
    bl_label = 'Append Template'

    def execute(self, context):

        active_scene = bpy.context.scene
        file_path = bpy.utils.user_resource('SCRIPTS', "addons") + '\\3D角色渲染模板.blend'
        scene_path = 'Scene'
        workspace_path = "WorkSpace"
        bpy.ops.wm.append(
            filepath = os.path.join(file_path, scene_path, 'Models'),
            directory = os.path.join(file_path, scene_path),
            filename='Models'
        )
        bpy.ops.wm.append(
            filepath = os.path.join(file_path, scene_path, 'Background'),
            directory = os.path.join(file_path, scene_path),
            filename='Background'
        )
        bpy.context.window.scene = bpy.data.scenes['Models']
        bpy.data.scenes.remove(active_scene)

        bpy.ops.wm.append(
            filepath = os.path.join(file_path, workspace_path, 'Main Workspace'),
            directory = os.path.join(file_path, workspace_path),
            filename='Main Workspace'
        )
        bpy.context.window.workspace = bpy.data.workspaces['Main Workspace']






#=============================================================
#  PANEL
#=============================================================
class REAL_PT_AutoPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_context = ""
    bl_region_type = "UI"
    bl_label = "自动化渲染"
    bl_category = u"自动化渲染"

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        bgcolor = scn.bgcolor_enum

        col = layout.column(align=True)


        bl_label = "Auto tools"
        
        row_bgcolor = layout.row(align=True)
        row_bgcolor.scale_y = 1 
        #row_bgcolor.label(text = '更改背景颜色:')
        row_bgcolor.prop(bgcolor, 'bg_color_enum', text = '背景颜色') 
        
        row_title = layout.row(align=True)
        row_title.scale_y = 1 
        #row_title.label(text = '更改节点名:')
        row_title.prop(scn, 'title_enum', text = '节点名')      
        
        row_name = layout.row(align=True)
        row_name.scale_y = 1 
        #row_name.label(text = '更改作者名:')
        row_name.prop(scn, 'name_enum', text = '作者名') 
        
        row = layout.row(align=True)
        row.scale_y = 1.5
        row.operator("rabichora.autorender", text="自动化渲染", icon="IMAGE_ZDEPTH")
        
        row1 = layout.row(align=True)
        row1.scale_y = 1
        row1.operator("wm.url_open", text="Help").url = "https://iwiki.woa.com/pages/viewpage.action?pageId=807726005"
        

        




    
#=============================================================
#  CLASSES
#=============================================================
classes = {
    
    REAL_PT_AutoPanel,
    
    BG_Color_Enum,
    
    REAL_OT_AutoRenderer
    
}







#=============================================================
#  REGISTER
#=============================================================
def render_register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bgcolor_enum = PointerProperty(type = BG_Color_Enum)
    bpy.types.Scene.title_enum = bpy.props.EnumProperty(
        items = title_option,
        description = '选择节点名',
        default = None,
        update = execute_title
    )
    bpy.types.Scene.name_enum = bpy.props.EnumProperty(
        items = name_option,
        description = '选择作者名',
        default = None,
        update = execute_name
    )


def render_unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.bgcolor_enum
    del bpy.types.Scene.title_enum
    del bpy.types.Scene.name_enum


#=============================================================
#  MAIN
#=============================================================
if __name__ == "__main__":
    render_register()
