// Copyright (c) 2018, Ovresko Solutions Algerie and contributors
// For license information, please see license.txt

frappe.ui.form.on('Version vehicule', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 0 ) {
				frm.set_df_property('origin', 'default', null);
			}
	}
});
