.syntax unified
.cpu cortex-m4

.align 4
.global F5_add
.global F5_mult
.global F5_sqr

.type F5_add, %function
.type F5_mult, %function
.type F5_sqr, %function
			
F5_add:
		PUSH {r4-r12, r14}
		LDR r3, [r0] 
		LDR r4, [r0, #4] 
		LDR r5, [r0, #8]
		LDR r6, [r1] 
		LDR r7, [r1, #4] 
		LDR r8, [r1, #8]
		
		EOR r0, r6, #0xffffffff 
		AND r1, r0, r7
		AND r9, r1, r4

		PUSH {r1}
		EOR r10, r8, #0xffffffff
		ORR r10, r10, r5
		ORR r10, r10, r4
		EOR r10, r10, #0xffffffff
		ORR r9, r9, r10
		EOR r9, r9, #0xffffffff
		ORR r9, r9, r3
		EOR r9, r9, #0xffffffff
		ORR r10, r8, r6
		EOR r11, r5, #0xffffffff
		ORR r10, r10, r11
		EOR r11, r4, #0xffffffff
		ORR r12, r11, r0
		EOR r14, r3, #0xffffffff
		ORR r12, r12, r14
		AND r10, r10, r12
		PUSH {r12}
		ORR r10, r10, r7
		EOR r10, r10, #0xffffffff
		ORR r9, r9, r10
		ORR r10, r0, r4
		ORR r10, r10, r14
		EOR r1, r7, #0xffffffff
		ORR r1, r1, r10
		EOR r1, r1, #0xffffffff
		ORR r1, r1, r9
		
		STR r1, [r2, #8]
		
		AND r1, r0, r3
		ORR r9, r3, r8
		EOR r9, r9, #0xffffffff
		ORR r9, r9, r1
		EOR r9, r9, #0xffffffff
		ORR r9, r9, r11
		AND r9, r9, r10
		ORR r9, r9, r7
		EOR r9, r9, #0xffffffff
		AND r11, r11, r7
		ORR r10, r5, r6
		EOR r10, r10, #0xffffffff
		ORR r12, r3, r0
		EOR r12, r12, #0xffffffff
		ORR r10, r12, r10
		AND r10, r10, r11
		ORR r10, r10, r9
		AND r9, r8, r5
		ORR r10, r10, r9
		POP {r9}
		EOR r1, r7, #0xffffffff
		ORR r1, r1, r9
		EOR r1, r1, #0xffffffff
		ORR r9, r6, r8
		EOR r9, r9, #0xffffffff
		AND r9, r9, r3
		ORR r0, r5, r0
		ORR r0, r0, r3
		EOR r0, r0, #0xffffffff
		ORR r0, r0, r9
		EOR r0, r0, #0xffffffff
		AND r9, r4, r7
		ORR r0, r0, r9
		EOR r0, r0, #0xffffffff
		ORR r0, r0, r1
		POP {r9}
		ORR r9, r9, r8
		AND r9, r9, r5
		AND r12, r8, r4
		AND r12, r12, r14
		ORR r9, r12, r9
		ORR r9, r9, r0
		
		STR r10, [r2, #4]
		STR r9, [r2]
		
		LDR r9, [r2]
		LDR r10, [r2, #4]
		LDR r11, [r2, #8]
		
		POP {r4-r12, r14}
		bx lr
		
F5_mult:
		 PUSH {r4-r12}
		LDR r3, [r0] 
		LDR r4, [r0, #4] 
		LDR r5, [r0, #8]
		LDR r6, [r1] 
		LDR r7, [r1, #4] 
		LDR r8, [r1, #8]
		
		EOR r0, r6, #0xffffffff
		ORR r1, r0, r7
		EOR r1, r1, #0xffffffff
		AND r9, r1, r5
		EOR r10, r4, #0xffffffff
		AND r11, r8, r10
		AND r11, r11, r3
		ORR r11, r11, r9
		EOR r9, r7, #0xffffffff
		ORR r9, r9, r10
		EOR r10, r3, r6
		ORR r10, r10, r9
		EOR r10, r10, #0xffffffff
		ORR r10, r10, r11
		ORR r1, r1, r8 
		AND r1, r1, r4
		EOR r11, r3, #0xffffffff
		ORR r4, r4, r11
		EOR r4, r4, #0xffffffff
		ORR r4, r4, r5
		AND r4, r4, r7
		ORR r1, r1, r4
		AND r4, r5, r8
		ORR r12, r9, r10
		EOR r12, r12, #0xffffffff
		ORR r12, r12, r4
		AND	r0, r0, r5
		AND r11, r11, r8
		ORR r11, r11, r0
		AND r11, r11, r1
		AND r6, r6, r3
		AND r6, r6, r9
		ORR r6, r6, r11
		ORR r6, r6, r12
		
		STR r6, [r2]
		STR r1, [r2, #4]
		STR r10, [r2, #8]		
		
		POP {r4-r12}
		bx lr
	
	
F5_sqr:
		LDR r2, [r0]
		LDR r3, [r0, #4]
		LDR r0, [r0, #8]

		STR r3, [r1, #8]
		
		EOR r3, r3, #0xffffffff
		AND r3, r2, r3
		ORR r3, r3, r0
		EOR r0, r0, r0
		
		STR r3, [r1]
		STR r0, [r1, #4]
		
		bx lr
