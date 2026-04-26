# Computer Networking - Transport Layer
<!-- GFM-TOC -->
* [Computer Networking - Transport Layer](#computer-networking---transport-layer)
    * [UDP and TCP Characteristics](#udp-and-tcp-characteristics)
    * [UDP Header Format](#udp-header-format)
    * [TCP Header Format](#tcp-header-format)
    * [TCP Three-Way Handshake](#tcp-three-way-handshake)
    * [TCP Four-Way Handshake](#tcp-four-way-handshake)
    * [TCP Reliable Transmission](#tcp-reliable-transmission)
    * [TCP Sliding Window](#tcp-sliding-window)
    * [TCP Flow Control](#tcp-flow-control)
    * [TCP Congestion Control](#tcp-congestion-control)
        * [1. Slow Start and Congestion Avoidance](#_1-slow-start-and-congestion-avoidance)
        * [2. Fast Retransmit and Fast Recovery](#_2-fast-retransmit-and-fast-recovery)
<!-- GFM-TOC -->


The network layer only sends packets to the destination host, but the real communication is not between hosts; it is between processes in hosts. The transport layer provides logical communication between processes and hides the core details of the lower network layer from upper-layer users, making applications appear to have an end-to-end logical communication channel between two transport-layer entities.

## UDP and TCP Characteristics

- User Datagram Protocol (UDP) is connectionless, provides best-effort delivery, has no congestion control, is message-oriented (it neither merges nor splits messages passed down by the application, only adding a UDP header), and supports one-to-one, one-to-many, many-to-one, and many-to-many interactive communication.

- Transmission Control Protocol (TCP) is connection-oriented, provides reliable delivery, has flow control and congestion control, provides full-duplex communication, is byte-stream-oriented (treats messages passed down from the application layer as a byte stream and organizes the byte stream into data blocks of varying sizes), and each TCP connection can only be point-to-point (one-to-one).

## UDP Header Format

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/d4c3a4a1-0846-46ec-9cc3-eaddfca71254.jpg" width="600"/> </div><br>

The header fields are only 8 bytes, including source port, destination port, length, and checksum. The 12-byte pseudo-header is temporarily added to calculate the checksum.

## TCP Header Format

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/55dc4e84-573d-4c13-a765-52ed1dd251f9.png" width="700"/> </div><br>

-   **Sequence number**: used to number the byte stream. For example, sequence number 301 means the first byte is numbered 301. If the carried data length is 100 bytes, the sequence number of the next segment should be 401.

-   **Acknowledgment number**: the sequence number of the next expected segment. For example, if B correctly receives a segment from A with sequence number 501 and data length 200 bytes, B expects the next segment to have sequence number 701, so the acknowledgment number in B's acknowledgment segment sent to A is 701.

-   **Data offset**: the offset of the data portion from the start of the segment; in practice, it indicates the header length.

-   **Acknowledgment ACK**: when ACK=1, the acknowledgment number field is valid; otherwise, it is invalid. TCP specifies that after a connection is established, all transmitted segments must set ACK to 1.

-   **Synchronization SYN**: used to synchronize sequence numbers when establishing a connection. When SYN=1 and ACK=0, this is a connection request segment. If the peer agrees to establish the connection, the response has SYN=1 and ACK=1.

-   **Finish FIN**: used to release a connection. When FIN=1, it indicates that the sender of this segment has finished sending data and requests connection release.

-   **Window**: the window value is used by the receiver to let the sender set its sending window. This limit is needed because the receiver's data buffer space is limited.

## TCP Three-Way Handshake

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e92d0ebc-7d46-413b-aec1-34a39602f787.png" width="600"/> </div><br>

Assume A is the client and B is the server.

- First, B is in the LISTEN state, waiting for client connection requests.

- A sends a connection request segment to B with SYN=1 and ACK=0, and chooses an initial sequence number x.

- After B receives the connection request segment, if it agrees to establish the connection, it sends a connection acknowledgment segment to A with SYN=1, ACK=1, acknowledgment number x+1, and also chooses an initial sequence number y.

- After A receives B's connection acknowledgment segment, it also sends an acknowledgment to B with acknowledgment number y+1 and sequence number x+1.

- After B receives A's acknowledgment, the connection is established.

**Reason for the three-way handshake**

The third handshake prevents an expired connection request from reaching the server and causing the server to open a connection incorrectly.

If a connection request sent by the client is delayed in the network, the client may receive the server's connection acknowledgment only after a long time. After waiting for a retransmission timeout, the client requests the connection again. However, the delayed connection request may still eventually reach the server. Without the three-way handshake, the server would open two connections. With the third handshake, the client ignores the server's later connection acknowledgment for the delayed connection request and does not perform the third handshake, so the connection is not opened again.

## TCP Four-Way Handshake

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f87afe72-c2df-4c12-ac03-9b8d581a8af8.jpg" width="600"/> </div><br>

The following description does not discuss sequence numbers or acknowledgment numbers because their rules are relatively simple. It also does not discuss ACK because ACK is always 1 after the connection is established.

- A sends a connection release segment with FIN=1.

- After B receives it, B sends an acknowledgment. At this point, TCP is in a half-closed state: B can send data to A, but A cannot send data to B.

- When B no longer needs the connection, it sends a connection release segment with FIN=1.

- After A receives it, A sends an acknowledgment, enters the TIME-WAIT state, and releases the connection after waiting 2 MSL (Maximum Segment Lifetime).

- B releases the connection after receiving A's acknowledgment.

**Reason for the four-way handshake**

After the client sends a FIN connection release segment, the server receives it and enters the CLOSE-WAIT state. This state lets the server send any remaining data that has not yet been transmitted. After transmission is complete, the server sends a FIN connection release segment.

**TIME_WAIT**  

The client enters this state after receiving the server's FIN segment. It does not directly enter the CLOSED state; it must wait for 2MSL as set by a timer. There are two reasons:

- Ensure that the final acknowledgment segment can arrive. If B does not receive the acknowledgment segment sent by A, it will resend the connection release request segment. A waits for a period of time to handle this situation.

- Waiting for a period of time allows all segments generated during this connection to disappear from the network, so the next new connection will not encounter old connection request segments.

## TCP Reliable Transmission

TCP uses timeout retransmission to implement reliable transmission: if an already sent segment is not acknowledged within the timeout period, the segment is retransmitted.

The time from sending a segment to receiving its acknowledgment is called the round-trip time (RTT). The weighted average round-trip time RTTs is calculated as follows:

<div align="center"><img src="https://latex.codecogs.com/gif.latex?RTTs=(1-a)*(RTTs)+a*RTT" class="mathjax-pic"/></div> <br>
Here, 0 <= a < 1. As a increases, RTTs is more easily affected by RTT.

The timeout RTO should be slightly greater than RTTs. TCP calculates the timeout as follows:

<div align="center"><img src="https://latex.codecogs.com/gif.latex?RTO=RTTs+4*RTT_d" class="mathjax-pic"/></div> <br>
Here, RTT<sub>d</sub> is the weighted average deviation.

## TCP Sliding Window

A window is part of the buffer and is used to temporarily store the byte stream. The sender and receiver each have a window. The receiver tells the sender its window size through the window field in TCP segments, and the sender sets its own window size based on this value and other information.

Bytes inside the sending window are allowed to be sent, and bytes inside the receiving window are allowed to be received. If bytes on the left side of the sending window have been sent and acknowledged, the sending window slides right by some distance until the first byte on the left is no longer in the sent-and-acknowledged state. The receiving window slides similarly: when bytes on the left side of the receiving window have been acknowledged and delivered to the host, the receiving window slides right.

The receiving window only acknowledges the last byte in the window that arrives in order. For example, if the receiving window has received bytes {31, 34, 35}, only {31} arrived in order while {34, 35} did not, so only byte 31 is acknowledged. After the sender receives an acknowledgment for a byte, it knows that all bytes before that byte have been received.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a3253deb-8d21-40a1-aae4-7d178e4aa319.jpg" width="800"/> </div><br>

## TCP Flow Control

Flow control controls the sender's sending rate to ensure that the receiver has time to receive the data.

The window field in the acknowledgment segment sent by the receiver can be used to control the sender's window size, thereby affecting the sender's sending rate. If the window field is set to 0, the sender cannot send data.

## TCP Congestion Control

If network congestion occurs, packets are lost, and the sender continues retransmitting, which makes network congestion worse. Therefore, when congestion occurs, the sender's rate should be controlled. This is similar to flow control, but the motivation is different. Flow control ensures that the receiver can receive in time, while congestion control reduces congestion across the entire network.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/51e2ed95-65b8-4ae9-8af3-65602d452a25.jpg" width="500"/> </div><br>

TCP mainly performs congestion control through four algorithms: slow start, congestion avoidance, fast retransmit, and fast recovery.

The sender needs to maintain a state variable called the congestion window (cwnd). Note the difference between the congestion window and the sender window: the congestion window is only a state variable, while the sender window actually determines how much data the sender can send.

For discussion, make the following assumptions:

- The receiver has a large enough receive buffer, so flow control does not occur.
- Although TCP windows are byte-based, here the window size unit is assumed to be segments.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/910f613f-514f-4534-87dd-9b4699d59d31.png" width="800"/> </div><br>

### 1. Slow Start and Congestion Avoidance

Slow start is executed at the beginning of sending. Set cwnd = 1, so the sender can send only 1 segment. After receiving an acknowledgment, cwnd doubles, so the number of segments the sender can send becomes 2, 4, 8, and so on.

Note that slow start doubles cwnd every round, causing cwnd to grow very quickly. This makes the sender's sending rate grow too quickly and increases the possibility of network congestion. A slow-start threshold ssthresh is set. When cwnd \>= ssthresh, congestion avoidance begins, and cwnd increases by only 1 each round.

If a timeout occurs, set ssthresh = cwnd / 2 and then execute slow start again.

### 2. Fast Retransmit and Fast Recovery

On the receiver side, every received segment should acknowledge the last received in-order segment. For example, if M<sub>1</sub> and M<sub>2</sub> have already been received, and M<sub>4</sub> is then received, an acknowledgment for M<sub>2</sub> should be sent.

On the sender side, if three duplicate acknowledgments are received, the sender can know that the next segment was lost. It then performs fast retransmit and immediately retransmits the next segment. For example, if three acknowledgments for M<sub>2</sub> are received, M<sub>3</sub> was lost, so M<sub>3</sub> is retransmitted immediately.

In this case, only an individual segment was lost, not network congestion. Therefore fast recovery is performed: set ssthresh = cwnd / 2 and cwnd = ssthresh. Note that this directly enters congestion avoidance.

The "slow" in slow start and "fast" in fast recovery refer to the set value of cwnd, not the growth rate of cwnd. Slow start sets cwnd to 1, while fast recovery sets cwnd to ssthresh.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f61b5419-c94a-4df1-8d4d-aed9ae8cc6d5.png" width="600"/> </div><br>
