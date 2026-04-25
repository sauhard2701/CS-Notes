# Computer Networking - Application Layer
<!-- GFM-TOC -->
* [Computer Networking - Application Layer](#computer-networking---application-layer)
    * [Domain Name System](#domain-name-system)
    * [File Transfer Protocol](#file-transfer-protocol)
    * [Dynamic Host Configuration Protocol](#dynamic-host-configuration-protocol)
    * [Remote Login Protocol](#remote-login-protocol)
    * [Email Protocols](#email-protocols)
        * [1. SMTP](#1-smtp)
        * [2. POP3](#2-pop3)
        * [3. IMAP](#3-imap)
    * [Common Ports](#common-ports)
    * [Web Page Request Process](#web-page-request-process)
        * [1. DHCP Configures Host Information](#1-dhcp-configures-host-information)
        * [2. ARP Resolves MAC Address](#2-arp-resolves-mac-address)
        * [3. DNS Resolves Domain Name](#3-dns-resolves-domain-name)
        * [4. HTTP Requests the Page](#4-http-requests-the-page)
<!-- GFM-TOC -->


## Domain Name System

DNS is a distributed database that provides conversion between hostnames and IP addresses. Here, distributed database means that each site stores only its own portion of the data.

Domain names have a hierarchical structure. From top to bottom, the levels are: root domain, top-level domain, and second-level domain.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/b54eeb16-0b0e-484c-be62-306f57c40d77.jpg"/> </div><br>

DNS can use UDP or TCP for transmission, and both use port 53. In most cases, DNS uses UDP, which requires domain resolvers and domain servers to handle timeouts and retransmissions themselves to ensure reliability. TCP is used in two cases:

- If the returned response exceeds 512 bytes, because UDP supports at most 512 bytes of data.
- Zone transfer, where the primary domain server transfers changed data to the secondary domain server.

## File Transfer Protocol

FTP uses TCP connections. It requires two connections to transfer a file:

- Control connection: the server opens port 21 and waits for the client connection. After the client actively establishes the connection, this connection is used to send client commands to the server and return server responses.
- Data connection: used to transfer file data.

Depending on whether the server actively establishes the data connection, FTP has active and passive modes:

- Active mode: the server actively establishes the data connection. The server port is 20, and the client port is random but must be greater than 1024 because 0\~1023 are well-known ports.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/03f47940-3843-4b51-9e42-5dcaff44858b.jpg"/> </div><br>

- Passive mode: the client actively establishes the data connection. The client port is chosen by the client, and the server port is random.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/be5c2c61-86d2-4dba-a289-b48ea23219de.jpg"/> </div><br>

Active mode requires the client to open a port to the server, so the client firewall must be configured. Passive mode only requires the server to open ports and does not require client firewall configuration. However, passive mode weakens server-side security because too many ports are opened.

## Dynamic Host Configuration Protocol

DHCP (Dynamic Host Configuration Protocol) provides plug-and-play networking, so users no longer need to manually configure IP addresses and related information.

DHCP configures not only the IP address, but also the subnet mask and gateway IP address.

The DHCP process is as follows:

1. The client sends a Discover message. The destination address is 255.255.255.255:67 and the source address is 0.0.0.0:68. It is placed in UDP and broadcast to all hosts on the same subnet. If the client and DHCP server are not on the same subnet, a relay agent is needed.
2. After receiving the Discover message, the DHCP server sends an Offer message to the client. This message contains the information the client needs. Because the client may receive information from multiple DHCP servers, the client needs to choose one.
3. If the client selects the information provided by a DHCP server, it sends a Request message to that DHCP server.
4. The DHCP server sends an Ack message, indicating that the client can now use the provided information.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/23219e4c-9fc0-4051-b33a-2bd95bf054ab.jpg"/> </div><br>

## Remote Login Protocol

TELNET is used to log in to a remote host, and output from the remote host is returned.

TELNET can adapt to differences among many computers and operating systems, such as different newline definitions in different operating systems.

## Email Protocols

An email system consists of three parts: user agents, mail servers, and mail protocols.

Mail protocols include sending protocols and retrieval protocols. SMTP is commonly used for sending, while POP3 and IMAP are commonly used for retrieval.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7b3efa99-d306-4982-8cfb-e7153c33aab4.png" width="700"/> </div><br>

### 1. SMTP

SMTP can send only ASCII code, while the Internet mail extension MIME can send binary files. MIME does not modify or replace SMTP; it adds structure to the message body and defines encoding rules for non-ASCII code.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ed5522bb-3a60-481c-8654-43e7195a48fe.png" width=""/> </div><br>

### 2. POP3

POP3 is characterized by deleting mail once the user reads it from the server. However, the latest versions of POP3 can avoid deleting mail.

### 3. IMAP

In IMAP, mail on the client and server remains synchronized. If mail is not manually deleted, it is not deleted from the server. This IMAP approach lets users access mail on the server anytime and anywhere.

## Common Ports

| Application | Application-Layer Protocol | Port | Transport-Layer Protocol | Notes |
| :---: | :--: | :--: | :--: | :--: |
| Domain name resolution | DNS | 53 | UDP/TCP | TCP is used when the length exceeds 512 bytes |
| Dynamic Host Configuration Protocol | DHCP | 67/68 | UDP | |
| Simple Network Management Protocol | SNMP | 161/162 | UDP | |
| File Transfer Protocol | FTP | 20/21 | TCP | Control connection 21, data connection 20 |
| Remote terminal protocol | TELNET | 23 | TCP | |
| Hypertext Transfer Protocol | HTTP | 80 | TCP | |
| Simple Mail Transfer Protocol | SMTP | 25 | TCP | |
| Mail retrieval protocol | POP3 | 110 | TCP | |
| Internet Message Access Protocol | IMAP | 143 | TCP | |

## Web Page Request Process

### 1. DHCP Configures Host Information

- Suppose the host initially has no IP address or other information. It first needs to use DHCP to obtain them.

- The host generates a DHCP request message and places it in a UDP segment with destination port 67 and source port 68.

- The segment is then placed in an IP datagram with broadcast destination IP address (255.255.255.255) and source IP address (0.0.0.0).

- The datagram is then placed in a MAC frame. The frame has destination address FF:\<zero-width space\>FF:\<zero-width space\>FF:\<zero-width space\>FF:\<zero-width space\>FF:FF and is broadcast to all devices connected to the switch.

- After the DHCP server connected to the switch receives the broadcast frame, it continuously decapsulates it upward to obtain the IP datagram, UDP segment, and DHCP request message. It then generates a DHCP ACK message containing the following information: IP address, DNS server IP address, default gateway router IP address, and subnet mask. The message is placed in a UDP segment, the UDP segment is placed in an IP datagram, and finally it is placed in a MAC frame.

- The destination address of the frame is the requesting host's MAC address. Because the switch has self-learning capability, after the host previously sent the broadcast frame, the switch recorded the forwarding table entry mapping the MAC address to its forwarding interface. Therefore, the switch can now directly determine which interface should receive the frame.

- After the host receives the frame, it continuously decapsulates it to obtain the DHCP message. It then configures its IP address, subnet mask, and DNS server IP address, and installs the default gateway in its IP forwarding table.

### 2. ARP Resolves MAC Address

- The host creates a TCP socket through the browser, and the socket sends an HTTP request to the HTTP server. To create this socket, the host needs to know the IP address corresponding to the website's domain name.

- The host generates a DNS query message with port 53, because the DNS server port is 53.

- The DNS query message is placed in an IP datagram whose destination address is the DNS server IP address.

- The IP datagram is placed in an Ethernet frame, which will be sent to the gateway router.

- The DHCP process only knows the gateway router's IP address. To obtain the gateway router's MAC address, the ARP protocol is needed.

- The host generates an ARP query message whose destination address is the gateway router IP address, places it in an Ethernet frame with broadcast destination address (FF:\<zero-width space\>FF:\<zero-width space\>FF:\<zero-width space\>FF:\<zero-width space\>FF:FF), and sends the Ethernet frame to the switch. The switch forwards the frame to all connected devices, including the gateway router.

- After the gateway router receives the frame, it continuously decapsulates it upward to obtain the ARP message. It finds that the IP address matches the IP address of its interface, so it sends an ARP reply message containing its MAC address back to the host.

### 3. DNS Resolves Domain Name

- After the gateway router's MAC address is known, the DNS resolution process can continue.

- After the gateway router receives the Ethernet frame containing the DNS query message, it extracts the IP datagram and uses the forwarding table to decide which router the IP datagram should be forwarded to.

- Because routers have both interior gateway protocols (RIP, OSPF) and exterior gateway protocols (BGP), the routing table already has route entries from the gateway router to the DNS server.

- After the message reaches the DNS server, the DNS server extracts the DNS query message and looks up the domain name to be resolved in the DNS database.

- After finding the DNS record, it sends a DNS response message. The response is placed in a UDP segment, then in an IP datagram, forwarded back through routers to the gateway router, and reaches the host through the Ethernet switch.

### 4. HTTP Requests the Page

- With the HTTP server's IP address, the host can create a TCP socket, which will be used to send an HTTP GET message to the web server.

- Before creating the TCP socket, a connection must be established with the HTTP server through the three-way handshake. A TCP SYN segment with destination port 80 is generated and sent to the HTTP server.

- After the HTTP server receives the segment, it generates a TCP SYN ACK segment and sends it back to the host.

- After the connection is established, the browser generates an HTTP GET message and delivers it to the HTTP server.

- The HTTP server reads the HTTP GET message from the TCP socket, generates an HTTP response message, places the web page content in the message body, and sends it back to the host.

- After the browser receives the HTTP response message, it extracts the web page content, renders it, and displays the web page.
