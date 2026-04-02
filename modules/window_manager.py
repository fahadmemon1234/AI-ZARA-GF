"""
ZARA - Advanced Real-time Intelligent Assistant
Window Manager Module - Window control and manipulation
"""

import pygetwindow as gw
import pyautogui
from typing import List, Dict, Any, Optional
import win32gui
import win32con


class WindowManager:
    """
    Window management - control, move, resize windows.
    Handles window operations like minimize, maximize, close, snap, etc.
    """

    def __init__(self):
        """Initialize window manager."""
        pass

    def get_all_windows(self) -> List[Dict[str, Any]]:
        """
        Get list of all open windows.
        
        Returns:
            List of window info dictionaries
        """
        windows = []
        
        try:
            all_windows = gw.getAllWindows()
            
            for window in all_windows:
                # Filter out invisible/empty windows
                if window.title and window.width > 0 and window.height > 0:
                    windows.append({
                        "title": window.title,
                        "left": window.left,
                        "top": window.top,
                        "width": window.width,
                        "height": window.height,
                        "is_active": window.isActive,
                        "is_minimized": window.isMinimized,
                        "is_maximized": window.isMaximized,
                        "handle": window._hWnd
                    })
        except Exception as e:
            pass
        
        return windows

    def switch_window(self, title: str) -> Dict[str, Any]:
        """
        Find and activate window by partial title.
        
        Args:
            title: Partial or full window title
            
        Returns:
            Status dictionary
        """
        try:
            title_lower = title.lower()
            windows = gw.getAllWindows()
            
            for window in windows:
                if title_lower in window.title.lower():
                    window.activate()
                    window.bring_to_front()
                    
                    return {
                        "success": True,
                        "message": f"Switched to: {window.title}",
                        "title": window.title,
                        "action": "switch_window"
                    }
            
            return {
                "success": False,
                "message": f"No window found matching '{title}'",
                "action": "switch_window"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def minimize_window(self, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Minimize specific or active window.
        
        Args:
            title: Window title (None for active window)
            
        Returns:
            Status dictionary
        """
        try:
            if title:
                windows = gw.getAllWindows()
                
                for window in windows:
                    if title.lower() in window.title.lower():
                        window.minimize()
                        
                        return {
                            "success": True,
                            "message": f"Minimized: {window.title}",
                            "title": window.title,
                            "action": "minimize"
                        }
                
                return {
                    "success": False,
                    "message": f"No window found matching '{title}'",
                    "action": "minimize"
                }
            else:
                # Minimize active window
                active = gw.getActiveWindow()
                
                if active:
                    active.minimize()
                    
                    return {
                        "success": True,
                        "message": f"Minimized: {active.title}",
                        "title": active.title,
                        "action": "minimize_active"
                    }
                
                return {
                    "success": False,
                    "message": "No active window",
                    "action": "minimize"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def maximize_window(self, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Maximize specific or active window.
        
        Args:
            title: Window title (None for active window)
            
        Returns:
            Status dictionary
        """
        try:
            if title:
                windows = gw.getAllWindows()
                
                for window in windows:
                    if title.lower() in window.title.lower():
                        window.maximize()
                        
                        return {
                            "success": True,
                            "message": f"Maximized: {window.title}",
                            "title": window.title,
                            "action": "maximize"
                        }
                
                return {
                    "success": False,
                    "message": f"No window found matching '{title}'",
                    "action": "maximize"
                }
            else:
                # Maximize active window
                active = gw.getActiveWindow()
                
                if active:
                    active.maximize()
                    
                    return {
                        "success": True,
                        "message": f"Maximized: {active.title}",
                        "title": active.title,
                        "action": "maximize_active"
                    }
                
                return {
                    "success": False,
                    "message": "No active window",
                    "action": "maximize"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def restore_window(self, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Restore minimized/maximized window.
        
        Args:
            title: Window title (None for active window)
            
        Returns:
            Status dictionary
        """
        try:
            if title:
                windows = gw.getAllWindows()
                
                for window in windows:
                    if title.lower() in window.title.lower():
                        window.restore()
                        
                        return {
                            "success": True,
                            "message": f"Restored: {window.title}",
                            "title": window.title,
                            "action": "restore"
                        }
                
                return {
                    "success": False,
                    "message": f"No window found matching '{title}'",
                    "action": "restore"
                }
            else:
                active = gw.getActiveWindow()
                
                if active:
                    active.restore()
                    
                    return {
                        "success": True,
                        "message": f"Restored: {active.title}",
                        "title": active.title,
                        "action": "restore_active"
                    }
                
                return {
                    "success": False,
                    "message": "No active window",
                    "action": "restore"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def close_window(self, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Close specific or active window.
        
        Args:
            title: Window title (None for active window)
            
        Returns:
            Status dictionary
        """
        try:
            if title:
                windows = gw.getAllWindows()
                
                for window in windows:
                    if title.lower() in window.title.lower():
                        window.close()
                        
                        return {
                            "success": True,
                            "message": f"Closed: {window.title}",
                            "title": window.title,
                            "action": "close"
                        }
                
                return {
                    "success": False,
                    "message": f"No window found matching '{title}'",
                    "action": "close"
                }
            else:
                # Close active window using Alt+F4
                pyautogui.hotkey('alt', 'f4')
                
                return {
                    "success": True,
                    "message": "Sent close command to active window (Alt+F4)",
                    "action": "close_active"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def snap_window(self, direction: str, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Snap window to screen position.
        
        Args:
            direction: 'left', 'right', 'top', 'bottom', 'full', 'fullscreen'
            title: Window title (None for active window)
            
        Returns:
            Status dictionary
        """
        try:
            # Get target window
            if title:
                windows = gw.getAllWindows()
                window = None
                
                for w in windows:
                    if title.lower() in w.title.lower():
                        window = w
                        break
                
                if not window:
                    return {
                        "success": False,
                        "message": f"No window found matching '{title}'",
                        "action": "snap"
                    }
            else:
                window = gw.getActiveWindow()
                
                if not window:
                    return {
                        "success": False,
                        "message": "No active window",
                        "action": "snap"
                    }
            
            screen_width = pyautogui.size().width
            screen_height = pyautogui.size().height
            direction = direction.lower()
            
            if direction == 'left':
                window.moveTo(0, 0)
                window.resizeTo(screen_width // 2, screen_height)
                
            elif direction == 'right':
                window.moveTo(screen_width // 2, 0)
                window.resizeTo(screen_width // 2, screen_height)
                
            elif direction == 'top':
                window.moveTo(0, 0)
                window.resizeTo(screen_width, screen_height // 2)
                
            elif direction == 'bottom':
                window.moveTo(0, screen_height // 2)
                window.resizeTo(screen_width, screen_height // 2)
                
            elif direction in ['full', 'fullscreen']:
                window.maximize()
                
            else:
                return {
                    "success": False,
                    "message": f"Unknown direction: {direction}. Use: left, right, top, bottom, full",
                    "action": "snap"
                }
            
            return {
                "success": True,
                "message": f"Snapped window to {direction}",
                "title": window.title,
                "direction": direction,
                "action": "snap"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def show_desktop(self) -> Dict[str, Any]:
        """
        Show desktop (minimize all windows).
        Uses Win+D hotkey.
        
        Returns:
            Status dictionary
        """
        try:
            # Win+D hotkey to show desktop
            pyautogui.hotkey('win', 'd')
            
            return {
                "success": True,
                "message": "Desktop shown",
                "action": "show_desktop"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_active_window(self) -> Dict[str, Any]:
        """
        Get current active window info.
        
        Returns:
            Window info dictionary
        """
        try:
            active = gw.getActiveWindow()
            
            if active:
                return {
                    "title": active.title,
                    "left": active.left,
                    "top": active.top,
                    "width": active.width,
                    "height": active.height,
                    "is_minimized": active.isMinimized,
                    "is_maximized": active.isMaximized,
                    "handle": active._hWnd
                }
            
            return {
                "title": None,
                "message": "No active window"
            }
            
        except Exception as e:
            return {"error": str(e)}

    def center_window(self, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Center window on screen.
        
        Args:
            title: Window title (None for active window)
            
        Returns:
            Status dictionary
        """
        try:
            # Get target window
            if title:
                windows = gw.getAllWindows()
                window = None
                
                for w in windows:
                    if title.lower() in w.title.lower():
                        window = w
                        break
                
                if not window:
                    return {
                        "success": False,
                        "message": f"No window found matching '{title}'",
                        "action": "center"
                    }
            else:
                window = gw.getActiveWindow()
                
                if not window:
                    return {
                        "success": False,
                        "message": "No active window",
                        "action": "center"
                    }
            
            screen_width = pyautogui.size().width
            screen_height = pyautogui.size().height
            
            # Calculate center position
            x = (screen_width - window.width) // 2
            y = (screen_height - window.height) // 2
            
            window.moveTo(x, y)
            
            return {
                "success": True,
                "message": f"Centered: {window.title}",
                "title": window.title,
                "position": {"x": x, "y": y},
                "action": "center"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def move_window(self, title: str, x: int, y: int) -> Dict[str, Any]:
        """
        Move window to specific position.
        
        Args:
            title: Window title
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Status dictionary
        """
        try:
            windows = gw.getAllWindows()
            
            for window in windows:
                if title.lower() in window.title.lower():
                    window.moveTo(x, y)
                    
                    return {
                        "success": True,
                        "message": f"Moved {window.title} to ({x}, {y})",
                        "title": window.title,
                        "position": {"x": x, "y": y},
                        "action": "move"
                    }
            
            return {
                "success": False,
                "message": f"No window found matching '{title}'",
                "action": "move"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def resize_window(self, title: str, width: int, height: int) -> Dict[str, Any]:
        """
        Resize window.
        
        Args:
            title: Window title
            width: New width
            height: New height
            
        Returns:
            Status dictionary
        """
        try:
            windows = gw.getAllWindows()
            
            for window in windows:
                if title.lower() in window.title.lower():
                    window.resizeTo(width, height)
                    
                    return {
                        "success": True,
                        "message": f"Resized {window.title} to {width}x{height}",
                        "title": window.title,
                        "size": {"width": width, "height": height},
                        "action": "resize"
                    }
            
            return {
                "success": False,
                "message": f"No window found matching '{title}'",
                "action": "resize"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def set_always_on_top(self, title: str, enable: bool = True) -> Dict[str, Any]:
        """
        Set window always on top.
        Uses Win32 API for always on top.
        
        Args:
            title: Window title
            enable: True to enable, False to disable
            
        Returns:
            Status dictionary
        """
        try:
            windows = gw.getAllWindows()
            
            for window in windows:
                if title.lower() in window.title.lower():
                    # Use Win32 API for always on top
                    hwnd = win32gui.FindWindow(None, window.title)
                    
                    if hwnd:
                        if enable:
                            win32gui.SetWindowPos(
                                hwnd, win32con.HWND_TOPMOST,
                                0, 0, 0, 0,
                                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
                            )
                        else:
                            win32gui.SetWindowPos(
                                hwnd, win32con.HWND_NOTOPMOST,
                                0, 0, 0, 0,
                                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
                            )
                        
                        return {
                            "success": True,
                            "message": f"Always on top {'enabled' if enable else 'disabled'} for {window.title}",
                            "title": window.title,
                            "enabled": enable,
                            "action": "always_on_top"
                        }
            
            return {
                "success": False,
                "message": f"No window found matching '{title}'",
                "action": "always_on_top"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

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

    def get_window_count(self) -> int:
        """
        Get number of open windows.
        
        Returns:
            Window count
        """
        try:
            return len(gw.getAllWindows())
        except:
            return 0

    def tile_windows(self) -> Dict[str, Any]:
        """
        Tile all windows (cascade layout).
        
        Returns:
            Status dictionary
        """
        try:
            windows = gw.getAllWindows()
            
            if not windows:
                return {
                    "success": False,
                    "message": "No windows to tile",
                    "action": "tile"
                }
            
            screen_width = pyautogui.size().width
            screen_height = pyautogui.size().height
            
            # Calculate grid
            cols = int(len(windows) ** 0.5) + 1
            rows = (len(windows) + cols - 1) // cols
            
            cell_width = screen_width // cols
            cell_height = screen_height // rows
            
            for i, window in enumerate(windows):
                row = i // cols
                col = i % cols
                
                x = col * cell_width
                y = row * cell_height
                
                window.moveTo(x, y)
                window.resizeTo(cell_width, cell_height)
            
            return {
                "success": True,
                "message": f"Tiled {len(windows)} windows",
                "count": len(windows),
                "action": "tile"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
