# Proyecto PlatformIO (ESP-IDF) para FTS. Reutiliza SIN copiar los componentes
# de ../upstream/components; el componente "main" propio esta en src/.
cmake_minimum_required(VERSION 3.16.0)

# PlatformIO ya pasa -DEXTRA_COMPONENT_DIRS (src/); se anexa, no se reemplaza.
get_filename_component(FTS_UPSTREAM_DIR "${CMAKE_CURRENT_LIST_DIR}/../upstream" ABSOLUTE)
list(APPEND EXTRA_COMPONENT_DIRS "${FTS_UPSTREAM_DIR}/components")

# usb_uplink (esp_tinyusb) queda fuera del build: este montaje no usa USB-NCM.
set(EXCLUDE_COMPONENTS usb_uplink)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(fts_pio)
