		AREA globalvars, DATA, READWRITE
extra_storage dcd 0,  0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0; 1 + 6 + 8 words of storage
		
		AREA Program, CODE, READONLY
		ENTRY
		EXPORT F7_add
		EXPORT F7_mult
		EXPORT F7_sqr
			
F7_add	PUSH {r4-r12, lr}
		; This time, we cannot afford to keep all input in memory
		; We keep the pointer to a and b in r0 and r1
		; We keep a pointer to extra memory in r14
		; The pointer to the output array is in the first word of the extra memory
		; Whenever possible, we use r2 to temporarily load addresses in
		
		LDR r14, =extra_storage
		STR r2, [r14]				; Store output pointer in the first word of extra storage
		
		LDR r3, [r0]				; Load a0
		LDR r4, [r1]				; Load b0
		LDR r6, [r1, #4]			; Load b1
		
		STR r3, [r14, #4]			; Store a0 to extra_storage[1]
		STR r4, [r14, #16]			; Store b0 to extra_storage[4]
		STR r6, [r14, #20]			; Store b1 to extra_storage[5]
		
		AND r5, r3, r4				; 1		
		EOR r7, r6, #0xffffffff		; 2
		ORR r8, r3, r4				; 3
		EOR r9, r4, #0xffffffff		; 4
		
		LDR r3, [r0, #4]			; Load a1
		LDR r10, [r0, #8]			; Load a2
		LDR r2, [r1, #8]			; Load b2
		
		EOR r11, r10, #0xffffffff	; 5
		
		STR r7, [r14, #28]			; Store 2 in storage[7]
		STR r3, [r14, #8]			; Store a1 to extra_storage[2]
		STR r10, [r14, #12]			; Store a2 to extra_storage[3]
		STR r2, [r14, #24]			; Store b2 to extra_storage[6]
		STR r9, [r14, #32]			; Store 4 in storage[8]
		
		; We no longer need the pointers to a and b: r0 and r1 are freed
		
		ORR r7, r7, r11				; 6
		EOR r12, r3, #0xffffffff	; 7
		EOR r4, r2, #0xffffffff		; 8
		ORR r0, r4, r12				; 9
		AND r1, r0, r7				; 10
		ORR r2, r4, r11				; 11
		AND r1, r1, r2				; 12
		ORR r1, r1, r9				; 13
		EOR r1, r1, #0xffffffff		; 13
		
		ORR r9, r3, r6				; 14
		
		STR r9, [r14, #36]			; Store 14 to extra_storage[9]
		STR r4, [r14, #40]			; Store 8 to extra_storage[10]
		STR r7, [r14, #44]			; Store 6 to extra_storage[11]
		STR r2, [r14, #48]			; Store 11 to extra_storage[12]
		STR r11, [r14, #52]			; Store 5 to extra_storage[13]
		
		ORR r9, r9, r10				; 15
		EOR r9, r9, #0xffffffff		; 15
		AND r4, r4, r7				; 16
		ORR r4, r4, r9				; 17
		EOR r4, r4, #0xffffffff		; 17
		
		LDR r3, [r14, #16]			; Loads b0
		LDR r10, [r14, #4]			; Loads a0
		
		ORR r4, r4, r3				; 18
		EOR r4, r4, #0xffffffff		; 18
		ORR r1, r1, r4				; 19
		AND r1, r1, r10				; 20
		ORR r12, r12, r3			; 21
		ORR r12, r12, r7			; 22
		EOR r12, r12, #0xffffffff	; 22
		ORR r12, r12, r1			; 23
		
		LDR r7, [r14, #28]			; Loads 2
		LDR r10, [r14, #36]			; Loads 14
		LDR r2, [r14, #16]			; Loads b0
		LDR r6, [r14, #24]			; Loads b2
		LDR r3, [r14, #48]			; Loads 11
		
		ORR r3, r3, r2				; 24
		EOR r3, r3, #0xffffffff		; 24
		ORR r10, r10, r6			; 25
		EOR r10, r10, #0xffffffff	; 25
		AND r11, r11, r0			; 26
		ORR r11, r11, r10			; 27
		AND r11, r11, r2			; 28
		ORR r3, r3, r11				; 29
		EOR r3, r3, #0xffffffff		; 29
		
		LDR r6, [r14, #4]			; Loads a0
		
		ORR r0, r0, r7				; 30
		AND r0, r0, r3				; 31
		ORR r0, r0, r6				; 32
		EOR r0, r0, #0xffffffff		; 32
		ORR r0, r0, r12				; 33 - c0

		LDR r3, [r14]				; Load address to output
		LDR r11, [r14, #12]			; Loads a2
		STR r0, [r3]				; Store c0 in output
		
		EOR r0, r0, #0xffffffff		; 34
		ORR r4, r0, r11				; 35
		AND r12, r4, r8				; 36
		ORR r12, r12, r7			; 37
		EOR r12, r12, #0xffffffff	; 37
		EOR r6, r6, #0xffffffff		; 38
		
		LDR r9, [r14, #20]			; Loads b1
		LDR r3, [r14, #32]			; Loads 4
		
		ORR r9, r9, r6				; 39
		EOR r9, r9, #0xffffffff		; 39
		AND r9, r9, r0				; 40
		ORR r9, r9, r12				; 41
		EOR r9, r9, #0xffffffff		; 41
		
		LDR r12, [r14, #48]			; Loads 11
		
		ORR r3, r3, r12				; 42
		AND r3, r3, r9				; 43
		
		LDR r1, [r14, #16]			; Loads b0
		LDR r12, [r14, #8]			; Loads a1
		LDR r11, [r14, #20]			; Loads b1
		LDR r9, [r14, #24]			; Loads b2
		
		ORR r3, r3, r12				; 44
		EOR r3, r3, #0xffffffff		; 44
		ORR r0, r0, r9				; 45
		AND r0, r0, r8				; 46
		ORR r0, r0, r11				; 47
		EOR r0, r0, #0xffffffff		; 47
		AND r1, r1, r11				; 48
		AND r4, r4, r1				; 49
		ORR r4, r4, r0				; 50
		
		LDR r0, [r14, #40]			; Loads 8
		LDR r8, [r14, #48]			; Loads 11
		
		ORR r7, r7, r0				; 51
		AND r7, r7, r8				; 52
		ORR r7, r7, r6				; 53
		EOR r7, r7, #0xffffffff		; 53
		ORR r4, r4, r7				; 54
		AND r4, r4, r12				; 55
		ORR r4, r4, r3				; 56
		
		LDR r7, [r14]				; Load address to output
		STR r4, [r7, #4]			; Store c1 in output
		
		EOR r4, r4, #0xffffffff		; 57
		
		LDR r11, [r14, #52]			; Loads 5
		
		AND r7, r11, r4				; 58 
		ORR r7, r7, r5				; 59
		AND r7, r7, r12				; 60
		ORR r12, r4, r2				; 61
		
		LDR r5, [r14, #36]			; Loads 14
		
		AND r2, r12, r5				; 62
		ORR r2, r2, r11				; 63
		EOR r2, r2, #0xffffffff		; 63
		ORR r7, r7, r2				; 64
		EOR r7, r7, #0xffffffff		; 64
		ORR r7, r7, r9				; 65
		EOR r7, r7, #0xffffffff		; 65
									; We need a0 = ~38
		EOR r0, r6, #0xffffffff		; Compute a0 from 38
		AND r2, r0, r11				; 66
		AND r2, r2, r1				; 67
		ORR r2, r2, r7				; 68
		ORR r0, r0, r4				; 69
		AND r0, r0, r5				; 70
		
		LDR r11, [r14, #8]			; Loads a1
		LDR r8, [r14, #12]			; Loads a2
		LDR r5, [r14, #44]			; Loads 6
		
		ORR r0, r0, r8				; 71
		EOR r0, r0, #0xffffffff		; 71
		AND r8, r8, r11				; 72
		AND r8, r8, r12				; 73
		ORR r0, r0, r8				; 74
		ORR r6, r6, r5				; 75
		EOR r6, r6, #0xffffffff		; 75
		ORR r6, r6, r0				; 76
		AND r6, r6, r9				; 77
		ORR r6, r6, r2				; 78
		
		LDR r7, [r14]				; Load address to output
		STR r6, [r7, #8]			; Store c2 in output
				
		POP {r4-r12, lr}
		bx lr

F7_mult	PUSH {r4-r12, lr}	
		LDR r3, [r0]				; Loads a0 into r3
		LDR r4, [r0, #4]			; Loads a1 into r4
		LDR r5, [r0, #8]			; Loads a2 into r5
		LDR r6, [r1]				; Loads b0 into r6
		LDR r7, [r1, #4]			; Loads b1 into r7
		LDR r8, [r1, #8]			; Loads b2 into r8
		
		AND r9, r3, r8				; 1
		ORR r10, r5, r6				; 2
		EOR r10, r10, #0xffffffff	; 2
		ORR r11, r4, r7				; 3
		EOR r11, r11, #0xffffffff	; 3
		ORR r10, r10, r11			; 4 - r11 freed
		AND r9, r9, r10				; 5 - r10 freed
		ORR r10, r3, r8				; 6
		EOR r10, r10, #0xffffffff	; 6
		AND r11, r5, r6				; 7
		AND r12, r4, r7				; 8
		ORR r11, r11, r12			; 9 - r12 freed
		AND r10, r10, r11			; 10 - r11 freed
		ORR r9, r9, r10				; 11 - r10 freed
		EOR r10, r4, #0xffffffff	; 12
		AND r10, r10, r5			; 13
		PUSH {r10}					; Store 13 on stack
		EOR r11, r7, #0xffffffff	; 14
		AND r11, r11, r6			; 15 - We also need 14 for 55, but we will just recompute it later
		AND r10, r10, r11			; 16 - r11 freed
		EOR r11, r5, #0xffffffff	; 17
		AND r11, r11, r4			; 18
		EOR r12, r6, #0xffffffff	; 19
		AND r14, r12, r7			; 20
		AND r14, r14, r11			; 21
		ORR r14, r14, r10			; 22 - r10 freed
		ORR r14, r14, r9			; 23 - r9 freed
		
		STR r14, [r2, #8]			; Stores c2 - r14 freed
									; r12 is still taken
		
		EOR r9, r8, #0xffffffff		; 24
		AND r9, r9, r6				; 25 - We also need 24 for 53, but we will just recompute it later
		AND r9, r9, r11				; 26 - We also need 18 for 56, but we will just recompute it later - r11 freed
		AND r12, r12, r8			; 27
		LDR r10, [sp]				; Restore 13 from stack, but keep it there as well
		AND r12, r12, r10			; 28 - r10 freed
		ORR r12, r12, r9			; 29
		AND r10, r3, r7				; 30
		ORR r11, r6, r8				; 31
		EOR r11, r11, #0xffffffff	; 31
		ORR r14, r4, r5				; 32
		EOR r14, r14, #0xffffffff	; 32
		ORR r11, r11, r14			; 33 - r14 freed
		AND r10, r10, r11			; 34 - r11 freed
		ORR r11, r3, r7				; 35
		EOR r11, r11, #0xffffffff	; 35
		AND r14, r5, r8				; 36
		AND r9, r4, r6				; 37
		ORR r9, r9, r14				; 38 - r14 freed
		AND r9, r9, r11				; 39 - r11 freed
		ORR r9, r9, r10				; 40 - r10 freed
		ORR r12, r12, r9			; 41 - r9 freed
		
		STR r12, [r2, #4]			; Stores c1 - r10 freed
		
		AND r9, r3, r6				; 42
		ORR r10, r5, r7				; 43
		EOR r10, r10, #0xffffffff	; 43
		ORR r11, r4, r8				; 44
		EOR r11, r11, #0xffffffff	; 44
		ORR r10, r10, r11			; 45 - r11 freed
		AND r9, r9, r10				; 46 - r10 freed
		ORR r10, r3, r6				; 47
		EOR r10, r10, #0xffffffff	; 47
		AND r11, r7, r5				; 48
		AND r12, r4, r8				; 49
		ORR r11, r11, r12			; 50 - r12 freed
		AND r10, r10, r11			; 51 - r11 freed
		ORR r9, r9, r10				; 52 - r10 freed
		EOR r10, r8, #0xffffffff	; Recompute 24
		AND r10, r10, r7			; 53
		POP {r11}					; Restore 13 from the stack
		AND r10, r10, r11			; 54 - r11 freed
		EOR r11, r7, #0xffffffff	; Recompute 14
		AND r11, r11, r8			; 55
		EOR r12, r5, #0xffffffff 	; Recompute 17
		AND r12, r12, r4			; Recompute 18
		AND r11, r11, r12			; 56 - r12 freed
		ORR r10, r10, r11			; 57 - r11 freed
		ORR r9, r9, r10				; 58 - c0
		
		STR r9, [r2]				; Stores c0
		
		POP {r4-r12, lr}
		bx lr
			
F7_sqr	PUSH {r4-r7}
		LDR r2, [r0]			; Loads a0 into r2
		LDR r3, [r0, #4]		; Loads a1 into r3
		LDR r4, [r0, #8]		; Loads a2 into r4
		
		AND r0, r2, r4			; 1
		EOR r5, r3, #0xffffffff	; 2
		ORR r5, r5, r4			; 3
		ORR r5, r5, r2			; 4
		EOR r5, r5, #0xffffffff ; 4
		ORR r5, r5, r0			; 5 - c2		
		AND r6, r2, r3			; 6
		EOR r7, r4, #0xffffffff	; 7
		ORR r7, r7, r3			; 8
		ORR r7, r7, r2			; 9
		EOR r7, r7, #0xffffffff	; 9
		ORR r6, r6, r7			; 10 - c1 - r7 freed
		AND r7, r3, r4			; 11
		ORR r3, r3, r4			; 12 - r4 freed
		EOR r3, r3, #0xffffffff	; 12
		AND r3, r3, r2			; 13
		ORR r7, r7, r3			; 14 - c0
		
		STR r7, [r1]			; Store c0
		STR r6, [r1, #4]		; Store c1
		STR r5, [r1, #8]		; Store c2

		POP {r4-r7}

		bx lr
			
		END