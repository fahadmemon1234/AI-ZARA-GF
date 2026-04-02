"""
ARIA - Advanced Real-time Intelligent Assistant
Memory Manager Module - Persistent storage for conversations and memories
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import MEMORY_FILE, CONVERSATIONS_FILE, DATA_DIR


class MemoryManager:
    """
    Memory management for ARIA.
    Handles persistent storage of conversations, facts, and user preferences.
    """

    def __init__(self):
        """Initialize memory manager and ensure data files exist."""
        self.memory_file = MEMORY_FILE
        self.conversations_file = CONVERSATIONS_FILE
        
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Initialize files if they don't exist
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Create data files if they don't exist."""
        if not os.path.exists(self.memory_file):
            self._save_json(self.memory_file, [])
        
        if not os.path.exists(self.conversations_file):
            self._save_json(self.conversations_file, [])

    def _save_json(self, filepath: str, data: Any):
        """Save data to JSON file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving {filepath}: {e}")

    def _load_json(self, filepath: str) -> Any:
        """Load data from JSON file."""
        try:
            if not os.path.exists(filepath):
                return []
            
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {filepath}: {e}")
            return []

    # ============== Memory Operations ==============

    def save_memory(self, key: str, value: str) -> Dict[str, Any]:
        """
        Save a memory entry.
        
        Args:
            key: Memory key (e.g., "user_name", "favorite_color")
            value: Memory value
            
        Returns:
            Status dictionary
        """
        try:
            memories = self._load_json(self.memory_file)
            
            # Check if key already exists
            for i, mem in enumerate(memories):
                if mem.get('key') == key:
                    # Update existing memory
                    memories[i]['value'] = value
                    memories[i]['updated_at'] = datetime.now().isoformat()
                    memories[i]['access_count'] = memories[i].get('access_count', 0) + 1
                    
                    self._save_json(self.memory_file, memories)
                    
                    return {
                        "success": True,
                        "message": "Memory updated",
                        "action": "updated",
                        "key": key
                    }
            
            # Add new memory
            new_memory = {
                "key": key,
                "value": value,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "access_count": 0,
                "type": "fact"
            }
            
            memories.append(new_memory)
            self._save_json(self.memory_file, memories)
            
            return {
                "success": True,
                "message": "Memory saved",
                "action": "created",
                "key": key
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def load_memory(self, key: str) -> Optional[str]:
        """
        Load a memory by key.
        
        Args:
            key: Memory key to lookup
            
        Returns:
            Memory value or None if not found
        """
        try:
            memories = self._load_json(self.memory_file)
            
            for mem in memories:
                if mem.get('key') == key:
                    # Increment access count
                    mem['access_count'] = mem.get('access_count', 0) + 1
                    self._save_json(self.memory_file, memories)
                    return mem.get('value')
            
            return None
            
        except Exception as e:
            print(f"Error loading memory: {e}")
            return None

    def get_memory(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get full memory entry by key.
        
        Args:
            key: Memory key
            
        Returns:
            Full memory dictionary or None
        """
        try:
            memories = self._load_json(self.memory_file)
            
            for mem in memories:
                if mem.get('key') == key:
                    return mem
            
            return None
            
        except Exception as e:
            return None

    def get_all_memory(self) -> List[Dict[str, Any]]:
        """
        Get all memory entries.
        
        Returns:
            List of all memories
        """
        return self._load_json(self.memory_file)

    def delete_memory(self, key: str) -> Dict[str, Any]:
        """
        Delete a memory by key.
        
        Args:
            key: Memory key to delete
            
        Returns:
            Status dictionary
        """
        try:
            memories = self._load_json(self.memory_file)
            memories = [m for m in memories if m.get('key') != key]
            self._save_json(self.memory_file, memories)
            
            return {
                "success": True,
                "message": "Memory deleted",
                "key": key
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def search_memory(self, query: str) -> List[Dict[str, Any]]:
        """
        Search memories by query.
        
        Args:
            query: Search query
            
        Returns:
            List of matching memories
        """
        try:
            memories = self._load_json(self.memory_file)
            query_lower = query.lower()
            
            results = []
            for mem in memories:
                key = mem.get('key', '').lower()
                value = mem.get('value', '').lower()
                
                if query_lower in key or query_lower in value:
                    results.append(mem)
            
            return results
            
        except Exception as e:
            return []

    def add_memory_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a custom memory entry.
        
        Args:
            entry: Memory entry dictionary with keys:
                   - key (required)
                   - value (required)
                   - type (optional, default: "fact")
                   - metadata (optional)
                   
        Returns:
            Status dictionary
        """
        try:
            if not entry.get('key') or not entry.get('value'):
                return {"success": False, "error": "Key and value are required"}
            
            memories = self._load_json(self.memory_file)
            
            # Build memory entry
            memory = {
                "key": entry['key'],
                "value": entry['value'],
                "type": entry.get('type', 'fact'),
                "metadata": entry.get('metadata', {}),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "access_count": 0
            }
            
            # Check for existing key
            for i, mem in enumerate(memories):
                if mem.get('key') == memory['key']:
                    memories[i] = memory
                    self._save_json(self.memory_file, memories)
                    return {
                        "success": True,
                        "message": "Memory updated",
                        "action": "updated"
                    }
            
            memories.append(memory)
            self._save_json(self.memory_file, memories)
            
            return {
                "success": True,
                "message": "Memory added",
                "action": "created"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def clear_all_memory(self) -> Dict[str, Any]:
        """
        Clear all memories.
        
        Returns:
            Status dictionary
        """
        try:
            self._save_json(self.memory_file, [])
            return {"success": True, "message": "All memories cleared"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ============== Conversation Operations ==============

    def add_conversation(self, user_msg: str, ai_reply: str) -> Dict[str, Any]:
        """
        Add a conversation turn.
        
        Args:
            user_msg: User's message
            ai_reply: AI's response
            
        Returns:
            Status dictionary
        """
        try:
            conversations = self._load_json(self.conversations_file)
            
            # Add new conversation
            conversation = {
                "user": user_msg,
                "assistant": ai_reply,
                "timestamp": datetime.now().isoformat()
            }
            
            conversations.append(conversation)
            
            # Keep only last 50 conversations
            if len(conversations) > 50:
                conversations = conversations[-50:]
            
            self._save_json(self.conversations_file, conversations)
            
            return {
                "success": True,
                "message": "Conversation saved",
                "total_conversations": len(conversations)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_recent_conversations(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent conversations.
        
        Args:
            n: Number of recent conversations to return
            
        Returns:
            List of conversation dictionaries
        """
        try:
            conversations = self._load_json(self.conversations_file)
            
            if not conversations:
                return []
            
            return conversations[-n:]
            
        except Exception as e:
            return []

    def get_all_conversations(self) -> List[Dict[str, Any]]:
        """
        Get all conversations.
        
        Returns:
            List of all conversations
        """
        return self._load_json(self.conversations_file)

    def clear_conversations(self) -> Dict[str, Any]:
        """
        Clear all conversations.
        
        Returns:
            Status dictionary
        """
        try:
            self._save_json(self.conversations_file, [])
            return {"success": True, "message": "Conversations cleared"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_conversation_stats(self) -> Dict[str, Any]:
        """
        Get conversation statistics.
        
        Returns:
            Statistics dictionary
        """
        try:
            conversations = self._load_json(self.conversations_file)
            
            if not conversations:
                return {
                    "total": 0,
                    "first_conversation": None,
                    "last_conversation": None
                }
            
            return {
                "total": len(conversations),
                "first_conversation": conversations[0].get('timestamp') if conversations else None,
                "last_conversation": conversations[-1].get('timestamp') if conversations else None
            }
            
        except Exception as e:
            return {"error": str(e)}

    # ============== User Preferences ==============

    def save_preference(self, key: str, value: Any) -> Dict[str, Any]:
        """
        Save user preference.
        
        Args:
            key: Preference key
            value: Preference value
            
        Returns:
            Status dictionary
        """
        return self.save_memory(f"pref_{key}", str(value))

    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Get user preference.
        
        Args:
            key: Preference key
            default: Default value if not found
            
        Returns:
            Preference value or default
        """
        value = self.load_memory(f"pref_{key}")
        return value if value is not None else default

    # ============== Context Management ==============

    def get_context_summary(self) -> str:
        """
        Get a summary of all memories for AI context.
        
        Returns:
            Formatted context string
        """
        memories = self.get_all_memory()
        
        if not memories:
            return "No stored memories."
        
        context_parts = []
        for mem in memories[:10]:  # Limit to 10 most relevant
            context_parts.append(f"- {mem.get('key', 'unknown')}: {mem.get('value', '')}")
        
        return "User memories:\n" + "\n".join(context_parts)

    def export_data(self, filepath: str = None) -> Dict[str, Any]:
        """
        Export all data to a file.
        
        Args:
            filepath: Export file path (default: data/export_timestamp.json)
            
        Returns:
            Status dictionary
        """
        try:
            if not filepath:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = os.path.join(DATA_DIR, f"export_{timestamp}.json")
            
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "memories": self.get_all_memory(),
                "conversations": self.get_all_conversations()
            }
            
            self._save_json(filepath, export_data)
            
            return {
                "success": True,
                "message": "Data exported",
                "path": filepath
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def import_data(self, filepath: str) -> Dict[str, Any]:
        """
        Import data from a file.
        
        Args:
            filepath: Import file path
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(filepath):
                return {"success": False, "error": "File not found"}
            
            import_data = self._load_json(filepath)
            
            # Import memories
            if 'memories' in import_data:
                existing = self.get_all_memory()
                existing_keys = {m.get('key') for m in existing}
                
                for mem in import_data['memories']:
                    if mem.get('key') not in existing_keys:
                        self.add_memory_entry(mem)
            
            # Import conversations
            if 'conversations' in import_data:
                existing = self.get_all_conversations()
                existing.extend(import_data['conversations'])
                
                # Keep last 50
                if len(existing) > 50:
                    existing = existing[-50:]
                
                self._save_json(self.conversations_file, existing)
            
            return {
                "success": True,
                "message": "Data imported"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get memory manager status."""
        return {
            "memory_file": self.memory_file,
            "conversations_file": self.conversations_file,
            "memory_count": len(self.get_all_memory()),
            "conversation_count": len(self.get_all_conversations()),
            "data_dir_exists": os.path.exists(DATA_DIR)
        }
