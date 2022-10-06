import logging
from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, QThread, pyqtSignal
import time
import srt
import os
import datetime
from translators.apis import TranslatorError
import translators as ts

#from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QFileDialog 

def prepare_sub_content_to_display(cont):
    return cont.replace("\n"," ")#[0:100]

class Worker(QObject):

    finished = pyqtSignal()

    status = pyqtSignal(str)

    progress = pyqtSignal(str)
    
    translating_now = pyqtSignal(str)

    translated_to_first = pyqtSignal(str)

    translated_to_second = pyqtSignal(str)

    def __init__(
        self,

        srt_files:list,

        first_language:str,

        second_language:str = None,
        
        first_language_color:str = None,

        second_language_color:str = None
        ):


        QObject.__init__(self)
        
        self.srt_files = srt_files
        
        self.first_language = first_language
        
        self.second_language = second_language

        self.first_language_color = first_language_color
        self.second_language_color = second_language_color
        
    def create_output_filename(self,srt_file, file_extension = ".srt"):

        output_file = f'{srt_file}_Translated_into_{self.first_language}'

        if self.second_language:
            output_file = f'{output_file}_and_{self.second_language}'

        created_at = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

        output_file =  f'{output_file}_at_{created_at}{file_extension}' #'new_srt_file.srt' #srt_file
        
        return output_file

    def saveOutputFilenameDialog(self,data_to_save, recommended_file_name:str):

        user_defined_output_filename , check = QFileDialog.getSaveFileName(
            None, 
            'Save translated srt as...',
            recommended_file_name,
            "SRT Files (*.srt)")
        if user_defined_output_filename:

            with open(user_defined_output_filename,'w',encoding = 'utf-8') as new_srt:
                        new_srt.write(srt.compose(data_to_save))
    
    

    #@pyqtSlot
    def run(self):

        some_files_are_selected = self.srt_files is not None
        if self.first_language:

            if some_files_are_selected:

                for srt_file in self.srt_files:

                    status_msg = f'Translating: {os.path.relpath(srt_file)} to {self.first_language}'

                    self.status.emit(status_msg)

                    output_file_name = self.create_output_filename(srt_file = srt_file)
                    
                    try:
                        with open(srt_file, 'r',encoding = 'utf-8') as s:
                            text_of_srt_file = s.read()

                        # Parse lines as srt
                        subs = list(srt.parse( text_of_srt_file ))

                    except srt.SRTParseError:
                        self.status.emit(f"{srt_file} is not a valid srt file.")
                        time.sleep(3)
                        continue
                    except UnicodeDecodeError:
                        self.status.emit((f"{srt_file} does not even contain proper text in utf-8 encoding."))
                        time.sleep(3)
                        continue

                    
                    for s,sub in enumerate(subs):

                        total_dialogues = len(subs)
                        
                        percent_of_completeness = round((s+1) / total_dialogues,4)*100
                        
                        progress_msg = f'Dialogue {s+1} / {len(subs)} ({round(percent_of_completeness,2)}%)'
                        
                        self.progress.emit(progress_msg)
                        self.translating_now.emit(prepare_sub_content_to_display(sub.content) )

                        #TODO: Fix it
                        from_language = 'auto'

                        first_lang_translation = ts.google(
                                sub.content,
                                from_language = from_language,
                                to_language = self.first_language)

                        if self.first_language_color:
                            first_lang_translation = self.add_color_on_subtitle(subtitle = first_lang_translation, color = self.first_language_color)

                        self.translated_to_first.emit(f"In {self.first_language}:\t{prepare_sub_content_to_display(first_lang_translation)}")

                        second_lang_translation = ts.google(
                                sub.content, 
                                from_language = from_language, 
                                to_language = self.second_language) if self.second_language \
                                    else sub.content

                        if self.second_language_color: 
                            second_lang_translation = self.add_color_on_subtitle(
                                subtitle = second_lang_translation, 
                                color = self.second_language_color)
                    
                        emit_for_second_translation = \
                            f"And in {self.second_language} : {prepare_sub_content_to_display(second_lang_translation)}" if self.second_language \
                                else "" 

                        self.translated_to_second.emit(emit_for_second_translation)

                        this_subs_content = first_lang_translation + '\n' + second_lang_translation

                        sub.content = this_subs_content
                    
                    self.saveOutputFilenameDialog(data_to_save = subs, recommended_file_name = output_file_name)

            else:       

                status_msg = f'You need to select some files.'  
                
                self.status.emit(status_msg)
        else:
            self.status.emit("You need to select at least the first language that you want the srt to get translated to.")

        self.finished.emit()
    
    def add_color_on_subtitle(self,subtitle:str,color:str):
        return f'<font color={color}>{subtitle}</font>'


def displace_subs(
    srt_file = "../8.Simple.Rules.S01E03.WEBRip.x264-ION10.srt",
    displace_to_earlier = True, #If false, to a later moment
    seconds:int = 3 #**kwargs
    ):

    with open(srt_file, 'r',encoding = 'utf-8') as s:
        text_of_srt_file = s.read()

    # Parse lines as srt
    subs = list(srt.parse( text_of_srt_file ))

    timediff = datetime.timedelta(seconds = 3 ) 

    for sub in subs:

        if displace_to_earlier:
            sub.start = sub.start - timediff
            sub.end = sub.end - timediff
        else:
            sub.start = sub.start + timediff
            sub.end = sub.end + timediff

    with open("../shifted_srt.srt",'w',encoding = 'utf-8') as new_srt:
        new_srt.write(srt.compose(subs))
    