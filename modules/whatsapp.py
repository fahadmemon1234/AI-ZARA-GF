"""
ZARA - Advanced Real-time Intelligent Assistant
WhatsApp Automation Module
"""

import pywhatkit
import webbrowser
import time
import os
from typing import Dict, Any, Optional
import pyautogui
import pyperclip


class WhatsAppAutomation:
    """
    WhatsApp Web automation using pywhatkit and pyautogui.
    Handles messaging, file sharing, and calls.
    """

    def __init__(self):
        """Initialize WhatsApp automation."""
        self.base_url = "https://web.whatsapp.com"

    def send_message(self, contact: str, message: str, hour: int = None, minute: int = None, wait_time: int = 15) -> Dict[str, Any]:
        """
        Send WhatsApp message to contact.
        
        Args:
            contact: Phone number with country code (e.g., '+923001234567') or contact name
            message: Message to send
            hour: Hour to send (24-hour format). If None, sends instantly
            minute: Minute to send. If None, sends instantly
            wait_time: Wait time in seconds after opening WhatsApp Web
            
        Returns:
            Status dictionary
        """
        try:
            if not contact or not message:
                return {
                    "success": False,
                    "message": "Contact and message are required",
                    "action": "send_message"
                }
            
            # If hour/minute not provided, send instantly
            if hour is None or minute is None:
                return self.send_message_instant(contact, message, wait_time)
            
            # Schedule message for specific time
            pywhatkit.sendwhatmsg(
                phone_no=contact,
                message=message,
                time_hour=hour,
                time_min=minute,
                wait_time=wait_time,
                tab_close=True,
                close_time=3
            )
            
            return {
                "success": True,
                "message": f"Message scheduled for {hour:02d}:{minute:02d}",
                "contact": contact,
                "scheduled_time": f"{hour:02d}:{minute:02d}",
                "action": "send_message"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_message_instant(self, phone_number: str, message: str, wait_time: int = 15, tab_close: bool = True) -> Dict[str, Any]:
        """
        Send WhatsApp message instantly.
        
        Args:
            phone_number: Phone number with country code (e.g., '+923001234567')
            message: Message to send
            wait_time: Wait time in seconds
            tab_close: Close tab after sending
            
        Returns:
            Status dictionary
        """
        try:
            if not phone_number or not message:
                return {
                    "success": False,
                    "message": "Phone number and message are required",
                    "action": "send_message_instant"
                }
            
            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone_number,
                message=message,
                wait_time=wait_time,
                tab_close=tab_close
            )
            
            return {
                "success": True,
                "message": "Message sent successfully",
                "contact": phone_number,
                "message_preview": message[:50] + "..." if len(message) > 50 else message,
                "action": "send_message_instant"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_file(self, phone_number: str, file_path: str, caption: str = "") -> Dict[str, Any]:
        """
        Send file via WhatsApp Web.
        Opens WhatsApp Web and guides through file attachment flow.
        
        Args:
            phone_number: Phone number with country code
            file_path: Path to file to send
            caption: Optional caption for the file
            
        Returns:
            Status dictionary
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "message": f"File not found: {file_path}",
                    "action": "send_file"
                }
            
            # Open WhatsApp Web with the contact
            url = f"https://web.whatsapp.com/send?phone={phone_number}"
            webbrowser.open(url)
            
            # Wait for WhatsApp to load
            time.sleep(8)
            
            # Click attachment icon (paperclip)
            # Note: This requires precise coordinates which vary by screen resolution
            # This is a general guide - actual coordinates may need adjustment
            pyautogui.click(x=1050, y=950)  # Approximate attachment button position
            time.sleep(1)
            
            # Type file path in the file dialog
            pyperclip.copy(file_path)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            
            # Press Enter to confirm
            pyautogui.press('enter')
            
            # Add caption if provided
            if caption:
                pyperclip.copy(caption)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
            
            # Send
            pyautogui.press('enter')
            
            return {
                "success": True,
                "message": f"File sent: {os.path.basename(file_path)}",
                "contact": phone_number,
                "file": file_path,
                "caption": caption,
                "action": "send_file"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def make_call(self, phone_number: str, video: bool = False) -> Dict[str, Any]:
        """
        Open WhatsApp Web call interface.
        
        Args:
            phone_number: Phone number with country code
            video: True for video call, False for voice call
            
        Returns:
            Status dictionary
        """
        try:
            if not phone_number:
                return {
                    "success": False,
                    "message": "Phone number is required",
                    "action": "make_call"
                }
            
            # Open WhatsApp Web with the contact
            url = f"https://web.whatsapp.com/send?phone={phone_number}"
            webbrowser.open(url)
            
            call_type = "video" if video else "voice"
            
            return {
                "success": True,
                "message": f"WhatsApp Web opened for {call_type} call",
                "contact": phone_number,
                "call_type": call_type,
                "url": url,
                "note": "Click the call button manually to initiate the call",
                "action": "make_call"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_chat(self, contact: str) -> Dict[str, Any]:
        """
        Open WhatsApp chat with contact.
        
        Args:
            contact: Phone number or contact name
            
        Returns:
            Status dictionary
        """
        try:
            if not contact:
                return {
                    "success": False,
                    "message": "Contact is required",
                    "action": "open_chat"
                }
            
            # Check if contact is a phone number
            if contact.startswith('+') or contact.isdigit():
                url = f"https://web.whatsapp.com/send?phone={contact}"
            else:
                # For contact name, just open WhatsApp Web
                url = self.base_url
            
            webbrowser.open(url)
            
            return {
                "success": True,
                "message": f"Opening WhatsApp chat with {contact}",
                "contact": contact,
                "url": url,
                "action": "open_chat"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_group_message(self, group_id: str, message: str) -> Dict[str, Any]:
        """
        Send message to WhatsApp group.
        
        Args:
            group_id: Group invite link or group ID
            message: Message to send
            
        Returns:
            Status dictionary
        """
        try:
            if not group_id or not message:
                return {
                    "success": False,
                    "message": "Group ID and message are required",
                    "action": "send_group_message"
                }
            
            # If group_id is an invite link, open it
            if 'chat.whatsapp.com' in group_id:
                webbrowser.open(group_id)
                time.sleep(5)
                
                # Type and send message
                pyperclip.copy(message)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
                pyautogui.press('enter')
                
                return {
                    "success": True,
                    "message": "Message sent to group",
                    "group": group_id[:50] + "..." if len(group_id) > 50 else group_id,
                    "action": "send_group_message"
                }
            else:
                return {
                    "success": False,
                    "message": "Please provide a valid WhatsApp group invite link",
                    "action": "send_group_message"
                }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_qr_code(self) -> Dict[str, Any]:
        """
        Open WhatsApp Web for QR code scanning.
        
        Returns:
            Status dictionary
        """
        try:
            webbrowser.open(self.base_url)
            
            return {
                "success": True,
                "message": "WhatsApp Web opened. Please scan QR code to login.",
                "url": self.base_url,
                "action": "get_qr_code"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_bulk_messages(self, contacts: list, message: str, delay: int = 30) -> Dict[str, Any]:
        """
        Send message to multiple contacts.
        
        Args:
            contacts: List of phone numbers
            message: Message to send
            delay: Delay between messages in seconds
            
        Returns:
            Status dictionary
        """
        try:
            if not contacts or not message:
                return {
                    "success": False,
                    "message": "Contacts and message are required",
                    "action": "send_bulk_messages"
                }
            
            results = []
            
            for i, contact in enumerate(contacts):
                try:
                    result = self.send_message_instant(contact, message, wait_time=10)
                    results.append({
                        "contact": contact,
                        "success": result.get("success", False),
                        "message": result.get("message", "")
                    })
                    
                    # Wait before next message
                    if i < len(contacts) - 1:
                        time.sleep(delay)
                        
                except Exception as e:
                    results.append({
                        "contact": contact,
                        "success": False,
                        "message": str(e)
                    })
            
            success_count = sum(1 for r in results if r.get("success"))
            
            return {
                "success": True,
                "message": f"Sent {success_count}/{len(contacts)} messages",
                "total": len(contacts),
                "successful": success_count,
                "failed": len(contacts) - success_count,
                "results": results,
                "action": "send_bulk_messages"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_good_morning(self, contacts: list) -> Dict[str, Any]:
        """
        Send good morning message to contacts.
        
        Args:
            contacts: List of phone numbers
            
        Returns:
            Status dictionary
        """
        messages = [
            "Good Morning! ☀️ Have a wonderful day ahead!",
            "Rise and shine! Good Morning! 🌅",
            "Good Morning! Wishing you a day full of happiness! 😊",
            "Hello! Good Morning! Hope your day starts with a smile! 😄"
        ]
        
        import random
        message = random.choice(messages)
        
        return self.send_bulk_messages(contacts, message, delay=30)

    def send_good_night(self, contacts: list) -> Dict[str, Any]:
        """
        Send good night message to contacts.
        
        Args:
            contacts: List of phone numbers
            
        Returns:
            Status dictionary
        """
        messages = [
            "Good Night! 🌙 Sweet dreams!",
            "Sleep well! Good Night! 😴",
            "Good Night! Rest well for a better tomorrow! 🌟",
            "Night night! Have peaceful sleep! 💤"
        ]
        
        import random
        message = random.choice(messages)
        
        return self.send_bulk_messages(contacts, message, delay=30)

    def is_whatsapp_web_open(self) -> bool:
        """
        Check if WhatsApp Web is open.
        
        Returns:
            True if WhatsApp Web is detected
        """
        try:
            import pygetwindow as gw
            windows = gw.getAllWindows()
            
            for window in windows:
                if 'whatsapp' in window.title.lower():
                    return True
            
            return False
            
        except:
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get WhatsApp automation status."""
        return {
            "available": True,
            "base_url": self.base_url,
            "capabilities": [
                "send_message", "send_message_instant", "send_file",
                "make_call", "open_chat", "send_group_message",
                "send_bulk_messages", "get_qr_code"
            ],
            "note": "WhatsApp Web must be logged in for most features"
        }
