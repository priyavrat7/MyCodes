#!/usr/bin/env python3
"""
Python Fundamentals for Network Testing - Cisco Interview Prep
Topics: Data structures, functions, OOP, error handling
"""

# 1. DATA STRUCTURES (Critical for network data processing)
def demonstrate_data_structures():
    """Network devices often return data in various formats"""
    
    # Lists - for storing multiple network interfaces
    interfaces = ['GigabitEthernet0/1', 'GigabitEthernet0/2', 'FastEthernet0/1']
    print(f"Network Interfaces: {interfaces}")
    
    # Dictionaries - for device configuration and status
    device_config = {
        'hostname': 'cisco-switch-01',
        'ip_address': '192.168.1.1',
        'interfaces': {
            'GigE0/1': {'status': 'up', 'speed': '1000'},
            'GigE0/2': {'status': 'down', 'speed': '1000'}
        },
        'vlans': [10, 20, 30, 100]
    }
    
    # Accessing nested data (common in network APIs)
    print(f"Device: {device_config['hostname']}")
    print(f"Interface GigE0/1 status: {device_config['interfaces']['GigE0/1']['status']}")
    
    # Sets - for unique VLANs, IP addresses
    vlans_switch1 = {10, 20, 30, 40}
    vlans_switch2 = {20, 30, 50, 60}
    common_vlans = vlans_switch1.intersection(vlans_switch2)
    print(f"Common VLANs: {common_vlans}")
    
    # Tuples - for immutable network coordinates
    network_endpoint = ('192.168.1.1', 22, 'ssh')  # (ip, port, protocol)
    print(f"Endpoint: {network_endpoint}")

# 2. FUNCTIONS AND DECORATORS (For test automation)
def network_test_decorator(func):
    """Decorator to add logging to network tests"""
    def wrapper(*args, **kwargs):
        print(f"Starting test: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            print(f"Test {func.__name__} PASSED")
            return result
        except Exception as e:
            print(f"Test {func.__name__} FAILED: {e}")
            raise
    return wrapper

@network_test_decorator
def ping_test(host, count=4):
    """Simulate a ping test"""
    import random
    if random.choice([True, False]):  # Simulate success/failure
        return f"Ping to {host} successful ({count} packets)"
    else:
        raise Exception(f"Ping to {host} failed")

# 3. CLASSES AND OOP (Essential for test frameworks)
class NetworkDevice:
    """Base class for network devices"""
    
    def __init__(self, hostname, ip_address, device_type):
        self.hostname = hostname
        self.ip_address = ip_address
        self.device_type = device_type
        self.interfaces = {}
        self.is_connected = False
    
    def connect(self):
        """Simulate device connection"""
        print(f"Connecting to {self.hostname} ({self.ip_address})")
        self.is_connected = True
        return True
    
    def disconnect(self):
        """Simulate device disconnection"""
        print(f"Disconnecting from {self.hostname}")
        self.is_connected = False
    
    def get_interface_status(self, interface):
        """Get interface status"""
        return self.interfaces.get(interface, "Interface not found")
    
    def __str__(self):
        return f"{self.device_type}: {self.hostname} ({self.ip_address})"

class CiscoSwitch(NetworkDevice):
    """Cisco Switch specific implementation"""
    
    def __init__(self, hostname, ip_address, model):
        super().__init__(hostname, ip_address, "Cisco Switch")
        self.model = model
        self.vlans = set()
    
    def add_vlan(self, vlan_id, vlan_name):
        """Add VLAN to switch"""
        self.vlans.add(vlan_id)
        print(f"Added VLAN {vlan_id} ({vlan_name}) to {self.hostname}")
    
    def show_vlans(self):
        """Display configured VLANs"""
        return sorted(list(self.vlans))

# 4. ERROR HANDLING (Critical for robust test automation)
def robust_device_connection(device_ip, timeout=30):
    """Demonstrate proper error handling for network operations"""
    try:
        # Simulate connection attempt
        import random
        if random.random() < 0.3:  # 30% chance of failure
            # The error is specific AND the keyword (ConnectionError) is predefined
            raise ConnectionError(f"Cannot connect to {device_ip}")
        
        print(f"Successfully connected to {device_ip}")
        return True
        
    except ConnectionError as e:
        print(f"Connection Error: {e}")
        return False
    except TimeoutError as e:
        print(f"Timeout Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return False
    finally:
        print("Connection attempt completed")

# 5. LIST COMPREHENSIONS AND GENERATORS (Efficient data processing)
def process_network_data():
    """Demonstrate efficient data processing techniques"""
    
    # Sample network data as a list of dictionaries
    interfaces_data = [
        {'name': 'GigE0/1', 'status': 'up', 'speed': 1000, 'utilization': 45},
        {'name': 'GigE0/2', 'status': 'down', 'speed': 1000, 'utilization': 0},
        {'name': 'GigE0/3', 'status': 'up', 'speed': 100, 'utilization': 78},
        {'name': 'FastE0/1', 'status': 'up', 'speed': 100, 'utilization': 23}
    ]
    
    # List comprehension - find active high-utilization interfaces
    high_util_interfaces = [
        iface['name'] for iface in interfaces_data 
        if iface['status'] == 'up' and iface['utilization'] > 50
    ]
    print(f"High utilization interfaces: {high_util_interfaces}")
    
    # Generator for memory-efficient processing
    def interface_alerts(interfaces):
        for iface in interfaces:
            if iface['status'] == 'down':
                yield f"ALERT: {iface['name']} is DOWN"
            elif iface['utilization'] > 80:
                yield f"WARNING: {iface['name']} utilization is {iface['utilization']}%"
    
    # Process alerts
    for alert in interface_alerts(interfaces_data):
        print(alert)

# 6. CONTEXT MANAGERS (For resource management)
class NetworkConnection:
    """Context manager for network connections"""
    
    def __init__(self, device_ip):
        self.device_ip = device_ip
        self.connection = None
    
    def __enter__(self):
        print(f"Establishing connection to {self.device_ip}")
        self.connection = f"Connection to {self.device_ip}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing connection to {self.device_ip}")
        if exc_type:
            print(f"Connection closed due to error: {exc_val}")
        return False

# MAIN EXECUTION
if __name__ == "__main__":
    print("=== CISCO PYTHON INTERVIEW PREP - FUNDAMENTALS ===\n")
    
    # 1. Data Structures
    print("1. DATA STRUCTURES:")
    demonstrate_data_structures()
    print()
    
    # 2. Functions and Decorators
    print("2. FUNCTIONS AND DECORATORS:")
    try:
        result = ping_test("192.168.1.1")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Caught exception: {e}")
    print()
    
    # 3. OOP
    print("3. OBJECT-ORIENTED PROGRAMMING:")
    switch = CiscoSwitch("SW-Core-01", "192.168.1.10", "Catalyst 9300")
    switch.connect()
    switch.add_vlan(100, "Production")
    switch.add_vlan(200, "Development")
    print(f"Configured VLANs: {switch.show_vlans()}")
    print(f"Device Info: {switch}")
    switch.disconnect()
    print()
    
    # 4. Error Handling
    print("4. ERROR HANDLING:")
    robust_device_connection("192.168.1.1")
    print()
    
    # 5. Data Processing
    print("5. EFFICIENT DATA PROCESSING:")
    process_network_data()
    print()
    
    # 6. Context Managers
    print("6. CONTEXT MANAGERS:")
    with NetworkConnection("192.168.1.1") as conn:
        print(f"Using {conn}")
        # Simulate some work
        print("Executing network commands...")
