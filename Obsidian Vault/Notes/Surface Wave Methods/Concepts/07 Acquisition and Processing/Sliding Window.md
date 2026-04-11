---
name: Sliding Window
description: Técnica de análisis de un subconjunto deslizante del sismograma para generar secciones pseudo-2D de VS en [[MASW Method|MASW]] rodante — balance entre resolución lateral y resolución de la [[Dispersion Curve|curva de dispersión]]
type: reference
---

# Sliding Window — Ventana Deslizante (Rolling Array)

> [!CONCEPT] Definición
> La **ventana deslizante** (*sliding window* o *rolling array*) es la técnica que extiende el [[MASW Method|MASW]] 1D a un perfil pseudo-2D: el arreglo de geófonos se desplaza lateralmente en incrementos regulares $\Delta L$ (tipicamente $\Delta x$ o $2\Delta x$) mientras se adquiere una nueva fuente en cada posición. Para cada posición de la ventana, se extrae una [[Dispersion Curve|curva de dispersión]] y se invierte para obtener un perfil 1D $V_S(z)$; la yuxtaposición de los perfiles genera la **sección pseudo-2D de VS**. La resolución lateral es aproximadamente igual a la longitud de la ventana $D$ (apertura total del arreglo), no al incremento $\Delta L$ — cada perfil 1D representa el promedio lateral del subsuelo bajo la ventana completa. El balance fundamental: ventanas más largas (mayor $D$) tienen mejor resolución en profundidad y resolución de modos, pero menor resolución lateral; ventanas más cortas tienen mejor resolución lateral pero peor [[Dispersion Curve|curva de dispersión]].
>
> — Foti et al. (2018), Cap. 7, §7.5; Park et al. (2002), *Geophysics*.

## Implementación práctica

### Adquisición en campo

1. Desplegar el arreglo completo de $N$ geófonos con espaciado $\Delta x$ → apertura total $D = (N-1)\Delta x$
2. Mover la fuente (sledgehammer) en incrementos $\Delta L$ manteniendo el arreglo fijo → múltiples posiciones de fuente con el mismo arreglo
3. O bien: desplazar todo el arreglo más la fuente → muestreo completamente deslizante

### Procesamiento

Para cada posición de la ventana:
1. Extraer el subsismograma correspondiente
2. Aplicar análisis f-k → espectrograma de la posición
3. Identificar la cresta del modo fundamental → $c_R(f)$
4. Invertir la [[Dispersion Curve|curva de dispersión]] → $V_S(z)$
5. Asignar el perfil al punto medio de la ventana

### Inversión con restricciones laterales

Para mejorar la continuidad lateral de la sección, se puede aplicar una **inversión lateralmente restringida** (*laterally constrained inversion*, LCI): los parámetros de las ventanas adyacentes se acoplan mediante penalización de la variación lateral (minimizar $\sum_j (m_j - m_{j+1})^2$). Esto produce secciones más suaves pero puede suprimir variaciones laterales abruptas reales.

## Resolución lateral

La resolución lateral del [[MASW Method|MASW]] rolling depende de:
- **Apertura de la ventana $D$**: determina la longitud mínima de escala resolvible lateralmente → heterogeneidades más cortas que $D$ se promedian
- **Incremento de desplazamiento $\Delta L$**: determina el muestreo lateral → $\Delta L \leq D/2$ para evitar aliasing lateral (criterio de Nyquist lateral)

Una discontinuidad lateral abrupta (por ejemplo, un relleno sobre roca o una falla) aparece "suavizada" en la sección 2D con una zona de transición de ancho ~$D$.

> [!EXAMPLE] Evidencia empírica: Miller et al. (1999) — 2D [[MASW Method|MASW]] vía CMP roll-along para mapeo de bedrock
> **Paper 030 (Miller, Xia, Park & Ivanov 1999, The Leading Edge, 462 citas)** introduce el perfil 2D de VS mediante adquisición CMP roll-along: un arreglo de 48 canales (geófonos 4.5 Hz Geospace GS11D, espaciado 2 ft = 0.6 m) con sismógrafo de 60 canales Geometrics StrataView registra múltiples disparos desplazados en increments de 4 ft en el sitio contaminado de Olathe (Kansas). Para cada posición CMP se extrae una [[Dispersion Curve|curva de dispersión]] y se invierte un perfil 1D que luego se yuxtapone lateralmente para generar la sección 2D. El mapa de bedrock resultante muestra acuerdo < 1 ft con perforaciones independientes en un rango de profundidad 0.6–10.7 m. La ventaja respecto al [[MASW Method|MASW]] 1D convencional es la resolución lateral detallada, comparable a la sísmica de reflexión pero sin sus limitaciones de inversiones de velocidad. Este trabajo es el antecedente directo de la técnica de ventana deslizante moderna.
>
> — Research Database, entrada 030 (core); Miller et al. (1999), *The Leading Edge* 18(12):1402–1407.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — [[MASW Method|MASW]] rolling y ground-roll en la sección 2D de VS
> Foti et al. (2018, §7.5, Figs. 7.33–7.36) presentan el análisis de [[Ground Roll|ground-roll]] de datos de reflexión sísmica en el sitio La Salle mediante ventana deslizante: el sismograma de reflexión (kilométrico) se divide en ventanas de $\sim$50 m de longitud con incrementos de 5 m. Para cada ventana se extrae una [[Dispersion Curve|curva de dispersión]] y se invierte con inversión lateralmente restringida. La sección pseudo-2D de $V_S$ resultante (Fig. 7.35) muestra variaciones laterales suaves entre 200–400 m/s en los primeros 30 m, con mayor detalle en las heterogeneidades laterales respecto a una sección de inversión 1D sin restricciones. La superposición con la sección de reflexión (Fig. 7.36) confirma que las variaciones de $V_S$ correlacionan con las unidades estratigráficas visibles en los reflectores.
>
> — Foti et al. (2018), §7.5, pp. 384–392, Figs. 7.33–7.36.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 7, §7.5, pp. 384–392 — [[MASW Method|MASW]] rolling y secciones 2D |
| Miller et al. (1999), *The Leading Edge* 18(12):1402–1407 | Paper 030 — 2D [[MASW Method|MASW]] CMP roll-along; mapeo bedrock Olathe Kansas; 462 citas |
| Xia et al. (2004), SEG Expanded Abstracts | Paper 011 — inversión generalizada 2D para mejorar resolución horizontal sin cambio de hardware |
| Park et al. (2002), *Geophysics* | Extensión del [[MASW Method|MASW]] a perfiles 2D mediante arreglo deslizante |
| Hayashi & Suzuki (2004), *Exploration Geophysics* 35:7–13 | Paper 040 — CMP cross-correlation para perfiles 2D de alta resolución; procesamiento en 4 pasos |
