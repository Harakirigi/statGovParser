import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.constants import *
import sv_ttk

import time
import webbrowser
import threading

from utils.downloader import *
from utils.parser import *
from styles.title_bar_theme import apply_theme_to_titlebar

# region Config


# apply_theme_to_titlebar(root)
# sv_ttk.set_theme("dark")
root = ttk.Window(themename="darkly")
root.geometry("800x600+600+200")
root.title("Stat.Gov Parser Manager")

PARSE_URL = 'https://stat.gov.kz/en/'
SOUP = None
SUCCESS_COLOR = '#40C9A2'
DANGER_COLOR = '#F43F5E'

# endregion


# region Actions

def request_page():
    clear_window()
    request_label = ttk.Label(root, text='Send request to the stat.gov.kz to access the parser:')
    request_label.pack(pady=10, padx=5)

    request_btn = ttk.Button(root, text='Send Request', command=send_request, bootstyle=PRIMARY)
    request_btn.pack(pady=5, padx=5)



def send_request(SOUP=None, progress=True):
    if not SOUP:
        if progress: show_progress(0.001)
        SOUP = get_request(PARSE_URL)

    if not SOUP:
        clear_window()

        fail_label = ttk.Label(root, text=f'Request to {PARSE_URL} failed! Try again later', foreground=DANGER_COLOR)
        fail_label.pack(pady=5, padx=5)
        
        back_btn = ttk.Button(root, text='Try again', command=send_request, bootstyle=PRIMARY)
        back_btn.pack(padx=10, pady=10)

        exit_btn = ttk.Button(root, text="Exit", command=root.quit, bootstyle=DANGER)
        exit_btn.pack(pady=5, padx=5)

        return print('Error in send_request function')

    try:
        clear_window()

        success_COLOR_label = ttk.Label(root, text=f'Request to {PARSE_URL} has been sent successfully!', foreground=SUCCESS_COLOR)
        success_COLOR_label.pack(pady=5, padx=5)
        choose_label = ttk.Label(root, text='Now you can choose the category you want to parse')
        choose_label.pack(pady=5, padx=5)

        economics_btn = ttk.Button(root, text='Economics', command=lambda: create_buttons(SOUP, 'Economics'), bootstyle=SECONDARY)
        economics_btn.pack(padx=10, pady=10, side="top")
        social_btn = ttk.Button(root, text='Social statistics', command=lambda: create_buttons(SOUP, 'Social statistics'), bootstyle=SECONDARY)
        social_btn.pack(padx=10, pady=10, side="top")
        industry_btn = ttk.Button(root, text='Industry statistics', command=lambda: create_buttons(SOUP, 'Industry statistics'), bootstyle=SECONDARY)
        industry_btn.pack(padx=10, pady=10, side="top")
        income_btn = ttk.Button(root, text='Labor and income', command=lambda: create_buttons(SOUP, 'Labor and income'), bootstyle=SECONDARY)
        income_btn.pack(padx=10, pady=10, side="top")
        environment_btn = ttk.Button(root, text='Environment', command=lambda: create_buttons(SOUP, 'Environment'), bootstyle=SECONDARY)
        environment_btn.pack(padx=10, pady=10, side="top")
        all_btn = ttk.Button(root, text='All', command=lambda: to_get_page(SOUP, 'All', 'All', all=True), bootstyle=PRIMARY)
        all_btn.pack(padx=10, pady=10, side="top")

        return
    
    except Exception as e:
        clear_window()

        fail_label = ttk.Label(root, text=f'Request to {PARSE_URL} failed! Try again later', foreground=DANGER_COLOR)
        fail_label.pack(pady=5, padx=5)
        
        back_btn = ttk.Button(root, text='Try again', command=send_request, bootstyle=PRIMARY)
        back_btn.pack(padx=10, pady=10)

        exit_btn = ttk.Button(root, text="Exit", command=root.quit, bootstyle=DANGER)
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
            button = ttk.Button(root, text=btn_text, command=lambda btn_text=btn_text: to_get_page(SOUP, category_name, btn_text, all=False), bootstyle=SECONDARY)
            button.pack(pady=5, padx=5)
        
        all_btn = ttk.Button(root, text='Select all above', command=lambda: to_get_page(SOUP, category_name, 'All', all=True), bootstyle=PRIMARY)
        all_btn.pack(pady=5, padx=5)

        back_btn = ttk.Button(root, text='Back', command=lambda: send_request(SOUP=SOUP, progress=False), bootstyle=DARK)
        back_btn.pack(pady=5, padx=5)
    except:
        clear_window()
        fail_label = ttk.Label(root, text=f'Something went wrong, please try later', foreground=DANGER_COLOR)
        fail_label.pack(pady=5, padx=5)
        back_btn = ttk.Button(root, text='Back', command=lambda: send_request(SOUP=SOUP, progress=False), bootstyle=DARK)
        back_btn.pack(pady=5, padx=5)



