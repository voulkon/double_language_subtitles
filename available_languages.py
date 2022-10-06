import pycountry

init_available_languages = [

    'en', 'es', 'pt', 'de',  'fr', 'el', 'ru', 
    'af', 'ak', 'am', 'ar', 'as', 'ay', 'az', 
    'be', 'bg', 'bho', 'bm', 'bn', 'bs', 'ca',
    'ceb', 'ckb', 'co', 'cs', 'cy', 'da',
    'doi', 'dv', 'ee', 'en-US',   'eo', 
    'et', 'eu', 'fa', 'fi',  'fy', 'ga', 
    'gd', 'gl', 'gn', 'gom', 'gu', 'ha', 'haw', 'hi',
    'hmn', 'hr', 'mi', 'mk', 'ml', 'mn', 'mni-Mtei', 'mr',
    'ms', 'mt', 'my', 'ne', 'nl', 'no', 'nso', 'ny', 'om', 
    'or', 'pa', 'pl', 'ps',  'qu', 'ro', 'rw', 'sa',
    'sd', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'st', 
    'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tr', 
    'ts', 'tt', 'ug', 'uk', 'ur', 'uz', 'vi', 'xh', 'yi', 'yo', 'zh-CN',
    'zh-TW', 'zu']

available_languages = []
not_found = []
for lang in init_available_languages:
    
    pretty_lang = (pycountry.languages.get(alpha_2 = lang))

    if pretty_lang is None:
        not_found.append(lang)
        lang_name = ""
    else:
        lang_name = pretty_lang.name

    final_lang = f"{lang} - {lang_name}"

    available_languages.append(final_lang)

