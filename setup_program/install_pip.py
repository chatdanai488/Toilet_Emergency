import pip


def install(package):
    pip.main(['install', package])


pip_list = ["importlib", "subprocess", "zipfile",
            "serial", "socket", "customtkinter", "tkinter", "pillow", "pygame", "linebot"]

for i in pip_list:
    try:
        install(i)
    except Exception as e:
        print(e)
