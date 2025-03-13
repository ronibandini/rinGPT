# -*- coding: utf-8 -*-

# RinGPT 2.0
# AI-Powered Doorbell with Physical Tool Integration
# Roni Bandini, March 2025, Buenos Aires, Argentina
# https://github.com/ronibandini/rinGPT
# MIT License

from pinpong.board import *
from pinpong.extension.unihiker import *
from unihiker import Audio
from unihiker import GUI
from openai import OpenAI
import time
import datetime
import speech_recognition as sr
from pathlib import Path
import asyncio
import edge_tts
import warnings
import uuid
import requests 
import os
import random
import json
from art import *
import textwrap

warnings.filterwarnings('ignore')

Board().begin()  
audio = Audio()
gui = GUI()

################################################################## Settings
demoMode        = 1
ttsVoice        = "en-US-JennyNeural"
btnDoorbell     = Pin(Pin.P23, Pin.IN)   
door            = Servo(Pin(Pin.P0))
led             = Pin(Pin.P25, Pin.OUT)
np1             = NeoPixel(Pin((Pin.P13)),3)

chatGPTKey      =""
tiempoGrabacion =5
model           = "gpt-4"
temperature     = 0.1
myFolder          ="/home/doorbell/"

telegramEnabled  = 1
telegramBot     =""
telegramChatId  =""

################################################################# updateScreen
def textWrapper(texto, ancho=29):
    return "\n".join(textwrap.wrap(texto, width=ancho))

################################################################# updateScreen
def updateScreen(myLine):
    gui.clear()
    img = gui.draw_image(x=0, y=0, w=240, h=320, image=myFolder+'images/template.png')

    maxLength=26
    myY=90
    myX=25
    
    gui.draw_text(x=myX, y=myY, text=textWrapper(myLine, maxLength), font_size=10, color="black")

    gui.draw_text(x=45, y=303, text="RinGPT 2.0 - Roni Bandini", font_size=9, color="black")

################################################################# puerta
def puerta(accion):
    if accion==1:
        print("Opening the door")
        door.angle(180)
    else:
        print("Closing the door")
        door.angle(90)


def luzRoja():
    np1.brightness(128)
    np1.range_color(0,2,0xFF0000)
    time.sleep(1)   
    np1.brightness(0)

def luzVerde():
    np1.brightness(128)
    np1.range_color(0,2,0x00FF00)
    time.sleep(1)
    np1.brightness(0)
    
################################################################# agenda
def agenda(nombre):
    myAgenda = ["Ana Smith", "John Davidson"]
    if nombre in myAgenda:
        return "The visitor has an appointment"
    else:
        return "The visitor does not have an appointment"

################################################################# getDayTime

def getDayTime():

    # get current datetime
    dt = datetime.datetime.now()
    print('Datetime is:', dt)

    # get weekday name
    diaDeLaSemana=dt.strftime('%A')

    print('Day of the week:', diaDeLaSemana)

    return "Today is "+str(dt)+ " of a "+diaDeLaSemana


################################################################# mapearValor
def mapearValor(valor, min_origen=0, max_origen=4095, min_destino=0, max_destino=100):
    # Regla de tres simple
    return (valor - min_origen) * (max_destino - min_destino) / (max_origen - min_origen) + min_destino

################################################################# getLightConditions
def getLightConditions():
    lightValue = light.read()  # Read the ambient light intensity
    print("Intensidad de luz: %d" % (lightValue))     
    return "Light intensity: "+str(mapearValor(lightValue))+"%"

################################################################# writeLog
def writeLog(myLine):
    now = datetime.datetime.now()
    dtFormatted = now.strftime("%Y-%m-%d %H:%M:%S")
    with open('log.txt', 'a') as f:
        myLine=str(dtFormatted)+","+myLine
        f.write(myLine+"\n")

################################################################# sendTelegram

def sendTelegram(message):
    global telegramBot
    global telegramChatId
    global telegramEnabled 
    apiURL = f'https://api.telegram.org/bot{telegramBot}/sendMessage'
    telegramMessage="RinGPT, there is someone at the door unappointed: "+message

    if telegramEnabled==1:
        try:
            response = requests.post(apiURL, json={'chat_id': telegramChatId, 'text': telegramMessage})
            print(response.text)
        except Exception as e:
            print(e)

################################################################# myTTS
async def myTtts(myText, myFile) -> None:
    global ttsVoice 
    communicate = edge_tts.Communicate(myText, ttsVoice)
    await communicate.save(myFolder+'audio/'+myFile)


################################################################# main

client = OpenAI(api_key=chatGPTKey,)

