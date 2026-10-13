#!/usr/bin/env python3
"""
Network Protocols and Concepts - Cisco Interview Prep
Topics: TCP/IP, VLAN, Layer 2/3, OSPF, BGP, MPLS, SDN, QoS
"""

import ipaddress
import struct
import socket
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from enum import Enum
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. LAYER 2 CONCEPTS
class VLANManager:
    """VLAN management and operations"""
    
    def __init__(self):
        self.vlans = {}
        self.vlan_interfaces = {}
    
    def create_vlan(self, vlan_id: int, name: str, description: str = ""):
        """Create a new VLAN"""
        if not (1 <= vlan_id <= 4094):
            raise ValueError("VLAN ID must be between 1 and 4094")
        
        if vlan_id in self.vlans:
            raise ValueError(f"VLAN {vlan_id} already exists")
        
        self.vlans[vlan_id] = {
            'id': vlan_id,
            'name': name,
            'description': description,
            'status': 'active',
            'interfaces': []
        }
        
        logger.info(f"Created VLAN {vlan_id}: {name}")
        return self.vlans[vlan_id]
    
    def assign_interface_to_vlan(self, interface: str, vlan_id: int, mode: str = 'access'):
        """Assign interface to VLAN"""
        if vlan_id not in self.vlans:
            raise ValueError(f"VLAN {vlan_id} does not exist")
        
        if mode not in ['access', 'trunk']:
            raise ValueError("Mode must be 'access' or 'trunk'")
        
        self.vlan_interfaces[interface] = {
            'vlan_id': vlan_id,
            'mode': mode,
            'native_vlan': vlan_id if mode == 'trunk' else None
        }
        
        self.vlans[vlan_id]['interfaces'].append(interface)
        logger.info(f"Assigned {interface} to VLAN {vlan_id} in {mode} mode")
    
    def get_vlan_info(self, vlan_id: int) -> Dict:
        """Get VLAN information"""
        return self.vlans.get(vlan_id, {})
    
    def list_vlans(self) -> Dict:
        """List all VLANs"""
        return self.vlans

class SpanningTreeProtocol:
    """Spanning Tree Protocol simulation"""
    
    def __init__(self, bridge_id: str):
        self.bridge_id = bridge_id
        self.root_bridge = bridge_id
        self.port_states = {}
        self.port_costs = {}
    
    def set_port_state(self, port: str, state: str):
        """Set port state (blocking, listening, learning, forwarding)"""
        valid_states = ['blocking', 'listening', 'learning', 'forwarding', 'disabled']
        if state not in valid_states:
            raise ValueError(f"Invalid state. Must be one of: {valid_states}")
        
        self.port_states[port] = state
        logger.info(f"Port {port} state set to {state}")
    
    def calculate_root_bridge(self, bridge_priorities: Dict[str, int]):
        """Calculate root bridge based on priorities"""
        self.root_bridge = min(bridge_priorities.keys(), 
                              key=lambda x: bridge_priorities[x])
        logger.info(f"Root bridge: {self.root_bridge}")
        return self.root_bridge
    
    def get_port_states(self) -> Dict:
        """Get all port states"""
        return self.port_states

# 2. LAYER 3 CONCEPTS
class IPRoutingTable:
    """IP Routing table management"""
    
    def __init__(self):
        self.routes = []
        self.interfaces = {}
    
    def add_route(self, destination: str, next_hop: str, interface: str, 
                  metric: int = 1, protocol: str = 'static'):
        """Add route to routing table"""
        try:
            dest_network = ipaddress.ip_network(destination, strict=False)
            next_hop_ip = ipaddress.ip_address(next_hop) if next_hop != '0.0.0.0' else None
            
            route = {
                'destination': str(dest_network),
                'next_hop': str(next_hop_ip) if next_hop_ip else 'directly_connected',
                'interface': interface,
                'metric': metric,
                'protocol': protocol,
                'administrative_distance': self._get_admin_distance(protocol)
            }
            
            self.routes.append(route)
            logger.info(f"Added route: {destination} via {next_hop} ({protocol})")
            return route
            
        except ValueError as e:
            logger.error(f"Invalid route parameters: {e}")
            return None
    
    def lookup_route(self, destination_ip: str):
        """Perform longest prefix match for destination"""
        try:
            dest_ip = ipaddress.ip_address(destination_ip)
            best_match = None
            longest_prefix = -1
            
            for route in self.routes:
                network = ipaddress.ip_network(route['destination'])
                if dest_ip in network:
                    if network.prefixlen > longest_prefix:
                        longest_prefix = network.prefixlen
                        best_match = route
            
            return best_match
            
        except ValueError as e:
            logger.error(f"Invalid destination IP: {e}")
            return None
    
    def _get_admin_distance(self, protocol: str) -> int:
        """Get administrative distance for routing protocol"""
        distances = {
            'directly_connected': 0,
            'static': 1,
            'eigrp': 90,
            'ospf': 110,
            'rip': 120,
            'external_eigrp': 170,
            'ibgp': 200,
            'ebgp': 20
        }
        return distances.get(protocol, 255)
    
    def show_routing_table(self):
        """Display routing table"""
        logger.info("=== ROUTING TABLE ===")
        for route in sorted(self.routes, key=lambda x: x['administrative_distance']):
            logger.info(f"{route['destination']} via {route['next_hop']} "
                       f"[{route['administrative_distance']}/{route['metric']}] "
                       f"({route['protocol']})")

