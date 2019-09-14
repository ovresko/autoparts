frappe.ui.form.on("Fiche technique item", {
	validate: function(frm){
		frm.set_value("titre",frm.doc.parametre+" "+frm.doc.valeur_p+" "+frm.doc.valeur);
	}}
