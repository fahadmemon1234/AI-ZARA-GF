"""
ZARA - Advanced Real-time Intelligent Assistant
News Fetcher Module - Real-time news headlines
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional
import xml.etree.ElementTree as ET


class NewsFetcher:
    """
    News fetching from various sources.
    Handles top news, topic-based news, and article summarization.
    """

    def __init__(self):
        """Initialize news fetcher."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = 10

    def get_top_news(self, category: str = 'general', count: int = 5) -> Dict[str, Any]:
        """
        Get top headlines from Google News RSS.
        
        Args:
            category: News category (general, world, business, tech, etc.)
            count: Number of articles to return (default: 5)
            
        Returns:
            Dictionary with news articles
        """
        try:
            # Google News RSS feeds
            rss_urls = {
                'general': 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en',
                'world': 'https://news.google.com/rss/topic/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZ4ZDQ0U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
                'business': 'https://news.google.com/rss/topic/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZ6Ykd3U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
                'tech': 'https://news.google.com/rss/topic/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
                'sports': 'https://news.google.com/rss/topic/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFQ0Y1djU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
                'entertainment': 'https://news.google.com/rss/topic/CAAqJggKIiBDQkFTRWdvSUwyMHZNRE55YXk0U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
                'science': 'https://news.google.com/rss/topic/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp5YXpjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
                'health': 'https://news.google.com/rss/topic/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZ6Ykd3U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
            }
            
            url = rss_urls.get(category.lower(), rss_urls['general'])
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "Could not fetch news",
                    "action": "get_top_news"
                }
            
            # Parse RSS feed
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            articles = []
            for item in items[:count]:
                title = item.find('title').text if item.find('title') is not None else "No title"
                link = item.find('link').text if item.find('link') is not None else ""
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                source = item.find('source').text if item.find('source') is not None else "Google News"
                
                articles.append({
                    "title": title,
                    "link": link,
                    "published": pub_date,
                    "source": source
                })
            
            return {
                "success": True,
                "message": f"Retrieved {len(articles)} news articles",
                "category": category,
                "articles": articles,
                "count": len(articles),
                "action": "get_top_news"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_news_by_topic(self, topic: str, count: int = 5) -> Dict[str, Any]:
        """
        Search news by keyword/topic.
        
        Args:
            topic: Topic/keyword to search
            count: Number of articles to return
            
        Returns:
            Dictionary with news articles
        """
        try:
            # Google News search RSS
            url = f"https://news.google.com/rss/search?q={topic.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
            
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "Could not fetch news",
                    "action": "get_news_by_topic"
                }
            
            # Parse RSS feed
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            articles = []
            for item in items[:count]:
                title = item.find('title').text if item.find('title') is not None else "No title"
                link = item.find('link').text if item.find('link') is not None else ""
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                
                articles.append({
                    "title": title,
                    "link": link,
                    "published": pub_date
                })
            
            return {
                "success": True,
                "message": f"Found {len(articles)} articles about '{topic}'",
                "topic": topic,
                "articles": articles,
                "count": len(articles),
                "action": "get_news_by_topic"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def read_news_aloud(self, news_list: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Format news for reading aloud.
        
        Args:
            news_list: List of news articles
            
        Returns:
            Formatted text for TTS
        """
        try:
            if not news_list:
                return {
                    "success": False,
                    "message": "No news articles provided",
                    "action": "read_news_aloud"
                }
            
            # Format for reading
            formatted_parts = []
            formatted_parts.append("Here are the top news headlines:")
            
            for i, article in enumerate(news_list[:5], 1):
                title = article.get('title', 'No title')
                # Clean title for TTS
                title = title.replace('|', '').replace('-', '').replace('&', 'and')
                formatted_parts.append(f"{i}. {title}")
            
            formatted_text = "\n".join(formatted_parts)
            
            return {
                "success": True,
                "message": "News formatted for reading",
                "text": formatted_text,
                "article_count": len(news_list[:5]),
                "action": "read_news_aloud"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_pakistan_news(self, count: int = 5) -> Dict[str, Any]:
        """
        Get Pakistan-specific news.
        
        Args:
            count: Number of articles to return
            
        Returns:
            Dictionary with news articles
        """
        try:
            # Pakistan news from Google News
            url = "https://news.google.com/rss/search?q=pakistan&hl=en-US&gl=PK&ceid=PK:en"
            
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "Could not fetch Pakistan news",
                    "action": "get_pakistan_news"
                }
            
            # Parse RSS feed
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            articles = []
            for item in items[:count]:
                title = item.find('title').text if item.find('title') is not None else "No title"
                link = item.find('link').text if item.find('link') is not None else ""
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                
                articles.append({
                    "title": title,
                    "link": link,
                    "published": pub_date
                })
            
            return {
                "success": True,
                "message": f"Retrieved {len(articles)} Pakistan news articles",
                "articles": articles,
                "count": len(articles),
                "action": "get_pakistan_news"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_tech_news(self, count: int = 5) -> Dict[str, Any]:
        """
        Get technology news.
        
        Args:
            count: Number of articles to return
            
        Returns:
            Dictionary with tech news articles
        """
        try:
            return self.get_top_news(category='tech', count=count)
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_business_news(self, count: int = 5) -> Dict[str, Any]:
        """
        Get business news.
        
        Args:
            count: Number of articles to return
            
        Returns:
            Dictionary with business news articles
        """
        try:
            return self.get_top_news(category='business', count=count)
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_sports_news(self, count: int = 5) -> Dict[str, Any]:
        """
        Get sports news.
        
        Args:
            count: Number of articles to return
            
        Returns:
            Dictionary with sports news articles
        """
        try:
            return self.get_top_news(category='sports', count=count)
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def summarize_article(self, url: str) -> Dict[str, Any]:
        """
        Fetch URL and summarize article content.
        
        Args:
            url: Article URL
            
        Returns:
            Dictionary with article summary
        """
        try:
            if not url:
                return {
                    "success": False,
                    "message": "No URL provided",
                    "action": "summarize_article"
                }
            
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "Could not fetch article",
                    "action": "summarize_article"
                }
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                script.decompose()
            
            # Try to find article title
            title = None
            for title_tag in ['h1', 'title']:
                title_elem = soup.find(title_tag)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if title_tag == 'h1':
                        break
            
            # Get main content
            # Try common article containers
            article_content = None
            for class_name in ['article-content', 'article-body', 'post-content', 'entry-content', 'article']:
                article_content = soup.find('div', class_=class_name)
                if article_content:
                    break
            
            if not article_content:
                # Get all paragraphs
                paragraphs = soup.find_all('p')
                content = '\n'.join([p.get_text(strip=True) for p in paragraphs[:10]])
            else:
                paragraphs = article_content.find_all('p')
                content = '\n'.join([p.get_text(strip=True) for p in paragraphs[:10]])
            
            # Create summary (first 300 chars)
            summary = content[:300] + "..." if len(content) > 300 else content
            
            return {
                "success": True,
                "message": "Article summarized",
                "url": url,
                "title": title if title else "No title found",
                "summary": summary,
                "content_length": len(content),
                "action": "summarize_article"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_bbc_news(self, count: int = 5) -> Dict[str, Any]:
        """
        Get news from BBC.
        
        Args:
            count: Number of articles to return
            
        Returns:
            Dictionary with BBC news articles
        """
        try:
            url = "http://feeds.bbci.co.uk/news/rss.xml"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "Could not fetch BBC news",
                    "action": "get_bbc_news"
                }
            
            root = ET.fromstring(response.content)
            channel = root.find('channel')
            items = channel.findall('item')[:count]
            
            articles = []
            for item in items:
                title = item.find('title').text if item.find('title') is not None else "No title"
                link = item.find('link').text if item.find('link') is not None else ""
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                desc = item.find('description').text if item.find('description') is not None else ""
                
                articles.append({
                    "title": title,
                    "link": link,
                    "published": pub_date,
                    "description": desc[:200] if desc else "",
                    "source": "BBC"
                })
            
            return {
                "success": True,
                "message": f"Retrieved {len(articles)} BBC news articles",
                "articles": articles,
                "count": len(articles),
                "action": "get_bbc_news"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_reuters_news(self, count: int = 5) -> Dict[str, Any]:
        """
        Get news from Reuters.
        
        Args:
            count: Number of articles to return
            
        Returns:
            Dictionary with Reuters news articles
        """
        try:
            url = "https://www.reutersagency.com/feed/"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "Could not fetch Reuters news",
                    "action": "get_reuters_news"
                }
            
            root = ET.fromstring(response.content)
            channel = root.find('channel')
            items = channel.findall('item')[:count]
            
            articles = []
            for item in items:
                title = item.find('title').text if item.find('title') is not None else "No title"
                link = item.find('link').text if item.find('link') is not None else ""
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                
                articles.append({
                    "title": title,
                    "link": link,
                    "published": pub_date,
                    "source": "Reuters"
                })
            
            return {
                "success": True,
                "message": f"Retrieved {len(articles)} Reuters news articles",
                "articles": articles,
                "count": len(articles),
                "action": "get_reuters_news"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get news fetcher status."""
        return {
            "available": True,
            "sources": ["Google News", "BBC", "Reuters"],
            "categories": ["general", "world", "business", "tech", "sports", "entertainment", "science", "health"],
            "capabilities": [
                "get_top_news", "get_news_by_topic", "read_news_aloud",
                "get_pakistan_news", "get_tech_news", "summarize_article"
            ]
        }
