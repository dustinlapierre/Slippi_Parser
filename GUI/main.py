# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 18:18:42 2018

@author: Jordan
"""

from kivy import properties
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Canvas, Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

player1_character = ""
player2_character = ""
stage = ""
shared_queue = None
player1_stocks = 0
player2_stocks = 0
commentary = "" #dont worry about this yet


class MainScreen(FloatLayout):
    content = properties.StringProperty()
    lines = 0
    contentList = []
    outputString = ""
    lastLine = ""

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.label = self.ids.lbl_console_window

        f = open("GUI/input.txt", "r+")
        f.truncate(0)
        f.close()

    def update(self, *args):
        if(not shared_queue.empty()):
            stock_update = shared_queue.get()
            player1_stocks = stock_update[0]
            player2_stocks = stock_update[1]
            print(player1_stocks, player2_stocks)
            shared_queue.task_done()
        self.contentList = []
        newLastLine = ""
        with open("GUI/input.txt", "r+") as f:
            for line in f:
                self.contentList.append(line)

            if len(self.contentList) != 0:
                newLastLine = self.contentList[len(self.contentList) - 1]

            if newLastLine != self.lastLine:
                self.lastLine = self.contentList[len(self.contentList) - 1]

                if len(self.contentList) > 8:
                    self.outputString = ''.join(self.contentList[-8:])
                else:
                    self.outputString = ''.join(self.contentList)

                self.label.text = ""
                self.content = self.outputString
                self.label.text = self.content


class MainApp(App):
    def build(self):
        main = MainScreen()
        Clock.schedule_interval(main.update, 0.1)
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
    MainApp().run()
