class Player:
    def __init__(self):
        self.health = 10
        self.stamina = 100
        self.inventoryCols = 5
        self.inventoryRows = 2
        self.inventory = [([0] * self.inventoryCols) for row in range(self.inventoryRows)]
        self.currTool = None
        self.currArmor = None