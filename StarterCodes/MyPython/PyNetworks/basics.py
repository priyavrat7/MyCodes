#!/usr/bin/env python3
"""
OSPF Switch Testing - Quick Reference and Basics
Focused preparation for Cisco OSPF on Switches project
"""

# Quick OSPF concepts for interview
OSPF_NEIGHBOR_STATES = [
    "Down", "Attempt", "Init", "2-Way", 
    "ExStart", "Exchange", "Loading", "Full"
]

OSPF_LSA_TYPES = {
    1: "Router LSA",
    2: "Network LSA", 
    3: "Summary LSA",
    4: "ASBR Summary LSA",
    5: "External LSA"
}

# Key OSPF testing areas for switches
def ospf_testing_checklist():
    """Essential OSPF testing areas for Cisco switches"""
    return {
        "neighbor_adjacency": "Verify OSPF neighbors form correctly",
        "dr_bdr_election": "Test Designated Router election process",
        "lsa_propagation": "Validate Link State Advertisement flooding",
        "convergence_time": "Measure network convergence after changes",
        "area_configuration": "Verify multi-area OSPF setup",
        "authentication": "Test OSPF security mechanisms",
        "load_balancing": "Verify equal-cost path utilization"
    }

# Sample OSPF neighbor parsing (interview question)
def parse_ospf_neighbors(show_output):
    """Parse 'show ip ospf neighbor' output - common interview task"""
    neighbors = []
    lines = show_output.strip().split('\n')
    
    for line in lines[1:]:  # Skip header
        if line.strip():
            parts = line.split()
            if len(parts) >= 6:
                neighbor = {
                    'neighbor_id': parts[0],
                    'priority': int(parts[1]),
                    'state': parts[2],
                    'dead_time': parts[3],
                    'address': parts[4],
                    'interface': parts[5]
                }
                neighbors.append(neighbor)
    
    return neighbors

# OSPF testing automation example
def test_ospf_adjacency(expected_neighbors):
    """Test if OSPF neighbors are in expected state"""
    # This would connect to actual switch in real scenario
    mock_output = """
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.1.1.2          1   FULL/BDR        00:00:35    192.168.1.2     Gi1/0/1
10.1.1.3          1   FULL/DROTHER    00:00:38    192.168.1.3     Gi1/0/2
"""
    
    neighbors = parse_ospf_neighbors(mock_output)
    
    for neighbor in neighbors:
        if neighbor['neighbor_id'] in expected_neighbors:
            if 'FULL' in neighbor['state']:
                print(f"✓ Neighbor {neighbor['neighbor_id']} is FULL")
            else:
                print(f"✗ Neighbor {neighbor['neighbor_id']} not FULL: {neighbor['state']}")
        else:
            print(f"! Unexpected neighbor: {neighbor['neighbor_id']}")

if __name__ == "__main__":
    print("OSPF Switch Testing - Quick Start")
    print("=" * 40)
    
    # Show testing checklist
    checklist = ospf_testing_checklist()
    for area, description in checklist.items():
        print(f"{area}: {description}")
    
    print("\nTesting OSPF adjacency...")
    test_ospf_adjacency(['10.1.1.2', '10.1.1.3'])
    
    print("\nKey OSPF States:", OSPF_NEIGHBOR_STATES)
    print("Key LSA Types:", OSPF_LSA_TYPES)
