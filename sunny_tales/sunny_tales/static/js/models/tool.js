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
		var wrapper = $("<div class='resizable draggable' style='overflow:hidden;'></div>");
		// Wrap around the html from config and convert to html string
		var close_x = $("<div style='overflow: visible;'><img id=close_x src='/static/png/glyphicons_197_remove.png' style='position: absolute;display:none;top:-20px'></div>")

		j_htmlObject.appendTo(wrapper);
		wrapper.appendTo(close_x)

		//j_htmlObject = $("<div><img id=close_x src='/static/png/glyphicons_197_remove.png' style='position: absolute;display:none;'></div>").appendTo($(wrapper).clone()).html();
		this.set("html", close_x);
	}
});
