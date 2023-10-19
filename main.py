from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
word = {}
word_dict = {}

# get data to display

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    word_dict = original_data.to_dict("records")
else:
    word_dict = data.to_dict("records")


def new_word():
    global word, flip_timer
    window.after_cancel(flip_timer)
    word = random.choice(word_dict)
    french = word["French"]
    canvas.itemconfig(text_lang, text="French", fill="black")
    canvas.itemconfig(text_word, text=french, fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(text_lang, text="English", fill="white")
    canvas.itemconfig(text_word, text=word["English"], fill="white")
    canvas.itemconfig(canvas_image, image=card_back)


def is_known():
    word_dict.remove(word)
    data = pandas.DataFrame(word_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    new_word()

# UI


window = Tk()
window.title("Flash Cards Project")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
text_lang = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
text_word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=new_word)
wrong_button.grid(column=0, row=1)


right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

new_word()
window.mainloop()
