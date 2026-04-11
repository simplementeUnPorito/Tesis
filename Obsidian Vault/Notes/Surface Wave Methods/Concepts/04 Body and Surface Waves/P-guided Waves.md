---
name: P-guided Waves
description: Modos fugantes (leaky modes) de alta [[Phase Velocity|velocidad de fase]] en el sistema agua-sedimentos; sensibles a VP del subfondo; complementarios a ondas de Scholte en caracterización marina
type: reference
---

# Ondas Guiadas de Tipo P (P-guided Waves)

> [!CONCEPT] Definición
> Las **ondas guiadas de tipo P** son **modos fugantes** (*leaky modes*) de la ecuación de dispersión del sistema agua-sedimentos: raíces complejas cuya [[Phase Velocity|velocidad de fase]] supera $V_{P,\text{agua}} \approx 1500$ m/s. Físicamente son ondas P multi-reflejadas en la capa de agua, con energía parcialmente atrapada y parcialmente radiada al subsuelo. Son sensibles a $V_P$ del subfondo — complementarias a las [[Scholte Waves|ondas de Scholte]] (sensibles a $V_S$) — y en la inversión conjunta permiten caracterizar completamente el subsuelo marino.
>
> — Foti et al. (2018), Cap. 8, §§8.2.2–8.2.3, pp. 403–412.

## Definición

Las **ondas guiadas de tipo P** (*P-guided waves*) son modos de propagación que existen en el sistema agua-sedimentos. Corresponden a los **modos fugantes** (*leaky modes*) de la ecuación de dispersión: raíces complejas cuya parte real de la [[Phase Velocity|velocidad de fase]] supera la velocidad compresional del agua (~1500 m/s). Físicamente son **ondas P multireflejadas** en la capa de agua (entre la superficie libre del agua y el fondo marino), con energía parcialmente atrapada y parcialmente radiada hacia el subsuelo.

En oceanografía acústica se denominan ondas ULF (*ultra-low frequency*), típicamente en el rango 1–100 Hz en plataformas continentales. En aguas muy someras (ensayos near-shore), el rango se desplaza hacia valores más altos.

## Diferencia con ondas de Scholte

| Característica | [[Scholte Waves|Ondas de Scholte]] | Ondas guiadas P |
|---|---|---|
| Tipo de modo | Modo real (propagante) | Modo fugante (leaky) |
| Velocidad de fase | < Vp_agua | > Vp_agua |
| Parámetro sensoriado | Vs del sedimento | Vp del sedimento y del agua |
| Frecuencia de corte | Sin corte (modo fund.) | Depende de la geometría |
| Visibilidad en registro | Baja velocidad, llegan tarde | Alta velocidad, llegan primero |
| Aplicación | Perfil Vs marino | Perfil Vp marino |

## Condición de existencia y aproximación acústica

Las ondas guiadas P existen cuando la capa de agua puede funcionar como guía acústica, es decir, cuando la velocidad compresional del sedimento supera la del agua. La **aproximación acústica** (tratar el sedimento como un fluido con Vs = 0) es válida cuando el ratio de Poisson es alto, como ocurre en sedimentos saturados blandos (Vs << Vp). Esta aproximación simplifica el modelado directo.

## Información a priori necesaria

Para modelar e invertir ondas guiadas P se necesita:
- **Velocidad del agua:** medible con un sensor de temperatura/salinidad, o asumida ≈ 1500 m/s.
- **Velocidad compresional del subfondo:** estimable del tiempo de llegada del primer arribo en el registro.

## Inversión conjunta con ondas de Scholte

Si se adquieren simultáneamente [[Scholte Waves|ondas de Scholte]] (sensibles a Vs) y ondas guiadas P (sensibles a Vp), la **inversión conjunta** permite estimar ambos perfiles acoplando los modelos geométricos (espesores de capa compartidos). Esta combinación hace posible la caracterización completa del subsuelo marino con un único dataset.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — inversión conjunta ondas de Scholte + guiadas P
> Foti et al. (2018, §8.2.3) presentan un caso de inversión conjunta de ondas de Scholte (sensibles a $V_S$) y ondas guiadas P (sensibles a $V_P$) en un sitio de plataforma continental. La inversión conjunta, con espesores de capa compartidos entre ambos tipos de datos, permite estimar el perfil completo $V_P(z)$, $V_S(z)$ con mayor constraño que cualquiera de los dos tipos por separado. Los datos de ondas guiadas P aportan información sobre la compresibilidad del sedimento y ayudan a fijar el nivel freático efectivo del subsuelo marino.
>
> — Foti et al. (2018), Cap. 8, §8.2.3, pp. 408–412.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 8, §§8.2.2–8.2.3, pp. 403–412 |
