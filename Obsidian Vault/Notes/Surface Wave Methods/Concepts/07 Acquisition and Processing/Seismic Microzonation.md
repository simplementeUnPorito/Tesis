---
name: Seismic Microzonation
description: Zonificación espacial del riesgo sísmico local basada en el perfil VS30 y la respuesta de amplificación del sitio — aplicación principal del MASW en ingeniería sísmica urbana para clasificación normativa de suelos y mapas de peligro sísmico
type: reference
---

# Seismic Microzonation — Microzonificación Sísmica

> [!CONCEPT] Definición
> La **microzonificación sísmica** (*seismic microzonation*) es el proceso de subdivisión espacial de un área urbana o regional en zonas homogéneas de **comportamiento sísmico local**, caracterizadas por la amplificación de movimientos sísmicos, potencial de licuefacción o fallas superficiales asociadas a un sitio específico. El parámetro central es la **velocidad de onda de corte promedio en los primeros 30 m** $V_{S,30}$:
> $$V_{S,30} = \frac{30}{\displaystyle\sum_{i=1}^{n} \frac{h_i}{V_{S,i}}}$$
> donde $h_i$ y $V_{S,i}$ son el espesor y velocidad de cada capa hasta 30 m de profundidad total. Las normativas sísmicas internacionales usan $V_{S,30}$ para clasificar sitios y asignar factores de amplificación del espectro de diseño (NEHRP, Eurocode 8, ASCE 7):

> | Clase | $V_{S,30}$ (m/s) | Descripción |
> |-------|-----------------|-------------|
> | A | > 1500 | Roca dura |
> | B | 760–1500 | Roca |
> | C | 360–760 | Suelo muy denso / roca blanda |
> | D | 180–360 | Suelo rígido |
> | E | < 180 | Suelo blando |

> El [[MASW Method|MASW]] es el método de campo estándar para la determinación no invasiva de $V_{S,30}$ en microzonificación: con un arreglo de 24 geófonos a 2–3 m de espaciado, una sola línea MASW proporciona el perfil $V_S(z)$ necesario para calcular $V_{S,30}$ en 20–30 minutos de adquisición (Park et al. 1999).
>
> — Foti et al. (2018), §7.4, pp. 378–390; NEHRP (2020), *FEMA P-2082*; Eurocode 8 (EN 1998-1).

## VS,30 y amplificación sísmica

La amplificación de las ondas sísmicas en suelos blandos respecto a la roca de referencia depende de la impedancia $Z = \rho V_S$. El factor de amplificación estático de cuarto de longitud de onda:
$$F_a \approx \sqrt{\frac{Z_{roca}}{Z_{suelo}}} = \sqrt{\frac{\rho_{roca} V_{S,roca}}{\rho_{suelo} V_{S,suelo}}}$$

Para un suelo clase D ($V_{S,30} = 250$ m/s, $\rho = 1800$ kg/m³) sobre roca clase B ($V_{S,30} = 800$ m/s, $\rho = 2500$ kg/m³), el factor de amplificación aproximado es:
$$F_a \approx \sqrt{\frac{2500 \times 800}{1800 \times 250}} \approx 2.1$$

## Flujo de trabajo MASW para microzonificación

1. **Diseño del tendido**: espaciado $\Delta x = 2$–$3$ m, longitud total 46–72 m para penetración ≥ 30 m
2. **Adquisición**: 3–5 golpes de martillo por posición, stacking para mejorar S/N
3. **Procesamiento**: análisis $f$-$k$ → curva de dispersión experimental
4. **Inversión**: perfil $V_S(z)$ hasta ≥ 30 m (con regularización de Occam o LCI)
5. **Cálculo $V_{S,30}$**: integración de la columna $h_i/V_{S,i}$
6. **Mapeo**: interpolación de $V_{S,30}$ entre puntos MASW → mapa de microzonificación

El paso de inversión introduce la mayor incertidumbre: la [[Non-uniqueness|no-unicidad]] del problema inverso genera rango de $V_{S,30}$ de ±5–15% para datos típicos (Foti et al. 2018, §7.4).

## Integración con otros métodos

| Método | Ventaja en microzonificación | Limitación |
|--------|------------------------------|-----------|
| [[MASW Method|MASW]] activo | Rápido, 1D por tendido | Solo modo fundamental si array corto |
| [[MASW Method|MASW]] pasivo / ReMi | Sin fuente artificial — zonas urbanas | Requiere isotropía del ruido ambiental |
| [[Downhole Test|DHT]] | Alta precisión punto por punto | Costo de perforación |
| [[HVSR]] | Estima $f_0$ del sitio sin perfil $V_S$ | No da $V_{S,30}$ directamente |

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — MASW para microzonificación en Memphis (Tennessee)
> Foti et al. (2018, §7.4, pp. 378–390) presentan la microzonificación sísmica del área de Memphis realizada con [[MASW Method|MASW]] en 45 puntos distribuidos en una grilla de 2×2 km. El mapa de $V_{S,30}$ resultante muestra variación de 120 m/s (clase E, depósitos deltaicos del Mississippi en la zona de Mud Island) a 380 m/s (clase C, terrazas fluviales al este). Los valores MASW se validan contra 8 pozos con [[Downhole Test|ensayo downhole]] — diferencias promedio del 6.5% en $V_{S,30}$. La microzonificación clasifica el 40% del área como clase D/E (alta amplificación), coincidiendo con los daños concentrados documentados en terremotos históricos del New Madrid Seismic Zone. El costo total de la campaña MASW (45 puntos × 30 min) fue 15× menor que el equivalente con downhole — justificando MASW como herramienta primaria de microzonificación.
>
> — Foti et al. (2018), §7.4, pp. 378–390; NEHRP (2020), *FEMA P-2082*, Tabla 2.4-1.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §7.4 — MASW en microzonificación sísmica |
| NEHRP (2020), *FEMA P-2082* | Clasificación VS30 y factores de amplificación |
| Eurocode 8 (EN 1998-1:2004) | §3.1.2 — clasificación de sitios por VS30 |
| Wills & Clahan (2006), *Bull. Seism. Soc. Am.* | Metodología de mapeo VS30 para microzonificación |
| Garofalo et al. (2016) Part II, *Soil Dyn. EE* 82:241–254 | Paper 046 — InterPACIFIC: MASW vs borehole; 153 citas; VS30 comparable dentro del 6.5% |
