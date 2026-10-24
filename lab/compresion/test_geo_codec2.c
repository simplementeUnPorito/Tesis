#include <stdio.h>
#include <string.h>
#include "geo_codec2_propuesto.h"

int main(int argc, char **argv)
{
    FILE *file;
    int32_t x[30], y[30];
    uint8_t flags[30], decoded_flags[30], packet[GEOZ2_MAX_BYTES];
    unsigned long batches = 0, mismatches = 0, total = 0, maximum = 0;
    if (argc != 2 || !(file = fopen(argv[1], "rb"))) return 2;
    while (fread(x, sizeof(x[0]), 30, file) == 30 &&
           fread(flags, sizeof(flags[0]), 30, file) == 30) {
        size_t size = geoz2_encode(x, flags, packet);
        if (!size || !geoz2_decode(packet, size, y, decoded_flags) ||
            memcmp(x, y, sizeof(x)) || memcmp(flags, decoded_flags, sizeof(flags)))
            ++mismatches;
        total += (unsigned long)size;
        if (size > maximum) maximum = (unsigned long)size;
        ++batches;
    }
    fclose(file);
    printf("lotes %lu malos %lu media %.4f B max %lu B\n", batches, mismatches,
           batches ? (double)total / batches : 0.0, maximum);
    return mismatches ? 1 : 0;
}
