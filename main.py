
from ui import UndoRedoApp
import tkinter as tk


def main():
    root = tk.Tk()
    app = UndoRedoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()