from model.const import Const
from model.text import Text
from model.stack_item import StackItem
from view.container import CategoryItem


class ScreenController:
    def __init__(self, main):
        self.main = main
        self.view = None
        self.rv = None
        self.stack = []
        self.drop_category_menu = None
        self.buttons_category = []
        self.stack_item = None


    def show_category(self, number):
        self.rv.data = self.form_menu(number)
        self.form_menu_items(self.rv.data, number)
        self.rv.refresh_from_data()


    def change_view(self, choice):
        if choice == Const.SEARCH:
            self.view = self.main.container.ids.search_screen
            self.rv = self.main.container.ids.search_screen.ids.category_list
        if choice == Const.CATALOG_SCREEN:
            self.view = self.main.container.ids.catalog_screen
            self.rv = self.main.container.ids.catalog_screen.ids.category_list


    def form_menu(self, number):
        self.drop_category_menu = self.main.category.drop_cat[number]
        return self.main.category.cat_items[number]


    def form_menu_items(self, menu, number):
        for item in menu:
            if number == 6:
                drop_button = CategoryItem(item_id=item['item_id'], cat_id=item['cat_id'],
                                           cat_prev_id=item['cat_prev_id'],
                                           text=item['text'], next=item['next'], level=item['level'],
                                           cat=self.main.category.cat_name[number],
                                           size_hint_y=None, height=44,
                                           background_color=[0.4, 0.6, 1, 1]
                                           if item['next'] == 'cat' else [0.4, 0.1, 1, 1],
                                           background_normal='')
            else:
                drop_button = CategoryItem(item_id=item['item_id'], prev_id=item['prev_id'],
                                           text=item['text'], next=item['next'], level=item['level'],
                                           cat=self.main.category.cat_name[number],
                                           size_hint_y=None, height=44,
                                           background_color=[0.4, 0.6, 1, 1] if item['next'] == Const.CAT else [0.4, 0.1, 1, 1],
                                           background_normal='')
            drop_button.bind(on_release=lambda btn: self.menu_item_action(number, btn))
            self.drop_category_menu.add_widget(drop_button)
            self.buttons_category.append(drop_button)


    def menu_item_action(self, number, button):
        self.drop_category_menu.dismiss()
        self.main.category.set_data(number, button.item_id)
        drop = None
        for i in range(1, 6):
            if self.main.container.ids.manager.current == Const.ADD_NOTE:
                drop = self.main.category.kv_note_drop_cat[i]
            if self.main.container.ids.manager.current == Const.ADD_CATEGORY:
                drop = self.main.category.kv_cat_drop_cat[i]
            if i == number:
                drop.text = button.text
                drop.item_id = button.item_id
                drop.prev_id = button.prev_id
            if i > number:
                drop.text = '---'
                drop.item_id = ''
                drop.prev_id = ''

        if self.main.container.ids.action_bar.ids.action_label.text == Text.data['add_note']:
            self.main.note.set_cat_opt(button, number)
        if self.main.container.ids.action_bar.ids.action_label.text == Text.data['edit_note']:
            self.main.note.set_cat_opt(button, number)


    def recycle_button_action(self, item):
        if item.type == Const.CAT:
            stack_item = StackItem(item.item_id, item.prev_id, item.text, item.next, item.type, item.level, search=self.main.search)
        else:
            stack_item = StackItem(item.item_id, item.cat_id, item.text, item.next, item.type, item.level, item.cat_prev_id, search=self.main.search)

        if stack_item not in self.stack:
            self.stack.append(stack_item)

        if Const.NOTE in item.type:
            self.main.action_button_callback(Const.NOTE)
            self.main.note.show_note(item.item_id)
        else:
            if Const.CAT in item.next:
                self.main.category.refresh_category(item.level + 1, item.item_id, Const.GET_SUBMENU_FOR_NOTES)
                self.show_category(item.level + 1)
            else:
                self.main.category.refresh_category(6, item.item_id, Const.GET_NOTES_IN_SUBMENU)
                self.show_category(6)


    def back_button_action(self):
        if len(self.stack) > 0:
            self.stack_item = self.stack.pop()
            if not self.stack_item.search:
                if self.stack_item.type == Const.NOTE:
                    self.main.action_button_callback(Const.CATALOG_SCREEN)
                    self.main.category.refresh_category(self.stack_item.level, self.stack_item.prev_id, Const.GET_NOTES_IN_SUBMENU)
                else:
                    self.main.category.refresh_category(self.stack_item.level, self.stack_item.prev_id, Const.GET_MENU)
                self.show_category(self.stack_item.level)
            else:
                self.main.action_button_callback(Const.SEARCH_SCREEN)


    def cat_menu(self, number):
        main_button = None

        if self.main.container.ids.manager.current == Const.ADD_CATEGORY:
            main_button = self.main.category.kv_cat_drop_cat[number]

        if self.main.container.ids.manager.current == Const.ADD_NOTE:
            main_button = self.main.category.kv_note_drop_cat[number]

        menu = self.form_menu(number)
        for widget in self.buttons_category:
            self.drop_category_menu.remove_widget(widget)

        self.form_menu_items(menu, number)

        main_drop_category_button = main_button
        main_drop_category_button.bind(on_release=self.drop_category_menu.open)
