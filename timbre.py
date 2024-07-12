# -*- coding: utf-8 -*-

# RinGPT
# Roni Bandini, July 2024
# Buenos Aires, Argentina
# https://bandini.medium.com

import time
import datetime
from pinpong.board import *
from pinpong.extension.unihiker import *
from unihiker import Audio
from unihiker import GUI
import speech_recognition as sr
from openai import OpenAI
from pathlib import Path
import asyncio
import edge_tts
import warnings
import uuid
import requests 
import os
import random
from art import *

warnings.filterwarnings('ignore')

Board().begin()  
audio = Audio()
gui = GUI()

# Settings
ttsVoice        = "es-AR-TomasNeural"
btnDoorbell     = Pin(Pin.P23, Pin.IN)   
btnProgre       = Pin(Pin.P22, Pin.IN)   
chatGPTKey      =""
tiempoGrabacion =5
pausaTimbre     =2
model           = "gpt-3.5-turbo-instruct"
temperature     =0.8
prompt1          ="Vivís en Buenos Aires y estás muy ocupado. Tocan la puerta por quinta vez y dicen: "
prompt2          =". Respondele en siete palabras o menos."
telegramEnabled  = 0
telegramBot     =""
telegramChatId  =""
defaultAnswer   ="Gracias, pero no puedo atender en este momento"

# default answers
recon   = ['ropita','ropa','Dios','medias','cuchillo','Nada']
answers = ['ropita','ropita','ateo','yacompre','afilador','nohaynadie']

client = OpenAI(api_key=chatGPTKey,)

gui.clear()
img = gui.draw_image(x=0, y=0, w=240, h=320, image='/home/timbre/images/portada.png')

def writeLog(myLine):
    now = datetime.datetime.now()
    dtFormatted = now.strftime("%Y-%m-%d %H:%M:%S")
    with open('log.txt', 'a') as f:
        myLine=str(dtFormatted)+","+myLine
        f.write(myLine+"\n")


def sendTelegram(message):
    global telegramBot
    global telegramChatId
    global telegramEnabled 
    apiURL = f'https://api.telegram.org/bot{telegramBot}/sendMessage'
    telegramMessage="RinGPT, hay alguien en la puerta: "+message

    if telegramEnabled==1:
        try:
            response = requests.post(apiURL, json={'chat_id': telegramChatId, 'text': telegramMessage})
            print(response.text)
        except Exception as e:
            print(e)

async def myTtts(myText, myFile) -> None:
    global ttsVoice 
    communicate = edge_tts.Communicate(myText, ttsVoice)
    await communicate.save('/home/timbre/audio/'+myFile)

def findAnswer(myText):

    myCounter=0 

    for x in recon:
      if x in myText:       
        return answers[myCounter]
        break

      myCounter=myCounter+1

    return "-"

os.system('clear')
Art=text2art("RinGPT") 
print(Art)
print("")
print("Roni Bandini, July 2024, MIT License")
print("")

while True:

    # read button
    v = btnDoorbell.read_digital()   
    
    if v==1 or button_a.is_pressed() == True:

        # button is pressed
        writeLog("Doorbell")

        print("Timbre...")
        buzzer.pitch(494, 4)          
        print("Doorbell sound")
        audio.play('/home/timbre/audio/doorbell.mp3')     

        myGreeting=random.randint(1, 3)

        if myGreeting==1:
            print("Hola. Quien es...")
            audio.play('/home/timbre/audio/quienes.mp3')
        if myGreeting==2:
            print("Diga")
            audio.play('/home/timbre/audio/diga.mp3')
        if myGreeting==3:
            print("Qué necesitás")
            audio.play('/home/timbre/audio/quenecesitas.mp3')

        print("Recording...")
        filename = str(uuid.uuid4())
        audio.record('/home/timbre/audio/'+filename +'.wav', tiempoGrabacion) 

        print("Wait a second...")
        audio.play('/home/timbre/audio/aguarde.mp3')

        print("Speech recognition")
        r = sr.Recognizer()
        audio_file = sr.AudioFile('/home/timbre/audio/'+filename +'.wav')
        with audio_file as source: 
           r.adjust_for_ambient_noise(source) 
           myAudio = r.record(source)          

        try:    
           result = r.recognize_google(myAudio,language="es-ES",key=None)

        except Exception as e:
           print("No response")
           writeLog("No answer")
           result="Nada"
           
                
        writeLog("Visitor says: "+result)

        # send telegram 
        sendTelegram(result)

        # check default answers
        fileName=findAnswer(result)

        # switch progre mode
        if btnProgre.read_digital()==1:            
            print("Progre mode enabled")
            fileName="progre"

        if fileName=="-":

            print("Calling ChatGPT...")
            print(prompt1+" "+result+" "+prompt2) 


            completion = client.completions.create(
                    model=model,
                    prompt=prompt1+" "+result+" "+prompt2,
                    max_tokens=200,
                    n=1,
                    stop=None,
                    temperature=temperature,
                )

            selectedItem=completion.choices[0].text

            print("ChatGPT answer:")
            print(selectedItem)
            

            if selectedItem=="":
                print("No answer from ChatGPT, use default")
                selectedItem=defaultAnswer           
                break

            writeLog("ChatGPT: "+selectedItem)

            # create audio for ChatGPT response            
            fileName = str(uuid.uuid4())            
            asyncio.run(myTtts(selectedItem,fileName+".mp3"))
            my_file = Path("/home/timbre/audio/"+fileName+".mp3")

            # wait until answer is ready
            while my_file.is_file()==False:
        	    print("Answer not ready...")        	    

        audio.play('/home/timbre/audio/'+fileName+'.mp3')

        print("Waiting for button...")

