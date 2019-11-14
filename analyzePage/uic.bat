echo off

pyuic5 -o ui_analyzeWidget.py widget.ui

pyrcc5 -o res_rc.py res.qrc