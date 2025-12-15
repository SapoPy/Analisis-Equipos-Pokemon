import requests 
from bs4 import BeautifulSoup
import json
from TeamPokemon import * 
from metricas import *
from entropia_k_elementos import *
import numpy as np

class Meta():
        def __init__(self, regulation: str) -> None:
                """
                regulation: nombre de json
                """
                self.regulation = regulation
                self.meta = {}
                with open(f"{regulation}.json", "r", encoding="utf-8") as f:
                        reg_json = json.load(f)
        
                for pok in reg_json:
                        print(f"Estamos en {pok}")
                        pok = DistribucionPokemon(pok, regulation)
                        self.meta[pok.Name] = pok.get_dict()
                
        def save_json(self) -> None:
                """
                Guarda en un json los datos de Meta
                """
                with open("Meta"+self.regulation + ".json", "w", encoding="utf-8") as f:
                        json.dump(self.meta, f, indent=4, ensure_ascii=False)
                        print("JSON generado con éxito.")

class DistribucionPokemon():
        def __init__(self, Name, regulation) -> None:
                if Name == "Other":
                        self.Name = Name
                        self.prob = self.get_prob(regulation)
                        self.soup = ""
                        self.moves = {None: 1}
                        self.teammates = {None: 1}
                        self.evs_spread = {None: 1}
                        self.abilities = {None: 1}
                        self.items = {None: 1}
                        self.entropy = 0
                else: 
                        self.Name = Name
                        self.soup = BeautifulSoup(requests.get(f"https://www.pikalytics.com/pokedex/{regulation}/{Name.lower()}").text,"lxml")
                        self.prob = self.get_prob(regulation)
                        self.moves = self.get_moves()
                        self.teammates = self.get_teammates()
                        self.evs_spread = self.get_spread()
                        self.abilities = self.get_abilities()
                        self.items = self.get_item()
                        self.normalize()
                        self.entropy = self.get_entropy()

        def normalize(self) -> float:
                norml = sum(self.moves.values())
                for move in self.moves:
                        self.moves[move] = self.moves[move] * 4 / norml 
        def get_prob(self, regulation: str) -> float:
                # Extraer el JSON de Next.js

                with open(f"{regulation}.json", "r", encoding="utf-8") as f:
                        load_usage = json.load(f)

                return load_usage[self.Name]
        def get_moves(self) -> dict:
                data = self.soup.find("div", {"id": "moves_wrapper"})

                movesset = {}

                moves = data.find_all("div", {"class": "pokedex-move-entry-new"})

                for move in moves:
                        divs = move.find_all("div")

                        # No se que hace esto
                        #if len(divs) < 2: 
                        #    continue
    
                        name = divs[0].text.strip()
                        if name == "Nothing":
                                perc = float(divs[2].text.replace("%", "").strip())
                                if perc > 100:
                                        perc = 100.0
                                        movesset[name] = perc/100
                                continue
                        perc = float(divs[2].text.replace("%", "").strip())/100
                        movesset[name] = perc
                return movesset
        def get_teammates(self) -> dict:
                data = self.soup.find("div", {"id": "teammate_wrapper"})

                teammates = {}

                mates = data.find_all("a")

                for mate in mates:
                        name = mate.get("data-name", "").strip()
                        
                        perc = float(mate.text.strip().split()[-1].replace("%", ""))/100
                        teammates[name] = perc
                return teammates
        def get_spread(self) -> dict:
        
                EVs = {}
                for EV in self.soup.find_all("div",{"id":"dex_spreads_wrapper"})[0].text.split("\n\n"):
                        if len(EV) > 1: 
                                EV = EV.replace("\n"," ").split(" ")
                                EVs[EV[1] +" "+ EV[2]] = float(EV[3].replace("%", ""))/100
                if sum(EVs.values()) < 1:
                        EVs["Other"] = 1 - sum(EVs.values())
                return EVs
        def get_abilities(self) -> dict:
                abilities = {}
                for ab in self.soup.find_all("div",{"id":"abilities_wrapper"})[0].text.split("\n\n\n"):
                        if ab != "":
                                try:
                                        ability = ab.split("\n")[0]
                                        perc = float(ab.split("\n")[1].replace("%",""))/100
                                        abilities[ability] = perc
                                except:
                                        abilities["Other"] = 1
                return abilities
        def get_item(self) -> dict:
                items = {}

                for item in self.soup.find_all("div",{"id":"items_wrapper"})[0].text.split("\n\n\n\n\n\n\n\n"):
                        if item != "":
                                items[item.split("\n")[0]] = float(item.split("\n")[1].replace("%",""))/100
                
                return items
        def get_entropy(self) -> float:
                total_entropy = 0

                for spread in self.evs_spread:
                        total_entropy += entropy(self.evs_spread[spread])
                for item in self.items:
                        total_entropy += entropy(self.items[item])
                for ability in self.abilities.keys():
                        total_entropy += entropy(self.abilities[ability])
                probs = np.array(list(self.moves.values()))
                attempts = [[27000, 1e-5, False],[50000, 1e-4, False], [100000, 5e-3, True]]

                for params in attempts:
                        try:
                                total_entropy += get_entropy_of_k_elements(probs, 4, params[0], params[1], params[2])
                                break  # éxito → salimos del loop
                        except (FloatingPointError, RuntimeError, ValueError):
                                continue
                else:
                        # Si TODOS los intentos fallan
                        print(f"Aparentemento no convergio la entropia para los movimientos, es posible que el pokemon {self.Name} se haya jugado sin los 4 movimientos")
                return total_entropy
        def get_dict(self) -> dict:
                data = {}
                data["Prob"]        =  self.prob
                data["Moves"]       =  self.moves
                data["TeamMates"]   =  self.teammates
                data["Evs Spreads"] =  self.evs_spread
                data["Abilities"]   =  self.abilities
                data["Items"]       =  self.items
                data["Entropy"]     =  self.entropy
                return data

if __name__ == "__main__":

        REGULATION = "gen9vgc2025regj"

        pokemon = "Iron Crown"

        datos = requests.get(f"https://www.pikalytics.com/pokedex/{REGULATION}/{pokemon.lower()}").text

        dist = DistribucionPokemon(pokemon, REGULATION)
        print(dist.entropy)

        with open(f"{REGULATION}.json", "r", encoding="utf-8") as f:
                reg_json = json.load(f)
        
        meta = Meta(REGULATION)
        meta.save_json()


