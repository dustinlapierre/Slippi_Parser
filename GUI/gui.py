import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty

player1_character = "None"
player2_character = "None"
stage = "None"
shared_queue = None
player1_stocks = 0
player2_stocks = 0
commentary = "" #dont worry about this yet

class MainView(FloatLayout):
    stage_label = StringProperty()
    char1_label = StringProperty()
    char2_label = StringProperty()
    p1_stocks = StringProperty()
    p2_stocks = StringProperty()

    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)
        self.stage_label = stage
        self.char1_label = player1_character
        self.char2_label = player2_character

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

class GuiApp(App):
    def build(self):
        main = MainView()
        Clock.schedule_interval(main.update, 0.05)
        return main

def GuiThreadStart(character1, character2, current_stage, connection):
    global player1_character
    player1_character = character1
    global player2_character
    player2_character = character2
    global stage
    stage = current_stage
    global shared_queue
    shared_queue = connection
    GuiApp().run()
