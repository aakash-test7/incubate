import streamlit as st
from navigation import render_navigation_buttons
from footer import render_footer

st.set_page_config(
    page_title="Incubate2025 - Neonatal Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional, subtle neonatal care design
st.markdown("""
<style>
    /* Main page styling */
    .main-container {
        background: linear-gradient(135deg, #FAFBFC 0%, #F0F4F8 100%);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid rgba(91, 155, 213, 0.1);
    }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(45deg, #5B9BD5, #7FB8E6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin: 30px 0;
    }
    
    /* Welcome section */
    .welcome-section {
        background: #F8FAFE;
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0;
        border: 1px solid #E1E8ED;
        box-shadow: 0 2px 8px rgba(91, 155, 213, 0.08);
    }
    
    /* Feature cards */
    .feature-card {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border: 1px solid #E1E8ED;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(91, 155, 213, 0.12);
    }
    
    /* Text styling */
    .home-text {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #2C3E50;
        text-align: left;
    }
    
    .section-header {
        color: #5B9BD5;
        font-size: 1.6rem;
        font-weight: 600;
        margin: 15px 0 10px 0;
        text-align: center;
    }
    
    /* Info box styling */
    .stAlert {
        border-radius: 10px !important;
        border: 1px solid #5B9BD5 !important;
        background: #F8FAFE !important;
    }
</style>
""", unsafe_allow_html=True)

render_navigation_buttons()

# Main content in a clean container
#st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Professional title
st.markdown('<h1 class="main-title">NEONATAL DASHBOARD</h1>', unsafe_allow_html=True)

# Welcome section
st.markdown("""
<div class="welcome-section">
    <h2 class="section-header"> Your Personal Neonatal Care Assistant </h2>
    <p class="home-text">
        This application is designed to provide guidance on key aspects of neonatal care, 
        especially for parents in resource-limited settings. Our goal is to empower you with 
        evidence-based information to help your newborn thrive in their most critical early days.
    </p>
</div>
""", unsafe_allow_html=True)

# Feature cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #5B9BD5; text-align: center;"> Feeding Guidance</h3>
        <p class="home-text">Get personalized breastfeeding advice, feeding schedules, and troubleshooting tips for common challenges.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #7FB8E6; text-align: center;"> Nutrition Support</h3>
        <p class="home-text">Receive tailored nutritional recommendations to ensure optimal growth and development for your baby.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #5B9BD5; text-align: center;"> Infection Prevention</h3>
        <p class="home-text">Learn essential hygiene practices and early warning signs to keep your newborn safe and healthy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3 style="color: #7FB8E6; text-align: center;"> Umbilical Care</h3>
        <p class="home-text">Get expert guidance on proper umbilical cord care and monitoring for potential complications.</p>
    </div>
    """, unsafe_allow_html=True)

# Navigation info
st.markdown("""
<div class="welcome-section">
    <p class="home-text" style="text-align: center; font-size: 1.2rem;">
        Navigate through the different sections using the buttons at the top of the page to get 
        personalized advice on feeding, infection prevention, nutrition, and umbilical care.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Professional info message
#st.info(" Select a care guide from the navigation buttons above to get started on your neonatal care journey!", icon="ℹ️")

render_footer()

