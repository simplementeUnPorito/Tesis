# Interferometría Sísmica Pasiva (Seismic Interferometry)

> **Contexto:** Técnica pasiva para recuperar la función de Green entre receptores mediante la cross-correlación de registros de ruido ambiental.
> **Fuente:** Foti et al. (2014), Cap. 8.4, pp. 427–430; Wapenaar et al. (2010); Shapiro y Campillo (2004).

## Principio

La **interferometría sísmica** designa el proceso de generar trazas sísmicas desde fuentes virtuales mediante la **cross-correlación** (o convolución) de observaciones en diferentes receptores. Estudios teóricos demostraron que el campo difuso de ruido ambiental puede transformarse en una respuesta de impulso sísmica determinista —la **función de Green** entre receptores— mediante este procedimiento (Weaver y Lobkis 2001, 2002; Snieder 2004; Wapenaar 2004).

En sismología global, la componente de onda superficial de la función de Green entre dos receptores puede recuperarse de la cross-correlación de sus registros de ruido (Campillo y Paul 2003; Shapiro y Campillo 2004). El mismo principio fue posteriormente validado en el rango de frecuencias de ingeniería sísmica (1–100 Hz).

## Procedimiento

1. **Cross-correlación por fuente**: considérense dos receptores $R_1$ y $R_2$ que observan señales de ondas superficiales provenientes de fuentes $S_j$ distribuidas alrededor del array. Para cada fuente se cross-correlacionan las señales $T(S_j, R_1)$ y $T(S_j, R_2)$, produciendo una traza correlacionada $T_{12}(S_j)$. La correlación depende de la posición relativa de la fuente y de las propiedades del subsuelo entre los receptores (Fig. 8.28, p. 427).

2. **Correlogram gather**: las trazas correlacionadas para todas las fuentes se ordenan según el **azimut de la fuente**, formando un gather análogo al shot gather en sísmica activa (Fig. 8.29, p. 428). Este gather es regular y suave a pesar de las diferentes distancias de las fuentes, porque la cross-correlación cancela los efectos de trayectoria desde la fuente hasta los receptores.

3. **Suma sobre fuentes**: al sumar las trazas correlacionadas, las contribuciones de fuentes en posiciones opuestas entre sí se anulan. Solo las fuentes en los **puntos estacionarios** —casi alineadas con los dos receptores— contribuyen constructivamente. El resultado es una traza causal/anticausal equivalente a la respuesta de impulso entre $R_1$ y $R_2$: se puede interpretar como si $R_1$ fuera una **fuente virtual** registrada en $R_2$.

## Aplicación en ondas superficiales

Las señales extraídas pueden procesarse exactamente como datos activos virtuales. La aplicación principal es la **recuperación de la velocidad de fase de ondas superficiales** a partir de ruido ambiental (Shapiro y Campillo 2004). La mayoría de los estudios actuales usa arrays 2D dispersos para obtener una **distribución tomográfica** de las velocidades de ondas superficiales.

En arrays lineales, el interferograma permite usar un receptor de referencia como fuente virtual, generando un shot gather que se procesa con análisis [[MASW Method|f-k]] estándar.

## Interferograma vs. [[ReMi Method|ReMi]]

El método [[ReMi Method|ReMi]] (*Refraction Microtremor*) procesa directamente los registros de ruido en el dominio f-k, asumiendo que el mínimo de la curva de slowness corresponde a la dispersión real. La interferometría sísmica ofrece ventajas prácticas respecto a ReMi:

- En un campo de ondas **no isotrópico**, ReMi puede llevar a velocidades **sobreestimadas** porque el análisis utiliza la velocidad aparente. El interferograma, al cancelar las contribuciones de direcciones opuestas, extrae el número de onda verdadero (Fig. 8.31, p. 429).
- El espectro f-k del interferograma muestra los máximos **exactamente sobre el número de onda teórico verdadero** (Fig. 8.30, p. 429), mientras que el espectro ReMi del mismo dataset sintético muestra los máximos sobre el número de onda aparente.
- La hipótesis de campo difuso isotrópico puede **validarse con el interferograma**: si existe una fuente dominante a distancia limitada, el interferograma muestra eventos no lineales que advierten sobre la invalidez de los resultados (Fig. 8.32, p. 430). ReMi no ofrece este diagnóstico directo.

## Hipótesis fundamentales

- **Campo difuso**: el ruido ambiental debe ser estadísticamente isótropo (fuentes distribuidas en todas las direcciones con energía similar). Esta condición se degrada en entornos urbanos con fuentes direccionales dominantes.
- **Ondas superficiales dominantes**: la mayor parte de la energía del ruido ambiental en frecuencias de ingeniería corresponde a ondas superficiales (ondas de [[Rayleigh Waves|Rayleigh]] y [[Love Waves|Love]]).
- **Medio homogéneo lateral**: el subsuelo entre los receptores se aproxima como un modelo 1D; variaciones laterales fuertes violan la hipótesis.

## Relación con SPAC/ESAC

La interferometría sísmica y la [[Dispersion Relation|autocorrelación espacial]] (SPAC/ESAC, Aki 1957) comparten la misma base física: ambas explotan la coherencia espacial del campo de ruido para estimar la velocidad de fase. La interferometría trabaja en el dominio temporal (función de Green) mientras que SPAC/ESAC trabaja en el dominio frecuencial (coherencia espacial). En la práctica, el método ESAC puede verse como una implementación en frecuencia del mismo principio interferométrico.

## Limitaciones

- Requiere registros largos (minutos a horas) para acumular suficiente estadística del campo difuso.
- La recuperación correcta de la función de Green requiere distribución casi uniforme de fuentes alrededor del array.
- La contaminación por fuentes transitorias fuertes (tráfico, maquinaria) degrada el resultado; se requiere selección de ventanas o robustización estadística.
- Los modos superiores de ondas superficiales son más difíciles de aislar que con métodos activos.

## Referencias

- Shapiro, N.M., Campillo, M. (2004), *GRL*.
- Wapenaar, K. et al. (2010a), *Geophysics*.
- Foti et al. (2014), Cap. 8.4, pp. 427–430.
