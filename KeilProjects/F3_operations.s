		AREA Program, CODE, READONLY
		ENTRY
		EXPORT F3_add
		EXPORT F3_mult
		EXPORT F3_sqr
			
; c0 = (a1 & b1) | (a0 & ~b0 & ~b1) | (b0 & ~a0 & ~a1)
;	 = (a1 & b1) | (a0 & ~(b0 | b1)) | (b0 & ~(a0 | a1))

; c1 = (a0 & b0) | (a1 & ~b0 & ~b1) | (b1 & ~a0 & ~a1)
;	 = (a0 & b0) | (a1 & ~(b0 | b1)) | (b1 & ~(a0 | a1))
F3_add	PUSH {r4-r9}
		
		; We start by loading each bit into its own register
		LDR r3, [r0] 		; Loads a0 into r3
		LDR r4, [r0, #4] 	; Loads a1 into r4	
		LDR r5, [r1] 		; Loads b0 into r5
		LDR r6, [r1, #4] 	; Loads b1 into r6
		
		; Compute the common parts
		ORR r7, r5, r6			; b0 | b1
		EOR r7, r7, #0xFFFFFFFF	; ~(b0 | b1)
		
		ORR r8, r3, r4			; a0 | a1
		EOR r8, r8, #0xFFFFFFFF	; ~(a0 | a1)

		; Compute c0 and c1
		AND r9, r3, r7			; r9 = a0 & ~(b0 | b1)
		AND r3, r3, r5			; r3 = a0 & b0
		AND r5, r5, r8			; r5 = b0 & ~(a0 | a1)
		ORR r9, r9, r5			; r9 = (a0 & ~(b0 | b1)) | (b0 & ~(a0 | a1))
		AND r7, r4, r7			; r7 = a1 & ~(b0 | b1)
		ORR r3, r3, r7			; r3 = (a0 & b0) | (a1 & ~(b0 | b1))
		AND r8, r6, r8			; r6 = b1 & ~(a0 | a1)
		ORR r3, r3, r8			; r3 = (a0 & b0) | (a1 & ~(b0 | b1)) | ( b1 & ~(a0 | a1)))
		AND r4, r4, r6			; r4 = a1 & b1
		ORR r4, r4, r9			; r4 = (a1 & b1) | (a0 & ~(b0 | b1)) | (b0 & ~(a0 | a1))
		
		; Write result to memory
		STR r4, [r2]
		STR r3, [r2, #4]
		
		POP {r4-r9}
		bx lr
		
; c0 = (a0 & b0) | (a1 & b1)
; c1 = (a0 & b1) | (a1 & b0)
F3_mult PUSH {r4-r7}
		
		; We start by loading each bit into its own register
		LDR r3, [r0] 		; Loads a0 into r3
		LDR r4, [r0, #4] 	; Loads a1 into r4	
		LDR r5, [r1] 		; Loads b0 into r5
		LDR r6, [r1, #4] 	; Loads b1 into r6
		
		; Compute c0 and c1
		AND r7, r3, r5		; r7 = a0 & b0
		AND r3, r3, r6		; r3 = a0 & b1
		AND r6, r4, r6		; r6 = a1 & b1
		AND r5, r4, r5		; r5 = a1 & b0
		
		ORR r7, r7, r6		; (a0 & b0) | (a1 & b1)
		ORR r3, r3, r5		; (a0 & b1) | (a1 & b0)
		
		; Write result to memory
		STR r7, [r2]
		STR r3, [r2, #4]
		
		POP {r4-r7}
		bx lr
		
F3_sqr	LDR r2, [r0]		; Loads a0 into r3
		LDR r3, [r0, #4]	; Loads a1 into r4
		
		; Compute c0 and c1
		EOR r2, r2, r3		; r2 = a0 | a1
		EOR r0, r3, r3		; r3 = 0
		
		; Write result to memory
		STR r2, [r1]
		STR r0, [r1, #4]	
		
		bx lr

		END