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
					lid =  li.modified.strftime("%Y-%m-%d %H:%M:%S.%f")
					print("lid %s" % lid)
					result = conn.get_list(dt.document_type, fields = ['*'], filters = {'modified':(">", lid),'docstatus':("<", 2)})
			elif dt.date_sync:
				dtd =  dt.date_sync.strftime("%Y-%m-%d %H:%M:%S.%f")
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
					
					print("val %s " % val)
					val = frappe.get_doc(val)
					
					#print(val)
					if frappe.db.exists(dt.document_type,val.name):
						print("exists %s" % val.name)
						val.flags.ignore_if_duplicate = True
						val.flags.ignore_links = True
						val.flags.ignore_permissions = True
						val.flags.ignore_mandatory = True
						val.save(ignore_permissions=True, ignore_version=True)
					else:
						print("new %s" % val.name)
						val.flags.ignore_if_duplicate = True
						val.flags.ignore_links = True
						val.flags.ignore_permissions = True
						val.flags.ignore_mandatory = True
						val.docstatus=None
						val.__islocal = True
						val.insert(
							ignore_permissions=True,
							ignore_links=True, 
							ignore_if_duplicate=True,
							ignore_mandatory=True)
						frappe.db.commit()
				
