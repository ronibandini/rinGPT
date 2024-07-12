#!/usr/bin/env python3

# Speech generation for RinGPT

import asyncio
import edge_tts

ttsVoice = "es-AR-TomasNeural"


async def myTtts(myText, myFile) -> None:
    global ttsVoice 
    communicate = edge_tts.Communicate(myText, ttsVoice)
    await communicate.save(myFile)

asyncio.run(myTtts("Eeee ¿qué necesitás?","quenecesitas.mp3"))
