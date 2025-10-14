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
     
