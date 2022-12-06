# Shop
Category: Reverse Engineering

## Description
> Best Stuff - Cheap Stuff, Buy Buy Buy... Store Instance: source. The shop is open for business at nc mercury.picoctf.net 42159.

## Solution

First we run the `file` command as a simple check to see if it can tell us
what type of file it is.

```
$ file source
source: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, Go BuildID=PjavkptB2tPNbBJewQBD/KlDP1g_fpBnKyhti11wQ/JIWBEgtPAt3YPE6g8qd7/pWlMkjZuAYGqbSv46xuR, with debug_info, not stripped
```

From the output we can tell a few things:
* It's a 32bit ELF binary
* It's a Go binary
* Has debug info and it's not stripped

Go is notoriously difficult to reverse engineer with the usual suspects
such as Ghidra or IDA, even so I open them in both of these decompilers and
spent quite a some minutes trying to figure it all out with not much to show,
except that there's a function called: `get_flag` in the package `main` that
reads a file where presumably the flag is located in the server.

So we fallback and run the program and notice that it's about buying and selling
fruits:


```
Welcome to the market!
=====================
You have 40 coins
        Item            Price   Count
(0) Quiet Quiches       10      12
(1) Average Apple       15      8
(2) Fruitful Flag       100     1
(3) Sell an Item
(4) Exit
Choose an option:
```

Looking at the output it's clear that the option number 3, has the flag since
it is named: `Fruitful Flag`.
Unfortunately we only have 40 credits and need 100 to buy it.

After some trial and error of buying and selling, we realize that we can only
sell them at the same price we buy them and after we do so they are removed
from the "market" so to speak.

Therefore there's not arbitrage with respect to buying and selling. Thus our
only option is to play with the number of items to if the bounds are correctly
checked.

After trying to buy huge numbers of fruits, we notice that we actually have a
negative number of credits.

```
Welcome to the market!
=====================
You have 40 coins
        Item            Price   Count
(0) Quiet Quiches       10      12
(1) Average Apple       15      8
(2) Fruitful Flag       100     1
(3) Sell an Item
(4) Exit
Choose an option:
0
How many do you want to buy?
12
You have -80 coins
        Item            Price   Count
(0) Quiet Quiches       10      0
(1) Average Apple       15      8
(2) Fruitful Flag       100     1
(3) Sell an Item
(4) Exit
Choose an option:
```

But technically we shouldn't be able to buy more than what we have, thus this
implies the program doesn't handle the checks of credits or counts correctly.

The assumption here is that the total credits we have after a buy follows the
following formula:

```
final_credits = initial_credits - price * count
```

In our case we had 40 Credits and bought all 12 Quiet Quiches, therefore:

```
final_credits = 40 - 10 * 12
final_credits = 40 - 120
final_credits = -80
```

Considering this formula we could try buying a negative number of items and we
should end up with more credits that what we started with:

```
Welcome to the market!
=====================
You have 40 coins
        Item            Price   Count
(0) Quiet Quiches       10      12
(1) Average Apple       15      8
(2) Fruitful Flag       100     1
(3) Sell an Item
(4) Exit
Choose an option:
0
How many do you want to buy?
-10
You have 140 coins
        Item            Price   Count
(0) Quiet Quiches       10      22
(1) Average Apple       15      8
(2) Fruitful Flag       100     1
(3) Sell an Item
(4) Exit
Choose an option:
```

Success! Once we do that we select the Flag from the menu and receive the
following error:

```
Choose an option:
2
How many do you want to buy?
1
panic: open flag.txt: no such file or directory

goroutine 1 [running]:
main.check(0x810fb10, 0x196701e0)
        /opt/hacksports/shared/staging/Shop_2_2090033420886329/problem_files/source.go:125 +0x36
main.get_flag()
        /opt/hacksports/shared/staging/Shop_2_2090033420886329/problem_files/source.go:118 +0x5b
main.menu(0x1967a0c0, 0x3, 0x4, 0x1967a100, 0x3, 0x4, 0x8c, 0x0, 0x3, 0x4, ...)
        /opt/hacksports/shared/staging/Shop_2_2090033420886329/problem_files/source.go:77 +0x568
main.openShop()
        /opt/hacksports/shared/staging/Shop_2_2090033420886329/problem_files/source.go:28 +0x1aa
main.main()
        /opt/hacksports/shared/staging/Shop_2_2090033420886329/problem_files/source.go:18 +0x17
```

So indeed that seems to be where the flag is located. Now all we have to do is
run in the server and we get the flag:

```
Flag is:  [112 105 99 111 67 84 70 123 98 52 100 95 98 114 111 103 114 97 109 109 101 114 95 55 57 55 98 50 57 50 99 125]
```

This seems to be ASCII so we use an ASCII converter to get the flag!

# Flag
picoCTF{b4d_brogrammer_797b292c}


