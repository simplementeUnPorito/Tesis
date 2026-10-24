#pragma once
/* Propuesta experimental: predictor FLAC fijo 0..3 + Rice exacto por lote.
 * API compatible con geo_codec.h; el bitstream no es compatible.
 * Formato: control, k, muestras warm-up signed-24, residuos Rice, flags RLE.
 * control: bits 0..1 orden, bit 2 escape crudo, bit 3 presencia de flags.
 */
#include <stddef.h>
#include <stdint.h>

#define GEOZ2_SAMPLES 30
#define GEOZ2_MAX_BYTES 160
#define GEOZ2_ORDER_MASK 0x03u
#define GEOZ2_ESCAPE 0x04u
#define GEOZ2_HAS_FLAGS 0x08u

typedef struct {
    uint8_t *buf;
    size_t cap, pos;
    uint8_t acc, nbits;
    int over;
} geoz2_bw_t;

static inline void geoz2_putbit(geoz2_bw_t *w, unsigned bit)
{
    if (w->over) return;
    w->acc = (uint8_t)((w->acc << 1) | (bit & 1u));
    if (++w->nbits == 8u) {
        if (w->pos >= w->cap) { w->over = 1; return; }
        w->buf[w->pos++] = w->acc;
        w->acc = w->nbits = 0;
    }
}

static inline void geoz2_flush(geoz2_bw_t *w)
{
    if (w->nbits && !w->over) {
        if (w->pos >= w->cap) { w->over = 1; return; }
        w->buf[w->pos++] = (uint8_t)(w->acc << (8u - w->nbits));
    }
    w->acc = w->nbits = 0;
}

static inline int32_t geoz2_sext24(uint32_t value)
{
    return (value & 0x800000u) ? (int32_t)(value | 0xFF000000u)
                               : (int32_t)(value & 0xFFFFFFu);
}

static inline void geoz2_put_s24(uint8_t *out, int32_t value)
{
    uint32_t u = (uint32_t)value & 0xFFFFFFu;
    out[0] = (uint8_t)u;
    out[1] = (uint8_t)(u >> 8);
    out[2] = (uint8_t)(u >> 16);
}

static inline int32_t geoz2_get_s24(const uint8_t *in)
{
    return geoz2_sext24((uint32_t)in[0] | (uint32_t)in[1] << 8 |
                        (uint32_t)in[2] << 16);
}

static inline int64_t geoz2_predict(const int32_t *x, unsigned i, unsigned order)
{
    switch (order) {
    case 0: return 0;
    case 1: return x[i - 1u];
    case 2: return 2LL * x[i - 1u] - x[i - 2u];
    default: return 3LL * x[i - 1u] - 3LL * x[i - 2u] + x[i - 3u];
    }
}

static inline uint64_t geoz2_zigzag(int64_t value)
{
    return value >= 0 ? (uint64_t)value << 1
                      : ((uint64_t)(-(value + 1)) << 1) | 1u;
}

static inline int64_t geoz2_unzigzag(uint64_t value)
{
    return (value & 1u) ? -(int64_t)(value >> 1) - 1 : (int64_t)(value >> 1);
}

static inline size_t geoz2_put_flags(const uint8_t *flags, uint8_t *out,
                                      size_t pos)
{
    unsigned at = 0;
    while (at < GEOZ2_SAMPLES) {
        unsigned run = 1;
        while (at + run < GEOZ2_SAMPLES && flags[at + run] == flags[at]) ++run;
        out[pos++] = flags[at];
        out[pos++] = (uint8_t)run;
        at += run;
    }
    return pos;
}

