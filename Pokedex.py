import pypokedex
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import *
import urllib3 
from io import BytesIO

#The first thing you will see is a function called resize elements that is commented out. This is sort of the 
# Start on how to make the window adjust to the resizing on windows. In line 55, also commented out it says "window.bind("<Configure>", resize_elements)". 
# This says that when the windows action of resizing happens on the box, call the resize_elements function. Right now all it does is reduce the width by 2 for each element
# when uncommented. you need the function and the call for the function to work.
    
'''
# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)
'''
'''
def resize_elements(event):
     # Resize and reposition elements
    my_canvas.config(width=event.width, height=event.height)

    # Reposition elements based on the new window size
    my_canvas.coords(title_text, event.width / 2, 50)
    my_canvas.coords(subtitle_text, event.width / 2, 100)
    my_canvas.coords(pokemon_info, event.width / 2, 150)
    my_canvas.coords(pokemon_image, event.width / 2, event.height / 2)
    my_canvas.coords(pokemon_types, event.width / 2, 575)
    my_canvas.coords(pokemon_weight_height, event.width / 2, 625)
    my_canvas.coords(pokemon_basestats, event.width / 2, 675)
    my_canvas.coords(Pokemon_window, event.width / 2, 800)
    my_canvas.coords(load_btn_window, event.width / 2, 900)
'''

window = tk.Tk()
window.geometry("1000x1000")
window.resizable(width=False, height=False)

img_ref = None #this is to help with the image error

# Create Canvas
my_canvas = Canvas(window, width=1000, height=1000, bd=0, highlightthickness=0)
my_canvas.pack(fill="both", expand=True)

# Set background
bg = PhotoImage(file="images\Pokemon Background.png")
c = my_canvas.create_image(0, 0, image=bg, anchor="nw")

#Add title and subtitle
title_text = my_canvas.create_text(500, 50, text="National Pokedex", font=("Rockwell", 50), fill="white")
subtitle_text = my_canvas.create_text(500, 100, text="Created by JCPandaz", font=("Rockwell", 15), fill="red")

#Pokemon Information
pokemon_info = my_canvas.create_text(500, 150, text=f" ", font=("Rockwell", 50), fill= "black")
pokemon_image = my_canvas.create_image(500,400)
pokemon_types = my_canvas.create_text(500, 575, text=f" ", font=("Rockwell", 25), fill= "black")
pokemon_weight_height = my_canvas.create_text(500, 625, text=f" ", font=("Rockwell", 20), fill= "black")
pokemon_basestats = my_canvas.create_text(500, 675, text=f" ", font=("Rockwell", 15), fill= "black")

#load_pokemon v2 - getter function that retrieves Pokemon information
def load_pokemon():
    try: 
        pokemon = pypokedex.get(name=Pokemon_Entry.get())
        http = urllib3.PoolManager()
        response = http.request('GET', pokemon.sprites.front.get('default'))

        if response.status == 200:
            image = PIL.Image.open(BytesIO(response.data))
            resize_image = image.resize((300, 300))
            img = PIL.ImageTk.PhotoImage(resize_image)

            global img_ref
            img_ref = img

            my_canvas.itemconfig(pokemon_image, image=img)
            my_canvas.itemconfig(pokemon_info, text=f"{pokemon.dex} - {pokemon.name}".title())
            my_canvas.itemconfig(pokemon_types, text=" - ".join([t for t in pokemon.types]).title())
            my_canvas.itemconfig(pokemon_weight_height, text=f"Weight: {pokemon.weight}00 g - Height: {pokemon.height}0 cm")
            my_canvas.itemconfig(pokemon_basestats, text=f"HP: {pokemon.base_stats.hp} - Attack: {pokemon.base_stats.attack} - Defense: {pokemon.base_stats.defense} - Special Attack: {pokemon.base_stats.sp_atk} - Special Defense: {pokemon.base_stats.sp_def} - Speed: {pokemon.base_stats.speed}")
        else: 
            # Handle unsuccessful response
            my_canvas.itemconfig(pokemon_info, text="Failed to fetch Sprite.")
            print("Failed to fetch the image from the API")

    except pypokedex.exceptions.PyPokedexHTTPError as e: #this is the error message that this api returns if it didnt find the pokemon it was looking for
 
        error_message = "The requested Pokémon was not found!"
        my_canvas.itemconfig(pokemon_info, text=error_message, font=("Rockwell", 20), fill="red")
        print(e)

    except Exception as e: #if an error occurred and who on earth knows what it was, just tell the user an error occurred

        my_canvas.itemconfig(pokemon_info, text="An error occurred.", font=("Rockwell", 20), fill= "red")
        print(e)



#Adds Message
my_canvas.create_text(500, 750, text="Enter Name or Pokedex #", font=("Rockwell", 20), fill= "black")

#Add Entry box
Pokemon_Entry = Entry(window, font=("Rockwell", 24), width=15, fg="black", bd=2)
Pokemon_window=my_canvas.create_window(500,800, window=Pokemon_Entry)

#Add Button
Load_Button = Button(window, text= "LOAD POKEMON", font=("Rockwell", 20), width = 15, command =load_pokemon)
load_btn_window = my_canvas.create_window(500,900, window=Load_Button)
'''
#resize background function
def resizer(event):
    
    global bg1, resized_bg, new_bg
    #Open Image
    bg1 = PIL.Image.open("Pokemon Background.png")
    #resize
    resized_bg = bg1.resize((event.width, event.height))
    #Define image again
    new_bg = PIL.ImageTk.PhotoImage(resized_bg)
    #Add it back to canvas
    my_canvas.create_image(0,0, image =new_bg, anchor="nw")
    my_canvas.config(width=event.width, height=event.height)
'''
#window.bind("<Configure>", resizer)
#my_canvas.addtag_all("all")

window.mainloop()

