import pip


class install_pip_:
    def __init__(self) -> None:
        self.pip_list = ["importlib", "subprocess", "zipfile",
                         "pyserial", "socket", "customtkinter", "tkinter", "pillow", "pygame", "line-bot-sdk", "esptool"]
        self.run()

    def install(self, package):
        pip.main(['install', package])

    def run(self):
        for i in self.pip_list:
            try:
                self.install(i)
            except Exception as e:
                print(e)
