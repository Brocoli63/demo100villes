"""
# =============================================================================
# Fichier: stats_villes
# Créé: 2026-03-26 09:52
# Auteur: sylvain.branconnier (Montréal, QC)
# Projet: demo_graph1
# Version: 1.0 - PySide6 Native Apps

La classe StatVilles a pour objectif d'implémenter à partir du Dataframe:
- Les différents calculs statistiques
- Les aggrégations (regroupement) de données
# ============================================================================

"""

class StatVilles:
    @staticmethod
    def calculer_stats(df):
        """
        Calculer stats
        :param df: Dataframe
        :return:
        """
        if df is None:
            return ""
        moyenne_pop = df['Population'].mean()
        groupby_pays = df.groupby('Pays')['Population'].agg(['sum', 'count'])
        groupby_pays.columns = ['Population_totale', 'Nb_villes']
        groupby_pays = groupby_pays.sort_values('Population_totale', ascending=False).round(0)
        stats = f"** Moyenne ** : {moyenne_pop:,.0f} hab\n\n** Par Pays **\n"
        stats += groupby_pays.to_string()
        return stats

    @staticmethod
    def pays_data_for_bar(df, top_n=10):
        if df is None:
            return None, None, None
        groupby_pays = df.groupby('Pays')['Population'].agg(['sum', 'count'])
        groupby_pays.columns = ['Population_totale', 'Nb_villes']
        top = groupby_pays.nlargest(top_n, 'Population_totale')
        return top.index.tolist(), top['Nb_villes'].tolist(), top['Population_totale'].tolist()

    @staticmethod
    def top_5_villes_data(df):
        if df is None:
            return None, None
        top5 = df.nlargest(5, 'Population')[['Ville', 'Population']]
        return top5['Ville'].tolist(), top5['Population'].tolist()
