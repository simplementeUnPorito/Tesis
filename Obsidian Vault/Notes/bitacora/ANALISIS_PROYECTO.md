# Análisis del Proyecto — Tesis MASW Geofóno SM-24

*Generado automáticamente por el loop de bitácora — 4 de junio de 2026*

---

## Timeline de Etapas

```mermaid
timeline
    title Evolución del Proyecto — Feb 2026 → May 2026
    
    section Fundación
        Feb 25 : Commit inicial
                : Estructura básica del repositorio
    
    section Marco Teórico
        Mar 03 : Vault Obsidian arranca
                : Capítulo 1 resumen
                : Pruebas GitHub Actions
        Mar 11 : Foti — libros MASW en PDF
        Mar 13 : Chapter 2 pre-reordenamiento
        Mar 17 : MATLAB MASW submodule
                : Scripts Python calibración
                : XDDDD (primer commit épico)
        Mar 18 : Seguridad del vault
        Mar 19 : Caps 3/4/5 + Near-field Effect
        Mar 20 : Claudio revisión
        Mar 23 : BLABLABLA (expansion papers)
    
    section INVESTIGADOR IA
        Apr 10 : XDXDXD — arranque loop IA
        Apr 11 : 89 commits — 144 conceptos Zettelkasten
        Apr 12 : 25 commits — SEXTA FASE, 148 conceptos
    
    section Hardware Inicial
        Apr 15 : Assets reorganización
        Apr 17 : SM-24 modelo + primeras mediciones
        Apr 18 : Pivote analógico→FIR digital
        Apr 19 : Loop auto-mejora 15 commits
        Apr 22 : Primera señal real SM-24
        Apr 27 : Scope simplificado + compensadores
        Apr 29 : FIR notch 50Hz 464 taps + DFB
        Apr 30 : Pivot Sallen-Key → MFB
    
    section Sistema Digital
        May 05 : Análisis espectral Welch
        May 10 : Calibración VDAC offset
        May 17 : Protocolo 4-byte, validación op-amp
        May 18 : 4 motores búsqueda compensador
    
    section Sistema Completo
        May 20 : DiferencialToSingleEnded — cadena analógica completa
        May 24 : ESP32 inalámbrico multi-nodo
        May 25 : HELLO, START probe, CP210x
        May 26 : PRESTART — ¡FUNCIONA!
        May 28 : AcondicionamientoMartillo
        May 29 : Primer build martillo OK
        May 31 : Refactor UART, PR #2 merge
```

---

## Actividad por Día

```mermaid
xychart-beta
    title "Commits por Día (excluyendo loop INVESTIGADOR)"
    x-axis ["25-Feb", "03-Mar", "11-Mar", "13-Mar", "17-Mar", "18-Mar", "19-Mar", "20-Mar", "23-Mar", "10-Apr", "15-Apr", "17-Apr", "18-Apr", "19-Apr", "22-Apr", "27-Apr", "29-Apr", "30-Apr", "05-May", "10-May", "17-May", "18-May", "20-May", "24-May", "25-May", "26-May", "28-May", "29-May", "31-May"]
    y-axis "Commits" 0 --> 20
    bar [1, 7, 1, 2, 6, 1, 2, 1, 1, 1, 1, 4, 1, 15, 1, 1, 1, 2, 1, 3, 2, 1, 3, 3, 4, 2, 1, 1, 4]
```

---

## Mapa de Tecnologías

