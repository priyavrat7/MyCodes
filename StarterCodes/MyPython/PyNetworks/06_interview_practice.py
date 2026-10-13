#!/usr/bin/env python3
"""
Cisco Python Interview Practice Questions and Solutions
Topics: Common interview questions, coding challenges, system design
"""

import time
import threading
import queue
import json
import re
from collections import defaultdict, deque
from typing import List, Dict, Set, Optional, Tuple
import heapq
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. PYTHON FUNDAMENTALS QUESTIONS
class PythonFundamentals:
    """Common Python interview questions"""
    
    @staticmethod
    def explain_gil():
        """Explain Python's Global Interpreter Lock"""
        explanation = """
        Python's Global Interpreter Lock (GIL):
        
        1. What is GIL?
           - A mutex that prevents multiple native threads from executing Python bytecodes at once
           - Only one thread can execute Python code at a time
        
        2. Why does it exist?
           - Protects access to Python objects
           - Prevents race conditions in memory management
           - Simplifies C extension development
        
        3. Impact on multithreading:
           - CPU-bound tasks don't benefit from multithreading
           - I/O-bound tasks can still benefit (GIL released during I/O)
           - Use multiprocessing for CPU-bound parallelism
        
        4. Alternatives:
           - multiprocessing module
           - asyncio for I/O-bound tasks
           - C extensions that release GIL
        """
        return explanation
    
    @staticmethod
    def demonstrate_decorators():
        """Demonstrate decorator patterns"""
        
        # 1. Function decorator
        def timing_decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()
                print(f"{func.__name__} took {end - start:.4f} seconds")
                return result
            return wrapper
        
        # 2. Class decorator
        def singleton(cls):
            instances = {}
            def get_instance(*args, **kwargs):
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
                return instances[cls]
            return get_instance
        
        # 3. Parameterized decorator
        def retry(max_attempts=3):
            def decorator(func):
                def wrapper(*args, **kwargs):
                    for attempt in range(max_attempts):
                        try:
                            return func(*args, **kwargs)
                        except Exception as e:
                            if attempt == max_attempts - 1:
                                raise e
                            print(f"Attempt {attempt + 1} failed: {e}")
                return wrapper
            return decorator
        
        return timing_decorator, singleton, retry
    
    @staticmethod
    def demonstrate_context_managers():
        """Demonstrate context manager patterns"""
        
        # 1. Class-based context manager
        class NetworkConnection:
            def __init__(self, host, port):
                self.host = host
                self.port = port
                self.connection = None
            
            def __enter__(self):
                print(f"Connecting to {self.host}:{self.port}")
                self.connection = f"Connection to {self.host}:{self.port}"
                return self.connection
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                print(f"Closing connection to {self.host}:{self.port}")
                if exc_type:
                    print(f"Exception occurred: {exc_val}")
                return False
        
        # 2. Function-based context manager
        from contextlib import contextmanager
        
        @contextmanager
        def device_config_mode(device):
            print(f"Entering config mode on {device}")
            try:
                yield f"config_session_{device}"
            finally:
                print(f"Exiting config mode on {device}")
        
        return NetworkConnection, device_config_mode

