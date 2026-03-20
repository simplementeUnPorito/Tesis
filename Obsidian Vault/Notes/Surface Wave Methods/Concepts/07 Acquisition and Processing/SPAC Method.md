# SPAC / ESAC (Spatial Autocorrelation)

> **Contexto:** Método pasivo basado en la autocorrelación espacial del campo de ondas superficiales para estimar la curva de dispersión a partir de ruido ambiental.
> **Fuente:** Foti et al. (2014), Cap. 4.5, pp. 231–235; Aki (1957, 1965); Ohori et al. (2002).

## Principio

El método **SPAC** (*Spatial Autocorrelation*) fue desarrollado por Aki (1957, 1965) para extraer la [[Dispersion Relation|curva de dispersión]] de [[Rayleigh Waves|ondas de Rayleigh]] a partir de registros de microtremores (ruido sísmico ambiental). Se basa en la relación entre la **función de autocorrelación espacial** del campo de ondas y el número de onda dominante.

La autocorrelación espacial se define como (Foti Ec. 4.28):

$$R(\chi) = E\!\left[s(\mathbf{x},t)\,s(\mathbf{x}+\chi,t)\right] = \frac{1}{2\pi}\int_{-\infty}^{\infty} S(\mathbf{k})\,e^{-i\mathbf{k}\cdot\chi}\,d\mathbf{k}$$

donde $\chi$ es el lag espacial y $E[\cdot]$ es el valor esperado. Esta expresión es la transformada inversa de Fourier del espectro de número de onda: la autocorrelación espacial codifica el contenido espectral del campo.

## Caso 1: fuente única (ondas unidireccionales)

Para una onda plana con número de onda $k_0$ y dirección conocida, la autocorrelación normalizada es (Foti Ec. 4.33):

$$\rho(\chi) = \cos(k_0 \cdot \chi)$$

La estimación experimental se realiza mediante los **espectros de potencia cruzados normalizados** entre pares de receptores (Foti Ec. 4.34):

$$\rho(\chi,\omega) = \frac{\mathfrak{Re}\!\left(\hat{S}_{ij}(\omega)\right)}{\sqrt{\hat{S}_{ii}(\omega)\,\hat{S}_{jj}(\omega)}}$$

donde $\hat{S}_{ij}$ es el espectro cruzado promediado y $\hat{S}_{ii}$, $\hat{S}_{jj}$ son los espectros de potencia individuales. Se ajusta la expresión teórica a los coeficientes experimentales por mínimos cuadrados para obtener $k_0(f)$.

Esta forma aplica a datos de **fuente activa** donde la dirección de propagación es conocida.

## Caso 2: campo isótropo (microtremores pasivos)

Para un **campo de ondas isótropo** —fuentes distribuidas uniformemente en todas las direcciones— la autocorrelación normalizada tiene simetría radial (Foti Ec. 4.40):

$$\rho(r) = J_0(k_0 r)$$

donde $J_0$ es la función de Bessel de orden cero y $r$ es la separación entre receptores. Esta es la expresión original de Aki (1957). La estimación experimental usa un receptor de referencia en el origen (Foti Ec. 4.41):

$$\rho(r,\omega) = \frac{\mathfrak{Re}\!\left(\hat{S}_{0j}(\omega)\right)}{\sqrt{\hat{S}_{00}(\omega)\,\hat{S}_{jj}(\omega)}}$$

La implementación original de Aki requería un **array circular** para realizar el promedio azimutal a radio constante $r$.

## ESAC — Extensión a geometrías arbitrarias

La versión extendida **ESAC** (*Extended Spatial Autocorrelation*, Ohori et al. 2002) elimina la restricción de geometría circular: ajusta simultáneamente la expresión teórica (Ec. 4.33 o Ec. 4.40) a **todos los pares de receptores disponibles** con cualquier separación y orientación. Esto la hace aplicable a:

- Arrays lineales (como los del método [[MASW Method|MASW]]).
- Arrays irregulares con receptores a diversas distancias.
- Combinaciones de datos activos y pasivos.

La selección entre Ec. 4.33 (unidireccional) y Ec. 4.40 (isótropa) depende del tipo de datos: activo o pasivo.

## Comparación con métodos de transformada (f-k, τ-p)

| Aspecto | SPAC/ESAC | f-k / beamformer |
|---|---|---|
| Separación de modos | No (velocidad aparente) | Sí (resolución multimodal) |
| Requisito geométrico | Array circular (SPAC) / libre (ESAC) | Array lineal o 2D |
| Hipótesis de isotropía | Necesaria (datos pasivos) | No (beamformer) |
| Estimación directa de $V_{ph}$ | Por ajuste a $J_0$ o $\cos$ | Por posición del máximo en f-k |

## Limitaciones

- **No separa modos**: SPAC/ESAC entrega una velocidad de fase **aparente** (influencia ponderada de todos los modos propagantes). No es posible resolver contribuciones modales individuales.
- **Campo cercano**: puede sesgar el coeficiente de autocorrelación del receptor de referencia en datos activos con fuente cercana.
- **Hipótesis de isotropía**: para datos pasivos, la isotropía debe verificarse (por ejemplo, mediante la simetría del espectro f-k). Si existe una dirección preferencial de ruido, los resultados pueden ser erróneos — véase [[Seismic Interferometry]] para una estrategia que permite validar esta hipótesis.

## Referencias

- Aki, K. (1957), *Bull. Earthquake Research Inst. Tokyo*.
- Ohori, M. et al. (2002), *BSSA*.
- Foti et al. (2014), Cap. 4.5, pp. 231–235, Ecs. 4.28–4.41, Figs. 4.24–4.25.
