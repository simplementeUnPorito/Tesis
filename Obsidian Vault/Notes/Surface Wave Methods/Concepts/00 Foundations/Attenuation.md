### Atenuación en medios disipativos (sección 2.5)

En [[Viscoelastic Media]], la atenuación de amplitud durante la propagación se describe mediante el número de onda complejo:

$$
\tilde{k} = k_R + i\,k_I
$$

El término $k_I$ controla el decaimiento exponencial de la amplitud:

$$
u \propto e^{-k_I x}
$$

El **material damping ratio** $D$ cuantifica la fracción de energía disipada por ciclo:

$$
D = \frac{k_I}{2k_R} = \frac{1}{2Q}
$$

donde $Q$ es el factor de calidad del material.

### Distinción con atenuación geométrica

Es importante no confundir:

- **Atenuación geométrica**: decaimiento de amplitud por expansión del frente de onda ($\propto 1/\sqrt{r}$ para Rayleigh desde fuente puntual). No involucra disipación de energía.
- **Atenuación material (intrínseca)**: disipación real de energía en calor. Cuantificada por $D$ o $Q$.

Ambas contribuyen al decaimiento observado en un arreglo de geófonos. Separarlas es necesario si el objetivo es caracterizar el perfil de $D$.

### Fuente

- PDF: Sebastiano Foti Chapter 2
- Sección: 2.5 Wave propagation in dissipative media