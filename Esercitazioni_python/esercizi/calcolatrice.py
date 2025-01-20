#operazione a scelta tra un numero inserito dall'utente e un numero casuale tra 1 e 100
#uso di if print input random
import random as r
num1 = int(input("Inserisci un numero: "))
num2 =  r.randint(1,100)
operazione = input(f"Inserisci l'operazione che vorresti effettuare con {num1} e {num2} | x,+,-,/: ")
testo = f"{num1}{operazione}{num2} = "

if operazione == "+" :
    testo = testo + str(int(num1+num2))
elif operazione == "-":
    testo = testo + str(int(num1+num2))
elif operazione == "x": 
    testo = testo + str(int(num1+num2))
elif operazione == "/": 
    testo = testo + str(int(num1+num2))

print(testo)