---
name: Seismic Cone Penetration Test
description: Ensayo geotécnico que combina la penetración estática CPT con la medición sísmica downhole — obtiene perfiles de resistencia geotécnica y VS simultáneamente en un solo sondeo
type: reference
---

# Seismic Cone Penetration Test (SCPT) — Cono de Penetración Sísmica

> [!CONCEPT] Definición
> El **Seismic Cone Penetration Test (SCPT)** es una variante del ensayo geotécnico estándar CPT (*Cone Penetration Test*) que integra receptores sísmicos (geófonos triaxiales) en el cono de penetración para medir la **velocidad de onda de corte** $V_S$ y de compresión $V_P$ en tiempo real durante el sondeo. La fuente sísmica se coloca en superficie (martillo lateral para ondas SH, cuerpo para ondas P) y se activa en diferentes posiciones de profundidad del cono — es un [[Downhole Test|ensayo downhole]] integrado en el CPT. El perfil $V_S(z)$ se obtiene del tiempo de intervalo entre dos posiciones de cono sucesivas: $V_S = \Delta z / \Delta t$ — medición directa sin necesidad de inversión. Simultáneamente, el CPT registra la resistencia de punta $q_c(z)$, el rozamiento lateral $f_s(z)$ y la presión de poros $u_2(z)$, que sirven para la clasificación geotécnica y la estimación de la estratigrafía. El SCPT es la referencia de campo más completa para la caracterización sísmica de suelos blandos por combinar propiedades de rigidez a pequeña deformación ($V_S$) con propiedades de resistencia geotécnica ($q_c$, $f_s$) en una sola operación.
>
> — Robertson & Cabal (2015), *CPT Guide*; Foti et al. (2018), §1.1; ASTM D5778.

## Principio de funcionamiento

### Equipo

- **Cono CPT estándar**: área de 10 cm² (diámetro 35.7 mm), con sensor de resistencia de punta y forro de fricción
- **Receptores sísmicos integrados**: geófonos triaxiales (uno o dos niveles) en el cuerpo del varillaje
- **Fuente sísmica en superficie**: martillo lateral (producción de ondas SH), placa de reacción en superficie

### Procedimiento sísmico

1. Avanzar el cono CPT a la profundidad $z_1$ → medir primera llegada $t_1$
2. Avanzar a $z_2 = z_1 + 1$ m → medir primera llegada $t_2$
3. Velocidad de intervalo: $V_S(z_1, z_2) = (r_2 - r_1)/(t_2 - t_1)$ donde $r_i = \sqrt{x^2 + z_i^2}$ (camino inclinado)
4. Alternativa: usar dos receptores a distancias $\Delta z$ → correlación cruzada entre señales → velocidad de intervalo sin ambigüedad de tiempo de origen

## Comparación con otros ensayos de VS

| Ensayo | Tipo | Profundidad | Pozos requeridos | Costo | Resolución vertical |
|--------|------|-------------|-----------------|-------|---------------------|
| SCPT | Invasivo (cono) | ~60 m en suelos blandos | 0 (solo penetración) | Medio | ~1 m |
| [[Downhole Test|DHT]] | Invasivo (pozo) | Depth del pozo | 1 | Medio | ~0.5 m |
| [[Cross-Hole Test|CHT]] | Invasivo (pozos) | Depth de los pozos | ≥2 | Alto | ~0.5 m |
| [[MASW Method|MASW]] | No invasivo | ~30–50 m | 0 | Bajo | λ/3–λ/2 |

## Ventajas del SCPT sobre ensayos sísmicos dedicados

1. **Integración geotécnica**: $V_S(z)$ + $q_c(z)$ + $f_s(z)$ en una sola pasada → correlaciones directas entre rigidez dinámica y resistencia estática
2. **Eficiencia**: no requiere pozo adicional — el penetrómetro avanza continuamente
3. **Aplicable en suelos blandos**: donde las perforaciones son costosas o el suelo no es autosoportante
4. **Alta repetibilidad**: la fuente superficial es controlada (golpe calibrado)

## Limitaciones

- Solo aplicable en suelos (no en roca o gravas densas donde el cono no penetra)
- La perturbación del suelo por la penetración del cono modifica localmente las condiciones de esfuerzo
- La interpretación requiere corrección por la trayectoria inclinada (fuente superficial → cono en profundidad)

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — SCPT como referencia para perfil VS en Memphis
> Foti et al. (2018, §7.3.1) presentan la comparación entre el perfil $V_S(z)$ obtenido por inversión simultánea de la [[Dispersion Curve|curva de dispersión]] y atenuación de Rayleigh (método [[MASW Method|MASW]] con [[Occam Algorithm|algoritmo de Occam]]) y el perfil de un SCPT en el sitio Mud Island, Memphis (Tennessee). El perfil [[MASW Method|MASW]] muestra $V_S$ creciente de ~90 m/s (0–3 m) a ~200 m/s (15–20 m) — concordante con los depósitos aluviales deltaicos del Mississippi. El perfil SCPT (Fig. 7.26, p. 378) reproduce la misma tendencia con diferencias < 10% en la mayoría de las capas. El SCPT confirma además la posición de la tabla de agua a ~8 m (visible como salto en $q_c$) y la presencia de capas de arena suelta en la zona 5–12 m (bajos valores de $f_s/q_c$). La integración [[MASW Method|MASW]] + SCPT permite una caracterización completa del sitio para análisis de respuesta sísmica y evaluación de licuefacción.
>
> — Foti et al. (2018), §7.3.1, pp. 376–378, Fig. 7.26.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §7.3.1 — SCPT como referencia en Memphis |
| Robertson & Cabal (2015), *CPT Guide* | Manual de referencia para CPT y SCPT |
| ASTM D5778 | Norma estándar para CPT eléctrico (incluye variante sísmica) |
