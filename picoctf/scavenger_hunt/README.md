# Scavenger Hunt
Category: Web Exploitation

## Description
> There is some interesting information hidden around this site  http://mercury.picoctf.net:39491/. Can you find it?

## Solution

First off, tried downloading the website using curl and httpie which rendered
the first part of the flag as a comment in the HTML.

Then I checked the page in the browser simply clicking the buttons or tabs but
nothing to obvious happened.

That's when I checked the developer tools and specifically the Style Editor
and looked at the `mycss.css` which could be seen used in the HTML, where at
the end of the file I found the other second part of the flag.

At this moment I suspected that the third part of the flag would be in the
javascript somewhere.

In the `myjs.js` which again was written in the HTML of the website that was
being used I found a clue but not the flag directly:

```
/* How can I keep Google from indexing my website? */
```

Which after some searching refers to the `noindex` metatag.

This is a type of the type:

```
<meta content="noindex">
```

Located in the `<head>` section of the HTML.

Looking again at the head section of the HTML I didn't find the flag but since the Javascript is available I checked there.

It's not in the javascript function either.

Another way to stop Google from indexing is to add a `X-Robots-Tag` as part of the Response HTTP Headers.

Trying to fake the crawler by passing the User-Agent we receive no such
header.

The third option to stop a crawler from indexing a website is the `robot.txt`
file.

So we try an httppie GET request to: `mercury.picoctf.net:39491/robots.txt`
which gives us the third part (but not the final part).

```
HTTP/1.1 200 OK
Content-Length: 124
Content-Type: text/plain
Last-Modified: Tue, 16 Mar 2021 00:52:54 GMT

User-agent: *
Disallow: /index.html
# Part 3: t_0f_pl4c
# I think this is an apache server... can you Access the next flag?
```

Apache servers have a `.htaccess` file that provide a way to make
configuration changes on a per-directory basis and this hints allures to it.
Checking it renders the fourth part of the flag.

```
# Part 4: 3s_2_lO0k
# I love making websites on my Mac, I can Store a lot of information there.
```

Apple's macOS have a file named `.DS_Store` that it is kind of the analog of
the `.htaccess` for Apache. Checking it we find the fifth and final part of
the flag:

```
Congrats! You completed the scavenger hunt. Part 5: _f7ce8828}
```

## Flag

picoCTF{th4ts_4_l0t_0f_pl4c3s_2_lO0k_f7ce8828}
