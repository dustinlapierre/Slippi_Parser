# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 18:18:42 2018

@author: Jordan
"""

from kivy import properties
from kivy.app import App
from kivy.clock import Clock, partial, mainthread
from kivy.graphics import Canvas, Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import threading
from queue import Queue

global player1_stocks
global player2_stocks
global commentary

player1_character = ""
player2_character = ""
stage = ""

shared_queue = None
player1_stocks = 0
player2_stocks = 0
commentary = ""

class MainScreen(FloatLayout):
    content = properties.StringProperty()
    lines = 0
    contentList = []
    outputString = ""
    lastLine = ""

    stage_image = properties.StringProperty('')
    player1_image = properties.StringProperty('')
    player1 = properties.StringProperty('')
    player2 = properties.StringProperty('')
    stage_name = properties.StringProperty('')
    player2_image = properties.StringProperty('')
    player1_stock = properties.StringProperty('')
    player2_stock = properties.StringProperty('')

    done = False

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.label = self.ids.lbl_console_window

        f = open("GUI/input.txt", "r+")
        f.truncate(0)
        f.close()

        self.stage_name = stage
        self.stage_image = "GUI/stages/" + stage + ".jpg"

        self.player1 = player1_character
        self.player1_image = "GUI/characters/" + player1_character + ".jpg"
        self.player1_stock = "GUI/stocks/" + player1_character + ".png"

        self.player2 = player2_character
        self.player2_image = "GUI/characters/" + player2_character + ".jpg"
        self.player2_stock = "GUI/stocks/" + player2_character + ".png"

        #-------------------------------------------------------------------

        self.ids.lbl_stage.text = self.stage_name
        with self.canvas.before:
            self.rect = Rectangle(size=(self.width, self.height), source=self.stage_image)

        # TODO: Add text color support for different maps

        self.bind(pos = self.update_rect, size=self.update_rect)

        self.ids.lbl_player_1.text = self.player1
        self.ids.img_player_1.source =  str(self.player1_image)

        self.ids.lbl_Player_2.text = self.player2
        self.ids.img_player_2.source =  str(self.player2_image)

        self.ids.img_player_1_stock_1.source =  str(self.player1_stock)
        self.ids.img_player_1_stock_2.source =  str(self.player1_stock)
        self.ids.img_player_1_stock_3.source =  str(self.player1_stock)

        self.ids.img_player_2_stock_1.source =  str(self.player2_stock)
        self.ids.img_player_2_stock_2.source =  str(self.player2_stock)
        self.ids.img_player_2_stock_3.source =  str(self.player2_stock)

        #f = open("GUI/stocks.txt", "r+")
        #f.truncate(0)
        #f.write("3\n3")
        #f.close()

        #threading.Timer(0.1, self.update).start()


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def getQueue(self, *args):
        global player1_stocks
        global player2_stocks

        #while True:
        while not shared_queue.empty():
            stock_update = shared_queue.get()
            #print("1: " + stock_update[0])
            #print("2: " + stock_update[1])
            player1_stocks = stock_update[0]
            player2_stocks = stock_update[1]
            print("Player1: " + str(player1_stocks) + " Player 2: " + str(player2_stocks))
            shared_queue.task_done()

    def update(self, *args):
        global player1_stocks
        global player2_stocks
        global commentary

        #print("Update before queue")

        #if(not shared_queue.empty()):
        #while not shared_queue.empty():
        #    stock_update = shared_queue.get()
        #    player1_stocks = stock_update[0]
        #    player2_stocks = stock_update[1]
        #    print("Player1: " + str(player1_stocks) + " Player 2: " + str(player2_stocks))
        #    shared_queue.task_done()

        #--------------------------CONSOLE-------------------------------------------
        #print("after queue")

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

        #print("UPDATE 2")

        #---------------STOCKS-----------------------------------------------

        #print("player 1 stocks:" + str(player1_stocks))
        #print("player 2 stocks:" + str(player2_stocks))

        if player1_stocks == None or player2_stocks == None:
            raise ValueError("Invalid Value for Stocks")
        if player1_stocks > 3 or player2_stocks > 3:
            raise ValueError("Invalid Value for Stocks")

        if player1_stocks < 0 or player2_stocks < 0:
            raise ValueError("Invalid Value for Stocks")

        if player1_stocks == 2:
            self.remove_widget(self.ids.img_player_1_stock_3)
        if player1_stocks == 1:
            self.remove_widget(self.ids.img_player_1_stock_3)
            self.remove_widget(self.ids.img_player_1_stock_2)
        if player1_stocks == 0:
            self.remove_widget(self.ids.img_player_1_stock_1)
            self.remove_widget(self.ids.img_player_1_stock_2)
            self.remove_widget(self.ids.img_player_1_stock_3)

        if player2_stocks == 2:
            self.remove_widget(self.ids.img_player_2_stock_3)
        if player2_stocks == 1:
            self.remove_widget(self.ids.img_player_2_stock_3)
            self.remove_widget(self.ids.img_player_2_stock_2)
        if player2_stocks == 0:
            self.remove_widget(self.ids.img_player_2_stock_1)
            self.remove_widget(self.ids.img_player_2_stock_2)
            self.remove_widget(self.ids.img_player_2_stock_3)

class MainApp(App):
    def build(self):
        main = MainScreen()
        print("MAIN")
        #while True:
        #    main.update()

        t = threading.Thread(target=main.getQueue, args=None)
        t.start()
        t.join()

        Clock.schedule_interval(main.getQueue, 0.1)
        Clock.schedule_interval(main.update, 0.1)


        print("MAIN 2")
        return main

def GuiThreadStart(character1, character2, current_stage, connection):
    print("GUI THREAD START")
    global player1_character
    player1_character = character1
    global player2_character
    player2_character = character2
    global stage
    stage = current_stage
    global shared_queue
    shared_queue = connection

    #global stocks
    #stocks = shared_queue.get()
    #shared_queue.task_done()
    #print(stocks[0])
    #print(stocks[1])

    print("before main")
    #stocks = connection.get()
    #print("stock1: " + str(stocks[0]))
    #print("stock2: " + str(stocks[1]))
    #p = partial(MainApp().run())
    #Clock.schedule_once(p, 0.000001)
    MainApp().run()


    #t = threading.Thread(target=MainApp().run(), args=None)
    #t.start()
    #t.join()

if __name__ == "__main__":
    MainApp().run()
