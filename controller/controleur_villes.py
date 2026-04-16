"""
# =====================================================
# Fichier: controller_villes
# Créé: 2026-03-26 09:53
# Auteur: sylvain.branconnier (Montréal, QC)
# Projet: demo_graph1
# Version: 1.0 - PySide6 Native Apps

La classe ControleurVilles a un rôle de chef d'orchestre.
- Elle gère l'interaction entre l'utilisateur (View) et les données (Model)
- Bouton "Charger CSV" --> active un QFileDialog
- Onglet Statistique / Graphique --> calcule et prépare les stats à partir de la classe StatsVilles
# =====================================================
"""

from PySide6.QtWidgets import QFileDialog
from model.lecteur_villes import LecteurVilles
from services.stats_villes import StatVilles

class ControleurVilles:
    def __init__(self, model: LecteurVilles):
        self.model = model

    def selectionner_et_charger_csv(self):
        fichier = QFileDialog.getOpenFileName(
            None,
            "Sélectionne CSV villes",
            "data",
            "CSV (*.csv)"
        )[0]
        if fichier and self.model.charger_csv(fichier):
            return True
        return False

    def get_stats(self):
        return StatVilles.calculer_stats(self.model.df)

    def get_pays_bar_data(self):
        return StatVilles.pays_data_for_bar(self.model.df)

    def get_top5_data(self):
        return StatVilles.top_5_villes_data(self.model.df)
