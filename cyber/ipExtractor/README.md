# 🔍 Cyber IP Extractor

A comprehensive cyber reconnaissance tool that combines port scanning with system information gathering and geolocation intelligence.

## 🎯 Features

### 📡 System Info & Geolocation Extraction
- Local system fingerprinting (OS, MAC, UUID, etc.)
- Public IP detection and geolocation
- Target IP geolocation and ISP information
- Network intelligence gathering

### 🔍 Advanced Port Scanning
- Quick scan with common ports
- Custom port list scanning
- Port range scanning
- Network/subnet range support
- Multi-threaded scanning for performance
- Service detection and banner grabbing

### 🛡️ Intelligence & Reporting
- Basic vulnerability assessment
- Service fingerprinting
- JSON, CSV, and HTML report generation
- Comprehensive reconnaissance summaries

## 🚀 Installation

1. Clone or navigate to the project directory
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Quick Scan
```bash
python main.py 192.168.1.1 --quick
```

### Network Range Scan
```bash
python main.py 192.168.1.0/24 --quick
```

### Custom Port Scan
```bash
python main.py 192.168.1.1 --ports 80 443 8080 8443
```

### Port Range Scan
```bash
python main.py 192.168.1.1 --range 1 1000
```

### Export Results
```bash
# JSON export
python main.py 192.168.1.1 --quick --export json

# CSV export
python main.py 192.168.1.1 --quick --export csv

# HTML report
python main.py 192.168.1.1 --quick --export html

# Custom filename
python main.py 192.168.1.1 --quick --export json --output my_scan_report.json
```

### Advanced Options
```bash
# Custom timeout and threads
python main.py 192.168.1.0/24 --quick --timeout 5.0 --threads 50
```

## 🎯 Workflow

The tool follows a 3-step reconnaissance process:

1. **Port Scanning** - Discovers open ports and services
2. **Intelligence Gathering** - Enriches IPs with geolocation and system info
3. **Local Fingerprinting** - Collects local system information

## 📊 Report Formats

### JSON Report
Complete structured data including:
- Scan metadata
- Local system fingerprint
- Target intelligence with geolocation
- Open ports and services
- Potential vulnerabilities

### CSV Report
Tabular format focusing on:
- IP addresses
- Open ports
- Services
- Banner information

### HTML Report
Visual report with:
- Formatted tables
- Color-coded status
- Service banners
- Export-friendly layout

## ⚠️ Legal & Ethical Usage

**IMPORTANT**: This tool is designed for:
- Educational purposes and cybersecurity training
- Authorized penetration testing
- Network security assessments
- Research with proper permissions

**Always ensure you have:**
- Explicit permission to scan target networks
- Authorization from network owners
- Compliance with local laws and regulations

## 🔧 Technical Details

### Dependencies
- `requests` - HTTP requests for geolocation APIs
- `getmac` - MAC address extraction
- `socket` - Network connections
- `ipaddress` - IP address manipulation
- `threading` - Concurrent scanning

### API Services Used
- `ipify.org` - Public IP detection
- `ip-api.com` - Geolocation and ISP data

### Common Ports Scanned
21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995,
1723, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9200, 27017

## 🛠️ Examples

### Educational Reconnaissance
```bash
# Scan your own public IP
python main.py $(curl -s ifconfig.me) --quick --export json

# Local network discovery (with permission)
python main.py 192.168.1.0/24 --quick --export html
```

### Security Assessment
```bash
# Web server assessment
python main.py target-server.com --ports 80 443 8080 8443 --export json

# Database server check
python main.py db-server.local --ports 3306 5432 6379 27017 --export csv
```

## 📚 Learning Objectives

Using this tool helps you understand:
- Network reconnaissance techniques
- Port scanning methodologies
- Geolocation intelligence gathering
- System fingerprinting
- Vulnerability assessment basics
- Report generation and analysis

---

**⚠️ Remember**: Use responsibly and only on networks you're authorized to test!
