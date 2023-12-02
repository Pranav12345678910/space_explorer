class Tool:
    def __init__(self, damage, woodEfficiency, metalEfficiency, attackSpeed, 
                 name, hitRadius):
        self.damage = damage
        #how much wood they collect per stroke
        self.woodEfficiency = woodEfficiency
        #how much metal they collect per stroke
        self.metalEfficiency = metalEfficiency
        #possible attacks per second
        self.attackSpeed = attackSpeed
        self.name = name
        self.hitRadius = hitRadius
    
    def __repr__(self):
        return (self.name)