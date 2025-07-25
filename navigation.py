import streamlit as st

def render_navigation_buttons():
    """
    Displays the navigation buttons for the app with beautiful childish styling.
    Uses st.switch_page to navigate between pages.
    """
    # Custom CSS for professional, subtle navigation
    st.markdown("""
    <style>
        /* Navigation container styling */
        .nav-container {
            background: #F8FAFE;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 12px rgba(91, 155, 213, 0.15);  /* Increased shadow depth */
            border: 1px solid #E1E8ED;
        }
        
        /* Navigation title */
        .nav-title {
            text-align: center;
            color: #5B9BD5;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        /* Button styling override */
        .stButton > button {
            background: linear-gradient(135deg, #E0F7FA, #F8FAFE) !important;
            color: #2C3E50 !important;
            border: 1px solid #E1E8ED !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 12px 16px !important;  /* Slightly wider padding */
            transition: all 0.2s ease !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
            height: 50px !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(91, 155, 213, 0.2) !important;
            border-color: #5B9BD5 !important;
            background: linear-gradient(135deg, #B2EBF2, #E1F5FE) !important; /* More noticeable hover color */
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # 
    # Create columns for buttons             background: linear-gradient(135deg, #B2EBF2, #E1F5FE) !important; /* More noticeable hover color */

    col1, col2, col3, col4, col5 = st.columns(5, gap="small")

    with col1:
        if st.button(":material/home: Home", use_container_width=True, key="home_btn"):
            st.switch_page("Home.py")

    with col2:
        if st.button(":material/baby_changing_station: Feeding", use_container_width=True, key="feed_btn"):
            st.switch_page("pages/1_Feed.py")

    with col3:
        if st.button(":material/sanitizer: Infection", use_container_width=True, key="infection_btn"):
            st.switch_page("pages/2_Infection.py")

    with col4:
        if st.button(":material/nutrition: Nutrition", use_container_width=True, key="nutrition_btn"):
            st.switch_page("pages/3_Nutrition.py")

    with col5:
        if st.button(":material/medical_services: Umbilical", use_container_width=True, key="umbilical_btn"):
            st.switch_page("pages/4_Umbilical.py")


