#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_actSer_triggered();

    void on_actAboutSys_triggered();

    void on_actAboutQt_triggered();

    void on_actAnalyze_triggered();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
