	.def	@feat.00;
	.scl	3;
	.type	0;
	.endef
	.globl	@feat.00
@feat.00 = 0
	.file	"out.ll"
	.def	main;
	.scl	2;
	.type	32;
	.endef
	.text
	.globl	main                            # -- Begin function main
	.p2align	4
main:                                   # @main
.seh_proc main
# %bb.0:                                # %entry
	subq	$40, %rsp
	.seh_stackalloc 40
	.seh_endprologue
	movl	$6, %eax
	addl	$5, %eax
	movl	%eax, 36(%rsp)
	movl	36(%rsp), %edx
	leaq	.L.fmt(%rip), %rcx
	callq	printf
	xorl	%eax, %eax
	.seh_startepilogue
	addq	$40, %rsp
	.seh_endepilogue
	retq
	.seh_endproc
                                        # -- End function
	.section	.rdata,"dr"
.L.fmt:                                 # @.fmt
	.asciz	"%d\n"

	.addrsig
	.addrsig_sym printf
