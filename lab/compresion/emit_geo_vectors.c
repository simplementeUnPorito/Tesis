/* Genera payloads con el encoder exacto del firmware para la prueba JS. */
#include <stdint.h>
#include <stdio.h>
#include "../../src/firmware/esp32/Nodo comunicación/master/src/geo_codec.h"

typedef struct { uint8_t *buf, acc, nbits; size_t pos; } old_bw_t;

static void old_bit(old_bw_t *w, unsigned bit)
{
    w->acc = (uint8_t)((w->acc << 1) | (bit & 1u));
    if (++w->nbits == 8u) { w->buf[w->pos++] = w->acc; w->acc = w->nbits = 0; }
}

static size_t old_encode(const int32_t *x, const uint8_t *flags, uint8_t *out)
{
    uint64_t best_bits = UINT64_MAX;
    uint32_t u[GEOZ_SAMPLES - 1];
    unsigned best_k = 0, i, k;
    int has_flags = 0;
    size_t pos;
    for (i = 0; i < GEOZ_SAMPLES; i++) if (flags[i]) has_flags = 1;
    for (i = 1; i < GEOZ_SAMPLES; i++) {
        const int32_t d = geoz_sext24((uint32_t)x[i] & 0xFFFFFFu) -
                          geoz_sext24((uint32_t)x[i - 1] & 0xFFFFFFu);
        u[i - 1] = d >= 0 ? (uint32_t)d << 1 : ((uint32_t)(-(d + 1)) << 1) | 1u;
    }
    for (k = 0; k < 24; k++) {
        uint64_t bits = 0;
        for (i = 0; i < GEOZ_SAMPLES - 1; i++) bits += (u[i] >> k) + 1u + k;
        if (bits < best_bits) { best_bits = bits; best_k = k; }
    }
    if (5u + (size_t)((best_bits + 7u) / 8u) < 91u) {
        old_bw_t w = { out, 0, 0, 5u };
        out[0] = (uint8_t)(1u | (has_flags ? GEOZ_HAS_FLAGS : 0u));
        geoz_put_s24(out + 1, x[0]);
        out[4] = (uint8_t)best_k;
        for (i = 0; i < GEOZ_SAMPLES - 1; i++) {
            uint32_t q = u[i] >> best_k;
            unsigned shift;
            while (q--) old_bit(&w, 1);
            old_bit(&w, 0);
            for (shift = best_k; shift; shift--) old_bit(&w, (u[i] >> (shift - 1u)) & 1u);
        }
        if (w.nbits) out[w.pos++] = (uint8_t)(w.acc << (8u - w.nbits));
        pos = w.pos;
    } else {
        out[0] = (uint8_t)(GEOZ_ESCAPE | (has_flags ? GEOZ_HAS_FLAGS : 0u));
        pos = 1;
        for (i = 0; i < GEOZ_SAMPLES; i++, pos += 3) geoz_put_s24(out + pos, x[i]);
    }
    return has_flags ? geoz_put_flags(flags, out, pos) : pos;
}

int main(int argc, char **argv)
{
    FILE *in, *out;
    int32_t values[GEOZ_SAMPLES];
    uint8_t flags[GEOZ_SAMPLES], payload[GEOZ_MAX_BYTES], old[GEOZ_MAX_BYTES];
    if (argc != 3 || !(in = fopen(argv[1], "rb"))) return 2;
    if (!(out = fopen(argv[2], "wb"))) { fclose(in); return 3; }
    for (;;) {
        const size_t got = fread(values, sizeof(values[0]), GEOZ_SAMPLES, in);
        size_t len, old_len;
        uint8_t len8;
        if (got == 0u) break;
        if (got != GEOZ_SAMPLES ||
            fread(flags, sizeof(flags[0]), GEOZ_SAMPLES, in) != GEOZ_SAMPLES) return 4;
        len = geoz_encode(values, flags, payload);
        old_len = old_encode(values, flags, old);
        if (len == 0u || len > 255u || old_len == 0u || old_len > 255u) return 5;
        len8 = (uint8_t)len;
        if (fwrite(&len8, 1, 1, out) != 1u || fwrite(payload, 1, len, out) != len) return 6;
        len8 = (uint8_t)old_len;
        if (fwrite(&len8, 1, 1, out) != 1u || fwrite(old, 1, old_len, out) != old_len) return 6;
    }
    if (ferror(in) || fclose(out) != 0) return 7;
    fclose(in);
    return 0;
}
