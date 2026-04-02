"""
ZARA - Advanced Real-time Intelligent Assistant
Screenshot Tool Module - Capture screen and extract text using OCR
"""

import os
import time
import threading
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageGrab
import pyautogui


class ScreenshotTool:
    """
    Screenshot capture and OCR (Optical Character Recognition).
    Handles full screen, region, window screenshots and text extraction.
    """

    def __init__(self):
        """Initialize screenshot tool."""
        # Default screenshot directory
        self.screenshot_dir = os.path.join(
            os.path.expanduser("~"),
            "Pictures",
            "ARIA Screenshots"
        )
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # Screen reader state
        self.screen_reader_active = False
        self.screen_reader_thread = None
        self.ocr_callback = None

    def _generate_filename(self, prefix: str = "screenshot") -> str:
        """Generate timestamped filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.png"

    def _get_filepath(self, filename: str = None, prefix: str = "screenshot") -> str:
        """Get full filepath for screenshot."""
        if filename is None:
            filename = self._generate_filename(prefix)
        return os.path.join(self.screenshot_dir, filename)

    # ============== Basic Screenshots ==============

    def take_screenshot(self, save_path: str = None) -> Dict[str, Any]:
        """
        Take a full screen screenshot.
        
        Args:
            save_path: Custom save path (default: auto-generated in screenshot_dir)
            
        Returns:
            Status dictionary with screenshot path
        """
        try:
            # Generate filepath
            filepath = self._get_filepath(save_path) if save_path else self._get_filepath()
            
            # Take screenshot
            screenshot = ImageGrab.grab()
            
            # Save
            screenshot.save(filepath, 'PNG')
            
            return {
                "success": True,
                "message": "Screenshot taken",
                "path": filepath,
                "filename": os.path.basename(filepath),
                "size": screenshot.size,
                "action": "take_screenshot"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def screenshot_region(self, x: int, y: int, width: int, height: int, save_path: str = None) -> Dict[str, Any]:
        """
        Take a screenshot of a specific region.
        
        Args:
            x: X coordinate of top-left corner
            y: Y coordinate of top-left corner
            width: Width of region
            height: Height of region
            save_path: Custom save path
            
        Returns:
            Status dictionary
        """
        try:
            filepath = self._get_filepath(save_path, "region")
            
            # Capture region
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            
            # Save
            screenshot.save(filepath, 'PNG')
            
            return {
                "success": True,
                "message": f"Region screenshot taken ({width}x{height})",
                "path": filepath,
                "region": {"x": x, "y": y, "width": width, "height": height},
                "size": screenshot.size,
                "action": "screenshot_region"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def screenshot_window(self, title: str = None, save_path: str = None) -> Dict[str, Any]:
        """
        Take a screenshot of a specific window.
        
        Args:
            title: Window title (partial match). None for active window.
            save_path: Custom save path
            
        Returns:
            Status dictionary
        """
        try:
            import pygetwindow as gw
            
            # Find window
            if title:
                windows = gw.getWindowsWithTitle(title)
                if not windows:
                    return {
                        "success": False,
                        "message": f"No window found matching: {title}",
                        "action": "screenshot_window"
                    }
                window = windows[0]
            else:
                window = gw.getActiveWindow()
                if not window:
                    return {
                        "success": False,
                        "message": "No active window found",
                        "action": "screenshot_window"
                    }
            
            # Capture window
            filepath = self._get_filepath(save_path, "window")
            
            # Get window screenshot using coordinates
            screenshot = ImageGrab.grab(bbox=(
                window.left,
                window.top,
                window.left + window.width,
                window.top + window.height
            ))
            
            # Save
            screenshot.save(filepath, 'PNG')
            
            return {
                "success": True,
                "message": f"Window screenshot taken: {window.title}",
                "path": filepath,
                "window_title": window.title,
                "size": screenshot.size,
                "action": "screenshot_window"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def screenshot_selected_area(self) -> Dict[str, Any]:
        """
        Take a screenshot of user-selected area.
        Shows crosshair cursor for selection.
        
        Returns:
            Status dictionary
        """
        try:
            print("Select an area on the screen...")
            
            # Let user select area
            screenshot = pyautogui.screenshot()
            
            # For now, just take full screenshot
            # Full selection UI would require additional GUI code
            filepath = self._get_filepath(prefix="selected")
            screenshot.save(filepath, 'PNG')
            
            return {
                "success": True,
                "message": "Screenshot taken (full screen - selection requires GUI)",
                "path": filepath,
                "action": "screenshot_selected_area"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== OCR - Text Extraction ==============

    def get_screen_text(self, region: Tuple[int, int, int, int] = None) -> Dict[str, Any]:
        """
        Extract text from screen using OCR (pytesseract).
        
        Args:
            region: Optional region tuple (x, y, width, height)
            
        Returns:
            Dictionary with extracted text
        """
        try:
            # Import pytesseract
            try:
                import pytesseract
            except ImportError:
                return {
                    "success": False,
                    "message": "pytesseract not installed. Run: pip install pytesseract",
                    "action": "get_screen_text"
                }
            
            # Take screenshot
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()
            
            # Perform OCR
            text = pytesseract.image_to_string(screenshot)
            
            # Save screenshot for reference
            filepath = self._get_filepath(prefix="ocr")
            screenshot.save(filepath, 'PNG')
            
            return {
                "success": True,
                "message": "Text extracted from screen",
                "text": text.strip() if text.strip() else "No text found on screen",
                "text_length": len(text.strip()) if text.strip() else 0,
                "screenshot_path": filepath,
                "region": region,
                "action": "get_screen_text"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_selected_text(self) -> Dict[str, Any]:
        """
        Get currently selected text on screen.
        Uses Ctrl+C and reads from clipboard.
        
        Returns:
            Dictionary with selected text
        """
        try:
            import pyperclip
            
            # Clear clipboard first
            pyperclip.copy('')
            
            # Copy selected text
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)  # Wait for copy
            
            # Get from clipboard
            text = pyperclip.paste()
            
            if text:
                return {
                    "success": True,
                    "message": "Selected text retrieved",
                    "text": text.strip(),
                    "text_length": len(text.strip()),
                    "action": "get_selected_text"
                }
            else:
                return {
                    "success": False,
                    "message": "No text selected",
                    "action": "get_selected_text"
                }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def ocr_image(self, image_path: str) -> Dict[str, Any]:
        """
        Extract text from an image file.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with extracted text
        """
        try:
            import pytesseract
            
            if not os.path.exists(image_path):
                return {
                    "success": False,
                    "message": f"Image not found: {image_path}",
                    "action": "ocr_image"
                }
            
            # Open image
            image = Image.open(image_path)
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            
            return {
                "success": True,
                "message": "Text extracted from image",
                "text": text.strip() if text.strip() else "No text found in image",
                "text_length": len(text.strip()) if text.strip() else 0,
                "image_path": image_path,
                "action": "ocr_image"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Continuous Screen Reader ==============

    def start_screen_reader(self, interval: float = 5.0, callback=None) -> Dict[str, Any]:
        """
        Start continuous OCR screen reader in background thread.
        
        Args:
            interval: Seconds between OCR scans
            callback: Function to call with OCR results
            
        Returns:
            Status dictionary
        """
        try:
            if self.screen_reader_active:
                return {
                    "success": False,
                    "message": "Screen reader already running",
                    "action": "start_screen_reader"
                }
            
            self.screen_reader_active = True
            self.ocr_callback = callback
            
            def reader_loop():
                """Background OCR loop."""
                while self.screen_reader_active:
                    try:
                        # Take screenshot and OCR
                        result = self.get_screen_text()
                        
                        if result.get('success') and result.get('text'):
                            # Call callback with result
                            if self.ocr_callback:
                                self.ocr_callback(result)
                            else:
                                print(f"📝 OCR Result: {result['text'][:100]}...")
                        
                        # Wait for next scan
                        time.sleep(interval)
                        
                    except Exception as e:
                        print(f"Screen reader error: {e}")
                        time.sleep(1)
            
            # Start background thread
            self.screen_reader_thread = threading.Thread(target=reader_loop, daemon=True)
            self.screen_reader_thread.start()
            
            return {
                "success": True,
                "message": f"Screen reader started (interval: {interval}s)",
                "interval": interval,
                "action": "start_screen_reader"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def stop_screen_reader(self) -> Dict[str, Any]:
        """
        Stop the continuous screen reader.
        
        Returns:
            Status dictionary
        """
        try:
            if not self.screen_reader_active:
                return {
                    "success": False,
                    "message": "Screen reader not running",
                    "action": "stop_screen_reader"
                }
            
            self.screen_reader_active = False
            
            if self.screen_reader_thread:
                self.screen_reader_thread.join(timeout=3)
            
            return {
                "success": True,
                "message": "Screen reader stopped",
                "action": "stop_screen_reader"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def is_screen_reader_active(self) -> bool:
        """Check if screen reader is running."""
        return self.screen_reader_active

    # ============== Utilities ==============

    def get_screenshot_history(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get list of recent screenshots.
        
        Args:
            limit: Maximum number of screenshots to return
            
        Returns:
            Dictionary with screenshot list
        """
        try:
            if not os.path.exists(self.screenshot_dir):
                return {
                    "success": False,
                    "message": "Screenshot directory not found",
                    "action": "get_screenshot_history"
                }
            
            # Get PNG files sorted by modification time
            files = []
            for filename in os.listdir(self.screenshot_dir):
                if filename.lower().endswith('.png'):
                    filepath = os.path.join(self.screenshot_dir, filename)
                    files.append({
                        "name": filename,
                        "path": filepath,
                        "size": os.path.getsize(filepath),
                        "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                    })
            
            # Sort by modification time (newest first)
            files.sort(key=lambda x: x['modified'], reverse=True)
            
            return {
                "success": True,
                "screenshots": files[:limit],
                "total_count": len(files),
                "returned_count": len(files[:limit]),
                "directory": self.screenshot_dir,
                "action": "get_screenshot_history"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def clear_screenshots(self) -> Dict[str, Any]:
        """
        Delete all screenshots.
        
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(self.screenshot_dir):
                return {
                    "success": True,
                    "message": "Screenshot directory does not exist",
                    "action": "clear_screenshots"
                }
            
            deleted_count = 0
            
            for filename in os.listdir(self.screenshot_dir):
                if filename.lower().endswith('.png'):
                    filepath = os.path.join(self.screenshot_dir, filename)
                    os.remove(filepath)
                    deleted_count += 1
            
            return {
                "success": True,
                "message": f"Deleted {deleted_count} screenshot(s)",
                "deleted_count": deleted_count,
                "action": "clear_screenshots"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_screenshot_directory(self) -> str:
        """Get screenshot directory path."""
        return self.screenshot_dir

    def get_status(self) -> Dict[str, Any]:
        """Get screenshot tool status."""
        return {
            "available": True,
            "screenshot_dir": self.screenshot_dir,
            "screen_reader_active": self.screen_reader_active,
            "ocr_available": self._is_pytesseract_available()
        }

    def _is_pytesseract_available(self) -> bool:
        """Check if pytesseract is installed."""
        try:
            import pytesseract
            return True
        except ImportError:
            return False
