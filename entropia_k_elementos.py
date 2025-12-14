from pokemon import *
import requests 
from bs4 import BeautifulSoup
# guardar como entropia_equipo.py y ejecutar con python
import math
import numpy as np
import json

def elementary_sym_polys(weights, K):
    # devuelve e[0..K] donde e[j] es el polinomio simétrico elemental de grado j
    # e[0] = 1
    N = len(weights)
    e = np.zeros(K+1, dtype=float)
    e[0] = 1.0
    for w in weights:
        # actualizar de K..1
        for j in range(K, 0, -1):
            e[j] += w * e[j-1]
    return e  # e[j] para j=0..K

def prefix_suffix_e(weights, K):
    # Calcula e_prefix[i][0..K] = e de los primeros i elementos
    # y e_suffix[i][0..K] = e de los elementos i..N-1
    N = len(weights)
    e_pref = np.zeros((N+1, K+1), dtype=float)
    e_pref[0,0] = 1.0
    for i in range(N):
        e_pref[i+1] = e_pref[i].copy()
        for j in range(K, 0, -1):
            e_pref[i+1,j] += weights[i] * e_pref[i+1,j-1]
    e_suf = np.zeros((N+1, K+1), dtype=float)
    e_suf[N,0] = 1.0
    for i in range(N-1, -1, -1):
        e_suf[i] = e_suf[i+1].copy()
        for j in range(K, 0, -1):
            e_suf[i,j] += weights[i] * e_suf[i,j-1]
    return e_pref, e_suf

def expected_inclusions(weights, K):
    # Devuelve vector p_model tal que p_model[i] = P(i in S) bajo P(S) proporcional a prod w_i, |S|=K
    N = len(weights)
    # e_all = e_k(weights)
    e_all = elementary_sym_polys(weights, K)[K]
    if e_all == 0:
        raise ValueError("Z_k (normalizador) es 0 o underflow numérico.")
    # Para calcular e_{k-1} sobre todos menos i, usamos prefix/suffix:
    e_pref, e_suf = prefix_suffix_e(weights, K-1)  # suficiente hasta K-1
    p_model = np.zeros(N, dtype=float)
    for i in range(N):
        # e_{k-1} of weights except i = sum_{j=0..k-1} pref[i][j] * suf[i+1][k-1-j]
        e_excl = 0.0
        for j in range(0, K):
            e_excl += e_pref[i,j] * e_suf[i+1, K-1-j]
        p_model[i] = weights[i] * e_excl / e_all
    return p_model, e_all  # p_model vector y Z_k

def fit_weights_from_marginals(p_target, K, maxiter=2000, tol=1e-7, print_progress:bool = False):
    # multiplicative iterative update:
    N = len(p_target)
    # inicializar pesos pos. pequeños (evitar ceros)
    w = np.maximum(1e-6, np.array(p_target) + 1e-3)  # inicio razonable
    for it in range(maxiter):
        p_model, Zk = expected_inclusions(w, K)
        # evitar division por cero
        mask = p_model > 0
        # multiplicative update: w_i <- w_i * (p_target[i] / p_model[i])
        ratio = np.ones(N)
        ratio[mask] = p_target[mask] / p_model[mask]
        # regularizar ratios para estabilidad
        ratio = np.clip(ratio, 1e-8, 1e6)
        w *= ratio
        # normalización numérica: escalar para evitar overflow (multiplicar por const no cambia p_model)
        w /= np.mean(w)
        # comprobar convergencia (max error)
        p_model2, _ = expected_inclusions(w, K)
        err = np.max(np.abs(p_model2 - p_target))
        if it % 5000 == 0 and print_progress:
            print(f"Error maximo: {err}")
        if err < tol:
            # print("Converged iter:", it, "err:", err)
            return w
    raise RuntimeError(f"No convergió en {maxiter} iteraciones. err={err}")

def entropy_from_weights(weights, K, p_model=None):
    # H = - sum_i p_i*log w_i + log Z_k(w)
    if p_model is None:
        p_model, Zk = expected_inclusions(weights, K)
    else:
        _, Zk = expected_inclusions(weights, K)  # recomputa Zk
    # evitar log(0)
    logs = np.log(np.maximum(weights, 1e-300))
    H = - np.sum(p_model * logs) + math.log(Zk)
    return H

def get_entropy_of_k_elements(prob:list, k: int, maxiter: int ,tol: float, print_progress: bool = False) -> float:
    w = fit_weights_from_marginals(prob, k, maxiter, tol, print_progress)
    p_model, Zk = expected_inclusions(w, k)
    H_nats = entropy_from_weights(w, k, p_model=p_model)
    return H_nats


# EJEMPLO DE USO:
if __name__ == "__main__":
    with open("gen9vgc2025regh.json", "r", encoding="utf-8") as f:
        usos_cargados = json.load(f)    

    # Ejemplo: supongamos tienes N pokes con probabilidades de inclusión p_i (suman ~k)
    # Aqui p_target es la prob. de aparecer en un equipo de k=6 (ejemplo ficticio).
    p_target = np.array(list(usos_cargados.values()))
    K = 6
    # Asegúrate de que sum(p_target) is roughly K; si no, revisa tus datos.
    print("sum p_target =", p_target.sum(), "debería aproximarse a", K)

    # Ajustar pesos w:
    w = fit_weights_from_marginals(p_target, K)
    print("weights found (primeros):", w[:10])

    # Obtener p_model (debe coincidir con p_target)
    p_model, Zk = expected_inclusions(w, K)
    print("max error en marginals:", np.max(np.abs(p_model - p_target)))

    # Calcular entropía (nats). Si quieres bits, dividir por ln(2).
    H_nats = entropy_from_weights(w, K, p_model=p_model)
    H_bits = H_nats / math.log(2)
    print("Entropía H (nats):", H_nats)
    print("Entropía H (bits):", H_bits)
