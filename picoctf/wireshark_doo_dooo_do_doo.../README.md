# Wireshark doo dooo do doo...
Category: Forensics

## Description
> Can you find the flag? shark1.pcapng.

## Solution

We open the file in Wireshark and saw many frames, of different types: TCP,
HTTP, TLSv1.2, ARP.

We look into some of the top frames and find that many of the HTTP ones are
connecting using the Kerberos authentication protocol, and are therefore
encrypted.

A typical filter is to find for HTTP frames with response code 200 (OK), since
these are requests well formed and had a valid response.

We focus on TCP since there's little chance that the TCP or ARP frames would
have the flag embedded as part of the payload, since they have a somewhat
tight frame.

So we run the filter `http.response_code == 200` and that returns all the
HTTP packets, many of them Kerberos but a few of them have a HTTP/1.1 OK
(text/html)` info. 

Examine the first one of them and it contains a suspicious payload in `text/html`
format.

```
Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}
```

Here we can see that the `cvpbPGS` fits the length and the case change of
`picoCTF` besides the opening and closing brackets being in from and
surrounding a text inside. Therefore we assume that this is the flag, but
unfortunately it's encrypted.

One thing to note about the encrypted is that it is case insensitive i.e: the
lower case `p` corresponding to the `c` in `pico`, is the same letter (`P`)
just in caps for the corresponding `C` in `CTF`.

Since the encoding is using alphabet characters we try to see if it's a simple
substituion cypher like **ROT13**, so we paste this in a online ROT13 decoder
and get:

```
The flag is picoCTF{p33kab00_1_s33_u_deadbeef}
```

Voila the flag!

## Flag
picoCTF{p33kab00_1_s33_u_deadbeef}
