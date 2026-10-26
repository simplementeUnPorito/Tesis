#include "aa_design.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define AA_PI 3.14159265358979323846

/* Deterministic I0 series; adequate for beta < 10 used here. */
static double aa_i0(double x)
{
    double term = 1.0;
    double sum = 1.0;
    double y = x * x * 0.25;
    int k = 1;
    do {
        term *= y / ((double)k * (double)k);
        sum += term;
        k++;
    } while (term > sum * 1.0e-16 && k < 100);
    return sum;
}

static long aa_round_long(double x)
{
    if (x >= 0.0) {
        return (long)floor(x + 0.5);
    }
    return (long)ceil(x - 0.5);
}

static int aa_tap_count(int factor)
{
    double width;
    double estimate;
    int taps;
    width = (AA_STOP_EDGE_RATIO - AA_PASS_EDGE_RATIO) / (double)factor;
    estimate = (AA_ATTEN_DB - 8.0) / (2.285 * AA_PI * width) + 1.0;
    taps = (int)ceil(estimate);
    if ((taps & 1) == 0) {
        taps++;
    }
    return taps;
}

int aa_design_q23(int factor, aa_q23_t *coeff, int capacity, int *ntaps_out)
{
    double work[AA_MAX_TAPS];
    double beta;
    double denom;
    double sum;
    double cutoff;
    int64_t qsum;
    int64_t residual;
    int taps;
    int middle;
    int i;

    if (coeff == (aa_q23_t *)0 || ntaps_out == (int *)0 || factor < 2 ||
        factor > AA_MAX_DECIMATION) {
        return 0;
    }
    taps = aa_tap_count(factor);
    if (taps > capacity || taps > AA_MAX_TAPS) {
        return 0;
    }

    beta = 0.1102 * (AA_ATTEN_DB - 8.7);
    denom = aa_i0(beta);
    cutoff = 1.0 / (double)factor; /* fraction of native Nyquist */
    middle = (taps - 1) / 2;
    sum = 0.0;
    for (i = 0; i < taps; i++) {
        double m = (double)(i - middle);
        double ideal;
        double ratio = (2.0 * (double)i) / (double)(taps - 1) - 1.0;
        double root = 1.0 - ratio * ratio;
        double window;
        if (m == 0.0) {
            ideal = cutoff;
        } else {
            ideal = sin(AA_PI * cutoff * m) / (AA_PI * m);
        }
        if (root < 0.0) {
            root = 0.0;
        }
        window = aa_i0(beta * sqrt(root)) / denom;
        work[i] = ideal * window;
        sum += work[i];
    }

    qsum = 0;
    for (i = 0; i < taps; i++) {
        int64_t q = (int64_t)aa_round_long((work[i] / sum) * (double)AA_Q23_SCALE);
        if (q < INT32_MIN || q > INT32_MAX) {
            return 0;
        }
        coeff[i] = (aa_q23_t)q;
        qsum += q;
    }
    residual = AA_Q23_SCALE - qsum;
    if ((int64_t)coeff[middle] + residual > INT32_MAX ||
        (int64_t)coeff[middle] + residual < INT32_MIN) {
        return 0;
    }
    coeff[middle] = (aa_q23_t)((int64_t)coeff[middle] + residual);
    *ntaps_out = taps;
    return 1;
}

int aa_decimator_init(aa_decimator_t *decimator, int factor)
{
    int taps;
    if (decimator == (aa_decimator_t *)0) {
        return 0;
    }
    memset(decimator, 0, sizeof(*decimator));
    if (!aa_design_q23(factor, decimator->coeff, AA_MAX_TAPS, &taps)) {
        return 0;
    }
    decimator->factor = factor;
    decimator->ntaps = taps;
    return 1;
}

int aa_decimator_push(aa_decimator_t *decimator, int32_t input,
                      int32_t *output)
{
    int64_t acc = 0;
    int64_t rounded;
    int newest;
    int phase;
    int tap;
    int index;

    if (decimator == (aa_decimator_t *)0 || output == (int32_t *)0) {
        return 0;
    }
    if (!decimator->primed) {
        for (tap = 0; tap < decimator->ntaps; tap++) {
            decimator->state[tap] = input;
        }
        decimator->primed = 1;
    }
    decimator->state[decimator->write_index] = input;
    decimator->write_index++;
    if (decimator->write_index == decimator->ntaps) {
        decimator->write_index = 0;
    }
    if (decimator->phase != 0) {
        decimator->phase++;
        if (decimator->phase == decimator->factor) {
            decimator->phase = 0;
        }
        return 0;
    }
    decimator->phase = 1;

    newest = decimator->write_index - 1;
    if (newest < 0) {
        newest = decimator->ntaps - 1;
    }
    /* Polyphase ordering: h[p + kN] for phase p. */
    for (phase = 0; phase < decimator->factor; phase++) {
        for (tap = phase; tap < decimator->ntaps; tap += decimator->factor) {
            index = newest - tap;
            while (index < 0) {
                index += decimator->ntaps;
            }
            acc += (int64_t)decimator->coeff[tap] *
                   (int64_t)decimator->state[index];
        }
    }
    if (acc >= 0) {
        rounded = (acc + (AA_Q23_SCALE / 2)) / AA_Q23_SCALE;
    } else {
        rounded = -((-acc + (AA_Q23_SCALE / 2)) / AA_Q23_SCALE);
    }
    if (rounded > INT32_MAX) {
        rounded = INT32_MAX;
    } else if (rounded < INT32_MIN) {
        rounded = INT32_MIN;
    }
    *output = (int32_t)rounded;
    return 1;
}

#ifdef AA_DESIGN_STANDALONE
int main(int argc, char **argv)
{
    aa_q23_t coeff[AA_MAX_TAPS];
    aa_decimator_t decimator;
    int32_t output;
    int taps;
    int factor;
    int i;
    if (argc != 2 && argc != 3) {
        return 2;
    }
    factor = atoi(argv[1]);
    if (argc == 3) {
        int count = atoi(argv[2]);
        if (!aa_decimator_init(&decimator, factor)) {
            return 3;
        }
        for (i = 0; i < count; i++) {
            if (aa_decimator_push(&decimator, 123456, &output)) {
                printf("%d %ld\n", i, (long)output);
            }
        }
        return 0;
    }
    if (!aa_design_q23(factor, coeff, AA_MAX_TAPS, &taps)) {
        return 3;
    }
    printf("%d\n", taps);
    for (i = 0; i < taps; i++) {
        printf("%d%c", (int)coeff[i], (i + 1 == taps) ? '\n' : ' ');
    }
    return 0;
}
#endif
