import asyncio
import pickle
from model.config import Config
from model.text import Text
from model.const import Const


class Client:
    def __init__(self, loop, main):
        self.loop = loop
        self.main = main
        self.reader = None
        self.writer = None
        self.running = Config.data['server_mode']
        self.db_file = self.main.db.read_db()


    def start(self):
        asyncio.ensure_future(self.open_connection())

    async def open_connection(self):
        self.main.settings.set_client_connection_status(Text.data['status_connecting'])

        try:
            self.reader, self.writer = await asyncio.open_connection(Config.data['server_address'],
                                                                     Config.data['server_port'],
                                                                     loop=self.loop)
            self.main.settings.set_client_connection_status(Text.data['status_yes'])
            self.main.settings.disable_client_buttons(False)
        except:
            self.main.settings.set_client_connection_status(Text.data['status_no'])
            self.main.settings.disable_client_buttons(True)


    def upload(self):
        self.main.settings.show_client_waiting_screen(True, Const.UPLOAD)
        asyncio.ensure_future(self.client_send())


    async def client_send(self):
        self.db_file = self.main.db.read_db()
        init_file_length = (len(self.db_file)).to_bytes(10, byteorder='big')
        data = init_file_length
        data += self.db_file
        self.writer.write(data)

        data = await self.reader.read(100)
        response = pickle.loads(data)

        if response == Const.UPLOAD_OK:
            self.main.settings.set_client_upload_status(Text.data['upload_yes'])
        else:
            self.main.settings.set_client_upload_status(Text.data['upload_no'])

        self.main.settings.reset_client_ui()
        self.main.settings.show_client_waiting_screen(False, Const.UPLOAD)


    def download(self):
        self.main.settings.show_client_waiting_screen(True, Const.DOWNLOAD)
        self.main.settings.set_download_waiting_label(Text.data['waiting'])

        asyncio.ensure_future(self.client_receive())


    async def client_receive(self):
        zero = (0).to_bytes(10, byteorder='big')
        self.writer.write(zero)
        data = bytearray()
        data += await self.reader.readexactly(10)
        size = int.from_bytes(data, 'big')

        while len(data) != size + 10:
            data += await self.reader.read(100000)
            pb_value = len(data) / size * 100

            self.main.settings.set_progress_bar(pb_value)

            if len(data) == size + 10:
                self.main.db.close()
                self.main.settings.set_download_waiting_label(Text.data['saving_to_disk'])
                await asyncio.sleep(0.2)
                self.main.db.write_db(data[10:])
                self.writer.write(pickle.dumps(Const.UPLOAD_OK))


                if len(self.main.db.read_db()) == size:
                    self.main.settings.set_client_download_status(Text.data['download_yes'])
                else:
                    self.main.settings.set_client_download_status(Text.data['download_no'])

                await self.writer.drain()

        self.writer.close()
        self.main.settings.reset_client_ui()
        self.main.settings.show_client_waiting_screen(False, Const.DOWNLOAD)


    def stop_client(self):
        print('Close the socket')
        self.writer.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    c = Client(loop, None)
    coro = c.open_connection()
    loop.run_until_complete(coro)
    asyncio.ensure_future(c.client_send())
    loop.close()