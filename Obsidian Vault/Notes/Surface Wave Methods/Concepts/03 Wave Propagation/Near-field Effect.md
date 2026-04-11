---
name: Near-field Effect
description: Región cercana a la fuente donde las Rayleigh waves no se comportan como ondas planas y la velocidad aparente es distorsionada por contribuciones de ondas de cuerpo.
type: concept
---

# Near-field Effect

> [!CONCEPT] Definición
> El **near-field effect** es la distorsión de la [[Phase Velocity]] aparente de las [[Rayleigh Waves]] que ocurre en la zona cercana a la fuente, donde las [[Body Waves]] ([[P-waves]], [[S-Waves]]) tienen amplitud comparable a las [[Surface Waves|ondas superficiales]]. Solo a distancias suficientemente grandes (*far-field*) las [[Rayleigh Waves]] dominan y la velocidad aparente converge a la verdadera velocidad de Rayleigh del modo fundamental.
>
> — Foti et al., *Surface Wave Methods*, §2.4.2, pp. 83–86; §3.4.1.6, pp. 160–162.

---

## 1. Intuición física

Una fuente puntual en superficie genera simultáneamente [[Body Waves]] y [[Surface Waves|ondas superficiales]]. La diferencia clave está en cómo decae la amplitud con la distancia $r$:

| Tipo de onda | Decaimiento en superficie |
|---|---|
| [[Body Waves]] ([[P-waves]], [[S-Waves]]) | $\propto r^{-2}$ (rápido) |
| [[Rayleigh Waves]] | $\propto r^{-0.5}$ (lento) |

En el campo cercano, las [[Body Waves]] son comparables o dominantes → la velocidad aparente medida **no corresponde** a $c_R$ del modo fundamental. A distancias mayores, el campo queda dominado por [[Rayleigh Waves]] y la aproximación de onda plana es válida.

Este fenómeno fue estudiado originalmente en el contexto del [[Lamb's Problem]]: la solución exacta incluye ondas de cuerpo y superficiales; el campo lejano retiene solo las superficiales.

---

## 2. Criterio cuantitativo

El umbral entre campo cercano y campo lejano depende de la [[Wavelength|longitud de onda de Rayleigh]] $\lambda_R$:

| Condición del sitio | Offset mínimo recomendado |
|---|---|
| Medio normalmente dispersivo | $r \gtrsim \lambda_R / 2$ (Stokoe et al. 1994) |
| Medio inversamente dispersivo | $r \gtrsim \lambda_R$ a $2\lambda_R$ |

Como $\lambda_R$ depende de la frecuencia y de $V_S$ (desconocida a priori), el criterio es **frecuencia-dependiente**: para frecuencias bajas (longitudes de onda largas), el campo cercano se extiende más lejos — imponiendo offsets de fuente mayores que reducen el SNR.

---

## 3. Consecuencia para la medición

Dentro del campo cercano, la [[Phase Velocity|velocidad de fase]] aparente puede estar sesgada hacia arriba o abajo según la frecuencia y la estratigrafía. Esto contamina la [[Dispersion Curve|curva de dispersión]] experimental y puede inducir errores sistemáticos en la inversión del perfil Vs(z).

> [!EXAMPLE] Evidencia empírica: Yoon & Rix (2009) — cuantificación del near-field en [[MASW Method|MASW]] activo
> **Paper 024 (Yoon & Rix 2009)** cuantifica mediante modelado numérico y datos de campo el sesgo introducido por el near-field en [[MASW Method|MASW]]. Sus resultados muestran que el error en la [[Dispersion Curve|curva de dispersión]] puede superar el 10–15% en frecuencias bajas cuando el offset fuente-receptor es insuficiente.
>
> El criterio operacional derivado: excluir del análisis los receptores para los cuales $r < \lambda_R/2$ a cada frecuencia. Esto puede implementarse como un *mute* frecuencia-dependiente en el dominio f-k.
>
> — Fuente: Research Database, entrada 024 (core). Ver también Paper 026 (Park, Miller & Miura 2002) para parámetros óptimos de adquisición.

---

## 4. Implicaciones para el diseño experimental

- El **primer [[Geophone|geófono]]** debe ubicarse al menos a $\lambda_R/2$ de la fuente, idealmente a $\lambda_R$.
- Para frecuencias bajas esto impone offsets largos, que a su vez reducen el SNR → tradeoff fundamental del diseño [[MASW Method|MASW]].
- Algunas técnicas de procesamiento permiten identificar y enmudecer (*mute*) los receptores afectados por campo cercano a cada frecuencia (Foti §4.4).
- En arreglos pasivos ([[ReMi Method]], [[SPAC Method]]), el near-field es menos crítico porque no hay fuente controlada.

---

## 5. Relaciones con otros conceptos

- [[Rayleigh Waves]] — ondas cuya velocidad se distorsiona en el near-field
- [[Body Waves]] — origen de la interferencia en campo cercano
- [[Lamb's Problem]] — solución teórica exacta que incluye near-field
- [[Phase Velocity]] — observable contaminado en campo cercano
- [[Wavelength]] — $\lambda_R$ define la escala del near-field
- [[MASW Method]] — método más afectado por near-field activo
- [[Near-field Effect]] ↔ [[Geometric Dispersion]] — ambos afectan la [[Dispersion Curve|curva de dispersión]] experimental

---

## 6. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.4.2, pp. 83–86 |
| Foti et al. (2018), *Surface Wave Methods* | §3.4.1.6, pp. 160–162 |
| Yoon & Rix (2009), *J. Geotech. Geoenviron. Eng.* | Paper 024 — near-field en [[MASW Method|MASW]] activo |
| Park, Miller & Miura (2002) | Paper 026 — parámetros óptimos de adquisición |
