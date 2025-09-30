import tkinter as tk
from tkinter import ttk

class SkolmatApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Skolmat")
        self.root.geometry("720x420")
        
        self.dagar = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]
        self.mat = {
            "vanlig": ["Köttbullar", "Fish & chips", "Pannkakor", "Pasta", "Pytt i panna"],
            "vegan": ["Sojabullar", "Tofu & pommes", "Havrepannkakor", "Pasta vegan", "Quinoapytt"]
        }
        
        # GUI
        ttk.Label(self.root, text="Välj dag:").pack(pady=5)
        
        self.dag_var = tk.StringVar(value=self.dagar[0])
        ttk.Combobox(self.root, textvariable=self.dag_var, 
                    values=self.dagar, state="readonly").pack()
        
        self.vegan_var = tk.BooleanVar()
        ttk.Checkbutton(self.root, text="Vegan", 
                       variable=self.vegan_var).pack()
        
        self.visa_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.visa_label.pack(pady=20)
        
        # Bind events
        self.dag_var.trace('w', self.uppdatera)
        self.vegan_var.trace('w', self.uppdatera)
        
        self.uppdatera()
    
    def uppdatera(self, *args):
        dag_index = self.dagar.index(self.dag_var.get())
        typ = "vegan" if self.vegan_var.get() else "vanlig"
        matratt = self.mat[typ][dag_index]
        
        self.visa_label.config(
            text=matratt + (" 🌱" if self.vegan_var.get() else ""),
            bg="lightgreen" if self.vegan_var.get() else "lightyellow"
        )
    
    def starta(self):
        self.root.mainloop()

app = SkolmatApp()
app.starta()