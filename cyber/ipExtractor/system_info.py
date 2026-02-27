#!/usr/bin/env python3
import platform
import uuid
import getmac
import requests
import json
from typing import Dict, Optional

class SystemInfoExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_local_system_info(self) -> Dict:
        """Extract local system information"""
        try:
            return {
                'os_version': platform.system() + ' ' + platform.release(),
                'platform': platform.platform(),
                'processor': platform.processor(),
                'architecture': platform.architecture()[0],
                'hostname': platform.node(),
                'mac_address': getmac.get_mac_address(),
                'uuid': str(uuid.getnode())
            }
        except Exception as e:
            return {'error': f'Failed to get local system info: {str(e)}'}
    
    def get_public_ip_info(self) -> Dict:
        """Get public IP and geolocation information"""
        try:
            # Get public IP
            ip_response = self.session.get('https://api.ipify.org?format=json', timeout=5)
            ip_data = ip_response.json()
            public_ip = ip_data.get('ip')
            
            # Get geolocation data
            geo_response = self.session.get(
                f'http://ip-api.com/json/{public_ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query',
                timeout=5
            )
            geo_data = geo_response.json()
            
            if geo_data.get('status') == 'fail':
                return {'error': f'Geolocation failed: {geo_data.get("message", "Unknown error")}'}
            
            return {
                'public_ip': public_ip,
                'country': geo_data.get('country'),
                'country_code': geo_data.get('countryCode'),
                'region': geo_data.get('regionName'),
                'city': geo_data.get('city'),
                'zip_code': geo_data.get('zip'),
                'latitude': geo_data.get('lat'),
                'longitude': geo_data.get('lon'),
                'timezone': geo_data.get('timezone'),
                'isp': geo_data.get('isp'),
                'organization': geo_data.get('org'),
                'as_number': geo_data.get('as'),
                'query_ip': geo_data.get('query')
            }
        except Exception as e:
            return {'error': f'Failed to get public IP info: {str(e)}'}
    
    def get_target_ip_info(self, target_ip: str) -> Dict:
        """Get geolocation info for a specific target IP"""
        try:
            geo_response = self.session.get(
                f'http://ip-api.com/json/{target_ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query',
                timeout=5
            )
            geo_data = geo_response.json()
            
            if geo_data.get('status') == 'fail':
                return {'error': f'Geolocation failed for {target_ip}: {geo_data.get("message", "Unknown error")}'}
            
            return {
                'target_ip': target_ip,
                'country': geo_data.get('country'),
                'country_code': geo_data.get('countryCode'),
                'region': geo_data.get('regionName'),
                'city': geo_data.get('city'),
                'zip_code': geo_data.get('zip'),
                'latitude': geo_data.get('lat'),
                'longitude': geo_data.get('lon'),
                'timezone': geo_data.get('timezone'),
                'isp': geo_data.get('isp'),
                'organization': geo_data.get('org'),
                'as_number': geo_data.get('as'),
                'query_ip': geo_data.get('query')
            }
        except Exception as e:
            return {'error': f'Failed to get info for {target_ip}: {str(e)}'}
    
    def get_complete_system_fingerprint(self, target_ip: Optional[str] = None) -> Dict:
        """Get complete system fingerprint including local info and target IP info"""
        fingerprint = {
            'local_system': self.get_local_system_info(),
            'public_info': self.get_public_ip_info()
        }
        
        if target_ip:
            fingerprint['target_info'] = self.get_target_ip_info(target_ip)
        
        return fingerprint
