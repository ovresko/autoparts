# -*- coding: utf-8 -*-
# Copyright (c) 2018, Ovresko Solutions Algerie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class OEM(Document):
        def validate(self):
            self.oem_simplifie = self.oem.replace(" ","")
