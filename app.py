import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Configuration de la page
st.set_page_config(
    page_title="HR Dashboard Pro",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour les couleurs
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .employee-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .notification-badge {
        background-color: #EF4444;
        color: white;
        border-radius: 50%;
        padding: 0.2rem 0.6rem;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .stButton > button {
        width: 100%;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
    }
    .vacation-card {
        background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des données
if "employees" not in st.session_state:
    # Exemple de données initiales
    st.session_state.employees = [
        {"id": 1, "name": "Ali Benali", "role": "Développeur", "department": "IT", "salary": 25000, "join_date": "2023-01-15", "status": "Actif", "email": "ali.benali@entreprise.com", "phone": "0612345678"},
        {"id": 2, "name": "Fatima Zahra", "role": "RH Manager", "department": "RH", "salary": 35000, "join_date": "2022-05-10", "status": "Actif", "email": "fatima.zahra@entreprise.com", "phone": "0623456789"},
        {"id": 3, "name": "Karim Alami", "role": "Analyste", "department": "Finance", "salary": 28000, "join_date": "2023-08-22", "status": "Actif", "email": "karim.alami@entreprise.com", "phone": "0634567890"},
        {"id": 4, "name": "Salma Toufiq", "role": "Designer", "department": "Marketing", "salary": 22000, "join_date": "2024-01-08", "status": "Actif", "email": "salma.toufiq@entreprise.com", "phone": "0645678901"},
        {"id": 5, "name": "Youssef Khalil", "role": "Commercial", "department": "Ventes", "salary": 32000, "join_date": "2022-11-30", "status": "Actif", "email": "youssef.khalil@entreprise.com", "phone": "0656789012"},
        {"id": 6, "name": "Leila Mansouri", "role": "Support Client", "department": "Support", "salary": 18000, "join_date": "2023-03-25", "status": "En congé", "email": "leila.mansouri@entreprise.com", "phone": "0667890123"},
    ]
    st.session_state.next_id = 7

if "vacations" not in st.session_state:
    st.session_state.vacations = [
        {"id": 1, "employee_id": 1, "employee_name": "Ali Benali", "start_date": "2024-03-15", "end_date": "2024-03-22", "type": "Annuel", "status": "Approuvé", "reason": "Vacances familiales"},
        {"id": 2, "employee_id": 6, "employee_name": "Leila Mansouri", "start_date": "2024-03-10", "end_date": "2024-04-10", "type": "Maternité", "status": "Approuvé", "reason": "Congé maternité"},
        {"id": 3, "employee_id": 3, "employee_name": "Karim Alami", "start_date": "2024-04-01", "end_date": "2024-04-05", "type": "Maladie", "status": "En attente", "reason": "Consultation médicale"},
    ]
    st.session_state.next_vacation_id = 4

if "evaluations" not in st.session_state:
    st.session_state.evaluations = [
        {"id": 1, "employee_id": 1, "employee_name": "Ali Benali", "date": "2024-01-15", "score": 4.5, "comment": "Excellent travail sur le projet X", "manager": "Fatima Zahra"},
        {"id": 2, "employee_id": 2, "employee_name": "Fatima Zahra", "date": "2024-01-20", "score": 4.8, "comment": "Leadership exceptionnel", "manager": "Directeur Général"},
        {"id": 3, "employee_id": 3, "employee_name": "Karim Alami", "date": "2024-02-10", "score": 4.2, "comment": "Bonnes compétences analytiques", "manager": "Fatima Zahra"},
    ]
    st.session_state.next_evaluation_id = 4

# Titre principal avec style
st.markdown('<h1 class="main-header">👥 Tableau de Bord RH - Gestion des Employés</h1>', unsafe_allow_html=True)

# Sidebar pour la navigation
with st.sidebar:
    # Compter les notifications
    pending_vacations = len([v for v in st.session_state.vacations if v["status"] == "En attente"])
    total_notifications = pending_vacations
    
    st.markdown(f"### 🎨 Navigation")
    page = st.radio(
        "Choisir une section:",
        ["📊 Vue d'ensemble", "➕ Ajouter Employé", "👥 Liste des Employés", "📈 Statistiques", 
         "🏖️ Gestion Congés", "⭐ Évaluations", "⚙️ Paramètres"]
    )
    
    st.markdown("---")
    st.markdown("### 🏢 Départements")
    departments = ["Tous"] + list(set([emp["department"] for emp in st.session_state.employees]))
    selected_dept = st.selectbox("Filtrer par département:", departments)
    
    st.markdown("---")
    st.markdown("### 🔍 Recherche")
    search_name = st.text_input("Rechercher par nom:")
    
    # Notifications
    st.markdown("---")
    st.markdown(f"### 🔔 Notifications")
    
    # Vérifier les congés en attente
    if pending_vacations > 0:
        st.warning(f"**{pending_vacations} demande(s) de congé en attente**")
    
    # Vérifier les anniversaires ce mois-ci (simulé)
    st.info("🎂 **Anniversaires ce mois:** Ali (15), Karim (22)")
    
    # Vérifier les contrats à renouveler (simulé)
    st.info("📝 **2 contrats à renouveler** ce mois")
    
    st.markdown("---")
    st.markdown("### 📊 Résumé")
    total_emp = len(st.session_state.employees)
    active_emp = len([e for e in st.session_state.employees if e["status"] == "Actif"])
    on_leave = len([e for e in st.session_state.employees if e["status"] == "En congé"])
    avg_salary = sum(e["salary"] for e in st.session_state.employees) / total_emp if total_emp > 0 else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("👥 Total", total_emp)
    with col2:
        st.metric("✅ Actifs", active_emp)
    
    col3, col4 = st.columns(2)
    with col3:
        st.metric("🏖️ En congé", on_leave)
    with col4:
        st.metric("💰 Moyenne", f"{avg_salary:,.0f}")

# Filtrage des employés
filtered_employees = st.session_state.employees
if selected_dept != "Tous":
    filtered_employees = [e for e in filtered_employees if e["department"] == selected_dept]
if search_name:
    filtered_employees = [e for e in filtered_employees if search_name.lower() in e["name"].lower()]

# Pages principales
if page == "📊 Vue d'ensemble":
    # KPI Cards
    st.subheader("📈 Tableau de Bord KPI")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        total_budget = sum(e["salary"] for e in st.session_state.employees)
        st.metric("💰 Budget Total", f"{total_budget:,.0f} MAD", "+12%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        if st.session_state.employees:
            highest_salary = max(e["salary"] for e in st.session_state.employees)
            highest_emp = next(e["name"] for e in st.session_state.employees if e["salary"] == highest_salary)
            st.metric("👑 Salaire Max", f"{highest_salary:,.0f} MAD", highest_emp.split()[0])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        if st.session_state.employees:
            # Taux de rotation
            resigned = len([e for e in st.session_state.employees if e["status"] == "Démission"])
            turnover_rate = (resigned / total_emp * 100) if total_emp > 0 else 0
            st.metric("🔄 Rotation", f"{turnover_rate:.1f}%", "-2.5%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        if st.session_state.evaluations:
            avg_score = sum(e["score"] for e in st.session_state.evaluations) / len(st.session_state.evaluations)
            st.metric("⭐ Performance", f"{avg_score:.1f}/5", "+0.3")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Répartition des Salaires")
        if st.session_state.employees:
            df_salary = pd.DataFrame(st.session_state.employees)
            fig_salary = px.bar(df_salary, x='name', y='salary', 
                              color='department',
                              title="Salaires par Employé",
                              labels={'salary': 'Salaire (MAD)', 'name': 'Employé'},
                              color_discrete_sequence=px.colors.qualitative.Set3,
                              text='salary')
            fig_salary.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig_salary.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
            st.plotly_chart(fig_salary, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Répartition par Département")
        if st.session_state.employees:
            dept_data = pd.DataFrame([e["department"] for e in st.session_state.employees])
            dept_counts = dept_data[0].value_counts()
            fig_dept = px.pie(values=dept_counts.values, 
                            names=dept_counts.index,
                            title="Employés par Département",
                            color_discrete_sequence=px.colors.sequential.RdBu,
                            hole=0.3)
            st.plotly_chart(fig_dept, use_container_width=True)
    
    # Tableau des employés récents
    st.subheader("👥 Employés Récents")
    if st.session_state.employees:
        recent_employees = sorted(st.session_state.employees, 
                                 key=lambda x: datetime.strptime(x["join_date"], "%Y-%m-%d"), 
                                 reverse=True)[:5]
        
        for emp in recent_employees:
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.write(f"**{emp['name']}**")
                st.caption(f"{emp['role']}")
            with col2:
                st.write(f"🏢 {emp['department']}")
            with col3:
                st.write(f"📅 {emp['join_date']}")
            with col4:
                status_color = "🟢" if emp["status"] == "Actif" else "🟡"
                st.write(status_color)

elif page == "➕ Ajouter Employé":
    st.subheader("🎯 Ajouter un Nouvel Employé")
    
    with st.form("add_employee_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nom Complet *", placeholder="Ex: Mohamed Alami")
            role = st.text_input("Poste *", placeholder="Ex: Développeur Full Stack")
            department = st.selectbox("Département *", ["IT", "RH", "Finance", "Marketing", "Ventes", "Support", "Production", "Logistique"])
            email = st.text_input("Email *", placeholder="exemple@entreprise.com")
        
        with col2:
            salary = st.number_input("Salaire Mensuel (MAD) *", min_value=3000, max_value=200000, value=15000, step=1000)
            join_date = st.date_input("Date d'embauche *", datetime.now())
            phone = st.text_input("Téléphone", placeholder="06XXXXXXXX")
            status = st.selectbox("Statut *", ["Actif", "En congé", "Démission"])
        
        submitted = st.form_submit_button("➕ Ajouter Employé", type="primary", use_container_width=True)
        
        if submitted:
            if name.strip() and role.strip() and email.strip():
                new_employee = {
                    "id": st.session_state.next_id,
                    "name": name,
                    "role": role,
                    "department": department,
                    "salary": salary,
                    "join_date": join_date.strftime("%Y-%m-%d"),
                    "status": status,
                    "email": email,
                    "phone": phone
                }
                st.session_state.employees.append(new_employee)
                st.session_state.next_id += 1
                st.success(f"✅ Employé {name} ajouté avec succès!")
                st.balloons()
            else:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")

elif page == "👥 Liste des Employés":
    st.subheader("📋 Liste des Employés")
    
    # Options de tri
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        sort_by = st.selectbox("Trier par", ["Nom", "Salaire", "Date d'embauche", "Département"])
    with col2:
        sort_order = st.selectbox("Ordre", ["Croissant", "Décroissant"])
    with col3:
        items_per_page = st.selectbox("Par page", [10, 25, 50])
    
    # Trier les employés
    if sort_by == "Nom":
        filtered_employees.sort(key=lambda x: x["name"], reverse=(sort_order == "Décroissant"))
    elif sort_by == "Salaire":
        filtered_employees.sort(key=lambda x: x["salary"], reverse=(sort_order == "Décroissant"))
    elif sort_by == "Date d'embauche":
        filtered_employees.sort(key=lambda x: x["join_date"], reverse=(sort_order == "Décroissant"))
    elif sort_by == "Département":
        filtered_employees.sort(key=lambda x: x["department"], reverse=(sort_order == "Décroissant"))
    
    if not filtered_employees:
        st.warning("Aucun employé trouvé avec les critères de recherche.")
    else:
        # Pagination
        total_pages = (len(filtered_employees) + items_per_page - 1) // items_per_page
        page_number = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        
        start_idx = (page_number - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(filtered_employees))
        
        st.caption(f"Affichage {start_idx + 1}-{end_idx} sur {len(filtered_employees)} employés")
        
        for emp in filtered_employees[start_idx:end_idx]:
            status_color = {
                "Actif": "🟢",
                "En congé": "🟡", 
                "Démission": "🔴"
            }.get(emp["status"], "⚪")
            
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 1, 1])
                
                with col1:
                    st.markdown(f"**{emp['name']}**")
                    st.caption(f"{emp['email']}")
                    st.caption(f"📱 {emp.get('phone', 'N/A')}")
                
                with col2:
                    st.write(f"💼 {emp['role']}")
                    st.caption(f"🏢 {emp['department']}")
                
                with col3:
                    st.write(f"💰 {emp['salary']:,.0f} MAD")
                    st.caption("Mensuel")
                
                with col4:
                    st.write(f"📅 {emp['join_date']}")
                    days_diff = (datetime.now() - datetime.strptime(emp['join_date'], "%Y-%m-%d")).days
                    st.caption(f"({days_diff//365} ans, {(days_diff%365)//30} mois)")
                    st.caption(f"{status_color} {emp['status']}")
                
                with col5:
                    if st.button("✏️", key=f"edit_{emp['id']}", help="Modifier"):
                        st.session_state.edit_id = emp['id']
                
                with col6:
                    if st.button("🗑️", key=f"delete_{emp['id']}", help="Supprimer"):
                        st.session_state.employees = [e for e in st.session_state.employees if e['id'] != emp['id']]
                        st.rerun()
                
                st.divider()
        
        # Afficher la pagination
        if total_pages > 1:
            cols = st.columns(total_pages + 2)
            for i in range(total_pages):
                if cols[i].button(str(i + 1), key=f"page_{i}"):
                    page_number = i + 1
                    st.rerun()
    
    # Section de modification
    if 'edit_id' in st.session_state:
        emp_to_edit = next((e for e in st.session_state.employees if e['id'] == st.session_state.edit_id), None)
        if emp_to_edit:
            st.subheader(f"✏️ Modifier: {emp_to_edit['name']}")
            
            with st.form("edit_employee_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("Nom", emp_to_edit["name"])
                    new_role = st.text_input("Poste", emp_to_edit["role"])
                    new_dept = st.selectbox("Département", 
                                           ["IT", "RH", "Finance", "Marketing", "Ventes", "Support", "Production", "Logistique"],
                                           index=["IT", "RH", "Finance", "Marketing", "Ventes", "Support", "Production", "Logistique"].index(emp_to_edit["department"]) 
                                           if emp_to_edit["department"] in ["IT", "RH", "Finance", "Marketing", "Ventes", "Support", "Production", "Logistique"] else 0)
                    new_email = st.text_input("Email", emp_to_edit.get("email", ""))
                
                with col2:
                    new_salary = st.number_input("Salaire", value=emp_to_edit["salary"], min_value=3000, max_value=200000, step=1000)
                    new_join_date = st.date_input("Date d'embauche", 
                                                 datetime.strptime(emp_to_edit["join_date"], "%Y-%m-%d"))
                    new_phone = st.text_input("Téléphone", emp_to_edit.get("phone", ""))
                    new_status = st.selectbox("Statut", ["Actif", "En congé", "Démission"],
                                             index=["Actif", "En congé", "Démission"].index(emp_to_edit["status"]))
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.form_submit_button("💾 Enregistrer les modifications", use_container_width=True, type="primary"):
                        emp_to_edit.update({
                            "name": new_name,
                            "role": new_role,
                            "department": new_dept,
                            "salary": new_salary,
                            "join_date": new_join_date.strftime("%Y-%m-%d"),
                            "status": new_status,
                            "email": new_email,
                            "phone": new_phone
                        })
                        del st.session_state.edit_id
                        st.success("✅ Employé mis à jour avec succès!")
                        st.rerun()
                
                if st.form_submit_button("❌ Annuler", use_container_width=True):
                    del st.session_state.edit_id
                    st.rerun()

elif page == "📈 Statistiques":
    st.subheader("📊 Statistiques Avancées")
    
    if st.session_state.employees:
        df = pd.DataFrame(st.session_state.employees)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Distribution des Salaires")
            fig_hist = px.histogram(df, x='salary', nbins=10, 
                                   title="Distribution des Salaires",
                                   labels={'salary': 'Salaire (MAD)'},
                                   color_discrete_sequence=['#3B82F6'],
                                   marginal="box")
            fig_hist.update_layout(bargap=0.1)
            st.plotly_chart(fig_hist, use_container_width=True)
            
            st.markdown("### 🏢 Salaires par Département")
            dept_stats = df.groupby('department')['salary'].agg(['mean', 'count', 'min', 'max']).reset_index()
            dept_stats = dept_stats.rename(columns={'mean': 'Salaire Moyen', 'count': 'Nombre', 'min': 'Min', 'max': 'Max'})
            st.dataframe(dept_stats, use_container_width=True)
        
        with col2:
            st.markdown("### 📅 Embauches par Mois")
            df['join_date'] = pd.to_datetime(df['join_date'])
            df['join_month'] = df['join_date'].dt.strftime('%Y-%m')
            monthly_hire = df.groupby('join_month').size().reset_index(name='count')
            
            fig_timeline = px.line(monthly_hire, x='join_month', y='count',
                                  title="Embauches par Mois",
                                  markers=True,
                                  line_shape='spline',
                                  color_discrete_sequence=['#10B981'])
            fig_timeline.update_traces(fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.1)')
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            st.markdown("### 📋 Analyse des Dépenses")
            total_by_dept = df.groupby('department')['salary'].sum().reset_index()
            total_by_dept = total_by_dept.sort_values('salary', ascending=False)
            
            fig_expenses = px.bar(total_by_dept, x='department', y='salary',
                                 title="Dépenses Salariales par Département",
                                 labels={'salary': 'Dépenses Total (MAD)', 'department': 'Département'},
                                 color='department',
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_expenses, use_container_width=True)
        
        # Analyses avancées
        st.markdown("---")
        st.subheader("🤖 Insights et Recommandations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔍 Détection d'Anomalies")
            
            # Calculer la moyenne et écart-type
            mean_salary = df['salary'].mean()
            std_salary = df['salary'].std()
            
            anomalies = df[(df['salary'] > mean_salary + 2*std_salary) | (df['salary'] < mean_salary - 2*std_salary)]
            
            if not anomalies.empty:
                st.warning("**Salaire anormal détecté:**")
                for _, row in anomalies.iterrows():
                    diff = ((row['salary'] - mean_salary) / mean_salary) * 100
                    st.write(f"• {row['name']}: {row['salary']:,.0f} MAD ({diff:+.1f}% vs moyenne)")
            else:
                st.success("✅ Pas d'anomalie salariale détectée")
        
        with col2:
            st.markdown("### 🎯 Recommandations RH")
            
            recommendations = []
            
            # Écarts salariaux par département
            for dept in df['department'].unique():
                dept_df = df[df['department'] == dept]
                dept_mean = dept_df['salary'].mean()
                
                for _, emp in dept_df.iterrows():
                    # Salaires trop bas par rapport à la moyenne du département
                    # Remplacer les lignes 513-514 par :
                    tenure_days = (datetime.now() - emp['join_date']).days if isinstance(emp['join_date'], pd.Timestamp) else (datetime.now() - datetime.strptime(str(emp['join_date']), "%Y-%m-%d")).days
                    if tenure_days > 365:  # Plus d'un an
                            recommendations.append(f"📈 **{emp['name']}** ({dept}): Salaire {emp['salary']:,.0f} MAD vs moyenne {dept_mean:,.0f} MAD (-{(1-emp['salary']/dept_mean)*100:.1f}%)")
            
            if recommendations:
                for rec in recommendations[:3]:
                    st.info(rec)
            else:
                st.success("✅ Pas de recommandation urgente")

elif page == "🏖️ Gestion Congés":
    st.subheader("🏖️ Gestion des Congés")
    
    tab1, tab2, tab3 = st.tabs(["📋 Congés en Cours", "➕ Nouvelle Demande", "📅 Calendrier"])
    
    with tab1:
        st.markdown("### 📋 Demandes de Congés")
        
        # Filtres
        col1, col2 = st.columns(2)
        with col1:
            filter_status = st.selectbox("Filtrer par statut", ["Tous", "Approuvé", "En attente", "Rejeté"])
        with col2:
            filter_type = st.selectbox("Filtrer par type", ["Tous", "Annuel", "Maladie", "Maternité", "Paternité"])
        
        filtered_vacations = st.session_state.vacations
        if filter_status != "Tous":
            filtered_vacations = [v for v in filtered_vacations if v["status"] == filter_status]
        if filter_type != "Tous":
            filtered_vacations = [v for v in filtered_vacations if v["type"] == filter_type]
        
        if not filtered_vacations:
            st.info("Aucune demande de congé trouvée.")
        else:
            for vac in filtered_vacations:
                status_color = {
                    "Approuvé": "🟢",
                    "En attente": "🟡",
                    "Rejeté": "🔴"
                }.get(vac["status"], "⚪")
                
                start_date = datetime.strptime(vac["start_date"], "%Y-%m-%d")
                end_date = datetime.strptime(vac["end_date"], "%Y-%m-%d")
                duration = (end_date - start_date).days + 1
                
                with st.container():
                    col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{vac['employee_name']}**")
                        st.caption(f"{vac['type']}")
                        if vac.get("reason"):
                            st.caption(f"📝 {vac['reason'][:30]}...")
                    
                    with col2:
                        st.write(f"📅 {vac['start_date']}")
                        st.caption("Début")
                    
                    with col3:
                        st.write(f"📅 {vac['end_date']}")
                        st.caption(f"Fin ({duration} jours)")
                    
                    with col4:
                        st.write(f"{status_color}")
                        st.caption(vac["status"])
                    
                    with col5:
                        if vac["status"] == "En attente":
                            if st.button("✓", key=f"approve_{vac['id']}", help="Approuver"):
                                vac["status"] = "Approuvé"
                                st.rerun()
                    
                    with col6:
                        if vac["status"] == "En attente":
                            if st.button("✗", key=f"reject_{vac['id']}", help="Rejeter"):
                                vac["status"] = "Rejeté"
                                st.rerun()
                        else:
                            if st.button("🗑️", key=f"delete_vac_{vac['id']}", help="Supprimer"):
                                st.session_state.vacations = [v for v in st.session_state.vacations if v['id'] != vac['id']]
                                st.rerun()
                    
                    st.divider()
    
    with tab2:
        st.markdown("### ➕ Nouvelle Demande de Congé")
        
        with st.form("new_vacation_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                emp_options = [f"{e['id']} - {e['name']} ({e['department']})" for e in st.session_state.employees if e['status'] == 'Actif']
                selected_emp = st.selectbox("Employé *", emp_options)
                leave_type = st.selectbox("Type de congé *", ["Annuel", "Maladie", "Maternité", "Paternité", "Sans solde", "Exceptionnel"])
            
            with col2:
                col_start, col_end = st.columns(2)
                with col_start:
                    start_date = st.date_input("Date de début *", datetime.now())
                with col_end:
                    end_date = st.date_input("Date de fin *", datetime.now())
                reason = st.text_area("Motif *", placeholder="Détaillez la raison du congé...")
            
            submitted = st.form_submit_button("📤 Soumettre la demande", type="primary", use_container_width=True)
            
            if submitted:
                if start_date <= end_date and reason.strip():
                    emp_id = int(selected_emp.split(" - ")[0])
                    emp_name = selected_emp.split(" - ")[1].split(" (")[0]
                    
                    new_vacation = {
                        "id": st.session_state.next_vacation_id,
                        "employee_id": emp_id,
                        "employee_name": emp_name,
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": end_date.strftime("%Y-%m-%d"),
                        "type": leave_type,
                        "reason": reason,
                        "status": "En attente"
                    }
                    st.session_state.vacations.append(new_vacation)
                    st.session_state.next_vacation_id += 1
                    st.success("✅ Demande de congé soumise avec succès!")
                    st.balloons()
                else:
                    st.error("❌ Veuillez vérifier les dates et remplir le motif")
    
    with tab3:
        st.markdown("### 📅 Calendrier des Congés")
        
        # Sélection du mois
        current_date = datetime.now()
        selected_month = st.selectbox("Sélectionner le mois", 
                                     [f"{i:02d}/2024" for i in range(1, 13)],
                                     index=current_date.month - 1)
        
        # Simuler un calendrier des congés
        st.markdown(f"#### Congés pour {selected_month}")
        
        calendar_data = []
        month_vacations = [v for v in st.session_state.vacations 
                          if v["status"] == "Approuvé" 
                          and v["start_date"][:7] == f"2024-{selected_month.split('/')[0]}"[:7]]
        
        if month_vacations:
            for vac in month_vacations:
                calendar_data.append({
                    "Employé": vac["employee_name"],
                    "Type": vac["type"],
                    "Début": vac["start_date"],
                    "Fin": vac["end_date"],
                    "Durée": (datetime.strptime(vac["end_date"], "%Y-%m-%d") - datetime.strptime(vac["start_date"], "%Y-%m-%d")).days + 1
                })
            
            df_calendar = pd.DataFrame(calendar_data)
            st.dataframe(df_calendar, use_container_width=True, hide_index=True)
            
            # Statistiques des congés
            st.markdown("#### 📊 Statistiques des Congés")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Congés", len(month_vacations))
            with col2:
                total_days = sum([(datetime.strptime(v["end_date"], "%Y-%m-%d") - datetime.strptime(v["start_date"], "%Y-%m-%d")).days + 1 
                                 for v in month_vacations])
                st.metric("Jours Totaux", total_days)
            with col3:
                most_common_type = pd.DataFrame(calendar_data)["Type"].mode()[0] if calendar_data else "N/A"
                st.metric("Type le Plus Fréquent", most_common_type)
        else:
            st.info("Aucun congé prévu pour ce mois.")

elif page == "⭐ Évaluations":
    st.subheader("⭐ Évaluations de Performance")
    
    tab1, tab2 = st.tabs(["📊 Historique", "➕ Nouvelle Évaluation"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📈 Performance par Employé")
            
            if st.session_state.evaluations:
                eval_df = pd.DataFrame(st.session_state.evaluations)
                
                # Graphique des scores
                avg_scores = eval_df.groupby('employee_name')['score'].mean().reset_index()
                avg_scores = avg_scores.sort_values('score', ascending=False)
                
                fig_scores = px.bar(avg_scores, x='employee_name', y='score',
                                   title="Score Moyen par Employé",
                                   labels={'score': 'Score Moyen (/5)', 'employee_name': 'Employé'},
                                   color='score',
                                   color_continuous_scale='RdYlGn')
                st.plotly_chart(fig_scores, use_container_width=True)
                
                # Table des évaluations détaillées
                st.markdown("### 📋 Dernières Évaluations")
                recent_evals = eval_df.sort_values('date', ascending=False).head(10)
                st.dataframe(recent_evals[['employee_name', 'date', 'score', 'manager', 'comment']],
                            use_container_width=True,
                            hide_index=True)
        
        with col2:
            st.markdown("### 🏆 Top Performeurs")
            
            if st.session_state.evaluations:
                eval_df = pd.DataFrame(st.session_state.evaluations)
                top_performers = eval_df.groupby('employee_name')['score'].mean().nlargest(5).reset_index()
                
                for i, (_, row) in enumerate(top_performers.iterrows(), 1):
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "⭐"
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); 
                                padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;'>
                        <h4>{medal} {row['employee_name']}</h4>
                        <p>Score: {row['score']:.2f}/5</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 📊 Résumé")
                
                avg_score = eval_df['score'].mean()
                max_score = eval_df['score'].max()
                min_score = eval_df['score'].min()
                
                st.metric("Score Moyen", f"{avg_score:.2f}/5")
                st.metric("Meilleur Score", f"{max_score:.2f}/5")
                st.metric("Score Minimum", f"{min_score:.2f}/5")
    
    with tab2:
        st.markdown("### ➕ Nouvelle Évaluation de Performance")
        
        with st.form("new_evaluation_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                emp_options = [f"{e['id']} - {e['name']}" for e in st.session_state.employees]
                selected_emp = st.selectbox("Employé *", emp_options)
                
                score = st.slider("Score (/5) *", 1.0, 5.0, 3.0, 0.1)
                manager = st.text_input("Évaluateur *", placeholder="Nom du manager")
            
            with col2:
                eval_date = st.date_input("Date d'évaluation *", datetime.now())
                
                st.markdown("#### Compétences")
                technical = st.slider("Compétences techniques", 1, 5, 3)
                communication = st.slider("Communication", 1, 5, 3)
                teamwork = st.slider("Travail d'équipe", 1, 5, 3)
                leadership = st.slider("Leadership", 1, 5, 3)
            
            comment = st.text_area("Commentaires et recommandations *", 
                                 placeholder="Décrivez les points forts, axes d'amélioration...",
                                 height=150)
            
            submitted = st.form_submit_button("📝 Enregistrer l'évaluation", type="primary", use_container_width=True)
            
            if submitted:
                if manager.strip() and comment.strip():
                    emp_id = int(selected_emp.split(" - ")[0])
                    emp_name = selected_emp.split(" - ")[1]
                    
                    new_eval = {
                        "id": st.session_state.next_evaluation_id,
                        "employee_id": emp_id,
                        "employee_name": emp_name,
                        "date": eval_date.strftime("%Y-%m-%d"),
                        "score": score,
                        "technical": technical,
                        "communication": communication,
                        "teamwork": teamwork,
                        "leadership": leadership,
                        "comment": comment,
                        "manager": manager
                    }
                    st.session_state.evaluations.append(new_eval)
                    st.session_state.next_evaluation_id += 1
                    st.success("✅ Évaluation enregistrée avec succès!")
                    st.balloons()
                else:
                    st.error("❌ Veuillez remplir tous les champs obligatoires")

else:  # Paramètres
    st.subheader("⚙️ Paramètres et Administration")
    
    tab1, tab2, tab3 = st.tabs(["📊 Données", "🎨 Personnalisation", "⚠️ Administration"])
    
    with tab1:
        st.markdown("### 📊 Gestion des Données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Import de Données")
            uploaded_file = st.file_uploader("Importer des employés (CSV/JSON)", type=['csv', 'json'])
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                        # Convertir DataFrame en liste de dictionnaires
                        new_employees = df.to_dict('records')
                        st.success(f"✅ {len(new_employees)} employés chargés")
                        st.dataframe(df.head(), use_container_width=True)
                        
                        if st.button("💾 Importer dans la base"):
                            for emp in new_employees:
                                emp["id"] = st.session_state.next_id
                                st.session_state.next_id += 1
                                st.session_state.employees.append(emp)
                            st.success("✅ Données importées avec succès!")
                            
                    elif uploaded_file.name.endswith('.json'):
                        data = json.load(uploaded_file)
                        st.success(f"✅ {len(data)} employés chargés")
                        
                        if st.button("💾 Importer dans la base"):
                            for emp in data:
                                emp["id"] = st.session_state.next_id
                                st.session_state.next_id += 1
                                st.session_state.employees.append(emp)
                            st.success("✅ Données importées avec succès!")
                            
                except Exception as e:
                    st.error(f"❌ Erreur lors du chargement: {str(e)}")
        
        with col2:
            st.markdown("#### 📤 Export de Données")
            export_format = st.selectbox("Format d'export", ["CSV", "Excel", "JSON"])
            
            if st.button("📥 Exporter les données", use_container_width=True):
                df = pd.DataFrame(st.session_state.employees)
                
                if export_format == "CSV":
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger CSV",
                        data=csv,
                        file_name=f"employes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        type="primary"
                    )
                elif export_format == "Excel":
                    excel_file = df.to_excel(index=False)
                    st.download_button(
                        label="📥 Télécharger Excel",
                        data=excel_file,
                        file_name=f"employes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                elif export_format == "JSON":
                    json_data = df.to_json(orient='records', indent=2)
                    st.download_button(
                        label="📥 Télécharger JSON",
                        data=json_data,
                        file_name=f"employes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            st.markdown("---")
            st.markdown("#### 📊 Statistiques Base de Données")
            st.write(f"**Employés:** {len(st.session_state.employees)}")
            st.write(f"**Congés:** {len(st.session_state.vacations)}")
            st.write(f"**Évaluations:** {len(st.session_state.evaluations)}")
    
    with tab2:
        st.markdown("### 🎨 Personnalisation de l'Interface")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Thème Couleurs")
            primary_color = st.color_picker("Couleur primaire", "#3B82F6")
            secondary_color = st.color_picker("Couleur secondaire", "#10B981")
            accent_color = st.color_picker("Couleur d'accent", "#8B5CF6")
            
            if st.button("💾 Appliquer les couleurs", use_container_width=True):
                st.success("✅ Couleurs appliquées (simulation)")
            
            st.markdown("---")
            st.markdown("#### 📱 Affichage")
            show_avatars = st.checkbox("Afficher les avatars", value=True)
            compact_mode = st.checkbox("Mode compact")
            auto_refresh = st.checkbox("Actualisation automatique", value=True)
        
        with col2:
            st.markdown("#### 🔔 Notifications")
            email_notifications = st.checkbox("Notifications par email", value=True)
            push_notifications = st.checkbox("Notifications push", value=True)
            
            st.markdown("##### Types de notifications:")
            notify_new_employee = st.checkbox("Nouvel employé", value=True)
            notify_vacation_request = st.checkbox("Demande de congé", value=True)
            notify_evaluation = st.checkbox("Nouvelle évaluation", value=True)
            notify_contract_end = st.checkbox("Fin de contrat", value=True)
            
            if st.button("💾 Enregistrer les préférences", use_container_width=True):
                st.success("✅ Préférences enregistrées")
    
    with tab3:
        st.markdown("### ⚠️ Zone d'Administration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔧 Maintenance")
            
            if st.button("🔄 Réinitialiser les filtres", use_container_width=True):
                if 'edit_id' in st.session_state:
                    del st.session_state.edit_id
                st.success("✅ Filtres réinitialisés")
            
            if st.button("🧹 Nettoyer les données", use_container_width=True):
                # Supprimer les employés avec statut "Démission" depuis plus d'un an
                current_date = datetime.now()
                old_resigned = []
                for emp in st.session_state.employees[:]:
                    if emp["status"] == "Démission":
                        join_date = datetime.strptime(emp["join_date"], "%Y-%m-%d")
                        if (current_date - join_date).days > 365:
                            old_resigned.append(emp["name"])
                            st.session_state.employees.remove(emp)
                
                if old_resigned:
                    st.warning(f"✅ {len(old_resigned)} anciens employés supprimés: {', '.join(old_resigned)}")
                else:
                    st.info("✅ Aucun ancien employé à supprimer")
            
            if st.button("📊 Générer rapport système", use_container_width=True):
                report = f"""
                ### 📋 Rapport Système - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                
                **Statistiques:**
                - Employés totaux: {len(st.session_state.employees)}
                - Employés actifs: {len([e for e in st.session_state.employees if e['status'] == 'Actif'])}
                - Demandes de congé: {len(st.session_state.vacations)}
                - Évaluations: {len(st.session_state.evaluations)}
                
                **Métriques:**
                - Budget salarial total: {sum(e['salary'] for e in st.session_state.employees):,.0f} MAD
                - Salaire moyen: {sum(e['salary'] for e in st.session_state.employees)/len(st.session_state.employees):,.0f} MAD
                - Score moyen d'évaluation: {sum(e['score'] for e in st.session_state.evaluations)/len(st.session_state.evaluations):.2f}/5
                
                **Dernière activité:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                st.markdown(report)
        
        with col2:
            st.markdown("#### 🗑️ Actions Dangereuses")
            st.warning("⚠️ Ces actions sont irréversibles!")
            
            delete_confirm = st.text_input("Écrire 'SUPPRIMER' pour confirmer:")
            
            col_del1, col_del2 = st.columns(2)
            
            with col_del1:
                if st.button("🗑️ Supprimer tous les congés", type="secondary", use_container_width=True):
                    if delete_confirm == "SUPPRIMER":
                        st.session_state.vacations = []
                        st.session_state.next_vacation_id = 1
                        st.error("✅ Tous les congés ont été supprimés!")
                        st.rerun()
                    else:
                        st.error("❌ Veuillez écrire 'SUPPRIMER' pour confirmer")
            
            with col_del2:
                if st.button("🗑️ Supprimer toutes les évaluations", type="secondary", use_container_width=True):
                    if delete_confirm == "SUPPRIMER":
                        st.session_state.evaluations = []
                        st.session_state.next_evaluation_id = 1
                        st.error("✅ Toutes les évaluations ont été supprimées!")
                        st.rerun()
                    else:
                        st.error("❌ Veuillez écrire 'SUPPRIMER' pour confirmer")
            
            if st.button("🔥 Supprimer TOUTES les données", type="secondary", use_container_width=True):
                if delete_confirm == "SUPPRIMER":
                    st.session_state.employees = []
                    st.session_state.vacations = []
                    st.session_state.evaluations = []
                    st.session_state.next_id = 1
                    st.session_state.next_vacation_id = 1
                    st.session_state.next_evaluation_id = 1
                    st.error("🔥 TOUTES les données ont été supprimées!")
                    st.rerun()
                else:
                    st.error("❌ Veuillez écrire 'SUPPRIMER' pour confirmer")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; color: white;'>
        <h4>HR Dashboard Pro v2.0</h4>
        <p>© 2024 - Développé avec ❤️ et Streamlit 🎈</p>
        <p>Dernière mise à jour: {}</p>
        <p>👥 {} employés | 🏖️ {} congés | ⭐ {} évaluations</p>
    </div>
    """.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        len(st.session_state.employees),
        len(st.session_state.vacations),
        len(st.session_state.evaluations)
    ), unsafe_allow_html=True)