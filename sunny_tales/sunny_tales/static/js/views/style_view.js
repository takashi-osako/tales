StyleView = Backbone.View.extend({
    el : $("#style"),
    template : Handlebars.templates['style.template'],
    select_template : Handlebars.templates['style.select.template'],
    checkbox_template : Handlebars.templates['style.checkbox.template'],
    text_template : Handlebars.templates['style.text.template'],
    textarea_template : Handlebars.templates['style.textarea.template'],
    render : function(b_styleModel) {
        // Template
        var template_html = this.template(b_styleModel.toJSON());
        var j_style = this.$el;
        j_style.append(template_html);
        var b_styles = b_styleModel.get("styles");
        _.each(b_styles, function(b_style) {

            var targetCSS = b_style.css;
            if (targetCSS !== undefined && targetCSS.length > 0) {
                _.each(targetCSS, function(css) {
                    var css_name = css.name;
                    var defaults = css.defaults;
                    var value = this.b_styleModel.b_myModel.value(css_name);
                    var elementId = this.b_styleModel.get("elementId");
                    var updatingId = this.b_style.id;
                    if (value !== undefined && value !== null) {
                        if (css.data_type === "boolean") {
                            $("#style #" + elementId + " #" + updatingId).prop("checked", value);
                        } else {
                            $("#style #" + elementId + " #" + updatingId).val(value);
                        }
                        //firebox bug? I could not use method data()
                        $("#style #" + elementId + " #" + updatingId).attr("data-css-name", css_name);
                    }
                }, {
                    "b_styleModel" : this.b_styleModel,
                    "b_style" : b_style
                });
            }
        }, {
            "b_styleModel" : b_styleModel
        });

        // Set the textbox value if we have a textbox
        if (this.$el.find("#text").length) {
            this.$el.find("#text").val(b_styleModel.b_myModel.get("value"));
        }
        return this;
    },
    initialize : function(b_styleCollection) {
        this.b_styleCollection = b_styleCollection;
        this.b_styleCollection.bind("add", this.render, this);
        this.b_styleCollection.bind("reset", this.clear, this);
        // Register all the supported styles
        Handlebars.registerPartial('style.select.template', this.select_template);
        Handlebars.registerPartial('style.checkbox.template', this.checkbox_template);
        Handlebars.registerPartial('style.text.template', this.text_template);
        Handlebars.registerPartial('style.textarea.template', this.textarea_template);
    },
    clear : function() {
        this.$el.empty()
    },
    events : {
        "change #text" : "setTextValue",
        "change #style_top" : "setStyle",
        "change #style_left" : "setStyle",
        "change #style_width" : "setStyle",
        "change #style_height" : "setStyle",
        "change #style_border-width" : "setStyle",
        "change #style_border-style" : "setStyle",
        "change #font_family" : "setStyle",
        "change #font_size" : "setStyle",
        "change #text_align" : "setStyle",
        "change #underline" : "setStyle",
        "change #bold" : "setStyle",
        "change #italic" : "setStyle",
        "change #color" : "setStyle",
        "change #background_color" : "setStyle",
        "change #vertical_align" : "setStyle"
    },
    setStyle : function(e) {
        var b_myModel = this.b_styleCollection.at(0).b_myModel;
        var css_name = $(e.currentTarget).data('css-name');
        var value;
        if ($(e.currentTarget).is(":checkbox")) {
            value = $(e.currentTarget).prop("checked");
        } else {
            value = $(e.currentTarget).val();
        }
        b_myModel.css_set(css_name, value);
    },
    setTextValue : function(e) {
        var b_myModel = this.b_styleCollection.at(0).b_myModel;
        var newValue = $(e.currentTarget).val();

        var htmlFriendlyValue = newValue.replace(/\r\n/g, '<br/>');

        // Sets the new text
        // This must be set before we update model's value for vertical alignment to work properly
        $('#' + b_myModel.cid + ' #value').html(htmlFriendlyValue);

        b_myModel.set("value", newValue);

        // Do we even care what is the value of html
        // This is not necessary but it's good to see the value is consistent
        var j_html = $(b_myModel.get("html"));
        $(j_html).find('#value').text(htmlFriendlyValue);
        var modifiedHtml = $('<div>').append($(j_html).clone()).html();

        b_myModel.set("html", modifiedHtml);
    }
});


// Check if we need \n or \r\n saved in template
// $.valHooks.textarea = {
    // get : function(elem) {
        // return elem.value.replace(/\r?\n/g, "\r\n");
    // }
// }; 