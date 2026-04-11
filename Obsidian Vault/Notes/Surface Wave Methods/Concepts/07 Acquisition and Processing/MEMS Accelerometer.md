---
name: MEMS Accelerometer
description: Sensor de estado sólido que mide aceleración — alternativa al geófono en [[MASW Method|MASW]]; respuesta plana desde DC, digital, robusto; mayor ruido de piso en bajas frecuencias
type: reference
---

# MEMS Accelerometer — Acelerómetro MEMS

> [!CONCEPT] Definición
> Los **acelerómetros MEMS** (*Micro-Electro-Mechanical Systems*) son sensores de estado sólido que miden **aceleración** del suelo, en contraste con el [[Geophone|geófono]] que mide velocidad. Son sensores capacitivos o piezoresistivos que detectan el desplazamiento de una masa inercial microscópica grabada en silicio. Su respuesta es plana desde DC (0 Hz) hasta frecuencias altas (> 200 Hz), sin la limitación de la frecuencia natural del geófono. Son digitales (contienen ADC interno), robustos mecánicamente (sin partes móviles a escala macroscópica), de bajo costo y peso reducido. Aplicados a [[MASW Method|MASW]] y [[Adquisición de Datos|adquisición sísmica]], son una alternativa viable a los geófonos en el rango 5–200 Hz. Su limitación es el **mayor ruido de piso** a bajas frecuencias (<1 Hz) comparado con geófonos de banda ancha de alta calidad, aunque para [[MASW Method|MASW]] activo (>5 Hz) esta diferencia es prácticamente insignificante.
>
> — Foti et al. (2018), Cap. 3, §3.2; Muyzert (2007), *Geophysics*.

## Comparación con geófonos

| Característica | [[Geophone|Geófono]] | MEMS Accelerometer |
|---|---|---|
| Magnitud medida | Velocidad de partícula | Aceleración |
| Respuesta en frecuencia | Plana por encima de $f_n$ | Plana desde DC |
| Sensibilidad a bajas frecuencias | Baja (debajo de $f_n$) | Alta (DC a bajas $f$) |
| Ruido de piso | Bajo (<1 ng/√Hz con bobina inducida) | Mayor (capacitivo: ~1–10 ng/√Hz) |
| Masa/volumen | Mayor (bobina + imán) | Menor (chip MEMS) |
| Costo unitario | Bajo–medio | Bajo |
| Señal de salida | Analógica | Digital (con ADC integrado) |
| Robusto a inclinación | Moderado | Alto (sin partes móviles críticas) |

## Conversión de señal

Como el MEMS mide aceleración $\ddot{u}(t)$, para comparar con la teoría de propagación de ondas (que trabaja en desplazamiento o velocidad) se integra numéricamente:
- Velocidad: $\dot{u}(t) = \int \ddot{u}\, dt$
- Desplazamiento: $u(t) = \int\int \ddot{u}\, dt^2$

En el dominio de la frecuencia, la división por $i\omega$ o $(i\omega)^2$ es exacta. Para el análisis f-k del [[MASW Method|MASW]], la fase de la señal no cambia con la integración → la [[Dispersion Curve|curva de dispersión]] extraída es idéntica usando geófonos o MEMS.

## Aplicaciones en métodos de ondas superficiales

- **[[MASW Method|MASW]] activo (5–100 Hz)**: los MEMS son equivalentes a los geófonos de 4.5–14 Hz. El ruido de piso elevado a <1 Hz no afecta el análisis.
- **Pasivo (ReMi, SPAC, 0.1–5 Hz)**: los MEMS de alta calidad (de diseño sísmico) son comparables a los geófonos de 4.5 Hz en el rango 0.5–5 Hz — suficiente para profundidades de hasta 100–200 m.
- **Monitoreo de largo plazo**: la robustez y el bajo consumo de los MEMS los hace ideales para redes de sensores distribuidos en monitoreo continuo (microzonificación, respuesta sísmica de sitio).

> [!EXAMPLE] Evidencia empírica: Garofalo et al. (2016) — MEMS en arrays pasivos InterPACIFIC
> **Papers 006+007 (Garofalo et al. 2016a/b)** incluyen algunos equipos participantes que utilizaron acelerómetros MEMS en lugar de geófonos para los arrays pasivos del estudio InterPACIFIC. Los resultados muestran que en el rango de frecuencias 1–10 Hz (relevante para profundidades de 20–100 m en los tres sitios), los sistemas basados en MEMS producen [[Dispersion Curve|curvas de dispersión]] consistentes con los sistemas de geófonos. Las diferencias entre operadores que usaron MEMS vs geófonos son comparables a las diferencias entre operadores con el mismo tipo de sensor — confirmando que el tipo de sensor (dentro de rangos razonables de calidad) no es la fuente dominante de variabilidad. La variabilidad está dominada por las decisiones de procesamiento e inversión.
>
> — Research Database, entradas 006, 007 (core); Garofalo et al. (2016a/b).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 3, §3.2 — sensores para adquisición sísmica |
| Muyzert (2007), *Geophysics* | MEMS para símica de exploración y near-surface |
| Garofalo et al. (2016a/b) | Papers 006, 007 — MEMS vs geófonos en InterPACIFIC |
| Kafadar (2020), *Geosci. Instrum.* 9(2):365–373 | Paper 052 — sistema de bajo costo con geófonos para HVSR; resultados comparables a equipos comerciales |
