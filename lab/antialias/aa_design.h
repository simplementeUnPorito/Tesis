#ifndef AA_DESIGN_H
#define AA_DESIGN_H

/* Portable host model of the PSoC anti-alias FIR decimator. */

#include <stdint.h>

#define AA_FS_HZ             2000.0
#define AA_ATTEN_DB          90.0
#define AA_PASS_EDGE_RATIO   0.8
#define AA_STOP_EDGE_RATIO   1.2
#define AA_MAX_DECIMATION    16
#define AA_MAX_TAPS          511
#define AA_Q23_SCALE         8388608LL

typedef int32_t aa_q23_t;

typedef struct aa_decimator_tag {
    int factor;
    int ntaps;
    int phase;
    int write_index;
    int primed;
    aa_q23_t coeff[AA_MAX_TAPS];
    int32_t state[AA_MAX_TAPS];
} aa_decimator_t;

/* Designs a symmetric Type-I Kaiser-windowed sinc low-pass.
 * Pass edge = 0.8 new Nyquist, stop edge = 1.2 new Nyquist.
 * The ideal-sinc midpoint is therefore the new Nyquist. Coefficients are
 * Q1.23, symmetric, and adjusted so their integer sum is exactly 2^23.
 * Returns 1 on success, 0 for an unsupported factor or size. */
int aa_design_q23(int factor, aa_q23_t *coeff, int capacity, int *ntaps_out);

/* Initializes filter and clears state. Returns 1 on success. */
int aa_decimator_init(aa_decimator_t *decimator, int factor);

/* Pushes one signed 24-bit input. It emits samples 0, N, 2N, ... and uses
 * a signed 64-bit accumulator, matching aa_decim.h on the PSoC. */
int aa_decimator_push(aa_decimator_t *decimator, int32_t input,
                      int32_t *output);

#endif
