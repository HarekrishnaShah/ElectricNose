echo off

pyuic5 -o ui_mainwindow.py mainwindow.ui

pyrcc5 -o res_rc.py res.qrc