<!-- GFM-TOC -->
* [1. Importance of Readability](#1-importance-of-readability)
* [2. Use Names to Express Code Meaning](#2-use-names-to-express-code-meaning)
* [3. Avoid Ambiguous Names](#3-avoid-ambiguous-names)
* [4. Good Code Style](#4-good-code-style)
* [5. Why Write Comments](#5-why-write-comments)
* [6. How to Write Comments](#6-how-to-write-comments)
* [7. Improve Control Flow Readability](#7-improve-control-flow-readability)
* [8. Split Long Expressions](#8-split-long-expressions)
* [9. Variables and Readability](#9-variables-and-readability)
* [10. Extract Functions](#10-extract-functions)
* [11. Do One Thing at a Time](#11-do-one-thing-at-a-time)
* [12. Describe Code in Natural Language](#12-describe-code-in-natural-language)
* [13. Reduce Code Size](#13-reduce-code-size)
* [References](#references)
<!-- GFM-TOC -->


# 1. Importance of Readability

A large part of programming time is spent reading code, not only your own code but also other people's code. Therefore, readable code can greatly improve programming efficiency.

Readable code often leads to better code architecture because programmers are more willing to modify it, and it is easier to modify.

Readability should only be sacrificed for efficiency in core areas. Otherwise, readability comes first.

# 2. Use Names to Express Code Meaning

Some more expressive words:

| Word | Alternatives |
| :---: | --- |
| send | deliver、dispatch、announce、distribute、route  |
| find  |  search、extract、locate、recover |
| start| launch、create、begin、open|
| make | create、set up、build、generate、compose、add、new |

Using i, j, and k as loop iterator names is too simple. Names such as user_i and member_i are more expressive. The more nested the loops are, the harder the code is to understand, and expressive iterator names improve readability.

Adding adjectives and other information to names makes them more expressive, but also longer. The guideline for name length is: the larger the scope, the longer the name. Therefore, simple names should only be used in short scopes.

# 3. Avoid Ambiguous Names

After choosing a name, think about how others might interpret it and whether they could misunderstand the intended meaning.

Boolean-related names should use prefixes such as is, can, should, and has.

- Use min and max to express numeric ranges.
- Use first and last to express inclusive ranges in an access space.

- begin and end express an exclusive range in an access space, meaning end does not include the tail.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191209003453268.png"/> </div><br>

# 4. Good Code Style

Use appropriate blank lines and indentation.

Neatly aligned comments:

```java
int a = 1;   // comment
int b = 11;  // comment
int c = 111; // comment
```

Statement order should not be arbitrary. For example, assignments to variables associated with an HTML form should follow the same order as the form in the HTML.

# 5. Why Write Comments

When reading code, comments are noticed first. If the comments are not very useful, they waste code-reading time. Code whose meaning is immediately clear does not need comments. In particular, not every method needs a comment, such as simple getter and setter methods. Adding comments to these methods can make the code less readable.

Do not choose careless names just because comments exist. Instead, strive to choose good names and avoid comments when possible.

Comments can record the reasoning behind the current solution, making the code easier for readers to understand.

Comments can be used to remind readers about special cases.

Use TODO and similar markers:

| Marker | Usage |
|---|---|
|TODO| To do |
|FIXME| Needs fixing |
|HACK| Rough solution |
|XXX| Danger! There is an important issue here |

# 6. How to Write Comments

Be as concise and clear as possible:

```java
// The first String is student's name
// The Second Integer is student's score
Map<String, Integer> scoreMap = new HashMap<>();
```

```java
// Student's name -> Student's score
Map<String, Integer> scoreMap = new HashMap<>();
```

Add test cases for illustration:

```java
// ...
// Example: add(1, 2), return 3
int add(int x, int y) {
    return x + y;
}
```

Use professional terms to shorten conceptual explanations, such as using design pattern names to explain code.

# 7. Improve Control Flow Readability

In conditional expressions, place variables on the left and constants on the right. For example, the first statement below is correct:

```java
if (len < 10)
if (10 > len)
```

Use the ? : ternary operator to make code more compact only when the logic is simple; otherwise, split it into if / else.

The condition of do / while appears at the end, which is not simple and clear and can be confusing. Prefer while instead.

If there is only one goto target, goto may still be acceptable, but overly complex goto usage makes code especially hard to read and should be avoided.

In nested loops, using return statements can often reduce the number of nesting levels.

# 8. Split Long Expressions

Long expressions are hard to read. Introduce explanatory variables to split expressions:

```python
if line.split(':')[0].strip() == "root":
    ...
```
```python
username = line.split(':')[0].strip()
if username == "root":
    ...
```

Use De Morgan's laws to simplify some logical expressions:

```java
if (!a && !b) {
    ...
}
```
```java
if (!(a || b)) {
    ...
}
```

# 9. Variables and Readability

**Remove control-flow variables**. In loops, using break or return can reduce the use of control-flow variables.

```java
boolean done = false;
while (/* condition */ && !done) {
    ...
    if ( ... ) {
        done = true;
        continue;
    }
}
```

```java
while(/* condition */) {
    ...
    if ( ... ) {
        break;
    }
}
```

**Reduce variable scope**. The smaller the scope, the easier it is to locate all places where a variable is used.

JavaScript can use closures to reduce scope. In the following code, submit_form is a function variable, and the submitted variable controls that the function is not submitted twice. In the first implementation, submitted is a global variable. In the second implementation, submitted is placed inside an anonymous function, limiting its scope.

```js
submitted = false;
var submit_form = function(form_name) {
    if (submitted) {
        return;
    }
    submitted = true;
};
```

```js
var submit_form = (function() {
    var submitted = false;
    return function(form_name) {
        if(submitted) {
            return;
        }
        submitted = true;
    }
}());  // () makes the outer anonymous function execute immediately
```

Variables not declared with var in JavaScript are global variables, and global variables can easily cause confusion. Therefore, variables should always be declared with var.

Variables should be defined as close as possible to where they are used.

**Example Analysis**

The following text input fields appear on a web page:

```html
<input type = "text" id = "input1" value = "a">
<input type = "text" id = "input2" value = "b">
<input type = "text" id = "input3" value = "">
<input type = "text" id = "input4" value = "d">
```

Now we need to accept a string and place it in the first empty input field. The initial implementation is as follows:

```js
var setFirstEmptyInput = function(new_alue) {
    var found = false;
    var i = 1;
    var elem = document.getElementById('input' + i);
    while (elem != null) {
        if (elem.value === '') {
            found = true;
            break;
        }
        i++;
        elem = document.getElementById('input' + i);
    }
    if (found) elem.value = new_value;
    return elem;
}
```

The implementation above has the following problems:

- found can be removed.
- elem has too large a scope.
- The while loop can be replaced with a for loop.

```js
var setFirstEmptyInput = function(new_value) {
    for (var i = 1; true; i++) {
        var elem = document.getElementById('input' + i);
        if (elem === null) {
            return null;
        }
        if (elem.value === '') {
            elem.value = new_value;
            return elem;
        }
    }
};
```

# 10. Extract Functions

Engineering means splitting a large problem into small problems and then putting the solutions to those problems back together.

First, clarify the high-level goal of a function. Then extract code that does not work directly toward that goal into independent functions.

Introductory code:

```java
int findClostElement(int[] arr) {
    int clostIdx;
    int clostDist = Interger.MAX_VALUE;
    for (int i = 0; i < arr.length; i++) {
        int x = ...;
        int y = ...;
        int z = ...;
        int value = x * y * z;
        int dist = Math.sqrt(Math.pow(value, 2), Math.pow(arr[i], 2));
        if (dist < clostDist) {
            clostIdx = i;
            clostDist = value;
        }
    }
    return clostIdx;
}
```

In the code above, the loop mainly calculates distance. This part does not belong to the code's high-level goal. The high-level goal is to find the value with the minimum distance, so this part can be extracted into an independent function. This also brings additional benefits: it can be tested separately, and program errors can be found and fixed quickly.

```java
public int findClostElement(int[] arr) {
    int clostIdx;
    int clostDist = Interger.MAX_VALUE;
    for (int i = 0; i < arr.length; i++) {
        int dist = computDist(arr, i);
        if (dist < clostDist) {
            clostIdx = i;
            clostDist = value;
        }
    }
    return clostIdx;
}
```

Extracting more functions is not always better. If too much code is extracted, readers may need to jump around constantly when reading the code. Extracting a block into a subfunction is good only when the current function does not need to understand the details of that block and the subfunction can express its content.

Function extraction is also used to reduce code duplication.

# 11. Do One Thing at a Time

Code that does only one thing makes it easy to understand what it does.

Basic process: list all tasks the code performs, then split each task into different functions or different sections.

# 12. Describe Code in Natural Language

First write the code logic in natural language, that is, pseudocode, and then write the code. This makes the code logic clearer.

# 13. Reduce Code Size

Do not overdesign. Many changes occur during coding, and overdesigned content often ends up being useless.

Use standard library implementations more often.

# References

- Dustin Boswell, Trevor, et al. The Art of Readable Code [M]. China Machine Press, 2012.
