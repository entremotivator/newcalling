import streamlit as st
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
import pandas as pd

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title=" AI Assistant Manager",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    }
    .assistant-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f9f9f9;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .sidebar-section {
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv('VAPI_API_KEY', '')
if 'api_base' not in st.session_state:
    st.session_state.api_base = os.getenv('VAPI_API_BASE', 'https://api.vapi.ai')
if 'assistants' not in st.session_state:
    st.session_state.assistants = []
if 'selected_assistant' not in st.session_state:
    st.session_state.selected_assistant = None

# Sidebar navigation
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.title("🤖 VAPI AI Manager")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Navigation
page = st.sidebar.selectbox(
    "Navigate to:",
    ["🏠 Dashboard", "👁️ View Assistants", "➕ Create Assistant", "✏️ Edit Assistant", "⚙️ Settings"]
)

# API Configuration in sidebar
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown("### API Configuration")
api_status = "✅ Connected" if st.session_state.api_key else "❌ Not configured"
st.sidebar.markdown(f"**Status:** {api_status}")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Helper functions
def make_api_request(method, endpoint, data=None):
    """Make API request to VAPI AI"""
    if not st.session_state.api_key:
        st.error("API key not configured. Please go to Settings.")
        return None
    
    headers = {
        'Authorization': f'Bearer {st.session_state.api_key}',
        'Content-Type': 'application/json'
    }
    
    url = f"{st.session_state.api_base}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PATCH':
            response = requests.patch(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

def load_assistants():
    """Load assistants from VAPI AI API"""
    assistants = make_api_request('GET', '/assistant')
    if assistants:
        st.session_state.assistants = assistants
        return assistants
    return []

def format_datetime(dt_string):
    """Format datetime string for display"""
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return dt_string

# Main content based on selected page
if page == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">VAPI AI Assistant Manager</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("API Status", "Connected" if st.session_state.api_key else "Not Connected")
    
    with col2:
        if st.button("🔄 Refresh Assistants"):
            load_assistants()
        st.metric("Total Assistants", len(st.session_state.assistants))
    
    with col3:
        st.metric("API Base", st.session_state.api_base.replace('https://', ''))
    
    st.markdown('<div class="section-header">Recent Activity</div>', unsafe_allow_html=True)
    
    if st.session_state.assistants:
        # Show recent assistants
        recent_assistants = sorted(st.session_state.assistants, 
                                 key=lambda x: x.get('updatedAt', ''), reverse=True)[:5]
        
        for assistant in recent_assistants:
            with st.container():
                st.markdown('<div class="assistant-card">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{assistant.get('name', 'Unnamed Assistant')}**")
                    st.write(f"ID: {assistant.get('id', 'N/A')}")
                
                with col2:
                    st.write(f"Created: {format_datetime(assistant.get('createdAt', ''))}")
                
                with col3:
                    st.write(f"Updated: {format_datetime(assistant.get('updatedAt', ''))}")
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No assistants found. Create your first assistant or check your API configuration.")

elif page == "👁️ View Assistants":
    st.markdown('<h1 class="main-header">View Assistants</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="section-header">Your VAPI AI Assistants</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Refresh"):
            load_assistants()
    
    # Load assistants if not already loaded
    if not st.session_state.assistants:
        load_assistants()
    
    if st.session_state.assistants:
        # Create a DataFrame for better display
        assistant_data = []
        for assistant in st.session_state.assistants:
            assistant_data.append({
                'Name': assistant.get('name', 'Unnamed'),
                'ID': assistant.get('id', 'N/A'),
                'Created': format_datetime(assistant.get('createdAt', '')),
                'Updated': format_datetime(assistant.get('updatedAt', '')),
                'First Message': assistant.get('firstMessage', 'N/A')[:50] + '...' if assistant.get('firstMessage') else 'N/A'
            })
        
        df = pd.DataFrame(assistant_data)
        st.dataframe(df, use_container_width=True)
        
        # Detailed view
        st.markdown('<div class="section-header">Detailed View</div>', unsafe_allow_html=True)
        selected_id = st.selectbox("Select an assistant to view details:", 
                                  options=[a['id'] for a in st.session_state.assistants],
                                  format_func=lambda x: next((a['name'] or f"Assistant {x[:8]}..." for a in st.session_state.assistants if a['id'] == x), x))
        
        if selected_id:
            selected_assistant = next((a for a in st.session_state.assistants if a['id'] == selected_id), None)
            if selected_assistant:
                st.json(selected_assistant)
    else:
        st.info("No assistants found. Create your first assistant or check your API configuration.")

elif page == "➕ Create Assistant":
    st.markdown('<h1 class="main-header">Create New Assistant</h1>', unsafe_allow_html=True)
    
    with st.form("create_assistant_form"):
        st.markdown('<div class="section-header">Basic Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Assistant Name*", placeholder="Enter assistant name")
            first_message = st.text_area("First Message", 
                                       placeholder="What should the assistant say first?",
                                       help="This is the first message the assistant will say when a call starts")
        
        with col2:
            first_message_mode = st.selectbox("First Message Mode", 
                                            options=["assistant-speaks-first", 
                                                   "assistant-waits-for-user",
                                                   "assistant-speaks-first-with-model-generated-message"])
            max_duration = st.number_input("Max Duration (seconds)", 
                                         min_value=10, max_value=43200, value=600)
        
        st.markdown('<div class="section-header">Voice Configuration</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            voice_provider = st.selectbox("Voice Provider", 
                                        options=["elevenlabs", "openai", "azure", "playht"])
            voice_id = st.text_input("Voice ID", placeholder="Enter voice ID")
        
        with col2:
            voice_speed = st.slider("Voice Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
            voice_stability = st.slider("Voice Stability", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
        
        st.markdown('<div class="section-header">Model Configuration</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            model_provider = st.selectbox("Model Provider", 
                                        options=["openai", "anthropic", "google", "azure"])
            model_name = st.text_input("Model Name", placeholder="e.g., gpt-4, claude-3-sonnet")
        
        with col2:
            temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
            max_tokens = st.number_input("Max Tokens", min_value=1, max_value=4000, value=1000)
        
        system_message = st.text_area("System Message", 
                                    placeholder="Enter system instructions for the assistant",
                                    help="This defines the assistant's behavior and personality")
        
        st.markdown('<div class="section-header">Advanced Settings</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            background_sound = st.selectbox("Background Sound", 
                                          options=["off", "office", "nature", "cafe"])
            end_call_message = st.text_input("End Call Message", 
                                           placeholder="Message when ending call")
        
        with col2:
            voicemail_message = st.text_input("Voicemail Message", 
                                            placeholder="Message for voicemail")
            end_call_phrases = st.text_area("End Call Phrases (one per line)", 
                                          placeholder="goodbye\ntalk to you later\nend call")
        
        submitted = st.form_submit_button("Create Assistant", type="primary")
        
        if submitted:
            if not name:
                st.error("Assistant name is required!")
            else:
                # Prepare assistant data
                assistant_data = {
                    "name": name,
                    "firstMessage": first_message if first_message else None,
                    "firstMessageMode": first_message_mode,
                    "maxDurationSeconds": max_duration,
                    "voice": {
                        "provider": voice_provider,
                        "voiceId": voice_id if voice_id else None,
                        "speed": voice_speed,
                        "stability": voice_stability
                    },
                    "model": {
                        "provider": model_provider,
                        "model": model_name if model_name else None,
                        "temperature": temperature,
                        "maxTokens": max_tokens,
                        "messages": [
                            {
                                "role": "system",
                                "content": system_message if system_message else "You are a helpful AI assistant."
                            }
                        ] if system_message else None
                    },
                    "backgroundSound": background_sound,
                    "endCallMessage": end_call_message if end_call_message else None,
                    "voicemailMessage": voicemail_message if voicemail_message else None,
                    "endCallPhrases": [phrase.strip() for phrase in end_call_phrases.split('\n') if phrase.strip()] if end_call_phrases else None
                }
                
                # Remove None values
                assistant_data = {k: v for k, v in assistant_data.items() if v is not None}
                assistant_data["voice"] = {k: v for k, v in assistant_data["voice"].items() if v is not None}
                assistant_data["model"] = {k: v for k, v in assistant_data["model"].items() if v is not None}
                
                # Create assistant
                result = make_api_request('POST', '/assistant', assistant_data)
                
                if result:
                    st.success(f"✅ Assistant '{name}' created successfully!")
                    st.json(result)
                    # Refresh assistants list
                    load_assistants()
                else:
                    st.error("Failed to create assistant. Please check your configuration.")

elif page == "✏️ Edit Assistant":
    st.markdown('<h1 class="main-header">Edit Assistant</h1>', unsafe_allow_html=True)
    
    # Load assistants if not already loaded
    if not st.session_state.assistants:
        load_assistants()
    
    if st.session_state.assistants:
        # Select assistant to edit
        selected_id = st.selectbox("Select Assistant to Edit:", 
                                  options=[a['id'] for a in st.session_state.assistants],
                                  format_func=lambda x: next((a['name'] or f"Assistant {x[:8]}..." for a in st.session_state.assistants if a['id'] == x), x))
        
        if selected_id:
            selected_assistant = next((a for a in st.session_state.assistants if a['id'] == selected_id), None)
            
            if selected_assistant:
                with st.form("edit_assistant_form"):
                    st.markdown('<div class="section-header">Basic Information</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Assistant Name*", value=selected_assistant.get('name', ''))
                        first_message = st.text_area("First Message", 
                                                   value=selected_assistant.get('firstMessage', ''))
                    
                    with col2:
                        first_message_mode = st.selectbox("First Message Mode", 
                                                        options=["assistant-speaks-first", 
                                                               "assistant-waits-for-user",
                                                               "assistant-speaks-first-with-model-generated-message"],
                                                        index=0 if selected_assistant.get('firstMessageMode') == 'assistant-speaks-first' else 1)
                        max_duration = st.number_input("Max Duration (seconds)", 
                                                     min_value=10, max_value=43200, 
                                                     value=selected_assistant.get('maxDurationSeconds', 600))
                    
                    # Voice configuration
                    st.markdown('<div class="section-header">Voice Configuration</div>', unsafe_allow_html=True)
                    voice_config = selected_assistant.get('voice', {})
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        voice_provider = st.selectbox("Voice Provider", 
                                                    options=["elevenlabs", "openai", "azure", "playht"],
                                                    index=0)  # Default to first option
                        voice_id = st.text_input("Voice ID", value=voice_config.get('voiceId', ''))
                    
                    with col2:
                        voice_speed = st.slider("Voice Speed", min_value=0.5, max_value=2.0, 
                                              value=voice_config.get('speed', 1.0), step=0.1)
                        voice_stability = st.slider("Voice Stability", min_value=0.0, max_value=1.0, 
                                                  value=voice_config.get('stability', 0.5), step=0.1)
                    
                    # Model configuration
                    st.markdown('<div class="section-header">Model Configuration</div>', unsafe_allow_html=True)
                    model_config = selected_assistant.get('model', {})
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        model_provider = st.selectbox("Model Provider", 
                                                    options=["openai", "anthropic", "google", "azure"],
                                                    index=0)  # Default to first option
                        model_name = st.text_input("Model Name", value=model_config.get('model', ''))
                    
                    with col2:
                        temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, 
                                              value=model_config.get('temperature', 0.7), step=0.1)
                        max_tokens = st.number_input("Max Tokens", min_value=1, max_value=4000, 



                                               value=model_config.get('maxTokens', 1000))
                    
                    # Get system message from model messages
                    system_message = ""
                    if model_config.get('messages'):
                        for msg in model_config['messages']:
                            if msg.get('role') == 'system':
                                system_message = msg.get('content', '')
                                break
                    
                    system_message = st.text_area("System Message", value=system_message)
                    
                    # Advanced settings
                    st.markdown('<div class="section-header">Advanced Settings</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        background_sound = st.selectbox("Background Sound", 
                                                      options=["off", "office", "nature", "cafe"],
                                                      index=0)  # Default to first option
                        end_call_message = st.text_input("End Call Message", 
                                                       value=selected_assistant.get('endCallMessage', ''))
                    
                    with col2:
                        voicemail_message = st.text_input("Voicemail Message", 
                                                        value=selected_assistant.get('voicemailMessage', ''))
                        end_call_phrases_text = '\n'.join(selected_assistant.get('endCallPhrases', []))
                        end_call_phrases = st.text_area("End Call Phrases (one per line)", 
                                                      value=end_call_phrases_text)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submitted = st.form_submit_button("Update Assistant", type="primary")
                    with col2:
                        delete_clicked = st.form_submit_button("Delete Assistant", type="secondary")
                    
                    if submitted:
                        if not name:
                            st.error("Assistant name is required!")
                        else:
                            # Prepare update data
                            update_data = {
                                "name": name,
                                "firstMessage": first_message if first_message else None,
                                "firstMessageMode": first_message_mode,
                                "maxDurationSeconds": max_duration,
                                "voice": {
                                    "provider": voice_provider,
                                    "voiceId": voice_id if voice_id else None,
                                    "speed": voice_speed,
                                    "stability": voice_stability
                                },
                                "model": {
                                    "provider": model_provider,
                                    "model": model_name if model_name else None,
                                    "temperature": temperature,
                                    "maxTokens": max_tokens,
                                    "messages": [
                                        {
                                            "role": "system",
                                            "content": system_message if system_message else "You are a helpful AI assistant."
                                        }
                                    ] if system_message else None
                                },
                                "backgroundSound": background_sound,
                                "endCallMessage": end_call_message if end_call_message else None,
                                "voicemailMessage": voicemail_message if voicemail_message else None,
                                "endCallPhrases": [phrase.strip() for phrase in end_call_phrases.split('\n') if phrase.strip()] if end_call_phrases else None
                            }
                            
                            # Remove None values
                            update_data = {k: v for k, v in update_data.items() if v is not None}
                            update_data["voice"] = {k: v for k, v in update_data["voice"].items() if v is not None}
                            update_data["model"] = {k: v for k, v in update_data["model"].items() if v is not None}
                            
                            # Update assistant
                            result = make_api_request('PATCH', f'/assistant/{selected_id}', update_data)
                            
                            if result:
                                st.success(f"✅ Assistant '{name}' updated successfully!")
                                st.json(result)
                                # Refresh assistants list
                                load_assistants()
                            else:
                                st.error("Failed to update assistant. Please check your configuration.")
                    
                    if delete_clicked:
                        st.warning("⚠️ Are you sure you want to delete this assistant?")
                        if st.button("Yes, Delete Assistant", type="secondary"):
                            result = make_api_request('DELETE', f'/assistant/{selected_id}')
                            if result is not None:  # DELETE returns empty response on success
                                st.success(f"✅ Assistant deleted successfully!")
                                # Refresh assistants list
                                load_assistants()
                                st.rerun()
                            else:
                                st.error("Failed to delete assistant.")
    else:
        st.info("No assistants found. Create your first assistant or check your API configuration.")

elif page == "⚙️ Settings":
    st.markdown('<h1 class="main-header">Settings</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">API Configuration</div>', unsafe_allow_html=True)
    
    with st.form("settings_form"):
        api_key = st.text_input("VAPI API Key", 
                               value=st.session_state.api_key, 
                               type="password",
                               help="Your VAPI AI API key from dashboard.vapi.ai")
        
        api_base = st.text_input("API Base URL", 
                                value=st.session_state.api_base,
                                help="Base URL for VAPI AI API (default: https://api.vapi.ai)")
        
        org_id = st.text_input("Organization ID (Optional)", 
                              value=os.getenv('VAPI_ORG_ID', ''),
                              help="Your organization ID if applicable")
        
        submitted = st.form_submit_button("Save Settings", type="primary")
        
        if submitted:
            st.session_state.api_key = api_key
            st.session_state.api_base = api_base
            
            # Test API connection
            if api_key:
                test_result = make_api_request('GET', '/assistant?limit=1')
                if test_result is not None:
                    st.success("✅ API connection successful!")
                    # Load assistants with new settings
                    load_assistants()
                else:
                    st.error("❌ API connection failed. Please check your API key.")
            else:
                st.warning("⚠️ API key is required for the application to work.")
    
    st.markdown('<div class="section-header">Environment Setup</div>', unsafe_allow_html=True)
    
    st.info("""
   
    3. Restart the application
    """)
    
    st.markdown('<div class="section-header">Application Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
        **Current Configuration:**
        - API Base: {st.session_state.api_base}
        - API Key: {'✅ Set' if st.session_state.api_key else '❌ Not set'}
        - Total Assistants: {len(st.session_state.assistants)}
        """)
    
    with col2:
        st.info("""
        **Features:**
        - ✅ View all assistants
        - ✅ Create new assistants
        - ✅ Edit existing assistants
        - ✅ Delete assistants
        - ✅ API configuration
        """)
    
    st.markdown('<div class="section-header">About</div>', unsafe_allow_html=True)
    st.markdown("""
   
    
    This application provides a user-friendly interface to:
    - Create and configure voice AI assistants
    - Manage assistant settings and parameters
    - View and edit existing assistants
    - Configure API connections
    
    Built by The ATM Agency.
    """)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; margin-top: 2rem;">'
    'VAPI AI Assistant Manager | Built with Streamlit'
    '</div>', 
    unsafe_allow_html=True
)

