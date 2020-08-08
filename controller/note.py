import uuid
from model.config import Config
from model.const import Const
from view.my_popup import PopupMsg
from view.container import NoteImage
from view.container import NoteLabel
from view.container import NoteResult
from model.text import Text
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from PIL import ImageGrab
from kivy.core.image import Image as CoreImage
import io


class Note:
    def __init__(self, main, db):
        self.main = main
        self.db = db
        self.cat_id = None
        self.cat_prev_id = None
        self.cat = None
        self.number = 0
        self.cat_name = ['', 'cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'note']
        self.popup = PopupMsg()
        self.text_inputs = []
        self.images = []
        self.results = []
        self.note_layout_widgets = []
        self.title = self.main.container.ids.add_note_screen.ids.add_note_title
        self.note_layout = self.main.container.ids.note_screen.ids.note
        self.note_content = None
        self.note_body_layout = self.main.container.ids.add_note_screen.ids.add_note_body
        self.note_body_layout_widgets = []


    def set_note_data(self, data):
        self.id = data[0]
        self.title.text = data[3]
        self.note_body_layout.cols = 2
        texts = data[7:12]
        images = data[12:17]
        results = data[17:22]
        self.edit_screen(data[3], texts, images, results)


    def edit_screen(self, title, texts, images, results):
        self.reset_counters()
        self.main.container.ids.add_note_screen.ids.submit_button.text = Text.data['update']

        for i in range(5):
            if texts[i]:
                widget = TextInput(text=f'{texts[i]}', size_hint=(0.95, None), height=200)
                self.text_inputs.append(widget)
                self.note_body_layout.add_widget(widget)
                self.common(Const.TEXT,widget, 0)
                self.text_counter += 1

            if images[i]:
                data = io.BytesIO(images[i])
                data.seek(0)
                im = CoreImage(io.BytesIO(data.read()), ext="jpeg")
                image = NoteImage(im=data.getvalue())
                image.texture = im.texture
                self.images.append(image)
                self.note_body_layout.add_widget(image)
                self.common(Const.IMAGE, image, 1)
                self.image_counter += 1

            if results[i]:
                widget = TextInput(text=f'{results[i]}', size_hint=(0.95, None), height=200)
                self.results.append(widget)
                self.note_body_layout.add_widget(widget)
                self.common(Const.RESULT, widget, 0)
                self.result_counter += 1


    def common(self, type, widget, num):
        relative = GridLayout(size_hint=(0.1, 1), cols=1, spacing=5)
        self.note_body_layout.add_widget(relative)
        delete_button = Button(text=Text.data['del'], size_hint=(1, 0.25), font_size=18,
                               background_color=[0.4, 0.6, 1, 1], background_normal='', )
        relative.add_widget(delete_button)
        self.note_body_layout_widgets.append(delete_button)

        if num:
            update_button = Button(text=Text.data['update'], size_hint=(1, 0.25), font_size=18,
                                   background_color=[0.4, 0.6, 1, 1], background_normal='', )
            relative.add_widget(update_button)
            self.note_body_layout_widgets.append(update_button)
            update_callback = lambda a: self.update_image(widget)
            update_button.bind(on_release=update_callback)

        self.note_body_layout_widgets.append(relative)
        self.note_body_layout_widgets.append(widget)

        delete_callback = lambda a: self.delete(type, self.note_body_layout, widget, relative, delete_button)
        delete_button.bind(on_release=delete_callback)


    def delete(self, type, layout, widget, relative, button):
        if type == Const.TEXT:
            self.main.text_inputs.remove(widget)
            self.main.text_counter -= 1
        if type == Const.IMAGE:
            self.main.image_counter -= 1
            self.main.images.remove(widget)
        if type == Const.RESULT:
            self.main.result_counter -= 1
            self.main.results.remove(widget)

        relative.remove_widget(button)
        layout.remove_widget(relative)
        layout.remove_widget(widget)


    def set_container(self, container):
        self.main = container


    def set_cat_opt(self, item, number):
        self.cat_id = item.item_id
        self.cat_prev_id = item.prev_id
        self.cat = item.cat
        self.number = number


    def create_note(self, title, text_inputs, images, results):
        if self.cat_id and title and [input.text for input in text_inputs]:
            id = str(uuid.uuid4())
            result = self.db.read(self.cat, self.cat_id, Const.GET_NOTE_UPMENU)
            notes_titles = [title[0] for title in self.db.read(Const.NOTE, self.cat_id, Const.GET_NOTES_TITLES_IN_SUBMENU)]

            if title.text not in notes_titles:
                if result:
                    if result[0][3] != 'cat':
                        self.db.create(number=self.number, id=id, prev_id=self.cat_id, cat_prev_id=self.cat_prev_id,
                                       cat_name=title.text, opt=Const.CREATE_NOTE, texts=text_inputs, images=images,
                                       results=results, prev_cat=self.number)
                        self.db.update(self.cat_name[self.number], self.cat_id, Const.UPDATE_BY_NOTE)
                        self.clear_add_note()
                else:
                    self.popup.show(Text.data['note_notification'])
            else:
                self.popup.show(Text.data['note_title_exist'])
        else:
            self.popup.show(Text.data['no_cat_selected'])


    def delete_note(self, type, id, opt):
        self.db.delete(type, id, opt)


    def get_note_data(self, id):
        return self.db.read(Const.NOTE, id, Const.GET_NOTE)


    def add_note_widget(self, type):
        widget = None
        relative = GridLayout(size_hint=(0.1, 1), cols=1, spacing=10)

        if type == Const.TEXT:
            widget = TextInput(hint_text=f'{Text.data["add_note_text_chunk"]} {self.text_counter}{Text.data["chunk"]}',
                               size_hint=(0.95, None), height=200)
            self.text_inputs.append(widget)
            self.note_body_layout.add_widget(widget)

        if type == Const.IMAGE:
            img = ImageGrab.grabclipboard()
            if img:
                data = io.BytesIO()
                img.save(data, format='jpeg', quality=Config.data['quality'])
                data.seek(0)
                im = CoreImage(io.BytesIO(data.read()), ext="jpeg")
                widget = NoteImage(im=data.getvalue())
                widget.texture = im.texture
                self.images.append(widget)
                self.note_body_layout.add_widget(widget)
            else:
                self.popup.show(Text.data['clipboard_empty'])
                return

            update_button = Button(text=Text.data['update'], size_hint=(1, 0.25),  font_size=18,
                                   background_color=[0.4, 0.6, 1, 1], background_normal='', )
            relative.add_widget(update_button)
            self.note_body_layout_widgets.append(update_button)

            update_callback = lambda a: self.update_image(widget)
            update_button.bind(on_release=update_callback)

        if type == Const.RESULT:
            widget = TextInput(hint_text=f'{Text.data["add_note_result_chunk"]} {self.result_counter}{Text.data["chunk"]}',
                               size_hint=(0.98, None), height=200)
            self.results.append(widget)
            self.note_body_layout.add_widget(widget)

        self.note_body_layout.add_widget(relative)
        delete_button = Button(text=Text.data['del'], size_hint=(1, 0.25), font_size=18,
                               background_color=[0.4, 0.6, 1, 1], background_normal='', )
        relative.add_widget(delete_button)
        self.note_body_layout_widgets.append(delete_button)
        self.note_body_layout_widgets.append(relative)
        self.note_body_layout_widgets.append(widget)
        delete_callback = lambda a: self.delete(type, self.note_body_layout, widget, relative, delete_button)
        delete_button.bind(on_release=delete_callback)


    def reset_counters(self):
        self.text_counter = 0
        self.image_counter = 0
        self.result_counter = 0


    def update_image(self, widget):
        img = ImageGrab.grabclipboard()
        if img:
            data = io.BytesIO()
            img.save(data, format='jpeg', quality=Config.data['quality'])
            data.seek(0)
            im = CoreImage(io.BytesIO(data.read()), ext="jpeg")
            widget.im = data.getvalue()
            widget.texture = im.texture


    def show_note(self, item_id):
        self.note_content = self.get_note_data(item_id)
        self.main.actionbar_widget_controller.set_title(self.note_content[3])
        texts = self.note_content[7:12]
        images = self.note_content[12:17]
        results = self.note_content[17:22]

        for i in range(5):
            if texts[i]:
                label = NoteLabel(text=texts[i])
                self.note_layout_widgets.append(label)
                self.note_layout.add_widget(label)

            if images[i]:
                pic = io.BytesIO(images[i])
                im = CoreImage(pic, ext="jpeg")
                image = NoteImage()
                image.texture = im.texture
                self.note_layout_widgets.append(image)
                self.note_layout.add_widget(image)

            if results[i]:
                label = NoteResult(text=results[i])
                self.note_layout_widgets.append(label)
                self.note_layout.add_widget(label)


    def clear_note(self):
        if self.note_layout_widgets:
            for widget in self.note_layout_widgets:
                self.note_layout.remove_widget(widget)
            self.note_layout_widgets.clear()


    def clear_add_note(self):
        self.main.container.ids.add_note_screen.ids.add_note_title.text = ''
        self.main.container.ids.add_note_screen.ids.note_drop_cat1.text = '---'
        self.main.container.ids.add_note_screen.ids.note_drop_cat2.text = '---'
        self.main.container.ids.add_note_screen.ids.note_drop_cat3.text = '---'
        self.main.container.ids.add_note_screen.ids.note_drop_cat4.text = '---'
        self.main.container.ids.add_note_screen.ids.note_drop_cat5.text = '---'
        if self.note_body_layout_widgets:
            for widget in self.note_body_layout_widgets:
                self.note_body_layout.remove_widget(widget)
            self.note_body_layout_widgets.clear()
        self.text_inputs = []
        self.images = []
        self.results = []


    def fill_note(self, text_inputs, images, results):
        text_len = len(text_inputs)
        for _ in range(text_len, 5, 1):
            text_inputs.append(NoteLabel())

        images_len = len(images)
        for _ in range(images_len, 5, 1):
            images.append(NoteImage())

        res_len = len(results)
        for _ in range(res_len, 5, 1):
            results.append(NoteResult())
        return text_inputs, images, results


    def clear_cat_opt(self):
        self.cat_id = None
        self.cat_prev_id = None
        self.cat = None
        self.number = None


    def update_note(self):
        if self.cat_id and self.title.text and [input.text for input in self.text_inputs]:
            texts, images, results = self.fill_note(self.text_inputs, self.images, self.results)
            self.db.update(Const.NOTE, self.id, Const.UPDATE_NOTE, self.cat_id, self.cat_prev_id,
                           self.number, self.title.text, texts, images, results)
            self.clear_add_note()
        else:
            self.popup.show(Text.data['no_cat_selected'])
