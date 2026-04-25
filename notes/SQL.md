<!-- GFM-TOC -->
* [1. Basics](#1-basics)
* [2. Create Tables](#2-create-tables)
* [3. Modify Tables](#3-modify-tables)
* [4. Insert](#4-insert)
* [5. Update](#5-update)
* [6. Delete](#6-delete)
* [7. Query](#7-query)
    * [DISTINCT](#distinct)
    * [LIMIT](#limit)
* [8. Sorting](#8-sorting)
* [9. Filtering](#9-filtering)
* [10. Wildcards](#10-wildcards)
* [11. Calculated Fields](#11-calculated-fields)
* [12. Functions](#12-functions)
    * [Aggregation](#aggregation)
    * [Text Processing](#text-processing)
    * [Date and Time Processing](#date-and-time-processing)
    * [Numeric Processing](#numeric-processing)
* [13. Grouping](#13-grouping)
* [14. Subqueries](#14-subqueries)
* [15. Joins](#15-joins)
    * [Inner Join](#inner-join)
    * [Self Join](#self-join)
    * [Natural Join](#natural-join)
    * [Outer Join](#outer-join)
* [16. Combined Queries](#16-combined-queries)
* [17. Views](#17-views)
* [18. Stored Procedures](#18-stored-procedures)
* [19. Cursors](#19-cursors)
* [20. Triggers](#20-triggers)
* [21. Transaction Management](#21-transaction-management)
* [22. Character Sets](#22-character-sets)
* [23. Access Control](#23-access-control)
* [References](#references)
<!-- GFM-TOC -->


# 1. Basics

A schema defines how data is stored, what kind of data is stored, and how data is decomposed. Both databases and tables have schemas.

Primary-key values must not be modified or reused. A primary-key value from a deleted row should not be assigned to a new row.

SQL (Structured Query Language) is standardized by the ANSI standards committee, so standard SQL is called ANSI SQL. Each DBMS has its own implementation, such as PL/SQL and Transact-SQL.

SQL statements are case-insensitive, but whether database table names, column names, and values are case-sensitive depends on the specific DBMS and its configuration.

SQL supports the following three types of comments:

```sql
# comment
SELECT *
FROM mytable; -- comment
/* comment 1
   comment 2 */
```

Create and use a database:

```sql
CREATE DATABASE test;
USE test;
```

# 2. Create Tables

```sql
CREATE TABLE mytable (
  # int type, not null, auto-increment
  id INT NOT NULL AUTO_INCREMENT,
  # int type, not null, default value 1
  col1 INT NOT NULL DEFAULT 1,
  # variable-length string type, maximum 45 characters, nullable
  col2 VARCHAR(45) NULL,
  # date type, nullable
  col3 DATE NULL,
  # set id as the primary key
  PRIMARY KEY (`id`));
```

# 3. Modify Tables

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

# 4. Insert

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

# 5. Update

```sql
UPDATE mytable
SET col = val
WHERE id = 1;
```

# 6. Delete

```sql
DELETE FROM mytable
WHERE id = 1;
```

**TRUNCATE TABLE**   can clear a table, meaning it deletes all rows.

```sql
TRUNCATE TABLE mytable;
```

Always use a WHERE clause when performing update and delete operations; otherwise, the entire table's data may be damaged. You can test with a SELECT statement first to prevent accidental deletion.

# 7. Query

## DISTINCT

Identical values appear only once. DISTINCT applies to all columns, meaning rows are considered identical only when all selected column values are identical.

```sql
SELECT DISTINCT col1, col2
FROM mytable;
```

## LIMIT

Limits the number of returned rows. It can take two parameters: the first is the starting row, beginning at 0, and the second is the total number of rows to return.

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

# 8. Sorting

-   **ASC**  : ascending order (default)
-   **DESC**  : descending order

You can sort by multiple columns and specify a different sort order for each column:

```sql
SELECT *
FROM mytable
ORDER BY col1 DESC, col2 ASC;
```

# 9. Filtering

Unfiltered data can be very large, causing unnecessary data to be transferred over the network and wasting bandwidth. Therefore, use SQL statements to filter unnecessary data whenever possible instead of transferring all data to the client and filtering there.

```sql
SELECT *
FROM mytable
WHERE col IS NULL;
```

The following table shows operators available in the WHERE clause.

| Operator | Description |
| :---: | :---: |
| = | Equal to |
| &lt; | Less than |
| &gt; | Greater than |
| &lt;&gt; != | Not equal to |
| &lt;= !&gt; | Less than or equal to |
| &gt;= !&lt; | Greater than or equal to |
| BETWEEN | Between two values |
| IS NULL | Is a NULL value |

Note that NULL is different from both 0 and an empty string.

**AND and OR**   are used to connect multiple filter conditions. AND is processed first. When a filter expression involves multiple AND and OR operators, use () to determine precedence and make the precedence relationship clearer.

**IN**   matches a set of values. It can also be followed by a SELECT clause to match a set of values returned by a subquery.

**NOT**   negates a condition.

# 10. Wildcards

Wildcards are also used in filter statements, but they can only be used with text fields.

-   **%**   matches \>=0 arbitrary characters;

-   **\_**   matches exactly 1 arbitrary character;

-   **[ ]**   matches characters in a set. For example, [ab] matches character a or b. The caret ^ can negate it, meaning characters in the set are not matched.

Use LIKE for wildcard matching.

```sql
SELECT *
FROM mytable
WHERE col LIKE '[^AB]%'; -- any text that does not start with A or B
```

Do not overuse wildcards. Matching with a wildcard at the beginning is very slow.

# 11. Calculated Fields

Performing data conversion and formatting on the database server is often much faster than doing it on the client. If the converted and formatted data is smaller, it also reduces network traffic.

Calculated fields usually need an alias using   **AS**  ; otherwise, the output field name is the calculated expression.

```sql
SELECT col1 * col2 AS alias
FROM mytable;
```

**CONCAT()**   connects two fields. Many databases pad a value with spaces to fill the column width, so the concatenated result may contain unnecessary spaces. Use **TRIM()** to remove leading and trailing spaces.

```sql
SELECT CONCAT(TRIM(col1), '(', TRIM(col2), ')') AS concat_col
FROM mytable;
```

# 12. Functions

Functions differ across DBMSs and are therefore not portable. The following are mainly MySQL functions.

## Aggregation

| Function | Description |
| :---: | :---: |
| AVG() | Returns the average value of a column |
| COUNT() | Returns the number of rows in a column |
| MAX() | Returns the maximum value of a column |
| MIN() | Returns the minimum value of a column |
| SUM() | Returns the sum of values in a column |

AVG() ignores NULL rows.

Use DISTINCT to aggregate distinct values.

```sql
SELECT AVG(DISTINCT col1) AS avg_col
FROM mytable;
```

## Text Processing

| Function | Description |
| :---: | :---: |
|  LEFT() | Characters on the left |
| RIGHT() | Characters on the right |
| LOWER() | Convert to lowercase |
| UPPER() | Convert to uppercase |
| LTRIM() | Remove spaces on the left |
| RTRIM() | Remove spaces on the right |
| LENGTH() | Length |
| SOUNDEX() | Convert to a phonetic value |

**SOUNDEX()**   converts a string into an alphanumeric pattern describing its pronunciation.

```sql
SELECT *
FROM mytable
WHERE SOUNDEX(col1) = SOUNDEX('apple')
```

## Date and Time Processing


- Date format: YYYY-MM-DD
- Time format: HH:\<zero-width space\>MM:SS

| Function | Description |
| :---: | :---: |
| ADDDATE() | Add a date interval, such as days or weeks |
| ADDTIME() | Add a time interval, such as hours or minutes |
| CURDATE() | Return the current date |
| CURTIME() | Return the current time |
| DATE() | Return the date part of a date/time value |
| DATEDIFF() | Compute the difference between two dates |
| DATE_ADD() | Highly flexible date arithmetic function |
| DATE_FORMAT() | Return a formatted date or time string |
| DAY()| Return the day part of a date |
| DAYOFWEEK() | Return the day of the week for a date |
| HOUR() | Return the hour part of a time |
| MINUTE() | Return the minute part of a time |
| MONTH() | Return the month part of a date |
| NOW() | Return the current date and time |
| SECOND() | Return the second part of a time |
| TIME() | Return the time part of a date/time value |
| YEAR() | Return the year part of a date |

```sql
mysql> SELECT NOW();
```

```
2018-4-14 20:25:11
```

## Numeric Processing

| Function | Description |
| :---: | :---: |
| SIN() | Sine |
| COS() | Cosine |
| TAN() | Tangent |
| ABS() | Absolute value |
| SQRT() | Square root |
| MOD() | Remainder |
| EXP() | Exponent |
| PI() | Pi |
| RAND() | Random number |

# 13. Grouping

Put rows with the same data value into the same group.

Aggregate functions can be applied to grouped data, such as computing the average value for each group.

The specified grouping field not only groups by that field but also automatically sorts by that field.

```sql
SELECT col, COUNT(*) AS num
FROM mytable
GROUP BY col;
```

GROUP BY automatically sorts by the grouping field, and ORDER BY can also sort by aggregate fields.

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

- The GROUP BY clause appears after the WHERE clause and before the ORDER BY clause;
- Except for aggregate fields, every field in the SELECT statement must appear in the GROUP BY clause;
- Rows with NULL are grouped separately;
- Most SQL implementations do not support GROUP BY columns with variable-length data types.

# 14. Subqueries

A subquery can return data from only one field.

The result of a subquery can be used as a filter condition in a WHERE statement:

```sql
SELECT *
FROM mytable1
WHERE col1 IN (SELECT col2
               FROM mytable2);
```

The following statement retrieves the number of orders for each customer. The subquery executes once for every customer retrieved by the first query:

```sql
SELECT cust_name, (SELECT COUNT(*)
                   FROM Orders
                   WHERE Orders.cust_id = Customers.cust_id)
                   AS orders_num
FROM Customers
ORDER BY cust_name;
```

# 15. Joins

Joins connect multiple tables using the JOIN keyword, and the condition uses ON instead of WHERE.

Joins can replace subqueries and are usually more efficient.

AS can be used to alias column names, calculated fields, and table names. Aliasing table names simplifies SQL statements and helps when joining the same table.

## Inner Join

An inner join is also called an equijoin and uses the INNER JOIN keyword.

```sql
SELECT A.value, B.value
FROM tablea AS A INNER JOIN tableb AS B
ON A.key = B.key;
```

You can omit the explicit INNER JOIN and use a normal query, connecting the columns from two tables with equality in the WHERE clause.

```sql
SELECT A.value, B.value
FROM tablea AS A, tableb AS B
WHERE A.key = B.key;
```

## Self Join

A self join can be viewed as a type of inner join where the joined table is the same table.

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

## Natural Join

A natural join connects columns with the same name through equality tests. There can be multiple same-named columns.

Difference between inner join and natural join: an inner join specifies the join columns, while a natural join automatically joins all columns with the same name.

```sql
SELECT A.value, B.value
FROM tablea AS A NATURAL JOIN tableb AS B;
```

## Outer Join

Outer joins preserve rows that do not have matching rows. They include left outer joins, right outer joins, and full outer joins. A left outer join preserves unmatched rows from the left table.

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

# 16. Combined Queries

Use   **UNION**   to combine two queries. If the first query returns M rows and the second returns N rows, the combined query usually returns M+N rows.

Each query must contain the same columns, expressions, and aggregate functions.

Duplicate rows are removed by default. Use UNION ALL to keep duplicate rows.

Only one ORDER BY clause is allowed, and it must be at the end of the statement.

```sql
SELECT col
FROM mytable
WHERE col = 1
UNION
SELECT col
FROM mytable
WHERE col =2;
```

# 17. Views

A view is a virtual table. It does not contain data itself, so indexes cannot be created on it.

Operations on views are the same as operations on normal tables.

Views have the following benefits:

- Simplify complex SQL operations, such as complex joins;
- Use only part of the data from the underlying tables;
- Ensure data security by granting users access only to views;
- Change data format and presentation.

```sql
CREATE VIEW myview AS
SELECT Concat(col1, col2) AS concat_col, col3*col4 AS compute_col
FROM mytable
WHERE col5 = val;
```

# 18. Stored Procedures

Stored procedures can be viewed as batch processing for a series of SQL operations.

Benefits of using stored procedures:

- Code encapsulation, providing a certain level of security;
- Code reuse;
- High performance because they are precompiled.

Creating a stored procedure in the command line requires a custom delimiter because the command line uses ; as the terminator, and the stored procedure also contains semicolons. Otherwise, those semicolons may be incorrectly treated as terminators and cause syntax errors.

There are three kinds of parameters: in, out, and inout.

Use select into statements to assign values to variables.

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

# 19. Cursors

Using a cursor in a stored procedure allows moving through and traversing a result set.

Cursors are mainly used in interactive applications where users need to browse and modify arbitrary rows in a dataset.

The four steps for using a cursor:

1. Declare the cursor; this step does not actually retrieve data;
2. Open the cursor;
3. Fetch data;
4. Close the cursor;

```sql
delimiter //
create procedure myprocedure(out ret int)
    begin
        declare done boolean default 0;

        declare mycursor cursor for
        select col1 from mytable;
        # Define a continue handler; when sqlstate '02000' occurs, execute set done = 1
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

# 20. Triggers

Triggers execute automatically when the following statements are run on a table: DELETE, INSERT, and UPDATE.

A trigger must specify whether it runs before or after the statement. Use the BEFORE keyword for execution before the statement, and AFTER for execution after it. BEFORE is used for data validation and cleanup, while AFTER is used for audit tracking, recording changes into another table.

An INSERT trigger contains a virtual table named NEW.

```sql
CREATE TRIGGER mytrigger AFTER INSERT ON mytable
FOR EACH ROW SELECT NEW.col into @result;

SELECT @result; -- get the result
```

A DELETE trigger contains a virtual table named OLD, which is read-only.

An UPDATE trigger contains virtual tables named NEW and OLD. NEW can be modified, while OLD is read-only.

MySQL does not allow CALL statements in triggers, meaning stored procedures cannot be called.

# 21. Transaction Management

Basic terms:

- A transaction is a group of SQL statements;
- Rollback is the process of undoing specified SQL statements;
- Commit writes the results of unstored SQL statements to database tables;
- A savepoint is a temporary placeholder set during transaction processing. You can roll back to it, which is different from rolling back the entire transaction.

SELECT statements cannot be rolled back, and rolling them back would not be meaningful. CREATE and DROP statements also cannot be rolled back.

MySQL commits transactions implicitly by default. Each statement is treated as a transaction and committed after execution. When a START TRANSACTION statement appears, implicit commit is disabled. After a COMMIT or ROLLBACK statement executes, the transaction closes automatically and implicit commit is restored.

Setting autocommit to 0 disables automatic commit. The autocommit flag applies to each connection, not to the server.

If no savepoint is set, ROLLBACK rolls back to the START TRANSACTION statement. If a savepoint is set and specified in ROLLBACK, the transaction rolls back to that savepoint.

```sql
START TRANSACTION
// ...
SAVEPOINT delete1
// ...
ROLLBACK TO delete1
// ...
COMMIT
```

# 22. Character Sets

Basic terms:

- A character set is a collection of letters and symbols;
- Encoding is the internal representation of members of a character set;
- Collation specifies how characters are compared, mainly for sorting and grouping.

In addition to specifying the character set and collation for a table, they can also be specified for a column:

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

# 23. Access Control

MySQL account information is stored in the mysql database.

```sql
USE mysql;
SELECT user FROM user;
```

**Create Account**  

Newly created accounts have no permissions.

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

**View Permissions**  

```sql
SHOW GRANTS FOR myuser;
```

**Grant Permissions**  

Accounts are defined in the form username@host. username@% uses the default host name.

```sql
GRANT SELECT, INSERT ON mydatabase.* TO myuser;
```

**Revoke Permissions**  

GRANT and REVOKE can control access at several levels:

- Entire server, using GRANT ALL and REVOKE ALL;
- Entire database, using ON database.\*;
- Specific table, using ON database.table;
- Specific columns;
- Specific stored procedures.

```sql
REVOKE SELECT, INSERT ON mydatabase.* FROM myuser;
```

**Change Password**  

The Password() function must be used for encryption.

```sql
SET PASSWROD FOR myuser = Password('new_password');
```

# References

- Ben Forta. SQL in 10 Minutes, Sams Teach Yourself[M]. Posts and Telecom Press, 2013.