gui.clear()
img = gui.draw_image(x=0, y=0, w=240, h=320, image=myFolder+'images/ringpt.png')

os.system('clear')
Art=text2art("RinGPT 2.0") 
print(Art)
print("")
print("Roni Bandini, March 2025, MIT License")
print("")


textoScreen=""

while True:

    # read on board button or external
    v = btnDoorbell.read_digital()   
    
    if v==1 or button_a.is_pressed() == True:

        # button is pressed
        writeLog("Ring")
        print("Ring...")
        textoScreen=textoScreen+"Doorbell\n"
        updateScreen(textoScreen)

        # play doorbell 
        print("Doorbell sound")
        audio.play(myFolder +'audio/doorbell.mp3')     
        time.sleep(1)        
        
        # answer
        print("Who is there...")
        textoScreen=textoScreen+"Please state your name and the purpose of your visit\n"
        updateScreen(textoScreen)
        audio.play(myFolder +'audio/quienes.mp3')    

        textoScreen=textoScreen+"Listening\n"
        updateScreen(textoScreen)
        print("Listening...")
        filename = str(uuid.uuid4())
        audio.record(myFolder+'audio/'+filename +'.wav', tiempoGrabacion) 

        # speech recon
        textoScreen=textoScreen+"Speech recognition\n"
        updateScreen(textoScreen)
        print("Speech recognition")
        r = sr.Recognizer()
        audio_file = sr.AudioFile(myFolder+'audio/'+filename +'.wav')
        with audio_file as source: 
           r.adjust_for_ambient_noise(source) 
           myAudio = r.record(source)          

        try:    
           desgrabacion = r.recognize_google(myAudio,key=None)       

        except Exception as e:
           print("No response")
           writeLog("No answer")
           desgrabacion=""                       

        # for demo purposes
        if demoMode==1 and desgrabacion=='':      
           #desgrabacion="Hi there. I'm John Davidson. I have an appointment with Mr. Smith" 
           desgrabacion="I'm officer Karadagian" 

        textoScreen=textoScreen+"Says: "+desgrabacion+"\n"
        updateScreen(textoScreen)   

        writeLog("Says: "+desgrabacion)
        print("Says: "+desgrabacion)                

        function_descriptions = [
            {
                "name": "getName",
                "description": "Get the visitors name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nombre": {
                            "type": "string",
                            "description": "Name of the visitor",
                        }
                    },
                "additionalProperties": False,
                    "required": ["nombre"],
                },
            }
        ]
        
        # Get visitor's name

        print("")
        print("Extracting the name...")

        completion = client.chat.completions.create(
          model=model,
          messages=[
            {"role": "user", "content": desgrabacion}
          ],
          functions=function_descriptions,
          function_call="auto"
        )

        output = completion.choices[0].message

        if output.function_call==None:
            print("Could not get the name")
            print(output.content)
            sys.exit()

        nombre = json.loads(output.function_call.arguments).get("nombre")

        print("Extracted name: "+nombre)
        textoScreen=textoScreen+"Name: "+nombre+"\n"
        updateScreen(textoScreen)   
                
        # Agent tool selection

        systemContent = """
            You are an AI agent with access to the following tools:

            agenda(name): Determines if the visitor has an appointment.
            getDayTime(): Retrieves the day of the week and time.
            getLightConditions(): Retrieves the street lighting conditions.
            """

        systemContent += """
            Visitors are allowed on Monday, Tuesday, Wednesday, Thursday, and Friday between 9 AM and 6 PM.
            The only exception is Officer Karadagián, who may enter at any time, but only if there is at least 20% light in the hallway.
            To determine whether to open the door, which tools would you use and in what order?
            Example: If determining the day of the week is necessary to open the door, use getDayTime(), but do not include getLightConditions() unless required.
            Respond with a JSON containing a single key, tools, listing the function names in the correct order. 
            Valid output example:            
            {
              "tools": ["agenda", "getDayTime"]
            }

            Do not explain anything or answer with something else than the Json
            """

        completion = client.chat.completions.create(
            model=model,                

            messages=[
            {"role": "system", "content": systemContent},
            {"role": "user", "content": desgrabacion}
            ],
            max_tokens=1500,
            n=1,
            stop=None,
            temperature=temperature,
        )

        responseTools = completion.choices[0].message.content.strip()

        print("\nAI Agent selected tools:", responseTools)

        try:
            # Load Json
            toolsToUse = json.loads(responseTools)

            if "tools" in toolsToUse:
                print("\nTools:", toolsToUse["tools"])
            else:
                raise ValueError("Tools JSON doesnt have key 'tools'.")
                sys.exit()

        except (json.JSONDecodeError, ValueError) as e:
                print("Error: not valid Json.")
                print("Details:", str(e))
                sys.exit()

        # Compile tool response

        compilaRespuestaHerramientas = {}
        toolCounter=0

        for tool in toolsToUse["tools"]:

            if tool=="agenda":
                compilaRespuestaHerramientas["agenda"] = agenda(nombre)
                toolCounter=toolCounter+1
            if tool=="getDayTime":
                compilaRespuestaHerramientas["getDayTime"] = getDayTime()
                toolCounter=toolCounter+1
            if tool=="getLightConditions":
                compilaRespuestaHerramientas["getLightConditions"] = getLightConditions()
                toolCounter=toolCounter+1
        
        print("Tools calling ended")
        respuestaDeHerramientas = compilaRespuestaHerramientas

        print("Tools answer: ",respuestaDeHerramientas)
        textoScreen="Selected tools: "+str(toolCounter)+"\n"
        updateScreen(textoScreen)   
                
        # Agent final decision

        systemContent ="""             
            You are an AI receptionist. 

            Only visitors are allowed on Monday, Tuesday, Wednesday, Thursday, and Friday between 9 AM and 6 PM.
            The door is only opened for visitors listed in the agenda.
            The only exception is Officer Karadagián, who may enter at any time, but only if there is at least 15% light in the hallway.

            Indicate whether the door will be opened by returning a JSON object with two keys: actions and motivos.

            In actions, specify "abrir" to open the door or "cerrar" to keep it closed.
            In motivos, provide the reasons for the decision made.
            {
              "actions": ["abrir"],
              "motivos": ["Scheduled visitor attending during working hours."]
            }

            """

        promptDoor ="A visitor rings the bell and says: " +desgrabacion+" The context is: "+str(respuestaDeHerramientas)

        completion = client.chat.completions.create(
            model=model,
             messages=[
            {"role": "system", "content": systemContent},
            {"role": "user", "content":  promptDoor}
            ],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=temperature,
        )

        responseActions=completion.choices[0].message.content.strip()
        
        try:
            doorResponse = json.loads(responseActions)
            motivos=str(doorResponse["motivos"])
            acciones=str(doorResponse["actions"]).strip()
        except json.JSONDecodeError:
            print("Error: not a valid Json for door response.")
            writeLog("Error: not a valid Json for door response.")
            sys.exit()
            
        writeLog("Agent decision: "+str(doorResponse))
        print("Agent decision: "+str(doorResponse))  
        textoScreen=textoScreen+"Resolución: "+str(doorResponse)+"\n"
        updateScreen(textoScreen)  

        # Compose Agent's answer
        systemContent ="""             
            You are an AI receptionist
            """

        if "abrir" in acciones:
            mensajeAlVisitante="Welcome the visitor with a brief reference to the current time, which is "+str(getDayTime())+".Do not ask any additional questions. Simply greet the visitor. Example if it's early: Welcome, the early bird gets the worm. Example if it's late: Welcome and please note that the office closes at 6 PM. "
        else:
            mensajeAlVisitante="Tell the visitor, named "+nombre+", that company policy does not allow entry. Do not ask any additional questions or add any other information."         

        completion = client.chat.completions.create(
            model=model,
             messages=[
            {"role": "system", "content": systemContent},
            {"role": "user", "content":  mensajeAlVisitante}
            ],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=temperature,
        )

        respuestaFinal=completion.choices[0].message.content.strip()

        # Open the door or notify

        if "abrir" in acciones:
            luzVerde()
            puerta(1)
            time.sleep(3)
            puerta(0)
        else:
            luzRoja()
            print("Acciones: ",acciones)
            sendTelegram(nombre)                      
        
        # TTS for final response

        print("Visitor response: "+respuestaFinal+"\n")
        textoScreen=str(respuestaFinal)
        updateScreen(textoScreen)  
        
        print("Creates audio")            
        fileName = str(uuid.uuid4())            
        asyncio.run(myTtts(respuestaFinal,fileName+".mp3"))
        my_file = Path(myFolder+"audio/"+fileName+".mp3")

        # Espera hasta que se encuentre listo el audio

        while my_file.is_file()==False:
            print("Answer not ready...")                
        
        print("Answering")

        # Play
        audio.play(myFolder +'audio/'+fileName+'.mp3')

        time.sleep(2)

        gui.clear()
        img = gui.draw_image(x=0, y=0, w=240, h=320, image=myFolder +'images/ringpt.png')

