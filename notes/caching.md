# Caching
<!-- GFM-TOC -->
* [Caching](#caching)
    * [1. Cache Characteristics](#1-cache-characteristics)
    * [2. Cache Locations](#2-cache-locations)
    * [3. CDN](#3-cdn)
    * [4. Cache Problems](#4-cache-problems)
    * [5. Data Distribution](#5-data-distribution)
    * [6. Consistent Hashing](#6-consistent-hashing)
    * [7. LRU](#7-lru)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Cache Characteristics

### Hit Rate

When a request can be answered by accessing the cache, it is called a cache hit.

The higher the cache hit rate, the higher the cache utilization.

### Maximum Space

Caches are usually located in memory, and memory space is usually much smaller than disk space, so the maximum cache space cannot be very large.

When the amount of data stored in the cache exceeds the maximum space, some data must be evicted to store newly arrived data.

### Eviction Policy

- FIFO (First In First Out): a first-in-first-out policy. In real-time scenarios where the newest data needs to be accessed frequently, FIFO can be used so that the earliest entered data, which is the oldest data, is evicted.

- LRU (Least Recently Used): evicts the data that has not been used for the longest time, meaning the data whose last access time is farthest from now. This policy can keep hot data, that is, frequently accessed data, in memory and thus maintain the cache hit rate.

- LFU (Least Frequently Used): evicts the data used least often over a period of time.

## 2. Cache Locations

### Browser

When an HTTP response allows caching, the browser caches static resources such as HTML, CSS, JavaScript, and images.

### ISP

An Internet Service Provider (ISP) is the first hop for network access. Caching data in the ISP can greatly improve user access speed.

### Reverse Proxy

A reverse proxy sits in front of the server, and both requests and responses pass through it. By caching data in the reverse proxy, cached responses can be used directly when users request the reverse proxy.

### Local Cache

Use Guava Cache to cache data in the server's local memory. Server code can directly read the cache from local memory, which is very fast.

### Distributed Cache

Use distributed caches such as Redis and Memcache to cache data in a distributed cache system.

Compared with local cache, distributed cache is deployed separately and can allocate hardware resources according to demand. In addition, server clusters can all access the distributed cache, while local caches need to be synchronized between servers in the cluster, which is difficult to implement and has high performance overhead.

### Database Cache

Database management systems such as MySQL have their own query cache mechanisms to improve query efficiency.

### Java Internal Cache

To optimize space and improve the creation efficiency of strings and primitive wrapper classes, Java designed the string constant pool and buffer pools for the six wrapper classes Byte, Short, Character, Integer, Long, and Boolean.

### CPU Multi-Level Cache

To solve the mismatch between computation speed and main-memory IO speed, CPUs introduce multi-level cache structures and use cache consistency protocols such as MESI to solve cache data consistency problems in multi-core CPUs.

## 3. CDN

A Content Distribution Network (CDN) is an interconnected network system that uses servers closer to users to distribute static resources such as HTML, CSS, JavaScript, music, images, and videos faster and more reliably.

CDN mainly has the following advantages:

- Distributes data to users faster.
- Improves overall system bandwidth performance by deploying multiple servers.
- Multiple servers can be viewed as a redundancy mechanism, providing high availability.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/15313ed8-a520-4799-a300-2b6b36be314f.jpg"/> </div><br>

## 4. Cache Problems

### Cache Penetration

This refers to requesting data that definitely does not exist. The request penetrates the cache and reaches the database.

Solutions:

- Cache empty data for these nonexistent entries.
- Filter this type of request.

### Cache Avalanche

This refers to a situation where a large number of requests reach the database because data has not been loaded into the cache, cached data expires over a large area at the same time, or cache servers go down.

In a system with caching, the system depends heavily on the cache, and the cache handles a large portion of data requests. When a cache avalanche occurs, the database cannot handle such a large number of requests, causing it to crash.

Solutions:

- To prevent a cache avalanche caused by large-scale cache expiration at the same time, observe user behavior and set reasonable cache expiration times.
- To prevent a cache avalanche caused by cache server downtime, use distributed caching. Each node in a distributed cache stores only part of the data, so when one node goes down, caches on other nodes remain available.
- Cache warming can also be performed to avoid a cache avalanche shortly after system startup, before large amounts of data have been cached.


### Cache Consistency

Cache consistency requires cached data to be updated in real time when the data itself is updated.

Solutions:

- Update the cache immediately when the data is updated.
- Before reading the cache, first check whether it is up to date; if it is not, update it first.

Ensuring cache consistency has a high cost. Cached data is best suited for data with low consistency requirements, where some dirty data is acceptable.

### Cache Bottomless Pit

This refers to a situation where many cache nodes are added to meet business requirements, but performance decreases instead of improving.

Cause: cache systems usually use a hash function to map keys to corresponding cache nodes. As the number of cache nodes increases, keys are distributed across more nodes, causing one client batch operation to involve multiple network operations. This means the time consumed by batch operations increases as the number of nodes increases. In addition, more network connections also affect node performance.

Solutions:

- Optimize batch data operation commands.
- Reduce the number of network communications.
- Lower access costs by using long connections, connection pools, NIO, and similar techniques.

## 5. Data Distribution

### Hash Distribution

Hash distribution calculates the hash value of data and assigns the data to different nodes based on that hash value. For example, if there are N nodes and the primary key of the data is key, the node number assigned to the data is: hash(key)%N.

Traditional hash distribution has one problem: when the number of nodes changes, meaning N changes, almost all data must be redistributed, causing a large amount of data migration.

### Sequential Distribution

Divide data into multiple continuous parts and distribute them to different nodes by data ID or time. For example, if the ID range of a User table is 1 \~ 7000, sequential distribution can divide it into multiple subtables with primary key ranges of 1 \~ 1000, 1001 \~ 2000, ..., and 6001 \~ 7000.

Compared with hash distribution, sequential distribution mainly has the following advantages:

- It can preserve the original order of the data.
- It can accurately control the amount of data stored on each server, maximizing storage-space utilization.

## 6. Consistent Hashing

Distributed Hash Table (DHT) is a hash distribution method designed to overcome the large amount of data migration caused by changes in the number of server nodes in traditional hash distribution.

### Core Principles

Treat the hash space [0, 2<sup>n</sup>-1] as a hash ring, and place each server node on the hash ring. After each data object obtains a hash value through hashing and modulo operations, it is stored on the first node clockwise on the hash ring whose value is greater than or equal to that hash value.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/68b110b9-76c6-4ee2-b541-4145e65adb3e.jpg"/> </div><br>

When nodes are added or removed, consistent hashing only affects neighboring nodes on the hash ring. For example, when node X is added in the figure below, only the data on its previous node C needs to be redistributed; nodes A, B, and D are unaffected.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/66402828-fb2b-418f-83f6-82153491bcfe.jpg"/> </div><br>

### Virtual Nodes

The consistent hashing described above has the problem of uneven data distribution. The amount of data stored by different nodes may vary greatly.

Uneven data distribution is mainly caused by uneven node distribution on the hash ring, which is especially obvious when there are few nodes.

The solution is to add virtual nodes and map them to real nodes. Because there are many more virtual nodes than real nodes, virtual nodes are distributed more evenly on the hash ring than the original real nodes, making data distribution more even.

## 7. LRU

The following is an LRU implementation based on a doubly linked list plus HashMap. The algorithm is explained as follows:

- When a node is accessed, remove it from its original position and insert it at the head of the linked list. This ensures that the tail of the linked list stores the least recently used node, and when the number of nodes exceeds the maximum cache space, the tail node is evicted.
- To make deletion O(1), traversal cannot be used to find a node. The HashMap stores the mapping from Key to node. A node can be obtained by Key in O(1), then removed from the doubly linked list in O(1).

```java
public class LRU<K, V> implements Iterable<K> {

    private Node head;
    private Node tail;
    private HashMap<K, Node> map;
    private int maxSize;

    private class Node {

        Node pre;
        Node next;
        K k;
        V v;

        public Node(K k, V v) {
            this.k = k;
            this.v = v;
        }
    }


    public LRU(int maxSize) {

        this.maxSize = maxSize;
        this.map = new HashMap<>(maxSize * 4 / 3);

        head = new Node(null, null);
        tail = new Node(null, null);

        head.next = tail;
        tail.pre = head;
    }


    public V get(K key) {

        if (!map.containsKey(key)) {
            return null;
        }

        Node node = map.get(key);
        unlink(node);
        appendHead(node);

        return node.v;
    }


    public void put(K key, V value) {

        if (map.containsKey(key)) {
            Node node = map.get(key);
            unlink(node);
        }

        Node node = new Node(key, value);
        map.put(key, node);
        appendHead(node);

        if (map.size() > maxSize) {
            Node toRemove = removeTail();
            map.remove(toRemove.k);
        }
    }


    private void unlink(Node node) {

        Node pre = node.pre;
        Node next = node.next;

        pre.next = next;
        next.pre = pre;

        node.pre = null;
        node.next = null;
    }


    private void appendHead(Node node) {
        Node next = head.next;
        node.next = next;
        next.pre = node;
        node.pre = head;
        head.next = node;
    }


    private Node removeTail() {

        Node node = tail.pre;

        Node pre = node.pre;
        tail.pre = pre;
        pre.next = tail;

        node.pre = null;
        node.next = null;

        return node;
    }


    @Override
    public Iterator<K> iterator() {

        return new Iterator<K>() {
            private Node cur = head.next;

            @Override
            public boolean hasNext() {
                return cur != tail;
            }

            @Override
            public K next() {
                Node node = cur;
                cur = cur.next;
                return node.k;
            }
        };
    }
}
```

## References

- Large-Scale Distributed Storage Systems
- [Things About Caching](https://tech.meituan.com/cache_about.html)
- [Consistent Hashing Algorithm](https://my.oschina.net/jayhu/blog/732849)
- [Content Distribution Network](https://zh.wikipedia.org/wiki/%E5%85%A7%E5%AE%B9%E5%82%B3%E9%81%9E%E7%B6%B2%E8%B7%AF)
- [How Aspiration CDN helps to improve your website loading speed?](https://www.aspirationhosting.com/aspiration-cdn/)
