import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ListProperty
from kivy.graphics import Canvas, Color, Rectangle

player1_character = "None"
player2_character = "None"
stage = "None"
shared_queue = None
shared_commentary_queue = None
player1_stocks = 4
player2_stocks = 4
commentary = []

class MainView(FloatLayout):
    stage_label = StringProperty()
    char1_label = StringProperty()
    char2_label = StringProperty()
    p1_stocks = StringProperty()
    p2_stocks = StringProperty()

    comm = StringProperty() #commentary
    size_difference = 0

    stage_image = StringProperty()

    player1_image = StringProperty()
    player2_image = StringProperty()

    player1_stock_image = StringProperty()
    player2_stock_image = StringProperty()

    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)
        self.stage_label = stage
        self.char1_label = player1_character
        self.char2_label = player2_character

        self.label = self.ids.lbl_console_window

        self.stage_image = "GUI/stages/" + self.stage_label + ".jpg"

        self.player1_image = "GUI/characters/" + self.char1_label + ".jpg"
        self.player1_stock_image = "GUI/stocks/" + self.char1_label + ".png"

        self.player2_image = "GUI/characters/" + self.char2_label + ".jpg"
        self.player2_stock_image = "GUI/stocks/" + self.char2_label + ".png"

        if self.stage_image == "GUI/stages/Dreamland 64.jpg" or self.stage_image == "GUI/stages/Yoshi's Story.jpg":
            self.ids.lbl_stage.text = "[color=black]" + self.stage_label + "[/color]"
            self.ids.lbl_player_1.text = "[color=black]" + self.char1_label + "[/color]"
            self.ids.lbl_Player_2.text = "[color=black]" + self.char2_label + "[/color]"
        else:
            self.ids.lbl_stage.text = self.stage_label
            self.ids.lbl_player_1.text = self.char1_label
            self.ids.lbl_Player_2.text = self.char2_label

        with self.canvas.before:
            self.rect = Rectangle(size=(self.width, self.height), source=self.stage_image)
        self.ids.img_player_1.source = str(self.player1_image)
        self.ids.img_player_2.source = str(self.player2_image)

        self.ids.img_player_1_stock_1.source = str(self.player1_stock_image)
        self.ids.img_player_1_stock_2.source = str(self.player1_stock_image)
        self.ids.img_player_1_stock_3.source = str(self.player1_stock_image)
        self.ids.img_player_1_stock_4.source = str(self.player1_stock_image)

        self.ids.img_player_2_stock_1.source = str(self.player2_stock_image)
        self.ids.img_player_2_stock_2.source = str(self.player2_stock_image)
        self.ids.img_player_2_stock_3.source = str(self.player2_stock_image)
        self.ids.img_player_2_stock_4.source = str(self.player2_stock_image)

        self.bind(pos = self.update_rect, size=self.update_rect)

    def update(self, *args):
        global player1_stocks
        global player2_stocks

        if(not shared_queue.empty()):
            stock_update = shared_queue.get()
            player1_stocks = stock_update[0]
            player2_stocks = stock_update[1]
            shared_queue.task_done()

        self.p1_stocks = str(player1_stocks)
        self.p2_stocks = str(player2_stocks)

        #---------------CONSOLE----------------------------------------------
        if(not shared_commentary_queue.empty()):
            temp_list = []
            temp_list = shared_commentary_queue.get().split('\n')
            for index in temp_list:
                commentary.append(index + '\n')
            shared_commentary_queue.task_done()

        if len(commentary) > 12:
            self.size_difference = len(commentary) - 12
            for i in range(self.size_difference):
                    commentary.pop(0)

        if len(commentary) != 0:
            self.comm = ''.join(commentary)
            self.label.text = self.comm

        #---------------STOCKS-----------------------------------------------

        if self.p1_stocks == None or self.p2_stocks == None:
            raise ValueError("Invalid Value for Stocks")
        elif self.p1_stocks > "4" or self.p2_stocks > "4":
            raise ValueError("Invalid Value for Stocks")
        elif self.p1_stocks < "0" or self.p2_stocks < "0":
            raise ValueError("Invalid Value for Stocks")

        if self.p1_stocks == "3":
            self.remove_widget(self.ids.img_player_1_stock_4)
        if self.p1_stocks == "2":
            self.remove_widget(self.ids.img_player_1_stock_4)
            self.remove_widget(self.ids.img_player_1_stock_3)
        elif self.p1_stocks == "1":
            self.remove_widget(self.ids.img_player_1_stock_4)
            self.remove_widget(self.ids.img_player_1_stock_3)
            self.remove_widget(self.ids.img_player_1_stock_2)
        elif self.p1_stocks == "0":
            self.remove_widget(self.ids.img_player_1_stock_1)
            self.remove_widget(self.ids.img_player_1_stock_2)
            self.remove_widget(self.ids.img_player_1_stock_3)
            self.remove_widget(self.ids.img_player_1_stock_4)

        if self.p2_stocks == "3":
            self.remove_widget(self.ids.img_player_2_stock_4)
        if self.p2_stocks == "2":
            self.remove_widget(self.ids.img_player_2_stock_4)
            self.remove_widget(self.ids.img_player_2_stock_3)
        elif self.p2_stocks == "1":
            self.remove_widget(self.ids.img_player_2_stock_4)
            self.remove_widget(self.ids.img_player_2_stock_3)
            self.remove_widget(self.ids.img_player_2_stock_2)
        elif self.p2_stocks == "0":
            self.remove_widget(self.ids.img_player_2_stock_1)
            self.remove_widget(self.ids.img_player_2_stock_2)
            self.remove_widget(self.ids.img_player_2_stock_3)
            self.remove_widget(self.ids.img_player_2_stock_4)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class GuiApp(App):
    def build(self):
        main = MainView()

        Clock.schedule_interval(main.update, 0.05)

        return main

def GuiThreadStart(character1, character2, current_stage, connection, commentary_queue):
    global player1_character
    global player2_character
    global stage
    global shared_queue
    global shared_commentary_queue

    player1_character = character1
    player2_character = character2
    stage = current_stage
    shared_queue = connection
    shared_commentary_queue = commentary_queue
    GuiApp().run()
