 Dashboard Arkose Montreuil

  Dashboard interactif de suivi de performance pour la salle d'escalade Arkose Montreuil.

  Contexte

  Arkose Montreuil propose un espace de grimpe de 700 m² avec 150 blocs sur 6 niveaux de difficulté. Ce dashboard a
  été créé pour analyser la fréquentation et optimiser la stratégie marketing.

  Problématique : Comment améliorer la communication et le marketing pour attirer davantage de grimpeurs tout en
  valorisant l'espace et les expériences uniques ?

  Fonctionnalités

  - KPIs clés : Total visites, moyenne journalière, nouveaux clients, taux de fidélité
  - Évolution temporelle : Graphique de fréquentation hebdomadaire
  - Répartition des entrées : Abonnés vs Nouveaux vs Restauration
  - Analyse par jour : Performance selon le jour de la semaine
  - Analyse mensuelle : Comparaison mois par mois
  - Heatmap : Visualisation croisée Jour x Mois
  - Insights automatiques : Recommandations marketing basées sur les données
  - Filtres interactifs : Par mois et jour de la semaine

  Technologies utilisées

  - Python 3
  - Streamlit - Interface web interactive
  - Pandas - Manipulation des données
  - Plotly - Visualisations interactives

  Installation

  # Cloner le repo
  git clone https://github.com/nour911x/arkose_dashboard.git
  cd arkose_dashboard

  # Installer les dépendances
  pip install -r requirements.txt

  # Lancer le dashboard
  streamlit run arkose_dashboard.py

  Structure du projet

  arkose-dashboard/
  ├── arkose_dashboard.py    # Code principal du dashboard
  ├── requirements.txt       # Dépendances Python
  ├── README.md             # Documentation
  └── data/
      └── ARKOSE_donnees_2025.csv  # Données de fréquentation

  Aperçu

  Le dashboard est accessible sur http://localhost:8501 après lancement.
