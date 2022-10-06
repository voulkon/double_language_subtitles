from color_palettes import palettes

selected_palette = "weed_and_pizza"
wanted_palette = palettes[selected_palette]

TITLE = "Multi-Lang Subs"

ASIDE_THE_TITLE_PIC = "imgs/without_backgroun - pequeno.png"
BOTTOM_LOGO_POSITION = 'imgs/bottom_logo.png' #'logo.png' 'Google-Translate-Logo.png' #
LOGO_POSITION = BOTTOM_LOGO_POSITION #'imgs/logo.png'
GOOGLE_TRANSLATE_LOGO_POSITION = 'imgs\Google_Translate_logo.svg.png'
NAME_ON_WINDOW = TITLE

USE_THIS_FONT_FAMILY = "Roboto" # "Ink Free"  #  
USE_THIS_FONT_FAMILY_FOR_LOG_BOX = USE_THIS_FONT_FAMILY

BUTTONS_COLOR = "#baffc9"
TITLE_COLOR = "#bae1ff"


WINDOW_COLOR = wanted_palette["WINDOW_COLOR"]
LOG_BOX_COLOR = wanted_palette["LOG_BOX_COLOR"]
SELECTED_FILES_BOX_COLOR = wanted_palette["LOG_BOX_COLOR"]

TITLE_FONT_COLOR = wanted_palette["TITLE_COLOR"]
TRANSLATE_BUTTON_COLOR = wanted_palette["BUTTONS_COLOR"]
SELECT_SRT_BUTTON_COLOR = wanted_palette["BUTTONS_COLOR"] 


TITLE_FONT_SIZE = 25
WINDOW_FONT_SIZE = 8
TRANSLATE_BUTTON_FONT_SIZE = 15
LOG_BOX_FONT_SIZE = 13
SRT_FILES_SELECTED_FONT_SIZE = 10

WINDOW_HEIGHT = 680
WINDOW_WIDTH = 1100

select_srt_button_TEXT = "Load SRT File(s)"
srt_files_selected_TEXT = "No Files have been Chosen"


first_language_label_TEXT = "Translate To:"
first_language_color_TEXT = "Add Color:"
second_language_label_TEXT = "Also Translate To:"
second_language_color_TEXT = "Add Color on 2nd Language:"

INITIAL_PARAMETERS_COLLECTORS_LABELS = [
            first_language_label_TEXT, second_language_label_TEXT,
            first_language_color_TEXT, second_language_color_TEXT
            ]

DEFAULT_FOR_SUBS = "Leave Original"

SEPARATORS_WIDTH = 3