static inline size_t geoz2_encode(const int32_t *x, const uint8_t *flags,
                                   uint8_t *out)
{
    uint64_t best_u[GEOZ2_SAMPLES], trial_u[GEOZ2_SAMPLES];
    uint64_t best_bits = UINT64_MAX;
    unsigned best_order = 0, best_k = 0, order, k, i, best_count = 0;
    int has_flags = 0;
    size_t best_size = (size_t)-1, pos;

    if (!x || !out) return 0;
    for (i = 0; i < GEOZ2_SAMPLES; ++i) {
        if (x[i] < -8388608 || x[i] > 8388607) return 0;
        if (flags && flags[i]) has_flags = 1;
    }
    for (order = 0; order <= 3; ++order) {
        unsigned count = GEOZ2_SAMPLES - order;
        for (i = order; i < GEOZ2_SAMPLES; ++i)
            trial_u[i - order] = geoz2_zigzag((int64_t)x[i] - geoz2_predict(x, i, order));
        for (k = 0; k <= 31; ++k) {
            uint64_t bits = 0;
            size_t size;
            for (i = 0; i < count; ++i) bits += (trial_u[i] >> k) + 1u + k;
            size = 2u + 3u * order + (size_t)((bits + 7u) / 8u);
            if (size < best_size || (size == best_size && order < best_order) ||
                (size == best_size && order == best_order && k < best_k)) {
                best_size = size;
                best_bits = bits;
                best_order = order;
                best_k = k;
                best_count = count;
                for (i = 0; i < count; ++i) best_u[i] = trial_u[i];
            }
        }
    }
    if (best_size < 91u) {
        geoz2_bw_t writer;
        out[0] = (uint8_t)(best_order | (has_flags ? GEOZ2_HAS_FLAGS : 0u));
        out[1] = (uint8_t)best_k;
        pos = 2;
        for (i = 0; i < best_order; ++i, pos += 3) geoz2_put_s24(out + pos, x[i]);
        writer.buf = out;
        writer.cap = GEOZ2_MAX_BYTES;
        writer.pos = pos;
        writer.acc = writer.nbits = 0;
        writer.over = 0;
        for (i = 0; i < best_count; ++i) {
            uint64_t q = best_u[i] >> best_k;
            unsigned shift;
            while (q--) geoz2_putbit(&writer, 0);
            geoz2_putbit(&writer, 1);
            for (shift = best_k; shift != 0; --shift)
                geoz2_putbit(&writer, (unsigned)(best_u[i] >> (shift - 1u)) & 1u);
        }
        geoz2_flush(&writer);
        if (writer.over) return 0;
        pos = writer.pos;
        (void)best_bits;
    } else {
        out[0] = (uint8_t)(GEOZ2_ESCAPE | (has_flags ? GEOZ2_HAS_FLAGS : 0u));
        pos = 1;
        for (i = 0; i < GEOZ2_SAMPLES; ++i, pos += 3) geoz2_put_s24(out + pos, x[i]);
    }
    if (has_flags) pos = geoz2_put_flags(flags, out, pos);
    return pos;
}

typedef struct {
    const uint8_t *buf;
    size_t len, bit;
    int error;
} geoz2_br_t;

static inline unsigned geoz2_getbit(geoz2_br_t *r)
{
    unsigned value;
    if (r->bit >= r->len * 8u) { r->error = 1; return 0; }
    value = (r->buf[r->bit >> 3] >> (7u - (r->bit & 7u))) & 1u;
    ++r->bit;
    return value;
}

static inline int geoz2_decode(const uint8_t *in, size_t len, int32_t *x,
                               uint8_t *flags)
{
    unsigned order, k, i;
    size_t pos;
    if (!in || !x || len < 1) return 0;
    order = in[0] & GEOZ2_ORDER_MASK;
    if (in[0] & GEOZ2_ESCAPE) {
        if (len < 91u) return 0;
        for (i = 0; i < GEOZ2_SAMPLES; ++i) x[i] = geoz2_get_s24(in + 1u + 3u*i);
        pos = 91;
    } else {
        geoz2_br_t reader;
        if (len < 2u + 3u*order) return 0;
        k = in[1];
        if (k > 31) return 0;
        for (i = 0; i < order; ++i) x[i] = geoz2_get_s24(in + 2u + 3u*i);
        reader.buf = in + 2u + 3u*order;
        reader.len = len - 2u - 3u*order;
        reader.bit = 0;
        reader.error = 0;
        for (i = order; i < GEOZ2_SAMPLES; ++i) {
            uint64_t q = 0, remainder = 0, u;
            int64_t value;
            unsigned j;
            while (!geoz2_getbit(&reader) && !reader.error) {
                if (++q > (1u << 27)) { reader.error = 1; break; }
            }
            for (j = 0; j < k && !reader.error; ++j)
                remainder = (remainder << 1) | geoz2_getbit(&reader);
            if (reader.error) return 0;
            u = (q << k) | remainder;
            value = geoz2_predict(x, i, order) + geoz2_unzigzag(u);
            if (value < -8388608 || value > 8388607) return 0;
            x[i] = (int32_t)value;
        }
        pos = 2u + 3u*order + (reader.bit + 7u) / 8u;
    }
    if (flags) {
        for (i = 0; i < GEOZ2_SAMPLES; ++i) flags[i] = 0;
        if (in[0] & GEOZ2_HAS_FLAGS) {
            unsigned at = 0;
            while (at < GEOZ2_SAMPLES) {
                unsigned run, j;
                uint8_t value;
                if (pos + 2u > len) return 0;
                value = in[pos++];
                run = in[pos++];
                if (!run || at + run > GEOZ2_SAMPLES) return 0;
                for (j = 0; j < run; ++j) flags[at++] = value;
            }
        }
    }
    return pos == len;
}
