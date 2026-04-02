"""
ZARA - Advanced Real-time Intelligent Assistant
Multi-API Manager Module - Unified interface for all AI APIs
"""

import os
from typing import Dict, Any, Optional, List
from config import (
    ANTHROPIC_API_KEY,
    GEMINI_API_KEY,
    OPENAI_API_KEY,
    GROQ_API_KEY,
    ELEVENLABS_API_KEY,
    ELEVENLABS_VOICE_ID,
    MEM0_API_KEY,
    LIVEKIT_API_KEY,
    LIVEKIT_API_SECRET,
    LIVEKIT_URL
)


class MultiAPIManager:
    """
    Unified manager for multiple AI APIs.
    Supports: Groq (FREE), Anthropic Claude, Google Gemini, OpenAI GPT, ElevenLabs, LiveKit, Mem0
    """

    def __init__(self):
        """Initialize all API clients."""
        self.clients = {}
        self._init_groq()  # Initialize Groq FIRST (FREE + FAST!)
        self._init_anthropic()
        self._init_gemini()
        self._init_openai()
        self._init_elevenlabs()
        self._init_livekit()
        self._init_mem0()

    # ============== Groq (FREE + FAST!) ==============

    def _init_groq(self):
        """Initialize Groq client (FREE - Llama 3.1)."""
        if GROQ_API_KEY and GROQ_API_KEY != "gsk_your-groq-key-here":
            try:
                from groq import Groq
                self.clients['groq'] = Groq(api_key=GROQ_API_KEY)
                print("✅ Groq initialized (Llama 3.1 70B - FREE!)")
            except Exception as e:
                print(f"⚠️  Groq initialization error: {e}")
                self.clients['groq'] = None
        else:
            self.clients['groq'] = None

    def groq_chat(self, message: str, system_prompt: str = "", max_tokens: int = 200) -> Dict[str, Any]:
        """
        Chat with Groq Llama 3.1 (FREE!).
        
        Args:
            message: User message
            system_prompt: System instructions
            max_tokens: Maximum response tokens
            
        Returns:
            Response dictionary
        """
        client = self.clients.get('groq')
        if not client:
            return {
                "success": False,
                "reply": "Groq not available. Please check GROQ_API_KEY.",
                "model": "none",
                "provider": "groq"
            }

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Latest Llama 3.3 model
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )

            return {
                "success": True,
                "reply": response.choices[0].message.content.strip(),
                "model": "llama-3.3-70b-versatile",
                "provider": "groq",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens
                }
            }

        except Exception as e:
            return {
                "success": False,
                "reply": f"Groq error: {str(e)}",
                "model": "llama-3.1-70b-versatile",
                "provider": "groq"
            }

    # ============== Anthropic Claude ==============

    def _init_anthropic(self):
        """Initialize Anthropic Claude client."""
        if ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "your_anthropic_api_key_here":
            try:
                import anthropic
                self.clients['anthropic'] = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                print("✅ Anthropic Claude initialized")
            except Exception as e:
                print(f"⚠️  Anthropic initialization error: {e}")
                self.clients['anthropic'] = None
        else:
            self.clients['anthropic'] = None

    def claude_chat(self, message: str, system_prompt: str = "", max_tokens: int = 200) -> Dict[str, Any]:
        """
        Chat with Claude AI.
        
        Args:
            message: User message
            system_prompt: System instructions
            max_tokens: Maximum response tokens
            
        Returns:
            Response dictionary
        """
        client = self.clients.get('anthropic')
        if not client:
            return {
                "success": False,
                "reply": "Claude AI not available. Please check ANTHROPIC_API_KEY.",
                "model": "none",
                "provider": "anthropic"
            }

        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": message}]
            )

            return {
                "success": True,
                "reply": response.content[0].text.strip(),
                "model": "claude-sonnet-4-20250514",
                "provider": "anthropic",
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }

        except Exception as e:
            return {
                "success": False,
                "reply": f"Claude error: {str(e)}",
                "model": "claude-sonnet-4-20250514",
                "provider": "anthropic"
            }

    # ============== Google Gemini ==============

    def _init_gemini(self):
        """Initialize Google Gemini client."""
        if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=GEMINI_API_KEY)
                # Try gemini-1.5-flash first (newer), fallback to gemini-pro
                try:
                    self.clients['gemini'] = genai.GenerativeModel('gemini-1.5-flash')
                    print("✅ Google Gemini initialized (gemini-1.5-flash)")
                except:
                    self.clients['gemini'] = genai.GenerativeModel('gemini-pro')
                    print("✅ Google Gemini initialized (gemini-pro)")
            except Exception as e:
                print(f"⚠️  Gemini initialization error: {e}")
                self.clients['gemini'] = None
        else:
            self.clients['gemini'] = None

    def gemini_chat(self, message: str, max_tokens: int = 200) -> Dict[str, Any]:
        """
        Chat with Google Gemini AI.
        
        Args:
            message: User message
            max_tokens: Maximum response tokens
            
        Returns:
            Response dictionary
        """
        client = self.clients.get('gemini')
        if not client:
            return {
                "success": False,
                "reply": "Gemini AI not available. Please check GEMINI_API_KEY.",
                "model": "none",
                "provider": "google"
            }

        try:
            response = client.generate_content(
                message,
                generation_config={
                    'max_output_tokens': max_tokens,
                    'temperature': 0.7,
                }
            )

            return {
                "success": True,
                "reply": response.text.strip(),
                "model": "gemini-1.5-flash",
                "provider": "google"
            }

        except Exception as e:
            return {
                "success": False,
                "reply": f"Gemini error: {str(e)}",
                "model": "gemini-1.5-flash",
                "provider": "google"
            }

    # ============== OpenAI GPT ==============

    def _init_openai(self):
        """Initialize OpenAI client."""
        if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
            try:
                from openai import OpenAI
                self.clients['openai'] = OpenAI(api_key=OPENAI_API_KEY)
                print("✅ OpenAI initialized")
            except Exception as e:
                print(f"⚠️  OpenAI initialization error: {e}")
                self.clients['openai'] = None
        else:
            self.clients['openai'] = None

    def openai_chat(self, message: str, system_prompt: str = "", model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
        """
        Chat with OpenAI GPT.
        
        Args:
            message: User message
            system_prompt: System instructions
            model: Model to use (gpt-3.5-turbo, gpt-4, etc.)
            
        Returns:
            Response dictionary
        """
        client = self.clients.get('openai')
        if not client:
            return {
                "success": False,
                "reply": "OpenAI not available. Please check OPENAI_API_KEY.",
                "model": "none",
                "provider": "openai"
            }

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=200,
                temperature=0.7
            )

            return {
                "success": True,
                "reply": response.choices[0].message.content.strip(),
                "model": model,
                "provider": "openai",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens
                }
            }

        except Exception as e:
            return {
                "success": False,
                "reply": f"OpenAI error: {str(e)}",
                "model": model,
                "provider": "openai"
            }

    # ============== ElevenLabs Voice Generation ==============

    def _init_elevenlabs(self):
        """Initialize ElevenLabs client."""
        if ELEVENLABS_API_KEY and ELEVENLABS_API_KEY != "your_elevenlabs_api_key_here":
            try:
                import requests
                self.clients['elevenlabs'] = {
                    'api_key': ELEVENLABS_API_KEY,
                    'voice_id': ELEVENLABS_VOICE_ID,
                    'requests': requests
                }
                print(f"✅ ElevenLabs initialized (Voice: {ELEVENLABS_VOICE_ID})")
            except Exception as e:
                print(f"⚠️  ElevenLabs initialization error: {e}")
                self.clients['elevenlabs'] = None
        else:
            self.clients['elevenlabs'] = None

    def elevenlabs_tts(self, text: str, voice_id: str = None) -> Dict[str, Any]:
        """
        Generate speech using ElevenLabs API directly (more reliable).
        
        Args:
            text: Text to convert to speech
            voice_id: Voice ID to use (default: from config)
            
        Returns:
            Response with audio base64
        """
        client = self.clients.get('elevenlabs')
        if not client:
            return {
                "success": False,
                "error": "ElevenLabs not available. Please check ELEVENLABS_API_KEY.",
                "provider": "elevenlabs"
            }

        try:
            voice_id = voice_id or client['voice_id']
            api_key = client['api_key']
            
            # Use direct HTTP request (more reliable than SDK)
            import requests
            import base64
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg"
            }
            
            data = {
                "text": text,
                "model_id": "eleven_flash_v2_5",  # Most realistic & natural voice model
                "voice_settings": {
                    "stability": 0.35,        # Lower = more expressive & emotional
                    "similarity_boost": 0.85, # Higher = more faithful to voice
                    "style": 0.50,            # Adds natural speech patterns
                    "use_speaker_boost": True # Enhances voice clarity
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                return {
                    "success": True,
                    "audio_base64": audio_base64,
                    "provider": "elevenlabs",
                    "voice_id": voice_id,
                    "text_length": len(text),
                    "model_id": "eleven_multilingual_v2"
                }
            else:
                error_detail = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                return {
                    "success": False,
                    "error": f"ElevenLabs API error {response.status_code}: {error_detail}",
                    "provider": "elevenlabs"
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "ElevenLabs request timed out",
                "provider": "elevenlabs"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"ElevenLabs error: {str(e)}",
                "provider": "elevenlabs"
            }

    def get_elevenlabs_voices(self) -> Dict[str, Any]:
        """
        Get list of available ElevenLabs voices.
        
        Returns:
            List of voices
        """
        client = self.clients.get('elevenlabs')
        if not client:
            return {
                "success": False,
                "voices": [],
                "provider": "elevenlabs"
            }

        try:
            url = "https://api.elevenlabs.io/v1/voices"
            headers = {
                "Accept": "application/json",
                "xi-api-key": client['api_key']
            }
            
            response = client['requests'].get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                voices = data.get('voices', [])
                return {
                    "success": True,
                    "voices": voices,
                    "count": len(voices),
                    "provider": "elevenlabs"
                }
            else:
                return {
                    "success": False,
                    "voices": [],
                    "provider": "elevenlabs"
                }

        except Exception as e:
            return {
                "success": False,
                "voices": [],
                "error": str(e),
                "provider": "elevenlabs"
            }

    # ============== LiveKit Real-Time Communication ==============

    def _init_livekit(self):
        """Initialize LiveKit client."""
        if LIVEKIT_API_KEY and LIVEKIT_API_SECRET and LIVEKIT_URL:
            try:
                from livekit.api import AccessToken, TokenVerifier
                self.clients['livekit'] = {
                    'api_key': LIVEKIT_API_KEY,
                    'api_secret': LIVEKIT_API_SECRET,
                    'url': LIVEKIT_URL,
                    'token_generator': AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET),
                    'verifier': TokenVerifier(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
                }
                print(f"✅ LiveKit initialized ({LIVEKIT_URL})")
            except Exception as e:
                print(f"⚠️  LiveKit initialization error: {e}")
                self.clients['livekit'] = None
        else:
            self.clients['livekit'] = None

    def generate_livekit_token(self, room_name: str, participant_name: str, participant_id: str = None) -> Dict[str, Any]:
        """
        Generate LiveKit access token for real-time communication.
        
        Args:
            room_name: Room name to join
            participant_name: Participant name
            participant_id: Participant ID (optional)
            
        Returns:
            Token and connection info
        """
        client = self.clients.get('livekit')
        if not client:
            return {
                "success": False,
                "error": "LiveKit not available. Please check LIVEKIT_* environment variables.",
                "provider": "livekit"
            }

        try:
            from livekit.api import VideoGrants
            
            grants = VideoGrants(
                room_join=True,
                room=room_name
            )
            
            token = client['token_generator'].with_identity(participant_id or participant_name).with_name(participant_name).with_grants(grants).to_jwt()
            
            return {
                "success": True,
                "token": token,
                "url": client['url'],
                "room_name": room_name,
                "participant_name": participant_name,
                "provider": "livekit"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"LiveKit error: {str(e)}",
                "provider": "livekit"
            }

    # ============== Mem0 Memory Layer ==============

    def _init_mem0(self):
        """Initialize Mem0 client."""
        if MEM0_API_KEY and MEM0_API_KEY != "your_mem0_api_key_here":
            try:
                from mem0 import Memory
                # Mem0 initialization - config format may vary by version
                # Try multiple initialization methods
                try:
                    # Method 1: Simple initialization (no config)
                    self.clients['mem0'] = Memory()
                    print("✅ Mem0 memory layer initialized")
                except Exception as e1:
                    try:
                        # Method 2: Config dict
                        config = {
                            "api_key": MEM0_API_KEY,
                            "vector_store": {
                                "provider": "qdrant",
                                "config": {
                                    "collection_name": "aria-memory",
                                    "host": "localhost",
                                    "port": 6333,
                                }
                            }
                        }
                        self.clients['mem0'] = Memory(config=config)
                        print("✅ Mem0 memory layer initialized (config mode)")
                    except Exception as e2:
                        try:
                            # Method 3: API key parameter
                            self.clients['mem0'] = Memory(api_key=MEM0_API_KEY)
                            print("✅ Mem0 memory layer initialized (API key mode)")
                        except Exception as e3:
                            print(f"⚠️  Mem0 initialization error: {e3}")
                            self.clients['mem0'] = None
            except ImportError:
                print("ℹ️  Mem0 not installed (optional feature)")
                self.clients['mem0'] = None
            except Exception as e:
                print(f"⚠️  Mem0 initialization error: {e}")
                self.clients['mem0'] = None
        else:
            self.clients['mem0'] = None

    def mem0_add_memory(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        Add memory using Mem0.
        
        Args:
            user_id: User identifier
            message: Message to remember
            
        Returns:
            Status dictionary
        """
        client = self.clients.get('mem0')
        if not client:
            return {
                "success": False,
                "error": "Mem0 not available. Please check MEM0_API_KEY.",
                "provider": "mem0"
            }

        try:
            # Try different API formats
            try:
                result = client.add(message, user_id=user_id)
            except TypeError:
                # Fallback: simple add without user_id
                result = client.add(message)
            
            return {
                "success": True,
                "result": result if result else "Memory saved",
                "provider": "mem0"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Mem0 error: {str(e)}",
                "provider": "mem0"
            }

    def mem0_get_memories(self, user_id: str) -> Dict[str, Any]:
        """
        Get memories for a user using Mem0.
        
        Args:
            user_id: User identifier
            
        Returns:
            Memories list
        """
        client = self.clients.get('mem0')
        if not client:
            return {
                "success": False,
                "memories": [],
                "provider": "mem0"
            }

        try:
            # Try different API formats
            try:
                memories = client.get_all(user_id=user_id)
            except TypeError:
                # Fallback: get all without user_id
                memories = client.get_all()
            
            return {
                "success": True,
                "memories": memories if memories else [],
                "count": len(memories) if memories else 0,
                "provider": "mem0"
            }

        except Exception as e:
            return {
                "success": False,
                "memories": [],
                "error": str(e),
                "provider": "mem0"
            }

    def mem0_search(self, user_id: str, query: str) -> Dict[str, Any]:
        """
        Search memories using Mem0.
        
        Args:
            user_id: User identifier
            query: Search query
            
        Returns:
            Search results
        """
        client = self.clients.get('mem0')
        if not client:
            return {
                "success": False,
                "results": [],
                "provider": "mem0"
            }

        try:
            # Try different API formats
            try:
                results = client.search(query, user_id=user_id)
            except TypeError:
                # Fallback: search without user_id
                results = client.search(query)
            
            return {
                "success": True,
                "results": results if results else [],
                "count": len(results) if results else 0,
                "provider": "mem0"
            }

        except Exception as e:
            return {
                "success": False,
                "results": [],
                "error": str(e),
                "provider": "mem0"
            }

    # ============== Unified Chat ==============

    def chat(self, message: str, provider: str = "auto", system_prompt: str = "") -> Dict[str, Any]:
        """
        Unified chat interface - automatically selects best available AI.
        Priority: Groq (FREE+FAST) → Google (FREE) → Anthropic (PAID) → OpenAI (PAID)
        
        Args:
            message: User message
            provider: Preferred provider (auto, groq, google, anthropic, openai)
            system_prompt: System instructions
            
        Returns:
            Response from best available AI
        """
        if provider == "auto":
            # Try in order: Groq (FREE+FAST) → Google (FREE) → Anthropic (PAID) → OpenAI (PAID)
            if self.clients.get('groq'):
                return self.groq_chat(message, system_prompt)
            elif self.clients.get('gemini'):
                return self.gemini_chat(message)
            elif self.clients.get('anthropic'):
                return self.claude_chat(message, system_prompt)
            elif self.clients.get('openai'):
                return self.openai_chat(message, system_prompt)
            else:
                return {
                    "success": False,
                    "reply": "No AI provider available. Please add a Groq API key (FREE!).",
                    "model": "none",
                    "provider": "none"
                }
        elif provider == "groq":
            return self.groq_chat(message, system_prompt)
        elif provider == "google":
            return self.gemini_chat(message)
        elif provider == "anthropic":
            return self.claude_chat(message, system_prompt)
        elif provider == "openai":
            return self.openai_chat(message, system_prompt)
        else:
            return self.chat(message, "auto", system_prompt)

    # ============== Status ==============

    def get_status(self) -> Dict[str, Any]:
        """Get status of all API clients."""
        return {
            "anthropic": {
                "available": self.clients.get('anthropic') is not None,
                "model": "claude-sonnet-4-20250514"
            },
            "google": {
                "available": self.clients.get('gemini') is not None,
                "model": "gemini-pro"
            },
            "openai": {
                "available": self.clients.get('openai') is not None,
                "models": ["gpt-3.5-turbo", "gpt-4"]
            },
            "elevenlabs": {
                "available": self.clients.get('elevenlabs') is not None,
                "voice_id": ELEVENLABS_VOICE_ID if self.clients.get('elevenlabs') else None
            },
            "livekit": {
                "available": self.clients.get('livekit') is not None,
                "url": LIVEKIT_URL if self.clients.get('livekit') else None
            },
            "mem0": {
                "available": self.clients.get('mem0') is not None
            }
        }
