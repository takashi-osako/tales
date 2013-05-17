SaveTemplateView = Backbone.View.extend({
    el : $('#menu'),
    initialize : function(b_model_template) {
        this.b_template = b_model_template
    },
    events : {
        "click #save-template" : "saveTemplate",
        "change #bol-name" : "setName",
    },
    saveTemplate : function() {
        //call RESTFul to store jsonTemplate
        this.b_template.save();
    },
    setName : function(e) {
        var value = $(e.currentTarget).val();
        this.b_template.set("name", value);
    }
});
