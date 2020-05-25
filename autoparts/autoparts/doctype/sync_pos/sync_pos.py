# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ovresko Solutions Algerie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from autoparts.autoparts.doctype.sync_pos.frappeclient import FrappeClient
import json

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
		return "success %s" % (item.name)
		#url = self.url + "/api/resource/" + doc.get("doctype") + "/" + doc.get("name")
		#data = frappe.as_json(doc)
		#res = self.session.put(url, data={"data":data})
		#return self.post_process(res)
	except Exception:
		return frappe.get_traceback()
	
@frappe.whitelist()
def get_last_modified(doctype):
	if doctype:
		_last = frappe.get_all(doctype,fields=["name","modified"],order_by='modified desc',limit=1)
		if _last:
			li = _last[0]
			if li:
				lid =  li.modified.strftime("%Y-%m-%d %H:%M:%S.%f")
				print("lid %s" % lid)
				return lid
		else:
			# empty
			return "empty"
	return None

def start_sync():
	sp = frappe.get_single('Sync POS')
	user = sp.user
	pwd = sp.password
	url = sp.serveur
	do_sync = sp.sync
	items = sp.sync_pos_item
	if(user and url and pwd and do_sync and items):
		print("%s %s %s" % (url,user,pwd))
		conn = FrappeClient(url, user, pwd)
		for dt in items:
			if not dt.document_type:
				continue
				
			# sync back
			if dt.sync:
				try:
					last_edit = conn.get_api(
						"autoparts.autoparts.doctype.sync_pos.sync_pos.get_last_modified",
								 params={"doctype":dt.document_type}
					)
				except:
					print("Something went wrong")
				else:
					print("last_edit %s" % last_edit)
					my_items = []
					if last_edit and last_edit!= "empty":
						my_items = frappe.db.get_list(dt.document_type, fields = ['*'], filters = {'modified':(">", last_edit),'docstatus':("<", 2)})
					elif last_edit == "empty":
						my_items = frappe.db.get_list(dt.document_type, fields = ['*'], filters = {'docstatus':("<", 2)})
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
									print("up result %s " % result)
									#conn.update(data)
								except Exception:
									msg = frappe.get_traceback()
									print("ERROR %s " % (msg or ''))


			# sync up
			result = []
			lid = get_last_modified(dt.document_type)
			#_last = frappe.get_all(dt.document_type,fields=["name","modified"],order_by='modified desc',limit=1)
			if lid and lid != "empty":
				result = conn.get_list(dt.document_type, fields = ['*'], filters = {'modified':(">", lid),'docstatus':("<", 2)})
			elif dt.date_sync:
				dtd =  dt.date_sync.strftime("%Y-%m-%d %H:%M:%S.%f")
				print("dt %s" % dtd)
				result = conn.get_list(dt.document_type, fields = ['*'], filters = {'modified':(">", dtd),'docstatus':("<", 2)})
			elif lid == "empty":
				result = conn.get_list(dt.document_type, fields = ['*'], filters = {'docstatus':("<", 2)})
			if result:
				print("found to pull %s" % len(result or []))
				#dt.date_sync = 
				for val in result:
					if not val:
						continue
					val["doctype"] = dt.document_type
					
					
					val = frappe.get_doc(val)
					print("downloading: %s" % val.name)
					
					
					try:
						print("exists %s" % val.name)
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

