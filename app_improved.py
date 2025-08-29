import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
from vapi_client import (
    VAPIClient, 
    validate_assistant_data, 
    get_assistant_summary,
    DEFAULT_ASSISTANT_TEMPLATE,
    VOICE_PROVIDERS,
    MODEL_PROVIDERS
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="VAPI AI Assistant Manager",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .assistant-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f9f9f9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    .sidebar-section {
        margin-bottom: 2rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.getenv('VAPI_API_KEY', '')
    if 'api_base' not in st.session_state:
        st.session_state.api_base = os.getenv('VAPI_API_BASE', 'https://api.vapi.ai')
    if 'assistants' not in st.session_state:
        st.session_state.assistants = []
    if 'client' not in st.session_state:
        st.session_state.client = None
    if 'connection_status' not in st.session_state:
        st.session_state.connection_status = False

def get_client():
    """Get or create VAPI client"""
    if not st.session_state.api_key:
        return None
    
    if (st.session_state.client is None or 
        st.session_state.client.api_key != st.session_state.api_key or
        st.session_state.client.api_base != st.session_state.api_base):
        
        st.session_state.client = VAPIClient(
            api_key=st.session_state.api_key,
            api_base=st.session_state.api_base
        )
        # Test connection
        st.session_state.connection_status = st.session_state.client.test_connection()
    
    return st.session_state.client

def load_assistants():
    """Load assistants from VAPI AI"""
    client = get_client()
    if client and st.session_state.connection_status:
        assistants = client.list_assistants()
        if assistants is not None:
            st.session_state.assistants = assistants
            return True
    return False

# Initialize session state
init_session_state()

# Sidebar
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.title("🤖 VAPI AI Manager")

# Connection status
client = get_client()
if st.session_state.connection_status:
    st.sidebar.success("✅ API Connected")
else:
    st.sidebar.error("❌ API Not Connected")

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Navigation
page = st.sidebar.selectbox(
    "Navigate to:",
    ["🏠 Dashboard", "👁️ View Assistants", "➕ Create Assistant", "✏️ Edit Assistant", "⚙️ Settings"],
    key="navigation"
)

# Quick stats in sidebar
if st.session_state.assistants:
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### Quick Stats")
    st.sidebar.metric("Total Assistants", len(st.session_state.assistants))
    
    # Recent activity
    if st.session_state.assistants:
        recent = sorted(st.session_state.assistants, 
                       key=lambda x: x.get('updatedAt', ''), reverse=True)[:3]
        st.sidebar.markdown("**Recent:**")
        for assistant in recent:
            name = assistant.get('name', 'Unnamed')[:20]
            st.sidebar.text(f"• {name}")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Refresh button
if st.sidebar.button("🔄 Refresh Data"):
    load_assistants()
    st.rerun()

# Main content
if page == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">VAPI AI Assistant Manager</h1>', unsafe_allow_html=True)
    
    # Status overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_color = "🟢" if st.session_state.connection_status else "🔴"
        st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
        st.metric("API Status", f"{status_color} {'Connected' if st.session_state.connection_status else 'Disconnected'}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Assistants", len(st.session_state.assistants))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
        api_display = st.session_state.api_base.replace('https://', '').replace('http://', '')
        st.metric("API Endpoint", api_display)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
        key_status = "Set" if st.session_state.api_key else "Not Set"
        st.metric("API Key", key_status)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Load assistants if not loaded and connected
    if st.session_state.connection_status and not st.session_state.assistants:
        load_assistants()
    
    # Recent assistants
    if st.session_state.assistants:
        st.markdown('<div class="section-header">Recent Assistants</div>', unsafe_allow_html=True)
        
        recent_assistants = sorted(st.session_state.assistants, 
                                 key=lambda x: x.get('updatedAt', ''), reverse=True)[:5]
        
        for assistant in recent_assistants:
            summary = get_assistant_summary(assistant)
            
            with st.container():
                st.markdown('<div class="assistant-card">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([3, 2, 2])
                
                with col1:
                    st.markdown(f"**{summary['name']}**")
                    st.text(f"ID: {summary['id'][:20]}...")
                    if summary['first_message'] != 'N/A':
                        st.text(f"First Message: {summary['first_message'][:50]}...")
                
                with col2:
                    st.text(f"Voice: {summary['voice_provider']}")
                    st.text(f"Model: {summary['model_provider']}")
                    if summary['model_name'] != 'N/A':
                        st.text(f"Model Name: {summary['model_name']}")
                
                with col3:
                    st.text(f"Created: {summary['created']}")
                    st.text(f"Updated: {summary['updated']}")
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        if st.session_state.connection_status:
            st.info("No assistants found. Create your first assistant!")
        else:
            st.warning("Please configure your API settings to get started.")

elif page == "👁️ View Assistants":
    st.markdown('<h1 class="main-header">View Assistants</h1>', unsafe_allow_html=True)
    
    if not st.session_state.connection_status:
        st.error("❌ API not connected. Please check your settings.")
        st.stop()
    
    # Load assistants
    if st.button("🔄 Refresh Assistants") or not st.session_state.assistants:
        with st.spinner("Loading assistants..."):
            load_assistants()
    
    if st.session_state.assistants:
        # Summary table
        st.markdown('<div class="section-header">Assistants Overview</div>', unsafe_allow_html=True)
        
        # Create summary data
        summary_data = []
        for assistant in st.session_state.assistants:
            summary = get_assistant_summary(assistant)
            summary_data.append({
                'Name': summary['name'],
                'ID': summary['id'][:12] + '...',
                'Voice Provider': summary['voice_provider'],
                'Model Provider': summary['model_provider'],
                'Model': summary['model_name'],
                'Created': summary['created'],
                'Updated': summary['updated']
            })
        
        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Detailed view
        st.markdown('<div class="section-header">Detailed View</div>', unsafe_allow_html=True)
        
        assistant_options = {
            assistant['id']: assistant.get('name', f"Assistant {assistant['id'][:8]}...")
            for assistant in st.session_state.assistants
        }
        
        selected_id = st.selectbox(
            "Select an assistant to view details:",
            options=list(assistant_options.keys()),
            format_func=lambda x: assistant_options[x],
            key="view_assistant_select"
        )
        
        if selected_id:
            selected_assistant = next(
                (a for a in st.session_state.assistants if a['id'] == selected_id), 
                None
            )
            
            if selected_assistant:
                # Display assistant details in organized sections
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Basic Information")
                    st.text(f"Name: {selected_assistant.get('name', 'N/A')}")
                    st.text(f"ID: {selected_assistant.get('id', 'N/A')}")
                    st.text(f"Created: {get_assistant_summary(selected_assistant)['created']}")
                    st.text(f"Updated: {get_assistant_summary(selected_assistant)['updated']}")
                    
                    if selected_assistant.get('firstMessage'):
                        st.subheader("First Message")
                        st.text_area("", value=selected_assistant['firstMessage'], disabled=True, key="first_msg_view")
                
                with col2:
                    st.subheader("Configuration")
                    st.text(f"First Message Mode: {selected_assistant.get('firstMessageMode', 'N/A')}")
                    st.text(f"Max Duration: {selected_assistant.get('maxDurationSeconds', 'N/A')} seconds")
                    st.text(f"Background Sound: {selected_assistant.get('backgroundSound', 'N/A')}")
                    
                    # Voice configuration
                    voice_config = selected_assistant.get('voice', {})
                    if voice_config:
                        st.subheader("Voice Settings")
                        st.text(f"Provider: {voice_config.get('provider', 'N/A')}")
                        st.text(f"Voice ID: {voice_config.get('voiceId', 'N/A')}")
                        st.text(f"Speed: {voice_config.get('speed', 'N/A')}")
                        st.text(f"Stability: {voice_config.get('stability', 'N/A')}")
                
                # Model configuration
                model_config = selected_assistant.get('model', {})
                if model_config:
                    st.subheader("Model Configuration")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.text(f"Provider: {model_config.get('provider', 'N/A')}")
                        st.text(f"Model: {model_config.get('model', 'N/A')}")
                        st.text(f"Temperature: {model_config.get('temperature', 'N/A')}")
                        st.text(f"Max Tokens: {model_config.get('maxTokens', 'N/A')}")
                    
                    with col2:
                        messages = model_config.get('messages', [])
                        if messages:
                            system_msg = next((msg['content'] for msg in messages if msg.get('role') == 'system'), None)
                            if system_msg:
                                st.text_area("System Message:", value=system_msg, disabled=True, key="system_msg_view")
                
                # Raw JSON view
                with st.expander("View Raw JSON"):
                    st.json(selected_assistant)
    else:
        st.info("No assistants found. Create your first assistant!")

elif page == "➕ Create Assistant":
    st.markdown('<h1 class="main-header">Create New Assistant</h1>', unsafe_allow_html=True)
    
    if not st.session_state.connection_status:
        st.error("❌ API not connected. Please check your settings.")
        st.stop()
    
    with st.form("create_assistant_form", clear_on_submit=False):
        # Basic Information
        st.markdown('<div class="section-header">Basic Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Assistant Name*", placeholder="Enter assistant name")
            first_message = st.text_area(
                "First Message", 
                placeholder="What should the assistant say first?",
                help="This is the first message the assistant will say when a call starts"
            )
        
        with col2:
            first_message_mode = st.selectbox(
                "First Message Mode", 
                options=["assistant-speaks-first", "assistant-waits-for-user", "assistant-speaks-first-with-model-generated-message"],
                help="How the assistant should start the conversation"
            )
            max_duration = st.number_input(
                "Max Duration (seconds)", 
                min_value=10, max_value=43200, value=600,
                help="Maximum call duration in seconds"
            )
        
        # Voice Configuration
        st.markdown('<div class="section-header">Voice Configuration</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            voice_provider = st.selectbox(
                "Voice Provider", 
                options=list(VOICE_PROVIDERS.keys()),
                format_func=lambda x: f"{VOICE_PROVIDERS[x]['name']} - {VOICE_PROVIDERS[x]['description']}"
            )
            voice_id = st.text_input("Voice ID", placeholder="Enter voice ID (optional)")
        
        with col2:
            voice_speed = st.slider("Voice Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
            voice_stability = st.slider("Voice Stability", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
        
        # Model Configuration
        st.markdown('<div class="section-header">Model Configuration</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            model_provider = st.selectbox(
                "Model Provider", 
                options=list(MODEL_PROVIDERS.keys()),
                format_func=lambda x: f"{MODEL_PROVIDERS[x]['name']} - {MODEL_PROVIDERS[x]['description']}"
            )
            
            # Model selection based on provider
            available_models = MODEL_PROVIDERS[model_provider]['models']
            model_name = st.selectbox("Model", options=available_models)
        
        with col2:
            temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
            max_tokens = st.number_input("Max Tokens", min_value=1, max_value=4000, value=1000)
        
        system_message = st.text_area(
            "System Message", 
            placeholder="Enter system instructions for the assistant",
            help="This defines the assistant's behavior and personality",
            value="You are a helpful AI assistant. Be friendly, concise, and helpful in your responses."
        )
        
        # Advanced Settings
        st.markdown('<div class="section-header">Advanced Settings</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            background_sound = st.selectbox("Background Sound", options=["off", "office", "nature", "cafe"])
            end_call_message = st.text_input("End Call Message", placeholder="Message when ending call")
        
        with col2:
            voicemail_message = st.text_input("Voicemail Message", placeholder="Message for voicemail")
            end_call_phrases = st.text_area(
                "End Call Phrases (one per line)", 
                placeholder="goodbye\ntalk to you later\nend call",
                help="Phrases that will trigger the call to end"
            )
        
        # Submit button
        submitted = st.form_submit_button("Create Assistant", type="primary")
        
        if submitted:
            if not name:
                st.error("❌ Assistant name is required!")
            else:
                # Prepare assistant data
                assistant_data = {
                    "name": name,
                    "firstMessage": first_message,
                    "firstMessageMode": first_message_mode,
                    "maxDurationSeconds": max_duration,
                    "voice": {
                        "provider": voice_provider,
                        "voiceId": voice_id,
                        "speed": voice_speed,
                        "stability": voice_stability
                    },
                    "model": {
                        "provider": model_provider,
                        "model": model_name,
                        "temperature": temperature,
                        "maxTokens": max_tokens,
                        "messages": [
                            {
                                "role": "system",
                                "content": system_message
                            }
                        ]
                    },
                    "backgroundSound": background_sound,
                    "endCallMessage": end_call_message,
                    "voicemailMessage": voicemail_message,
                    "endCallPhrases": [phrase.strip() for phrase in end_call_phrases.split('\n') if phrase.strip()]
                }
                
                # Clean the data
                assistant_data = validate_assistant_data(assistant_data)
                
                # Create assistant
                client = get_client()
                if client:
                    with st.spinner("Creating assistant..."):
                        result = client.create_assistant(assistant_data)
                    
                    if result:
                        st.success(f"✅ Assistant '{name}' created successfully!")
                        st.json(result)
                        # Refresh assistants list
                        load_assistants()
                    else:
                        st.error("❌ Failed to create assistant. Please check your configuration and try again.")
                else:
                    st.error("❌ API client not available. Please check your settings.")

elif page == "✏️ Edit Assistant":
    st.markdown('<h1 class="main-header">Edit Assistant</h1>', unsafe_allow_html=True)
    
    if not st.session_state.connection_status:
        st.error("❌ API not connected. Please check your settings.")
        st.stop()
    
    # Load assistants if not loaded
    if not st.session_state.assistants:
        with st.spinner("Loading assistants..."):
            load_assistants()
    
    if st.session_state.assistants:
        # Select assistant to edit
        assistant_options = {
            assistant['id']: assistant.get('name', f"Assistant {assistant['id'][:8]}...")
            for assistant in st.session_state.assistants
        }
        
        selected_id = st.selectbox(
            "Select Assistant to Edit:",
            options=list(assistant_options.keys()),
            format_func=lambda x: assistant_options[x],
            key="edit_assistant_select"
        )
        
        if selected_id:
            selected_assistant = next(
                (a for a in st.session_state.assistants if a['id'] == selected_id), 
                None
            )
            
            if selected_assistant:
                with st.form("edit_assistant_form"):
                    # Basic Information
                    st.markdown('<div class="section-header">Basic Information</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Assistant Name*", value=selected_assistant.get('name', ''))
                        first_message = st.text_area(
                            "First Message", 
                            value=selected_assistant.get('firstMessage', '')
                        )
                    
                    with col2:
                        current_mode = selected_assistant.get('firstMessageMode', 'assistant-speaks-first')
                        mode_options = ["assistant-speaks-first", "assistant-waits-for-user", "assistant-speaks-first-with-model-generated-message"]
                        mode_index = mode_options.index(current_mode) if current_mode in mode_options else 0
                        
                        first_message_mode = st.selectbox(
                            "First Message Mode", 
                            options=mode_options,
                            index=mode_index
                        )
                        max_duration = st.number_input(
                            "Max Duration (seconds)", 
                            min_value=10, max_value=43200, 
                            value=selected_assistant.get('maxDurationSeconds', 600)
                        )
                    
                    # Voice Configuration
                    st.markdown('<div class="section-header">Voice Configuration</div>', unsafe_allow_html=True)
                    voice_config = selected_assistant.get('voice', {})
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        current_voice_provider = voice_config.get('provider', 'elevenlabs')
                        voice_provider_options = list(VOICE_PROVIDERS.keys())
                        voice_provider_index = voice_provider_options.index(current_voice_provider) if current_voice_provider in voice_provider_options else 0
                        
                        voice_provider = st.selectbox(
                            "Voice Provider", 
                            options=voice_provider_options,
                            index=voice_provider_index,
                            format_func=lambda x: f"{VOICE_PROVIDERS[x]['name']} - {VOICE_PROVIDERS[x]['description']}"
                        )
                        voice_id = st.text_input("Voice ID", value=voice_config.get('voiceId', ''))
                    
                    with col2:
                        voice_speed = st.slider(
                            "Voice Speed", 
                            min_value=0.5, max_value=2.0, 
                            value=voice_config.get('speed', 1.0), 
                            step=0.1
                        )
                        voice_stability = st.slider(
                            "Voice Stability", 
                            min_value=0.0, max_value=1.0, 
                            value=voice_config.get('stability', 0.5), 
                            step=0.1
                        )
                    
                    # Model Configuration
                    st.markdown('<div class="section-header">Model Configuration</div>', unsafe_allow_html=True)
                    model_config = selected_assistant.get('model', {})
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        current_model_provider = model_config.get('provider', 'openai')
                        model_provider_options = list(MODEL_PROVIDERS.keys())
                        model_provider_index = model_provider_options.index(current_model_provider) if current_model_provider in model_provider_options else 0
                        
                        model_provider = st.selectbox(
                            "Model Provider", 
                            options=model_provider_options,
                            index=model_provider_index,
                            format_func=lambda x: f"{MODEL_PROVIDERS[x]['name']} - {MODEL_PROVIDERS[x]['description']}"
                        )
                        
                        # Model selection based on provider
                        available_models = MODEL_PROVIDERS[model_provider]['models']
                        current_model = model_config.get('model', available_models[0])
                        model_index = available_models.index(current_model) if current_model in available_models else 0
                        
                        model_name = st.selectbox("Model", options=available_models, index=model_index)
                    
                    with col2:
                        temperature = st.slider(
                            "Temperature", 
                            min_value=0.0, max_value=2.0, 
                            value=model_config.get('temperature', 0.7), 
                            step=0.1
                        )
                        max_tokens = st.number_input(
                            "Max Tokens", 
                            min_value=1, max_value=4000, 
                            value=model_config.get('maxTokens', 1000)
                        )
                    
                    # Get system message
                    system_message = ""
                    messages = model_config.get('messages', [])
                    for msg in messages:
                        if msg.get('role') == 'system':
                            system_message = msg.get('content', '')
                            break
                    
                    system_message = st.text_area(
                        "System Message", 
                        value=system_message,
                        help="This defines the assistant's behavior and personality"
                    )
                    
                    # Advanced Settings
                    st.markdown('<div class="section-header">Advanced Settings</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        current_bg_sound = selected_assistant.get('backgroundSound', 'off')
                        bg_sound_options = ["off", "office", "nature", "cafe"]
                        bg_sound_index = bg_sound_options.index(current_bg_sound) if current_bg_sound in bg_sound_options else 0
                        
                        background_sound = st.selectbox("Background Sound", options=bg_sound_options, index=bg_sound_index)
                        end_call_message = st.text_input(
                            "End Call Message", 
                            value=selected_assistant.get('endCallMessage', '')
                        )
                    
                    with col2:
                        voicemail_message = st.text_input(
                            "Voicemail Message", 
                            value=selected_assistant.get('voicemailMessage', '')
                        )
                        end_call_phrases_text = '\n'.join(selected_assistant.get('endCallPhrases', []))
                        end_call_phrases = st.text_area(
                            "End Call Phrases (one per line)", 
                            value=end_call_phrases_text
                        )
                    
                    # Action buttons
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        submitted = st.form_submit_button("Update Assistant", type="primary")
                    with col2:
                        delete_clicked = st.form_submit_button("Delete Assistant", type="secondary")
                    
                    if submitted:
                        if not name:
                            st.error("❌ Assistant name is required!")
                        else:
                            # Prepare update data
                            update_data = {
                                "name": name,
                                "firstMessage": first_message,
                                "firstMessageMode": first_message_mode,
                                "maxDurationSeconds": max_duration,
                                "voice": {
                                    "provider": voice_provider,
                                    "voiceId": voice_id,
                                    "speed": voice_speed,
                                    "stability": voice_stability
                                },
                                "model": {
                                    "provider": model_provider,
                                    "model": model_name,
                                    "temperature": temperature,
                                    "maxTokens": max_tokens,
                                    "messages": [
                                        {
                                            "role": "system",
                                            "content": system_message
                                        }
                                    ] if system_message else []
                                },
                                "backgroundSound": background_sound,
                                "endCallMessage": end_call_message,
                                "voicemailMessage": voicemail_message,
                                "endCallPhrases": [phrase.strip() for phrase in end_call_phrases.split('\n') if phrase.strip()]
                            }
                            
                            # Clean the data
                            update_data = validate_assistant_data(update_data)
                            
                            # Update assistant
                            client = get_client()
                            if client:
                                with st.spinner("Updating assistant..."):
                                    result = client.update_assistant(selected_id, update_data)
                                
                                if result:
                                    st.success(f"✅ Assistant '{name}' updated successfully!")
                                    st.json(result)
                                    # Refresh assistants list
                                    load_assistants()
                                else:
                                    st.error("❌ Failed to update assistant. Please check your configuration and try again.")
                            else:
                                st.error("❌ API client not available. Please check your settings.")
                    
                    if delete_clicked:
                        st.warning("⚠️ This action cannot be undone!")
                        if st.button("Confirm Delete", type="secondary", key="confirm_delete"):
                            client = get_client()
                            if client:
                                with st.spinner("Deleting assistant..."):
                                    success = client.delete_assistant(selected_id)
                                
                                if success:
                                    st.success("✅ Assistant deleted successfully!")
                                    # Refresh assistants list
                                    load_assistants()
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to delete assistant.")
                            else:
                                st.error("❌ API client not available. Please check your settings.")
    else:
        st.info("No assistants found. Create your first assistant!")

elif page == "⚙️ Settings":
    st.markdown('<h1 class="main-header">Settings</h1>', unsafe_allow_html=True)
    
    # API Configuration
    st.markdown('<div class="section-header">API Configuration</div>', unsafe_allow_html=True)
    
    with st.form("settings_form"):
        api_key = st.text_input(
            "VAPI API Key", 
            value=st.session_state.api_key, 
            type="password",
            help="Your VAPI AI API key from dashboard.vapi.ai"
        )
        
        api_base = st.text_input(
            "API Base URL", 
            value=st.session_state.api_base,
            help="Base URL for VAPI AI API (default: https://api.vapi.ai)"
        )
        
        org_id = st.text_input(
            "Organization ID (Optional)", 
            value=os.getenv('VAPI_ORG_ID', ''),
            help="Your organization ID if applicable"
        )
        
        submitted = st.form_submit_button("Save Settings", type="primary")
        
        if submitted:
            # Update session state
            st.session_state.api_key = api_key
            st.session_state.api_base = api_base
            st.session_state.client = None  # Reset client to force recreation
            
            # Test connection
            if api_key:
                with st.spinner("Testing API connection..."):
                    client = get_client()
                    if st.session_state.connection_status:
                        st.success("✅ API connection successful!")
                        # Load assistants with new settings
                        load_assistants()
                    else:
                        st.error("❌ API connection failed. Please check your API key and try again.")
            else:
                st.warning("⚠️ API key is required for the application to work.")
    
    # Connection Status
    st.markdown('<div class="section-header">Connection Status</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.connection_status:
            st.success("✅ API Connected")
            st.info(f"**Endpoint:** {st.session_state.api_base}")
            st.info(f"**Assistants Loaded:** {len(st.session_state.assistants)}")
        else:
            st.error("❌ API Not Connected")
            st.warning("Please configure your API key above.")
    
    with col2:
        if st.button("🔍 Test Connection"):
            if st.session_state.api_key:
                with st.spinner("Testing connection..."):
                    client = get_client()
                    if st.session_state.connection_status:
                        st.success("✅ Connection successful!")
                    else:
                        st.error("❌ Connection failed!")
            else:
                st.error("❌ API key required!")
    
    # Environment Setup Guide
    st.markdown('<div class="section-header">Environment Setup</div>', unsafe_allow_html=True)
    
    st.info("""
    **To set up environment variables permanently:**
    
    1. Create a `.env` file in the application directory
    2. Add the following lines:
    ```
    VAPI_API_KEY=your_api_key_here
    VAPI_API_BASE=https://api.vapi.ai
    VAPI_ORG_ID=your_org_id_here
    ```
    3. Restart the application
    
    **To get your API key:**
    1. Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
    2. Sign in to your account
    3. Navigate to Settings or API Keys section
    4. Copy your API key
    """)
    
    # Application Information
    st.markdown('<div class="section-header">Application Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Current Configuration:**
        - API Base: `{}`
        - API Key: {}
        - Total Assistants: {}
        - Connection Status: {}
        """.format(
            st.session_state.api_base,
            '✅ Set' if st.session_state.api_key else '❌ Not set',
            len(st.session_state.assistants),
            '✅ Connected' if st.session_state.connection_status else '❌ Disconnected'
        ))
    
    with col2:
        st.markdown("""
        **Features Available:**
        - ✅ View all assistants
        - ✅ Create new assistants
        - ✅ Edit existing assistants
        - ✅ Delete assistants
        - ✅ API configuration
        - ✅ Connection testing
        - ✅ Real-time updates
        """)
    
    # About Section
    st.markdown('<div class="section-header">About</div>', unsafe_allow_html=True)
    st.markdown("""
    **VAPI AI Assistant Manager** is a comprehensive Streamlit application for managing VAPI AI voice assistants.
    
    **Key Features:**
    - 🤖 **Assistant Management**: Create, view, edit, and delete voice AI assistants
    - ⚙️ **Configuration**: Full control over voice, model, and behavior settings
    - 🔧 **API Integration**: Direct integration with VAPI AI platform
    - 📊 **Dashboard**: Overview of all your assistants and their status
    - 🎛️ **Settings**: Easy API configuration and connection testing
    
    **Supported Providers:**
    - **Voice**: ElevenLabs, OpenAI, Azure, PlayHT
    - **Models**: OpenAI GP


T-4, Anthropic Claude, Google Gemini, Azure OpenAI
    
    Built with ❤️ using Streamlit and the VAPI AI API.
    """)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; margin-top: 2rem; padding: 1rem;">'
    '🤖 VAPI AI Assistant Manager | Built with Streamlit | '
    '<a href="https://vapi.ai" target="_blank">VAPI AI Platform</a>'
    '</div>', 
    unsafe_allow_html=True
)

