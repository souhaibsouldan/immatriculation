from odoo import models, fields

class CentreImpot(models.Model):
    _name = 'centre.impot'
    _description = 'Centre Impot'

    name = fields.Char(string='Nom du Centre', required=True)
    code = fields.Char(string='Code', required=True)
    adresse = fields.Char(string='Adresse')
    telephone = fields.Char(string='Téléphone')