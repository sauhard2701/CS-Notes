# Operating Systems - Overview
<!-- GFM-TOC -->
* [Operating Systems - Overview](#operating-systems---overview)
    * [Basic Characteristics](#basic-characteristics)
        * [1. Concurrency](#_1-concurrency)
        * [2. Sharing](#_2-sharing)
        * [3. Virtualization](#_3-virtualization)
        * [4. Asynchrony](#_4-asynchrony)
    * [Basic Functions](#basic-functions)
        * [1. Process Management](#_1-process-management)
        * [2. Memory Management](#_2-memory-management)
        * [3. File Management](#_3-file-management)
        * [4. Device Management](#_4-device-management)
    * [System Calls](#system-calls)
    * [Monolithic Kernel and Microkernel](#monolithic-kernel-and-microkernel)
        * [1. Monolithic Kernel](#_1-monolithic-kernel)
        * [2. Microkernel](#_2-microkernel)
    * [Interrupt Classification](#interrupt-classification)
        * [1. External Interrupts](#_1-external-interrupts)
        * [2. Exceptions](#_2-exceptions)
        * [3. Trap](#_3-trap)
<!-- GFM-TOC -->


## Basic Characteristics

### 1. Concurrency

Concurrency means multiple programs can run during the same period from a macroscopic view, while parallelism means multiple instructions can run at the same instant.

Parallelism requires hardware support, such as multiple pipelines, multicore processors, or distributed computing systems.

Operating systems introduce processes and threads so programs can run concurrently.

### 2. Sharing

Sharing means resources in the system can be used by multiple concurrent processes.

There are two sharing modes: mutually exclusive sharing and simultaneous sharing.

Resources shared mutually exclusively are called critical resources, such as printers. Only one process can access them at a time, so synchronization mechanisms are needed to enforce mutual exclusion.

### 3. Virtualization

Virtualization turns one physical entity into multiple logical entities.

There are two main virtualization techniques: time-division multiplexing and space-division multiplexing.

Multiple processes can execute concurrently on the same processor using time-division multiplexing. Each process takes turns occupying the processor, executing for only a small time slice before quickly switching.

Virtual memory uses space-division multiplexing. It abstracts physical memory as address spaces, with each process having its own address space. Pages in the address space are mapped to physical memory, but not all pages need to reside in physical memory. When a page not in physical memory is used, a page replacement algorithm brings that page into memory.

### 4. Asynchrony

Asynchrony means a process does not execute to completion all at once; instead, it progresses intermittently at an unpredictable speed.

## Basic Functions

### 1. Process Management

Process control, process synchronization, process communication, deadlock handling, processor scheduling, and so on.

### 2. Memory Management

Memory allocation, address mapping, memory protection and sharing, virtual memory, and so on.

### 3. File Management

File storage-space management, directory management, file read/write management, protection, and so on.

### 4. Device Management

Completes user I/O requests, makes devices easier for users to use, and improves device utilization.

It mainly includes buffer management, device allocation, device handling, virtual devices, and so on.

## System Calls

If a process in user mode needs kernel-mode functionality, it makes a system call to trap into the kernel, and the operating system completes the operation on its behalf.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/tGPV0.png" width="600"/> </div><br>

Linux system calls mainly include the following:

| Task | Commands |
| :---: | --- |
| Process control | fork(); exit(); wait(); |
| Process communication | pipe(); shmget(); mmap(); |
| File operations | open(); read(); write(); |
| Device operations | ioctl(); read(); write(); |
| Information maintenance | getpid(); alarm(); sleep(); |
| Security | chmod(); umask(); chown(); |

## Monolithic Kernel and Microkernel

### 1. Monolithic Kernel

A monolithic kernel places operating system functionality in the kernel as a tightly integrated whole.

Because modules share information, performance is high.

### 2. Microkernel

As operating systems become increasingly complex, some operating system functionality is moved out of the kernel to reduce kernel complexity. The moved-out parts are divided into independent services according to layering principles.

In a microkernel architecture, the operating system is divided into small, well-defined modules. Only the microkernel itself runs in kernel mode; the remaining modules run in user mode.

Because frequent switching between user mode and kernel mode is required, there is some performance loss.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2_14_microkernelArchitecture.jpg"/> </div><br>

## Interrupt Classification

### 1. External Interrupts

Caused by events other than CPU instruction execution, such as an I/O completion interrupt, which indicates that device input/output processing has completed and the processor can send the next input/output request. Other examples include clock interrupts and console interrupts.

### 2. Exceptions

Caused by internal events during CPU instruction execution, such as illegal opcodes, address out-of-bounds errors, arithmetic overflow, and so on.

### 3. Trap

Using a system call in a user program.
