#!/usr/bin/env python3
"""
OSPF on Switches - Specialized Testing Module for Cisco Interview
Focus: Testing OSPF implementation on Cisco Catalyst switches
"""

import re
import json
import time
import ipaddress
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. OSPF STATES AND TYPES FOR SWITCHES
class OSPFState(Enum):
    """OSPF Neighbor States"""
    DOWN = "Down"
    ATTEMPT = "Attempt"
    INIT = "Init"
    TWO_WAY = "2-Way"
    EXSTART = "ExStart"
    EXCHANGE = "Exchange"
    LOADING = "Loading"
    FULL = "Full"

class OSPFNetworkType(Enum):
    """OSPF Network Types on Switch Interfaces"""
    BROADCAST = "broadcast"
    POINT_TO_POINT = "point-to-point"
    POINT_TO_MULTIPOINT = "point-to-multipoint"
    NBMA = "nbma"

class OSPFLSAType(Enum):
    """OSPF LSA Types relevant to switches"""
    ROUTER_LSA = 1          # Type 1 - Router LSA
    NETWORK_LSA = 2         # Type 2 - Network LSA (DR generates)
    SUMMARY_LSA = 3         # Type 3 - Summary LSA
    ASBR_SUMMARY_LSA = 4    # Type 4 - ASBR Summary LSA
    EXTERNAL_LSA = 5        # Type 5 - External LSA

# 2. DATA STRUCTURES FOR OSPF TESTING
@dataclass
class OSPFNeighbor:
    """OSPF Neighbor information for switch testing"""
    neighbor_id: str
    priority: int
    state: OSPFState
    dead_time: int
    address: str
    interface: str
    dr: str = "0.0.0.0"
    bdr: str = "0.0.0.0"
    area: str = "0.0.0.0"

@dataclass
class OSPFInterface:
    """OSPF Interface configuration on switch"""
    name: str
    ip_address: str
    area: str
    network_type: OSPFNetworkType
    hello_interval: int = 10
    dead_interval: int = 40
    priority: int = 1
    cost: int = 1
    state: str = "DR"
    neighbors: List[OSPFNeighbor] = None
    
    def __post_init__(self):
        if self.neighbors is None:
            self.neighbors = []

@dataclass
class OSPFArea:
    """OSPF Area information"""
    area_id: str
    area_type: str = "normal"  # normal, stub, nssa, totally-stub
    interfaces: List[str] = None
    lsa_count: int = 0
    
    def __post_init__(self):
        if self.interfaces is None:
            self.interfaces = []

