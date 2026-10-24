/* Prueba el codec real del firmware y la compatibilidad con su encoder viejo.
 * Cada registro binario contiene 30 int32_t seguidos por 30 uint8_t. */
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#if defined(__i386__) || defined(__x86_64__)
#include <x86intrin.h>
#endif
#include "../../src/firmware/esp32/Nodo comunicación/slave/src/geo_codec.h"

typedef struct {
    uint8_t *buf;
    size_t pos;
    uint8_t acc;
    uint8_t nbits;
} old_bw_t;

static void old_putbit(old_bw_t *w, unsigned bit)
{
    w->acc = (uint8_t)((w->acc << 1) | (bit & 1u));
    if (++w->nbits == 8u) {
        w->buf[w->pos++] = w->acc;
        w->acc = 0;
        w->nbits = 0;
    }
}

static void old_flush(old_bw_t *w)
{
    if (w->nbits) w->buf[w->pos++] = (uint8_t)(w->acc << (8u - w->nbits));
    w->acc = 0;
    w->nbits = 0;
}

static uint32_t old_zigzag(int32_t value)
{
    return value >= 0 ? (uint32_t)value << 1
                      : ((uint32_t)(-(value + 1)) << 1) | 1u;
}

/* Copia aislada del encoder anterior: D1, cabecera antigua y Rice 1...0. */
static size_t old_encode(const int32_t *x, const uint8_t *flags, uint8_t *out)
{
    uint32_t u[GEOZ_SAMPLES - 1];
    uint64_t best_bits = UINT64_MAX;
    unsigned best_k = 0;
    unsigned i, k;
    int has_flags = 0;
    size_t pos;

    for (i = 0; i < GEOZ_SAMPLES; ++i) if (flags[i]) has_flags = 1;
    for (i = 1; i < GEOZ_SAMPLES; ++i) {
        const int32_t a = geoz_sext24((uint32_t)x[i] & 0xFFFFFFu);
        const int32_t b = geoz_sext24((uint32_t)x[i - 1u] & 0xFFFFFFu);
        u[i - 1u] = old_zigzag(a - b);
    }
    for (k = 0; k < 24u; ++k) {
        uint64_t bits = 0;
        for (i = 0; i < GEOZ_SAMPLES - 1u; ++i) bits += (u[i] >> k) + 1u + k;
        if (bits < best_bits) { best_bits = bits; best_k = k; }
    }
    if (5u + (size_t)((best_bits + 7u) / 8u) < 91u) {
        old_bw_t writer;
        const uint32_t x0 = (uint32_t)x[0] & 0xFFFFFFu;
        out[0] = (uint8_t)(1u | (has_flags ? GEOZ_HAS_FLAGS : 0u));
        out[1] = (uint8_t)x0;
        out[2] = (uint8_t)(x0 >> 8);
        out[3] = (uint8_t)(x0 >> 16);
        out[4] = (uint8_t)best_k;
        writer.buf = out;
        writer.pos = 5u;
        writer.acc = 0;
        writer.nbits = 0;
        for (i = 0; i < GEOZ_SAMPLES - 1u; ++i) {
            uint32_t q = u[i] >> best_k;
            unsigned shift;
            while (q--) old_putbit(&writer, 1u);
            old_putbit(&writer, 0u);
            for (shift = best_k; shift != 0u; --shift)
                old_putbit(&writer, (u[i] >> (shift - 1u)) & 1u);
        }
        old_flush(&writer);
        pos = writer.pos;
    } else {
        out[0] = (uint8_t)(GEOZ_ESCAPE | (has_flags ? GEOZ_HAS_FLAGS : 0u));
        pos = 1u;
        for (i = 0; i < GEOZ_SAMPLES; ++i, pos += 3u) geoz_put_s24(out + pos, x[i]);
    }
    if (has_flags) {
        unsigned at = 0;
        while (at < GEOZ_SAMPLES) {
            unsigned run = 1;
            while (at + run < GEOZ_SAMPLES && flags[at + run] == flags[at]) ++run;
            out[pos++] = flags[at];
            out[pos++] = (uint8_t)run;
            at += run;
        }
    }
    return pos;
}

static uint64_t cycle_now(void)
{
#if defined(__i386__) || defined(__x86_64__)
    _mm_lfence();
    return __rdtsc();
#else
    return 0;
#endif
}

static int test_file(const char *path)
{
    FILE *file = fopen(path, "rb");
    int32_t x[GEOZ_SAMPLES], y[GEOZ_SAMPLES];
    uint8_t flags[GEOZ_SAMPLES], decoded_flags[GEOZ_SAMPLES];
    uint8_t packet[GEOZ_MAX_BYTES], old_packet[GEOZ_MAX_BYTES];
    uint64_t cycles = 0;
    unsigned long batches = 0, new_bad = 0, old_bad = 0, total = 0, maximum = 0;

    if (!file) { perror(path); return 1; }
    for (;;) {
        size_t got = fread(x, sizeof(x[0]), GEOZ_SAMPLES, file);
        size_t size, old_size;
        uint64_t start, end;
        if (got == 0u) break;
        if (got != GEOZ_SAMPLES ||
            fread(flags, sizeof(flags[0]), GEOZ_SAMPLES, file) != GEOZ_SAMPLES) {
            fprintf(stderr, "%s: registro truncado\n", path);
            fclose(file);
            return 1;
        }
        start = cycle_now();
        size = geoz_encode(x, flags, packet);
        end = cycle_now();
        cycles += end - start;
        if (!size || size > GEOZ_MAX_BYTES ||
            !geoz_decode(packet, size, y, decoded_flags) ||
            memcmp(x, y, sizeof(x)) || memcmp(flags, decoded_flags, sizeof(flags)) ||
            !geoz_decode(packet, size, y, NULL) || memcmp(x, y, sizeof(x)))
            ++new_bad;
        old_size = old_encode(x, flags, old_packet);
        if (!geoz_decode(old_packet, old_size, y, decoded_flags) ||
            memcmp(x, y, sizeof(x)) || memcmp(flags, decoded_flags, sizeof(flags)) ||
            !geoz_decode(old_packet, old_size, y, NULL) || memcmp(x, y, sizeof(x)))
            ++old_bad;
        total += (unsigned long)size;
        if (size > maximum) maximum = (unsigned long)size;
        ++batches;
    }
    if (ferror(file)) { perror(path); fclose(file); return 1; }
    fclose(file);
    printf("%s: lotes %lu, v2 malos %lu, antiguos malos %lu, media %.4f B, "
           "max %lu B, codificacion ~%.0f ciclos/lote\n",
           path, batches, new_bad, old_bad,
           batches ? (double)total / (double)batches : 0.0, maximum,
           batches ? (double)cycles / (double)batches : 0.0);
    return (new_bad || old_bad || !batches) ? 1 : 0;
}

int main(int argc, char **argv)
{
    int result = 0;
    int i;
    if (argc < 2) {
        fprintf(stderr, "uso: %s archivo.bin [archivo.bin ...]\n", argv[0]);
        return 2;
    }
    for (i = 1; i < argc; ++i) result |= test_file(argv[i]);
    return result;
}
