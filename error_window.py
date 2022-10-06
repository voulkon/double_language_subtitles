
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from app_params import (LOGO_POSITION, WINDOW_COLOR, 
                        WINDOW_HEIGHT,WINDOW_WIDTH,
                        USE_THIS_FONT_FAMILY, TITLE_FONT_SIZE)

class ErrorWindow(QMainWindow):

    def setupErrorUI(self,MainWindow):

        MainWindow.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        MainWindow.setWindowIcon(QtGui.QIcon(LOGO_POSITION))
        #MainWindow.setFont()
        #MainWindow.setWindowOpacity(1.0)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setWindowTitle( "Not Connected to the Internet" )
        
        
        if WINDOW_COLOR:
            MainWindow.setStyleSheet(f"background-color: {WINDOW_COLOR};")

        
        #### Central Widget ###

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        MainWindow.setCentralWidget(self.centralwidget)

        self.Main_message = QtWidgets.QLabel(self.centralwidget)
        
        self.Main_message.setAlignment(QtCore.Qt.AlignCenter)

        self.Main_message.setText("Not connected to the internet.\n Please try again later")

        to_occupy = .9
        
        to_start_from = 1-to_occupy

        self.Main_message.setGeometry(
            round(WINDOW_WIDTH * to_start_from),
            round(WINDOW_HEIGHT * to_start_from),
            round(WINDOW_WIDTH * to_occupy),
            round(WINDOW_HEIGHT * to_occupy)
            )

        self.Main_message.setFont(QtGui.QFont(
            USE_THIS_FONT_FAMILY, 
            TITLE_FONT_SIZE))

        self.Main_message.setStyleSheet("background-color: #bd2222; color: white;")
        #self.Main_message.setStyleSheet("""QLineEdit { background-color: green; color: white }""")

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    
    MainWindow = QtWidgets.QMainWindow()
    
    ui = ErrorWindow()
            
    ui.setupErrorUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
