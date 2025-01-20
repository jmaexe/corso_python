#numero da indovinare senza limiti tra 1 e 20
import random as r

numero_da_indovinare = r.randint(1,20)
numero = -1 
n_tentativi = 0
while(numero != numero_da_indovinare) : 
    numero = int(input("Inserisci un numero da 1 a 20: "))
    if numero_da_indovinare > numero : 
        print(f"Il numero da indovinare è maggiore di {numero}")
    elif numero_da_indovinare < numero : 
        print(f"Il numero da indovinare è minore di {numero}")
    n_tentativi+=1
    
print(f"Numero indovinato ({numero_da_indovinare}) in {n_tentativi} tentativi. Grazie per aver giocato!")