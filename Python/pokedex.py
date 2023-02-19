import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class PokedexGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Pokedex")
        self.master.geometry("1080x720+10+10")
        self.master.resizable(False, False)
        
        self.pokemon_image = None

        # Create GUI elements
        self.search_label = ttk.Label(self.master, text="Enter a Pokemon name or number:")
        self.search_label.pack(pady=10)

        self.search_entry = ttk.Entry(self.master)
        self.search_entry.pack(padx=10, pady=5)

        self.search_button = ttk.Button(self.master, text="Search", command=self.search_pokemon)
        self.search_button.pack(padx=10, pady=5)

        self.pokemon_name = ttk.Label(self.master, text="")
        self.pokemon_name.pack(pady=10)

        self.pokemon_type = ttk.Label(self.master, text="")
        self.pokemon_type.pack(pady=10)

        self.pokemon_weight = ttk.Label(self.master, text="")
        self.pokemon_weight.pack(pady=10)

        self.pokemon_height = ttk.Label(self.master, text="")
        self.pokemon_height.pack(pady=10)

        self.pokemon_image_label = ttk.Label(self.master)
        self.pokemon_image_label.pack(pady=10)

    def search_pokemon(self):
        pokemon_name = self.search_entry.get()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pokemon_name = data["name"].capitalize()
            pokemon_types = ", ".join([t["type"]["name"].capitalize() for t in data["types"]])
            pokemon_weight = data["weight"] / 10.0
            pokemon_height = data["height"] / 10.0
            pokemon_image_url = data["sprites"]["other"]["official-artwork"]["front_default"]
            image = Image.open(requests.get(pokemon_image_url, stream=True).raw)
            self.pokemon_name.config(text=f"{pokemon_name}")
            self.pokemon_type.config(text=f"Type: {pokemon_types}")
            self.pokemon_weight.config(text=f"Weight: {pokemon_weight} kg")
            self.pokemon_height.config(text=f"Height: {pokemon_height} m")
            self.pokemon_image = ImageTk.PhotoImage(image)
            self.pokemon_image_label.config(image=self.pokemon_image)
        else:
            self.pokemon_name.config(text="Pokemon not found.")
            self.pokemon_type.config(text="")
            self.pokemon_weight.config(text="")
            self.pokemon_height.config(text="")
            self.pokemon_image_label.config(image="")

root = tk.Tk()
pokedex_gui = PokedexGUI(root)
root.mainloop()
