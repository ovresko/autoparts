# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ovresko Solutions Algerie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from autoparts.autoparts.doctype.sync_pos.frappeclient import FrappeClient
import json
from frappe.utils import getdate, get_datetime

class SyncPOS(Document):
	pass

@frappe.whitelist()
def save_data(doc):
	print("save_data %s" % doc)
	try:
		_obj = json.loads(doc)
		#_bypass_modified = _obj["_bypass_modified"]
		item = frappe.get_doc(_obj)
		item._bypass_modified = True
		item.modified = _obj["modified"]
		item._original_modified = _obj["modified"]
		item.save(ignore_permissions=True, ignore_version=True)
		frappe.db.commit()
		return "success"
		#url = self.url + "/api/resource/" + doc.get("doctype") + "/" + doc.get("name")
		#data = frappe.as_json(doc)
		#res = self.session.put(url, data={"data":data})
		#return self.post_process(res)
	except Exception:
		return frappe.get_traceback()
@frappe.whitelist()
def set_last_modified(doctype,date,client):
	lsp = frappe.db.get_list("Sync Last Push", fields = ['*'] ,filters = {'document_type':doctype,"client":client})
	found = False
	if lsp:
		dt = lsp[0]
		if dt:
			#dt.date = get_datetime(date) 
			frappe.db.sql("""update `tabSync Last Push` set date = %s where name = '%s'""" % (date,dt.name))
			#rappe.db.set_value("Sync Last Push",dt.name,"date",dt.date)
			found = True
	if not found:
		sp = frappe.get_single('Sync POS')
		new_lsp = frappe.get_doc({
			'doctype': 'Sync Last Push',
			'parent': sp.name,
			'date':date,
			'parentfield':'sync_last_push',
			'parenttype':'Sync POS',
			'document_type':doctype,
			'client':client
		})
		new_lsp.insert()
		frappe.db.commit()
	
	return "last_edit_result = %s %s " % (dt.name,date)

@frappe.whitelist()
def get_last_modified(doctype,client):
	if doctype and client:
		lsp = frappe.db.get_list("Sync Last Push", 
					 fields = ['*'],
					 order_by='modified asc',
					 limit_page_length=1,
					 filters = {'document_type':doctype,"client":client})
		if lsp:
			dt = lsp[0]
			if dt:
				dtd =  dt.date.strftime("%Y-%m-%d %H:%M:%S.%f")
				print("LAST EDIT TARGET %s" % dtd)
				return dtd
	return None

def start_sync():
	sp = frappe.get_single('Sync POS')
	user = sp.user
	pwd = sp.password
	url = sp.serveur
	do_sync = sp.sync
	client = sp.client_name
	items = sp.sync_pos_item
	if(user and url and pwd and do_sync and items):
		print("%s %s %s" % (url,user,pwd))
		conn = FrappeClient(url, user, pwd)
		for dt in items:
			if not dt.document_type:
				continue
			#lid = get_last_modified(dt.document_type)	
			# sync back
			if dt.sync:
				try:
					last_edit = conn.get_api(
						"autoparts.autoparts.doctype.sync_pos.sync_pos.get_last_modified",
								 params={"doctype":dt.document_type,"client":client}
					)
				except:
					print("Something went wrong")
				else:
					print("last_edit %s" % last_edit)
					my_items = []
					if last_edit:
						my_items = frappe.db.get_list(dt.document_type, fields = ['*'],order_by='modified asc',limit_page_length=20, filters = {'modified':(">", last_edit),'docstatus':("<", 2)})
					else:
						my_items = frappe.db.get_list(dt.document_type, fields = ['*'],order_by='modified asc',limit_page_length=20, filters = {'docstatus':("<", 2)})
					print("found to push %s" % len(my_items or []))
					if my_items:
						for val in my_items:
							if not val:
								continue
							val["doctype"] = dt.document_type

							
							val = frappe.get_doc(val)
							print("uploading: %s" % val.name)
							
							if val:
								try:
									if not last_edit or (get_datetime(val.modified) > get_datetime(last_edit)):
										last_edit = get_datetime(val.modified)
									val._original_modified = val.modified
									val.flags.ignore_if_duplicate = True
									val.flags.ignore_links = True
									val.flags.ignore_permissions = True
									val.flags.ignore_mandatory = True
									val._bypass_modified = True
									result = conn.get_api(
										"autoparts.autoparts.doctype.sync_pos.sync_pos.save_data",
												 params={"doc":val.as_json()}
									)
									#data = val.as_dict()
									
									#conn.update(data)
								except Exception:
									msg = frappe.get_traceback()
									print("ERROR %s " % (msg or ''))
						if last_edit:
							last_edit_result = conn.get_api("autoparts.autoparts.doctype.sync_pos.sync_pos.set_last_modified",
											params={"doctype":dt.document_type,"date":last_edit,"client":client })
							print("up result %s %s: %s " % (result,last_edit,last_edit_result))
									


			# sync up
			if dt.sync_pull:
				result = []
				
				#_last = frappe.get_all(dt.document_type,fields=["name","modified"],order_by='modified desc',limit=1)
				#if lid and lid != "empty":
				#	result = conn.get_list(dt.document_type, fields = ['*'], filters = {'modified':(">", lid),'docstatus':("<", 2)})
				#el
				if dt.date_sync:
					dtd =  dt.date_sync.strftime("%Y-%m-%d %H:%M:%S.%f")
					print("dt %s" % dtd)
					result = conn.get_list(dt.document_type, fields = ['*'],order_by='modified asc',limit_page_length=20, filters = {'modified':(">", dtd),'docstatus':("<", 2)})
				else:
					result = conn.get_list(dt.document_type, fields = ['*'],order_by='modified asc',limit_page_length=20, filters = {'docstatus':("<", 2)})
				print("found to pull %s" % len(result or []))
				if result:
					#dt.date_sync = 
					for val in result:
						if not val:
							continue
						val["doctype"] = dt.document_type


						val = frappe.get_doc(val)
						print("downloading: %s" % val.name)


						try:
							if not dt.date_sync or (get_datetime(val.modified) > get_datetime(dt.date_sync)):
								dt.date_sync = get_datetime(val.modified)
								print("changing date %s " % dt.date_sync)
							print("exists %s %s %s" % (val.modified,val.name,get_datetime(dt.date_sync)))
							val._original_modified = val.modified
							val.flags.ignore_if_duplicate = True
							val.flags.ignore_links = True
							val.flags.ignore_permissions = True
							val.flags.ignore_mandatory = True
							val._bypass_modified = True
							val.save(ignore_permissions=True, ignore_version=True)
							frappe.db.commit()
						except:
							msg = frappe.get_traceback()
							print("get went wrong %s" % msg)
							
					#frappe.db.set_value("Sync DocTypes",dt.name,"date_sync",dt.date_sync)
					frappe.db.sql("""update `tabSync DocTypes` set date_sync = %s where name = '%s'""" % (dt.date_sync,dt.name))
					print("last sync pull %s" % dt.date_sync)
