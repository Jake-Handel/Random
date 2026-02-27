#!/usr/bin/env python3
import argparse
import json
import sys
import time
from typing import Dict, List, Optional
from pathlib import Path

from system_info import SystemInfoExtractor
from port_scanner import PortScanner, ScanResult

class CyberIPExtractor:
    def __init__(self):
        self.info_extractor = SystemInfoExtractor()
        self.port_scanner = PortScanner()
    
    def scan_and_enrich(self, target: str, scan_type: str = 'quick', 
                       ports: Optional[List[int]] = None, 
                       port_range: Optional[tuple] = None) -> Dict:
        """
        Main workflow: Scan target IPs and enrich with system info/geolocation
        """
        print(f"[*] Starting cyber reconnaissance on: {target}")
        print("=" * 60)
        
        # Step 1: Port scanning
        print("[1/3] Scanning for open ports...")
        scan_results = self._perform_port_scan(target, scan_type, ports, port_range)
        
        if not scan_results:
            print("[!] No open ports found or scan failed")
            return {}
        
        print(f"[+] Found {sum(len(results) for results in scan_results.values())} open ports")
        
        # Step 2: System info and geolocation enrichment
        print("[2/3] Gathering system and geolocation intelligence...")
        enriched_results = self._enrich_scan_results(scan_results)
        
        # Step 3: Local system fingerprinting
        print("[3/3] Collecting local system fingerprint...")
        local_fingerprint = self.info_extractor.get_local_system_info()
        
        # Compile final report
        final_report = {
            'scan_metadata': {
                'target': target,
                'scan_type': scan_type,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_hosts_scanned': len(scan_results),
                'total_open_ports': sum(len(results) for results in scan_results.values())
            },
            'local_system_fingerprint': local_fingerprint,
            'target_intelligence': enriched_results
        }
        
        print("[+] Reconnaissance complete!")
        return final_report
    
    def _perform_port_scan(self, target: str, scan_type: str, 
                          ports: Optional[List[int]], 
                          port_range: Optional[tuple]) -> Dict[str, List[ScanResult]]:
        """Perform port scanning based on scan type"""
        try:
            if scan_type == 'quick':
                return self.port_scanner.quick_scan(target)
            elif scan_type == 'custom' and ports:
                return self.port_scanner.custom_scan(target, ports)
            elif scan_type == 'range' and port_range:
                start_port, end_port = port_range
                return self.port_scanner.scan_port_range(target, start_port, end_port)
            else:
                raise ValueError("Invalid scan type or missing parameters")
        except Exception as e:
            print(f"[!] Port scan failed: {str(e)}")
            return {}
    
    def _enrich_scan_results(self, scan_results: Dict[str, List[ScanResult]]) -> List[Dict]:
        """Enrich scan results with geolocation and system info"""
        enriched_targets = []
        
        for ip, port_results in scan_results.items():
            print(f"    [*] Enriching IP: {ip}")
            
            # Get geolocation info for this IP
            geo_info = self.info_extractor.get_target_ip_info(ip)
            
            # Compile target intelligence
            target_intel = {
                'ip': ip,
                'geolocation': geo_info,
                'open_ports': [],
                'services_detected': [],
                'potential_vulnerabilities': []
            }
            
            # Process each open port
            for port_result in port_results:
                port_info = {
                    'port': port_result.port,
                    'status': port_result.status,
                    'service': port_result.service,
                    'banner': port_result.banner
                }
                target_intel['open_ports'].append(port_info)
                
                if port_result.service != 'Unknown':
                    target_intel['services_detected'].append(port_result.service)
                
                # Basic vulnerability assessment
                vulns = self._assess_vulnerabilities(port_result)
                target_intel['potential_vulnerabilities'].extend(vulns)
            
            enriched_targets.append(target_intel)
        
        return enriched_targets
    
    def _assess_vulnerabilities(self, port_result: ScanResult) -> List[str]:
        """Basic vulnerability assessment based on open ports"""
        vulnerabilities = []
        
        # Common vulnerable services
        vulnerable_services = {
            21: ['FTP - Anonymous login possible', 'FTP - Plain text authentication'],
            23: ['Telnet - Unencrypted communication', 'Telnet - Weak authentication'],
            25: ['SMTP - Open relay possible', 'SMTP - Information disclosure'],
            53: ['DNS - Zone transfer possible', 'DNS - Cache poisoning'],
            80: ['HTTP - Potential web vulnerabilities', 'HTTP - Information disclosure'],
            110: ['POP3 - Plain text authentication'],
            143: ['IMAP - Plain text authentication'],
            3389: ['RDP - Brute force attacks', 'RDP - Man-in-the-middle possible'],
            5432: ['PostgreSQL - Default credentials', 'PostgreSQL - Data exposure'],
            3306: ['MySQL - Default credentials', 'MySQL - Data exposure'],
            6379: ['Redis - No authentication', 'Redis - Remote code execution'],
            27017: ['MongoDB - No authentication', 'MongoDB - Data exposure']
        }
        
        if port_result.port in vulnerable_services:
            vulnerabilities.extend(vulnerable_services[port_result.port])
        
        # Check for banners that might reveal version info
        if port_result.banner:
            if any(version in port_result.banner.lower() for version in ['version', 'v1.0', 'v2.0', 'v3.0']):
                vulnerabilities.append('Service version disclosure in banner')
        
        return vulnerabilities
    
    def export_report(self, report: Dict, format_type: str, filename: str):
        """Export report in various formats"""
        try:
            if format_type == 'json':
                with open(filename, 'w') as f:
                    json.dump(report, f, indent=2)
                print(f"[+] Report exported to {filename}")
            
            elif format_type == 'csv':
                # Extract port scan results for CSV export
                scan_results = {}
                for target in report.get('target_intelligence', []):
                    ip = target['ip']
                    scan_results[ip] = []
                    for port_info in target['open_ports']:
                        scan_results[ip].append(ScanResult(
                            ip=ip,
                            port=port_info['port'],
                            status=port_info['status'],
                            service=port_info['service'],
                            banner=port_info['banner']
                        ))
                
                self.port_scanner.export_to_csv(scan_results, filename)
                print(f"[+] Port scan results exported to {filename}")
            
            elif format_type == 'html':
                # Extract port scan results for HTML export
                scan_results = {}
                for target in report.get('target_intelligence', []):
                    ip = target['ip']
                    scan_results[ip] = []
                    for port_info in target['open_ports']:
                        scan_results[ip].append(ScanResult(
                            ip=ip,
                            port=port_info['port'],
                            status=port_info['status'],
                            service=port_info['service'],
                            banner=port_info['banner']
                        ))
                
                self.port_scanner.export_to_html(scan_results, filename)
                print(f"[+] HTML report exported to {filename}")
            
            else:
                raise ValueError(f"Unsupported export format: {format_type}")
                
        except Exception as e:
            print(f"[!] Export failed: {str(e)}")
    
    def print_summary(self, report: Dict):
        """Print a summary of the reconnaissance results"""
        print("\n" + "=" * 60)
        print("RECONNAISSANCE SUMMARY")
        print("=" * 60)
        
        metadata = report.get('scan_metadata', {})
        print(f"Target: {metadata.get('target', 'N/A')}")
        print(f"Scan Type: {metadata.get('scan_type', 'N/A')}")
        print(f"Timestamp: {metadata.get('timestamp', 'N/A')}")
        print(f"Hosts with Open Ports: {metadata.get('total_hosts_scanned', 0)}")
        print(f"Total Open Ports: {metadata.get('total_open_ports', 0)}")
        
        print("\nTARGET INTELLIGENCE:")
        print("-" * 40)
        
        for target in report.get('target_intelligence', []):
            ip = target['ip']
            geo = target.get('geolocation', {})
            
            print(f"\n🎯 Target: {ip}")
            if 'error' not in geo:
                print(f"   📍 Location: {geo.get('city', 'N/A')}, {geo.get('region', 'N/A')}, {geo.get('country', 'N/A')}")
                print(f"   🌐 ISP: {geo.get('isp', 'N/A')}")
                print(f"   🏢 Organization: {geo.get('organization', 'N/A')}")
            else:
                print(f"   ❌ Geolocation: {geo.get('error', 'Failed')}")
            
            print(f"   🔓 Open Ports: {len(target['open_ports'])}")
            for port_info in target['open_ports'][:5]:  # Show first 5 ports
                print(f"      - Port {port_info['port']}/{port_info['service'].lower()}: {port_info['status']}")
            
            if len(target['open_ports']) > 5:
                print(f"      ... and {len(target['open_ports']) - 5} more")
            
            if target['potential_vulnerabilities']:
                print(f"   ⚠️  Potential Issues: {len(target['potential_vulnerabilities'])}")
                for vuln in target['potential_vulnerabilities'][:3]:  # Show first 3
                    print(f"      - {vuln}")

