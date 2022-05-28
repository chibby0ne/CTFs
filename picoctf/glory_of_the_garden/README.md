# Glory of the Garden
Category: Forensics, 50 points

# Description
> This garden contains more than it seems.

# Solution

As with any CTF with images, we run `exiftool` and realize this is a
`JPEG/JFIF` of 6.7 MPixels and 2999x2249 resolution. The flag is not in the
metadata of the image, shown to use by `exiftool`.

We also open the image just to do a quick check that the flag is not hidden
*in the picture*, but unfortunately it's just a picture of a pretty nice
garden.

This in addition gives us a clue, that the image is in fact not corrupted
since a regular image viewer was able to open it, but just in case we examine
the image with `kaitai` visualizer, and check every segment and information
detailed there. The flag is also not plain in the data shown by `kaitai`.

At this point, we start reading the [wikipedia article of
JPEG](https://en.wikipedia.org/wiki/JPEG#Syntax_and_structure), to understand
how the format is structured, what are the segments and sections and what are
the bytes that separate them.

We notice that there's a marker named: `SOI` for Start of image, and it is
encoded as `FF D8` which are in fact the first 2 bytes of the image as seen in
kaitai. And that the image ends with a marker named `EOI` for End of Image,
which is `FF D9`.

Opening up the image with [ImHex](https://github.com/WerWolv/ImHex) we search
for this hex (`FF D9`) and find that **they are in fact located not at the end
of the actual file** and is followed by a bunch of bytes with message to the
reader with the ASCII representation of the flag.

This was something I learned: we can have additional information in JPEG/JFIF
files since the `EOI` bytes don't need to be in the end of the file itself or
at least not having it at the end of the file doesn't corrupt the image file.

# Flag
picoCTF{more_than_m33ts_the_3y33dd2eEF5}
