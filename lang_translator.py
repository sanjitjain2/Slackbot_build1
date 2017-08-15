from googletrans import Translator

def translate(message):
    translator = Translator( service_urls=[
          'translate.google.com',
          'translate.google.co.kr',
        ])

    msg_arr = message.split()
    script = ' '.join(msg_arr[2:])
    lang = msg_arr[1]
    translations = translator.translate([script], dest=lang.replace('-', ''))

    for translation in translations:
        return 'Translated script is: \n' + translation.text
        #print(translation.origin, ' -> ', translation.text)

'''
Language Codes:
Dutch: nl
French: fr
Spanish: de
Danish: da
English: en'''
if __name__ == '__main__':
    print translate('translate fr- How are you?')
