class NavAirport:
    def __init__(self, name):
        self.name = name
        self.sids = []   # Departure NavPoints
        self.stars = []  # Arrival NavPoints

    def add_sid(self, sid):
        self.sids.append(sid)

    def add_star(self, star):
        self.stars.append(star)

    def __repr__(self):
        return f"NavAirport({self.name}, SIDs={self.sids}, STARs={self.stars})"
