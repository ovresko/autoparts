# -*- coding: utf-8 -*-
# Copyright (c) 2020, Ovresko Solutions Algerie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from autoparts.autoparts.doctype.frappeclient import FrappeClient


class SyncPOS(Document):
	pass

def start_sync():
	sp = frappe.get_single('Sync POS')
	user = sp.user
	pwd = sp.password
	url = sp.server
	do_sync = sp.sync
	items = sp.sync_pos_item
	if(user and url and pwd and do_sync and items):
		conn = FrappeClient(url, user, pwd)
		for dt in items:
			if not dt.sync or not dt.document_type:
				continue
			result = []
			_last = frappe.get_all(dt.document_type,fields=["name","modified"],order_by='modified asc',limit=1)
			if _last:
				li = _last[0]
				result = conn.get_list(dt.document_type, fields = ['*'], filters = {'modified':(">", li.modified)})
			elif dt.date_sync:
				result = conn.get_list(dt.document_type, fields = ['*'], filters = {'modified':(">", dt.date_sync)})
			if result:
				#dt.date_sync = 
				for val in result:
					if frappe.db.exists(dt.document_type,val.name):
						val.ignore_permissions = True
						val.ignore_mandatory = True
						val.save()
					else:
						val.ignore_permissions = True
						val.ignore_mandatory = True
						val.insert()
				
