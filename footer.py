import streamlit as st

def render_footer():
    """
    Renders a professional, subtle footer with neonatal care theme.
    """
    footer_html = """
    <style>
        .center-title {
            text-align: center;
            margin-top: 0;
        }
        .center-heading {
            text-align: center;
        }
        .footer {
            background: #E8F4FF;
            color: #2C3E50;
            text-align: center;
            padding: 1.5rem 0;
            margin-top: 3rem;
            border-radius: 12px;
            border: 1px solid #E1E8ED;
            box-shadow: 0 2px 8px rgba(91, 155, 213, 0.08);
        }
        
        .footer-text {
            font-size: 1.5rem;
            font-weight: 600;
            color: #5B9BD5;
            margin: 0;
        }
        
        .footer-tagline {
            font-size: 0.9rem;
            color: #666;
            margin-top: 8px;
            font-style: italic;
        }
    </style>
    <div class="footer">
        <div class="footer-text">© INCUBATE 2025</div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

