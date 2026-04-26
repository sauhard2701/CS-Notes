# Computer Networking - Link Layer
<!-- GFM-TOC -->
* [Computer Networking - Link Layer](#computer-networking---link-layer)
    * [Basic Issues](#basic-issues)
        * [1. Framing](#_1-framing)
        * [2. Transparent Transmission](#_2-transparent-transmission)
        * [3. Error Detection](#_3-error-detection)
    * [Channel Classification](#channel-classification)
        * [1. Broadcast Channels](#_1-broadcast-channels)
        * [2. Point-to-Point Channels](#_2-point-to-point-channels)
    * [Channel Multiplexing](#channel-multiplexing)
        * [1. Frequency-Division Multiplexing](#_1-frequency-division-multiplexing)
        * [2. Time-Division Multiplexing](#_2-time-division-multiplexing)
        * [3. Statistical Time-Division Multiplexing](#_3-statistical-time-division-multiplexing)
        * [4. Wavelength-Division Multiplexing](#_4-wavelength-division-multiplexing)
        * [5. Code-Division Multiplexing](#_5-code-division-multiplexing)
    * [CSMA/CD Protocol](#csmacd-protocol)
    * [PPP Protocol](#ppp-protocol)
    * [MAC Address](#mac-address)
    * [Local Area Network](#local-area-network)
    * [Ethernet](#ethernet)
    * [Switches](#switches)
    * [Virtual LAN](#virtual-lan)
<!-- GFM-TOC -->


## Basic Issues

### 1. Framing

Add a header and trailer to packets passed down from the network layer to mark the beginning and end of a frame.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/29a14735-e154-4f60-9a04-c9628e5d09f4.png" width="300"/> </div><br>

### 2. Transparent Transmission

Transparency means that something that actually exists appears as if it does not exist.

Frames use headers and trailers as delimiters. If the data portion of a frame contains the same content as the header or trailer, the frame's start and end positions may be incorrectly identified. Escape characters need to be inserted before any content in the data portion that matches the header or trailer. If an escape character appears in the data portion, another escape character is added before it. After processing on the receiving side, the original data can be restored. In this process, the transparently transmitted content is the escape character, and users do not perceive its existence.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e738a3d2-f42e-4755-ae13-ca23497e7a97.png" width="500"/> </div><br>

### 3. Error Detection

The data link layer currently widely uses cyclic redundancy check (CRC) to detect bit errors.

## Channel Classification

### 1. Broadcast Channels

One-to-many communication: data sent by one node can be received by all nodes on the broadcast channel.

All nodes send data on the same broadcast channel, so special control methods are needed for coordination to avoid conflicts, also called collisions.

There are mainly two control methods for coordination: using channel multiplexing techniques and using the CSMA/CD protocol.

### 2. Point-to-Point Channels

One-to-one communication.

Because collisions do not occur, it is relatively simple and uses the PPP protocol for control.

## Channel Multiplexing

### 1. Frequency-Division Multiplexing

In frequency-division multiplexing, all hosts occupy different frequency bandwidth resources at the same time.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/4aa5e057-bc57-4719-ab57-c6fbc861c505.png" width="350"/> </div><br>

### 2. Time-Division Multiplexing

In time-division multiplexing, all hosts occupy the same frequency bandwidth resources at different times.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/67582ade-d44a-46a6-8757-3c1296cc1ef9.png" width="350"/> </div><br>

When using frequency-division multiplexing or time-division multiplexing for communication, a host continuously occupies part of the channel resources during communication. However, because computer data is bursty, there is no need to occupy channel resources continuously and prevent other users from using them, so both methods have low channel utilization.

### 3. Statistical Time-Division Multiplexing

This is an improvement over time-division multiplexing. It does not fix each user's position in a time-division multiplexing frame. As long as there is data, it is gathered into a statistical time-division multiplexing frame and sent.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/6283be2a-814a-4a10-84bf-9592533fe6bc.png" width="350"/> </div><br>

### 4. Wavelength-Division Multiplexing

Frequency-division multiplexing for light. Because the frequency of light is very high, the optical carrier used is conventionally represented by wavelength rather than frequency.

### 5. Code-Division Multiplexing

Assign each user an m-bit chip sequence, and all chip sequences are orthogonal. For any two chip sequences <img src="https://latex.codecogs.com/gif.latex?\vec{S}" class="mathjax-pic"/> and <img src="https://latex.codecogs.com/gif.latex?\vec{T}" class="mathjax-pic"/>, we have:

<!-- <div align="center"><img src="https://latex.codecogs.com/gif.latex?\frac{1}{m}\vec{S}\cdot\vec{T}=0" class="mathjax-pic"/></div> <br> -->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/308a02e9-3346-4251-8c41-bd5536dab491.png" width="100px"> </div><br>

For convenience, let m=8 and let chip sequence <img src="https://latex.codecogs.com/gif.latex?\vec{S}" class="mathjax-pic"/> be 00011011. When the user with this chip sequence sends bit 1, it sends this chip sequence; when it sends bit 0, it sends the complement 11100100.

In calculations, 00011011 is written as (-1 -1 -1 +1 +1 -1 +1 +1), giving:

<!-- <div align="center"><img src="https://latex.codecogs.com/gif.latex?\frac{1}{m}\vec{S}\cdot\vec{S}=1" class="mathjax-pic"/></div> <br> -->

<!-- <div align="center"><img src="https://latex.codecogs.com/gif.latex?\frac{1}{m}\vec{S}\cdot\vec{S'}=-1" class="mathjax-pic"/></div> <br> -->

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/6fda1dc7-5c74-49c1-bb79-237a77e43a43.png" width="100px"> </div><br>

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e325a903-f0b1-4fbd-82bf-88913dc2f290.png" width="125px"> </div><br>

Here, <img src="https://latex.codecogs.com/gif.latex?\vec{S'}" class="mathjax-pic"/> is the complement of <img src="https://latex.codecogs.com/gif.latex?\vec{S}" class="mathjax-pic"/>.

Using the formulas above, when the receiver uses chip sequence <img src="https://latex.codecogs.com/gif.latex?\vec{S}" class="mathjax-pic"/> to compute the inner product of received data, a result of 0 indicates data sent by other users, a result of 1 indicates bit 1 sent by this user, and a result of -1 indicates bit 0 sent by this user.

Code-division multiplexing requires sending m times as much data as before.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/99b6060e-099d-4201-8e86-f8ab3768a7cf.png" width="500px"> </div><br>


## CSMA/CD Protocol

CSMA/CD stands for Carrier Sense Multiple Access with Collision Detection.

-   **Multiple access**: indicates that this is a bus network, where many hosts connect to the bus in a multipoint manner.
-   **Carrier sense**: each host must continuously listen to the channel. Before sending, if it detects that the channel is in use, it must wait.
-   **Collision detection**: while sending, if it detects that another host is already sending data on the channel, a collision has occurred. Although each host has already detected that the channel is idle before sending, collisions may still occur because of electromagnetic-wave propagation delay.

Let the end-to-end propagation delay be τ. The first sending station can know whether a collision has occurred after at most 2τ, which is called the   **contention period**  . Only after the contention period passes without detecting a collision can it be certain that this transmission will not collide.

When a collision occurs, the station stops sending and waits for a period of time before sending again. This time is determined by the   **truncated binary exponential backoff algorithm**  . A number is randomly selected from the discrete integer set {0, 1, .., (2<sup>k</sup>-1)}, denoted as r, and r times the contention period is used as the retransmission waiting time.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/19d423e9-74f7-4c2b-9b97-55890e0d5193.png" width="400"/> </div><br>

## PPP Protocol

Internet users usually need to connect to an ISP before accessing the Internet. PPP is the data link layer protocol used for communication between the user's computer and the ISP.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e1ab9f28-cb15-4178-84b2-98aad87f9bc8.jpg" width="300"/> </div><br>

PPP frame format:

- The F field is the frame delimiter.
- The A and C fields have no meaning for now.
- The FCS field is the check sequence using CRC.
- The information field length does not exceed 1500.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/759013d7-61d8-4509-897a-d75af598a236.png" width="400"/> </div><br>

## MAC Address

A MAC address is a link-layer address with a length of 6 bytes (48 bits). It uniquely identifies a network adapter, or network card.

A host has as many MAC addresses as it has network adapters. For example, laptops commonly have both wireless and wired network adapters, so they have two MAC addresses.

## Local Area Network

A local area network is a typical broadcast channel. Its main characteristics are that the network is owned by one organization and both its geographic range and number of stations are limited.

Main local area network technologies include Ethernet, Token Ring, FDDI, and ATM. Ethernet currently dominates the wired LAN market.

LANs can be classified by network topology:

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/807f4258-dba8-4c54-9c3c-a707c7ccffa2.jpg" width="800"/> </div><br>

## Ethernet

Ethernet is a star-topology LAN.

Early Ethernet used hubs for connection. A hub is a physical-layer device that operates on bits rather than frames. When a bit arrives at an interface, the hub regenerates the bit and amplifies its energy intensity to extend the network transmission distance, then sends the bit to all other interfaces. If the hub receives frames from two different interfaces at the same time, a collision occurs.

Current Ethernet uses switches instead of hubs. A switch is a link-layer device. It does not cause collisions and can perform store-and-forward based on MAC addresses.

Ethernet frame format:

-   **Type**: marks the protocol used by the upper layer.
-   **Data**: length is between 46 and 1500; padding is needed if it is too small.
-   **FCS**: frame check sequence, using the CRC check method.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/164944d3-bbd2-4bb2-924b-e62199c51b90.png" width="500"/> </div><br>

## Switches

Switches have self-learning capability. They learn the contents of the switching table, which stores mappings from MAC addresses to interfaces.

Because of this self-learning capability, a switch is a plug-and-play device and does not require a network administrator to manually configure the switching table.

In the figure below, the switch has four interfaces. When host A sends a data frame to host B, the switch writes the mapping from host A to interface 1 into the switching table. To send the data frame to B, the switch first checks the switching table. At this point there is no entry for host B, so host A sends a broadcast frame. Hosts C and D discard the frame. When host B responds to the frame and sends a packet to host A, the switch looks up the switching table, finds that host A maps to interface 1, and sends the data frame to interface 1. At the same time, the switch adds the mapping from host B to interface 2.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a4444545-0d68-4015-9a3d-19209dc436b3.png" width="800"/> </div><br>

## Virtual LAN

A virtual LAN can establish logical groups independent of physical location. Only members in the same virtual LAN receive link-layer broadcast messages.

For example, in the figure below, (A1, A2, A3, A4) belong to one virtual LAN. Broadcasts sent by A1 are received by A2, A3, and A4, while other stations do not receive them.

Virtual LANs are established using VLAN trunk connections. A special interface on each switch is configured as a trunk interface to interconnect VLAN switches. IEEE defines an extended Ethernet frame format, 802.1Q, which adds a 4-byte VLAN tag header to the standard Ethernet frame to indicate which virtual LAN the frame belongs to.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e98e9d20-206b-4533-bacf-3448d0096f38.png" width="500"/> </div><br>
