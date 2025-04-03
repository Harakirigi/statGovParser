import tkinter as tk
from utils.get_api_link import *

root = tk.Tk()
root.geometry("600x400+600+200")
# root.configure(bg='lightblue')
root.title("Stat.Gov Parser Manager")

icon = tk.PhotoImage(file='gui/icon.png')
root.iconphoto(True, icon)


frame = tk.Frame(root, bg="black", padx=20, pady=20)
frame.pack(padx=20, pady=20)

def show_input():
    parse_url = 'https://stat.gov.kz'
    response = get_request(parse_url)

    if response:
        welcome.destroy()
        send_request.destroy()

        global success
        success = tk.Label(root, text=f'Request to {parse_url} has been sent successfully!', fg='green')
        success.pack()

        global call_action
        call_action = tk.Label(root, text='Now you can choose the category')
        call_action.pack()

        global download_button
        download_button = tk.Button(root, text="Download", command=download)
        download_button.pack(padx=10, pady=15)
    else:
        fail = tk.Label(root, text=f'Request to {parse_url} failed! Try again later', fg='red')
        fail.pack()

        exit_btn = tk.Button(root, text="Exit", command=root.quit, padx=10)
        exit_btn.pack(padx=10, pady=15)


def download():
    res_2 = tk.Label(root, text='Downloading...', fg='green')
    res_2.pack()

    download_all()
    res_2.config(text='Everything downloaded successfully!')

    success.destroy()
    call_action.destroy()
    download_button.destroy()

    exit_btn = tk.Button(root, text="Exit", command=root.quit, padx=10)
    exit_btn.pack(padx=10, pady=15)

        

# text = tk.Text(root, height=5, width=30)
# frame = tk.Frame(root, borderwidth=2, relief="groove")
# check = tk.Checkbutton(root, text="Agree", variable=var)
# radio = tk.Radiobutton(root, text="Option 1", variable=var, value=1)

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=show_input)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

welcome = tk.Label(root, text="Send request to the stat.gov.kz to access the parser:")
welcome.pack()

send_request = tk.Button(root, text="Send request", command=show_input)
send_request.pack(padx=10, pady=15)
# entry = tk.Entry(root, width=80)
# entry.pack()

