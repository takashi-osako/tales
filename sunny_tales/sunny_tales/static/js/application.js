/*
 * This is main function for template editor
 */
$(function() {
    // display layouts
    $('body').layout({
        applyDefaultStyles : true
    });
    
    var toolMenu = new ToolMenuModel;
    var templateModel = new TemplateModel;
    var styleCollection =  new StyleCollection;
    // render toolbox view
    var toolboxView = new ToolBoxView(toolMenu);
    var canvasView = new CanvasView(toolMenu, templateModel, styleCollection);
    var saveTemplateView = new SaveTemplateView(templateModel);
    var styleView = new StyleView(styleCollection);
    var createPdfView = new CreatePdfView(templateModel);
});