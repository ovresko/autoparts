# -*- coding: utf-8 -*-
# Copyright (c) 2018, Ovresko Solutions Algerie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class Generationvehicule(Document):
	def autoname(self):
		if self.modele_vehicule:
                        marque = frappe.get_doc('Modele de vehicule',self.modele_vehicule)
                        code = marque.code_interne
                        self.code_interne = make_autoname(code + '.##')
		if not self.code_interne:
			self.code_interne = self.generation
		self.name = self.code_interne
