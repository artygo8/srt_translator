from selenium import webdriver
import time, chime, signal, sys
from selenium.webdriver.common.keys import Keys
import time
import pyperclip


# you can change these
CHIME_THEME = 'zelda'   # mario, zelda, material, big-sur or chime


# Colors
class Color:
    RED = (255, 100, 100)
    GREEN = (100, 255, 100)
    BLUE = (100, 100, 255)

colored = lambda rgb, text : f'\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{text}\033[30m'


class Translator:

    def __init__(self, language='fr'):
        try:
            self.driver = webdriver.Firefox()
            self.lang = language
            url = 'https://' + 'w' * 3 + '.' + ''.join(chr(ord(i) + e) for e, i in enumerate('ddcmh')) + '.com/' + language + '/translator'  # OBFUSCATION
            self.driver.get(url)
            
            time.sleep(2)
            self.source_textarea = self.driver.find_element_by_class_name('lmt__source_textarea')
            self.target_textarea = self.driver.find_element_by_class_name('lmt__target_textarea')
        except:
            exit(colored(Color.RED, 'Failed to start the webdriver'))

    def __del__(self):
        self.driver.quit()

    def translate_part(self, subcontent):
        ''' Since we can translate only 5k characters in Translator.'''
        self.source_textarea.clear()
        self.source_textarea.send_keys(subcontent)
        time.sleep(len(subcontent) // 500 + 2)
        self.target_textarea.send_keys(Keys.META, 'a')
        self.target_textarea.send_keys(Keys.META, 'c')
        return pyperclip.paste()

    def translate(self, content):
        lst = content.split('\n')
        tmp = ''
        result = ''
        while lst:
            while len(tmp) < 4000 and lst:
                tmp += lst.pop(0) + '\n'
            result += self.translate_part(tmp)
            tmp = ''
        return result


def signal_handler(sig, frame):
    chime.error()
    exit(colored(Color.BLUE, '\ngood-bye !'))


# MAIN

if __name__ == '__main__':

    chime.theme(CHIME_THEME)
    signal.signal(signal.SIGINT, signal_handler)
    chime.info()
    translator = Translator()

    if len(sys.argv) != 2:
        exit(colored(Color.RED, 'You need to provide a `.srt` file !'))

    input_file_name = sys.argv[1]
    output_file_name = input_file_name.replace('.srt', f'.translated_{translator.lang}.srt')

    with open(input_file_name, 'r') as infile:
        with open(output_file_name, 'w+') as outfile:
            outfile.write(translator.translate(infile.read()))

    chime.success()
    print(colored(Color.GREEN, 'the following file was created successfully: ' + output_file_name))
