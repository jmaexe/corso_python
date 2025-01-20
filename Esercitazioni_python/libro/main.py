import libro as l

print("Gestionale Libreria : ")


scelta = 0
while scelta!= -1:
    print("\n1. Aggiungi libro")
    print("2. Prendi in prestito libro")
    print("3. Restituisci libro")
    print("4. Mostra libri disponibili")
    print("5. Mostra libri in prestito")
    print("6. Mostra se libro sia disponibile o in prestito")
    print("-1. Esci")

    scelta = int(input("Inserisci un numero per la scelta : \n"))

    if scelta == 1:
        titolo = input("Inserisci il titolo del libro : ")
        l.aggiungiLibro(titolo)
    elif scelta == 2:
        num = int(input("Inserisci il numero del libro da prendere in prestito : "))
        l.prendiInPrestitoLibro(num)
    elif scelta == 3:
        num = int(input("Inserisci il numero del libro da restituire : "))
        l.restituisciLibro(num)
    elif scelta == 4 :
        l.mostraLibriDisponibili()
    elif scelta == 5 : 
        l.mostraLibriInPrestito()
    elif scelta == 6 : 
        num = int(input("Inserisci il numero del libro da controllare : "))
        if l.isDisponibile(num): print(f"Libro - {num} è disponibile !")
        else : print(f"Libro - {num} è in prestito!")
    elif -1: 
        break;

print("Grazie per aver utilizzato il nostro gestionale libreria!")