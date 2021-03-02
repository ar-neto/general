"""
It can count things
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class Counterbee(toga.App):

    def startup(self): 
        self.amount=0
        main_box = toga.Box(style=Pack(direction=COLUMN))        
        

        name_label = toga.Label(
            'Your counter is at ',
            style=Pack(padding=(0, 5))
        )
        self.result = toga.TextInput(readonly=True)
        self.result.value= self.amount
        
        #button functions
        button_add_1 = toga.Button(
            'Click me to \nadd one \nto the counter',
            on_press=self.add_1,
            style=Pack(padding=5)
        )

        button_add_10 = toga.Button(
            'Click me to \nadd ten \nto the counter',
            on_press=self.add_10,
            style=Pack(padding=5)
        )

        button_sub_1 = toga.Button(
            'Click me to \nsubtract one \nto the counter',
            on_press=self.sub_1,
            style=Pack(padding=5)
        )

        button_sub_10 = toga.Button(
            'Click me to \nsubtract ten \nto the counter',
            on_press=self.sub_10,
            style=Pack(padding=5)
        )

        #add the buttons to the screen
        main_box.add(name_label)
        main_box.add(self.result)
        main_box.add(button_add_1)
        main_box.add(button_add_10)
        main_box.add(button_sub_1)
        main_box.add(button_sub_10)
        


        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    #buttons' functionality
    def add_1(self, widget):
        self.amount+=1
        self.result.value= self.amount
        

    def sub_1(self, widget):
        self.amount-=1
        self.result.value= self.amount

    def add_10(self, widget):
        self.amount+=10
        self.result.value= self.amount

    def sub_10(self, widget):
        self.amount-=10
        self.result.value= self.amount




def main():
    return Counterbee()
