// Copyright (c) 2019, Ovresko Solutions Algerie and contributors
// For license information, please see license.txt

frappe.ui.form.on('Outil Creation Article Excel', {

	onload: function(frm) {
	
	},

	refresh: function(frm) {
	 	
			frm.disable_save();
			frm.page.set_primary_action(__('Create Invoices'), () => {
			let btn_primary = frm.page.btn_primary.get(0);
			return frm.call({
				
				
				}
			});
		});
  	
	},
	lancer: function(frm){
	  frappe.call({     
		method: "autoparts.doctype.outil_creation_article_excel.outil_creation_article_excel.lancer",     
		callback: function(r) 
		{
			
		};
	
			});
	}
});
