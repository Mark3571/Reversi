#Reversi Imperatief Programmeren
#Gemaakt door Mark Crooijmans en Bruno Schuttelaars

import tkinter as tk
from PIL import Image, ImageDraw, ImageTk


#Defineer de klasse voor het spel
class ReversiGame:
    #Constanten voor status vakje
    EMPTY = 0 #Geen steen op veld
    BLUE = 1 #Blauwe steen
    RED = 2 #Rode steen

    #Initialiseer GUI scherm
    def __init__(self,scherm):
        self.scherm = scherm
        scherm.title("Reversi game") #Geef venster Titel

        #Variabele voor de groote van het bord
        #Gekoppeldt aan het label waarin de bordgroote staat
        self.board_size = tk.IntVar(value=6)  # standaard 6x6

        #Frame voor knoppen van menu
        menu = tk.Frame(scherm)
        menu.pack()

        #Label en dropdown voor schermgroote
        #Bij verandering start er nieuw spel
        tk.Label(menu, text="schermgroote:").pack(side=tk.LEFT)
        tk.OptionMenu(menu, self.board_size, 4,6,8,10, command=self.new_game).pack(side=tk.LEFT)

        #Knop om nieuw spel te starten
        tk.Button(menu, text= "Nieuw spel", command=self.new_game).pack(side=tk.LEFT)

        #Help knop die switch tussen help aan/uit
        self.help_knop = tk.Button(menu, text="Help: uit", command=self.switch_help)
        self.help_knop.pack(side=tk.LEFT)

        #Frame om huidige staat beurt/status te tonen
        status = tk.Frame(scherm)
        status.pack(fill=tk.X)

        #Label dat de huidige aantallen toont
        self.count_label = tk.Label(status, text="Blauw: 0   Rood: 0", font=("Arial", 12))
        self.count_label.pack(side=tk.LEFT)

        #Label dat aangeeft wie er is
        self.turn_label = tk.Label(status, text="Status: -", font=("Arial", 12))
        self.turn_label.pack(side=tk.RIGHT)

        #Canvas waarin getekent gaat worden
        self.canvas = tk.Canvas(scherm, width=600, height=600, bg="white")
        self.canvas.pack()

        #Bind de linkermuisknop aan de on_click-methode
        self.canvas.bind("<Button-1>", self.on_click)

        #Laat zien of help aan of uit staat
        self.help_shown = False

        #Memory voor images
        self.images = {}

        #Start een nieuw spel 
        self.new_game()



scherm = tk.Tk()
ReversiGame(scherm)
scherm.mainloop()
