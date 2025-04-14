import random
import heapq
from app.dao.city_dao import CityDAO
from app.dao.location_street_customer_dao import LocationDAO, StreetDAO, CustomerDAO

class CityGenerator:
    def __init__(self):
        self.city_id_counter = 1
        self.location_id_counter = 1
        self.street_id_counter = 1
        self.customer_id_counter = 1
        self.graph = {}  # Graph representation for routes

        # DAO instances
        self.city_dao = CityDAO()
        self.location_dao = LocationDAO()
        self.street_dao = StreetDAO()
        self.customer_dao = CustomerDAO()

    def generate_random_name(self, base_name):
        """
        Generate a random name based on the base name plus a random number
        """
        random_number = random.randint(1, 1000)
        return f"{base_name}{random_number}"

    def generate_city(self):
        base_name = "City_"
        unique_name = self.generate_random_name(base_name)
        city = {
            "id": unique_name.split("_")[1],
            "name": unique_name,
            "population": random.randint(1000, 1000000),
            "region": random.choice(["North", "South", "East", "West"])
        }
        self.city_id_counter += 1
        return city

    def generate_location(self, city_id, location_type="junction"):
        base_name = "Location_"
        unique_name = self.generate_random_name(base_name)
        location = {
            "id": unique_name.split("_")[1],
            "name": unique_name,
            "city_id": city_id,
            "type": location_type
        }
        self.location_id_counter += 1
        return location

    def generate_street(self, city_id, start_location_id, end_location_id):
        base_name = "Street_"
        unique_name = self.generate_random_name(base_name)
        street = {
            "id": unique_name.split("_")[1],
            "name": unique_name,
            "city_id": city_id,
            "start_location_id": start_location_id,
            "end_location_id": end_location_id,
            "length": round(random.uniform(0.5, 10.0), 2)
        }
        self.street_id_counter += 1
        return street

    def generate_customer(self, city_id):
        base_name = "Customer_"
        unique_name = self.generate_random_name(base_name)
        customer = {
            "id": unique_name.split("_")[1],
            "name": unique_name,
            "email": f"customer{self.customer_id_counter}@example.com",
            "phone": f"+1-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "city_id": city_id
        }
        self.customer_id_counter += 1
        return customer

    def generate_city_data(self, num_cities=1, locations_per_city=5, streets_per_city=5, customers_per_city=10):
        cities = []
        locations = []
        streets = []
        customers = []

        for _ in range(num_cities):
            city = self.generate_city()
            cities.append(city)

            # Generate locations for the city
            city_locations = []
            for _ in range(locations_per_city):
                location = self.generate_location(city["id"])
                locations.append(location)
                city_locations.append(location)

            # Generate streets connecting random locations
            for _ in range(streets_per_city):
                start_location = random.choice(city_locations)
                end_location = random.choice(city_locations)
                if start_location["id"] != end_location["id"]:  # Avoid self-loops
                    street = self.generate_street(city["id"], start_location["id"], end_location["id"])
                    streets.append(street)
                else:
                    while start_location["id"] == end_location["id"]:
                        end_location = random.choice(city_locations)
                    street = self.generate_street(city["id"], start_location["id"], end_location["id"])
                    streets.append(street)
            # Clean location nodes that are not connected to any street
            for location in city_locations:
                if not any(street["start_location_id"] == location["id"] or
                           street["end_location_id"] == location["id"] for street in streets):
                    locations.remove(location)
            # Generate customers for the city
            for _ in range(customers_per_city):
                customer = self.generate_customer(city["id"])
                customers.append(customer)

        # Build the graph for route calculations
        self.build_graph(streets)

        return {
            "cities": cities,
            "locations": locations,
            "streets": streets,
            "customers": customers
        }

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
