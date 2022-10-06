import datetime
import logging
import os
from typing import KeysView
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import srt
import time
import requests
import sys 
from available_languages import available_languages
from color_constants import colors
from app_params import *
from app_params import INITIAL_PARAMETERS_COLLECTORS_LABELS
from error_window import ErrorWindow
testing_ui = False

LOGGING_DETAIL = logging.INFO
logging.basicConfig(level=LOGGING_DETAIL)

from util_functions import * 

from PyQt5.QtCore import QObject, QThread, pyqtSignal

class Ui_MainWindow(QMainWindow):

    def setupUi(self, MainWindow):
        
        self.create_fonts(set_bold = True)

        ### Main Window ###
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT

        MainWindow.resize(self.window_width, self.window_height)
        MainWindow.setWindowIcon(QtGui.QIcon(LOGO_POSITION))
        MainWindow.setFont(self.window_font)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setWindowTitle( NAME_ON_WINDOW )

        if WINDOW_COLOR:
            MainWindow.setStyleSheet(f"background-color: {WINDOW_COLOR};")

        #### Central Widget ###

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        MainWindow.setCentralWidget(self.centralwidget)
        
        #### Title ###

        self.set_up_title()

        ##### Group Box of Parameters ###

        self.create_parameters_section()
        
        ###### Fill Options for colors of subtitles ###

        #self.fill_colors_of_subtitles_dropdown()

        #### Action Button ###

        self.create_run_translation_button()

        #### Logs for user ###
        
        self.set_up_logs_box()

        #### Bottom Logo ###

        self.set_up_bottom_logo()

        #### Tribute to Google for the Translation ###
        self.show_google_translate_logo()
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.srt_files = None
        
    def show_google_translate_logo(self):
        
        self.google_trans_logo = QtWidgets.QLabel(self.centralwidget)
        
        google_photo = QtGui.QPixmap(GOOGLE_TRANSLATE_LOGO_POSITION)

        google_photo_height = google_photo.height()
        google_photo_width = google_photo.width()
        
        will_start_at_height = self.bottom_label_ends_at - google_photo_height - 5
        will_start_at_width = self.window_width-google_photo_width-5

        self.google_trans_logo.setGeometry(
            will_start_at_width,
            will_start_at_height,
            google_photo_width,
            google_photo_height
        )

        self.google_trans_logo.setPixmap(google_photo)

        self.google_trans_logo_caption = QtWidgets.QLabel(self.centralwidget)
        self.google_trans_logo_caption.setText("Powered by:")
        #self.google_trans_logo_caption.setFont()

        caption_width = self.google_trans_logo_caption.width()
        caption_heigth = self.google_trans_logo_caption.height()

        self.google_trans_logo_caption.setGeometry(
            will_start_at_width,
            will_start_at_height - caption_heigth - 2 ,
            caption_width,
            caption_heigth
        )

    def create_fonts(self,set_bold = False):
        
        self.window_font = QtGui.QFont(USE_THIS_FONT_FAMILY, WINDOW_FONT_SIZE) # self.base_font
        
        self.title_font = QtGui.QFont(USE_THIS_FONT_FAMILY, TITLE_FONT_SIZE)
        
        self.group_box_font = QtGui.QFont(USE_THIS_FONT_FAMILY, LOG_BOX_FONT_SIZE)
    
        self.translate_button_font = QtGui.QFont(USE_THIS_FONT_FAMILY, TRANSLATE_BUTTON_FONT_SIZE)
        
        self.log_box_font = QtGui.QFont(USE_THIS_FONT_FAMILY_FOR_LOG_BOX, LOG_BOX_FONT_SIZE)

        self.srt_files_selected_font = QtGui.QFont(USE_THIS_FONT_FAMILY_FOR_LOG_BOX, LOG_BOX_FONT_SIZE)

        if set_bold:
            
            self.window_font.setBold(True)
            self.title_font.setBold(True)
            self.group_box_font.setBold(True)
            self.translate_button_font.setBold(True)

    def create_choose_srt_button(self):

        self.select_srt_button = QtWidgets.QPushButton(self.parameters_widget)
        
        self.select_srt_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        if SELECT_SRT_BUTTON_COLOR:
            self.select_srt_button.setStyleSheet(f"background-color: {SELECT_SRT_BUTTON_COLOR};")

        self.select_srt_button.clicked.connect( self.openFileNamesDialog)

        self.select_srt_button.setText( select_srt_button_TEXT)

        self.select_srt_button.setFont( self.group_box_font)

    def create_parameters_section(self):
        
        self.parameters_widget = QtWidgets.QWidget(self.centralwidget)

        self.parameters_layout = QtWidgets.QGridLayout(self.parameters_widget)
        
        self.parameters_widget.setFont(self.group_box_font)

        self.create_choose_srt_button()

        self.create_srt_files_selected()

        self.create_input_parameters_collectors()

        left_col_will_occupy_cols = 1
        rightmost_col_will_occupy_cols = 1

        self.parameters_layout.addWidget(
            self.select_srt_button, 
            0,  0, 
            1,  left_col_will_occupy_cols
            )

        self.parameters_layout.addWidget(
            self.srt_files_selected,
            1,  0, 
            3,  left_col_will_occupy_cols)

        self.parameters_layout.addWidget(
            self.first_lang, 
            0, left_col_will_occupy_cols,
            1, rightmost_col_will_occupy_cols
            )

        self.parameters_layout.addWidget(
            self.first_lang_color, 
            1, left_col_will_occupy_cols,
            1, rightmost_col_will_occupy_cols)

        self.parameters_layout.addWidget(
            self.second_lang, 
            2, left_col_will_occupy_cols,
            1, rightmost_col_will_occupy_cols)

        self.parameters_layout.addWidget(
            self.second_lang_color, 
            3, left_col_will_occupy_cols,
            1, rightmost_col_will_occupy_cols)


        layout_will_occupy_of_total_width = 0.95
        
        width_coordinates = which_width_to_start_from_to_align_in_center(
            objects_width_rate = layout_will_occupy_of_total_width,
            windows_width = self.window_width
            )
        
        total_width = layout_will_occupy_of_total_width * self.window_width

        left_side_will_occupy = round( total_width/2)
        
        right_side_will_occupy = total_width - left_side_will_occupy
        
        self.parameters_layout.setColumnMinimumWidth(0,left_side_will_occupy)

        self.parameters_layout.setColumnMinimumWidth(1,round(right_side_will_occupy))
        
        self.parameters_widget.setLayout(self.parameters_layout)

        self.parameters_widget.adjustSize()

        parameters_will_start_from_height = self.title_widget_ends_at_height + 20
        
        widgets_width = self.parameters_widget.width()
        widgets_height = self.parameters_widget.height()

        self.parameters_widget.setGeometry(
            width_coordinates["should_start_from"],
            parameters_will_start_from_height,
            widgets_width,
            widgets_height
        )
        
        self.parameters_end_at = parameters_will_start_from_height + widgets_height 
        
    def create_srt_files_selected(self):
        
        self.srt_files_selected = QtWidgets.QLabel(self.parameters_widget)
        
        self.srt_files_selected.setFont(self.srt_files_selected_font)
        self.srt_files_selected.setText( srt_files_selected_TEXT)

        if SELECTED_FILES_BOX_COLOR:
            
            self.srt_files_selected.setStyleSheet(f"background-color: {SELECTED_FILES_BOX_COLOR};")

    def set_up_bottom_logo(self):

        self.bottom_label_host = QtWidgets.QWidget(self.centralwidget)

        self.bottom_label_layout = QtWidgets.QVBoxLayout(self.bottom_label_host) 

        self.bottom_logo_label = QtWidgets.QLabel() 
        
        self.bottom_logo_label.setPixmap(QtGui.QPixmap(BOTTOM_LOGO_POSITION))
    
        self.bottom_label_layout.addWidget(self.bottom_logo_label)

        self.bottom_label_host.setLayout(self.bottom_label_layout)

        self.bottom_label_host.adjustSize()

        bottom_logos_height = self.bottom_label_host.height()
        bottom_logos_width = self.bottom_label_host.width()

        bottom_logo_starts_from_height = self.bottom_info_widget_ends_at + 10
        
        width_coordinates = \
            which_width_to_start_from_to_align_in_center_absolute_number(
                objects_width = bottom_logos_width,
                windows_width = self.window_width
                )


        self.bottom_label_host.setGeometry(
            QtCore.QRect(

            round(width_coordinates["should_start_from"]),
            
            bottom_logo_starts_from_height,
            
            width_coordinates["objects_width"],
            
            bottom_logos_height

            )
            )
        
        self.bottom_label_ends_at = bottom_logo_starts_from_height + bottom_logos_height
    
    def create_input_parameters_collectors(self):
        
        self.first_lang = QtWidgets.QComboBox(self.parameters_widget)

        self.first_lang_color = QtWidgets.QComboBox(self.parameters_widget)

        self.second_lang = QtWidgets.QComboBox(self.parameters_widget)
        
        self.second_lang.setFont(self.group_box_font)

        self.second_lang_color = QtWidgets.QComboBox(self.parameters_widget)

        for c,collector in enumerate([
            self.first_lang, 
            self.second_lang,
            self.first_lang_color,
            self.second_lang_color
            ]):
                
                init_label = INITIAL_PARAMETERS_COLLECTORS_LABELS[c]

                collector.addItem("")
                collector.setItemText(0, init_label)

                collector.addItem("")
                collector.setItemText(1, DEFAULT_FOR_SUBS)

        starting_adding_items_from = 2

        for l,lang in enumerate(available_languages):
            self.first_lang.addItem("")
            # The -1 in (starting_adding_items_from - 1) is because we don't want 
            # the "Leave Original" option in the first Language, it's useless
            # So, we overwrite it by starting inputing languages 1 position earlier than
            # we would otherwise do
            self.first_lang.setItemText(l+(starting_adding_items_from-1),lang)
            self.second_lang.addItem("")
            self.second_lang.setItemText(l+starting_adding_items_from,lang)

        
        model = self.first_lang_color.model()
        for row,color in enumerate(colors):
            
            self.first_lang_color.addItem(color.title())
            r = colors[color][0]
            g = colors[color][1]
            b = colors[color][2]
            model.setData(model.index(row + starting_adding_items_from, 0), QtGui.QColor(r,g,b), QtCore.Qt.BackgroundRole)        
        
        model = self.second_lang_color.model()
        for row,color in enumerate(colors):
            
            self.second_lang_color.addItem(color.title())
            r = colors[color][0]
            g = colors[color][1]
            b = colors[color][2]

            model.setData(model.index(row+starting_adding_items_from, 0), QtGui.QColor(r,g,b), QtCore.Qt.BackgroundRole)  
       

        self.first_lang.setFont(self.group_box_font)
        self.second_lang.setFont(self.group_box_font)
        self.first_lang_color.setFont(self.group_box_font)
        self.second_lang_color.setFont(self.group_box_font)
    
    def create_run_translation_button(self):

        self.run_translation_button = QtWidgets.QPushButton(self.centralwidget)

        self.run_translation_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        width_coordinates = \
            which_width_to_start_from_to_align_in_center(
                objects_width_rate = 181/879,
                windows_width = self.window_width
                )

        translate_button_starts_from_height = self.parameters_end_at + 40
        translate_buttons_height = 60

        self.run_translation_button.setGeometry(
            QtCore.QRect(
                width_coordinates["should_start_from"], 
                translate_button_starts_from_height, 
                width_coordinates["objects_width"],
                translate_buttons_height
                )
                )
        
        self.run_translation_button.setFont(self.translate_button_font)

        self.run_translation_button.setText("Translate")

        if TRANSLATE_BUTTON_COLOR:
            self.run_translation_button.setStyleSheet(f"background-color: {TRANSLATE_BUTTON_COLOR};")
        
        self.run_translation_button.clicked.connect(self.call_translation)
        
        self.translate_button_ends_at = translate_buttons_height + translate_button_starts_from_height

    def set_up_logs_box(self):
        
        self.status_base_text = "Status:"
        self.logs_base_text = "Progress:"
        self.translating_text = "Translating:"

        self.bottom_info_widget = QtWidgets.QWidget(self.centralwidget)

        self.bottom_info_layout = QtWidgets.QVBoxLayout(self.bottom_info_widget)
        
        self.status = QtWidgets.QLabel(self.bottom_info_widget)
        self.logs = QtWidgets.QLabel(self.bottom_info_widget)
        self.initial_text = QtWidgets.QLabel(self.bottom_info_widget)
        
        self.translated_to_first = QtWidgets.QLabel(self.bottom_info_widget)
        self.translated_to_second = QtWidgets.QLabel(self.bottom_info_widget)
        

        self.status.setText(self.status_base_text)        
        self.logs.setText(self.logs_base_text)
        self.initial_text.setText(self.translating_text)
        self.translated_to_first.setText(self.translating_text)
        self.translated_to_second.setText(self.translating_text)
        

        self.bottom_info_layout.addWidget(self.status)
        self.bottom_info_layout.addWidget(self.logs)
        self.bottom_info_layout.addWidget(self.initial_text)
        self.bottom_info_layout.addWidget(self.translated_to_first)
        self.bottom_info_layout.addWidget(self.translated_to_second)
        
        self.status.setFont(self.log_box_font)

        self.logs.setFont(self.log_box_font)
        self.initial_text.setFont(self.log_box_font)
        self.translated_to_first.setFont(self.log_box_font)
        self.translated_to_second.setFont(self.log_box_font)
        
        if LOG_BOX_COLOR:
            self.bottom_info_widget.setStyleSheet(f"background-color: {LOG_BOX_COLOR};")

        width_coordinates = \
            which_width_to_start_from_to_align_in_center(
                objects_width_rate = 0.95,
                windows_width = self.window_width
                )

        bottom_info_widget_starts_at = self.translate_button_ends_at + 30
        bottom_info_widgets_height = 245

        self.bottom_info_widget.setGeometry(QtCore.QRect(
            width_coordinates["should_start_from"], 
            bottom_info_widget_starts_at, 
            width_coordinates["objects_width"], 
            bottom_info_widgets_height))

        self.bottom_info_widget_ends_at = bottom_info_widget_starts_at + bottom_info_widgets_height

    def set_up_title(self):

        width_coordinates = \
            which_width_to_start_from_to_align_in_center(
                objects_width_rate = 0.5,
                windows_width = WINDOW_WIDTH
                )

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)        

        self.horizontalLayout = QtWidgets.QGridLayout(self.horizontalLayoutWidget)
        
        left_title_logo = QtWidgets.QLabel(self.horizontalLayoutWidget)
        
        left_title_logo.setPixmap(QtGui.QPixmap(ASIDE_THE_TITLE_PIC))

        self.Title = QtWidgets.QLabel(self.horizontalLayoutWidget)

        self.Title.setFont(self.title_font)

        if TITLE_FONT_COLOR:
            self.Title.setStyleSheet(f"color: {TITLE_FONT_COLOR};")
        
        self.Title.setText( f"<html><head/><body><p align=\"center\">{TITLE}</p></body></html>")

        self.Title.adjustSize()

        self.right_title_logo = QtWidgets.QLabel(self.horizontalLayoutWidget)
        
        self.right_title_logo.setPixmap(QtGui.QPixmap(ASIDE_THE_TITLE_PIC))

        self.horizontalLayout.addWidget(left_title_logo, 1,  0, alignment = QtCore.Qt.AlignCenter)#AlignLeft
        
        self.horizontalLayout.addWidget(self.Title, 1,  1, alignment = QtCore.Qt.AlignCenter)
        
        self.horizontalLayout.addWidget(self.right_title_logo,  1,  2,alignment= QtCore.Qt.AlignCenter)#AlignRight

        self.horizontalLayoutWidget.adjustSize()

        widgets_width = self.horizontalLayoutWidget.width()
        widgets_height = self.horizontalLayoutWidget.height()

        width_coordinates = which_width_to_start_from_to_align_in_center_absolute_number(
            objects_width = widgets_width,
            windows_width = self.window_width
            )

        stand_at_this_percentile_of_page = 0.03

        self.horizontalLayoutWidget.setGeometry(
            width_coordinates["should_start_from"],
            round(self.window_height*stand_at_this_percentile_of_page),
            widgets_width,
            widgets_height)

        self.title_widget_ends_at_height = round(self.window_height*stand_at_this_percentile_of_page) + widgets_height
        self.title_widgets_left_border = width_coordinates["should_start_from"]

    def create_group_box(self):
       
        width_coordinates = which_width_to_start_from_to_align_in_center(
                objects_width_rate = 0.95,
                windows_width = self.window_width
                )

        self.groupBox_width = width_coordinates["objects_width"]
        
        self.groupBox_starts_at = width_coordinates["should_start_from"]  

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        
        self.groupBox.setGeometry(
            QtCore.QRect(width_coordinates["should_start_from"], 
            130, 
            self.groupBox_width, 
            251))
   
    def openFileNamesDialog(self):

        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"Select SRTs", "." )# "","All Files (*);;Python Files (*.py)")#,options=options)#, 
        
        if files:

            self.srt_files = files

            self.srt_files_selected.setText( "\n".join([os.path.basename(file) for file in files]) )
            
            self.srt_files_selected.adjustSize()

            return files

    def call_translation(self):
        
        def clean_language(lang:str):
            return lang.split(' - ')[0]
        
        def is_default_for_subs(currentText):
            return (currentText == DEFAULT_FOR_SUBS) | (currentText in INITIAL_PARAMETERS_COLLECTORS_LABELS)

        first_language = None if is_default_for_subs(self.first_lang.currentText()) else clean_language(self.first_lang.currentText())
        
        second_language = None if is_default_for_subs(self.second_lang.currentText()) else clean_language(self.second_lang.currentText())
        
        first_language_color = None if is_default_for_subs(self.first_lang_color.currentText()) else self.first_lang_color.currentText()
        
        second_language_color = None if is_default_for_subs(self.second_lang_color.currentText()) else self.second_lang_color.currentText()
        
        if first_language_color:
            if first_language_color[0] != "#":
                first_language_color = colors[first_language_color.lower()].hex_format
                
        
        
        if second_language_color:
            if second_language_color[0] != "#":
                second_language_color = colors[second_language_color.lower()].hex_format
                   

        try:
            #self.translation_thread = QThread()
            self.thread = QThread()

            #self.translation_worker = Worker()#subs
            self.worker = Worker(
                
                srt_files = self.srt_files,
                first_language = first_language,
                second_language = second_language,
                first_language_color = first_language_color,
                second_language_color = second_language_color
                
                )

            #self.translation_worker.moveToThread(self.translation_thread)
            self.worker.moveToThread(self.thread)

            #self.translation_thread.started.connect(self.translation_worker.translate_subs)
            self.thread.started.connect(self.worker.run)
            
            #self.translation_worker.finished.connect(self.translation_thread.quit)
            self.worker.finished.connect(self.thread.quit)

            #self.translation_worker.finished.connect(self.translation_worker.deleteLater)
            self.worker.finished.connect(self.worker.deleteLater)

            #self.translation_thread.finished.connect(self.translation_thread.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            #self.translation_worker.progress.connect(self.reportProgress)
            self.worker.translating_now.connect(self.report_translating_now)
            self.worker.progress.connect(self.report_progress)
            self.worker.status.connect(self.report_status)
            
            self.worker.translated_to_first.connect(self.report_translated_to_first)

            self.worker.translated_to_second.connect(self.report_translated_to_second)

            self.thread.start()

            # self.translation_thread.quit()
            # self.translation_thread.wait()
        except (RuntimeError, TypeError, NameError) as e: 
            #TODO: More specific
            self.report_status(e) #"An error has occurred")
 
    def report_status(self,status_msg):

        self.status.setText(f"{self.status_base_text}\t{status_msg}")

    def report_progress(self,progress_msg):

        self.logs.setText(f"{self.logs_base_text}\t{progress_msg}")
 
    def report_translating_now(self,translating_now_msg):

        self.initial_text.setText(f"{self.translating_text}\t{translating_now_msg}")

    def report_translated_to_first(self,translating_now_msg):
        
        self.translated_to_first.setText(f"{translating_now_msg}")

    def report_translated_to_second(self,translating_now_msg):

        self.translated_to_second.setText(f"{translating_now_msg}")