# 2. NETWORKING SPECIFIC CODING CHALLENGES
class NetworkingChallenges:
    """Network-specific coding problems"""
    
    @staticmethod
    def parse_cisco_config(config_text: str) -> Dict:
        """Parse Cisco configuration text"""
        config = {}
        current_section = None
        indent_stack = []
        
        lines = config_text.strip().split('\n')
        
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('!'):
                continue
            
            # Calculate indentation level
            indent = len(line) - len(line.lstrip())
            
            # Adjust stack based on indentation
            while indent_stack and indent <= indent_stack[-1][1]:
                indent_stack.pop()
            
            if indent == 0:
                # Top-level command
                if stripped.startswith('interface '):
                    interface_name = stripped.split()[1]
                    config.setdefault('interfaces', {})[interface_name] = {}
                    current_section = config['interfaces'][interface_name]
                    indent_stack = [(interface_name, indent)]
                elif stripped.startswith('router '):
                    router_type = ' '.join(stripped.split()[1:])
                    config.setdefault('routing', {})[router_type] = {}
                    current_section = config['routing'][router_type]
                    indent_stack = [(router_type, indent)]
                else:
                    config[stripped] = True
            else:
                # Nested command
                if current_section is not None:
                    if ' ' in stripped:
                        key, value = stripped.split(' ', 1)
                        current_section[key] = value
                    else:
                        current_section[stripped] = True
        
        return config
    
    @staticmethod
    def find_network_path(topology: Dict, start: str, end: str) -> List[str]:
        """Find shortest path in network topology using BFS"""
        if start == end:
            return [start]
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            for neighbor in topology.get(current, []):
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return []  # No path found
    
    @staticmethod
    def calculate_subnet_utilization(subnet: str, used_ips: List[str]) -> Dict:
        """Calculate subnet utilization"""
        import ipaddress
        
        try:
            network = ipaddress.ip_network(subnet, strict=False)
            total_hosts = network.num_addresses - 2  # Exclude network and broadcast
            
            valid_used_ips = []
            for ip in used_ips:
                try:
                    ip_addr = ipaddress.ip_address(ip)
                    if ip_addr in network and ip_addr not in [network.network_address, network.broadcast_address]:
                        valid_used_ips.append(str(ip_addr))
                except ValueError:
                    continue
            
            used_count = len(set(valid_used_ips))  # Remove duplicates
            utilization = (used_count / total_hosts) * 100 if total_hosts > 0 else 0
            
            return {
                'subnet': subnet,
                'total_hosts': total_hosts,
                'used_hosts': used_count,
                'available_hosts': total_hosts - used_count,
                'utilization_percent': round(utilization, 2),
                'network_address': str(network.network_address),
                'broadcast_address': str(network.broadcast_address)
            }
        
        except ValueError as e:
            return {'error': str(e)}
    
    @staticmethod
    def parse_show_interface_output(output: str) -> Dict:
        """Parse 'show interface' output"""
        interfaces = {}
        current_interface = None
        
        lines = output.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Interface line
            if ' is ' in line and ('up' in line or 'down' in line):
                parts = line.split(' is ')
                if len(parts) >= 2:
                    interface_name = parts[0].strip()
                    status_parts = parts[1].split(', line protocol is ')
                    admin_status = status_parts[0].strip()
                    protocol_status = status_parts[1].strip() if len(status_parts) > 1 else 'unknown'
                    
                    interfaces[interface_name] = {
                        'admin_status': admin_status,
                        'protocol_status': protocol_status
                    }
                    current_interface = interface_name
            
            # Parse additional interface details
            elif current_interface and line:
                if line.startswith('Hardware is'):
                    interfaces[current_interface]['hardware'] = line.split('Hardware is ')[1].split(',')[0]
                elif 'address is' in line:
                    mac_match = re.search(r'address is ([0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4})', line)
                    if mac_match:
                        interfaces[current_interface]['mac_address'] = mac_match.group(1)
                elif line.startswith('Internet address is'):
                    ip_match = re.search(r'Internet address is (\d+\.\d+\.\d+\.\d+/\d+)', line)
                    if ip_match:
                        interfaces[current_interface]['ip_address'] = ip_match.group(1)
                elif 'MTU' in line:
                    mtu_match = re.search(r'MTU (\d+) bytes', line)
                    if mtu_match:
                        interfaces[current_interface]['mtu'] = int(mtu_match.group(1))
        
        return interfaces

