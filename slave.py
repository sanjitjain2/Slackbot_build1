import os
import slackclient
import time
import random
import requests, bs4, sys
import json
import urllib2
from lang_translator import translate

#from scrabble.py(whatever is the name)
import scrabble

'''
In scrabble.py file make function scrabble() and include all code there
add rack as the argument of the function and don't take it from the user
return a list of all possible words along with points
'''
###Add this in slave.py

#from google_search import search_google

#export SLAVE_SLACK_TOK
#export SLAVE_SLACK_NAME=slavebot
#export SLAVE_SLACK_ID=U60R56RP1

#delay in seconds before checkking for new events
SOCKET_DELAY = 1

#slackbot enviornment variables
SLAVE_SLACK_NAME ='slavebot'
SLAVE_SLACK_TOKEN = 'xoxb-204855229783-8LKQPVWIT61qU7vlUs6HhicA'
SLAVE_SLACK_ID = 'U60R56RP1'

slave_slack_client = slackclient.SlackClient(SLAVE_SLACK_TOKEN)


def is_for_me(event):
    """Know if the message is dedicated to me"""
    # check if not my own event
    type = event.get('type')
    if type and type == 'message' and not(event.get('user')==SLAVE_SLACK_ID):
        # in case it is a private message return true
        if is_private(event):
            return True
        # in case it is not a private message check mention
        text = event.get('text')
        channel = event.get('channel')
        if slave_slack_mention in text.strip().split():
            return True


def is_private(event):
    """Checks if private slack channel"""
    return event.get('channel').startswith('D')

#how the bot is mentioned on slack
def get_mention(user):
    return '<@{user}>'.format(user=user)
    
slave_slack_mention = get_mention(SLAVE_SLACK_ID)

def handle_message(message,user,channel):
    
    if is_translate( message):
        tell_translation(message, channel)
    
    elif is_hi(message):
        user_mention = get_mention(user)
        post_message(message=say_hi(user_mention),channel=channel)

    elif is_google_search(message):
        user_mention = get_mention(user)
        edit_message = message
        post_message(message='Googling... ' + edit_message.split(' ',1)[1],channel=channel)
        for counter_var in range(1,6):
            post_message(message=search_google(edit_message.split(' ',1)[1],channel,counter_var),channel=channel)
    
    elif is_weather( message):
            tell_weather(message, channel)
        
    elif is_time( message):
            mention = get_mention( user)
            post_message( tell_time(mention), channel)

    elif is_bye(message):
        user_mention = get_mention(user)
        post_message(message=say_bye(user_mention),channel=channel)
        
    elif is_scrabble(message):
        scrabble_cheat(message, channel)
    
    else:
        post_message(message='Not sure what you have just said!',channel=channel)

def post_message(message,channel):
    slave_slack_client.api_call('chat.postMessage',channel=channel,text=message,as_user=True)



def is_hi(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens for g in ['hello', 'bonjour', 'hey', 'hi', 'sup', 'morning', 'hola', 'ohai', 'yo'])


def is_bye(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens for g in ['bye', 'goodbye', 'revoir', 'adios', 'later', 'cya'])


def is_time( message):
    message.replace('?', '')
    return any( st in message.strip().lower() for st in ['time', 'what is the hour of the day', 
            'tell me the date today', "what's the day today", 'date', "what's the date today"])


def tell_time(user_mention):
    return str(time.ctime()) + str(user_mention)

def say_hi(user_mention):
    #Say HI to a user by formatting their mention
    response_template = random.choice(['Sup, {mention}...',
                                       'Yo!',
                                       'Hola {mention}',
                                       'Bonjour!'])
    return response_template.format(mention=user_mention)


def say_bye(user_mention):
    #Say BYE to a user
    response_template = random.choice(['see you later, alligator...',
                                       'adios amigo',
                                       'Bye {mention}!',
                                       'Au revoir!'])
    return response_template.format(mention=user_mention)


def is_weather( message):
    return any( message.strip().lower().startswith(st) for st in ['weather', 'tell me weather'])


def weather_forecast(place):
    base_url = 'http://api.openweathermap.org/data/2.5/forecast?q='
    url = base_url + place + 'india&APPID=041d68834f4ca8f569d71cd6df88ae61'
    data = json.load(urllib2.urlopen(url))
    return data


