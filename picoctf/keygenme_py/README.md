# keygenme-py
Category: Reverse Engineering, 30 points

# Description
> keygenme-trial.py

# Solution

This was a rather simple reverse engineer CTF. 

Reading the code from top to bottom we realize that the flag is the key used
to unlock the full version of the arcane calculator.

Most of the flag (and therefore the key) is already shown in plaintext utf-8,
but there's a dynamic part that gets created from the sha-256 has of the
username `GOUGH`.

The check_key function is the one detailing how the key is validated and
contains a check for the first static part as well as the dynamic part (the
part using the hash of the username).

Creating a string that follows the order of the characters checked in from
the hash of the username and inserting it between the static parts renders the flag.

# Flag
picoCTF{1n_7h3_|<3y_of_f911a486}
