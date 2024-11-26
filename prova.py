# class Persona:
#     def __init__(self,nome):
#         self.nome = nome
#     def stampa(self) :
#         return self.nome

# class Studente(Persona) :
#     def __init__(self, nome,classe):
#         super().__init__(nome)
#         self.classe = classe


# p = Persona("Andrea")
# s = Studente("Andrea","5H")
# print(p.stampa())
# print(s.classe34)
# a = 2323431411
# b ="aefbb"
# nome = input("Inserisci nome: ")
# cognome = input("Inserisci cognome: ")
# print(f"{nome} {cognome}")
# e= False
# print(f"hello world! {a} {type(nome)}")
# print("ciao" + b)
# print("ciao",b)
# print("faefa:" ,len(str(e)))
# array = [1,23,515,1,232,341]
# i = 0
# while i < 10 :
#     print(i)
#     i+=1
# # else:
# print("bo")
# for x in range(len(array)) :
#     print(array[x])

# var = "Andrea"
# print(var)

# num1 = int(input("Inserisci il primo numero: "))
# num2 = int(input("Inserisci il secondo numero: "))
# operazione = input("Inserisci l'operazione che vorresti effettuare x,+,-,/: ")
# testo = f"{num1}{operazione}{num2} "

# if operazione == "+" :
#     testo = testo + str(int(num1+num2))
# elif operazione == "-":
#     testo = testo + str(int(num1+num2))
# elif operazione == "x": 
#     testo = testo + str(int(num1+num2))
# elif operazione == "/": 
#     testo = testo + str(int(num1+num2))

# print(testo)

# nome = input("Inserisci il tuo nome : ")
# cognome = input("Inserisci il tuo cognome : ")

# presentazione = f"nome : {nome}, cognome : {cognome}"

# print(presentazione)

# a = input("Inserisci primo numero a:  ")
# b = input("Inserisci secondo numero b: ")

# if a > b : 
#     print("a maggiore di b")
# elif a < b : 
#     print("a minore di b")
# else :
#     print("a è uguale a b")

# totale = int(input("quanti cibi vuoi inserire nella lista : "))
# lista =[]
# while  totale > 0 :
#     lista.append(input("Inserisci cibo : "))
#     totale-=1

# for cibo in lista :
#     print(cibo)

# cibo_da_cercare = input("Inserisci il cibo che vorresti cercare")
# if cibo_da_cercare in lista : 
#     print(f"{cibo_da_cercare} è presente nella lista !")
# else :
#     print(f"{cibo_da_cercare} non è presente nella lista")


    # for i in range(5,10) :
    #     print(i)

import random as r
numero1 = r.randint(0,10)
numero2 = int(input(f"Inserisci numero da confrontare a {numero1}"))
if numero1 > numero2 : 
    print(f"numero {numero1} è maggiore di numero {numero2}")
else :
    print(f"numero {numero1} è minore di numero {numero2}")