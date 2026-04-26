# Operating Systems - Deadlocks
<!-- GFM-TOC -->
* [Operating Systems - Deadlocks](#operating-systems---deadlocks)
    * [Necessary Conditions](#necessary-conditions)
    * [Handling Methods](#handling-methods)
    * [Ostrich Strategy](#ostrich-strategy)
    * [Deadlock Detection and Recovery](#deadlock-detection-and-recovery)
        * [1. Deadlock Detection with One Resource per Type](#_1-deadlock-detection-with-one-resource-per-type)
        * [2. Deadlock Detection with Multiple Resources per Type](#_2-deadlock-detection-with-multiple-resources-per-type)
        * [3. Deadlock Recovery](#_3-deadlock-recovery)
    * [Deadlock Prevention](#deadlock-prevention)
        * [1. Break Mutual Exclusion](#_1-break-mutual-exclusion)
        * [2. Break Hold and Wait](#_2-break-hold-and-wait)
        * [3. Break No Preemption](#_3-break-no-preemption)
        * [4. Break Circular Wait](#_4-break-circular-wait)
    * [Deadlock Avoidance](#deadlock-avoidance)
        * [1. Safe State](#_1-safe-state)
        * [2. Banker Algorithm for Single Resource](#_2-banker-algorithm-for-single-resource)
        * [3. Banker Algorithm for Multiple Resources](#_3-banker-algorithm-for-multiple-resources)
<!-- GFM-TOC -->


## Necessary Conditions

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/c037c901-7eae-4e31-a1e4-9d41329e5c3e.png"/> </div><br>

- Mutual exclusion: each resource is either assigned to one process or available.
- Hold and wait: a process that already holds one resource can request new resources.
- No preemption: a resource assigned to a process cannot be forcibly preempted; it can only be explicitly released by the process holding it.
- Circular wait: two or more processes form a cycle, and each process in the cycle waits for a resource held by the next process.

## Handling Methods

There are mainly four methods:

- Ostrich strategy
- Deadlock detection and recovery
- Deadlock prevention
- Deadlock avoidance

## Ostrich Strategy

Bury your head in the sand and pretend the problem never happened.

Because solving deadlocks is expensive, the ostrich strategy, which takes no action, can achieve higher performance.

The ostrich strategy can be used when deadlocks have little impact on users or when the probability of deadlock is very low.

Most operating systems, including Unix, Linux, and Windows, handle deadlocks simply by ignoring them.

## Deadlock Detection and Recovery

This approach does not try to prevent deadlocks. Instead, when a deadlock is detected, it takes measures to recover.

### 1. Deadlock Detection with One Resource per Type

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/b1fa0453-a4b0-4eae-a352-48acca8fff74.png"/> </div><br>

The figure above is a resource allocation graph. Rectangles represent resources, and circles represent processes. An edge from a resource to a process means the resource has been allocated to that process; an edge from a process to a resource means the process is requesting that resource.

Figure a contains a cycle, extracted as figure b. It satisfies the circular-wait condition, so a deadlock occurs.

The deadlock detection algorithm for one resource per type works by detecting whether a directed graph contains a cycle. Starting from one node, perform depth-first search and mark visited nodes. If an already marked node is visited, the directed graph contains a cycle, which means a deadlock has been detected.

### 2. Deadlock Detection with Multiple Resources per Type

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e1eda3d5-5ec8-4708-8e25-1a04c5e11f48.png"/> </div><br>

In the figure above, there are three processes and four resources. Each data item means:

- E vector: total amount of resources.
- A vector: remaining amount of resources.
- C matrix: number of resources held by each process; each row represents the resources held by one process.
- R matrix: number of resources requested by each process.

The requests of processes P<sub>1</sub> and P<sub>2</sub> cannot be satisfied, but process P<sub>3</sub> can run. Let P<sub>3</sub> execute and then release its resources; at this point A = (2 2 2 0). P<sub>2</sub> can then execute and release its resources, making A = (4 2 2 1). P<sub>1</sub> can then execute as well. All processes can complete successfully, so there is no deadlock.

The algorithm is summarized as follows:

Initially, no process is marked. A process may be marked during execution. When the algorithm ends, any unmarked process is a deadlocked process.

1. Find an unmarked process P<sub>i</sub> whose requested resources are less than or equal to A.
2. If such a process is found, add row `i` of matrix C to A, mark the process, and return to step 1.
3. If no such process exists, the algorithm terminates.

### 3. Deadlock Recovery

- Recover by preemption.
- Recover by rollback.
- Recover by killing processes.

## Deadlock Prevention

Prevent deadlocks before the program runs.

### 1. Break Mutual Exclusion

For example, printer spooling allows several processes to output at the same time; the only process that actually requests the physical printer is the printer daemon.

### 2. Break Hold and Wait

One implementation is to require every process to request all resources it needs before it starts executing.

### 3. Break No Preemption

### 4. Break Circular Wait

Assign a global order to resources, and require processes to request resources only in that order.

## Deadlock Avoidance

Avoid deadlocks while the program is running.

### 1. Safe State

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ed523051-608f-4c3f-b343-383e2d194470.png"/> </div><br>

In figure a, the second column, Has, indicates the number of resources already held; the third column, Max, indicates the total number of resources needed; Free indicates the number of resources still available. Starting from figure a, first let B obtain all required resources, as in figure b. After B finishes, it releases its resources, making Free become 5, as in figure c. Then run C and A in the same way so all processes can complete. Therefore, the state shown in figure a is safe.

Definition: a state is safe if no deadlock has occurred and, even if all processes suddenly request their maximum resource needs, there still exists some scheduling order that allows every process to complete.

Safe-state detection is similar to deadlock detection because a safe state must not lead to deadlock. The Banker's algorithm below is very similar to the deadlock detection algorithm, so they can be compared together.

### 2. Banker Algorithm for Single Resource

Consider a banker in a small town who has promised each customer a certain loan limit. The algorithm determines whether satisfying a request would enter an unsafe state. If so, the request is rejected; otherwise, resources are allocated.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/d160ec2e-cfe2-4640-bda7-62f53e58b8c0.png"/> </div><br>

Figure c above is an unsafe state, so the algorithm rejects the preceding request and avoids entering the state shown in figure c.

### 3. Banker Algorithm for Multiple Resources

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/62e0dd4f-44c3-43ee-bb6e-fedb9e068519.png"/> </div><br>

The figure above has five processes and four resources. The left diagram shows allocated resources, and the right diagram shows resources still needed. On the far right, E, P, and A represent total resources, allocated resources, and available resources respectively. Note that these are vectors, not single values. For example, A=(1020) means the four resources have 1/0/2/0 remaining.

The algorithm for checking whether a state is safe is as follows:

- Check whether the right-side matrix has a row less than or equal to vector A. If no such row exists, the system will deadlock and the state is unsafe.
- If such a row is found, mark that process as terminated and add its allocated resources to A.
- Repeat the two steps above until all processes are marked as terminated; then the state is safe.

If a state is not safe, the system must refuse to enter it.
