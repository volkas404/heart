import requests
import tkinter.font
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox as messagebox
import mysql.connector
class PokedexGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Pokedex")
        self.master.geometry("800x800+100+10")
        self.master.resizable(False, False)
        style = ttk.Style()
        self.pokemon_image = None
        mydb=DB()
        notebook = ttk.Notebook(self.master)
        style.configure('TNotebook.Tab', font=('Arial','13','bold'), padding=[6, 6])
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

        style.configure("small.TButton", font=('Arial', 15), foreground="red")
        self.love_button = ttk.Button(tab1, text="Love pokemon", command=self.love_pokemon, style="small.TButton")
        self.love_button.place(x=50,y=50)

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

        self.pokemon_image_label1 = ttk.Label(tab2)
        self.pokemon_image_label1.pack(pady=5)

        self.move_list = tk.Listbox(tab2,font=helv36,height=20)
        self.move_list.pack()

        #Tìm kiếm chiêu thức
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text='Search moves')
        self.search_label2 = ttk.Label(tab3, text="Choose a moves:", font=helv36)
        self.search_label2.pack(pady=5)

        self.move_list1 = self.get_move_list()
        self.search_combo2 = ttk.Combobox(tab3, values=self.move_list1, state="readonly",font=helv36)
        self.search_combo2.pack(padx=5, pady=5)
        self.search_combo2.bind(self.search_move)

        self.search_var2= tk.StringVar()
        self.search_var2.trace("w", self.update_move_list)
        self.search_entry2 = ttk.Entry(tab3, textvariable=self.search_var2,font=helv36)
        self.search_entry2.pack(padx=5, pady=5)
        self.update_move_list()

        self.search_button2 = ttk.Button(tab3, text="Search", command=self.search_move)
        self.search_button2.pack(padx=5, pady=5)
        
        self.type = ttk.Label(tab3, text="",font=helv36)
        self.type.pack(pady=5)
        self.damage_class = ttk.Label(tab3, text="",font=helv36)
        self.damage_class.pack(pady=5)
        self.accuracy = ttk.Label(tab3, text="",font=helv36)
        self.accuracy.pack(pady=5)
        self.power = ttk.Label(tab3, text="",font=helv36)
        self.power.pack(pady=5)
        self.pp = ttk.Label(tab3, text="",font=helv36)
        self.pp.pack(pady=5)
        self.effect = ttk.Label(tab3, text="",font=helv36,wraplength=400)
        self.effect.pack(pady=5)

        #Danh sách yêu thích
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text='Favorite pokemons')
        style.configure("Treeview", font=helv36)
        self.my_tree = ttk.Treeview(tab4, style="Treeview")
        self.scrollbar = ttk.Scrollbar(tab4, orient="vertical", command=self.my_tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.my_tree.configure(yscrollcommand=self.scrollbar.set)
        self.my_tree['columns'] = ('Column 1', 'Column 2')

        self.my_tree.column('#0', width=0, stretch="NO")
        self.my_tree.column('Column 1', anchor="center", width=100)
        self.my_tree.column('Column 2', anchor="center", width=100)

        self.my_tree.heading('#0', text='', anchor="center")
        self.my_tree.heading('Column 1', text='Pokemon name', anchor="center")
        self.my_tree.heading('Column 2', text='Type', anchor="center")
        self.mycursor = mydb.cursor()

        self.mycursor.execute("SELECT * FROM love_pokemon")
        for row in self.mycursor:
            self.my_tree.insert(parent='', index='end', values=(row[0], row[1]))

        self.my_tree.pack(fill="both", expand=True)
        
        def update_tab(event):
            current_tab = event.widget.nametowidget(event.widget.select())
            if current_tab == tab4:
                self.my_tree.delete(*self.my_tree.get_children())
                tab4db = mysql.connector.connect(
                host="localhost",
                user="pkm",
                password="123456",
                database="pokemon"
                )
                mycursor = tab4db.cursor()
                mycursor.execute("SELECT * FROM love_pokemon")
                for row in mycursor:
                    self.my_tree.insert(parent='', index='end', values=(row[0], row[1]))
        notebook.bind("<<NotebookTabChanged>>", update_tab)

        #Cài đặt
        tab5 = ttk.Frame(notebook)
        notebook.add(tab5, text='Setting')
        style.configure("big.TButton", font=(None, 20), foreground="red")
        self.contact_button = ttk.Button(tab5, text="Contact", style="big.TButton", command=self.show_contact)
        self.contact_button.pack(padx=5, pady=20)
        self.contact_button.configure(padding=(40, 10))
        self.info_button = ttk.Button(tab5, text="Info", style="big.TButton", command=self.show_info)
        self.info_button.pack(padx=5, pady=20)
        self.info_button.configure(padding=(40, 10))
        self.rules_button = ttk.Button(tab5, text="Terms of Use", style="big.TButton", command=self.show_rules)
        self.rules_button.pack(padx=5, pady=20)
        self.rules_button.configure(padding=(40, 10))
        self.Exit_button = ttk.Button(tab5, text="Exit", style="big.TButton", command=self.master.destroy)
        self.Exit_button.pack(padx=5, pady=20)
        self.Exit_button.configure(padding=(40, 10))
        
    def show_contact(self):
        contact_window = tk.Toplevel(root)
        contact_window.title("Contact")
        contact_window.geometry("700x200+150+100")
        contact_window.resizable(False, False)
        info_label = tk.Label(contact_window, text="App name: Pokedex \nAddress: 273 An Duong Vuong, Ward 3, District 5, Ho Chi Minh City \nPhone: 0862419307 \nEmail: aefdcv@gmail.com \nGithub: https://github.com/volkas404", font=("Arial", 15))
        info_label.pack(pady=20)

    def show_info(self):
        info_window = tk.Toplevel(root)
        info_window.title("Info")
        info_window.geometry("700x600+150+100")
        info_window.resizable(False, False)
        info_label = tk.Label(info_window, text="Pokedex is a mobile application that allows users to search for information about different Pokemon species. With hundreds of different Pokemon species, each with unique characteristics, finding information about them can be very difficult. However, with Pokedex, users can easily search for information about all Pokemon species, from information about height, weight, type, to attack moves and illustrations.",font=("Arial", 15), wraplength=600)
        info_label.pack(pady=10)
        info_label1 = tk.Label(info_window, text="The features of the Pokedex app include:",font=("Arial", 15))
        info_label1.pack(pady=10)
        info_label2 = tk.Label(info_window, text="Search for information about all Pokemon species: Users can search for information about all Pokemon species by entering their names in the search bar.",font=("Arial", 15), wraplength=600)
        info_label2.pack(pady=10)
        info_label3 = tk.Label(info_window, text="Detailed information about each Pokemon species: Each Pokemon species has a separate information page with complete information about its characteristics, illustrations, and attack moves.",font=("Arial", 15), wraplength=600)
        info_label3.pack(pady=10)
        info_label4 = tk.Label(info_window, text="Save favorite species list: Users can save a list of their favorite Pokemon species for easy access later.",font=("Arial", 15), wraplength=600)
        info_label4.pack(pady=10)
        info_label5 = tk.Label(info_window, text="With Pokedex, searching for information about Pokemon species becomes easier and more convenient than ever. This application is considered one of the best apps for fans of the Pokemon world.",font=("Arial", 15), wraplength=600)
        info_label5.pack(pady=10)

    def show_rules(self):
        rules_window = tk.Toplevel(root)
        rules_window.title("Rules")
        rules_window.geometry("700x760+150+20")
        rules_window.resizable(False, False)
        rules_label = tk.Label(rules_window, text="Terms of Use for Pokedex Application:",font=("Arial", 20), wraplength=600)
        rules_label.pack(pady=1)
        rules_label1 = tk.Label(rules_window, text="1.Purpose of Use:",font=("Arial", 15))
        rules_label1.pack(pady=1)
        rules_label11 = tk.Label(rules_window, text="Pokedex is an application for users to search for information about Pokemon species.",font=("Arial", 15), wraplength=600)
        rules_label11.pack(pady=1)
        rules_label2 = tk.Label(rules_window, text="2.Ownership:",font=("Arial", 15), wraplength=600)
        rules_label2.pack(pady=1)
        rules_label21 = tk.Label(rules_window, text="Pokedex is a product of the application development company.",font=("Arial", 15), wraplength=600)
        rules_label21.pack(pady=1)
        rules_label22 = tk.Label(rules_window, text="All intellectual property rights related to Pokedex belong to the application development company.",font=("Arial", 15), wraplength=600)
        rules_label22.pack(pady=1)
        rules_label3 = tk.Label(rules_window, text="3.Limitations of Use:",font=("Arial", 15), wraplength=600)
        rules_label3.pack(pady=1)
        rules_label31 = tk.Label(rules_window, text="Users are allowed to use Pokedex to search for information about Pokemon species. \nUsers are not allowed to copy, distribute, or use Pokedex for commercial purposes.",font=("Arial", 15), wraplength=600)
        rules_label31.pack(pady=1)
        rules_label4 = tk.Label(rules_window, text="4.Information Security:",font=("Arial", 15), wraplength=600)
        rules_label4.pack(pady=1)
        rules_label41 = tk.Label(rules_window, text="The application development company commits to ensuring the security of user information.",font=("Arial", 15), wraplength=600)
        rules_label41.pack(pady=1)
        rules_label5 = tk.Label(rules_window, text="5.Changes to Terms:",font=("Arial", 15), wraplength=600)
        rules_label5.pack(pady=1)
        rules_label51 = tk.Label(rules_window, text="The application development company reserves the right to change the terms of use of Pokedex without prior notice.\nUsers must review and agree to these changes before continuing to use Pokedex.",font=("Arial", 15), wraplength=600)
        rules_label51.pack(pady=1)
        rules_label6 = tk.Label(rules_window, text="6.Termination of Use:",font=("Arial", 15), wraplength=600)
        rules_label6.pack(pady=1)
        rules_label61 = tk.Label(rules_window, text="Users have the right to terminate the use of Pokedex at any time.",font=("Arial", 15), wraplength=600)
        rules_label61.pack(pady=1)
        rules_label62 = tk.Label(rules_window, text="The application development company has the right to terminate the provision of Pokedex to users if it discovers a violation of the terms of use.",font=("Arial", 15), wraplength=600)
        rules_label62.pack(pady=1)

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
            search_results2 = [move for move in self.move_list1 if search_term.lower() in move.lower()]
            self.search_combo2.config(values=search_results2)
        else:
            self.search_combo2.config(values=self.move_list1)
    def search_move(self):
        move_name = self.search_combo2.get()
        url = f"https://pokeapi.co/api/v2/move/{move_name.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            type = data["type"]["name"]
            damage_class = data["damage_class"]["name"]
            accuracy = data["accuracy"]
            pp = data["pp"]
            power = data["power"]
            effect = data["effect_entries"][0]["effect"]
            self.type.config(text=f"Type: {type}")
            self.damage_class.config(text=f"Damage class: {damage_class}")
            self.accuracy.config(text=f"Accuracy: {accuracy}")
            self.pp.config(text=f"PP: {pp}")
            self.power.config(text=f"Power: {power}")
            self.effect.config(text=f"Effect: {effect}")

    def love_pokemon(self):
        mydb = DB()
        mycursor = mydb.cursor()

        # Kiểm tra xem pokemon đã tồn tại trong bảng hay chưa
        select_sql = "SELECT * FROM love_pokemon WHERE name = %s AND type = %s"
        select_val = (self.pokemon_name.cget("text"), self.pokemon_type.cget("text"))
        mycursor.execute(select_sql, select_val)
        result = mycursor.fetchone()
        
        # Nếu pokemon chưa tồn tại, thêm mới vào bảng
        if result is None:
            insert_sql = "INSERT INTO love_pokemon (name, type) VALUES (%s, %s)"
            type = self.pokemon_type.cget("text")
            typecut = type.split(": ")
            insert_val = (self.pokemon_name.cget("text"), typecut[1])
            mycursor.execute(insert_sql, insert_val)
            mydb.commit()
            messagebox.showinfo("Thông báo", "Success!")
        else:
            messagebox.showinfo("Thông báo", "Error, pokemon is exist!")

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
            new_size = (400, 400)
            resized_image = image.resize(new_size)
            self.pokemon_name.config(text=f"{pokemon_name} #{pokemon_id}")
            self.pokemon_type.config(text=f"Type: {pokemon_types}")
            self.pokemon_weight.config(text=f"Weight: {pokemon_weight} kg")
            self.pokemon_height.config(text=f"Height: {pokemon_height} m")
            self.pokemon_image = ImageTk.PhotoImage(resized_image)
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
            pokemon_image_url = data["sprites"]["other"]["official-artwork"]["front_default"]
            image = Image.open(requests.get(pokemon_image_url, stream=True).raw)
            new_size = (250, 250)
            resized_image = image.resize(new_size)
            self.pokemon_image1 = ImageTk.PhotoImage(resized_image)
            self.pokemon_image_label1.config(image=self.pokemon_image1)
            moves = [move['move']['name'] for move in data['moves']]
            self.move_list.delete(0, 'end')
            i = 0
            for move in moves:
                self.move_list.insert(i, move)
                i = i+1
            
def DB():
    # Thiết lập kết nối với CSDL
    mydb = mysql.connector.connect(
    host="localhost",       # địa chỉ máy chủ MySQL
    user="pkm",            # tên đăng nhập vào MySQL
    password="123456",            # mật khẩu để truy cập MySQL
    database="pokemon"   # tên của database
    )
    return mydb
root = tk.Tk()
pokedex_gui = PokedexGUI(root)
root.mainloop()
