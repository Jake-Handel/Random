#!/usr/bin/env python3
import socket
import ipaddress
import threading
import concurrent.futures
from typing import List, Dict, Tuple, Optional
import time
from dataclasses import dataclass

@dataclass
class ScanResult:
    ip: str
    port: int
    status: str
    service: Optional[str] = None
    banner: Optional[str] = None

class PortScanner:
    def __init__(self, timeout: float = 2.0, max_threads: int = 100):
        self.timeout = timeout
        self.max_threads = max_threads
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995,
            1723, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9200, 27017
        ]
        self.services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 111: 'RPC', 135: 'RPC', 139: 'NetBIOS',
            143: 'IMAP', 443: 'HTTPS', 993: 'IMAPS', 995: 'POP3S',
            1723: 'PPTP', 3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
            5900: 'VNC', 6379: 'Redis', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt',
            9200: 'Elasticsearch', 27017: 'MongoDB'
        }
    
    def scan_port(self, ip: str, port: int) -> Optional[ScanResult]:
        """Scan a single port on a target IP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            
            if result == 0:
                service = self.services.get(port, 'Unknown')
                banner = None
                
                # Try to grab banner for common services
                if port in [21, 22, 23, 25, 80, 110, 143, 443]:
                    try:
                        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        if len(banner) > 100:
                            banner = banner[:100] + '...'
                    except:
                        pass
                
                sock.close()
                return ScanResult(ip, port, 'open', service, banner)
            
            sock.close()
            return None
            
        except Exception:
            return None
    
    def scan_host(self, ip: str, ports: List[int]) -> List[ScanResult]:
        """Scan all specified ports on a single host"""
        open_ports = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {executor.submit(self.scan_port, ip, port): port for port in ports}
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
        
        return sorted(open_ports, key=lambda x: x.port)
    
    def scan_network(self, network: str, ports: List[int]) -> Dict[str, List[ScanResult]]:
        """Scan all hosts in a network range"""
        try:
            network_obj = ipaddress.ip_network(network, strict=False)
        except ValueError as e:
            raise ValueError(f'Invalid network format: {e}')
        
        results = {}
        total_hosts = network_obj.num_addresses
        
        if total_hosts > 254:
            print(f'Warning: Large network ({total_hosts} hosts). This may take a while...')
        
        def scan_single_host(ip_str):
            host_results = self.scan_host(ip_str, ports)
            if host_results:
                return ip_str, host_results
            return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(self.max_threads, 50)) as executor:
            futures = [executor.submit(scan_single_host, str(ip)) for ip in network_obj.hosts()]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    ip, host_results = result
                    results[ip] = host_results
                    print(f'Found open ports on {ip}: {[p.port for p in host_results]}')
        
        return results
    
    def quick_scan(self, target: str) -> Dict[str, List[ScanResult]]:
        """Quick scan using common ports"""
        if '/' in target:
            return self.scan_network(target, self.common_ports)
        else:
            results = self.scan_host(target, self.common_ports)
            return {target: results} if results else {}
    
    def custom_scan(self, target: str, ports: List[int]) -> Dict[str, List[ScanResult]]:
        """Custom scan with specified port range"""
        if '/' in target:
            return self.scan_network(target, ports)
        else:
            results = self.scan_host(target, ports)
            return {target: results} if results else {}
    
    def scan_port_range(self, target: str, start_port: int, end_port: int) -> Dict[str, List[ScanResult]]:
        """Scan a range of ports"""
        ports = list(range(start_port, end_port + 1))
        return self.custom_scan(target, ports)
    
    def export_to_csv(self, results: Dict[str, List[ScanResult]], filename: str):
        """Export scan results to CSV"""
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['ip', 'port', 'status', 'service', 'banner']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for ip, scan_results in results.items():
                for result in scan_results:
                    writer.writerow({
                        'ip': result.ip,
                        'port': result.port,
                        'status': result.status,
                        'service': result.service,
                        'banner': result.banner
                    })
    
    def export_to_html(self, results: Dict[str, List[ScanResult]], filename: str):
        """Export scan results to HTML report"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Port Scan Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .host {{ margin-bottom: 30px; }}
        .host-header {{ background-color: #f0f0f0; padding: 10px; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .open {{ color: green; font-weight: bold; }}
        .banner {{ font-family: monospace; font-size: 12px; max-width: 300px; word-break: break-all; }}
    </style>
</head>
<body>
    <h1>Port Scan Report</h1>
    <p>Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
"""
        
        for ip, scan_results in results.items():
            html_content += f"""
    <div class="host">
        <div class="host-header">Host: {ip}</div>
        <table>
            <tr><th>Port</th><th>Status</th><th>Service</th><th>Banner</th></tr>
"""
            for result in scan_results:
                banner_html = f'<div class="banner">{result.banner or "N/A"}</div>'
                html_content += f"""
            <tr>
                <td>{result.port}</td>
                <td class="open">{result.status}</td>
                <td>{result.service}</td>
                <td>{banner_html}</td>
            </tr>
"""
            html_content += """
        </table>
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        with open(filename, 'w') as f:
            f.write(html_content)
