import tkinter as tk

from start_screen import StartScreen


def main():

    root = tk.Tk()

    StartScreen(root)

    root.mainloop()


if __name__ == "__main__":
    main()