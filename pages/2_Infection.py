import streamlit as st
import google.generativeai as genai
from PIL import Image
from navigation import render_navigation_buttons

st.set_page_config(page_title="Infection Prevention", initial_sidebar_state="collapsed")

# Custom CSS for professional infection prevention page
st.markdown("""
<style>
    /* Page-specific styling */
    .infection-container {
        background: #F8FAFE;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border: 1px solid #E1E8ED;
        box-shadow: 0 2px 8px rgba(91, 155, 213, 0.08);
    }
    
    .infection-title {
        color: #5B9BD5;
        text-align: center;
        font-size: 2.2rem;
        font-weight: 600;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

render_navigation_buttons()

# Professional title
st.markdown('<h1 class="infection-title">Infection Prevention Assistant</h1>', unsafe_allow_html=True)

# --- GEMINI PROMPT & MODEL CONFIGURATION ---
# This detailed system prompt guides the AI to function as a medical expert.
# It explicitly asks the AI to identify probable causes, including bacterial,
# viral, and fungal infections, directly addressing the need to cover "neonatal infections."
SYSTEM_INSTRUCTION = """
You are an expert medical AI assistant specializing in neonatology. Your function is to assist healthcare professionals in the early identification of neonatal sepsis and septic shock based on clinical data and medical images.

**Analysis Objective:**
Analyze the provided clinical signs, lab results, and any uploaded images to assess the risk for neonatal sepsis or shock. Use established clinical reasoning patterns (like those informing nSOFA scores) to guide your analysis.

**Input Data (will be provided in a structured format):**
- Clinical and Vital Signs
- Laboratory/Diagnostic Parameters
- Optional Medical Images (umbilical cord, skin, chest X-ray)

**AI-Powered Diagnostic Logic:**
1.  **Synthesize Data:** Analyze all inputs to identify patterns indicative of infection or shock.
2.  **Risk Stratification:** Clearly state the risk level for neonatal sepsis or septic shock.
3.  **Differential Diagnosis:** Suggest probable causes (e.g., bacterial, fungal, viral) and types of shock (hypovolemic, cardiogenic, septic). This covers the requirement to identify various neonatal infections.
4.  **Image Analysis (if provided):** If an image is uploaded, describe your findings. Look for visual signs of omphalitis (redness, discharge from umbilical stump), pneumonia (infiltrates on X-ray), or sepsis-related rashes (pustules, petechiae).

**Mandatory Output Format:**
Your entire response must be in Markdown.

### 🏥 AI-Powered Sepsis Risk Assessment

**1. Risk Summary & Probable Cause:**
* **Risk Level:** (e.g., `High Risk`, `Moderate Risk`, `Low Risk`).
* **Summary:** (A concise, one-sentence summary of findings, e.g., "High suspicion of early-onset neonatal sepsis based on tachycardia, temperature instability, and elevated CRP.")
* **Probable Cause:** (Suggest likely pathogens or conditions, e.g., "Bacterial sepsis (GBS, E. coli), consider viral causes.")

**2. Abnormal Parameters:**
*Create a Markdown table listing only the parameters that are outside the normal range for the infant's age and weight, along with their values.*
| Parameter | Value | Normal Range (for context) |
|---|---|---|
| Heart Rate | 185 bpm | 110-160 bpm |
| CRP | 25 mg/L | < 10 mg/L |

**3. Suggested Clinical Actions & Monitoring:**
*Provide a bulleted list of recommended next steps.*
* (e.g., "Consider obtaining blood, urine, and CSF cultures.")
* (e.g., "Recommend starting empirical antibiotic therapy as per unit protocol.")
* (e.g., "Closely monitor vital signs, urine output, and perfusion status.")

**4. Image Analysis (if applicable):**
*If an image was analyzed, provide a heading and your interpretation.*
**Image Interpretation:**
* (e.g., "The umbilical cord image shows significant periumbilical erythema and purulent discharge, consistent with omphalitis.")
"""

def get_gemini_response(prompt_text, images):
    """
    Sends a prompt with optional images to the Gemini model and returns the response.
    """
    if not prompt_text:
        return "Please fill in the clinical data to get an analysis."

    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    # The content payload must be a list
    content = [SYSTEM_INSTRUCTION, prompt_text]
    if images:
        for img in images.values():
            content.append(img)
            
    try:
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        st.error(f"An error occurred during API call: {e}")
        return None

def clinic_page():
    st.subheader("A. Clinical and Vital Signs")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Infant Age (days)", min_value=0, max_value=90, value=7, step=1)
        birth_weight = st.number_input("Birth Weight (kg)", min_value=0.5, max_value=10.0, value=3.0, step=0.1)
        current_weight = st.number_input("Current Weight (kg)", min_value=0.5, max_value=10.0, value=3.1, step=0.1)
        gestational_age = st.number_input("Gestational Age at Birth (weeks)", min_value=22, max_value=45, value=40, step=1)
        feeding_status = st.selectbox("Feeding Status", ["Exclusive Breastfeeding", "Mixed Feeding", "Formula-fed"])
    with col2:
        temperature = st.number_input("Temperature (°C)", min_value=34.0, max_value=42.0, value=37.5, step=0.1)
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=50, max_value=250, value=160, step=1)
        resp_rate = st.number_input("Respiratory Rate (breaths/min)", min_value=10, max_value=100, value=50, step=1)
        cap_refill = st.number_input("Capillary Refill Time (seconds)", min_value=1, max_value=10, value=2, step=1)
        skin_perfusion = st.selectbox("Skin Perfusion/Mottling", ["Normal", "Pale", "Mottled", "Cyanotic"])
    with col3:
        lethargy = st.checkbox("Lethargy or Irritability")
        urine_output = st.number_input("Urine Output (ml/kg/hr)", min_value=0.0, max_value=10.0, value=1.5, step=0.1)
        spo2 = st.number_input("Oxygen Saturation (SpO2 %)", min_value=70, max_value=100, value=98, step=1)
        bp_systolic = st.number_input("Blood Pressure - Systolic (mmHg, optional)", min_value=0, max_value=150, value=70, step=1)
        bp_diastolic = st.number_input("Blood Pressure - Diastolic (mmHg, optional)", min_value=0, max_value=100, value=40, step=1)
    
    # Store in session state
    st.session_state.clinical_data = {
        'age': age, 'birth_weight': birth_weight, 'current_weight': current_weight,
        'gestational_age': gestational_age, 'feeding_status': feeding_status,
        'temperature': temperature, 'heart_rate': heart_rate, 'resp_rate': resp_rate,
        'cap_refill': cap_refill, 'skin_perfusion': skin_perfusion, 'lethargy': lethargy,
        'urine_output': urine_output, 'spo2': spo2, 'bp_systolic': bp_systolic,
        'bp_diastolic': bp_diastolic
    }

def lab_page():
    st.subheader("B. Lab/Diagnostic Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        ph = st.number_input("Blood pH", min_value=6.8, max_value=7.8, value=7.35, step=0.01)
        lactate = st.number_input("Lactate (mmol/L)", min_value=0.0, max_value=20.0, value=1.5, step=0.1)
        crp = st.number_input("CRP (C-reactive protein, mg/L)", min_value=0, max_value=300, value=5, step=1)
    with col2:
        wbc = st.number_input("WBC Count (x10^9/L)", min_value=0, max_value=50, value=10, step=1)
        platelets = st.number_input("Platelet Count (x10^9/L)", min_value=0, max_value=600, value=250, step=1)
        blood_culture = st.selectbox("Blood Culture Result", ["Not Available", "Pending", "No Growth", "Growth Detected"])
    with col3:
        procalcitonin = st.number_input("Procalcitonin (ng/mL, optional)", min_value=0.0, max_value=100.0, value=0.5, step=0.1)
        glucose = st.number_input("Glucose (mg/dL)", min_value=0, max_value=500, value=90, step=1)
    
    # Store in session state
    st.session_state.lab_data = {
        'ph': ph, 'lactate': lactate, 'crp': crp, 'wbc': wbc,
        'platelets': platelets, 'blood_culture': blood_culture,
        'procalcitonin': procalcitonin, 'glucose': glucose
    }

def image_page():
    st.subheader("C. Upload Images (Optional)")
    uploaded_umbilical = st.file_uploader("Upload Umbilical Cord Image", type=["jpg", "png", "jpeg"])
    uploaded_skin = st.file_uploader("Upload Skin Rash/Pustule Image", type=["jpg", "png", "jpeg"])
    uploaded_xray = st.file_uploader("Upload Chest X-ray Image", type=["jpg", "png", "jpeg"])
    
    # Store in session state
    st.session_state.image_data = {
        'uploaded_umbilical': uploaded_umbilical,
        'uploaded_skin': uploaded_skin,
        'uploaded_xray': uploaded_xray
    }

# --- UI & APP LOGIC ---
def sepsis_detector_app():
    """Main function to render the Streamlit page."""

    #st.title(":material/sanitizer: Infection Prevention Guide")
    st.markdown("---")

    #st.write("This page will provide guidance on preventing infections in newborns.")

    # Per your request, a disclaimer is included to ensure responsible use.
    st.warning(
        "**Disclaimer:** This is a clinical decision support tool. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified health provider."
    )

    # Use session state to store the response for a smoother user experience
    if 'response' not in st.session_state:
        st.session_state.response = ""

    # --- INPUT SECTION ---
    # The UI is organized into tabs for clarity, as suggested.
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = ''
    
    def set_active_tab(tab_name):
        st.session_state.active_tab = tab_name

    with st.expander("Enter Patient Data and Upload Images", expanded=True):
        col1, col2, col3 = st.columns(3)
        if col1.button("Clinical & Vital Signs", key="btn_A",use_container_width=True):
            set_active_tab('CLINIC')
            st.rerun()
        if col2.button("Lab Parameters", key="btn_B",use_container_width=True):
            set_active_tab('LAB')
            st.rerun()
        if col3.button("Image Uploads", key="btn_C",use_container_width=True):
            set_active_tab('IMAGE')
            st.rerun()
    
    # Display content based on active tab
    if st.session_state.active_tab == 'CLINIC':
        clinic_page()
    elif st.session_state.active_tab == 'LAB':
        lab_page()
    elif st.session_state.active_tab == 'IMAGE':
        image_page()

    # --- ANALYSIS BUTTON ---
    c1,c2,c3=st.columns([1, 1, 1])
    if c2.button(":material/stethoscope: Analyze Patient Data", type="primary",use_container_width=True):
        # Check if data exists in session state
        if 'clinical_data' not in st.session_state or 'lab_data' not in st.session_state:
            st.error("Please fill in all required data in Clinical and Lab tabs before analysis.")
            return
            
        with st.spinner("AI is analyzing the data... Please wait."):
            # Get data from session state
            clinical = st.session_state.clinical_data
            lab = st.session_state.lab_data
            images_data = st.session_state.get('image_data', {})
            
            # Format the text prompt with all the patient data
            prompt = f"""
            Analyze the following neonatal data for signs of sepsis or shock:

            **A. Clinical and Vital Signs:**
            - Infant Age: {clinical['age']} days
            - Birth Weight: {clinical['birth_weight']} kg
            - Current Weight: {clinical['current_weight']} kg
            - Gestational Age: {clinical['gestational_age']} weeks
            - Feeding Status: {clinical['feeding_status']}
            - Temperature: {clinical['temperature']} °C
            - Heart Rate: {clinical['heart_rate']} bpm
            - Respiratory Rate: {clinical['resp_rate']} breaths/min
            - Capillary Refill Time: {clinical['cap_refill']} seconds
            - Skin Perfusion: {clinical['skin_perfusion']}
            - Lethargy/Irritability: {'Yes' if clinical['lethargy'] else 'No'}
            - Urine Output: {clinical['urine_output']} ml/kg/hr
            - SpO2: {clinical['spo2']}%
            - Blood Pressure: {clinical['bp_systolic']}/{clinical['bp_diastolic']} mmHg

            **B. Lab/Diagnostic Parameters:**
            - Blood pH: {lab['ph']}
            - Lactate: {lab['lactate']} mmol/L
            - CRP: {lab['crp']} mg/L
            - WBC Count: {lab['wbc']} x10^9/L
            - Platelet Count: {lab['platelets']} x10^9/L
            - Blood Culture: {lab['blood_culture']}
            - Procalcitonin: {lab['procalcitonin']} ng/mL
            - Glucose: {lab['glucose']} mg/dL
            """

            # Prepare images for the API call
            images = {}
            if images_data.get('uploaded_umbilical'):
                images['umbilical'] = Image.open(images_data['uploaded_umbilical'])
            if images_data.get('uploaded_skin'):
                images['skin'] = Image.open(images_data['uploaded_skin'])
            if images_data.get('uploaded_xray'):
                images['xray'] = Image.open(images_data['uploaded_xray'])

            # Get response from Gemini
            st.session_state.response = get_gemini_response(prompt, images)

    # --- OUTPUT SECTION ---
    if st.session_state.response:
        st.markdown("---")
        st.subheader("Analysis Results")

        col1, col2 = st.columns([0.6, 0.4])

        with col1:
            st.markdown(st.session_state.response)

        with col2:
            images_data = st.session_state.get('image_data', {})
            if images_data.get('uploaded_umbilical'):
                st.image(images_data['uploaded_umbilical'], caption="Uploaded Umbilical Image", use_container_width=True)
            if images_data.get('uploaded_skin'):
                st.image(images_data['uploaded_skin'], caption="Uploaded Skin Image", use_container_width=True)
            if images_data.get('uploaded_xray'):
                st.image(images_data['uploaded_xray'], caption="Uploaded Chest X-ray", use_container_width=True)


if __name__ == "__main__":
    sepsis_detector_app()
                