```mermaid
graph TB
    subgraph "Sensor"
        SM24[SM-24 Geófono<br/>fn=4.5Hz G=28.8V·s/m]
        Martillo[PCB 086D20<br/>Martillo impulso]
    end
    
    subgraph "Frontend Analógico — PSoC 5LP"
        PGApn[PGAp + PGAn<br/>Diferencial 2×]
        OPAbp[OPAbp<br/>Bandpass MFB]
        OPAadder[OPAadder<br/>Sumador Pazos]
        OPAlp[OPAlp<br/>Lowpass]
        LPF[LPF 1+2<br/>Anti-alias]
        ADC[ADC SAR<br/>1020-4000 SPS]
        DFB[DFB — FIR<br/>Notch 50Hz 464 taps]
        VDAC[VDAC<br/>Calibración offset]
    end
    
    subgraph "Comunicación"
        UART[UART 460800 baud<br/>Frame 95 bytes]
        SPI_old[SPI 4MHz — obsoleto<br/>Frame 306 bytes]
        ESPNOW[ESP-NOW<br/>MsgData 165 bytes]
        TCP[WiFi TCP<br/>Puerto 5005]
    end
    
    subgraph "ESP32 Red"
        Slave[ESP32 Esclavo<br/>PsocUART → EspNow]
        Master[ESP32 Maestro<br/>WiFi AP + TCP Server]
    end
    
    subgraph "Análisis — MATLAB"
        Scope[InterfaceESP.m<br/>GUI 4 nodos]
        Espectral[analisis_espectral.m<br/>Welch PSD Δf=0.062Hz]
        Modelo[analisis_modelo.m<br/>Modelo forward MASW]
        FIR[filtroFir.m<br/>800 taps multiband]
    end
    
    subgraph "Diseño — Python"
        Simple[calculoCompensadorSimple.py<br/>Grid + modelo real op-amp]
        Full[calculoCompensadorFull.py<br/>GPU + exhaustivo]
        GPU[calculoCompensadorGPU.py<br/>PyTorch CUDA/XPU]
        Optimo[calculoCompensadorOptimo.py<br/>differential_evolution]
        Graf[graficar_compensador_csv.py<br/>CLI visualizador]
    end
    
    SM24 --> PGApn
    Martillo --> AcondMartillo[AcondicionamientoMartillo<br/>PSoC separado]
    PGApn --> OPAbp
    PGApn --> OPAadder
    OPAbp --> OPAadder
    OPAadder --> OPAlp
    OPAlp --> LPF
    LPF --> ADC
    ADC --> DFB
    VDAC --> OPAadder
    DFB --> UART
    UART --> Slave
    Slave --> ESPNOW
    ESPNOW --> Master
    Master --> TCP
    TCP --> Scope
    
    Simple --> Graf
    Full --> Graf
    GPU --> Graf
    Optimo --> Graf
    
    Scope --> Espectral
    Scope --> Modelo
    
    style SM24 fill:#4CAF50,color:#fff
    style Martillo fill:#4CAF50,color:#fff
    style OPAbp fill:#2196F3,color:#fff
    style OPAadder fill:#2196F3,color:#fff
    style DFB fill:#9C27B0,color:#fff
    style ESPNOW fill:#FF9800,color:#fff
    style Master fill:#FF9800,color:#fff
    style Slave fill:#FF9800,color:#fff
    style SPI_old fill:#999,color:#fff
```

---

## Evolución del Protocolo PSoC

```mermaid
sequenceDiagram
    participant M as MATLAB
    participant PSoC as PSoC 5LP
    
    rect rgb(200, 230, 200)
        Note over M,PSoC: Protocolo 1 — Abril 22 (10 bytes, [0xAA])
        PSoC->>M: [0xAA][type][ch][d3][d2][d1][d0][s3][s2][s1]
    end
    
    rect rgb(200, 200, 230)
        Note over M,PSoC: Protocolo 2 — Abril 27 (8 bytes, [0xAA])
        PSoC->>M: [0xAA][type][ch][d3][d2][d1][d0][status]
    end
    
    rect rgb(230, 200, 200)
        Note over M,PSoC: Protocolo 3 — Abril 29 (5 bytes, [0x56])
        PSoC->>M: [0x56][0x00][b2][b1][b0]
        M->>PSoC: [0xAB][0xA5][0x00][0xA5] (config req)
    end
    
    rect rgb(200, 220, 240)
        Note over M,PSoC: Protocolo 4 — Mayo 17 (4 bytes, TYPE|CH multiplexed)
        PSoC->>M: [0x56][TYPE:4|CH:2|D17:1|D16:1][D15:D8][D7:D0]
    end
    
    rect rgb(240, 220, 200)
        Note over M,PSoC: Protocolo Final — Mayo 31 (UART, 95 bytes/frame)
        PSoC->>M: [0xAB][n=30][seq_lo][seq_hi] + 30×3 bytes + [CRC]
        M->>PSoC: [0xAB][cmd][param][checksum XOR]
    end
```

---

## Evolución del Vault Obsidian

