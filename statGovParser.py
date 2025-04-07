import tkinter as tk
from gui import root

base_url = "https://stat.gov.kz"
url = "https://stat.gov.kz/en/industries/economy/prices/dynamic-tables/"

icon = tk.PhotoImage(file='./static/icon.png')
root.iconphoto(True, icon)

root.mainloop()
