# -*- coding: utf-8 -*-
# Copyright (c) 2018, Ovresko Solutions Algerie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import nowdate, getdate


class Generationvehicule(Document):
    def validate(self):
        marque = frappe.get_doc('Modele de vehicule',self.modele_vehicule)
        self.nom_generation = marque.modele + ' '+self.generation
        periode = ''        
        if self.date_debut:
            year,month,day = str(self.date_debut).split('-')
            periode += month+'.'+year[-2:] +' - '
            today = nowdate()
            d = getdate(self.date_debut).year
            self.age = getdate(today).year - d

        if self.date_fin:
            y,m,d = str(self.date_fin).split('-')
            periode += m+'.'+y[-2:]
        
        #frappe.msgprint(periode)
        if periode:
            self.periode = '('+periode+')'
        else:
            self.periode = ''
    def autoname(self):
        if self.modele_vehicule:
            marque = frappe.get_doc('Modele de vehicule',self.modele_vehicule)
            code = marque.code_interne
            self.nom_generation = marque.modele + ' '+self.generation
            self.code_interne = make_autoname(code + '.##')
        if not self.code_interne:
            self.code_interne = self.generation
        #self.name = self.code_interne