```mermaid
xychart-beta
    title "Conceptos Zettelkasten acumulados por semana"
    x-axis ["Semana 1 (Feb)", "Semana 4 (Mar)", "Semana 6 (Mar)", "Semana 10 (Abr)", "Semana 15 (Abr-11)", "Semana 16 (Abr-12)", "Semana 17-20", "Semana 21-22", "May-Junio"]
    y-axis "Conceptos" 0 --> 160
    line [0, 10, 25, 30, 144, 148, 150, 155, 160]
```

**Hitos del vault:**
- `2026-03-03`: Primer Zettelkasten — Capítulo 1 MASW
- `2026-03-17`: Expansión teórica con submodule MATLAB MASW
- `2026-04-11`: INVESTIGADOR loop — 89 commits, 144 conceptos en un día
- `2026-04-12`: Cierre INVESTIGADOR — 148 conceptos totales, 4107 wikilinks
- `2026-05-31`: Estado final — ~160 conceptos, sistema completo documentado

---

## Mapa de Etapas del Proyecto

```mermaid
gantt
    title Cronograma del Proyecto — Feb 2026 a May 2026
    dateFormat  YYYY-MM-DD
    axisFormat  %d-%b
    
    section Marco Teórico
    Repositorio inicial         :done, 2026-02-25, 2026-03-03
    Vault Obsidian + Caps 1-2   :done, 2026-03-03, 2026-03-13
    Papers + MATLAB submodule   :done, 2026-03-17, 2026-03-23
    INVESTIGADOR Zettelkasten   :done, 2026-04-10, 2026-04-12
    
    section Hardware
    Modelo SM-24 Simulink        :done, 2026-04-10, 2026-04-17
    Primera señal real SM-24     :done, 2026-04-17, 2026-04-22
    Protocolo UART PSoC          :done, 2026-04-22, 2026-04-29
    FIR notch 50Hz DFB           :done, 2026-04-29, 2026-05-05
    
    section Analógico
    MFB vs Sallen-Key decisión   :done, 2026-04-30, 2026-05-05
    Análisis espectral Welch     :done, 2026-05-05, 2026-05-10
    Calibración VDAC             :done, 2026-05-10, 2026-05-17
    Protocolo 4-byte AMUX        :done, 2026-05-17, 2026-05-18
    Búsqueda compensador Python  :done, 2026-05-18, 2026-05-20
    
    section Sistema Completo
    DiferencialToSingleEnded     :done, 2026-05-20, 2026-05-24
    ESP32 arquitectura            :done, 2026-05-24, 2026-05-25
    Debug hardware real           :done, 2026-05-25, 2026-05-26
    Primera transmisión exitosa   :milestone, 2026-05-26, 1d
    Martillo PSoC               :done, 2026-05-28, 2026-05-31
    Refactor UART + PR merge      :done, 2026-05-31, 2026-06-01
```

---

## Estadísticas Globales

| Métrica | Valor |
|---------|-------|
| **Período** | 25 Feb → 31 May 2026 (95 días) |
| **Total commits** | ~197 (incluyendo loop INVESTIGADOR) |
| **Días con trabajo** | 31 únicos |
| **Commits técnicos** | ~110 (excluyendo INVESTIGADOR) |
| **Proyectos PSoC** | 6 (`DiferencialConRrefs*`, `DiferencialToSingleEnded`, `DiferencialToSingleEnded_ESP`, `AcondicionamientoMartillo`) |
| **Scripts Python** | 7 (`calculoCompensador*`, `graficar_compensador_csv.py`, `analisis_espectral.py`) |
| **Scripts MATLAB** | ~12 (`geophone_scope*`, `analisis_*`, `filtroFir.m`, `compensador*.m`) |
| **Conceptos Zettelkasten** | ~160 |
| **Wikilinks** | >4107 |
| **Protocolos UART PSoC** | 5 evoluciones |
| **Bytes por frame (final)** | 95 (de 306 en SPI) |
| **Pico de actividad** | 11 Abril (89 commits INVESTIGADOR) |
| **Commit más épico** | "Parece que funciona la putaaaa" (26 Mayo) |

---

## Arco del Proyecto — Análisis Cualitativo

### Fase 1: El Marco (Feb–Mar 2026)

El proyecto arranca en silencio. Un repositorio vacío, un commit inicial, y la certeza de que hay que escribir una tesis sobre MASW. El trabajo de marzo es lento y honesto: construir el vault Obsidian, leer a Foti y Sebastiano, entender la física de las ondas de Rayleigh antes de escribir una línea de código de medición.

