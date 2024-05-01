import pip


def install(package):
    pip.main(['install', package])


pip_list = ["importlib", "subprocess", "zipfile",
            "pyserial", "socket", "customtkinter", "tkinter", "pillow", "pygame", "line-bot-sdk", "esptool"]

for i in pip_list:
    try:
        install(i)
    except Exception as e:
        print(e)
