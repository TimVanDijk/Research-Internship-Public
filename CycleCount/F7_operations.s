.syntax unified
.cpu cortex-m4

.align 4
.global F7_add
.global F7_mult
.global F7_sqr

.type F7_add, %function
.type F7_mult, %function
.type F7_sqr, %function

extra_storage: .int 0,  0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0
		
F7_add:
		PUSH {r4-r12, lr}		
		LDR r14, =extra_storage
		STR r2, [r14]
		
		LDR r3, [r0]
		LDR r4, [r1]
		LDR r6, [r1, #4]
		
		STR r3, [r14, #4]
		STR r4, [r14, #16]
		STR r6, [r14, #20]
		
		AND r5, r3, r4
		EOR r7, r6, #0xffffffff
		ORR r8, r3, r4
		EOR r9, r4, #0xffffffff
		
		LDR r3, [r0, #4]
		LDR r10, [r0, #8]
		LDR r2, [r1, #8]
		
		EOR r11, r10, #0xffffffff
		
		STR r7, [r14, #28]
		STR r3, [r14, #8]
		STR r10, [r14, #12]
		STR r2, [r14, #24]
		STR r9, [r14, #32]
		
		
		ORR r7, r7, r11
		EOR r12, r3, #0xffffffff
		EOR r4, r2, #0xffffffff
		ORR r0, r4, r12
		AND r1, r0, r7
		ORR r2, r4, r11
		AND r1, r1, r2
		ORR r1, r1, r9
		EOR r1, r1, #0xffffffff
		
		ORR r9, r3, r6
		
		STR r9, [r14, #36]
		STR r4, [r14, #40]
		STR r7, [r14, #44]
		STR r2, [r14, #48]
		STR r11, [r14, #52]
		
		ORR r9, r9, r10
		EOR r9, r9, #0xffffffff
		AND r4, r4, r7
		ORR r4, r4, r9
		EOR r4, r4, #0xffffffff
		
		LDR r3, [r14, #16]
		LDR r10, [r14, #4]
		
		ORR r4, r4, r3
		EOR r4, r4, #0xffffffff
		ORR r1, r1, r4
		AND r1, r1, r10
		ORR r12, r12, r3
		ORR r12, r12, r7
		EOR r12, r12, #0xffffffff
		ORR r12, r12, r1
		
		LDR r7, [r14, #28]
		LDR r10, [r14, #36]
		LDR r2, [r14, #16]
		LDR r6, [r14, #24]
		LDR r3, [r14, #48]
		
		ORR r3, r3, r2
		EOR r3, r3, #0xffffffff
		ORR r10, r10, r6
		EOR r10, r10, #0xffffffff
		AND r11, r11, r0
		ORR r11, r11, r10
		AND r11, r11, r2
		ORR r3, r3, r11
		EOR r3, r3, #0xffffffff
		
		LDR r6, [r14, #4]
		
		ORR r0, r0, r7
		AND r0, r0, r3
		ORR r0, r0, r6
		EOR r0, r0, #0xffffffff
		ORR r0, r0, r12

		LDR r3, [r14]
		LDR r11, [r14, #12]
		STR r0, [r3]
		
		EOR r0, r0, #0xffffffff
		ORR r4, r0, r11
		AND r12, r4, r8
		ORR r12, r12, r7
		EOR r12, r12, #0xffffffff
		EOR r6, r6, #0xffffffff
		
		LDR r9, [r14, #20]
		LDR r3, [r14, #32]
		
		ORR r9, r9, r6
		EOR r9, r9, #0xffffffff
		AND r9, r9, r0
		ORR r9, r9, r12
		EOR r9, r9, #0xffffffff
		
		LDR r12, [r14, #48]
		
		ORR r3, r3, r12
		AND r3, r3, r9
		
		LDR r1, [r14, #16]
		LDR r12, [r14, #8]
		LDR r11, [r14, #20]
		LDR r9, [r14, #24]
		
		ORR r3, r3, r12
		EOR r3, r3, #0xffffffff
		ORR r0, r0, r9
		AND r0, r0, r8
		ORR r0, r0, r11
		EOR r0, r0, #0xffffffff
		AND r1, r1, r11
		AND r4, r4, r1
		ORR r4, r4, r0
		
		LDR r0, [r14, #40]
		LDR r8, [r14, #48]
		
		ORR r7, r7, r0
		AND r7, r7, r8
		ORR r7, r7, r6
		EOR r7, r7, #0xffffffff
		ORR r4, r4, r7
		AND r4, r4, r12
		ORR r4, r4, r3
		
		LDR r7, [r14]
		STR r4, [r7, #4]
		
		EOR r4, r4, #0xffffffff
		
		LDR r11, [r14, #52]
		
		AND r7, r11, r4
		ORR r7, r7, r5
		AND r7, r7, r12
		ORR r12, r4, r2
		
		LDR r5, [r14, #36]
		
		AND r2, r12, r5
		ORR r2, r2, r11
		EOR r2, r2, #0xffffffff
		ORR r7, r7, r2
		EOR r7, r7, #0xffffffff
		ORR r7, r7, r9
		EOR r7, r7, #0xffffffff

		EOR r0, r6, #0xffffffff
		AND r2, r0, r11
		AND r2, r2, r1
		ORR r2, r2, r7
		ORR r0, r0, r4
		AND r0, r0, r5
		
		LDR r11, [r14, #8]
		LDR r8, [r14, #12]
		LDR r5, [r14, #44]
		
		ORR r0, r0, r8
		EOR r0, r0, #0xffffffff
		AND r8, r8, r11
		AND r8, r8, r12
		ORR r0, r0, r8
		ORR r6, r6, r5
		EOR r6, r6, #0xffffffff
		ORR r6, r6, r0
		AND r6, r6, r9
		ORR r6, r6, r2
		
		LDR r7, [r14]
		STR r6, [r7, #8]
				
		POP {r4-r12, lr}
		bx lr

F7_mult:
		PUSH {r4-r12, lr}	
		LDR r3, [r0]
		LDR r4, [r0, #4]
		LDR r5, [r0, #8]
		LDR r6, [r1]
		LDR r7, [r1, #4]
		LDR r8, [r1, #8]
		
		AND r9, r3, r8
		ORR r10, r5, r6
		EOR r10, r10, #0xffffffff
		ORR r11, r4, r7
		EOR r11, r11, #0xffffffff
		ORR r10, r10, r11
		AND r9, r9, r10
		ORR r10, r3, r8
		EOR r10, r10, #0xffffffff
		AND r11, r5, r6
		AND r12, r4, r7
		ORR r11, r11, r12
		AND r10, r10, r11
		ORR r9, r9, r10
		EOR r10, r4, #0xffffffff
		AND r10, r10, r5
		PUSH {r10}
		EOR r11, r7, #0xffffffff
		AND r11, r11, r6
		AND r10, r10, r11
		EOR r11, r5, #0xffffffff
		AND r11, r11, r4
		EOR r12, r6, #0xffffffff
		AND r14, r12, r7
		AND r14, r14, r11
		ORR r14, r14, r10
		ORR r14, r14, r9
		
		STR r14, [r2, #8]

		
		EOR r9, r8, #0xffffffff
		AND r9, r9, r6
		AND r9, r9, r11
		AND r12, r12, r8
		LDR r10, [sp]
		AND r12, r12, r10
		ORR r12, r12, r9
		AND r10, r3, r7
		ORR r11, r6, r8
		EOR r11, r11, #0xffffffff
		ORR r14, r4, r5
		EOR r14, r14, #0xffffffff
		ORR r11, r11, r14
		AND r10, r10, r11
		ORR r11, r3, r7
		EOR r11, r11, #0xffffffff
		AND r14, r5, r8
		AND r9, r4, r6
		ORR r9, r9, r14
		AND r9, r9, r11
		ORR r9, r9, r10
		ORR r12, r12, r9
		
		STR r12, [r2, #4]
		
		AND r9, r3, r6
		ORR r10, r5, r7
		EOR r10, r10, #0xffffffff
		ORR r11, r4, r8
		EOR r11, r11, #0xffffffff
		ORR r10, r10, r11
		AND r9, r9, r10
		ORR r10, r3, r6
		EOR r10, r10, #0xffffffff
		AND r11, r7, r5
		AND r12, r4, r8
		ORR r11, r11, r12
		AND r10, r10, r11
		ORR r9, r9, r10
		EOR r10, r8, #0xffffffff
		AND r10, r10, r7
		POP {r11}
		AND r10, r10, r11
		EOR r11, r7, #0xffffffff
		AND r11, r11, r8
		EOR r12, r5, #0xffffffff 
		AND r12, r12, r4
		AND r11, r11, r12
		ORR r10, r10, r11
		ORR r9, r9, r10
		
		STR r9, [r2]
		
		POP {r4-r12, lr}
		bx lr
			
F7_sqr:
		PUSH {r4-r7}
		LDR r2, [r0]
		LDR r3, [r0, #4]
		LDR r4, [r0, #8]
		
		AND r0, r2, r4
		EOR r5, r3, #0xffffffff
		ORR r5, r5, r4
		ORR r5, r5, r2
		EOR r5, r5, #0xffffffff 
		ORR r5, r5, r0
		AND r6, r2, r3
		EOR r7, r4, #0xffffffff
		ORR r7, r7, r3
		ORR r7, r7, r2
		EOR r7, r7, #0xffffffff
		ORR r6, r6, r7
		AND r7, r3, r4
		ORR r3, r3, r4
		EOR r3, r3, #0xffffffff
		AND r3, r3, r2
		ORR r7, r7, r3
		
		STR r7, [r1]
		STR r6, [r1, #4]
		STR r5, [r1, #8]

		POP {r4-r7}

		bx lr
		