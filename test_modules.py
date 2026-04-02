"""
ARIA - Advanced Real-time Intelligent Assistant
Module Testing Script - Test all modules for basic functionality

NOTE: Does NOT test shutdown/restart/sleep/lock commands for safety!
"""

import sys
import os
import time
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

def print_test(name, passed, details=""):
    status = f"{Colors.OKGREEN}PASS{Colors.ENDC}" if passed else f"{Colors.FAIL}FAIL{Colors.ENDC}"
    print(f"  {status} - {name}")
    if details and not passed:
        print(f"       {Colors.FAIL}Error: {details}{Colors.ENDC}")

# ============== Test Functions ==============

def test_voice_engine():
    """Test VoiceEngine initialization."""
    print(f"\n{Colors.OKCYAN}Testing VoiceEngine...{Colors.ENDC}")
    try:
        from modules.voice_engine import VoiceEngine
        engine = VoiceEngine()
        
        # Test TTS availability
        tts_available = engine.engine is not None
        print_test("TTS Engine initialized", tts_available)
        
        # Test microphone availability
        stt_available = engine.microphone is not None
        print_test("Microphone initialized", stt_available)
        
        # Test wake word detection
        is_wake = engine.is_wake_word("hey aria")
        print_test("Wake word detection", is_wake == True)
        
        # Test clean command
        cleaned = engine.clean_command("aria open chrome")
        print_test("Clean command", cleaned == "open chrome")
        
        return True
    except Exception as e:
        print_test("VoiceEngine", False, str(e))
        return False

def test_system_control_safe():
    """Test SystemControl (SAFE - no shutdown/restart tests)."""
    print(f"\n{Colors.OKCYAN}Testing SystemControl (SAFE MODE)...{Colors.ENDC}")
    try:
        from modules.system_control import SystemControl
        sc = SystemControl()
        
        # Test battery (safe)
        battery = sc.get_battery()
        print_test("Get battery status", 'available' in battery)
        
        # Test CPU usage (safe)
        cpu = sc.get_cpu_usage()
        print_test("Get CPU usage", 'usage_percent' in cpu)
        
        # Test RAM usage (safe)
        ram = sc.get_ram_usage()
        print_test("Get RAM usage", 'used_gb' in ram)
        
        # Test network info (safe)
        network = sc.get_network_info()
        print_test("Get network info", 'ip_address' in network)
        
        # Test uptime (safe)
        uptime = sc.get_uptime()
        print_test("Get uptime", isinstance(uptime, str))
        
        # Test process count (safe)
        count = sc.get_process_count()
        print_test("Get process count", count > 0)
        
        # Test full system status (safe)
        status = sc.full_system_status()
        print_test("Full system status", 'uptime' in status)
        
        return True
    except Exception as e:
        print_test("SystemControl", False, str(e))
        return False

def test_volume_control():
    """Test VolumeControl."""
    print(f"\n{Colors.OKCYAN}Testing VolumeControl...{Colors.ENDC}")
    try:
        from modules.volume_control import VolumeControl
        vc = VolumeControl()
        
        # Test get volume (safe)
        volume = vc.get_volume()
        print_test("Get volume", isinstance(volume, int) and 0 <= volume <= 100)
        
        # Test is muted (safe)
        muted = vc.is_muted()
        print_test("Is muted check", isinstance(muted, bool))
        
        # Test get status (safe)
        status = vc.get_status()
        print_test("Get status", 'available' in status)
        
        return True
    except Exception as e:
        print_test("VolumeControl", False, str(e))
        return False

def test_brightness_control():
    """Test BrightnessControl."""
    print(f"\n{Colors.OKCYAN}Testing BrightnessControl...{Colors.ENDC}")
    try:
        from modules.brightness import BrightnessControl
        bc = BrightnessControl()
        
        # Test get brightness (safe)
        brightness = bc.get_brightness()
        print_test("Get brightness", isinstance(brightness, int))
        
        # Test get status (safe)
        status = bc.get_status()
        print_test("Get status", 'available' in status)
        
        return True
    except Exception as e:
        print_test("BrightnessControl", False, str(e))
        return False

def test_app_manager():
    """Test AppManager."""
    print(f"\n{Colors.OKCYAN}Testing AppManager...{Colors.ENDC}")
    try:
        from modules.app_manager import AppManager
        am = AppManager()
        
        # Test list running apps (safe)
        apps = am.list_running_apps()
        print_test("List running apps", isinstance(apps, list) and len(apps) > 0)
        
        # Test is app running - check for explorer (should be running) (safe)
        explorer_running = am.is_app_running('explorer')
        print_test("Check if explorer running", explorer_running == True)
        
        # Test get openable apps (safe)
        openable = am.get_openable_apps()
        print_test("Get openable apps", len(openable) > 0)
        
        return True
    except Exception as e:
        print_test("AppManager", False, str(e))
        return False

