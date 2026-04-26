# Operating Systems - Memory Management
<!-- GFM-TOC -->
* [Operating Systems - Memory Management](#operating-systems---memory-management)
    * [Virtual Memory](#virtual-memory)
    * [Paged Address Translation](#paged-address-translation)
    * [Page Replacement Algorithms](#page-replacement-algorithms)
        * [1. Optimal](#_1-optimal)
        * [2. Least Recently Used](#_2-least-recently-used)
        * [3. Not Recently Used](#_3-not-recently-used)
        * [4. First-In First-Out](#_4-first-in-first-out)
        * [5. Second-Chance Algorithm](#_5-second-chance-algorithm)
        * [6. Clock](#_6-clock)
    * [Segmentation](#segmentation)
    * [Segmented Paging](#segmented-paging)
    * [Paging vs Segmentation](#paging-vs-segmentation)
<!-- GFM-TOC -->


## Virtual Memory

The purpose of virtual memory is to extend physical memory into a larger logical memory space, giving programs more usable memory.

To manage memory better, the operating system abstracts memory as an address space. Each program has its own address space, which is divided into multiple blocks called pages. These pages are mapped to physical memory, but they do not need to map to contiguous physical memory, and not all pages need to be in physical memory. When a program references a page that is not in physical memory, hardware performs the necessary mapping, loads the missing page into physical memory, and re-executes the failed instruction.

As the description above shows, virtual memory allows a program to run without mapping every page in its address space to physical memory. In other words, a program does not need to be loaded entirely into memory to run, making it possible to run large programs with limited memory. For example, if a computer can generate 16-bit addresses, a program's address space ranges from 0\~64K. If the computer has only 32KB of physical memory, virtual memory allows it to run a 64K program.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7b281b1e-0595-402b-ae35-8c91084c33c1.png"/> </div><br>

## Paged Address Translation

The memory management unit (MMU) manages translation between address space and physical memory. The page table stores mappings between pages, which belong to the program address space, and page frames, which belong to physical memory.

A virtual address is divided into two parts: one stores the page number, and the other stores the offset.

The page table below stores 16 pages, which require 4 bits for indexing. For example, for the virtual address (0010 000000000100), the first 4 bits store page number 2. The page table entry is (110 1), where the last bit indicates whether the page is present in memory; 1 means present. The last 12 bits store the offset. The address of this page's corresponding page frame is (110 000000000100).

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/cf4386a1-58c9-4eca-a17f-e12b1e9770eb.png" width="500"/> </div><br>

## Page Replacement Algorithms

During program execution, if the page to be accessed is not in memory, a page fault occurs and the page is loaded into memory. If there is no free memory at that time, the system must swap one page out of memory to disk swap space to make room.

Page replacement algorithms are similar to cache eviction policies. Memory can be viewed as a cache for the disk. In a cache system, cache size is limited. When new cached data arrives, some existing cached data must be evicted to make room.

The main goal of page replacement algorithms is to minimize the page replacement rate, or equivalently the page fault rate.

### 1. Optimal

> OPT, Optimal replacement algorithm

The selected page to evict is the one that will not be accessed for the longest time, which usually guarantees the lowest page fault rate.

This is a theoretical algorithm because it is impossible to know how long it will be before a page is accessed again.

Example: a system allocates three physical frames to a process and has the following page reference sequence:

```html
7，0，1，2，0，3，0，4，2，3，0，3，2，1，2，0，1，7，0，1
```

At the start, pages 7, 0, and 1 are loaded into memory. When the process accesses page 2, a page fault occurs, and page 7 is swapped out because it will be accessed again farthest in the future.

### 2. Least Recently Used

> LRU, Least Recently Used

Although future page usage cannot be known, past page usage can be observed. LRU evicts the page that has not been used for the longest time.

To implement LRU, maintain a linked list of all pages in memory. When a page is accessed, move it to the head of the list. This ensures that the page at the tail is the least recently used.

Because every access requires updating the linked list, this implementation of LRU is expensive.

```html
4，7，0，7，1，0，1，2，1，2，6
```

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/eb859228-c0f2-4bce-910d-d9f76929352b.png"/> </div><br>
### 3. Not Recently Used

> NRU, Not Recently Used

Each page has two status bits: R and M. When a page is accessed, R is set to 1; when a page is modified, M is set to 1. The R bit is cleared periodically. Pages can be divided into the following four classes:

- R=0，M=0
- R=0，M=1
- R=1，M=0
- R=1，M=1

When a page fault occurs, the NRU algorithm randomly selects a page from the non-empty class with the smallest class number and evicts it.

NRU prefers to evict modified dirty pages (R=0, M=1) instead of frequently used clean pages (R=1, M=0).

### 4. First-In First-Out

> FIFO, First In First Out

The selected page to evict is the one that entered first.

This algorithm may evict frequently accessed pages, increasing the page fault rate.

### 5. Second-Chance Algorithm

FIFO may replace frequently used pages. To avoid this problem, make a simple modification:

When a page is accessed, either read or written, set its R bit to 1. When replacement is needed, check the R bit of the oldest page. If R is 0, the page is both old and unused, so it can be replaced immediately. If R is 1, clear R to 0, move the page to the tail of the list, update its load time as if it had just been loaded, and continue searching from the head of the list.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ecf8ad5d-5403-48b9-b6e7-f2e20ffe8fca.png"/> </div><br>

### 6. Clock

> Clock

The second-chance algorithm needs to move pages in a linked list, reducing efficiency. The clock algorithm connects pages with a circular linked list and uses a pointer to refer to the oldest page.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/5f5ef0b6-98ea-497c-a007-f6c55288eab1.png"/> </div><br>

## Segmentation

Virtual memory uses paging, which divides the address space into fixed-size pages and maps each page to memory.

The figure below shows multiple tables created by a compiler during compilation. Four of these tables grow dynamically. If a one-dimensional address space from a paging system is used, dynamic growth can cause overlap problems.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/22de0538-7c6e-4365-bd3b-8ce3c5900216.png"/> </div><br>

Segmentation divides each table into segments. Each segment forms an independent address space. Segment lengths can differ and can grow dynamically.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e0900bb2-220a-43b7-9aa9-1d5cd55ff56e.png"/> </div><br>

## Segmented Paging

A program's address space is divided into multiple segments with independent address spaces, and each segment's address space is divided into pages of equal size. This provides both the sharing and protection of segmentation and the virtual memory capability of paging.

## Paging vs Segmentation

- Transparency to programmers: paging is transparent, while segmentation requires programmers to explicitly divide each segment.

- Address-space dimensions: paging uses a one-dimensional address space, while segmentation is two-dimensional.

- Whether size can change: page size is fixed, while segment size can change dynamically.

- Reason for existence: paging is mainly used to implement virtual memory and obtain a larger address space; segmentation is mainly used to divide programs and data into logically independent address spaces and helps with sharing and protection.
