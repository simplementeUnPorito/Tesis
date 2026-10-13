# Componente "main" envoltorio: compila el fts_main.c de upstream tal cual y
# genera build_info.h con el mismo script de upstream. No requiere usb_uplink
# (fts_main.c solo lo incluye con CONFIG_FTS_MODE_USB_NCM).
get_filename_component(FTS_UPSTREAM_MAIN "${CMAKE_CURRENT_LIST_DIR}/../../upstream/main" ABSOLUTE)

set(BUILD_INFO_H "${CMAKE_CURRENT_BINARY_DIR}/build_info.h")
execute_process(
    COMMAND ${CMAKE_COMMAND}
        -DOUTPUT_FILE=${BUILD_INFO_H}
        -DCMAKE_SOURCE_DIR=${FTS_UPSTREAM_MAIN}
        -P ${FTS_UPSTREAM_MAIN}/build_info.cmake
)

idf_component_register(
    SRCS "${FTS_UPSTREAM_MAIN}/fts_main.c"
    INCLUDE_DIRS "${CMAKE_CURRENT_BINARY_DIR}"
    PRIV_REQUIRES esp_driver_mcpwm esp_driver_gpio dtr dtc ftm fts_mqtt ws2812
                  esp_netif esp_event nvs_flash esp_rom
)
