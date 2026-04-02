"""
ZARA - Advanced Real-time Intelligent Assistant
Mouse & Keyboard Control Module - Input automation using pyautogui
"""

import pyautogui
import time
from typing import Dict, Any, Optional, Tuple
from config import HOST


class MouseKeyboard:
    """
    Mouse and keyboard automation using pyautogui.
    Handles cursor movement, clicks, typing, and hotkeys.
    """

    def __init__(self):
        """Initialize mouse and keyboard control."""
        # Safety settings
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.1  # Pause between actions
        
        # Default settings
        self.default_duration = 0.5  # Movement duration
        self.default_interval = 0.05  # Typing interval

    # ============== Mouse Movement ==============

    def move_cursor(self, x: int, y: int, duration: float = None) -> Dict[str, Any]:
        """
        Move mouse cursor to coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Movement duration in seconds (default: default_duration)
            
        Returns:
            Status dictionary
        """
        try:
            duration = duration if duration is not None else self.default_duration
            
            pyautogui.moveTo(x, y, duration=duration)
            
            return {
                "success": True,
                "message": f"Mouse moved to ({x}, {y})",
                "position": {"x": x, "y": y},
                "action": "move_cursor"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def move_cursor_relative(self, x_offset: int, y_offset: int, duration: float = None) -> Dict[str, Any]:
        """
        Move mouse cursor relative to current position.
        
        Args:
            x_offset: X offset
            y_offset: Y offset
            duration: Movement duration
            
        Returns:
            Status dictionary
        """
        try:
            duration = duration if duration is not None else self.default_duration
            
            pyautogui.move(x_offset, y_offset, duration=duration)
            
            current = pyautogui.position()
            
            return {
                "success": True,
                "message": f"Mouse moved by ({x_offset}, {y_offset})",
                "position": {"x": current.x, "y": current.y},
                "action": "move_cursor_relative"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_cursor_position(self) -> Dict[str, Any]:
        """
        Get current cursor position.
        
        Returns:
            Position dictionary
        """
        try:
            pos = pyautogui.position()
            
            return {
                "success": True,
                "x": pos.x,
                "y": pos.y,
                "position": f"({pos.x}, {pos.y})"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Mouse Clicks ==============

    def click(self, button: str = 'left', clicks: int = 1) -> Dict[str, Any]:
        """
        Click mouse button.
        
        Args:
            button: 'left', 'right', 'middle'
            clicks: Number of clicks
            
        Returns:
            Status dictionary
        """
        try:
            pyautogui.click(clicks=clicks, button=button)
            
            return {
                "success": True,
                "message": f"{button.capitalize()} clicked {clicks} time(s)",
                "button": button,
                "clicks": clicks,
                "action": "click"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def right_click(self) -> Dict[str, Any]:
        """
        Right click at current position.
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.rightClick()
            
            return {
                "success": True,
                "message": "Right clicked",
                "action": "right_click"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def double_click(self, button: str = 'left') -> Dict[str, Any]:
        """
        Double click mouse button.
        
        Args:
            button: 'left', 'right', 'middle'
            
        Returns:
            Status dictionary
        """
        try:
            pyautogui.doubleClick(button=button)
            
            return {
                "success": True,
                "message": f"Double clicked ({button})",
                "button": button,
                "action": "double_click"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def middle_click(self) -> Dict[str, Any]:
        """
        Middle click at current position.
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.middleClick()
            
            return {
                "success": True,
                "message": "Middle clicked",
                "action": "middle_click"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def click_at(self, x: int, y: int, button: str = 'left') -> Dict[str, Any]:
        """
        Click at specific coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            button: 'left', 'right', 'middle'
            
        Returns:
            Status dictionary
        """
        try:
            pyautogui.click(x=x, y=y, button=button)
            
            return {
                "success": True,
                "message": f"Clicked at ({x}, {y})",
                "position": {"x": x, "y": y},
                "button": button,
                "action": "click_at"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Mouse Scroll ==============

    def scroll(self, amount: int) -> Dict[str, Any]:
        """
        Scroll mouse wheel.
        
        Args:
            amount: Scroll amount (positive = up, negative = down)
            
        Returns:
            Status dictionary
        """
        try:
            pyautogui.scroll(amount)
            
            direction = "up" if amount > 0 else "down"
            
            return {
                "success": True,
                "message": f"Scrolled {direction} ({abs(amount)} clicks)",
                "amount": amount,
                "direction": direction,
                "action": "scroll"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def scroll_up(self, clicks: int = 3) -> Dict[str, Any]:
        """
        Scroll up.
        
        Args:
            clicks: Number of clicks
            
        Returns:
            Status dictionary
        """
        return self.scroll(clicks)

    def scroll_down(self, clicks: int = 3) -> Dict[str, Any]:
        """
        Scroll down.
        
        Args:
            clicks: Number of clicks
            
        Returns:
            Status dictionary
        """
        return self.scroll(-clicks)

    def hscroll(self, amount: int) -> Dict[str, Any]:
        """
        Horizontal scroll.
        
        Args:
            amount: Scroll amount (positive = right, negative = left)
            
        Returns:
            Status dictionary
        """
        try:
            pyautogui.hscroll(amount)
            
            direction = "right" if amount > 0 else "left"
            
            return {
                "success": True,
                "message": f"Horizontal scroll {direction} ({abs(amount)} clicks)",
                "amount": amount,
                "direction": direction,
                "action": "hscroll"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Drag Operations ==============

    def drag(self, x1: int, y1: int, x2: int, y2: int, button: str = 'left', duration: float = 0.5) -> Dict[str, Any]:
        """
        Drag from one position to another.
        
        Args:
            x1, y1: Start position
            x2, y2: End position
            button: Mouse button
            duration: Drag duration
            
        Returns:
            Status dictionary
        """
        try:
            # Move to start position
            pyautogui.moveTo(x1, y1, duration=0.2)
            
            # Drag to end position
            pyautogui.drag(x2 - x1, y2 - y1, duration=duration, button=button)
            
            return {
                "success": True,
                "message": f"Dragged from ({x1}, {y1}) to ({x2}, {y2})",
                "start": {"x": x1, "y": y1},
                "end": {"x": x2, "y": y2},
                "button": button,
                "action": "drag"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def drag_to(self, x: int, y: int, button: str = 'left', duration: float = 0.5) -> Dict[str, Any]:
        """
        Drag to specific position from current location.
        
        Args:
            x, y: Target position
            button: Mouse button
            duration: Drag duration
            
        Returns:
            Status dictionary
        """
        try:
            current = pyautogui.position()
            
            pyautogui.dragTo(x, y, duration=duration, button=button)
            
            return {
                "success": True,
                "message": f"Dragged to ({x}, {y})",
                "start": {"x": current.x, "y": current.y},
                "end": {"x": x, "y": y},
                "button": button,
                "action": "drag_to"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Keyboard - Typing ==============

    def type_text(self, text: str, interval: float = None) -> Dict[str, Any]:
        """
        Type text character by character.
        
        Args:
            text: Text to type
            interval: Interval between keystrokes (default: default_interval)
            
        Returns:
            Status dictionary
        """
        try:
            interval = interval if interval is not None else self.default_interval
            
            pyautogui.write(text, interval=interval)
            
            return {
                "success": True,
                "message": f"Typed: {text[:50]}{'...' if len(text) > 50 else ''}",
                "length": len(text),
                "action": "type_text"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def type_text_safe(self, text: str, interval: float = 0.1) -> Dict[str, Any]:
        """
        Type text with safer characters (avoids special keys).
        
        Args:
            text: Text to type
            interval: Interval between keystrokes
            
        Returns:
            Status dictionary
        """
        try:
            # Only allow safe characters
            safe_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?@#$%&*()_+-=[]{}|;:,.<>?'
            safe_text = ''.join(c for c in text if c in safe_chars)
            
            return self.type_text(safe_text, interval)
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Keyboard - Key Presses ==============

    def press_key(self, key: str, presses: int = 1, interval: float = 0.1) -> Dict[str, Any]:
        """
        Press a keyboard key.
        
        Args:
            key: Key name (e.g., 'enter', 'space', 'a', 'f1')
            presses: Number of times to press
            interval: Interval between presses
            
        Returns:
            Status dictionary
        """
        try:
            pyautogui.press(key, presses=presses, interval=interval)
            
            return {
                "success": True,
                "message": f"Pressed '{key}' {presses} time(s)",
                "key": key,
                "presses": presses,
                "action": "press_key"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def press_keys(self, keys: list, interval: float = 0.1) -> Dict[str, Any]:
        """
        Press multiple keys in sequence.
        
        Args:
            keys: List of keys to press
            interval: Interval between presses
            
        Returns:
            Status dictionary
        """
        try:
            for key in keys:
                pyautogui.press(key, interval=interval)
            
            return {
                "success": True,
                "message": f"Pressed keys: {', '.join(keys)}",
                "keys": keys,
                "action": "press_keys"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def hotkey(self, *keys) -> Dict[str, Any]:
        """
        Press multiple keys as hotkey combination.
        
        Args:
            *keys: Keys to press together (e.g., 'ctrl', 'c')
            
        Returns:
            Status dictionary
        """
        try:
            pyautogui.hotkey(*keys)
            
            return {
                "success": True,
                "message": f"Pressed hotkey: {'+'.join(keys)}",
                "keys": list(keys),
                "action": "hotkey"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def key_down(self, key: str) -> Dict[str, Any]:
        """
        Hold down a key.
        
        Args:
            key: Key to hold
            
        Returns:
            Status dictionary
        """
        try:
            pyautogui.keyDown(key)
            
            return {
                "success": True,
                "message": f"Holding '{key}'",
                "key": key,
                "action": "key_down"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def key_up(self, key: str) -> Dict[str, Any]:
        """
        Release a key.
        
        Args:
            key: Key to release
            
        Returns:
            Status dictionary
        """
        try:
            pyautogui.keyUp(key)
            
            return {
                "success": True,
                "message": f"Released '{key}'",
                "key": key,
                "action": "key_up"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Common Shortcuts ==============

    def copy(self) -> Dict[str, Any]:
        """Copy selected content (Ctrl+C)."""
        return self.hotkey('ctrl', 'c')

    def paste(self) -> Dict[str, Any]:
        """Paste clipboard content (Ctrl+V)."""
        return self.hotkey('ctrl', 'v')

    def cut(self) -> Dict[str, Any]:
        """Cut selected content (Ctrl+X)."""
        return self.hotkey('ctrl', 'x')

    def undo(self) -> Dict[str, Any]:
        """Undo last action (Ctrl+Z)."""
        return self.hotkey('ctrl', 'z')

    def redo(self) -> Dict[str, Any]:
        """Redo last undone action (Ctrl+Y)."""
        return self.hotkey('ctrl', 'y')

    def select_all(self) -> Dict[str, Any]:
        """Select all content (Ctrl+A)."""
        return self.hotkey('ctrl', 'a')

    def save(self) -> Dict[str, Any]:
        """Save current file (Ctrl+S)."""
        return self.hotkey('ctrl', 's')

    def open(self) -> Dict[str, Any]:
        """Open file dialog (Ctrl+O)."""
        return self.hotkey('ctrl', 'o')

    def new(self) -> Dict[str, Any]:
        """Create new file/window (Ctrl+N)."""
        return self.hotkey('ctrl', 'n')

    def close(self) -> Dict[str, Any]:
        """Close current tab/window (Ctrl+W)."""
        return self.hotkey('ctrl', 'w')

    def find(self) -> Dict[str, Any]:
        """Open find dialog (Ctrl+F)."""
        return self.hotkey('ctrl', 'f')

    def print(self) -> Dict[str, Any]:
        """Open print dialog (Ctrl+P)."""
        return self.hotkey('ctrl', 'p')

    def refresh(self) -> Dict[str, Any]:
        """Refresh page (F5)."""
        return self.press_key('f5')

    def fullscreen(self) -> Dict[str, Any]:
        """Toggle fullscreen (F11)."""
        return self.press_key('f11')

    def alt_tab(self) -> Dict[str, Any]:
        """Switch to next window (Alt+Tab)."""
        return self.hotkey('alt', 'tab')

    def win_d(self) -> Dict[str, Any]:
        """Show desktop (Win+D)."""
        return self.hotkey('win', 'd')

    def win_e(self) -> Dict[str, Any]:
        """Open file explorer (Win+E)."""
        return self.hotkey('win', 'e')

    def win_l(self) -> Dict[str, Any]:
        """Lock computer (Win+L)."""
        return self.hotkey('win', 'l')

    def win_r(self) -> Dict[str, Any]:
        """Open run dialog (Win+R)."""
        return self.hotkey('win', 'r')

    def win_t(self) -> Dict[str, Any]:
        """Open taskbar (Win+T)."""
        return self.hotkey('win', 't')

    def alt_f4(self) -> Dict[str, Any]:
        """Close current window (Alt+F4)."""
        return self.hotkey('alt', 'f4')

    def ctrl_shift_esc(self) -> Dict[str, Any]:
        """Open task manager (Ctrl+Shift+Esc)."""
        return self.hotkey('ctrl', 'shift', 'esc')

    # ============== Swipe Gestures ==============

    def swipe(self, direction: str, distance: int = 100) -> Dict[str, Any]:
        """
        Simulate swipe gesture.
        
        Args:
            direction: 'up', 'down', 'left', 'right'
            distance: Swipe distance in pixels
            
        Returns:
            Status dictionary
        """
        try:
            current = pyautogui.position()
            
            if direction.lower() == 'up':
                pyautogui.drag(0, -distance, duration=0.3, button='left')
            elif direction.lower() == 'down':
                pyautogui.drag(0, distance, duration=0.3, button='left')
            elif direction.lower() == 'left':
                pyautogui.drag(-distance, 0, duration=0.3, button='left')
            elif direction.lower() == 'right':
                pyautogui.drag(distance, 0, duration=0.3, button='left')
            else:
                return {
                    "success": False,
                    "message": f"Invalid direction: {direction}. Use: up, down, left, right",
                    "action": "swipe"
                }
            
            return {
                "success": True,
                "message": f"Swiped {direction} ({distance}px)",
                "direction": direction,
                "distance": distance,
                "action": "swipe"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def swipe_up(self, distance: int = 100) -> Dict[str, Any]:
        """Swipe up gesture."""
        return self.swipe('up', distance)

    def swipe_down(self, distance: int = 100) -> Dict[str, Any]:
        """Swipe down gesture."""
        return self.swipe('down', distance)

    def swipe_left(self, distance: int = 100) -> Dict[str, Any]:
        """Swipe left gesture."""
        return self.swipe('left', distance)

    def swipe_right(self, distance: int = 100) -> Dict[str, Any]:
        """Swipe right gesture."""
        return self.swipe('right', distance)

    # ============== Utilities ==============

    def get_screen_size(self) -> Dict[str, Any]:
        """
        Get screen resolution.
        
        Returns:
            Screen size dictionary
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

    def on_screen(self, x: int, y: int) -> bool:
        """
        Check if coordinates are on screen.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if on screen
        """
        return pyautogui.onScreen(x, y)

    def set_pause(self, seconds: float) -> Dict[str, Any]:
        """
        Set pause between pyautogui actions.
        
        Args:
            seconds: Pause duration
            
        Returns:
            Status dictionary
        """
        try:
            pyautogui.PAUSE = seconds
            
            return {
                "success": True,
                "message": f"Pause set to {seconds}s",
                "pause": seconds,
                "action": "set_pause"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def set_failsafe(self, enable: bool) -> Dict[str, Any]:
        """
        Enable/disable failsafe (move to corner to abort).
        
        Args:
            enable: True to enable
            
        Returns:
            Status dictionary
        """
        try:
            pyautogui.FAILSAFE = enable
            
            return {
                "success": True,
                "message": f"Failsafe {'enabled' if enable else 'disabled'}",
                "enabled": enable,
                "action": "set_failsafe"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """
        Get mouse/keyboard status.
        
        Returns:
            Status dictionary
        """
        pos = pyautogui.position()
        size = pyautogui.size()
        
        return {
            "available": True,
            "cursor_position": {"x": pos.x, "y": pos.y},
            "screen_size": {"width": size.width, "height": size.height},
            "failsafe": pyautogui.FAILSAFE,
            "pause": pyautogui.PAUSE
        }
