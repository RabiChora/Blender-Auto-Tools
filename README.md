# JK自动化Blender插件使用指南

## 功能

- 自动贴图填充

- 自动图片降噪

- 自动展示图片渲染

  

## 安装方法

下载：

1. 将下载的压缩文件包**解压到当前文件夹**：![image-20210902095719834](https://i.loli.net/2021/09/02/LeBfMSTyFW4agvC.png) $>$ ![image-20210902095733162](https://i.loli.net/2021/09/02/ngi4cyHR9YBCSh8.png)

2. 打开blender；

3. 在左上角的菜单栏点击Edit > Preferences... 
	![image-20210831130832321](C:\Users\rabichorali\AppData\Roaming\Typora\typora-user-images\image-20210831130832321.png)
	
4. 在弹出的窗口选择 Add-ons，然后再右上角点击Install...
	![image-20210831130953960](C:\Users\rabichorali\AppData\Roaming\Typora\typora-user-images\image-20210831130953960.png)
	
5. 在弹出的新窗口中选择刚才解压好的文件夹 **JK Blender Tools** 下面的**Auto JK Tools.zip** 
    *（注意这个压缩包**不要解压！！**）*
    ![image-20210902095827832](https://i.loli.net/2021/09/02/j5caBEbGoVlh7IH.png)

6. 最后在安装好之后会弹出下面这个界面，勾选上这个插件就可以了。
   ![image-20210831131426513](C:\Users\rabichorali\AppData\Roaming\Typora\typora-user-images\image-20210831131426513.png)
   
   

## 功能简介与使用方法

### 1. 自动贴图填充工具

会根据Albedo（颜色贴图）的名字在对应文件夹里查找前缀相同的图片，填入正确的节点中。（如下图）
<img src="https://i.loli.net/2021/08/31/jbFzdLnQVGP3u5w.png" alt="贴图填充.png" style="zoom:67%;" />

**需要图片节点的Name是“Standard_x”格式，x代表了图片的作用：**
![节点名称.png](https://i.loli.net/2021/08/31/Ko645Lx1BTwCDPI.png)
D：颜色
M：R-金属度；G-粗糙度；B-AO
N：法线
E：自发光
S：3S

***Blender模板材质名称：JKStandard***

使用方法：
- 打开blend文件之后会出现两个界面，在左边界面（主界面，比较大的界面）左下角板块的Shader Editor（板块的左上角图标为：![image-20210831102615827](https://i.loli.net/2021/08/31/cnP9N6ZLwzTlIy7.png))中，在名为“颜色贴图D”的节点中点击“Open”，在弹出的窗口中选择合适的规范命名贴图。
  ![](https://i.loli.net/2021/08/31/qZ2MbikoswrzRQF.png)<img src="https://i.loli.net/2021/08/31/9fBcSd6UonWV8TF.png" alt="image-20210831103203718" style="zoom: 50%;" />

- 之后在同一个板块的右侧边栏点击最后一个标签“JK材质工具”，之后点击“根据颜色贴图查找其他”即可填入缺失的其他贴图。
<img src="https://i.loli.net/2021/08/31/bnGo4FZQTHXJmO6.png" alt="image-20210831103416486" style="zoom:67%;" />



### 2. 自动图片降噪工具

会为***导入的本地图片或者blender缓存中的图片***进行降噪并储存为新的图片或覆盖原图进行储存（可选择）。

***不支持为Viewer Node中的图片进行直接降噪***，如果有需要为渲染结果进行降噪请先将图片存入本地再导入进入blender。

使用方法：

- 打开一个Image Editor板块（板块左上角图标为：![image-20210831104232070](C:\Users\rabichorali\AppData\Roaming\Typora\typora-user-images\image-20210831104232070.png))
  <img src="https://i.loli.net/2021/08/31/sraSfIubWRJpOlD.png" alt="image-20210831104201198" style="zoom: 67%;" />

- 打开一张图片；
- **将输入法切换为英文**，按下**“N”**打开侧边栏；
- 点击右手边侧边栏最下方的标签**“JK贴图降噪”**；
- 在弹出的面板中可以勾选是否需要**覆盖原图**进行保存；
	![image-20210831104552342](https://i.loli.net/2021/08/31/L38JRnB4GTywkzg.png)
- 最后点击按钮**“贴图降噪（已导入图片）”**进行自动降噪；
- 等待blender运行完毕后降噪的图片将展示在这个板块中，图片会储存在和导入的图片相同的文件夹中，如果需要储存在其他位置，可以点击上边栏中的Image > Save As...进行另存为：
![image-20210831104850015](C:\Users\rabichorali\AppData\Roaming\Typora\typora-user-images\image-20210831104850015.png)



### 3. 自动化模型模板图渲染

此功能需要在blender模板文件**“3D角色渲染模板.blend”**进行运行。在导入了对应模型，修改了版头文字，背景颜色和阴影颜色之后点击按钮即可一键渲染出模板图。

使用方法：

- 打开blender模板文件**“3D角色渲染模板.blend”**
  
- 导入模型；

- 将模型拖入**“角色”**Collection； 

  ***<u>（不要新建Collection！不要新建Collection！！不要新建Collection！！！）</u>***
![image-20210831112159744](https://i.loli.net/2021/08/31/ZQUD84ydRVvo95n.png)

- 在插件界面更改节点名，作者名，和背景颜色：
  ![image-20210902100016102](C:\Users\rabichorali\AppData\Roaming\Typora\typora-user-images\image-20210902100016102.png)

  - **如何更改节点，作者名：**

    - 更改节点名：

      1. 在右侧图层栏里找到“文字” > "Titles": ![image-20210902170142203](https://i.loli.net/2021/09/02/irmFPHL3nYq4JjX.png)

      2. 选中任何一个**非灰色项目**：![image-20210902170251465](https://i.loli.net/2021/09/02/cResfrMGDxt69hH.png)**(不一定是当前图片中显示的项目)**

      3. 将鼠标移至窗口**左上角的3D View**中，键盘先按下**“Shift+D”**然后**鼠标按下右键**（这个操作会复制一个所选的项目在项目所在位置）；

      4. 然后键盘按下**Tab键**，进入编辑模式，按下**“Ctrl+A”**全选所有字母，**将输入法切为英文**，输入所需要的节点名，然后再次全选（Ctrl+A），拷贝（Ctrl+C），再次按下Tab键退出编辑模式；

      5. 在右侧的图层栏里会生成一个复制项目，名字为**“所选择拷贝的项目名.001”**：![image-20210902170916900](https://i.loli.net/2021/09/02/eYgAc9huQHi3P5m.png)

         双击这个名字，进入名字编辑模式之后，粘贴刚才拷贝的文本（Ctrl+V），这样新的节点名就会出现在插件的选项里了。

         ![image-20210902171124492](C:\Users\rabichorali\AppData\Roaming\Typora\typora-user-images\image-20210902171142189.png)	![image-20210902171213382](https://i.loli.net/2021/09/02/AgcxtWU5HFTPQ4E.png)

    - 更改作者名：

      1. 在右侧图层栏找到“文字” > “Names”![image-20210902171441116](https://i.loli.net/2021/09/02/8wPyIgBnXfQYNrJ.png)

      2. 之后测操作与更改节点名一样，参考 更改节点名方法2-5步。

         

- 在**3D视图界面**调整模型位置，面向：

  点击选择右上角倒数第二个渲染模式，并点击视图内的相机按钮调整到相机视图

  ![image-20210831130039268](https://i.loli.net/2021/08/31/X1h8g5vmREWlK2T.png)

- 最后点击右边侧边栏最后一项**“JK自动化渲染”**，点击**“自动渲染”**进行渲染出图。（注意电脑需要事先安装好Photoshop，否则将不能完成渲染）
	![image-20210902100108189](https://i.loli.net/2021/09/02/OMWf1BcHDJ8InoN.png)
	
- 渲染后的图片会保存在 C:\tmp\ 这个文件夹下，想要另存在别的路径，可以点击**Image Editor**（模板blend文件右上角板块）中的Image > Save As...进行另存为：
  ![image-20210831104850015](C:\Users\rabichorali\AppData\Roaming\Typora\typora-user-images\image-20210831104850015.png)
