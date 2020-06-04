#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import random
import string # to process standard python strings
import json
import speech_recognition as sr
import time 
import num2words
import re
import string
from num2words import num2words
from difflib import SequenceMatcher
#sudo pip3 install --upgrade speechrecognition
#sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
#sudo apt-get install ffmpeg libav-tools
#sudo pip3 install pyaudio
#sudo pip3 install num2words


# In[3]:


def remove_punctuation(file):
    punctu = string.punctuation + '“”' + '–'
    punctu = punctu.replace('-', '')
    file = file.replace('/', ' ')
    file_withoutpunct = [char for char in file if char not in punctu]
    x = ''.join(file_withoutpunct)
    x = x.replace('-', ' ')
    return x


# In[4]:


def change_to_lower(file):
    return file.lower()


# In[5]:


def remove_accents(file):
    file = file.replace('á', 'a')
    file = file.replace('é', 'e')
    file = file.replace('í', 'i')
    file = file.replace('ó', 'o')
    file = file.replace('ú', 'u')
    return file


# In[6]:


def find_floats_replace(file):
    dec = [float(s) for s in re.findall('\d+\.+\d', file)] #array with all the decimals in the text
    towords = [num2words(i, lang = 'es') for i in dec] #change these numbers to words in spanish
    for i in range(len(dec)): 
        dec[i] = '{}'.format(dec[i]) #convert the decimals into strings with the decimals inside
    for i in range (len(dec)):
        file = file.replace(dec[i], towords[i]) #replace the decimals by words in the file
    return file


# In[7]:


def find_integers_replace(file):
    dec = [int(s) for s in re.findall('\d+', file)] #list of numbers that appear in the text
    towords = [num2words(i, lang = 'es') for i in dec] #change that list to words
    for i in range(len(dec)):
        dec[i] = '{}'.format(dec[i])
    for i in range (len(dec)):
        file = file.replace(dec[i], towords[i])
    return file


# In[8]:


def remove_percent_floats(file):
    cases1 = [str(s) for s in (re.findall('\d+\.+\d%', file))] #or re.findall('\d+ + %', file)
    cases2 = [str(s) for s in re.findall('\d+\.+\d+ +%', file)]
    cases = cases1 + cases2
    numpercent = []
    for i in cases:
        numpercent.append(re.findall('\d+\.+\d', i))
    numpercent = [item for sublist in numpercent for item in sublist]
    for i in range(len(numpercent)):
        numpercent[i] = num2words(numpercent[i])
        numpercent[i] = '{} por ciento'.format(numpercent[i])
    for i in range(len(cases)):
        file = file.replace(cases[i], numpercent[i])
    return file


# In[9]:


def remove_percent(file):
    cases1 = [str(s) for s in (re.findall('\d+%', file))] #or re.findall('\d+ + %', file)
    cases2 = [str(s) for s in re.findall('\d+ +%', file)]
    cases = cases1 + cases2
    numpercent = []
    for i in cases:
        numpercent.append(re.findall('\d+', i))
    numpercent = [item for sublist in numpercent for item in sublist]
    for i in range(len(numpercent)):
        numpercent[i] = num2words(numpercent[i])
        numpercent[i] = '{} por ciento'.format(numpercent[i])
    for i in range(len(cases)):
        file = file.replace(cases[i], numpercent[i])
    return file


# In[10]:


def final_normalization(file):    
    file = remove_percent_floats(file)
    file = remove_percent(file)
    file = change_to_lower(file)
    file = find_floats_replace(file)
    file = remove_punctuation(file)
    file = find_integers_replace(file)
    file = remove_punctuation(file)
    file = remove_accents(file)
    return file


# In[11]:


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# In[12]:


GREETING_INPUTS = ["hola", "ola", "buenos dias", "que pasa", "como estas","ey"]
GREETING_RESPONSES = ["Hola", "Buenos días", "Que pasa!", "Cómo va?", "Contenta de verte!", "Que bien, tu por aquí!"]
def greeting(sentence):
    sentence = final_normalization(sentence)
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# In[13]:


opcion1 = ['reproducir', 'escuchar']
opcion2 = ['nombre cancion', 'titulo']
opcion3 = ['nombre cantante','cantante', 'grupo', 'quien', 'artista']
opcion4 = ['lyric', 'letra']


# In[14]:


with open('prueba.json') as file:
    data = json.load(file)


# In[15]:


