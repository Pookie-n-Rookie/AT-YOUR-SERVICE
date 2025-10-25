import streamlit as st
import requests
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

# Page config
st.set_page_config(
    page_title="AT YOUR SERVICE",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🤖"
)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark background for main app */
    .main {
        background-color: #0e1117;
        color: #ffffff;
        padding-top: 1rem;
    }
    
    /* Sidebar dark theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d29 0%, #0e1117 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1rem;
    }
    
    /* Header styling with vibrant gradient */
    .main-header {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 50%, #f107a3 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(123, 47, 247, 0.4);
        animation: gradient 3s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Input areas - white with black text and VISIBLE CURSOR */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        caret-color: #000000 !important;
        border-radius: 15px !important;
        border: 2px solid #7b2ff7 !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease;
        font-family: 'Arial', sans-serif !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #666666 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.3) !important;
        outline: none !important;
    }
    
    /* Remove extra spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    
    /* Button styling with gradient */
    div.stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        color: white;
        height: 60px;
        width: 100%;
        font-size: 1.2rem;
        font-weight: 700;
        border-radius: 15px;
        border: none;
        box-shadow: 0 6px 25px rgba(0, 212, 255, 0.5);
        transition: all 0.3s ease;
        margin-top: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 35px rgba(123, 47, 247, 0.7);
        background: linear-gradient(135deg, #7b2ff7 0%, #f107a3 100%);
    }
    
    div.stButton > button:active {
        transform: translateY(0);
    }
    
    /* Response box - dark with neon border */
    .response-box {
        background: linear-gradient(145deg, #1a1d29 0%, #262b3d 100%);
        color: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #7b2ff7;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(123, 47, 247, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        line-height: 1.8;
        font-size: 1.05rem;
    }
    
    /* Chat history item */
    .chat-item {
        background: linear-gradient(145deg, #1a1d29 0%, #262b3d 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 4px solid #00d4ff;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .chat-query {
        color: #00d4ff;
        font-weight: 600;
        margin-bottom: 0.8rem;
        font-size: 1.05rem;
    }
    
    .chat-response {
        color: #ffffff;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* Radio buttons styling */
    .stRadio {
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .stRadio > label {
        font-weight: 700;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stRadio > div {
        background: linear-gradient(145deg, #1a1d29 0%, #262b3d 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #7b2ff7;
        box-shadow: 0 4px 15px rgba(123, 47, 247, 0.3);
    }
    
    .stRadio label {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        padding: 0.5rem !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.2s ease !important;
        border-radius: 8px !important;
    }
    
    .stRadio label:hover {
        background: rgba(123, 47, 247, 0.2) !important;
        padding-left: 0.8rem !important;
    }
    
    .stRadio input[type="radio"] {
        accent-color: #00d4ff !important;
        width: 18px !important;
        height: 18px !important;
        margin-right: 0.5rem !important;
    }
    
    .stRadio input[type="radio"]:checked + label {
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.3) 0%, transparent 100%) !important;
        border-left: 3px solid #00d4ff !important;
        font-weight: 700 !important;
    } - dark theme */
    [data-baseweb="menu"] {
        background-color: #1a1d29 !important;
        border: 2px solid #7b2ff7 !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 32px rgba(123, 47, 247, 0.5) !important;
        padding: 0.5rem 0 !important;
    }
    
    /* Dropdown options */
    [data-baseweb="menu"] li {
        background-color: transparent !important;
        color: #ffffff !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        border-left: 3px solid transparent !important;
        margin: 0.25rem 0.5rem !important;
        border-radius: 8px !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background: linear-gradient(90deg, rgba(123, 47, 247, 0.3) 0%, transparent 100%) !important;
        border-left-color: #00d4ff !important;
        padding-left: 1.2rem !important;
    }
    
    [data-baseweb="menu"] li[aria-selected="true"] {
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.3) 0%, transparent 100%) !important;
        border-left-color: #00d4ff !important;
        font-weight: 700 !important;
    }
    
    /* Checkbox styling */
    .stCheckbox {
        padding: 0.8rem 0;
        color: #ffffff !important;
    }
    
    .stCheckbox label {
        color: #ffffff !important;
        font-size: 1.1rem;
    }
    
    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        color: #00d4ff;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        text-align: center;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    /* Info box in sidebar */
    .info-box {
        background: linear-gradient(135deg, #7b2ff7 0%, #00d4ff 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(123, 47, 247, 0.4);
    }
    
    /* Query section */
    .query-section {
        background: linear-gradient(145deg, #1a1d29 0%, #262b3d 100%);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(123, 47, 247, 0.3);
    }
    
    /* Labels - white text */
    .stTextArea label, .stSelectbox label {
        font-weight: 700;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Section headers */
    h3 {
        color: #00d4ff !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        margin-top: 0.5rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    /* Model info box */
    .model-info {
        background: linear-gradient(135deg, #262b3d 0%, #1a1d29 100%);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #7b2ff7;
        color: #00d4ff;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(123, 47, 247, 0.3);
    }
    
    /* Clear history button */
    .clear-history-btn {
        background: linear-gradient(135deg, #f107a3 0%, #7b2ff7 100%);
        color: white;
        padding: 0.8rem;
        border-radius: 10px;
        text-align: center;
        cursor: pointer;
        margin-top: 1rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(241, 7, 163, 0.4);
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning {
        background-color: rgba(26, 29, 41, 0.8) !important;
        color: #ffffff !important;
        border-radius: 10px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #00d4ff !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #8b92a8;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(123, 47, 247, 0.3);
    }
    
    /* Divider */
    hr {
        border-color: rgba(123, 47, 247, 0.3) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* History container */
    .history-container {
        max-height: 600px;
        overflow-y: auto;
        padding-right: 0.5rem;
    }
    
    /* Scrollbar styling */
    .history-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .history-container::-webkit-scrollbar-track {
        background: #1a1d29;
        border-radius: 10px;
    }
    
    .history-container::-webkit-scrollbar-thumb {
        background: #7b2ff7;
        border-radius: 10px;
    }
    
    .history-container::-webkit-scrollbar-thumb:hover {
        background: #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🤖 AI AGENT ASSISTANT</h1>
    <p class="main-subtitle">Advanced Language Models • Real-Time Web Search • Intelligent Responses</p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Settings")
    
    st.markdown('<div class="info-box">💡 Configure Your AI Agent</div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 Model Selection")
    selected_model = st.selectbox(
        "Choose AI Model:",
        settings.ALLOWED_MODEL_NAMES,
        help="Select the language model to use",
        label_visibility="collapsed"
    )
    
    # Show selected model clearly
    st.markdown(f"""
    <div class='selected-model-display'>
        <span style='color: #8b92a8; font-size: 0.9rem;'>Selected:</span> 
        <strong style='color: #00d4ff;'>{selected_model}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🌐 Search Settings")
    allow_web_search = st.checkbox(
        "Enable Web Search",
        value=True,
        help="Allow the agent to search the web for current information"
    )
    
    st.markdown("---")
    
    st.markdown("### 📝 System Prompt")
    system_prompt = st.text_area(
        "Define Agent Behavior:",
        height=150,
        placeholder="e.g., You are a helpful assistant that provides accurate answers...",
        help="Set the personality and behavior of your AI agent"
    )
    
    # Clear history button
    if len(st.session_state.chat_history) > 0:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

# Main content area
st.markdown("### 💬 Ask Your Question")

st.markdown('<div class="query-section">', unsafe_allow_html=True)

user_query = st.text_area(
    "What would you like to know?",
    height=150,
    placeholder="Type your question here... e.g., 'What are the latest developments in AI?'",
    label_visibility="collapsed",
    key="user_input"
)

# Button with icon
if st.button("🚀 Ask Agent"):
    if not user_query.strip():
        st.warning("⚠️ Please enter a query before submitting.")
    else:
        API_URL = "http://127.0.0.1:9999/chat"
        
        payload = {
            "model_name": selected_model,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        try:
            with st.spinner("🔄 Processing your request..."):
                logger.info("Sending request to backend")
                response = requests.post(API_URL, json=payload, timeout=60)

                if response.status_code == 200:
                    agent_response = response.json().get("response", "")
                    logger.info("Successfully received response from backend")
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "query": user_query,
                        "response": agent_response,
                        "model": selected_model
                    })
                    
                    st.success("✅ Response generated successfully!")

                else:
                    logger.error(f"Backend returned status code {response.status_code}")
                    st.error(f"❌ Backend Error: Status code {response.status_code}")
                    
                    try:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.error(f"Details: {error_detail}")
                    except:
                        pass

        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            st.error("⏱️ Request timed out. Please try again with a simpler query.")
            
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to backend")
            st.error("🔌 Cannot connect to backend. Please ensure the server is running.")
            
        except Exception as e:
            logger.error(f"Error occurred while sending request to backend: {e}", exc_info=True)
            st.error(f"❌ An error occurred: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Display chat history
if len(st.session_state.chat_history) > 0:
    st.markdown("---")
    st.markdown("### 📜 Chat History")
    
    st.markdown('<div class="history-container">', unsafe_allow_html=True)
    
    # Display in reverse order (most recent first)
    for idx, chat in enumerate(reversed(st.session_state.chat_history)):
        formatted_response = chat['response'].replace('\n', '<br>')
        
        st.markdown(f"""
        <div class="chat-item">
            <div class="chat-query">
                <strong>🙋 Query #{len(st.session_state.chat_history) - idx}:</strong> {chat['query']}
            </div>
            <div class="chat-response">
                <strong>🤖 Response:</strong><br>{formatted_response}
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #8b92a8;">
                Model: {chat['model']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class='footer'>
    <small>Built with  using Streamlit • Powered by LangChain & Groq</small>
</div>
""", unsafe_allow_html=True)