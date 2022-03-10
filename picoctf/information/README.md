# information
Category: Forensics, 10 points

## Description
> Files can always be changed in a secret way. Can you find the flag? cat.jpg

## Solution
First intuition is to check the view the image. No flag was seen in the image.

Then we could perhaps look into the metadata of the image using `exiftool`. 

```
$ exiftool cat.jpg
```

Part of the interesting metadata (ignoring file access/modification/inode change times and exiftool version)

```
File Permissions                : -rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.02
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Current IPTC Digest             : 7a78f3d9cfb1ce42ab5a3aa30573d617
Copyright Notice                : PicoCTF
Application Record Version      : 4
XMP Toolkit                     : Image::ExifTool 10.80
License                         : cGljb0NURnt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9
Rights                          : PicoCTF
Image Width                     : 2560
Image Height                    : 1598
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 2560x1598
Megapixels                      : 4.1
```

In here we can see 2 interesting values, one for `Current IPTC Digest` and
`License`. The first looks like a hex value, but the second one looks like a
base64 encoded value (since it contains upper and lower case letters a-z not
just a-f).

We try decoding the second value and that rendered the flag:

```
$ echo cGljb0NURnt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9 | base64 -d -
```

## Flag
picoCTF{the_m3tadata_1s_modified}
