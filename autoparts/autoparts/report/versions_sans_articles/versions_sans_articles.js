frappe.query_reports["Versions sans articles"] = {
    "filters": [
        {
            "fieldname":"item_group",
            "label": __("Groupe Article"),
            "fieldtype": "Link",
            "options": "Item Group",
		"reqd": 1,
		"on_change": function(query_report) {
				
				frappe.query_report.refresh();
			}
        },
    ]
}
