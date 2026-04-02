"""
ZARA - Advanced Real-time Intelligent Assistant
App Manager Module - Application launch and management
"""

import subprocess
import os
import psutil
import pygetwindow as gw
from typing import List, Dict, Any, Optional
from config import APP_PATHS


class AppManager:
    """
    Application management - open, close, and focus apps.
    Handles launching applications and managing running processes.
    """

    def __init__(self):
        """Initialize app manager with app paths from config."""
        self.app_paths = APP_PATHS

    def _expand_path(self, path: str) -> str:
        """
        Expand environment variables in path.
        
        Args:
            path: Path with potential environment variables
            
        Returns:
            Expanded path
        """
        return os.path.expandvars(path)

    def _find_app_path(self, app_name: str) -> tuple:
        """
        Find app path from APP_PATHS by name matching.
        
        Args:
            app_name: Application name to find
            
        Returns:
            Tuple of (matched_name, path) or (None, None)
        """
        app_name_lower = app_name.lower().strip()
        
        # Direct match
        if app_name_lower in self.app_paths:
            return app_name_lower, self.app_paths[app_name_lower]
        
        # Partial match
        for name, path in self.app_paths.items():
            if name.lower() in app_name_lower or app_name_lower in name.lower():
                return name, path
        
        # Try common aliases
        aliases = {
            "browser": "chrome",
            "internet": "chrome",
            "web": "chrome",
            "notes": "notepad",
            "text": "notepad",
            "calc": "calculator",
            "files": "file explorer",
            "folder": "file explorer",
            "music": "spotify",
            "video": "vlc",
            "media": "vlc",
        }
        
        if app_name_lower in aliases:
            return self._find_app_path(aliases[app_name_lower])
        
        return None, None

    def open_app(self, app_name: str) -> Dict[str, Any]:
        """
        Open an application.
        
        Args:
            app_name: Name of the application to open
            
        Returns:
            Status dictionary
        """
        app_name_lower = app_name.lower().strip()
        
        # Find app in paths
        matched_name, app_path = self._find_app_path(app_name_lower)
        
        if not app_path:
            # Try to open as direct command/executable
            app_path = app_name_lower
            matched_name = app_name_lower
        
        try:
            expanded_path = self._expand_path(app_path)
            
            # Check if it's a URI scheme (like ms-settings:, mailto:, etc.)
            if ':' in expanded_path and not os.path.exists(expanded_path):
                os.startfile(expanded_path)
                return {
                    "success": True,
                    "message": f"Opening {matched_name}",
                    "app": matched_name,
                    "type": "uri"
                }
            
            # Check if file exists
            if os.path.exists(expanded_path):
                subprocess.Popen(expanded_path, shell=True)
                return {
                    "success": True,
                    "message": f"Opened {matched_name}",
                    "app": matched_name,
                    "path": expanded_path
                }
            else:
                # Try as command
                subprocess.Popen(expanded_path, shell=True)
                return {
                    "success": True,
                    "message": f"Launching {matched_name}",
                    "app": matched_name,
                    "command": expanded_path
                }
                
        except FileNotFoundError:
            return {
                "success": False,
                "message": f"Application '{matched_name}' not found",
                "app": matched_name,
                "error": "not_found"
            }
        except PermissionError:
            return {
                "success": False,
                "message": f"Permission denied to open {matched_name}",
                "app": matched_name,
                "error": "permission_denied"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error opening {matched_name}",
                "app": matched_name,
                "error": str(e)
            }

    def close_app(self, app_name: str) -> Dict[str, Any]:
        """
        Close an application by name (graceful terminate).
        
        Args:
            app_name: Name of the application to close
            
        Returns:
            Status dictionary
        """
        app_name_lower = app_name.lower().strip()
        
        try:
            closed_count = 0
            terminated_processes = []
            
            for proc in psutil.process_iter(['name', 'pid', 'exe']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    # Check if process name matches
                    if app_name_lower in proc_name or proc_name in app_name_lower:
                        proc.terminate()  # Graceful terminate
                        closed_count += 1
                        terminated_processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name']
                        })
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed_count > 0:
                return {
                    "success": True,
                    "message": f"Closed {closed_count} instance(s) of {app_name}",
                    "count": closed_count,
                    "processes": terminated_processes
                }
            else:
                return {
                    "success": False,
                    "message": f"No running instance of {app_name} found",
                    "app": app_name
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def force_close_app(self, app_name: str) -> Dict[str, Any]:
        """
        Force close an application (kill process).
        
        Args:
            app_name: Name of the application to kill
            
        Returns:
            Status dictionary
        """
        app_name_lower = app_name.lower().strip()
        
        try:
            killed_count = 0
            killed_processes = []
            
            for proc in psutil.process_iter(['name', 'pid']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    if app_name_lower in proc_name or proc_name in app_name_lower:
                        proc.kill()  # Force kill
                        killed_count += 1
                        killed_processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name']
                        })
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if killed_count > 0:
                return {
                    "success": True,
                    "message": f"Force closed {killed_count} instance(s) of {app_name}",
                    "count": killed_count,
                    "processes": killed_processes
                }
            else:
                return {
                    "success": False,
                    "message": f"No running instance of {app_name} found",
                    "app": app_name
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_running_apps(self) -> List[str]:
        """
        Get list of running application names.
        
        Returns:
            Sorted list of unique app names
        """
        apps = []
        seen = set()
        
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name']
                if name and name not in seen:
                    apps.append(name)
                    seen.add(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return sorted(apps)

    def is_app_running(self, app_name: str) -> bool:
        """
        Check if an application is running.
        
        Args:
            app_name: Name of the application
            
        Returns:
            True if running, False otherwise
        """
        app_name_lower = app_name.lower().strip()
        
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()
                if app_name_lower in proc_name or proc_name in app_name_lower:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return False

    def focus_app(self, app_name: str) -> Dict[str, Any]:
        """
        Bring application window to front.
        
        Args:
            app_name: Name of the application to focus
            
        Returns:
            Status dictionary
        """
        app_name_lower = app_name.lower().strip()
        
        try:
            # Get all windows
            windows = gw.getAllWindows()
            
            for window in windows:
                if app_name_lower in window.title.lower():
                    window.activate()
                    window.bring_to_front()
                    
                    return {
                        "success": True,
                        "message": f"Focused: {window.title}",
                        "title": window.title,
                        "app": app_name
                    }
            
            return {
                "success": False,
                "message": f"No window found for {app_name}",
                "app": app_name
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_app_windows(self, app_name: str) -> List[Dict[str, Any]]:
        """
        Get all windows for an application.
        
        Args:
            app_name: Name of the application
            
        Returns:
            List of window info dictionaries
        """
        app_name_lower = app_name.lower().strip()
        windows_info = []
        
        try:
            windows = gw.getAllWindows()
            
            for window in windows:
                if app_name_lower in window.title.lower():
                    windows_info.append({
                        "title": window.title,
                        "left": window.left,
                        "top": window.top,
                        "width": window.width,
                        "height": window.height,
                        "is_active": window.isActive,
                        "is_minimized": window.isMinimized,
                        "is_maximized": window.isMaximized
                    })
        except Exception as e:
            pass
        
        return windows_info

    def get_running_app_count(self) -> int:
        """
        Get number of running applications.
        
        Returns:
            Count of running processes
        """
        return len(psutil.pids())

    def get_app_process_info(self, app_name: str) -> List[Dict[str, Any]]:
        """
        Get detailed process info for an app.
        
        Args:
            app_name: Name of the application
            
        Returns:
            List of process info dictionaries
        """
        app_name_lower = app_name.lower().strip()
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info', 'exe']):
            try:
                proc_name = proc.info['name'].lower()
                
                if app_name_lower in proc_name or proc_name in app_name_lower:
                    mem_info = proc.info['memory_info']
                    processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "exe": proc.info['exe'],
                        "cpu_percent": proc.info['cpu_percent'],
                        "memory_percent": proc.info['memory_percent'],
                        "memory_mb": round(mem_info.rss / (1024 * 1024), 2) if mem_info else 0,
                        "status": proc.status()
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return processes

    def restart_app(self, app_name: str) -> Dict[str, Any]:
        """
        Restart an application.
        
        Args:
            app_name: Name of the application to restart
            
        Returns:
            Status dictionary
        """
        # Close the app first
        close_result = self.close_app(app_name)
        
        if not close_result.get('success'):
            # Try force close
            self.force_close_app(app_name)
        
        # Wait a moment
        import time
        time.sleep(1)
        
        # Open the app
        return self.open_app(app_name)

    def get_openable_apps(self) -> List[str]:
        """
        Get list of apps that can be opened.
        
        Returns:
            List of app names from APP_PATHS
        """
        return list(self.app_paths.keys())