def to_get_page(SOUP, category_name, btn_text, all=False):
    is_json = tk.IntVar()
    is_csv = tk.IntVar()
    clear_window()
    show_progress(0.003)

    links_to_stats = get_page(SOUP, category_name, btn_text, all)
    stats_page = get_request(links_to_stats[0])

    if check_stats(stats_page):
        clear_window()

        DARK_label = ttk.Label(root, text=f'You are currently in "{category_name}/{btn_text}" directory', font=('Segoe UI', 10, 'bold'))
        DARK_label.pack(pady=5, padx=5)

        stats_label = ttk.Label(root, text='Select the format you want to download')
        stats_label.pack(pady=5, padx=5)

        select_option = ttk.Combobox(root, values=['Spreadsheets only', 'Dynamic Tables only', 'Select All'], state='readonly')
        select_option.current(0)
        select_option.pack(pady=5, padx=5)

        json_checkbox = ttk.Checkbutton(root, text="Download JSON files if exists", variable=is_json)
        json_checkbox.pack(pady=10, padx=10)
        ToolTip(json_checkbox, text="Attention! Very few documents have JSON file format supported. You may download XLS file format in majority. However, it's recommended to disable these options for better speed performance")

        csv_checkbox = ttk.Checkbutton(root, text="Download CSV files if exists", variable=is_csv)
        csv_checkbox.pack(pady=10, padx=10)
        ToolTip(csv_checkbox, text="Attention! Very few documents have CSV file format supported. You may download XLS file format in majority. However, it's recommended to disable these options for better speed performance")

        error_label = ttk.Label(root, foreground=DANGER_COLOR)

        download_btn = ttk.Button(root, text='Download now', command=lambda: start_download(
            links_to_stats,
            select_option.get(), 
            error_label,
            json_selected = True if is_json.get() == 1 else False,
            csv_selected = True if is_csv.get() == 1 else False,
            ), bootstyle=PRIMARY)
        download_btn.pack(pady=10, padx=10)
        back_btn = ttk.Button(root, text='Back', command=lambda: create_buttons(SOUP=SOUP, category_name=category_name), bootstyle=DARK)
        back_btn.pack(pady=5, padx=5)
    else:
        clear_window()
        stats_label = ttk.Label(root, text='Docs not found in this subcategory, choose other ones', foreground=DANGER_COLOR)
        stats_label.pack(pady=5, padx=5)
        back_btn = ttk.Button(root, text='Back', command=lambda: create_buttons(SOUP=SOUP, category_name=category_name), bootstyle=DARK)
        back_btn.pack(pady=5, padx=5)



