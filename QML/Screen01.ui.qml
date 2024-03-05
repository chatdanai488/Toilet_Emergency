

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick 6.5
import QtQuick.Controls 6.5
import QtQuick.Window 6.5

Rectangle {
    id: rectangle
    width: parent ? parent : 1920
    height: parent ? parent : 1080
    color: "#ececec"
    ScrollView {
        width: parent.width // Match the width of the parent (window)
        height: parent.height // Match the height of the parent (window)

        Rectangle {
            id: rectangle1
            y: 20
            width: parent.width * (560/1920)
            height: parent.height * (1035/1080)
            color: "#ffffff"
            anchors.left: parent.left
            anchors.leftMargin: 22

            Column {
                id: column
                anchors.fill: parent
                spacing: 0
                padding: 20

                Rectangle {
                    id: rectangle2
                    width: 200
                    height: 100
                    color: "#6cc7f3"
                    radius: 20
                    border.color: "#00a4fd"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 20
                    anchors.rightMargin: 20
                    layer.sourceRect.width: 0
                }

                Rectangle {
                    id: rectangle4
                    width: 200
                    height: 10
                    color: "#00395d6e"
                    radius: 20
                    border.color: "#0000a4fd"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 20
                    anchors.rightMargin: 20
                    layer.sourceRect.width: 0
                }

                Rectangle {
                    id: rectangle3
                    height: 75
                    color: "#ffffff"
                    border.width: 2
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 20
                    anchors.rightMargin: 20

                    Text {
                        id: text1
                        text: qsTr("求助影像")
                        anchors.fill: parent
                        anchors.leftMargin: 30
                        anchors.rightMargin: 30
                        font.pixelSize: 35
                        verticalAlignment: Text.AlignVCenter
                        fontSizeMode: Text.HorizontalFit
                    }
                }

                Rectangle {
                    id: rectangle5
                    height: 300
                    color: "#ffffff"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 20
                    anchors.rightMargin: 20

                    BusyIndicator {
                        id: busyIndicator
                        anchors.fill: parent
                        anchors.topMargin: 30
                        anchors.bottomMargin: 30
                    }
                }

                Rectangle {
                    id: rectangle6
                    height: 75
                    color: "#ffffff"
                    border.width: 2
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 20
                    anchors.rightMargin: 20
                    Text {
                        id: text2
                        text: qsTr("求助訊息")
                        anchors.fill: parent
                        anchors.leftMargin: 30
                        anchors.rightMargin: 30
                        font.pixelSize: 35
                        verticalAlignment: Text.AlignVCenter
                        fontSizeMode: Text.HorizontalFit
                    }
                }
            }
        }
    }
}
