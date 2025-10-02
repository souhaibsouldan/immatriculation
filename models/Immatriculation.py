# -*- coding: utf-8 -*-

from odoo import models, fields, api , _


class immatriculation(models.Model):
    _name = 'immatriculation.fiscale'
    _description = 'immatriculation.fiscale'


    # =========================
    # Numero d'immatriculation Fiscale
    # =========================

    nif = fields.Char("N° d'immatriculation fiscale")

    # =========================
    # Dispositions générales
    # =========================
    nom_commercial = fields.Char("Nom commercial")
    adresse_ets = fields.Char("Adresse ETS / Siège social")
    tel_fixe = fields.Char("Tel fixe")
    bp = fields.Char("Boîte Postale")
    tel = fields.Char("Téléphone")
    mail_general = fields.Char("Email")



    nombre_salaries = fields.Integer("Nombre de salariés")
    cin_carte_sejour = fields.Char("N° CIN ou Carte de séjour")
    nationalite = fields.Char("Nationalité")
    date_lieu_naissance = fields.Char("Date et lieu de naissance")
    domicile_personnel = fields.Char("Domicile personnel")

    # =========================
    # Identification du mandataire une autre classe 
    # =========================

    nom_prenom_mandataire = fields.Char("Nom & Prénom / Dénomination sociale")
    adresse_mandataire = fields.Char("Adresse / Siège social")
    tel_mandataire = fields.Char("Téléphone")
    fax_mandataire = fields.Char("Fax")
    mail_mandataire = fields.Char("Mail")
    cin_rcs_mandataire = fields.Char("N° CIN ou RCS")

    # =========================
    # Déclaration relative à l’activité
    # =========================
    activite_principale = fields.Char("Activité principale")
    activite_secondaire = fields.Char("Activité secondaire")

    # =========================
    # Déclaration des salariés
    # =========================
    nom_prenom_salarie = fields.Char("Nom & Prénom")
    salaire_brut = fields.Float("Salaire brut mensuel")
    date_embauche = fields.Date("Date d’embauche")
    emploi_occupe = fields.Char("Emploi occupé")
    matricule_cnss = fields.Char("Matricule CNSS")

    # =========================
    # Signature
    # =========================
    signature_gerant = fields.Binary("Signature du gérant / mandataire")
    declaration_honneur = fields.Boolean("Déclaration sur l’honneur")

    # =========================
    # Pièces à joindre (communes)
    # =========================
    copie_cin_passport = fields.Binary("Copie CIN / Passeport (gérant et salariés)")
    pouvoir_mandataire = fields.Binary("Pouvoir du mandataire si nécessaire")
    agrement_activite = fields.Binary("Agrément à l’activité si nécessaire")
    contrat_bail = fields.Binary("Contrat de bail")
    lettre_engagement = fields.Binary("Lettre d’engagement")