# 3. ALGORITHM AND DATA STRUCTURE QUESTIONS
class AlgorithmChallenges:
    """Algorithm challenges relevant to networking"""
    
    @staticmethod
    def dijkstra_shortest_path(graph: Dict, start: str) -> Dict:
        """Dijkstra's algorithm for shortest path (used in OSPF)"""
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0
        previous = {}
        unvisited = list(graph.keys())
        
        while unvisited:
            current = min(unvisited, key=lambda x: distances[x])
            unvisited.remove(current)
            
            if distances[current] == float('infinity'):
                break
            
            for neighbor, weight in graph[current].items():
                distance = distances[current] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
        
        return distances, previous
    
    @staticmethod
    def detect_network_loop(topology: Dict) -> bool:
        """Detect loops in network topology using DFS"""
        visited = set()
        rec_stack = set()
        
        def dfs(node, parent=None):
            if node in rec_stack:
                return True  # Back edge found - loop detected
            
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in topology.get(node, []):
                if neighbor != parent and dfs(neighbor, node):
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in topology:
            if node not in visited:
                if dfs(node):
                    return True
        
        return False
    
    @staticmethod
    def load_balance_servers(requests: List[int], servers: int) -> List[List[int]]:
        """Distribute network requests across servers (load balancing)"""
        if servers <= 0:
            return []
        
        # Use min-heap to track server loads
        server_loads = [(0, i, []) for i in range(servers)]
        heapq.heapify(server_loads)
        
        for request in requests:
            # Get server with minimum load
            current_load, server_id, server_requests = heapq.heappop(server_loads)
            
            # Assign request to this server
            server_requests.append(request)
            new_load = current_load + request
            
            # Put server back with updated load
            heapq.heappush(server_loads, (new_load, server_id, server_requests))
        
        # Return server assignments
        result = [[] for _ in range(servers)]
        for load, server_id, server_requests in server_loads:
            result[server_id] = server_requests
        
        return result

# 4. SYSTEM DESIGN QUESTIONS
class SystemDesignChallenges:
    """System design questions for network automation"""
    
    @staticmethod
    def design_network_monitoring_system():
        """Design a network monitoring system"""
        design = {
            "components": {
                "data_collectors": {
                    "snmp_collectors": "Collect SNMP data from devices",
                    "syslog_collectors": "Collect syslog messages",
                    "netflow_collectors": "Collect network flow data",
                    "api_collectors": "REST API polling"
                },
                "data_processing": {
                    "stream_processor": "Real-time data processing (Apache Kafka/Storm)",
                    "batch_processor": "Historical data analysis",
                    "anomaly_detector": "ML-based anomaly detection"
                },
                "data_storage": {
                    "time_series_db": "Metrics storage (InfluxDB/Prometheus)",
                    "document_db": "Configuration and topology (MongoDB)",
                    "relational_db": "Inventory and relationships (PostgreSQL)"
                },
                "apis_and_interfaces": {
                    "rest_api": "External integrations",
                    "web_dashboard": "User interface",
                    "alerting_system": "Notifications and alerts"
                }
            },
            "data_flow": [
                "1. Devices generate telemetry data",
                "2. Collectors gather data via SNMP/APIs/Syslog",
                "3. Stream processor handles real-time analysis",
                "4. Data stored in appropriate databases",
                "5. Dashboard displays metrics and alerts",
                "6. Alerting system notifies on issues"
            ],
            "scalability_considerations": [
                "Horizontal scaling of collectors",
                "Load balancing for API endpoints",
                "Database sharding for large datasets",
                "Caching for frequently accessed data",
                "Message queues for decoupling components"
            ]
        }
        return design
    
    @staticmethod
    def design_network_automation_platform():
        """Design a network automation platform"""
        design = {
            "architecture": {
                "controller_layer": {
                    "orchestrator": "Workflow orchestration engine",
                    "scheduler": "Job scheduling and queuing",
                    "state_manager": "Device state management"
                },
                "abstraction_layer": {
                    "device_drivers": "Device-specific implementations",
                    "protocol_handlers": "NETCONF, RESTCONF, SSH handlers",
                    "template_engine": "Configuration templating"
                },
                "data_layer": {
                    "inventory_db": "Device inventory and topology",
                    "config_store": "Configuration templates and policies",
                    "audit_log": "Change tracking and compliance"
                }
            },
            "key_features": [
                "Multi-vendor device support",
                "Configuration templating and validation",
                "Rollback and recovery mechanisms",
                "Compliance checking and reporting",
                "Integration with CI/CD pipelines",
                "Role-based access control"
            ],
            "implementation_technologies": {
                "backend": "Python (Django/Flask), Go, or Java",
                "database": "PostgreSQL + Redis for caching",
                "message_queue": "RabbitMQ or Apache Kafka",
                "containerization": "Docker + Kubernetes",
                "frontend": "React or Vue.js"
            }
        }
        return design

