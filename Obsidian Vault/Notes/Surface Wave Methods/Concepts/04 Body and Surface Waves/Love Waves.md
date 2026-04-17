---
name: Love Waves
description: [[Surface Waves|Ondas superficiales]] SH que requieren estratificación para existir; dispersivas; su [[Joint Inversion|inversión conjunta]] con Rayleigh reduce la [[Non-uniqueness|no-unicidad]] del perfil VS
type: reference
---

# Ondas de Love (Love Waves)

> [!CONCEPT] Definición
> Las **ondas de Love** son [[Surface Waves|ondas superficiales]] polarizadas horizontalmente (SH) que **requieren estratificación**: no pueden existir en un [[Elastic Half Space|semiespacio homogéneo]]. Se propagan cuando una capa superficial con menor velocidad de corte $V_{S1}$ suprayace un semiespacio más rígido ($V_{S2} > V_{S1}$), atrapando la energía SH por reflexión total interna. Sus [[Dispersion Curve|curvas de dispersión]] dependen únicamente de $V_S$ y densidades — no de $V_P$ — lo que las hace complementarias a las [[Rayleigh Waves]] en [[Joint Inversion|inversión conjunta]].
>
> — Foti et al. (2018), §2.3, pp. 63–70; Cap. 8, §8.1.

## 1. Naturaleza y movimiento de partícula

Las ondas de Love resultan de ondas [[SH-wave|SH]] guiadas en la capa superficial. El movimiento de partícula es:
- **Horizontal**, perpendicular a la dirección de propagación
- Sin componente vertical ni radial
- Requieren **receptores horizontales** ([[Geophone|geófono]] SH orientados perpendicularmente a la línea)

A diferencia de las [[Rayleigh Waves]], las Love no presentan movimiento elíptico vertical.

## 2. Condición de existencia

Para que existan ondas de Love, la [[Phase Velocity|velocidad de fase]] $c_L$ debe satisfacer:

$$V_{S1} < c_L < V_{S2}$$

Cuando se cumple esta condición, las ondas SH quedan atrapadas por reflexión total interna en la interfaz $z = H$. **No existen en un semiespacio homogéneo** — esta es la diferencia fundamental con las [[Rayleigh Waves]], que sí existen sin estratificación.

## 3. [[Dispersion Relation|relación de dispersión]]

La condición de esfuerzo nulo en $z = 0$ y la continuidad de desplazamiento y esfuerzo en $z = H$ conducen a:

$$\tan(\beta_1 H) = \frac{\mu_2 \beta_2}{\mu_1 \beta_1}$$

donde:

$$\beta_1 = \sqrt{\frac{\omega^2}{V_{S1}^2} - k^2}, \qquad \beta_2 = \sqrt{k^2 - \frac{\omega^2}{V_{S2}^2}}$$

y $\mu_1$, $\mu_2$ son los módulos de corte de la capa y del semiespacio. Esta relación contiene $\omega$ y $k$ de forma separada, confirmando la [[Wave Dispersion|dispersividad]] intrínseca. A diferencia de la ecuación secular de [[Rayleigh Waves]] en el semiespacio homogéneo, que no contiene $\omega$ ni $k$ por separado.

## 4. Modos de propagación

La [[Dispersion Relation|relación de dispersión]] admite múltiples soluciones (ver [[Surface Wave Modes]]):

- **Modo fundamental (modo 0):** existe para todas las frecuencias; a bajas frecuencias $c_L \to V_{S2}$; a altas frecuencias $c_L \to V_{S1}$
- **Modos superiores (modos 1, 2, ...):** cada uno tiene una frecuencia de corte mínima $f_c$ por debajo de la cual no se propaga

A diferencia de las [[Rayleigh Waves]], las [[Dispersion Curve|curvas de dispersión]] de Love **no presentan puntos de osculación** entre modos — son más regulares y fáciles de identificar modalmente.

## 5. Comparativa con ondas de Rayleigh

