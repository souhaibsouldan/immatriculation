# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ImmatriculationMandataire(models.Model):
    _name = 'immatriculation.mandataire'
    _description = 'immatriculation.mandataire'  
    
    dos_id = fields.Many2one('immatriculation.fiscale',string='Immatriculation', ondelete='cascade', required=True)
    name = fields.Char("Nom & Prénom")
    type_mandataire = fields.Selection([
        ('mandataire', 'MANDATAIRE'),
        ('commissaire', 'COMMISSAIRE AUX COMPTES'),
    ], string="Type de mandataire", required=True)
    adresse_mandataire = fields.Char("Adresse / Siège social")
    tel_mandataire = fields.Char("Téléphone")
    fax_mandataire = fields.Char("Fax")
    mail_mandataire = fields.Char("Mail")
    cin_rcs_mandataire = fields.Char("N° CIN ou RCS")
    identification_representant_legal = fields.Text("Identification spécifique du représentant légal")