StyleModel = Backbone.Model.extend({
    initialize : function(b_myModel, styles) {
        this.set("styles", styles);
        this.b_myModel = b_myModel;
    },
    styles : null,
    targetId: null,
    elementId: null
});
