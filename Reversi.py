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

    #Manieren om over bord te gaan
    DIRS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

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
        tk.Label(menu, text="Schermgroote:").pack(side=tk.LEFT)
        tk.OptionMenu(menu, self.board_size, 4,6,8,10, command=self.new_game).pack(side=tk.LEFT, padx = 4)

        #Knop om nieuw spel te starten
        tk.Button(menu, text= "Nieuw spel", command=self.new_game).pack(side=tk.LEFT, padx = 4)

        #Help knop die switch tussen help aan/uit
        self.help_btn = tk.Button(menu, text="Help: uit", command=self.switch_help)
        self.help_btn.pack(side=tk.LEFT, padx = 4)

        #Frame om huidige staat beurt/status te tonen
        status = tk.Frame(scherm)
        status.pack(fill=tk.X, padx = 6)

        #Label dat de huidige aantallen toont
        self.count_label = tk.Label(status, text="Blauw: 0  Rood: 0", font=("Arial", 12))
        self.count_label.pack(side=tk.LEFT)

        #Label dat aangeeft wie er is
        self.turn_label = tk.Label(status, text="Status:- ", font=("Arial", 12))
        self.turn_label.pack(side=tk.RIGHT)

        #Canvas waarin getekent gaat worden
        self.canvas = tk.Canvas(scherm, width=600, height=600, bg="white")
        self.canvas.pack(padx = 4, pady = 4)

        #Bind de linkermuisknop aan de on_click-methode
        #self.canvas.bind("<Button-1>", self.on_click)

        #Laat zien of help aan of uit staat
        self.help_shown = False

        #Memory voor images
        self.images = {}

        #Start een nieuw spel 
        self.new_game()

    #Initialiseer een nieuw spel
    def new_game(self):
        #Lees de gekozen bordgschermte en sla op in n
        self.n = int(self.board_size.get())

        #Maak een n x n bord en vul alle velden met EMPTY
        self.board = [[self.EMPTY for _ in range(self.n)] for __ in range(self.n)]

        #Plaats de startopstelling in het midden
        mid = self.n // 2
        self.board[mid-1][mid-1] = self.BLUE
        self.board[mid][mid] = self.BLUE
        self.board[mid-1][mid] = self.RED
        self.board[mid][mid-1] = self.RED

        #Blauw is beginspeler
        self.current_player = self.BLUE

        #Zet help uit en update de knoptekst
        self.help_shown = False
        self.help_btn.config(text="Help: uit")

        #Teken het bord 
        self.draw_board()

        #Update de statuslabels
        #self.update_status()        


    #Teken het bord
    def draw_board(self):
        #Maak volledig canvas leeg
        self.canvas.delete("all")

        #Canvas afmetingen
        w, h = 600, 600
        pad = 20  #Rand canvas en bord
        #Celgroote berekenen zodat het bord netjes in de canvas past
        self.cell_size = (w - 2* pad) / self.n

        #Teken verticale lijnen voor het raster
        for i in range(self.n+1):
            x0 = pad + i* self.cell_size
            self.canvas.create_line(x0, pad, x0, pad+self.n * self.cell_size, fill="#333")

        #Teken horizontale lijnen van het raster
        for j in range(self.n+1):
            y0 = pad + j*self.cell_size
            self.canvas.create_line(pad, y0, pad+self.n * self.cell_size, y0, fill="#333")

        #Teken per vakje alle stenen
        for r in range(self.n):
            for c in range(self.n):
                val = self.board[r][c]
                #Wanneer veld niet leeg is teken blauwe of rode steen
                if val != self.EMPTY:
                    color = "blue" if val == self.BLUE else "red"
                    self.draw_stone(r, c, color)

    #Teken steen op rij r, kolom c met de gegeven color
    def draw_stone(self, r, c, color):
        pad = 20
        #Bereken het midden van de cel in pixels
        x = pad + c*self.cell_size + self.cell_size/2
        y = pad + r*self.cell_size + self.cell_size/2
        #Straal van de steen
        straal = self.cell_size * 0.42

        #Maak een key voor het geheugen (hiermee voorkomen hergegeneren dezelfde afbeeldingen)
        key = (color, int(straal))
        if key not in self.images:
            #Maak image
            img = Image.new("RGBA", (int(straal*2)+4, int(straal*2)+4), (0,0,0,0))
            draw = ImageDraw.Draw(img)

            # Kies hoofdkleur: blauw of rood
            main_col = (0,0,255) if color=="blue" else (220,0,0)

            # Teken de hoofd-ellips (de steen) met zwarte outline
            draw.ellipse((0,0,straal*2-2,straal*2-2), fill=main_col, outline="black", width=2)

            # Converteer image
            self.images[key] = ImageTk.PhotoImage(img)

        #Haal de afbeelding uit memory en teken
        img = self.images[key]
        #Teken
        self.canvas.create_image(x-straal, y-straal, anchor=tk.NW, image=img)

    #Switch voor de help functie
    def switch_help(self):
        #Wissel bool
        self.help_shown = not self.help_shown
        #Verander knoptekst
        self.help_btn.config(text=f"Help: {'aan' if self.help_shown else 'uit'}")
        #Herteken bord
        self.draw_board()

    #Update status van het spel
    def update_status(self):
        #Tel stenen voor beide spelers
        b = sum(row.count(self.BLUE) for  row in self.board)
        r = sum(row.count(self.RED) for row in self.board)
        #Update het tekstlabel
        self.count_label.config(text=f"Blauw: {b}   Rood: {r}")

        #Als er geen legale zet meer is, bepaal winnaar
        if not self.legal_moves(self.BLUE) and not self.legal_moves(self.RED):
            if b > r:
                status =  "Blauw is winnaar"
            elif r > b:
                status = "Rood is winnaar" 
            else:
                status = "Remise"
        else:
            #Laat zien wie er aan zet is
            s = "Blauw aan zet" if self.current_player==self.BLUE else "Rood aan zet"
        self.turn_label.config(text=f"Status: {status}") 




scherm = tk.Tk()
ReversiGame(scherm)
scherm.mainloop()
