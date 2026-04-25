# Operating Systems - Process Management
<!-- GFM-TOC -->
* [Operating Systems - Process Management](#operating-systems---process-management)
    * [Processes and Threads](#processes-and-threads)
        * [1. Process](#1-process)
        * [2. Thread](#2-thread)
        * [3. Differences](#3-differences)
    * [Process State Transitions](#process-state-transitions)
    * [Process Scheduling Algorithms](#process-scheduling-algorithms)
        * [1. Batch Systems](#1-batch-systems)
        * [2. Interactive Systems](#2-interactive-systems)
        * [3. Real-Time Systems](#3-real-time-systems)
    * [Process Synchronization](#process-synchronization)
        * [1. Critical Section](#1-critical-section)
        * [2. Synchronization and Mutual Exclusion](#2-synchronization-and-mutual-exclusion)
        * [3. Semaphore](#3-semaphore)
        * [4. Monitor](#4-monitor)
    * [Classic Synchronization Problems](#classic-synchronization-problems)
        * [1. Dining Philosophers Problem](#1-dining-philosophers-problem)
        * [2. Readers-Writers Problem](#2-readers-writers-problem)
    * [Interprocess Communication](#interprocess-communication)
        * [1. Pipes](#1-pipes)
        * [2. FIFO](#2-fifo)
        * [3. Message Queues](#3-message-queues)
        * [4. Semaphore](#4-semaphore)
        * [5. Shared Memory](#5-shared-memory)
        * [6. Sockets](#6-sockets)
<!-- GFM-TOC -->


## Processes and Threads

### 1. Process

A process is the basic unit of resource allocation.

The Process Control Block (PCB) describes a process's basic information and running state. Creating and terminating a process are both operations on the PCB.

The following figure shows four programs creating four processes. These four processes can execute concurrently.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a6ac2b08-3861-4e85-baa8-382287bfee9f.png"/> </div><br>

### 2. Thread

A thread is the basic unit of independent scheduling.

A process can contain multiple threads, and they share the process's resources.

QQ and a browser are two processes. A browser process contains many threads, such as HTTP request threads, event response threads, rendering threads, and so on. Concurrent execution of threads allows the browser to respond to other user events while initiating an HTTP request after the user clicks a new link.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/3cd630ea-017c-488d-ad1d-732b4efeddf5.png"/> </div><br>

### 3. Differences

I. Resource Ownership

A process is the basic unit of resource allocation, but a thread does not own resources. A thread can access resources belonging to its process.

II. Scheduling

A thread is the basic unit of independent scheduling. Switching threads within the same process does not cause a process switch, while switching from a thread in one process to a thread in another process does cause a process switch.

III. System Overhead

When creating or terminating a process, the system must allocate or reclaim resources such as memory space and I/O devices, so the overhead is much greater than creating or terminating a thread. Similarly, process switching involves saving the CPU context of the current process and setting up the CPU context of the newly scheduled process, while thread switching only needs to save and set a small number of registers, so the overhead is low.

IV. Communication

Threads can communicate by directly reading and writing data in the same process, while process communication requires IPC.

## Process State Transitions

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ProcessState.png" width="500"/> </div><br>

- Ready state: waiting to be scheduled
- Running state
- Waiting state: waiting for resources

Note the following:

- Only ready and running states can transition to each other; all other transitions are one-way. A process in the ready state obtains CPU time through the scheduling algorithm and becomes running. A running process becomes ready after its allocated CPU time slice is exhausted, waiting for the next scheduling.
- The waiting state is reached from the running state because required resources are unavailable, but those resources do not include CPU time. Lack of CPU time changes a process from running to ready.

## Process Scheduling Algorithms

Scheduling algorithms have different goals in different environments, so they should be discussed by environment.

### 1. Batch Systems

Batch systems do not have many user operations. In such systems, scheduling algorithms aim to guarantee throughput and turnaround time, which is the time from submission to termination.

**1.1 First-Come, First-Served (FCFS)**  

A non-preemptive scheduling algorithm that schedules jobs in request order.

It favors long jobs but is unfavorable to short jobs, because short jobs must wait until earlier long jobs finish, and long jobs take a long time to execute. This causes excessive waiting time for short jobs.

**1.2 Shortest Job First (SJF)**  

A non-preemptive scheduling algorithm that schedules jobs in ascending order of estimated running time.

Long jobs may starve, waiting indefinitely for short jobs to finish. If short jobs keep arriving, long jobs may never be scheduled.

**1.3 Shortest Remaining Time Next (SRTN)**  

The preemptive version of shortest job first. It schedules by remaining running time. When a new job arrives, its total running time is compared with the current process's remaining time. If the new process needs less time, the current process is suspended and the new process runs. Otherwise, the new process waits.

### 2. Interactive Systems

Interactive systems have many user interactions. In such systems, scheduling algorithms aim to respond quickly.

**2.1 Round Robin**  

All ready processes are arranged in a queue according to FCFS. At each scheduling event, CPU time is allocated to the process at the front of the queue, and that process can execute for one time slice. When the time slice is exhausted, the timer issues a clock interrupt, and the scheduler stops the process, sends it to the end of the ready queue, and continues allocating CPU time to the process at the front of the queue.

The efficiency of round-robin scheduling is closely related to the time-slice size:

- Process switching must save the current process information and load the new process information. If the time slice is too small, process switching becomes too frequent and too much time is spent on switching.
- If the time slice is too long, real-time responsiveness cannot be guaranteed.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/8c662999-c16c-481c-9f40-1fdba5bc9167.png"/> </div><br>

**2.2 Priority Scheduling**  

Assign each process a priority and schedule according to priority.

To prevent low-priority processes from waiting forever, increase the priority of waiting processes over time.

**2.3 Multilevel Feedback Queue**  

If a process needs to execute for 100 time slices, round-robin scheduling requires 100 switches.

Multilevel queues are designed for processes that need to execute across multiple consecutive time slices. They set up multiple queues, each with a different time-slice size, such as 1, 2, 4, 8, and so on. If a process does not finish in the first queue, it is moved to the next queue. With this approach, the previous process only needs 7 switches.

Each queue also has a different priority, with the top queue having the highest priority. Therefore, a process in the current queue can be scheduled only when no process is waiting in the previous queue.

This scheduling algorithm can be viewed as a combination of round-robin scheduling and priority scheduling.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/042cf928-3c8e-4815-ae9c-f2780202c68f.png"/> </div><br>

### 3. Real-Time Systems

Real-time systems require a request to receive a response within a fixed time.

They are divided into hard real-time and soft real-time systems. The former must meet absolute deadlines, while the latter can tolerate some timeout.

## Process Synchronization

### 1. Critical Section

The code segment that accesses a critical resource is called a critical section.

To access critical resources mutually exclusively, each process must perform a check before entering the critical section.

```html
// entry section
// critical section;
// exit section
```

### 2. Synchronization and Mutual Exclusion

- Synchronization: a direct constraint relationship produced by cooperation among multiple processes, giving processes a certain execution order.
- Mutual exclusion: among multiple processes, only one process can enter the critical section at the same time.

### 3. Semaphore

A semaphore is an integer variable on which down and up operations can be performed, commonly known as P and V operations.

-   **down**: if the semaphore is greater than 0, decrement it by 1; if the semaphore equals 0, the process sleeps and waits until the semaphore is greater than 0.
-   **up**: increment the semaphore by 1 and wake a sleeping process so it can complete its down operation.

down and up operations must be designed as indivisible primitives. The usual approach is to disable interrupts while executing these operations.

If a semaphore can only be 0 or 1, it becomes a **mutex**. 0 means the critical section is locked, and 1 means the critical section is unlocked.

```c
typedef int semaphore;
semaphore mutex = 1;
void P1() {
    down(&mutex);
    // critical section
    up(&mutex);
}

void P2() {
    down(&mutex);
    // critical section
    up(&mutex);
}
```

\<font size=3\>   **Using Semaphores to Implement the Producer-Consumer Problem**   \</font\> \</br\>

Problem description: Use a buffer to store items. A producer can place an item only when the buffer is not full, and a consumer can take an item only when the buffer is not empty.

Because the buffer is a critical resource, a mutex is needed to control mutually exclusive access to the buffer.

To synchronize producer and consumer behavior, record the number of items in the buffer. Semaphores can be used for this count. Two semaphores are needed here: empty records the number of empty buffer slots, and full records the number of full buffer slots. The empty semaphore is used in the producer process; when empty is not 0, the producer can place an item. The full semaphore is used in the consumer process; when full is not 0, the consumer can take an item.

Note that the buffer must not be locked before testing the semaphore. In other words, do not execute down(mutex) before down(empty). If this is done, the following may happen: after the producer locks the buffer, it executes down(empty) and finds empty = 0, so the producer sleeps. The consumer cannot enter the critical section because the producer has locked the buffer, so the consumer cannot execute up(empty). empty stays 0 forever, causing the producer to wait forever without releasing the lock, and the consumer also waits forever.

```c
#define N 100
typedef int semaphore;
semaphore mutex = 1;
semaphore empty = N;
semaphore full = 0;

void producer() {
    while(TRUE) {
        int item = produce_item();
        down(&empty);
        down(&mutex);
        insert_item(item);
        up(&mutex);
        up(&full);
    }
}

void consumer() {
    while(TRUE) {
        down(&full);
        down(&mutex);
        int item = remove_item();
        consume_item(item);
        up(&mutex);
        up(&empty);
    }
}
```

### 4. Monitor

Implementing the producer-consumer problem with semaphores requires a lot of control in client code. A monitor separates the control code, making it less error-prone and easier for client code to call.

The C language does not support monitors. The following example uses a Pascal-like language to describe a monitor. The monitor in the example provides insert() and remove() methods, and client code solves the producer-consumer problem by calling these two methods.

```pascal
monitor ProducerConsumer
    integer i;
    condition c;

    procedure insert();
    begin
        // ...
    end;

    procedure remove();
    begin
        // ...
    end;
end monitor;
```

A monitor has an important property: only one process can use the monitor at a time. When a process cannot continue executing, it must not keep occupying the monitor; otherwise, other processes can never use it.

A monitor introduces **condition variables** and related operations, **wait()** and **signal()**, to implement synchronization. Performing wait() on a condition variable blocks the calling process and releases the monitor so another process can hold it. signal() is used to wake a blocked process.

<font size=3>  **Using Monitors to Implement the Producer-Consumer Problem**  </font><br>

```pascal
// monitor
monitor ProducerConsumer
    condition full, empty;
    integer count := 0;
    condition c;

    procedure insert(item: integer);
    begin
        if count = N then wait(full);
        insert_item(item);
        count := count + 1;
        if count = 1 then signal(empty);
    end;

    function remove: integer;
    begin
        if count = 0 then wait(empty);
        remove = remove_item;
        count := count - 1;
        if count = N -1 then signal(full);
    end;
end monitor;

// producer client
procedure producer
begin
    while true do
    begin
        item = produce_item;
        ProducerConsumer.insert(item);
    end
end;

// consumer client
procedure consumer
begin
    while true do
    begin
        item = ProducerConsumer.remove;
        consume_item(item);
    end
end;
```

## Classic Synchronization Problems

The producer-consumer problem has already been discussed above.

### 1. Dining Philosophers Problem

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a9077f06-7584-4f2b-8c20-3a8e46928820.jpg"/> </div><br>

Five philosophers sit around a round table, with food in front of each philosopher. A philosopher alternates between two activities: eating and thinking. When a philosopher eats, they must first pick up the two chopsticks on their left and right, and they can pick up only one chopstick at a time.

The following is an incorrect solution. If all philosophers pick up the chopstick on their left at the same time, every philosopher waits for another philosopher to finish eating and release a chopstick, causing deadlock.

```c
#define N 5

void philosopher(int i) {
    while(TRUE) {
        think();
        take(i);       // pick up the left chopstick
        take((i+1)%N); // pick up the right chopstick
        eat();
        put(i);
        put((i+1)%N);
    }
}
```

To prevent deadlock, set two conditions:

- Both left and right chopsticks must be picked up at the same time.
- A philosopher is allowed to eat only when neither neighbor is eating.

```c
#define N 5
#define LEFT (i + N - 1) % N // left neighbor
#define RIGHT (i + 1) % N    // right neighbor
#define THINKING 0
#define HUNGRY   1
#define EATING   2
typedef int semaphore;
int state[N];                // track each philosopher's state
semaphore mutex = 1;         // mutual exclusion for the critical section; state is the critical array and must be modified mutually exclusively
semaphore s[N];              // one semaphore per philosopher

void philosopher(int i) {
    while(TRUE) {
        think(i);
        take_two(i);
        eat(i);
        put_two(i);
    }
}

void take_two(int i) {
    down(&mutex);
    state[i] = HUNGRY;
    check(i);
    up(&mutex);
    down(&s[i]); // can start eating only after receiving notification; otherwise waits forever
}

void put_two(i) {
    down(&mutex);
    state[i] = THINKING;
    check(LEFT); // try to notify the left and right neighbors that this philosopher has finished eating, so they can start
    check(RIGHT);
    up(&mutex);
}

void eat(int i) {
    down(&mutex);
    state[i] = EATING;
    up(&mutex);
}

// Check whether both neighbors are not eating; if so, call up(&s[i]) so down(&s[i]) is notified and can continue.
void check(i) {         
    if(state[i] == HUNGRY && state[LEFT] != EATING && state[RIGHT] !=EATING) {
        state[i] = EATING;
        up(&s[i]);
    }
}
```

### 2. Readers-Writers Problem

Multiple processes are allowed to read data at the same time, but reads and writes, as well as writes and writes, are not allowed to occur simultaneously.

An integer variable count records the number of processes reading the data. A mutex count_mutex is used to lock count, and a mutex data_mutex is used to lock the data being read or written.

```c
typedef int semaphore;
semaphore count_mutex = 1;
semaphore data_mutex = 1;
int count = 0;

void reader() {
    while(TRUE) {
        down(&count_mutex);
        count++;
        if(count == 1) down(&data_mutex); // the first reader locks the data to prevent writer access
        up(&count_mutex);
        read();
        down(&count_mutex);
        count--;
        if(count == 0) up(&data_mutex);
        up(&count_mutex);
    }
}

void writer() {
    while(TRUE) {
        down(&data_mutex);
        write();
        up(&data_mutex);
    }
}
```

The following content was provided by [@Bandi Yugandhar](https://github.com/yugandharbandi).

The first case may result Writer to starve. This case favous Writers i.e no writer, once added to the queue, shall be kept waiting longer than absolutely necessary(only when there are readers that entered the queue before the writer).

```c
int readcount, writecount;                   //(initial value = 0)
semaphore rmutex, wmutex, readLock, resource; //(initial value = 1)

//READER
void reader() {
<ENTRY Section>
 down(&readLock);                 //  reader is trying to enter
 down(&rmutex);                  //   lock to increase readcount
  readcount++;                 
  if (readcount == 1)          
   down(&resource);              //if you are the first reader then lock  the resource
 up(&rmutex);                  //release  for other readers
 up(&readLock);                 //Done with trying to access the resource

<CRITICAL Section>
//reading is performed

<EXIT Section>
 down(&rmutex);                  //reserve exit section - avoids race condition with readers
 readcount--;                       //indicate you're leaving
  if (readcount == 0)          //checks if you are last reader leaving
   up(&resource);              //if last, you must release the locked resource
 up(&rmutex);                  //release exit section for other readers
}

//WRITER
void writer() {
  <ENTRY Section>
  down(&wmutex);                  //reserve entry section for writers - avoids race conditions
  writecount++;                //report yourself as a writer entering
  if (writecount == 1)         //checks if you're first writer
   down(&readLock);               //if you're first, then you must lock the readers out. Prevent them from trying to enter CS
  up(&wmutex);                  //release entry section

<CRITICAL Section>
 down(&resource);                //reserve the resource for yourself - prevents other writers from simultaneously editing the shared resource
  //writing is performed
 up(&resource);                //release file

<EXIT Section>
  down(&wmutex);                  //reserve exit section
  writecount--;                //indicate you're leaving
  if (writecount == 0)         //checks if you're the last writer
   up(&readLock);               //if you're last writer, you must unlock the readers. Allows them to try enter CS for reading
  up(&wmutex);                  //release exit section
}
```

We can observe that every reader is forced to acquire ReadLock. On the otherhand, writers doesn’t need to lock individually. Once the first writer locks the ReadLock, it will be released only when there is no writer left in the queue.

From the both cases we observed that either reader or writer has to starve. Below solutionadds the constraint that no thread shall be allowed to starve; that is, the operation of obtaining a lock on the shared data will always terminate in a bounded amount of time.

```source-c
int readCount;                  // init to 0; number of readers currently accessing resource

// all semaphores initialised to 1
Semaphore resourceAccess;       // controls access (read/write) to the resource
Semaphore readCountAccess;      // for syncing changes to shared variable readCount
Semaphore serviceQueue;         // FAIRNESS: preserves ordering of requests (signaling must be FIFO)

void writer()
{ 
    down(&serviceQueue);           // wait in line to be servicexs
    // <ENTER>
    down(&resourceAccess);         // request exclusive access to resource
    // </ENTER>
    up(&serviceQueue);           // let next in line be serviced

    // <WRITE>
    writeResource();            // writing is performed
    // </WRITE>

    // <EXIT>
    up(&resourceAccess);         // release resource access for next reader/writer
    // </EXIT>
}

void reader()
{ 
    down(&serviceQueue);           // wait in line to be serviced
    down(&readCountAccess);        // request exclusive access to readCount
    // <ENTER>
    if (readCount == 0)         // if there are no readers already reading:
        down(&resourceAccess);     // request resource access for readers (writers blocked)
    readCount++;                // update count of active readers
    // </ENTER>
    up(&serviceQueue);           // let next in line be serviced
    up(&readCountAccess);        // release access to readCount

    // <READ>
    readResource();             // reading is performed
    // </READ>

    down(&readCountAccess);        // request exclusive access to readCount
    // <EXIT>
    readCount--;                // update count of active readers
    if (readCount == 0)         // if there are no readers left:
        up(&resourceAccess);     // release resource access for all
    // </EXIT>
    up(&readCountAccess);        // release access to readCount
}

```

## Interprocess Communication

Process synchronization and interprocess communication are easy to confuse. Their difference is:

- Process synchronization: controls multiple processes to execute in a certain order.
- Interprocess communication: transfers information between processes.

Interprocess communication is a means, while process synchronization is a goal. In other words, to achieve process synchronization, processes need to communicate and transfer information required for synchronization.

### 1. Pipes

A pipe is created by calling the pipe function. fd[0] is used for reading, and fd[1] is used for writing.

```c
#include <unistd.h>
int pipe(int fd[2]);
```

It has the following limitations:

- It only supports half-duplex communication, meaning one-way alternating transmission.
- It can only be used between parent-child processes or sibling processes.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/53cd9ade-b0a6-4399-b4de-7f1fbd06cdfb.png"/> </div><br>

### 2. FIFO

Also called a named pipe, it removes the limitation that pipes can only be used between parent-child processes.

```c
#include <sys/stat.h>
int mkfifo(const char *path, mode_t mode);
int mkfifoat(int fd, const char *path, mode_t mode);
```

FIFO is often used in client-server applications. FIFO acts as a rendezvous point to pass data between client and server processes.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2ac50b81-d92a-4401-b9ec-f2113ecc3076.png"/> </div><br>

### 3. Message Queues

Compared with FIFO, message queues have the following advantages:

- Message queues can exist independently of reader and writer processes, avoiding difficulties that may occur when opening and closing synchronous pipes in FIFO.
- They avoid FIFO's synchronous blocking problem and do not require processes to provide their own synchronization methods.
- Reader processes can selectively receive messages by message type, unlike FIFO, which can only receive by default.

### 4. Semaphore

It is a counter used to provide multiple processes with access to shared data objects.

### 5. Shared Memory

Allows multiple processes to share a given storage area. Because data does not need to be copied between processes, this is the fastest form of IPC.

Semaphores are needed to synchronize access to shared storage.

Multiple processes can map the same file into their address spaces to implement shared memory. In addition, XSI shared memory does not use files; it uses anonymous memory segments.

### 6. Sockets

Unlike other communication mechanisms, sockets can be used for communication between processes on different machines.
