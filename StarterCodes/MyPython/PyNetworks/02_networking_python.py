#!/usr/bin/env python3
"""
Python Networking Libraries and Concepts - Cisco Interview Prep
Topics: Socket programming, HTTP requests, JSON/XML parsing, regular expressions
"""

import socket
import json
import re
import ipaddress
from urllib.parse import urlparse
import threading
import time

# 1. SOCKET PROGRAMMING (Low-level networking)
class NetworkScanner:
    """Simple network scanner using sockets"""
    
    def __init__(self, target_network="192.168.1.0/24"):
        self.target_network = target_network
        self.open_ports = {}
    
    def scan_port(self, host, port, timeout=1):
        """Scan a single port on a host"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0  # 0 means connection successful
        except socket.error:
            return False
    
    def scan_common_ports(self, host):
        """Scan common network device ports"""
        common_ports = {
            22: 'SSH',
            23: 'Telnet', 
            80: 'HTTP',
            443: 'HTTPS',
            161: 'SNMP',
            514: 'Syslog'
        }
        
        open_ports = {}
        for port, service in common_ports.items():
            if self.scan_port(host, port):
                open_ports[port] = service
        
        return open_ports
    
    def ping_host(self, host):
        """Simple ping using socket (ICMP requires root, so we use TCP)"""
        return self.scan_port(host, 80, timeout=0.5) or self.scan_port(host, 443, timeout=0.5)

# 2. IP ADDRESS MANIPULATION
class IPAddressUtils:
    """Utilities for IP address operations"""
    
    @staticmethod
    def validate_ip(ip_string):
        """Validate IP address format"""
        try:
            ipaddress.ip_address(ip_string)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def get_network_info(cidr):
        """Get network information from CIDR notation"""
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            return {
                'network_address': str(network.network_address),
                'broadcast_address': str(network.broadcast_address),
                'netmask': str(network.netmask),
                'num_hosts': network.num_addresses - 2,  # Exclude network and broadcast
                'hosts': [str(ip) for ip in list(network.hosts())[:5]]  # First 5 hosts
            }
        except ValueError as e:
            return {'error': str(e)}
    
    @staticmethod
    def subnet_calculator(ip, old_prefix, new_prefix):
        """Calculate subnets"""
        try:
            original_network = ipaddress.ip_network(f"{ip}/{old_prefix}", strict=False)
            subnets = list(original_network.subnets(new_prefix=new_prefix))
            return [str(subnet) for subnet in subnets[:10]]  # First 10 subnets
        except ValueError as e:
            return [f"Error: {e}"]

# 3. REGULAR EXPRESSIONS (For parsing network device output)
class NetworkOutputParser:
    """Parse common network device outputs using regex"""
    
    def __init__(self):
        # Common regex patterns for network parsing
        self.patterns = {
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'mac_address': r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})',
            'interface': r'(GigabitEthernet|FastEthernet|Ethernet|Gi|Fa|Et)\d+/\d+(?:/\d+)?',
            'vlan_id': r'VLAN\s+(\d+)',
            'ip_route': r'(\d+\.\d+\.\d+\.\d+/\d+)\s+via\s+(\d+\.\d+\.\d+\.\d+)'
        }
    
    def parse_show_interfaces(self, output):
        """Parse 'show interfaces' output"""
        interfaces = []
        
        # Sample parsing logic
        interface_blocks = re.split(r'\n(?=\w)', output)
        
        for block in interface_blocks:
            if_match = re.search(self.patterns['interface'], block)
            if if_match:
                interface_name = if_match.group(0)
                
                # Extract status
                status = 'down'
                if 'line protocol is up' in block.lower():
                    status = 'up'
                
                # Extract IP if present
                ip_match = re.search(r'Internet address is (\d+\.\d+\.\d+\.\d+/\d+)', block)
                ip_address = ip_match.group(1) if ip_match else None
                
                interfaces.append({
                    'name': interface_name,
                    'status': status,
                    'ip_address': ip_address
                })
        
        return interfaces
    
    def extract_mac_addresses(self, text):
        """Extract all MAC addresses from text"""
        return re.findall(self.patterns['mac_address'], text)
    
    def extract_ip_addresses(self, text):
        """Extract all IP addresses from text"""
        return re.findall(self.patterns['ip_address'], text)

# 4. JSON/XML DATA HANDLING (For REST APIs and device configs)
class NetworkDataProcessor:
    """Process network data in various formats"""
    
    def process_device_json(self, json_data):
        """Process device information from JSON"""
        try:
            if isinstance(json_data, str):
                data = json.loads(json_data)
            else:
                data = json_data
            
            # Extract key information
            result = {
                'hostname': data.get('hostname', 'Unknown'),
                'model': data.get('model', 'Unknown'),
                'version': data.get('version', 'Unknown'),
                'interfaces': []
            }
            
            # Process interfaces
            if 'interfaces' in data:
                for interface in data['interfaces']:
                    result['interfaces'].append({
                        'name': interface.get('name'),
                        'status': interface.get('admin_status'),
                        'ip': interface.get('ip_address')
                    })
            
            return result
            
        except json.JSONDecodeError as e:
            return {'error': f'JSON parsing error: {e}'}
    
    def create_test_report(self, test_results):
        """Create JSON test report"""
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': len(test_results),
            'passed': sum(1 for r in test_results if r['status'] == 'PASS'),
            'failed': sum(1 for r in test_results if r['status'] == 'FAIL'),
            'results': test_results
        }
        
        return json.dumps(report, indent=2)

# 5. THREADING FOR CONCURRENT NETWORK OPERATIONS
class ConcurrentNetworkTester:
    """Perform network tests concurrently"""
    
    def __init__(self, max_threads=10):
        self.max_threads = max_threads
        self.results = []
        self.lock = threading.Lock()
    
    def test_device_connectivity(self, device_info):
        """Test connectivity to a single device"""
        host = device_info['ip']
        name = device_info['name']
        
        scanner = NetworkScanner()
        is_reachable = scanner.ping_host(host)
        open_ports = scanner.scan_common_ports(host) if is_reachable else {}
        
        result = {
            'device': name,
            'ip': host,
            'reachable': is_reachable,
            'open_ports': open_ports,
            'timestamp': time.strftime('%H:%M:%S')
        }
        
        with self.lock:
            self.results.append(result)
            print(f"Tested {name} ({host}): {'REACHABLE' if is_reachable else 'UNREACHABLE'}")
    
    def test_multiple_devices(self, devices):
        """Test multiple devices concurrently"""
        threads = []
        
        for device in devices:
            thread = threading.Thread(target=self.test_device_connectivity, args=(device,))
            threads.append(thread)
            thread.start()
            
            # Limit concurrent threads
            if len(threads) >= self.max_threads:
                for t in threads:
                    t.join()
                threads = []
        
        # Wait for remaining threads
        for thread in threads:
            thread.join()
        
        return self.results

# DEMONSTRATION FUNCTIONS
def demonstrate_socket_programming():
    """Demonstrate socket programming concepts"""
    print("=== SOCKET PROGRAMMING ===")
    
    scanner = NetworkScanner()
    
    # Test local connectivity
    test_hosts = ['127.0.0.1', '8.8.8.8', '1.1.1.1']
    
    for host in test_hosts:
        print(f"Testing {host}:")
        open_ports = scanner.scan_common_ports(host)
        if open_ports:
            print(f"  Open ports: {open_ports}")
        else:
            print(f"  No common ports open or host unreachable")
    print()

def demonstrate_ip_utilities():
    """Demonstrate IP address utilities"""
    print("=== IP ADDRESS UTILITIES ===")
    
    ip_utils = IPAddressUtils()
    
    # Test IP validation
    test_ips = ['192.168.1.1', '256.1.1.1', '10.0.0.0', 'invalid']
    for ip in test_ips:
        print(f"IP {ip} is {'valid' if ip_utils.validate_ip(ip) else 'invalid'}")
    
    # Network information
    network_info = ip_utils.get_network_info('192.168.1.0/24')
    print(f"\nNetwork 192.168.1.0/24 info:")
    for key, value in network_info.items():
        print(f"  {key}: {value}")
    
    # Subnet calculation
    subnets = ip_utils.subnet_calculator('192.168.1.0', 24, 26)
    print(f"\nSubnetting 192.168.1.0/24 into /26 networks:")
    for subnet in subnets:
        print(f"  {subnet}")
    print()

def demonstrate_regex_parsing():
    """Demonstrate network output parsing"""
    print("=== REGEX PARSING ===")
    
    # Sample Cisco output
    sample_output = """
