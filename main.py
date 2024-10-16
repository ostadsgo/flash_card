import csv
import time
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk


class FlashCard(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.words = []
        self.index = 0
        # open image
        img_front = Image.open("./images/card_front.png")
        img_back = Image.open("./images/card_back.png")
        img_right = Image.open("./images/right.png")
        img_wrong = Image.open("./images/wrong.png")
        # photo image
        front_card_image = ImageTk.PhotoImage(img_front)
        back_card_image = ImageTk.PhotoImage(img_back)
        right_image = ImageTk.PhotoImage(img_right)
        wrong_image = ImageTk.PhotoImage(img_wrong)
        # image labels
        card_opts = {"compound": tk.CENTER, "font": ("Helvetica", 17, "bold")}
        self.front_card_label = ttk.Label(self, image=front_card_image, **card_opts)
        self.back_card_label = ttk.Label(self, image=back_card_image, **card_opts)
        self.right_label = ttk.Label(self, image=right_image)
        self.wrong_label = ttk.Label(self, image=wrong_image)
        # save image as object attrs
        self.front_card_label.image = front_card_image
        self.back_card_label.image = back_card_image
        self.right_label.image = right_image
        self.wrong_label.image = wrong_image
        # calls
        self.read_words()
        self.start()
        self.right_label.bind("<1>", self.on_right)
        self.wrong_label.bind("<1>", self.on_wrong)

    def read_words(self):
        with open("./data/french_words.csv") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for fr, en in reader:
                self.words.append((fr, en))

    def start(self):
        first_word = self.words[self.index]
        fr, _ = first_word
        self.front_card_label["text"] = fr
        # pack images
        self.front_card_label.grid(row=0, column=0, sticky="we", columnspan=2)
        self.right_label.grid(row=1, column=0, sticky="sw")
        self.wrong_label.grid(row=1, column=1, sticky="se")
        self.index += 1

    def on_right(self, e):
        print(self.index)
        if self.index < len(self.words):
            self.back_card_label.grid_forget()
            fr, _ = self.words[self.index]

            self.front_card_label.grid(row=0, column=0, sticky="we", columnspan=2)
            self.front_card_label["text"] = fr
            self.index += 1

        else:
            self.index = 0
            self.back_card_label.grid_forget()
            fr, _ = self.words[self.index]

            self.front_card_label.grid(row=0, column=0, sticky="we", columnspan=2)
            self.front_card_label["text"] = fr
            self.index += 1

    def on_wrong(self, e):
        _, en = self.words[self.index - 1]
        self.back_card_label.grid(row=0, column=0, sticky="we", columnspan=2)

        self.back_card_label["text"] = en


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        flash_card = FlashCard(self, padding=(50, 30), relief="sunken")
        flash_card.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
