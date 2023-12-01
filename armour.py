class Armour:
    def __init__(self, protectionFactor, speedFactor, name):
        self.protectionFactor = protectionFactor
        self.speedFactor = speedFactor
        self.name = name
    
    def __repr__(self):
        return (self.name)