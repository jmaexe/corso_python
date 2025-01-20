#prima inserire i due numeri e poi cliccare sull'operazione desiderata
#gestione controllo errori nel caso non siano numeri, nel caso si inserisca 0 come secondo numero nella divisione
import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()
# window.geometry('')
window.title("prova")
window.resizable(True, True)
# window.geometry("600x400")
window.configure(background="black")
# canvas = tk.Canvas(window, height=100, width=100)
# canvas.pack()
# bg = ImageTk.PhotoImage(Image.open(r"/home/its/Documents/Python/Esercitazioni_python/calcolatrice_visuale/img.png")) 
# bg_l = tk.Label(window, image=bg)
# bg_l.place()
frame = tk.Frame(window,)
label1 = tk.Label(frame, text="Inserisci il primo numero:",bg="orange")
label1.grid(row=0, column=0)
numBox1 = tk.Entry(frame)
numBox1.grid(row=1, column=0)
frame.grid(row=0,column=0,padx=10,pady=10)

frame2 = tk.Frame(window,)
label2 = tk.Label(frame2, text="Inserisci il secondo numero:",bg="orange")
label2.grid(row=0, column=0)
numBox2 = tk.Entry(frame2)
numBox2.grid(row=1, column=0)
frame2.grid(row=0,column=1)


frame3 = tk.Frame(window,bg="black")
frame3.grid(row=1,column=0,columnspan=2)
bottoni = ['x','/','+','-']
i = 0
for bottone in bottoni : 
    bottone = tk.Button(frame3, text=bottone, command= lambda operazione=bottone: calcola(operazione),bg="blue",relief="flat",)
    bottone.grid(row=0, column=i,padx=5)
    i+=1



def calcola(operazione) : 
    if numBox1.get() == "" or numBox2.get() == "":
        risultato_label.config(text="Devi inserire due numeri")
        return
    try:
        num1 = float(numBox1.get())
        num2 = float(numBox2.get())
    except ValueError:
        return
    if operazione == '+':
        risultato = num1 + num2
    elif operazione == '-':
        risultato = num1 - num2
    elif operazione == 'x':
        risultato = num1 * num2
    elif operazione == '/':
        if num2 == 0:
            risultato = "Non puoi dividere per zero"
            risultato_label.config(text="Non puoi dividere per zero")
            return  
        else:
            risultato = num1 / num2
    else:
        risultato = "Operazione non valida"
    risultato_label.config(text="Risultato: " + str(risultato))
    risultato_label = tk.Label(window, text="Risultato:",bg="yellow",
font=("Helvetica",12))
    risultato_label.grid(row=2, column=0,columnspan=2,pady=10)




if __name__ == "__main__":
    window.mainloop()

