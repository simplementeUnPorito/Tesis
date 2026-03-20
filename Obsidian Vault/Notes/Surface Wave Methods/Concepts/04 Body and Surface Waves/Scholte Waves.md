# Ondas de Scholte

> **Fuente principal:** Sebastiano Foti, Chapter 8, Sección 8.2 · pp. 403–412

Son ondas superficiales que se propagan en la **interfaz sólido-líquido** (fondo marino), de forma análoga a las [[Rayleigh Waves|ondas de Rayleigh]] en la interfaz sólido-aire. Fueron descritas por Scholte (1947) como los **modos normales reales** del sistema de capas para el caso *soft bottom* [12, 13].

## Condición de existencia (*soft bottom*)

La condición *soft bottom* se cumple cuando la **velocidad de corte del sólido es menor que la velocidad compresional del agua**:

$$V_{S,\text{sólido}} < V_{P,\text{agua}} \approx 1500 \text{ m/s}$$

Esta condición es casi universalmente válida en sedimentos no consolidados (Vs < 200 m/s). En este caso, las ondas de Scholte son los **modos normales reales** de la ecuación secular (raíces reales), a diferencia de los modos fugaces de onda P-guiada que corresponden a raíces complejas.

## Motivación en contexto marino

En sedimentos saturados, la **velocidad de onda P está dominada por la compresibilidad del agua poral** (~1500 m/s) y varía muy poco entre tipos de sedimento. La **velocidad de onda S, en cambio, está controlada por el esqueleto sólido** y está directamente correlacionada con parámetros geotécnicos. En consecuencia:

- La variación de Vs en los primeros metros de sedimento es **un orden de magnitud mayor** que la variación de Vp.
- El análisis de ondas de Scholte permite estimar el perfil Vs del subfondo de manera **no invasiva**.
- El ratio Vp/Vs puede ser > 10 en sedimentos muy blandos.

## Características físicas

- **Movimiento de partícula:** elíptico retrógrado, análogo al de las ondas de Rayleigh. La energía se concentra en la interfaz sólido-líquido.
- **Penetración:** ≈ una longitud de onda en el sólido, ≈ media longitud de onda en el líquido (para dos semiespacios en contacto).
- **Dispersión:** modales y dispersivas, como las Rayleigh. El **modo fundamental no tiene frecuencia de corte** (existe para cualquier frecuencia). Los modos superiores sí tienen frecuencia de corte.
- **Velocidad:** siempre menor que la velocidad de Rayleigh del sólido equivalente (sin columna de agua). A frecuencia → 0, la velocidad de Scholte tiende a la velocidad de Rayleigh del semiespacio. A frecuencia → ∞, tiende a la velocidad de onda de Stoneley en la interfaz sólido-líquido.

## Efecto de la capa de agua sobre la dispersión

Incluso una **capa de agua muy delgada** (0.5–3 m) modifica la curva de dispersión de Scholte con respecto a la de Rayleigh (sin agua). Este efecto es no trivial:

- Para Hw = 0.5 m ya existe una diferencia apreciable.
- Para Hw = 3 m la diferencia puede alcanzar **hasta ~18%** en el rango de 10–20 Hz.
- La diferencia aumenta con la profundidad de agua y disminuye con la frecuencia.

**Consecuencia práctica:** analizar datos de Scholte con un modelo directo de ondas de Rayleigh (ignorando la capa de agua) lleva a una **subestimación sistemática de Vs** en los sedimentos. Es imprescindible incluir el espesor y la velocidad del agua como parámetros del modelo de inversión.

> Referencia: Figura 8.10b (p. 406) y Figura 8.12 (p. 407) del libro.

## Generación y registro en campo

**Fuentes:**
- Impacto en el fondo marino o **fuente de presión en la columna de agua** (air-gun, sparker, speargun).
- Un air-gun puede excitar ondas de Scholte con alta eficiencia incluso en 100 m de agua; la capa de agua actúa como filtro pasa-alto (limita la banda hacia bajas frecuencias).
- En aguas someras, fuentes de impacto son más eficientes en el rango de frecuencias de Scholte (>5 Hz).

**Receptores:**
- Hidrófonos acoplados al fondo (*ocean bottom hydrophones*).
- Geófonos enterrados en el sedimento (OBS — *ocean bottom seismometer*).
- En la orilla: hibridación geophones (tierra) + hidrófonos (fondo), misma fuente.

## Ondas de Scholte vs ondas P-guiadas

En el mismo sistema agua-sedimento coexisten dos tipos de ondas aprovechables:

| Característica | Ondas de Scholte | Ondas P-guiadas |
|---|---|---|
| Tipo | Modos normales reales | Modos fugaces (*leaky modes*) |
| Velocidad de fase | < Vs del sólido (muy baja) | > Vp del agua (> 1500 m/s) |
| Parámetro estimado | **Vs** del subfondo | **Vp** del subfondo |
| Visibilidad en registros | Tren de baja velocidad, a veces débil | Dominante, llega primero |
| Separación en registro | Requiere filtro pasa-bajo | Directamente visible |

La **inversión conjunta** de ondas de Scholte (Vs) y P-guiadas (Vp) permite estimar ambos perfiles con espesores compartidos, aprovechando la complementariedad de la información.

## Flujo de trabajo en contexto marino

1. Adquirir registros de fondo marino (hidrófonos o OBS).
2. Identificar el tren de ondas de Scholte (baja velocidad) separado del frente de ondas P-guiadas (alta velocidad).
3. Aplicar filtro pasa-bajo si las ondas de Scholte son débiles frente a las P-guiadas.
4. Extraer la curva de dispersión de Scholte (análisis f-k o τ-p).
5. Invertir incluyendo la capa de agua (velocidad y espesor) como parámetros del modelo.
6. Si se dispone de datos de P-guiadas: inversión conjunta Scholte + P-guiadas.

## Aplicación en la orilla (*shoreline*)

Un arreglo híbrido con geófonos en tierra e hidrófonos en el fondo permite registrar simultáneamente:
- **Ondas de Rayleigh** en la parte terrestre.
- **Ondas de Scholte** en la parte submarina.

La inversión conjunta de ambos conjuntos de datos permite una **caracterización continua** a lo largo de la línea costera, sin discontinuidad en la transición tierra-mar.

## Relaciones

- [[Rayleigh Waves]] — análogo terrestre; Scholte = Rayleigh en interfaz sólido-líquido
- [[Dispersion Curve]] — curva de dispersión de Scholte afectada por la capa de agua
- [[Phase Velocity]] — velocidad siempre menor que la de Rayleigh para el mismo sólido

## Fuentes

- Scholte, J.G.J. (1947). The range of existence of Rayleigh and Stoneley waves. *Geophys. J. Int.*, 5(s5), 120–126.
- PDF: Sebastiano Foti Chapter 8 (sección 8.2 — Scholte waves, guided P-waves, marine example, pp. 403–412)
