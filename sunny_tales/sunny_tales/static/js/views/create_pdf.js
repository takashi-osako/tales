CreatePdfView = Backbone.View.extend({
	el : $('#menu'),
	initialize : function(b_model_template) {
		this.b_template = b_model_template;
		this.b_pdf = new PdfModel();
	},
	events : {
		"click #create-pdf" : "createPdf",
	},
	createPdf : function() {
		// call RESTFul to request for pdf creation
		// Get id from template model and use the same id for pdf model
		var id = this.b_template.id;
		if (id) {
			window.open("/api/v0/createpdf/" + id + "/" + $('#bol-trans_ref_no').val(), name = "_blank")
			//this.b_pdf.id = id;
			//this.b_pdf.trans_ref_no = $('#bol-trans_ref_no').val()
			//this.b_pdf.fetch();
		}
	}
});