def test_window_manager():
    """Test WindowManager."""
    print(f"\n{Colors.OKCYAN}Testing WindowManager...{Colors.ENDC}")
    try:
        from modules.window_manager import WindowManager
        wm = WindowManager()
        
        # Test get all windows (safe)
        windows = wm.get_all_windows()
        print_test("Get all windows", isinstance(windows, list))
        
        # Test get window count (safe)
        count = wm.get_window_count()
        print_test("Get window count", count >= 0)
        
        # Test get active window (safe)
        active = wm.get_active_window()
        print_test("Get active window", isinstance(active, dict))
        
        return True
    except Exception as e:
        print_test("WindowManager", False, str(e))
        return False

def test_file_manager():
    """Test FileManager with temp folder."""
    print(f"\n{Colors.OKCYAN}Testing FileManager...{Colors.ENDC}")
    try:
        from modules.file_manager import FileManager
        fm = FileManager()
        
        # Test create folder (safe)
        test_folder = "test_aria_temp_folder"
        create_result = fm.create_folder(test_folder)
        print_test("Create folder", create_result.get('success', False))
        
        # Test folder exists
        folder_exists = os.path.exists(test_folder)
        print_test("Folder exists", folder_exists)
        
        # Test list files (safe)
        list_result = fm.list_files('.')
        print_test("List files", 'files' in list_result or 'success' in list_result)
        
        # Test delete folder (safe - our own temp folder)
        if folder_exists:
            import shutil
            shutil.rmtree(test_folder)
            deleted = not os.path.exists(test_folder)
            print_test("Delete temp folder", deleted)
        
        # Test get file info (safe)
        if os.path.exists('main.py'):
            info = fm.get_file_info('main.py')
            print_test("Get file info", 'size' in info)
        
        return True
    except Exception as e:
        print_test("FileManager", False, str(e))
        return False

def test_memory_manager():
    """Test MemoryManager."""
    print(f"\n{Colors.OKCYAN}Testing MemoryManager...{Colors.ENDC}")
    try:
        from modules.memory_manager import MemoryManager
        mm = MemoryManager()
        
        # Test save memory (safe)
        save_result = mm.save_memory("test_key", "test_value")
        print_test("Save memory", save_result.get('success', False))
        
        # Test load memory (safe)
        loaded = mm.load_memory("test_key")
        print_test("Load memory", loaded == "test_value")
        
        # Test get all memory (safe)
        all_memory = mm.get_all_memory()
        print_test("Get all memory", isinstance(all_memory, list))
        
        # Test get recent conversations (safe)
        convos = mm.get_recent_conversations(5)
        print_test("Get recent conversations", isinstance(convos, list))
        
        # Test delete test memory (safe cleanup)
        delete_result = mm.delete_memory("test_key")
        print_test("Delete test memory", delete_result.get('success', False))
        
        return True
    except Exception as e:
        print_test("MemoryManager", False, str(e))
        return False

def test_google_search():
    """Test GoogleSearch."""
    print(f"\n{Colors.OKCYAN}Testing GoogleSearch...{Colors.ENDC}")
    try:
        from modules.google_search import GoogleSearch
        gs = GoogleSearch()
        
        # Test get datetime (safe)
        dt = gs.get_datetime()
        print_test("Get datetime", 'date' in dt and 'time' in dt)
        
        # Test get time (safe)
        time_result = gs.get_time()
        print_test("Get time", 'time' in time_result)
        
        # Test get date (safe)
        date_result = gs.get_date()
        print_test("Get date", 'date' in date_result)
        
        # Test get status (safe)
        status = gs.get_status()
        print_test("Get status", 'available' in status)
        
        return True
    except Exception as e:
        print_test("GoogleSearch", False, str(e))
        return False

def test_media_player():
    """Test MediaPlayer."""
    print(f"\n{Colors.OKCYAN}Testing MediaPlayer...{Colors.ENDC}")
    try:
        from modules.media_player import MediaPlayer
        mp = MediaPlayer()
        
        # Test get status (safe)
        status = mp.get_status()
        print_test("Get status", 'available' in status)
        
        # Test supported formats (safe)
        formats = mp.supported_media_extensions
        print_test("Supported formats", len(formats) > 0)
        
        return True
    except Exception as e:
        print_test("MediaPlayer", False, str(e))
        return False

