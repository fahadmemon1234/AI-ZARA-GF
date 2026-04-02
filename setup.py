"""
ZARA - Advanced Real-time Intelligent Assistant
Setup Script - Automated installation and configuration
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}  {text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def print_step(step_num, text):
    print(f"\n{Colors.OKBLUE}[Step {step_num}/6]{Colors.ENDC} {Colors.BOLD}{text}{Colors.ENDC}")

# ============== Step 1: Create Directories ==============

def create_directories():
    """Create all required directories."""
    print_step(1, "Creating required directories...")
    
    directories = [
        'modules',
        'data',
        'public',
        'data/screenshots',
        'data/exports'
    ]
    
    created = 0
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print_success(f"Created: {directory}/")
            created += 1
        else:
            print_info(f"Already exists: {directory}/")
    
    print_success(f"Directories ready! ({created} created)")
    return True

# ============== Step 2: Initialize Data Files ==============

def initialize_data_files():
    """Create data files with empty structures."""
    print_step(2, "Initializing data files...")
    
    # Memory file
    memory_file = Path('data/memory.json')
    if not memory_file.exists():
        memory_data = {
            "entries": {},
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "count": 0
        }
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, indent=2, ensure_ascii=False)
        print_success("Created: data/memory.json")
    else:
        print_info("Already exists: data/memory.json")
    
    # Conversations file
    conversations_file = Path('data/conversations.json')
    if not conversations_file.exists():
        conversations_data = {
            "conversations": [],
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "count": 0
        }
        with open(conversations_file, 'w', encoding='utf-8') as f:
            json.dump(conversations_data, f, indent=2, ensure_ascii=False)
        print_success("Created: data/conversations.json")
    else:
        print_info("Already exists: data/conversations.json")
    
    print_success("Data files initialized!")
    return True

# ============== Step 3: Check & Install Dependencies ==============

def check_and_install_dependencies():
    """Check if pip packages are installed, install missing ones."""
    print_step(3, "Checking Python dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'python-dotenv',
        'anthropic',
        'SpeechRecognition',
        'pyttsx3',
        'pyaudio',
        'psutil',
        'pyautogui',
        'screen-brightness-control',
        'pycaw',
        'comtypes',
        'pywhatkit',
        'pillow',
        'pytesseract',
        'PyPDF2',
        'fpdf2',
        'requests',
        'beautifulsoup4',
        'pyperclip',
        'pygetwindow',
        'keyboard',
        'mouse',
        'pywin32',
        'newsapi-python',
        'aiofiles',
        'python-multipart'
    ]
    
    installed = 0
    missing = []
    
    for package in required_packages:
        try:
            # Special case for some packages with different import names
            if package == 'pywin32':
                __import__('win32api')
            elif package == 'beautifulsoup4':
                __import__('bs4')
            elif package == 'Pillow':
                __import__('PIL')
            elif package == 'screen-brightness-control':
                __import__('screen_brightness_control')
            elif package == 'python-dotenv':
                __import__('dotenv')
            elif package == 'python-multipart':
                __import__('multipart')
            else:
                __import__(package.replace('-', '_'))
            
            installed += 1
            print_success(f"Installed: {package}")
            
        except ImportError:
            missing.append(package)
            print_warning(f"Missing: {package}")
    
    if missing:
        print_warning(f"\n{len(missing)} packages missing. Installing...")
        for package in missing:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
                print_success(f"Installed: {package}")
            except subprocess.CalledProcessError:
                print_error(f"Failed to install: {package}")
    
    print_success(f"Dependencies check complete! ({installed}/{len(required_packages)} already installed)")
    return True

# ============== Step 4: Check Tesseract OCR ==============

def check_tesseract():
    """Check if tesseract-ocr is installed."""
    print_step(4, "Checking Tesseract OCR...")
    
    try:
        # Try to find tesseract
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print_success(f"Tesseract OCR found: {version}")
            return True
        else:
            raise FileNotFoundError
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print_warning("Tesseract OCR not found!")
        print_info("\nTo install Tesseract OCR:")
        print_info("  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print_info("  Add to PATH after installation")
        print_info("\nOCR features will work after installation.")
        print_info("Other features will work normally without Tesseract.")
        return False

# ============== Step 5: Setup .env File ==============

def setup_env_file():
    """Copy .env.example to .env if .env doesn't exist."""
    print_step(5, "Setting up environment file...")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print_success("Created: .env (from .env.example)")
            print_warning("\n⚠️  IMPORTANT: Edit .env and add your API keys!")
            print_info("   Get FREE Anthropic API key from: https://console.anthropic.com")
            print_info("   Add to .env: ANTHROPIC_API_KEY=your_key_here")
        else:
            # Create basic .env
            env_content = """# ARIA - Environment Variables

# Anthropic API Key (REQUIRED for AI features)
# Get FREE key from: https://console.anthropic.com
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional API Keys
NEWS_API_KEY=
WEATHER_API_KEY=

# Server Configuration
PORT=8000
HOST=127.0.0.1
"""
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            print_success("Created: .env (basic template)")
            print_warning("\n⚠️  IMPORTANT: Edit .env and add your API keys!")
    else:
        print_info(".env already exists")
    
    return True

# ============== Step 6: Final Verification ==============

def final_verification():
    """Final verification of setup."""
    print_step(6, "Running final verification...")
    
    checks = [
        ('modules/', 'Modules directory'),
        ('data/', 'Data directory'),
        ('public/', 'Public directory'),
        ('main.py', 'Main server file'),
        ('config.py', 'Configuration file'),
        ('requirements.txt', 'Dependencies file'),
    ]
    
    all_ok = True
    for path, name in checks:
        if os.path.exists(path):
            print_success(f"Found: {name}")
        else:
            print_error(f"Missing: {name}")
            all_ok = False
    
    return all_ok

# ============== Main Setup ==============

def main():
    """Main setup function."""
    print_header("🤖 ARIA - Setup Wizard")
    print_info("Advanced Real-time Intelligent Assistant")
    print_info("This script will set up ARIA on your system\n")
    
    # Get base directory
    base_dir = Path(__file__).parent
    os.chdir(base_dir)
    
    steps = [
        create_directories,
        initialize_data_files,
        check_and_install_dependencies,
        check_tesseract,
        setup_env_file,
        final_verification
    ]
    
    success = 0
    failed = 0
    
    for step in steps:
        try:
            if step():
                success += 1
            else:
                failed += 1
        except Exception as e:
            print_error(f"Step failed: {str(e)}")
            failed += 1
    
    # Summary
    print_header("Setup Summary")
    print_success(f"Successful steps: {success}/{len(steps)}")
    
    if failed > 0:
        print_warning(f"Failed steps: {failed}/{len(steps)}")
    
    print("\n" + "="*60)
    print(f"{Colors.OKGREEN}{Colors.BOLD}🎉 Setup Complete!{Colors.ENDC}")
    print("="*60)
    print(f"\n{Colors.OKBLUE}Next steps:{Colors.ENDC}")
    print("  1. Edit .env and add your ANTHROPIC_API_KEY")
    print("     Get FREE key: https://console.anthropic.com")
    print("\n  2. (Optional) Install Tesseract OCR for OCR features")
    print("     Windows: https://github.com/UB-Mannheim/tesseract/wiki")
    print("\n  3. Run ARIA:")
    print(f"     {Colors.OKGREEN}python main.py{Colors.ENDC}")
    print("\n  4. Open browser:")
    print(f"     {Colors.OKCYAN}http://localhost:8000{Colors.ENDC}")
    print("\n" + "="*60)
    
    return failed == 0

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed with error: {str(e)}")
        sys.exit(1)
