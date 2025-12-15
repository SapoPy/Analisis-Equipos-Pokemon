from pokemon import *
import requests 
from bs4 import BeautifulSoup
import numpy as np
import json
from entropia_k_elementos import *

if __name__ == "__main__":
    with open("gen9vgc2025regh.json", "r", encoding="utf-8") as f:
        usos_cargados = json.load(f)    

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
    print("Entropía H (nats):", H_nats)

    with open("Metagen9vgc2025regh.json", "r", encoding="utf-8") as f:
        meta = json.load(f) 
    
    H_interna = 0
    for pokemon in meta:
        H_interna += meta[pokemon]["Prob"] * meta[pokemon]["Entropy"]
    
    print("Entropía interna promedio (nats):", H_interna)

    print("Entropía total:", (H_nats + H_interna)/np.log(6))