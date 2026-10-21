# Resultado prueba RADIOSIL E2E

Generado: 2026-10-21T11:21:28.559-03:00

Esclavo: `COM8` @ 115200; maestro: `COM6` @ 921600; N=100.

| Intento | RADIOSIL | Recibidas/esperadas | Por nodo | Segundos | #RADIOSIL vuelve | HOT_WAIT n= | START_OK | ACK | STATUS/HELLO | READY | Resultado |
|---:|:---:|---:|:---|---:|:---:|:---:|:---:|---:|---:|---:|:---:|
| 1 | on | 3000/3000 | 0x02: 3000 | 6.42 | sí | sí | sí | 4 | 9 | 3 | OK |
| 2 | off | 3000/3000 | 0x02: 3000 | 5.29 | no | sí | sí | 5 | 30 | 3 | OK |
| 3 | on | 3000/3000 | 0x02: 3000 | 4.70 | sí | sí | sí | 5 | 30 | 3 | OK |
| 4 | off | 3000/3000 | 0x02: 3000 | 4.52 | no | sí | sí | 5 | 30 | 3 | OK |
| 5 | on | 3000/3000 | 0x02: 3000 | 6.78 | sí | sí | sí | 5 | 30 | 3 | OK |
| 6 | off | 0/3000 | — | 60.04 | no | no | no | 5 | 310 | 4 | FALLÓ |
| 7 | on | 3000/3000 | 0x02: 3000 | 4.90 | sí | sí | sí | 4 | 30 | 2 | OK |
| 8 | on | 3000/3000 | 0x02: 3000 | 4.96 | sí | sí | sí | 5 | 30 | 3 | OK |
| Resumen | on | — | — | — | — | — | — | — | — | — | 5/5 OK |
| Resumen | off | — | — | — | — | — | — | — | — | — | 2/3 OK |
