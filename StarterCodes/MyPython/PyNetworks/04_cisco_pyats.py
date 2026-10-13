#!/usr/bin/env python3
"""
Cisco pyATS Framework - Interview Preparation
Topics: pyATS concepts, Genie, testbed files, parsers, test scripts

Note: This is a conceptual demonstration. Real pyATS requires installation:
pip install pyats[full]
"""

import json
import yaml #to create and load testbed files
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import logging
import time
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. TESTBED CONFIGURATION (Core pyATS concept)
class TestbedManager:
    """Manage testbed configuration for pyATS"""
    
    def __init__(self):
        self.testbed_data = {}
    
    def create_testbed_yaml(self, filename="testbed.yaml"):
        """Create a sample testbed YAML file"""
        testbed_config = {
            'testbed': {
                'name': 'cisco_network_testbed',
                'alias': 'lab_testbed'
            },
            'devices': {
                'core_switch': {
                    'type': 'switch',
                    'os': 'iosxe',
                    'platform': 'cat9k',
                    'alias': 'core-sw-01',
                    'connections': {
                        'cli': {
                            'protocol': 'ssh',
                            'ip': '192.168.1.100',
                            'port': 22,
                            'arguments': {
                                'connection_timeout': 60,
                                'init_exec_commands': [],
                                'init_config_commands': []
                            }
                        }
                    },
                    'credentials': {
                        'default': {
                            'username': 'admin',
                            'password': 'cisco123'
                        },
                        'enable': {
                            'password': 'enable123'
                        }
                    },
                    'custom': {
                        'model': 'C9300-24T',
                        'version': '16.12.05'
                    }
                },
                'access_switch': {
                    'type': 'switch',
                    'os': 'iosxe',
                    'platform': 'cat9k',
                    'alias': 'access-sw-01',
                    'connections': {
                        'cli': {
                            'protocol': 'ssh',
                            'ip': '192.168.1.101',
                            'port': 22
                        }
                    },
                    'credentials': {
                        'default': {
                            'username': 'admin',
                            'password': 'cisco123'
                        }
                    }
                },
                'router': {
                    'type': 'router',
                    'os': 'iosxe',
                    'platform': 'isr',
                    'alias': 'edge-rtr-01',
                    'connections': {
                        'cli': {
                            'protocol': 'telnet',
                            'ip': '192.168.1.1',
                            'port': 23
                        }
                    },
                    'credentials': {
                        'default': {
                            'username': 'admin',
                            'password': 'cisco123'
                        }
                    }
                }
            },
            'topology': {
                'core_switch': {
                    'interfaces': {
                        'GigabitEthernet1/0/1': {
                            'link': 'link_1',
                            'type': 'ethernet'
                        },
                        'GigabitEthernet1/0/2': {
                            'link': 'link_2', 
                            'type': 'ethernet'
                        }
                    }
                },
                'access_switch': {
                    'interfaces': {
                        'GigabitEthernet1/0/1': {
                            'link': 'link_1',
                            'type': 'ethernet'
                        }
                    }
                },
                'router': {
                    'interfaces': {
                        'GigabitEthernet0/0/0': {
                            'link': 'link_2',
                            'type': 'ethernet'
                        }
                    }
                }
            }
        }
        
        with open(filename, 'w') as f:
            yaml.dump(testbed_config, f, default_flow_style=False, indent=2)
        
        self.testbed_data = testbed_config
        logger.info(f"Created testbed file: {filename}")
        return testbed_config
    
    def load_testbed(self, filename="testbed.yaml"):
        """Load testbed from YAML file"""
        try:
            with open(filename, 'r') as f:
                self.testbed_data = yaml.safe_load(f)
            logger.info(f"Loaded testbed from {filename}")
            return self.testbed_data
        except FileNotFoundError:
            logger.error(f"Testbed file {filename} not found")
            return None

