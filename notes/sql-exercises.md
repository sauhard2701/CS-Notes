# SQL Exercises
<!-- GFM-TOC -->
* [SQL Exercises](#sql-exercises)
    * [595. Big Countries](#595-big-countries)
    * [627. Swap Salary](#627-swap-salary)
    * [620. Not Boring Movies](#620-not-boring-movies)
    * [596. Classes More Than 5 Students](#596-classes-more-than-5-students)
    * [182. Duplicate Emails](#182-duplicate-emails)
    * [196. Delete Duplicate Emails](#196-delete-duplicate-emails)
    * [175. Combine Two Tables](#175-combine-two-tables)
    * [181. Employees Earning More Than Their Managers](#181-employees-earning-more-than-their-managers)
    * [183. Customers Who Never Order](#183-customers-who-never-order)
    * [184. Department Highest Salary](#184-department-highest-salary)
    * [176. Second Highest Salary](#176-second-highest-salary)
    * [177. Nth Highest Salary](#177-nth-highest-salary)
    * [178. Rank Scores](#178-rank-scores)
    * [180. Consecutive Numbers](#180-consecutive-numbers)
    * [626. Exchange Seats](#626-exchange-seats)
<!-- GFM-TOC -->


## 595. Big Countries

https://leetcode.com/problems/big-countries/description/

### Description

```html
+-----------------+------------+------------+--------------+---------------+
| name            | continent  | area       | population   | gdp           |
+-----------------+------------+------------+--------------+---------------+
| Afghanistan     | Asia       | 652230     | 25500100     | 20343000      |
| Albania         | Europe     | 28748      | 2831741      | 12960000      |
| Algeria         | Africa     | 2381741    | 37100000     | 188681000     |
| Andorra         | Europe     | 468        | 78115        | 3712000       |
| Angola          | Africa     | 1246700    | 20609294     | 100990000     |
+-----------------+------------+------------+--------------+---------------+
```

Find countries with an area greater than 3,000,000 or a population greater than 25,000,000.

```html
+--------------+-------------+--------------+
| name         | population  | area         |
+--------------+-------------+--------------+
| Afghanistan  | 25500100    | 652230       |
| Algeria      | 37100000    | 2381741      |
+--------------+-------------+--------------+
```

### Solution

```sql
SELECT name,
    population,
    area
FROM
    World
WHERE
    area > 3000000
    OR population > 25000000;
```

### SQL Schema

SQL Schema is used to create table structures and import data in a local environment, making local debugging easier.

```sql
DROP TABLE
IF
    EXISTS World;
CREATE TABLE World ( NAME VARCHAR ( 255 ), continent VARCHAR ( 255 ), area INT, population INT, gdp INT );
INSERT INTO World ( NAME, continent, area, population, gdp )
VALUES
    ( 'Afghanistan', 'Asia', '652230', '25500100', '203430000' ),
    ( 'Albania', 'Europe', '28748', '2831741', '129600000' ),
    ( 'Algeria', 'Africa', '2381741', '37100000', '1886810000' ),
    ( 'Andorra', 'Europe', '468', '78115', '37120000' ),
    ( 'Angola', 'Africa', '1246700', '20609294', '1009900000' );
```

## 627. Swap Salary

https://leetcode.com/problems/swap-salary/description/

### Description

```html
| id | name | sex | salary |
|----|------|-----|--------|
| 1  | A    | m   | 2500   |
| 2  | B    | f   | 1500   |
| 3  | C    | m   | 5500   |
| 4  | D    | f   | 500    |
```

Use a single SQL query to reverse the sex field.

```html
| id | name | sex | salary |
|----|------|-----|--------|
| 1  | A    | f   | 2500   |
| 2  | B    | m   | 1500   |
| 3  | C    | f   | 5500   |
| 4  | D    | m   | 500    |
```

### Solution

The XOR result of two equal values is 0, and the XOR result of 0 with any value is that value.

The sex field has only two values, 'f' and 'm', and follows this pattern:

```
'f' ^ ('m' ^ 'f') = 'm' ^ ('f' ^ 'f') = 'm'
'm' ^ ('m' ^ 'f') = 'f' ^ ('m' ^ 'm') = 'f'
```

Therefore, XORing the sex field with 'm' ^ 'f' reverses the sex field.

```sql
UPDATE salary
SET sex = CHAR ( ASCII(sex) ^ ASCII( 'm' ) ^ ASCII( 'f' ) );
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS salary;
CREATE TABLE salary ( id INT, NAME VARCHAR ( 100 ), sex CHAR ( 1 ), salary INT );
INSERT INTO salary ( id, NAME, sex, salary )
VALUES
    ( '1', 'A', 'm', '2500' ),
    ( '2', 'B', 'f', '1500' ),
    ( '3', 'C', 'm', '5500' ),
    ( '4', 'D', 'f', '500' );
```

## 620. Not Boring Movies

https://leetcode.com/problems/not-boring-movies/description/

### Description


```html
+---------+-----------+--------------+-----------+
|   id    | movie     |  description |  rating   |
+---------+-----------+--------------+-----------+
|   1     | War       |   great 3D   |   8.9     |
|   2     | Science   |   fiction    |   8.5     |
|   3     | irish     |   boring     |   6.2     |
|   4     | Ice song  |   Fantacy    |   8.6     |
|   5     | House card|   Interesting|   9.1     |
+---------+-----------+--------------+-----------+
```

Find movies whose id is odd and whose description is not boring, ordered by rating in descending order.

```html
+---------+-----------+--------------+-----------+
|   id    | movie     |  description |  rating   |
+---------+-----------+--------------+-----------+
|   5     | House card|   Interesting|   9.1     |
|   1     | War       |   great 3D   |   8.9     |
+---------+-----------+--------------+-----------+
```

### Solution

```sql
SELECT
    *
FROM
    cinema
WHERE
    id % 2 = 1
    AND description != 'boring'
ORDER BY
    rating DESC;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS cinema;
CREATE TABLE cinema ( id INT, movie VARCHAR ( 255 ), description VARCHAR ( 255 ), rating FLOAT ( 2, 1 ) );
INSERT INTO cinema ( id, movie, description, rating )
VALUES
    ( 1, 'War', 'great 3D', 8.9 ),
    ( 2, 'Science', 'fiction', 8.5 ),
    ( 3, 'irish', 'boring', 6.2 ),
    ( 4, 'Ice song', 'Fantacy', 8.6 ),
    ( 5, 'House card', 'Interesting', 9.1 );
```

## 596. Classes More Than 5 Students

https://leetcode.com/problems/classes-more-than-5-students/description/

### Description

```html
+---------+------------+
| student | class      |
+---------+------------+
| A       | Math       |
| B       | English    |
| C       | Math       |
| D       | Biology    |
| E       | Math       |
| F       | Computer   |
| G       | Math       |
| H       | Math       |
| I       | Math       |
+---------+------------+
```

Find classes with at least five students.

```html
+---------+
| class   |
+---------+
| Math    |
+---------+
```

### Solution

Group by the class column, then use the count aggregate function to count the number of records in each group, and use HAVING to filter. HAVING filters groups, while WHERE filters individual records or rows.

```sql
SELECT
    class
FROM
    courses
GROUP BY
    class
HAVING
    count( DISTINCT student ) >= 5;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS courses;
CREATE TABLE courses ( student VARCHAR ( 255 ), class VARCHAR ( 255 ) );
INSERT INTO courses ( student, class )
VALUES
    ( 'A', 'Math' ),
    ( 'B', 'English' ),
    ( 'C', 'Math' ),
    ( 'D', 'Biology' ),
    ( 'E', 'Math' ),
    ( 'F', 'Computer' ),
    ( 'G', 'Math' ),
    ( 'H', 'Math' ),
    ( 'I', 'Math' );
```

## 182. Duplicate Emails

https://leetcode.com/problems/duplicate-emails/description/

### Description

Email address table:

```html
+----+---------+
| Id | Email   |
+----+---------+
| 1  | a@b.com |
| 2  | c@d.com |
| 3  | a@b.com |
+----+---------+
```

Find duplicate email addresses:

```html
+---------+
| Email   |
+---------+
| a@b.com |
+---------+
```

### Solution

Group by Email and use COUNT to count records. Results greater than or equal to 2 indicate duplicate Email values.

```sql
SELECT
    Email
FROM
    Person
GROUP BY
    Email
HAVING
    COUNT( * ) >= 2;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS Person;
CREATE TABLE Person ( Id INT, Email VARCHAR ( 255 ) );
INSERT INTO Person ( Id, Email )
VALUES
    ( 1, 'a@b.com' ),
    ( 2, 'c@d.com' ),
    ( 3, 'a@b.com' );
```


## 196. Delete Duplicate Emails

https://leetcode.com/problems/delete-duplicate-emails/description/

### Description

Email address table:

```html
+----+---------+
| Id | Email   |
+----+---------+
| 1  | john@example.com |
| 2  | bob@example.com |
| 3  | john@example.com |
+----+---------+
```

Delete duplicate email addresses:

```html
+----+------------------+
| Id | Email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+
```

### Solution

Keep only the row with the smallest Id among identical Email values and delete the others.

Join query:

```sql
DELETE p1
FROM
    Person p1,
    Person p2
WHERE
    p1.Email = p2.Email
    AND p1.Id > p2.Id
```

Subquery:

```sql
DELETE
FROM
    Person
WHERE
    id NOT IN (
        SELECT id 
        FROM ( 
            SELECT min( id ) AS id 
            FROM Person
            GROUP BY email
        ) AS m
    );
```

Note that the solution above nests an extra SELECT statement. Without doing so, the error "You can't specify target table 'Person' for update in FROM clause" occurs. The following demonstrates this incorrect solution.

```sql
DELETE
FROM
    Person
WHERE
    id NOT IN ( 
        SELECT min( id ) AS id 
        FROM Person 
        GROUP BY email 
    );
```

Reference: [pMySQL Error 1093 - Can't specify target table for update in FROM clause](https://stackoverflow.com/questions/45494/mysql-error-1093-cant-specify-target-table-for-update-in-from-clause)

### SQL Schema

Same as 182.

## 175. Combine Two Tables

https://leetcode.com/problems/combine-two-tables/description/

### Description

Person table:

```html
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| PersonId    | int     |
| FirstName   | varchar |
| LastName    | varchar |
+-------------+---------+
PersonId is the primary key column for this table.
```

Address table:

```html
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| AddressId   | int     |
| PersonId    | int     |
| City        | varchar |
| State       | varchar |
+-------------+---------+
AddressId is the primary key column for this table.
```

Find FirstName, LastName, City, and State, regardless of whether a user has filled in address information.

### Solution

This involves the Person and Address tables. When joining these two tables, Person table information must be preserved even if no related information exists in the Address table. Use a left outer join and place the Person table on the left side of LEFT JOIN.

```sql
SELECT
    FirstName,
    LastName,
    City,
    State
FROM
    Person P
    LEFT JOIN Address A
    ON P.PersonId = A.PersonId;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS Person;
CREATE TABLE Person ( PersonId INT, FirstName VARCHAR ( 255 ), LastName VARCHAR ( 255 ) );
DROP TABLE
IF
    EXISTS Address;
CREATE TABLE Address ( AddressId INT, PersonId INT, City VARCHAR ( 255 ), State VARCHAR ( 255 ) );
INSERT INTO Person ( PersonId, LastName, FirstName )
VALUES
    ( 1, 'Wang', 'Allen' );
INSERT INTO Address ( AddressId, PersonId, City, State )
VALUES
    ( 1, 2, 'New York City', 'New York' );
```

## 181. Employees Earning More Than Their Managers

https://leetcode.com/problems/employees-earning-more-than-their-managers/description/

### Description

Employee table:

```html
+----+-------+--------+-----------+
| Id | Name  | Salary | ManagerId |
+----+-------+--------+-----------+
| 1  | Joe   | 70000  | 3         |
| 2  | Henry | 80000  | 4         |
| 3  | Sam   | 60000  | NULL      |
| 4  | Max   | 90000  | NULL      |
+----+-------+--------+-----------+
```

Find employees whose salary is greater than their manager's salary.

### Solution

```sql
SELECT
    E1.NAME AS Employee
FROM
    Employee E1
    INNER JOIN Employee E2
    ON E1.ManagerId = E2.Id
    AND E1.Salary > E2.Salary;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS Employee;
CREATE TABLE Employee ( Id INT, NAME VARCHAR ( 255 ), Salary INT, ManagerId INT );
INSERT INTO Employee ( Id, NAME, Salary, ManagerId )
VALUES
    ( 1, 'Joe', 70000, 3 ),
    ( 2, 'Henry', 80000, 4 ),
    ( 3, 'Sam', 60000, NULL ),
    ( 4, 'Max', 90000, NULL );
```

## 183. Customers Who Never Order

https://leetcode.com/problems/customers-who-never-order/description/

### Description

Customers table:

```html
+----+-------+
| Id | Name  |
+----+-------+
| 1  | Joe   |
| 2  | Henry |
| 3  | Sam   |
| 4  | Max   |
+----+-------+
```

Orders table:

```html
+----+------------+
| Id | CustomerId |
+----+------------+
| 1  | 3          |
| 2  | 1          |
+----+------------+
```

Find customers who have no orders:

```html
+-----------+
| Customers |
+-----------+
| Henry     |
| Max       |
+-----------+
```

### Solution

Left outer join

```sql
SELECT
    C.Name AS Customers
FROM
    Customers C
    LEFT JOIN Orders O
    ON C.Id = O.CustomerId
WHERE
    O.CustomerId IS NULL;
```

Subquery

```sql
SELECT
    Name AS Customers
FROM
    Customers
WHERE
    Id NOT IN ( 
        SELECT CustomerId 
        FROM Orders 
    );
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS Customers;
CREATE TABLE Customers ( Id INT, NAME VARCHAR ( 255 ) );
DROP TABLE
IF
    EXISTS Orders;
CREATE TABLE Orders ( Id INT, CustomerId INT );
INSERT INTO Customers ( Id, NAME )
VALUES
    ( 1, 'Joe' ),
    ( 2, 'Henry' ),
    ( 3, 'Sam' ),
    ( 4, 'Max' );
INSERT INTO Orders ( Id, CustomerId )
VALUES
    ( 1, 3 ),
    ( 2, 1 );
```

## 184. Department Highest Salary

https://leetcode.com/problems/department-highest-salary/description/

### Description

Employee table:

```html
+----+-------+--------+--------------+
| Id | Name  | Salary | DepartmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 70000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
+----+-------+--------+--------------+
```

Department table:

```html
+----+----------+
| Id | Name     |
+----+----------+
| 1  | IT       |
| 2  | Sales    |
+----+----------+
```

Find the information for the highest earner in each department:

```html
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Max      | 90000  |
| Sales      | Henry    | 80000  |
+------------+----------+--------+
```

### Solution

Create a temporary table containing the maximum salary of employees in each department. Group by department and use the MAX() aggregate function to obtain the maximum salary.

Then use a join to find employees in each department whose salary equals the maximum salary in the temporary table.

```sql
SELECT
    D.NAME Department,
    E.NAME Employee,
    E.Salary
FROM
    Employee E,
    Department D,
    ( SELECT DepartmentId, MAX( Salary ) Salary 
     FROM Employee 
     GROUP BY DepartmentId ) M
WHERE
    E.DepartmentId = D.Id
    AND E.DepartmentId = M.DepartmentId
    AND E.Salary = M.Salary;
```

### SQL Schema

```sql
DROP TABLE IF EXISTS Employee;
CREATE TABLE Employee ( Id INT, NAME VARCHAR ( 255 ), Salary INT, DepartmentId INT );
DROP TABLE IF EXISTS Department;
CREATE TABLE Department ( Id INT, NAME VARCHAR ( 255 ) );
INSERT INTO Employee ( Id, NAME, Salary, DepartmentId )
VALUES
    ( 1, 'Joe', 70000, 1 ),
    ( 2, 'Henry', 80000, 2 ),
    ( 3, 'Sam', 60000, 2 ),
    ( 4, 'Max', 90000, 1 );
INSERT INTO Department ( Id, NAME )
VALUES
    ( 1, 'IT' ),
    ( 2, 'Sales' );
```


## 176. Second Highest Salary

https://leetcode.com/problems/second-highest-salary/description/

### Description

```html
+----+--------+
| Id | Salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
```

Find the employee with the second highest salary.

```html
+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+
```

If no result is found, return null instead of returning no data.

### Solution

To return null when no data is found, wrap another SELECT around the query result.

```sql
SELECT
    ( SELECT DISTINCT Salary 
     FROM Employee 
     ORDER BY Salary DESC 
     LIMIT 1, 1 ) SecondHighestSalary;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS Employee;
CREATE TABLE Employee ( Id INT, Salary INT );
INSERT INTO Employee ( Id, Salary )
VALUES
    ( 1, 100 ),
    ( 2, 200 ),
    ( 3, 300 );
```

## 177. Nth Highest Salary

### Description

Find the employee with the N-th highest salary.

### Solution

```sql
CREATE FUNCTION getNthHighestSalary ( N INT ) RETURNS INT BEGIN

SET N = N - 1;
RETURN ( 
    SELECT ( 
        SELECT DISTINCT Salary 
        FROM Employee 
        ORDER BY Salary DESC 
        LIMIT N, 1 
    ) 
);

END
```

### SQL Schema

Same as 176.


## 178. Rank Scores

https://leetcode.com/problems/rank-scores/description/

### Description

Scores table:

```html
+----+-------+
| Id | Score |
+----+-------+
| 1  | 3.50  |
| 2  | 3.65  |
| 3  | 4.00  |
| 4  | 3.85  |
| 5  | 4.00  |
| 6  | 3.65  |
+----+-------+
```

Sort the scores and calculate ranks.

```html
+-------+------+
| Score | Rank |
+-------+------+
| 4.00  | 1    |
| 4.00  | 1    |
| 3.85  | 2    |
| 3.65  | 3    |
| 3.65  | 3    |
| 3.50  | 4    |
+-------+------+
```

### Solution

To calculate the rank of a score, count the number of scores greater than or equal to that score.

| Id | score | number of scores greater than or equal to this score | rank |
| :---: | :---: | :---: | :---: |
| 1 | 4.1 | 3 | 3 |
| 2 | 4.2 | 2 | 2 |
| 3 | 4.3 | 1 | 1 |

Use a join to find records whose score is greater than or equal to a given score:

```sql
SELECT
	*
FROM
    Scores S1
    INNER JOIN Scores S2
    ON S1.score <= S2.score
ORDER BY
    S1.score DESC, S1.Id;
```

| S1.Id | S1.score | S2.Id | S2.score |
| :---: | :---: | :---: | :---: |
|3|	4.3|	3	|4.3|
|2|	4.2|	2|	4.2|
|2|	4.2	|3	|4.3|
|1|	4.1	|1|	4.1|
|1|	4.1	|2|	4.2|
|1|	4.1	|3|	4.3|

Each S1.score corresponds to several records. Group them and count the records in each group as 'Rank'.

```sql
SELECT
    S1.score 'Score',
    COUNT(*) 'Rank'
FROM
    Scores S1
    INNER JOIN Scores S2
    ON S1.score <= S2.score
GROUP BY
    S1.id, S1.score
ORDER BY
    S1.score DESC, S1.Id;
```

| score | Rank |
| :---: | :---: |
| 4.3 | 1 |
| 4.2 | 2 |
| 4.1 | 3 |

The solution above appears correct, but it returns an incorrect result for the following data:

| Id | score |
| :---: | :---: |
| 1 | 4.1 |
| 2 | 4.2 |
| 3 | 4.2 |

| score | Rank |
| :---: | :--: |
|  4.2  |  2   |
|  4.2  |  2   |
|  4.1  |  3   |

The expected result is:

| score | Rank |
| :---: | :--: |
|  4.2  |  1   |
|  4.2  |  1   |
|  4.1  |  2   |

The join result is:

| S1.Id | S1.score | S2.Id | S2.score |
| :---: | :------: | :---: | :------: |
|   2   |   4.2    |   3   |   4.2    |
|   2   |   4.2    |   2   |   4.2    |
|   3   |   4.2    |   3   |   4.2    |
|   3   |   4.2    |   2   |   4.1    |
|   1   |   4.1    |   3   |   4.2    |
|   1   |   4.1    |   2   |   4.2    |
|   1   |   4.1    |   1   |   4.1    |

The desired result places equal scores at the same rank, and identical scores occupy only one position. In the example above, the records with Id=2 and Id=3 have the same highest score, so they tie for first. The record with Id=1 should rank second, not third. Therefore, when using COUNT, use COUNT( DISTINCT S2.score ) so identical scores are counted only once.

```sql
SELECT
    S1.score 'Score',
    COUNT( DISTINCT S2.score ) 'Rank'
FROM
    Scores S1
    INNER JOIN Scores S2
    ON S1.score <= S2.score
GROUP BY
    S1.id, S1.score
ORDER BY
    S1.score DESC;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS Scores;
CREATE TABLE Scores ( Id INT, Score DECIMAL ( 3, 2 ) );
INSERT INTO Scores ( Id, Score )
VALUES
    ( 1, 4.1 ),
    ( 2, 4.1 ),
    ( 3, 4.2 ),
    ( 4, 4.2 ),
    ( 5, 4.3 ),
    ( 6, 4.3 );
```

## 180. Consecutive Numbers

https://leetcode.com/problems/consecutive-numbers/description/

### Description

Numbers table:

```html
+----+-----+
| Id | Num |
+----+-----+
| 1  |  1  |
| 2  |  1  |
| 3  |  1  |
| 4  |  2  |
| 5  |  1  |
| 6  |  2  |
| 7  |  2  |
+----+-----+
```

Find numbers that appear three times consecutively.

```html
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
```

### Solution

```sql
SELECT
    DISTINCT L1.num ConsecutiveNums
FROM
    Logs L1,
    Logs L2,
    Logs L3
WHERE L1.id = l2.id - 1
    AND L2.id = L3.id - 1
    AND L1.num = L2.num
    AND l2.num = l3.num;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS LOGS;
CREATE TABLE LOGS ( Id INT, Num INT );
INSERT INTO LOGS ( Id, Num )
VALUES
    ( 1, 1 ),
    ( 2, 1 ),
    ( 3, 1 ),
    ( 4, 2 ),
    ( 5, 1 ),
    ( 6, 2 ),
    ( 7, 2 );
```

## 626. Exchange Seats

https://leetcode.com/problems/exchange-seats/description/

### Description

The seat table stores the student corresponding to each seat.

```html
+---------+---------+
|    id   | student |
+---------+---------+
|    1    | Abbot   |
|    2    | Doris   |
|    3    | Emerson |
|    4    | Green   |
|    5    | Jeames  |
+---------+---------+
```

Swap students in adjacent seats. If the last seat has an odd id, do not swap the student in that seat.

```html
+---------+---------+
|    id   | student |
+---------+---------+
|    1    | Doris   |
|    2    | Abbot   |
|    3    | Green   |
|    4    | Emerson |
|    5    | Jeames  |
+---------+---------+
```

### Solution

Use multiple UNION operations.

```sql
## Process even ids by subtracting 1
## For example, 2,4,6,... become 1,3,5,...
SELECT
    s1.id - 1 AS id,
    s1.student
FROM
    seat s1
WHERE
    s1.id MOD 2 = 0 UNION
## Process odd ids by adding 1. However, if the largest id is odd, leave it unchanged.
## For example, 1,3,5,... become 2,4,6,...
SELECT
    s2.id + 1 AS id,
    s2.student
FROM
    seat s2
WHERE
    s2.id MOD 2 = 1
    AND s2.id != ( SELECT max( s3.id ) FROM seat s3 ) UNION
## If the largest id is odd, select this row separately
SELECT
    s4.id AS id,
    s4.student
FROM
    seat s4
WHERE
    s4.id MOD 2 = 1
    AND s4.id = ( SELECT max( s5.id ) FROM seat s5 )
ORDER BY
    id;
```

### SQL Schema

```sql
DROP TABLE
IF
    EXISTS seat;
CREATE TABLE seat ( id INT, student VARCHAR ( 255 ) );
INSERT INTO seat ( id, student )
VALUES
    ( '1', 'Abbot' ),
    ( '2', 'Doris' ),
    ( '3', 'Emerson' ),
    ( '4', 'Green' ),
    ( '5', 'Jeames' );
```
