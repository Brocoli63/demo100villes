"""
# =====================================================
# Fichier: graphiques
# Créé: 2026-03-26 09:53
# Auteur: sylvain.branconnier (Montréal, QC)
# Projet: demo_graph1
# Version: 1.0 - PySide6 Native Apps

La classe Graphiques implémente les graphiques associés aux données (Dataframe).
- Construit l’interface graphique des graphiques (un histogramme + un camembert).
- Met à jour ces graphiques à partir d’un DataFrame déjà préparé (via StatVilles).

# =====================================================
"""

from PySide6.QtCharts import (QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis,
                              QValueAxis, QPieSeries)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout

from services.stats_villes import StatVilles  # ← Service MVC !

class Graphiques(QWidget):
    view_pie: QChartView
    chart_pie: QChart
    series_pie: QPieSeries
    view_bar: QChartView
    chart_bar: QChart

    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = None  # stocke le DataFrame courant provenant du modèle (LecteurVilles).
        self.setup_ui()

    def setup_ui(self):
        """
        Définition de l'interface de l'onglet graphique
        """
        layout = QHBoxLayout(self)

        # Histogramme
        self.chart_bar = QChart()
        self.chart_bar.setTitle("Top Pays : Nb Villes + Pop Totale")
        self.view_bar = QChartView(self.chart_bar)
        layout.addWidget(self.view_bar, 1)

        # Camembert
        self.series_pie = QPieSeries()
        self.chart_pie = QChart()
        self.chart_pie.addSeries(self.series_pie)
        self.chart_pie.setTitle("Top 5 Villes")
        self.view_pie = QChartView(self.chart_pie)
        layout.addWidget(self.view_pie, 1)

    def set_model(self, modele):
        """
        Application du modèle de donnée (LecteurVilles) provenant de myMainWindow.
        """
        self.df = modele.df

    def update_graphs(self):
        """
        Création et paramétrage des graphiques.
        """
        if self.df is None:
            return

        pays, nb_villes, pop_totale = StatVilles.pays_data_for_bar(self.df)
        villes, pops = StatVilles.top_5_villes_data(self.df)

        # Histogramme
        if pays:
            self.chart_bar.removeAllSeries()

            set1 = QBarSet("Nb Villes")
            set2 = QBarSet("Pop (M)")
            set1.append(nb_villes)
            set2.append([p / 1_000_000 for p in pop_totale])

            series = QBarSeries()
            series.append(set1)
            series.append(set2)
            self.chart_bar.addSeries(series)

            axis_x = QBarCategoryAxis()
            axis_x.append(pays)
            self.chart_bar.addAxis(axis_x, Qt.AlignBottom)
            series.attachAxis(axis_x)

            axis_y = QValueAxis()
            axis_y.setLabelFormat("%i")
            self.chart_bar.addAxis(axis_y, Qt.AlignLeft)
            series.attachAxis(axis_y)

            self.chart_bar.legend().setVisible(True)
            self.chart_bar.legend().setAlignment(Qt.AlignBottom)

        # Camembert
        self.series_pie.clear()
        if villes:
            for ville, pop in zip(villes, pops):
                self.series_pie.append(ville, pop)

