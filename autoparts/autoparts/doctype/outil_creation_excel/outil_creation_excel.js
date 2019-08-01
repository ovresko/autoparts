// Copyright (c) 2019, Ovresko Solutions Algerie and contributors
// For license information, please see license.txt

frappe.ui.form.on('Outil Creation Excel', {
	refresh: function(frm) {
		 frm.add_custom_button(__('Lancer la creation'), function(){
       			frappe.msgprint('Operation en cours'); 
			frappe.call({
			method: 'autoparts.autoparts.doctype.outil_creation_excel.outil_creation_excel.lancer',
			 args:{
                                groupe: frm.doc.groupe
                        },
			callback: (r) => {
				
			
				if (r.message) {
					frappe.msgprint(r.message);
				}
			}
			});
	
    		});		

	}
});
