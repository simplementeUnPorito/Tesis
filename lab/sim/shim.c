/* shim.c - expone el lazo REAL del firmware a un programa de PC.
 *
 * La idea es no reescribir nada: `control_config.c` es aritmetica pura -solo
 * necesita stdint.h y string.h- asi que se compila tal cual para el host y se
 * lo maneja desde Python.  Reimplementar el PI en Python probaria mi
 * reimplementacion, que es justo lo que no sirve.
 *
 * Por la frontera solo cruzan tipos primitivos: nada de layouts de structs,
 * que es de donde salen los errores tontos entre lenguajes.
 */
#include "control_config.h"
#include <string.h>

static ControlConfig cfg;
static ControlPI pi;

void sim_defaults(void) { control_config_defaults(&cfg); }
void sim_set(unsigned i, int32_t v) { if (i < CP_COUNT) cfg.value[i] = v; }
int32_t sim_get(unsigned i) { return i < CP_COUNT ? cfg.value[i] : 0; }
unsigned sim_count(void) { return CP_COUNT; }

void sim_pi_reset(int16_t fine, int16_t coarse)
{
    memset(&pi, 0, sizeof pi);
    pi.fine = fine;
    pi.coarse = coarse;
}
void sim_force(uint32_t now, uint32_t ms) { control_pi_force(&pi, now, ms); }
void sim_step(uint32_t now, int32_t lp, int lpv, int32_t sum, int sumv)
{
    control_pi_step(&pi, &cfg, now, lp, lpv, sum, sumv);
}

int16_t sim_fine(void)    { return pi.fine; }
int16_t sim_coarse(void)  { return pi.coarse; }
int     sim_holding(void) { return pi.holding; }
int32_t sim_slope(void)   { return pi.slope_uv; }
int     sim_armed(void)   { return pi.slope_armed; }
int16_t sim_rescue_step(void) { return pi.rescue_step; }
int     sim_bracket(void) { return pi.rescue_bracket; }
int     sim_settled(uint32_t now) { return control_pi_settled(&pi, &cfg, now); }
int     sim_valid(int32_t uv) { return control_measurement_valid(&cfg, uv); }