def start_download(links_to_stats, option, error_label, json_selected, csv_selected):
    def run_download():

        message_box.insert('end', 'Parsing elements...\nGetting things done\n', 'info')
        message_box.see('end')
        message_label.config(text='Parsing elements...')


        link_page_to_parse = check_for_links(links_to_stats, option)
        # bodies = [get_body(page, link) for link, page in link_page_to_parse.items()]
        bodies = []
        for link, page in link_page_to_parse.items():
            body = get_body(page, link)
            bodies.append(body)

        # links = [get_link(body, json_selected, csv_selected) for body in bodies]
        links = []
        for body in bodies:
            link = get_link(body, json_selected, csv_selected)
            links.append(link)


        message_box.insert('end', 'Download started successfully!\n', 'info')
        message_box.see('end')

        success_warning_danger = [0,0,0]
        
        message_label.config(text='Downloading... Please wait...')

        for link in links:
            for title, url in link.items():
                message = downloader(title, url)
                classs = define_class(message)
                success_warning_danger = count_downloads(message, success_warning_danger)
                message_box.insert('end', message + '\n', classs)
                message_box.see('end')
                time.sleep(0.05)



        clear_window(exception=message_box)

        message_label.config(text='Everything downloaded successfully!', foreground=SUCCESS_COLOR, font=('Segoe UI', 10, 'bold'))

        message_box.insert('end', 'Everything downloaded successfully!\n', 'info')
        message_box.insert('end', f'Files downloaded: {success_warning_danger[0]}\nWarnings given: {success_warning_danger[1]}\nFails: {success_warning_danger[2]}\n', 'info')
        message_box.see('end')

        back_btn = ttk.Button(root, text='Back to Main Menu', command=lambda: send_request(SOUP=SOUP, progress=False), bootstyle=PRIMARY)
        back_btn.pack(padx=10, pady=10)

        exit_btn = ttk.Button(root, text="Exit", command=root.quit, bootstyle=INFO)
        exit_btn.pack(pady=5, padx=5)



    if len(option) == 0:
        error_label.config(text='You have to select one of the provided values')
        error_label.pack(pady=5, padx=5)
        return
    
    if len(option) > 30:
        error_label.config(text='Why so many characters...')
        return

    elif option == 'Spreadsheets only' or option == 'Dynamic Tables only' or option == 'Select All':
        clear_window()

        global message_box
        message_box = tk.Text(root, height=20, width=70)
        message_box.tag_config('success', foreground=SUCCESS_COLOR)
        message_box.tag_config('danger', foreground=DANGER_COLOR)
        message_box.tag_config('warning', foreground='#E6AF2E')
        message_box.tag_config('info', foreground='white')
        message_box.pack(pady=5)

        message_label = ttk.Label(root, text='Parsing elements...\n', foreground=SUCCESS_COLOR)
        message_label.pack(pady=5)

        threading.Thread(target=run_download).start()

    else:
        error_label.config(text=f'You have to select the provided values only, not {option}')
        return
        



# region Util Functions


def clear_window(exception=None):
    for widget in root.winfo_children():
        if widget is not menu_bar and not exception:
            widget.destroy()

def show_progress(duration, label='Processing...', ):
    progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
    progress.pack(pady=10)
    label = ttk.Label(root, text=label)
    label.pack(pady=10)

    for i in range(101):
        progress['value'] = i
        root.update()
        time.sleep(duration)
    progress['value'] = 0



def change_theme(root, theme):
    root.style.theme_use(theme)


def define_class(message):
    if message.startswith('✅'):
        return 'success'
    if message.startswith('⚠️'):
        return 'warning'
    if message.startswith('❌'):
        return 'danger'

def count_downloads(message, success_warning_danger):
    if message.startswith('✅'):
        success_warning_danger[0] += 1
    if message.startswith('⚠️'):
        success_warning_danger[1] += 1
    if message.startswith('❌'):
        success_warning_danger[2] += 1

    return success_warning_danger


# endregion


# region Menu Bar

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)


home_menu = tk.Menu(menu_bar, tearoff=0, bg='#222222', fg='white',
                   activebackground='#222222', activeforeground='white')
menu_bar.add_cascade(label="Home", menu=home_menu)
toolbar_var = tk.BooleanVar(value=True)
statusbar_var = tk.BooleanVar(value=True)
home_menu.add_command(label='Home Page', command=request_page)
home_menu.add_separator()
home_menu.add_command(label="Exit", command=root.quit)

theme_menu = tk.Menu(menu_bar, tearoff=0, bg='#222222', fg='white',
                    activebackground='#222222', activeforeground='white')
menu_bar.add_cascade(label="Change Theme", menu=theme_menu)
theme_menu.add_command(label="Solar", command=lambda: change_theme(root, 'solar'))
theme_menu.add_command(label="Superhero", command=lambda: change_theme(root, 'superhero'))
theme_menu.add_command(label="Darkly", command=lambda: change_theme(root, 'darkly'))
theme_menu.add_command(label="Cyborg", command=lambda: change_theme(root, 'cyborg'))
theme_menu.add_command(label="Vapor", command=lambda: change_theme(root, 'vapor'))

request_page()

# endregion

