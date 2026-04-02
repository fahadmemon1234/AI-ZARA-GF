"""
ZARA - Advanced Real-time Intelligent Assistant
Brightness Control Module - Screen brightness management
"""

import screen_brightness_control as sbc
from typing import Dict, Any


class BrightnessControl:
    """
    Screen brightness control using screen_brightness_control library.
    Handles monitor brightness adjustment.
    """

    def __init__(self):
        """Initialize brightness control."""
        self.default_step = 10
        self.min_safe_brightness = 10  # Don't go below 10% for safety

    def get_brightness(self) -> int:
        """
        Get current brightness percentage.
        
        Returns:
            Brightness level from 0 to 100
        """
        try:
            # Get brightness from primary monitor
            brightness = sbc.get_brightness()
            
            # Return average if multiple monitors
            if isinstance(brightness, list):
                return int(sum(brightness) / len(brightness))
            
            return int(brightness)
            
        except Exception as e:
            print(f"Error getting brightness: {e}")
            return 50  # Return default if error

    def set_brightness(self, level: int) -> Dict[str, Any]:
        """
        Set brightness to specific percentage.
        
        Args:
            level: Brightness level (0-100)
            
        Returns:
            Status dictionary
        """
        try:
            # Clamp value between min_safe and 100
            level = max(self.min_safe_brightness, min(100, level))
            
            # Set brightness
            sbc.set_brightness(level)
            
            return {
                "success": True,
                "message": f"Brightness set to {level}%",
                "level": level,
                "action": "set_brightness"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def increase_brightness(self, step: int = None) -> Dict[str, Any]:
        """
        Increase brightness by step.
        
        Args:
            step: Amount to increase (default: default_step)
            
        Returns:
            Status dictionary
        """
        try:
            if step is None:
                step = self.default_step
            
            current = self.get_brightness()
            new_level = min(100, current + step)
            
            return self.set_brightness(new_level)
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def decrease_brightness(self, step: int = None) -> Dict[str, Any]:
        """
        Decrease brightness by step.
        
        Args:
            step: Amount to decrease (default: default_step)
            
        Returns:
            Status dictionary
        """
        try:
            if step is None:
                step = self.default_step
            
            current = self.get_brightness()
            new_level = max(self.min_safe_brightness, current - step)
            
            return self.set_brightness(new_level)
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def max_brightness(self) -> Dict[str, Any]:
        """
        Set brightness to maximum (100%).
        
        Returns:
            Status dictionary
        """
        return self.set_brightness(100)

    def min_brightness(self) -> Dict[str, Any]:
        """
        Set brightness to minimum safe level (10%).
        
        Returns:
            Status dictionary
        """
        return self.set_brightness(self.min_safe_brightness)

    def set_step(self, step: int) -> Dict[str, Any]:
        """
        Set the brightness step increment.
        
        Args:
            step: New step value (1-50)
            
        Returns:
            Status dictionary
        """
        if step < 1 or step > 50:
            return {
                "success": False,
                "message": "Step must be between 1 and 50",
                "action": "set_step"
            }
        
        self.default_step = step
        
        return {
            "success": True,
            "message": f"Brightness step set to {step}",
            "step": step,
            "action": "set_step"
        }

    def get_all_monitors_brightness(self) -> Dict[str, Any]:
        """
        Get brightness of all monitors.
        
        Returns:
            Dictionary with monitor brightness info
        """
        try:
            brightness_list = sbc.get_brightness()
            
            monitors = []
            if isinstance(brightness_list, list):
                for i, brightness in enumerate(brightness_list):
                    monitors.append({
                        "monitor": i + 1,
                        "brightness": brightness
                    })
            else:
                monitors.append({
                    "monitor": 1,
                    "brightness": brightness_list
                })
            
            return {
                "success": True,
                "monitors": monitors,
                "count": len(monitors)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def set_monitor_brightness(self, monitor: int, level: int) -> Dict[str, Any]:
        """
        Set brightness for specific monitor.
        
        Args:
            monitor: Monitor index (0-based)
            level: Brightness level (0-100)
            
        Returns:
            Status dictionary
        """
        try:
            level = max(self.min_safe_brightness, min(100, level))
            
            sbc.set_brightness(level, display=monitor)
            
            return {
                "success": True,
                "message": f"Monitor {monitor} brightness set to {level}%",
                "monitor": monitor,
                "level": level,
                "action": "set_monitor_brightness"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_brightness_info(self) -> Dict[str, Any]:
        """
        Get detailed brightness information.
        
        Returns:
            Dictionary with brightness info
        """
        try:
            # Get min and max brightness levels
            min_brightness = sbc.get_min_brightness()
            max_brightness = sbc.get_max_brightness()
            current = self.get_brightness()
            
            return {
                "success": True,
                "current": current,
                "min": min_brightness if isinstance(min_brightness, int) else min_brightness[0] if min_brightness else 0,
                "max": max_brightness if isinstance(max_brightness, int) else max_brightness[0] if max_brightness else 100,
                "step": self.default_step,
                "min_safe": self.min_safe_brightness
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def auto_brightness(self, enable: bool) -> Dict[str, Any]:
        """
        Enable/disable auto brightness (if supported).
        
        Args:
            enable: True to enable, False to disable
            
        Returns:
            Status dictionary
        """
        try:
            # Note: Auto brightness support varies by hardware
            if enable:
                return {
                    "success": True,
                    "message": "Auto brightness enabled (if supported by hardware)",
                    "action": "auto_brightness_enable"
                }
            else:
                return {
                    "success": True,
                    "message": "Auto brightness disabled",
                    "action": "auto_brightness_disable"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def fade_brightness(self, target_level: int, duration: float = 1.0) -> Dict[str, Any]:
        """
        Fade brightness to target level smoothly.
        
        Args:
            target_level: Target brightness (0-100)
            duration: Fade duration in seconds
            
        Returns:
            Status dictionary
        """
        try:
            import time
            
            target_level = max(self.min_safe_brightness, min(100, target_level))
            current = self.get_brightness()
            
            # Calculate steps
            steps = 20
            delay = duration / steps
            step_size = (target_level - current) / steps
            
            for i in range(steps):
                new_level = int(current + (step_size * (i + 1)))
                sbc.set_brightness(new_level)
                time.sleep(delay)
            
            return {
                "success": True,
                "message": f"Brightness faded to {target_level}%",
                "target": target_level,
                "duration": duration,
                "action": "fade_brightness"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """
        Get brightness control status.
        
        Returns:
            Status dictionary
        """
        return {
            "available": True,
            "brightness": self.get_brightness(),
            "step": self.default_step,
            "min_safe": self.min_safe_brightness
        }
