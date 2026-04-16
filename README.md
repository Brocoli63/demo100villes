# Analyse de données avec Pandas et QtChart

# 1. Fonctionnalités
✅ TableView : Tableau des 100+ villes (Rang, Ville, Pays, Population)

✅ Pandas : Chargement et nettoyage CSV, groupby, stats avec Dataframe

✅ QtCharts : Histogramme groupé + Camembert interactifs

✅ MVC : Architecture MVC (sans package)

✅ Responsive : QSplitter + contraintes taille

# 2. Structure MVCs (sans packages)
### 1) main.py → Démarre Qt

### 2) main_window.py → (MVC_View: L'interface client)

→ Tout ce qui est présenté à l'utilisateur.

### 3) lecteur_villes.py → (MVC_Model: Le moule de nos données). 

→ Chargement et gestion du CSV dans le Dataframe de Pandas

### 4) controleur_villes.py → (MVC_Controler: Gère les intérations de l'utilisateur et les données)

→ 1) S'occupe de la sélection du fichier CSV

→ 2)l'obtention des statistiques.

### 5) graphiques_charts.py → (MVC_View: L'interface client)

→  Présentation de l'onglet graphique avec QtCharts


### 6) stats_villes.py → (MVCs_Service: Logique de métier). 

→ Effectue et prépare les calculs.

# 3. Installation & Lancement
## 3.1. Environnement virtuel (recommandé)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
### .venv\Scripts\activate     # Windows
## 3.2 Dépendances
pip install pandas PySide6
## 3.3 Lancer
python main.py
# 4. Architecture MVC
![architectureMVC.png](images%2FarchitectureMVC.png)

| Fichier             | Rôle           | Contenu                          |
|---------------------|----------------|----------------------------------|
| main.py             | Entrée         | QApplication + MainWindow        |
| main_window.py      | Vue            | UI + charger() orchestre         |
| lecteur_villes.py   | Model          | CSV → DataFrame + groupby()      |
| conroleur_villes.py | Controleur     | Gère les interactions UI         |
| graphiques.py       | Vue spécialisé | QBarSeries + QPieSeries          |
| stats_villes.py     | Service        | Calcul + aggrégation avec Pandas |

# 5. Flux de données dans notre application
1. Clic "Charger CSV" (main_window.py)
   ↓
2. controleur_villes → QFileDialog → CSV sélectionné
   ↓
3. lecteur_villes2.charger_csv() → DataFrame nettoyé
   ↓
4. table_view.setModel(model) → Table remplie
   ↓
5. stats_villes.calculer_stats(df) → Texte stats
   ↓
6. stats_view.setPlainText(stats) → Affichage stats
   ↓
7. graphiques.set_model(model) → Graphs mis à jour

# 6. CSV requis 

| Rang | Ville       | Pays     | Population   |
|------|-------------|----------|--------------|
| 1    | Tokyo       | Japon    | 37 451 472   |
| 2    | Delhi       | Inde     | 32 900 000   |
| 3    | Shanghai    | Chine    | 29 867 000   |
| 4    | Dacca       | Bangladesh | 22 007 000 |
| 5    | São Paulo   | Brésil   | 22 000 000   |

**Format CSV** : `Rang;Ville;Pays;Population` (séparateur `;`, encoding `latin-1`)

# 7. Dépannage
| Problème         | Solution                                    |
| ---------------- | ------------------------------------------- |
| 0 villes         | Vérifier row_count() dans lecteur_villes.py |
| QBarSeries error | series.append(set1) un par un               |
| CSV échoue       | sep=';' + encoding='latin-1'                |
| PySide6 absent   | pip install PySide6                         |
