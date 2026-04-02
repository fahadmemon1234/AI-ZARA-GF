"""
ZARA - Advanced Real-time Intelligent Assistant
Modules Package - Import and expose all module classes
"""

# System Control
from .system_control import SystemControl

# Application Management
from .app_manager import AppManager

# Window Management
from .window_manager import WindowManager

# Audio Control
from .volume_control import VolumeControl
from .brightness import BrightnessControl

# Media & Entertainment
from .media_player import MediaPlayer

# Input Automation
from .mouse_keyboard import MouseKeyboard

# File Operations
from .file_manager import FileManager

# Screenshot & OCR
from .screenshot import ScreenshotTool

# Image Processing
from .image_tools import ImageTools

# PDF Tools
from .pdf_tools import PDFTools

# Web & Search
from .google_search import GoogleSearch

# News
from .news_fetcher import NewsFetcher

# WhatsApp Automation
from .whatsapp import WhatsAppAutomation

# Memory & Storage
from .memory_manager import MemoryManager

# Voice Engine
from .voice_engine import VoiceEngine

# Desktop Management
from .desktop_manager import DesktopManager

# AI Brain
from .ai_brain import AIBrain

# Command Router
from .command_router import CommandRouter

# Multi-API Manager (NEW - All AI APIs)
from .multi_api_manager import MultiAPIManager

# ============== All Exports ==============

__all__ = [
    # System
    'SystemControl',
    
    # Apps & Windows
    'AppManager',
    'WindowManager',
    'DesktopManager',
    
    # Audio & Display
    'VolumeControl',
    'BrightnessControl',
    
    # Media
    'MediaPlayer',
    
    # Input
    'MouseKeyboard',
    
    # Files
    'FileManager',
    
    # Screenshots & Images
    'ScreenshotTool',
    'ImageTools',
    
    # PDF
    'PDFTools',
    
    # Web & Search
    'GoogleSearch',
    
    # News
    'NewsFetcher',
    
    # WhatsApp
    'WhatsAppAutomation',
    
    # Memory
    'MemoryManager',
    
    # Voice
    'VoiceEngine',
    
    # AI
    'AIBrain',
    'CommandRouter',
    'MultiAPIManager',
]

# ============== Package Info ==============

__version__ = '1.0.0'
__author__ = 'ARIA Team'
__description__ = 'ARIA - Advanced Real-time Intelligent Assistant Modules'

# ============== Helper Functions ==============

def get_all_modules() -> list:
    """Get list of all available module names."""
    return __all__.copy()

def get_module_info(module_name: str) -> dict:
    """
    Get information about a specific module.
    
    Args:
        module_name: Name of the module
        
    Returns:
        Dictionary with module info
    """
    module_classes = {
        'SystemControl': {
            'description': 'System power control and status monitoring',
            'capabilities': ['shutdown', 'restart', 'sleep', 'lock', 'battery', 'cpu', 'ram', 'network']
        },
        'AppManager': {
            'description': 'Application launch and management',
            'capabilities': ['open_app', 'close_app', 'list_running_apps', 'focus_app']
        },
        'WindowManager': {
            'description': 'Window control and manipulation',
            'capabilities': ['minimize', 'maximize', 'close', 'snap', 'virtual_desktops']
        },
        'VolumeControl': {
            'description': 'Audio volume control using pycaw',
            'capabilities': ['get_volume', 'set_volume', 'mute', 'toggle_mute']
        },
        'BrightnessControl': {
            'description': 'Screen brightness control',
            'capabilities': ['get_brightness', 'set_brightness', 'increase', 'decrease']
        },
        'MediaPlayer': {
            'description': 'Media playback control',
            'capabilities': ['youtube', 'spotify', 'media_controls', 'zoom']
        },
        'MouseKeyboard': {
            'description': 'Mouse and keyboard automation',
            'capabilities': ['move', 'click', 'type', 'hotkey', 'shortcuts']
        },
        'FileManager': {
            'description': 'File and folder operations',
            'capabilities': ['create', 'delete', 'move', 'copy', 'zip', 'unzip', 'search']
        },
        'ScreenshotTool': {
            'description': 'Screenshot capture and OCR',
            'capabilities': ['screenshot', 'region_capture', 'ocr', 'screen_reader']
        },
        'ImageTools': {
            'description': 'Image processing and conversion',
            'capabilities': ['image_to_pdf', 'ocr', 'resize', 'convert', 'compress']
        },
        'PDFTools': {
            'description': 'PDF manipulation',
            'capabilities': ['merge', 'split', 'read', 'extract_pages', 'info']
        },
        'GoogleSearch': {
            'description': 'Web search and information',
            'capabilities': ['search', 'weather', 'datetime', 'open_website']
        },
        'NewsFetcher': {
            'description': 'News headlines and articles',
            'capabilities': ['top_news', 'topic_news', 'pakistan_news', 'summarize']
        },
        'WhatsAppAutomation': {
            'description': 'WhatsApp Web automation',
            'capabilities': ['send_message', 'send_file', 'call', 'group_message']
        },
        'MemoryManager': {
            'description': 'Conversation and fact memory',
            'capabilities': ['save_memory', 'load_memory', 'conversations', 'search']
        },
        'VoiceEngine': {
            'description': 'Speech recognition and TTS',
            'capabilities': ['speak', 'listen', 'wake_word', 'continuous_listen']
        },
        'DesktopManager': {
            'description': 'Desktop and system appearance',
            'capabilities': ['wallpaper', 'theme', 'folders', 'taskbar', 'virtual_desktops']
        },
        'AIBrain': {
            'description': 'Claude AI conversation engine',
            'capabilities': ['chat', 'intent_detection', 'summarize', 'answer_questions']
        },
        'CommandRouter': {
            'description': 'Command routing and intent detection',
            'capabilities': ['route_commands', 'keyword_matching', 'module_integration']
        },
        'MultiAPIManager': {
            'description': 'Unified interface for all AI APIs',
            'capabilities': [
                'anthropic_claude', 'google_gemini', 'openai_gpt',
                'elevenlabs_tts', 'livekit_realtime', 'mem0_memory'
            ]
        }
    }
    
    return module_classes.get(module_name, {
        'description': 'Unknown module',
        'capabilities': []
    })

def get_capabilities_summary() -> dict:
    """
    Get summary of all module capabilities.
    
    Returns:
        Dictionary with all capabilities
    """
    return {
        'version': __version__,
        'total_modules': len(__all__),
        'modules': __all__,
        'categories': {
            'System': ['SystemControl', 'DesktopManager'],
            'Applications': ['AppManager', 'WindowManager'],
            'Audio_Display': ['VolumeControl', 'BrightnessControl'],
            'Media': ['MediaPlayer'],
            'Input': ['MouseKeyboard'],
            'Files': ['FileManager', 'ScreenshotTool', 'ImageTools', 'PDFTools'],
            'Web': ['GoogleSearch', 'NewsFetcher'],
            'Communication': ['WhatsAppAutomation'],
            'Memory': ['MemoryManager'],
            'Voice': ['VoiceEngine'],
            'AI': ['AIBrain', 'CommandRouter', 'MultiAPIManager']
        }
    }
