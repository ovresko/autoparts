from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
            "label": "Gestion autoparts",
            "items":[
                {
                    "type": "doctype",
                    "name": "Modele automobile"
                },
                {
                    "type": "doctype",
                    "name": "Version automobile"
                },
                {
                    "type": "doctype",
                    "name": "Constructeur"
                },
                {
                    "type": "doctype",
                    "name": "Item"
                },
                {
                    "type": "doctype",
                    "name": "Brand"
                }
            ]
        },
		{
			"label": _("Stock Reports"),
			"items": [				
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Balance",
					"doctype": "Stock Ledger Entry"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Projected Qty",
					"doctype": "Item",
				},
				{
					"type": "page",
					"name": "stock-balance",
					"label": _("Stock Summary")
				}
			]
		}
	]
