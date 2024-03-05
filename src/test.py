import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.setSource(QUrl("QML\\Screen01.ui.qml"))  # Adjust the path as needed

    if view.status() == QQuickView.Error:
        print("Error loading QML:", view.errors())
        sys.exit(-1)

    view.show()
    sys.exit(app.exec())

