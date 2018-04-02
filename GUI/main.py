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
        Clock.schedule_interval(main.update, 0.25)
        return main

def GuiThreadStart(character1, character2, stage, connection):
    print(character1)
    print(character2)
    print(stage)
    print(connection.get())
    connection.task_done()
    MainApp().run()
