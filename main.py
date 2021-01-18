import tkinter as tk
import pandas as pd
import random

BACKGROUND_COLOR = '#B1DDC6'
FONT = 'Calibri'
to_learn = {}
random_selection = {}

try:
    data = pd.read_csv('data/items_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data/french_words_test.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')
first_item = to_learn[0]
key_list = [key for key in first_item.keys()]


def next_card():
    """chooses a new item to learn"""

    global random_selection, flip_timer

    window.after_cancel(flip_timer)
    try:
        random_selection = random.choice(to_learn)
    except IndexError:
        canvas.itemconfig(card_bg, image=card_front_img)
        canvas.itemconfig(card_title, text='Congratulations!', fill='black')
        canvas.itemconfig(card_word, text='No more cards left.', fill='black')
    else:
        canvas.itemconfig(card_bg, image=card_front_img)
        canvas.itemconfig(card_title, text=key_list[0], fill='black')
        canvas.itemconfig(card_word, text=random_selection[key_list[0]], fill='black')
        flip_timer = window.after(3000, flip_card)


def flip_card():
    """flips to the current item's definition"""

    canvas.itemconfig(card_bg, image=card_back_img)
    canvas.itemconfig(card_title, text=key_list[1], fill='white')
    canvas.itemconfig(card_word, text=random_selection[key_list[1]], fill='white')


def word_is_learned():
    """removes current item from the list of items to learn"""

    try:
        to_learn.remove(random_selection)
    except ValueError:
        pass
    else:
        words_to_learn = pd.DataFrame(to_learn)
        words_to_learn.to_csv('data/items_to_learn.csv', index=False)
        next_card()


# ---UI --- #

window = tk.Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = tk.PhotoImage(file='images/card_front.png')
card_back_img = tk.PhotoImage(file='images/card_back.png')
card_bg = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text='', font=(FONT, 40, 'italic'))
card_word = canvas.create_text(400, 263, text='', font=(FONT, 60, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

right_img = tk.PhotoImage(file='images/right.png')
wrong_img = tk.PhotoImage(file='images/wrong.png')

wrong_button = tk.Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0, pady=10)

right_button = tk.Button(image=right_img, highlightthickness=0, command=word_is_learned)
right_button.grid(row=1, column=1, pady=10)

next_card()

window.mainloop()
