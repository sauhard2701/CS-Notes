# Computer Networking - Network Layer
<!-- GFM-TOC -->
* [Computer Networking - Network Layer](#computer-networking---network-layer)
    * [Overview](#overview)
    * [IP Datagram Format](#ip-datagram-format)
    * [IP Addressing](#ip-addressing)
        * [1. Classful Addressing](#1-classful-addressing)
        * [2. Subnetting](#2-subnetting)
        * [3. Classless Addressing](#3-classless-addressing)
    * [Address Resolution Protocol ARP](#address-resolution-protocol-arp)
    * [Internet Control Message Protocol ICMP](#internet-control-message-protocol-icmp)
        * [1. Ping](#1-ping)
        * [2. Traceroute](#2-traceroute)
    * [Virtual Private Network VPN](#virtual-private-network-vpn)
    * [Network Address Translation NAT](#network-address-translation-nat)
    * [Router Structure](#router-structure)
    * [Router Packet Forwarding Process](#router-packet-forwarding-process)
    * [Routing Protocols](#routing-protocols)
        * [1. Interior Gateway Protocol RIP](#1-interior-gateway-protocol-rip)
        * [2. Interior Gateway Protocol OSPF](#2-interior-gateway-protocol-ospf)
        * [3. Exterior Gateway Protocol BGP](#3-exterior-gateway-protocol-bgp)
<!-- GFM-TOC -->


## Overview

Because the network layer is the core of the entire Internet, it should be kept as simple as possible. The network layer provides only a simple, flexible, connectionless, best-effort datagram service to upper layers.

Using the IP protocol, heterogeneous physical networks can be connected so that they appear as one unified network at the network layer.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/8d779ab7-ffcc-47c6-90ec-ede8260b2368.png" width="800"/> </div><br>

Three other protocols are used together with IP:

- Address Resolution Protocol (ARP)
- Internet Control Message Protocol (ICMP)
- Internet Group Management Protocol (IGMP)

## IP Datagram Format

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/85c05fb1-5546-4c50-9221-21f231cdc8c5.jpg" width="700"/> </div><br>

-   **Version**: has two values, 4 (IPv4) and 6 (IPv6).

-   **Header length**: occupies 4 bits, so the maximum value is 15. A value of 1 represents the length of one 32-bit word, or 4 bytes. Because the fixed part is 20 bytes, the minimum value is 5. If the optional fields are not a multiple of 4 bytes, the padding at the end is used to fill them.

-   **Differentiated services**: used to obtain better service, generally not used.

-   **Total length**: includes the header length and data length.

-   **Time to live**: TTL exists to prevent undeliverable datagrams from circulating endlessly on the Internet. It is measured in router hops, and the datagram is discarded when TTL becomes 0.

-   **Protocol**: indicates which protocol should receive the carried data for processing, such as ICMP, TCP, or UDP.

-   **Header checksum**: because the checksum must be recalculated every time a datagram passes through a router, excluding the data portion from the checksum reduces computation.

-   **Identification**: when a datagram is too long and fragmentation occurs, different fragments of the same datagram have the same identifier.

-   **Fragment offset**: used together with the identifier when fragmentation occurs. The unit of fragment offset is 8 bytes.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/23ba890e-e11c-45e2-a20c-64d217f83430.png" width="700"/> </div><br>

## IP Addressing

IP addressing has gone through three historical stages:

- Classful addressing
- Subnetting
- Classless addressing

### 1. Classful Addressing

It consists of two parts: network number and host number. Different classes have different fixed network-number lengths.

IP address ::= {\< network number \>, \< host number \>}

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/cbf50eb8-22b4-4528-a2e7-d187143d57f7.png" width="500"/> </div><br>

### 2. Subnetting

By taking part of the host number field as the subnet number, a two-level IP address is divided into a three-level IP address.

IP address ::= {\< network number \>, \< subnet number \>, \< host number \>}

To use subnets, a subnet mask must be configured. The default subnet mask for a class B address is 255.255.0.0. If the subnet of a class B address occupies two bits, the subnet mask is 11111111 11111111 11000000 00000000, which is 255.255.192.0.

Note that external networks cannot see the existence of subnets.

### 3. Classless Addressing

Classless addressing CIDR eliminates the traditional concepts of class A, class B, class C addresses and subnetting. It uses a network prefix and host number to encode IP addresses, and the length of the network prefix can vary as needed.

IP address ::= {\< network prefix \>, \< host number \>}

CIDR notation appends the network prefix length to the IP address. For example, 128.14.35.7/20 indicates that the first 20 bits are the network prefix.

CIDR's address mask can still be called a subnet mask. The number of leading 1s in the subnet mask is the length of the network prefix.

A CIDR address block contains many addresses, and one CIDR network can represent many previous networks. In the routing table, one route can replace multiple previous routes, reducing the number of routing table entries. This method of reducing routing table entries by using network prefixes is called route aggregation, also called   **supernetting**  .

Entries in a routing table consist of a "network prefix" and a "next-hop address." A lookup may produce more than one match, so longest prefix matching should be used to determine which match to use.

## Address Resolution Protocol ARP

The network layer implements communication between hosts, while the link layer implements communication over each specific link. Therefore, during communication, the source and destination addresses of an IP datagram remain unchanged, while MAC addresses change as the link changes.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/66192382-558b-4b05-a35d-ac4a2b1a9811.jpg" width="700"/> </div><br>

ARP obtains the MAC address from an IP address.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/b9d79a5a-e7af-499b-b989-f10483e71b8b.jpg" width="500"/> </div><br>

Each host has an ARP cache containing a mapping table from IP addresses to MAC addresses for hosts and routers on the local area network.

If host A knows host B's IP address but the ARP cache has no mapping from that IP address to a MAC address, host A broadcasts an ARP request packet. After host B receives the request, it sends an ARP response packet to host A to report its MAC address. Host A then writes the mapping from host B's IP address to MAC address into its cache.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/8006a450-6c2f-498c-a928-c927f758b1d0.png" width="700"/> </div><br>

## Internet Control Message Protocol ICMP

ICMP is used to forward IP datagrams more effectively and improve the chance of successful delivery. It is encapsulated in IP datagrams, but it does not belong to an upper-layer protocol.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e3124763-f75e-46c3-ba82-341e6c98d862.jpg" width="500"/> </div><br>

ICMP messages are divided into error report messages and query messages.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/aa29cc88-7256-4399-8c7f-3cf4a6489559.png" width="600"/> </div><br>

### 1. Ping

Ping is an important application of ICMP, mainly used to test connectivity between two hosts.

Ping works by sending an ICMP Echo request message to the destination host. After receiving it, the destination host sends an Echo reply message. Ping estimates the packet round-trip time and packet loss rate based on time and the number of successful responses.

### 2. Traceroute

Traceroute is another application of ICMP, used to trace the path of a packet from source to destination.

The IP datagrams sent by Traceroute encapsulate undeliverable UDP user datagrams, and the destination host sends a destination-unreachable error report message.

- The source host sends a sequence of IP datagrams to the destination host. The first datagram P1 has its TTL set to 1. When P1 reaches the first router R1 on the path, R1 receives it and decrements TTL by 1. At this point TTL is 0, so R1 discards P1 and sends an ICMP time-exceeded error report message to the source host.
- The source host then sends the second datagram P2 and sets TTL to 2. P2 first reaches R1. R1 receives it, decrements TTL by 1, and forwards it to R2. R2 receives it and also decrements TTL by 1. Since TTL is now 0, R2 discards P2 and sends an ICMP time-exceeded error message to the source host.
- This process continues until the final datagram has just reached the destination host. The host does not forward the datagram and does not decrement the TTL value. However, because the datagram encapsulates an undeliverable UDP datagram, the destination host sends an ICMP destination-unreachable error report message to the source host.
- The source host then knows the IP addresses of the routers on the path to the destination host and the round-trip time to each router.

## Virtual Private Network VPN

Because IP addresses are scarce, the number of IP addresses an organization can obtain is often far smaller than the number of hosts it owns. Also, an organization does not need to connect all of its hosts to the external Internet. Computers inside the organization can use IP addresses that are valid only within the organization, called private addresses.

There are three private address blocks:

- 10.0.0.0 \~ 10.255.255.255
- 172.16.0.0 \~ 172.31.255.255
- 192.168.0.0 \~ 192.168.255.255

A VPN uses the public Internet as the communication carrier between the organization's private networks. "Private" means that hosts inside the organization communicate only with other hosts inside the organization. "Virtual" means it appears to be private, but actually passes through the public Internet.

In the figure below, communication between sites A and B passes through the Internet. If host X at site A wants to communicate with host Y at site B, the IP datagram's source address is 10.1.0.1 and destination address is 10.2.0.3. The datagram is first sent to router R1 connected to the Internet. R1 encrypts the internal data and then adds a new datagram header. The source address is R1's global address 125.1.2.3, and the destination address is R2's global address 194.4.5.6. After router R2 receives the datagram, it decrypts the data portion and restores the original datagram. At this point, the destination address is 10.2.0.3, so it is delivered to Y.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1556770b-8c01-4681-af10-46f1df69202c.jpg" width="800"/> </div><br>

## Network Address Translation NAT

When a host inside a private network uses a local IP address but wants to communicate with hosts on the Internet, NAT can be used to convert the local IP to a global IP.

In the past, NAT mapped local IPs and global IPs one-to-one. With this approach, a private network with n global IP addresses could have at most n hosts connected to the Internet at the same time. To use global IP addresses more efficiently, commonly used NAT translation tables now also use transport-layer port numbers, allowing multiple hosts inside a private network to share one global IP address. NAT that uses port numbers is also called Network Address and Port Translation (NAPT).

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2719067e-b299-4639-9065-bed6729dbf0b.png" width=""/> </div><br>

## Router Structure

Functionally, a router can be divided into routing and packet forwarding.

The packet forwarding structure consists of three parts: switching fabric, a set of input ports, and a set of output ports.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/c3369072-c740-43b0-b276-202bd1d3960d.jpg" width="600"/> </div><br>

## Router Packet Forwarding Process

- Extract the destination host IP address D from the datagram header and obtain the destination network address N.
- If N is a network address directly connected to this router, deliver it directly.
- If the routing table has a specific host route whose destination address is D, send the datagram to the next-hop router specified in the table.
- If the routing table has a route to network N, send the datagram to the next-hop router specified in the routing table.
- If the routing table has a default route, send the datagram to the default router specified in the routing table.
- Report an error in forwarding the packet.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1ab49e39-012b-4383-8284-26570987e3c4.jpg" width="800"/> </div><br>

## Routing Protocols

Routing protocols are adaptive and can adjust as network traffic and topology change.

The Internet can be divided into many smaller autonomous systems (AS). One AS can use a routing protocol different from other ASes.

Routing protocols can be divided into two main categories:

- Routing within an autonomous system: RIP and OSPF
- Routing between autonomous systems: BGP

### 1. Interior Gateway Protocol RIP

RIP is a distance-vector-based routing protocol. Distance refers to hop count. A directly connected router has hop count 1. The maximum hop count is 15, and more than 15 means unreachable.

RIP exchanges its routing table only with neighboring routers at fixed time intervals. After several exchanges, all routers eventually know the shortest distance to any network in the autonomous system and the next-hop router address.

Distance-vector algorithm:

- For a RIP message sent by a neighboring router with address X, first modify all entries in the message, change the address in the next-hop field to X, and add 1 to all distance fields.
- For each entry in the modified RIP message, perform the following steps:
 - If the original routing table does not contain destination network N, add this entry to the routing table.
 - Otherwise: if the next-hop router address is X, replace the original routing table entry with the received entry. Otherwise, if the distance d in the received entry is less than the distance in the routing table, update it. For example, if the original routing table entry is Net2, 5, P and the new entry is Net2, 4, X, update it. Otherwise, do nothing.
- If no routing table update is received from a neighboring router for 3 minutes, mark that neighboring router as unreachable, setting the distance to 16.

RIP is simple to implement and has low overhead. However, the maximum distance RIP can use is 15, which limits network scale. Also, when a network failure occurs, it takes a relatively long time to propagate this information to all routers.

### 2. Interior Gateway Protocol OSPF

Open Shortest Path First (OSPF) was developed to overcome RIP's shortcomings.

"Open" means OSPF is not controlled by any vendor and is publicly published. "Shortest Path First" means it uses Dijkstra's SPF shortest-path algorithm.

OSPF has the following characteristics:

- It sends information to all routers in the autonomous system. This method is flooding.
- The information sent is the link state with neighboring routers. Link state includes which routers are connected and the link metrics, represented by cost, distance, delay, bandwidth, and so on.
- Routers send information only when the link state changes.

All routers have the network-wide topology map, and the maps are consistent. Compared with RIP, OSPF's update process converges quickly.

### 3. Exterior Gateway Protocol BGP

BGP (Border Gateway Protocol)

Routing between ASes is difficult, mainly because:

- The Internet is very large.
- Different ASes use different internal routing protocols, so path metrics cannot be accurately defined.
- Routing between ASes must consider related policies, such as some ASes being unwilling to let other AS traffic pass through them.

BGP can only find a relatively good route, not the optimal route.

Each AS must configure a BGP speaker. Routing information is exchanged by establishing a TCP connection between two neighboring BGP speakers.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/9cd0ae20-4fb5-4017-a000-f7d3a0eb3529.png" width="600"/> </div><br>
