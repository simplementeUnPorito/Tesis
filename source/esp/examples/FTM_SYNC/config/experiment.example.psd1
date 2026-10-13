# FTM_SYNC - configuracion local. Copiar a config\experiment.local.psd1 (ignorado por git) y editar.
@{
    # --- CONFIRMAR CONTRA EL PINOUT DE LA PLACA ANTES DE CONECTAR NADA ---
    # Pasar a $true recien despues de verificar en la hoja de pines de TU placa que
    # PulseGpio (y LedGpio) estan libres, que no son pines de strapping/flash/PSRAM/USB
    # y que son accesibles en el header. Flash-Node.ps1 se niega a flashear mientras sea $false.
    BoardPinoutConfirmed = $false
    BoardModel           = 'SIN CONFIRMAR (probable YD-ESP32-S3 N16R8, ver PLACA_YD_ESP32S3.md)'

    # Pulso de referencia por hardware (MCPWM). Upstream usa GPIO7 por defecto y en su README
    # (sondas en GND + GPIO7). 2 kHz, 5 % de ciclo (25 us en alto): es para OSCILOSCOPIO.
    # Un LED en este pin se ve apenas tenue, NO parpadea.
    PulseGpio = 7

    # LED visible (parpadeo, periodo 1,25 s) que upstream maneja con gpio_set_level() desde la ISR del
    # temporizador, en un pin DISTINTO de PulseGpio. Es ACTIVO EN BAJO: 3V3 -> resistencia
    # (330 ohm..1 kohm) -> LED -> pin. Desactivado hasta elegir un pin libre y confirmado.
    # LedType = 'gpio'   : LED simple activo en bajo (gpio_set_level desde la ISR).
    # LedType = 'ws2812' : LED RGB direccionable (opcion FTS_LED_WS2812 de upstream: driver RMT +
    #                      tarea; el LED integrado NO es un LED simple y NO sirve para medir ns).
    #                      Segun PLACA_YD_ESP32S3.md el WS2812 de la YD-ESP32-S3 estaria en GPIO48
    #                      (provisional, sin confirmar fisicamente).
    LedEnabled = $false
    LedType    = 'gpio'
    LedGpio    = -1

    # 'usb-serial-jtag' (USB nativo) o 'uart0' (puerto UART/puente). Confirmar segun el cable usado.
    Console = 'usb-serial-jtag'

    # Red del experimento (el maestro crea el AP; clave >= 8 caracteres).
    WifiSsid     = 'FTM_SYNC_TESIS'
    WifiPassword = 'ftmsync-tesis-01'
    WifiChannel  = 1

    # Carpeta de ESP-IDF v5.5.1 ya instalada (la que contiene export.ps1). Vacio = se usa el
    # entorno ya activo (idf.py en PATH / IDF_PATH). Este paquete NO instala nada.
    IdfPath = ''

    # Carpeta de trabajo (copia de upstream + managed_components + builds). Vacio = FTM_SYNC\work.
    # Si el build falla por rutas largas de Windows, apuntar a algo corto, p. ej. C:\fw.
    WorkRoot = ''

    # Puertos COM por nodo (se asignan al conectar cada placa; verificar en el Administrador de dispositivos).
    Ports = @{ REF = 'COM?'; F1 = 'COM?'; F2 = 'COM?'; F3 = 'COM?'; F4 = 'COM?' }
}
