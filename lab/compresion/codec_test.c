/* Ida y vuelta del codec del firmware (geo_codec.h) sobre lotes de un archivo
 * binario: por lote, 30 int32 + 30 uint8. Imprime largo por lote o FALLA. */
#include <stdio.h>
#include <string.h>
#include "../../src/firmware/esp32/Nodo comunicación/slave/src/geo_codec.h"
int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 2;
    int32_t x[30], y[30];
    uint8_t fl[30], gl[30], buf[GEOZ_MAX_BYTES];
    unsigned long n = 0, bad = 0, total = 0, maxlen = 0;
    while (fread(x, 4, 30, f) == 30 && fread(fl, 1, 30, f) == 30) {
        size_t len = geoz_encode(x, fl, buf);
        if (len > maxlen) maxlen = len;
        total += len;
        if (!geoz_decode(buf, len, y, gl) || memcmp(x, y, sizeof x) || memcmp(fl, gl, sizeof fl)) bad++;
        n++;
    }
    printf("lotes %lu malos %lu media %.1f B max %lu B\n", n, bad, n ? (double)total / n : 0, maxlen);
    return bad ? 1 : 0;
}
