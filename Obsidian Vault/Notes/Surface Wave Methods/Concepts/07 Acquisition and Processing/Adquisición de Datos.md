---
name: Adquisición de Datos
description: Primer paso del flujo [[MASW Method|MASW]] — generación y registro de ondas sísmicas en campo; parámetros de diseño del arreglo, fuentes activas/pasivas y desafíos operativos
type: reference
---

# Adquisición de Datos Sísmicos

> [!CONCEPT] Definición
> La **adquisición de datos** es el primer paso crítico del flujo de trabajo de los métodos de [[Surface Waves|ondas superficiales]]: consiste en generar ondas sísmicas y registrar su propagación en tiempo y espacio, produciendo los **sismogramas multicanal** $u(x_j, t_n)$ que alimentan el [[Procesamiento de Señales|procesamiento]] y la [[Inversión|inversión]]. El sistema se compone de tres elementos: (1) **fuente** (activa o pasiva) que determina el contenido en frecuencias y la profundidad de investigación, (2) **arreglo de receptores** cuya geometría determina la resolución modal y el rango de longitudes de onda accesible, y (3) **sistema de registro** (sismógrafo multicanal) que digitaliza las señales. Los parámetros de diseño — espaciado $\Delta x$, apertura total $D$, offset de fuente $L_s$, duración del registro $T$ — controlan la calidad de la [[Dispersion Curve|curva de dispersión]] extraída y, por tanto, la resolución del perfil $V_S(z)$ final.
>
> — Foti et al. (2018), Cap. 3, pp. 77–192.

## Componentes del sistema de adquisición

### 1. Fuentes sísmicas

Las fuentes determinan el **rango de frecuencias** de las ondas generadas y, por tanto, la profundidad de investigación ($z_{max} \approx \lambda_{max}/2$):

| Fuente | Tipo | Rango de frecuencia típico | Profundidad |
|---|---|---|---|
| Sledgehammer (martillo + placa) | Activa | 5–100 Hz | <30 m |
| Caída de peso | Activa | 3–50 Hz | <50 m |
| Vibroseis (sweep) | Activa | 1–100 Hz | <100 m |
| Ruido ambiental (tráfico, viento) | Pasiva | 0.1–10 Hz | >50 m |

Las **fuentes activas** permiten controlar la forma de onda, la posición y el timing → análisis f-k con alta resolución. Las **fuentes pasivas** aportan energía en bajas frecuencias (mayor profundidad) pero dependen de la distribución del ruido ambiental.

### 2. Receptores y arreglos

Los receptores estándar en [[MASW Method|MASW]] son **[[Geophone|geófono]] verticales** (14 Hz, 28 Hz o 4.5 Hz) que miden la componente vertical del movimiento → sensibles a [[Rayleigh Waves|ondas de Rayleigh]]. Para medir [[Love Waves|ondas de Love]] se requieren [[Geophone|geófono]] horizontales transversales.

**Geometría del arreglo** ([[MASW Method|MASW]] activo):

| Parámetro | Símbolo | Efecto sobre la [[Dispersion Curve|curva de dispersión]] |
|---|---|---|
| Espaciado entre [[Geophone|geófono]] | $\Delta x$ | [[Wavelength|Longitud de onda]] mínima: $\lambda_{min} \approx 2\Delta x$ |
| Apertura total | $D = N\Delta x$ | [[Wavelength|Longitud de onda]] máxima: $\lambda_{max} \approx D$ |
| Offset de fuente | $L_s$ | Exclusión de [[Near-field Effect|efectos de campo cercano]]: $L_s \geq \lambda_{max}/2$ |
| Número de canales | $N$ | Resolución modal: mayor $N$ → mejor separación de modos |
| Duración del registro | $T$ | Resolución en frecuencia: $\Delta f = 1/T$ |

### 3. Sistema de registro

Los **sismógrafos multicanal** deben ofrecer:
- Suficiente rango dinámico (≥90 dB) para registrar simultáneamente la onda directa (alta amplitud) y las ondas de largo offset (baja amplitud).
- Frecuencia de muestreo temporal $f_s \geq 2 f_{max}$ (criterio de Nyquist).
- Sincronización temporal precisa entre canales (trigger desde la fuente).

Una ventaja operativa de la adquisición en superficie es la posibilidad de **verificar visualmente el acoplamiento [[Geophone|geófono]]–suelo**, relevante especialmente para estimar el [[Shear Damping Ratio|amortiguamiento]] $D_s$ a partir de la curva de [[Attenuation|atenuación]].

## Desafíos en la adquisición

### Ruido incoherente

Vibraciones aleatorias (tráfico, maquinaria, viento) degradan la señal. Se mitigan mediante apilamiento (*stacking*) de disparos repetidos — el ruido incoherente decrece como $1/\sqrt{N}$ mientras la señal es coherente.

### Efectos de campo cercano

Los receptores demasiado cercanos a la fuente reciben ondas con **frentes curvos** (hipótesis de onda plana violada) y componentes de [[Body Waves|ondas de cuerpo]] significativas. El offset mínimo debe ser $L_s \geq \lambda_{max}/2$ (regla empírica de Park et al. 1999). El [[MOPA|test chi-cuadrado de MOPA]] permite detectar los receptores afectados de forma objetiva.

### [[Aliasing|Aliasing]] espacial

Un espaciado excesivamente grande $\Delta x$ produce [[Aliasing|aliasing]] espacial (ambigüedad en el [[Wavenumber|número de onda]]): las ondas de longitud $\lambda < 2\Delta x$ se presentan en el espectro f-k con velocidad aparente incorrecta. La condición anti-[[Aliasing|aliasing]] es $\Delta x \leq \lambda_{min}/2$.

> [!EXAMPLE] Evidencia empírica: Park et al. (1999) — diseño del arreglo de adquisición [[MASW Method|MASW]] en Kansas
> **Paper 001 (Park, Miller & Xia 1999)** establece los criterios de diseño del arreglo [[MASW Method|MASW]] en el estudio de campo en Kansas: 24 [[Geophone|geófono]] verticales (14 Hz de frecuencia natural), espaciado $\Delta x = 1.5$ m, apertura total $D = 34.5$ m, offset de fuente $L_s = 10$ m. El sledgehammer (10 lb sobre placa metálica) produce energía predominante en 5–50 Hz. Las reglas de diseño demostraron que: (1) el offset de fuente $L_s = 10$ m ≈ $\lambda_{max}/2$ es suficiente para excluir efectos de campo cercano en el rango de profundidades de interés (<20 m); (2) el espaciado de 1.5 m previene [[Aliasing|aliasing]] espacial hasta ~50 Hz; (3) 24 canales proporcionan resolución modal suficiente para separar el modo fundamental de los superiores entre 5–30 Hz.
>
> — Research Database, entrada 001 (core); Park, Miller & Xia (1999), *Geophysics* 64(3).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 3, pp. 77–192 — adquisición completa |
| Park, Miller & Xia (1999), *Geophysics* 64(3) | Paper 001 — diseño del arreglo [[MASW Method|MASW]] |
