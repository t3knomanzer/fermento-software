class JarSchema:

    def __init__(self, name, distance):
        self.name = name
        self.distance = distance

    def to_dict(self):
        return {"name": self.name, "distance": self.distance}
