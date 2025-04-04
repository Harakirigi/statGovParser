import tkinter as tk
from utils.get_api_link import *
from draft.draft2 import show_categories

root = tk.Tk()
root.geometry("600x400+600+200")
# frame.configure(bg='lightblue')
root.title("Stat.Gov Parser Manager")

# icon = tk.PhotoImage(file='gui/icon.png')
# frame.iconphoto(True, icon)

btns_dict = {}

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

def start():
    parse_url = 'https://stat.gov.kz/en/'
    response = get_request(parse_url)

    if response:
        welcome.destroy()
        send_request.destroy()

        global success
        success = tk.Label(frame, text=f'Request to {parse_url} has been sent successfully!', fg='green')
        success.pack()

        global call_action
        call_action = tk.Label(frame, text='Now you can choose the category')
        call_action.pack()

        economics_btn = tk.Button(frame, text='Econimics', command=lambda: create_buttons(parse_url, 'Economics'))
        economics_btn.pack(padx=10, pady=10, side="top")
        social_btn = tk.Button(frame, text='Social statistics', command=lambda: create_buttons(parse_url, 'Social statistics'))
        social_btn.pack(padx=10, pady=10, side="top")
        industry_btn = tk.Button(frame, text='Industry statistics', command=lambda: create_buttons(parse_url, 'Industry statistics'))
        industry_btn.pack(padx=10, pady=10, side="top")
        income_btn = tk.Button(frame, text='Labor and income', command=lambda: create_buttons(parse_url, 'Labor and income'))
        income_btn.pack(padx=10, pady=10, side="top")
        environment_btn = tk.Button(frame, text='Environment', command=lambda: create_buttons(parse_url, 'Environment'))
        environment_btn.pack(padx=10, pady=10, side="top")
        

        # global download_button
        # download_button = tk.Button(frame, text="Download", command=download)
        # download_button.pack(padx=10, pady=15)
    else:
        fail = tk.Label(frame, text=f'Request to {parse_url} failed! Try again later', fg='red')
        fail.pack()

        exit_btn = tk.Button(frame, text="Exit", command=frame.quit, padx=10)
        exit_btn.pack(padx=10, pady=15)


def download():
    res_2 = tk.Label(frame, text='Downloading...', fg='green')
    res_2.pack()

    download_all()
    res_2.config(text='Everything downloaded successfully!')

    success.destroy()
    call_action.destroy()
    # download_button.destroy()

    exit_btn = tk.Button(frame, text="Exit", command=frame.quit, padx=10)
    exit_btn.pack(padx=10, pady=15)


def create_buttons(parse_url, category_name):
    try:
        for btn in btns_dict:
            btns_dict[btn].destroy()
    except NameError:
        pass

    btns = show_categories(parse_url, category_name)

    for i, btn_text in enumerate(btns):
        btn_name = f"btn_{i+1}"
        btns_dict[btn_name] = tk.Button(frame, text=btn_text)
        btns_dict[btn_name].pack(padx=10, pady=10)

    back_btn = tk.Button(frame, text='Back', command=start).pack(padx=10, pady=10)
    btns_dict["back_btn"] = back_btn

# text = tk.Text(frame, height=5, width=30)
# frame = tk.Frame(frame, borderwidth=2, relief="groove")
# check = tk.Checkbutton(frame, text="Agree", variable=var)
# radio = tk.Radiobutton(frame, text="Option 1", variable=var, value=1)

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=start)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=frame.quit)

welcome = tk.Label(frame, text="Send request to the stat.gov.kz to access the parser:")
welcome.pack()

send_request = tk.Button(frame, text="Send request", command=start)
send_request.pack(padx=10, pady=15)
# entry = tk.Entry(frame, width=80)
# entry.pack()

