
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #2E8B57;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #2E8B57;
    }
    .status-success { color: #28a745; }
    .status-pending { color: #ffc107; }
    .status-cancelled { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Database connection function
@st.cache_resource
def get_database_connection():
    return sqlite3.connect('food_waste_management.db', check_same_thread=False)

# Load data functions
@st.cache_data
def load_providers():
    conn = get_database_connection()
    return pd.read_sql_query("SELECT * FROM providers", conn)

@st.cache_data
def load_receivers():
    conn = get_database_connection()
    return pd.read_sql_query("SELECT * FROM receivers", conn)

@st.cache_data
def load_food_listings():
    conn = get_database_connection()
    return pd.read_sql_query("SELECT * FROM food_listings", conn)

@st.cache_data
def load_claims():
    conn = get_database_connection()
    return pd.read_sql_query("SELECT * FROM claims", conn)

# SQL Query functions
def execute_query(query):
    conn = get_database_connection()
    return pd.read_sql_query(query, conn)

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">🍽️ Local Food Wastage Management System</h1>', unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Dashboard", "Food Listings", "Claims Management", "Providers & Receivers", 
         "Analytics", "SQL Queries", "Reports"]
    )

    if page == "Dashboard":
        show_dashboard()
    elif page == "Food Listings":
        show_food_listings()
    elif page == "Claims Management":
        show_claims_management()
    elif page == "Providers & Receivers":
        show_providers_receivers()
    elif page == "Analytics":
        show_analytics()
    elif page == "SQL Queries":
        show_sql_queries()
    elif page == "Reports":
        show_reports()

def show_dashboard():
    st.header("📈 Dashboard Overview")

    # Load data
    providers = load_providers()
    receivers = load_receivers()
    food_listings = load_food_listings()
    claims = load_claims()

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🏪 Total Providers",
            value=len(providers),
            delta=f"{len(providers.groupby('City'))} cities"
        )

    with col2:
        st.metric(
            label="👥 Total Receivers", 
            value=len(receivers),
            delta=f"{len(receivers.groupby('City'))} cities"
        )

    with col3:
        st.metric(
            label="🍎 Food Items",
            value=len(food_listings),
            delta=f"{food_listings['Quantity'].sum():,} total units"
        )

    with col4:
        completed_claims = len(claims[claims['Status'] == 'Completed'])
        st.metric(
            label="✅ Successful Claims",
            value=completed_claims,
            delta=f"{completed_claims/len(claims)*100:.1f}% success rate"
        )

    # Charts row
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Claims Status Distribution")
        status_counts = claims['Status'].value_counts()
        fig_pie = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Claim Status Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("🏙️ Food Listings by City")
        city_counts = food_listings['Location'].value_counts()
        fig_bar = px.bar(
            x=city_counts.index,
            y=city_counts.values,
            title="Food Listings by City",
            labels={'x': 'City', 'y': 'Number of Listings'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

def show_food_listings():
    st.header("🍽️ Food Listings Management")

    # Load data
    food_listings = load_food_listings()
    providers = load_providers()

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        city_filter = st.selectbox(
            "Filter by City:",
            ["All"] + list(food_listings['Location'].unique())
        )

    with col2:
        food_type_filter = st.selectbox(
            "Filter by Food Type:",
            ["All"] + list(food_listings['Food_Type'].unique())
        )

    with col3:
        meal_type_filter = st.selectbox(
            "Filter by Meal Type:",
            ["All"] + list(food_listings['Meal_Type'].unique())
        )

    # Apply filters
    filtered_data = food_listings.copy()

    if city_filter != "All":
        filtered_data = filtered_data[filtered_data['Location'] == city_filter]

    if food_type_filter != "All":
        filtered_data = filtered_data[filtered_data['Food_Type'] == food_type_filter]

    if meal_type_filter != "All":
        filtered_data = filtered_data[filtered_data['Meal_Type'] == meal_type_filter]

    # Display results
    st.subheader(f"📋 Found {len(filtered_data)} food items")

    # Add provider information
    display_data = filtered_data.merge(
        providers[['Provider_ID', 'Name', 'Contact']], 
        on='Provider_ID', 
        how='left'
    )

    st.dataframe(
        display_data[['Food_Name', 'Quantity', 'Food_Type', 'Meal_Type', 
                     'Location', 'Expiry_Date', 'Name', 'Contact']].rename(columns={
            'Name': 'Provider_Name',
            'Contact': 'Provider_Contact'
        }),
        use_container_width=True
    )

def show_claims_management():
    st.header("📝 Claims Management")

    # CRUD Operations tabs
    tab1, tab2, tab3 = st.tabs(["View Claims", "Add New Claim", "Update Claim"])

    with tab1:
        # Display claims
        claims = load_claims()
        food_listings = load_food_listings()
        receivers = load_receivers()

        # Join with food and receiver information
        claims_detailed = claims.merge(
            food_listings[['Food_ID', 'Food_Name', 'Quantity']], 
            on='Food_ID'
        ).merge(
            receivers[['Receiver_ID', 'Name']], 
            on='Receiver_ID'
        )

        st.dataframe(
            claims_detailed[['Claim_ID', 'Food_Name', 'Quantity', 'Name', 'Status', 'Timestamp']].rename(columns={
                'Name': 'Receiver_Name'
            }),
            use_container_width=True
        )

    with tab2:
        st.subheader("➕ Add New Claim")

        # Form for new claim
        with st.form("new_claim_form"):
            food_listings = load_food_listings()
            receivers = load_receivers()

            selected_food = st.selectbox(
                "Select Food Item:",
                options=food_listings['Food_ID'].tolist(),
                format_func=lambda x: f"{food_listings[food_listings['Food_ID']==x]['Food_Name'].iloc[0]} (Qty: {food_listings[food_listings['Food_ID']==x]['Quantity'].iloc[0]})"
            )

            selected_receiver = st.selectbox(
                "Select Receiver:",
                options=receivers['Receiver_ID'].tolist(),
                format_func=lambda x: f"{receivers[receivers['Receiver_ID']==x]['Name'].iloc[0]}"
            )

            submitted = st.form_submit_button("Submit Claim")

            if submitted:
                # Add claim to database
                conn = get_database_connection()
                cursor = conn.cursor()

                # Get next claim ID
                cursor.execute("SELECT MAX(Claim_ID) FROM claims")
                max_id = cursor.fetchone()[0] or 0
                new_claim_id = max_id + 1

                cursor.execute("""
                    INSERT INTO claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (new_claim_id, selected_food, selected_receiver, 'Pending', datetime.now().isoformat()))

                conn.commit()
                st.success(f"Claim {new_claim_id} submitted successfully!")
                st.rerun()

    with tab3:
        st.subheader("✏️ Update Claim Status")

        claims = load_claims()

        claim_to_update = st.selectbox(
            "Select Claim to Update:",
            options=claims['Claim_ID'].tolist()
        )

        new_status = st.selectbox(
            "New Status:",
            options=['Pending', 'Completed', 'Cancelled']
        )

        if st.button("Update Status"):
            conn = get_database_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE claims 
                SET Status = ?
                WHERE Claim_ID = ?
            """, (new_status, claim_to_update))

            conn.commit()
            st.success(f"Claim {claim_to_update} status updated to {new_status}!")
            st.rerun()

def show_providers_receivers():
    st.header("👥 Providers & Receivers Directory")

    tab1, tab2 = st.tabs(["Providers", "Receivers"])

    with tab1:
        providers = load_providers()

        # Provider type filter
        provider_type = st.selectbox(
            "Filter by Provider Type:",
            ["All"] + list(providers['Type'].unique())
        )

        if provider_type != "All":
            providers = providers[providers['Type'] == provider_type]

        st.dataframe(providers, use_container_width=True)

    with tab2:
        receivers = load_receivers()

        # Receiver type filter
        receiver_type = st.selectbox(
            "Filter by Receiver Type:",
            ["All"] + list(receivers['Type'].unique())
        )

        if receiver_type != "All":
            receivers = receivers[receivers['Type'] == receiver_type]

        st.dataframe(receivers, use_container_width=True)

def show_analytics():
    st.header("📊 Analytics & Insights")

    # Load data
    food_listings = load_food_listings()
    claims = load_claims()
    providers = load_providers()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🍎 Food Type Distribution")
        food_type_counts = food_listings['Food_Type'].value_counts()
        fig = px.bar(x=food_type_counts.index, y=food_type_counts.values)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🍽️ Meal Type Distribution")
        meal_type_counts = food_listings['Meal_Type'].value_counts()
        fig = px.bar(x=meal_type_counts.index, y=meal_type_counts.values)
        st.plotly_chart(fig, use_container_width=True)

def show_sql_queries():
    st.header("🔍 SQL Query Results")

    queries = {
        "Query 1: Providers by City": "SELECT City, COUNT(*) as Total_Providers FROM providers GROUP BY City ORDER BY Total_Providers DESC",
        "Query 2: Provider Type Contributions": """
            SELECT p.Type, COUNT(f.Food_ID) as Total_Items, SUM(f.Quantity) as Total_Quantity
            FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            GROUP BY p.Type ORDER BY Total_Quantity DESC
        """,
        "Query 3: Claim Status Distribution": "SELECT Status, COUNT(*) as Count FROM claims GROUP BY Status",
        # Add more queries as needed
    }

    selected_query = st.selectbox("Select Query:", list(queries.keys()))

    if st.button("Execute Query"):
        result = execute_query(queries[selected_query])
        st.dataframe(result, use_container_width=True)

def show_reports():
    st.header("📋 Reports")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Wastage Report"):
            wastage_query = """
                SELECT f.Location, COUNT(f.Food_ID) as Unclaimed_Items, SUM(f.Quantity) as Wasted_Quantity
                FROM food_listings f LEFT JOIN claims c ON f.Food_ID = c.Food_ID
                WHERE c.Food_ID IS NULL OR c.Status = 'Cancelled'
                GROUP BY f.Location ORDER BY Wasted_Quantity DESC
            """
            result = execute_query(wastage_query)
            st.dataframe(result, use_container_width=True)

    with col2:
        if st.button("Generate Performance Report"):
            performance_query = """
                SELECT p.Name, COUNT(c.Claim_ID) as Successful_Claims
                FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID
                JOIN claims c ON f.Food_ID = c.Food_ID
                WHERE c.Status = 'Completed'
                GROUP BY p.Provider_ID, p.Name ORDER BY Successful_Claims DESC LIMIT 10
            """
            result = execute_query(performance_query)
            st.dataframe(result, use_container_width=True)

if __name__ == "__main__":
    main()
