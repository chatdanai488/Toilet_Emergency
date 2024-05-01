from uploadesp32 import ArduinoSketchUploader
from update import InoFileEditor
from get_port import get_serial_ports


def update():

    file_path = "arduino\\sketch_test1\\sketch_test1.ino"
    wifi_name = "TCUST-FREE"
    mycom_ip = "172.16.204.48"
    my_port = 1234

    ino_editor = InoFileEditor(file_path)
    # data = ino_editor.update_code(wifi_name, mycom_ip, my_port)
    data = ino_editor.auto_update("C101")
    ino_editor.write_code(data)

# -----------------------------------------------


def upload():
    # use folder path
    sketch_path = "arduino\\sketch_test1"

    arduino_port = get_serial_ports()

    uploader = ArduinoSketchUploader(sketch_path, arduino_port[0])
    if uploader.compile_sketch():
        if uploader.upload_sketch():
            # uploader.communicate_serial()
            # print("ok")
            pass


update()
upload()
