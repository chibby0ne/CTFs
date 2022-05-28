# vault-door-training
Category: Reverse Engineering, 50 points

# Description
> Your mission is to enter Dr. Evil's laboratory and retrieve the blueprints
> for his Doomsday Project. The laboratory is protected by a series of locked
> vault doors. Each door is controlled by a computer and requires a password
> to open. Unfortunately, our undercover agents have not been able to obtain
> the secret passwords for the vault doors, but one of our junior agents
> obtained the source code for each vault's computer! You will need to read
> the source code for each level to figure out what the password is for that
> vault door. As a warmup, we have created a replica vault in our training
> facility. The source code for the training vault is here:
> VaultDoorTraining.java

# Solution

This one an extremely trivial flag to find. The content between the brackets
of the flag is written in the source code given, and all that it's missing is
the `picoCTF{` plus a character at the end which as we know from picoCTF, must
be the closing bracket `}`.
We can verify that this is the correct flag, compiling and running the given
program and getting an: "Access Granted"


# Flag
picoCTF{w4rm1ng_Up_w1tH_jAv4_3808d338b46}
