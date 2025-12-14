import numpy as np
import math
import json
import time
from collections import Counter
from main import * 

def sample_team_indices_from_w(weights, k):
    w = np.maximum(weights, 1e-300)
    U = np.random.random(len(w))
    E = -np.log(U) / w
    idx = np.argpartition(E, k)[:k]
    return tuple(sorted(idx.tolist()))

def empirical_entropy_from_samples(counter, M):
    H = 0.0
    for count in counter.values():
        p = count / M
        H -= p * math.log(p)
    return H


if __name__ == "__main__":
    t_total_start = time.perf_counter()

    # Cargar probabilidades marginales
    t_load = time.perf_counter()
    with open("usos.json", "r", encoding="utf-8") as f:
        usos = json.load(f)
    print(f"Tiempo carga JSON: {time.perf_counter() - t_load:.3f} s")

    names = list(usos.keys())
    p_target = np.array([usos[n] for n in names], dtype=float)
    K = 6

    # Ajuste de pesos
    t_weights = time.perf_counter()
    try:
        w = np.load("weights_w.npy").astype(float)
        print("Pesos w cargados desde archivo.")
    except Exception:
        print("Ajustando pesos w desde marginales (esto puede tardar)...")
        w = fit_weights_from_marginals(p_target, K)
        np.save("weights_w.npy", w)
    print(f"Tiempo ajuste/carga de pesos: {time.perf_counter() - t_weights:.3f} s")

    # Verificar marginals modeladas
    p_model, Zk = expected_inclusions(w, K)
    print("Error max entre p_target y p_model:", np.max(np.abs(p_model - p_target)))

    # Entropía teórica
    t_entropy = time.perf_counter()
    H_model_nats = entropy_from_weights(w, K, p_model=p_model)
    print(f"Tiempo cálculo entropía modelo: {time.perf_counter() - t_entropy:.3f} s")
    print("Entropía teórica [nats]:", H_model_nats, " [bits]:", H_model_nats / math.log(2))

    # --- Muestreo Monte Carlo ---
    M = int(8000000)
    counter = Counter()
    batch = 200000

    t_mc = time.perf_counter()
    print("Iniciando muestreo Monte Carlo...")

    for i in range(0, M, batch):
        b = min(batch, M - i)
        for _ in range(b):
            team = sample_team_indices_from_w(w, K)
            counter[team] += 1

        if (i // batch) % 10 == 0:
            print(f"Progress: {(i+b)/M * 100:.2f} %")

    print(f"Tiempo muestreo Monte Carlo: {time.perf_counter() - t_mc:.3f} s")

    # Entropía empírica
    t_emp = time.perf_counter()
    H_emp_nats = empirical_entropy_from_samples(counter, M)
    print(f"Tiempo cálculo entropía empírica: {time.perf_counter() - t_emp:.3f} s")

    H_emp_bits = H_emp_nats / math.log(2)
    print("Entropía empírica [nats]:", H_emp_nats, " [bits]:", H_emp_bits)

    print("Diferencia (emp - modelo) [nats]:", H_emp_nats - H_model_nats)
    print("Número de equipos distintos observados:", len(counter))

    # Top equipos
    topk = 1000
    print("Top equipos observados (frecuencia, equipos):")
    for team, cnt in counter.most_common(topk):
        names_team = [names[idx] for idx in team]
        print(f"{cnt}/{M} = {cnt/M:.6f}  {names_team}")

    # Tiempo total
    print(f"Tiempo TOTAL del programa: {time.perf_counter() - t_total_start:.3f} s")
