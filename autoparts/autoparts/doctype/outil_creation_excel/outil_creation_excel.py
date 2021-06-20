# -*- coding: utf-8 -*-
# Copyright (c) 2019, Ovresko Solutions Algerie and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
#from erpnext.controllers.item_variant import make_variant_based_on_manufacturer
from erpnext.controllers.item_variant import get_variant

class OutilCreationExcel(Document):
    pass
@frappe.whitelist()
def lancer(groupe):
    if not groupe:
        frappe.msgprint(_("Groupe est invalide"))
        return None
#   try:
    refs = []
    items = frappe.db.get_all("Article Excel",filters={'groupe_article':groupe },fields=['designation_commerciale','oem_simplifie','name','version','generation','modele','groupe_article','oem', 'moog','bosch','mahle','mahle_2','meyle','era','bga','gsp','corteco','magneti_marelli','mann_filtre','clean_filters','hengst_filter','hengst_filter_2','champion'])
    oems = set(i.oem_simplifie for i in items)
    #frappe.msgprint(len(oems) + " oem")
    doc_groupe = frappe.get_doc('Item Group',groupe)
    result = ''
    frappe.msgprint("Operation encours, vous devez laisser la page ouverte")
    for oem in oems:
        #self.titre = "En cours..."
        if not oem:
            continue
        #tpl = tuple([e.name for e in al])
        all_models = frappe.db.get_all('OEM',filters={'oem_simplifie':oem},fields=['name'])
        if all_models and len(all_models) > 0:
            continue
        model = frappe.new_doc('Item')
        #result += doc_groupe.name
        model.has_variants = 1
        model.variant_based_on = 'Manufacturer'
        model.item_code = 'code'
        model.generer_code_interne = 1
        model.item_name =  doc_groupe.name
        model.item_group = doc_groupe.name
        model.is_purchase_item = 1
        model.is_sales_item = 1
        #model.designation_commerciale = oem.designation_commerciale
        model.adresse_magasin = "NA"
        model.nom_generique_long = model.item_name
        #myversions = [v for v in items if v.oem == oem]
        myversions = list(filter(lambda x: x.oem_simplifie == oem,items))
        #frappe.msgprint((oem))
        if myversions:
            model.designation_commerciale = myversions[0].designation_commerciale
        if oem:
            row = model.append('oem')
            row.oem_simplifie=oem
            full_oem = [r for r in items if r.oem_simplifie == oem]
            if full_oem:
                row.oem = full_oem[0].oem
        for version in myversions:
            #frappe.msgprint(str(version.version))
            #ver = frappe.get_doc('Version vehicule',version.version)
            #frappe.msgprint(str(ver))
            if version.version:
                model.append('versions',{
                            'version_vehicule':version.version
                            })
            elif version.generation:
                model.append('generation_vehicule_supporte',{
                'generation_vehicule':version.generation
                })
            elif version.modele:
                model.append('modele_vehicule_supporte',{
                'modele_vehicule':version.modele
                })
        model.save()
        #frappe.msgprint(model.name)
        #frappe.db.commit()
        items_oem = frappe.db.get_all('Article Excel',filters={'oem_simplifie':oem},fields=['oem_simplifie','name','bga','version','generation','modele','groupe_article','oem', 'moog','bosch','mahle','meyle','era','gsp','corteco','magneti_marelli','mann_filtre','clean_filters','hengst_filter','hengst_filter_2','mahle_2','champion'])
        #frappe.msgprint(str(len(items_oem)))
        result = ''
        for o in items_oem:
            filters = [o.moog,o.bosch,o.mahle,o.mahle_2,o.meyle,o.era,o.gsp,o .corteco,o.bga,o.magneti_marelli,o.mann_filtre,o.clean_filters,o.hengst_filter,o.hengst_filter_2,o.champion]
            not_null_filters =list([x for x in filters if x is not None and x != ''])
            #frappe.msgprint(' '.join(not_null_filters))
            exist = []
            exist = frappe.db.get_all('Item',filters={'manufacturer_part_no':('in',not_null_filters),'has_variants':0},fields=['name'])
            #frappe.msgprint('items with ref: '+o.oem+' '+str('[%s]' % ', '.join(map(str, exist)))+' n '+str(len(exist)))
            if exist and len(exist) > 0:
                #result += str(' - '.join(exist))
                frappe.delete_doc('Article Excel', o.name)
                continue
            if o.moog:
                #exist = frappe.db.get_all('Item',filters={'manufacturer_part_no':o.moog},fields=['namr'])
                variant1 = get_variant(template=model.name,manufacturer='MOOG',manufacturer_part_no=o.moog)
                variant1.save()
                #frappe.db.commit()
            if o.bosch:
                variant2 = get_variant(template=model.name,manufacturer='BOSCH',manufacturer_part_no=o.bosch)
                variant2.save()
            if o.mahle:
                variant3 = get_variant(template=model.name,manufacturer='MAHLE',manufacturer_part_no=o.mahle)
                variant3.save()
            if o.mahle_2:
                variant3 = get_variant(template=model.name,manufacturer='MAHLE',manufacturer_part_no=o.mahle_2)
                variant3.save()
            if o.meyle:
                variant4 = get_variant(template=model.name,manufacturer='MEYLE',manufacturer_part_no=o.meyle)
                variant4.save()
            if o.era:
                variant5 = get_variant(template=model.name,manufacturer='ERA',manufacturer_part_no=o.era)
                variant5.save()
            if o.gsp:
                variant6 = get_variant(template=model.name,manufacturer='GSP',manufacturer_part_no=o.gsp)
                variant6.save()
            if o.corteco:
                variant7 = get_variant(template=model.name,manufacturer='CORTECO',manufacturer_part_no=o.corteco)
                variant7.save()
            if o.bga:
                variant8 = get_variant(template=model.name,manufacturer='BGA',manufacturer_part_no=o.bga)
                variant8.save()
            if o.magneti_marelli:
                variant9 = get_variant(template=model.name,manufacturer='MAGNETI MARELLI',manufacturer_part_no=o.magneti_marelli)
                variant9.save()
            if o.mann_filtre:
                variant10 = get_variant(template=model.name,manufacturer='MANN FILTRE',manufacturer_part_no=o.mann_filtre)
                variant10.save()
            if o.clean_filters:
                variant11 = get_variant(template=model.name,manufacturer='CLEAN FILTERS',manufacturer_part_no=o.clean_filters)
                variant11.save()
            if o.hengst_filter:
                variant11 = get_variant(template=model.name,manufacturer='HENGST FILTER',manufacturer_part_no=o.hengst_filter)
                variant11.save()
            if o.hengst_filter_2:
                variant11 = get_variant(template=model.name,manufacturer='HENGST FILTER',manufacturer_part_no=o.hengst_filter_2)
                variant11.save()
            if o.champion:
                variant11 = get_variant(template=model.name,manufacturer='CHAMPION',manufacturer_part_no=o.champion)
                variant11.save()
            frappe.db.commit()
            frappe.delete_doc('Article Excel', o.name)
            #frappe.db.commit()
        
    frappe.msgprint("OK... operation termine")
    return "Termine "+result
#   except Exception as e:
#       return e.message
        #return "ERREUR"