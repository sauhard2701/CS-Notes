# Computer Networking - Overview
<!-- GFM-TOC -->
* [Computer Networking - Overview](#computer-networking---overview)
    * [Network of Networks](#network-of-networks)
    * [ISP](#isp)
    * [Host Communication Modes](#host-communication-modes)
    * [Circuit Switching and Packet Switching](#circuit-switching-and-packet-switching)
        * [1. Circuit Switching](#1-circuit-switching)
        * [2. Packet Switching](#2-packet-switching)
    * [Delay](#delay)
        * [1. Queuing Delay](#1-queuing-delay)
        * [2. Processing Delay](#2-processing-delay)
        * [3. Transmission Delay](#3-transmission-delay)
        * [4. Propagation Delay](#4-propagation-delay)
    * [Computer Network Architecture](#computer-network-architecture)
        * [1. Five-Layer Protocol Stack](#1-five-layer-protocol-stack)
        * [2. OSI](#2-osi)
        * [3. TCP/IP](#3-tcpip)
        * [4. Data Transfer Across Layers](#4-data-transfer-across-layers)
<!-- GFM-TOC -->


## Network of Networks

A network connects hosts, while an internet connects many different networks together. Therefore, an internet is a network of networks. The Internet is the global internet.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/network-of-networks.gif" width="450"/> </div><br>

## ISP

An Internet Service Provider (ISP) can obtain many IP addresses from Internet management organizations and owns communication lines, routers, and other networking devices. Individuals or organizations can access the Internet by paying a fee to an ISP.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/72be01cd-41ae-45f7-99b9-a8d284e44dd4.png" width="500"/> </div><br>

The current Internet has a multi-level ISP structure. ISPs are divided by coverage area into tier-1 ISPs, regional ISPs, and access ISPs. An Internet Exchange Point (IXP) allows two ISPs to connect directly without passing through a third ISP.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/3be42601-9d33-4d29-8358-a9d16453af93.png" width="500"/> </div><br>

## Host Communication Modes

- Client-server (C/S): the client requests services, and the server provides services.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/914894c2-0bc4-46b5-bef9-0316a69ef521.jpg" width="240px"> </div><br>

- Peer-to-peer (P2P): clients and servers are not distinguished.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/42430e94-3137-48c0-bdb6-3cebaf9102e3.jpg" width="200px"> </div><br>

## Circuit Switching and Packet Switching

### 1. Circuit Switching

Circuit switching is used in telephone communication systems. Before two users communicate, a dedicated physical link must be established, and the link is occupied throughout the communication process. Because the transmission line cannot be used continuously during the entire communication process, circuit switching has very low line utilization, often less than 10%.

### 2. Packet Switching

Each packet has a header and trailer containing control information such as source and destination addresses. Multiple packets can be transmitted over the same transmission line without affecting each other, so multiple packets can be transmitted on the same line at the same time. In other words, packet switching does not occupy the transmission line exclusively.

In a postal communication system, after a post office receives a letter, it stores it first and then forwards letters with the same destination together to the next destination. This is the store-and-forward process, and packet switching also uses store-and-forward.

## Delay

Total delay = queuing delay + processing delay + transmission delay + propagation delay

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/4b2ae78c-e254-44df-9e37-578e2f2bef52.jpg" width="380"/> </div><br>

### 1. Queuing Delay

The time a packet spends waiting in a router's input and output queues. It depends on the current traffic volume of the network.

### 2. Processing Delay

The time required for a host or router to process a packet after receiving it, such as analyzing headers, extracting data from the packet, performing error checks, or finding an appropriate route.

### 3. Transmission Delay

The time required for a host or router to transmit a data frame.

<!-- <div align="center"><img src="https://latex.codecogs.com/gif.latex?delay=\frac{l(bit)}{v(bit/s)}" class="mathjax-pic"/></div> <br> -->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/dcdbb96c-9077-4121-aeb8-743e54ac02a4.png" width="150px"> </div><br>


Here, l represents the length of the data frame, and v represents the transmission rate.

### 4. Propagation Delay

The time required for electromagnetic waves to propagate through a channel. Electromagnetic waves propagate at a speed close to the speed of light.

<!-- <div align="center"><img src="https://latex.codecogs.com/gif.latex?delay=\frac{l(m)}{v(m/s)}" class="mathjax-pic"/></div> <br> -->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a1616dac-0e12-40b2-827d-9e3f7f0b940d.png" width="150"> </div><br>

Here, l represents the channel length, and v represents the propagation speed of electromagnetic waves in the channel.

## Computer Network Architecture

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/0fa6c237-a909-4e2a-a771-2c5485cd8ce0.png" width="450"/> </div><br>

### 1. Five-Layer Protocol Stack

-   **Application Layer**: Provides data transmission services for specific applications, such as HTTP and DNS. The data unit is a message.

-   **Transport Layer**: Provides general data transmission services for processes. Because there are many application-layer protocols, defining general transport-layer protocols can support a growing number of application-layer protocols. The transport layer includes two protocols: Transmission Control Protocol (TCP), which provides connection-oriented and reliable data transmission services with segments as the data unit; and User Datagram Protocol (UDP), which provides connectionless best-effort data transmission services with user datagrams as the data unit. TCP mainly provides integrity, while UDP mainly provides timeliness.

-   **Network Layer**: Provides data transmission services for hosts. In contrast, transport-layer protocols provide data transmission services for processes within hosts. The network layer encapsulates segments or user datagrams passed down from the transport layer into packets.

-   **Data Link Layer**: The network layer still focuses on data transmission services between hosts, and there can be many links between hosts. Link-layer protocols provide data transmission services for hosts on the same link. The data link layer encapsulates packets passed down from the network layer into frames.

-   **Physical Layer**: Considers how to transmit bit streams over transmission media, rather than referring to specific transmission media. The role of the physical layer is to hide differences in transmission media and communication methods as much as possible so that the data link layer does not perceive them.

### 2. OSI

The presentation layer and session layer are used as follows:

-   **Presentation Layer**: Handles data compression, encryption, and data description, so applications do not need to care about differences in internal data formats across hosts.

-   **Session Layer**: Establishes and manages sessions.

The five-layer protocol stack has no presentation layer or session layer. These functions are left to application developers.

### 3. TCP/IP

It has only four layers, equivalent to merging the data link layer and physical layer in the five-layer protocol stack into the network interface layer.

The TCP/IP architecture does not strictly follow the OSI layering concept. The application layer may directly use the IP layer or the network interface layer.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/48d79be8-085b-4862-8a9d-18402eb93b31.png" width="250"/> </div><br>

### 4. Data Transfer Across Layers

During downward transmission, headers or trailers required by lower-layer protocols need to be added. During upward transmission, headers and trailers are continuously removed.

Routers have only the lower three protocol layers because routers are located in the network core and do not need to provide services for processes or applications, so they do not need the transport layer or application layer.
