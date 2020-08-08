from kivy.app import App
from controller.main_controller import Main
from model.text import Text
from model.config import Config
from net.server import Server
import asyncio


class MyNotesApp(App):
    def __init__(self):
        super().__init__()
        self.server = None
        self.main = None
        self.other_task = None


    def build(self):
        # self.icon = 'myicon.png'
        Text.get_text(True)

        self.main = Main(self)
        return self.main.container


    def app_func(self):
        '''This will run both methods asynchronously and then block until they
        are finished
        '''
        self.other_task = asyncio.ensure_future(self.waste_time_freely())

        async def run_wrapper():
            # we don't actually need to set asyncio as the lib because it is
            # the default, but it doesn't hurt to be explicit
            await self.async_run(async_lib='asyncio')
            self.other_task.cancel()

        return asyncio.gather(run_wrapper(), self.other_task)

    async def waste_time_freely(self):
        '''This method is also run by the asyncio loop and periodically prints
        something.
        '''
        # await self.s.start_server()

if __name__ == "__main__":
    Config.get_config(True)
    loop = asyncio.get_event_loop()
    mynotes = MyNotesApp()
    loop.run_until_complete(mynotes.app_func())
    loop.close()
