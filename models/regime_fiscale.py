from odoo import models, fields

class RegimeFiscale(models.Model):
    _name = 'regime.fiscale'
    _description = 'Régime Fiscale'

    name = fields.Char(string='Nom', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')