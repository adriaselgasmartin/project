from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport

#Crea una clase que se llena de variables a partir de lectura de documentos txt
class AirSpace:
    def __init__(self):
        self.nav_points = []
        self.nav_segments = []
        self.nav_airports = []

    def load_nav_points(self, filename):
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 4:
                    number, name, lat, lon = parts[:4]
                    self.nav_points.append(NavPoint(number, name, lat, lon))

    def load_nav_segments(self, filename):
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 3:
                    origin, destination, distance = parts[:3]
                    self.nav_segments.append(NavSegment(origin, destination, distance))

    def load_airports(self, filename):
        with open(filename, "r") as file:
            current_airport = None
            for line in file:
                line = line.strip()
                if line.startswith("LE"):  # Airport line
                    current_airport = NavAirport(line)
                    self.nav_airports.append(current_airport)
                elif line.endswith(".D") and current_airport:
                    current_airport.add_sid(line)
                elif line.endswith(".A") and current_airport:
                    current_airport.add_star(line)

    def __repr__(self):
        return f"AirSpace(NavPoints={len(self.nav_points)}, Segments={len(self.nav_segments)}, Airports={len(self.nav_airports)})"
 
