"""
===========================================================================
 Fichier: lecteur_villes.py (MVC --> model)
 Créé: 2026-03-25 14:58
 Auteur: sylvain.branconnier (Alma, QC)
 Projet: demo_graph1
 Version: 1.0 - PySide6 Native Apps / Pandas / QtChart

La classe LecteurVilles a pour objectif d'implémenter le modèle associé aux données
 d'un tableaux de villes.

Elle implémente:
    1. Instanciation d'un objet de type "Dataframe"
    2. Chargement du CSV avec Pandas
    3. Nettoyage et validation du CSV
    4. Application du modèle associé au CSV pour le chargement dans le QTableView
============================================================================
"""
import pandas as pd
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

class LecteurVilles(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.df = None
        self.colonnes = ["Rang", "Ville", "Pays", "Population"]

    def charger_csv(self, fichier_csv):
        try:
            self.df = pd.read_csv(fichier_csv, sep=';', encoding='latin-1')
            obligatoires = set(self.colonnes)
            if not obligatoires.issubset(self.df.columns):
                print(f"Colonnes manquantes: {obligatoires - set(self.df.columns)}")
                return False

            self.df = self.df[self.colonnes]  # Correction: self.colonnes
            self.df['Ville'] = self.df['Ville'].astype(str).str.strip()
            self.df['Pays'] = self.df['Pays'].astype(str).str.strip()
            self.df = self.df.dropna()
            self.df = self.df.astype({'Rang': 'int32', 'Population': 'int32'})
            self.layoutChanged.emit()  # Notifie la vue
            print(f"✓ {len(self.df)} villes valides")
            return True
        except Exception as e:
            print(f"Erreur: {e}")
            return False

    def rowCount(self, parent=QModelIndex()):  # Standard Qt
        return len(self.df) if self.df is not None else 0

    def columnCount(self, parent=QModelIndex()):
        return len(self.colonnes)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid() or self.df is None:
            return None
        row, col = index.row(), index.column()
        value = self.df.iloc[row, col]
        if role == Qt.DisplayRole:
            if col == 3:
                return f"{value:,}"
            return str(value)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.colonnes[section]
        return None
