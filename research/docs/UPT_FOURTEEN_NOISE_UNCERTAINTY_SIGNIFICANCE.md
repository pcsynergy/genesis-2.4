# UPT-14 — Noise, Uncertainty, and Statistical Significance

**Author:** Pablo Salvador Cardenas  
**Status:** computational research milestone; synthetic-data validation only

## Purpose

UPT-13 introduced held-out comparison between first-order memory relaxation and a zero-coupling null. UPT-14 specifies an observation model and adds uncertainty and significance procedures. It does not introduce a new physical law.

## Observation model

The latent memory coordinate follows

\[
m_{i+1}=u_i+(m_i-u_i)e^{-r\Delta t_i},\qquad r\geq0,
\]

where prescribed field mean \(u_i\) is held constant on interval \(i\). The initial value \(m_0\) is treated as known. Later observations are

\[
y_i=m_i+\epsilon_i,\qquad
\epsilon_i\overset{\rm iid}{\sim}\mathcal N(0,\sigma^2),\quad i\geq1.
\]

The noise standard deviation \(\sigma\) is declared as known input. The latent trajectory is propagated from the initial condition, not from noisy intermediate observations.

## Estimation

For fixed known \(\sigma\), maximizing Gaussian likelihood is equivalent to minimizing

\[
\operatorname{SSE}(r)=\sum_{i=1}^{n}[y_i-m_i(r)]^2,
\qquad r\in[0,r_{\max}].
\]

A bounded golden-section search is used, with explicit comparison of both boundaries and the interior candidate. The null model is \(r=0\). The likelihood-ratio statistic is

\[
T=\max\left(0,\frac{\operatorname{SSE}(0)-\operatorname{SSE}(\hat r)}{\sigma^2}\right).
\]

## Uncertainty and null calibration

1. **Rate interval:** parametric percentile bootstrap simulates observations from the fitted trajectory using declared Gaussian \(\sigma\), refits each sample, and reports percentile bounds.
2. **Significance:** because \(r=0\) is on the boundary of the allowed parameter space, UPT-14 does not rely on a naive ordinary chi-square reference. It simulates the statistic under \(r=0\), refits each null sample, and computes

\[
p=\frac{1+\#\{T_b\geq T_{\rm obs}\}}{B+1}.
\]

Seeds are explicit for reproducibility.

## Interpretation and limitations

- The interval is conditional on the model, known \(\sigma\), fixed prescribed inputs, known initial condition, independent Gaussian errors, and parametric bootstrap.
- The null p-value is calibrated only under that same stated null observation model.
- The implementation does not estimate \(\sigma\), handle correlated or heteroscedastic noise, account for uncertainty in \(u_i\), or infer an uncertain initial condition.
- Synthetic results are not empirical evidence for nonzero coupling, a new physical mechanism, or UPT as a physical theory.
- Before application to measurements, justify the noise model, input uncertainty, sampling design, parameter identifiability, and competing established models.

## Reproducibility

Run: python -m unittest discover -s research/tests -v

Run: python research/examples/upt14_uncertainty_experiment.py

The experiment uses fixed seeds and synthetic rate/noise values. Outputs demonstrate software behavior and the stated statistical procedure only.
