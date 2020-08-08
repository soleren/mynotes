
class Config:
    data = {}

    @staticmethod
    def get_config(main):
        if main:
            with open('config/config.txt') as file:
                Config.data = eval(file.read())
        else:
            with open('../config/config.txt') as file:
                Config.data = eval(file.read())

    @staticmethod
    def set_config():
        with open('config/config.txt', mode='w') as file:
            file.write(str(Config.data))
