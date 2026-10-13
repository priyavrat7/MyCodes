#!/usr/bin/env python3
"""
Python Test Automation Frameworks - Cisco Interview Prep
Topics: pytest, unittest, test fixtures, mocking, parameterized tests
"""

import unittest # unittest is a testing framework for Python
import pytest # pytest is a testing framework for Python
import json # json is a way to parse JSON data
import time # time is a way to measure the time it takes to run a function
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass # dataclasses are a way to define classes with automatically generated special methods
from typing import List, Dict, Any # typing is a way to specify the type of variables in a function
import logging # logging is a way to log messages to a file or console
import paramiko

# Configure logging for test automation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 1. DATA CLASSES FOR TEST DATA
@dataclass
class NetworkDevice:
    """Network device data class"""
    hostname: str
    ip_address: str
    device_type: str
    model: str
    version: str
    interfaces: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.interfaces is None:
            self.interfaces = []

@dataclass
class TestResult:
    """Test result data class"""
    test_name: str
    status: str  # PASS, FAIL, SKIP
    duration: float
    error_message: str = None
    device: str = None

# 2. TEST BASE CLASS (For inheritance)
class NetworkTestBase:
    """Base class for network tests"""
    
    def __init__(self):
        self.devices = []
        self.test_results = []
        self.start_time = None
    
    def setup_test_environment(self):
        """Setup test environment"""
        logger.info("Setting up test environment")
        self.start_time = time.time()
    
    def teardown_test_environment(self):
        """Cleanup test environment"""
        logger.info("Tearing down test environment")
        duration = time.time() - self.start_time if self.start_time else 0
        logger.info(f"Total test duration: {duration:.2f} seconds")
    
    def add_device(self, device: NetworkDevice):
        """Add device to test environment"""
        self.devices.append(device)
        logger.info(f"Added device: {device.hostname}")
    
    def record_test_result(self, result: TestResult):
        """Record test result"""
        self.test_results.append(result)
        logger.info(f"Test {result.test_name}: {result.status}")

