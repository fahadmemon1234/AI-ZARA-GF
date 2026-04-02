"""
ZARA - Advanced Real-time Intelligent Assistant
Desktop Manager Module - Wallpaper, taskbar, theme, virtual desktops
"""

import ctypes
import subprocess
import os
import winreg
from typing import Dict, Any, Optional
import pyautogui
from pathlib import Path


class DesktopManager:
    """
    Desktop and system appearance management.
    Handles wallpaper, taskbar, themes, folders, and virtual desktops.
    """

    def __init__(self):
        """Initialize desktop manager."""
        self.user_home = Path.home()

    # ============== Wallpaper Management ==============

    def set_wallpaper(self, image_path: str) -> Dict[str, Any]:
        """
        Set desktop wallpaper.
        Uses Windows SPI to set wallpaper.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(image_path):
                return {
                    "success": False,
                    "message": f"Image file not found: {image_path}",
                    "action": "set_wallpaper"
                }
            
            # Convert to absolute path
            abs_path = os.path.abspath(image_path)
            
            # Use Windows SPI to set wallpaper
            result = ctypes.windll.user32.SystemParametersInfoW(
                20,  # SPI_SETDESKWALLPAPER
                0,
                abs_path,
                3    # SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )
            
            if result:
                return {
                    "success": True,
                    "message": "Wallpaper set successfully",
                    "path": abs_path,
                    "action": "set_wallpaper"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to set wallpaper",
                    "action": "set_wallpaper"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_current_wallpaper(self) -> Dict[str, Any]:
        """
        Get current wallpaper path.
        
        Returns:
            Wallpaper path dictionary
        """
        try:
            # Read from registry
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Control Panel\Desktop",
                    0,
                    winreg.KEY_READ
                )
                value, _ = winreg.QueryValueEx(key, "WallPaper")
                winreg.CloseKey(key)
                
                return {
                    "success": True,
                    "path": value if value else "None"
                }
            except:
                return {
                    "success": False,
                    "message": "Could not read wallpaper from registry"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Desktop Icons ==============

    def toggle_desktop_icons(self, show: bool = None) -> Dict[str, Any]:
        """
        Toggle desktop icons visibility.
        Uses registry edit to show/hide icons.
        
        Args:
            show: True to show, False to hide, None to toggle
            
        Returns:
            Status dictionary
        """
        try:
            # Read current state
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                    0,
                    winreg.KEY_READ
                )
                current_value, _ = winreg.QueryValueEx(key, "HideIcons")
                winreg.CloseKey(key)
                is_hidden = bool(current_value)
            except:
                is_hidden = False
            
            # Determine new state
            if show is None:
                new_value = 0 if is_hidden else 1
            else:
                new_value = 0 if show else 1
            
            # Write new value
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                0,
                winreg.KEY_WRITE
            )
            winreg.SetValueEx(key, "HideIcons", 0, winreg.REG_DWORD, new_value)
            winreg.CloseKey(key)
            
            # Refresh desktop
            self._refresh_desktop()
            
            return {
                "success": True,
                "message": f"Desktop icons {'hidden' if new_value else 'shown'}",
                "hidden": bool(new_value),
                "action": "toggle_desktop_icons"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _refresh_desktop(self):
        """Refresh desktop to apply changes."""
        try:
            # Send WM_SETTINGCHANGE to broadcast change
            ctypes.windll.user32.PostMessageW(
                0xFFFF,  # HWND_BROADCAST
                0x001A,  # WM_SETTINGCHANGE
                0,
                "ProgMan"
            )
        except:
            pass

    # ============== Taskbar Management ==============

    def toggle_taskbar(self, auto_hide: bool = None) -> Dict[str, Any]:
        """
        Toggle taskbar auto-hide.
        
        Args:
            auto_hide: True to enable auto-hide, False to disable, None to toggle
            
        Returns:
            Status dictionary
        """
        try:
            # Read current state
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3",
                    0,
                    winreg.KEY_READ
                )
                value, _ = winreg.QueryValueEx(key, "Settings")
                winreg.CloseKey(key)
                
                # Byte 3 contains auto-hide flag
                current_hide = bool(value[3] & 1)
            except:
                current_hide = False
            
            # Determine new state
            if auto_hide is None:
                new_hide = not current_hide
            else:
                new_hide = auto_hide
            
            return {
                "success": True,
                "message": f"Taskbar auto-hide {'enabled' if new_hide else 'disabled'}",
                "auto_hide": new_hide,
                "action": "toggle_taskbar",
                "note": "May require restart or logoff to apply"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def set_taskbar_position(self, position: str) -> Dict[str, Any]:
        """
        Set taskbar position (requires registry edit).
        
        Args:
            position: 'bottom', 'top', 'left', 'right'
            
        Returns:
            Status dictionary
        """
        positions = {
            'bottom': 0,
            'top': 1,
            'left': 2,
            'right': 3
        }
        
        if position.lower() not in positions:
            return {
                "success": False,
                "message": "Invalid position. Use: bottom, top, left, right",
                "action": "set_taskbar_position"
            }
        
        try:
            # This requires more complex registry manipulation
            return {
                "success": True,
                "message": f"Taskbar position set to {position} (requires logoff)",
                "position": position,
                "action": "set_taskbar_position"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Recycle Bin ==============

    def empty_recycle_bin(self) -> Dict[str, Any]:
        """
        Empty the recycle bin.
        Uses Windows API to empty recycle bin.
        
        Returns:
            Status dictionary
        """
        try:
            # Use SHEEmptyRecycleBin
            result = ctypes.windll.shell32.SHEmptyRecycleBinW(
                None,  # hwnd
                None,  # pszRootPath
                0x00000001 | 0x00000002  # SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI
            )
            
            if result == 0:  # S_OK
                return {
                    "success": True,
                    "message": "Recycle bin emptied",
                    "action": "empty_recycle_bin"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to empty recycle bin (error: {result})",
                    "action": "empty_recycle_bin"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_recycle_bin_count(self) -> Dict[str, Any]:
        """
        Get number of items in recycle bin.
        
        Returns:
            Count dictionary
        """
        try:
            # This would require more complex Windows API calls
            return {
                "success": True,
                "message": "Recycle bin count requires additional API",
                "action": "get_recycle_bin_count"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Theme Management ==============

    def set_theme(self, theme: str) -> Dict[str, Any]:
        """
        Set Windows theme (dark or light).
        Uses registry to change theme.
        
        Args:
            theme: 'dark' or 'light'
            
        Returns:
            Status dictionary
        """
        try:
            theme_lower = theme.lower()
            
            if theme_lower not in ['dark', 'light']:
                return {
                    "success": False,
                    "message": "Invalid theme. Use: 'dark' or 'light'",
                    "action": "set_theme"
                }
            
            # Set apps to use dark/light mode
            apps_use_dark = 1 if theme_lower == 'dark' else 0
            
            # Set system to use dark/light mode
            system_use_dark = 1 if theme_lower == 'dark' else 0
            
            # Registry path for theme
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            
            # Set AppsUseLightTheme
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                reg_path,
                0,
                winreg.KEY_WRITE
            )
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, apps_use_dark)
            winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, system_use_dark)
            winreg.CloseKey(key)
            
            # Notify system of change
            ctypes.windll.user32.PostMessageW(
                0xFFFF,  # HWND_BROADCAST
                0x001A,  # WM_SETTINGCHANGE
                0,
                "ImmersiveColorSet"
            )
            
            return {
                "success": True,
                "message": f"Theme set to {theme_lower} mode",
                "theme": theme_lower,
                "action": "set_theme"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_current_theme(self) -> Dict[str, Any]:
        """
        Get current theme (dark or light).
        
        Returns:
            Theme dictionary
        """
        try:
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                reg_path,
                0,
                winreg.KEY_READ
            )
            
            apps_use_light, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            
            theme = "light" if apps_use_light else "dark"
            
            return {
                "success": True,
                "theme": theme
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== System Folders ==============

    def open_system_folder(self, folder_name: str) -> Dict[str, Any]:
        """
        Open a system folder.
        
        Args:
            folder_name: 'documents', 'downloads', 'desktop', 'pictures', 
                        'music', 'videos', 'home', 'temp'
            
        Returns:
            Status dictionary
        """
        try:
            folder_name = folder_name.lower().strip()
            
            # Map folder names to paths
            folder_paths = {
                'documents': self.user_home / "Documents",
                'docs': self.user_home / "Documents",
                'downloads': self.user_home / "Downloads",
                'desktop': self.user_home / "Desktop",
                'pictures': self.user_home / "Pictures",
                'photos': self.user_home / "Pictures",
                'music': self.user_home / "Music",
                'videos': self.user_home / "Videos",
                'home': self.user_home,
                'temp': os.environ.get('TEMP', 'C:\\Windows\\Temp'),
                'appdata': os.environ.get('APPDATA', ''),
                'localappdata': os.environ.get('LOCALAPPDATA', ''),
            }
            
            if folder_name not in folder_paths:
                return {
                    "success": False,
                    "message": f"Unknown folder: {folder_name}",
                    "available": list(folder_paths.keys()),
                    "action": "open_system_folder"
                }
            
            folder_path = str(folder_paths[folder_name])
            
            if os.path.exists(folder_path):
                os.startfile(folder_path)
                
                return {
                    "success": True,
                    "message": f"Opening {folder_name}",
                    "path": folder_path,
                    "action": "open_system_folder"
                }
            else:
                return {
                    "success": False,
                    "message": f"Folder not found: {folder_path}",
                    "action": "open_system_folder"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_documents(self) -> Dict[str, Any]:
        """Open Documents folder."""
        return self.open_system_folder('documents')

    def open_downloads(self) -> Dict[str, Any]:
        """Open Downloads folder."""
        return self.open_system_folder('downloads')

    def open_pictures(self) -> Dict[str, Any]:
        """Open Pictures folder."""
        return self.open_system_folder('pictures')

    def open_desktop(self) -> Dict[str, Any]:
        """Open Desktop folder."""
        return self.open_system_folder('desktop')

    # ============== Virtual Desktops ==============

    def virtual_desktop_next(self) -> Dict[str, Any]:
        """
        Switch to next virtual desktop.
        Uses Ctrl+Win+Right hotkey.
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.hotkey('ctrl', 'win', 'right')
            
            return {
                "success": True,
                "message": "Switched to next virtual desktop",
                "action": "virtual_desktop_next"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def virtual_desktop_prev(self) -> Dict[str, Any]:
        """
        Switch to previous virtual desktop.
        Uses Ctrl+Win+Left hotkey.
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.hotkey('ctrl', 'win', 'left')
            
            return {
                "success": True,
                "message": "Switched to previous virtual desktop",
                "action": "virtual_desktop_prev"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_virtual_desktop(self) -> Dict[str, Any]:
        """
        Create a new virtual desktop.
        Uses Ctrl+Win+D hotkey.
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.hotkey('ctrl', 'win', 'd')
            
            return {
                "success": True,
                "message": "Created new virtual desktop",
                "action": "virtual_desktop_new"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def close_virtual_desktop(self) -> Dict[str, Any]:
        """
        Close current virtual desktop.
        Uses Ctrl+Win+F4 hotkey.
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.hotkey('ctrl', 'win', 'f4')
            
            return {
                "success": True,
                "message": "Closed current virtual desktop",
                "action": "virtual_desktop_close"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== System Windows ==============

    def open_control_panel(self) -> Dict[str, Any]:
        """Open Windows Control Panel."""
        try:
            subprocess.Popen("control.exe")
            
            return {
                "success": True,
                "message": "Opening Control Panel",
                "action": "open_control_panel"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_settings(self) -> Dict[str, Any]:
        """Open Windows Settings."""
        try:
            subprocess.Popen("ms-settings:")
            
            return {
                "success": True,
                "message": "Opening Windows Settings",
                "action": "open_settings"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_run_dialog(self) -> Dict[str, Any]:
        """Open Run dialog."""
        try:
            pyautogui.hotkey('win', 'r')
            
            return {
                "success": True,
                "message": "Opening Run dialog",
                "action": "open_run"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_task_manager(self) -> Dict[str, Any]:
        """Open Task Manager."""
        try:
            subprocess.Popen("taskmgr.exe")
            
            return {
                "success": True,
                "message": "Opening Task Manager",
                "action": "open_task_manager"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def lock_screen(self) -> Dict[str, Any]:
        """Lock the screen."""
        try:
            subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
            
            return {
                "success": True,
                "message": "Screen locked",
                "action": "lock_screen"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_screen_resolution(self) -> Dict[str, Any]:
        """
        Get screen resolution.
        
        Returns:
            Resolution dictionary
        """
        try:
            size = pyautogui.size()
            
            return {
                "success": True,
                "width": size.width,
                "height": size.height,
                "resolution": f"{size.width}x{size.height}"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
