Tool = Backbone.Model.extend({
    defaults : {
        name : 'element name',
        type : 'element_type',
        value : '',
        resizable : false,
        style : []
    },
    //use "type" as Tool's id
    idAttribute : "type",
    initialize : function() {
        var html = this.get("html");
        var j_htmlObject = $(html);
        // Add id to identify where we should replace the text
        j_htmlObject.attr("id", "value");
        // Set the text
        j_htmlObject.text(this.get("value"));

        // Add relevant classes
        var wrapper = $("<div class='ui-widget-content resizable draggable'></div>");
        // Wrap around the html from config and convert to html string
        $(j_htmlObject).appendTo(wrapper);
        
        j_htmlObject = $('<div>').append($(wrapper).clone()).html();
        this.set("html", j_htmlObject);
    }
});
