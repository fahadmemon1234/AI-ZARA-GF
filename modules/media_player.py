"""
ZARA - Advanced Real-time Intelligent Assistant
Media Player Module - YouTube, Spotify, browser control, media keys
"""

import webbrowser
import subprocess
import os
from typing import Dict, Any, Optional
import pyautogui


class MediaPlayer:
    """
    Media player control - YouTube, Spotify, local media, browser control.
    Handles media playback and zoom controls.
    """

    def __init__(self):
        """Initialize media player."""
        self.supported_media_extensions = [
            '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',  # Video
            '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'   # Audio
        ]

    # ============== YouTube ==============

    def play_youtube(self, query: str) -> Dict[str, Any]:
        """
        Play video on YouTube.
        Opens YouTube search in default browser.

        Args:
            query: Search query (song name, artist, etc.)

        Returns:
            Status dictionary
        """
        try:
            if not query:
                return {
                    "success": False,
                    "message": "No search query provided",
                    "action": "play_youtube"
                }

            # Create YouTube search URL
            search_query = query.replace(' ', '+')
            url = f"https://www.youtube.com/results?search_query={search_query}"
            
            # Open in browser
            webbrowser.open(url)

            return {
                "success": True,
                "message": f"Playing '{query}' on YouTube",
                "query": query,
                "url": url,
                "action": "youtube_play"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def play_youtube_direct(self, video_id: str) -> Dict[str, Any]:
        """
        Play specific YouTube video by ID.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Status dictionary
        """
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": "Opening YouTube video",
                "video_id": video_id,
                "url": url,
                "action": "youtube_play_direct"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_youtube_music(self) -> Dict[str, Any]:
        """
        Open YouTube Music.
        
        Returns:
            Status dictionary
        """
        try:
            url = "https://music.youtube.com"
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": "Opening YouTube Music",
                "url": url,
                "action": "youtube_music"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Spotify ==============

    def play_spotify(self, query: str) -> Dict[str, Any]:
        """
        Play on Spotify.
        Opens Spotify search in browser.
        
        Args:
            query: Search query (song, artist, playlist)
            
        Returns:
            Status dictionary
        """
        try:
            if not query:
                return {
                    "success": False,
                    "message": "No search query provided",
                    "action": "play_spotify"
                }
            
            # Create Spotify search URL
            search_query = query.replace(' ', '%20')
            url = f"https://open.spotify.com/search/{search_query}"
            
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": f"Playing '{query}' on Spotify",
                "query": query,
                "url": url,
                "action": "spotify_play"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def play_spotify_track(self, track_id: str) -> Dict[str, Any]:
        """
        Play specific Spotify track.
        
        Args:
            track_id: Spotify track ID
            
        Returns:
            Status dictionary
        """
        try:
            url = f"https://open.spotify.com/track/{track_id}"
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": "Opening Spotify track",
                "track_id": track_id,
                "url": url,
                "action": "spotify_play_track"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def play_spotify_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """
        Play Spotify playlist.
        
        Args:
            playlist_id: Spotify playlist ID
            
        Returns:
            Status dictionary
        """
        try:
            url = f"https://open.spotify.com/playlist/{playlist_id}"
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": "Opening Spotify playlist",
                "playlist_id": playlist_id,
                "url": url,
                "action": "spotify_play_playlist"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_spotify_app(self) -> Dict[str, Any]:
        """
        Open Spotify desktop app.
        
        Returns:
            Status dictionary
        """
        try:
            # Try to open Spotify using URI
            subprocess.Popen(["start", "spotify:"], shell=True)
            
            return {
                "success": True,
                "message": "Opening Spotify app",
                "action": "spotify_app"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Local Media ==============

    def play_local_file(self, filepath: str) -> Dict[str, Any]:
        """
        Play local media file.
        Uses default application for the file type.
        
        Args:
            filepath: Path to media file
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(filepath):
                return {
                    "success": False,
                    "message": f"File not found: {filepath}",
                    "action": "play_local_file"
                }
            
            # Check if it's a media file
            _, ext = os.path.splitext(filepath)
            
            if ext.lower() not in self.supported_media_extensions:
                return {
                    "success": False,
                    "message": f"Unsupported media format: {ext}",
                    "supported": self.supported_media_extensions,
                    "action": "play_local_file"
                }
            
            # Open with default application
            os.startfile(filepath)
            
            return {
                "success": True,
                "message": f"Playing: {os.path.basename(filepath)}",
                "filepath": filepath,
                "action": "play_local_file"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def play_with_vlc(self, filepath: str) -> Dict[str, Any]:
        """
        Play media file with VLC player.
        
        Args:
            filepath: Path to media file
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(filepath):
                return {
                    "success": False,
                    "message": f"File not found: {filepath}",
                    "action": "play_with_vlc"
                }
            
            # Common VLC paths
            vlc_paths = [
                r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
            ]
            
            vlc_path = None
            for path in vlc_paths:
                if os.path.exists(path):
                    vlc_path = path
                    break
            
            if not vlc_path:
                # Try to find VLC in PATH
                vlc_path = "vlc"
            
            subprocess.Popen([vlc_path, filepath])
            
            return {
                "success": True,
                "message": f"Playing in VLC: {os.path.basename(filepath)}",
                "filepath": filepath,
                "action": "play_with_vlc"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Media Controls ==============

    def pause_media(self) -> Dict[str, Any]:
        """
        Toggle play/pause using media key.
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.press('playpause')
            
            return {
                "success": True,
                "message": "Play/pause toggled",
                "action": "pause_media"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def next_track(self) -> Dict[str, Any]:
        """
        Skip to next track using media key.
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.press('nexttrack')
            
            return {
                "success": True,
                "message": "Next track",
                "action": "next_track"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def prev_track(self) -> Dict[str, Any]:
        """
        Go to previous track using media key.
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.press('previoustrack')
            
            return {
                "success": True,
                "message": "Previous track",
                "action": "prev_track"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def stop_media(self) -> Dict[str, Any]:
        """
        Stop media playback using media key.
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.press('stop')
            
            return {
                "success": True,
                "message": "Media stopped",
                "action": "stop_media"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Browser Control ==============

    def open_browser(self, url: str) -> Dict[str, Any]:
        """
        Open URL in default browser.
        
        Args:
            url: Website URL
            
        Returns:
            Status dictionary
        """
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": f"Opening {url}",
                "url": url,
                "action": "open_browser"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_website(self, site_name: str) -> Dict[str, Any]:
        """
        Open popular website by name.
        
        Args:
            site_name: Site name (youtube, google, spotify, netflix, etc.)
            
        Returns:
            Status dictionary
        """
        try:
            sites = {
                'youtube': 'https://www.youtube.com',
                'yt': 'https://www.youtube.com',
                'google': 'https://www.google.com',
                'spotify': 'https://open.spotify.com',
                'netflix': 'https://www.netflix.com',
                'prime': 'https://www.primevideo.com',
                'amazon': 'https://www.amazon.com',
                'twitter': 'https://www.twitter.com',
                'x': 'https://www.twitter.com',
                'facebook': 'https://www.facebook.com',
                'instagram': 'https://www.instagram.com',
                'reddit': 'https://www.reddit.com',
                'github': 'https://www.github.com',
                'stackoverflow': 'https://stackoverflow.com',
            }
            
            site_lower = site_name.lower().strip()
            
            if site_lower in sites:
                return self.open_browser(sites[site_lower])
            else:
                return self.open_browser(site_lower)
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Zoom Controls ==============

    def zoom_in(self) -> Dict[str, Any]:
        """
        Zoom in browser (Ctrl++).
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.hotkey('ctrl', '+')
            
            return {
                "success": True,
                "message": "Zoomed in",
                "action": "zoom_in"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def zoom_out(self) -> Dict[str, Any]:
        """
        Zoom out browser (Ctrl+-).
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.hotkey('ctrl', '-')
            
            return {
                "success": True,
                "message": "Zoomed out",
                "action": "zoom_out"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def zoom_reset(self) -> Dict[str, Any]:
        """
        Reset browser zoom (Ctrl+0).
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.hotkey('ctrl', '0')
            
            return {
                "success": True,
                "message": "Zoom reset",
                "action": "zoom_reset"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def set_zoom(self, level: int) -> Dict[str, Any]:
        """
        Set browser zoom to specific level.
        
        Args:
            level: Zoom percentage (50-200)
            
        Returns:
            Status dictionary
        """
        try:
            level = max(50, min(200, level))
            
            # Reset first
            self.zoom_reset()
            
            # Calculate number of zoom steps (each step is ~10%)
            steps = abs(level - 100) // 10
            
            if level > 100:
                for _ in range(steps):
                    self.zoom_in()
            elif level < 100:
                for _ in range(steps):
                    self.zoom_out()
            
            return {
                "success": True,
                "message": f"Zoom set to {level}%",
                "level": level,
                "action": "set_zoom"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Fullscreen ==============

    def toggle_fullscreen(self) -> Dict[str, Any]:
        """
        Toggle fullscreen mode (F11).
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.press('f11')
            
            return {
                "success": True,
                "message": "Fullscreen toggled",
                "action": "toggle_fullscreen"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def enter_fullscreen(self) -> Dict[str, Any]:
        """
        Enter fullscreen mode (F11).
        
        Returns:
            Status dictionary
        """
        return self.toggle_fullscreen()

    def exit_fullscreen(self) -> Dict[str, Any]:
        """
        Exit fullscreen mode (F11 or Esc).
        
        Returns:
            Status dictionary
        """
        try:
            pyautogui.press('f11')
            
            return {
                "success": True,
                "message": "Exited fullscreen",
                "action": "exit_fullscreen"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Status ==============

    def get_status(self) -> Dict[str, Any]:
        """
        Get media player status.
        
        Returns:
            Status dictionary
        """
        return {
            "available": True,
            "supported_formats": self.supported_media_extensions,
            "capabilities": [
                "youtube", "spotify", "local_media",
                "media_controls", "zoom_controls", "browser"
            ]
        }
