# MacroHard WeakEdge
Category: Forensics

## Description
> I've hidden a flag in this file. Can you find it? Forensics is fun.pptm

## Solution

Opening the file and examining the slides doesn't reveal any particular
important clue.

Looked for the metadata of the file. Seems it was created by a "John" in 2020,
but nothing else out of the ordinary.

Afterwards ran it through `strings | grep pico` but that didn't render
anything as well.

Tried opening the pptm with vim and that showed me that the file is indeed a
zipfile of many different files containing, styles, each slide, metadata,
etc... But mostly xml files.

So I unzipped the pptm and started looking around.

After examining the directories, and perusing files I found a file named `hidden` which contained a series of ASCII characters separated by spaces.

Copied that and tried ROT13 and several different ROTs to no avail.

Then after a bit noticed that it could be base64 at which point I opened
wikipedia and looked at the alphabet of characters possible which showed that
indeed they were all valid base64 encoding characters.

Proceeded to decode it but got an error from the base64 tool saying invalid
input.

That's because the whitespaces are not valid base64 characters, so I tried a
bit of piping through tr removing the space and then to base64 decoding which
rendered the flag.

## Flag
picoCTF{D1d_u_kn0w_ppts_r_z1p5}
