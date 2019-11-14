echo off

pyuic5 -o ui_analysisDialog.py dialog.ui

pyrcc5 -o res_rc.py res.qrc