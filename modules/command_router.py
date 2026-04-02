"""
ZARA - Advanced Real-time Intelligent Assistant
Command Router Module - Intent detection and command routing
"""

import re
import os
import time
from typing import Dict, Any, Optional

# Import all modules
from .system_control import SystemControl
from .app_manager import AppManager
from .window_manager import WindowManager
from .volume_control import VolumeControl
from .brightness import BrightnessControl
from .media_player import MediaPlayer
from .mouse_keyboard import MouseKeyboard
from .file_manager import FileManager
from .screenshot import ScreenshotTool
from .image_tools import ImageTools
from .pdf_tools import PDFTools
from .google_search import GoogleSearch
from .news_fetcher import NewsFetcher
from .whatsapp import WhatsAppAutomation
from .memory_manager import MemoryManager
from .desktop_manager import DesktopManager


class CommandRouter:
    """
    Routes voice/text commands to appropriate module functions.
    Uses keyword matching and intent detection for command routing.
    """

    def __init__(self):
        """Initialize command router with all module instances."""
        # Initialize all modules
        self.system_control = SystemControl()
        self.app_manager = AppManager()
        self.window_manager = WindowManager()
        self.volume_control = VolumeControl()
        self.brightness_control = BrightnessControl()
        self.media_player = MediaPlayer()
        self.mouse_keyboard = MouseKeyboard()
        self.file_manager = FileManager()
        self.screenshot_tool = ScreenshotTool()
        self.image_tools = ImageTools()
        self.pdf_tools = PDFTools()
        self.google_search = GoogleSearch()
        self.news_fetcher = NewsFetcher()
        self.whatsapp = WhatsAppAutomation()
        self.memory_manager = MemoryManager()
        self.desktop_manager = DesktopManager()

    def route(self, command: str) -> Dict[str, Any]:
        """
        Route command to appropriate function based on keywords.
        
        Args:
            command: Voice/text command
            
        Returns:
            Response dictionary with result and action taken
        """
        if not command:
            return {
                "success": False,
                "response": "Please provide a command.",
                "action": "none"
            }

        command_lower = command.lower().strip()

        # Try each routing rule in order - PRIORITY ORDER
        result = self._try_media_commands(command_lower)
        if result:
            return result

        result = self._try_system_commands(command_lower)
        if result:
            return result

        result = self._try_app_commands(command_lower)
        if result:
            return result

        result = self._try_volume_commands(command_lower)
        if result:
            return result

        result = self._try_brightness_commands(command_lower)
        if result:
            return result

        result = self._try_window_commands(command_lower)
        if result:
            return result

        result = self._try_screenshot_commands(command_lower)
        if result:
            return result

        result = self._try_pdf_commands(command_lower)
        if result:
            return result

        result = self._try_file_commands(command_lower)
        if result:
            return result

        result = self._try_whatsapp_commands(command_lower)
        if result:
            return result

        result = self._try_mouse_keyboard_commands(command_lower)
        if result:
            return result

        result = self._try_news_commands(command_lower)
        if result:
            return result

        result = self._try_search_commands(command_lower)
        if result:
            return result

        result = self._try_time_commands(command_lower)
        if result:
            return result

        result = self._try_memory_commands(command_lower)
        if result:
            return result

        result = self._try_pdf_commands(command_lower)
        if result:
            return result

        result = self._try_image_commands(command_lower)
        if result:
            return result

        result = self._try_desktop_commands(command_lower)
        if result:
            return result

        result = self._try_keyboard_commands(command_lower)
        if result:
            return result

        result = self._try_file_commands(command_lower)
        if result:
            return result

        result = self._try_mouse_keyboard_commands(command_lower)
        if result:
            return result

        # No match - return for AI processing
        return {
            "success": True,
            "response": "No command match found",
            "action": "ai_fallback",
            "command": command,
            "needs_ai": True
        }

    def _extract_number(self, text: str) -> Optional[int]:
        """Extract first number from text."""
        match = re.search(r'\d+', text)
        return int(match.group()) if match else None

    # ============== System Commands ==============

    def _try_system_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try system control commands."""
        # Shutdown
        if any(kw in cmd for kw in ["shutdown", "shut down", "turn off computer"]):
            delay = self._extract_number(cmd) or 0
            result = self.system_control.shutdown(delay)
            return {
                "success": result.get("success", False),
                "response": result.get("message", "Shutting down"),
                "action": "shutdown"
            }

        # Restart
        if any(kw in cmd for kw in ["restart", "reboot"]):
            delay = self._extract_number(cmd) or 0
            result = self.system_control.restart(delay)
            return {
                "success": result.get("success", False),
                "response": result.get("message", "Restarting"),
                "action": "restart"
            }

        # Sleep
        if any(kw in cmd for kw in ["sleep", "go to sleep", "suspend"]):
            result = self.system_control.sleep()
            return {
                "success": result.get("success", False),
                "response": result.get("message", "Going to sleep"),
                "action": "sleep"
            }

        # Lock
        if any(kw in cmd for kw in ["lock", "lock computer", "lock screen"]):
            result = self.system_control.lock()
            return {
                "success": result.get("success", False),
                "response": result.get("message", "Locking computer"),
                "action": "lock"
            }

        # Battery
        if "battery" in cmd:
            result = self.system_control.get_battery()
            if result.get("available"):
                msg = f"Battery at {result.get('percent')}%"
                if result.get('plugged_in'):
                    msg += " and charging"
                return {"success": True, "response": msg, "action": "battery_status"}
            return {"success": True, "response": "No battery detected", "action": "battery_status"}

        # System status
        if any(kw in cmd for kw in ["system status", "cpu status", "ram status", "computer status", "performance"]):
            result = self.system_control.full_system_status()
            cpu = result.get("cpu", {}).get("usage_percent", "N/A")
            ram = result.get("ram", {})
            ram_msg = f"{ram.get('used_gb', 'N/A')}GB of {ram.get('total_gb', 'N/A')}GB"
            return {
                "success": True,
                "response": f"CPU: {cpu}%, RAM: {ram_msg}, Uptime: {result.get('uptime', 'N/A')}",
                "action": "system_status",
                "details": result
            }

        # Cancel shutdown
        if "cancel shutdown" in cmd or "cancel restart" in cmd:
            result = self.system_control.cancel_shutdown()
            return {
                "success": result.get("success", False),
                "response": result.get("message", "Shutdown cancelled"),
                "action": "cancel_shutdown"
            }

        return None

    # ============== App Commands ==============

    def _try_app_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try application commands."""
        # Special apps - WhatsApp Desktop, Paint, VS Code
        if any(kw in cmd for kw in ["whatsapp desktop", "whatsapp app", "system whatsapp"]):
            # WhatsApp Desktop path
            whatsapp_path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "WhatsApp", "WhatsApp.exe")
            if os.path.exists(whatsapp_path):
                os.startfile(whatsapp_path)
                return {"success": True, "response": "Opening WhatsApp Desktop", "action": "open_whatsapp_desktop"}
            else:
                return {"success": False, "response": "WhatsApp Desktop not found. Use WhatsApp Web instead.", "action": "whatsapp_not_found"}
        
        # Paint / Painting
        if any(kw in cmd for kw in ["paint", "painting", "draw", "chitrokari"]):
            os.startfile("mspaint.exe")
            return {"success": True, "response": "Opening Paint for you! 🎨", "action": "open_paint"}
        
        # VS Code / Code / Visual Studio Code
        if any(kw in cmd for kw in ["vs code", "visual studio code", "code", "coding", "code likho"]):
            vscode_path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Microsoft VS Code", "Code.exe")
            if os.path.exists(vscode_path):
                os.startfile(vscode_path)
                return {"success": True, "response": "Opening VS Code for coding! 💻", "action": "open_vscode"}
            else:
                # Try alternative path
                alt_path = r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"
                alt_path = os.path.expandvars(alt_path)
                if os.path.exists(alt_path):
                    os.startfile(alt_path)
                    return {"success": True, "response": "Opening VS Code for coding! 💻", "action": "open_vscode"}
                return {"success": False, "response": "VS Code not found. Please install VS Code.", "action": "vscode_not_found"}
        
        # Write code in VS Code
        if any(kw in cmd for kw in ["code likho", "write code", "python code", "javascript code", "react code"]):
            # Extract programming language and code description
            code_desc = cmd.replace("code likho", "").replace("write code", "").replace("python", "").replace("javascript", "").replace("react", "").strip()
            if not code_desc:
                code_desc = "simple program"
            
            # Open VS Code first
            vscode_path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Microsoft VS Code", "Code.exe")
            if os.path.exists(vscode_path):
                os.startfile(vscode_path)
                return {"success": True, "response": f"Opening VS Code to write {code_desc} code! 💻", "action": "open_vscode_coding"}
            else:
                return {"success": False, "response": "VS Code not found", "action": "vscode_not_found"}
        
        # Type in Notepad - Auto type whatever user says (including single word "notepad")
        if any(kw in cmd for kw in ["notepad mai likho", "notepad mein type", "type in notepad", "notepad type", "notepad"]):
            # Extract text to type
            text_to_type = cmd.replace("notepad mai likho", "").replace("notepad mein type", "").replace("type in notepad", "").replace("notepad type", "").replace("notepad", "").strip()
            
            if text_to_type:
                # Open Notepad
                os.startfile("notepad.exe")
                time.sleep(1)  # Wait for Notepad to open
                
                # Type the text using pyautogui
                self.mouse_keyboard.type_text(text_to_type)
                
                return {"success": True, "response": f"Typed '{text_to_type}' in Notepad", "action": "notepad_type"}
            else:
                # Just open Notepad if no text provided
                os.startfile("notepad.exe")
                return {"success": True, "response": "Opening Notepad", "action": "open_notepad"}
        
        # Open app - English and Hindi
        open_patterns = ["open ", "launch ", "start ", "khol ", "kholo ", "khol do ", "chalao "]
        for pattern in open_patterns:
            if cmd.startswith(pattern) or pattern in cmd:
                # Extract app name
                for p in open_patterns:
                    if p in cmd:
                        app_name = cmd.split(p, 1)[1].strip()
                        break
                app_name = app_name.replace("do", "").replace("kar do", "").strip()
                result = self.app_manager.open_app(app_name)
                return {
                    "success": result.get("success", False),
                    "response": result.get("message", f"Opening {app_name}"),
                    "action": "open_app",
                    "app": app_name
                }

        # Close app - English and Hindi
        close_patterns = ["close ", "quit ", "exit ", "stop ", "band ", "band karo "]
        for pattern in close_patterns:
            if cmd.startswith(pattern):
                app_name = cmd[len(pattern):].strip()
                result = self.app_manager.close_app(app_name)
                return {
                    "success": result.get("success", False),
                    "response": result.get("message", f"Closing {app_name}"),
                    "action": "close_app",
                    "app": app_name
                }

        # Is app running
        if "is " in cmd and " running" in cmd:
            match = re.search(r"is (.+) running", cmd)
            if match:
                app_name = match.group(1)
                is_running = self.app_manager.is_app_running(app_name)
                msg = f"Yes, {app_name} is running" if is_running else f"No, {app_name} is not running"
                return {"success": True, "response": msg, "action": "check_app"}

        return None

    # ============== Volume Commands ==============

    def _try_volume_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try volume commands."""
        # Volume up - English and Hindi (including single word "volume")
        if any(kw in cmd for kw in ["volume up", "increase volume", "volume higher", "turn up volume",
                                      "volume badha", "volume badhao", "volume badha do", "aawaz badha", "volume"]):
            step = self._extract_number(cmd) or 10
            result = self.volume_control.increase_volume(step)
            return {
                "success": True,
                "response": f"Volume increased to {self.volume_control.get_volume()}%",
                "action": "volume_up"
            }

        # Volume down - English and Hindi
        if any(kw in cmd for kw in ["volume down", "decrease volume", "volume lower", "turn down volume",
                                      "volume kam", "volume kam karo", "volume kam karo", "aawaz kam"]):
            step = self._extract_number(cmd) or 10
            result = self.volume_control.decrease_volume(step)
            return {
                "success": True,
                "response": f"Volume decreased to {self.volume_control.get_volume()}%",
                "action": "volume_down"
            }

        # Mute toggle
        if any(kw in cmd for kw in ["mute", "unmute", "toggle mute", "mute karo", "aawaz band"]):
            result = self.volume_control.toggle_mute()
            status = "muted" if self.volume_control.is_muted() else "unmuted"
            return {"success": True, "response": f"Audio {status}", "action": "mute_toggle"}

        # Set volume percentage
        volume_match = re.search(r'(?:volume |set volume to |volume at )(\d+)', cmd)
        if volume_match:
            level = int(volume_match.group(1))
            result = self.volume_control.set_volume(level)
            return {"success": True, "response": f"Volume set to {level}%", "action": "volume_set"}

        # What's the volume
        if "what" in cmd and "volume" in cmd:
            level = self.volume_control.get_volume()
            return {"success": True, "response": f"Volume is at {level}%", "action": "volume_query"}

        return None

    # ============== Brightness Commands ==============

    def _try_brightness_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try brightness commands."""
        # Brightness up - English and Hindi (including single word "brightness")
        if any(kw in cmd for kw in ["brightness up", "increase brightness", "brighter", "screen brighter",
                                      "brightness badha", "brightness badhao", "brightness badha do", "brightness"]):
            step = self._extract_number(cmd) or 10
            result = self.brightness_control.increase_brightness(step)
            return {
                "success": True,
                "response": f"Brightness increased to {self.brightness_control.get_brightness()}%",
                "action": "brightness_up"
            }

        # Brightness down - English and Hindi
        if any(kw in cmd for kw in ["brightness down", "decrease brightness", "dimmer", "screen dimmer",
                                      "brightness kam", "brightness kam karo", "kam karo"]):
            step = self._extract_number(cmd) or 10
            result = self.brightness_control.decrease_brightness(step)
            return {
                "success": True,
                "response": f"Brightness decreased to {self.brightness_control.get_brightness()}%",
                "action": "brightness_down"
            }

        # Set brightness percentage
        bright_match = re.search(r'(?:brightness |set brightness to |brightness at )(\d+)', cmd)
        if bright_match:
            level = int(bright_match.group(1))
            result = self.brightness_control.set_brightness(level)
            return {"success": True, "response": f"Brightness set to {level}%", "action": "brightness_set"}

        return None

    # ============== Media Commands ==============

    def _try_media_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try media player commands."""
        # Play on YouTube
        youtube_match = re.search(r'play (.+) on youtube|youtube play (.+)', cmd)
        if youtube_match:
            query = youtube_match.group(1) or youtube_match.group(2)
            result = self.media_player.play_youtube(query)
            return {"success": True, "response": f"Playing {query} on YouTube", "action": "youtube_play"}

        # Play on Spotify
        spotify_match = re.search(r'play (.+) on spotify|spotify play (.+)', cmd)
        if spotify_match:
            query = spotify_match.group(1) or spotify_match.group(2)
            result = self.media_player.play_spotify(query)
            return {"success": True, "response": f"Playing {query} on Spotify", "action": "spotify_play"}

        # Next track
        if any(kw in cmd for kw in ["next track", "next song", "skip", "skip track"]):
            result = self.media_player.next_track()
            return {"success": True, "response": "Next track", "action": "next_track"}

        # Previous track
        if any(kw in cmd for kw in ["previous track", "previous song", "go back", "last track"]):
            result = self.media_player.prev_track()
            return {"success": True, "response": "Previous track", "action": "prev_track"}

        # Pause/Play
        if any(kw in cmd for kw in ["pause", "pause music", "play music", "toggle play"]):
            result = self.media_player.pause_media()
            return {"success": True, "response": "Play/pause toggled", "action": "pause_play"}

        # Stop
        if any(kw in cmd for kw in ["stop music", "stop playing"]):
            result = self.media_player.stop_media()
            return {"success": True, "response": "Media stopped", "action": "stop_media"}

        # Zoom
        if "zoom in" in cmd:
            result = self.media_player.zoom_in()
            return {"success": True, "response": "Zoomed in", "action": "zoom_in"}
        if "zoom out" in cmd:
            result = self.media_player.zoom_out()
            return {"success": True, "response": "Zoomed out", "action": "zoom_out"}
        if "zoom reset" in cmd or "reset zoom" in cmd:
            result = self.media_player.zoom_reset()
            return {"success": True, "response": "Zoom reset", "action": "zoom_reset"}

        # Open website - Enhanced with more sites (including Hindi/Hinglish)
        if any(kw in cmd for kw in ["youtube", "google", "facebook", "instagram", "twitter", "linkedin", 
                                     "github", "reddit", "netflix", "amazon", "whatsapp web", "gmail"]):
            
            # Map common names to URLs
            url_map = {
                "youtube": "https://youtube.com",
                "google": "https://google.com",
                "facebook": "https://facebook.com",
                "insta": "https://instagram.com",
                "instagram": "https://instagram.com",
                "twitter": "https://twitter.com",
                "x": "https://twitter.com",
                "linkedin": "https://linkedin.com",
                "github": "https://github.com",
                "stackoverflow": "https://stackoverflow.com",
                "reddit": "https://reddit.com",
                "netflix": "https://netflix.com",
                "amazon": "https://amazon.com",
                "whatsapp": "https://web.whatsapp.com",
                "whatsapp web": "https://web.whatsapp.com",
                "gmail": "https://gmail.com",
                "drive": "https://drive.google.com",
                "docs": "https://docs.google.com",
                "sheets": "https://sheets.google.com",
                "slides": "https://slides.google.com",
                "maps": "https://maps.google.com",
                "news": "https://news.google.com",
            }
            
            # Find which site is mentioned
            for site_name, url in url_map.items():
                if site_name in cmd:
                    result = self.media_player.open_browser(url)
                    return {"success": True, "response": f"Opening {url}", "action": "open_url"}

        # Play song on YouTube - Enhanced for ANY video
        if any(kw in cmd for kw in ["song", "gaana", "music", "gaana", "sangeet", "play ", "baja ", "laga ", "chalao ", "video", "dikhao", "youtube"]):
            if "youtube" in cmd or any(kw in cmd for kw in ["song", "gaana", "music", "play ", "baja ", "laga ", "chalao ", "video", "dikhao"]):
                # Extract video name - remove all common keywords
                video_query = cmd
                remove_keywords = ["play ", "baja ", "laga ", "chalao ", "dikhao ", "do", "karo", "youtube", "pe", "par", "video", "song", "gaana", "music", "sangeet", "movie", "trailer", "full"]
                for keyword in remove_keywords:
                    video_query = video_query.replace(keyword, "")
                video_query = video_query.strip()
                
                if not video_query or len(video_query) < 3:
                    video_query = "latest hindi songs 2024"
                
                url = f"https://youtube.com/results?search_query={video_query.replace(' ', '+')}"
                result = self.media_player.open_browser(url)
                return {"success": True, "response": f"Playing {video_query} on YouTube", "action": "play_song"}

        # Play on Spotify
        if "spotify" in cmd or "spotify pe" in cmd:
            song_query = cmd.replace("spotify", "").replace("pe", "").replace("play ", "").replace("baja ", "").strip()
            if not song_query:
                song_query = "top hits"
            url = f"https://open.spotify.com/search/{song_query.replace(' ', '%20')}"
            result = self.media_player.open_browser(url)
            return {"success": True, "response": f"Playing {song_query} on Spotify", "action": "spotify_play"}

        return None

    # ============== PDF Commands ==============

    def _try_pdf_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try PDF commands."""
        # Merge PDFs
        if any(kw in cmd for kw in ["merge pdf", "join pdf", "pdf jodo", "pdf merge", "combine pdf"]):
            # Auto-find PDFs in Downloads folder
            downloads = os.path.join(os.path.expanduser("~"), "Downloads")
            pdf_files = [os.path.join(downloads, f) for f in os.listdir(downloads) if f.endswith('.pdf')][:5]
            
            if pdf_files:
                result = self.pdf_tools.merge_pdfs(pdf_files)
                return {"success": True, "response": f"Merged {len(pdf_files)} PDFs", "action": "merge_pdfs"}
            else:
                return {"success": False, "response": "No PDFs found in Downloads folder", "action": "merge_pdfs"}

        # PDF to Images
        if any(kw in cmd for kw in ["pdf to images", "pdf se images", "pdf convert", "convert pdf"]):
            result = self.pdf_tools.pdf_to_images()
            return {"success": True, "response": "PDF converted to images", "action": "pdf_to_images"}

        return None

    # ============== File Commands ==============

    def _try_file_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try file management commands."""
        # Create folder
        if any(kw in cmd for kw in ["create folder", "folder banao", "new folder", "folder create"]):
            folder_name = "New Folder"
            if "named" in cmd or "naam" in cmd:
                match = re.search(r'(?:named |naam )(.+)', cmd)
                if match:
                    folder_name = match.group(1).strip()
            result = self.file_manager.create_folder(folder_name)
            return {"success": True, "response": f"Folder '{folder_name}' created", "action": "create_folder"}

        # Delete file
        if any(kw in cmd for kw in ["delete file", "file delete", "remove file", "file hatao"]):
            result = self.file_manager.delete_file()
            return {"success": True, "response": "File deleted", "action": "delete_file"}

        # Open folder
        if any(kw in cmd for kw in ["open folder", "folder kholo", "folder open"]):
            folder = "Documents"
            if "downloads" in cmd:
                folder = "Downloads"
            elif "pictures" in cmd or "photos" in cmd:
                folder = "Pictures"
            elif "desktop" in cmd:
                folder = "Desktop"
            result = self.file_manager.open_folder(folder)
            return {"success": True, "response": f"Opening {folder}", "action": "open_folder"}

        return None

    # ============== Mouse & Keyboard Commands ==============

    def _try_mouse_keyboard_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try mouse and keyboard commands."""
        # Click
        if any(kw in cmd for kw in ["click", "click karo", "mouse click"]):
            result = self.mouse_keyboard.click()
            return {"success": True, "response": "Clicked", "action": "click"}

        # Double click
        if any(kw in cmd for kw in ["double click", "double click karo"]):
            result = self.mouse_keyboard.double_click()
            return {"success": True, "response": "Double clicked", "action": "double_click"}

        # Type text
        if any(kw in cmd for kw in ["type ", "likho ", "type karo "]):
            text = cmd.replace("type ", "").replace("likho ", "").replace("type karo ", "").strip()
            result = self.mouse_keyboard.type_text(text)
            return {"success": True, "response": f"Typed: {text}", "action": "type"}

        # Press key
        if any(kw in cmd for kw in ["press ", "dabao ", "press key"]):
            key = cmd.replace("press ", "").replace("dabao ", "").replace("press key", "").strip()
            result = self.mouse_keyboard.press_key(key)
            return {"success": True, "response": f"Pressed {key}", "action": "press_key"}

        return None

    # ============== WhatsApp Commands ==============

    def _try_whatsapp_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try WhatsApp commands."""
        # Open WhatsApp Web
        if any(kw in cmd for kw in ["whatsapp", "whatsapp web", "whatsapp kholo"]):
            # Open WhatsApp Web in browser
            import webbrowser
            webbrowser.open("https://web.whatsapp.com")
            return {"success": True, "response": "Opening WhatsApp Web", "action": "open_whatsapp"}

        # Send WhatsApp message to contact - Auto search and send
        if any(kw in cmd for kw in ["whatsapp message", "whatsapp pe bhejo", "whatsapp send", "message bhejo"]):
            # Extract contact name and message
            # Pattern: "whatsapp pe [name] ko [message] bhejo"
            contact_name = ""
            message_text = ""
            
            # Try to extract contact name (between "ko" and next keyword)
            ko_match = re.search(r'ko (.+?)(?:ko|message|msg|bhejo|send|likh|$)', cmd)
            if ko_match:
                contact_name = ko_match.group(1).strip()
            
            # Extract message (after contact name or after "likh" or "message")
            msg_patterns = ["likh", "message", "msg", "bhejo", "send", "likha"]
            for pattern in msg_patterns:
                if pattern in cmd:
                    msg_idx = cmd.find(pattern)
                    message_text = cmd[msg_idx + len(pattern):].strip()
                    message_text = message_text.replace("ko", "").replace("bhejo", "").replace("send", "").strip()
                    break
            
            if contact_name and message_text:
                # Open WhatsApp Web
                import webbrowser
                webbrowser.open("https://web.whatsapp.com")
                time.sleep(3)  # Wait for WhatsApp to load
                
                # Search for contact
                self.mouse_keyboard.type_text(contact_name)
                time.sleep(1)
                
                # Press Enter to select contact
                self.mouse_keyboard.press_key("enter")
                time.sleep(1)
                
                # Type message
                self.mouse_keyboard.type_text(message_text)
                time.sleep(0.5)
                
                # Press Enter to send
                self.mouse_keyboard.press_key("enter")
                
                return {"success": True, "response": f"Message sent to {contact_name}: '{message_text}'", "action": "whatsapp_send_message"}
            else:
                return {"success": False, "response": "Please provide contact name and message. Example: 'WhatsApp pe Rahul ko hello bhejo'", "action": "whatsapp_incomplete"}

        return None

    def _try_window_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try window management commands."""
        # Minimize
        if "minimize" in cmd:
            match = re.search(r'minimize (.+)', cmd)
            title = match.group(1) if match else None
            result = self.window_manager.minimize_window(title)
            return {"success": True, "response": "Window minimized", "action": "minimize"}

        # Maximize
        if "maximize" in cmd or "full screen" in cmd:
            match = re.search(r'maximize (.+)', cmd)
            title = match.group(1) if match else None
            result = self.window_manager.maximize_window(title)
            return {"success": True, "response": "Window maximized", "action": "maximize"}

        # Close window
        if any(kw in cmd for kw in ["close window", "close this", "close that"]):
            result = self.window_manager.close_window()
            return {"success": True, "response": "Window closed", "action": "close_window"}

        # Switch window
        if any(kw in cmd for kw in ["switch to", "switch window", "focus "]):
            match = re.search(r'(?:switch to |focus )(.+)', cmd)
            if match:
                title = match.group(1).replace("window", "").strip()
                result = self.window_manager.switch_window(title)
                return {"success": True, "response": f"Switched to {title}", "action": "switch_window"}

        # Show desktop
        if any(kw in cmd for kw in ["show desktop", "minimize all", "desktop"]):
            result = self.window_manager.show_desktop()
            return {"success": True, "response": "Desktop shown", "action": "show_desktop"}

        # Virtual desktops
        if "next desktop" in cmd or "next virtual desktop" in cmd:
            result = self.window_manager.virtual_desktop_next()
            return {"success": True, "response": "Switched to next desktop", "action": "virtual_desktop_next"}
        if "previous desktop" in cmd or "prev desktop" in cmd:
            result = self.window_manager.virtual_desktop_prev()
            return {"success": True, "response": "Switched to previous desktop", "action": "virtual_desktop_prev"}
        if "new desktop" in cmd or "create desktop" in cmd:
            result = self.window_manager.create_virtual_desktop()
            return {"success": True, "response": "Created new desktop", "action": "virtual_desktop_new"}

        return None

    # ============== Screenshot Commands ==============

    def _try_screenshot_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try screenshot commands."""
        if any(kw in cmd for kw in ["screenshot", "screen capture", "capture screen", "take picture"]):
            result = self.screenshot_tool.take_screenshot()
            return {
                "success": result.get("success", False),
                "response": "Screenshot taken",
                "action": "screenshot"
            }

        if any(kw in cmd for kw in ["screen text", "read screen", "ocr", "extract text from screen"]):
            result = self.screenshot_tool.get_screen_text()
            text = result.get("text", "")[:200]
            return {
                "success": True,
                "response": f"Screen text: {text}" if text else "No text found on screen",
                "action": "screen_ocr"
            }

        return None

    # ============== News Commands ==============

    def _try_news_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try news commands."""
        if any(kw in cmd for kw in ["news", "headlines", "what's happening", "top news"]):
            if "pakistan" in cmd:
                result = self.news_fetcher.get_pakistan_news()
            elif "tech" in cmd or "technology" in cmd:
                result = self.news_fetcher.get_tech_news()
            else:
                result = self.news_fetcher.get_top_news()

            articles = result.get("articles", [])
            if articles:
                summary = " | ".join([a["title"] for a in articles[:3]])
                return {"success": True, "response": summary, "action": "news", "details": result}
            return {"success": True, "response": "No news available", "action": "news"}

        return None

    # ============== Search Commands ==============

    def _try_search_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try search commands."""
        search_patterns = ["search ", "google ", "look up ", "find "]
        for pattern in search_patterns:
            if cmd.startswith(pattern):
                query = cmd[len(pattern):].strip()
                result = self.google_search.search(query)
                return {"success": True, "response": f"Searching for {query}", "action": "search"}

        return None

    # ============== Time Commands ==============

    def _try_time_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try time/date commands."""
        # Time - including single word "time"
        if any(kw in cmd for kw in ["what time", "current time", "time is it", "kya time", "time batao", "time kya hua", "time"]):
            result = self.google_search.get_datetime()
            return {"success": True, "response": f"Current time is {result.get('time')}", "action": "time"}

        # Date - including single word "date"
        if any(kw in cmd for kw in ["what date", "current date", "what day", "today's date", "kya date", "date batao", "aaj kya hai", "date"]):
            result = self.google_search.get_datetime()
            return {"success": True, "response": f"Today is {result.get('date')}", "action": "date"}

        return None

    # ============== Memory Commands ==============

    def _try_memory_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try memory commands."""
        # Remember something
        remember_match = re.search(r'remember (?:that )?(.+)', cmd)
        if remember_match:
            thing = remember_match.group(1).strip()
            key = thing[:30].replace(" ", "_").lower()
            result = self.memory_manager.save_memory(key, thing)
            return {"success": True, "response": f"I'll remember that: {thing[:50]}", "action": "remember"}

        # What do you remember
        if any(kw in cmd for kw in ["what do you remember", "what did i tell you", "show memory", "my memories"]):
            memories = self.memory_manager.get_all_memory()
            if memories:
                summary = "\n".join([f"- {m.get('value', '')}" for m in memories[:5]])
                return {"success": True, "response": f"Memories:\n{summary}", "action": "show_memory"}
            return {"success": True, "response": "I don't have any memories yet", "action": "show_memory"}

        return None

    # ============== Image Commands ==============

    def _try_image_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try image commands."""
        if "image to pdf" in cmd or "convert image to pdf" in cmd:
            return {
                "success": True,
                "response": "Please provide image path to convert to PDF",
                "action": "image_to_pdf",
                "needs_ai": True
            }

        if "resize image" in cmd:
            return {
                "success": True,
                "response": "Please provide image path and new dimensions",
                "action": "resize_image",
                "needs_ai": True
            }

        return None

    # ============== Desktop Commands ==============

    def _try_desktop_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try desktop commands."""
        if "wallpaper" in cmd or "change wallpaper" in cmd:
            return {
                "success": True,
                "response": "Please provide image path for wallpaper",
                "action": "set_wallpaper",
                "needs_ai": True
            }

        if "dark theme" in cmd or "dark mode" in cmd:
            result = self.desktop_manager.set_theme("dark")
            return {"success": True, "response": "Theme set to dark mode", "action": "set_theme"}

        if "light theme" in cmd or "light mode" in cmd:
            result = self.desktop_manager.set_theme("light")
            return {"success": True, "response": "Theme set to light mode", "action": "set_theme"}

        if "empty recycle bin" in cmd or "clear recycle bin" in cmd:
            result = self.desktop_manager.empty_recycle_bin()
            return {"success": True, "response": "Recycle bin emptied", "action": "empty_recycle_bin"}

        return None

    # ============== Keyboard Commands ==============

    def _try_keyboard_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try keyboard commands."""
        # Type text
        type_match = re.search(r'type (.+)', cmd)
        if type_match:
            text = type_match.group(1).strip()
            result = self.mouse_keyboard.type_text(text)
            return {"success": True, "response": f"Typed: {text[:50]}", "action": "type_text"}

        # Press key
        press_match = re.search(r'press (.+)', cmd)
        if press_match:
            key = press_match.group(1).strip()
            result = self.mouse_keyboard.press_key(key)
            return {"success": True, "response": f"Pressed {key}", "action": "press_key"}

        return None

    # ============== File Commands ==============

    def _try_file_commands(self, cmd: str) -> Optional[Dict[str, Any]]:
        """Try file commands."""
        # Create folder
        if any(kw in cmd for kw in ["folder banao", "create folder", "new folder", "folder create"]):
            folder_name = "New Folder"
            result = self.file_manager.create_folder(folder_name)
            return {"success": True, "response": f"Folder '{folder_name}' created", "action": "create_folder"}
        
        # Open folders
        if any(kw in cmd for kw in ["open documents", "my documents", "documents kholo"]):
            result = self.file_manager.open_documents()
            return {"success": True, "response": "Opening Documents folder", "action": "open_documents"}

        if any(kw in cmd for kw in ["open downloads", "my downloads", "downloads kholo"]):
            result = self.file_manager.open_downloads()
            return {"success": True, "response": "Opening Downloads folder", "action": "open_downloads"}

        if any(kw in cmd for kw in ["open pictures", "my photos", "pictures kholo"]):
            result = self.file_manager.open_pictures()
            return {"success": True, "response": "Opening Pictures folder", "action": "open_pictures"}

        return None

    def get_available_commands(self) -> list:
        """Get list of available commands."""
        return [
            "System: shutdown, restart, sleep, lock, battery status, system status",
            "Apps: open [app], close [app], is [app] running",
            "Volume: volume up/down, mute, set volume to [number]",
            "Brightness: brightness up/down, set brightness to [number]",
            "Media: play [song] on youtube/spotify, next/previous/pause music",
            "Windows: minimize/maximize/close window, show desktop, switch to [app]",
            "Screenshots: take screenshot, read screen text",
            "WhatsApp: send whatsapp to [contact] [message]",
            "News: news, headlines, pakistan news, tech news",
            "Search: search [query], google [query]",
            "Time: what time is it, what's the date",
            "Memory: remember [something], what do you remember",
            "PDF: merge pdfs, split pdf",
            "Images: image to pdf, resize image",
            "Desktop: change wallpaper, dark/light theme, empty recycle bin",
            "Keyboard: type [text], press [key]"
        ]

    def get_status(self) -> Dict[str, Any]:
        """Get command router status."""
        return {
            "available": True,
            "modules_initialized": 17,
            "capabilities": self.get_available_commands()
        }
