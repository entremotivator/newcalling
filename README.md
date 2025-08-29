# VAPI AI Assistant Manager

A comprehensive Streamlit application for managing VAPI AI voice assistants with a user-friendly interface.

## Features

🤖 **Assistant Management**
- Create new voice AI assistants with custom configurations
- View all existing assistants in a detailed dashboard
- Edit assistant settings including voice, model, and behavior parameters
- Delete assistants with confirmation prompts

⚙️ **Configuration Options**
- Voice providers: ElevenLabs, OpenAI, Azure, PlayHT
- Model providers: OpenAI GPT-4, Anthropic Claude, Google Gemini, Azure OpenAI
- Advanced settings: background sounds, call duration, end call phrases
- System message customization for assistant personality

🔧 **API Integration**
- Direct integration with VAPI AI platform
- Real-time connection testing
- Secure API key management
- Organization ID support

📊 **Dashboard & Analytics**
- Overview of all assistants and their status
- Connection status monitoring
- Quick stats and recent activity
- Responsive design for desktop and mobile

## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Settings Page
![Settings](screenshots/settings.png)

### Create Assistant
![Create Assistant](screenshots/create_assistant.png)

## Installation

### Prerequisites
- Python 3.11 or higher
- VAPI AI account and API key

### Quick Start

1. **Clone or download the application files**
   ```bash
   # If you have the files, navigate to the directory
   cd vapi_streamlit_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional)**
   Create a `.env` file in the project directory:
   ```env
   VAPI_API_KEY=your_api_key_here
   VAPI_API_BASE=https://api.vapi.ai
   VAPI_ORG_ID=your_org_id_here
   ```

4. **Run the application**
   ```bash
   streamlit run app_improved.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## Configuration

### Getting Your API Key

1. Go to [dashboard.vapi.ai](https://dashboard.vapi.ai)
2. Sign in to your account
3. Navigate to Settings or API Keys section
4. Copy your API key

### API Configuration

You can configure the API settings in two ways:

1. **Through the Settings page** (recommended for testing)
   - Navigate to Settings in the application
   - Enter your API key, base URL, and organization ID
   - Click "Save Settings" and test the connection

2. **Through environment variables** (recommended for production)
   - Create a `.env` file with your credentials
   - Restart the application

## Usage Guide

### 1. Initial Setup
- Start the application and navigate to Settings
- Enter your VAPI AI API key
- Test the connection to ensure it's working

### 2. Creating Assistants
- Go to "Create Assistant" page
- Fill in the basic information (name, first message)
- Configure voice settings (provider, voice ID, speed, stability)
- Set up model configuration (provider, model, temperature, tokens)
- Add system message to define assistant personality
- Configure advanced settings as needed
- Click "Create Assistant"

### 3. Managing Assistants
- Use "View Assistants" to see all your assistants
- Select an assistant to view detailed information
- Use "Edit Assistant" to modify existing assistants
- Delete assistants when no longer needed

### 4. Dashboard Overview
- Monitor API connection status
- View total number of assistants
- See recent activity and updates
- Quick access to all features

## File Structure

```
vapi_streamlit_app/
├── app_improved.py          # Main Streamlit application
├── vapi_client.py          # VAPI AI API client module
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # This documentation
└── screenshots/           # Application screenshots
```

## API Client Module

The `vapi_client.py` module provides a clean interface to the VAPI AI API:

- `VAPIClient`: Main client class for API interactions
- `validate_assistant_data()`: Data validation and cleaning
- `get_assistant_summary()`: Assistant information formatting
- Provider configurations and templates

## Dependencies

- **streamlit**: Web application framework
- **requests**: HTTP client for API calls
- **python-dotenv**: Environment variable management
- **pandas**: Data manipulation and display

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Verify your API key is correct
   - Check that the API base URL is `https://api.vapi.ai`
   - Ensure your VAPI AI account is active

2. **Application Won't Start**
   - Check that all dependencies are installed
   - Verify Python version is 3.11 or higher
   - Look for syntax errors in the console output

3. **Features Not Working**
   - Ensure API connection is established
   - Check browser console for JavaScript errors
   - Try refreshing the page

### Error Messages

- **"API not connected"**: Configure your API key in Settings
- **"No assistants found"**: Create your first assistant or check API connection
- **"Failed to create/update assistant"**: Check your API key and assistant configuration

## Development

### Running in Development Mode

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
streamlit run app_improved.py --server.runOnSave true
```

### Code Structure

The application follows a modular structure:
- Main UI components in `app_improved.py`
- API interactions in `vapi_client.py`
- Configuration through environment variables
- Session state management for user data

## Deployment

### Local Deployment

The application runs locally on `http://localhost:8501` by default.

### Production Deployment

For production deployment, consider:
- Using environment variables for API keys
- Setting up HTTPS
- Configuring proper error handling
- Adding authentication if needed

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_improved.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Security Considerations

- Never commit API keys to version control
- Use environment variables for sensitive data
- Regularly rotate API keys
- Monitor API usage and costs
- Implement proper error handling

## Support

For issues related to:
- **VAPI AI API**: Contact VAPI AI support
- **Application bugs**: Check the troubleshooting section
- **Feature requests**: Consider contributing to the project

## License

This project is provided as-is for educational and development purposes.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Changelog

### Version 1.0.0
- Initial release
- Full CRUD operations for assistants
- API configuration interface
- Dashboard with metrics
- Responsive design
- Error handling and validation

---

**Built with ❤️ using Streamlit and the VAPI AI API**

