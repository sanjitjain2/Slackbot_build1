# -*- coding: utf-8 -*-

#xoxp-93050519090-93234884004-233665289968-a817ab3df828ec7527d96cf6a92b2649
#(Slack web api token)

from gtts import gTTS
def text_to_speech(txt, language):
    tts = gTTS(text=u''+txt, lang=language, slow=False)
    #tts = gTTS(text=u'आप पागल हो? क्या आप अपना मुंह बंद नहीं कर सकते?', lang='hi', slow=False)
    #tts = gTTS(text=u'তোমার সম্পর্কে আমাকে কিছু বল.', lang='bn', slow=False)
    #tts = gTTS(text='What the hell are you doing? Cannot you do it properly.', lang='hi', slow=False)
    #tts = gTTS(text="Dans l'arriere-pays de Provence,  30 kilometres au sud-ouest de Draguignan, l'Abbaye du Thoronet est un chef-d'uvre de l'art roman provenal.", lang='fr', slow=False)

    #tts = gTTS(text='Mon nom est ici', lang='en', slow=False)
    tts.save('hello.mp3')

if __name__ == '__main__':
    text_to_speech('What the hell are you doing? Cannot you do it properly.', lang='en')
















'''
import sys      #for cmd line argv
import time     #for delay
import pygst        #for playing mp3 stream
import gst      # " "

#take command line args as the input string
input_string = "What the hell are you doing? Cannot you do it properly."
#remove the program name from the argv list
#input_string.pop(0)

#convert to google friendly url (with + replacing spaces)
tts_string = '+'.join(input_string)

print tts_string

#use string in combination with the translate url as the stream to be played
music_stream_uri = 'http://translate.google.com/translate_tts?tl=es&q=' + tts_string
player = gst.element_factory_make("playbin", "player")
player.set_property('uri', music_stream_uri)
player.set_state(gst.STATE_PLAYING)

#requires a delay, if the py process closes before the mp3 has finished it will be cut off.
time.sleep(12)'''
