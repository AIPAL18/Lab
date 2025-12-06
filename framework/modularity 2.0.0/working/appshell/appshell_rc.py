# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.9.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x01\x13\
i\
mport QtQuick\x0aim\
port QtQuick.Win\
dow\x0aimport QtQui\
ck.Controls\x0a\x0aApp\
licationWindow {\
\x0a    id: root\x0a  \
  visible: true\x0a\
    width: 600\x0a \
   height: 500\x0a \
   title: \x22Hello\
App\x22\x0a\x0a    Text {\
\x0a        anchors\
.centerIn: paren\
t\x0a        text: \
\x22Hello World!\x22\x0a \
       font.poin\
tSize: 24\x0a    }\x0a\
}\x0a\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00x<\
\x00q\
\x00m\x00l\
\x00\x08\
\x08\x01^\x5c\
\x00M\
\x00a\x00i\x00n\x00.\x00q\x00m\x00l\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x96@XI\x88\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