# 5. PRACTICAL CODING EXERCISES
class PracticalExercises:
    """Hands-on coding exercises"""
    
    @staticmethod
    def network_device_simulator():
        """Create a simple network device simulator"""
        
        class NetworkDevice:
            def __init__(self, hostname, device_type="switch"):
                self.hostname = hostname
                self.device_type = device_type
                self.interfaces = {}
                self.routing_table = []
                self.arp_table = {}
                self.mac_table = {}
                self.vlans = {}
            
            def add_interface(self, name, ip_address=None, status="up"):
                self.interfaces[name] = {
                    'ip_address': ip_address,
                    'status': status,
                    'mac_address': f"00:1a:2b:3c:4d:{len(self.interfaces):02x}"
                }
            
            def add_route(self, destination, next_hop, interface):
                self.routing_table.append({
                    'destination': destination,
                    'next_hop': next_hop,
                    'interface': interface,
                    'metric': 1
                })
            
            def show_interfaces(self):
                result = []
                for name, info in self.interfaces.items():
                    result.append(f"{name:<20} {info['ip_address'] or 'unassigned':<15} {info['status']}")
                return "\n".join(result)
            
            def show_routing_table(self):
                result = []
                for route in self.routing_table:
                    result.append(f"{route['destination']:<18} {route['next_hop']:<15} {route['interface']}")
                return "\n".join(result)
        
        return NetworkDevice
    
    @staticmethod
    def configuration_backup_system():
        """Create a configuration backup system"""
        
        class ConfigBackupManager:
            def __init__(self):
                self.backups = {}
                self.versions = defaultdict(list)
            
            def backup_config(self, device_id, config_data):
                timestamp = time.strftime('%Y%m%d_%H%M%S')
                backup_id = f"{device_id}_{timestamp}"
                
                self.backups[backup_id] = {
                    'device_id': device_id,
                    'timestamp': timestamp,
                    'config': config_data,
                    'size': len(config_data)
                }
                
                self.versions[device_id].append(backup_id)
                return backup_id
            
            def restore_config(self, backup_id):
                if backup_id in self.backups:
                    return self.backups[backup_id]['config']
                return None
            
            def list_backups(self, device_id=None):
                if device_id:
                    return self.versions.get(device_id, [])
                return list(self.backups.keys())
            
            def compare_configs(self, backup_id1, backup_id2):
                config1 = self.backups.get(backup_id1, {}).get('config', '')
                config2 = self.backups.get(backup_id2, {}).get('config', '')
                
                lines1 = config1.split('\n')
                lines2 = config2.split('\n')
                
                differences = []
                max_lines = max(len(lines1), len(lines2))
                
                for i in range(max_lines):
                    line1 = lines1[i] if i < len(lines1) else ''
                    line2 = lines2[i] if i < len(lines2) else ''
                    
                    if line1 != line2:
                        differences.append({
                            'line': i + 1,
                            'backup1': line1,
                            'backup2': line2
                        })
                
                return differences
        
        return ConfigBackupManager

