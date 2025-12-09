
class TeamPokemon():
    def __init__(self) -> None:
        self.pokemon = ""
        self.teras = {}
        self.usage = 0
        self.moves = {}
        self.teammates = {}
        self.items = {}
        self.abilities = {}
        self.ev_spreads = {}
        

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

def get_name_and_obj(linea: str) -> tuple:
    objeto = ""
    name = ""
    found = False
    for i in range(len(linea)):
        if linea[i] == "@":
            objeto = linea[i+2:]
            break
        if linea[i] == " " and not found:
            name = linea[:i]
            found = True
            
    return name, objeto[:len(objeto) - 3]

def get_ability(linea: str):
    ability = linea[9:]
    return ability[:len(ability)- 3]


with open("ejemplo1.txt", "r") as f:
    texto = f.readlines()
nombre = ""
objeto = ""
movimientos = []
habilidad = ""
ev_n = ""

print(texto)

pokemon = Pokemon()

nombre, objeto= get_name_and_obj(texto[0])
pokemon.pokemon = nombre
pokemon.item = objeto
print(nombre, objeto)


habilidad = get_ability(texto[1])

pokemon.ability = habilidad
print(get_ability(texto[1]))


def get_spread(linea1, linea2):
    nature = ""
    for i in range(len(linea2)):
        if linea2[i] == " ":
            nature = linea2[:i]
            break
    return nature

print("sas")
print(texto[4])
print(texto[5])
print(get_spread(texto[4], texto[5]))

print(pokemon)