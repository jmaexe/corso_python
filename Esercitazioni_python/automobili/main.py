from ClasseAuto import Auto

a = Auto("Fiat", "Panda", 2020)

scelta = 0
while scelta != -1 : 
    scelta = int(input("\nInserisci\n 1 per aumentare la velocita\n 2 per diminuire la velocita,\n 3 per mostrare le caratteritische dell'auto\n -1 per fermare il programma: "))

    if scelta == 1 :
        velocita = int(input("Quanto vuoi aumentare la velocita? "))
        a.aumentaVelocita(velocita)
        print("\n" + a.getVelocita() + "\n")
    elif scelta == 2 :
        velocita = int(input("Quanto vuoi diminuire la velocita? "))
        a.diminuisciVelocita(velocita)
        print("\n" + a.getVelocita() + "\n")
    elif scelta == 3 :
        print("\n" + a.getInfo() + "\n")
    