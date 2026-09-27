/* Host-only translation unit: compiles the unedited runtime through stubs. */
#include "project.h"
#include <string.h>
static uint8 ee[2048], dac[4]; static uint16 pgaout=16000;
const int g_fir_calibration_coeffs_q23[1]={0};
uint8 EEPROM_ReadByte(uint16 a){return a<sizeof ee?ee[a]:0;}
uint8 EEPROM_Write(const uint8 *p,uint8 row){memcpy(ee+(uint16)row*16,p,16);return CYRET_SUCCESS;}
void EEPROM_UpdateTemperature(void){} uint8 CyEnterCriticalSection(void){return 0;} void CyExitCriticalSection(uint8 x){(void)x;}
void CySysTickStart(void){} void CySysTickSetCallback(uint8 x,void(*f)(void)){(void)x;(void)f;} void ADC_StopConvert(void){} void ADC_StartConvert(void){}
void psoc_amux_select_exclusive(uint8 a,uint8 b){(void)a;(void)b;} void psoc_adc_select_calibration_config(void){} void psoc_adc_cal_override(uint8 x){(void)x;}
uint8 psoc_calibration_set_stage_dac(uint8 s,int16 c){if(s<4)dac[s]=(uint8)c;return s<4;} void psoc_hw_set_pga(uint8 x){(void)x;} void psoc_hw_set_pgaout(uint8 x){pgaout=(uint16)x*1000;}
uint16 psoc_hw_pgaout_gain_x1000(void){return pgaout;} uint8 psoc_filter_load_fir_coefficients(const int*x,uint8 n){(void)x;(void)n;return 1;} void dma_route_select(uint8 x){(void)x;} void psoc_link_put_array(const uint8*x,uint8 n){(void)x;(void)n;}
#include "control_runtime.inc"
/* Primitive host adapter; a sample is injected through the original scanner. */
void host_reset(void){memset(ee,0,sizeof ee);memset(dac,0,sizeof dac);control_init();}
void host_tick_sample(int32 uv){control_tick();control_on_filtered_sample(uv);control_service();}
int16 host_code(unsigned i){return i<4?ctl_codes[i]:0;}
unsigned host_state(void){return ctl_state;}
