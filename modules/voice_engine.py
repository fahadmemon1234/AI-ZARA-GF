"""
ARIA - Advanced Real-time Intelligent Assistant
Voice Engine Module - Speech-to-Text and Text-to-Speech (FEMALE VOICE ONLY)
"""

import pyttsx3
import speech_recognition as sr
import threading
import re


class VoiceEngine:
    """
    Voice input/output engine for ARIA.
    FEMALE VOICE ONLY - No male voice fallback allowed.
    """

    def __init__(self):
        """Initialize voice engine with female voice only."""
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self._setup_female_voice()

    def _setup_female_voice(self):
        """Force female voice only — no male voice fallback"""
        voices = self.engine.getProperty('voices')
        
        female_voice = None
        
        # Priority 1: Exact female voice names (Windows SAPI)
        preferred = [
            'zira',        # Microsoft Zira (US English Female)
            'hazel',       # Microsoft Hazel (UK English Female)
            'susan',       # Microsoft Susan
            'eva',         # Eva
            'linda',       # Linda
            'helen',       # Helen
            'female',      # Generic female
            'woman',       # Generic woman
        ]
        
        # Search by name match (case-insensitive)
        for name in preferred:
            for voice in voices:
                if name in voice.name.lower():
                    female_voice = voice
                    break
            if female_voice:
                break
        
        # Priority 2: Search by gender property
        if not female_voice:
            for voice in voices:
                if hasattr(voice, 'gender') and voice.gender == 'female':
                    female_voice = voice
                    break
        
        # Priority 3: Search by voice ID containing female indicators
        if not female_voice:
            for voice in voices:
                vid = voice.id.lower()
                if any(x in vid for x in ['zira', 'female', 'hazel', 'susan']):
                    female_voice = voice
                    break
        
        # Apply female voice — if none found, print warning (do NOT fall back to male)
        if female_voice:
            self.engine.setProperty('voice', female_voice.id)
            print(f"[ARIA Voice] Female voice set: {female_voice.name}")
        else:
            print("[ARIA Voice] WARNING: No female voice found.")
            print("[ARIA Voice] Please install Microsoft Zira via Windows Settings > Time & Language > Speech")
            # Still set voice properties for best quality
        
        # Voice properties optimized for female voice
        self.engine.setProperty('rate', 168)      # Natural speaking pace
        self.engine.setProperty('volume', 0.95)   # Clear volume
        self.engine.setProperty('pitch', 1.0)     # Natural pitch (pyttsx3 pitch is limited)

    def speak(self, text: str):
        """Speak text using female voice"""
        if not text:
            return
        # Clean text for better TTS
        clean = re.sub(r'[*_~`]', '', text)           # Remove markdown
        clean = re.sub(r'http\S+', 'link', clean)      # Replace URLs
        clean = re.sub(r'[^\w\s,.!?\'"-]', '', clean)  # Remove special chars
        
        self.engine.say(clean)
        self.engine.runAndWait()

    def speak_async(self, text: str):
        """Speak in background thread so it doesn't block"""
        t = threading.Thread(target=self.speak, args=(text,), daemon=True)
        t.start()

    def listen(self, timeout: int = 5, language: str = 'en-IN') -> str:
        """Listen for one voice command"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio, language=language)
                return text.lower().strip()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                return ""

    def listen_continuous(self, callback, wake_word: str = 'aria'):
        """Continuously listen in background, trigger callback on wake word"""
        def _listen_loop():
            self.is_listening = True
            while self.is_listening:
                command = self.listen(timeout=8)
                if command and wake_word in command:
                    clean = self.clean_command(command, wake_word)
                    if clean:
                        callback(clean)
        
        t = threading.Thread(target=_listen_loop, daemon=True)
        t.start()

    def stop_listening(self):
        self.is_listening = False

    def is_wake_word(self, text: str, wake_word: str = 'aria') -> bool:
        return wake_word in text.lower()

    def clean_command(self, text: str, wake_word: str = 'aria') -> str:
        """Remove wake word and return clean command"""
        text = text.lower().replace(wake_word, '').strip()
        text = re.sub(r'^[,.\s]+', '', text)
        return text.strip()

    def get_available_voices(self) -> list:
        """Return list of all available voices with details"""
        voices = self.engine.getProperty('voices')
        result = []
        for v in voices:
            result.append({
                'id': v.id,
                'name': v.name,
                'gender': getattr(v, 'gender', 'unknown'),
                'languages': getattr(v, 'languages', [])
            })
        return result

    def list_female_voices(self) -> list:
        """Return only female voices"""
        all_voices = self.get_available_voices()
        female_keywords = ['zira', 'hazel', 'susan', 'eva', 'female', 'woman', 'linda', 'helen']
        return [
            v for v in all_voices 
            if any(k in v['name'].lower() or k in v['id'].lower() for k in female_keywords)
            or v.get('gender') == 'female'
        ]
