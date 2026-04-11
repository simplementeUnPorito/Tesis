---
name: Soil Liquefaction
description: Fenómeno de pérdida de resistencia del suelo saturado ante carga sísmica cíclica — evaluado mediante VS1 normalizado usando el método de Andrus & Stokoe (2000) basado en medidas [[MASW Method|MASW]]
type: reference
---

# Soil Liquefaction — Licuefacción del Suelo

> [!CONCEPT] Definición
> La **licuefacción del suelo** (*soil liquefaction*) es el fenómeno por el cual un suelo granular saturado pierde temporalmente su resistencia de corte bajo carga sísmica cíclica. El mecanismo físico es el incremento de la presión de poros intersticial $\Delta u$ durante la carga dinámica: cuando $\Delta u$ iguala a la presión de confinamiento efectiva $\sigma'_v$, el esfuerzo efectivo cae a cero y el suelo se comporta como un fluido denso. La susceptibilidad a la licuefacción depende de la densidad relativa del suelo, el confinamiento y la historia de deformación. El parámetro sísmico relevante es la **velocidad de onda de corte normalizada**:
> $$V_{S1} = V_S \left(\frac{p_a}{\sigma'_v}\right)^{0.25}$$
> donde $p_a = 100$ kPa es la presión atmosférica de referencia. La curva de **Resistencia Cíclica** (CRR) contra $V_{S1}$ (Andrus & Stokoe 2000) permite evaluar la potencialidad de licuefacción directamente a partir de [[MASW Method|perfiles MASW]] de $V_S(z)$, sin necesidad de perforaciones — aplicación clave de los métodos de ondas superficiales en ingeniería sísmica. El método de [[MASW Method|MASW]] ofrece ventajas sobre SPT/CPT en gravas y rellenos donde la penetración es difícil (Andrus & Stokoe 2000, §6).
>
> — Andrus & Stokoe (2000), *JGGE* 126(11), 1015–1025; Foti et al. (2018), §1.2.2; Seed & Idriss (1971).

## Mecanismo de licuefacción

1. **Suelo granular saturado** (arena fina-limo) bajo confinamiento $\sigma'_v$ (esfuerzo vertical efectivo)
2. **Carga sísmica cíclica**: cada ciclo de corte produce contracción volumétrica tendencial del esqueleto
3. **Incremento de presión de poros** $\Delta u$: drenaje impedido en suelos de baja permeabilidad durante el sismo
4. **Pérdida de resistencia**: cuando $u \to \sigma_v$ (total), $\sigma'_v \to 0$ → resistencia de corte $\tau = \sigma'_v \tan\phi' \to 0$

## Evaluación por velocidad de onda de corte

El procedimiento simplificado de Andrus & Stokoe (2000) sigue la metodología de Seed-Idriss:

$$\text{FS} = \frac{\text{CRR}_{7.5}(V_{S1})}{\text{CSR}} \cdot \text{MSF}$$

donde:
- **CSR** = Cyclic Stress Ratio = $0.65 \cdot (\sigma_v/\sigma'_v) \cdot a_{\max}/g \cdot r_d$
- **CRR** = Cyclic Resistance Ratio en función de $V_{S1}$ — tabulado empíricamente
- **MSF** = Magnitude Scaling Factor para magnitudes $M_w \neq 7.5$

La base de datos de Andrus & Stokoe (2000) incluye 26 terremotos con arenas finas, limos y gravas — abarcando $V_{S1}$ entre 80 y 250 m/s.

### Ventajas del método $V_S$ sobre SPT/CPT

| Aspecto | SPT/CPT | $V_S$ ([[MASW Method|MASW]]) |
|---------|---------|-------------|
| Aplicabilidad en gravas | Limitada (daño a herramienta) | Alta |
| Perturbación del suelo | Alta | Nula |
| Resolución vertical | ~1.5 m (SPT) | ~1–3 m |
| Costo | Medio-alto | Bajo |
| Sensibilidad a cementación | Sí (sobrestima resistencia) | Sí (mismo sesgo) |

## Relación con $[[Vs30|Vs,30]]$ y normativa sísmica

El parámetro $[[Vs30|Vs,30]]$ (velocidad media en los primeros 30 m) de la normativa sísmica (NEHRP, Eurocode 8) está directamente vinculado con la susceptibilidad a la licuefacción: suelos clase D/E ($[[Vs30|Vs,30]] < 200$ m/s) son los de mayor riesgo. El [[MASW Method|MASW]] es el método estándar para determinar $[[Vs30|Vs,30]]$ de forma no invasiva (véase [[Vs30]]).

> [!EXAMPLE] Evidencia empírica: Andrus & Stokoe (2000) — base de datos VS1 vs CRR en 26 terremotos
> Andrus & Stokoe (2000, JGGE 126(11)) presentan la mayor base de datos empírica para evaluación de licuefacción por $V_S$: 225 sitios en terremotos históricos (Loma Prieta 1989, Kobe 1995, Northridge 1994, Imperial Valley 1979, entre otros). La curva CRR vs. $V_{S1}$ muestra que arenas con $V_{S1} > 215$ m/s no licuaron en ninguno de los eventos analizados (límite superior de susceptibilidad). El umbral crítico para arena limpia con FC < 5% se ubica en $V_{S1} \approx 200$ m/s para CSR = 0.30. La dispersión de la base de datos es menor que la del SPT equivalente, confirmando que $V_S$ es un indicador más robusto de la densidad intrínseca del suelo. Foti et al. (2018, §1.2.2) citan este trabajo como motivación principal del [[MASW Method|MASW]] en aplicaciones de riesgo sísmico.
>
> — Research Database, entry 061; Andrus & Stokoe (2000), *JGGE* 126(11), 1015–1025.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Andrus & Stokoe (2000), *JGGE* 126(11) | Curvas CRR vs VS1 — base de datos 26 terremotos |
| Foti et al. (2018), *Surface Wave Methods* | §1.2.2 — aplicaciones [[MASW Method|MASW]] en riesgo sísmico |
| Seed & Idriss (1971), *JSMFE* | Procedimiento simplificado de evaluación de licuefacción |
| NEHRP (2020), *FEMA P-2082* | Clasificación VS30 y amplificación sísmica |
