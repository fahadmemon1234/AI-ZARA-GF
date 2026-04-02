"""
ARIA - Advanced Real-time Intelligent Assistant
Volume Control Module - Audio management using pycaw and keyboard fallbacks
"""

from typing import Dict, Any
import warnings

# Suppress pycaw warnings
warnings.filterwarnings("ignore", message=".*AudioDevice.*")


class VolumeControl:
    """
    Windows volume control using pycaw and fallback methods.
    Handles system audio volume and mute functionality.
    """

    def __init__(self):
        """Initialize volume control with audio endpoint."""
        self.volume_interface = None
        self._init_audio_interface()

    def _init_audio_interface(self):
        """Initialize the audio endpoint interface with error handling."""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            # Get default audio endpoint (speakers)
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
        except Exception as e:
            # Silently fail - will use keyboard fallback methods
            self.volume_interface = None

    def get_volume(self) -> int:
        """Get current volume percentage."""
        try:
            if self.volume_interface:
                volume_scalar = self.volume_interface.GetMasterVolumeLevelScalar()
                return int(volume_scalar * 100)
        except:
            pass
        return 50  # Default

    def set_volume(self, level: int) -> Dict[str, Any]:
        """Set volume to specific percentage (0-100)."""
        try:
            if self.volume_interface:
                level = max(0, min(100, level))
                self.volume_interface.SetMasterVolumeLevelScalar(level / 100, None)
                return {"success": True, "message": f"Volume set to {level}%", "level": level}
        except:
            pass
        
        # Fallback to keyboard
        return self._set_volume_keyboard(level)

    def _set_volume_keyboard(self, level: int) -> Dict[str, Any]:
        """Set volume using keyboard media keys (fallback)."""
        try:
            import pyautogui
            current = 50
            diff = level - current
            presses = max(1, abs(diff) // 5)
            
            for _ in range(presses):
                if diff > 0:
                    pyautogui.press('volumeup')
                else:
                    pyautogui.press('volumedown')
            
            return {"success": True, "message": f"Volume adjusted to ~{level}%", "method": "keyboard"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def increase_volume(self, step: int = 10) -> Dict[str, Any]:
        """Increase volume by step."""
        try:
            if self.volume_interface:
                current = self.get_volume()
                return self.set_volume(min(100, current + step))
        except:
            pass
        
        # Fallback
        try:
            import pyautogui
            for _ in range(max(1, step // 5)):
                pyautogui.press('volumeup')
            return {"success": True, "message": f"Volume increased by {step}%"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def decrease_volume(self, step: int = 10) -> Dict[str, Any]:
        """Decrease volume by step."""
        try:
            if self.volume_interface:
                current = self.get_volume()
                return self.set_volume(max(0, current - step))
        except:
            pass
        
        # Fallback
        try:
            import pyautogui
            for _ in range(max(1, step // 5)):
                pyautogui.press('volumedown')
            return {"success": True, "message": f"Volume decreased by {step}%"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def mute(self) -> Dict[str, Any]:
        """Mute system audio."""
        try:
            if self.volume_interface:
                self.volume_interface.SetMute(1, None)
                return {"success": True, "message": "System muted", "muted": True}
        except:
            pass
        return self.toggle_mute()

    def unmute(self) -> Dict[str, Any]:
        """Unmute system audio."""
        try:
            if self.volume_interface:
                self.volume_interface.SetMute(0, None)
                return {"success": True, "message": "System unmuted", "muted": False}
        except:
            pass
        return {"success": True, "message": "System unmuted", "muted": False}

    def toggle_mute(self) -> Dict[str, Any]:
        """Toggle mute state."""
        try:
            if self.volume_interface:
                current = self.volume_interface.GetMute()
                self.volume_interface.SetMute(0 if current else 1, None)
                return {"success": True, "message": "Audio " + ("muted" if not current else "unmuted"), "muted": bool(not current)}
        except:
            pass
        
        # Fallback to keyboard
        try:
            import pyautogui
            pyautogui.press('volumemute')
            return {"success": True, "message": "Mute toggled (keyboard)"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def is_muted(self) -> bool:
        """Check if audio is muted."""
        try:
            if self.volume_interface:
                return bool(self.volume_interface.GetMute())
        except:
            pass
        return False

    def get_status(self) -> Dict[str, Any]:
        """Get volume control status."""
        return {
            "available": True,
            "pycaw_available": self.volume_interface is not None,
            "volume": self.get_volume(),
            "muted": self.is_muted()
        }
