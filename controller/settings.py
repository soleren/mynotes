import shutil
from model.config import Config
from view.my_popup import PopupMsg
from model.text import Text
from model.const import Const
from view.container import UploadWaitingScreen
from view.container import DownloadWaitingScreen


class Settings:
    def __init__(self, main):
        self.main = main
        self.server_mode = False
        self.client_connection_status = self.main.container.ids.settings_screen.ids.client_connection
        self.client_upload_status = self.main.container.ids.settings_screen.ids.client_upload
        self.client_download_status = self.main.container.ids.settings_screen.ids.client_download
        self.client_download_button = self.main.container.ids.settings_screen.ids.download_button
        self.client_upload_button = self.main.container.ids.settings_screen.ids.upload_button
        self.client_download_button.disabled = True
        self.client_upload_button.disabled = True
        self.layout = self.main.container
        self.upload_waiting_screen = UploadWaitingScreen()
        self.download_waiting_screen = DownloadWaitingScreen()
        self.progress_bar = self.download_waiting_screen.ids.progress_bar
        self.download_waiting_label = self.download_waiting_screen.ids.waiting_server_label


    def backup(self):
        shutil.copy2('db/my.db', 'db/backup_my.db')


    def start_server(self, instance):
        self.server_mode = instance.active
        self.main.server.check_switch_state(instance)


    def start_client(self):
        self.main.client.start()


    def upload_db(self):
        self.main.client.upload()


    def download_db(self):
        self.main.client.download()


    def apply_changes(self, *args):
        try:
            image_quality = int(args[0])
            if image_quality < 0:
                image_quality = 0
            if image_quality > 100:
                image_quality = 100
            Config.data['quality'] = image_quality
        except:
            PopupMsg().show(Text.data['invalid_quality'])

        if self.isValidIPAddress(args[2]):
            Config.data['server_address'] = args[2]
        else:
            PopupMsg().show(Text.data['invalid_server_address'])

        try:
            port = int(args[3])
            if port < 0:
                port = 0
            if port > 65535:
                port = 65535
            Config.data['server_port'] = port
        except:
            PopupMsg().show(Text.data['invalid_зщке'])

        Config.data['server_mode'] = args[1]
        Config.set_config()


    def isValidIPAddress(self, ip):
        def isIPv4(s):
            try:
                return str(int(s)) == s and 0 <= int(s) <= 255
            except:
                return False

        if ip.count(".") == 3 and all(isIPv4(i) for i in ip.split(".")):
            return True
        return False


    def set_client_connection_status(self, text):
        self.client_connection_status.text = text


    def disable_client_buttons(self, disable):
        self.client_download_button.disabled = disable
        self.client_upload_button.disabled = disable


    def show_client_waiting_screen(self, show, type):
        if type == Const.UPLOAD:
            if show:
                self.layout.add_widget(self.upload_waiting_screen)
            else:
                self.layout.remove_widget(self.upload_waiting_screen)
        else:
            if show:
                self.layout.add_widget(self.download_waiting_screen)
            else:
                self.layout.remove_widget(self.download_waiting_screen)


    def set_client_upload_status(self, text):
        self.client_upload_status.text = text


    def set_client_download_status(self, text):
        self.client_download_status.text = text


    def reset_client_ui(self):
        self.disable_client_buttons(True)
        self.set_client_connection_status(Text.data['status_default'])

    def set_progress_bar(self, value):
        self.progress_bar.value = value

    def set_download_waiting_label(self, text):
        self.download_waiting_label.text = text
