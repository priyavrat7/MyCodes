# 🔌 Network Switches - Complete Technical Guide

## 📋 Table of Contents
1. [What is a Switch?](#what-is-a-switch)
2. [Switch Types](#switch-types)
3. [Key Technical Terms](#key-technical-terms)
4. [Switch Functions](#switch-functions)
5. [Switch Protocols](#switch-protocols)
6. [Switch Configuration Concepts](#switch-configuration-concepts)
7. [Layer 2 vs Layer 3 Switches](#layer-2-vs-layer-3-switches)
8. [VLAN Concepts](#vlan-concepts)
9. [Spanning Tree Protocol](#spanning-tree-protocol)
10. [Switch Port Types](#switch-port-types)
11. [Common Switch Commands](#common-switch-commands)
12. [Troubleshooting Terms](#troubleshooting-terms)

---

## What is a Switch?

A **network switch** is a networking device that connects devices on a computer network by using packet switching to receive, process, and forward data to the destination device.

### Key Characteristics:
- **Layer 2 Device** (Data Link Layer)
- **Operates on MAC addresses**
- **Creates separate collision domains**
- **Forwards frames based on MAC address table**

---

## Switch Types

### 1. **Unmanaged Switch**
- Basic plug-and-play device
- No configuration needed
- Fixed settings
- Used in small networks/home offices

### 2. **Managed Switch**
- Full configuration capabilities
- Can configure VLANs, STP, QoS

  - **VLAN (Virtual Local Area Network):** Allows the creation of separate broadcast domains within a single physical switch. VLANs improve security, segment traffic, and reduce network congestion by isolating groups of devices onto logical networks.
  - **STP (Spanning Tree Protocol):** Prevents network loops in switched Ethernet networks by creating a loop-free logical topology. STP automatically blocks redundant paths and ensures there is only one active path between two network devices.

    > **How Cisco switches support OSPF in relation to STP:**  
    > While STP is responsible for loop prevention at Layer 2, Cisco switches are engineered to support advanced Layer 3 protocols like OSPF (Open Shortest Path First) for dynamic routing between VLANs and subnets. Modern Cisco switches can run both STP and OSPF concurrently: STP protects the switching infrastructure by keeping the Layer 2 network stable and loop-free, while OSPF enables the switch to participate in IP routing, exchange routing information, and quickly converge after network changes.  
    > Cisco enhances its switching platforms for OSPF by:
    > - Supporting OSPFv2/v3 within switch software (IOS, IOS XE)
    > - Allowing VLAN interfaces (SVIs) to participate in OSPF
    > - Implementing hardware-accelerated routing for line-rate OSPF performance
    > - Integrating OSPF with advanced STP features (like Rapid PVST+, MST) to ensure routing reconverges promptly when STP changes a network path
    >
    > **What is Rapid PVST+?**  
    > Rapid PVST+ (Rapid Per-VLAN Spanning Tree Plus) is Cisco's implementation of the IEEE 802.1w Rapid Spanning Tree Protocol (RSTP), applied to each VLAN individually. It provides much faster convergence than traditional STP, minimizing downtime after topology changes such as link or switch failures. Each VLAN has its own spanning tree instance, allowing for load balancing and improved resiliency across different VLANs on a network.
    >
    > **What is MST?**  
    > MST (Multiple Spanning Tree) or MSTP (Multiple Spanning Tree Protocol, IEEE 802.1s) is a standard that allows multiple VLANs to be mapped to a single spanning tree instance, significantly reducing the number of spanning tree calculations in large networks. This enables better scalability than PVST+ by grouping VLANs with similar topology requirements. MST helps conserve switch resources and ensures faster convergence while supporting flexible network designs.
    > - Providing diagnostic/debugging commands to monitor OSPF neighbors, adjacencies, and LSAs directly on the switch CLI
  > **How does Cisco find the MST (Multiple Spanning Tree) topology? Does it use algorithms like Dijkstra or Bellman-Ford?**
  >
  > **Answer:**  
  > Cisco switches implement MST (Multiple Spanning Tree Protocol, IEEE 802.1s) to manage loop-free and resilient Layer 2 topologies across VLANs. MST does *not* use Dijkstra or Bellman-Ford algorithms—those are used for Layer 3 routing protocols (like OSPF and RIP).  
  >
  > Instead, MST—like traditional STP and Rapid PVST+—uses a variant of the *Spanning Tree Algorithm (STA)*, which is based on concepts from graph theory’s "minimum spanning tree" algorithms (such as Kruskal’s or Prim’s algorithms), but is executed in a distributed fashion among all switches.  
  > 
  > **How MST works (in Cisco and all standards-based environments):**
  > - All switches in an MST region exchange special BPDUs (Bridge Protocol Data Units) to share information about VLANs, bridge priorities, and port costs.
  > - Each *MST Instance (MSTI)* is assigned a set of VLANs. Multiple MSTIs can run on the same switch, with each instance building its own logical spanning tree.
  > - For each MSTI—including the special Common Spanning Tree (CST, also called IST)—the switches collectively elect:
  >   - a *root bridge* (switch),
  >   - calculate the shortest-cost paths from the root using path costs (sum of port costs),
  >   - select root, designated, and blocked ports accordingly.
  > - The choice of forwarding/blocking is based on rules defined by the STA, ensuring only the most efficient (lowest-cost) loop-free path per VLAN group (instance).
  >
  > **Summary:**  
  > Cisco MSTP does *not* use Dijkstra or Bellman-Ford. It runs the distributed Spanning Tree Algorithm (not centralized like Prim’s or Kruskal’s), using BPDUs to collaboratively compute the minimum spanning tree for each instance across the layer 2 topology.
  >
  > The distributed Spanning Tree Algorithm used by MSTP is based on the original algorithm invented by Radia Perlman for spanning tree protocols. In practice, all switches running MSTP implement this distributed STA, where each switch exchanges BPDUs (Bridge Protocol Data Units) and independently applies rules (defined by the IEEE 802.1D/802.1s standard) to elect a root bridge for each MST instance, calculate lowest-cost paths, and select port roles (root, designated, blocked). The computation is not a single centralized calculation—rather, it's a synchronized process where all participating switches follow the protocol rules to agree on a topology that prevents loops and provides optimal forwarding.
  > **Is the Minimum Steiner Tree related to switching, MST, or network design?**
  >
  > The Minimum Steiner Tree (MST) problem from graph theory is *sometimes conceptually related* to network design, but **not directly implemented** in standard switch protocols like STP, Rapid PVST+, or MST/MSTP. The distributed Spanning Tree protocols used on switches (including Cisco's) *do not* compute an actual Steiner tree; instead, they build a minimum spanning tree (MST) using only the set of switches and links in the physical topology.
  >
  > **Relation of the Minimum Steiner Tree to network design:**
  > - In *theoretical or planning scenarios*, the Minimum Steiner Tree is used to design the most cost-effective network that connects a set of required nodes (switches, routers, sites), possibly using additional "relay" nodes. It finds a tree with the lowest total cost, possibly placing additional (Steiner) points to minimize cabling or transmission expense.
  > - In practical Ethernet switching (STP/MST), protocols only work with the existing topology. No extra "relay" nodes are introduced—the network dynamically computes a *spanning tree* across what is already present to ensure loop-freedom, not a true Steiner tree.
  >
  > **Summary:**  
  > - Minimum Steiner Tree is relevant as a *theoretical tool* for designing or optimizing physical topologies before deployment.
  > - Once the network is built, switches use algorithms more closely related to the Minimum Spanning Tree (MST), not Steiner Tree, to manage forwarding paths.
  > - Cisco MSTP, STP, and Rapid PVST+ do not use the Minimum Steiner Tree algorithm, but network planners might consider Steiner trees when minimizing the infrastructure required to interconnect sites.
  > **How could a Steiner tree actually help with network design?**
  >
  > In network planning, the Minimum Steiner Tree problem is valuable for finding the most cost-efficient way to physically connect a set of required sites (for example, multiple buildings or remote offices). Unlike the Minimum Spanning Tree, which only connects the given list of sites via the shortest total cable length, the Steiner Tree allows the addition of extra "relay" nodes (Steiner points) wherever it's optimal—even if no end user is there—to further reduce overall wiring cost. These relay points can be junction boxes, fiber distribution hubs, or aggregation switches strategically placed to minimize the sum of all cabling or link costs.
  > 
  > **Example application:**  
  > Suppose you need to connect five separate buildings on a campus network, but running cables directly between every pair of buildings is too expensive—maybe because of long distances or obstacles like roads or rivers. If you just use the Minimum Spanning Tree (MST) approach, you'd only connect the buildings themselves and lay the cables along the shortest possible set of links, but every connection must start and end at an actual building. However, the *Steiner Tree* approach gives you more flexibility: you're allowed to add new junction points anywhere (for example, by placing a small switch or a fiber splice cabinet at a strategic spot that isn't at a building, such as in the middle of a field or near an intersection). These extra junctions, or "Steiner points," let you run shorter cables between groups of buildings—so that instead of long direct runs, multiple buildings can be connected through these new points, dramatically reducing total fiber or cable costs.
  >
  > The reason MST (Minimum Spanning Tree) and Steiner Tree are different here is: MST only connects the required endpoints (the buildings), while Steiner Tree lets you "cheat" and place new connection points anywhere it helps. Standard switch protocols like STP or MSTP can't create or use such extra "relay" points; they only compute the minimum spanning tree on whatever switches and links already exist. In contrast, Steiner Tree is a *design* or *planning* tool you use *before* deployment, to minimize the cost of physically connecting all your sites by proposing optimal relay locations. After your design is built, your switches just use MSTP/STP, since they can't invent new connection points during operation.

  > **Famous Example: Cable Laying for a Campus or Metro Network**
  >
  > The Minimum Steiner Tree problem is classically used in *physical network design* to **reduce the total cost of cable or fiber installation** when connecting multiple locations. For instance:
  >
  > - **Campus Network Design:** Imagine you need to connect several buildings (A, B, C, D, E) in a university campus with network cables. Instead of running individual cables between each pair (which is extremely costly), or even just laying out the shortest set of links connecting all buildings (the Minimum Spanning Tree), the *Steiner Tree* approach lets you consider placing extra connection points (Steiner points)—maybe a utility vault or fiber juncture somewhere on the property—at locations *not* at the original buildings. This flexible placement can drastically reduce the total length (and thus cost) of cabling required.
  > - **Metropolitan Fiber Network:** Fiber providers often use Steiner tree techniques when planning new fiber infrastructure to connect several customer locations spread across a city. By adding splice points or intermediate distribution hubs at optimal spots (not just at customer addresses), the total fiber laid across the city can be greatly minimized.
  >
  > **Summary:** The classic, "textbook" example for applying the Minimum Steiner Tree problem is *designing the cable or fiber layout that connects multiple sites (buildings, offices, or base stations) at the minimum total installation cost*, potentially using optimally placed junctions or relay points that are not in the original set of endpoints.
  > 
  > In summary, the Steiner Tree gives theoretical insight and practical guidance for minimizing infrastructure cost in the design phase, before installation. However, after the network is built, standard protocols like STP/MSTP just operate on the fixed topology; they do not compute Steiner trees dynamically.
  - **QoS (Quality of Service):** Enables prioritization of certain types of network traffic (such as voice, video, or critical data) to ensure performance and reduce latency or jitter on important applications.
- CLI or web interface
- Used in enterprise networks

### 3. **Layer 2 Switch**
- Operates at Data Link Layer
- Forwards based on MAC addresses
- Cannot route between networks (because Layer 2 switches operate only at the Data Link layer and do not read or process IP addresses, so they have no capability to forward traffic between different IP networks or subnets)
- Most common type

### 4. **Layer 3 Switch**
- Combines Layer 2 switching + Layer 3 routing
- Can run routing protocols (OSPF, BGP, EIGRP)
- **OSPF (Open Shortest Path First):**
  - OSPF is a Link State routing protocol used at Layer 3 (the Network layer) to dynamically find the best path for IP traffic within large enterprise networks.
  - It enables routers and Layer 3 switches to automatically exchange routing information and calculate the shortest (lowest-cost) path to each network, using Dijkstra’s algorithm.
  - OSPF quickly detects changes in network topology (such as link failures) and updates all participating routers, ensuring fast convergence and optimal routing.
  - It supports features like route summarization, authentication, load balancing, and hierarchical area design (reducing routing overhead).
  - Commonly used in medium to large businesses because it scales well and supports complex, redundant topologies for high availability.

- Routes between VLANs
- Used in enterprise core/distribution layers

### 5. **PoE Switch (Power over Ethernet)**
- Provides power to connected devices
- Powers IP phones, cameras, access points
- Standards: PoE, PoE+, PoE++

### 6. **Stackable Switch**
- Multiple switches act as one logical unit
- Shared management interface
- Increased port density
- Common in Cisco Catalyst series

---

## Key Technical Terms

### **MAC Address (Media Access Control)**
- **Definition**: Unique identifier assigned to network interface
- **Format**: 48-bit address (e.g., `00:1A:2B:3C:4D:5E`)
- **Purpose**: Identifies devices at Layer 2
- **Types**:
  - **Unicast**: Single device
  - **Multicast**: Group of devices
  - **Broadcast**: All devices (`FF:FF:FF:FF:FF:FF`)

### **MAC Address Table (CAM Table)**
- **Definition**: Table mapping MAC addresses to switch ports
- **Purpose**: Determines which port to forward frames to
- **Learning**: Switch learns MAC addresses from incoming frames
- **Aging**: Entries expire after inactivity (default 300 seconds)

### **Frame**
- **Definition**: Data unit at Layer 2
- **Structure**: Header + Data + Trailer
- **Contains**: Source MAC, Destination MAC, Data, FCS

### **Collision Domain**
- **Definition**: Network segment where collisions can occur
- **Switch**: Each port is a separate collision domain
- **Hub**: All ports share one collision domain

### **Broadcast Domain**
- **Definition**: Network segment where broadcasts are forwarded
- **Switch**: All ports in same VLAN share broadcast domain
- **Router**: Separates broadcast domains

### **VLAN (Virtual LAN)**
- **Definition**: Logical segmentation of network
- **Purpose**: Isolate traffic, improve security
- **Range**: 1-4094 (1 and 1002-1005 reserved)
- **Types**: Access, Trunk, Native VLAN

### **Trunk Port**
- **Definition**: Port that carries multiple VLANs
- **Protocol**: 802.1Q (VLAN tagging)
- **Purpose**: Connect switches, carry VLAN traffic
- **Tagged**: Frames include VLAN ID

### **Access Port**
- **Definition**: Port assigned to single VLAN
- **Purpose**: Connect end devices
- **Untagged**: Frames don't include VLAN tag

### **Native VLAN**
- **Definition**: VLAN for untagged traffic on trunk
- **Default**: VLAN 1
- **Security**: Should be changed from default

### **STP (Spanning Tree Protocol)**
- **Definition**: Prevents loops in switched networks
- **Purpose**: Ensures loop-free topology
- **Standards**: 802.1D (STP), 802.1w (RSTP), 802.1s (MSTP)
- **States**: Blocking, Listening, Learning, Forwarding

### **Port Channel (EtherChannel)**
- **Definition**: Bundling multiple physical links
- **Purpose**: Increased bandwidth, redundancy
- **Protocols**: LACP, PAgP
- **Load Balancing**: Distributes traffic across links

### **Duplex**
- **Definition**: Communication direction
- **Half-Duplex**: One direction at a time
- **Full-Duplex**: Both directions simultaneously
- **Auto-Negotiation**: Automatically determines best setting

### **Speed**
- **Definition**: Data transfer rate
- **Common**: 10 Mbps, 100 Mbps, 1 Gbps, 10 Gbps
- **Auto-Negotiation**: Automatically determines best speed

### **QoS (Quality of Service)**
- **Definition**: Prioritizing network traffic
- **Purpose**: Ensure critical traffic gets priority
- **Methods**: Classification, Marking, Queuing, Policing

### **Port Security**
- **Definition**: Restricting access based on MAC addresses
- **Purpose**: Prevent unauthorized access
- **Actions**: Protect, Restrict, Shutdown

### **CDP (Cisco Discovery Protocol)**
- **Definition**: Cisco proprietary protocol
- **Purpose**: Discover neighboring Cisco devices
- **Layer 2**: Works without IP configuration

### **LLDP (Link Layer Discovery Protocol)**
- **Definition**: Vendor-neutral protocol
- **Purpose**: Discover neighboring devices
- **Standard**: IEEE 802.1AB

---

## Switch Functions

### **1. Learning**
- Switch examines source MAC address of incoming frames
- Adds MAC-to-port mapping to table
- Builds MAC address table dynamically

### **2. Forwarding**
- Switch examines destination MAC address
- Looks up in MAC address table
- Forwards to appropriate port

### **3. Filtering**
- Switch doesn't forward frames to source port
- Reduces unnecessary traffic

### **4. Flooding**
- When destination MAC not in table
- Sends frame to all ports (except source)
- Used for unknown unicast, broadcast, multicast

---

## Switch Protocols

### **Spanning Tree Protocol (STP)**
- **Purpose**: Prevent loops
- **Algorithm**: Creates loop-free tree topology
- **Root Bridge**: Reference point for all switches
- **BPDU**: Bridge Protocol Data Unit (control messages)

### **Rapid STP (RSTP)**
- **Improvement**: Faster convergence than STP
- **Port States**: Discarding, Learning, Forwarding
- **Convergence**: ~1-3 seconds (vs 30-50 seconds for STP)

### **Multiple STP (MSTP)**
- **Purpose**: Multiple spanning trees
- **Benefit**: Load balancing across VLANs
- **Instance**: Group of VLANs mapped to spanning tree

### **VLAN Trunking Protocol (VTP)**
- **Purpose**: Manage VLANs across switches
- **Modes**: Server, Client, Transparent
- **Note**: Less common in modern networks

### **Link Aggregation Control Protocol (LACP)**
- **Purpose**: Automatically form port channels
- **Standard**: IEEE 802.3ad
- **Mode**: Active, Passive

### **Port Aggregation Protocol (PAgP)**
- **Purpose**: Cisco proprietary port channeling
- **Modes**: Auto, Desirable, On, Off

---

## Switch Configuration Concepts

### **Switch Virtual Interface (SVI)**
- **Definition**: Virtual interface for VLAN
- **Purpose**: Layer 3 routing for VLAN
- **Example**: `interface vlan 10` with IP address

### **Management VLAN**
- **Definition**: VLAN for switch management
- **Purpose**: Remote access to switch
- **Security**: Should be separate from user VLANs

### **Inter-VLAN Routing**
- **Definition**: Routing between VLANs
- **Methods**: Router-on-a-stick, Layer 3 switch
- **Requirement**: Layer 3 device needed

### **Switch Stack**
- **Definition**: Multiple switches as one unit
- **Benefit**: Single management interface
- **Cisco**: StackWise technology

### **Switch Priority**
- **Definition**: Value used in STP root bridge election
- **Range**: 0-61440 (increments of 4096)
- **Lower = Higher Priority**

---

## Layer 2 vs Layer 3 Switches

### **Layer 2 Switch**
| Feature | Description |
|---------|-------------|
| **Layer** | Data Link (Layer 2) |
| **Forwarding** | Based on MAC addresses |
| **Routing** | Cannot route |
| **VLANs** | Can create VLANs |
| **Inter-VLAN Routing** | Requires router |
| **Protocols** | STP, VLAN, CDP/LLDP |

### **Layer 3 Switch**
| Feature | Description |
|---------|-------------|
| **Layer** | Network (Layer 3) + Data Link (Layer 2) |
| **Forwarding** | Based on IP addresses (routing) |
| **Routing** | Can route between networks |
| **VLANs** | Can create VLANs |
| **Inter-VLAN Routing** | Built-in (SVI) |
| **Protocols** | OSPF, BGP, EIGRP, STP, VLAN |

### **When to Use Layer 3 Switch**
- Need routing between VLANs
- Running routing protocols (OSPF, BGP)
- Enterprise core/distribution layer
- High-performance routing needed

---

## VLAN Concepts

### **VLAN Types**

#### **1. Default VLAN**
- **VLAN 1**: Default for all ports
- **Security Risk**: Should not be used for data
- **Management**: Often used for management

#### **2. Data VLAN**
- **Purpose**: Carry user data
- **Examples**: VLAN 10 (Sales), VLAN 20 (Engineering)

#### **3. Voice VLAN**
- **Purpose**: Carry VoIP traffic
- **QoS**: Typically has priority
- **Example**: VLAN 100

#### **4. Native VLAN**
- **Purpose**: Untagged traffic on trunk
- **Default**: VLAN 1
- **Security**: Should be changed

#### **5. Management VLAN**
- **Purpose**: Switch management access
- **Security**: Should be separate VLAN

### **VLAN Trunking**

#### **802.1Q Tagging**
- **Standard**: IEEE 802.1Q
- **Tag Size**: 4 bytes added to frame
- **Fields**: TPID, Priority, CFI, VLAN ID

#### **ISL (Inter-Switch Link)**
- **Type**: Cisco proprietary
- **Status**: Legacy (rarely used)
- **Replaced by**: 802.1Q

### **VLAN Configuration**
```cisco
! Create VLAN
vlan 10
 name Sales

! Assign port to VLAN
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 10

! Configure trunk
interface GigabitEthernet0/24
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
 switchport trunk native vlan 99
```

---

## Spanning Tree Protocol

### **STP Concepts**

#### **Root Bridge**
- **Definition**: Reference point for all switches
- **Election**: Lowest Bridge ID wins
- **Bridge ID**: Priority + MAC address

#### **Root Port**
- **Definition**: Port with best path to root bridge
- **Per Switch**: One root port per switch (except root)

#### **Designated Port**
- **Definition**: Port forwarding traffic on segment
- **Per Segment**: One designated port per segment

#### **Blocked Port**
- **Definition**: Port blocked to prevent loops
- **State**: Blocking (no forwarding)

### **STP Port States**

1. **Blocking**
   - No forwarding
   - Receives BPDUs
   - 20 seconds (max age)

2. **Listening**
   - No forwarding
   - Sends/receives BPDUs
   - 15 seconds

3. **Learning**
   - No forwarding
   - Learning MAC addresses
   - 15 seconds

4. **Forwarding**
   - Forwarding frames
   - Learning MAC addresses
   - Normal operation

5. **Disabled**
   - Administratively down
   - No participation in STP

### **STP Timers**
- **Hello Time**: 2 seconds (BPDU interval)
- **Forward Delay**: 15 seconds (Listening + Learning)
- **Max Age**: 20 seconds (BPDU timeout)

---

## Switch Port Types

### **1. Access Port**
- **VLAN**: Single VLAN
- **Traffic**: Untagged
- **Use**: Connect end devices

### **2. Trunk Port**
- **VLANs**: Multiple VLANs
- **Traffic**: Tagged (802.1Q)
- **Use**: Connect switches

### **3. Routed Port**
- **Layer 3**: IP address assigned
- **No Switching**: Acts as router interface
- **Use**: Layer 3 routing

### **4. Port Channel**
- **Multiple Links**: Bundled together
- **Load Balancing**: Traffic distributed
- **Redundancy**: Link failure protection

---

## Common Switch Commands

### **Basic Commands**
```cisco
! Show MAC address table
show mac address-table

! Show interfaces
show interfaces
show interfaces status
show interfaces brief

! Show VLANs
show vlan
show vlan brief

! Show spanning tree
show spanning-tree
show spanning-tree root
show spanning-tree detail
```

### **Configuration Commands**
```cisco
! Configure interface
interface GigabitEthernet0/1
 description Connected to Server
 switchport mode access
 switchport access vlan 10
 speed 1000
 duplex full
 no shutdown

! Configure trunk
interface GigabitEthernet0/24
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
 switchport trunk native vlan 99

! Create VLAN
vlan 10
 name Sales
```

### **Verification Commands**
```cisco
! Verify MAC table
show mac address-table dynamic
show mac address-table address <MAC>

! Verify VLANs
show vlan id 10
show interfaces switchport

! Verify STP
show spanning-tree vlan 10
show spanning-tree interface Gi0/1

! Verify port channel
show etherchannel summary
show etherchannel port-channel
```

---

## Troubleshooting Terms

### **Broadcast Storm**
- **Definition**: Excessive broadcast traffic
- **Cause**: Loops, misconfiguration
- **Effect**: Network performance degradation

### **MAC Address Flapping**
- **Definition**: MAC address seen on multiple ports
- **Cause**: Loops, duplicate MACs
- **Effect**: Unstable MAC table

### **STP Convergence**
- **Definition**: Time for STP to stabilize
- **STP**: 30-50 seconds
- **RSTP**: 1-3 seconds

### **Port Err-Disable**
- **Definition**: Port automatically disabled
- **Causes**: Security violation, loop detection
- **Recovery**: Manual or automatic (errdisable recovery)

### **Duplex Mismatch**
- **Definition**: Ports with different duplex settings
- **Symptom**: High collision/error rates
- **Fix**: Set both ports to same duplex

### **Speed Mismatch**
- **Definition**: Ports with different speeds
- **Symptom**: Link may not come up
- **Fix**: Set both ports to same speed

---

## Switch Performance Metrics

### **Forwarding Rate**
- **Definition**: Frames per second switch can forward
- **Measurement**: pps (packets per second)
- **Factors**: Port speed, number of ports

### **Switching Capacity**
- **Definition**: Total bandwidth switch can handle
- **Calculation**: Sum of all port speeds
- **Example**: 48 ports × 1 Gbps = 48 Gbps

### **Latency**
- **Definition**: Time for frame to traverse switch
- **Typical**: < 10 microseconds
- **Impact**: Real-time applications

### **Jitter**
- **Definition**: Variation in latency
- **Impact**: Voice/video quality
- **Mitigation**: QoS, buffer management

---

## Security Terms

### **Port Security**
- **Definition**: Restrict access by MAC address
- **Violation Modes**: Protect, Restrict, Shutdown
- **Sticky MAC**: Learn and save MAC addresses

### **DHCP Snooping**
- **Definition**: Prevent rogue DHCP servers
- **Purpose**: Security against attacks
- **Trusted Ports**: Ports allowed to send DHCP offers

### **Dynamic ARP Inspection (DAI)**
- **Definition**: Validate ARP packets
- **Purpose**: Prevent ARP spoofing
- **Requires**: DHCP Snooping

### **IP Source Guard**
- **Definition**: Filter traffic based on IP/MAC
- **Purpose**: Prevent IP spoofing
- **Binding**: IP-MAC-port binding

---

## Switch Architecture Terms

### **ASIC (Application-Specific Integrated Circuit)**
- **Definition**: Hardware for fast switching
- **Purpose**: Wire-speed forwarding
- **Benefit**: Low latency, high performance

### **CAM Table (Content Addressable Memory)**
- **Definition**: Hardware table for MAC addresses
- **Purpose**: Fast lookups
- **Size**: Limited (varies by switch model)

### **TCAM (Ternary CAM)**
- **Definition**: Advanced CAM for Layer 3
- **Purpose**: Fast routing lookups
- **Use**: Layer 3 switches

### **Backplane**
- **Definition**: Internal switching fabric
- **Purpose**: Connect all ports
- **Capacity**: Determines total throughput

---

## Cisco-Specific Terms

### **Cisco Catalyst**
- **Series**: Enterprise switches
- **Examples**: Catalyst 2960, 3750, 9300
- **Features**: Full Layer 2/3 capabilities

### **Cisco Nexus**
- **Series**: Data center switches
- **Features**: High performance, low latency
- **Use**: Data centers, cloud

### **Cisco IOS**
- **Definition**: Operating system for switches
- **Modes**: User, Privileged, Global Config
- **Commands**: CLI-based configuration

### **StackWise**
- **Definition**: Cisco stacking technology
- **Purpose**: Multiple switches as one unit
- **Benefit**: Single management, increased ports

---

## OSPF on Switches (Your Focus Area)

### **Layer 3 Switch OSPF**
- **Requirement**: Layer 3 switch (not Layer 2)
- **Configuration**: Enable routing, configure OSPF
- **Interfaces**: SVI (Switch Virtual Interface)
- **Use Case**: Routing between VLANs

### **OSPF on Switch Interfaces**
- **SVI**: Virtual interface per VLAN
- **Routed Port**: Physical port with IP
- **Network Statement**: Advertise networks in OSPF

### **Key Commands**
```cisco
! Enable IP routing
ip routing

! Create SVI
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown

! Configure OSPF
router ospf 1
 network 192.168.10.0 0.0.0.255 area 0
```

---

## Quick Reference

### **Switch Decision Process**
1. Receive frame on port
2. Learn source MAC → Add to table
3. Check destination MAC in table
4. If found → Forward to port
5. If not found → Flood to all ports

### **VLAN Decision Process**
1. Frame arrives on port
2. Check port VLAN assignment
3. Access port → Untagged, assign VLAN
4. Trunk port → Check tag, use VLAN ID
5. Forward based on VLAN

### **STP Decision Process**
1. Elect root bridge (lowest Bridge ID)
2. Each switch finds root port (best path)
3. Each segment elects designated port
4. Block all other ports
5. Form loop-free tree

---

## Summary

### **Key Takeaways**
- **Switches operate at Layer 2** (MAC addresses)
- **Layer 3 switches can route** (IP addresses)
- **VLANs segment networks** logically
- **STP prevents loops** in switched networks
- **Trunks carry multiple VLANs** between switches
- **Port channels increase bandwidth** and redundancy

### **For Your Cisco Interview**
- Understand Layer 2 vs Layer 3 switches
- Know VLAN concepts (access, trunk, native)
- Understand STP and loop prevention
- Be familiar with switch commands
- Know how OSPF works on Layer 3 switches

---

**This guide covers essential switch terminology and concepts for your Cisco OSPF testing role. Study these terms and understand how switches work in network environments!** 🚀
