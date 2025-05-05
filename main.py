# main.py – App launcher and Tkinter GUI entry.

from gui import ScraperApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
