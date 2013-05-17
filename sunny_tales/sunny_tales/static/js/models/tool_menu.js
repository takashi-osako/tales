ToolMenuModel = Backbone.Model.extend({
	initialize : function() {
		this.set("tools", new ToolsCollection)
	},
	tools : null,
	url : '/api/v0/toolbox',
	idAttribute: "_id",
	parse : function(response) {
		if (response) {
		    // Save the 'style' that is common for all elements
		    this.set("common_style", response.style);
			var listSource = this.get("tools");
			_.each(response.elements, function(element, index, list) {
				listSource.add(new Tool(element));
			});
			return listSource;
		}
	}
})