| Propiedad | Love Waves | Rayleigh Waves |
|---|---|---|
| Polarización | Horizontal (SH) | Elíptica vertical (P + SV) |
| Existencia en semiespacio homogéneo | **No** | Sí |
| Dependencia de $V_P$ | No — solo $V_S$ y densidad | Sí (indirectamente) |
| Fuente en campo | Golpe horizontal | Golpe vertical |
| Receptores | Geófonos horizontales SH | Geófonos verticales |
| Osculaciones modales | Ninguna | Pueden ocurrir |

## 6. Adquisición en campo

Para excitar Love waves:
- **Fuente horizontal:** golpear un durmiente de madera perpendicularmente a la línea de adquisición; el peso de personas sobre el durmiente aumenta la fricción con el suelo
- **Técnica de inversión de polaridad:** dos golpes en sentidos opuestos; la componente SH suma (cambia de signo) y la compresión cancela — aísla la señal SH

Resonancias SH en capas superficiales con alto contraste de velocidad:

$$f_{res} \approx \frac{V_{S,\text{top}}}{4H}$$

Aunque el espectro de una sola traza sea angosto, el análisis multicanal (f-k) permite recuperar la [[Dispersion Curve|curva de dispersión]] en un rango amplio de frecuencias.

## 7. Ventaja en [[Joint Inversion|inversión conjunta]] Love + Rayleigh

La [[Joint Inversion|inversión conjunta]] Love + Rayleigh (asumiendo isotropía) proporciona mayor constraño del perfil $V_S(z)$ que cualquiera de las dos por separado. Las curvas de Love pueden confirmar la identificación modal cuando las curvas de Rayleigh son ambiguas. Las Love son insensibles a $V_P$ — lo que elimina una fuente de error sistemático en sitios con capas saturadas donde $V_P$ es controlada por el agua poral.

> [!EXAMPLE] Evidencia empírica: Dal Moro & Ferigo (2011) — [[Joint Inversion|inversión conjunta]] Love + Rayleigh
> **Paper 045 (Dal Moro & Ferigo 2011)** aplica inversión simultánea de [[Dispersion Curve|curvas de dispersión]] de Love y Rayleigh en un sitio con fuerte contraste de velocidad. Los resultados muestran que:
> - Las curvas de Love están libres de los puntos de osculación modal que afectan las curvas de Rayleigh en el mismo sitio
> - La [[Joint Inversion|inversión conjunta]] reduce significativamente la [[Non-uniqueness|no-unicidad]] del perfil $V_S(z)$ respecto a la inversión individual de cada tipo de onda
> - El modo fundamental de Love es identificable a frecuencias donde el modo fundamental de Rayleigh resulta ambiguo por interferencia modal
>
> Este resultado valida el uso de fuentes horizontales y receptores SH como complemento a las mediciones estándar de Rayleigh en sitios problemáticos.
>
> — Research Database, entrada 045 (core).

## 8. Relaciones con otros conceptos

- [[SH-wave]] — tipo de onda que forma las Love waves
- [[Rayleigh Waves]] — contraste: Love requiere estratificación, Rayleigh no
- [[Layered Media]] — condición necesaria para que existan Love waves
- [[Elastic Half Space]] — medio donde las Love **no** existen
- [[Phase Velocity]] — observable: curva $c_L(f)$
- [[Group Velocity]] — velocidad de transporte de energía del paquete Love
- [[Wave Dispersion]] — las Love son intrínsecamente dispersivas
- [[Surface Wave Modes]] — modos fundamental y superiores de Love
- [[MASW Method]] — puede explotar Love waves con fuente horizontal

## 9. Fuentes

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.3, pp. 63–70 |
| Foti et al. (2018), Cap. 8 | §8.1 — adquisición, resonancias, ejemplo Terceira Island |
| Dal Moro & Ferigo (2011) | Paper 045 — [[Joint Inversion|inversión conjunta]] Love + Rayleigh |
