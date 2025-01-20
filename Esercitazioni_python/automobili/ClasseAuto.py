class Auto :
    def __init__(self, marca, modello, anno,velocita = 0) :
        self.marca = marca
        self.modello = modello
        self.anno = anno
        self.velocita = velocita
    
    
    def getInfo(self) :
        return f"Marca: {self.marca}, Modello: {self.modello}, Anno: {self.anno}, velocita: {self.velocita}"

    def aumentaVelocita(self,velocita) :
        self.velocita += velocita
    
    def diminuisciVelocita(self,velocita):
        self.velocita -= velocita
    
    def getVelocita(self) : 
        return f"questo veicolo sta andando a una velocita: {self.velocita}km/h"
