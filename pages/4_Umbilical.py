import streamlit as st
import google.generativeai as genai
from PIL import Image
from navigation import render_navigation_buttons

st.set_page_config(page_title="Umbilical Cord Assistant", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for professional umbilical care page
st.markdown("""
<style>
    /* Page-specific styling */
    .umbilical-container {
        background: #F8FAFE;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border: 1px solid #E1E8ED;
        box-shadow: 0 2px 8px rgba(91, 155, 213, 0.08);
    }
    
    .umbilical-title {
        color: #5B9BD5;
        text-align: center;
        font-size: 2.2rem;
        font-weight: 600;
        margin: 20px 0;
    }
    
    /* Upload area styling */
    .stFileUploader {
        background: #FFFFFF !important;
        border: 2px dashed #5B9BD5 !important;
        border-radius: 8px !important;
        padding: 15px !important;
    }
    
    .stFileUploader label {
        color: #5B9BD5 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Checkbox styling */
    .stCheckbox label {
        color: #5B9BD5 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Analysis button */
    .stButton > button {
        background: #5B9BD5 !important;
        color: white !important;
        border: 1px solid #5B9BD5 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 12px 25px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(91, 155, 213, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(91, 155, 213, 0.25) !important;
        background: #4A90E2 !important;
    }
    
    /* Section headers */
    .section-header {
        color: #5B9BD5;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 20px 0 12px 0;
        border-bottom: 1px solid #E1E8ED;
        padding-bottom: 5px;
    }
    
    /* Results container */
    .results-container {
        background: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E1E8ED;
        margin: 15px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
</style>
""", unsafe_allow_html=True)

render_navigation_buttons()

# Professional title
st.markdown('<h1 class="umbilical-title">Umbilical Care Assistant</h1>', unsafe_allow_html=True)

try:
    # Per your request: gemini_key = st.secrets["gemini_api_key"]["GEMINI_API_KEY"]
    gemini_key = st.secrets["gemini_api_key"]["GEMINI_API_KEY"]
    genai.configure(api_key=gemini_key)
except (KeyError, TypeError):
    st.error(":material/error: Gemini API key not found. Please set it in your Streamlit secrets.")
    st.stop()

# --- GEMINI PROMPT & MODEL CONFIGURATION ---
# This system prompt is expertly crafted to guide the Gemini model to act as a
# neonatal specialist. It focuses on analyzing an umbilical cord image and related
# symptoms to provide a detailed and structured risk assessment for omphalitis.
SYSTEM_INSTRUCTION = """
You are an expert AI medical assistant specializing in neonatology and pediatric care. Your primary function is to analyze an image of a neonatal umbilical cord along with user-reported symptoms to identify potential signs of omphalitis (infection).

**Analysis Objective:**
Your analysis must be based on a comparison between the provided image and symptoms against the known characteristics of a healthy, healing umbilical cord versus an infected one.

**Input Data (will be provided):**
1.  An image of the umbilical cord.
2.  A list of symptoms checked by the user (e.g., discoloration, odor, swelling, discharge).
3.  Any other text observations from the user.

**Mandatory Output Format:**
Your entire response must be in Markdown and follow this exact structure. Do not deviate from these headings.

### :material/medical_services: Umbilical Cord Health Assessment

**1. Risk Assessment:**
* **Risk Level:** (State one: `Low Risk`, `Moderate Risk`, or `High Risk` of infection).
* **Summary:** (Provide a concise, one-sentence summary of your findings that justifies the risk level.)

**2. Visual Analysis of the Image:**
* **Cord Stump:** (Describe the appearance of the cord itself—e.g., "The cord appears dry and is detaching normally," or "The cord looks moist and discolored.")
* **Surrounding Skin:** (Describe the skin around the navel—e.g., "The skin at the base of the cord is a normal skin tone," or "There is significant redness and swelling extending onto the abdomen.")
* **Signs of Concern:** (Explicitly list any visual signs that are concerning for infection, such as pus, extensive redness, or streaks.)

**3. Symptom Analysis:**
* (Analyze the user-provided symptoms. For each reported symptom, explain its clinical significance. For example: "The reported **foul odor** is a strong indicator of a bacterial infection.")

**4. Recommended Actions:**
* (Provide a clear, bulleted list of next steps. Be direct and prioritize safety.)
* **For High/Moderate Risk:** Advise immediate consultation with a healthcare professional (e.g., "Seek medical attention from a pediatrician or visit an urgent care clinic within the next few hours.").
* **For Low Risk:** Suggest routine care and monitoring (e.g., "Continue to keep the area clean and dry. Monitor for any changes such as redness, swelling, or discharge.").
* **General Care Tip:** Always include a tip on proper cord care, like "Ensure the diaper is folded below the cord to allow it to air dry."
"""

def get_gemini_response(prompt_text, image):
    """
    Sends a prompt and an image to the Gemini Pro Vision model for analysis.
    """
    if not image:
        return "Please upload an image for analysis."
    
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    try:
        # The content payload must be a list containing the text prompt and the image
        response = model.generate_content([prompt_text, image])
        return response.text
    except Exception as e:
        st.error(f"An error occurred during the API call: {e}")
        return "Analysis failed. Please ensure the uploaded image is in a standard format (JPG, PNG) and try again."

# --- UI & APP LOGIC ---
def umbilical_cord_analyzer_app():
    """Main function to render the Streamlit page."""

    #st.title(":material/healing: Umbilical Cord Care Guide")
    st.markdown("---")

    #st.write("This page will provide guidance on proper umbilical cord care.")
    st.warning(
        "**Disclaimer:** This tool is for informational and clinical decision support purposes only. It is **not a substitute for professional medical diagnosis**. Always consult a qualified healthcare provider for any health concerns."
    )

    # --- INPUT SECTION (Sidebar) ---
    with st.sidebar:
        st.header("1. Upload Image")
        uploaded_image = st.file_uploader(
            "Upload a clear image of the umbilical cord area.",
            type=["jpg", "png", "jpeg"]
        )

        st.header("2. Report Symptoms")
        symptom_redness = st.checkbox("Redness or Discoloration around the cord")
        symptom_odor = st.checkbox("Foul Odor from the cord")
        symptom_swelling = st.checkbox("Swelling or Puffiness of the skin")
        symptom_discharge = st.checkbox("Pus or Yellow/Green Discharge")
        other_observations = st.text_area("Other Observations (optional)")

    # --- ANALYSIS & OUTPUT SECTION (Main Page) ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Uploaded Image")
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Image of the umbilical cord for analysis.", use_container_width=True)
        else:
            st.info("Please upload an image using the sidebar to begin the analysis.")

    with col2:
        st.subheader("AI-Powered Analysis")
        if st.button(":material/science: Analyze Cord Health", disabled=not uploaded_image):
            with st.spinner("The AI is analyzing the image and symptoms..."):
                # Constructing the detailed prompt for the AI
                symptoms_list = []
                if symptom_redness: symptoms_list.append("Redness/Discoloration")
                if symptom_odor: symptoms_list.append("Foul Odor")
                if symptom_swelling: symptoms_list.append("Swelling/Puffiness")
                if symptom_discharge: symptoms_list.append("Pus/Discharge")

                prompt = f"""
                Please analyze the uploaded image of a neonatal umbilical cord based on the following reported symptoms and provide a health assessment.

                **Reported Symptoms:** {', '.join(symptoms_list) if symptoms_list else "None reported."}
                **Other Observations:** {other_observations if other_observations else "None."}
                """

                # Calling the Gemini API with the prompt and image
                response_text = get_gemini_response(prompt, image)
                st.markdown(response_text)
        else:
            st.info("Click the 'Analyze Cord Health' button after uploading an image.")


if __name__ == "__main__":
    umbilical_cord_analyzer_app()

