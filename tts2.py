# -*- coding: utf-8 -*-
from gtts import gTTS

def text_to_speech(txt, language):
    tts = gTTS(text=u''+txt, lang=language, slow=False)
    #tts = gTTS(text='What the hell are you doing? Cannot you do it properly.', lang='hi', slow=False)
    #tts = gTTS(text="Dans l'arriere-pays de Provence,  30 kilometres au sud-ouest de Draguignan", lang='fr', slow=False)
    
    tts.save('hello.mp3')

if __name__ == '__main__':
    text_to_speech("What the hell are you doing? Can't you do it properly.", lang='en')


