# Copyright 2021 Criomby
# criomby@pm.me

import tkinter as tk
from PIL import ImageTk, Image
import random
import os

# increase right counter
def count_right():
    global right_num
    right_num.set(right_num.get() + 1)
    print("Count 'Right guesses' increased")

# increase wrong counter
def count_wrong():
    global wrong_num
    wrong_num.set(wrong_num.get() + 1)
    print("Count 'Wrong guesses' increased")

# function to get the .ico file found in the pyinstaller --onefile exe,
# which sets the path not as 'env' anymore, but as sys._MEIPASS
# Copyright:
# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# GUI
window = tk.Tk()
window.title('GuessTheCard')
window.iconbitmap(resource_path('icon_cgg.ico'))
window.geometry('300x440')
window.resizable(False, False)
# DEFINITIONS
# define frames
frame_top = tk.Frame()
frame_top.pack()
frame_cards = tk.Frame()
frame_cards.pack()
frame_buttons = tk.Frame()
frame_buttons.pack()
frame_counters = tk.Frame()
frame_counters.pack()

# define counter variables
right_num = tk.IntVar()
wrong_num = tk.IntVar()
right_num.set(0)
wrong_num.set(0)

# define labels
label_top = tk.Label(text='Will the next card be higher or lower?', width=30, height=3,
                     #font = ('Helvetica', '10', 'bold'),
                     master=frame_top)
label_right = tk.Label(text='Right guesses:', width=50, height=2,
                       #font = ('TkDefaultFont', '10', 'bold'),
                       master=frame_counters)
label_right_num = tk.Label(textvariable=right_num, width=15, height=2,
                           font = ('TkDefaultFont', '10', 'bold'),
                           master=frame_counters, fg = 'dark green')
label_wrong = tk.Label(text='Wrong guesses:', width=50, height=2,
                       #font = ('TkDefaultFont', '10', 'bold'),
                       master=frame_counters)
label_wrong_num = tk.Label(textvariable=wrong_num, width=15, height=2,
                           font = ('TkDefaultFont', '10', 'bold'),
                           master=frame_counters, fg = 'OrangeRed4')
label_space1 = tk.Label(text='', width=50, height=1, master=frame_buttons)
label_space2 = tk.Label(text='', width=50, height=1, master=frame_buttons)

# card images
# card back image for card deck
card_back = resource_path('card_back.jpg')
img_back_open = Image.open(card_back)
img_back = ImageTk.PhotoImage(img_back_open)
label_image_back = tk.Label(image = img_back, master=frame_cards)

# program opens the same card when opening
global current_img
current_img = str(random.randint(1, 52)) + '.jpg'
global previous_img
previous_img = ''

img_open = Image.open(resource_path(current_img))
img_start = ImageTk.PhotoImage(img_open)
label_image = tk.Label(image = img_start, master=frame_cards)

#function to change image
def get_new_card():
    global label_image
    global current_img
    global previous_img
    #save state of current card
    previous_img = current_img
    # gen new card
    current_img = str(random.randint(1, 52)) + '.jpg'
    new_img_open = Image.open(resource_path(current_img))
    new_card = ImageTk.PhotoImage(new_img_open)
    label_image.configure(image=new_card)
    label_image.image = new_card
    print('Card updated')

def press_higher():
    global current_img
    global previous_img
    # check if new card higher or lower than previous card
    # print functions created for monitoring / logging of results
    print('HIGHER BUTTON')
    print('-----------------------------------------')
    print('current_img:', current_img, ', previous_img:', previous_img)
    get_new_card()
    print('current_img:', current_img, ', previous_img:', previous_img)
    print('-----------------------------------------')

    # extract numbers from card descriptions
    card_number_current = current_img[:-4]
    card_number_previous = previous_img[:-4]
    print(card_number_current, '>', card_number_previous)
    print('result:', int(card_number_current) > int(card_number_previous))

    if int(card_number_current) > int(card_number_previous):
        count_right()
    elif int(card_number_current) == int(card_number_previous):
        print('Same card.')
        # generate new card
        press_higher()
    else:
        count_wrong()
    print('-----------------------------------------')
    print('END BUTTON PRESS EVENT')

def press_lower():
    global current_img
    global previous_img
    # check if new card higher or lower than previous card
    # print functions added for monitoring / logging of results
    print('LOWER BUTTON')
    print('-----------------------------------------')
    print('current_img:', current_img, ', previous_img:', previous_img)
    get_new_card()
    print('current_img:', current_img, ', previous_img:', previous_img)
    print('-----------------------------------------')

    # extract numbers from card descriptions
    card_number_current = current_img[:-4]
    card_number_previous = previous_img[:-4]
    print(card_number_current, '<', card_number_previous)
    print('result:', int(card_number_current) < int(card_number_previous))

    if int(card_number_current) < int(card_number_previous):
        count_right()
    elif int(card_number_current) == int(card_number_previous):
        print('Same card.')
        # generate new card
        press_lower()
    else:
        count_wrong()
    print('-----------------------------------------')
    print('END BUTTON PRESS EVENT')

# define buttons
button_higher = tk.Button(text='Higher', width=15, height=2,
                          command = press_higher, bg = 'powder blue', relief = 'flat', master=frame_buttons)
button_lower = tk.Button(text='Lower', width=15, height=2,
                         command = press_lower, bg = 'bisque2', relief = 'flat', master=frame_buttons)

# PACKS:
label_top.pack()
label_image.pack(side=tk.LEFT)
label_image_back.pack(side=tk.RIGHT)
label_space2.pack()
button_higher.pack()
button_lower.pack()
label_space1.pack()
label_right.pack()
label_right_num.pack()
label_wrong.pack()
label_wrong_num.pack()

window.mainloop()
