import pandas
import random
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    card_canvas.itemconfig(card_title, text="French", fill="black")
    card_canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    card_canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    card_canvas.itemconfig(card_background, image=card_back_img)
    card_canvas.itemconfig(card_title, text="English", fill="white")
    card_canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def known_card():
    to_learn.remove(current_card)
    unknown_words_data = pandas.DataFrame(to_learn)
    unknown_words_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash Card Project")
window.config(padx=70, pady=70, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
wrong_button = PhotoImage(file="images/wrong.png")
right_button = PhotoImage(file="images/right.png")

card_canvas = Canvas(width=800, height=530, background=BACKGROUND_COLOR, highlightthickness=0)
card_background = card_canvas.create_image(400, 265, image=card_front_img, )
card_title = card_canvas.create_text(400, 150, text="Title", fill="black", font=("Ariel", 40, "italic"))
card_word = card_canvas.create_text(400, 263, text=f"Word", fill="black", font=("Ariel", 60, "bold"))
card_canvas.grid(column=1, row=1, columnspan=2)

unknown_wrong_button = Button(image=wrong_button, highlightthickness=0, command=next_card)
unknown_wrong_button.grid(column=1, row=2)

known_right_button = Button(image=right_button, highlightthickness=0, command=known_card)
known_right_button.grid(column=2, row=2)

next_card()

window.mainloop()
