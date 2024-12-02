import tkinter as tk
from auth import login_window

def main():
    root = tk.Tk()
    login_window(root)  # Pasando 'root' como argumento
    root.mainloop()

if __name__ == "__main__":
    main()
