# Cookies
Tags: Web Exploitation, 30 points

# Description
Who doesn't love cookies? Try to figure out the best one. http://mercury.picoctf.net:27177/

# Solution

Using web developer tools, and looking at the Response Headers and Response
cookies, noticed that whenever we tried a valid cookie in the form like: "chocolate chip" or
"snickerdoodle", we would get a different response Cookie with `name=23` where
23 would be a specific number for the given cookie, and that another request
one made to the endpoint `/check`.

Therefore all that is needed is to brute force from 0 until we reach the
cookie that will return us the flag in the response body, a POST request to
/search with Cookie:name=#, where # is the number to try. 

BTW The number to get the flag is 18.


# Flag
picoCTF{3v3ry1_l0v3s_c00k135_064663be}