# 3. OSPF PROTOCOL SIMULATION
@dataclass
class OSPFNeighbor:
    """OSPF Neighbor information"""
    router_id: str
    ip_address: str
    interface: str
    state: str
    priority: int
    dead_time: int
    area: str

class OSPFProtocol:
    """OSPF Protocol simulation"""
    
    def __init__(self, router_id: str, area: str = "0.0.0.0"):
        self.router_id = router_id
        self.area = area
        self.neighbors = {}
        self.lsa_database = {}
        self.interfaces = {}
    
    def add_neighbor(self, neighbor: OSPFNeighbor):
        """Add OSPF neighbor"""
        self.neighbors[neighbor.router_id] = neighbor
        logger.info(f"Added OSPF neighbor: {neighbor.router_id} ({neighbor.state})")
    
    def update_neighbor_state(self, router_id: str, new_state: str):
        """Update neighbor state"""
        if router_id in self.neighbors:
            old_state = self.neighbors[router_id].state
            self.neighbors[router_id].state = new_state
            logger.info(f"Neighbor {router_id} state: {old_state} -> {new_state}")
    
    def calculate_shortest_path(self, destination: str):
        """Simulate SPF calculation (simplified)"""
        # In real OSPF, this would be Dijkstra's algorithm
        logger.info(f"Calculating shortest path to {destination}")
        
        # Mock SPF calculation
        path_cost = 10  # Simplified cost
        next_hop = list(self.neighbors.keys())[0] if self.neighbors else None
        
        return {
            'destination': destination,
            'cost': path_cost,
            'next_hop': next_hop,
            'path_type': 'intra-area'
        }
    
    def show_neighbors(self):
        """Display OSPF neighbors"""
        logger.info("=== OSPF NEIGHBORS ===")
        for router_id, neighbor in self.neighbors.items():
            logger.info(f"{router_id:<15} {neighbor.state:<10} {neighbor.interface}")

# 4. BGP PROTOCOL SIMULATION
@dataclass
class BGPPeer:
    """BGP Peer information"""
    peer_ip: str
    peer_as: int
    state: str
    local_as: int
    peer_type: str  # iBGP or eBGP

class BGPProtocol:
    """BGP Protocol simulation"""
    
    def __init__(self, local_as: int, router_id: str):
        self.local_as = local_as
        self.router_id = router_id
        self.peers = {}
        self.rib_in = {}  # Routing Information Base - Input
        self.rib_out = {}  # Routing Information Base - Output
        self.best_paths = {}
    
    def add_peer(self, peer: BGPPeer):
        """Add BGP peer"""
        self.peers[peer.peer_ip] = peer
        logger.info(f"Added BGP peer: {peer.peer_ip} (AS{peer.peer_as})")
    
    def advertise_network(self, network: str, next_hop: str, as_path: List[int]):
        """Advertise network to BGP peers"""
        advertisement = {
            'network': network,
            'next_hop': next_hop,
            'as_path': as_path,
            'local_pref': 100,
            'med': 0,
            'origin': 'IGP'
        }
        
        for peer_ip, peer in self.peers.items():
            if peer.state == 'Established':
                if peer_ip not in self.rib_out:
                    self.rib_out[peer_ip] = []
                self.rib_out[peer_ip].append(advertisement)
        
        logger.info(f"Advertised network {network} to BGP peers")
    
    def best_path_selection(self, network: str):
        """BGP best path selection algorithm"""
        candidates = []
        
        # Collect all paths for the network
        for peer_ip, routes in self.rib_in.items():
            for route in routes:
                if route['network'] == network:
                    candidates.append((peer_ip, route))
        
        if not candidates:
            return None
        
        # Simplified best path selection (normally much more complex)
        # 1. Highest local preference
        # 2. Shortest AS path
        # 3. Lowest MED
        # 4. eBGP over iBGP
        
        best_path = min(candidates, key=lambda x: (
            -x[1].get('local_pref', 100),  # Higher is better
            len(x[1].get('as_path', [])),   # Shorter is better
            x[1].get('med', 0)              # Lower is better
        ))
        
        self.best_paths[network] = best_path
        logger.info(f"Selected best path for {network}: via {best_path[0]}")
        return best_path

