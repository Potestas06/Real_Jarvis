import customtkinter as tk

tk.set_appearance_mode("dark")

window = tk.CTk()
window.title("Günter")
window.geometry("500x500")

status = tk.CTkLabel(window, text="listening...", font=("Arial", 20))
status.pack()

display = tk.CTkLabel(window)
display.pack()




window.mainloop()