var username = $.getenv("USERNAME");
var basicPath = "C:/tmp/";
//alert(username)

var fileModel = File(basicPath + "Scene_Models.png");
var imageModel = app.open(fileModel);

var fileBackground = File(basicPath + "Scene_Background.png");
var imageBackground = app.open(fileBackground);

app.activeDocument = imageBackground;

var doc = app.activeDocument;
var newLayer = doc.artLayers.add();
newLayer.name = "Models";

app.activeDocument = imageModel;
doc = app.activeDocument;
doc.activeLayer.copy();

var cTID = function(s) { return app.charIDToTypeID(s); };
var sTID = function(s) { return app.stringIDToTypeID(s); };

function pasteInPlace(enabled, withDialog) {
    if (enabled != undefined && !enabled)
      return;
    var dialogMode = (withDialog ? DialogModes.ALL : DialogModes.NO);
    var desc1 = new ActionDescriptor();
    desc1.putBoolean(sTID("inPlace"), true);
    desc1.putEnumerated(cTID('AntA'), cTID('Annt'), cTID('Anno'));
    executeAction(cTID('past'), desc1, dialogMode);
  };

app.activeDocument = imageBackground;
pasteInPlace();

function sfwPNG24(saveFile){
    var pngOpts = new PNGSaveOptions;
    pngOpts.compression = 9;
    pngOpts.interlaced = false;
    activeDocument.saveAs(saveFile, pngOpts, true, Extension.LOWERCASE);
}
var savePath = basicPath + "RenderedImage.png";
var saveFile = File(savePath);
sfwPNG24(saveFile);
activeDocument.saveAs(saveFile);

imageBackground.close(SaveOptions.SAVECHANGES);
imageModel.close(SaveOptions.DONOTSAVECHANGES);