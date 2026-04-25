# System Design Basics
<!-- GFM-TOC -->
* [System Design Basics](#system-design-basics)
    * [1. Performance](#1-performance)
    * [2. Scalability](#2-scalability)
    * [3. Extensibility](#3-extensibility)
    * [4. Availability](#4-availability)
    * [5. Security](#5-security)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Performance

### Performance Metrics

#### 1. Response Time

The time consumed from when a request is sent until its response is received.

When testing response time, repeated requests are usually sent and the average response time is calculated.

#### 2. Throughput

The number of requests the system can process per unit of time, usually measured in requests per second.

#### 3. Concurrent Users

The number of concurrent user requests the system can handle at the same time.

In a system without concurrency, requests are executed sequentially, so response time is the reciprocal of throughput. For example, if the system supports 100 req/s, the average response time should be 0.01s.

Modern large-scale systems all support multithreading to handle concurrent requests. Multithreading can improve throughput and reduce response time mainly for two reasons:

- Multiple CPUs
- I/O wait time

With techniques such as I/O multiplexing, the system does not need to block while waiting for one I/O operation to complete and can process other requests instead. Using this waiting time greatly improves CPU utilization.

A higher concurrent user count is not always better. If concurrency is too high, the system cannot process all requests in time, too many requests have to wait, and response time increases sharply.

### Performance Optimization

#### 1. Clustering

Group multiple servers into a cluster and use load balancing to forward requests to the cluster, avoiding performance degradation caused by excessive load on a single server.

#### 2. Caching

Caching improves performance for the following reasons:

- Cached data is usually stored in media such as memory, which is especially fast for reads.
- Cached data can be located geographically closer to users.
- Computation results can be cached to avoid repeated computation.

#### 3. Asynchronous

Some workflows can convert operations into messages, send them to a message queue, and return immediately. The operation is then processed asynchronously.

## 2. Scalability

Scalability means continuously adding servers to a cluster to relieve rising concurrent user access pressure and growing data storage requirements.

### Scalability and Performance

If a system has performance problems, a single user's request is always slow.

If a system has scalability problems, a single user's request may be fast, but the system becomes slow under high concurrency.

### Implement Scalability

As long as application servers are stateless, new servers can be easily added to the cluster through a load balancer.

Relational database scalability is implemented through sharding, which distributes data across different nodes according to certain rules, solving the storage-space limit of a single storage server.

Non-relational databases are designed for massive data from the start and usually provide strong scalability support.

## 3. Extensibility

Extensibility means adding new features without affecting other applications in the existing system, which requires low coupling between applications.

There are two main ways to implement extensibility:

- Use message queues for decoupling, so applications communicate by passing messages.
- Use distributed services to separate business logic from reusable services. Business applications call reusable services through a distributed service framework. New products can implement business logic by calling reusable services without affecting other products.

## 4. Availability

### Redundancy

The main way to ensure high availability is redundancy: when one server fails, requests are sent to other servers.

Application-server redundancy is relatively easy to implement. As long as application servers are stateless, when one application server fails, the load balancer forwards that server's original user requests to another application server without affecting users.

Storage-server redundancy requires master-slave replication. When the master server fails, a slave server must be promoted to master; this process is called failover.

### Monitoring

Monitor system load information such as CPU, memory, disk, and network. When a metric reaches a threshold, notify operations staff so problems can be discovered before the system fails.

### Service Degradation

Service degradation means the system proactively disables some features to handle a large number of requests while keeping core features available.

## 5. Security

Security requires the system to have reliable countermeasures against various attack techniques.

## References

- Technical Architecture of Large Websites: Core Principles and Case Studies
