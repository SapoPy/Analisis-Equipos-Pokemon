from pokemon import *
import requests 
from bs4 import BeautifulSoup
import numpy as np
import json
from entropia_k_elementos import *



# EJEMPLO DE USO:
if __name__ == "__main__":
    with open("usos.json", "r", encoding="utf-8") as f:
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
    H_bits = H_nats / np.log(2)
    print("Entropía H (nats):", H_nats)
    print("Entropía H (bits):", H_bits)
