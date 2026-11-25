"""Linear stability tools for finite phase-oscillator networks."""
from __future__ import annotations
from math import cos


def phase_jacobian(phases, adjacency, coupling):
    """Jacobian of the normalized sine-coupled phase interaction."""
    n = len(phases)
    if n == 0 or len(adjacency) != n or any(len(row) != n for row in adjacency):
        raise ValueError("adjacency must be square and match nonempty phases")
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(adjacency[i])
        if degree == 0:
            continue
        for j in range(n):
            if i == j or adjacency[i][j] == 0:
                continue
            value = coupling * adjacency[i][j] * cos(phases[j] - phases[i]) / degree
            out[i][j] += value
            out[i][i] -= value
    return out


def symmetric_eigenvalues(matrix, tolerance=1e-12, max_sweeps=10000):
    """Jacobi eigenvalue algorithm for real symmetric matrices (eigenvalues only)."""
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("matrix must be square")
    a = [[float(x) for x in row] for row in matrix]
    for i in range(n):
        for j in range(n):
            if abs(a[i][j] - a[j][i]) > 1e-10:
                raise ValueError("matrix must be symmetric")
    for _ in range(max_sweeps):
        p, q, largest = 0, 0, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > largest:
                    p, q, largest = i, j, abs(a[i][j])
        if largest < tolerance:
            return sorted(a[i][i] for i in range(n))
        apq = a[p][q]
        tau = (a[q][q] - a[p][p]) / (2.0 * apq)
        t = (1.0 if tau >= 0 else -1.0) / (abs(tau) + (1.0 + tau*tau)**0.5)
        c = 1.0 / (1.0 + t*t)**0.5
        s = t*c
        app, aqq = a[p][p], a[q][q]
        a[p][p] = app - t*apq
        a[q][q] = aqq + t*apq
        a[p][q] = a[q][p] = 0.0
        for k in range(n):
            if k == p or k == q:
                continue
            akp, akq = a[k][p], a[k][q]
            a[k][p] = a[p][k] = c*akp - s*akq
            a[k][q] = a[q][k] = s*akp + c*akq
    raise RuntimeError("Jacobi eigenvalue iteration did not converge")


def classify_transverse_stability(eigenvalues, zero_tolerance=1e-9):
    """Classify after excluding the neutral global-phase mode(s)."""
    nonzero = [x for x in eigenvalues if abs(x) > zero_tolerance]
    if not nonzero:
        return "neutral"
    if max(nonzero) < -zero_tolerance:
        return "linearly_asymptotically_stable"
    if max(nonzero) > zero_tolerance:
        return "linearly_unstable"
    return "marginal_or_degenerate"
