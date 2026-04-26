# Message Queues
<!-- GFM-TOC -->
* [Message Queues](#message-queues)
    * [1. Message Models](#_1-message-models)
        * [Point-to-Point](#point-to-point)
        * [Publish/Subscribe](#publishsubscribe)
    * [2. Use Cases](#_2-use-cases)
        * [Asynchronous Processing](#asynchronous-processing)
        * [Traffic Shaping](#traffic-shaping)
        * [Application Decoupling](#application-decoupling)
    * [3. Reliability](#_3-reliability)
        * [Sender Reliability](#sender-reliability)
        * [Receiver Reliability](#receiver-reliability)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Message Models

### Point-to-Point

After a message producer sends a message to a message queue, only one consumer can consume it once.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191212011250613.png"/> </div><br>

### Publish/Subscribe

After a message producer sends a message to a channel, multiple consumers can subscribe to that channel and consume the message.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191212011410374.png"/> </div><br>

The publish/subscribe pattern differs from the Observer pattern in the following ways:

- In the Observer pattern, observers and subjects know about each other; in publish/subscribe, producers and consumers do not know about each other and communicate through channels.
- The Observer pattern is synchronous: when an event is triggered, the subject calls the observer's method and waits for it to return. Publish/subscribe is asynchronous: after a producer sends a message to a channel, it does not need to care when consumers subscribe to that message and can return immediately.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191212011747967.png"/> </div><br>

## 2. Use Cases

### Asynchronous Processing

After the sender sends a message to the message queue, it does not need to wait synchronously for the receiver to finish processing it. It can return immediately and continue with other work. The receiver subscribes to messages from the queue and processes them asynchronously.

For example, a registration flow usually sends a verification email to confirm the registered user's identity. A message queue can make the email-sending step asynchronous: after the user fills in the registration information, registration can complete while the verification-email message is sent to the queue.

This is only appropriate when the business process allows asynchronous handling. In the registration example above, if registration cannot be completed until the user clicks the verification email, then a message queue should not be used for that step.

### Traffic Shaping

In high-concurrency scenarios, a large burst of requests in a short time can overwhelm the server.

Requests can be sent to a message queue, and the server can subscribe to and process messages according to its processing capacity.

### Application Decoupling

If modules do not call each other directly, coupling remains low. Modifying one module or adding a new one then has little impact on other modules, improving extensibility.

With a message queue, one module only needs to send messages to the queue, and other modules can selectively subscribe to messages to complete the interaction.

## 3. Reliability

### Sender Reliability

After the sender completes its operation, it must be able to send the message to the message queue successfully.

Implementation approach: create a message table in the local database and store message data and business data in the same database instance, so the local database transaction mechanism can be used. After the transaction commits successfully, transfer the messages from the message table to the message queue. If the transfer succeeds, delete the message-table data; otherwise, keep retrying.

### Receiver Reliability

The receiver must be able to consume a message from the message queue successfully once.

Two implementation approaches:

- Ensure the receiver's message-processing business logic is idempotent: as long as it is idempotent, consuming the message any number of times produces the same final result.
- Ensure each message has a unique ID, and use a log table to record IDs of messages that have already been consumed.

## References

- [Observer vs Pub-Sub](http://developers-club.com/posts/270339/)
- [Point-to-Point vs. Publish/Subscribe in Message Queues](https://blog.csdn.net/lizhitao/article/details/47723105)
