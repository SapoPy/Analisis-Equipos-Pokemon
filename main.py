from pokemon import *
import requests 
from bs4 import BeautifulSoup
import numpy as np
import json
from entropia_k_elementos import *
from metricas import * 

def information_pokemon(pokemon: Pokemon, meta: dict) -> float:
    """
    Entrega la información en nats de un pokemon en un meta
    """
    information_pokemon = 0
    for move in pokemon.moves:
        try:
            meta_move = meta[pokemon.pokemon]["Moves"][move]
            information_pokemon += information(meta_move)
        except KeyError:
            meta_move = meta[pokemon.pokemon]["Moves"]["Other"]
            information_pokemon += information(meta_move)
    
    try:
        meta_obj = meta[pokemon.pokemon]["Items"][pokemon.item]
        information_pokemon += information(meta_obj)
    except KeyError:
        meta_obj = meta[pokemon.pokemon]["Items"]["Other"]
        information_pokemon += information(meta_obj)
    
    try:
        meta_abil= meta[pokemon.pokemon]["Abilities"][pokemon.ability]
        information_pokemon += information(meta_abil)
    except KeyError:
        meta_abil = meta[pokemon.pokemon]["Abilities"]["Other"]
        information_pokemon += information(meta_abil)

    try:
        meta_ev_spread= meta[pokemon.pokemon]["Evs Spreads"][pokemon.ev_spread]
        information_pokemon += information(meta_ev_spread)
    except KeyError:
        meta_ev_spread = meta[pokemon.pokemon]["Evs Spreads"]["Other"]
        information_pokemon += information(meta_ev_spread)

    return information_pokemon

def information_team(team: Team, meta: dict) -> float:
    """
    Entrega la información en nats de un equipo en un meta
    """
    informacion_equipo = 0
    for pokemon in team.team:
        try:
            informacion_equipo += information(meta[pokemon.pokemon]["Prob"]) 
            informacion_equipo += information_pokemon(pokemon, meta)
        except KeyError: # me da la sensacion que esta exception no deberia ocurrir nunca
            informacion_equipo += information(meta["Other"])
    
    return informacion_equipo


if __name__ == "__main__":

    REGULATION = "gen9vgc2025regj"
    
    with open( REGULATION + ".json", "r", encoding="utf-8") as f:
        usos_cargados = json.load(f)    

    p_target = np.array(list(usos_cargados.values()))
    K = 6

    # Ajustar pesos w:
    w = fit_weights_from_marginals(p_target, K)

    # Obtener p_model (debe coincidir con p_target)
    p_model, Zk = expected_inclusions(w, K)
    
    # Calcular entropía (nats). Si quieres bits, dividir por ln(2).
    H_nats = entropy_from_weights(w, K, p_model=p_model)
    

    with open( "Meta" + REGULATION + ".json", "r", encoding="utf-8") as f:
        meta = json.load(f) 
    
    H_interna = 0
    for pokemon in meta:
        H_interna += meta[pokemon]["Prob"] * meta[pokemon]["Entropy"]
    
    print(f"Entropía del Meta: {(H_nats + H_interna):.3f} nats")

    nombre_equipo = "VGCCPaste1"

    team = Team(nombre_equipo)

    informacion_equipo = information_team(team, meta)
    
    print(f"Cantidad de informacion del equipo {nombre_equipo}: {informacion_equipo:.3f} nats")