# 3. OSPF SWITCH TESTING CLASS
class OSPFSwitchTester:
    """Comprehensive OSPF testing for Cisco switches"""
    
    def __init__(self, switch_hostname: str):
        self.switch_hostname = switch_hostname
        self.ospf_process_id = None
        self.router_id = None
        self.areas = {}
        self.interfaces = {}
        self.neighbors = {}
        self.lsdb = {}  # Link State Database
        
    def parse_ospf_neighbor_output(self, output: str) -> Dict[str, OSPFNeighbor]:
        """Parse 'show ip ospf neighbor' output from switch"""
        neighbors = {}
        
        # Sample output parsing
        lines = output.strip().split('\n')
        
        # Skip header lines
        data_started = False
        for line in lines:
            line = line.strip()
            
            if 'Neighbor ID' in line and 'Pri' in line:
                data_started = True
                continue
                
            if not data_started or not line:
                continue
            
            # Parse neighbor line
            # Format: Neighbor ID     Pri   State           Dead Time   Address         Interface
            parts = line.split()
            if len(parts) >= 6:
                neighbor = OSPFNeighbor(
                    neighbor_id=parts[0],
                    priority=int(parts[1]),
                    state=self._parse_ospf_state(parts[2]),
                    dead_time=self._parse_dead_time(parts[3]),
                    address=parts[4],
                    interface=parts[5]
                )
                neighbors[neighbor.neighbor_id] = neighbor
        
        return neighbors
    
    def parse_ospf_interface_output(self, output: str) -> Dict[str, OSPFInterface]:
        """Parse 'show ip ospf interface' output from switch"""
        interfaces = {}
        current_interface = None
        
        lines = output.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Interface header line
            if ' is up, line protocol is up' in line:
                interface_name = line.split(' is up')[0].strip()
                current_interface = interface_name
                interfaces[interface_name] = OSPFInterface(
                    name=interface_name,
                    ip_address="",
                    area="",
                    network_type=OSPFNetworkType.BROADCAST
                )
            
            elif current_interface and line:
                interface_obj = interfaces[current_interface]
                
                if line.startswith('Internet Address'):
                    # Extract IP address
                    ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+/\d+)', line)
                    if ip_match:
                        interface_obj.ip_address = ip_match.group(1)
                
                elif line.startswith('Area'):
                    # Extract area
                    area_match = re.search(r'Area (\d+\.\d+\.\d+\.\d+)', line)
                    if area_match:
                        interface_obj.area = area_match.group(1)
                
                elif 'Network Type' in line:
                    # Extract network type
                    if 'BROADCAST' in line.upper():
                        interface_obj.network_type = OSPFNetworkType.BROADCAST
                    elif 'POINT_TO_POINT' in line.upper():
                        interface_obj.network_type = OSPFNetworkType.POINT_TO_POINT
                
                elif 'Hello' in line and 'Dead' in line:
                    # Extract timers
                    hello_match = re.search(r'Hello (\d+)', line)
                    dead_match = re.search(r'Dead (\d+)', line)
                    if hello_match:
                        interface_obj.hello_interval = int(hello_match.group(1))
                    if dead_match:
                        interface_obj.dead_interval = int(dead_match.group(1))
        
        return interfaces
    
    def parse_ospf_database_output(self, output: str) -> Dict:
        """Parse 'show ip ospf database' output"""
        lsdb = {
            'router_lsas': [],
            'network_lsas': [],
            'summary_lsas': [],
            'external_lsas': []
        }
        
        current_section = None
        lines = output.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            if 'Router Link States' in line:
                current_section = 'router_lsas'
            elif 'Net Link States' in line:
                current_section = 'network_lsas'
            elif 'Summary Link States' in line:
                current_section = 'summary_lsas'
            elif 'Type-5 AS External Link States' in line:
                current_section = 'external_lsas'
            elif current_section and line and not line.startswith('Link ID'):
                # Parse LSA entry
                parts = line.split()
                if len(parts) >= 4:
                    lsa_entry = {
                        'link_id': parts[0],
                        'adv_router': parts[1],
                        'age': parts[2],
                        'seq': parts[3] if len(parts) > 3 else '',
                        'checksum': parts[4] if len(parts) > 4 else ''
                    }
                    lsdb[current_section].append(lsa_entry)
        
        return lsdb
    
    def _parse_ospf_state(self, state_str: str) -> OSPFState:
        """Parse OSPF state string to enum"""
        state_mapping = {
            'FULL/DR': OSPFState.FULL,
            'FULL/BDR': OSPFState.FULL,
            'FULL/DROTHER': OSPFState.FULL,
            'FULL': OSPFState.FULL,
            '2WAY/DROTHER': OSPFState.TWO_WAY,
            '2WAY': OSPFState.TWO_WAY,
            'INIT': OSPFState.INIT,
            'DOWN': OSPFState.DOWN
        }
        return state_mapping.get(state_str.upper(), OSPFState.DOWN)
    
    def _parse_dead_time(self, dead_time_str: str) -> int:
        """Parse dead time string to seconds"""
        # Format: 00:00:35
        if ':' in dead_time_str:
            parts = dead_time_str.split(':')
            if len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                return hours * 3600 + minutes * 60 + seconds
        return 0

