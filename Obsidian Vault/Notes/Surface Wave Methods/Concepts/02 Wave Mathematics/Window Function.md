---
name: Window Function
description: Función de ponderación temporal o espacial aplicada a señales antes de la DFT para reducir el spectral leakage — familia de ventanas (rectangular, Hann, Hamming, Tukey, Blackman) con diferentes compromisos entre resolución frecuencial y supresión de lóbulos laterales
type: reference
---

# Window Function — Función de Ventana

> [!CONCEPT] Definición
> Una **función de ventana** $w(t)$ es una función no negativa que multiplica una señal $s(t)$ antes de calcular su DFT, con el objetivo de reducir el **[[Spectral Leakage|spectral leakage]]** causado por el truncamiento de señales no periódicas en un intervalo finito:
> $$s_w(t) = s(t) \cdot w(t), \qquad S_w(f) = S(f) * W(f)$$
> donde $W(f)$ es la transformada de Fourier de la ventana. El diseño de una función de ventana implica el **compromiso fundamental** entre:
> - **Lóbulo principal** (*main lobe*): ancho $\Delta f_{\text{ML}}$ — determina la resolución espectral; un lóbulo más estrecho da mejor resolución
> - **Lóbulos laterales** (*side lobes*): nivel en dB — determinan la contaminación por [[Spectral Leakage|fuga espectral]]; lóbulos más bajos dan menor contaminación
> Matemáticamente, ambos objetivos son incompatibles: reducir los lóbulos laterales requiere ensanchar el lóbulo principal. En [[MASW Method|MASW]], las ventanas se aplican tanto en el dominio temporal (a cada traza) como en el dominio espacial (sobre el arreglo de [[Geophone|geófono]]) antes de la transformada $f$-$k$, controlando la calidad del panel espectral para la extracción de la [[Dispersion Curve|curva de dispersión]].
>
> — Foti et al. (2018), §3.3.5, pp. 135–138; Harris (1978), *Proc. IEEE* 66(1), 51–83.

## Ventanas estándar

| Ventana | $w(t)$ en $[0, T]$ | Ancho ML | Lóbulos lat. | Uso en [[MASW Method|MASW]] |
|---------|-------------------|----------|--------------|-------------|
| Rectangular | $1$ | $2/T$ | -13 dB | Referencia; alias si señal no periódica |
| Hann (Hanning) | $\frac{1}{2}(1 - \cos(2\pi t/T))$ | $4/T$ | -31.5 dB | Estándar en sísmica superficial |
| [[Hamming Window|Hamming]] | $0.54 - 0.46\cos(2\pi t/T)$ | $4/T$ | -42.5 dB | Mayor supresión a costa de lóbulo más alto |
| Blackman | $0.42 - 0.5\cos(2\pi t/T) + 0.08\cos(4\pi t/T)$ | $6/T$ | -58 dB | Máxima supresión; pérdida de resolución |
| Tukey ($\alpha=0.5$) | Coseno en los extremos; 1 en el centro | $\approx 3/T$ | -25 dB | Compromiso Hann-rectangular |
| Kaiser ($\beta=8$) | Función de Bessel modificada $I_0$ | Variable | Variable | Diseño paramétrico óptimo |

La **ventana de Hann** (coseno elevado con ceros en los extremos) es la más usada en [[MASW Method|MASW]] por su balance apropiado: reduce los lóbulos laterales de -13 dB (rectangular) a -31.5 dB con solo 2× pérdida de resolución.

## Ventaneo 2D en el análisis f-k

En [[MASW Method|MASW]], la sección de sismogramas $u(x, t)$ se ventanea en ambas dimensiones:
$$u_w(x, t) = u(x, t) \cdot w_x(x) \cdot w_t(t)$$

El panel $f$-$k$ resultante: $U_w(f, k) = U(f,k) * W_x(k) * W_t(f)$ — la resolución en $k$ está controlada por $w_x$ (apertura del arreglo) y en $f$ por $w_t$ (longitud del registro).

## Ventana [[Hann Window|Hann]] y [[Hamming Window|Hamming]]: diferencia práctica

La diferencia entre Hann y Hamming es el coeficiente de offset:
- **Hann**: coeficientes $(0.5, 0.5)$ → los extremos llegan a cero → continuidad $C^0$ en los bordes → lóbulos caen como $1/f^3$
- **Hamming**: coeficientes $(0.54, 0.46)$ → los extremos no llegan a cero → discontinuidad → lóbulos caen como $1/f$ pero el primer lóbulo lateral es más bajo

En sísmica de [[Surface Waves|ondas superficiales]] se prefiere Hann porque la continuidad en los extremos evita discontinuidades artificiales que se propagarían al panel $f$-$k$.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — comparación ventanas en [[MASW Method|MASW]] sitio Pisa
> Foti et al. (2018, §3.3.5) presentan la comparación del panel $f$-$k$ del sitio Pisa con ventanas rectangular, Hann y Tukey ($\alpha = 0.5$). Con ventana rectangular: modo fundamental dominante a 10 Hz con lóbulos laterales a -13 dB que contaminan la región del primer modo superior (12 Hz). Con ventana Hann: lóbulos laterales a -31.5 dB — el primer modo superior emerge como cresta separada en $k$, identificable para inversión multimodal. Con ventana Tukey: resultado intermedio (-25 dB de lóbulos), con mejor resolución que Hann al precio de mayor contaminación. Foti concluye que la ventana Hann es la opción por defecto para análisis [[MASW Method|MASW]] estándar; Tukey es preferida cuando se requiere mayor resolución para separar modos próximos en frecuencia.
>
> — Foti et al. (2018), §3.3.5, pp. 135–138; Harris (1978), *Proc. IEEE* 66(1), 51–83.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §3.3.5 — ventaneo en análisis [[MASW Method|MASW]] |
| Harris, F.J. (1978), *Proc. IEEE* 66(1), 51–83 | Referencia fundamental de ventanas de análisis |
| Nuttall, A.H. (1981), *Proc. IEEE* 69(4) | Ventanas de mínimos cuadrados óptimas |
