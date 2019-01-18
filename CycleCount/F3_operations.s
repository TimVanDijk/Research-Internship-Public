.syntax unified
.cpu cortex-m4

.align 4
.global F3_add
.global F3_mult
.global F3_sqr

.type F3_add, %function
.type F3_mult, %function
.type F3_sqr, %function

F3_add:	
		PUSH {r4-r9}
		
		LDR r3, [r0] 
		LDR r4, [r0, #4] 
		LDR r5, [r1] 
		LDR r6, [r1, #4] 
		
		ORR r7, r5, r6
		EOR r7, r7, #0xFFFFFFFF
		
		ORR r8, r3, r4
		EOR r8, r8, #0xFFFFFFFF

		AND r9, r3, r7
		AND r3, r3, r5
		AND r5, r5, r8
		ORR r9, r9, r5
		AND r7, r4, r7
		ORR r3, r3, r7
		AND r8, r6, r8
		ORR r3, r3, r8
		AND r4, r4, r6
		ORR r4, r4, r9

		STR r4, [r2]
		STR r3, [r2, #4]
		
		POP {r4-r9}
		bx lr
		


F3_mult: 
		PUSH {r4-r7}
	

		LDR r3, [r0] 
		LDR r4, [r0, #4] 
		LDR r5, [r1] 
		LDR r6, [r1, #4] 
		

		AND r7, r3, r5
		AND r3, r3, r6
		AND r6, r4, r6
		AND r5, r4, r5
		
		ORR r7, r7, r6
		ORR r3, r3, r5
		

		STR r7, [r2]
		STR r3, [r2, #4]
		
		POP {r4-r7}
		bx lr
		
F3_sqr:	
		LDR r2, [r0]
		LDR r3, [r0, #4]
		

		EOR r2, r2, r3
		EOR r0, r3, r3
		

		STR r2, [r1]
		STR r0, [r1, #4]	
		
		bx lr
