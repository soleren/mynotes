from kivy.uix.popup import Popup
from kivy.lang.builder import Builder

Builder.load_string("""
<MyPopup>:
    auto_dismiss: False
    size_hint:(0.25, 0.5)
    title_size:20
    title_align:'center'
    title_color: 0,0,0,1
    background: 'images/white.png'
    
    MyButton:
        font_size:20
        text: Text.data['popup_close']
        on_release: root.dismiss()
""")


class MyPopup(Popup):
    pass


class PopupMsg:
    def show(self, text):
        MyPopup(title=text, separator_height=0).open()