# 5. QUALITY OF SERVICE (QoS)
class QoSManager:
    """Quality of Service management"""
    
    def __init__(self):
        self.class_maps = {}
        self.policy_maps = {}
        self.service_policies = {}
    
    def create_class_map(self, name: str, match_criteria: Dict):
        """Create traffic class map"""
        self.class_maps[name] = {
            'name': name,
            'match_criteria': match_criteria
        }
        logger.info(f"Created class-map: {name}")
    
    def create_policy_map(self, name: str, classes: Dict):
        """Create policy map with QoS actions"""
        self.policy_maps[name] = {
            'name': name,
            'classes': classes
        }
        logger.info(f"Created policy-map: {name}")
    
    def apply_service_policy(self, interface: str, policy_name: str, direction: str):
        """Apply service policy to interface"""
        if policy_name not in self.policy_maps:
            raise ValueError(f"Policy map {policy_name} does not exist")
        
        if direction not in ['input', 'output']:
            raise ValueError("Direction must be 'input' or 'output'")
        
        self.service_policies[interface] = {
            'policy': policy_name,
            'direction': direction
        }
        logger.info(f"Applied policy {policy_name} to {interface} ({direction})")
    
    def classify_traffic(self, packet_info: Dict) -> str:
        """Classify traffic based on packet information"""
        # Simplified traffic classification
        dscp = packet_info.get('dscp', 0)
        src_port = packet_info.get('src_port', 0)
        dst_port = packet_info.get('dst_port', 0)
        protocol = packet_info.get('protocol', 'tcp')
        
        # Classification logic
        if dscp >= 46:  # EF (Expedited Forwarding)
            return 'voice'
        elif dscp >= 34:  # AF4x (Assured Forwarding)
            return 'video'
        elif dst_port in [80, 443, 8080]:
            return 'web'
        elif protocol == 'tcp' and dst_port == 22:
            return 'management'
        else:
            return 'best-effort'

# 6. SOFTWARE DEFINED NETWORKING (SDN)
class SDNController:
    """Simple SDN Controller simulation"""
    
    def __init__(self, controller_id: str):
        self.controller_id = controller_id
        self.switches = {}
        self.flow_tables = {}
        self.topology = {'nodes': [], 'links': []}
    
    def register_switch(self, switch_id: str, switch_info: Dict):
        """Register switch with controller"""
        self.switches[switch_id] = switch_info
        self.topology['nodes'].append(switch_id)
        logger.info(f"Registered switch: {switch_id}")
    
    def install_flow(self, switch_id: str, flow_rule: Dict):
        """Install flow rule on switch"""
        if switch_id not in self.switches:
            raise ValueError(f"Switch {switch_id} not registered")
        
        if switch_id not in self.flow_tables:
            self.flow_tables[switch_id] = []
        
        flow_rule['priority'] = flow_rule.get('priority', 100)
        flow_rule['idle_timeout'] = flow_rule.get('idle_timeout', 0)
        
        self.flow_tables[switch_id].append(flow_rule)
        logger.info(f"Installed flow rule on {switch_id}: {flow_rule}")
    
    def calculate_path(self, src_switch: str, dst_switch: str):
        """Calculate path between switches"""
        # Simplified path calculation
        if src_switch == dst_switch:
            return [src_switch]
        
        # In real SDN, this would use graph algorithms
        path = [src_switch, dst_switch]  # Direct path for simplicity
        logger.info(f"Calculated path: {' -> '.join(path)}")
        return path
    
    def get_network_view(self):
        """Get global network view"""
        return {
            'controller': self.controller_id,
            'switches': len(self.switches),
            'total_flows': sum(len(flows) for flows in self.flow_tables.values()),
            'topology': self.topology
        }

# DEMONSTRATION FUNCTIONS
def demonstrate_layer2_concepts():
    """Demonstrate Layer 2 concepts"""
    logger.info("=== LAYER 2 CONCEPTS ===")
    
    # VLAN Management
    vlan_mgr = VLANManager()
    vlan_mgr.create_vlan(10, "Production", "Production VLAN")
    vlan_mgr.create_vlan(20, "Development", "Development VLAN")
    vlan_mgr.assign_interface_to_vlan("GigE0/1", 10, "access")
    vlan_mgr.assign_interface_to_vlan("GigE0/2", 20, "access")
    
    # Spanning Tree
    stp = SpanningTreeProtocol("0001.0001.0001")
    stp.set_port_state("GigE0/1", "forwarding")
    stp.set_port_state("GigE0/2", "blocking")
    
    bridge_priorities = {
        "0001.0001.0001": 32768,
        "0002.0002.0002": 4096,
        "0003.0003.0003": 8192
    }
    stp.calculate_root_bridge(bridge_priorities)

