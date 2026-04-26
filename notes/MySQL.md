# MySQL
<!-- GFM-TOC -->
* [MySQL](#mysql)
    * [1. Indexes](#_1-indexes)
        * [B+ Tree Principles](#b-tree-principles)
        * [MySQL Indexes](#mysql-indexes)
        * [Index Optimization](#index-optimization)
        * [Index Advantages](#index-advantages)
        * [Index Usage Conditions](#index-usage-conditions)
    * [2. Query Performance Optimization](#_2-query-performance-optimization)
        * [Analyze with Explain](#analyze-with-explain)
        * [Optimize Data Access](#optimize-data-access)
        * [Refactor Query Patterns](#refactor-query-patterns)
    * [3. Storage Engines](#_3-storage-engines)
        * [InnoDB](#innodb)
        * [MyISAM](#myisam)
        * [Comparison](#comparison)
    * [4. Data Types](#_4-data-types)
        * [Integer Types](#integer-types)
        * [Floating-Point Types](#floating-point-types)
        * [Strings](#strings)
        * [Time and Date](#time-and-date)
    * [5. Sharding](#_5-sharding)
        * [Horizontal Sharding](#horizontal-sharding)
        * [Vertical Sharding](#vertical-sharding)
        * [Sharding Strategies](#sharding-strategies)
        * [Sharding Issues](#sharding-issues)
    * [6. Replication](#_6-replication)
        * [Master-Slave Replication](#master-slave-replication)
        * [Read/Write Splitting](#readwrite-splitting)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Indexes

### B+ Tree Principles

#### 1. Data Structures

B Tree means Balance Tree, or balanced tree. A balanced tree is a search tree, and all leaf nodes are on the same level.

B+ Tree is implemented based on B Tree plus sequential access pointers between leaf nodes. It has the balance property of B Tree and improves range-query performance through sequential access pointers.

In a B+ Tree, keys in a node are arranged from left to right in nondecreasing order. If the adjacent keys to the left and right of a pointer are key<sub>i</sub> and key<sub>i+1</sub>, and the pointer is not null, then all keys in the node pointed to by that pointer are greater than or equal to key<sub>i</sub> and less than or equal to key<sub>i+1</sub>.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/33576849-9275-47bb-ada7-8ded5f5e7c73.png" width="350px"> </div><br>

#### 2. Operations

During lookup, first perform binary search in the root node to find the pointer where a key belongs, then recursively search the node pointed to by that pointer. Continue until reaching a leaf node, then perform binary search on the leaf node to find the data corresponding to the key.

Insertions and deletions can break the balance of the tree, so after insertion or deletion, operations such as splitting, merging, and rotation are needed to maintain balance.

#### 3. Comparison with Red-Black Trees

Balanced trees such as red-black trees can also implement indexes, but file systems and database systems commonly use B+ Tree as the index structure because it has better performance for accessing disk data.

1. B+ Tree has lower tree height

The height of a balanced tree is O(h)=O(log<sub>d</sub>N), where d is the degree of each node. A red-black tree has degree 2, while the degree of a B+ Tree is generally very large, so the height h of a red-black tree is much larger than that of a B+ Tree.

2. Disk access principles

Operating systems usually divide memory and disk into fixed-size blocks. Each block is called a page, and memory and disk exchange data in page units. Database systems set the size of an index node to the page size, so one I/O can load an entire node.

If data is not in the same disk block, the actuator arm usually needs to move to seek. Because of its physical structure, the actuator arm moves inefficiently, increasing disk read time. Compared with red-black trees, B+ Trees have lower height. The number of seeks is proportional to tree height, and accessing data within the same disk block requires only a short disk rotation time. Therefore, B+ Trees are more suitable for reading disk data.

3. Disk read-ahead

To reduce disk I/O, disks often do not read strictly on demand; they perform read-ahead each time. During read-ahead, the disk reads sequentially. Sequential reads do not require disk seeks and need only a short disk rotation time, so they are very fast. Read-ahead can also preload adjacent nodes.

### MySQL Indexes

Indexes are implemented at the storage-engine layer, not at the server layer, so different storage engines have different index types and implementations.

#### 1. B+Tree Indexes

B+Tree indexes are the default index type for most MySQL storage engines.

Because a full table scan is no longer required and only the tree needs to be searched, lookup is much faster.

Because B+ Tree is ordered, it can be used not only for lookup but also for sorting and grouping.

Multiple columns can be specified as index columns, and together they form the key.

It supports full-key, key-range, and key-prefix lookups. Key-prefix lookup applies only to leftmost-prefix lookup. If the lookup does not follow the order of the index columns, the index cannot be used.

InnoDB's B+Tree indexes are divided into primary indexes and secondary indexes. The data field of each leaf node in the primary index records the complete data row. This indexing method is called a clustered index. Because a data row cannot be stored in two different places, a table can have only one clustered index.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/45016e98-6879-4709-8569-262b2d6d60b9.png" width="350px"> </div><br>

The data field of each leaf node in a secondary index records the primary-key value. Therefore, when using a secondary index for lookup, MySQL first finds the primary-key value and then searches the primary index.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7c349b91-050b-4d72-a7f8-ec86320307ea.png" width="350px"> </div><br>

#### 2. Hash Indexes

Hash indexes can perform lookups in O(1) time, but they lose ordering:

- They cannot be used for sorting or grouping;
- They support only exact lookup and cannot be used for partial or range lookup.

The InnoDB storage engine has a special feature called the adaptive hash index. When an index value is used very frequently, InnoDB creates a hash index on top of the B+Tree index, giving the B+Tree index some advantages of hash indexes, such as fast hash lookup.

#### 3. Full-Text Indexes

The MyISAM storage engine supports full-text indexes, which are used to find keywords in text rather than directly comparing equality.

The lookup condition uses MATCH AGAINST instead of a normal WHERE clause.

Full-text indexes are implemented using inverted indexes, which record mappings from keywords to the documents containing them.

The InnoDB storage engine also began supporting full-text indexes in MySQL 5.6.4.

#### 4. Spatial Indexes

The MyISAM storage engine supports spatial data indexes (R-Tree), which can be used for geographic data storage. Spatial indexes index data across all dimensions and can efficiently support combined queries using any dimension.

GIS-related functions must be used to maintain the data.

### Index Optimization

#### 1. Independent Columns

During a query, an indexed column cannot be part of an expression or a function argument; otherwise, the index cannot be used.

For example, the following query cannot use the index on the actor_id column:

```sql
SELECT actor_id FROM sakila.actor WHERE actor_id + 1 = 5;
```

#### 2. Multi-Column Indexes

When multiple columns are used as query conditions, a multi-column index performs better than multiple single-column indexes. For example, in the following statement, it is better to define actor_id and film_id as a multi-column index.

```sql
SELECT film_id, actor_ id FROM sakila.film_actor
WHERE actor_id = 1 AND film_id = 1;
```

#### 3. Index Column Order

Put the most selective index column first.

Index selectivity is the ratio of distinct index values to the total number of records. Its maximum value is 1, where each record has a unique corresponding index value. The higher the selectivity, the more distinguishable each record is, and the higher the query efficiency.

For example, in the result shown below, customer_id is more selective than staff_id, so it is better to put customer_id before staff_id in the multi-column index.

```sql
SELECT COUNT(DISTINCT staff_id)/COUNT(*) AS staff_id_selectivity,
COUNT(DISTINCT customer_id)/COUNT(*) AS customer_id_selectivity,
COUNT(*)
FROM payment;
```

```html
   staff_id_selectivity: 0.0001
customer_id_selectivity: 0.0373
               COUNT(*): 16049
```

#### 4. Prefix Indexes

For BLOB, TEXT, and VARCHAR columns, prefix indexes must be used, indexing only the initial portion of the string.

The prefix length should be selected based on index selectivity.

#### 5. Covering Indexes

The index contains the values of all fields needed by the query.

It has the following advantages:

- Indexes are usually much smaller than data rows, so reading only the index greatly reduces data access.
- Some storage engines, such as MyISAM, cache only indexes in memory, while data relies on the operating system cache. Therefore, accessing only the index avoids system calls, which are usually time-consuming.
- For the InnoDB engine, if a secondary index can cover the query, the primary index does not need to be accessed.

### Index Advantages

- Greatly reduces the number of rows the server needs to scan.

- Helps the server avoid sorting and grouping, and avoid creating temporary tables. B+Tree indexes are ordered and can be used for ORDER BY and GROUP BY operations. Temporary tables are mainly created during sorting and grouping; if sorting and grouping are not needed, temporary tables are not needed either.

- Converts random I/O into sequential I/O. B+Tree indexes are ordered and store adjacent data together.

### Index Usage Conditions

- For very small tables, a simple full table scan is usually more efficient than building an index;

- For medium to large tables, indexes are very effective;

- For very large tables, however, the cost of creating and maintaining indexes increases. In this case, a technique is needed to directly identify the group of data to query instead of matching records one by one, such as partitioning.

## 2. Query Performance Optimization

### Analyze with Explain

Explain is used to analyze SELECT queries. Developers can optimize queries by analyzing Explain results.

Important fields include:

- select_type: query type, such as simple query, union query, or subquery
- key: index used
- rows: number of rows scanned

### Optimize Data Access

#### 1. Reduce Requested Data Volume

- Return only necessary columns: avoid using SELECT *.
- Return only necessary rows: use LIMIT to restrict returned data.
- Cache repeatedly queried data: caching can avoid database queries. When the data is queried repeatedly, caching can provide a very noticeable performance improvement.

#### 2. Reduce Server-Side Scanned Rows

The most effective approach is to use indexes to cover the query.

### Refactor Query Patterns

#### 1. Split Large Queries

If a large query is executed all at once, it may lock a large amount of data, fill the entire transaction log, exhaust system resources, and block many small but important queries.

```sql
DELETE FROM messages WHERE create < DATE_SUB(NOW(), INTERVAL 3 MONTH);
```

```sql
rows_affected = 0
do {
    rows_affected = do_query(
    "DELETE FROM messages WHERE create  < DATE_SUB(NOW(), INTERVAL 3 MONTH) LIMIT 10000")
} while rows_affected > 0
```

#### 2. Decompose Large Join Queries

Decompose a large join query into a single-table query for each table, then join the results in the application. Benefits include:

- More efficient caching. For a join query, if one table changes, the entire query cache cannot be used. After decomposition, even if one table changes, the query cache for other tables can still be used.
- After decomposition into multiple single-table queries, cached results from those queries are more likely to be reused by other queries, reducing redundant record lookups.
- Reduced lock contention;
- Joining at the application layer makes it easier to split the database, improving performance and scalability.
- The query itself may also become more efficient. In the example below, using IN() instead of a join allows MySQL to query in ID order, which may be more efficient than a random join.

```sql
SELECT * FROM tag
JOIN tag_post ON tag_post.tag_id=tag.id
JOIN post ON tag_post.post_id=post.id
WHERE tag.tag='mysql';
```

```sql
SELECT * FROM tag WHERE tag='mysql';
SELECT * FROM tag_post WHERE tag_id=1234;
SELECT * FROM post WHERE post.id IN (123,456,567,9098,8904);
```

## 3. Storage Engines

### InnoDB

InnoDB is MySQL's default transactional storage engine. Use another storage engine only when a required feature is not supported by InnoDB.

It implements the four standard isolation levels, with REPEATABLE READ as the default. Under the repeatable read isolation level, phantom reads are prevented through multiversion concurrency control (MVCC) plus Next-Key Locking.

The primary index is a clustered index, storing data in the index and avoiding direct disk reads, which greatly improves query performance.

It has many internal optimizations, including predictive reads when reading data from disk, automatically created adaptive hash indexes that speed up reads, and insert buffers that speed up insertions.

It supports true online hot backup. Other storage engines do not support online hot backup. To obtain a consistent view, writes to all tables must be stopped, and in mixed read/write scenarios, stopping writes may also mean stopping reads.

### MyISAM

MyISAM has a simple design and stores data in a compact format. It can still be used for read-only data, or for small tables where repair operations are acceptable.

It provides many features, including compressed tables and spatial data indexes.

It does not support transactions.

It does not support row-level locks and can only lock entire tables. Reads acquire shared locks on all tables that need to be read, while writes acquire exclusive locks on tables. However, new records can still be inserted while a table is being read; this is called concurrent insert.

Check and repair operations can be performed manually or automatically, but unlike transaction recovery and crash recovery, they may cause some data loss, and repair operations are very slow.

If the DELAY_KEY_WRITE option is specified, modified index data is not immediately written to disk after each modification. Instead, it is written to the key buffer in memory, and the corresponding index blocks are written to disk only when the key buffer is flushed or the table is closed. This can greatly improve write performance, but if the database or host crashes, indexes may be corrupted and require repair.

### Comparison

- Transactions: InnoDB is transactional and supports Commit and Rollback statements.

- Concurrency: MyISAM supports only table-level locks, while InnoDB also supports row-level locks.

- Foreign keys: InnoDB supports foreign keys.

- Backup: InnoDB supports online hot backup.

- Crash recovery: MyISAM is much more likely to be corrupted after a crash than InnoDB, and recovery is slower.

- Other features: MyISAM supports compressed tables and spatial data indexes.

## 4. Data Types

### Integer Types

TINYINT, SMALLINT, MEDIUMINT, INT, and BIGINT use 8, 16, 24, 32, and 64 bits of storage respectively. In general, smaller columns are better.

The number in INT(11) only specifies how many characters interactive tools display. It has no meaning for storage or computation.

### Floating-Point Types

FLOAT and DOUBLE are floating-point types, while DECIMAL is a high-precision decimal type. CPUs natively support floating-point operations but do not support DECIMAL computation, so DECIMAL computation costs more than floating-point computation.

FLOAT, DOUBLE, and DECIMAL can all specify column width. For example, DECIMAL(18, 9) means 18 digits total, with 9 digits used for the fractional part and the remaining 9 for the integer part.

### Strings

The main types are CHAR and VARCHAR. One is fixed length, and the other is variable length.

Variable-length types such as VARCHAR can save space because they store only the necessary content. However, UPDATE operations may make a row longer than before. When it exceeds the size that one page can hold, extra operations are required. MyISAM splits the row into different fragments for storage, while InnoDB needs to split pages to fit the row into a page.

During storage and retrieval, trailing spaces in VARCHAR are preserved, while trailing spaces in CHAR are removed.

### Time and Date

MySQL provides two similar date and time types: DATETIME and TIMESTAMP.

#### 1. DATETIME

It can store dates and times from the year 1000 to 9999, with second-level precision, using 8 bytes of storage.

It is independent of time zones.

By default, MySQL displays DATETIME values in a sortable and unambiguous format, such as "2008-01-16 22:37:08". This is the date and time representation defined by the ANSI standard.

#### 2. TIMESTAMP

Like a UNIX timestamp, it stores the number of seconds since midnight on January 1, 1970 (Greenwich Mean Time). It uses 4 bytes and can represent only dates from 1970 to 2038.

It is time-zone dependent, meaning the same timestamp represents different concrete times in different time zones.

MySQL provides the FROM_UNIXTIME() function to convert a UNIX timestamp to a date, and the UNIX_TIMESTAMP() function to convert a date to a UNIX timestamp.

By default, if no value is specified for a TIMESTAMP column during insertion, it is set to the current time.

TIMESTAMP should be used whenever possible because it is more space-efficient than DATETIME.

## 5. Sharding

### Horizontal Sharding

Horizontal sharding is also called sharding. It splits records from the same table into multiple tables with the same structure.

When the data in a table keeps growing, sharding becomes inevitable. It distributes data across different nodes in a cluster, reducing pressure on a single database.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/63c2909f-0c5f-496f-9fe5-ee9176b31aba.jpg" width=""> </div><br>

### Vertical Sharding

Vertical sharding splits one table into multiple tables by column. It is usually done according to how closely columns are related. It can also separate frequently used columns from infrequently used columns into different tables.

At the database level, vertical sharding deploys tables into different databases according to how closely the tables are related. For example, an e-commerce database can be vertically split into a product database, user database, and so on.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e130e5b8-b19a-4f1e-b860-223040525cf6.jpg" width=""> </div><br>

### Sharding Strategies

- Hash modulo: hash(key) % N;
- Range: can be an ID range or a time range;
- Mapping table: use a separate database to store the mapping relationship.

### Sharding Issues

#### 1. Transaction Issues

Use distributed transactions to solve this, such as the XA interface.

#### 2. Joins

The original join can be decomposed into multiple single-table queries, then joined in the application.

#### 3. ID Uniqueness

- Use globally unique IDs (GUIDs)
- Assign an ID range to each shard
- Distributed ID generator, such as Twitter's Snowflake algorithm

## 6. Replication

### Master-Slave Replication

It mainly involves three threads: the binlog thread, I/O thread, and SQL thread.

-   **binlog thread**  : responsible for writing data changes on the master server to the binary log.
-   **I/O thread**  : responsible for reading the binary log from the master server and writing it to the slave server's relay log.
-   **SQL thread**  : responsible for reading the relay log, parsing the data changes already executed by the master server, and replaying them on the slave server.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/master-slave.png" width=""> </div><br>

### Read/Write Splitting

The master server handles writes and reads with high freshness requirements, while slave servers handle reads.

Read/write splitting improves performance because:

- Master and slave servers handle their own reads and writes, greatly reducing lock contention;
- Slave servers can use MyISAM, improving query performance and saving system overhead;
- Redundancy is increased, improving availability.

Read/write splitting is commonly implemented with a proxy. The proxy server receives read and write requests from the application layer and decides which server to forward them to.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/master-slave-proxy.png" width=""> </div><br>

## References

- BaronScbwartz, PeterZaitsev, VadimTkacbenko, et al. High Performance MySQL[M]. Publishing House of Electronics Industry, 2013.
- Jiang Chengyao. MySQL Internals: InnoDB Storage Engine[M]. China Machine Press, 2011.
- [20+ best practices for MySQL performance optimization](https://www.jfox.info/20-tiao-mysql-xing-nen-you-hua-de-zui-jia-jing-yan.html)
- [Server-side guide: data storage | MySQL (09), distributed difficulties and solutions caused by database and table sharding](http://blog.720ui.com/2017/mysql_core_09_multi_db_table2/ "Server-side guide: data storage | MySQL (09), distributed difficulties and solutions caused by database and table sharding")
- [How to create unique row ID in sharded databases?](https://stackoverflow.com/questions/788829/how-to-create-unique-row-id-in-sharded-databases)
- [SQL Azure Federation – Introduction](http://geekswithblogs.net/shaunxu/archive/2012/01/07/sql-azure-federation-ndash-introduction.aspx "Title of this entry.")
- [Data structures and algorithm principles behind MySQL indexes](http://blog.codinglabs.org/articles/theory-of-mysql-index.html)
- [Using Explain for MySQL performance optimization](https://segmentfault.com/a/1190000008131735)
- [How Sharding Works](https://medium.com/@jeeyoungk/how-sharding-works-b4dec46b3f6)
- [Dianping order system database and table sharding practice](https://tech.meituan.com/dianping_order_db_sharding.html)
- [B+ tree](https://zh.wikipedia.org/wiki/B%2B%E6%A0%91)
