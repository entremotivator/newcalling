@echo off
REM VAPI AI Assistant Manager - Windows Installation Script
REM This script sets up the application environment and dependencies

echo 🤖 VAPI AI Assistant Manager - Windows Installation Script
echo ===========================================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.11 or higher.
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✅ pip found

REM Install dependencies
echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies. Please check the error messages above.
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!

REM Check if .env file exists, if not create from example
if not exist ".env" (
    if exist ".env.example" (
        echo.
        echo 📝 Creating .env file from template...
        copy ".env.example" ".env" >nul
        echo ✅ .env file created. Please edit it with your API credentials.
        echo.
        echo ⚠️  IMPORTANT: Edit the .env file and add your VAPI AI API key:
        echo    notepad .env
    )
) else (
    echo ✅ .env file already exists.
)

echo.
echo 🎉 Installation completed successfully!
echo.
echo 🚀 To start the application:
echo    streamlit run app_improved.py
echo.
echo 📖 Then open your browser to: http://localhost:8501
echo.
echo ⚙️  Don't forget to:
echo    1. Get your API key from https://dashboard.vapi.ai
echo    2. Configure it in the Settings page or .env file
echo    3. Test the connection before creating assistants
echo.
echo 📚 For more information, see README.md and DEPLOYMENT.md
echo.
echo Happy voice assistant building! 🤖✨
echo.
pause

