class Tool:
    def __init__(self, damage, efficiencyDict, attackSpeed, 
                 name, hitRadius, recipe):
        self.damage = damage
        #how much wood they collect per stroke
        self.efficiencyDict = efficiencyDict
        #possible attacks per second
        self.attackSpeed = attackSpeed
        self.name = name
        self.hitRadius = hitRadius
        self.recipe = recipe
    
    def __repr__(self):
        return (self.name)