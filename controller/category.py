import uuid
from model.const import Const
from view.my_popup import PopupMsg
from view.container import EditCatScreen
from model.text import Text
from kivy.uix.dropdown import DropDown


class Category:
    def __init__(self, main, db):
        self.main = main
        self.db = db
        self.cat_name = ['', 'cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'note']
        self.cats = []
        self.view = EditCatScreen()
        self.cat_ids = [None, '', '', '', '', '']
        self.cat_types = [None, 'cat1', 'cat2', 'cat3', 'cat4', 'cat5']
        self.layout = None
        self.number = 0
        self.search_string = ''
        self.popup = PopupMsg()
        self.drop_cat = [None, DropDown(), DropDown(), DropDown(), DropDown(),
                         DropDown(), DropDown()]
        self.setup_dropdown()
        self.cat_items = [None, [], [], [], [], [], []]
        self.note_content = []
        self.add_cat_screen = self.main.container.ids.add_category_screen
        self.add_note_screen = self.main.container.ids.add_note_screen
        self.kv_cat_drop_cat = [None, self.add_cat_screen.ids.drop_cat1,
                                self.add_cat_screen.ids.drop_cat2,
                                self.add_cat_screen.ids.drop_cat3,
                                self.add_cat_screen.ids.drop_cat4,
                                self.add_cat_screen.ids.drop_cat5]
        self.kv_note_drop_cat = [None, self.add_note_screen.ids.note_drop_cat1,
                                 self.add_note_screen.ids.note_drop_cat2,
                                 self.add_note_screen.ids.note_drop_cat3,
                                 self.add_note_screen.ids.note_drop_cat4,
                                 self.add_note_screen.ids.note_drop_cat5]



    def setup_dropdown(self):
        for i in range(1, 6, 1):
            self.drop_cat[i].container.spacing = 5
            self.drop_cat[i].container.padding = (0, 5, 0, 5)


    def create_category(self, *args):
        cat_id = str(uuid.uuid4())
        number = args[0]
        prev_level = number - 1
        prev_id = args[1]
        cat_name = args[2]

        if self.check_for_names_doubles(number, prev_id, cat_name):
            if number == 1:
                prev_id = cat_id

            if self.check_for_category_next_content(prev_level, prev_id):
                self.db.create(number, cat_id, prev_id, cat_name, Const.CREATE_CATEGORY)
                if prev_level > 0:
                    self.db.update(self.cat_name[prev_level], prev_id, Const.UPDATE_BY_CAT)


    def refresh_category(self, number, prev_cat, opt, search=''):
        cats = self.get_category(number, prev_cat, opt, search)

        if number == 6:
            self.cat_items[number] = [{"item_id": f"{item[0]}", "cat_id": f"{item[1]}", "cat_prev_id": f"{item[2]}",
                                       "text": f"{item[3]}", "next": f"{item[4]}", "type": f"{item[5]}",
                                       "level": item[6]} for item in cats]
        else:
            self.cat_items[number] = [{"item_id": f"{item[0]}", "prev_id": f"{item[1]}", "text": f"{item[2]}",
                                       "next": f"{item[3]}", "type": f"{item[4]}", "level": item[5]} for item in cats]
        if number == 6 and cats and opt != Const.SEARCH:
            self.note_content = cats[0]


    def remove_category(self, cat_number, sub_cat_number, item, opt):
        if not hasattr(item, 'item_id'):
            return
        result = self.get_category(sub_cat_number, item.item_id, opt)
        note_result = self.get_category(6, item.item_id,Const.GET_NOTES_IN_SUBMENU)

        if result:
            self.popup.show(Text.data['catalog_not_empty'])
        elif  note_result:
            self.popup.show(Text.data['catalog_not_empty_note'])
        else:
            self.db.delete(self.cat_name[cat_number], item.item_id, Const.REMOVE_CATEGORY)
            result = self.get_category(cat_number, item.prev_id, opt)

            if not result:
                prev_level = cat_number - 1
                if prev_level > 0:
                    self.db.update(self.cat_name[prev_level], item.prev_id, Const.UPDATE_BY_DEFAULT)


    def get_category(self, number, prev_id, opt, search=''):
        return self.db.read(self.cat_name[number], prev_id, opt, search)


    def check_for_category_next_content(self, prev_level, prev_id):
        if prev_level == 0:
            return True

        result = self.db.read(f'cat{prev_level}', prev_id, Const.GET_UPMENU)

        if result[0][3] == 'cat' or result[0][3] == '0':
            return True
        return False


    def check_for_names_doubles(self, number, prev_id, cat_name):
        cat = self.get_category(number, prev_id, Const.GET_SUBMENU)
        match = [item for item in cat if item[2] == cat_name]
        if match or len(cat_name) < 3:
            return False
        return True


    def show_widget(self, number, layout):
        if self.cat_ids[number]:
            self.number = number
            cat_name = self.db.read(self.cat_types[number], self.cat_ids[number], Const.GET_CAT)[0]
            self.set_layout(layout)
            self.view.ids.edit_cat_input.text = cat_name


    def set_layout(self, layout):
        self.layout = layout
        layout.add_widget(self.view)


    def show_search_widget(self, layout):
        self.set_layout(layout)
        self.view.ids.edit_cat_label.text = Text.data['search_note']
        self.view.ids.edit_cat_button.text = Text.data['search']


    def search(self, string):
        self.search_string = string
        if len(string) > 2:
            self.refresh_category(6, '', Const.SEARCH, string)
            self.hide_widget()
            self.main.action_button_callback(Const.SEARCH_SCREEN)
        else:
            self.popup.show(Text.data['name_too_short'])


    def update_name(self, new_name):
        if new_name:
            if len(new_name) > 2:
                if self.is_name_exist_in_cat(new_name):
                    self.popup.show(Text.data['cat_name_exists'])
                else:
                    self.db.update(self.cat_types[self.number], self.cat_ids[self.number], Const.UPDATE_CAT_NAME, new_name)
                    self.hide_widget()
            else:
                self.popup.show(Text.data['name_too_short'])
        else:
            self.popup.show(Text.data['name_is_empty'])


    def is_name_exist_in_cat(self, name):
        if name in self.db.read(self.cat_types[self.number], self.cat_ids[self.number], Const.GET_MENU_NAMES):
            return True
        return False


    def hide_widget(self):
        self.layout.remove_widget(self.view)


    def set_data(self, number, id):
        self.view.ids.edit_cat_label.text = f'{Text.data["category"]} {number}'
        self.cat_ids[number] = id


    def check_drop_cat(self, drop_cat):
        if hasattr(drop_cat, 'item_id'):
            return drop_cat.item_id
        return False