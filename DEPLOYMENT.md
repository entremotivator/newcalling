# Deployment Guide - VAPI AI Assistant Manager

This guide provides step-by-step instructions for deploying the VAPI AI Assistant Manager application.

## Quick Start (Local Development)

### 1. Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- VAPI AI account with API key

### 2. Installation Steps

```bash
# 1. Navigate to the application directory
cd vapi_streamlit_app

# 2. Install required packages
pip install -r requirements.txt

# 3. (Optional) Set up environment variables
cp .env.example .env
# Edit .env file with your API credentials

# 4. Run the application
streamlit run app_improved.py

# 5. Open your browser to http://localhost:8501
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Required: Your VAPI AI API key
VAPI_API_KEY=your_api_key_from_dashboard_vapi_ai

# Optional: API base URL (default: https://api.vapi.ai)
VAPI_API_BASE=https://api.vapi.ai

# Optional: Organization ID if you have one
VAPI_ORG_ID=your_organization_id
```

## Production Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. **Prepare your repository**
   ```bash
   # Ensure all files are in your repository
   git add .
   git commit -m "Add VAPI AI Assistant Manager"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the repository and branch
   - Set the main file path: `app_improved.py`
   - Add environment variables in the advanced settings
   - Deploy!

3. **Configure secrets**
   In Streamlit Cloud, add these secrets:
   ```toml
   VAPI_API_KEY = "your_api_key_here"
   VAPI_API_BASE = "https://api.vapi.ai"
   VAPI_ORG_ID = "your_org_id_here"
   ```

### Option 2: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   # Copy requirements and install dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application files
   COPY . .

   # Expose port
   EXPOSE 8501

   # Health check
   HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

   # Run the application
   CMD ["streamlit", "run", "app_improved.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run**
   ```bash
   # Build the image
   docker build -t vapi-assistant-manager .

   # Run the container
   docker run -p 8501:8501 \
     -e VAPI_API_KEY=your_api_key \
     -e VAPI_API_BASE=https://api.vapi.ai \
     vapi-assistant-manager
   ```

### Option 3: VPS/Server Deployment

1. **Server setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python and pip
   sudo apt install python3.11 python3.11-pip -y

   # Install git
   sudo apt install git -y
   ```

2. **Application deployment**
   ```bash
   # Clone or upload your application
   git clone your-repository-url
   cd vapi_streamlit_app

   # Install dependencies
   pip3.11 install -r requirements.txt

   # Set up environment variables
   nano .env
   # Add your API credentials

   # Run with nohup for background execution
   nohup streamlit run app_improved.py --server.port 8501 --server.address 0.0.0.0 &
   ```

3. **Set up reverse proxy (Nginx)**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

### Option 4: Heroku Deployment

1. **Prepare Heroku files**
   
   Create `Procfile`:
   ```
   web: streamlit run app_improved.py --server.port=$PORT --server.address=0.0.0.0
   ```

   Create `runtime.txt`:
   ```
   python-3.11.0
   ```

2. **Deploy to Heroku**
   ```bash
   # Install Heroku CLI and login
   heroku login

   # Create Heroku app
   heroku create your-app-name

   # Set environment variables
   heroku config:set VAPI_API_KEY=your_api_key
   heroku config:set VAPI_API_BASE=https://api.vapi.ai

   # Deploy
   git push heroku main
   ```

## Configuration for Production

### Security Settings

1. **Environment Variables**
   - Never commit API keys to version control
   - Use secure environment variable management
   - Rotate API keys regularly

2. **HTTPS Configuration**
   - Use SSL certificates for production
   - Configure secure headers
   - Enable HSTS if possible

### Performance Optimization

1. **Streamlit Configuration**
   Create `.streamlit/config.toml`:
   ```toml
   [server]
   port = 8501
   address = "0.0.0.0"
   maxUploadSize = 200
   enableCORS = false
   enableXsrfProtection = true

   [browser]
   gatherUsageStats = false
   serverAddress = "your-domain.com"
   serverPort = 80

   [theme]
   primaryColor = "#1f77b4"
   backgroundColor = "#ffffff"
   secondaryBackgroundColor = "#f0f2f6"
   textColor = "#262730"
   ```

2. **Caching**
   - The application uses Streamlit's session state for caching
   - API responses are cached during the session
   - Consider implementing Redis for multi-user deployments

## Monitoring and Maintenance

### Health Checks

1. **Application Health**
   ```bash
   # Check if Streamlit is running
   curl http://localhost:8501/_stcore/health

   # Check API connectivity
   curl -H "Authorization: Bearer YOUR_API_KEY" https://api.vapi.ai/assistant?limit=1
   ```

2. **Log Monitoring**
   ```bash
   # View Streamlit logs
   tail -f ~/.streamlit/logs/streamlit.log

   # Monitor system resources
   htop
   ```

### Backup and Recovery

1. **Configuration Backup**
   - Backup environment variables
   - Document API key rotation procedures
   - Keep deployment scripts versioned

2. **Data Considerations**
   - The application doesn't store persistent data locally
   - All data is managed through VAPI AI API
   - Ensure API key access for recovery

## Troubleshooting Deployment Issues

### Common Problems

1. **Port Already in Use**
   ```bash
   # Find process using port 8501
   lsof -i :8501
   
   # Kill the process
   kill -9 PID
   ```

2. **Permission Denied**
   ```bash
   # Fix file permissions
   chmod +x app_improved.py
   
   # Install packages with user flag
   pip install --user -r requirements.txt
   ```

3. **Module Not Found**
   ```bash
   # Verify Python path
   which python3.11
   
   # Install in correct environment
   python3.11 -m pip install -r requirements.txt
   ```

### Performance Issues

1. **Memory Usage**
   - Monitor RAM usage during operation
   - Consider upgrading server resources
   - Implement session cleanup if needed

2. **API Rate Limits**
   - Monitor VAPI AI API usage
   - Implement request throttling if needed
   - Cache responses appropriately

## Scaling Considerations

### Multi-User Deployment

1. **Session Management**
   - Each user gets isolated session state
   - API keys can be user-specific
   - Consider implementing user authentication

2. **Load Balancing**
   - Use multiple Streamlit instances
   - Implement sticky sessions
   - Consider container orchestration

### Enterprise Deployment

1. **Authentication**
   - Integrate with SSO providers
   - Implement role-based access control
   - Add audit logging

2. **Infrastructure**
   - Use container orchestration (Kubernetes)
   - Implement CI/CD pipelines
   - Set up monitoring and alerting

## Support and Maintenance

### Regular Maintenance Tasks

1. **Weekly**
   - Check application health
   - Monitor API usage
   - Review error logs

2. **Monthly**
   - Update dependencies
   - Rotate API keys
   - Review performance metrics

3. **Quarterly**
   - Security audit
   - Backup verification
   - Capacity planning

### Getting Help

- **Application Issues**: Check the README troubleshooting section
- **VAPI AI API**: Contact VAPI AI support
- **Deployment Issues**: Review this guide and check logs

---

**Need help with deployment? Check the logs, verify your API key, and ensure all dependencies are installed correctly.**

