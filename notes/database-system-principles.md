# Database System Principles
<!-- GFM-TOC -->
* [Database System Principles](#database-system-principles)
    * [1. Transactions](#_1-transactions)
        * [Overview](#overview)
        * [ACID](#acid)
        * [AUTOCOMMIT](#autocommit)
    * [2. Concurrency Consistency Problems](#_2-concurrency-consistency-problems)
        * [Lost Update](#lost-update)
        * [Dirty Read](#dirty-read)
        * [Non-Repeatable Read](#non-repeatable-read)
        * [Phantom Read](#phantom-read)
    * [3. Locking](#_3-locking)
        * [Lock Granularity](#lock-granularity)
        * [Lock Types](#lock-types)
        * [Locking Protocols](#locking-protocols)
        * [MySQL Implicit and Explicit Locking](#mysql-implicit-and-explicit-locking)
    * [4. Isolation Levels](#_4-isolation-levels)
        * [Read Uncommitted](#read-uncommitted)
        * [Read Committed](#read-committed)
        * [Repeatable Read](#repeatable-read)
        * [Serializable](#serializable)
    * [5. Multiversion Concurrency Control](#_5-multiversion-concurrency-control)
        * [Core Idea](#core-idea)
        * [Version Numbers](#version-numbers)
        * [Undo Log](#undo-log)
        * [ReadView](#readview)
        * [Snapshot Read and Current Read](#snapshot-read-and-current-read)
    * [6. Next-Key Locks](#_6-next-key-locks)
        * [Record Locks](#record-locks)
        * [Gap Locks](#gap-locks)
        * [Next-Key Locks](#next-key-locks)
    * [7. Relational Database Design Theory](#_7-relational-database-design-theory)
        * [Functional Dependencies](#functional-dependencies)
        * [Anomalies](#anomalies)
        * [Normal Forms](#normal-forms)
    * [8. ER Diagrams](#_8-er-diagrams)
        * [Three Entity Relationship Types](#three-entity-relationship-types)
        * [Represent Repeated Relationships](#represent-repeated-relationships)
        * [Multi-Way Relationships](#multi-way-relationships)
        * [Represent Subclasses](#represent-subclasses)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Transactions

### Overview

A transaction is a group of operations that satisfies the ACID properties. A transaction can be committed with Commit or rolled back with Rollback.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207222237925.png"/> </div><br>

### ACID

#### 1. Atomicity

A transaction is treated as the smallest indivisible unit. All operations in a transaction either commit successfully together or fail and roll back together.

Rollback can be implemented with an undo log. The undo log records the modification operations performed by the transaction; rollback executes these modifications in reverse.

#### 2. Consistency

The database remains in a consistent state before and after transaction execution. In a consistent state, all transactions read the same result for the same data.

#### 3. Isolation

Modifications made by one transaction are invisible to other transactions until the transaction is finally committed.

#### 4. Durability

Once a transaction commits, its modifications are permanently saved in the database. Even if the system crashes, the transaction's results must not be lost.

System crashes can be recovered using redo logs, thereby achieving durability. Unlike undo logs, which record logical data modifications, redo logs record physical modifications to data pages.

----

The concepts behind ACID are simple but not easy to fully understand, mainly because these properties are not peers:

- Only when consistency is satisfied is the execution result of a transaction correct.
- Without concurrency, transactions execute serially and isolation is guaranteed. In this case, atomicity is enough to guarantee consistency.
- With concurrency, multiple transactions execute in parallel. Transactions must satisfy both atomicity and isolation to satisfy consistency.
- Durability is required so transactions can survive system crashes.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207210437023.png"/> </div><br>

### AUTOCOMMIT

MySQL uses automatic commit mode by default. That is, if a transaction is not explicitly started with `START TRANSACTION`, every query operation is treated as a transaction and committed automatically.

## 2. Concurrency Consistency Problems

In a concurrent environment, transaction isolation is hard to guarantee, so many concurrency consistency problems can occur.

### Lost Update

A lost update means one transaction's update is replaced by another transaction's update. This is common in real life. For example, transactions T<sub>1</sub> and T<sub>2</sub> both modify the same data. T<sub>1</sub> modifies and commits first, then T<sub>2</sub> modifies later, and T<sub>2</sub>'s modification overwrites T<sub>1</sub>'s modification.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207221744244.png"/> </div><br>

### Dirty Read

A dirty read means that under different transactions, the current transaction can read data that another transaction has not yet committed. For example, T<sub>1</sub> modifies data but does not commit, and T<sub>2</sub> then reads this data. If T<sub>1</sub> rolls back the modification, the data read by T<sub>2</sub> is dirty data.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207221920368.png"/> </div><br>

### Non-Repeatable Read

A non-repeatable read means reading the same data set multiple times within one transaction, while another transaction accesses and modifies that same data set before the first transaction ends. Because of the second transaction's modification, the first transaction's two reads may produce inconsistent data. For example, T<sub>2</sub> reads data, T<sub>1</sub> modifies that data, and if T<sub>2</sub> reads it again, the result differs from the first read.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207222102010.png"/> </div><br>

### Phantom Read

A phantom read is essentially also a non-repeatable read. T<sub>1</sub> reads data within a range, T<sub>2</sub> inserts new data into that range, and T<sub>1</sub> reads the range again. The result then differs from the first read.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207222134306.png"/> </div><br>

----

The main reason for concurrency inconsistency is that transaction isolation is broken. The solution is to guarantee isolation through concurrency control. Concurrency control can be implemented with locking, but locking requires user control and is quite complex. Database management systems provide transaction isolation levels so users can handle concurrency consistency problems more easily.

## 3. Locking

### Lock Granularity

MySQL provides two locking granularities: row-level locks and table-level locks.

Lock only the data that needs to be modified whenever possible, instead of all resources. The less data that is locked, the lower the chance of lock contention and the higher the system concurrency.

However, locking consumes resources. Lock operations, including acquiring locks, releasing locks, and checking lock status, increase system overhead. Therefore, the smaller the lock granularity, the greater the system overhead.

When choosing lock granularity, make a trade-off between lock overhead and concurrency.


### Lock Types

#### 1. Read/Write Locks

- Exclusive lock, abbreviated as X lock, also called a write lock.
- Shared lock, abbreviated as S lock, also called a read lock.

There are two rules:

- If a transaction places an X lock on data object A, it can read and update A. During the lock, other transactions cannot place any lock on A.
- If a transaction places an S lock on data object A, it can read A but cannot update it. During the lock, other transactions can place S locks on A, but cannot place X locks.

The lock compatibility relationship is:

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207213523777.png"/> </div><br>

#### 2. Intention Locks

Intention locks make it easier to support multi-granularity locking.

When row-level and table-level locks both exist, if transaction T wants to place an X lock on table A, it must first check whether any other transaction has locked table A or any row in table A. This would require checking every row in table A, which is very time-consuming.

Intention locks introduce IX/IS on top of the original X/S locks. IX/IS are table locks used to indicate that a transaction wants to place an X lock or S lock on some data row in the table. There are two rules:

- Before a transaction obtains an S lock on a data-row object, it must first obtain an IS lock or a stronger lock on the table;
- Before a transaction obtains an X lock on a data-row object, it must first obtain an IX lock on the table.

By introducing intention locks, if transaction T wants to place an X lock on table A, it only needs to check whether any other transaction has placed an X/IX/S/IS lock on table A. If so, another transaction is using the table or a row in the table, so transaction T fails to acquire the X lock.

The compatibility relationship among lock types is:

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207214442687.png"/> </div><br>

Explanation:

- Any IS/IX locks are compatible with each other because they only indicate an intention to lock a table, not an actual lock;
- The compatibility relationship here is for table-level locks. A table-level IX lock is compatible with a row-level X lock, so two transactions can place X locks on two different rows. For example, transaction T<sub>1</sub> wants to place an X lock on row R<sub>1</sub>, and transaction T<sub>2</sub> wants to place an X lock on row R<sub>2</sub> in the same table. Both transactions need to place IX locks on the table, but IX locks are compatible, and IX locks are also compatible with row-level X locks, so both transactions can lock successfully and modify two rows in the same table.

### Locking Protocols

#### 1. Three-Level Locking Protocol

**Level-One Locking Protocol**  

When transaction T wants to modify data A, it must place an X lock and release it only after T ends.

This solves lost updates because two transactions cannot modify the same data at the same time, so one transaction's modification will not be overwritten.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207220440451.png"/> </div><br>

**Level-Two Locking Protocol**  

Based on level one, reading data A requires placing an S lock and releasing it immediately after the read.

This solves dirty reads because if a transaction is modifying data A, it holds an X lock according to the level-one locking protocol, so an S lock cannot be placed and the data cannot be read.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207220831843.png"/> </div><br>

**Level-Three Locking Protocol**  

Based on level two, reading data A requires placing an S lock and releasing it only after the transaction ends.

This solves non-repeatable reads because while A is being read, other transactions cannot place an X lock on A, preventing the data from changing during the read period.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207221313819.png"/> </div><br>

#### 2. Two-Phase Locking Protocol

Locking and unlocking are divided into two phases.

Serializable scheduling means using concurrency control so that the result of concurrently executed transactions is the same as the result of some serial execution of those transactions. Serially executed transactions do not interfere with each other, so concurrency consistency problems do not occur.

Following the two-phase locking protocol is a sufficient condition for ensuring serializable scheduling. For example, the following operations satisfy two-phase locking and are serializable.

```html
lock-x(A)...lock-s(B)...lock-s(C)...unlock(A)...unlock(C)...unlock(B)
```

But it is not a necessary condition. For example, the following operations do not satisfy two-phase locking, but they are still serializable.

```html
lock-x(A)...unlock(A)...lock-s(B)...unlock(B)...lock-s(C)...unlock(C)
```

### MySQL Implicit and Explicit Locking

MySQL's InnoDB storage engine uses the two-phase locking protocol. It automatically locks when needed according to the isolation level, and all locks are released at the same time. This is called implicit locking.

InnoDB can also use specific statements for explicit locking:

```sql
SELECT ... LOCK In SHARE MODE;
SELECT ... FOR UPDATE;
```

## 4. Isolation Levels

### Read Uncommitted

Modifications in a transaction are visible to other transactions even if they have not been committed.

### Read Committed

A transaction can read only modifications made by committed transactions. In other words, modifications made by a transaction are invisible to other transactions before commit.

### Repeatable Read

Guarantees that multiple reads of the same data within the same transaction return the same result.

### Serializable

Forces transactions to execute serially, so multiple transactions do not interfere with each other and concurrency consistency problems do not occur.

This isolation level requires locking because a locking mechanism is needed to ensure that only one transaction executes at a time, guaranteeing serial execution.

----

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191207223400787.png"/> </div><br>

## 5. Multiversion Concurrency Control

Multiversion Concurrency Control (MVCC) is a concrete way for MySQL's InnoDB storage engine to implement isolation levels. It is used to implement Read Committed and Repeatable Read. The Read Uncommitted isolation level always reads the latest data rows and has low requirements, so MVCC is unnecessary. The Serializable isolation level needs to lock all rows read, so MVCC alone cannot implement it.

### Core Idea

As mentioned in the locking section, locks can solve concurrency consistency problems that occur when multiple transactions execute at the same time. In practice, reads often outnumber writes, so read/write locks are introduced to avoid unnecessary locking; for example, reads do not conflict with reads. In read/write locks, reads and writes still conflict. MVCC uses the idea of multiple versions: write operations update the latest version snapshot, while read operations read older version snapshots without mutual exclusion. This is similar to CopyOnWrite.

In MVCC, transaction modification operations (DELETE, INSERT, UPDATE) add a new version snapshot for the data row.

The root cause of dirty reads and non-repeatable reads is that a transaction reads uncommitted modifications from another transaction. To solve dirty reads and non-repeatable reads during transaction reads, MVCC requires reading only committed snapshots. Of course, a transaction can read its own uncommitted snapshots; this is not considered a dirty read.

### Version Numbers

- System version number SYS_ID: an increasing number. Each time a new transaction starts, the system version number automatically increases.
- Transaction version number TRX_ID: the system version number when the transaction starts.

### Undo Log

The "multi-version" in MVCC refers to multiple versions of snapshots. Snapshots are stored in the Undo log, which connects all snapshots of a data row through the rollback pointer ROLL_PTR.

For example, create a table t in MySQL containing primary key id and a field x. First insert one data row, then update that row twice.

```sql
INSERT INTO t(id, x) VALUES(1, "a");
UPDATE t SET x="b" WHERE id=1;
UPDATE t SET x="c" WHERE id=1;
```

Because `START TRANSACTION` is not used to execute the operations above as one transaction, MySQL's AUTOCOMMIT mechanism treats each operation as a transaction. Therefore, the operations above involve three transactions in total. In addition to recording the transaction version number TRX_ID and the operation, the snapshot also records a one-bit DEL field that marks whether the row has been deleted.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208164808217.png"/> </div><br>

INSERT, UPDATE, and DELETE operations create a log and write the transaction version number TRX_ID into it. DELETE can be viewed as a special UPDATE, and it additionally sets the DEL field to 1.

### ReadView

MVCC maintains a ReadView structure. It mainly contains the list of uncommitted transactions in the current system, TRX_IDs {TRX_ID_1, TRX_ID_2, ...}, along with the minimum value TRX_ID_MIN and TRX_ID_MAX of that list.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208171445674.png"/> </div><br>

During a SELECT operation, whether a data-row snapshot can be used is determined from the relationship between the snapshot's TRX_ID and TRX_ID_MIN/TRX_ID_MAX:

- TRX_ID \< TRX_ID_MIN means the data-row snapshot was changed before all currently uncommitted transactions, so it can be used.

- TRX_ID \> TRX_ID_MAX means the data-row snapshot was changed after the transaction started, so it cannot be used.
- TRX_ID_MIN \<= TRX_ID \<= TRX_ID_MAX requires further judgment based on the isolation level:
  - Read Committed: if TRX_ID is in the TRX_IDs list, the transaction corresponding to this data-row snapshot has not yet committed, so the snapshot cannot be used. Otherwise, it has committed and can be used.
  - Repeatable Read: none can be used. If it could be used, other transactions could also read and modify this data-row snapshot, so the current transaction would read a different value for this row later, causing a non-repeatable read.

If the data-row snapshot cannot be used, follow the rollback pointer ROLL_PTR in the Undo Log to find the next snapshot, then apply the same judgment above.

### Snapshot Read and Current Read

#### 1. Snapshot Read

MVCC SELECT operations read data from snapshots and do not need locking.

```sql
SELECT * FROM table ...;
```

#### 2. Current Read

Other MVCC operations that modify the database (INSERT, UPDATE, DELETE) require locking so they can read the latest data. MVCC does not completely avoid locks; it only avoids locking for SELECT operations.

```sql
INSERT;
UPDATE;
DELETE;
```

During SELECT operations, locking can be forced explicitly. The first statement below requires an S lock, and the second requires an X lock.

```sql
SELECT * FROM table WHERE ? lock in share mode;
SELECT * FROM table WHERE ? for update;
```

## 6. Next-Key Locks

Next-Key Locks are a lock implementation in MySQL's InnoDB storage engine.

MVCC cannot solve phantom reads, so Next-Key Locks exist to solve this problem. Under the Repeatable Read isolation level, MVCC + Next-Key Locks can solve phantom reads.

### Record Locks

Lock the index on a record, not the record itself.

If a table has no index, InnoDB automatically creates a hidden clustered index on the primary key, so Record Locks can still be used.

### Gap Locks

Lock the gaps between indexes, excluding the indexes themselves. For example, when one transaction executes the following statement, other transactions cannot insert 15 into t.c.

```sql
SELECT c FROM t WHERE c BETWEEN 10 and 20 FOR UPDATE;
```

### Next-Key Locks

It combines Record Locks and Gap Locks. It locks not only the index on a record but also the gaps between indexes. It locks a left-open, right-closed interval. For example, if an index contains the values 10, 11, 13, and 20, the following intervals need to be locked:

```sql
(-∞, 10]
(10, 11]
(11, 13]
(13, 20]
(20, +∞)
```

## 7. Relational Database Design Theory

### Functional Dependencies

Use A-\>B to mean A functionally determines B. This can also be said as B functionally depends on A.

If {A1, A2, ..., An} is a set of one or more attributes in a relation, and this set functionally determines all other attributes in the relation and is minimal, then this set is called a key.

For A-\>B, if a proper subset A' of A can be found such that A'-\>B, then A-\>B is a partial functional dependency; otherwise, it is a full functional dependency.

For A-\>B and B-\>C, A-\>C is a transitive functional dependency.

### Anomalies

The following student-course relation has the functional dependency {Sno, Cname} -\> {Sname, Sdept, Mname, Grade}, and its key is {Sno, Cname}. In other words, once the student and course are determined, all other information is determined.

| Sno | Sname | Sdept | Mname | Cname | Grade |
| :---: | :---: | :---: | :---: | :---: |:---:|
| 1 | Student-1 | Department-1 | Dean-1 | Course-1 | 90 |
| 2 | Student-2 | Department-2 | Dean-2 | Course-2 | 80 |
| 2 | Student-2 | Department-2 | Dean-2 | Course-1 | 100 |
| 3 | Student-3 | Department-2 | Dean-2 | Course-2 | 95 |

Relations that do not conform to normal forms produce many anomalies, mainly the following four:

- Redundant data: for example, `Student-2` appears twice.
- Update anomaly: information in one record is modified, but the same information in another record is not.
- Deletion anomaly: deleting one piece of information also loses other information. For example, deleting `Course-1` requires deleting the first and third rows, so information about `Student-1` is lost.
- Insertion anomaly: for example, if you want to insert information about a student who has not selected any course, it cannot be inserted.

### Normal Forms

Normal form theory exists to solve the four anomalies above.

Higher-level normal forms depend on lower-level normal forms. 1NF is the lowest normal form.

#### 1. First Normal Form (1NF)

Attributes are indivisible.

#### 2. Second Normal Form (2NF)

Every non-prime attribute fully functionally depends on the key.

This can be satisfied through decomposition.

<font size=4>  **Before Decomposition**  </font><br>

| Sno | Sname | Sdept | Mname | Cname | Grade |
| :---: | :---: | :---: | :---: | :---: |:---:|
| 1 | Student-1 | Department-1 | Dean-1 | Course-1 | 90 |
| 2 | Student-2 | Department-2 | Dean-2 | Course-2 | 80 |
| 2 | Student-2 | Department-2 | Dean-2 | Course-1 | 100 |
| 3 | Student-3 | Department-2 | Dean-2 | Course-2 | 95 |

In the student-course relation above, {Sno, Cname} is the key, and the following functional dependencies exist:

- Sno -\> Sname, Sdept
- Sdept -\> Mname
- Sno, Cname-\> Grade

Grade fully functionally depends on the key. It has no redundant data; each student's course has a specific grade.

Sname, Sdept, and Mname all partially depend on the key. When a student takes multiple courses, this data appears multiple times, causing significant redundancy.

<font size=4>  **After Decomposition**  </font><br>

Relation-1

| Sno | Sname | Sdept | Mname |
| :---: | :---: | :---: | :---: |
| 1 | Student-1 | Department-1 | Dean-1 |
| 2 | Student-2 | Department-2 | Dean-2 |
| 3 | Student-3 | Department-2 | Dean-2 |

The following functional dependencies exist:

- Sno -\> Sname, Sdept
- Sdept -\> Mname

Relation-2

| Sno | Cname | Grade |
| :---: | :---: |:---:|
| 1 | Course-1 | 90 |
| 2 | Course-2 | 80 |
| 2 | Course-1 | 100 |
| 3 | Course-2 | 95 |

The following functional dependency exists:

- Sno, Cname -\>  Grade

#### 3. Third Normal Form (3NF)

Non-prime attributes do not transitively functionally depend on the key.

Relation-1 above has the following transitive functional dependency:

- Sno -\> Sdept -\> Mname

It can be decomposed as follows:

Relation-11

| Sno | Sname | Sdept |
| :---: | :---: | :---: |
| 1 | Student-1 | Department-1 |
| 2 | Student-2 | Department-2 |
| 3 | Student-3 | Department-2 |

Relation-12

| Sdept | Mname |
| :---: | :---: |
| Department-1 | Dean-1 |
| Department-2 | Dean-2 |

## 8. ER Diagrams

Entity-Relationship has three components: entities, attributes, and relationships.

It is used for conceptual design of relational database systems.

### Three Entity Relationship Types

There are three types: one-to-one, one-to-many, and many-to-many.

- If A to B is a one-to-many relationship, draw a line segment with an arrow pointing to B;
- If it is one-to-one, draw two line segments with arrows;
- If it is many-to-many, draw two line segments without arrows.

In the figure below, Course and Student have a one-to-many relationship.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/1d28ad05-39e5-49a2-a6a1-a6f496adba6a.png" width="380px"/> </div><br>

### Represent Repeated Relationships

If an entity appears several times in a relationship, connect it with that many lines.

The following figure represents prerequisite relationships for a course. The prerequisite relationship contains two Course entities: the first is the prerequisite course, and the second is the subsequent course. Therefore, two lines are needed to represent this relationship.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ac929ea3-daca-40ec-9e95-4b2fa6678243.png" width="250px"/> </div><br>

### Multi-Way Relationships

Although a teacher can offer multiple courses and teach many students, for a specific student and course, there is only one teacher. This forms a ternary relationship.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/5bb1b38a-527e-4802-a385-267dadbd30ba.png" width="350px"/> </div><br>

### Represent Subclasses

Use a triangle and two lines to connect classes and subclasses. Attributes and relationships related to subclasses connect to the subclass, while those related to both the parent class and subclasses connect to the parent class.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/14389ea4-8d96-4e96-9f76-564ca3324c1e.png" width="450px"/> </div><br>

## References

- Abraham Silberschatz, Henry F. Korth, S. Sudarshan, et al. Database System Concepts[M]. China Machine Press, 2006.
- Schwartz. High Performance MySQL, Third Edition[M]. Publishing House of Electronics Industry, 2013.
- Shi Jiaquan. Introduction to Database Systems[M]. Tsinghua University Press, 2006.
- [The InnoDB Storage Engine](https://dev.mysql.com/doc/refman/5.7/en/innodb-storage-engine.html)
- [Transaction isolation levels](https://www.slideshare.net/ErnestoHernandezRodriguez/transaction-isolation-levels)
- [Concurrency Control](http://scanftree.com/dbms/2-phase-locking-protocol)
- [The Nightmare of Locking, Blocking and Isolation Levels!](https://www.slideshare.net/brshristov/the-nightmare-of-locking-blocking-and-isolation-levels-46391666)
- [Database Normalization and Normal Forms with an Example](https://aksakalli.github.io/2012/03/12/database-normalization-and-normal-forms-with-an-example.html)
- [The basics of the InnoDB undo logging and history system](https://blog.jcole.us/2014/04/16/the-basics-of-the-innodb-undo-logging-and-history-system/)
- [MySQL locking for the busy web developer](https://www.brightbox.com/blog/2013/10/31/on-mysql-locks/)
- [MySQL and InnoDB, from basics to internals](https://draveness.me/mysql-innodb)
- [The relationship between transaction isolation levels and locks in InnoDB](https://tech.meituan.com/2014/08/20/innodb-lock.html)
