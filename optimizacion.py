import numpy as np
from scipy.optimize import minimize

# Parámetros del problema
p = 0.7
D = 24

b1 = 10
b2 = 5
b3 = 10

# Función objetivo
def objective(h):
    h1, h2, h3 = h
    return - (p/(1 + np.exp(-h2/b2)) + (1 - p)/(1 + np.exp(-h3/b3)))/(1 + np.exp(-h1/b1))

# Restricción: h1 + h2 + h3 <= D  -->  D - (h1+h2+h3) >= 0
cons = [
    {'type': 'ineq', 'fun': lambda h: D - (h[0] + h[1] + h[2])}
]

# Restricciones de no negatividad
bounds = [(0, None), (0, None), (0, None)]

# Punto inicial
x0 = np.array([0.1, 0.1, 0.1])

result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

print("Resultado:")
print("h1 =", result.x[0])
print("h2 =", result.x[1])
print("h3 =", result.x[2])
print("Valor óptimo =", -result.fun)
print("Éxito:", result.success)
