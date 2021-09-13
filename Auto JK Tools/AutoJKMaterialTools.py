import bpy
import os
from bpy.props import BoolProperty, FloatProperty, IntProperty, PointerProperty,StringProperty
from bpy.types import Operator, Panel, PropertyGroup
from mathutils import Vector

    

from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
    
##Interface Panel
#class DenoiseImagePanel(bpy.types.Panel):
class REAL_PT_AutoMate(Panel):
    bl_space_type = "NODE_EDITOR"
    bl_context = ""
    bl_region_type = "UI"
    bl_label = "JK材质工具"
    bl_category = u"JK材质工具"


    def draw(self, context):
        scn = context.scene
        layout = self.layout


        col = layout.column(align=True)


        bl_label = "AutoMaterial Tools"

        row = layout.row(align=True)
        row.scale_y = 1.5
        row.operator("rabichora.replacetex", text="根据 颜色贴图 查找其他", icon="IMAGE_ZDEPTH")

    
  

class REAL_OT_AutoMate(Operator):
    bl_idname = "rabichora.replacetex"
    bl_label = "Replace Texture"
    bl_description = "根据Albedo贴图寻找其他贴图"
    bl_options = {'REGISTER', 'UNDO'}
    
    debugMode=False

    #bpy.ops.test.open_filebrowser('INVOKE_DEFAULT')

    # @classmethod
    # def poll(cls, context) -> bool:
    #     enable=bool(context.area.spaces.active.image)
        
    #     return enable


    def execute(self, context):
        
        #ext="_tempNode_fengxzeng"
        tree = bpy.context.scene.node_tree
        mat=bpy.context.active_object.active_material
        if mat==None:
            return {'FINISHED'}
        tree=mat.node_tree.nodes
        ND=tree.get("Standard_D")
        NM=tree.get("Standard_M")
        NN=tree.get("Standard_N")
        NS=tree.get("Standard_S")
        NE=tree.get("Standard_E")

        if ND!=None:
            if ND.image!=None:
                if "_d_" in ND.image.filepath:
                        #if NM.image !=None:
                        ntexp=bpy.path.abspath(ND.image.filepath.replace("_d_","_m_"), library=ND.image.library)   
                        n=os.path.split(ntexp)[1]
                        t=bpy.data.images.get(n)
                        if t==None:
                            if os.path.exists(ntexp):
                                IMG_NM = bpy.data.images.load(filepath =ntexp )
                                if IMG_NM!=None:
                                    NM.image=IMG_NM
                                    print(IMG_NM)
                        else:
                            NM.image=t
                        #if NN.image !=None:
                        #ntexp=ND.image.filepath.replace("_d_","_n_")
                        ntexp=bpy.path.abspath(ND.image.filepath.replace("_d_","_n_"), library=ND.image.library)   
                        n=os.path.split(ntexp)[1]
                        t=bpy.data.images.get(n)
                        if t==None:
                            if os.path.exists(ntexp):
                                IMG_NN = bpy.data.images.load(filepath = ntexp)
                                if IMG_NN!=None:
                                    NN.image=IMG_NN
                                    print(IMG_NN)
                        else:
                            NN.image=t
                        print(ntexp)
                        #if NS.image !=None:
                        ntexp=bpy.path.abspath(ND.image.filepath.replace("_d_","_s_"), library=ND.image.library)   
                        #ntexp=ND.image.filepath.replace("_d_","_s_")
                        n=os.path.split(ntexp)[1]
                        t=bpy.data.images.get(n)
                        if t==None:
                            if os.path.exists(ntexp):
                                IMG_NS = bpy.data.images.load(filepath = ntexp)
                                if IMG_NS!=None:
                                    NS.image=IMG_NS
                                    print(IMG_NS)
                        else:
                            NS.image=t
                        print(ntexp)
                        #if NE.image !=None:
                        ntexp=bpy.path.abspath(ND.image.filepath.replace("_d_","_e_"), library=ND.image.library)   
                        #ntexp=ND.image.filepath.replace("_d_","_e_")
                        n=os.path.split(ntexp)[1]
                        t=bpy.data.images.get(n)
                        if t==None:
                            if os.path.exists(ntexp):
                                IMG_NE = bpy.data.images.load(filepath =ntexp)
                                if IMG_NE!=None:
                                    NE.image=IMG_NE
                                    print(IMG_NE)
                        else:
                            NE.image=t
                        print(ntexp)
                


        texsS=[ND,NE]
        texsL=[NM,NS,NN]


        for s in texsL:
            if s!=None:
                if s.image!=None:
                    s.image.colorspace_settings.name="Linear"
        for s in texsS:
            if s!=None:
                if s.image!=None:
                    s.image.colorspace_settings.name="sRGB"

        print(ND == None)
        self.report({'INFO'}, u"autu")
        return {'FINISHED'}
    



#############################################################################################
classes = (
    REAL_PT_AutoMate,
    REAL_OT_AutoMate,
    )


#material_register, material_unregister = bpy.utils.register_classes_factory(classes)


# Register
def material_register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_custom_save = bpy.props.BoolProperty(name="My Custom Save Property")
    
# Unregister
def material_unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    #del(bpy.types.Scene.directory)

if __name__ == "__main__":
    material_register()

    # test call