def are_we_connected_to_the_net(url_to_test = "http://www.google.com"):
    
    timeout = 10
    try:
        logging.info("Checking connection to the internet")
        
        start = time.time()
        
        request = requests.get(url_to_test, timeout=timeout)
        
        end = time.time()

        time_needed_to_check_internet_connection = end - start
        
        logging.info(f"{round(time_needed_to_check_internet_connection,3)} seconds needed to check connection to the internet")
        
        return True

    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

if __name__ == "__main__":
    
    connected_to_the_net = True if testing_ui else are_we_connected_to_the_net() 

    try:

        if not connected_to_the_net:
            
            app = QtWidgets.QApplication(sys.argv)
            
            MainWindow = QtWidgets.QMainWindow()        
            
            ui = ErrorWindow()
            
            ui.setupErrorUI(MainWindow)

            MainWindow.show()

            sys.exit(app.exec_())

            connected_to_the_net = are_we_connected_to_the_net()
        else:

            from subs_translator import Worker
            app = QtWidgets.QApplication(sys.argv)
            MainWindow = QtWidgets.QMainWindow()
            ui = Ui_MainWindow()
            ui.setupUi(MainWindow)
            MainWindow.show()
            sys.exit(app.exec_())


    except KeyboardInterrupt as k:
        print(k)


            
