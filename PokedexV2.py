import pypokedex
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import *
import urllib3 
from io import BytesIO
from PIL import Image

img_ref = None #this is to help with the image error
global_image_list = [] # making an empty global image list
background_list = [] #not optimized but a solution to the background

#Dex Entry Window
class dexEntry(Toplevel):

    def __init__(Pokemon, master = None):
            
        super().__init__(master = master)
        Pokemon.geometry("512x364")
        Pokemon.resizable(width=False, height=False)
        
        # Create Window Canvas
        my_canvas = Canvas(Pokemon, width=512, height=364, bd=0, highlightthickness=0)
        my_canvas.pack(fill="both", expand=True)
        
        # Set Pokedex Entry background
        image = Image.open("images\Pokedex Screen.png")
        resize_image = image.resize((512, 364))
        img = PIL.ImageTk.PhotoImage(resize_image)
        c = my_canvas.create_image(0, 0, image=img, anchor="nw")
        
        def add_image_to_background_list(image):
            global background_list
            background_list.append(image)

        add_image_to_background_list(img)
        

        #Pokemon Information
        pokemon_info = my_canvas.create_text(375, 60, text=f" ", font=("Consolas", 12), fill= "black")
        global pokemon_image
        pokemon_image = my_canvas.create_image(150,152)
        pokemon_type = my_canvas.create_text(375, 95, text=f" ", font=("Consolas", 12))
        pokemon_height = my_canvas.create_text(395, 185, text=f" ", font=("Consolas", 12), fill= "black")
        pokemon_weight = my_canvas.create_text(395, 215, text=f" ", font=("Consolas", 12), fill= "black")
        pokemon_basestats1 = my_canvas.create_text(256, 280, text=f" ", font=("Consolas", 14), fill= "black", width=500)
        pokemon_basestats2 = my_canvas.create_text(256, 305, text=f" ", font=("Consolas", 14), fill= "black", width=500)
        pokemon_speed = my_canvas.create_text(256, 330, text=f" ", font=("Consolas", 14), fill= "black", width=400)
        error_message = my_canvas.create_text(256, 300, text=f" ", font=("Consolas", 12), fill= "red")

        def add_image_to_global_list(image):
            global global_image_list
            global_image_list.append(image)
    
        def load_pokemon(Pokemon_Entry):
            try: 
                pokemon = pypokedex.get(name=Pokemon_Entry.get())
                Pokemon.title(f"Pokedex Entry No.{pokemon.dex} - {pokemon.name}".title())
                http = urllib3.PoolManager()
                #get front sprite and display it
                response = http.request('GET', pokemon.sprites.front.get('default'))
                if response.status == 200:
                    image = PIL.Image.open(BytesIO(response.data))
                    resize_image = image.resize((200, 200))
                    global  front_img
                    front_img = PIL.ImageTk.PhotoImage(resize_image)
                    add_image_to_global_list(front_img)
                    my_canvas.itemconfig(pokemon_image, image=front_img)
                #get back sprite
                response = http.request('GET', pokemon.sprites.back.get('default'))
                if response.status == 200:
                    image2 = PIL.Image.open(BytesIO(response.data))
                    resize_image2 = image2.resize((200, 200))
                    global back_img
                    back_img = PIL.ImageTk.PhotoImage(resize_image2)
                    add_image_to_global_list(back_img)
                    
                    #function for turn sprite button
                    def switchsprite():
                        global direction
                        if direction == "front":
                            my_canvas.itemconfig(pokemon_image, image=back_img)
                            direction = "back"
                            return
                        if direction == "back":
                            my_canvas.itemconfig(pokemon_image, image =front_img)
                            direction = "front"
                            return
                        
                    #switch sprite button and indicator
                    global direction
                    direction = "front"
                    sprite_btn = Button(my_canvas, text= "TURN SPRITE", font=("Consolas", 8), width = 15, command=switchsprite)
                    back_sprite_btn_window = my_canvas.create_window(66,50, window=sprite_btn)

                    #function for displaying the Pokemon Type(s)
                    def Type_Colors():
                        #changing pokemon.types list of strings so that it is just words                        
                        poke_types = f"{pokemon.types}"
                        modified_list = poke_types.strip("[]").replace("'","").replace(", "," - ")

                        #18 pokemon types
                        primary_types = ["grass","poison","water","fire","normal","psychic","electric","fighting","bug",
                                         "fairy","dragon","ice","steel","rock","flying","ground","ghost","dark"]
                        # Color palette for each Pokemon type
                        color_palette = {"grass": "green","poison": "purple","water": "blue", "fire": "red", "normal": "gray","psychic": "violet red", "electric": "yellow",
                                         "fighting": "brown4", "bug": "yellow green", "fairy": "light pink", "dragon": "goldenrod", "ice": "cyan", "steel": "dim gray",
                                         "rock": "tan2", "flying": "Skyblue1", "ground": "sienna4", "ghost": "purple4", "dark": "midnight blue"}
                        #nested for loop, checking the type or dual-type of the pokemon, and assigning the text a color from the color pallette
                        for type1 in primary_types:
                            for type2 in primary_types:
                                if f"{type1}" == f"{modified_list}":
                                    primary_color = color_palette.get(type1)
                                    my_canvas.itemconfig(pokemon_type, fill=primary_color)
                                    my_canvas.itemconfig(pokemon_type, text=" - ".join([t for t in pokemon.types]).title())
                                    return
                                if f"{type1} - {type2}" == f"{modified_list}":
                                    primary_color = color_palette.get(type1)
                                    secondary_color = color_palette.get(type2)
                                    pokemon_type1 = my_canvas.create_text(330, 95, text=f" ", font=("Consolas", 12))
                                    my_canvas.itemconfig(pokemon_type1, text=f"{type1}".title(), fill=primary_color)
                                    pokemon_type2 = my_canvas.create_text(420, 95, text=f" ", font=("Consolas", 12))
                                    my_canvas.itemconfig(pokemon_type2, text=f"{type2}".title(), fill=secondary_color)
                                    return
                    
                        
                    #my_canvas.itemconfig(pokemon_image, image=front_img)
                    my_canvas.itemconfig(pokemon_info, text=f"No.{pokemon.dex} - {pokemon.name}".title())
                    Type_Colors()
                    my_canvas.itemconfig(pokemon_height, text=f"Height: {pokemon.height}0 cm")
                    my_canvas.itemconfig(pokemon_weight, text=f"Weight: {pokemon.weight}00 g")
                    my_canvas.itemconfig(pokemon_basestats1, text=f"HP: {pokemon.base_stats.hp} - Attack: {pokemon.base_stats.attack} - Defense: {pokemon.base_stats.defense}")
                    my_canvas.itemconfig(pokemon_basestats2, text=f"Special Attack: {pokemon.base_stats.sp_atk} - Special Defense: {pokemon.base_stats.sp_def}")
                    my_canvas.itemconfig(pokemon_speed, text=f"Speed: {pokemon.base_stats.speed}")
                else: 
                    # Handle unsuccessful response
                    my_canvas.itemconfig(error_message, text="Failed to fetch Pokemon from API.")
                    print("Failed to fetch the load Pokemon from the API")

            except pypokedex.exceptions.PyPokedexHTTPError as e: #this is the error message that this api returns if it didnt find the pokemon it was looking for
                Pokemon.title("MISSINGNO.")
                image = PIL.Image.open("images\MissingNo.png")
                resize_image = image.resize((200, 200))
                missingno_img = PIL.ImageTk.PhotoImage(resize_image)
                add_image_to_global_list(img)

                my_canvas.itemconfig(pokemon_info, text="MISSINGNO.")
                my_canvas.itemconfig(pokemon_image, image=missingno_img)
                my_canvas.itemconfig(pokemon_type, text="???? - ????")
                my_canvas.itemconfig(pokemon_height, text="Height: ????")
                my_canvas.itemconfig(pokemon_weight, text="Weight: ????")
                my_canvas.itemconfig(error_message, text="The requested Pokemon was not found. Please try again.", font= ("Consolas", 10))
                print(e)

            except Exception as e: #if an error occurred and who on earth knows what it was, just tell the user an error occurred
                image = PIL.Image.open("images\MissingNo.png")
                resize_image = image.resize((200, 200))
                missingno_img = PIL.ImageTk.PhotoImage(resize_image)
                add_image_to_global_list(img)

                my_canvas.itemconfig(pokemon_info, text="MISSINGNO.")
                my_canvas.itemconfig(pokemon_image, image=missingno_img)
                my_canvas.itemconfig(pokemon_type, text="???? - ????")
                my_canvas.itemconfig(pokemon_height, text="Height: ????")
                my_canvas.itemconfig(pokemon_weight, text="Weight: ????")
                my_canvas.itemconfig(error_message, text="An error occurred. Please Try Again.", font= ("Consolas", 10))
                print(e)

        load_pokemon(Pokemon_Entry)

