import tkinter as tk
root = tk.Tk()
root.title("Stat.Gov Parser manager")

# entry = tk.Entry(root, width=30)
# text = tk.Text(root, height=5, width=30)
# frame = tk.Frame(root, borderwidth=2, relief="groove")
# check = tk.Checkbutton(root, text="Agree", variable=var)
# radio = tk.Radiobutton(root, text="Option 1", variable=var, value=1)
label = tk.Label(root, text="Click to go!")
label.pack()
button = tk.Button(root, text="Click Me", command=lambda: print("Button clicked!"))
button.pack()

root.mainloop()
