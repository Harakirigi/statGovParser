import tkinter as tk
from tkinter import ttk
import time
from utils.parser import *

# region Config

root = tk.Tk()
root.geometry("800x600+600+200")
root.title("Stat.Gov Parser Manager")
# icon = tk.PhotoImage(file='../static/icon.png')
# root.iconphoto(True, icon)

PARSE_URL = 'https://stat.gov.kz/en/'
SOUP = None


# endregion


# region Actions

def send_request(SOUP=None, progress=True):
    if not SOUP:
        if progress: show_progress()
        SOUP = get_request(PARSE_URL)

    if not SOUP:
        clear_window()

        fail_page = tk.Frame(root)
        fail_page.pack(pady=10)

        fail_label = tk.Label(fail_page, text=f'Request to {PARSE_URL} failed! Try again later', fg='red')
        fail_label.pack(pady=5, padx=5)
        
        back_btn = tk.Button(fail_page, text='Try again', command=send_request)
        back_btn.pack(padx=10, pady=10)

        exit_btn = tk.Button(fail_page, text="Exit", command=root.quit, padx=10)
        exit_btn.pack(pady=5, padx=5)

        return print('Error in send_request function')

    try:
        clear_window()

        success_page = tk.Frame(root)
        success_page.pack(pady=10)

        success_label = tk.Label(success_page, text=f'Request to {PARSE_URL} has been sent successfully!', fg='green')
        success_label.pack(pady=5, padx=5)
        choose_label = tk.Label(success_page, text='Now you can choose the category you want to parse')
        choose_label.pack(pady=5, padx=5)

        economics_btn = tk.Button(success_page, text='Economics', command=lambda: create_buttons(SOUP, 'Economics'))
        economics_btn.pack(padx=10, pady=10, side="top")
        social_btn = tk.Button(success_page, text='Social statistics', command=lambda: create_buttons(SOUP, 'Social statistics'))
        social_btn.pack(padx=10, pady=10, side="top")
        industry_btn = tk.Button(success_page, text='Industry statistics', command=lambda: create_buttons(SOUP, 'Industry statistics'))
        industry_btn.pack(padx=10, pady=10, side="top")
        income_btn = tk.Button(success_page, text='Labor and income', command=lambda: create_buttons(SOUP, 'Labor and income'))
        income_btn.pack(padx=10, pady=10, side="top")
        environment_btn = tk.Button(success_page, text='Environment', command=lambda: create_buttons(SOUP, 'Environment'))
        environment_btn.pack(padx=10, pady=10, side="top")
        all_btn = tk.Button(success_page, text='All', command=lambda: download(SOUP, 'All', 'All', all=True), font=("TkDefaultFont", 8, 'bold'))
        all_btn.pack(padx=10, pady=10, side="top")

        return
    
    except Exception as e:
        clear_window()

        fail_page = tk.Frame(root)
        fail_page.pack(pady=10)

        fail_label = tk.Label(fail_page, text=f'Request to {PARSE_URL} failed! Try again later', fg='red')
        fail_label.pack(pady=5, padx=5)
        
        back_btn = tk.Button(fail_page, text='Try again', command=send_request)
        back_btn.pack(padx=10, pady=10)

        exit_btn = tk.Button(fail_page, text="Exit", command=root.quit, padx=10)
        exit_btn.pack(pady=5, padx=5)

        return print(f'Error in send_request function: {e}')


def create_buttons(SOUP, category_name):
    try:
        clear_window()
        category_page = tk.Frame(root)
        category_page.pack(pady=5, padx=5)

        btns = get_category(SOUP, category_name)

        category_label = tk.Label(category_page, text=f'Subcategories of {category_name} category', font=("TkDefaultFont", 10, 'bold'))
        category_label.pack(pady=5, padx=5)

        for i, btn_text in enumerate(btns):
            btn_name = f"btn_{i+1}"
            btn_name = tk.Button(category_page, text=btn_text, command=lambda: download(SOUP, category_name, btn_text, all=False))
            btn_name.pack(pady=5, padx=5)
        
        all_btn = tk.Button(category_page, text='Download all above', command=lambda: download(SOUP, category_name, 'All', all=True), font=("TkDefaultFont", 8, 'bold'))
        all_btn.pack(pady=5, padx=5)

        back_btn = tk.Button(category_page, text='Back', command=lambda: send_request(SOUP=SOUP, progress=False))
        back_btn.pack(pady=5, padx=5)
    except:
        clear_window()
        fail_label = tk.Label(root, text=f'Something went wrong, please try later', fg='red')
        fail_label.pack(pady=5, padx=5)
        back_btn = tk.Button(root, text='Back', command=lambda: send_request(SOUP=SOUP, progress=False))
        back_btn.pack(pady=5, padx=5)




# region Util Functions

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def show_progress():
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
    progress_bar.pack(pady=10)
    label = tk.Label(root, text="Processing...")
    label.pack(pady=20)

    for i in range(101):
        time.sleep(0.001)
        progress_var.set(i)
        root.update_idletasks()



# endregion



# def download():
#     res_2 = tk.Label(frame, text='Downloading...', fg='green')
#     res_2.pack()

#     download_all()
#     res_2.config(text='Everything downloaded successfully!')

#     success.destroy()
#     call_action.destroy()
#     # download_button.destroy()

#     exit_btn = tk.Button(frame, text="Exit", command=frame.quit, padx=10)
#     exit_btn.pack(padx=10, pady=15)


# text = tk.Text(frame, height=5, width=30)
# frame = tk.Frame(frame, borderwidth=2, relief="groove")
# check = tk.Checkbutton(frame, text="Agree", variable=var)
# radio = tk.Radiobutton(frame, text="Option 1", variable=var, value=1)


# region Request Page

request_page = tk.Frame(root)
request_page.pack(pady=10)

request_label = tk.Label(request_page, text='Send request to the stat.gov.kz to access the parser:')
request_label.pack(pady=5, padx=5)

request_btn = tk.Button(request_page, text='Send Request', command=send_request)
request_btn.pack(pady=5, padx=5)

# endregion

