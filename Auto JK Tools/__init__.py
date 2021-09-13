bl_info = {
    "name": "Auto JK Tools",
    "description": "自动化贴图处理，自动化降噪图片，自动化渲染",
    "author": "rabichora",
    "version": (0, 1),
    "blender": (2, 93, 0),
    "location": "NodeEditor > Properties Panel; Image Editor > Properties Panel; View3D > Properties Panel",
    "doc_url": "https://github.com/xxxx",
    "tracker_url": "https://github.com/xxxx",
    "category": "Object",
    }

if 'bpy' in locals():
    import importlib
    if 'RenderTemplate' in locals():
        importlib.reload(RenderTemplate)
    if 'AutoDenoise' in locals():
        importlib.reload(AutoDenoise)
    if 'AutoJKMaterialTools' in locals():
        importlib.reload(AutoJKMaterialTools)
else:
    import bpy
    from . import (RenderTemplate)
    from . import (AutoDenoise)
    from . import (AutoJKMaterialTools)

def register():
    from .RenderTemplate import render_register
    render_register()
    from .AutoDenoise import denoise_register
    denoise_register()
    from .AutoJKMaterialTools import material_register
    material_register()

def unregister():
    from .RenderTemplate import render_unregister
    render_unregister()
    from .AutoDenoise import denoise_unregister
    denoise_unregister()
    from .AutoJKMaterialTools import material_unregister
    material_unregister()
    