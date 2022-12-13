# ARMssembly 1
Category: Reverse Engineering

## Description
> For what argument does this program print `win` with variables 79, 7 and 3? File: chall_1.S Flag format: picoCTF{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be picoCTF{0055aabb})

## Solution

The source code specifies that this is using the ARMv8-A ISA. This is a 64bit
architecture where registers whose name start with `w*` are the lower 32bits of the
registers same registers referred by `x*`.

First looking at the file we have two sections of code: `main` and `func`.
Let's first analyze main

### main

```asm
main:
	stp	x29, x30, [sp, -48]!
	add	x29, sp, 0
	str	w0, [x29, 28]
	str	x1, [x29, 16]
	ldr	x0, [x29, 16]
	add	x0, x0, 8
	ldr	x0, [x0]
	bl	atoi
	str	w0, [x29, 44]
	ldr	w0, [x29, 44]
	bl	func
	cmp	w0, 0
	bne	.L4
	adrp	x0, .LC0
	add	x0, x0, :lo12:.LC0
	bl	puts
	b	.L6
.L4:
	adrp	x0, .LC1
	add	x0, x0, :lo12:.LC1
	bl	puts
.L6:
	nop
	ldp	x29, x30, [sp], 48
	ret
```

Let's understand what is happening step by step:

```asm
	stp	x29, x30, [sp, -48]!
	add	x29, sp, 0
```

These instructions take care of the so called: call prologue. The first one
stores both `x29` which is frame pointer (`fp`) and `x30` which is the link
register (`lr`). The link register is used at the end of the current function
to restore the program counter to the next instruction. In this case they need
to be stored so that when main is exited the CPU continues on the function
that called this main function. It does by allocating 48 bytes in the stack
and placing them there. In addition it update the stack pointer to point to
the new address.

The second instruction updates the `fp` to match the `sp`.

```asm
	str	w0, [x29, 28]
	str	x1, [x29, 16]
```

Recall that a main function in C is of the form:

```c
int main(int argc, char *argv[])
```

According to the ARM64 ABI, these arguments of the main function are passed
using the registers `w0`, and `x1`.
Where `w0` is `argc` and `x1` is `argv`.

```asm
	add	x0, x0, 8
	ldr	x0, [x0]
```

With these two instructions we take the first argument `argv + 1`, i.e: `argv[1]`.
This is because it is 64bits it means that words are 8 bytes long therefore
adding 8 bytes would address the next element in the array.

The second instructions loads to the register `x0` that address in memory.

In the ARM64 ABI, arguments registers are those in the range `x0`-`x7`. They
are also used for returning values from a function. This is the reason why
it's reusing `x0`.

```asm
	bl	atoi
```

`atoi` is a function that converts a string (or more specifically `char *`) into an int.
So far all main is doing is converting that `argv[1]` into an int, therefore
the assumption is that it was passed a number, otherwise it would return an
error.

```asm
	str	w0, [x29, 44]
	ldr	w0, [x29, 44]
	bl	func
```

The return value is stored in memory in address `[fp + 44]` and then also
passed to `func` as first argument. 

```asm
	cmp	w0, 0
```

The return value of `func` is compared to 0. 

```asm
	bne	.L4
	adrp	x0, .LC0
	add	x0, x0, :lo12:.LC0
	bl	puts
	b	.L6
.L4:
	adrp	x0, .LC1
	add	x0, x0, :lo12:.LC1
	bl	puts
.L6:
	nop
	ldp	x29, x30, [sp], 48
	ret
```

So if the return value of `func` is equals to 0, then it prints using `puts`
the contents of the string in `LC0` which is the one that we are interested in
since its contents are `"You win!"`. If they are not then it jumps to the
label `.L4` where it prints `"You Lose :("`.

Then in both cases it restores the `fp` and `lr` with the addresses stored in
memory. This is the epilogue of the function call.


From main we can tell that we are interested in having a return value from
`func` of `0`.

Now analyzing `func`

### func


```asm
func:
	sub	sp, sp, #32
	str	w0, [sp, 12]
```

To begin it allocates 32 bytes in the stack and stores the argument passed in
address `[sp + 12]` in memory.


```asm
	mov	w0, 79
	str	w0, [sp, 16]
	mov	w0, 7
	str	w0, [sp, 20]
	mov	w0, 3
	str	w0, [sp, 24]
```

Then it stores it `79` `7` and `3` in the stack. This is akin to storing these
in automatic variables in C.

```asm
	ldr	w0, [sp, 20]
	ldr	w1, [sp, 16]
```

Then it's setting: `w0 = 7` and `w1 = 79`.

```asm
	lsl	w0, w1, w0
```

This is a left shift. So this is equivalent to, setting `w0 = 10112`

```asm
	str	w0, [sp, 28]
	ldr	w1, [sp, 28]
	ldr	w0, [sp, 24]
```

Then it saves that value in memory and moves it to `w1` and sets `w0 = 3`

```asm
	sdiv	w0, w1, w0
```

This does a integer division and sets the result to `w0`, so it's setting: `w0 = 3370`.

```asm
	str	w0, [sp, 28]
	ldr	w1, [sp, 28]
	ldr	w0, [sp, 12]
```

Again it saves the result in memory and moves it to `w1`, and now it takes the
argument to the function (the one that was provided by main through `argv[1]`)
and moves it `w0`

```asm
	sub	w0, w1, w0
	str	w0, [sp, 28]
	ldr	w0, [sp, 28]
```

Then it subtracts the `3370` by the argument of the function and stores it in
`w0`, so it's doing: `w0 = 3370 - argv[1]`

```
	add	sp, sp, 32
	ret
```

Then it pops the stack and returns.


From this analysis we can tell that all we need is to pass the value of `3370`
to the compiled program and we shall see the `You win!` message.

We could try compiling the program with a cross compiler and running it with
QEMU in emulation mode to verify this assertion.

Now all that is left is convert the number to hex, remove the `0x` and use a
32bit representation of it.

In python this is done with:
```
'{0:08x}'.format(3370)
```
and finally add the picoCTF flag prefix/suffix.

The following discussion helped me understand the usage of the registers as argc
and argv.
[link](https://github.com/below/HelloSilicon/issues/22#issuecomment-682205151)


## Flag
picoCTF{00000d2a}