def response(user_response, i):
    with sr.Microphone() as mp:
        audio = r.listen(mp)
        try:
            print('ROBO: Ahora te digo...')
            do = r.recognize_google(audio, language='es-ES')
            time.sleep(1.5)
            print('USER: ' + do)
            do = final_normalization(do)
            do = do.split()
            if 'todo' in do:
                response  = ('ROBO:' + data[i]['Song'] + ' - ' + data[i]['Author'] + ' y este es el link de youtube:\n' + data[i]['Link'] + '\n' + 'y esta es la letra:\n' + data[i]['Lyric'])
                print(response)
            else:
                check1 = any(item in do for item in opcion1) #link
                check2 = any(item in do for item in opcion2) #titulo
                check3 = any(item in do for item in opcion3) #artista
                check4 = any(item in do for item in opcion4) #lyrics
                print('ROBO: ')
                if (check1 == True): 
                    response = ('Link de youtube:\n' + data[i]['Link'])
                    print(response)  
                if (check2 == True):
                    response = data[i]['Song']
                    print(response)
                if (check3 == True):
                    response = data[i]['Author']
                    print(response)
                if (check4 == True):
                    response = 'Esta es la letra:\n' + data[i]['Lyric']
                    print(response)
            
        except:
            print('ROBO: Lo siento, no he entendido que opción elegías')


# In[16]:


def similarity(sentence1, sentence2, level):
    sentence1 = sentence1.split()
    sentence2 = sentence2.split()
    if len(sentence1)>len(sentence2):
        larger = sentence1
        smaller = sentence2
    else: 
        larger = sentence2
        smaller = sentence1
    new = []
    for i in range(len(larger)):
        x = []
        if i > (len(larger)-(len(smaller))):
                break
        for j in range(len(smaller)):
            x.append(larger[i+j])
        x = ' '.join(x)
        new.append(x)
    smaller = ' '.join(smaller)
    for j in new:
        if (similar(j, smaller)>=level):
            return True
    return False


# In[21]:


def song_in_db(user_response):
    aux = []
    array = []
    for i in data:
        lyrics = (i['Lyric'])
        lyrics = final_normalization(lyrics)
        array.append(lyrics) #array = todas las lyrics
    for i in range(len(array)):
        user_response = final_normalization(user_response)
        if (similarity(array[i], user_response, 0.8) == True):
            aux.append(i)
        
    aux = list(dict.fromkeys(aux))
    if len(aux)>0:
        return True, aux
    else: return False           


# In[22]:


def opciones(user_response):
    if song_in_db(user_response)[0] == True:
        for i in range (len(song_in_db(user_response)[1])):            
            print("""ROBO: ¿Que quieres hacer? con la canción número {} de canciones encontradas
                              * Reproducir
                              * Título
                              * Cantante o grupo
                              * Letra
                              * Todo
                        """.format(i+1))
            response(user_response, song_in_db(user_response)[1][i])  
        return('ROBO: Hecho') 
    
    return 'ROBO: Not found'


# In[24]:


flag=True
print("""ROBO: Mi nombre es Robo. Te diré la cancion que estas buscando! 
        Si quieres salir, sólo tienes que decir adiós!""")
while(flag==True):
    r = sr.Recognizer()
    with sr.Microphone() as mp:
        print('ROBO: Dime')
        audio = r.listen(mp)
        try:
            print('ROBO: Leyendo el audio. Por favor, espera un momento..')
            user_response = r.recognize_google(audio, language='es-ES')
            time.sleep(1.5)
            print('USER: ' + user_response)
            user_response = final_normalization(user_response)
            if len(user_response.split())<3:
                if((similarity('gracias',user_response, 0.9)==True)):
                    flag=False
                    print("ROBO: De nada! Que vaya bien!")
                elif(greeting(user_response)!=None):
                    print("ROBO: "+ greeting(user_response))
                elif((similarity('adios',user_response, 0.9)==True)):
                    flag=False
                    print("ROBO: Adiós, cuídate!")
                else: print('ROBO: Necesito que me digas más de la canción...')
                
            elif((similarity('adios',user_response, 0.9) == True and song_in_db(user_response)[0]==False)):
                flag=False
                print("ROBO: Adiós, cuídate!")
            elif((similarity('gracias',user_response, 0.9) == True and song_in_db(user_response)[0]==False)):
                flag=False
                print("ROBO: De nada! Que vaya bien!")
            else: print(opciones(user_response))
        except:
            print('ROBO: Lo siento, no te entiendo!')

    


# In[ ]:




