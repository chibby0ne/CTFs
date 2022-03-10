# Python Wrangling
Category: General Skills

## Description
> Python scripts are invoked kind of like programs in the Terminal... Can you run this Python script using this password to get the flag?

## Solution

After looking into the python code, we can see the flag used and the order of
the arguments that need to be provided which is:

``` 
python ende.py -d flag.txt.en $(cat pw.txt)
```

## Flag
picoCTF{4p0110_1n_7h3_h0us3_dbd1bea4}