def main():
    parser = argparse.ArgumentParser(
        description='Cyber IP Extractor - Combined Port Scanner and System Information Gatherer'
    )
    
    # Target specification
    parser.add_argument('target', help='Target IP address or network range (e.g., 192.168.1.1 or 192.168.1.0/24)')
    
    # Scan type options
    scan_group = parser.add_mutually_exclusive_group(required=True)
    scan_group.add_argument('--quick', action='store_true', help='Quick scan with common ports')
    scan_group.add_argument('--ports', nargs='+', type=int, help='Custom port list (e.g., --ports 80 443 8080)')
    scan_group.add_argument('--range', nargs=2, type=int, metavar=('START', 'END'), help='Port range (e.g., --range 1 1000)')
    
    # Export options
    parser.add_argument('--export', choices=['json', 'csv', 'html'], help='Export format')
    parser.add_argument('--output', help='Output filename (default: auto-generated)')
    
    # Other options
    parser.add_argument('--timeout', type=float, default=2.0, help='Connection timeout in seconds')
    parser.add_argument('--threads', type=int, default=100, help='Maximum threads for scanning')
    
    args = parser.parse_args()
    
    # Initialize the tool
    extractor = CyberIPExtractor()
    extractor.port_scanner.timeout = args.timeout
    extractor.port_scanner.max_threads = args.threads
    
    # Determine scan type
    scan_type = 'quick'
    ports = None
    port_range = None
    
    if args.ports:
        scan_type = 'custom'
        ports = args.ports
    elif args.range:
        scan_type = 'range'
        port_range = tuple(args.range)
    
    # Perform reconnaissance
    try:
        report = extractor.scan_and_enrich(args.target, scan_type, ports, port_range)
        
        if not report:
            print("[!] No results to report")
            sys.exit(1)
        
        # Print summary
        extractor.print_summary(report)
        
        # Export if requested
        if args.export:
            if args.output:
                filename = args.output
            else:
                timestamp = time.strftime('%Y%m%d_%H%M%S')
                extension = args.export
                filename = f"cyber_recon_{args.target.replace('/', '_')}_{timestamp}.{extension}"
            
            extractor.export_report(report, args.export, filename)
        
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()