# Operating Systems - Device Management
<!-- GFM-TOC -->
* [Operating Systems - Device Management](#operating-systems---device-management)
    * [Disk Structure](#disk-structure)
    * [Disk Scheduling Algorithms](#disk-scheduling-algorithms)
        * [1. First-Come First-Served](#_1-first-come-first-served)
        * [2. Shortest Seek Time First](#_2-shortest-seek-time-first)
        * [3. Elevator Algorithm](#_3-elevator-algorithm)
<!-- GFM-TOC -->


## Disk Structure

- Platter: a disk contains multiple platters.
- Track: a circular band on a platter; one platter can contain multiple tracks.
- Sector: an arc segment on a track. One track can contain multiple sectors. It is the smallest physical storage unit, currently mainly in sizes of 512 bytes and 4 KB.
- Head: located very close to the platter. It converts magnetic fields on the platter into electrical signals for reads, or converts electrical signals into magnetic fields on the platter for writes.
- Actuator arm: moves the head between tracks.
- Spindle: rotates the entire platter.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/014fbc4d-d873-4a12-b160-867ddaed9807.jpg"/> </div><br>

## Disk Scheduling Algorithms

The time to read or write a disk block is affected by:

- Rotational latency, where the spindle rotates the platter so the head reaches the proper sector.
- Seek time, where the actuator arm moves the head to the proper track.
- Actual data transfer time.

Among these, seek time is the longest, so the main goal of disk scheduling is to minimize the average seek time.

### 1. First-Come First-Served

> FCFS, First Come First Served

Schedule disk requests in their arrival order.

The advantages are fairness and simplicity. The drawback is also clear: because it does not optimize seeks, the average seek time can be relatively long.

### 2. Shortest Seek Time First

> SSTF, Shortest Seek Time First

Prioritize the track closest to the current head position.

Although the average seek time is lower, it is not fair enough. If newly arriving track requests are always closer than a waiting request, the waiting request may keep waiting forever, causing starvation. In particular, requests at the two ends of the disk are more likely to starve.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/4e2485e4-34bd-4967-9f02-0c093b797aaa.png"/> </div><br>

### 3. Elevator Algorithm

> SCAN

An elevator keeps moving in one direction until there are no requests in that direction, then changes direction.

The elevator algorithm, also called the SCAN algorithm, is similar to how an elevator runs. Disk requests are always scheduled in one direction until there are no pending requests in that direction, then the direction changes.

Because movement direction is considered, all disk requests will eventually be served, solving SSTF's starvation problem.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/271ce08f-c124-475f-b490-be44fedc6d2e.png"/> </div><br>
