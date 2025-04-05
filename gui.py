import tkinter as tk
from tkinter import ttk
import sv_ttk
import time
from utils.parser import *
from styles.title_bar_theme import apply_theme_to_titlebar

# region Config

root = tk.Tk()
root.geometry("800x600+600+200")
root.title("Stat.Gov Parser Manager")
# root.configure(background='#0F172A')

# icon = tk.PhotoImage(file='../static/icon.png')
# root.iconphoto(True, icon)
# style = ttk.Style()
# style.theme_use('default')

# style.configure('.',
#     background='#0F172A',
#     foreground='#FFFFFF',
#     font=('Segoe UI', 10),
#     padding=5,
# )

# style.configure('TButton',
#     background='#1E293B',
#     foreground='#FFFFFF',
#     borderwidth=1,
#     padding=(3, 3),
#     relief='solid',
#     anchor='center',
# )
# style.map('TButton',
#     background=[('active', '#202F46'), ('pressed', '#FFFFFF')],
#     foreground=[('active', '#FFFFFF'), ('pressed', '#202F46')],
# )


# style.configure('Normal.TLabel',
#     background='#0F172A',
#     foreground='#FFFFFF',
#     font=('Segoe UI', 10),
#     padding=5,
#     )
# style.configure('Success.TLabel',
#     foreground='#40C9A2',
#     )
# style.configure('Danger.TLabel',
#     foreground='#F43F5E',
#     )
apply_theme_to_titlebar(root)
sv_ttk.set_theme("dark")
# root.tk.call('source', 'forest-dark.tcl')
# ttk.Style().theme_use('forest-dark')

PARSE_URL = 'https://stat.gov.kz/en/'
SOUP = None
SUCCESS = '#40C9A2'
DANGER = '#F43F5E'

# endregion


# region Actions

def send_request(SOUP=None, progress=True):
    if not SOUP:
        if progress: show_progress()
        SOUP = get_request(PARSE_URL)

    if not SOUP:
        clear_window()

        fail_label = ttk.Label(root, text=f'Request to {PARSE_URL} failed! Try again later', foreground=DANGER)
        fail_label.pack(pady=5, padx=5)
        
        back_btn = ttk.Button(root, text='Try again', command=send_request)
        back_btn.pack(padx=10, pady=10)

        exit_btn = ttk.Button(root, text="Exit", command=root.quit)
        exit_btn.pack(pady=5, padx=5)

        return print('Error in send_request function')

    try:
        clear_window()

        success_label = ttk.Label(root, text=f'Request to {PARSE_URL} has been sent successfully!', foreground=SUCCESS)
        success_label.pack(pady=5, padx=5)
        choose_label = ttk.Label(root, text='Now you can choose the category you want to parse')
        choose_label.pack(pady=5, padx=5)

        economics_btn = ttk.Button(root, text='Economics', command=lambda: create_buttons(SOUP, 'Economics'))
        economics_btn.pack(padx=10, pady=10, side="top")
        social_btn = ttk.Button(root, text='Social statistics', command=lambda: create_buttons(SOUP, 'Social statistics'))
        social_btn.pack(padx=10, pady=10, side="top")
        industry_btn = ttk.Button(root, text='Industry statistics', command=lambda: create_buttons(SOUP, 'Industry statistics'))
        industry_btn.pack(padx=10, pady=10, side="top")
        income_btn = ttk.Button(root, text='Labor and income', command=lambda: create_buttons(SOUP, 'Labor and income'))
        income_btn.pack(padx=10, pady=10, side="top")
        environment_btn = ttk.Button(root, text='Environment', command=lambda: create_buttons(SOUP, 'Environment'))
        environment_btn.pack(padx=10, pady=10, side="top")
        all_btn = ttk.Button(root, text='All', command=lambda: to_get_page(SOUP, 'All', 'All', all=True), style='Accent.TButton')
        all_btn.pack(padx=10, pady=10, side="top")

        return
    
    except Exception as e:
        clear_window()

        fail_label = ttk.Label(root, text=f'Request to {PARSE_URL} failed! Try again later', foreground=DANGER)
        fail_label.pack(pady=5, padx=5)
        
        back_btn = ttk.Button(root, text='Try again', command=send_request)
        back_btn.pack(padx=10, pady=10)

        exit_btn = ttk.Button(root, text="Exit", command=root.quit)
        exit_btn.pack(pady=5, padx=5)

        return print(f'Error in send_request function: {e}')


def create_buttons(SOUP, category_name):
    try:
        clear_window()

        btns = get_category(SOUP, category_name)

        category_label = ttk.Label(root, text=f'Subcategories of {category_name} category', font=('Segoe UI', 10, 'bold'))
        category_label.pack(pady=5, padx=5)

        for i, btn_text in enumerate(btns):
            btn_name = f"btn_{i+1}"
            button = ttk.Button(root, text=btn_text, command=lambda btn_text=btn_text: to_get_page(SOUP, category_name, btn_text, all=False))
            button.pack(pady=5, padx=5)
        
        all_btn = ttk.Button(root, text='Select all above', command=lambda: to_get_page(SOUP, category_name, 'All', all=True), style='Accent.TButton')
        all_btn.pack(pady=5, padx=5)

        back_btn = ttk.Button(root, text='Back', command=lambda: send_request(SOUP=SOUP, progress=False))
        back_btn.pack(pady=5, padx=5)
    except:
        clear_window()
        fail_label = ttk.Label(root, text=f'Something went wrong, please try later', foreground=DANGER)
        fail_label.pack(pady=5, padx=5)
        back_btn = ttk.Button(root, text='Back', command=lambda: send_request(SOUP=SOUP, progress=False))
        back_btn.pack(pady=5, padx=5)



def to_get_page(SOUP, category_name, btn_text, all=False):
    clear_window()
    show_progress()
    stats_label = ttk.Label(root)

    links_to_stats = get_page(SOUP, category_name, btn_text, all)
    for link_to_stats in links_to_stats:
        stats_page = get_request(link_to_stats)

        if check_stats(stats_page):
            stats_label.config(text='Choose docs:')
        else:
            stats_label.config(text='Docs not found in this subcategory, choose other ones', style='Danger.TLabel')




# region Util Functions

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def show_progress():
    progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
    progress.pack(pady=10)
    label = ttk.Label(root, text="Processing...")
    label.pack(pady=10)

    for i in range(101):
        progress['value'] = i
        root.update()
        time.sleep(0.005)
    progress['value'] = 0



# endregion



# def download():
#     res_2 = ttk.Label(frame, text='Downloading...', foreground='green')
#     res_2.pack()

#     download_all()
#     res_2.config(text='Everything downloaded successfully!')

#     success.destroy()
#     call_action.destroy()
#     # download_button.destroy()

#     exit_btn = ttk.Button(frame, text="Exit", command=frame.quit, padx=10)
#     exit_btn.pack(padx=10, pady=15)


# text = ttk.Text(frame, height=5, width=30)
# frame = ttk.Frame(frame, borderwidth=2, relief="groove")
# check = ttk.Checkbutton(frame, text="Agree", variable=var)
# radio = ttk.Radiobutton(frame, text="Option 1", variable=var, value=1)


# region Request Page

request_label = ttk.Label(root, text='Send request to the stat.gov.kz to access the parser:')
request_label.pack(pady=5, padx=5)

request_btn = ttk.Button(root, text='Send Request', command=send_request, style='Accent.TButton')
request_btn.pack(pady=5, padx=5)

# endregion

