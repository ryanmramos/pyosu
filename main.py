import os
from tkinter import filedialog as fd

OSU_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "osu!")

def main():
    filename = fd.askopenfilename(initialdir=os.path.join(OSU_PATH, "Songs"),
                                  filetypes=[("*", ".osu")])
    osu_file = open(filename)
    for line in osu_file:
        print(line, end="")
    return

if __name__ == "__main__":
    main()