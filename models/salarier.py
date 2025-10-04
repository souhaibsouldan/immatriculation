from odoo import models, fields

class ImmatriculationSalarier(models.Model):
    _name = 'immatriculation.salarier'
    _description = 'Salariés de l\'immatriculation fiscale'

    dos_id = fields.Many2one('immatriculation.fiscale', string='Immatriculation', ondelete='cascade', required=True)
    nom_prenom_salarie = fields.Char("Nom & Prénom", required=True)
    salaire_brut = fields.Float("Salaire brut mensuel", required=True)
    date_embauche = fields.Date("Date d'embauche", required=True)
    emploi_occupe = fields.Char("Emploi occupé", required=True)
    matricule_cnss = fields.Char("Matricule CNSS", required=True)