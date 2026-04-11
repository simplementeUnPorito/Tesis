---
name: Wyllie Equation
description: Ecuación de tiempo de tránsito promedio 1/VP = φ/Vf + (1-φ)/Vm que relaciona la velocidad VP con la porosidad — usada con la Ley de Archie para acoplar modelos ERT y MASW en inversión conjunta petrofísica
type: reference
---

# Wyllie Equation — Ecuación de Wyllie (Time-Average Equation)

> [!CONCEPT] Definición
> La **ecuación de Wyllie** (o ecuación de tiempo-promedio, *time-average equation*) es la relación empírica que predice la velocidad de onda P $V_P$ de una roca o suelo saturado en función de la porosidad $\phi$:
> $$\frac{1}{V_P} = \frac{\phi}{V_f} + \frac{1-\phi}{V_m}$$
> donde $V_f$ es la velocidad del fluido intersticial (agua: ~1500 m/s) y $V_m$ es la velocidad de la matriz sólida mineral (cuarzo: ~6000 m/s, calcita: ~6600 m/s). La ecuación se interpreta como un modelo de **capas en serie**: el tiempo de tránsito total es la suma del tiempo en el fluido y el tiempo en la matriz, ponderados por sus fracciones volumétricas. Combinada con la [[Archie's Law|Ley de Archie]], la ecuación de Wyllie proporciona el vínculo petrofísico entre resistividad eléctrica y velocidad sísmica:
> $$\phi = \left(\frac{a\rho_w}{\rho_t}\right)^{1/m} \xrightarrow{\text{Wyllie}} V_P(\phi) = \left[\frac{\phi}{V_f} + \frac{1-\phi}{V_m}\right]^{-1}$$
> Esta cadena permite la **inversión conjunta petrofísica**: los datos MASW ($V_S$, y $V_P$ por [[Seismic Refraction|refracción]]) y ERT ($\rho_t$) comparten el parámetro $\phi$ como variable latente. La limitación principal es que Wyllie subestima $V_P$ para rocas consolidadas y sobreestima para suelos poco compactados — en geotecnia superficial su uso es aproximado.
>
> — Wyllie et al. (1956), *Geophysics* 21(1), 41–70; Foti et al. (2018), §8.6.1; Mavko et al. (2009), *The Rock Physics Handbook*.

## Comparación Wyllie vs. Biot-Gassmann

Para suelos saturados, la [[Biot Theory|ecuación de Gassmann]] es más rigurosa que la ecuación de Wyllie:

| Modelo | Expresión | Validez |
|--------|-----------|---------|
| Wyllie | $1/V_P = \phi/V_f + (1-\phi)/V_m$ | Roca compacta; aproximación lineal |
| Biot-Gassmann | $V_P = \sqrt{(K_{sat} + 4G/3)/\rho}$ | General, incluyendo suelos blandos |
| Empirical | $V_P = f(\phi, \text{tipo de suelo})$ | Correlaciones locales |

Para $V_S$ (módulo de corte), Wyllie no aplica directamente ya que $G_{fluido} = 0$. La relación $V_S$-porosidad es empírica: $V_S \approx (1-\phi)^n V_{S,mineral}$ con $n \approx 1.5$–2 para arenas.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — Wyllie para conversión VP-porosidad en sitio fluvial
> Foti et al. (2018, §8.6.1) usan la ecuación de Wyllie con $V_f = 1480$ m/s (agua a 15°C) y $V_m = 5800$ m/s (cuarzo impuro con arcilla) para convertir el perfil $V_P$ del sitio La Salle (obtenido por [[Seismic Refraction|refracción sísmica]]) en un perfil de porosidad $\phi(z)$. Para la zona saturada ($V_P \approx 1500$–1700 m/s, 4–20 m), Wyllie predice $\phi \approx 0.38$–0.45 — ligeramente sobreestimado respecto al valor de laboratorio en testigos ($\phi_{lab} = 0.33$–0.40). La discrepancia (8%) se atribuye a que en suelos blandos la ecuación de Wyllie no captura correctamente el acoplamiento fluido-esqueleto de [[Biot Theory|Biot]]. No obstante, el perfil de $\phi$ es suficientemente preciso para la conversión cualitativa ERT→MASW requerida en la inversión conjunta.
>
> — Foti et al. (2018), §8.6.1; Wyllie et al. (1956), *Geophysics* 21(1), 41–70.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Wyllie, Gregory & Gardner (1956), *Geophysics* 21(1), 41–70 | Ecuación de tiempo-promedio original |
| Foti et al. (2018), *Surface Wave Methods* | §8.6.1 — petrofísica en inversión conjunta |
| Mavko, Mukerji & Dvorkin (2009), *The Rock Physics Handbook* | §6 — modelos de velocidad-porosidad |
