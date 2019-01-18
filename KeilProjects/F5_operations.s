		AREA Program, CODE, READONLY
		ENTRY
		EXPORT F5_add
		EXPORT F5_mult
		EXPORT F5_sqr
			
F5_add	PUSH {r4-r12, r14}
		LDR r3, [r0] 		; Loads a0 into r3
		LDR r4, [r0, #4] 	; Loads a1 into r4	
		LDR r5, [r0, #8]	; Loads a2 into r5
		LDR r6, [r1] 		; Loads b0 into r6
		LDR r7, [r1, #4] 	; Loads b1 into r7
		LDR r8, [r1, #8]	; Loads b2 into r8
		
		EOR r0, r6, #0xffffffff 	; 1
		AND r1, r0, r7				; 2
		AND r9, r1, r4				; 3
		; We don't need the value in r1 until 47; free up the register
		PUSH {r1}
		EOR r10, r8, #0xffffffff	; 4
		ORR r10, r10, r5			; 5
		ORR r10, r10, r4			; 6
		EOR r10, r10, #0xffffffff	; 6
		ORR r9, r9, r10				; 7 - r10 freed
		EOR r9, r9, #0xffffffff		; 7
		ORR r9, r9, r3				; 8
		EOR r9, r9, #0xffffffff		; 8
		ORR r10, r8, r6				; 9
		EOR r11, r5, #0xffffffff	; 10
		ORR r10, r10, r11			; 11 - r11 freed
		EOR r11, r4, #0xffffffff	; 12
		ORR r12, r11, r0			; 13
		EOR r14, r3, #0xffffffff	; 14
		ORR r12, r12, r14			; 15
		AND r10, r10, r12			; 16 - r12 freed
		PUSH {r12}
		ORR r10, r10, r7			; 17
		EOR r10, r10, #0xffffffff	; 17
		ORR r9, r9, r10				; 18 - r10 freed
		ORR r10, r0, r4				; 19
		ORR r10, r10, r14			; 20
		EOR r1, r7, #0xffffffff		; 21
		ORR r1, r1, r10				; 22
		EOR r1, r1, #0xffffffff		; 22
		ORR r1, r1, r9				; 23 - r9 freed
		
		STR r1, [r2, #8]			; Store c2 to memory and free up r1
		
		AND r1, r0, r3				; 24
		ORR r9, r3, r8				; 25
		EOR r9, r9, #0xffffffff		; 25
		ORR r9, r9, r1				; 26 - r1 freed
		EOR r9, r9, #0xffffffff		; 26
		ORR r9, r9, r11				; 27
		AND r9, r9, r10				; 28 - r10 freed
		ORR r9, r9, r7				; 29
		EOR r9, r9, #0xffffffff		; 29
		AND r11, r11, r7			; 30
		ORR r10, r5, r6				; 31
		EOR r10, r10, #0xffffffff	; 31
		ORR r12, r3, r0				; 32
		EOR r12, r12, #0xffffffff	; 32
		ORR r10, r12, r10			; 33 - r10 freed
		AND r10, r10, r11			; 34 - r11 freed
		ORR r10, r10, r9			; 35 - r9 freed
		AND r9, r8, r5				; 36
		ORR r10, r10, r9			; 37 - r9 freed
		POP {r9}					; Restore output of 15
		EOR r1, r7, #0xffffffff		; recompute ~b1 as input for 38
		ORR r1, r1, r9				; 38 - r12 freed
		EOR r1, r1, #0xffffffff		; 38
		ORR r9, r6, r8				; 39
		EOR r9, r9, #0xffffffff		; 39
		AND r9, r9, r3				; 40
		ORR r0, r5, r0				; 41
		ORR r0, r0, r3				; 42
		EOR r0, r0, #0xffffffff		; 42
		ORR r0, r0, r9				; 43 - r9 freed
		EOR r0, r0, #0xffffffff		; 43
		AND r9, r4, r7				; 44
		ORR r0, r0, r9				; 45 - r9 freed
		EOR r0, r0, #0xffffffff		; 45
		ORR r0, r0, r1				; 46
		POP {r9}					; Fetch result of 2 from stack to compute 47
		ORR r9, r9, r8				; 47
		AND r9, r9, r5				; 48 - r12 freed
		AND r12, r8, r4				; 49
		AND r12, r12, r14			; 50 - r14 freed
		ORR r9, r12, r9				; 51 - r12 freed
		ORR r9, r9, r0				; 52
		
		STR r10, [r2, #4]			; Store c1 to memory
		STR r9, [r2]				; Store c0 to memory		
		
		LDR r9, [r2]
		LDR r10, [r2, #4]
		LDR r11, [r2, #8]
		
		POP {r4-r12, r14}
		bx lr
		
F5_mult PUSH {r4-r12}
		LDR r3, [r0] 		; Loads a0 into r3
		LDR r4, [r0, #4] 	; Loads a1 into r4	
		LDR r5, [r0, #8]	; Loads a2 into r5
		LDR r6, [r1] 		; Loads b0 into r6
		LDR r7, [r1, #4] 	; Loads b1 into r7
		LDR r8, [r1, #8]	; Loads b2 into r8
		
		EOR r0, r6, #0xffffffff		; 1
		ORR r1, r0, r7				; 2
		EOR r1, r1, #0xffffffff		; 2
		AND r9, r1, r5				; 3
		EOR r10, r4, #0xffffffff	; 4
		AND r11, r8, r10			; 5
		AND r11, r11, r3			; 6
		ORR r11, r11, r9			; 7 - r9 freed
		EOR r9, r7, #0xffffffff		; 8
		ORR r9, r9, r10				; 9 - r10 freed
		EOR r10, r3, r6				; 10
		ORR r10, r10, r9			; 11
		EOR r10, r10, #0xffffffff	; 11
		ORR r10, r10, r11			; 12 - r11 freed
		ORR r1, r1, r8 				; 13
		AND r1, r1, r4				; 14
		EOR r11, r3, #0xffffffff	; 15
		ORR r4, r4, r11				; 16
		EOR r4, r4, #0xffffffff		; 16
		ORR r4, r4, r5				; 17
		AND r4, r4, r7				; 18
		ORR r1, r1, r4				; 19 - r4 freed
		AND r4, r5, r8				; 20
		ORR r12, r9, r10			; 21
		EOR r12, r12, #0xffffffff	; 21
		ORR r12, r12, r4			; 22 - r4 freed
		AND	r0, r0, r5				; 23
		AND r11, r11, r8			; 24
		ORR r11, r11, r0			; 25 - r0 freed
		AND r11, r11, r1			; 26
		AND r6, r6, r3				; 27
		AND r6, r6, r9				; 28 - r9 freed
		ORR r6, r6, r11				; 29
		ORR r6, r6, r12				; 30
		
		STR r6, [r2]
		STR r1, [r2, #4]
		STR r10, [r2, #8]		
		
		POP {r4-r12}
		bx lr
	
	
F5_sqr	LDR r2, [r0]		; Loads a0 into r2
		LDR r3, [r0, #4]	; Loads a1 into r3
		LDR r0, [r0, #8]	; Loads a2 into r0

		STR r3, [r1, #8]		; c2 = a1
		
		EOR r3, r3, #0xffffffff	; r3 = ~a1
		AND r3, r2, r3			; r3 = a0 & ~a1
		ORR r3, r3, r0			; r3 = a2 | (a0 & ~a1)
		EOR r0, r0, r0			; r0 = 0
		
		STR r3, [r1]			; c0 = a2 | (a0 & ~a1)
		STR r0, [r1, #4]		; c1 = 0
		
		bx lr

		END