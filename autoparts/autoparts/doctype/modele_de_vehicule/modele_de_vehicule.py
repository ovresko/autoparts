# -*- coding: utf-8 -*-
# Copyright (c) 2019, Ovresko Solutions Algerie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class Modeledevehicule(Document):
	def autoname(self):
		marque = frappe.get_doc('Marque vehicule',self.marque_vehicule)
		code = marque.code_interne
		self.code_interne = make_autoname(code + '.##')
	def validate(self):
		if not self.code_interne:
			marque = frappe.get_doc('Marque vehicule',self.marque_vehicule)
			code = marque.code_interne
			self.code_interne = make_autoname(code + '.##')
