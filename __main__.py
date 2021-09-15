# Copyright 2021 Criomby
# criomby@pm.me

import tkinter as tk
from PIL import ImageTk, Image
import random
import os

class App(tk.Tk):

    def __init__(self):
        super(App, self).__init__()
        
        # GUI
        self.title('GuessTheCard')
        self.iconbitmap(self.resource_path('icon_cgg.ico'))
        self.geometry('300x440')
        self.resizable(False, False)
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
        self.right_num = tk.IntVar()
        self.wrong_num = tk.IntVar()
        self.right_num.set(0)
        self.wrong_num.set(0)

        # define labels
        label_top = tk.Label(text='Will the next card be higher or lower?', width=30, height=3,
                             # font = ('Helvetica', '10', 'bold'),
                             master=frame_top)
        label_right = tk.Label(text='Right guesses:', width=50, height=2,
                               # font = ('TkDefaultFont', '10', 'bold'),
                               master=frame_counters)
        label_right_num = tk.Label(textvariable=self.right_num, width=15, height=2,
                                   font=('TkDefaultFont', '10', 'bold'),
                                   master=frame_counters, fg='dark green')
        label_wrong = tk.Label(text='Wrong guesses:', width=50, height=2,
                               # font = ('TkDefaultFont', '10', 'bold'),
                               master=frame_counters)
        label_wrong_num = tk.Label(textvariable=self.wrong_num, width=15, height=2,
                                   font=('TkDefaultFont', '10', 'bold'),
                                   master=frame_counters, fg='OrangeRed4')
        label_space1 = tk.Label(text='', width=50, height=1, master=frame_buttons)
        label_space2 = tk.Label(text='', width=50, height=1, master=frame_buttons)

        # card images
        # card back image for card deck
        self.card_back = self.resource_path('card_back.jpg')
        self.img_back_open = Image.open(self.card_back)
        self.img_back = ImageTk.PhotoImage(self.img_back_open)
        self.label_image_back = tk.Label(image=self.img_back, master=frame_cards)

        # program opens the same card when opening
        self.current_img = str(random.randint(1, 52)) + '.jpg'
        self.previous_img = ''

        self.img_open = Image.open(self.resource_path(self.current_img))
        self.img_start = ImageTk.PhotoImage(self.img_open)
        self.label_image = tk.Label(image=self.img_start, master=frame_cards)
        
        # define buttons
        button_higher = tk.Button(text='Higher', width=15, height=2,
                                  command=self.press_higher, bg='powder blue', relief='flat', master=frame_buttons)
        button_lower = tk.Button(text='Lower', width=15, height=2,
                                 command=self.press_lower, bg='bisque2', relief='flat', master=frame_buttons)

        # PACKS:
        label_top.pack()
        self.label_image.pack(side=tk.LEFT)
        self.label_image_back.pack(side=tk.RIGHT)
        label_space2.pack()
        button_higher.pack()
        button_lower.pack()
        label_space1.pack()
        label_right.pack()
        label_right_num.pack()
        label_wrong.pack()
        label_wrong_num.pack()

    # increase right counter
    def count_right(self):
        self.right_num.set(self.right_num.get() + 1)
        print("Count 'Right guesses' increased")

    # increase wrong counter
    def count_wrong(self):
        self.wrong_num.set(self.wrong_num.get() + 1)
        print("Count 'Wrong guesses' increased")

    # function to get files found in the pyinstaller --onefile exe,
    # which sets the path not as 'env' anymore, but as sys._MEIPASS
    # https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # function to change image
    def get_new_card(self):
        # save state of current card
        self.previous_img = self.current_img
        # gen new card
        self.current_img = str(random.randint(1, 52)) + '.jpg'
        self.new_img_open = Image.open(self.resource_path(self.current_img))
        # new_img_open = img_open.resize((94, 125), Image.ANTIALIAS)
        self.new_card = ImageTk.PhotoImage(self.new_img_open)
        self.label_image.configure(image=self.new_card)
        self.label_image.image = self.new_card
        print('Card updated')

    def press_higher(self):
        # check if new card higher or lower than previous card
        # print functions created for monitoring / logging of results
        print('')
        print('HIGHER BUTTON')
        print('-----------------------------------------')
        print('current_img:', self.current_img, ', previous_img:', self.previous_img)
        self.get_new_card()
        print('current_img:', self.current_img, ', previous_img:', self.previous_img)
        print('-----------------------------------------')

        # extract numbers from card descriptions
        self.card_number_current = self.current_img[:-4]
        self.card_number_previous = self.previous_img[:-4]
        print(self.card_number_current, '>', self.card_number_previous)
        print('result:', int(self.card_number_current) > int(self.card_number_previous))

        if int(self.card_number_current) > int(self.card_number_previous):
            self.count_right()
        elif int(self.card_number_current) == int(self.card_number_previous):
            print('Same card.')
            # generate new card and repeat button press higher
            self.press_higher()
        else:
            self.count_wrong()
        print('-----------------------------------------')
        print('END BUTTON PRESS EVENT')

    def press_lower(self):
        # check if new card higher or lower than previous card
        # print functions added for monitoring / logging of results
        print('')
        print('LOWER BUTTON')
        print('-----------------------------------------')
        print('current_img:', self.current_img, ', previous_img:', self.previous_img)
        self.get_new_card()
        print('current_img:', self.current_img, ', previous_img:', self.previous_img)
        print('-----------------------------------------')

        # extract numbers from card descriptions
        self.card_number_current = self.current_img[:-4]
        self.card_number_previous = self.previous_img[:-4]
        print(self.card_number_current, '<', self.card_number_previous)
        print('result:', int(self.card_number_current) < int(self.card_number_previous))

        if int(self.card_number_current) < int(self.card_number_previous):
            self.count_right()
        elif int(self.card_number_current) == int(self.card_number_previous):
            print('Same card.')
            # generate new card and repeat button press lower
            self.press_lower()
        else:
            self.count_wrong()
        print('-----------------------------------------')
        print('END BUTTON PRESS EVENT')

if __name__ == '__main__':
    app = App()
    app.mainloop()