def test_mouse_keyboard():
    """Test MouseKeyboard."""
    print(f"\n{Colors.OKCYAN}Testing MouseKeyboard...{Colors.ENDC}")
    try:
        from modules.mouse_keyboard import MouseKeyboard
        mk = MouseKeyboard()
        
        # Test get cursor position (safe)
        pos = mk.get_cursor_position()
        print_test("Get cursor position", 'x' in pos and 'y' in pos)
        
        # Test get screen size (safe)
        size = mk.get_screen_size()
        print_test("Get screen size", 'width' in size and 'height' in size)
        
        # Test get status (safe)
        status = mk.get_status()
        print_test("Get status", 'available' in status)
        
        return True
    except Exception as e:
        print_test("MouseKeyboard", False, str(e))
        return False

def test_command_router():
    """Test CommandRouter."""
    print(f"\n{Colors.OKCYAN}Testing CommandRouter...{Colors.ENDC}")
    try:
        from modules.command_router import CommandRouter
        cr = CommandRouter()
        
        # Test route with no match (safe - returns AI fallback)
        result = cr.route("hello how are you")
        print_test("Route conversation", result.get('needs_ai', False) or result.get('success', False))
        
        # Test route volume query (safe)
        result = cr.route("what's the volume")
        print_test("Route volume query", result.get('success', False))
        
        # Test route battery (safe)
        result = cr.route("battery status")
        print_test("Route battery status", result.get('success', False))
        
        # Test get available commands (safe)
        commands = cr.get_available_commands()
        print_test("Get available commands", len(commands) > 0)
        
        # Test get status (safe)
        status = cr.get_status()
        print_test("Get status", 'available' in status)
        
        return True
    except Exception as e:
        print_test("CommandRouter", False, str(e))
        return False

def test_ai_brain():
    """Test AIBrain (without API call - just initialization)."""
    print(f"\n{Colors.OKCYAN}Testing AIBrain...{Colors.ENDC}")
    try:
        from modules.ai_brain import AIBrain
        ai = AIBrain()
        
        # Test initialization (safe)
        status = ai.get_status()
        print_test("Get status", 'status' in status)
        
        # Test conversation history (safe)
        history = ai.get_history()
        print_test("Get history", isinstance(history, list))
        
        # Test clear history (safe)
        ai.clear_history()
        print_test("Clear history", len(ai.get_history()) == 0)
        
        return True
    except Exception as e:
        print_test("AIBrain", False, str(e))
        return False

def test_news_fetcher():
    """Test NewsFetcher."""
    print(f"\n{Colors.OKCYAN}Testing NewsFetcher...{Colors.ENDC}")
    try:
        from modules.news_fetcher import NewsFetcher
        nf = NewsFetcher()
        
        # Test get status (safe)
        status = nf.get_status()
        print_test("Get status", 'available' in status)
        
        # Test sources (safe)
        sources = status.get('sources', [])
        print_test("News sources available", len(sources) > 0)
        
        return True
    except Exception as e:
        print_test("NewsFetcher", False, str(e))
        return False

def test_whatsapp():
    """Test WhatsAppAutomation."""
    print(f"\n{Colors.OKCYAN}Testing WhatsAppAutomation...{Colors.ENDC}")
    try:
        from modules.whatsapp import WhatsAppAutomation
        wa = WhatsAppAutomation()
        
        # Test get status (safe)
        status = wa.get_status()
        print_test("Get status", 'available' in status)
        
        # Test capabilities (safe)
        capabilities = status.get('capabilities', [])
        print_test("Capabilities available", len(capabilities) > 0)
        
        return True
    except Exception as e:
        print_test("WhatsAppAutomation", False, str(e))
        return False

def test_image_tools():
    """Test ImageTools."""
    print(f"\n{Colors.OKCYAN}Testing ImageTools...{Colors.ENDC}")
    try:
        from modules.image_tools import ImageTools
        it = ImageTools()
        
        # Test get status (safe)
        status = it.get_status()
        print_test("Get status", 'available' in status)
        
        # Test supported formats (safe)
        formats = it.get_supported_formats()
        print_test("Supported formats", len(formats) > 0)
        
        return True
    except Exception as e:
        print_test("ImageTools", False, str(e))
        return False

