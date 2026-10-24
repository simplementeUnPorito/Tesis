/* Corre aa_decim.h tal cual: imprime coeficientes y la salida a un impulso
 * y a un escalon para cada N. */
#include <stdio.h>
#include <stdlib.h>
#include "../../../src/firmware/psoc/AcondicionamientoAnalogico.cydsn/aa_decim.h"
int main(int argc, char **argv)
{
    int n = atoi(argv[1]);
    uint16 i;
    aa_configure((uint16)n);
    printf("L %u\n", g_aa_len);
    for (i = 0; i < g_aa_len; i++) printf("%d\n", g_aa_coef[i]);
    return 0;
}
