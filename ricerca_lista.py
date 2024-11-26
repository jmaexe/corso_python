#inserimento elementi in un dictionary (key : cibo , value : quantita), ricerca cibo con info relative
lista ={}
totale = int(input("quanti cibi vuoi inserire nella lista : "))
for i in range(totale):
    cibo = input("Inserisci nome del cibo : ")
    quantita = input(f"Inserisci la quantità di {cibo} : ")
    lista[cibo] = quantita 
    i+=1

print("Lista : ")

for cibo in lista : 
    print(f"{cibo}, quantita : {lista[cibo]}")

cibo_da_cercare = input("Inserisci il cibo che vorresti cercare : ")
if cibo_da_cercare in lista : 
    print(f"{cibo_da_cercare} presente nella lista per tot : {lista[cibo_da_cercare]}")
else :
    print(f"{cibo_da_cercare} non è presente nella lista !")