#Home Screen
Home = tk.Tk()
Home.geometry("360x640")
Home.resizable(width=False, height=False)
Home.title("Python Pokedex")

# Create Main Window Canvas
main = Canvas(Home, width=360, height=640, bd=0, highlightthickness=0)
main.pack(fill="both", expand=True)

# Set Pokedex background
image = Image.open("images\Home.png")
resize_image = image.resize((360, 640))
img = PIL.ImageTk.PhotoImage(resize_image)
c = main.create_image(0, 0, image=img, anchor="nw")

#Add Texts
title_text = main.create_text(180, 290, text="Python Pokedex", font=("Consolas", 30), fill="black")
subtitle_text = main.create_text(180, 320, text="Created by JCPandaz", font=("Consolas", 15), fill="red")
main.create_text(180, 420, text="Enter Name or Pokedex #:", font=("Consolas", 15), fill= "black")
#Add Entry box
Pokemon_Entry = Entry(Home, font=("Consolas", 24), width=15, fg="black", bd=2)
Pokemon_window=main.create_window(180,460, window=Pokemon_Entry)
#Add Button
btn = Button(Home, text= "LOAD POKEMON", font=("Consolas", 20), width = 18, command = dexEntry)
load_btn_window = main.create_window(180,578, window=btn)

Home.mainloop()