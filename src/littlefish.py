
class LittleFish(Player):
    def __init__(self, image: str, size: tuple, location: tuple = (0, 0), crab):
        Player.__init__(image,size,location)
        self.health = 10
        self.location = location
        

    def _contains(self):
        if(((crab.get_location()[0]-self.location[0])**2)+\
           (crab.get_location()[0]-self.location[0])**2 < 17):
            return True
        return False

    
        
