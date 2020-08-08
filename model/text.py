#-*- coding: utf8 -*-
class Text:
    data = {}
    @staticmethod
    def get_text(from_main):
        if from_main:
            with open('config/text.txt') as file:
                Text.data = eval(file.read())
        else:
            with open('../config/text.txt') as file:
                Text.data = eval(file.read())