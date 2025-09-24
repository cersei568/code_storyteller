import streamlit as st
from openai import OpenAI
from dotenv import dotenv_values
import tempfile
import json
from pathlib import Path
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="💻 Code Storyteller", 
    page_icon="💻", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    /* Root variables - Beautiful Beige Palette */
    :root {
        --primary-beige: #F5F1E8;
        --warm-beige: #F0E6D2;
        --cream: #FAF7F0;
        --sand: #E8DCC0;
        --taupe: #D4C4A0;
        --coffee: #8B7D6B;
        --dark-coffee: #6B5B47;
        --accent-gold: #DAA520;
        --accent-bronze: #CD7F32;
        --success-sage: #9CAF88;
        --warning-amber: #F4A460;
        --error-terracotta: #CD853F;
        
        --text-primary: #2C2C2C;
        --text-secondary: #4A4A4A;
        --text-muted: #6B6B6B;
        --text-light: #8A8A8A;
        
        --gradient-warm: linear-gradient(135deg, #F5F1E8 0%, #F0E6D2 50%, #E8DCC0 100%);
        --gradient-subtle: linear-gradient(135deg, #FAF7F0 0%, #F5F1E8 100%);
        --gradient-accent: linear-gradient(135deg, #DAA520 0%, #CD7F32 100%);
        
        --shadow-soft: 0 4px 20px rgba(139, 125, 107, 0.15);
        --shadow-medium: 0 8px 30px rgba(139, 125, 107, 0.2);
        --shadow-strong: 0 12px 40px rgba(139, 125, 107, 0.25);
        
        --border-beige: rgba(139, 125, 107, 0.2);
        --border-light: rgba(139, 125, 107, 0.1);
    }
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: var(--gradient-warm);
        min-height: 100vh;
        color: var(--text-primary);
    }
    
    /* Reset Streamlit defaults */
    .css-18e3th9 {
        padding-top: 2rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Beautiful Header */
    .app-header {
        background: var(--cream);
        border: 2px solid var(--border-beige);
        border-radius: 24px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow-medium);
        animation: fadeInDown 0.8s ease-out;
        backdrop-filter: blur(10px);
    }
    
    .app-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--text-primary), var(--coffee));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(139, 125, 107, 0.1);
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        color: var(--text-secondary);
        font-weight: 400;
        letter-spacing: 0.5px;
        font-style: italic;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: var(--warm-beige) !important;
        border-right: 2px solid var(--border-beige);
        backdrop-filter: blur(15px);
    }
    
    /* Ensure all text is black/dark */
    .main *, .css-1d391kg * {
        color: var(--text-primary) !important;
    }
    
    /* Button styles */
    .stButton > button {
        background: var(--gradient-accent);
        color: white !important;
        border: none;
        border-radius: 16px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-soft);
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
        text-transform: capitalize;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
        background: linear-gradient(135deg, #B8860B 0%, #A0522D 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Mode buttons */
    .mode-button {
        background: var(--sand) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-beige) !important;
        backdrop-filter: blur(10px);
    }
    
    .mode-button:hover {
        background: var(--taupe) !important;
        border-color: var(--coffee) !important;
        color: var(--text-primary) !important;
    }
    
    /* Special button variants */
    .delete-button {
        background: linear-gradient(135deg, var(--error-terracotta), #A0522D) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(205, 133, 63, 0.3) !important;
    }
    
    .delete-button:hover {
        box-shadow: 0 8px 25px rgba(205, 133, 63, 0.4) !important;
        background: linear-gradient(135deg, #A0522D, #8B4513) !important;
    }
    
    .success-button {
        background: linear-gradient(135deg, var(--success-sage), #7A8B5B) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(156, 175, 136, 0.3) !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--cream) !important;
        border: 2px solid var(--border-beige) !important;
        border-radius: 12px;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        padding: 0.75rem 1rem;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-muted) !important;
        font-style: italic;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 3px rgba(218, 165, 32, 0.2) !important;
        background: white !important;
        outline: none;
    }
    
    /* Input labels */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label {
        color: var(--text-primary) !important;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: var(--cream) !important;
        border: 2px solid var(--border-light);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.5s ease-out;
    }
    
    .stChatMessage * {
        color: var(--text-primary) !important;
    }
    
    /* Different styles for user vs assistant messages */
    .stChatMessage[data-testid="user-message"] {
        background: var(--sand) !important;
        border-color: var(--taupe);
        margin-left: 2rem;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: var(--warm-beige) !important;
        border-color: var(--coffee);
        margin-right: 2rem;
    }
    
    /* Glass card effect */
    .glass-card {
        background: var(--cream);
        border: 2px solid var(--border-beige);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .glass-card * {
        color: var(--text-primary) !important;
    }
    
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-medium);
        border-color: var(--coffee);
        background: white;
    }
    
    /* Metrics cards */
    .metric-card {
        background: var(--gradient-subtle);
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px solid var(--border-light);
        box-shadow: var(--shadow-soft);
        transition: transform 0.3s ease;
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
    }
    
    .metric-card * {
        color: var(--text-primary) !important;
    }
    
    /* Code blocks */
    .stCode {
        background: var(--sand) !important;
        border-radius: 12px !important;
        border: 2px solid var(--border-beige) !important;
        box-shadow: inset 0 2px 4px rgba(139, 125, 107, 0.1);
    }
    
    .stCode * {
        color: var(--text-primary) !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: var(--cream) !important;
        border: 2px solid var(--border-beige) !important;
        border-radius: 12px;
        color: var(--text-primary) !important;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 3px rgba(218, 165, 32, 0.2) !important;
    }
    
    .stSelectbox > div > div > div {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox option {
        background: var(--cream) !important;
        color: var(--text-primary) !important;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes gentlePulse {
        0%, 100% {
            transform: scale(1);
            box-shadow: var(--shadow-soft);
        }
        50% {
            transform: scale(1.02);
            box-shadow: var(--shadow-medium);
        }
    }
    
    /* Success/Error/Info messages */
    .stSuccess {
        background: linear-gradient(90deg, rgba(156, 175, 136, 0.15), rgba(156, 175, 136, 0.25)) !important;
        border-left: 4px solid var(--success-sage) !important;
        border-radius: 12px;
        color: var(--text-primary) !important;
    }
    
    .stError {
        background: linear-gradient(90deg, rgba(205, 133, 63, 0.15), rgba(205, 133, 63, 0.25)) !important;
        border-left: 4px solid var(--error-terracotta) !important;
        border-radius: 12px;
        color: var(--text-primary) !important;
    }
    
    .stInfo {
        background: linear-gradient(90deg, rgba(218, 165, 32, 0.15), rgba(218, 165, 32, 0.25)) !important;
        border-left: 4px solid var(--accent-gold) !important;
        border-radius: 12px;
        color: var(--text-primary) !important;
    }
    
    /* Chat input */
    .stChatInput > div > div {
        background: var(--cream) !important;
        border: 2px solid var(--border-beige) !important;
        border-radius: 25px;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }
    
    .stChatInput > div > div:focus-within {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 3px rgba(218, 165, 32, 0.2) !important;
    }
    
    .stChatInput input {
        color: var(--text-primary) !important;
        background: transparent !important;
        font-family: 'Inter', sans-serif;
    }
    
    .stChatInput input::placeholder {
        color: var(--text-muted) !important;
        font-style: italic;
    }
    
    /* Section headers */
    .section-header {
        color: var(--text-primary) !important;
        font-weight: 700;
        font-size: 1.4rem;
        margin: 1.5rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'Playfair Display', serif;
    }
    
    .section-header::before {
        content: '';
        width: 4px;
        height: 24px;
        background: var(--gradient-accent);
        border-radius: 2px;
    }
    
    /* Welcome message styling */
    .welcome-card {
        background: var(--gradient-subtle) !important;
        color: var(--text-primary) !important;
        text-align: center;
        padding: 3rem 2rem;
        border: 2px solid var(--border-light);
        animation: gentlePulse 3s ease-in-out infinite;
    }
    
    .welcome-card h3 {
        color: var(--text-primary) !important;
        margin-bottom: 1rem;
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
    }
    
    .welcome-card p {
        color: var(--text-secondary) !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--sand);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gradient-accent);
        border-radius: 10px;
        border: 2px solid var(--sand);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #B8860B, #A0522D);
    }
    
    /* Loading spinner */
    .stSpinner {
        color: var(--accent-gold) !important;
    }
    
    /* Audio player styling */
    .stAudio {
        border-radius: 12px;
        overflow: hidden;
        background: var(--cream);
        border: 2px solid var(--border-beige);
    }
    
    /* Floating elements */
    .floating-button {
        background: var(--gradient-accent);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
        box-shadow: var(--shadow-strong);
        animation: gentlePulse 2s infinite;
        cursor: pointer;
        transition: all 0.3s ease;
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 1000;
    }
    
    .floating-button:hover {
        transform: scale(1.1);
        box-shadow: 0 20px 40px rgba(218, 165, 32, 0.4);
    }
    
    /* Enhanced typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    p, span, div {
        color: var(--text-primary) !important;
        line-height: 1.6;
    }
    
    /* Sidebar specific overrides */
    .css-1d391kg .section-header {
        color: var(--dark-coffee) !important;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: var(--dark-coffee) !important;
    }
    
    /* Ensure black text in all contexts */
    .stMarkdown, .stMarkdown * {
        color: var(--text-primary) !important;
    }
    
    /* Chat message content */
    .stChatMessage .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    .stChatMessage .stMarkdown * {
        color: var(--text-primary) !important;
    }
    
    /* Code syntax highlighting adjustment */
    .stChatMessage code {
        background-color: var(--sand) !important;
        color: var(--text-primary) !important;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        border: 1px solid var(--border-beige);
    }
    
    /* Pre-formatted text blocks */
    .stChatMessage pre {
        background-color: var(--sand) !important;
        border: 2px solid var(--border-beige) !important;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stChatMessage pre code {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        color: var(--text-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- CONSTANTS --------------------
DEFAULT_PERSONALITY = """You are a helpful coding assistant who explains code clearly and concisely.
You can answer questions about programming and help users understand their code.
When explaining code, adapt your explanation style based on user preference."""
DB_PATH = Path("db")
DB_CONVERSATIONS_PATH = DB_PATH / "conversations"

MODEL_PRICINGS = {
    "tts-1": {"per_1000_chars": 0.015},
    "gpt-4o-mini": {"input_tokens": 0.150 / 1_000_000, "output_tokens": 0.600 / 1_000_000},
}
USD_TO_PLN = 3.6

# -------------------- SESSION STATE INITIALIZATION --------------------
if "api_key_validated" not in st.session_state:
    st.session_state["api_key_validated"] = False
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = ""

# -------------------- API KEY PROTECTION --------------------
def request_api_key():
    st.markdown("""
        <div class="app-header">
            <h1 class="app-title">🔑 API Key Required</h1>
            <p class="app-subtitle">Enter your OpenAI API key to unlock the magic</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...", help="Your API key is stored securely for this session only")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Validate & Enter", use_container_width=True):
            if api_key.startswith("sk-") and len(api_key) > 20:
                try:
                    client = OpenAI(api_key=api_key)
                    client.models.list()  # Test key
                    st.session_state["openai_api_key"] = api_key
                    st.session_state["api_key_validated"] = True
                    st.success("✅ Welcome to Code Storyteller!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Invalid API key: {str(e)}")
            else:
                st.error("❌ Please enter a valid API key.")
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state["api_key_validated"]:
    request_api_key()
    st.stop()

# -------------------- INIT OPENAI --------------------
openai_client = OpenAI(api_key=st.session_state["openai_api_key"])

# -------------------- DATABASE FUNCTIONS --------------------
def ensure_db():
    DB_PATH.mkdir(exist_ok=True)
    DB_CONVERSATIONS_PATH.mkdir(exist_ok=True)

def load_conversation_to_state(conv):
    st.session_state["id"] = conv["id"]
    st.session_state["name"] = conv["name"]
    st.session_state["messages"] = conv["messages"]
    st.session_state["chatbot_personality"] = conv["chatbot_personality"]
    st.session_state["total_cost"] = conv.get("total_cost", 0.0)

def get_all_conversations():
    ensure_db()
    convs = []
    for p in DB_CONVERSATIONS_PATH.glob("*.json"):
        with open(p, "r") as f:
            data = json.load(f)
            convs.append({"id": data["id"], "name": data["name"]})
    return sorted(convs, key=lambda x: x["id"], reverse=True)

def save_current_conversation():
    conv_id = st.session_state.get("id")
    if conv_id:
        conv = {
            "id": conv_id,
            "name": st.session_state.get("name", f"Conversation {conv_id}"),
            "chatbot_personality": st.session_state.get("chatbot_personality", DEFAULT_PERSONALITY),
            "messages": st.session_state.get("messages", []),
            "total_cost": st.session_state.get("total_cost", 0.0)
        }
        with open(DB_CONVERSATIONS_PATH / f"{conv_id}.json", "w") as f:
            json.dump(conv, f, indent=2)
        with open(DB_PATH / "current.json", "w") as f:
            json.dump({"current_conversation_id": conv_id}, f)

def create_new_conversation():
    ensure_db()
    existing_ids = [int(p.stem) for p in DB_CONVERSATIONS_PATH.glob("*.json")]
    conv_id = max(existing_ids) + 1 if existing_ids else 1
    conv = {
        "id": conv_id,
        "name": f"Conversation {conv_id}",
        "chatbot_personality": DEFAULT_PERSONALITY,
        "messages": [],
        "total_cost": 0.0
    }
    with open(DB_CONVERSATIONS_PATH / f"{conv_id}.json", "w") as f:
        json.dump(conv, f, indent=2)
    with open(DB_PATH / "current.json", "w") as f:
        json.dump({"current_conversation_id": conv_id}, f)
    load_conversation_to_state(conv)
    return conv_id

def load_current_conversation():
    ensure_db()
    current_file = DB_PATH / "current.json"
    if current_file.exists():
        with open(current_file, "r") as f:
            data = json.load(f)
        conv_file = DB_CONVERSATIONS_PATH / f"{data['current_conversation_id']}.json"
        if conv_file.exists():
            with open(conv_file, "r") as f:
                conv = json.load(f)
            load_conversation_to_state(conv)
        else:
            create_new_conversation()
    else:
        create_new_conversation()

# -------------------- CHAT FUNCTIONS --------------------
def calculate_cost(usage):
    if not usage:
        return 0.0
    input_cost = usage.get("prompt_tokens", 0) * MODEL_PRICINGS["gpt-4o-mini"]["input_tokens"]
    output_cost = usage.get("completion_tokens", 0) * MODEL_PRICINGS["gpt-4o-mini"]["output_tokens"]
    return input_cost + output_cost

def generate_tts(text):
    response = openai_client.audio.speech.create(model="tts-1", voice="alloy", input=text, response_format="mp3")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(response.read())
        filename = tmp.name
    cost = (len(text)/1000)*MODEL_PRICINGS["tts-1"]["per_1000_chars"]
    return filename, cost

def send_message(prompt, include_code=False, code_content="", explanation_type="General"):
    user_message = prompt
    if include_code:
        user_message = f"Please explain this code ({explanation_type}):\n```{code_content}```"
    messages = [{"role":"system","content":st.session_state.get("chatbot_personality", DEFAULT_PERSONALITY)}]
    messages += st.session_state.get("messages", [])[-10:]
    messages.append({"role":"user","content":user_message})
    
    resp = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )
    assistant_msg = resp.choices[0].message.content
    usage = resp.usage.to_dict() if resp.usage else {}
    
    st.session_state["messages"].append({"role":"user","content":user_message,"timestamp":time.time()})
    st.session_state["messages"].append({"role":"assistant","content":assistant_msg,"usage":usage,"timestamp":time.time()})
    st.session_state["total_cost"] = st.session_state.get("total_cost",0)+calculate_cost(usage)
    
    save_current_conversation()
    return assistant_msg, usage

# -------------------- INITIALIZE SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "show_code_input" not in st.session_state:
    st.session_state["show_code_input"] = False
if "id" not in st.session_state:
    load_current_conversation()
if "total_cost" not in st.session_state:
    st.session_state["total_cost"] = 0.0

# -------------------- BEAUTIFUL HEADER --------------------
st.markdown("""
    <div class="app-header">
        <h1 class="app-title">💻 Code Storyteller</h1>
        <p class="app-subtitle">Transform your code into beautiful stories with AI elegance</p>
    </div>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown('<h2 class="section-header">💬 Conversations</h2>', unsafe_allow_html=True)
    
    conversations = get_all_conversations()
    if conversations:
        for conv in conversations:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"📄 {conv['name']}", key=f"conv_{conv['id']}", use_container_width=True):
                    conv_file = DB_CONVERSATIONS_PATH / f"{conv['id']}.json"
                    if conv_file.exists():
                        with open(conv_file, "r") as f:
                            conv_data = json.load(f)
                        load_conversation_to_state(conv_data)
                        st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{conv['id']}", help="Delete conversation"):
                    (DB_CONVERSATIONS_PATH/f"{conv['id']}.json").unlink()
                    st.rerun()
            
            # Inline rename
            new_name = st.text_input("Rename:", value=conv["name"], key=f"rename_{conv['id']}", label_visibility="collapsed")
            if new_name != conv["name"]:
                if st.button("💾 Save", key=f"save_{conv['id']}", use_container_width=True):
                    conv_file = DB_CONVERSATIONS_PATH / f"{conv['id']}.json"
                    if conv_file.exists():
                        with open(conv_file, "r") as f:
                            conv_data = json.load(f)
                        conv_data["name"] = new_name
                        with open(conv_file, "w") as f:
                            json.dump(conv_data, f, indent=2)
                        st.success("✨ Renamed successfully!")
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("🌟 Start your first elegant conversation!")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if st.button("✨ New Conversation", use_container_width=True):
        create_new_conversation()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🤖 AI Personality</h2>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    new_personality = st.text_area("System prompt:", value=st.session_state.get("chatbot_personality", DEFAULT_PERSONALITY), height=150)
    if st.button("🎭 Update Personality", use_container_width=True):
        st.session_state["chatbot_personality"] = new_personality
        save_current_conversation()
        st.success("🎭 Personality updated with elegance!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<h2 class="section-header">💰 Usage Costs</h2>', unsafe_allow_html=True)
    total_cost = st.session_state.get('total_cost', 0)
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("💵 USD", f"${total_cost:.4f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("💸 PLN", f"{total_cost * USD_TO_PLN:.2f} zł")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- MODE SELECTION --------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    if st.button("💬 Chat Mode", use_container_width=True):
        st.session_state["show_code_input"] = False
        st.rerun()
with col2:
    if st.button("📝 Code Explanation", use_container_width=True):
        st.session_state["show_code_input"] = True
        st.rerun()
with col3:
    if st.button("🗑️ Clear", use_container_width=True, help="Clear current chat"):
        st.session_state["messages"] = []
        save_current_conversation()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# -------------------- CHAT DISPLAY --------------------
chat_container = st.container()
with chat_container:
    if st.session_state.get("messages"):
        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if msg["role"] == "assistant":
                    col1, col2, col3 = st.columns([8, 1, 1])
                    with col2:
                        if st.button("🔊", key=f"tts_{msg['timestamp']}", help="Generate elegant audio"):
                            with st.spinner("🎵 Creating beautiful audio..."):
                                audio_file, tts_cost = generate_tts(msg["content"])
                                st.session_state["total_cost"] += tts_cost
                                save_current_conversation()
                                st.audio(audio_file)
                    with col3:
                        if "tts_generated" in locals():
                            st.download_button(
                                "📥", 
                                data=open(audio_file, "rb") if 'audio_file' in locals() else b"", 
                                file_name="elegant_tts.mp3", 
                                mime="audio/mp3", 
                                key=f"dl_{msg['timestamp']}",
                                help="Download audio"
                            )
    else:
        st.markdown("""
            <div class="glass-card welcome-card">
                <h3>🌟 Welcome to Code Storyteller!</h3>
                <p>Begin an elegant conversation or share your code for beautiful explanations crafted with care.</p>
                <p style="font-style: italic; margin-top: 1rem; opacity: 0.8;">Where code meets poetry, and logic becomes art.</p>
            </div>
        """, unsafe_allow_html=True)

# -------------------- INPUT SECTION --------------------
if st.session_state.get("show_code_input"):
    st.markdown('<h2 class="section-header">📝 Code Analysis</h2>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    code_input = st.text_area(
        "Share your code masterpiece:", 
        height=200, 
        placeholder="// Your elegant code belongs here...\nfunction createMagic() {\n    console.log('Transforming code into poetry...');\n}",
        help="Share any code and I'll weave it into a beautiful explanation!"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        explanation_type = st.selectbox(
            "Choose your narrative style:", 
            ["General", "Detailed (line by line)", "Beginner-friendly", "Advanced analysis"],
            help="Select the depth and style of explanation that suits your needs"
        )
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("✨ Craft Explanation", use_container_width=True):
            if code_input.strip():
                with st.spinner("🔍 Weaving your code into an elegant story..."):
                    send_message("", include_code=True, code_content=code_input, explanation_type=explanation_type.split()[0])
                    st.rerun()
            else:
                st.error("Please share your code so I can craft its story! 📋")
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Chat input
    chat_input = st.chat_input("Share your thoughts about coding... ✨", key="main_chat_input")
    if chat_input:
        with st.spinner("🤔 Contemplating your question with care..."):
            send_message(chat_input)
            st.rerun()

# -------------------- FOOTER --------------------
st.markdown("""
    <div class="glass-card" style="text-align: center; margin-top: 2rem;">
        <p style="margin: 0; font-style: italic;">
            ✨ <strong>Elegant Tip:</strong> Switch gracefully between Chat and Code modes for the most refined experience
        </p>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.7; font-size: 0.9rem;">
            Crafted with care in warm beige tones for your coding journey
        </p>
    </div>
""", unsafe_allow_html=True)