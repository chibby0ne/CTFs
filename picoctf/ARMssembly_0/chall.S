	.arch armv8-a
	.file	"chall.c"
	.text
	.align	2
	.global	func1
	.type	func1, %function
func1:
	sub	sp, sp, #16         # sp -= 16
	str	w0, [sp, 12]        # mem[sp + 12] = w0
	str	w1, [sp, 8]         # mem[sp + 8] = w1
	ldr	w1, [sp, 12]        # w1 = mem[sp + 12] = w0
	ldr	w0, [sp, 8]         # w0 = mem[sp + 8] = w1
	cmp	w1, w0              
	bls	.L2                 # Branch to .L2, if (w1 <= w0)
	ldr	w0, [sp, 12]        # else w0 = mem[sp + 12], w0 = w1
	b	.L3                 # jump to .L3
.L2:
	ldr	w0, [sp, 8]         # w0 = mem[sp + 8] = w1
.L3:
	add	sp, sp, 16          # restore stack pointer
	ret                     # return
	.size	func1, .-func1
	.section	.rodata
	.align	3
.LC0:
	.string	"Result: %ld\n"
	.text
	.align	2
	.global	main
	.type	main, %function
main:
    # every register Xmm is a 64bit one, Wmm is the lower 32bit of the Xmm one 
    # x29 is the frame pointer, x30 is the link register
    # Initial sp is fp.
	stp	x29, x30, [sp, -48]!    # sp -= 48, mem[sp - 48] = x29 (fp), mem[sp - 40] = x30 (link register)
	add	x29, sp, 0              # Set x29 = sp, fp = sp
	str	x19, [sp, 16]           # mem[fp + 16] = x19 
	str	w0, [x29, 44]           # mem[fp + 44] = w0 (lower 32bit of x0)
	str	x1, [x29, 32]           # mem[fp + 32] = x1 
	ldr	x0, [x29, 32]           # x0 = mem[fp + 32], x0 = x1
	add	x0, x0, 8               # x0 += 8
	ldr	x0, [x0]                # x0 = memory contents of [x0], mem[fp + 40]
	bl	atoi                    # Branch to atoi and store return address in X30, function call atoi
	mov	w19, w0                 # w19 = w0, (lower 32bit of x0)

	ldr	x0, [x29, 32]           # x0 = mem[fp + 32]
	add	x0, x0, 16              # x0 += 16
	ldr	x0, [x0]                # x0 = memory contents of [x0], mem[fp + 48]
	bl	atoi                    # Branch to atoi and store return address in X30, function call atoi
	mov	w1, w0                  # w1 = w0
	mov	w0, w19                 # w0 = w19, w0 = result of prev atoi

	bl	func1                   # Call func1 with w0 and w1
	mov	w1, w0                  # w1 = w0
	adrp	x0, .LC0            # x0 = address(.LC0)
	add	x0, x0, :lo12:.LC0      # x0 += .LC0
	bl	printf                  # Call printf
	mov	w0, 0                   # w0 = 0, return 0
	ldr	x19, [sp, 16]           # x19 = contents of [sp - 16]
	ldp	x29, x30, [sp], 48      # sp += 48, restore x29 and x30
	ret
	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
