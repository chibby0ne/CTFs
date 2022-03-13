# Get aHEAD

Category: Web Exploitation, 20 points

## Description

> Find the flag being held on this server to get ahead of the competition http://mercury.picoctf.net:47967/

## Solution

Using httppie to make a `HEAD` request and reading the response headers. The
response headers will contain a header named 'flag' with the flag.


## Flag
picoCTF{r3j3ct_th3_du4l1ty_cca66bd3}
