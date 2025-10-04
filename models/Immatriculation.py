# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ImmatriculationFiscale(models.Model):
    _name = 'immatriculation.fiscale'
    _description = 'Immatriculation Fiscale'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Ajout du tracking
    _order = 'create_date desc'

    # =========================
    # Séquence et Identification
    # =========================
    name = fields.Char("N° de Dossier fiscal", copy=False, readonly=True, default=lambda self: _('New'))
    nif = fields.Char("N° d'Immatriculation Fiscale", tracking=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('immatriculation.fiscale') or _('New')
        return super(ImmatriculationFiscale, self).create(vals)

    # =========================
    # Type de contribuable avec validation améliorée
    # =========================
    type_contribuable = fields.Selection([
        ('personne_physique', 'Personne physique'),
        ('personne_morale', 'Personne morale'),
        ('succursale', 'Succursale'),
    ], string="Type de contribuable", required=True, tracking=True, group_expand='_read_group_type_contribuable')
    
    @api.model
    def _read_group_type_contribuable(self, values, domain, order):
        return self.env['immatriculation.fiscale']._fields['type_contribuable']._description_selection(self.env)

    # =========================
    # État du dossier
    # =========================
    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('soumis', 'Soumis'),
        ('en_cours', 'En cours de traitement'),
        ('approuve', 'Approuvé'),
        ('rejete', 'Rejeté'),
    ], string="État", default='brouillon', tracking=True, required=True)

    # =========================
    # Dispositions générales
    # =========================
    nom_commercial = fields.Char("Nom commercial", tracking=True)
    adresse_ets = fields.Text("Adresse ETS / Siège social")  # Changé en Text pour adresses
    tel_fixe = fields.Char("Tél fixe")
    bp = fields.Char("Boîte Postale")
    tel = fields.Char("Téléphone", required=True)  # Toujours requis
    mail_general = fields.Char("Email")
    nombre_salaries = fields.Integer("Nombre de salariés", default=0)
    date_immatriculation = fields.Date("Date d'immatriculation")
    centre_impot_id = fields.Many2one('centre.impot', string="Centre d'impôt")
    regime_fiscale_id = fields.Many2one('regime.fiscale', string="Régime fiscal")
    

    # =========================
    # Champs Informations Personnelles
    # =========================
    nom_prenom = fields.Char("Nom & Prénom")
    sexe = fields.Selection([
        ('masculin', 'Masculin'),
        ('feminin', 'Féminin'),
    ], string="Sexe")
    cin_carte_sejour = fields.Char("N° CIN ou Carte de séjour", tracking=True)
    nationalite = fields.Many2one('res.country', string="Nationalité")  # Amélioration
    date_naissance = fields.Date("Date de naissance")  # Séparé
    lieu_naissance = fields.Char("Lieu de naissance")  # Séparé
    domicile_personnel = fields.Text("Domicile personnel")

    # =========================
    # Champs spécifiques Personne Morale/Succursale
    # =========================
    denomination_sociale = fields.Char("Dénomination sociale", tracking=True)
    duree_societe = fields.Char("Durée de la société")
    forme_juridique = fields.Selection([
        ('sarl', 'SARL'),
        ('sa', 'SA'),
        ('suarl', 'SUARL'),
        ('snc', 'SNC'),
        ('scs', 'SCS'),
        ('sca', 'SCA'),
    ], string="Forme juridique")
    capital_social = fields.Float("Capital social", digits=(12, 0))  # Format monétaire
    nombre_associes = fields.Integer("Nombre d'associés")
    commissaire_comptes = fields.Char("Commissaire aux comptes")
    activite_raison_sociale = fields.Char("Activités sous la raison sociale")

    # =========================
    # Champs spécifiques Succursale/Personne Morale
    # =========================
    societe_etrangere_proprietaire = fields.Char("Société étrangère propriétaire")
    siege_social_etranger = fields.Char("Siège social société étrangère")
    forme_juridique_etrangere = fields.Char("Forme juridique société étrangère")
    nationalite_societe_etrangere = fields.Many2one('res.country', string="Nationalité société étrangère")
    
    # =========================
    # Relations améliorées
    # =========================
    activite_ids = fields.Many2many(
        'immatriculation.activite', 
        string="Activités exercées"
        # domain="[('type_activite', 'in', [type_contribuable, 'tous'])]"
    )
    
    mandataire_id = fields.Many2one(
        'immatriculation.mandataire', 
        string="Mandataire",
        context={'active_test': False}
    )

    contact_id = fields.Many2one(
        'res.partner', 
        string="Contact", 
        domain="[('is_company','=',False)]",
        context={'default_type': 'contact'}
    )

    # =========================
    # Salariés avec gestion améliorée
    # =========================
    salarier_ids = fields.One2many(
        'immatriculation.salarier', 
        'dos_id', 
        string="Salariés",
        context={'active_test': False}
    )

    # =========================
    # Signature et validation
    # =========================
    signature_gerant = fields.Binary("Signature du gérant / mandataire")
    date_signature = fields.Datetime("Date de signature", readonly=True)
    declaration_honneur = fields.Boolean("Déclaration sur l'honneur")
    user_id = fields.Many2one('res.users', string="Responsable", default=lambda self: self.env.user)

    # =========================
    # Pièces à joindre avec statut
    # =========================
    copie_cin_passport = fields.Binary("Copie CIN / Passeport (gérant et salariés)")
    pouvoir_mandataire = fields.Binary("Pouvoir du mandataire si nécessaire")
    agrement_activite = fields.Binary("Agrément à l'activité si nécessaire")
    contrat_bail = fields.Binary("Contrat de bail")
    lettre_engagement = fields.Binary("Lettre d'engagement")
    
    # Statut des pièces
    piece_cin_statut = fields.Selection([
        ('manquant', 'Manquant'),
        ('fourni', 'Fourni'),
        ('verifie', 'Vérifié'),
    ], string="Statut CIN", default='manquant')
    
    # =========================
    # Pièces spécifiques Personne Morale/Succursale
    # =========================
    attestations_bancaires = fields.Binary("2 attestations bancaires (copie et original)")
    statuts_societe = fields.Binary("Statuts de la société")
    
    # =========================
    # Pièces spécifiques Succursale
    # =========================
    statuts_societe_etrangere = fields.Binary("Copie certifiée conforme des statuts de la société étrangère")
    traduction_statuts_etranger = fields.Binary("Traduction des statuts étrangers")
    rcs_societe_etrangere = fields.Binary("Registre du commerce et des sociétés de la société étrangère")
    traduction_rcs_etranger = fields.Binary("Traduction du RCS étranger")
    decision_creation_succursale = fields.Binary("Décision de création de la succursale")

    # =========================
    # VALIDATIONS MÉTIER ENTERPRISE
    # =========================
    
    @api.constrains('type_contribuable', 'denomination_sociale', 'capital_social', 'cin_carte_sejour', 
                   'nom_prenom', 'societe_etrangere_proprietaire')
    def _check_required_business_rules(self):
        """Validation métier côté serveur"""
        for record in self:
            errors = []
            
            # Règles métier personne morale
            if record.type_contribuable == 'personne_morale':
                if not record.denomination_sociale:
                    errors.append("La dénomination sociale est obligatoire pour une personne morale")
                if not record.capital_social:
                    errors.append("Le capital social est obligatoire pour une personne morale")
                if not record.forme_juridique:
                    errors.append("La forme juridique est obligatoire pour une personne morale")
            
            # Règles métier personne physique
            elif record.type_contribuable == 'personne_physique':
                if not record.nom_prenom:
                    errors.append("Le nom et prénom sont obligatoires pour une personne physique")
                if not record.cin_carte_sejour:
                    errors.append("Le CIN ou carte de séjour est obligatoire pour une personne physique")
                if not record.date_naissance:
                    errors.append("La date de naissance est obligatoire pour une personne physique")
            
            # Règles métier succursale
            elif record.type_contribuable == 'succursale':
                if not record.denomination_sociale:
                    errors.append("La dénomination sociale est obligatoire pour une succursale")
                if not record.societe_etrangere_proprietaire:
                    errors.append("La société étrangère propriétaire est obligatoire pour une succursale")
                if not record.statuts_societe_etrangere:
                    errors.append("Les statuts de la société étrangère sont obligatoires pour une succursale")
            
            # Règles générales
            if not record.tel:
                errors.append("Le téléphone est obligatoire")
            if not record.adresse_ets:
                errors.append("L'adresse de l'établissement est obligatoire")
            
            if errors:
                raise ValidationError("\n".join(errors))

    @api.constrains('capital_social')
    def _check_capital_social(self):
        """Validation capital social"""
        for record in self:
            if record.capital_social and record.capital_social < 0:
                raise ValidationError("Le capital social ne peut pas être négatif")

    @api.constrains('mail_general')
    def _check_email_format(self):
        """Validation format email"""
        for record in self:
            if record.mail_general:
                if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', record.mail_general):
                    raise ValidationError("Format d'email invalide")

    @api.constrains('nombre_salaries')
    def _check_nombre_salaries(self):
        """Validation nombre salariés"""
        for record in self:
            if record.nombre_salaries < 0:
                raise ValidationError("Le nombre de salariés ne peut pas être négatif")

    # =========================
    # MÉTHODES DE WORKFLOW
    # =========================
    
    def action_soumettre(self):
        """Soumettre le dossier pour traitement"""
        self.write({'state': 'soumis'})
        # Log d'activité automatique via mail.thread
        self.message_post(body="Dossier soumis pour traitement")
        return True

    def action_approuver(self):
        """Approuver le dossier"""
        if not self.nif:
            # Génération automatique du NIF
            self.nif = self.env['ir.sequence'].next_by_code('nif.sequence') or f"NIF-{self.name}"
        self.write({'state': 'approuve'})
        self.message_post(body="Dossier approuvé - NIF attribué: %s" % self.nif)
        return True

    def action_rejeter(self):
        """Rejeter le dossier"""
        self.write({'state': 'rejete'})
        self.message_post(body="Dossier rejeté")
        return True

    def action_remettre_brouillon(self):
        """Remettre en brouillon"""
        self.write({'state': 'brouillon'})
        self.message_post(body="Dossier remis en brouillon")
        return True

    # =========================
    # MÉTHODES UTILITAIRES
    # =========================
    
    def name_get(self):
        """Affichage personnalisé du nom"""
        result = []
        for record in self:
            name = f"{record.name} - {record.denomination_sociale or record.nom_prenom or 'Sans nom'}"
            result.append((record.id, name))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """Recherche améliorée"""
        if args is None:
            args = []
        domain = args + ['|', '|', 
                        ('name', operator, name),
                        ('denomination_sociale', operator, name),
                        ('nom_prenom', operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)



class ImmatriculationMandataire(models.Model):
    _name = 'immatriculation.mandataire'
    _description = 'immatriculation.mandataire'  
    
    dossier_id = fields.One2many('immatriculation.fiscale','mandataire_id', string="Dossiers fiscaux")
    nom_prenom_mandataire = fields.Char("Nom & Prénom / Dénomination sociale")
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