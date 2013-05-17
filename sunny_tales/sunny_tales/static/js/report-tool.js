selection_id = {}
properties = {}
$(function() {
	$('body').layout({
		applyDefaultStyles : true
	});
	load_document();

	$("#canvas").droppable({
		activeClass : "ui-state-default",
		hoverClass : "ui-state-hover",
		drop : function(event, ui) {
			element_id = ui.draggable.attr("element_id");
			my_selection_id = ui.draggable.attr("id");

			if (element_id === undefined) {
				element_id = my_selection_id;
				//this is first time dragging.
				//make it unique and save original id to element_id
				//ui.draggable.attr('element_id',element_id)
				my_selection_id = generate_selection_id(element_id);
				value = ui.draggable.attr("value");
				new_element = $(value);
				new_element.attr("id", my_selection_id);
				new_element.attr("element_id", element_id);
				new_element.css('cursor', 'move')
				new_element.click(function() {
					populateStyleLayout($(this))
				})
				new_element.appendTo(this);
				if (element_id !== undefined && properties[element_id].resizable)
					$("#" + my_selection_id).resizable();
				$("#" + my_selection_id).draggable();
			}

		}
	});

});

// move to another file
function generate_selection_id(id) {
	var uid = selection_id[id];
	if (uid === undefined) {
		selection_id[id] = 0;
		uid = 0;
	}
	selection_id[id]++;
	return id + "_" + uid;
}

// refactor this
function load_document() {
	$.ajax({
		dataType : 'json',
		url : '/api/v0/template/new',
		success : function(data) {
			var id = data.id
			var elements = data.elements
			var template = get_template('elements.template')
			var output = Mustache.render(template, data)
			$("#selections").append(output)
			for (var i = 0; i < data.elements.length; i++) {
				var id = "#" + data.elements[i].type;
				properties[data.elements[i].type] = convertStyleJSONToHTMLStyle(data.elements[i].style);
				//properties[data.elements[i].type]=data.elements[i]
				make_draggable($(id));
			}
		},
		error : function(ts) {
			alart(ts.responseText)
		}
	})
}

function get_template(template_name) {
	var template;
	var target = '/static/html/templates/' + template_name
	$.ajax({
		dataType : 'html',
		url : target,
		async : false,
		success : function(response) {
			template = response;
		},
		error : function(ts) {
			alert(ts.responseText)
		}
	});
	return template;
}

function make_draggable(id) {
	id.draggable({
		appendTo : "body",
		helper : "clone"
	});
}

// display style property on style layout
function populateStyleLayout(clicked_element) {
	var element_id = clicked_element.attr('element_id')
	var property = properties[element_id]
	var template = get_template('element_style.template')
	var output = Mustache.render(template, property)
	$("#style").html(output);
	$("#style #text").html(clicked_element.html())
}

function createSelect(id, selections, default_value) {
	var select = $("<select></select>");
	select.attr('id', id);
	var i = 0;
	while (i < selections.length) {
		var selection = selections[i];
		var selected = '';
		if (default_value === selection) {
			selected = 'selected';
		}
		select.append('<option ' + selected + ' value=' + selection + '>' + selection + '</option>');
		i++;
	}
	return select.wrap('<div/>').parent().html();
}

function convertStyleJSONToHTMLStyle(style_json) {
	var i = 0;
	var html_style = [];
	while (i < style_json.length) {
		var html_output = {};
		var style = style_json[i];
		var input_type = style.input_type;
		var html = style.html;
		var user_input;

		var selection = style.selection;
		html_output['name'] = style.name;
		var id = style.name.replace(' ', '_').toLowerCase();
		// if there is "selections", then create select element
		if (selection === undefined) {

			if (input_type === "string") {
				if (html === undefined) {
					user_input = "<input type='text'></input>";
				} else {
					user_input = html;
				}
			} else if (input_type === "bool") {
				if (html === undefined) {
					user_input = "<input type='checkbox'></input>";
				} else {
					user_input = html;
				}
			} else if (input_type === "int") {
				if (html === undefined) {
					user_input = "<input type='text'></input>";
				} else {
					user_input = html;
				}
			}
			var temp_input = $(user_input);
			temp_input.attr('id', id);
			user_input = temp_input.wrap('<div/>').parent().html();
		} else {
			user_input = createSelect(id, selection, style.default);
		}
		html_output['user_input'] = user_input;
		html_style.push(html_output);
		i++;
	}

	return {
		"style" : html_style
	};
}
