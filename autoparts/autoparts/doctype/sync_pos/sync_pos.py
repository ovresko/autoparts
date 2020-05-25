# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ovresko Solutions Algerie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from autoparts.autoparts.doctype.sync_pos.frappeclient import FrappeClient


class SyncPOS(Document):
	pass

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
					my_items = []
					if last_edit and last_edit!= "empty":
						my_items = frappe.db.get_list(dt.document_type, fields = ['*'], filters = {'modified':(">", last_edit),'docstatus':("<", 2)})
					elif last_edit == "empty":
						my_items = frappe.db.get_list(dt.document_type, fields = ['*'], filters = {'docstatus':("<", 2)})

					if my_items:
						for val in my_items:
							if not val:
								continue
							val["doctype"] = dt.document_type

							print("up val %s " % val)
							val = frappe.get_doc(val)
							if val:
								try:
									val._original_modified = val.modified
									val.flags.ignore_if_duplicate = True
									val.flags.ignore_links = True
									val.flags.ignore_permissions = True
									val.flags.ignore_mandatory = True
									val._bypass_modified = True
									conn.update(val)
								except:
									print("push went wrong")


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
				#dt.date_sync = 
				for val in result:
					if not val:
						continue
					val["doctype"] = dt.document_type
					
					print("down val %s " % val)
					val = frappe.get_doc(val)
					
					#print(val)
					#if frappe.db.exists(dt.document_type,val.name):
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
						print("get went wrong")
					#else:
					#	print("new %s" % val.name)
					#	val._original_modified = val.modified
					#	val.flags.ignore_if_duplicate = True
					#	val.flags.ignore_links = True
					#	val.flags.ignore_permissions = True
					#	val.flags.ignore_mandatory = True
					#	val.docstatus=None
					#	val._bypass_modified = True
					#	val.__islocal = True
					#	val.insert(
					#		ignore_permissions=True,
					#		ignore_links=True, 
					#		ignore_if_duplicate=True,
					#		ignore_mandatory=True)
					#	frappe.db.commit()
			
