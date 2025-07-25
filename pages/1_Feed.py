import streamlit as st
import google.generativeai as genai
import time
import re
from navigation import render_navigation_buttons

# --- PAGE CONFIG ---
st.set_page_config(page_title="Feeding Assistant", initial_sidebar_state="expanded")

# Custom CSS for professional feeding page
st.markdown("""
<style>
    /* Page-specific styling */
    .feeding-container {
        background: #F8FAFE;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border: 1px solid #E1E8ED;
        box-shadow: 0 2px 8px rgba(91, 155, 213, 0.08);
    }
    
    .feeding-title {
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
st.markdown('<h1 class="feeding-title">Feeding Care Assistant</h1>', unsafe_allow_html=True)

# --- CONFIGURATION ---
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

# --- GEMINI PROMPT & MODEL CONFIGURATION (Breastfeeding Focus) ---
# This prompt is redesigned to make the AI a lactation expert. It asks for specific,
# actionable advice on latching, feeding plans, and troubleshooting, citing authoritative sources.
SYSTEM_INSTRUCTION = """
You are a Breastfeeding and Lactation Support AI, an expert dedicated to helping mothers successfully breastfeed their infants. Your tone is empathetic, supportive, and clear. Your goal is to provide practical, evidence-based guidance, especially for mothers in resource-limited settings.

You can respond in English or Hindi based on user preference. If responding in Hindi, use clear Devanagari script and maintain the same structured format.

Your response format MUST follow this exact structure, including the headings and delimiters:

###  Your Breastfeeding Snapshot
*A brief, 2-line summary of the current situation, identifying the main challenge and the primary goal based on the user's input.*

[START_FEEDING_PLAN]
###  Your Gentle Feeding Plan
*Create a step-by-step feeding plan. Use nested bullet points for clarity. Focus on demand feeding, watching for hunger cues (e.g., rooting, hand-to-mouth), and ensuring the baby feeds from at least one breast fully. Mention the importance of feeding 8-12 times in 24 hours for newborns.*
[END_FEEDING_PLAN]

[START_TROUBLESHOOTING]
###  Latching & Comfort Guide
*Create a Markdown table with two columns: 'Common Challenge' and 'Suggested Technique'.
- Address issues provided by the user (e.g., sore nipples, baby seems fussy).
- For sore nipples, suggest checking the latch (asymmetrical, wide mouth).
- For a fussy baby, suggest skin-to-skin contact to calm the baby and different feeding positions (e.g., cross-cradle, football hold).
- Provide a link to a reliable video on proper latching from a source like WHO or UNICEF.*
[END_TROUBLESHOOTING]

[START_RESOURCES]
###  Helpful Breastfeeding Resources
*Create a Markdown bulleted list with links to authoritative sources.
- **La Leche League International:** For comprehensive mother-to-mother support and articles.
- **World Health Organization (WHO):** For guidelines on breastfeeding and infant health.
- **UNICEF:** For resources on infant nutrition and mother-child wellbeing.
- Include a link to a resource for tracking diaper output (6+ wet diapers a day is a good sign of sufficient intake).*
[END_RESOURCES]
"""

def get_gemini_response(prompt):
    """
    Sends a prompt to the Gemini model and returns the response.
    Handles chat history and potential errors.
    """
    try:
        # Construct messages from session state for context
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
    Parses the model's response using custom delimiters and displays it in a
    structured layout with optional translation.
    """
    # Translate if needed
    if language == "Hindi":
        response_text = translate_text(response_text, "Hindi")
    
    plan_start = "[START_FEEDING_PLAN]"
    plan_end = "[END_FEEDING_PLAN]"
    trouble_start = "[START_TROUBLESHOOTING]"
    trouble_end = "[END_TROUBLESHOOTING]"
    res_start = "[START_RESOURCES]"
    res_end = "[END_RESOURCES]"

    # Check if all delimiters are present in the response
    if all(d in response_text for d in [plan_start, plan_end, trouble_start, trouble_end, res_start, res_end]):
        try:
            # Parse the response text into sections
            snapshot = response_text.split(plan_start)[0]
            feeding_plan = response_text.split(plan_start)[1].split(plan_end)[0]
            troubleshooting = response_text.split(trouble_start)[1].split(trouble_end)[0]
            resources = response_text.split(res_start)[1].split(res_end)[0]

            st.markdown(snapshot)

            col1, col2 = st.columns([0.6, 0.4])
            with col1:
                st.markdown(feeding_plan)
                st.markdown(resources)
            with col2:
                st.markdown(troubleshooting)

        except IndexError:
            # Fallback for parsing errors
            st.markdown(response_text)
    else:
        # If delimiters are missing, display the raw response
        st.markdown(response_text)

# --- UI & APP LOGIC ---
def breastfeeding_chatbot_page():
    """Main function to render the Breastfeeding Assistant Streamlit page."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome! I am your personal feeding assistant. \n\n**Please tell me about your breastfeeding journey in the sidebar so I can help.**"}]

    # The sidebar is updated to gather breastfeeding-specific information.
    with st.sidebar:
        st.title(":material/baby_changing_station: Feeding Details")
        st.caption("The more details you share, the better I can assist you.")
        
        # Language selection
        language = st.selectbox("Language / भाषा", ["English", "Hindi"], key="language")
        
        age = st.selectbox("Baby's Age", ["0-1 week", "1-4 weeks", "1-3 months", "3-6 months", "6+ months"], key="age")
        concerns = st.text_area("What are your main concerns?", key="concerns", placeholder="e.g., My nipples are sore, I'm worried my baby isn't getting enough milk.")
        latching = st.selectbox("How is the baby's latch?", ["Seems good", "Painful for me", "Baby seems to slip off", "Unsure"], key="latching")
        feeding_frequency = st.slider("How many times does the baby feed in 24 hours?", 1, 20, 8, key="feeding_frequency")
        diaper_output = st.selectbox("How many wet diapers in the last 24 hours?", ["1-2", "3-5", "6 or more"], key="diapers")
        
        c1,c2,c3 = st.columns([1,7,1])
        if c2.button(":material/child_care: Get Feeding Plan", use_container_width=True):
            # The user prompt is tailored to send the new inputs to the AI.
            user_prompt = f"""
            Please provide breastfeeding guidance in {language} based on this information:
            - **Baby's Age:** {age}
            - **Mother's Main Concerns:** {concerns if concerns else "Not specified"}
            - **Baby's Latch Quality:** {latching}
            - **Feeding Frequency:** {feeding_frequency} times per 24 hours
            - **Wet Diapers:** {diaper_output} in the last 24 hours
            """
            st.session_state.messages.append({"role": "user", "content": "I've submitted my breastfeeding details for a personalized plan."})
            with st.spinner("Creating your personalized plan..."):
                response = get_gemini_response(user_prompt)
                if response:
                    st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    #st.title(":material/breastfeeding: Breastfeeding Assistant AI")
    st.markdown("---")

    # Display the chat history
    for message in st.session_state.messages:
        avatar = ":material/support_agent:" if message["role"] == "assistant" else ":material/person:"
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "assistant":
                display_formatted_response(message["content"], st.session_state.get("language", "English"))
            else:
                st.markdown(message["content"])

    # Handle follow-up questions from the user
    if prompt := st.chat_input("Ask a follow-up question..."):
        # Translate user input if in Hindi
        if st.session_state.get("language", "English") == "Hindi":
            translated_prompt = f"Respond in Hindi: {prompt}"
        else:
            translated_prompt = prompt
            
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=":material/person:"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar=":material/support_agent:"):
            with st.spinner("Thinking..."):
                response = get_gemini_response(translated_prompt)
                if response:
                    display_formatted_response(response, st.session_state.get("language", "English"))
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.warning("Sorry, I couldn't get a response. Please try again.")

breastfeeding_chatbot_page()

