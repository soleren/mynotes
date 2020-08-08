from model.const import Const
from model.text import Text
from view.container import Container
from db.db import DB
from controller.actionbar_dropdown_menu import ActionBarDropDownMenu
from controller.actionbar_widget import ActionBarWidget
from controller.screen_controller import ScreenController
from controller.category import Category
from controller.note import Note
from controller.settings import Settings
from net.server import Server
from net.client import Client
import asyncio


class Main:
    def __init__(self, app):
        self.app = app
        self.db = DB()
        self.search = False
        self.db.connect()
        self.db.create_tables()
        self.loop = asyncio.get_event_loop()
        self.container = Container()
        self.settings = Settings(self)
        self.loop = asyncio.get_running_loop()
        self.server = Server(self.loop, self)
        self.client = Client(self.loop, self)
        self.actionbar_widget_controller = ActionBarWidget(self)
        self.actionbar_dropdown_menu_controller = ActionBarDropDownMenu(self, self.actionbar_widget_controller)
        self.category = Category(self, self.db)
        self.note = Note(self, self.db)
        self.screen_controller = ScreenController(self)
        self.action_button_callback(Const.CATALOG_SCREEN)


    def action_button_callback(self, choice):
        self.screen_controller.change_view(choice)

        if choice == Const.CATALOG_SCREEN:
            self.container.ids.manager.current = Const.CATALOG_SCREEN
            self.actionbar_widget_controller.set_title(Text.data['my_notes'])
            self.category.refresh_category(1, '', Const.GET_MENU)
            self.screen_controller.show_category(1)
            self.search = False

        if choice == Const.SEARCH:
            self.search = True
            self.container.ids.manager.current = Const.SEARCH_SCREEN
            self.actionbar_widget_controller.set_title(Text.data['my_notes'])
            self.category.show_search_widget(self.container.ids.search_screen)

        if choice == Const.SEARCH_SCREEN:
            self.search = True
            self.container.ids.manager.current = Const.SEARCH_SCREEN
            self.category.refresh_category(6, '', Const.SEARCH, self.category.search_string)
            self.screen_controller.show_category(6)

        if choice == Const.SETTINGS_SCREEN:
            self.actionbar_widget_controller.set_title(Text.data['settings'])
            self.container.ids.manager.current = Const.SETTINGS_SCREEN

        if choice == Const.NOTE:
            self.container.ids.manager.current = Const.NOTE
            self.note.clear_note()

        if choice == Const.ADD_CATEGORY:
            self.container.ids.manager.current = Const.ADD_CATEGORY
            self.actionbar_widget_controller.set_title(Text.data['add_category'])

        if choice == Const.ADD_NOTE:
            self.note.clear_add_note()
            self.note.clear_note()
            self.note.set_container(self)
            self.container.ids.manager.current = Const.ADD_NOTE
            self.actionbar_widget_controller.set_title(Text.data['add_note'])
            self.note.reset_counters()


        if choice == Const.ADD_TEXT:
            self.note.text_counter += 1
            if self.note.text_counter <= 5:
                self.note.add_note_widget(Const.TEXT)
            else:
                self.note.text_counter = 5

        if choice == Const.ADD_IMAGE:
            self.note.image_counter += 1
            if self.note.image_counter <= 5:
                self.note.add_note_widget(Const.IMAGE)
            else:
                self.note.image_counter = 5

        if choice == Const.ADD_RESULT:
            self.note.result_counter += 1
            if self.note.result_counter <= 5:
                self.note.add_note_widget(Const.RESULT)
            else:
                self.note.result_counter = 5

        if choice == Const.SUBMIT:
            texts, images, results = self.note.fill_note(self.note.text_inputs, self.note.images, self.note.results)
            self.note.create_note(self.container.ids.add_note_screen.ids.add_note_title, texts, images, results)

        if choice == Const.EDIT_NOTE:
            self.actionbar_widget_controller.set_title(Text.data['edit_note'])
            self.container.ids.manager.current = Const.ADD_NOTE
            self.note.clear_cat_opt()
            self.note.set_note_data(self.note.note_content)

        if choice == Const.DELETE_NOTE:
            self.note.delete_note(Const.NOTE, self.note.note_content[0], Const.DELETE_NOTE)
            self.screen_controller.back_button_action()

        if choice == Const.UPDATE_NOTE:
            self.note.update_note()