def tell_weather( message, channel):
    place = message.split()[-1]
    data2 = weather_forecast(place)
    post_message('Condition: ' + data2['list'][0]['weather'][0]['main'] + ' (' + data2['list'][0]['weather'][0]['description']   
                 + ')', channel)
    post_message('Temperature: ' + str(float(data2['list'][0]['main']['temp']) - 273.15) + ' Celsius', channel)
    
    
def is_translate( message):
    if message.lower().startswith('translate'):
        return True
    else:
        return False


def tell_translation( message, channel):
    msg = translate(message)
    post_message(msg, channel)


def run():
    if slave_slack_client.rtm_connect():
        print ('[.] SlaveBot is ON...')
        while True:
            event_list = slave_slack_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    if event.get('type') == 'message':
                        print event
                    if is_for_me(event):
                        handle_message(message=event.get('text'),
                                   user=event.get('user'), channel=event.get('channel'))
                        time.sleep(SOCKET_DELAY)
    else:
        print('[.] Connection to SlaveBot failed.')

#ADDING OF MODULES BEGIN HERE

def is_google_search(message):
    #Check if message sent is query for google search results
    tokens = [word.lower() for word in message.strip().split()]
    for g in ['google', 'search']:
        if g in tokens:
            return True
    else:
        return False

def search_google(query,channel,i):
    res = requests.get('http://www.google.com/search?q=' + query)

    try:
        res.raise_for_status()
    except Exception as exc:
        post_message(message='There was a problem',channel=channel)
    
    #retrieve top search results links
    soup = bs4.BeautifulSoup(res.text,"html5lib")

    #Open a browser tab for each result
    linkElems = soup.select('.r a')
    numOpen = min(5,len(linkElems))

    return (linkElems[i+1].get('href')[len('/url?q='):])

#rating
def getURL(page):							# getting the url to use in checking rating 
    """
    :param page: html of web page (here: Python home page) 
    :return: urls in that page 
    """
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote
    
def movie_rating(url):
	source_code=requests.get(url)
	plain_text=source_code.text 
	soup=bs4.BeautifulSoup(plain_text,"html5lib")
	for line in soup.findAll('span', {'itemprop':'ratingValue'}, {'class':'rating-box__value'}):
		print line.string + str("/10")

def movie():
	movie=raw_input("which movie rating you want?")
	u=str("http://www.imdb.com/find?ref_=nv_sr_fn&q=")+str(movie)+str("&s=all")
	response = requests.get(u)
	page = str(bs4.BeautifulSoup(response.content,"lxml"))
	rate=[]
	while True:
	    url, n = getURL(page)
	    page = page[n:]
	    url=''.join(url)
	    check=url.startswith('/title/')
	    if check:
	        link=str("http://www.imdb.com")+str(url)
	        rate=movie_rating(link)
	        break

def hotel_rating(url):
	source_code=requests.get(url)
	plain_text=source_code.text 
	soup=bs4.BeautifulSoup(plain_text,"html5lib")
	for line in soup.findAll('span', {'itemprop':'ratingValue'}, {'class':'rating-box__value'}):
		print line.string + str("/100")
		return

def hotel():
	hotel=raw_input("")+str(" trivago")
	url ="https://www.google.com/search?q="+str(hotel)
	response = requests.get(url)
	page = str(bs4.BeautifulSoup(response.content,"lxml"))	
	rate=[]
	while True:
	    url, n = getURL(page)
	    page = page[n:]
	    url=''.join(url)
	    check=url.startswith('/url?q=')
	    if check:
	        url=url[7:]
	    	break
	hotel_rating(url)
#to get movie rating call the function
#	movie()
#to get hotel rating call the function
#	hotel()

if __name__ == "__main__":
    run()
#func1
def is_scrabble(message):
    if message.lower().startswith('scrabble','How many words','points','scores','jumble'):
        return True
    else:
        return False
    
#func2
def scrabble_cheat(message, channel):
    rack = message.split() [1]
    words = scrabble(rack)
    result= 'All valid words are: \n'
    for word in words:
        result += word + '\n'
    post_message(result, channel)  
 

    
