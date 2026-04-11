# Porous Media

> [!CONCEPT] Definición
> Los **medios porosos** son materiales sólidos con una red de poros interconectados parcial o totalmente saturados con fluido (agua, gas o mezcla). En geofísica near-surface, la mayoría de los suelos y rocas blandas son medios porosos cuya respuesta elástica depende tanto del esqueleto sólido como del fluido intersticial.
>
> La teoría de la poroelasticidad de Biot (1956) es el marco estándar para describir la propagación de ondas en estos medios.
>
> — Foti et al., *Surface Wave Methods for Near-Surface Site Characterization*, CRC Press (2018), §2.1.1; Biot (1956).

---

## 1. Fundamento físico

En un medio poroso saturado coexisten dos fases:

- **Esqueleto sólido** — aporta rigidez estructural (módulos $K_s$, $G$)
- **Fluido intersticial** — aporta incompresibilidad y viscosidad dinámica

La propagación de ondas involucra el movimiento relativo entre ambas fases. El acoplamiento fluido-esqueleto depende de la frecuencia, introduciendo **dispersión material** que no existe en un medio elástico puro.

---

## 2. Teoría de Biot (1956)

La teoría de Biot predice la existencia de **tres tipos de ondas** en un medio poroso saturado:

| Onda | Naturaleza | Atenuación |
|------|-----------|-----------|
| Onda P rápida (P1) | Movimiento en fase fluido-sólido | Baja a bajas f |
| Onda P lenta (P2 / Biot) | Movimiento en contrafase fluido-sólido | Muy alta — casi siempre difusiva |
| Onda S | Cizallamiento del esqueleto | Moderada |

La **onda P lenta** es característica exclusiva de los medios porosos. A frecuencias sísmicas (< 1 kHz) se comporta como una onda difusiva (amortiguada), prácticamente indetectable en campo.

---

## 3. Implicaciones para ondas superficiales

Las [[Rayleigh Waves]] en medios porosos presentan [[Material Dispersion]] adicional a la [[Geometric Dispersion]]:

- La [[Phase Velocity]] de Rayleigh depende de la frecuencia incluso en un semiespacio **homogéneo** poroso saturado.
- El módulo de corte del esqueleto $G$ es el parámetro más relevante para las ondas S y Rayleigh — la saturación afecta principalmente a $V_P$, no a $V_S$.
- En la práctica, para ensayos MASW a frecuencias típicas (5–100 Hz), la dispersión por poroelasticidad es secundaria respecto a la [[Geometric Dispersion]] dominante.

> [!NOTE] Relevancia práctica para la tesis
> En suelos saturados (nivel freático somero), $V_P$ puede incrementarse drásticamente (≈1500 m/s) mientras $V_S$ permanece baja. Esto afecta el coeficiente de Poisson efectivo e introduce sesgo si se asume $\nu$ constante en la inversión. Ver [[Poisson Ratio]] y [[Non-uniqueness]].

---

## 4. Parámetros clave

| Parámetro | Símbolo | Descripción |
|-----------|---------|-------------|
| Porosidad | $n$ | Fracción de volumen de poros |
| Módulo de compresibilidad del esqueleto | $K_{sk}$ | Rigidez volumétrica drenada |
| Módulo del fluido | $K_f$ | Rigidez del agua/gas intersticial |
| Módulo de Biot-Gassmann | $K_{sat}$ | Rigidez no drenada efectiva |
| Módulo de corte | $G$ | Igual en condiciones drenadas y no drenadas |

El módulo $G$ es **independiente de la saturación** — razón por la que $V_S$ es robusta para caracterización del subsuelo independientemente del nivel freático.

---

## 5. Relaciones con otros conceptos

- [[Viscoelastic Media]] — otro tipo de medio con [[Material Dispersion]]
- [[Layered Media]] — estratificación que introduce [[Geometric Dispersion]]
- [[Material Dispersion]] — mecanismo de dispersión originado en las propiedades del material
- [[Poisson Ratio]] — parámetro muy sensible a la saturación
- [[Non-uniqueness]] — la saturación agrega incertidumbre en la inversión
- [[Attenuation]] — los medios porosos son altamente disipativos para la onda P lenta

---

## 6. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1, pp. 40–41 |
| Biot, M.A. (1956). Theory of propagation of elastic waves in a fluid-saturated porous solid. *Journal of the Acoustical Society of America*, 28(2), 168–191. | — |
| Gassmann, F. (1951). Über die Elastizität poröser Medien. *Vierteljahrsschrift der Naturforschenden Gesellschaft in Zürich*, 96, 1–23. | — |
