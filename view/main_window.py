"""
===========================================================================
 Fichier: main_window.py (MVC --> View)
 Créé: 2026-03-25 14:58
 Auteur: sylvain.branconnier (Alma, QC)
 Projet: demo_graph1
 Version: 1.0 - PySide6 Native Apps / Pandas / QtChart

La classe mainWindow construit l'interface principale (View) pour l'utilisateur.
Elle implémente:
    1. La fenêtre (QMainWindow)
    2. La zone centrale
    3. Les widgets
        3.1 Bouton de chargement CSV se connectant au @Slot()
            charger --> LecteurVille
        3.2 QTableView inclut dans QSplitter
        3.2
    4. Une instance lecteur (gestion du dataframe de pandas)
        de la classe LecteurVille
============================================================================
"""

from PySide6.QtWidgets import (QMainWindow, QTableView, QTextEdit, QVBoxLayout, QWidget,
                               QHBoxLayout, QPushButton, QLabel, QSplitter, QTabWidget)
from PySide6.QtCore import Qt, Slot

# Imports locaux
from model.lecteur_villes import LecteurVilles
from controller.controleur_villes import ControleurVilles
# from graphiques import Graphiques
from view.graphiques import Graphiques


class my_mainWindow(QMainWindow):
    # annotation "hint" pour enlever les warnings de PyCharm
    btn_charger: QPushButton
    lbl_status: QLabel
    tbl_view: QTableView
    stats_view: QTextEdit
    my_graphiques: Graphiques
    tbl_view: QTableView
    model: LecteurVilles
    controleur: ControleurVilles

    def __init__(self):
        super().__init__()
        self.setWindowTitle("demo_pandas MVC + QTCHARTS")
        self.resize(1200, 800)

        self.preparer_ui()
        self.initialiser_mvc()

    def preparer_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Boutons + Statut
        btn_layout = QHBoxLayout()
        self.btn_charger = QPushButton("Charger CSV")
        self.btn_charger.clicked.connect(self.charger)
        self.lbl_status = QLabel("Cliquez pour charger")
        btn_layout.addWidget(self.btn_charger)
        btn_layout.addWidget(self.lbl_status)
        btn_layout.addStretch(1)
        main_layout.addLayout(btn_layout)

        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        self.tbl_view = QTableView()
        self.tbl_view.setAlternatingRowColors(True)
        self.tbl_view.setMinimumHeight(700)
        self.tbl_view.setMaximumWidth(400)
        splitter.addWidget(self.tbl_view)

        # Onglet Stat + graphique
        tab_stat = QTabWidget()
        self.stats_view = QTextEdit()
        self.stats_view.setMaximumWidth(500)
        self.stats_view.setReadOnly(True)
        tab_stat.addTab(self.stats_view, "Statistiques")

        self.my_graphiques = Graphiques()
        tab_stat.addTab(self.my_graphiques, "Graphiques")

        splitter.addWidget(tab_stat)
        splitter.setSizes([600, 700])
        main_layout.addWidget(splitter)

    def initialiser_mvc(self):
        """Initialise Model + Controller"""
        self.model = LecteurVilles()
        self.controleur = ControleurVilles(self.model)
        self.tbl_view.setModel(self.model)

    @Slot()
    def charger(self):
        """Orchestre chargement via controller/service"""
        if self.controleur.selectionner_et_charger_csv():
            self.tbl_view.resizeColumnsToContents()
            stats = self.controleur.get_stats() # Obtenir les stats
            self.stats_view.setPlainText(stats)

            self.my_graphiques.set_model(self.model)  #
            self.my_graphiques.update_graphs()

            self.lbl_status.setText(f"✓ {self.model.rowCount()} villes + Charts")
        else:
            self.lbl_status.setText("Échec")
