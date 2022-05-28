# 2Warm
Category: General Skills, 50 points

# Description
> Can you convert the number 42 (base 10) to binary (base 2)? 


# Solution

With a little python magic:

```
$ python -c 'print(bin(42)}")'
```

We need to get rid of the `0b` prefix returned by the convention this command
and wrap the value with the usual `picoCTF{ }`.

# Flag
picoCTF{101010}