def test_pdf_tools():
    """Test PDFTools."""
    print(f"\n{Colors.OKCYAN}Testing PDFTools...{Colors.ENDC}")
    try:
        from modules.pdf_tools import PDFTools
        pdf = PDFTools()
        
        # Test get status (safe)
        status = pdf.get_status()
        print_test("Get status", 'available' in status)
        
        # Test capabilities (safe)
        capabilities = status.get('capabilities', [])
        print_test("Capabilities available", len(capabilities) > 0)
        
        return True
    except Exception as e:
        print_test("PDFTools", False, str(e))
        return False

def test_screenshot():
    """Test ScreenshotTool."""
    print(f"\n{Colors.OKCYAN}Testing ScreenshotTool...{Colors.ENDC}")
    try:
        from modules.screenshot import ScreenshotTool
        st = ScreenshotTool()
        
        # Test get status (safe)
        status = st.get_status()
        print_test("Get status", 'available' in status)
        
        # Test screenshot directory (safe)
        screenshot_dir = st.get_screenshot_directory()
        print_test("Screenshot directory", os.path.exists(screenshot_dir))
        
        return True
    except Exception as e:
        print_test("ScreenshotTool", False, str(e))
        return False

def test_desktop_manager():
    """Test DesktopManager."""
    print(f"\n{Colors.OKCYAN}Testing DesktopManager...{Colors.ENDC}")
    try:
        from modules.desktop_manager import DesktopManager
        dm = DesktopManager()
        
        # Test get screen resolution (safe)
        res = dm.get_screen_resolution()
        print_test("Get screen resolution", 'width' in res and 'height' in res)
        
        return True
    except Exception as e:
        print_test("DesktopManager", False, str(e))
        return False

# ============== Main Test Runner ==============

def main():
    """Run all tests."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("="*60)
    print("  🧪 ARIA - Module Testing Suite")
    print("="*60)
    print(f"{Colors.ENDC}\n")
    
    print(f"{Colors.WARNING}⚠️  SAFE MODE: Shutdown/Restart/Lock tests SKIPPED{Colors.ENDC}\n")
    
    tests = [
        ("VoiceEngine", test_voice_engine),
        ("SystemControl (Safe)", test_system_control_safe),
        ("VolumeControl", test_volume_control),
        ("BrightnessControl", test_brightness_control),
        ("AppManager", test_app_manager),
        ("WindowManager", test_window_manager),
        ("FileManager", test_file_manager),
        ("MemoryManager", test_memory_manager),
        ("GoogleSearch", test_google_search),
        ("MediaPlayer", test_media_player),
        ("MouseKeyboard", test_mouse_keyboard),
        ("CommandRouter", test_command_router),
        ("AIBrain", test_ai_brain),
        ("NewsFetcher", test_news_fetcher),
        ("WhatsAppAutomation", test_whatsapp),
        ("ImageTools", test_image_tools),
        ("PDFTools", test_pdf_tools),
        ("ScreenshotTool", test_screenshot),
        ("DesktopManager", test_desktop_manager),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            results.append((name, False))
            print(f"{Colors.FAIL}  CRITICAL ERROR: {str(e)}{Colors.ENDC}")
    
    # Summary
    print(f"\n{Colors.HEADER}")
    print("="*60)
    print("  📊 Test Summary")
    print("="*60)
    print(f"{Colors.ENDC}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.OKGREEN}✓{Colors.ENDC}" if result else f"{Colors.FAIL}✗{Colors.ENDC}"
        print(f"  {status} {name}")
    
    print(f"\n{Colors.OKBLUE}{'='*60}{Colors.ENDC}")
    percentage = (passed / total) * 100 if total > 0 else 0
    
    if percentage == 100:
        print(f"{Colors.OKGREEN}{Colors.BOLD}  Result: {passed}/{total} tests passed ({percentage:.0f}%){Colors.ENDC}")
        print(f"{Colors.OKGREEN}  All systems operational! 🎉{Colors.ENDC}")
    elif percentage >= 80:
        print(f"{Colors.WARNING}{Colors.BOLD}  Result: {passed}/{total} tests passed ({percentage:.0f}%){Colors.ENDC}")
        print(f"{Colors.WARNING}  Most systems operational ⚠️{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}{Colors.BOLD}  Result: {passed}/{total} tests passed ({percentage:.0f}%){Colors.ENDC}")
        print(f"{Colors.FAIL}  Some systems need attention ❌{Colors.ENDC}")
    
    print(f"{Colors.OKBLUE}{'='*60}{Colors.ENDC}\n")
    
    return passed == total

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests cancelled by user.")
        sys.exit(1)