GigabitEthernet0/1 is up, line protocol is up
  Hardware is Gigabit Ethernet, address is 0012.7f57.d940 (bia 0012.7f57.d940)
  Internet address is 192.168.1.1/24
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,

FastEthernet0/2 is administratively down, line protocol is down
  Hardware is Fast Ethernet, address is 0012.7f57.d941 (bia 0012.7f57.d941)
"""
    
    parser = NetworkOutputParser()
    interfaces = parser.parse_show_interfaces(sample_output)
    
    print("Parsed interfaces:")
    for interface in interfaces:
        print(f"  {interface}")
    
    # Extract MAC addresses
    mac_addresses = parser.extract_mac_addresses(sample_output)
    print(f"\nMAC addresses found: {mac_addresses}")
    print()

# MAIN EXECUTION
if __name__ == "__main__":
    print("=== CISCO PYTHON INTERVIEW PREP - NETWORKING ===\n")
    
    # Demonstrate different concepts
    demonstrate_socket_programming()
    demonstrate_ip_utilities()
    demonstrate_regex_parsing()
    
    # Concurrent testing example
    print("=== CONCURRENT NETWORK TESTING ===")
    devices = [
        {'name': 'Google DNS', 'ip': '8.8.8.8'},
        {'name': 'Cloudflare DNS', 'ip': '1.1.1.1'},
        {'name': 'Localhost', 'ip': '127.0.0.1'}
    ]
    
    tester = ConcurrentNetworkTester(max_threads=3)
    results = tester.test_multiple_devices(devices)
    
    print(f"\nTesting completed. Results:")
    for result in results:
        print(f"  {result['device']}: {result['reachable']}")
