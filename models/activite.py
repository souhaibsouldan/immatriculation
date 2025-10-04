from odoo import models, fields

class immatriculationActivite(models.Model):
    _name = 'immatriculation.activite'
    _description = 'Activité d%immatriculation'

    dossier_ids = fields.Many2many('immatriculation.fiscale', string="Dossiers d'immatriculation")
    name = fields.Char(string='Nom', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Actif', default=True)