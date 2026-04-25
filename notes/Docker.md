# Docker
<!-- GFM-TOC -->
* [Docker](#docker)
    * [1. Problems Solved](#1-problems-solved)
    * [2. Comparison with Virtual Machines](#2-comparison-with-virtual-machines)
    * [3. Advantages](#3-advantages)
    * [4. Use Cases](#4-use-cases)
    * [5. Images and Containers](#5-images-and-containers)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Problems Solved

Different machines have different operating systems, libraries, and components, so deploying an application to multiple machines requires a large amount of environment configuration.

Docker mainly solves environment configuration problems. It is a virtualization technology that isolates processes; isolated processes are independent of the host operating system and other isolated processes. With Docker, existing applications can be deployed to other machines without modifying application code or requiring developers to learn technologies specific to a particular environment.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/011f3ef6-d824-4d43-8b2c-36dab8eaaa72-1.png" width="400px"/> </div><br>

## 2. Comparison with Virtual Machines

A virtual machine is also a virtualization technology. The biggest difference from Docker is that it works by simulating hardware and installing an operating system on that hardware.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/be608a77-7b7f-4f8e-87cc-f2237270bf69.png" width="500"/> </div><br>

### Startup Speed

Starting a virtual machine requires starting the VM operating system first and then starting the application, which is very slow;

starting Docker is equivalent to starting a process on the host operating system.

### Resource Usage

A virtual machine is a complete operating system and consumes a large amount of disk, memory, and CPU resources, so one machine can run only dozens of virtual machines.

Docker is only a process. It only needs to package the application and related components, consumes very few resources at runtime, and one machine can run thousands of Docker containers.

## 3. Advantages

Besides fast startup and low resource usage, Docker has the following advantages:

### Easier Migration

It provides a consistent runtime environment. A packaged application can be migrated across different machines without worrying that environment changes will prevent it from running.

### Easier Maintenance

It uses layering and images so applications can more easily reuse repeated parts. The higher the reuse, the easier maintenance becomes.

### Easier Scaling

Base images can be extended to create new images, and the official ecosystem and open-source community provide many images. Extending these images makes it easy to obtain the images we need.

## 4. Use Cases

### Continuous Integration

Continuous integration means frequently integrating code into the main branch so errors can be discovered faster.

Docker is lightweight and isolated, so integrating code into one Docker container does not affect other containers.

### Scalable Cloud Services

Docker containers can be easily added or removed according to application load.

### Microservice Architecture

Docker's lightweight nature makes it well suited for deploying, maintaining, and composing microservices.

## 5. Images and Containers

An image is a static structure, similar to a class in object-oriented programming, while a container is an instance of an image.

An image contains the code and other components needed when a container runs. It is a layered structure, and each layer is read-only. When an image is built, it is built layer by layer, with each previous layer serving as the foundation for the next. This layered storage structure is well suited for image reuse and customization.

When a container is created, a writable layer is added on top of the image to store modifications made while the container runs.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/docker-filesystems-busyboxrw.png"/> </div><br>

## References

- [DOCKER 101: INTRODUCTION TO DOCKER WEBINAR RECAP](https://blog.docker.com/2017/08/docker-101-introduction-docker-webinar-recap/)
- [Docker Getting Started Tutorial](http://www.ruanyifeng.com/blog/2018/02/docker-tutorial.html)
- [Docker container vs Virtual machine](http://www.bogotobogo.com/DevOps/Docker/Docker_Container_vs_Virtual_Machine.php)
- [How to Create Docker Container using Dockerfile](https://linoxide.com/linux-how-to/dockerfile-create-docker-container/)
- [Understanding Docker (2): Docker Images](http://www.cnblogs.com/sammyliu/p/5877964.html)
- [Why Use Docker?](https://yeasy.gitbooks.io/docker_practice/introduction/why.html)
- [What is Docker](https://www.docker.com/what-docker)
- [What Is Continuous Integration?](http://www.ruanyifeng.com/blog/2015/09/continuous-integration.html)

