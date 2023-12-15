# app.py
import tkinter as tk

from menu import DatabaseMenu

def main():
    root = tk.Tk()
    app = DatabaseMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
