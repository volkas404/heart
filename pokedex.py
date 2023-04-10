import requests
import tkinter.font
import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import json
class PokedexGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Pokedex")
        self.master.geometry("500x800+100+10")
        self.master.resizable(False, False)
        self.pokemon_image = None

        notebook = ttk.Notebook(self.master)
        notebook.pack(fill='both', expand=True)
        helv36 = tkinter.font.Font(family="Georgia",size=10,weight="bold")

        #Tìm kiếm pokemon
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text='Search Pokemon')

        self.search_label = ttk.Label(tab1, text="Choose a Pokemon:", font=helv36)
        self.search_label.pack(pady=5)

        self.pokemon_list = self.get_pokemon_list()
        self.search_combo = ttk.Combobox(tab1, values=self.pokemon_list, state="readonly",font=helv36)
        self.search_combo.pack(padx=5, pady=5)
        self.search_combo.bind(self.search_pokemon)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_pokemon_list)
        self.search_entry = ttk.Entry(tab1, textvariable=self.search_var,font=helv36)
        self.search_entry.pack(padx=5, pady=5)
        self.update_pokemon_list()

        self.search_button = ttk.Button(tab1, text="Search", command=self.search_pokemon)
        self.search_button.pack(padx=5, pady=5)

        self.pokemon_name = ttk.Label(tab1, text="",font=helv36)
        self.pokemon_name.pack(pady=5)

        self.pokemon_type = ttk.Label(tab1, text="",font=helv36)
        self.pokemon_type.pack(pady=5)

        self.pokemon_weight = ttk.Label(tab1, text="",font=helv36)
        self.pokemon_weight.pack(pady=5)

        self.pokemon_height = ttk.Label(tab1, text="",font=helv36)
        self.pokemon_height.pack(pady=5)

        self.pokemon_evolution = ttk.Label(tab1, text="",font=helv36)
        self.pokemon_evolution.pack(pady=5)

        self.pokemon_image_label = ttk.Label(tab1)
        self.pokemon_image_label.pack(pady=5)

        #Tìm kiếm tất cả chiêu thức của pokemon
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text='Search moves of Pokemon')
        self.search_label1 = ttk.Label(tab2, text="Choose a Pokemon:", font=helv36)
        self.search_label1.pack(pady=5)

        self.pokemon_list1 = self.get_pokemon_list()
        self.search_combo1 = ttk.Combobox(tab2, values=self.pokemon_list1, state="readonly",font=helv36)
        self.search_combo1.pack(padx=5, pady=5)
        self.search_combo1.bind(self.search_pokemon)

        self.search_var1= tk.StringVar()
        self.search_var1.trace("w", self.update_pokemon_list1)
        self.search_entry1 = ttk.Entry(tab2, textvariable=self.search_var1,font=helv36)
        self.search_entry1.pack(padx=5, pady=5)
        self.update_pokemon_list1()

        self.search_button1 = ttk.Button(tab2, text="Search", command=self.show_moves)
        self.search_button1.pack(padx=5, pady=5)
        self.move_list = tk.Listbox(tab2,font=helv36,height=30)
        self.move_list.pack()

        #Tìm kiếm chiêu thức
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text='Search moves')
        self.search_label2 = ttk.Label(tab3, text="Choose a Pokemon:", font=helv36)
        self.search_label2.pack(pady=5)

        self.pokemon_list2 = self.get_pokemon_list()
        self.search_combo2 = ttk.Combobox(tab3, values=self.move_list, state="readonly",font=helv36)
        self.search_combo2.pack(padx=5, pady=5)
        self.search_combo2.bind(self.search_move)

        self.search_var2= tk.StringVar()
        self.search_var2.trace("w", self.update_pokemon_list1)
        self.search_entry2 = ttk.Entry(tab3, textvariable=self.search_var2,font=helv36)
        self.search_entry2.pack(padx=5, pady=5)
        self.update_move_list()

        self.search_button2 = ttk.Button(tab3, text="Search", command=self.search_move)
        self.search_button2.pack(padx=5, pady=5)

    def get_move_list(self):
        url = "https://pokeapi.co/api/v2/move/?offset=0&limit=2000"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            move_list = [pokemon["name"].capitalize() for pokemon in data["results"]]
            return move_list
        else:
            return []
    def update_move_list(self, *args):
        search_term = self.search_var2.get()
        if search_term:
            search_results2 = [move for move in self.move_list if search_term.lower() in move.lower()]
            self.search_combo2.config(values=search_results2)
        else:
            self.search_combo2.config(values=self.move_list)
    def search_move(self):
        move_name = self.search_combo2.get()
        url = f"https://pokeapi.co/api/v2/move/{move_name.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

    def get_pokemon_list(self):
        url = "https://pokeapi.co/api/v2/pokemon?limit=1118"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pokemon_list = [pokemon["name"].capitalize() for pokemon in data["results"]]
            return pokemon_list
        else:
            return []
    def update_pokemon_list(self, *args):
        search_term = self.search_var.get()
        if search_term:
            search_results = [pokemon for pokemon in self.pokemon_list if search_term.lower() in pokemon.lower()]
            self.search_combo.config(values=search_results)
        else:
            self.search_combo.config(values=self.pokemon_list)
    def update_pokemon_list1(self, *args):
        search_term = self.search_var1.get()
        if search_term:
            search_results1 = [pokemon for pokemon in self.pokemon_list1 if search_term.lower() in pokemon.lower()]
            self.search_combo1.config(values=search_results1)
        else:
            self.search_combo1.config(values=self.pokemon_list1)

    def search_pokemon(self):
        pokemon_name = self.search_combo.get()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pokemon_name = data["name"].capitalize()
            pokemon_id = data["id"]
            pokemon_types = ", ".join([t["type"]["name"].capitalize() for t in data["types"]])
            pokemon_weight = data["weight"] / 10.0
            pokemon_height = data["height"] / 10.0
            pokemon_image_url = data["sprites"]["other"]["official-artwork"]["front_default"]
            image = Image.open(requests.get(pokemon_image_url, stream=True).raw)
            self.pokemon_name.config(text=f"{pokemon_name} #{pokemon_id}")
            self.pokemon_type.config(text=f"Type: {pokemon_types}")
            self.pokemon_weight.config(text=f"Weight: {pokemon_weight} kg")
            self.pokemon_height.config(text=f"Height: {pokemon_height} m")
            self.pokemon_image = ImageTk.PhotoImage(image)
            self.pokemon_image_label.config(image=self.pokemon_image)
            
            evolution_chain_url = data["species"]["url"]
            evolution_chain_response = requests.get(evolution_chain_url)
            if evolution_chain_response.status_code == 200:
                evolution_chain_data = evolution_chain_response.json()
                evolution_chain_id = evolution_chain_data["evolution_chain"]["url"].split("/")[-2]
                evolution_chain_url = f"https://pokeapi.co/api/v2/evolution-chain/{evolution_chain_id}"
                evolution_chain_response = requests.get(evolution_chain_url)
                if evolution_chain_response.status_code == 200:
                    evolution_chain_data = evolution_chain_response.json()
                    evolution_chain = [evolution_chain_data["chain"]["species"]["name"].capitalize()]
                    if evolution_chain_data["chain"]["evolves_to"]:
                        for evo in evolution_chain_data["chain"]["evolves_to"]:
                            evolution_chain.append(evo["species"]["name"].capitalize())
                            if evo["evolves_to"]:
                                for evo2 in evo["evolves_to"]:
                                    evolution_chain.append(evo2["species"]["name"].capitalize())
                    self.pokemon_evolution.config(text=f"Evolution: {' -> '.join(evolution_chain)}")
                else:
                    self.pokemon_evolution.config(text="No evolution information.")
            else:
                self.pokemon_evolution.config(text="No evolution information.")

        else:
            self.pokemon_name.config(text="Pokemon not found.")
            self.pokemon_type.config(text="")
            self.pokemon_weight.config(text="")
            self.pokemon_height.config(text="")
            self.pokemon_evolution.config(text="")
            self.pokemon_image_label.config(image="")

    def show_moves(self):
        pokemon_name = self.search_combo1.get()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            moves = [move['move']['name'] for move in data['moves']]
            self.move_list.delete(0, 'end')
            i = 0
            for move in moves:
                self.move_list.insert(i, move)
                i = i+1
                
root = tk.Tk()
pokedex_gui = PokedexGUI(root)
root.mainloop()
