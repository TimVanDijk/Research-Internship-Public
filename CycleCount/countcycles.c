#include "stm32wrapper.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>

#define NUM_TESTS 25
#define FIELD 3
#define NUM_BITS (int) ceil(log(FIELD) / log(2))
#define REG_SIZE 32
#define BUF_SIZE 64

// Import assembly implementations
extern void F3_add(unsigned int* a, unsigned int* b, unsigned int* c);
extern void F3_mult(unsigned int* a, unsigned int* b, unsigned int* c);
extern void F3_sqr(unsigned int* a, unsigned int* c);

extern void F5_add(unsigned int* a, unsigned int* b, unsigned int* c);
extern void F5_mult(unsigned int* a, unsigned int* b, unsigned int* c);
extern void F5_sqr(unsigned int* a, unsigned int* c);

extern void F7_add(unsigned int* a, unsigned int* b, unsigned int* c);
extern void F7_mult(unsigned int* a, unsigned int* b, unsigned int* c);
extern void F7_sqr(unsigned int* a, unsigned int* c);

int main(void) {
    clock_setup();
    gpio_setup();
    usart_setup(115200);
    flash_setup();

    char buffer[BUF_SIZE];

    unsigned int inputA[NUM_BITS];
    unsigned int inputB[NUM_BITS];
    unsigned int solAdd[NUM_BITS];
    unsigned int solMult[NUM_BITS];
    unsigned int solSqr[NUM_BITS];
    unsigned int output[NUM_BITS];

    // Select addition and multiplication operations for current field
    void (*add)(unsigned int* a, unsigned int* b, unsigned int* c);
    void (*mult)(unsigned int* a, unsigned int* b, unsigned int* c);
    void (*sqr)(unsigned int* a, unsigned int* c);
    switch(FIELD) {
        case 3: add = F3_add; mult = F3_mult; sqr = F3_sqr; break;
        case 5: add = F5_add; mult = F5_mult; sqr = F5_sqr; break;
        case 7: add = F7_add; mult = F7_mult; sqr = F7_sqr; break;
        default: snprintf(buffer, BUF_SIZE, "Error: no operations are implemented for F_%d", FIELD); send_USART_str(buffer); return -1;
    }

    // Seed the random function. Unfortunately, there is no clock we can use.
    srand(4);   // chosen by fair dice roll.
                // guaranteed to be random.
                // (https://xkcd.com/221)

    int i, j, n;
    unsigned int oldcount, newcount;
    for (n = 0; n < NUM_TESTS; ++n) {
        // Clear arrays
        for (j = 0; j < NUM_BITS; ++j) {
            inputA[j] = 0; inputB[j] = 0;
            solAdd[j] = 0; solMult[j] = 0; solSqr[j] = 0;
            output[j] = 0;
        }
        
        // Pseudo-randomly generate two bitsliced input values
        for (i = 0; i < REG_SIZE; ++i) {
            unsigned int valueA = rand() % FIELD;
            for (j = 0; j < NUM_BITS; ++j)
                inputA[j] += ((valueA >> j) & 0b1) << i;
        }
        
        for (i = 0; i < REG_SIZE; ++i) {
            unsigned int valueB = rand() % FIELD;
            for (j = 0; j < NUM_BITS; ++j)
                inputB[j] += ((valueB >> j) & 0b1) << i;
        }
        
        // Compute corresponding solutions
        for (i = 0; i < REG_SIZE; ++i) {
            unsigned int valueA = 0;
            unsigned int valueB = 0;
            for (j = 0; j < NUM_BITS; ++j) {
                valueA += ((inputA[j] >> i) & 0b1) << j;
                valueB += ((inputB[j] >> i) & 0b1) << j;    
            }
        
            for (j = 0; j < NUM_BITS; ++j) {
                solAdd[j] += ((((valueA + valueB) % FIELD) >> j) & 0b1) << i;
                solMult[j] += ((((valueA * valueB) % FIELD) >> j) & 0b1) << i;
                solSqr[j] += ((((valueA * valueA) % FIELD) >> j) & 0b1) << i;
            }
        }      

        // Apply assembly functions to the inputs and compare results to solutions
        oldcount = DWT_CYCCNT;
        add(inputA, inputB, output);
        newcount = DWT_CYCCNT;
        memcmp(output, solAdd, sizeof(output)) == 0 ? snprintf(buffer, BUF_SIZE, "Test #%d: addition OK. This took %d cycles.", n, newcount - oldcount) : snprintf(buffer, BUF_SIZE, "Test #%d: addition FAILED. This took %d cycles.", n, newcount - oldcount);
        send_USART_str(buffer);
        
        oldcount = DWT_CYCCNT;
        mult(inputA, inputB, output);
        newcount = DWT_CYCCNT;
        memcmp(output, solMult, sizeof(output)) == 0 ? snprintf(buffer, BUF_SIZE, "Test #%d: multiplication OK. This took %d cycles.", n, newcount - oldcount) : snprintf(buffer, BUF_SIZE, "Test #%d: multiplication FAILED. This took %d cycles.", n, newcount - oldcount);
        send_USART_str(buffer);
        
        oldcount = DWT_CYCCNT;
        sqr(inputA, output);
        newcount = DWT_CYCCNT;
        memcmp(output, solSqr, sizeof(output)) == 0 ? snprintf(buffer, BUF_SIZE, "Test #%d: squaring OK. This took %d cycles.", n, newcount - oldcount) : snprintf(buffer, BUF_SIZE, "Test #%d: squaring FAILED. This took %d cycles.", n, newcount - oldcount);
        send_USART_str(buffer);

    }

    while(1);
    return 0;
}




