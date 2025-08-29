"""
VAPI AI Client Module
Handles all API interactions with VAPI AI platform
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime


class VAPIClient:
    """Client for interacting with VAPI AI API"""
    
    def __init__(self, api_key: str, api_base: str = "https://api.vapi.ai"):
        """
        Initialize VAPI client
        
        Args:
            api_key: VAPI AI API key
            api_base: Base URL for VAPI AI API
        """
        self.api_key = api_key
        self.api_base = api_base.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Any]:
        """
        Make HTTP request to VAPI AI API
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint
            data: Request data for POST/PATCH requests
            
        Returns:
            Response data or None if error
        """
        url = f"{self.api_base}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method == 'PATCH':
                response = requests.patch(url, headers=self.headers, json=data)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Handle successful responses
            if response.status_code in [200, 201]:
                return response.json() if response.content else {}
            elif response.status_code == 204:  # No content (successful DELETE)
                return {}
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Connection Error: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test API connection
        
        Returns:
            True if connection successful, False otherwise
        """
        result = self._make_request('GET', '/assistant?limit=1')
        return result is not None
    
    def list_assistants(self, limit: int = 100) -> Optional[List[Dict]]:
        """
        List all assistants
        
        Args:
            limit: Maximum number of assistants to return
            
        Returns:
            List of assistant objects or None if error
        """
        return self._make_request('GET', f'/assistant?limit={limit}')
    
    def get_assistant(self, assistant_id: str) -> Optional[Dict]:
        """
        Get specific assistant by ID
        
        Args:
            assistant_id: Assistant ID
            
        Returns:
            Assistant object or None if error
        """
        return self._make_request('GET', f'/assistant/{assistant_id}')
    
    def create_assistant(self, assistant_data: Dict) -> Optional[Dict]:
        """
        Create new assistant
        
        Args:
            assistant_data: Assistant configuration data
            
        Returns:
            Created assistant object or None if error
        """
        return self._make_request('POST', '/assistant', assistant_data)
    
    def update_assistant(self, assistant_id: str, assistant_data: Dict) -> Optional[Dict]:
        """
        Update existing assistant
        
        Args:
            assistant_id: Assistant ID
            assistant_data: Updated assistant configuration data
            
        Returns:
            Updated assistant object or None if error
        """
        return self._make_request('PATCH', f'/assistant/{assistant_id}', assistant_data)
    
    def delete_assistant(self, assistant_id: str) -> bool:
        """
        Delete assistant
        
        Args:
            assistant_id: Assistant ID
            
        Returns:
            True if successful, False otherwise
        """
        result = self._make_request('DELETE', f'/assistant/{assistant_id}')
        return result is not None
    
    def list_calls(self, assistant_id: Optional[str] = None, limit: int = 100) -> Optional[List[Dict]]:
        """
        List calls, optionally filtered by assistant
        
        Args:
            assistant_id: Optional assistant ID to filter by
            limit: Maximum number of calls to return
            
        Returns:
            List of call objects or None if error
        """
        endpoint = f'/call?limit={limit}'
        if assistant_id:
            endpoint += f'&assistantId={assistant_id}'
        return self._make_request('GET', endpoint)
    
    def create_call(self, call_data: Dict) -> Optional[Dict]:
        """
        Create a new call
        
        Args:
            call_data: Call configuration data
            
        Returns:
            Created call object or None if error
        """
        return self._make_request('POST', '/call', call_data)


def validate_assistant_data(data: Dict) -> Dict:
    """
    Validate and clean assistant data before sending to API
    
    Args:
        data: Raw assistant data
        
    Returns:
        Cleaned assistant data
    """
    # Remove empty strings and None values
    def clean_dict(d):
        if isinstance(d, dict):
            return {k: clean_dict(v) for k, v in d.items() if v is not None and v != ""}
        elif isinstance(d, list):
            return [clean_dict(item) for item in d if item is not None and item != ""]
        else:
            return d
    
    cleaned_data = clean_dict(data)
    
    # Ensure required nested structures exist
    if 'voice' in cleaned_data and cleaned_data['voice']:
        voice_data = cleaned_data['voice']
        # Remove empty voice configuration
        if not any(voice_data.values()):
            del cleaned_data['voice']
    
    if 'model' in cleaned_data and cleaned_data['model']:
        model_data = cleaned_data['model']
        # Remove empty model configuration
        if not any(model_data.values()):
            del cleaned_data['model']
    
    return cleaned_data


def format_datetime(dt_string: str) -> str:
    """
    Format datetime string for display
    
    Args:
        dt_string: ISO datetime string
        
    Returns:
        Formatted datetime string
    """
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except (ValueError, AttributeError):
        return dt_string


def get_assistant_summary(assistant: Dict) -> Dict:
    """
    Get summary information for an assistant
    
    Args:
        assistant: Assistant object
        
    Returns:
        Summary dictionary
    """
    return {
        'id': assistant.get('id', 'N/A'),
        'name': assistant.get('name', 'Unnamed Assistant'),
        'created': format_datetime(assistant.get('createdAt', '')),
        'updated': format_datetime(assistant.get('updatedAt', '')),
        'first_message': assistant.get('firstMessage', 'N/A'),
        'voice_provider': assistant.get('voice', {}).get('provider', 'N/A'),
        'model_provider': assistant.get('model', {}).get('provider', 'N/A'),
        'model_name': assistant.get('model', {}).get('model', 'N/A')
    }


# Default assistant template
DEFAULT_ASSISTANT_TEMPLATE = {
    "name": "New Assistant",
    "firstMessage": "Hello! How can I help you today?",
    "firstMessageMode": "assistant-speaks-first",
    "maxDurationSeconds": 600,
    "voice": {
        "provider": "elevenlabs",
        "speed": 1.0,
        "stability": 0.5
    },
    "model": {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "maxTokens": 1000,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Be friendly, concise, and helpful in your responses."
            }
        ]
    },
    "backgroundSound": "off"
}


# Voice provider options
VOICE_PROVIDERS = {
    "elevenlabs": {
        "name": "ElevenLabs",
        "description": "High-quality AI voices with emotional range"
    },
    "openai": {
        "name": "OpenAI",
        "description": "OpenAI's text-to-speech models"
    },
    "azure": {
        "name": "Azure Cognitive Services",
        "description": "Microsoft's speech synthesis service"
    },
    "playht": {
        "name": "PlayHT",
        "description": "AI voice generation platform"
    }
}


# Model provider options
MODEL_PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        "description": "OpenAI's language models"
    },
    "anthropic": {
        "name": "Anthropic",
        "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
        "description": "Anthropic's Claude models"
    },
    "google": {
        "name": "Google",
        "models": ["gemini-pro", "gemini-pro-vision"],
        "description": "Google's Gemini models"
    },
    "azure": {
        "name": "Azure OpenAI",
        "models": ["gpt-4", "gpt-35-turbo"],
        "description": "Azure-hosted OpenAI models"
    }
}

