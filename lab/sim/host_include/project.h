#ifndef HOST_PROJECT_H
#define HOST_PROJECT_H
#include <stdint.h>
#include <limits.h>
typedef uint8_t uint8; typedef uint16_t uint16; typedef uint32_t uint32;
typedef int8_t int8; typedef int16_t int16; typedef int32_t int32;
typedef int64_t int64;
#define CYRET_SUCCESS 0u
#define PSOC_AMUX_SIGNAL_CHANNEL_COUNT 5u
#define CAL_AMUX_HAS_CAP_CHANNEL 0u
#define PSOC_HW_CLASS 1u
#define PSOC_VIEW_CHANNEL_NONE 0xFFu
#define FILTER_FIR_NTAPS 1u
#define ADC_CF_2V5_COUNTS_PER_VOLT 1000000
extern const int g_fir_calibration_coeffs_q23[1];
uint8 EEPROM_ReadByte(uint16 address);
uint8 EEPROM_Write(const uint8 *data, uint8 row);
void EEPROM_UpdateTemperature(void);
uint8 CyEnterCriticalSection(void); void CyExitCriticalSection(uint8);
void CySysTickStart(void); void CySysTickSetCallback(uint8, void (*)(void));
void ADC_StopConvert(void); void ADC_StartConvert(void);
void psoc_amux_select_exclusive(uint8 channel,uint8 cap);
void psoc_adc_select_calibration_config(void); void psoc_adc_cal_override(uint8 x);
uint8 psoc_calibration_set_stage_dac(uint8 stage,int16 code);
void psoc_hw_set_pga(uint8 x); void psoc_hw_set_pgaout(uint8 x);
uint16 psoc_hw_pgaout_gain_x1000(void);
uint8 psoc_filter_load_fir_coefficients(const int *x,uint8 n);
void dma_route_select(uint8 x); void psoc_link_put_array(const uint8 *x,uint8 n);
#endif
