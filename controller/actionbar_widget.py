
class ActionBarWidget:
    def __init__(self, main):
        self.main = main
        self.view = self.main.container.ids.action_bar


    def set_title(self, title):
        self.main.container.ids.action_bar.ids.action_label.text = title

