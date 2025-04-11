import requests

CITY = "Noves"
COUNTRY = "Spain"

import requests

def get_streets(city, country="España"):
    BASE_URL = "http://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    area["name"="{country}"]["admin_level"="2"]->.countryArea; 
    area["name"="{city}"](area.countryArea)->.searchArea; 
    way[highway](area.searchArea);
    out body;
    """
    
    response = requests.get(BASE_URL, params={"data": query})
    data = response.json()

    streets = set()
    for element in data.get("elements", []):
        if "tags" in element and "name" in element["tags"]:
            streets.add(element["tags"]["name"])
    
    return sorted(streets)

# 🔹 Prueba con Novés, España
streets = get_streets("Novés")
print("Calles en Novés:", streets)


# Ejecutar la búsqueda
#streets = get_osm_streets(CITY, COUNTRY)
#print("\n".join(streets))

def get_osm_population(city, country):
    url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    area[name="{country}"]->.countryArea;
    node["place"](area.countryArea)["name"="{city}"];
    out;
    """
    print(query)
    response = requests.get(url, params={"data": query})
    data = response.json()
    
    for element in data.get("elements", []):
        if "tags" in element and "population" in element["tags"]:
            return int(element["tags"]["population"])
    
    return None  # No se encontró población en OSM

population = get_osm_population(CITY, COUNTRY)
print(f"Población de {CITY}: {population if population else 'No disponible en OSM'}")