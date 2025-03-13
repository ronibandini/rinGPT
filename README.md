# RinGPT

RinGPT es un timbre que usa agentes de IA para responder las 24hs ya sea vía LLM o por medio de reglas personalizadas. Asimismo notifica por Telegram.

![RinGPT](https://github.com/user-attachments/assets/f702e61a-a0f9-4f77-8e60-76c93da765fd)

# Versiones

La version 1.0 es un LLM Powered doorbell
La version 2.0 es un AI Agent Powered doorbell y se encuentra en la carpeta [/2.0/](https://github.com/ronibandini/rinGPT/tree/main/2.0)

Más sobre la versión 2.0 en https://app.readytensor.ai/publications/ringpt-20-ai-agent-powered-doorbell-gcuSB4vQCesp y 
https://bandini.medium.com/recepcionista-con-agente-de-ia-v%C3%ADa-openai-4e56ba8ef6db

# 1.0 Requerimientos

Placa Unihiker de DFRobot
Parlante BlueTooth
Push button

# 1.0 Esquema

![Esquema](https://github.com/user-attachments/assets/c498c454-72fe-47c4-b2da-336b7062105e)


# 1.0 Procedimiento de paireo

Para pairear el parlante Bluetooth al Unihiker es necesario conectarse por consola y ejecutar

bluetoothctl

default-agent

power on

trust 00:00:00:00:00:00

pair 00:00:00:00:00:00

connect 00:00:00:00:00:00

# Instalación de dependencias

pip install SpeechRecognition

apt-get install flac

pip install openai

pip install edge-tts

pip install arts

# 1.0 KEY de OpenAI

Para obtener los keys de openAI es necesario ir a 

https://platform.openai.com/

# Settings

ttsVoice        = "es-AR-TomasNeural"
btn             = Pin(Pin.P23, Pin.IN)   
chatGPTKey      =""
tiempoGrabacion =5
pausaTimbre     =2
model           = "gpt-3.5-turbo-instruct"
temperature     =0.8
prompt1          ="Estás ocupado trabajando y tocan la puerta para preguntar: "
prompt2          ="¿Qué respondes?"
telegramEnabled  = 0
telegramBot     =""
telegramChatId  =""
defaultAnswer   ="Gracias, pero no puedo atender en este momento"

# Demo

https://www.youtube.com/watch?v=6RJs4HPoyds

# Contacto

Por cotización de proyectos con IA en Arduino o Raspberry 
https://x.com/RoniBandini
https://www.instagram.com/ronibandini/
