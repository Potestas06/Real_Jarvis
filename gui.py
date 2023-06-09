import tkinter as tk
import reconizer


def gui():
    pass

talking = False

# window
root = tk.Tk()
root.tk_setPalette(background='#333', foreground='white')
root.title("Günter")
root.geometry("500x500")

# status bar
status = tk.Label(root, text="Loading...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.pack(side=tk.BOTTOM, fill=tk.X)

# output field
output = tk.Text(root, height=80, width=50)
output.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def aksgünterimage(ahhh):
    if ahhh:
        status['text'] = "thinking..."
    else:
        status['text'] = "Günter is listening..."

def Output_displayer(text):
    output.insert(tk.END,"Response: " + text + "\n")


root.mainloop()
