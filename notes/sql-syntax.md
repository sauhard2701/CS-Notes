# SQL Syntax
<!-- GFM-TOC -->
* [SQL Syntax](#sql-syntax)
    * [1. Basics](#_1-basics)
    * [2. Create Tables](#_2-create-tables)
    * [3. Modify Tables](#_3-modify-tables)
    * [4. Insert](#_4-insert)
    * [5. Update](#_5-update)
    * [6. Delete](#_6-delete)
    * [7. Query](#_7-query)
        * [DISTINCT](#distinct)
        * [LIMIT](#limit)
    * [8. Sorting](#_8-sorting)
    * [9. Filtering](#_9-filtering)
    * [10. Wildcards](#_10-wildcards)
    * [11. Calculated Fields](#_11-calculated-fields)
    * [12. Functions](#_12-functions)
        * [Aggregation](#aggregation)
        * [Text Processing](#text-processing)
        * [Date and Time Processing](#date-and-time-processing)
        * [Numeric Processing](#numeric-processing)
    * [13. Grouping](#_13-grouping)
    * [14. Subqueries](#_14-subqueries)
    * [15. Joins](#_15-joins)
        * [Inner Join](#inner-join)
        * [Self Join](#self-join)
        * [Natural Join](#natural-join)
        * [Outer Join](#outer-join)
    * [16. Combined Queries](#_16-combined-queries)
    * [17. Views](#_17-views)
    * [18. Stored Procedures](#_18-stored-procedures)
    * [19. Cursors](#_19-cursors)
    * [20. Triggers](#_20-triggers)
    * [21. Transaction Management](#_21-transaction-management)
    * [22. Character Sets](#_22-character-sets)
    * [23. Access Control](#_23-access-control)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Basics

A schema defines how data is stored, what kind of data is stored, and how data is organized. Both databases and tables have schemas.

Primary key values should not be modified or reused. A deleted primary key value should not be assigned as the primary key of a new row.

SQL (Structured Query Language) is standardized by the ANSI standards committee, so standard SQL is also called ANSI SQL. Each DBMS has its own implementation, such as PL/SQL and Transact-SQL.

SQL statements are case-insensitive, but whether database table names, column names, and values are case-sensitive depends on the specific DBMS and configuration.

SQL supports the following three comment styles:

```sql
## comment
SELECT *
FROM mytable; -- comment
/* comment 1
   comment 2 */
```

Database creation and usage:

```sql
CREATE DATABASE test;
USE test;
```

## 2. Create Tables

```sql
CREATE TABLE mytable (
  # int type, not null, auto-increment
  id INT NOT NULL AUTO_INCREMENT,
  # int type, not null, default value 1
  col1 INT NOT NULL DEFAULT 1,
  # variable-length string type, up to 45 characters, nullable
  col2 VARCHAR(45) NULL,
  # date type, nullable
  col3 DATE NULL,
  # set id as the primary key
  PRIMARY KEY (`id`));
```

## 3. Modify Tables

Add a column

```sql
ALTER TABLE mytable
ADD col CHAR(20);
```

Drop a column

```sql
ALTER TABLE mytable
DROP COLUMN col;
```

Drop a table

```sql
DROP TABLE mytable;
```

## 4. Insert

Regular insert

```sql
INSERT INTO mytable(col1, col2)
VALUES(val1, val2);
```

Insert retrieved data

```sql
INSERT INTO mytable1(col1, col2)
SELECT col1, col2
FROM mytable2;
```

Insert the contents of one table into a new table

```sql
CREATE TABLE newtable AS
SELECT * FROM mytable;
```

## 5. Update

```sql
UPDATE mytable
SET col = val
WHERE id = 1;
```

## 6. Delete

```sql
DELETE FROM mytable
WHERE id = 1;
```

**TRUNCATE TABLE** clears a table, meaning it deletes all rows.

```sql
TRUNCATE TABLE mytable;
```

Always use a WHERE clause when performing update and delete operations, otherwise data in the entire table may be damaged. Test with a SELECT statement first to prevent accidental deletion.

## 7. Query

### DISTINCT

Identical values appear only once. DISTINCT applies to all columns, meaning rows are considered identical only when all column values are identical.

```sql
SELECT DISTINCT col1, col2
FROM mytable;
```

### LIMIT

Limits the number of rows returned. It can take two parameters: the first is the starting row, beginning from 0, and the second is the total number of rows to return.

Return the first 5 rows:

```sql
SELECT *
FROM mytable
LIMIT 5;
```

```sql
SELECT *
FROM mytable
LIMIT 0, 5;
```

Return rows 3 through 5:

```sql
SELECT *
FROM mytable
LIMIT 2, 3;
```

## 8. Sorting

-   **ASC**: ascending order (default)
-   **DESC**: descending order

You can sort by multiple columns and specify a different sort order for each column:

```sql
SELECT *
FROM mytable
ORDER BY col1 DESC, col2 ASC;
```

## 9. Filtering

Unfiltered data can be very large, causing unnecessary data to be transferred over the network and wasting network bandwidth. Therefore, use SQL statements to filter unnecessary data as much as possible instead of transferring all data to the client and filtering there.

```sql
SELECT *
FROM mytable
WHERE col IS NULL;
```

The following table shows operators available in the WHERE clause.

| Operator | Description |
| :---: | :---: |
| = | equal to |
| &lt; | less than |
| &gt; | greater than |
| &lt;&gt; != | not equal to |
| &lt;= !&gt; | less than or equal to |
| &gt;= !&lt; | greater than or equal to |
| BETWEEN | between two values |
| IS NULL | is a NULL value |

Note that NULL is different from 0 and from the empty string.

**AND and OR** are used to connect multiple filter conditions. AND has higher precedence. When a filter expression contains multiple AND and OR operators, use () to set precedence and make it clearer.

The **IN** operator matches a set of values. It can also be followed by a SELECT clause to match a set of values obtained from a subquery.

The **NOT** operator negates a condition.

## 10. Wildcards

Wildcards are also used in filtering statements, but they can only be used with text fields.

-   **%** matches \>=0 arbitrary characters.

-   **\_** matches exactly one arbitrary character.

-   **[ ]** matches characters in a set. For example, [ab] matches character a or b. Use the caret ^ to negate the set, meaning characters in the set are not matched.

Use LIKE for wildcard matching.

```sql
SELECT *
FROM mytable
WHERE col LIKE '[^AB]%'; -- any text that does not start with A or B
```

Do not overuse wildcards. Matching with a wildcard at the beginning is very slow.

## 11. Calculated Fields

Completing data conversion and formatting on the database server is often much faster than doing so on the client, and if the converted and formatted data is smaller, network traffic can be reduced.

Calculated fields usually need an alias with **AS**; otherwise, the output field name is the calculation expression.

```sql
SELECT col1 * col2 AS alias
FROM mytable;
```

**CONCAT()** joins two fields. Many databases pad a value with spaces to the column width, so the joined result may contain unnecessary spaces. Use **TRIM()** to remove leading and trailing spaces.

```sql
SELECT CONCAT(TRIM(col1), '(', TRIM(col2), ')') AS concat_col
FROM mytable;
```

## 12. Functions

Functions differ across DBMSs and are therefore not portable. The following mainly covers MySQL functions.

### Aggregation

| Function | Description |
| :---: | :---: |
| AVG() | returns the average value of a column |
| COUNT() | returns the number of rows in a column |
| MAX() | returns the maximum value of a column |
| MIN() | returns the minimum value of a column |
| SUM() | returns the sum of values in a column |

AVG() ignores NULL rows.

Use DISTINCT to aggregate distinct values.

```sql
SELECT AVG(DISTINCT col1) AS avg_col
FROM mytable;
```

### Text Processing

| Function | Description |
| :---: | :---: |
|  LEFT() | left-side characters |
| RIGHT() | right-side characters |
| LOWER() | converts to lowercase characters |
| UPPER() | converts to uppercase characters |
| LTRIM() | removes spaces on the left |
| RTRIM() | removes spaces on the right |
| LENGTH() | length |
| SOUNDEX() | converts to a phonetic value |

**SOUNDEX()** converts a string into an alphanumeric pattern that describes its phonetic representation.

```sql
SELECT *
FROM mytable
WHERE SOUNDEX(col1) = SOUNDEX('apple')
```

### Date and Time Processing


- Date format: YYYY-MM-DD
- Time format: HH:\<zero-width space\>MM:SS

| Function | Description |
| :---: | :---: |
| ADDDATE() | adds to a date (days, weeks, etc.) |
| ADDTIME() | adds to a time (hours, minutes, etc.) |
| CURDATE() | returns the current date |
| CURTIME() | returns the current time |
| DATE() | returns the date part of a date-time value |
| DATEDIFF() | calculates the difference between two dates |
| DATE_ADD() | highly flexible date arithmetic function |
| DATE_FORMAT() | returns a formatted date or time string |
| DAY()| returns the day part of a date |
| DAYOFWEEK() | returns the weekday for a date |
| HOUR() | returns the hour part of a time |
| MINUTE() | returns the minute part of a time |
| MONTH() | returns the month part of a date |
| NOW() | returns the current date and time |
| SECOND() | returns the second part of a time |
| TIME() | returns the time part of a date-time value |
| YEAR() | returns the year part of a date |

```sql
mysql> SELECT NOW();
```

```
2018-4-14 20:25:11
```

### Numeric Processing

| Function | Description |
| :---: | :---: |
| SIN() | sine |
| COS() | cosine |
| TAN() | tangent |
| ABS() | absolute value |
| SQRT() | square root |
| MOD() | remainder |
| EXP() | exponent |
| PI() | pi |
| RAND() | random number |

## 13. Grouping

Put rows with the same data value into the same group.

Aggregate functions can be applied to grouped data, such as computing the average of each group.

The specified grouping field is used for grouping and is also automatically sorted by that field.

```sql
SELECT col, COUNT(*) AS num
FROM mytable
GROUP BY col;
```

GROUP BY automatically sorts by the grouping field. ORDER BY can also sort by aggregate fields.

```sql
SELECT col, COUNT(*) AS num
FROM mytable
GROUP BY col
ORDER BY num;
```

WHERE filters rows, while HAVING filters groups. Row filtering should happen before group filtering.

```sql
SELECT col, COUNT(*) AS num
FROM mytable
WHERE col > 2
GROUP BY col
HAVING num >= 2;
```

Grouping rules:

- The GROUP BY clause appears after the WHERE clause and before the ORDER BY clause.
- Except for aggregate fields, every field in the SELECT statement must appear in the GROUP BY clause.
- Rows with NULL are grouped separately.
- Most SQL implementations do not support GROUP BY columns with variable-length data types.

## 14. Subqueries

A subquery can return data from only one field.

The result of a subquery can be used as a filter condition in a WHERE statement:

```sql
SELECT *
FROM mytable1
WHERE col1 IN (SELECT col2
               FROM mytable2);
```

The following statement retrieves the number of orders for each customer. The subquery executes once for each customer retrieved by the first query:

```sql
SELECT cust_name, (SELECT COUNT(*)
                   FROM Orders
                   WHERE Orders.cust_id = Customers.cust_id)
                   AS orders_num
FROM Customers
ORDER BY cust_name;
```

## 15. Joins

Joins connect multiple tables using the JOIN keyword, and the condition uses ON instead of WHERE.

Joins can replace subqueries and are generally more efficient.

Use AS to assign aliases to column names, calculated fields, and table names. Table aliases simplify SQL statements and support joining the same table.

### Inner Join

An inner join is also called an equijoin and uses the INNER JOIN keyword.

```sql
SELECT A.value, B.value
FROM tablea AS A INNER JOIN tableb AS B
ON A.key = B.key;
```

You can omit explicit INNER JOIN and use a regular query, connecting the columns to be joined from the two tables with equality in WHERE.

```sql
SELECT A.value, B.value
FROM tablea AS A, tableb AS B
WHERE A.key = B.key;
```

### Self Join

A self join can be viewed as a type of inner join, except the joined table is the same table.

Given an employee table containing employee names and departments, find the names of all employees in the same department as Jim.

Subquery version

```sql
SELECT name
FROM employee
WHERE department = (
      SELECT department
      FROM employee
      WHERE name = "Jim");
```

Self-join version

```sql
SELECT e1.name
FROM employee AS e1 INNER JOIN employee AS e2
ON e1.department = e2.department
      AND e2.name = "Jim";
```

### Natural Join

A natural join connects columns with the same name through equality tests. There can be multiple same-name columns.

Difference between inner join and natural join: an inner join provides the columns to join, while a natural join automatically joins all columns with the same name.

```sql
SELECT A.value, B.value
FROM tablea AS A NATURAL JOIN tableb AS B;
```

### Outer Join

An outer join preserves rows without matches. It includes left outer join, right outer join, and full outer join. A left outer join preserves unmatched rows from the left table.

Retrieve order information for all customers, including customers who do not yet have order information.

```sql
SELECT Customers.cust_id, Customer.cust_name, Orders.order_id
FROM Customers LEFT OUTER JOIN Orders
ON Customers.cust_id = Orders.cust_id;
```

customers table:

| cust_id | cust_name |
| :---: | :---: |
| 1 | a |
| 2 | b |
| 3 | c |

orders table:

| order_id | cust_id |
| :---: | :---: |
|1    | 1 |
|2    | 1 |
|3    | 3 |
|4    | 3 |

Result:

| cust_id | cust_name | order_id |
| :---: | :---: | :---: |
| 1 | a | 1 |
| 1 | a | 2 |
| 3 | c | 3 |
| 3 | c | 4 |
| 2 | b | Null |

## 16. Combined Queries

Use **UNION** to combine two queries. If the first query returns M rows and the second returns N rows, the combined query result generally has M+N rows.

Each query must contain the same columns, expressions, and aggregate functions.

Duplicate rows are removed by default. Use UNION ALL if duplicate rows should be retained.

Only one ORDER BY clause can be included, and it must appear at the end of the statement.

```sql
SELECT col
FROM mytable
WHERE col = 1
UNION
SELECT col
FROM mytable
WHERE col =2;
```

## 17. Views

A view is a virtual table. It does not contain data itself, so indexes cannot be applied to it.

Operations on views are the same as operations on ordinary tables.

Views have the following benefits:

- simplify complex SQL operations, such as complex joins;
- use only part of the data from actual tables;
- ensure data security by granting users access only to views;
- change data format and representation.

```sql
CREATE VIEW myview AS
SELECT Concat(col1, col2) AS concat_col, col3*col4 AS compute_col
FROM mytable
WHERE col5 = val;
```

## 18. Stored Procedures

A stored procedure can be viewed as batch processing for a series of SQL operations.

Benefits of stored procedures:

- code encapsulation, providing a certain level of security;
- code reuse;
- high performance because they are precompiled.

Creating stored procedures on the command line requires a custom delimiter because the command line uses ; as the terminator, and stored procedures also contain semicolons. Otherwise, those semicolons are mistakenly treated as terminators, causing syntax errors.

They include three parameter types: in, out, and inout.

Assigning values to variables requires the select into statement.

Only one variable can be assigned at a time; set operations are not supported.

```sql
delimiter //

create procedure myprocedure( out ret int )
    begin
        declare y int;
        select sum(col1)
        from mytable
        into y;
        select y*y into ret;
    end //

delimiter ;
```

```sql
call myprocedure(@ret);
select @ret;
```

## 19. Cursors

Using cursors in stored procedures allows moving through a result set.

Cursors are mainly used in interactive applications where users need to browse and modify arbitrary rows in a dataset.

Four steps for using a cursor:

1. Declare the cursor; this step does not actually retrieve data.
2. Open the cursor.
3. Fetch data.
4. Close the cursor.

```sql
delimiter //
create procedure myprocedure(out ret int)
    begin
        declare done boolean default 0;

        declare mycursor cursor for
        select col1 from mytable;
        # Define a continue handler. When sqlstate '02000' occurs, set done = 1 is executed.
        declare continue handler for sqlstate '02000' set done = 1;

        open mycursor;

        repeat
            fetch mycursor into ret;
            select ret;
        until done end repeat;

        close mycursor;
    end //
 delimiter ;
```

## 20. Triggers

A trigger executes automatically when the following statements are executed on a table: DELETE, INSERT, and UPDATE.

A trigger must specify whether it executes automatically before or after the statement. Use the BEFORE keyword for execution before the statement and AFTER for execution after the statement. BEFORE is used for data validation and cleanup, while AFTER is used for audit trails, recording modifications into another table.

An INSERT trigger contains a virtual table named NEW.

```sql
CREATE TRIGGER mytrigger AFTER INSERT ON mytable
FOR EACH ROW SELECT NEW.col into @result;

SELECT @result; -- get result
```

A DELETE trigger contains a virtual table named OLD, which is read-only.

An UPDATE trigger contains virtual tables named NEW and OLD. NEW can be modified, while OLD is read-only.

MySQL does not allow CALL statements in triggers, meaning stored procedures cannot be called.

## 21. Transaction Management

Basic terms:

- Transaction: a group of SQL statements.
- Rollback: the process of undoing specified SQL statements.
- Commit: writing unstored SQL statement results into database tables.
- Savepoint: a temporary placeholder set during transaction processing. You can roll back to it, unlike rolling back the entire transaction.

SELECT statements cannot be rolled back, and rolling them back would not make sense. CREATE and DROP statements also cannot be rolled back.

MySQL commits transactions implicitly by default. Each statement is treated as a transaction and committed. When a START TRANSACTION statement appears, implicit commit is disabled. After COMMIT or ROLLBACK executes, the transaction closes automatically and implicit commit is restored.

Setting autocommit to 0 disables automatic commit. The autocommit flag applies to each connection, not to the server.

If no savepoint is set, ROLLBACK rolls back to the START TRANSACTION statement. If a savepoint is set and specified in ROLLBACK, rollback returns to that savepoint.

```sql
START TRANSACTION
// ...
SAVEPOINT delete1
// ...
ROLLBACK TO delete1
// ...
COMMIT
```

## 22. Character Sets

Basic terms:

- A character set is a collection of letters and symbols.
- Encoding is the internal representation of members of a character set.
- Collation specifies how characters are compared, mainly for sorting and grouping.

Besides specifying a character set and collation for a table, you can also specify them for columns:

```sql
CREATE TABLE mytable
(col VARCHAR(10) CHARACTER SET latin COLLATE latin1_general_ci )
DEFAULT CHARACTER SET hebrew COLLATE hebrew_general_ci;
```

Collation can be specified during sorting and grouping:

```sql
SELECT *
FROM mytable
ORDER BY col COLLATE latin1_general_ci;
```

## 23. Access Control

MySQL account information is stored in the mysql database.

```sql
USE mysql;
SELECT user FROM user;
```

**Create Account**  

Newly created accounts have no privileges.

```sql
CREATE USER myuser IDENTIFIED BY 'mypassword';
```

**Rename Account**  

```sql
RENAME USER myuser TO newuser;
```

**Delete Account**  

```sql
DROP USER myuser;
```

**View Privileges**  

```sql
SHOW GRANTS FOR myuser;
```

**Grant Privileges**  

Accounts are defined in the form username@host. username@% uses the default host name.

```sql
GRANT SELECT, INSERT ON mydatabase.* TO myuser;
```

**Revoke Privileges**  

GRANT and REVOKE can control access privileges at several levels:

- Entire server, using GRANT ALL and REVOKE ALL.
- Entire database, using ON database.\*.
- Specific table, using ON database.table.
- Specific column.
- Specific stored procedure.

```sql
REVOKE SELECT, INSERT ON mydatabase.* FROM myuser;
```

**Change Password**  

The Password() function must be used for encryption.

```sql
SET PASSWROD FOR myuser = Password('new_password');
```

## References

- Ben Forta. SQL in 10 Minutes, Sams Teach Yourself [M]. People's Posts and Telecommunications Press, 2013.
