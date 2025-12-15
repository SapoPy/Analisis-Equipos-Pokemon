class Pokemon():
    def __init__(self) -> None:
        self.pokemon = ""
        self.tera = ""
        self.moves = []
        self.item = ""
        self.ability = ""
        self.ev_spread = ""
    
    def __str__(self) -> str:
        return f"{self.pokemon} @ {self.item}\nAbility: {self.ability}\nEVs: {self.ev_spread}\nMoves: {self.moves}"
    
class Team():
    def __init__(self, paste: str = "") -> None:
        self.name = paste
        self.team = [] # lista de la clase Pokemon
        if not paste ==  "":
            self.make_team(paste)

    def __str__(self) -> str:
        txt = ""
        for i in range(len(self.team)):
            txt += "\n" + str(self.team[i]) + "\n"
        return txt[1:len(txt)-1]

    def __getitem__(self, idx: int) -> Pokemon:
        """
        Entrega ak pokemon en el indice idx
        """
        return self.team[idx]

    def make_team(self, paste: str) -> None:
        """
        Añade a al atributo team el equipo del paste, el paste es el texto en el formato de showdown
        """        
        with open(f"{paste}.txt", "r") as f:
            texto = f.readlines()

        last_i = 0
        for i in range(len(texto)):
            if texto[i] == "\n":
                pokemon = Pokemon()
                give_attr(pokemon, texto[last_i: i])
                self.team.append(pokemon)
                last_i = i+1


def get_name_and_obj(linea: str) -> tuple:
    """
    Entrega el nombre del pokemon y el objeto en linea
    """
    objeto = ""
    name = ""
    found = False
    for i in range(len(linea)):
        if linea[i] == "@":
            objeto = linea[i+2:]
            name = linea[:i-1]
            break

    return name, objeto[:len(objeto) - 3]

def get_ability(linea: str) -> str:
    """
    Entrega la habilidad en linea
    """
    ability = linea[9:]
    return ability[:len(ability)- 3]

def get_spread(linea1, linea2):
    """
    Entrega el EV spread y naturaleza en el formato Nature HP/Atk/Def/SpA/SpD/Spe
    """    
    nature = ""
    spread = ""
    for i in range(len(linea2)):
        if linea2[i] == " ":
            nature = linea2[:i]
            break
    
    def search_stat(stat:str, linea: str) -> str:
        elemntos = linea.split()
        for i in range(len(elemntos)):
            if elemntos[i] == stat:
                return elemntos[i-1]
        return "0"
    spread += nature + " " + search_stat("HP", linea1) +"/" + search_stat("Atk", linea1)+"/" + search_stat("Def", linea1)+"/" + search_stat("SpA", linea1)+"/"+ search_stat("SpD", linea1) +"/"+ search_stat("Spe", linea1)
    
    return spread

def get_moveset(lineas: list) -> list:
    """
    Entrega el moveset en una lista
    """
    moveset = []
    for linea in lineas:
        filtrado = linea[2:]
        filtrado = filtrado[:len(filtrado)-3]
        moveset.append(filtrado)
    return moveset

def give_attr(pokemon: Pokemon, paste: list) -> None:
    """
    Asigna todos los atributos que le corresponden a un pokemon dado un 
    """    
    nombre, objeto= get_name_and_obj(paste[0])
    pokemon.pokemon = nombre
    pokemon.item = objeto

    habilidad = get_ability(paste[1])
    pokemon.ability = habilidad

    spread = get_spread(paste[4], paste[5])
    pokemon.ev_spread = spread

    moves = paste[-4:]
    moveset = get_moveset(moves)
    pokemon.moves = moveset


if __name__ == "__main__":
    team = Team("ejemplo")

    print(team)