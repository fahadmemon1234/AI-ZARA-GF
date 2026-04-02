"""
ZARA - Advanced Real-time Intelligent Assistant
Google Search Module - Web search, weather, datetime
"""

import webbrowser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, Any, Optional


class GoogleSearch:
    """
    Google search and information retrieval.
    Handles web searches, weather, datetime, and website opening.
    """

    def __init__(self):
        """Initialize Google search."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = 10  # Request timeout in seconds

    def search(self, query: str) -> Dict[str, Any]:
        """
        Search Google (opens in browser).
        
        Args:
            query: Search query
            
        Returns:
            Status dictionary
        """
        try:
            if not query:
                return {
                    "success": False,
                    "message": "No search query provided",
                    "action": "search"
                }
            
            # Create Google search URL
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": f"Searching for: {query}",
                "query": query,
                "url": url,
                "action": "search"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def search_and_summarize(self, query: str, count: int = 1) -> Dict[str, Any]:
        """
        Search Google and summarize first result.
        Scrapes the first search result and returns summary.
        
        Args:
            query: Search query
            count: Number of results to summarize (default: 1)
            
        Returns:
            Dictionary with summary
        """
        try:
            # Search Google
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "Could not fetch search results",
                    "action": "search_and_summarize"
                }
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find search results
            results = []
            search_results = soup.find_all('div', class_='g')[:count]
            
            for result in search_results:
                try:
                    title_elem = result.find('h3')
                    link_elem = result.find('a')
                    snippet_elem = result.find('div', class_='VwiC3b')
                    
                    if title_elem and link_elem:
                        results.append({
                            "title": title_elem.get_text(),
                            "url": link_elem.get('href'),
                            "snippet": snippet_elem.get_text() if snippet_elem else "No description available"
                        })
                except:
                    continue
            
            if not results:
                # Try alternative selector
                search_results = soup.find_all('div', class_='yuRUbf')[:count]
                for result in search_results:
                    try:
                        title_elem = result.find('h3')
                        link_elem = result.find('a')
                        
                        if title_elem and link_elem:
                            results.append({
                                "title": title_elem.get_text(),
                                "url": link_elem.get('href'),
                                "snippet": "No description available"
                            })
                    except:
                        continue
            
            if not results:
                return {
                    "success": False,
                    "message": "No results found",
                    "action": "search_and_summarize"
                }
            
            # Fetch and summarize first result
            first_result = results[0]
            summary = self._fetch_page_summary(first_result['url'])
            
            return {
                "success": True,
                "message": f"Found and summarized: {first_result['title']}",
                "query": query,
                "result": {
                    "title": first_result['title'],
                    "url": first_result['url'],
                    "snippet": first_result['snippet'],
                    "summary": summary
                },
                "action": "search_and_summarize"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _fetch_page_summary(self, url: str, max_length: int = 500) -> str:
        """Fetch and summarize a webpage."""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return "Could not fetch page content"
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'header', 'footer']):
                script.decompose()
            
            # Get text content
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Truncate to max length
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            return text if text else "No content available"
            
        except:
            return "Could not fetch page content"

    def get_datetime(self) -> Dict[str, str]:
        """
        Get current date and time.
        
        Returns:
            Formatted date and time dictionary
        """
        try:
            now = datetime.now()
            
            return {
                "success": True,
                "date": now.strftime("%A, %B %d, %Y"),
                "time": now.strftime("%I:%M %p"),
                "day": now.strftime("%A"),
                "month": now.strftime("%B"),
                "year": now.strftime("%Y"),
                "hour": now.strftime("%I"),
                "minute": now.strftime("%M"),
                "period": now.strftime("%p"),
                "full": now.strftime("%B %d, %Y at %I:%M %p"),
                "iso": now.isoformat(),
                "timestamp": int(now.timestamp())
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_time(self) -> Dict[str, str]:
        """
        Get current time.
        
        Returns:
            Time dictionary
        """
        try:
            now = datetime.now()
            
            return {
                "success": True,
                "time": now.strftime("%I:%M %p"),
                "hour": int(now.strftime("%H")),
                "minute": int(now.strftime("%M")),
                "period": now.strftime("%p"),
                "12hour": now.strftime("%I:%M %p"),
                "24hour": now.strftime("%H:%M")
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_date(self) -> Dict[str, str]:
        """
        Get current date.
        
        Returns:
            Date dictionary
        """
        try:
            now = datetime.now()
            
            return {
                "success": True,
                "date": now.strftime("%A, %B %d, %Y"),
                "day": now.strftime("%A"),
                "month": now.strftime("%B"),
                "day_num": now.strftime("%d"),
                "year": now.strftime("%Y"),
                "month_num": now.strftime("%m")
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Get weather information using wttr.in API.
        
        Args:
            city: City name
            
        Returns:
            Weather information dictionary
        """
        try:
            if not city:
                return {
                    "success": False,
                    "message": "No city provided",
                    "action": "get_weather"
                }
            
            # Use wttr.in API (free, no API key required)
            url = f"http://wttr.in/{city.replace(' ', '+')}?format=j1"
            
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "Could not fetch weather data",
                    "action": "get_weather"
                }
            
            data = response.json()
            
            # Extract weather info
            current = data.get('current_condition', [{}])[0]
            area = data.get('nearest_area', [{}])[0]
            
            city_name = area.get('areaName', [{}])[0].get('value', city)
            country = area.get('country', [{}])[0].get('value', '')
            
            return {
                "success": True,
                "city": city_name,
                "country": country,
                "temperature_c": current.get('temp_C', 'N/A'),
                "temperature_f": current.get('temp_F', 'N/A'),
                "condition": current.get('weatherDesc', [{}])[0].get('value', 'Unknown'),
                "humidity": current.get('humidity', 'N/A'),
                "wind_speed_kmph": current.get('windspeedKmph', 'N/A'),
                "wind_speed_mph": current.get('windspeedMiles', 'N/A'),
                "wind_direction": current.get('winddir16Point', 'N/A'),
                "pressure_mb": current.get('pressure', 'N/A'),
                "feels_like_c": current.get('FeelsLikeC', 'N/A'),
                "feels_like_f": current.get('FeelsLikeF', 'N/A'),
                "visibility_km": current.get('visibility', 'N/A'),
                "uv_index": current.get('uvIndex', 'N/A'),
                "action": "get_weather"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_website(self, url: str) -> Dict[str, Any]:
        """
        Open website in browser.
        
        Args:
            url: Website URL
            
        Returns:
            Status dictionary
        """
        try:
            if not url:
                return {
                    "success": False,
                    "message": "No URL provided",
                    "action": "open_website"
                }
            
            # Add https if not present
            if not url.startswith('http'):
                url = 'https://' + url
            
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": f"Opening: {url}",
                "url": url,
                "action": "open_website"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_popular_site(self, site_name: str) -> Dict[str, Any]:
        """
        Open popular website by name.
        
        Args:
            site_name: Site name (youtube, google, facebook, etc.)
            
        Returns:
            Status dictionary
        """
        try:
            sites = {
                'google': 'https://www.google.com',
                'youtube': 'https://www.youtube.com',
                'facebook': 'https://www.facebook.com',
                'twitter': 'https://www.twitter.com',
                'x': 'https://www.twitter.com',
                'instagram': 'https://www.instagram.com',
                'linkedin': 'https://www.linkedin.com',
                'reddit': 'https://www.reddit.com',
                'github': 'https://www.github.com',
                'stackoverflow': 'https://stackoverflow.com',
                'amazon': 'https://www.amazon.com',
                'netflix': 'https://www.netflix.com',
                'spotify': 'https://www.spotify.com',
                'whatsapp': 'https://web.whatsapp.com',
                'gmail': 'https://mail.google.com',
                'drive': 'https://drive.google.com',
                'maps': 'https://maps.google.com',
            }
            
            site_lower = site_name.lower().strip()
            
            if site_lower in sites:
                return self.open_website(sites[site_lower])
            else:
                return self.search(site_lower)
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def translate(self, text: str, from_lang: str = 'auto', to_lang: str = 'en') -> Dict[str, Any]:
        """
        Translate text using Google Translate (opens in browser).
        
        Args:
            text: Text to translate
            from_lang: Source language
            to_lang: Target language
            
        Returns:
            Status dictionary
        """
        try:
            url = f"https://translate.google.com/?sl={from_lang}&tl={to_lang}&text={text.replace(' ', '+')}"
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": f"Opening Google Translate",
                "text": text[:50],
                "from": from_lang,
                "to": to_lang,
                "url": url,
                "action": "translate"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get Google search status."""
        return {
            "available": True,
            "capabilities": [
                "search", "search_and_summarize", "get_datetime",
                "get_weather", "open_website", "translate"
            ]
        }