# 4. OSPF TEST CASES FOR SWITCHES
class OSPFSwitchTestCases:
    """Specific test cases for OSPF on switches"""
    
    def __init__(self, tester: OSPFSwitchTester):
        self.tester = tester
        self.test_results = []
    
    def test_ospf_neighbor_adjacency(self, expected_neighbors: List[str]) -> bool:
        """Test OSPF neighbor adjacency formation"""
        logger.info("Testing OSPF neighbor adjacency...")
        
        # Mock neighbor output for testing
        neighbor_output = """
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.1.1.2          1   FULL/BDR        00:00:35    192.168.1.2     GigabitEthernet1/0/1
10.1.1.3          1   FULL/DROTHER    00:00:38    192.168.1.3     GigabitEthernet1/0/2
"""
        
        neighbors = self.tester.parse_ospf_neighbor_output(neighbor_output)
        
        # Check if all expected neighbors are present and in FULL state
        success = True
        for expected_neighbor in expected_neighbors:
            if expected_neighbor not in neighbors:
                logger.error(f"Expected neighbor {expected_neighbor} not found")
                success = False
            elif neighbors[expected_neighbor].state != OSPFState.FULL:
                logger.error(f"Neighbor {expected_neighbor} not in FULL state: {neighbors[expected_neighbor].state}")
                success = False
            else:
                logger.info(f"Neighbor {expected_neighbor}: {neighbors[expected_neighbor].state.value}")
        
        self.test_results.append({
            'test': 'ospf_neighbor_adjacency',
            'status': 'PASS' if success else 'FAIL',
            'details': f"Found {len(neighbors)} neighbors, expected {len(expected_neighbors)}"
        })
        
        return success
    
    def test_ospf_dr_bdr_election(self, interface: str, expected_dr: str, expected_bdr: str) -> bool:
        """Test OSPF DR/BDR election on switch interface"""
        logger.info(f"Testing DR/BDR election on {interface}...")
        
        # Mock interface output
        interface_output = f"""
{interface} is up, line protocol is up 
  Internet Address 192.168.1.1/24, Area 0.0.0.0, Attached via Network Statement
  Process ID 1, Router ID 10.1.1.1, Network Type BROADCAST, Cost: 1
  Topology-MTID    Cost    Disabled    Shutdown      Topology Name
        0           1         no          no            Base
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) {expected_dr}, Interface address 192.168.1.1
  Backup Designated router (ID) {expected_bdr}, Interface address 192.168.1.2
  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
"""
        
        # Parse and verify DR/BDR
        dr_match = re.search(r'Designated Router \(ID\) (\d+\.\d+\.\d+\.\d+)', interface_output)
        bdr_match = re.search(r'Backup Designated router \(ID\) (\d+\.\d+\.\d+\.\d+)', interface_output)
        
        success = True
        if dr_match and dr_match.group(1) == expected_dr:
            logger.info(f"DR election correct: {expected_dr}")
        else:
            logger.error(f"DR election incorrect. Expected: {expected_dr}, Found: {dr_match.group(1) if dr_match else 'None'}")
            success = False
        
        if bdr_match and bdr_match.group(1) == expected_bdr:
            logger.info(f"BDR election correct: {expected_bdr}")
        else:
            logger.error(f"BDR election incorrect. Expected: {expected_bdr}, Found: {bdr_match.group(1) if bdr_match else 'None'}")
            success = False
        
        self.test_results.append({
            'test': 'ospf_dr_bdr_election',
            'status': 'PASS' if success else 'FAIL',
            'interface': interface,
            'dr': dr_match.group(1) if dr_match else 'None',
            'bdr': bdr_match.group(1) if bdr_match else 'None'
        })
        
        return success
    
    def test_ospf_lsa_propagation(self, expected_lsa_types: List[OSPFLSAType]) -> bool:
        """Test OSPF LSA propagation and database synchronization"""
        logger.info("Testing OSPF LSA propagation...")
        
        # Mock LSDB output
        lsdb_output = """
            OSPF Router with ID (10.1.1.1) (Process ID 1)

                Router Link States (Area 0.0.0.0)

Link ID         ADV Router      Age         Seq#       Checksum
10.1.1.1        10.1.1.1        1234        0x80000001 0x1234
10.1.1.2        10.1.1.2        1235        0x80000002 0x1235

                Net Link States (Area 0.0.0.0)

Link ID         ADV Router      Age         Seq#       Checksum
192.168.1.1     10.1.1.1        1236        0x80000003 0x1236

                Summary Link States (Area 0.0.0.0)

Link ID         ADV Router      Age         Seq#       Checksum
10.2.2.0        10.1.1.1        1237        0x80000004 0x1237
"""
        
        lsdb = self.tester.parse_ospf_database_output(lsdb_output)
        
        success = True
        found_types = []
        
        if lsdb['router_lsas']:
            found_types.append(OSPFLSAType.ROUTER_LSA)
            logger.info(f"Found {len(lsdb['router_lsas'])} Router LSAs")
        
        if lsdb['network_lsas']:
            found_types.append(OSPFLSAType.NETWORK_LSA)
            logger.info(f"Found {len(lsdb['network_lsas'])} Network LSAs")
        
        if lsdb['summary_lsas']:
            found_types.append(OSPFLSAType.SUMMARY_LSA)
            logger.info(f"Found {len(lsdb['summary_lsas'])} Summary LSAs")
        
        # Check if all expected LSA types are present
        for expected_type in expected_lsa_types:
            if expected_type not in found_types:
                logger.error(f"Expected LSA type {expected_type.name} not found")
                success = False
        
        self.test_results.append({
            'test': 'ospf_lsa_propagation',
            'status': 'PASS' if success else 'FAIL',
            'found_lsa_types': [lsa_type.name for lsa_type in found_types],
            'expected_lsa_types': [lsa_type.name for lsa_type in expected_lsa_types]
        })
        
        return success
    
    def test_ospf_convergence_time(self, topology_change_event: str, max_convergence_time: int = 30) -> bool:
        """Test OSPF convergence time after topology change"""
        logger.info(f"Testing OSPF convergence after {topology_change_event}...")
        
        start_time = time.time()
        
        # Simulate topology change and convergence
        logger.info("Simulating topology change...")
        time.sleep(2)  # Simulate change detection time
        
        logger.info("Waiting for LSA flooding...")
        time.sleep(1)  # Simulate LSA flooding
        
        logger.info("Waiting for SPF calculation...")
        time.sleep(1)  # Simulate SPF calculation
        
        logger.info("Waiting for routing table update...")
        time.sleep(1)  # Simulate routing table update
        
        convergence_time = time.time() - start_time
        success = convergence_time <= max_convergence_time
        
        logger.info(f"Convergence completed in {convergence_time:.2f} seconds")
        
        if success:
            logger.info(f"Convergence time within acceptable limit ({max_convergence_time}s)")
        else:
            logger.error(f"Convergence time exceeded limit: {convergence_time:.2f}s > {max_convergence_time}s")
        
        self.test_results.append({
            'test': 'ospf_convergence_time',
            'status': 'PASS' if success else 'FAIL',
            'convergence_time': round(convergence_time, 2),
            'max_allowed_time': max_convergence_time,
            'event': topology_change_event
        })
        
        return success
    
    def test_ospf_area_configuration(self, expected_areas: Dict[str, str]) -> bool:
        """Test OSPF area configuration on switch"""
        logger.info("Testing OSPF area configuration...")
        
        # Mock area configuration
        configured_areas = {
            "0.0.0.0": "normal",
            "0.0.0.1": "stub",
            "0.0.0.2": "nssa"
        }
        '''
        Significance:
        This code snippet sets up a mock dictionary named `configured_areas`, which simulates the OSPF area configuration found on a switch during automated testing. The keys represent area IDs in dotted-decimal notation and the values specify the OSPF area type (e.g., "normal", "stub", "nssa"), which are important operational modes in OSPF deployments. This approach allows the test case to validate if the actual switch configuration matches expected area types, ensuring that OSPF is partitioned and configured as intended for correct routing protocol operations in enterprise or campus network topologies.
        # OSPF area types explanation:
        # "normal": A standard/default OSPF area with full LSA types; allows Type 5 external LSAs and full routing.
        # "stub": A stub area does not allow Type 5 external LSAs; reduces LSA flooding and uses a default route for destinations outside the area.
        # "nssa": "Not So Stubby Area" allows Type 7 LSAs (external routes redistributed into OSPF) but blocks Type 5 LSAs from the backbone; commonly used when redistributing external routes into a stub-like area.
        # These area types affect OSPF operation by limiting or allowing the propagation of external routing information, thus impacting scalability and security.
        '''
        
        success = True
        for area_id, area_type in expected_areas.items():
            if area_id not in configured_areas:
                logger.error(f"Expected area {area_id} not configured")
                success = False
            elif configured_areas[area_id] != area_type:
                logger.error(f"Area {area_id} type mismatch. Expected: {area_type}, Found: {configured_areas[area_id]}")
                success = False
            else:
                logger.info(f"Area {area_id} correctly configured as {area_type}")
        
        self.test_results.append({
            'test': 'ospf_area_configuration',
            'status': 'PASS' if success else 'FAIL',
            'configured_areas': configured_areas,
            'expected_areas': expected_areas
        })
        
        return success
    
    def get_test_summary(self) -> Dict:
        """Get comprehensive test summary"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['status'] == 'PASS')
        failed_tests = total_tests - passed_tests
        
        return {
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'detailed_results': self.test_results
        }

# 5. OSPF SWITCH TESTING SCENARIOS
class OSPFTestingScenarios:
    """Real-world OSPF testing scenarios for switches"""
    
    @staticmethod
    def campus_network_scenario():
        """Test OSPF in campus network with multiple switches"""
        logger.info("=== CAMPUS NETWORK OSPF TESTING SCENARIO ===")
        
        # Core switch testing
        core_switch = OSPFSwitchTester("core-sw-01")
        core_tests = OSPFSwitchTestCases(core_switch)
        
        # Test neighbor adjacencies
        expected_neighbors = ["10.1.1.2", "10.1.1.3", "10.1.1.4"]  # Access switches
        core_tests.test_ospf_neighbor_adjacency(expected_neighbors)
        
        # Test DR/BDR election
        core_tests.test_ospf_dr_bdr_election("GigabitEthernet1/0/1", "10.1.1.1", "10.1.1.2")
        
        # Test LSA propagation
        expected_lsas = [OSPFLSAType.ROUTER_LSA, OSPFLSAType.NETWORK_LSA, OSPFLSAType.SUMMARY_LSA]
        core_tests.test_ospf_lsa_propagation(expected_lsas)
        
        # Test convergence
        core_tests.test_ospf_convergence_time("Link failure on access switch", 15)
        
        return core_tests.get_test_summary()
    
    @staticmethod
    def multi_area_scenario():
        """Test OSPF multi-area configuration on switches"""
        logger.info("=== MULTI-AREA OSPF TESTING SCENARIO ===")
        
        abr_switch = OSPFSwitchTester("abr-sw-01")  # Area Border Router
        abr_tests = OSPFSwitchTestCases(abr_switch)
        
        # Test area configuration
        expected_areas = {
            "0.0.0.0": "normal",    # Backbone area
            "0.0.0.1": "normal",    # Area 1
            "0.0.0.2": "stub"       # Stub area
        }
        abr_tests.test_ospf_area_configuration(expected_areas)
        
        # Test inter-area LSA propagation
        expected_lsas = [OSPFLSAType.ROUTER_LSA, OSPFLSAType.NETWORK_LSA, OSPFLSAType.SUMMARY_LSA]
        abr_tests.test_ospf_lsa_propagation(expected_lsas)
        
        return abr_tests.get_test_summary()
    
    @staticmethod
    def redundancy_scenario():
        """Test OSPF redundancy and failover on switches"""
        logger.info("=== OSPF REDUNDANCY TESTING SCENARIO ===")
        
        redundant_switch = OSPFSwitchTester("redundant-sw-01")
        redundancy_tests = OSPFSwitchTestCases(redundant_switch)
        
        # Test primary path
        redundancy_tests.test_ospf_neighbor_adjacency(["10.1.1.2", "10.1.1.3"])
        
        # Test failover convergence
        redundancy_tests.test_ospf_convergence_time("Primary link failure", 10)
        
        # Test backup path establishment
        redundancy_tests.test_ospf_neighbor_adjacency(["10.1.1.3"])  # Only backup neighbor
        
        return redundancy_tests.get_test_summary()

# DEMONSTRATION AND MAIN EXECUTION
def demonstrate_ospf_switch_testing():
    """Demonstrate comprehensive OSPF switch testing"""
    logger.info("=== CISCO OSPF SWITCH TESTING DEMONSTRATION ===\n")
    
    # Run different testing scenarios
    campus_results = OSPFTestingScenarios.campus_network_scenario()
    logger.info(f"Campus Network Test Results: {campus_results['passed']}/{campus_results['total_tests']} passed")
    
    multi_area_results = OSPFTestingScenarios.multi_area_scenario()
    logger.info(f"Multi-Area Test Results: {multi_area_results['passed']}/{multi_area_results['total_tests']} passed")
    
    redundancy_results = OSPFTestingScenarios.redundancy_scenario()
    logger.info(f"Redundancy Test Results: {redundancy_results['passed']}/{redundancy_results['total_tests']} passed")
    
    # Overall summary
    total_tests = campus_results['total_tests'] + multi_area_results['total_tests'] + redundancy_results['total_tests']
    total_passed = campus_results['passed'] + multi_area_results['passed'] + redundancy_results['passed']
    
    logger.info(f"\n=== OVERALL OSPF TESTING SUMMARY ===")
    logger.info(f"Total Tests: {total_tests}")
    logger.info(f"Passed: {total_passed}")
    logger.info(f"Failed: {total_tests - total_passed}")
    logger.info(f"Success Rate: {(total_passed/total_tests*100):.1f}%")

if __name__ == "__main__":
    demonstrate_ospf_switch_testing()
    
    print("\n" + "="*70)
    print("OSPF ON SWITCHES - KEY TESTING AREAS FOR CISCO INTERVIEW")
    print("="*70)
    
    key_areas = [
        "1. OSPF Neighbor Adjacency Formation and Maintenance",
        "2. DR/BDR Election Process on Broadcast Networks",
        "3. LSA Types and Database Synchronization",
        "4. OSPF Convergence Time and Performance",
        "5. Multi-Area OSPF Configuration and Inter-Area Routing",
        "6. OSPF Authentication and Security",
        "7. OSPF Stub Areas and Route Summarization",
        "8. OSPF Load Balancing and Equal Cost Paths",
        "9. OSPF Troubleshooting and Debugging",
        "10. OSPF Integration with Other Protocols (BGP, EIGRP)"
    ]
    
    for area in key_areas:
        print(area)
    
    print("\n" + "="*70)
    print("CRITICAL OSPF COMMANDS TO KNOW FOR TESTING")
    print("="*70)
    
    commands = [
        "show ip ospf neighbor [detail]",
        "show ip ospf interface [brief]",
        "show ip ospf database",
        "show ip ospf database router",
        "show ip ospf database network",
        "show ip ospf database summary",
        "show ip ospf border-routers",
        "show ip route ospf",
        "debug ip ospf adj",
        "debug ip ospf lsa-generation",
        "debug ip ospf spf",
        "show ip ospf statistics"
    ]
    
    for cmd in commands:
        print(f"  {cmd}")
    
    print("\n" + "="*70)
    print("OSPF TESTING INTERVIEW QUESTIONS TO PREPARE")
    print("="*70)
    
    questions = [
        "1. How would you test OSPF neighbor adjacency formation?",
        "2. What factors affect DR/BDR election and how do you verify it?",
        "3. How do you validate OSPF LSA propagation across areas?",
        "4. What's your approach to testing OSPF convergence time?",
        "5. How would you test OSPF authentication mechanisms?",
        "6. How do you verify OSPF load balancing across equal cost paths?",
        "7. What's your strategy for testing OSPF in multi-area networks?",
        "8. How would you automate OSPF configuration compliance checking?",
        "9. How do you test OSPF behavior during network failures?",
        "10. What metrics do you use to validate OSPF performance?"
    ]
    
    for question in questions:
        print(question)
