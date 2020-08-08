from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.image import Image as kvImage
from kivy.uix.floatlayout import FloatLayout

from kivy.lang.builder import Builder


Builder.load_file('kv/actionbar_widget.kv')
Builder.load_file('kv/actionbar_dropdown_menu.kv')
Builder.load_file('kv/note_screen.kv')
Builder.load_file('kv/add_category.kv')
Builder.load_file('kv/add_note_screen.kv')
Builder.load_file('kv/catalog_screen.kv')
Builder.load_file('kv/search_screen.kv')
Builder.load_file('kv/settings_screen.kv')
Builder.load_file('kv/catalog_item.kv')
Builder.load_file('kv/container.kv')
Builder.load_file('kv/edit_cat_screen.kv')
Builder.load_file('kv/upload_waiting_screen.kv')
Builder.load_file('kv/download_waiting_screen.kv')


class CategoryItem(Button):
    item_id = StringProperty()
    prev_id = StringProperty()
    cat = StringProperty()
    next = StringProperty()
    level = NumericProperty()
    cat_id = StringProperty()
    cat_prev_id = StringProperty()


class EditCatScreen(Screen):
    pass


class AddNoteScreen(Screen):
    pass


class AddCategoryScreen(Screen):
    pass


class NoteScreen(Screen):
    pass


class RV(RecycleView):
    pass


class ActionBarDropDown(DropDown):
    pass


class MyDropButton(Button):
    pass


class ActionBarWidget(GridLayout):
    pass


class CatalogScreen(Screen):
    pass


class NoteResult(Label):
    pass


class NoteImage(kvImage):
    im = ObjectProperty()


class NoteLabel(Label):
    pass


class Container(Screen):
    pass


class SearchScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class UploadWaitingScreen(FloatLayout):
    pass


class DownloadWaitingScreen(FloatLayout):
    pass