# DEMONSTRATION AND TESTING
def run_interview_practice():
    """Run interview practice scenarios"""
    logger.info("=== CISCO PYTHON INTERVIEW PRACTICE ===\n")
    
    # 1. Python Fundamentals
    logger.info("1. PYTHON FUNDAMENTALS:")
    fundamentals = PythonFundamentals()
    
    # Demonstrate decorators
    timing_decorator, singleton, retry = fundamentals.demonstrate_decorators()
    
    @timing_decorator
    def sample_function():
        time.sleep(0.1)
        return "Function completed"
    
    result = sample_function()
    logger.info(f"Result: {result}")
    
    # 2. Networking Challenges
    logger.info("\n2. NETWORKING CHALLENGES:")
    challenges = NetworkingChallenges()
    
    # Parse Cisco config
    sample_config = """
interface GigabitEthernet0/1
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/2
 switchport mode access
 switchport access vlan 10
!
router ospf 1
 network 192.168.1.0 0.0.0.255 area 0
"""
    
    parsed_config = challenges.parse_cisco_config(sample_config)
    logger.info(f"Parsed config: {json.dumps(parsed_config, indent=2)}")
    
    # Network path finding
    topology = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    path = challenges.find_network_path(topology, 'A', 'F')
    logger.info(f"Shortest path from A to F: {path}")
    
    # 3. Algorithm Challenges
    logger.info("\n3. ALGORITHM CHALLENGES:")
    algorithms = AlgorithmChallenges()
    
    # Dijkstra's algorithm
    graph = {
        'A': {'B': 4, 'C': 2},
        'B': {'A': 4, 'C': 1, 'D': 5},
        'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
        'D': {'B': 5, 'C': 8, 'E': 2},
        'E': {'C': 10, 'D': 2}
    }
    
    distances, previous = algorithms.dijkstra_shortest_path(graph, 'A')
    logger.info(f"Shortest distances from A: {distances}")
    
    # Loop detection
    loop_topology = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A']  # Creates a loop
    }
    
    has_loop = algorithms.detect_network_loop(loop_topology)
    logger.info(f"Network has loop: {has_loop}")
    
    # 4. Practical Exercises
    logger.info("\n4. PRACTICAL EXERCISES:")
    exercises = PracticalExercises()
    
    # Device simulator
    NetworkDevice = exercises.network_device_simulator()
    device = NetworkDevice("switch-01", "switch")
    device.add_interface("GigE0/1", "192.168.1.1/24", "up")
    device.add_interface("GigE0/2", "192.168.2.1/24", "down")
    device.add_route("0.0.0.0/0", "192.168.1.254", "GigE0/1")
    
    logger.info("Device interfaces:")
    logger.info(device.show_interfaces())
    logger.info("\nRouting table:")
    logger.info(device.show_routing_table())

# MAIN EXECUTION
if __name__ == "__main__":
    run_interview_practice()
    
    print("\n" + "="*60)
    print("CISCO INTERVIEW PREPARATION CHECKLIST")
    print("="*60)
    
    checklist = [
        "✓ Python fundamentals (data structures, OOP, decorators)",
        "✓ Networking concepts (TCP/IP, VLAN, routing protocols)",
        "✓ Test automation frameworks (pytest, unittest)",
        "✓ pyATS framework and Genie parsers",
        "✓ Regular expressions for parsing device output",
        "✓ JSON/YAML data handling",
        "✓ Socket programming and network libraries",
        "✓ Threading and async programming",
        "✓ Algorithm and data structures",
        "✓ System design principles",
        "✓ Git version control",
        "✓ CI/CD concepts (Jenkins)",
        "✓ Network protocols (OSPF, BGP, MPLS)",
        "✓ SDN and network virtualization",
        "✓ QoS and traffic engineering"
    ]
    
    for item in checklist:
        print(item)
    
    print("\n" + "="*60)
    print("SAMPLE INTERVIEW QUESTIONS TO PRACTICE")
    print("="*60)
    
    questions = [
        "1. How would you automate configuration backup for 1000+ devices?",
        "2. Explain the difference between SNMP v2c and v3",
        "3. How would you detect network loops programmatically?",
        "4. Design a system to monitor network device health",
        "5. How would you implement load balancing in Python?",
        "6. Explain OSPF LSA types and their purposes",
        "7. How would you parse and validate network configurations?",
        "8. What's the difference between iBGP and eBGP?",
        "9. How would you implement a network topology discovery tool?",
        "10. Explain how you'd test network convergence time"
    ]
    
    for question in questions:
        print(question)
