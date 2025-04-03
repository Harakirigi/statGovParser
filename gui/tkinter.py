import tkinter as tk
from utils.get_api_link import *
root = tk.Tk()
root.geometry("600x400")
root.title("Stat.Gov Parser manager")

def show_input():
    parse_url = 'https://stat.gov.kz'
    response = get_request(parse_url)
    if response:
        res.config(text=f'Request to {parse_url} obtained successfully!\nNow you can choose ')
    else:
        res.config(text=f'Request to {parse_url} failed! Try again later')
        

# text = tk.Text(root, height=5, width=30)
# frame = tk.Frame(root, borderwidth=2, relief="groove")
# check = tk.Checkbutton(root, text="Agree", variable=var)
# radio = tk.Radiobutton(root, text="Option 1", variable=var, value=1)

label = tk.Label(root, text="In order to get access to the data of the stat.gov.kz website,\nyou have to establish the connection with it.\nTo do it click the button:")
label.pack()

# entry = tk.Entry(root, width=80)
# entry.pack()

button = tk.Button(root, text="Send request", command=show_input)
button.pack()

res = tk.Label(root)
res.pack()

