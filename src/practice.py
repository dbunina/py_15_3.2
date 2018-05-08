#
# How to use:
#
# Run in folder which contains files to be translated.
# Translation results will be stored in 'result' folder.
#

import chardet
import os
import requests


def translate_it(source_file, target_file, source_lang, target_lang='ru'):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param source_file: <str> source file for translation.
    :param target_file: <str> result file for translated text.
    :param source_lang: <str> language which the source text is written in.
    :param target_lang: <str> language the text should be translated to.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    lang = '{src}-{target}'.format(src=source_lang, target=target_lang)
    text = load_text(source_file)

    params = {
        'key': key,
        'lang': lang,
        'text': text,
    }

    response = requests.get(url, params=params).json()
    result = ' '.join(response.get('text', []))

    create_translation_file(target_file, result)
    print('Translated {} from {} to {}; result: {}'.format(source_file, source_lang, target_lang, target_file))


def load_text(file):
    file_path = os.path.join(os.getcwd(), file)

    with open(file_path, 'rb') as f:
        encoding = chardet.detect(f.read())['encoding']

    with open(file_path, encoding=encoding) as f:
        return f.read()


def create_translation_file(target_file, translated_text):
    target_dir = os.path.dirname(os.path.join(os.getcwd(), target_file))

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    target_path = os.path.join(target_dir, os.path.basename(target_file))

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(translated_text)


def main():
    current_dir = os.getcwd()
    for source_file in os.listdir(current_dir):
        if source_file.endswith('.txt'):
            lang = os.path.splitext(source_file)[0]
            target_file = os.path.join('result', '{}_RU.txt'.format(lang))

            translate_it(source_file, target_file, lang.lower())


main()