Los mensajes de commit en esta fase son mundanos: "Ordenamiento de directorios", "primer commit", "Resumen capitulo 1". Solo el "XDDDD" del 17 de marzo rompe la monotonía — algo no salió como se esperaba pero la broma ayuda.

### Fase 2: La Euforia Artificial (Abril 10-12)

El loop INVESTIGADOR es la fase más explosiva del proyecto en términos de números: 89 commits en un día, 144 conceptos, 4107 wikilinks. Es IA construyendo sobre IA, iteración sobre iteración. El vault crece de forma exponencial en 48 horas.

Pero el Zettelkasten no es el sistema de medición. Es la base teórica — necesaria, pero no suficiente. Después del 12 de abril, el trabajo real empieza.

### Fase 3: El Hardware Que No Funciona (Abril 15-30)

La primera señal real del SM-24 llega el 22 de abril. Es ruidosa, incompleta, y emocionante. El commit "CompensadorKai, compensadorPazos, geophone_scope" del 22 de abril es el primer día en que código de software toca datos de geofísica real.

Los pivotes son dolorosos: Sallen-Key funciona en teoría, MFB funciona mejor en práctica. El FIR notch de 50Hz con 464 taps en DFB hardware es elegante pero demoró semanas en funcionar. El VDAC de calibración offset (VDp=142, VDn=142) es el resultado de medir cuánto estaba corrido el cero del ADC.

### Fase 4: La Búsqueda del Compensador (Mayo 1-19)

Los cuatro scripts Python (`Simple`, `Full`, `GPU`, `Optimo`) son el reconocimiento de que el problema del compensador analógico es difícil y que una sola estrategia no alcanza. El commit "ayudame dios analogico quiero sucumbir al diablo digital" del 18 de mayo es el nadir emocional del proyecto — y también el pico de la ingeniería: 15 candidatos con ζ entre 197-944, modelos con A0=90dB, fp=8MHz, Rin=35MΩ.

### Fase 5: El Sistema Funciona (Mayo 20-31)

`DiferencialToSingleEnded` el 20 de mayo es el punto de quiebre. Una cadena analógica completa (PGAp/PGAn → OPAbp → OPAadder → OPAlp → ADC) corriendo en el PSoC, con protocolo UART y MATLAB recibiendo datos. No es perfecto — el "parece que funciona" del 26 de mayo incluye el "parece" con razón. Pero funciona.

El sistema ESP32 inalámbrico nace el 24 de mayo de código generado por Claude, es debugeado brutalmente el 25 (HELLO beacon, START probe, CP210x drivers), funciona por primera vez el 26, rompe el 28 ("AYUDAAAAAAAAAAA"), y se estabiliza el 31 con el refactor UART + PR merge.

La última semana de mayo es la semana en que el proyecto pasa de "señal ruidosa en un scope MATLAB" a "sistema distribuido inalámbrico de adquisición multi-canal". El commit final del mes — el merge de PR #2 — sella la arquitectura que irá al banco de pruebas en campo.

---

## Próximos Pasos Identificados (al 31 de Mayo)

1. **AcondicionamientoMartillo**: La ISR `getADCdata` está vacía. El firmware de lectura del martillo de impacto debe completarse para detectar onset del golpe, medir fuerza, y transmitir al ESP esclavo del martillo.

2. **Validación en campo**: Las mediciones con martillo real en suelo real son el próximo paso experimental. `analisis_modelo.m` ya está listo para el procesamiento.

3. **Compensador analógico**: Los 15 candidatos del CSV están en simulación. Uno debe elegirse, fabricarse, y medirse en hardware real para validar el modelo del op-amp.

4. **Calibración del sistema completo**: La cadena desde el SM-24 hasta MATLAB tiene múltiples factores de ganancia (PGA, VDAC, escala ADC, escala UART). Una calibración absoluta (mV/LSB end-to-end) es necesaria para obtener valores de velocidad de partícula en m/s.

5. **Curvas de dispersión**: Con datos reales de campo (múltiples distancias de fuente a receptor), se puede calcular la curva de dispersión de ondas Rayleigh y hacer la inversión para obtener el perfil Vs del suelo.

---

*Bitácora completa: 33 entradas, Mayo de 2026. Generada con Claude Code (claude-sonnet-4-6).*
