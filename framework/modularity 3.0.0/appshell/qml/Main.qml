import QtQuick
import QtQuick.Window
import QtQuick.Controls

ApplicationWindow {
    id: root
    visible: true
    width: 600
    height: 500
    title: "HelloApp"

    Text {
        anchors.centerIn: parent
        text: "Hello World!"
        font.pointSize: 24
    }
}
