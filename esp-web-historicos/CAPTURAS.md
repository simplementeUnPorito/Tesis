# Matriz de capturas de las interfaces ESP32

Las siete versiones se levantan sin placa con `serve_demo.py`. Las imágenes se
guardan en `docs/Primera Presentación/latex-nueva-estructura/figuras/interfaces/esp_historico`.
El objetivo es documentar la evolución completa antes de reducirla para la
presentación final.

## Cómo levantar y verificar las versiones

Desde `C:\Github\Tesis\esp-web-historicos`:

```powershell
python .\serve_demo.py --list
python .\serve_demo.py --version 07_2026-08-03_pga-pgaout --port 8010
```

La segunda orden abre la interfaz elegida en <http://127.0.0.1:8010/>. No hace
falta conectar una placa: el servidor simula el WebSocket del maestro, tres nodos,
el estado del enlace, el escaneo Wi-Fi y el guardado de SSID y URL de ingesta.
Para cambiar de hito se detiene el proceso con `Ctrl+C` y se reemplaza el valor de
`--version` por cualquiera de los nombres devueltos por `--list`.

La verificación automática de las siete versiones se ejecuta con:

```powershell
python .\verificar_versiones.py
```

Esto comprueba HTML, rutas REST e intercambio WebSocket; las interacciones visuales
de cada menú se revisan luego conforme a la matriz de capturas siguiente.

## Criterio común

Para cada versión se conserva una captura de página completa y acercamientos de
los paneles que existan. Cuando una función no está implementada todavía, la
pantalla vacía también se conserva porque documenta el estado de ese hito.

- vista inicial oscura y vista clara;
- estado conectado al WebSocket simulado;
- gráfico con señal cruda, filtrada, envolventes, remoción de DC y espectro,
  cuando esos controles existan;
- zoom, reset y cursores, cuando estén disponibles;
- cada pestaña o panel funcional;
- log con los mensajes de conexión;
- modal de autenticación, cuando aparezca.

## 01 — UI inicial (`323fcb7`)

- `01_vista_inicial_oscura.png`: página completa.
- `02_vista_inicial_clara.png`: cambio de tema.
- `03_captura_arm_start_stop.png`: controles ARM, START, STOP y STATUS.
- `04_grafico_zoom_reset.png`: gráfico y herramientas iniciales.
- `05_descarga_zip.png`: bloque de descarga.
- `06_log_websocket.png`: conexión al servidor simulado.

## 02 — funcional incompleta (`76d6092`)

- `01_captura.png`: pestaña Captura.
- `02_nodos.png`: pestaña Nodos.
- `03_esclavos.png`: pestaña Esclavos.
- `04_export.png`: pestaña Export.
- `05_log.png`: pestaña Log.
- `06_tema_claro.png`: página completa clara.

## 03 — autocalibración (`70ca42e`)

- `01_captura.png`: operación global.
- `02_nodos.png`: estado de nodos.
- `03_esclavos.png`: configuración individual.
- `04_export.png`: exportación.
- `05_cursores.png`: cursores 1 y 2 activos.
- `06_espectro.png`: vista espectral.
- `07_autocalibracion.png`: controles y estado de calibración.
- `08_log.png`: mensajes de la secuencia.

## 04 — página operativa (`8b63d2b`)

- `01_captura.png`: ARM, duración, START/STOP y calibración.
- `02_esclavos.png`: paneles por nodo.
- `03_preservados.png`: lista y selección.
- `04_preservar.png`: operación de preservación.
- `05_export_csv_zip.png`: guardado CSV/ZIP.
- `06_autenticacion.png`: modal de conexión.
- `07_log.png`: registro de operación.

## 05 — UI finalizada (`89384d8`)

- `01_captura_completa.png`: vista general del flujo de campo.
- `02_decimacion_n.png`: aplicación de N.
- `03_duraciones_geo_hammer.png`: duraciones independientes.
- `04_limites_ram_sd.png`: máximos de RAM y SD.
- `05_descontar.png`: operación Descontar.
- `06_esclavos.png`: configuración por nodo.
- `07_preservados.png`: selección, Todos, Ninguno y Vaciar.
- `08_log.png`: registro.
- `09_tema_claro.png`: página clara.

## 06 — enlace y mDNS (`9eb8b5a`)

- `01_captura.png`: pestaña Captura.
- `02_esclavos.png`: pestaña Esclavos.
- `03_preservados.png`: pestaña Preservados.
- `04_enlace_estado.png`: estado de red, IP, canal y cola.
- `05_enlace_buscar.png`: redes 2,4 GHz simuladas.
- `06_enlace_configuracion.png`: SSID, contraseña y URL de servidor.
- `07_subir_servidor.png`: operación de subida.
- `08_log.png`: registro del enlace.

## 07 — PGA/PGAout (`d6463a`)

- `01_captura_completa.png`: página completa en su estado final.
- `02_grafico_cruda_filtrada.png`: comparación temporal.
- `03_envolventes_dc.png`: envolventes y remoción de continua.
- `04_espectro.png`: espectro visible.
- `05_cursores_zoom.png`: cursores y navegación del gráfico.
- `06_captura_parametros.png`: ARM, N, duraciones y límites.
- `07_esclavos_general.png`: conjunto de nodos.
- `08_esclavo_pga.png`: configuración con PGA.
- `09_esclavo_pgaout.png`: selección PGAout.
- `10_preservados.png`: adquisiciones conservadas.
- `11_enlace_estado.png`: estado de conexión y cola.
- `12_enlace_escaneo.png`: resultado del escaneo.
- `13_enlace_servidor.png`: URL de ingesta guardada.
- `14_subida_servidor.png`: carga del ZIP.
- `15_log.png`: mensajes de conexión, comandos y errores.
- `16_tema_claro.png`: vista final clara.

El inventario suma 60 capturas previstas. Se agregarán además recortes cuando
un panel resulte ilegible en la captura de página completa.
