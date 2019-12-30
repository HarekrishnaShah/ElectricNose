echo off

pyuic5 -o ui_classifierDialog.py dialog.ui

pyrcc5 -o res_rc.py res.qrc