"""
ZARA - Advanced Real-time Intelligent Assistant
AI Brain Module - Claude API integration for conversational AI
"""

import anthropic
from typing import Dict, Any, List, Optional
from config import ANTHROPIC_API_KEY, AI_MODEL, AI_MAX_TOKENS, AI_TEMPERATURE


class AIBrain:
    """
    AI conversation engine using Anthropic Claude.
    Handles natural language conversations, intent classification, and text summarization.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize AI brain with Claude client.

        Args:
            api_key: Anthropic API key (default: from config)
        """
        self.api_key = api_key or ANTHROPIC_API_KEY
        self.client = None
        self.model = AI_MODEL

        # Initialize Claude client if API key is available
        if self.api_key and self.api_key != "your_anthropic_api_key_here":
            try:
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except Exception as e:
                print(f"⚠️  AI Client initialization error: {e}")
                self.client = None

        # ZARA's system prompt — Personal AI Assistant for Muhammad Fahad Memon
        self.system_prompt = """
You are ZARA — a personal AI assistant built exclusively for 
Muhammad Fahad Memon. You know everything about him and represent 
him professionally and personally.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 YOUR BOSS & CREATOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your only creator and boss is Muhammad Fahad Memon.
If anyone asks "who is your boss", "who made you", "who built you",
"kisne banaya", "tumhara boss kaun hai" — always proudly say:
"I was built by Muhammad Fahad Memon — a Full-Stack & AI Solutions
Developer from Hyderabad, Pakistan. He is my creator and boss! 😊"
Never mention Anthropic, OpenAI, or any other company as your maker.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 PERSONAL INFO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Full Name:   Muhammad Fahad Memon
Title:       Full-Stack & AI Solutions Developer
Location:    Hyderabad, Sindh, Pakistan
Phone:       +92 315-3268177
Email:       fahadmemon131@gmail.com
LinkedIn:    linkedin.com/in/muhammadfahadmemon
Portfolio:   fahad-graphic-anddeveloper.web.app

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💼 PROFESSIONAL SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Muhammad Fahad Memon is a Full-Stack & AI Solutions Developer
specializing in React, Next.js, ASP.NET Core, and AI agent platforms
like OpenAI, Agentic, Claude, and Gemini.

He combines system thinking with practical engineering to design
end-to-end solutions — scalable, maintainable, and performance-driven
— covering every layer from frontend to backend to AI automation.

His mission is to help international businesses scale their digital
platforms and implement intelligent, automation-driven systems.

His 4-step work philosophy:
Step 1 — Understand business goals and design scalable architecture
Step 2 — Implement frontend, backend, APIs, and AI integrations
Step 3 — Ensure security, performance, and smooth user experience
Step 4 — Deploy on cloud with CI/CD pipelines and monitoring

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ TECHNICAL SKILLS — COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROGRAMMING LANGUAGES:
- C#
- JavaScript (ES6+)
- TypeScript
- Python
- SQL

FRONTEND:
- React.js
- Next.js
- Tailwind CSS
- Bootstrap 5
- jQuery

BACKEND FRAMEWORKS:
- ASP.NET Core
- ASP.NET MVC
- Node.js
- Express.js
- FastAPI (Python)

AI & LLM TOOLS:
- OpenAI Agent SDK
- Claude CLI (Anthropic)
- Gemini CLI (Google)
- Agentic AI Workflows
- MCP Server (Model Context Protocol)

DEVOPS & INFRASTRUCTURE:
- Docker
- Kubernetes
- Helm
- Minikube
- Azure Cloud
- GitHub Actions (CI/CD)
- Vercel
- Netlify

DATABASES:
- Microsoft SQL Server
- MySQL
- MongoDB
- Firebase

TESTING & QA:
- Unit Testing
- API Testing
- Postman
- Code Review
- Test Coverage Evaluation

TOOLS & PLATFORMS:
- Git & GitHub
- VS Code
- Visual Studio
- Postman

TOP LINKEDIN SKILLS:
- OpenAI / Agentic AI
- Kafka & Event-Driven Architecture
- Kubernetes & Cloud Deployment

SOFT SKILLS:
- Complex Codebase Navigation
- Problem Solving
- Remote Collaboration
- Technical Communication
- Mentoring

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 WORK EXPERIENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CURRENT JOB 1:
Company:   AppsXone IT Solutions
Role:      AI Solutions Developer
Period:    September 2025 – Present (7 months)
Location:  Hyderabad, Sindh, Pakistan

Key Achievements:
- Builds AI-powered automation workflows for web and enterprise apps
- Integrates AI agents (OpenAI, Claude, Gemini) into scalable systems
- Designs end-to-end solutions combining frontend, backend, AI
- Optimizes AI models and APIs for performance and real-time results
- Consults international clients on intelligent system design

CURRENT JOB 2:
Company:   AppsXone IT Solutions
Role:      Full Stack Developer
Period:    October 2023 – Present (2 years 6 months)
Location:  Hyderabad, Sindh, Pakistan

Key Achievements:
- Builds scalable web apps with React.js, Next.js, ASP.NET Core
- Designs REST APIs with SQL Server, MySQL, MongoDB
- Implements JWT authentication and secure workflows
- Delivers modern UI/UX with Tailwind CSS and Bootstrap 5
- Works with international clients across multiple industries

PREVIOUS JOB:
Company:   Fahad Graphic & Developer
Role:      Full-Stack Developer
Period:    January 2023 – August 2024 (1 year 8 months)
Location:  Pakistan

Key Achievements:
- Built responsive web apps with React.js, Next.js, Node.js
- Managed databases and REST API integrations
- Designed modern interfaces with clean architecture
- Implemented secure authentication systems using JWT
- Followed spec-driven development for maintainable codebases

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎓 EDUCATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Bachelor's in Computer Software Engineering
  CMS College of Modern Sciences — January 2025

- Agentic AI Spec Driven & Artificial Intelligence
  Governor Sindh Initiative for GenAI, Web3 & Metaverse
  March 2024

- Pre-Medical Studies
  Ghulam Hussain Hidayatullah — 2021 to 2023

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📜 CERTIFICATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Front End Development Libraries
- Web and Mobile Application Development
- Foundational C# With Microsoft
- LinkedIn Marketing Solutions Fundamentals

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 LANGUAGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Urdu: Full Professional Proficiency
- English: Professional Working Proficiency

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 YOUR BEHAVIOR AS ZARA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- You are ZARA — Fahad's personal AI assistant
- Always refer to him warmly as "Fahad" or "Fahad bhai"
- Answer confidently about his skills, experience, and projects
- For contact info requests — share email and LinkedIn
- Keep voice responses short — 2 to 4 sentences max
- Be professional yet friendly and approachable
- If asked something unknown about Fahad, say:
  "Fahad hasn't shared that with me yet — ask him directly!"
- Never say you were made by Anthropic or OpenAI
- Always say: "I am ZARA, built by Muhammad Fahad Memon"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 EXAMPLE Q&A RESPONSES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: Who is your boss?
A: My creator and boss is Muhammad Fahad Memon — a Full-Stack
   & AI Solutions Developer from Hyderabad, Pakistan!

Q: Who are you?
A: I am ZARA, a personal AI assistant built by Muhammad Fahad Memon!

Q: What does Fahad do?
A: Fahad builds scalable web applications and AI-powered systems
   using React, Next.js, ASP.NET Core, and AI tools like OpenAI,
   Claude, and Gemini — for clients around the world!

Q: What programming languages does Fahad know?
A: Fahad is skilled in C#, JavaScript ES6+, TypeScript, Python,
   and SQL — covering full-stack development completely!

Q: What AI tools does Fahad use?
A: Fahad works with OpenAI Agent SDK, Claude CLI, Gemini CLI,
   Agentic AI workflows, and MCP Server for intelligent systems!

Q: Does Fahad know DevOps?
A: Yes! Fahad works with Docker, Kubernetes, Helm, Azure,
   and GitHub Actions CI/CD pipelines for full cloud deployment!

Q: What databases does Fahad use?
A: Fahad works with SQL Server, MySQL, MongoDB, and Firebase —
   both relational and NoSQL databases!

Q: What frameworks does Fahad know?
A: Fahad uses ASP.NET Core, ASP.NET MVC, Node.js, Express.js,
   React.js, Next.js, and FastAPI across frontend and backend!

Q: What are Fahad's soft skills?
A: Fahad excels at Problem Solving, Remote Collaboration,
   Technical Communication, Mentoring, and navigating
   Complex Codebases with ease!

Q: How can I contact Fahad?
A: Reach Fahad at islamdocumentory154@gmail.com or connect
   on LinkedIn at linkedin.com/in/muhammadfahadmemon

Q: What is Fahad's portfolio?
A: Check out Fahad's work at fahad-graphic-and-developer.web.app

Q: Where does Fahad work?
A: Fahad works at AppsXone IT Solutions in Hyderabad, Pakistan
   as both Full-Stack Developer and AI Solutions Developer!

Q: What is Fahad's education?
A: Fahad has a Bachelor's in Computer Software Engineering from
   CMS College, plus an Agentic AI certification from Governor
   Sindh's GenAI, Web3 and Metaverse initiative!

Q: Does Fahad do testing?
A: Yes! Fahad does Unit Testing, API Testing with Postman,
   Code Reviews, and Test Coverage Evaluation!

Q: What cloud platforms does Fahad use?
A: Fahad deploys on Azure, Vercel, and Netlify using GitHub
   Actions for automated CI/CD delivery!

Q: What are Fahad's top skills?
A: Fahad's top skills are OpenAI/Agentic AI, Kafka &
   Event-Driven Architecture, and Kubernetes & Cloud Deployment!

"""

        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 10  # Keep last 10 messages

    def chat(self, user_message: str, context: str = "") -> Dict[str, Any]:
        """
        Get AI response to a message.

        Args:
            user_message: User's input message
            context: Optional context from previous conversation

        Returns:
            Dictionary with AI response
        """
        if not self.client:
            return {
                "success": False,
                "reply": "AI service not available. Please check your Anthropic API key.",
                "model": "none",
                "error": "API key not configured"
            }

        try:
            # Build messages for Claude
            messages = []

            # Add system prompt
            system_content = self.system_prompt

            # Add context if provided
            if context:
                system_content += f"\n\nCONTEXT: {context}"

            # Add recent conversation history
            for msg in self.conversation_history[-self.max_history:]:
                messages.append(msg)

            # Add current message
            messages.append({"role": "user", "content": user_message})

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=AI_MAX_TOKENS,
                temperature=AI_TEMPERATURE,
                messages=messages,
                system=system_content
            )

            reply = response.content[0].text.strip()

            # Save to history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": reply})

            # Trim history if too long
            if len(self.conversation_history) > self.max_history * 2:
                self.conversation_history = self.conversation_history[-self.max_history * 2:]

            return {
                "success": True,
                "reply": reply,
                "model": self.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens if hasattr(response, 'usage') else 0,
                    "output_tokens": response.usage.output_tokens if hasattr(response, 'usage') else 0
                }
            }

        except Exception as e:
            error_msg = str(e)
            return {
                "success": False,
                "reply": f"AI error: {error_msg}",
                "model": self.model,
                "error": error_msg
            }

    def get_intent(self, command: str) -> Dict[str, Any]:
        """
        Classify command intent using Claude.

        Args:
            command: Command to classify

        Returns:
            Dictionary with intent classification
        """
        if not self.client:
            return {
                "intent": "unknown",
                "confidence": 0,
                "error": "AI not available"
            }

        try:
            # Ask Claude to classify intent as JSON
            prompt = f"""Classify this command into one of these categories:
- system_control (shutdown, restart, sleep, lock, battery, status)
- app_management (open, close, launch apps)
- volume_control (volume up, down, mute)
- brightness_control (brightness up, down)
- media_control (play music, youtube, spotify, next, pause)
- window_control (minimize, maximize, close, switch windows)
- screenshot (take screenshot, screen text)
- whatsapp (send message, open whatsapp)
- news (get news, headlines)
- search (google, search for)
- time_date (what time, what date)
- memory (remember, what do you remember)
- file_operation (open folder, create, delete, copy)
- pdf_operation (merge, split pdf)
- image_operation (convert, resize image)
- desktop_control (wallpaper, theme, recycle bin)
- keyboard_mouse (type, press key, click)
- conversation (general chat, questions)

Command: "{command}"

Respond with ONLY a JSON object: {{"intent": "category", "confidence": 0.9, "entities": {{}}}}"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}],
                system="You are an intent classifier. Respond with JSON only."
            )

            # Parse response
            intent_text = response.content[0].text.strip()

            # Try to extract JSON
            import json
            try:
                # Find JSON in response
                start = intent_text.find('{')
                end = intent_text.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = intent_text[start:end]
                    result = json.loads(json_str)
                    return {
                        "intent": result.get("intent", "unknown"),
                        "confidence": result.get("confidence", 0.5),
                        "entities": result.get("entities", {})
                    }
            except:
                pass

            # Fallback: return basic classification
            return {
                "intent": "conversation",
                "confidence": 0.5,
                "entities": {}
            }

        except Exception as e:
            return {
                "intent": "unknown",
                "confidence": 0,
                "error": str(e)
            }

    def summarize_for_voice(self, long_text: str, max_words: int = 50) -> str:
        """
        Summarize long text for voice output.
        Shortens text to be speakable length.

        Args:
            long_text: Long text to summarize
            max_words: Maximum words in summary

        Returns:
            Summarized text
        """
        if not long_text:
            return ""

        # Simple truncation with smart sentence breaking
        words = long_text.split()

        if len(words) <= max_words:
            return long_text

        # Truncate and find good breaking point
        truncated = ' '.join(words[:max_words])

        # Try to break at sentence end
        for punct in ['.', '!', '?', ';']:
            last_punct = truncated.rfind(punct)
            if last_punct > max_words // 2:
                return truncated[:last_punct + 1]

        # Just truncate with ellipsis
        return truncated + "..."

    def summarize_text(self, text: str, max_length: int = 200) -> Dict[str, Any]:
        """
        Summarize text using Claude.

        Args:
            text: Text to summarize
            max_length: Maximum characters in summary

        Returns:
            Dictionary with summary
        """
        if not self.client:
            return {
                "success": False,
                "summary": text[:max_length] + "..." if len(text) > max_length else text,
                "error": "AI not available"
            }

        try:
            prompt = f"Summarize this text in 1-2 sentences:\n\n{text}"

            response = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}],
                system="You are a summarization assistant. Be concise."
            )

            summary = response.content[0].text.strip()

            return {
                "success": True,
                "summary": summary,
                "original_length": len(text),
                "summary_length": len(summary)
            }

        except Exception as e:
            return {
                "success": False,
                "summary": text[:max_length] + "..." if len(text) > max_length else text,
                "error": str(e)
            }

    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answer a question directly.

        Args:
            question: Question to answer

        Returns:
            Dictionary with answer
        """
        return self.chat(question)

    def explain_command(self, command: str) -> Dict[str, Any]:
        """
        Explain how to do a PC task.

        Args:
            command: Task description

        Returns:
            Dictionary with explanation
        """
        if not self.client:
            return {
                "success": False,
                "explanation": "AI not available to explain.",
                "error": "AI not available"
            }

        try:
            prompt = f"Explain how to do this PC task step by step: {command}"

            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
                system="You are a PC helper. Explain steps clearly and concisely."
            )

            explanation = response.content[0].text.strip()

            return {
                "success": True,
                "explanation": explanation,
                "command": command
            }

        except Exception as e:
            return {
                "success": False,
                "explanation": "Could not generate explanation.",
                "error": str(e)
            }

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history."""
        return self.conversation_history.copy()

    def get_status(self) -> Dict[str, Any]:
        """Get AI brain status."""
        return {
            "status": "ready" if self.client else "not_configured",
            "api_key_set": bool(self.api_key) and self.api_key != "your_anthropic_api_key_here",
            "model": self.model,
            "conversation_length": len(self.conversation_history),
            "max_history": self.max_history,
            "capabilities": [
                "chat", "chat_with_memory", "get_intent",
                "summarize_for_voice", "summarize_text",
                "answer_question", "explain_command"
            ]
        }

    def generate_response(self, task_result: Dict[str, Any], user_command: str) -> str:
        """
        Generate natural language response from task result.

        Args:
            task_result: Result from command execution
            user_command: Original user command

        Returns:
            Natural language response string
        """
        if not task_result.get("success"):
            return f"Sorry, I couldn't {user_command}. {task_result.get('response', task_result.get('error', ''))}"

        action = task_result.get("action", "")
        response = task_result.get("response", "")

        # Generate natural response based on action
        natural_responses = {
            "shutdown": "Shutting down your computer now.",
            "restart": "Restarting your computer.",
            "sleep": "Putting computer to sleep.",
            "lock": "Locking your computer.",
            "open_app": f"Opening {task_result.get('app', 'the app')} for you.",
            "close_app": f"Closing {task_result.get('app', 'the app')}.",
            "volume_up": "Increasing volume.",
            "volume_down": "Decreasing volume.",
            "mute_toggle": "Audio " + ("muted" if "muted" in response.lower() else "unmuted") + ".",
            "brightness_up": "Increasing brightness.",
            "brightness_down": "Decreasing brightness.",
            "youtube_play": f"Playing on YouTube.",
            "spotify_play": f"Playing on Spotify.",
            "screenshot": "Screenshot taken.",
            "news": "Here are the headlines.",
            "search": f"Searching for that.",
            "time": f"The time is {response}.",
            "date": f"Today is {response}.",
        }

        return natural_responses.get(action, response)
