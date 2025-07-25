import streamlit as st
import google.generativeai as genai
import time
from navigation import render_navigation_buttons

st.set_page_config(page_title="Infant Nutrition", initial_sidebar_state="expanded")

# Custom CSS for professional nutrition page
st.markdown("""
<style>
    /* Page-specific styling */
    .nutrition-container {
        background: #F8FAFE;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border: 1px solid #E1E8ED;
        box-shadow: 0 2px 8px rgba(91, 155, 213, 0.08);
    }
    
    .nutrition-title {
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
st.markdown('<h1 class="nutrition-title">Infant Nutrition Assistant</h1>', unsafe_allow_html=True)

try:
    gemini_key = st.secrets["gemini_api_key"]["GEMINI_API_KEY"]
    genai.configure(api_key=gemini_key)
except (KeyError, TypeError):
    st.error(":material/error: Gemini API key not found. Please set it in your Streamlit secrets.")
    st.stop()


# --- TRANSLATION FUNCTION ---
def translate_text(text, target_language):
    """
    Translates text to the target language using Gemini API.
    """
    if target_language == "English":
        return text
    
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        prompt = f"Translate the following text to {target_language}. Maintain all formatting, markdown syntax, and structure exactly as is:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text

# --- GEMINI PROMPT & MODEL CONFIGURATION (ENHANCED V4) ---
# This version enhances the "Helpful Resources" section to be age-adaptive,
# including links for feeding, habits, safety, and development.
SYSTEM_INSTRUCTION = """
You are a neonatal nutrition expert specialized in caring for neonates and infants, particularly in resource-limited settings. Your goal is to provide personalized, evidence-based nutrition guidance to support growth, immunity, and development for vulnerable infants.

You can respond in English or Hindi based on user preference. If responding in Hindi, use clear Devanagari script and maintain the same structured format.

Your response format MUST follow this exact structure, including the headings and delimiters:

###  Your Baby's Nutritional Snapshot
*A brief, 2-line summary of the infant's condition, nutritional risks, and priorities based on the provided data.*

[START_NUTRITION_GUIDE]
###  Key Nutrients for Growth
*Create a Markdown table with three columns: 'Nutrient', 'Recommended Amount', and 'Food Examples'. For 'Food Examples', list sources like breastmilk, specific types of formula, or fortified foods suitable for the infant's age. The 'Recommended Amount' column should have numeric figures per kg per day (e.g., 1.5-2.2 g/kg/day, 10 µg/day).*
[END_NUTRITION_GUIDE]

[START_RESOURCES]
###  Helpful Resources & Care Guides
*Create a Markdown bulleted list with links. **Crucially, tailor the resources to the infant's specific age group.**
- **For younger infants (0-4 months):** Focus on links for safe sleep practices (e.g., American Academy of Pediatrics), lactation support (WHO, La Leche League), and correct formula preparation.
- **For infants approaching solid foods (4-6+ months):** Include links to WHO/UNICEF guidelines on complementary feeding, information on first foods, and recognizing signs of readiness for solids.
- **For older infants (6-12 months):** Add resources for developmental milestones (CDC), baby-proofing the home for safety, and managing common issues like teething.
*Always prioritize reliable sources.*
[END_RESOURCES]

###  Your Gentle Feeding & Care Plan
*Offer a gentle, practical step-by-step plan. For each main point, use nested bullet points (indentation) for sub-steps or detailed explanations to make the plan easy to follow. Use a polite, supportive tone aimed at caregivers in low-resource settings, emphasizing feasible and impactful actions.*
"""

def get_gemini_response(prompt):
    """
    Sends a prompt to the Gemini model and returns the response.
    Handles chat history and potential errors.
    """
    try:
        messages = [
            {"role": m["role"], "parts": [m["content"]]}
            for m in st.session_state.messages
            if m["role"] != "system"
        ]
        model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=SYSTEM_INSTRUCTION)
        chat = model.start_chat(history=messages)
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}. This might be due to API rate limits or configuration issues.")
        time.sleep(5)
        st.rerun()
        return None

def display_formatted_response(response_text, language="English"):
    """
    Parses the model's response using delimiters and displays it in a
    multi-column layout with optional translation.
    """
    # Translate if needed
    if language == "Hindi":
        response_text = translate_text(response_text, "Hindi")
    
    nutrition_start_delim = "[START_NUTRITION_GUIDE]"
    nutrition_end_delim = "[END_NUTRITION_GUIDE]"
    resources_start_delim = "[START_RESOURCES]"
    resources_end_delim = "[END_RESOURCES]"

    if all(d in response_text for d in [nutrition_start_delim, nutrition_end_delim, resources_start_delim, resources_end_delim]):
        try:
            snapshot = response_text.split(nutrition_start_delim)[0]
            st.markdown(snapshot)

            nutrition_guide = response_text.split(nutrition_start_delim)[1].split(nutrition_end_delim)[0]
            resources = response_text.split(resources_start_delim)[1].split(resources_end_delim)[0]

            col1, col2 = st.columns([0.65, 0.35])
            with col1:
                st.markdown(nutrition_guide)
            with col2:
                st.markdown(resources)

            diet_plan = response_text.split(resources_end_delim)[1]
            st.markdown(diet_plan)
        except IndexError:
            st.markdown(response_text)
    else:
        st.markdown(response_text)

# --- UI & APP LOGIC ---
def nutrition_chatbot_page():
    """Main function to render the Streamlit page."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome! I am here to help with neonatal nutrition. \n\n**Please provide the infant's details in the sidebar to generate a personalized nutrition plan.**"}]

    with st.sidebar:
        st.title(":material/child_care: Infant's Details")
        st.caption("Provide as much information as you can for the best guidance.")
        
        # Language selection
        language = st.selectbox("Language / भाषा", ["English", "Hindi"], key="language")
        
        age = st.selectbox("Infant's Age", ["0-1 month", "1-2 months", "2-4 months", "4-6 months", "6-9 months", "9-12 months"], key="age")
        weight = st.number_input("Weight (in kg)", min_value=0.5, max_value=20.0, step=0.25, key="weight")
        gestational_age = st.number_input("Gestational Age at Birth (weeks, optional)", min_value=20, max_value=45, value=40, step=1, key="gestational_age", format="%d")
        feeding_method = st.selectbox("Current Feeding Method", ["Exclusive Breastfeeding", "Formula Feeding", "Mixed Feeding (Breastmilk + Formula)"], key="feeding_method")
        illnesses = st.text_area("Recent Illnesses (optional)", key="illnesses", placeholder="e.g., fever, diarrhea, jaundice")
        conditions = st.text_area("Other Medical Conditions (optional)", key="conditions", placeholder="e.g., born preterm, low birth weight")
        c1,c2,c3=st.columns([1,7,1])
        if c2.button(":material/pediatrics: Generate Nutrition Plan",use_container_width=True):
            gestational_age_text = 'Not specified' if gestational_age == 40 else f'{gestational_age} weeks'
            user_prompt = f"""
            Please provide neonatal nutrition guidance in {language} based on this information:
            - **Infant's Age:** {age}
            - **Weight:** {weight} kg
            - **Gestational Age at Birth:** {gestational_age_text}
            - **Feeding Method:** {feeding_method}
            - **Recent Illnesses:** {'None' if not illnesses else illnesses}
            - **Other Medical Conditions:** {'None' if not conditions else conditions}
            """
            st.session_state.messages.append({"role": "user", "content": "I've submitted the infant's details for a nutrition plan."})
            with st.spinner("Generating personalized guidance..."):
                response = get_gemini_response(user_prompt)
                if response:
                    st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
            
    #st.title(":material/nutrition: Infant Nutrition Guide")
    st.markdown("---")

    #st.write("This page will provide guidance on infant nutrition.")

    for message in st.session_state.messages:
        avatar = ":material/child_care:" if message["role"] == "assistant" else ":material/person:"
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "assistant":
                display_formatted_response(message["content"], st.session_state.get("language", "English"))
            else:
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask a follow-up question..."):
        # Add language instruction if Hindi is selected
        if st.session_state.get("language", "English") == "Hindi":
            translated_prompt = f"Please respond in Hindi: {prompt}"
        else:
            translated_prompt = prompt
            
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=":material/person:"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar=":material/child_care:"):
            with st.spinner("Thinking..."):
                response = get_gemini_response(translated_prompt)
                if response:
                    display_formatted_response(response, st.session_state.get("language", "English"))
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.warning("Sorry, I couldn't get a response. Please try again.")

if __name__ == "__main__":
    nutrition_chatbot_page()