# 2. DEVICE CONNECTION SIMULATION (pyATS Device concept)
class MockDevice:
    """Mock device class simulating pyATS Device"""
    
    def __init__(self, name, device_info):
        self.name = name
        self.device_info = device_info
        self.connected = False
        self.command_outputs = self._initialize_mock_outputs()
    
    def connect(self):
        """Simulate device connection"""
        logger.info(f"Connecting to {self.name} ({self.device_info.get('connections', {}).get('cli', {}).get('ip', 'unknown')})")
        time.sleep(0.5)  # Simulate connection delay
        self.connected = True
        logger.info(f"Successfully connected to {self.name}")
        return True
    
    def disconnect(self):
        """Simulate device disconnection"""
        logger.info(f"Disconnecting from {self.name}")
        self.connected = False
    
    def execute(self, command):
        """Execute command on device (mock)"""
        if not self.connected:
            raise Exception(f"Device {self.name} is not connected")
        
        logger.info(f"Executing command on {self.name}: {command}")
        
        # Return mock output based on command
        return self.command_outputs.get(command, f"Mock output for: {command}")
    
    def parse(self, command, output=None):
        """Parse command output using Genie parsers (mock)"""
        if output is None:
            output = self.execute(command)
        
        # Mock parser results
        if "show version" in command:
            return self._parse_show_version(output)
        elif "show interfaces" in command:
            return self._parse_show_interfaces(output)
        elif "show ip route" in command:
            return self._parse_show_ip_route(output)
        else:
            return {"raw_output": output}
    
    def _initialize_mock_outputs(self):
        """Initialize mock command outputs"""
        return {
            "show version": """
Cisco IOS XE Software, Version 16.12.05
Cisco Catalyst 9300 Series Switches
System uptime is 45 days, 12 hours, 30 minutes
""",
            "show interfaces brief": """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1/0/1   unassigned      YES unset  up                    up      
GigabitEthernet1/0/2   192.168.1.100   YES manual up                    up      
GigabitEthernet1/0/3   unassigned      YES unset  down                  down    
""",
            "show ip route": """
Gateway of last resort is 192.168.1.1 to network 0.0.0.0

     10.0.0.0/8 is variably subnetted, 3 subnets, 2 masks
C       10.1.1.0/24 is directly connected, GigabitEthernet1/0/1
C       10.2.2.0/24 is directly connected, GigabitEthernet1/0/2
S*   0.0.0.0/0 [1/0] via 192.168.1.1
""",
            "show vlan brief": """
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi1/0/3, Gi1/0/4
10   Production                       active    Gi1/0/1, Gi1/0/2
20   Development                      active    Gi1/0/5, Gi1/0/6
"""
        }
    
    def _parse_show_version(self, output):
        """Parse show version output"""
        return {
            "version": {
                "version": "16.12.05",
                "platform": "Catalyst 9300",
                "uptime": "45 days, 12 hours, 30 minutes"
            }
        }
    
    def _parse_show_interfaces(self, output):
        """Parse show interfaces output"""
        return {
            "interface": {
                "GigabitEthernet1/0/1": {
                    "oper_status": "up",
                    "line_protocol": "up",
                    "ip_address": "unassigned"
                },
                "GigabitEthernet1/0/2": {
                    "oper_status": "up", 
                    "line_protocol": "up",
                    "ip_address": "192.168.1.100"
                },
                "GigabitEthernet1/0/3": {
                    "oper_status": "down",
                    "line_protocol": "down",
                    "ip_address": "unassigned"
                }
            }
        }
    
    def _parse_show_ip_route(self, output):
        """Parse show ip route output"""
        return {
            "vrf": {
                "default": {
                    "address_family": {
                        "ipv4": {
                            "routes": {
                                "10.1.1.0/24": {
                                    "route": "10.1.1.0/24",
                                    "source_protocol": "connected",
                                    "next_hop": {
                                        "outgoing_interface": {
                                            "GigabitEthernet1/0/1": {
                                                "outgoing_interface": "GigabitEthernet1/0/1"
                                            }
                                        }
                                    }
                                },
                                "0.0.0.0/0": {
                                    "route": "0.0.0.0/0",
                                    "source_protocol": "static",
                                    "next_hop": {
                                        "next_hop_list": {
                                            1: {
                                                "next_hop": "192.168.1.1"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

# 3. TEST SCRIPT STRUCTURE (pyATS AEtest)
class NetworkTestScript:
    """Simulate pyATS AEtest structure"""
    
    def __init__(self, testbed_manager):
        self.testbed_manager = testbed_manager
        self.devices = {}
        self.test_results = {}
    
    def common_setup(self):
        """Common setup section (like AEtest CommonSetup)"""
        logger.info("=== COMMON SETUP ===")
        
        # Load testbed
        testbed_data = self.testbed_manager.testbed_data
        if not testbed_data:
            raise Exception("No testbed data available")
        
        # Connect to devices
        for device_name, device_info in testbed_data.get('devices', {}).items():
            device = MockDevice(device_name, device_info)
            device.connect()
            self.devices[device_name] = device
        
        logger.info(f"Connected to {len(self.devices)} devices")
    
    def test_device_reachability(self):
        """Test case: Device reachability"""
        logger.info("=== TEST: Device Reachability ===")
        
        for device_name, device in self.devices.items():
            try:
                # Simulate ping test
                result = device.execute("ping 8.8.8.8")
                self.test_results[f"{device_name}_reachability"] = "PASSED"
                logger.info(f"Device {device_name}: Reachability test PASSED")
            except Exception as e:
                self.test_results[f"{device_name}_reachability"] = f"FAILED: {e}"
                logger.error(f"Device {device_name}: Reachability test FAILED")
    
    def test_interface_status(self):
        """Test case: Interface status verification"""
        logger.info("=== TEST: Interface Status ===")
        
        for device_name, device in self.devices.items():
            try:
                # Get interface information
                parsed_output = device.parse("show interfaces brief")
                interfaces = parsed_output.get("interface", {})
                
                # Check critical interfaces
                critical_interfaces = ["GigabitEthernet1/0/1", "GigabitEthernet1/0/2"]
                
                for interface in critical_interfaces:
                    if interface in interfaces:
                        status = interfaces[interface].get("oper_status")
                        if status == "up":
                            logger.info(f"{device_name} - {interface}: UP")
                        else:
                            logger.warning(f"{device_name} - {interface}: {status}")
                
                self.test_results[f"{device_name}_interfaces"] = "PASSED"
                
            except Exception as e:
                self.test_results[f"{device_name}_interfaces"] = f"FAILED: {e}"
                logger.error(f"Interface test failed for {device_name}: {e}")
    
    def test_routing_table(self):
        """Test case: Routing table verification"""
        logger.info("=== TEST: Routing Table ===")
        
        for device_name, device in self.devices.items():
            if device.device_info.get('type') == 'router':
                try:
                    parsed_output = device.parse("show ip route")
                    routes = parsed_output.get("vrf", {}).get("default", {}).get("address_family", {}).get("ipv4", {}).get("routes", {})
                    
                    # Check for default route
                    if "0.0.0.0/0" in routes:
                        logger.info(f"{device_name}: Default route present")
                        self.test_results[f"{device_name}_routing"] = "PASSED"
                    else:
                        logger.warning(f"{device_name}: No default route found")
                        self.test_results[f"{device_name}_routing"] = "FAILED: No default route"
                        
                except Exception as e:
                    self.test_results[f"{device_name}_routing"] = f"FAILED: {e}"
                    logger.error(f"Routing test failed for {device_name}: {e}")
    
    def common_cleanup(self):
        """Common cleanup section"""
        logger.info("=== COMMON CLEANUP ===")
        
        # Disconnect from devices
        for device_name, device in self.devices.items():
            device.disconnect()
        
        # Print test summary
        self._print_test_summary()
    
    def _print_test_summary(self):
        """Print test execution summary"""
        logger.info("=== TEST SUMMARY ===")
        
        passed = sum(1 for result in self.test_results.values() if result == "PASSED")
        failed = len(self.test_results) - passed
        
        logger.info(f"Total tests: {len(self.test_results)}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {failed}")
        
        for test_name, result in self.test_results.items():
            logger.info(f"  {test_name}: {result}")

# 4. GENIE PARSERS SIMULATION
class GenieParserManager:
    """Simulate Genie parser functionality"""
    
    def __init__(self):
        self.available_parsers = {
            'iosxe': {
                'show version': 'ShowVersion',
                'show interfaces': 'ShowInterfaces', 
                'show ip route': 'ShowIpRoute',
                'show vlan': 'ShowVlan',
                'show ip ospf neighbor': 'ShowIpOspfNeighbor'
            }
        }
    
    def get_parser(self, os_type, command):
        """Get parser for specific OS and command"""
        parsers = self.available_parsers.get(os_type, {})
        return parsers.get(command, None)
    
    def parse_command(self, device, command):
        """Parse command output using appropriate parser"""
        parser_name = self.get_parser(device.device_info.get('os', 'iosxe'), command)
        
        if parser_name:
            logger.info(f"Using parser {parser_name} for command: {command}")
            return device.parse(command)
        else:
            logger.warning(f"No parser available for command: {command}")
            return {"raw_output": device.execute(command)}

# 5. PYATS JOB FILE SIMULATION
class PyATSJobManager:
    """Simulate pyATS job file functionality"""
    
    def __init__(self):
        self.job_config = {}
    
    def create_job_file(self, filename="job.py"):
        """Create a sample pyATS job file"""
        job_content = '''#!/usr/bin/env python3

"""
pyATS Job File - Network Automation Test Suite
"""

import os
from pyats.easypy import run

def main(runtime):
    """Main job function"""
    
    # Get testbed file
    testbed_file = runtime.args.testbed_file or 'testbed.yaml'
    
    # Run test scripts
    run(
        testscript='network_connectivity_test.py',
        runtime=runtime,
        testbed=testbed_file,
        task_id='ConnectivityTests'
    )
    
    run(
        testscript='interface_verification_test.py', 
        runtime=runtime,
        testbed=testbed_file,
        task_id='InterfaceTests'
    )
    
    run(
        testscript='protocol_verification_test.py',
        runtime=runtime,
        testbed=testbed_file,
        task_id='ProtocolTests'
    )

if __name__ == '__main__':
    import argparse
    from pyats.easypy import main as easypy_main
    
    parser = argparse.ArgumentParser(description='Network Test Job')
    parser.add_argument('--testbed-file', 
                       help='Testbed YAML file',
                       default='testbed.yaml')
    
    # Run the job
    easypy_main()
'''
        
        with open(filename, 'w') as f:
            f.write(job_content)
        
        logger.info(f"Created job file: {filename}")
        return job_content

# MAIN DEMONSTRATION
def demonstrate_pyats_workflow():
    """Demonstrate complete pyATS workflow"""
    logger.info("=== CISCO PYATS FRAMEWORK DEMONSTRATION ===\n")
    
    # 1. Create and load testbed
    testbed_mgr = TestbedManager()
    testbed_mgr.create_testbed_yaml("demo_testbed.yaml")
    
    # 2. Create job file
    job_mgr = PyATSJobManager()
    job_mgr.create_job_file("demo_job.py")
    
    # 3. Run test script
    test_script = NetworkTestScript(testbed_mgr)
    
    try:
        # Execute test workflow
        test_script.common_setup()
        test_script.test_device_reachability()
        test_script.test_interface_status()
        test_script.test_routing_table()
        
    finally:
        test_script.common_cleanup()
    
    # 4. Demonstrate Genie parsers
    logger.info("\n=== GENIE PARSER DEMONSTRATION ===")
    parser_mgr = GenieParserManager()
    
    # Show available parsers
    for os_type, parsers in parser_mgr.available_parsers.items():
        logger.info(f"Available parsers for {os_type}:")
        for command, parser in parsers.items():
            logger.info(f"  {command} -> {parser}")

if __name__ == "__main__":
    demonstrate_pyats_workflow()
    
    print("\n=== PYATS COMMANDS TO REMEMBER ===")
    print("1. Install pyATS: pip install pyats[full]")
    print("2. Run job: pyats run job job.py --testbed-file testbed.yaml")
    print("3. View logs: pyats logs view")
    print("4. Create testbed: pyats create testbed")
    print("5. Learn device: genie learn interface --testbed testbed.yaml --devices device_name")
    print("6. Parse command: genie parse 'show version' --testbed testbed.yaml --devices device_name")
    print("7. Compare snapshots: genie diff before.json after.json")
    print("8. Generate test: pyats create testscript")
