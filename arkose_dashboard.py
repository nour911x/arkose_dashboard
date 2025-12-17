#Import des bibliothèques
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration de la page streamlit
st.set_page_config(
    page_title="Arkose Montreuil - Dashboard Performance",
    page_icon="🧗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A5F;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True) #unsafe_allow_html=True permet d’injecter du HTML/CSS dans Streamlit."C:\Users\ThinkPad\arkose_dashboard.py"

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\ThinkPad\Downloads\ARKOSE donnees_2025_graph.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Semaine'] = df['Date'].dt.isocalendar().week
    df['Mois_num'] = df['Date'].dt.month

    # Mapping des jours en français
    jour_ordre = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    df['Jour'] = pd.Categorical(df['Jour'], categories=jour_ordre, ordered=True)

    # Mapping des mois
    mois_ordre = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    mois_fr = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
               'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    df['Mois_fr'] = df['Mois'].map(dict(zip(mois_ordre, mois_fr)))
    df['Mois_fr'] = pd.Categorical(df['Mois_fr'], categories=mois_fr, ordered=True)

    return df

df = load_data()

# Header
st.markdown('<p class="main-header">🧗 Arkose Montreuil</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Dashboard de Suivi de Performance 2025</p>', unsafe_allow_html=True)

# Sidebar - Filtres
st.sidebar.header("🎯 Filtres")

# Filtre par mois
mois_list = df['Mois_fr'].unique().tolist()
selected_mois = st.sidebar.multiselect(
    "Sélectionner les mois",
    options=mois_list,
    default=mois_list
)

# Filtre par jour de la semaine
jours_list = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
selected_jours = st.sidebar.multiselect(
    "Sélectionner les jours",
    options=jours_list,
    default=jours_list
)

# Application des filtres
df_filtered = df[df['Mois_fr'].isin(selected_mois) & df['Jour'].isin(selected_jours)]

# KPIs principaux
st.markdown("### 📊 Indicateurs Clés de Performance")
col1, col2, col3, col4, col5 = st.columns(5)

total_visites = df_filtered['Total_jour'].sum()
moyenne_jour = df_filtered['Total_jour'].mean()
total_nouveaux = df_filtered['Entrée'].sum()
total_passages = df_filtered['Passage'].sum()
taux_fidelite = (total_passages / total_visites * 100) if total_visites > 0 else 0

with col1:
    st.metric("Total Visites", f"{total_visites:,.0f}", help="Nombre total de visites sur la période")
with col2:
    st.metric("Moyenne/Jour", f"{moyenne_jour:.0f}", help="Moyenne quotidienne de visiteurs")
with col3:
    st.metric("Nouveaux Clients", f"{total_nouveaux:,.0f}", help="Total des nouvelles entrées")
with col4:
    st.metric("Abonnés (Passages)", f"{total_passages:,.0f}", help="Entrées avec abonnement")
with col5:
    st.metric("Taux Fidélité", f"{taux_fidelite:.1f}%", help="% de visites avec abonnement")

st.markdown("---")

# Graphiques - Ligne 1
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📈 Évolution de la Fréquentation")

    # Agrégation hebdomadaire pour lisibilité
    df_weekly = df_filtered.groupby('Semaine').agg({
        'Total_jour': 'sum',
        'Passage': 'sum',
        'Plat': 'sum',
        'Entrée': 'sum',
        'Date': 'first'
    }).reset_index()

    fig_evolution = go.Figure()
    fig_evolution.add_trace(go.Scatter(
        x=df_weekly['Date'], y=df_weekly['Total_jour'],
        mode='lines+markers', name='Total',
        line=dict(color='#667eea', width=2),
        fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    fig_evolution.update_layout(
        xaxis_title="Date",
        yaxis_title="Visites hebdomadaires",
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig_evolution, use_container_width=True)

with col_right:
    st.markdown("### 🥧 Répartition des Types d'Entrées")

    repartition = pd.DataFrame({
        'Type': ['Abonnés (Passage)', 'Restauration (Plat)', 'Nouveaux (Entrée)'],
        'Valeur': [df_filtered['Passage'].sum(), df_filtered['Plat'].sum(), df_filtered['Entrée'].sum()]
    })

    fig_pie = px.pie(
        repartition, values='Valeur', names='Type',
        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb'],
        hole=0.4
    )
    fig_pie.update_traces(textposition='outside', textinfo='percent+label')
    fig_pie.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

# Graphiques - Ligne 2
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.markdown("### 📅 Performance par Jour de la Semaine")

    df_jour = df_filtered.groupby('Jour', observed=True).agg({
        'Total_jour': 'mean',
        'Entrée': 'mean'
    }).reset_index()

    fig_jour = go.Figure()
    fig_jour.add_trace(go.Bar(
        x=df_jour['Jour'], y=df_jour['Total_jour'],
        name='Moyenne visites',
        marker_color='#667eea'
    ))
    fig_jour.add_trace(go.Scatter(
        x=df_jour['Jour'], y=df_jour['Entrée'],
        name='Nouveaux clients (moy)',
        mode='lines+markers',
        yaxis='y2',
        line=dict(color='#f093fb', width=3)
    ))
    fig_jour.update_layout(
        yaxis=dict(title='Visites moyennes', side='left'),
        yaxis2=dict(title='Nouveaux clients', side='right', overlaying='y'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        height=400
    )
    st.plotly_chart(fig_jour, use_container_width=True)

with col_right2:
    st.markdown("### 📆 Performance Mensuelle")

    df_mois = df_filtered.groupby('Mois_fr', observed=True).agg({
        'Total_jour': 'sum',
        'Entrée': 'sum',
        'Passage': 'sum'
    }).reset_index()

    fig_mois = go.Figure()
    fig_mois.add_trace(go.Bar(
        x=df_mois['Mois_fr'], y=df_mois['Total_jour'],
        name='Total visites',
        marker_color='#667eea'
    ))
    fig_mois.add_trace(go.Scatter(
        x=df_mois['Mois_fr'], y=df_mois['Entrée'],
        name='Nouveaux clients',
        mode='lines+markers',
        yaxis='y2',
        line=dict(color='#f093fb', width=3)
    ))
    fig_mois.update_layout(
        yaxis=dict(title='Total visites'),
        yaxis2=dict(title='Nouveaux clients', side='right', overlaying='y'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        height=400
    )
    st.plotly_chart(fig_mois, use_container_width=True)

st.markdown("---")

# Heatmap des visites
st.markdown("### 🗓️ Heatmap de Fréquentation (Jour x Mois)")

pivot_heatmap = df_filtered.pivot_table(
    values='Total_jour',
    index='Jour',
    columns='Mois_fr',
    aggfunc='mean'
)

fig_heatmap = px.imshow(
    pivot_heatmap,
    color_continuous_scale='RdYlGn',
    aspect='auto',
    labels=dict(x="Mois", y="Jour", color="Visites moy.")
)
fig_heatmap.update_layout(height=350)
st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")

# Insights Marketing
st.markdown("### 💡 Insights Marketing & Recommandations")

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown("#### 📊 Analyse des Tendances")

    # Meilleur jour
    best_day = df_filtered.groupby('Jour', observed=True)['Total_jour'].mean().idxmax()
    best_day_val = df_filtered.groupby('Jour', observed=True)['Total_jour'].mean().max()

    # Pire jour
    worst_day = df_filtered.groupby('Jour', observed=True)['Total_jour'].mean().idxmin()
    worst_day_val = df_filtered.groupby('Jour', observed=True)['Total_jour'].mean().min()

    # Meilleur mois pour nouveaux clients
    best_month_new = df_filtered.groupby('Mois_fr', observed=True)['Entrée'].sum().idxmax()

    st.success(f"**Jour le plus fréquenté :** {best_day} ({best_day_val:.0f} visites/jour en moyenne)")
    st.warning(f"**Jour le moins fréquenté :** {worst_day} ({worst_day_val:.0f} visites/jour en moyenne)")
    st.info(f"**Meilleur mois pour l'acquisition :** {best_month_new}")

with col_insight2:
    st.markdown("#### 🎯 Recommandations")

    # Calcul du ratio week-end vs semaine
    df_weekend = df_filtered[df_filtered['Jour'].isin(['Samedi', 'Dimanche'])]
    df_semaine = df_filtered[~df_filtered['Jour'].isin(['Samedi', 'Dimanche'])]

    ratio_we = df_weekend['Total_jour'].mean() / df_semaine['Total_jour'].mean() if df_semaine['Total_jour'].mean() > 0 else 0

    recommandations = []

    if ratio_we < 1:
        recommandations.append("📌 **Booster le week-end** : Organiser des événements (compétitions, initiations)")
    else:
        recommandations.append("✅ **Week-end performant** : Maintenir les animations actuelles")

    # Taux de nouveaux clients
    taux_nouveaux = (df_filtered['Entrée'].sum() / df_filtered['Total_jour'].sum() * 100)
    if taux_nouveaux < 10:
        recommandations.append("📌 **Acquisition** : Renforcer les offres découverte et partenariats locaux")

    recommandations.append("📌 **Fidélisation** : Programme de parrainage pour convertir les nouveaux en abonnés")
    recommandations.append("📌 **Zone Kids** : Communiquer sur les mercredis/week-ends pour les familles")

    for rec in recommandations:
        st.markdown(rec)

st.markdown("---")

# Tableau détaillé
with st.expander("📋 Voir les données détaillées"):
    st.dataframe(
        df_filtered[['Date', 'Jour', 'Mois_fr', 'Passage', 'Plat', 'Entrée', 'Total_jour']].sort_values('Date', ascending=False),
        use_container_width=True,
        height=400
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🧗 <strong>Arkose Montreuil</strong> - 700 m² de surface grimpable | 150 blocs | 6 niveaux de difficulté</p>
    <p>Dashboard créé pour optimiser la stratégie marketing et communication</p>
</div>
""", unsafe_allow_html=True)
