import requests

class OSMService:
    def __init__(self, country="Spain"):
        self.BASE_URL = "http://overpass-api.de/api/interpreter"
        self.country = country
        self.session = requests.Session()  # Reuse session for efficiency

    def get_streets(self, city):
        query = f"""
        [out:json];
        area["name"="{self.country}"]["admin_level"="2"]->.countryArea; 
        area["name"="{city}"](area.countryArea)->.searchArea; 
        way[highway](area.searchArea);
        out body;
        """
        
        response = self.session.get(self.BASE_URL, params={"data": query}, timeout=10)
        data = response.json()

        streets = set()
        for element in data.get("elements", []):
            if "tags" in element and "name" in element["tags"]:
                streets.add(element["tags"]["name"])
        
        return sorted(streets)

    def get_country_of_city(self, city):
        query = f"""
        [out:json];
        node["name"="{city}"]["place"];
        is_in;
        area._[admin_level=2];
        out;
        """
        response = self.session.get(self.BASE_URL, params={"data": query})
        data = response.json()

        for element in data.get("elements", []):
            if "tags" in element and "name" in element["tags"]:
                return element["tags"]["name"]  # Country name

        return None  # No country found

    def get_population(self, city):
        query = f"""
        [out:json];
        area["name"="{self.country}"]["admin_level"="2"]->.countryArea;
        area["name"="{city}"](area.countryArea)->.searchArea;
        node["place"](area.searchArea)["name"="{city}"]["population"];
        out;
        """
        response = self.session.get(self.BASE_URL, params={"data": query})
        data = response.json()

        for element in data.get("elements", []):
            if "tags" in element and "population" in element["tags"]:
                return int(element["tags"]["population"])

        return None  # Population data not found
    
    def get_city_data(self, city, country= None):
        if country is None:
            country = self.country
        query = f"""
        [out:json];
        area["name"="{country}"]["admin_level"="2"]->.countryArea; 
        area["name"="{city}"](area.countryArea)->.searchArea; 
        
        (
          node["place"](area.searchArea)["name"="{city}"];   // City info
          way[highway](area.searchArea);                    // Streets
        );
        
        out body;
        """
        
        response = self.session.get(self.BASE_URL, params={"data": query}, timeout=15)
        data = response.json()

        city_info = {}
        streets = set()

        for element in data.get("elements", []):
            if element["type"] == "node" and "tags" in element:
                city_info["name"] = element["tags"].get("name")
                city_info["population"] = int(element["tags"].get("population", 0))
                city_info["region"] = self.country  # We already filtered it by country
            
            if element["type"] == "way" and "tags" in element and "name" in element["tags"]:
                streets.add(element["tags"]["name"])
        
        city_info["streets"] = sorted(streets)
        return city_info
