from model.const import Const
from model.text import Text
from view.container import ActionBarDropDown
from view.container import MyDropButton


class ActionBarDropDownMenu:
    def __init__(self, main, widget_controller):
        self.main = main
        self.widget_controller = widget_controller
        self.view = ActionBarDropDown()

        self.view.container.spacing = 5
        self.view.container.padding = (0, 5, 0, 0)

        self.root_drop_button = self.widget_controller.view.ids.root_drop_button
        self.edit_note_button = MyDropButton(text=Text.data['edit'])
        self.delete_note_button = MyDropButton(text=Text.data['del'])

        self.edit_note_button.bind(on_release=lambda btn: self.select(Const.EDIT_NOTE))
        self.delete_note_button.bind(on_release=lambda btn: self.select(Const.DELETE_NOTE))

        self.view.bind(on_select=lambda instance, x: setattr(self.root_drop_button, 'text', x))
        self.root_drop_button.bind(on_release=self.dropdown_menu_open)


    def dropdown_menu_open(self, instance):
        if self.main.container.ids.manager.current == Const.NOTE:
            if len(self.view.container.children) == 4:
                self.view.add_widget(self.edit_note_button)
                self.view.add_widget(self.delete_note_button)
        else:
            self.view.remove_widget(self.edit_note_button)
            self.view.remove_widget(self.delete_note_button)
        self.view.open(instance)


    def select(self, action):
        self.main.action_button_callback(action)
        self.view.dismiss()