def demonstrate_layer3_concepts():
    """Demonstrate Layer 3 concepts"""
    logger.info("\n=== LAYER 3 CONCEPTS ===")
    
    # Routing Table
    routing_table = IPRoutingTable()
    routing_table.add_route("0.0.0.0/0", "192.168.1.1", "GigE0/0", protocol="static")
    routing_table.add_route("10.1.1.0/24", "0.0.0.0", "GigE0/1", protocol="directly_connected")
    routing_table.add_route("10.2.2.0/24", "10.1.1.2", "GigE0/1", protocol="ospf")
    
    # Route lookup
    route = routing_table.lookup_route("10.2.2.100")
    if route:
        logger.info(f"Route lookup for 10.2.2.100: {route}")
    
    routing_table.show_routing_table()

def demonstrate_routing_protocols():
    """Demonstrate routing protocols"""
    logger.info("\n=== ROUTING PROTOCOLS ===")
    
    # OSPF
    ospf = OSPFProtocol("1.1.1.1", "0.0.0.0")
    neighbor1 = OSPFNeighbor("2.2.2.2", "192.168.1.2", "GigE0/1", "Full", 1, 40, "0.0.0.0")
    neighbor2 = OSPFNeighbor("3.3.3.3", "192.168.1.3", "GigE0/2", "2-Way", 1, 35, "0.0.0.0")
    
    ospf.add_neighbor(neighbor1)
    ospf.add_neighbor(neighbor2)
    ospf.show_neighbors()
    
    # BGP
    bgp = BGPProtocol(65001, "1.1.1.1")
    peer1 = BGPPeer("192.168.1.2", 65002, "Established", 65001, "eBGP")
    peer2 = BGPPeer("10.1.1.2", 65001, "Established", 65001, "iBGP")
    
    bgp.add_peer(peer1)
    bgp.add_peer(peer2)
    bgp.advertise_network("10.1.1.0/24", "192.168.1.1", [65001])

def demonstrate_qos_and_sdn():
    """Demonstrate QoS and SDN concepts"""
    logger.info("\n=== QoS AND SDN ===")
    
    # QoS
    qos = QoSManager()
    qos.create_class_map("VOICE", {"match": "dscp ef"})
    qos.create_class_map("VIDEO", {"match": "dscp af41"})
    qos.create_policy_map("WAN_POLICY", {
        "VOICE": {"priority": "256k"},
        "VIDEO": {"bandwidth": "512k"}
    })
    qos.apply_service_policy("GigE0/0", "WAN_POLICY", "output")
    
    # Traffic classification
    packet = {"dscp": 46, "src_port": 5060, "dst_port": 5060, "protocol": "udp"}
    traffic_class = qos.classify_traffic(packet)
    logger.info(f"Traffic classified as: {traffic_class}")
    
    # SDN
    controller = SDNController("controller-1")
    controller.register_switch("switch-1", {"dpid": "0x1", "ports": 24})
    controller.register_switch("switch-2", {"dpid": "0x2", "ports": 48})
    
    flow_rule = {
        "match": {"in_port": 1, "eth_dst": "aa:bb:cc:dd:ee:ff"},
        "actions": [{"output": 2}],
        "priority": 100
    }
    controller.install_flow("switch-1", flow_rule)
    
    network_view = controller.get_network_view()
    logger.info(f"Network view: {network_view}")

# MAIN EXECUTION
if __name__ == "__main__":
    logger.info("=== CISCO PYTHON INTERVIEW PREP - NETWORK PROTOCOLS ===\n")
    
    demonstrate_layer2_concepts()
    demonstrate_layer3_concepts()
    demonstrate_routing_protocols()
    demonstrate_qos_and_sdn()
    
    logger.info("\n=== KEY NETWORKING CONCEPTS TO REMEMBER ===")
    concepts = [
        "OSI 7-layer model and TCP/IP 4-layer model",
        "VLAN tagging (802.1Q) and trunking",
        "Spanning Tree Protocol (STP, RSTP, MST)",
        "IP addressing and subnetting (VLSM, CIDR)",
        "Routing protocols: OSPF, EIGRP, BGP",
        "Quality of Service (QoS): classification, marking, queuing",
        "MPLS and traffic engineering",
        "Software Defined Networking (SDN) and OpenFlow",
        "Network virtualization (VRF, VXLAN)",
        "Security protocols (IPSec, SSL/TLS)"
    ]
    
    for i, concept in enumerate(concepts, 1):
        logger.info(f"{i:2d}. {concept}")
