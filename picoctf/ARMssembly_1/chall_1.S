	.arch armv8-a
	.file	"chall_1.c"
	.text
	.align	2
	.global	func
	.type	func, %function
func:
	sub	sp, sp, #32
	str	w0, [sp, 12]
	mov	w0, 79
    # [sp, 16] = 79
	str	w0, [sp, 16]
	mov	w0, 7
    # [sp, 20] = 7
	str	w0, [sp, 20]
	mov	w0, 3
    # [sp, 24] = 3
	str	w0, [sp, 24]
    # w0 = 7
	ldr	w0, [sp, 20]
    # w1 = 79
	ldr	w1, [sp, 16]
    # w0 = 79 << 7 (w0 = 10112)
	lsl	w0, w1, w0
    # [sp, 28] = 10112
	str	w0, [sp, 28]
    # w1 = 10112
	ldr	w1, [sp, 28]
    # w0 = 3
	ldr	w0, [sp, 24]
    # w0 = 10112 // 3 (w0 = 3370)
	sdiv	w0, w1, w0
    # [sp, 28] = 3370
	str	w0, [sp, 28]
    # w1 = 3370
	ldr	w1, [sp, 28]
    # w0 = argument passed to func (is an int)
	ldr	w0, [sp, 12]
    # w0 -= 3370
	sub	w0, w1, w0
    # [sp, 28] = w0
	str	w0, [sp, 28]
    # w0 = [sp, 28]
	ldr	w0, [sp, 28]
    # epilogue
	add	sp, sp, 32
	ret
	.size	func, .-func
	.section	.rodata
	.align	3
.LC0:
	.string	"You win!"
	.align	3
.LC1:
	.string	"You Lose :("
	.text
	.align	2
	.global	main
	.type	main, %function
main:
	stp	x29, x30, [sp, -48]!
	add	x29, sp, 0

    # [fp + 28] = argc
	str	w0, [x29, 28]

    # [fp + 16] = &(argv)
	str	x1, [x29, 16]

    # x0 = &(argv)
	ldr	x0, [x29, 16]

    # x0 += 8 -> x0 = &(argv[1])
	add	x0, x0, 8

    # x0 = [x0] -> x0 = contents of &(argv[1]) (i.e: argv [1])
	ldr	x0, [x0]

    # convert to int
	bl	atoi

    # [x29, 44] = atoi(something)
	str	w0, [x29, 44]
	ldr	w0, [x29, 44]

    # func(x0)
	bl	func

    # if x0 == 0:
	cmp	w0, 0

    # else jump to .L4
	bne	.L4

    # print 'you win'
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
	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
