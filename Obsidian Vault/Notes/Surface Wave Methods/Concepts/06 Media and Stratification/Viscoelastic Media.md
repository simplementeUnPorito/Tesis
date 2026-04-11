---
name: Viscoelastic Media
description: Modelo constitutivo que combina comportamiento elástico y viscoso — base de la propagación de ondas con atenuación en suelos; módulos complejos y principio de correspondencia
type: reference
---

# Viscoelastic Media — Medios Viscoelásticos

> [!CONCEPT] Definición
> Un **medio viscoelástico** combina comportamiento elástico (recuperable) y viscoso (disipativo). En propagación de ondas sísmicas, los módulos de Lamé se reemplazan por **módulos complejos** dependientes de la frecuencia: $\tilde{\mu}(\omega) = \mu_R(\omega) + i\mu_I(\omega)$. Por el **principio de correspondencia elástico-viscoelástico**, todas las soluciones del problema elástico se extienden al caso disipativo con la sustitución $\lambda, \mu \to \tilde{\lambda}, \tilde{\mu}$. Esto permite extender directamente la [[Rayleigh Eigenproblem|ecuación secular de Rayleigh]] y el [[Layered Media|método de Thomson-Haskell]] a medios con atenuación. El [[Wavenumber|número de onda]] se vuelve complejo $\tilde{k} = k_R + ik_I$: $k_R$ controla la fase ([[Phase Velocity|velocidad de fase]] real) y $k_I$ controla la atenuación espacial, relacionada con el [[Shear Damping Ratio|razón de amortiguamiento]] $D_s = k_I/(2k_R) = 1/(2Q)$.
>
> — Foti et al. (2018), Cap. 2, §2.5; Lai & Rix (1998).

## Fundamento físico

En medios elásticos ideales no hay pérdida de energía durante la propagación. En medios reales (suelos, rocas), fricción interna entre partículas disipa energía como calor en cada ciclo de deformación. Los modelos viscoelásticos más usados en geofísica son:

- **Kelvin-Voigt**: esfuerzo = rigidez × deformación + viscosidad × velocidad de deformación. Adecuado para sólidos con recuperación completa.
- **Maxwell**: elemento elástico en serie con elemento viscoso. Modela fluencia (*creep*) pero no captura bien el comportamiento sísmico.
- **Sólido estándar lineal (SLS)**: combinación en paralelo que reproduce el comportamiento de geomateriales en el rango de frecuencias sísmicas — Q aproximadamente constante en décadas de frecuencia.

## Formulación matemática

### Módulos complejos

Las constantes de Lamé se reemplazan por módulos complejos:

$$\tilde{\mu}(\omega) = \mu_R(\omega) + i\,\mu_I(\omega) = \mu_R(1 + 2iD_s)$$

donde $D_s \ll 1$ (amortiguamiento débil típico en suelos: $D_s \sim 1$–$10\%$).

### Principio de correspondencia elástico-viscoelástico

Todas las soluciones del problema elástico son válidas en el viscoelástico con la sustitución $\lambda, \mu \to \tilde{\lambda}(\omega), \tilde{\mu}(\omega)$. Esto permite extender directamente la ecuación secular de Rayleigh y el método de Thomson-Haskell a medios disipativos.

### Número de onda complejo y atenuación

En un medio disipativo el número de onda es complejo:

$$\tilde{k} = k_R + i\,k_I$$

La solución armónica es:

$$u \propto e^{-k_I x}\, e^{i(k_R x - \omega t)}$$

La amplitud decae exponencialmente con la distancia $x$ a una tasa $k_I$ — la **atenuación espacial**.

### Factor de calidad y damping ratio

$$D_s = \frac{k_I}{2k_R} = \frac{1}{2Q}$$

Para suelos típicos: $D_s \sim 1$–$10\%$; $Q \sim 5$–$50$.

## Efectos de la disipación sobre la [[Phase Velocity|velocidad de fase]]

En condiciones de amortiguamiento débil ($D_s \ll 1$), la [[Phase Velocity|velocidad de fase]] es:

$$V_R(\omega) \approx V_R^{(\text{elástico})}(\omega)\left[1 + O(D_s^2)\right]$$

La corrección por disipación es de **segundo orden en $D_s$** — despreciable para estimar $V_S$. La atenuación espacial $k_I$ es de **primer orden en $D_s$** — directamente medible. Esto justifica la práctica estándar: primero invertir la [[Dispersion Curve|curva de dispersión]] para $V_S$, luego invertir la curva de atenuación para $D_s$ ([[Shear Damping Ratio]]).

## Implicaciones experimentales

Medir amplitudes con precisión para extraer el perfil de $D_s$ es más exigente instrumentalmente que medir velocidades de fase. Requiere:
- Control del acoplamiento suelo–geófono (afecta la amplitud registrada)
- Corrección de **atenuación geométrica** ($\propto 1/\sqrt{r}$ para ondas de superficie en 2D)
- Estimación o eliminación del **factor de fuente** (variaciones de acoplamiento fuente–suelo entre disparos)

> [!EXAMPLE] Evidencia empírica: Lai & Rix (1998) — inversión simultánea VS y DS desde [[Dispersion Curve|curvas de dispersión]] y atenuación
> Lai & Rix (1998) desarrollan el marco teórico completo para la inversión simultánea de la [[Dispersion Curve|curva de dispersión]] $c_R(f)$ y la curva de atenuación $\alpha_R(f)$ en medios viscoelásticos estratificados. Demuestran que la extensión del método de [[Layered Media|Thomson-Haskell]] a módulos complejos produce una ecuación secular compleja cuyas partes real e imaginaria están acopladas, de modo que la inversión simultánea es más consistente que la inversión secuencial. La relación $D_s \approx \alpha_R V_R / (2\pi f)$ es exacta al primer orden en $D_s$ y proporciona la conversión directa entre la curva de atenuación medida y el perfil $D_s(z)$. El método fue validado en el sitio de Pisa con resultados consistentes con ensayos de columna resonante (RCT).
>
> — Lai & Rix (1998), *Georgia Tech Research Report*; Foti et al. (2018), Cap. 2, §2.5; Cap. 5, §5.3.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 2, §2.5 — propagación en medios disipativos |
| Foti et al. (2018), *Surface Wave Methods* | Cap. 5, §5.3 — estimación de la curva de atenuación |
| Lai & Rix (1998), *Georgia Tech Research Report* | Marco teórico para inversión simultánea VS + DS |
