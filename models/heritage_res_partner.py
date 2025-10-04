from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    dos_id = fields.Many2many(
        'immatriculation.fiscale',
        string='Immatriculations Fiscales'
    )