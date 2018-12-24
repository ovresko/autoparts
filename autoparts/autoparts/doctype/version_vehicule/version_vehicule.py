# -*- coding: utf-8 -*-
# Copyright (c) 2018, Ovresko Solutions Algerie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.selling.doctype.sales_order.sales_order import make_material_request
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
from frappe.desk.form import assign_to
from erpnext.utilities.product import get_price, get_qty_in_stock

class Versionvehicule(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_item_price(item_code, price_list, customer_group, company, qty=1):
	price = get_price(
		item_code,
		price_list,
		customer_group,
		company,
		qty
	)

	return price

def create_demande(doc,method):
	if(doc.creer_demande_materiel == 1):
		stock_settings = frappe.get_single('Stock Settings')
		req = make_material_request(doc.name)
		req.schedule_date = doc.delivery_date
		req.material_request_type = "Material Transfer"
		user = stock_settings.compte_assigner_stock
		req.save()
		doc.demande_associe = req.name
		for line in doc.items:
			line.qts_prepares = line.qty
		doc.save()
		req.submit()
		assign_to.add({
				"assign_to": user,
				"doctype": "Material Request",
				"name": req.name,
				"description": "Transfert"+ " - " + doc.name
			})		
		frappe.msgprint("Demande materiel cree !")

@frappe.whitelist()
def sync_cmd(cmd_name,req):
	stock_entrise = frappe.get_all("Stock Entry",filters={"docstatus":1, "material_request":req},fields=["name"])
	result = []
	for entry in stock_entrise:
		item = frappe.get_doc("Stock Entry",entry)
		result.append(item)
	
	if result:
		SE = result[0].items
		commande = frappe.get_doc("Sales Order",cmd_name)
		for item in commande.items:
			first_or_default = next((x for x in SE if item.item_code == x.item_code), None)
			item.qts_prepares = first_or_default.qty
		
		commande.save()
	else:
		frappe.msgprint("Demande materiel n'est pas terminé! vérifier avec gestionnaire de stock !")
	return result

@frappe.whitelist()
def update_cmd_invoice(cmd_name,req):
	stock_entrise = frappe.get_all("Stock Entry",filters={"docstatus":1, "material_request":req},fields=["name"])
	result = []
	for entry in stock_entrise:
		item = frappe.get_doc("Stock Entry",entry)
		result.append(item)
	
	if result:
		SE = result[0].items
		commande = frappe.get_doc("Sales Order",cmd_name)
		for item in commande.items:
			first_or_default = next((x for x in SE if item.item_code == x.item_code), None)
			item.qts_prepares = first_or_default.qty		
		commande.save()
		invoice = make_sales_invoice(cmd_name)
		# invoice.is_pos = True
		for item in invoice.items:
			first_or_default = next((x for x in SE if item.item_code == x.item_code), None)
			item.qty = first_or_default.qty

		update_stocke = frappe.get_value("Selling Settings", None, "vente_sans_bon_livraison")
		if update_stocke:
			invoice.update_stock = update_stocke
		invoice.save()
	else:
		frappe.msgprint("Demande materiel n'est pas terminé! vérifier avec gestionnaire de stock !")
		return None
	return invoice
