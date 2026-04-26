# Distributed Systems
<!-- GFM-TOC -->
* [Distributed Systems](#distributed-systems)
    * [1. Distributed Locks](#_1-distributed-locks)
        * [Database Unique Indexes](#database-unique-indexes)
        * [Redis SETNX Command](#redis-setnx-command)
        * [Redis RedLock Algorithm](#redis-redlock-algorithm)
        * [Zookeeper Ordered Nodes](#zookeeper-ordered-nodes)
    * [2. Distributed Transactions](#_2-distributed-transactions)
        * [2PC](#_2pc)
        * [Local Message Table](#local-message-table)
    * [3. CAP](#_3-cap)
        * [Consistency](#consistency)
        * [Availability](#availability)
        * [Partition Tolerance](#partition-tolerance)
        * [Tradeoffs](#tradeoffs)
    * [4. BASE](#_4-base)
        * [Basically Available](#basically-available)
        * [Soft State](#soft-state)
        * [Eventual Consistency](#eventual-consistency)
    * [5. Paxos](#_5-paxos)
        * [Execution Process](#execution-process)
        * [Constraints](#constraints)
    * [6. Raft](#_6-raft)
        * [Single Candidate Election](#single-candidate-election)
        * [Multiple Candidate Election](#multiple-candidate-election)
        * [Data Synchronization](#data-synchronization)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Distributed Locks

In a single-machine scenario, a language's built-in locks can be used for process synchronization. In a distributed scenario, however, processes that need synchronization may be on different nodes, so distributed locks are needed.

Blocking locks are usually implemented with a mutex:

- A mutex value of 0 means another process is using the lock, so it is locked;
- A mutex value of 1 means it is unlocked.

1 and 0 can be represented by an integer value or by whether some data exists.

### Database Unique Indexes

Insert a record into a table when acquiring the lock, and delete the record when releasing the lock. A unique index guarantees that the record can be inserted only once, so whether the record exists can indicate whether the lock is held.

This has the following problems:

- The lock has no expiration time. If unlocking fails, other processes can no longer acquire the lock;
- It can only be a non-blocking lock. If insertion fails, an error is returned directly and retry is impossible;
- It is not reentrant. A process that already holds the lock must acquire it again.

### Redis SETNX Command

Use the SETNX (set if not exist) command to insert a key-value pair. If the key already exists, it returns False; otherwise, insertion succeeds and it returns True.

SETNX is similar to a database unique index. It guarantees that only one key-value pair for the key exists, so the existence of that key-value pair can indicate whether the lock is held.

The EXPIRE command can set an expiration time for a key-value pair, avoiding the failed-lock-release problem in the database unique index approach.

### Redis RedLock Algorithm

This algorithm uses multiple Redis instances to implement distributed locks, ensuring availability even when a single point fails.

- Try to acquire the lock from N independent Redis instances;
- Calculate the time spent acquiring the lock. The lock is considered acquired only if the time is less than the lock expiration time and the lock was acquired from a majority (N / 2 + 1) of instances;
- If acquiring the lock fails, release the lock on each instance.

### Zookeeper Ordered Nodes

#### 1. Zookeeper Abstract Model

Zookeeper provides a tree-structured namespace. The parent node of /app1/p_1 is /app1.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/aefa8042-15fa-4e8b-9f50-20b282a2c624.png" width="320px"> </div><br>

#### 2. Node Types

- Persistent node: does not disappear when a session ends or times out;
- Ephemeral node: disappears when a session ends or times out;
- Sequential node: appends an ordered numeric suffix to the node name. For example, a generated sequential node may be /lock/node-0000000000, and the next sequential node is /lock/node-0000000001, and so on.

#### 3. Listeners

Register a listener for a node. When the node state changes, a message is sent to the client.

#### 4. Distributed Lock Implementation

- Create a lock directory /lock;
- When a client needs to acquire the lock, create an ephemeral sequential child node under /lock;
- The client gets the child node list under /lock and checks whether the child node it created has the smallest sequence number in the current list. If so, it has acquired the lock. Otherwise, it listens to the previous child node and repeats this step after receiving a child-node change notification until it acquires the lock;
- Execute business code, then delete the corresponding child node after completion.

#### 5. Session Timeout

If a session that has acquired the lock times out, the ephemeral node created by that session is deleted, so other sessions can acquire the lock. This implementation avoids the failed-lock-release problem of the database unique index approach.

#### 6. Herd Effect

A node that has not acquired the lock only needs to listen to its previous child node. If it listened to all child nodes, then whenever any child node changed state, all other child nodes would receive notifications. This is the herd effect. We only want the next child node to receive the notification.

## 2. Distributed Transactions

Distributed transactions refer to transaction operations located on different nodes, while still requiring the ACID properties.

For example, in an order placement scenario, if inventory and orders are not on the same node, distributed transactions are involved.

Difference between distributed locks and distributed transactions:

- The key issue with locks is mutual exclusion between process operations. For example, if multiple processes modify an account balance at the same time and there is no mutual exclusion, the account balance may become incorrect.
- The key issue with transactions is that a series of operations involved in the transaction must satisfy ACID. For example, to satisfy atomicity, these operations must either all execute or none execute.

### 2PC

Two-phase commit (2PC) introduces a coordinator to coordinate participant behavior and ultimately decide whether the participants should actually execute the transaction.

#### 1. Execution Process

##### 1.1. Prepare Phase

The coordinator asks participants whether the transaction executed successfully, and participants send back execution results. The query can be viewed as a vote, and execution requires all participants to agree.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/44d33643-1004-43a3-b99a-4d688a08d0a1.png" width="550px"> </div><br>

##### 1.2. Commit Phase

If the transaction succeeds on every participant, the transaction coordinator sends a notification telling participants to commit. Otherwise, the coordinator tells participants to roll back.

Note that in the prepare phase, participants execute the transaction but have not committed it. They commit or roll back only after receiving the coordinator's notification in the commit phase.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/d2ae9932-e2b1-4191-8ee9-e573f36d3895.png" width="550px"> </div><br>

#### 2. Existing Problems

##### 2.1. Synchronous Blocking

All transaction participants are synchronously blocked while waiting for other participants to respond and cannot perform other operations.

##### 2.2. Single Point of Failure

The coordinator plays a very important role in 2PC, so coordinator failure has a large impact. If failure occurs during the commit phase in particular, all participants remain synchronously blocked and cannot complete other operations.

##### 2.3. Data Inconsistency

During the commit phase, if the coordinator sends only some Commit messages and then a network exception occurs, only some participants receive the Commit message. In other words, only some participants commit the transaction, making system data inconsistent.

##### 2.4. Overly Conservative

Failure of any node causes the entire transaction to fail, and there is no complete fault-tolerance mechanism.

### Local Message Table

The local message table and business data table are in the same database, so local transactions can ensure that operations on the two tables satisfy transaction properties, while a message queue ensures eventual consistency.

1. After one side of the distributed transaction writes business data, it sends a message to the local message table. The local transaction guarantees that this message is written to the local message table.
2. Then forward messages from the local message table to the message queue. If forwarding succeeds, delete the message from the local message table; otherwise, keep retrying.
3. The other side of the distributed transaction reads a message from the message queue and executes the operation in the message.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/476329d4-e2ef-4f7b-8ac9-a52a6f784600.png" width="740px"> </div><br>


## 3. CAP

A distributed system cannot simultaneously satisfy consistency (C), availability (A), and partition tolerance (P). At most, it can satisfy two of them at the same time.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a14268b3-b937-4ffa-a34a-4cc53071686b.jpg" width="450px"> </div><br>

### Consistency

Consistency is the property that multiple data replicas remain consistent. Under consistency, after the system performs a data update, it can transition from one consistent state to another.

After a data update succeeds in the system, if all users can read the latest value, the system is considered strongly consistent.

### Availability

Availability is the ability of a distributed system to provide normal service when facing various exceptions. It can be measured by the ratio of system available time to total time. Four nines of availability means the system is available 99.99% of the time.

Under availability, the services provided by the system must always be available, and every user operation request must return a result within a finite amount of time.

### Partition Tolerance

Network partitioning means nodes in a distributed system are divided into multiple regions. Nodes within each region can communicate, but regions cannot communicate with each other.

Under partition tolerance, when a distributed system encounters any network partition failure, it must still provide consistency and availability externally unless the entire network environment fails.

### Tradeoffs

In distributed systems, partition tolerance is essential because the network must always be assumed unreliable. Therefore, CAP theory is essentially a trade-off between availability and consistency.

Availability and consistency often conflict, making it difficult to satisfy both. When synchronizing data across multiple nodes:

- To guarantee consistency (CP), nodes that have not completed synchronization cannot be accessed, so some availability is lost;
- To guarantee availability (AP), data from all nodes can be read, but the data may be inconsistent.

## 4. BASE

BASE is the abbreviation of Basically Available, Soft State, and Eventually Consistent.

BASE theory is the result of the trade-off between consistency and availability in CAP. Its core idea is that even if strong consistency cannot be achieved, each application can use an appropriate approach based on its business characteristics to make the system eventually consistent.


### Basically Available

This means that when a distributed system fails, core availability is guaranteed while partial availability loss is allowed.

For example, during an e-commerce promotion, to ensure shopping-system stability, some consumers may be guided to a degraded page.

### Soft State

This means allowing data in the system to exist in an intermediate state and considering that this intermediate state does not affect overall system availability. In other words, synchronization between data replicas on different nodes may have delays.

### Eventual Consistency

Eventual consistency emphasizes that all data replicas in the system will eventually reach a consistent state after a period of synchronization.

ACID requires strong consistency and is usually used in traditional database systems. BASE requires eventual consistency and achieves availability by sacrificing strong consistency; it is usually used in large distributed systems.

In real distributed scenarios, different business units and components have different consistency requirements, so ACID and BASE are often used together.

## 5. Paxos

Used to solve consensus problems. For values produced by multiple nodes, this algorithm guarantees that only one value is selected.

There are three main types of nodes:

- Proposer: proposes a value;
- Acceptor: votes on each proposal;
- Learner: is informed of the voting result and does not participate in voting.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/b988877c-0f0a-4593-916d-de2081320628.jpg"/> </div><br>

### Execution Process

A proposal contains two fields: [n, v], where n is the sequence number (unique) and v is the proposed value.

#### 1. Prepare Phase

The following figure shows the initial process of running the algorithm in a system with two Proposers and three Acceptors. Each Proposer sends a Prepare request to all Acceptors.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1a9977e4-2f5c-49a6-aec9-f3027c9f46a7.png"/> </div><br>

When an Acceptor receives a Prepare request containing proposal [n1, v1] and has not received a Prepare request before, it sends a Prepare response, sets the currently received proposal to [n1, v1], and promises not to accept proposals with sequence numbers smaller than n1 in the future.

As shown below, when Acceptor X receives the Prepare request [n=2, v=8], it has not previously received a proposal, so it sends a [no previous] Prepare response, sets the currently received proposal to [n=2, v=8], and promises not to accept proposals with sequence numbers less than 2 in the future. The other Acceptors behave similarly.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/fb44307f-8e98-4ff7-a918-31dacfa564b4.jpg"/> </div><br>

If an Acceptor receives a Prepare request containing proposal [n2, v2] and has previously received proposal [n1, v1], then if n1 \> n2, it discards the proposal request. Otherwise, it sends a Prepare response containing the previously received proposal [n1, v1], sets the currently received proposal to [n2, v2], and promises not to accept proposals with sequence numbers smaller than n2 in the future.

As shown below, Acceptor Z receives the Prepare request [n=2, v=8] from Proposer A. Because it has already received proposal [n=4, v=5] and n \> 2, it discards the proposal request. Acceptor X receives the Prepare request [n=4, v=5] from Proposer B. Because its previously received proposal is [n=2, v=8] and 2 \<= 4, it sends a Prepare response [n=2, v=8], sets the currently received proposal to [n=4, v=5], and promises not to accept proposals with sequence numbers less than 4 in the future. Acceptor Y behaves similarly.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2bcc58ad-bf7f-485c-89b5-e7cafc211ce2.jpg"/> </div><br>

#### 2. Accept Phase

When a Proposer receives Prepare responses from more than half of the Acceptors, it can send an Accept request.

After Proposer A receives two Prepare responses, it sends an Accept request [n=2, v=8]. This Accept request is discarded by all Acceptors because all Acceptors have promised not to accept proposals with sequence numbers less than 4.

Later, Proposer B also receives two Prepare responses and begins sending an Accept request. Note that the v value of the Accept request must be the v value corresponding to the largest proposal number it received, which is 8. Therefore, it sends an Accept request [n=4, v=8].

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/9b838aee-0996-44a5-9b0f-3d1e3e2f5100.png"/> </div><br>

#### 3. Learn Phase

When an Acceptor receives an Accept request, if the sequence number is greater than or equal to the minimum sequence number promised by that Acceptor, it sends a Learn proposal to all Learners. When a Learner observes that a majority of Acceptors have accepted a proposal, the proposal value is chosen by Paxos.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/bf667594-bb4b-4634-bf9b-0596a45415ba.jpg"/> </div><br>

### Constraints

#### 1. Correctness

Means only one proposal value can take effect.

Because the Paxos protocol requires every effective proposal to be accepted by a majority of Acceptors, and Acceptors do not accept two different proposals, correctness can be guaranteed.

#### 2. Termination

Means a proposal will eventually take effect.

The Paxos protocol makes proposals sent by Proposers converge toward a proposal that can be accepted by a majority of Acceptors, thereby guaranteeing termination.

## 6. Raft

Raft is also a distributed consensus protocol, mainly used to elect a leader.

- [Raft: Understandable Distributed Consensus](http://thesecretlivesofdata.com/raft)

### Single Candidate Election

There are three types of nodes: Follower, Candidate, and Leader. The Leader periodically sends heartbeats to Followers. Each Follower sets a random election timeout, usually 150ms\~300ms. If it does not receive a heartbeat from the Leader within this time, it becomes a Candidate and enters the election phase.

- The following figure shows the initial stage of a distributed system, where there are only Followers and no Leader. After Node A waits for a random election timeout and receives no heartbeat from a Leader, it enters the election phase.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/111521118015898.gif"/> </div><br>

- At this point, Node A sends vote requests to all other nodes.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/111521118445538.gif"/> </div><br>

- Other nodes reply to the request. If more than half of the nodes reply, the Candidate becomes the Leader.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/111521118483039.gif"/> </div><br>

- After that, the Leader periodically sends heartbeats to Followers. When a Follower receives a heartbeat, it restarts its timer.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/111521118640738.gif"/> </div><br>

### Multiple Candidate Election

- If multiple Followers become Candidates and receive the same number of votes, voting must restart. For example, in the figure below, Node B and Node D both receive two votes, so voting must restart.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/111521119203347.gif"/> </div><br>

- Because each node sets a different random election timeout, the probability that multiple Candidates appear again and receive the same number of votes in the next round is low.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/111521119368714.gif"/> </div><br>

### Data Synchronization

- Modifications from clients are sent to the Leader. Note that the modification has not yet been committed; it is only written to the log.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/71550414107576.gif"/> </div><br>

- The Leader replicates the modification to all Followers.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/91550414131331.gif"/> </div><br>

- The Leader waits until a majority of Followers have also applied the modification, then commits the modification.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/101550414151983.gif"/> </div><br>

- At this point, the Leader notifies all Followers to commit the modification as well, and all nodes reach the same value.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/111550414182638.gif"/> </div><br>

## References

- Ni Chao. From Paxos to ZooKeeper: Principles and Practice of Distributed Consistency[M]. Publishing House of Electronics Industry, 2015.
- [Distributed locks with Redis](https://redis.io/topics/distlock)
- [A brief discussion of distributed locks](http://www.linkedkeeper.com/detail/blog.action?bid=1023)
- [Zookeeper-based distributed locks](http://www.dengshenyu.com/java/%E5%88%86%E5%B8%83%E5%BC%8F%E7%B3%BB%E7%BB%9F/2017/10/23/zookeeper-distributed-lock.html)
- [Distributed transactions and solution patterns](https://www.cnblogs.com/savorboard/p/distributed-system-transaction-consistency.html)
- [Transaction processing in distributed systems](https://coolshell.cn/articles/10910.html)
- [Deep understanding of distributed transactions](https://juejin.im/entry/577c6f220a2b5800573492be)
- [What is CAP theorem in distributed database system?](http://www.colooshiki.com/index.php/2017/04/20/what-is-cap-theorem-in-distributed-database-system/)
- [NEAT ALGORITHMS - PAXOS](http://harry.me/blog/2014/12/27/neat-algorithms-paxos/)
- [Paxos By Example](https://angus.nyc/2012/paxos-by-example/)
