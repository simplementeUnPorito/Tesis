# Resultado prueba RADIOSIL E2E

Generado: 2026-10-21T10:51:12.566-03:00

Esclavo: `COM8` @ 115200; maestro: `COM6` @ 921600; N=100.

| Intento | RADIOSIL | Recibidas/esperadas | Por nodo | Segundos | #RADIOSIL vuelve | ACK | STATUS/HELLO | READY | Resultado |
|---:|:---:|---:|:---|---:|:---:|---:|---:|---:|:---:|
| 1 | on | 3000/3000 | 0x02: 3000 | 4.07 | sí | 4 | 18 | 3 | OK |
| 2 | on | 0/3000 | — | 60.05 | no | 5 | 310 | 4 | FALLÓ |
| 3 | on | 3000/3000 | 0x02: 3000 | 3.95 | sí | 4 | 30 | 2 | OK |
| 4 | off | 3000/3000 | 0x02: 3000 | 4.47 | no | 5 | 30 | 3 | OK |
