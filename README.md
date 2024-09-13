# rinGPT

Timbre con IA que responde a toda hora y envía notificaciones por Telegram

# Requerimientos

Placa Unihiker
Parlante BlueTooth

# Procedimiento de paireo

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

# KEY de OpenAI

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
