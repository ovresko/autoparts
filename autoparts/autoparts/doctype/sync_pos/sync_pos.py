# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ovresko Solutions Algerie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from autoparts.autoparts.doctype.sync_pos.frappeclient import FrappeClient


class SyncPOS(Document):
	pass

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
			if not dt.sync or not dt.document_type:
				continue
			result = []
			_last = frappe.get_all(dt.document_type,fields=["name","modified"],order_by='modified desc',limit=1)
			if _last:
				li = _last[0]
				if li:
					lid =  li.modified.strftime("%Y-%m-%d %H:%M:%S")
					print("lid %s" % lid)
					result = conn.get_list(dt.document_type, fields = ['*'], filters = {'modified':(">", lid),'docstatus':("<", 2)})
			elif dt.date_sync:
				dtd =  dt.date_sync.strftime("%Y-%m-%d %H:%M:%S")
				print("dt %s" % dtd)
				result = conn.get_list(dt.document_type, fields = ['*'], filters = {'modified':(">", dtd),'docstatus':("<", 2)})
			else:
				result = conn.get_list(dt.document_type, fields = ['*'], filters = {'docstatus':("<", 2)})
			if result:
				#dt.date_sync = 
				for val in result:
					if not val:
						continue
					val["doctype"] = dt.document_type
					val = frappe.get_doc(val)
					print(val)
					#print(val)
					if frappe.db.exists(dt.document_type,val.name):
						print("exists %s" % val.name)
						val.ignore_permissions = True
						val.ignore_mandatory = True
						val.save()
					else:
						print("new %s" % val.name)
						val.ignore_if_duplicate = True
						val.ignore_links = True
						val.ignore_permissions = True
						val.ignore_mandatory = True
						val.insert()
				
