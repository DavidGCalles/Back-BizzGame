import random
import heapq
from app.dao.city_config_dao import CityConfigDAO
from app.dao.location_dao import LocationTypeDAO

class CityGenerator:
    def __init__(self):
        self.city_id_counter = 1
        self.location_id_counter = 1
        self.street_id_counter = 1
        self.customer_id_counter = 1
        self.graph = {}  # Graph representation for routes

        # DAO instances
        self.city_config_dao = CityConfigDAO()
        self.location_type_dao = LocationTypeDAO()

    def generate_random_name(self, base_name):
        """
        Generate a random name based on the base name plus a random number
        """
        random_number = random.randint(1, 500)
        return f"{base_name}{random_number}"

    def generate_city(self, values=None):
        if values is None:
            raise ValueError("Values must be provided when random is False")
        base_name = f"City_{values['difficulty_level']+'_'}"
        unique_name = self.generate_random_name(base_name)
        city = {
            "id": unique_name.split("_")[2],
            "name": unique_name,
            "population": int(values["max_population"]* values["residential_rate"]),
            "region": random.choice(["North", "South", "East", "West"])
        }
        self.city_id_counter += 1
        return city

    def generate_location(self, city_id:int, location_type: dict|None = None):
        base_name = f"Location_{location_type['name']+'_' if location_type is not None else ''}"
        unique_name = self.generate_random_name(base_name)
        location = {
            "id": int(f"{city_id}{self.location_id_counter}"),
            "name": unique_name,
            "city_id": city_id,
            "location_type_id": location_type["id"] if location_type else None,
        }
        self.location_id_counter += 1
        return location

    def generate_street(self, city_id, start_location_id, end_location_id):
        base_name = f"Street_{city_id}_"
        unique_name = self.generate_random_name(base_name)
        street = {
            "id": int(f"{city_id}{self.street_id_counter}"),
            "name": unique_name,
            "city_id": city_id,
            "start_location_id": start_location_id,
            "end_location_id": end_location_id,
            "length": round(random.uniform(0.5, 10.0), 2)
        }
        self.street_id_counter += 1
        return street

    def generate_customer(self, city_id):
        base_name = f"Customer_{city_id}"
        unique_name = self.generate_random_name(base_name)
        customer = {
            "id": int(f"{city_id}{self.customer_id_counter}"),
            "name": unique_name,
            "email": f"customer_{city_id}_{self.customer_id_counter}@example.com",
            "phone": f"+1-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "city_id": city_id
        }
        self.customer_id_counter += 1
        return customer

    def generate_city_data(self, rates=None):
        """
        Generate city data including cities, locations, streets, and customers.
        rates object is composed of:
        - max_population: Maximum population allowed in the city
        - max_locations: Maximum number of locations allowed in the city
        - residential_rate: Rate of residential locations
        - commercial_rate: Rate of commercial locations
        - difficulty_level: Difficulty level for city generation
        """
        cities = []
        locations = []
        streets = []
        customers = []

        if rates is None:
            residential_rate = random.uniform(0.3, 0.7)
            commercial_rate = 1 - residential_rate
            rates = {
                "max_population": random.randint(90, 200),
                "max_locations": random.randint(5, 20),
                "residential_rate": residential_rate,
                "commercial_rate": commercial_rate,
                "difficulty_level": random.choice(["easy", "medium", "hard"]),
            }
        city = self.generate_city(values=rates)
        cities.append(city)
        residential_locations = int(rates["max_locations"] * rates["residential_rate"])
        commercial_locations = int(rates["max_locations"] * rates["commercial_rate"])
        total_locations = residential_locations + commercial_locations
        location_types = self.location_type_dao.get_all_by_basic_type()
        for i in range(total_locations):
            location_type = None
            if i < residential_locations:
                location_type = random.choice(location_types["Residential"])
            elif i >= residential_locations and i < total_locations:
                location_type = random.choice(location_types["Business"])
            else:
                raise ValueError("Invalid location type assignment")
            location = self.generate_location(city["id"], location_type)
            locations.append(location)
        for i in range(int(rates["max_population"] * rates["residential_rate"])):
            customer = self.generate_customer(city["id"])
            customers.append(customer)
        for i in range(len(locations)):
            start_location = locations[i]
            end_location = random.choice(locations)
            while start_location["id"] == end_location["id"]:
                end_location = random.choice(locations)
            street = self.generate_street(city["id"], start_location["id"], end_location["id"])
            streets.append(street)

        # Build the graph for route calculations
        self.build_graph(streets)

        return {
            "cities": cities,
            "locations": locations,
            "streets": streets,
            "customers": customers
        }

    def generate_bounded_city_data(self, difficulty_level):
        """
        Generate bounded city data based on difficulty level.
        """
        try:
            config_rates = self.city_config_dao.get_single_city_config_by_difficulty(difficulty_level)
        except Exception as e:
            print(f"Error fetching city configuration: {e}")
            return None
        print(config_rates)
        return self.generate_city_data(config_rates)
    
    def build_graph(self, streets):
        """
        Build a graph representation from the streets data.
        """
        for street in streets:
            start = street["start_location_id"]
            end = street["end_location_id"]
            length = street["length"]

            if start not in self.graph:
                self.graph[start] = []
            if end not in self.graph:
                self.graph[end] = []

            self.graph[start].append((end, length))
            self.graph[end].append((start, length))  # Assuming undirected graph

    def calculate_shortest_path(self, start_location, end_location):
        """
        Calculate the shortest path between two locations using Dijkstra's Algorithm.
        """
        distances = {location: float('inf') for location in self.graph}
        distances[start_location] = 0
        priority_queue = [(0, start_location)]  # (distance, location_id)

        while priority_queue:
            current_distance, current_location = heapq.heappop(priority_queue)

            if current_distance > distances[current_location]:
                continue

            for neighbor, length in self.graph.get(current_location, []):
                distance = current_distance + length
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances[end_location] if distances[end_location] != float('inf') else None
