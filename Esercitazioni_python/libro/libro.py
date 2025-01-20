libriDisponibili = {1: "Guerra e pace",2: "Il ritratto di Dorian Gray",3: "La coscienza di Zeno"}
libriInPrestito = {} 
def aggiungiLibro(titolo) :
    # libriDisponibili.append(titolo)
    index = max(libriDisponibili.keys())
    index2 = max(libriInPrestito.keys())
    if index > index2 : libriDisponibili[index] = titolo
    else : libriDisponibili[index2] = titolo

def prendiInPrestitoLibro(i) :
    libro = libriDisponibili.pop(i)
    libriInPrestito[i] = libro
    # libro = libriDisponibili.pop(i-1)
    # libriInPrestito.append(libro)

def restituisciLibro(i) :
    libro = libriInPrestito.pop(i)
# max(libriDisponibili.keys())+1
    libriDisponibili[i] = libro

def mostraLibriDisponibili() :
    if len(libriDisponibili) == 0 :
        print("\nNessun libro disponibile !")
    else :
        print("Libri disponibili:\n")
        for num,titolo in libriDisponibili.items() :
            print(str(num) + ". " + titolo)
    # if(len(libriDisponibili) == 0) : print("\nNessun libro disponibile")
    # else : 
    #     for i in range(len(libriDisponibili)) : 
    #         print(libriDisponibili[i] + " - " + str(int(i+1)))

def isDisponibile(num) :
    return True if num in libriDisponibili.keys() else False 

def mostraLibriInPrestito() :
    if len(libriInPrestito) == 0 :
        print("\nNessun libro in prestito")
    else : 
        print("\nLibri in prestito:")
        for num,titolo in libriInPrestito.items() :
            print(str(num) + ". " + titolo)
    # for i in range(len(libriInPrestito)) : 
    #     print(libriInPrestito[i] + " - " + str(int(i+1)))

