import json
from bs4 import BeautifulSoup

def make_dist(ARCHIVO_HTML: str) -> dict:
    """
    Entrega el diccionario con la probabilidad de aparicion de cada pokemon que salgan en un archivo .txt
    sacado de inspeccionar elemntos de la pagina https://www.pikalytics.com
    """
    with open(ARCHIVO_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    dist = {}

    # Cada Pokémon está contenido en un <a ... class="pokedex_entry"...>
    entries = soup.find_all("a", class_="pokedex_entry")

    for ent in entries:
        nombre = ent.get("data-name", "").strip()
        nombre = nombre.replace("%20", " ")
        if not nombre:
            continue

        # El porcentaje exacto está en este span:
        span = ent.find("span", class_="float-right margin-right-20")
        if not span:
            continue

        texto = span.text.strip().replace("%", "")
        try:
            uso = float(texto) / 100.0
        except:
            continue

        dist[nombre] = uso
    return dist

def save_dist(dict_json: dict, save_output: str):
    """
    Guarda en un .json el diccionario dict_json
    """    
    with open(save_output, "w", encoding="utf-8") as f:
        json.dump(dict_json, f, indent=4, ensure_ascii=False)
        print("JSON generado con éxito.")

if __name__ == "__main__":
    ARCHIVO_HTML = "gen9vgc2025regj.txt"
    OUTPUT_JSON = "gen9vgc2025regj.json"
    usos = make_dist(ARCHIVO_HTML)
    print(usos)

    sum_prob = sum(list(usos.values()))

    if sum_prob < 6:
        usos["Other"] = 6 - sum_prob

    save_dist(usos, OUTPUT_JSON)

    with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
        usos_cargados = json.load(f)
    
    
    print(usos_cargados["Gholdengo"])   