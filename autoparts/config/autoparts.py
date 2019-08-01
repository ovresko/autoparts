from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
            "label": "Gestion autoparts",
            "items": [
                
                {
                    "type": "doctype",
                    "name": "Version vehicule",
					"description": _("Version vehicule"),
                },
				{
                    "type": "doctype",
                    "name": "Generation vehicule",
					"description": _("Generation vehicule"),
                },
                {
                    "type": "doctype",
                    "name": "Modele de vehicule",
					"description": _("Modele de vehicule"),
                },
		{
                    "type": "doctype",
                    "name": "Marque vehicule",
					"description": _("Marque vehicule"),
                },
                {
                    "type": "doctype",
                    "name": "Item",
					"description": _("Article"),
                },
                {
                    "type": "doctype",
                    "name": "Brand",
					"description": _("Marque"),
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
				},
				{
					 "type": "report",
                                        "is_query_report": True,
                                        "name": "Versions sans articles",
                                        "doctype": "Version vehicule",
				}
			]
		}
	]