# 3. UNITTEST FRAMEWORK EXAMPLES
class TestNetworkConnectivity(unittest.TestCase):
    """Network connectivity tests using unittest"""
    
    def setUp(self):
        """Setup before each test"""
        self.device = NetworkDevice(
            hostname="test-switch-01",
            ip_address="192.168.1.100",
            device_type="switch",
            model="Catalyst 9300",
            version="16.12.05"
        )
        self.mock_connection = Mock()
    
    def tearDown(self):
        """Cleanup after each test"""
        if hasattr(self, 'mock_connection'):
            self.mock_connection.disconnect()
    
    def test_device_ping(self):
        """Test device ping connectivity"""
        # Mock the ping response
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            # Simulate ping test
            result = self._ping_device(self.device.ip_address)
            self.assertTrue(result, f"Ping to {self.device.ip_address} should succeed")
    
    def test_ssh_connection(self):
        """Test SSH connection to device"""
        with patch('paramiko.SSHClient') as mock_ssh:
            mock_client = Mock()
            mock_ssh.return_value = mock_client
            mock_client.connect.return_value = None
            
            # Test connection
            result = self._ssh_connect(self.device.ip_address, 'admin', 'password')
            self.assertTrue(result, "SSH connection should succeed")
            mock_client.connect.assert_called_once()
    
    def test_interface_status(self):
        """Test interface status check"""
        # Mock device response
        mock_response = {
            'GigabitEthernet0/1': {'status': 'up', 'speed': '1000'},
            'GigabitEthernet0/2': {'status': 'down', 'speed': '1000'}
        }
        
        with patch.object(self, '_get_interface_status', return_value=mock_response):
            interfaces = self._get_interface_status(self.device)
            
            self.assertIn('GigabitEthernet0/1', interfaces)
            self.assertEqual(interfaces['GigabitEthernet0/1']['status'], 'up')
            self.assertEqual(interfaces['GigabitEthernet0/2']['status'], 'down')
    
    def test_vlan_configuration(self):
        """Test VLAN configuration"""
        expected_vlans = [10, 20, 30, 100]
        
        with patch.object(self, '_get_vlans', return_value=expected_vlans):
            vlans = self._get_vlans(self.device)
            
            self.assertEqual(len(vlans), 4)
            self.assertIn(10, vlans)
            self.assertIn(100, vlans)
    
    # Helper methods (would normally interact with real devices)
    def _ping_device(self, ip_address):
        """Simulate ping to device"""
        import subprocess
        try:
            result = subprocess.run(['ping', '-c', '1', ip_address], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
    
    def _ssh_connect(self, ip_address, username, password):
        """Simulate SSH connection"""
        # In real implementation, would use paramiko or netmiko
        return True
    
    def _get_interface_status(self, device):
        """Get interface status from device"""
        # Mock implementation
        return {}
    
    def _get_vlans(self, device):
        """Get VLANs from device"""
        # Mock implementation
        return []

# 4. PYTEST FRAMEWORK EXAMPLES
class TestNetworkProtocols:
    """Network protocol tests using pytest"""
    
    @pytest.fixture
    def network_device(self):
        """Pytest fixture for network device"""
        return NetworkDevice(
            hostname="pytest-switch-01",
            ip_address="192.168.1.101",
            device_type="switch",
            model="Catalyst 9300",
            version="16.12.05"
        )
    
    @pytest.fixture
    def mock_device_connection(self):
        """Mock device connection fixture"""
        connection = Mock()
        connection.is_connected = True
        connection.send_command = Mock()
        yield connection
        connection.disconnect()
    
    def test_ospf_neighbors(self, network_device, mock_device_connection):
        """Test OSPF neighbor discovery"""
        # Mock OSPF neighbor output
        mock_output = """
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.1.1.1          1   FULL/BDR        00:00:35    192.168.1.2     GigabitEthernet0/1
10.1.1.2          1   FULL/DR         00:00:38    192.168.1.3     GigabitEthernet0/2
"""
        mock_device_connection.send_command.return_value = mock_output
        
        neighbors = self._parse_ospf_neighbors(mock_output)
        
        assert len(neighbors) == 2
        assert neighbors[0]['neighbor_id'] == '10.1.1.1'
        assert neighbors[0]['state'] == 'FULL/BDR'
        assert neighbors[1]['neighbor_id'] == '10.1.1.2'
        assert neighbors[1]['state'] == 'FULL/DR'
    
    @pytest.mark.parametrize("vlan_id,expected_status", [
        (10, "active"),
        (20, "active"), 
        (999, "not_found"),
        (0, "invalid")
    ])
    def test_vlan_status(self, vlan_id, expected_status, mock_device_connection):
        """Parameterized test for VLAN status"""
        # Mock VLAN status based on VLAN ID
        if vlan_id in [10, 20]:
            mock_device_connection.send_command.return_value = f"VLAN {vlan_id} is active"
            status = "active"
        elif vlan_id == 999:
            mock_device_connection.send_command.return_value = "VLAN not found"
            status = "not_found"
        else:
            status = "invalid"
        
        assert status == expected_status
    
    @pytest.mark.slow
    def test_network_convergence(self, network_device):
        """Test network convergence (marked as slow test)"""
        # Simulate network convergence test
        convergence_time = self._measure_convergence_time()
        
        # Assert convergence happens within acceptable time
        assert convergence_time < 30.0, f"Convergence took {convergence_time}s, expected < 30s"
    
    def test_bandwidth_utilization(self, mock_device_connection):
        """Test bandwidth utilization monitoring"""
        # Mock interface statistics
        mock_stats = {
            'GigabitEthernet0/1': {'rx_bytes': 1000000, 'tx_bytes': 800000, 'utilization': 45.2},
            'GigabitEthernet0/2': {'rx_bytes': 2000000, 'tx_bytes': 1500000, 'utilization': 78.5}
        }
        
        high_util_interfaces = [
            name for name, stats in mock_stats.items() 
            if stats['utilization'] > 70
        ]
        
        assert len(high_util_interfaces) == 1
        assert 'GigabitEthernet0/2' in high_util_interfaces
    
    # Helper methods
    def _parse_ospf_neighbors(self, output):
        """Parse OSPF neighbor output"""
        neighbors = []
        lines = output.strip().split('\n')[1:]  # Skip header
        
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 6:
                    neighbors.append({
                        'neighbor_id': parts[0],
                        'priority': parts[1],
                        'state': parts[2],
                        'dead_time': parts[3],
                        'address': parts[4],
                        'interface': parts[5]
                    })
        
        return neighbors
    
    def _measure_convergence_time(self):
        """Simulate measuring network convergence time"""
        import random
        return random.uniform(15.0, 35.0)  # Random convergence time

# 5. CUSTOM TEST RUNNER
class NetworkTestRunner:
    """Custom test runner for network automation"""
    
    def __init__(self):
        self.test_suite = unittest.TestSuite()
        self.results = []
    
    def add_test_class(self, test_class):
        """Add test class to suite"""
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        self.test_suite.addTests(tests)
    
    def run_tests(self, verbose=True):
        """Run all tests in suite"""
        runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
        result = runner.run(self.test_suite)
        
        # Process results
        test_summary = {
            'total_tests': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'success_rate': ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
        }
        
        return test_summary

# 6. TEST DATA GENERATORS
class TestDataGenerator:
    """Generate test data for network tests"""
    
    @staticmethod
    def generate_network_devices(count=5):
        """Generate sample network devices"""
        devices = []
        device_types = ['switch', 'router', 'firewall', 'access_point']
        models = ['Catalyst 9300', 'ISR 4000', 'ASA 5500', 'Aironet 3800']
        
        for i in range(count):
            device = NetworkDevice(
                hostname=f"device-{i+1:02d}",
                ip_address=f"192.168.1.{100+i}",
                device_type=device_types[i % len(device_types)],
                model=models[i % len(models)],
                version=f"16.12.0{i % 9 + 1}"
            )
            devices.append(device)
        
        return devices
    
    @staticmethod
    def generate_interface_data(device_count=3, interfaces_per_device=4):
        """Generate interface test data"""
        interface_data = {}
        
        for device_id in range(1, device_count + 1):
            device_name = f"switch-{device_id:02d}"
            interface_data[device_name] = []
            
            for int_id in range(1, interfaces_per_device + 1):
                interface = {
                    'name': f'GigabitEthernet0/{int_id}',
                    'status': 'up' if int_id % 3 != 0 else 'down',
                    'speed': '1000',
                    'duplex': 'full',
                    'vlan': 10 + (int_id * 10)
                }
                interface_data[device_name].append(interface)
        
        return interface_data

# MAIN EXECUTION AND EXAMPLES
if __name__ == "__main__":
    print("=== CISCO PYTHON INTERVIEW PREP - TEST AUTOMATION ===\n")
    
    # 1. Run unittest examples
    print("1. UNITTEST FRAMEWORK:")
    test_runner = NetworkTestRunner()
    test_runner.add_test_class(TestNetworkConnectivity)
    summary = test_runner.run_tests(verbose=False)
    print(f"Test Summary: {summary}\n")
    
    # 2. Generate test data
    print("2. TEST DATA GENERATION:")
    generator = TestDataGenerator()
    devices = generator.generate_network_devices(3)
    
    for device in devices:
        print(f"  {device.hostname}: {device.ip_address} ({device.device_type})")
    
    interface_data = generator.generate_interface_data(2, 3)
    print(f"\nGenerated interface data for {len(interface_data)} devices")
    
    # 3. Custom test execution
    print("\n3. CUSTOM TEST EXECUTION:")
    base_test = NetworkTestBase()
    base_test.setup_test_environment()
    
    for device in devices:
        base_test.add_device(device)
    
    # Simulate some test results
    test_results = [
        TestResult("ping_test", "PASS", 1.2, device="device-01"),
        TestResult("ssh_test", "PASS", 2.5, device="device-01"),
        TestResult("interface_test", "FAIL", 0.8, "Interface down", "device-02"),
        TestResult("vlan_test", "PASS", 1.1, device="device-03")
    ]
    
    for result in test_results:
        base_test.record_test_result(result)
    
    base_test.teardown_test_environment()
    
    # Print final summary
    passed = sum(1 for r in test_results if r.status == "PASS")
    failed = sum(1 for r in test_results if r.status == "FAIL")
    print(f"\nFinal Results: {passed} passed, {failed} failed")
    
    print("\n=== To run pytest tests, use: ===")
    print("pytest 03_test_automation.py -v")
    print("pytest 03_test_automation.py -m slow  # Run only slow tests")
    print("pytest 03_test_automation.py --tb=short  # Short traceback format")
