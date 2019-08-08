// Copyright (c) 2019, Ovresko Solutions Algerie and contributors
// For license information, please see license.txt

frappe.ui.form.on('Critere vehicule', {
	setup: function(frm) {
		console.log('setting query '+frm.doc.critere);
		
		frm.set_query('valeur',function(){
		return {
				filters:[{'parent':frm.doc.critere}]
			};
		});
	}
});
