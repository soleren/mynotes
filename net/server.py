import asyncio
import pickle
from model.config import Config
from model.const import Const
from model.text import Text


class Server:
    def __init__(self, loop, main):
        self.main = main
        self.loop = loop
        self.msg_size = 1024
        self.host = None
        self.port = None
        self.connection = None
        self.address = None
        self.task = None
        self.running = Config.data['server_mode']
        self.data = bytearray()


    def check_switch_state(self, instance):
        self.running = instance.active
        if instance.active:
            self.start_server()


    def start_server(self):
        self.task = asyncio.ensure_future(asyncio.start_server(self.handle_client,
                                                               Config.data['default_address'],
                                                               Config.data['server_port']))


    async def handle_client(self, reader, writer):
        self.data += await reader.readexactly(10)
        size = int.from_bytes(self.data, 'big')
        print(f"size: {size}")
        if size > 0:
            asyncio.ensure_future(self.client_upload(reader, writer, size))
        else:
            asyncio.ensure_future(self.client_download(reader, writer))


    async def client_upload(self, reader, writer, size):
        while len(self.data) != size + 10:
            self.data += await reader.read(100000)
            pb_value = len(self.data) / size * 100
            if __name__ != "__main__":
                self.main.settings.set_progress_bar(pb_value)

            if len(self.data) == size + 10:
                self.main.db.close()
                if __name__ != "__main__":
                    self.main.settings.set_download_waiting_label(Text.data['saving_to_disk'])
                await asyncio.sleep(0.2)
                self.main.db.write_db(self.data[10:])
                writer.write(pickle.dumps(Const.UPLOAD_OK))

                if __name__ != "__main__":
                    if len(self.main.db.read_db()) == size:
                        self.main.settings.set_client_download_status(Text.data['download_yes'])
                    else:
                        self.main.settings.set_client_download_status(Text.data['download_no'])

            await writer.drain()
        writer.close()


    async def client_download(self, reader, writer):
        db_file = self.main.db.read_db()
        init_file_length = (len(db_file)).to_bytes(10, byteorder='big')
        data = init_file_length
        data += db_file

        writer.write(data)
        print(len(data))
        data = await reader.read(100)
        response = pickle.loads(data)
        print(response)


if __name__ == "__main__":
    Config.get_config(False)
    Text.get_text(False)
    loop = asyncio.get_event_loop()
    s = Server(loop, None)
    s.running = True
    coro = asyncio.start_server(s.handle_client,
                                '0.0.0.0',
                                55555, loop=loop)
    server = loop.run_until_complete(coro)
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
