import tkinter as tk
from db.item_queries import fetch_items

def home_page():
    root = tk.Tk()
    root.title("Home")

    items = fetch_items()
    
    tk.Label(root, text="Items available:").grid(row=0, column=0)
    
    for idx, item in enumerate(items, start=1):
        tk.Label(root, text=f"{item[1]} - ${item[2]}").grid(row=idx, column=0)
    
    root.mainloop()
