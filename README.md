# 🔔🤖 RinGPT

**AI-powered doorbell and autonomous receptionist built with Python, UNIHIKER, speech recognition, OpenAI models, Telegram, sensors, and physical tools.**

RinGPT replaces a conventional home doorbell with a system capable of answering visitors automatically.

The project started in 2024 as an **LLM-powered doorbell**: when somebody rings, RinGPT records the visitor, converts speech to text, checks predefined rules, asks an OpenAI model for a short response when necessary, generates speech, and can send a Telegram notification.

In 2025, **RinGPT 2.0** extended the concept into an **AI Agent-powered receptionist**. The agent can identify visitors, inspect a meeting agenda, check the current date and time, read the UNIHIKER light sensor, decide which tools to use, and determine whether a visitor should be admitted.

```text
Visitor
   │
   ▼
Doorbell
   │
   ▼
UNIHIKER
   │
   ├── Microphone
   ├── Speaker
   ├── Buttons
   ├── Light sensor
   └── GPIO
   │
   ▼
Speech Recognition
   │
   ▼
OpenAI
   │
   ├── LLM response
   └── AI Agent / tools
   │
   ├──────────────┐
   ▼              ▼
Telegram       Door control
```

---

## ✨ Features

- 🔔 AI-powered doorbell
- 🧠 LLM-generated visitor responses
- 🤖 AI Agent architecture in version 2.0
- 🎙️ Audio recording using the UNIHIKER microphone
- 🗣️ Speech-to-text conversion
- 🔊 Text-to-speech responses
- 🎵 Bluetooth speaker output
- 📲 Telegram notifications
- ⚡ Predefined responses for frequent visitors
- 🎲 Randomized greetings
- 📝 Interaction logging
- 📅 Agenda lookup tool
- 🕒 Date and time tool
- 💡 Ambient-light sensing
- 🚪 Servo-controlled door prototype
- 🖥️ UNIHIKER touchscreen interface
- 🐍 Python implementation

---

## 🧬 Versions

### RinGPT 1.0 — LLM-powered doorbell

The original version was developed in July 2024.

Its job is primarily conversational:

```text
Doorbell pressed
       │
       ▼
Play doorbell sound
       │
       ▼
Play random greeting
       │
       ▼
Record visitor for 5 seconds
       │
       ▼
Speech recognition
       │
       ├── Known keyword?
       │       │
       │       └── Play predefined response
       │
       └── No predefined response
               │
               ▼
        OpenAI completion
               │
               ▼
          Edge TTS
               │
               ▼
        Bluetooth speaker
```

It can also send the visitor transcript through Telegram.

Main file:

```text
timbre.py
```

---

### RinGPT 2.0 — AI Agent-powered receptionist

Version 2.0 was developed in 2025 and is located in:

```text
2.0/
```

Instead of using the LLM only to generate dialogue, version 2.0 gives the system access to **tools**.

```text
Visitor speaks
      │
      ▼
Identify visitor
      │
      ▼
AI Agent
      │
      ├── agenda()
      ├── getDayTime()
      └── getLightConditions()
      │
      ▼
Evaluate available information
      │
      ▼
Final decision
      │
      ├── Respond
      ├── Notify owner
      └── Unlock prototype door
```

The implementation uses plain Python and OpenAI API calls rather than a dedicated agent framework.

Main script:

```text
2.0/ringpt1.py
```

---

# 🧰 Hardware

## Version 1.0

| Qty | Component | Purpose |
|---:|---|---|
| 1 | **DFRobot UNIHIKER M10** | Main computer, microphone, screen and GPIO |
| 1 | Bluetooth speaker | Visitor audio |
| 1 | Push button / existing doorbell switch | Doorbell input |
| 1 | LED button | Alternate operating mode |
| — | Jumper / Gravity cables | Connections |

### UNIHIKER

Official product and documentation:

- [DFRobot UNIHIKER](https://www.dfrobot.com/product-2691.html)
- [UNIHIKER Documentation](https://www.unihiker.com/wiki/)

UNIHIKER provides:

- Debian-based operating system
- integrated microphone
- touchscreen
- Wi-Fi
- Bluetooth
- light sensor
- accelerometer
- buttons
- GPIO / Gravity interfaces

---

## Version 2.0

Version 2.0 adds physical actuation.

| Qty | Component |
|---:|---|
| 1 | UNIHIKER M10 |
| 1 | UNIHIKER IO Extender / Carrier |
| 1 | LED push button |
| 1 | 9 g servo motor |
| 1 | Bluetooth speaker |

The Hackster prototype uses an **SG90-class servo** to represent the physical door lock.

---

# 🔌 Connections

## Version 1.0

The current `timbre.py` source defines:

```python
btnDoorbell = Pin(Pin.P23, Pin.IN)
btnProgre = Pin(Pin.P22, Pin.IN)
```

Therefore:

| Function | UNIHIKER |
|---|---|
| Doorbell input | `P23` |
| Secondary mode button | `P22` |

The original doorbell switch is connected between:

```text
P23
 │
 └── Doorbell switch ── GND
```

---

## Version 2.0

The documented prototype uses:

```text
Doorbell button → P23
Servo           → P0 on IO board
```

The servo represents an electronic door-lock mechanism in the prototype.

---

# ⚙️ RinGPT 1.0

## Current settings

The source exposes the main configuration values near the beginning of `timbre.py`:

```python
ttsVoice = "es-AR-TomasNeural"

btnDoorbell = Pin(Pin.P23, Pin.IN)
btnProgre = Pin(Pin.P22, Pin.IN)

chatGPTKey = ""

tiempoGrabacion = 5
pausaTimbre = 2

model = "gpt-3.5-turbo-instruct"
temperature = 0.8

telegramEnabled = 0
telegramBot = ""
telegramChatId = ""

defaultAnswer = "Gracias, pero no puedo atender en este momento"
```

---

# 🎵 Doorbell sequence

When the button is detected, RinGPT first produces a buzzer tone:

```python
buzzer.pitch(494, 4)
```

and then plays:

```text
doorbell.mp3
```

The software randomly selects one of three greetings:

```text
Hola. ¿Quién es?
Diga
¿Qué necesitás?
```

These correspond to prerecorded audio files.

---

# 🎙️ Recording the visitor

The default recording duration is:

```python
tiempoGrabacion = 5
```

The recording is stored temporarily as a randomly named WAV file:

```python
filename = str(uuid.uuid4())

audio.record(
    '/home/timbre/audio/' + filename + '.wav',
    tiempoGrabacion
)
```

This avoids overwriting previous filenames during execution.

---

# 🗣️ Speech recognition

Version 1.0 uses Python's:

```python
speech_recognition
```

package.

The recorded WAV file is loaded with:

```python
audio_file = sr.AudioFile(
    '/home/timbre/audio/' + filename + '.wav'
)
```

and recognized using:

```python
r.recognize_google(
    myAudio,
    language="es-ES",
    key=None
)
```

The transcript is then used by the response logic.

---

# ⚡ Predefined responses

Not every visitor interaction requires an LLM request.

The source contains two parallel lists:

```python
recon = [
    'ropita',
    'ropa',
    'Dios',
    'medias',
    'cuchillo',
    'Nada'
]

answers = [
    'ropita',
    'ropita',
    'ateo',
    'yacompre',
    'afilador',
    'nohaynadie'
]
```

The helper function:

```python
findAnswer()
```

checks whether one of the predefined terms appears in the transcription.

```text
Visitor speech
      │
      ▼
Known keyword?
   │       │
  YES      NO
   │       │
   ▼       ▼
Preset    LLM
audio     response
```

This allows frequent situations to be handled immediately without calling an external model.

The lists can be replaced with other terms and responses.

---

# 🔀 Secondary response mode

The button on:

```text
P22
```

activates an alternate response mode:

```python
if btnProgre.read_digital() == 1:
    fileName = "progre"
```

This bypasses the usual response-selection flow and plays the corresponding preset audio.

---

# 🧠 LLM response

When there is no predefined answer, version 1.0 sends the transcription to OpenAI.

The current source uses:

```python
model = "gpt-3.5-turbo-instruct"
```

with the legacy Completions API:

```python
completion = client.completions.create(
    model=model,
    prompt=prompt1 + " " + result + " " + prompt2,
    max_tokens=200,
    n=1,
    stop=None,
    temperature=temperature
)
```

The prompt currently asks the model to respond in seven words or fewer.

Example structure:

```text
You live in Buenos Aires and are very busy.
The doorbell rings for the fifth time and they say:

<visitor transcript>

Reply in seven words or fewer.
```

---

# ⚠️ OpenAI model compatibility

The current source uses:

```text
gpt-3.5-turbo-instruct
```

which OpenAI currently classifies as an **older, deprecated model compatible only with the legacy Completions endpoint**.

Official documentation:

[OpenAI — gpt-3.5-turbo-instruct](https://developers.openai.com/api/docs/models/gpt-3.5-turbo-instruct)

A modernized version of RinGPT should migrate the generation logic to a currently supported model and API while preserving the surrounding doorbell workflow.

---

# 🔊 Text-to-speech

Dynamic replies are converted to audio using:

```python
edge_tts
```

The default voice is:

```python
ttsVoice = "es-AR-TomasNeural"
```

Audio is generated with:

```python
communicate = edge_tts.Communicate(
    myText,
    ttsVoice
)

await communicate.save(
    '/home/timbre/audio/' + myFile
)
```

The resulting MP3 is played through the paired Bluetooth speaker.

Project:

[edge-tts](https://github.com/rany2/edge-tts)

---

# 📲 Telegram notifications

RinGPT can send the visitor transcript through Telegram.

Enable it with:

```python
telegramEnabled = 1
```

and configure:

```python
telegramBot = ""
telegramChatId = ""
```

The request is sent to:

```text
https://api.telegram.org/bot<TOKEN>/sendMessage
```

The message begins with:

```text
RinGPT, hay alguien en la puerta:
```

followed by the recognized speech.

Telegram Bot API:

[core.telegram.org/bots/api](https://core.telegram.org/bots/api)

---

# 📝 Logging

Interactions are appended to:

```text
log.txt
```

with timestamps:

```python
now = datetime.datetime.now()
dtFormatted = now.strftime("%Y-%m-%d %H:%M:%S")
```

Logged events include:

- doorbell activations
- recognized visitor speech
- recognition failures
- ChatGPT responses
- other system actions

This is particularly useful because RinGPT is designed to operate unattended.

---

# 🤖 RinGPT 2.0

Version 2.0 transforms the concept from:

```text
LLM answers visitor
```

into:

```text
AI Agent
  │
  ├── observes
  ├── chooses tools
  ├── executes them
  └── makes a decision
```

---

## 🔄 Version 2.0 workflow

```text
Doorbell button
      │
      ▼
Play doorbell sound
      │
      ▼
Record visitor
      │
      ▼
Speech Recognition
      │
      ▼
OpenAI call #1
Extract visitor name
      │
      ▼
OpenAI call #2
Select relevant tools
      │
      ▼
Execute tools
      │
      ├── agenda()
      ├── getDayTime()
      └── getLightConditions()
      │
      ▼
Compile tool results
      │
      ▼
OpenAI decision
      │
      ├── open door
      └── notify owner
      │
      ▼
Generate spoken response
```

---

# 🛠️ AI Agent tools

The documented version exposes:

```python
def agenda(nombre):
    ...

def getDayTime():
    ...

def getLightConditions():
    ...
```

---

## 📅 `agenda(nombre)`

Checks whether a visitor appears in the current schedule.

The reference implementation uses hardcoded appointments.

It can be replaced with data from systems such as:

```text
Google Calendar
CalDAV
CRM
local database
REST API
n8n workflow
```

---

## 🕒 `getDayTime()`

Returns temporal context that the agent can use while deciding how to respond.

This gives the receptionist information such as the current date or time rather than requiring it to infer temporal context.

---

## 💡 `getLightConditions()`

Reads the UNIHIKER onboard light sensor.

The tool demonstrates that an AI agent can combine:

```text
software information
+
physical sensor information
```

before making a decision.

---

# 🚪 Physical actions

The version 2.0 prototype includes a servo attached to the IO expansion board.

The servo represents the action:

```text
unlock door
```

The prototype therefore demonstrates an AI workflow capable of affecting physical hardware.

Door actuation and Telegram notification are controlled by the program flow in the documented version rather than being exposed as fully autonomous agent tools.

---

# 🧠 Multiple LLM calls

Version 2.0 separates different reasoning tasks rather than asking one prompt to perform everything.

The documented sequence uses:

### Call 1 — Identify visitor

Function calling extracts the visitor's name from natural speech.

For example:

```text
"Hi, I'm Martín, I have a meeting at three."
```

becomes structured visitor data.

### Call 2 — Choose tools

The system determines which available tools are relevant.

Possible output might require:

```text
agenda
+
date/time
```

### Tool execution

Python executes the requested functions.

### Final decision

The results are sent back to the model so the receptionist can determine what action should follow.

This structure allows data generated by code and sensors to participate in the final decision.

---

# 🧠 Memory

RinGPT 2.0 does not implement persistent global conversational memory.

Instead, relevant information such as:

```text
visitor name
```

is temporarily stored by Python and reused in later calls during the same interaction.

---

# 🧰 Version 2.0 dependencies

Install the documented dependencies with:

```bash
pip install openai speech_recognition edge_tts art asyncio textwrap
```

Some packages may already be part of the Python standard library depending on the environment and do not require separate installation.

The project also uses UNIHIKER-specific libraries already available on the board.

---

# 📡 UNIHIKER setup

Connect UNIHIKER to a computer through USB.

Open:

```text
http://10.1.2.3
```

to configure its network connection.

After the device is connected to Wi-Fi, SSH access is available using the IP assigned to the board.

The factory documentation historically uses:

```text
user: root
password: dfrobot
```

Change default credentials before exposing the device to an untrusted network.

---

# 🔊 Pair the Bluetooth speaker

Open a terminal on UNIHIKER:

```bash
bluetoothctl
```

Then:

```text
default-agent
power on
scan on
trust 00:00:00:00:00:00
pair 00:00:00:00:00:00
connect 00:00:00:00:00:00
```

Replace:

```text
00:00:00:00:00:00
```

with the Bluetooth speaker's actual MAC address.

---

# 🚀 Installing RinGPT 1.0

## 1. Clone the repository

```bash
git clone https://github.com/ronibandini/rinGPT.git
cd rinGPT
```

---

## 2. Install dependencies

```bash
pip install SpeechRecognition
apt-get install flac
pip install openai
pip install edge-tts
pip install art
```

---

## 3. Copy the project to UNIHIKER

The original installation uses:

```text
/home/timbre
```

The project expects assets in locations such as:

```text
/home/timbre/audio/
/home/timbre/images/
```

---

## 4. Configure OpenAI

Edit:

```text
timbre.py
```

and set:

```python
chatGPTKey = ""
```

Create an API key from:

[OpenAI API Keys](https://platform.openai.com/api-keys)

Do not commit configured API credentials.

---

## 5. Configure Telegram

Optional:

```python
telegramEnabled = 1
telegramBot = ""
telegramChatId = ""
```

---

## 6. Configure the response behavior

Adjust:

```python
temperature = 0.8
prompt1 = "..."
prompt2 = "..."
defaultAnswer = "..."
```

and optionally replace the keyword/preset tables:

```python
recon = [...]
answers = [...]
```

---

## 7. Run

```bash
python timbre.py
```

After verifying the project manually, UNIHIKER's auto-run functionality can be used to launch it automatically.

---

# 🚀 Installing RinGPT 2.0

Enter:

```text
2.0/
```

and configure the version 2 script.

Install:

```bash
pip install openai speech_recognition edge_tts art asyncio textwrap
```

Configure:

- OpenAI API credentials
- Telegram credentials
- Bluetooth speaker
- agenda entries
- reception rules
- servo
- doorbell button

Run:

```bash
python ringpt1.py
```

---

# 📁 Repository structure

```text
rinGPT/
├── 2.0/
│   └── ...
│
├── audio/
│   └── ...
│
├── images/
│   └── ...
│
├── README.md
├── generateAudio.py
└── timbre.py
```

### `timbre.py`

RinGPT 1.0 main application.

Handles:

- doorbell input
- greetings
- recording
- speech recognition
- predefined responses
- OpenAI completion
- text-to-speech
- Telegram
- logs

### `generateAudio.py`

Utility for creating or regenerating prerecorded speech assets.

### `audio/`

Doorbell sounds, greetings and preset responses.

### `images/`

UNIHIKER interface assets.

### `2.0/`

AI Agent-powered RinGPT implementation.

---

# 🎥 Demo

## RinGPT 1.0

**[▶️ RinGPT AI Doorbell — YouTube](https://www.youtube.com/watch?v=6RJs4HPoyds)**

---

# 🔬 Ideas for extending the project

1. **📅 Live calendar integration** — replace the hardcoded agenda with Google Calendar, CalDAV, n8n, or another scheduling source.

2. **🔐 Deterministic access control** — separate conversational reasoning from actual authorization and require structured, independently validated rules before activating a physical lock.

3. **🧠 Persistent visitor history** — maintain a local database of previous visits, decisions, transcripts, and notifications that can be queried as a tool.

---

# 📰 External references

## 🗞️ Independent editorial coverage

### LA NACION — RinGPT and Contracultura Maker

**[Este sábado, una charla de Roni Bandini, el creador de la antena anti reggaeton y del portero que atiende solo](https://www.lanacion.com.ar/tecnologia/este-sabado-una-charla-de-roni-bandini-el-creador-de-la-antena-anti-reggaeton-y-del-portero-que-nid27092024/)**

LA NACION published a profile on September 27, 2024 covering RinGPT and its origin.

The article describes the motivation behind the project, its conversion of visitor speech to text, ChatGPT-generated answers, keyword handling, and the goal of having the doorbell respond even when nobody is available.

---

## 🏆 Ready Tensor Agentic AI Challenge

### Best AI Tool Innovation — 2025

RinGPT 2.0 was selected as one of the **Best AI Tool Innovation** winners in the **Ready Tensor Agentic AI Challenge 2025**.

**[Agentic AI Challenge 2025 Winners — Ready Tensor](https://www.readytensor.ai/agentic-ai-2025-winners/)**

The winning entry is listed as:

```text
RinGPT 2.0 AI Agent Powered Doorbell
```

---

# 🛠️ Project publications

## Hackaday.io

### RinGPT AI Doorbell

**[RinGPT AI doorbell — Hackaday.io](https://hackaday.io/project/196892-ringpt-ai-doorbell)**

The original project page documents:

- UNIHIKER
- Bluetooth audio
- P23 doorbell input
- P22 secondary button
- five-second recordings
- speech recognition
- predefined answers
- OpenAI responses
- Telegram notifications
- Edge TTS
- project setup

---

## Hackster.io

### RinGPT AI Agent Powered Doorbell

**[RinGPT AI Agent Powered Doorbell — Hackster.io](https://www.hackster.io/roni-bandini/ringpt-ai-agent-powered-doorbell-3bc719)**

Published March 13, 2025.

The tutorial covers version 2.0, including:

- UNIHIKER M10
- IO board
- LED button
- SG90 servo
- Bluetooth speaker
- visitor-name extraction
- function calling
- tool selection
- agenda queries
- light sensing
- physical door actuation
- Telegram notifications
- logging

---

## Ready Tensor

### RinGPT 2.0 AI Agent Powered Doorbell

**[Read the project on Ready Tensor](https://app.readytensor.ai/publications/ringpt-20-ai-agent-powered-doorbell-gcuSB4vQCesp)**

The publication documents the complete agent architecture and its interaction with both software and physical tools.

---

## DFRobot Maker Community

### RinGPT 2.0 AI Agent Powered UNIHIKER Doorbell

**[RinGPT 2.0 — DFRobot Maker Community](https://community.dfrobot.com/makelog-316253.html)**

DFRobot's Maker Community published the version 2.0 build with:

- hardware list
- connections
- dependencies
- API setup
- agent workflow
- available tools
- UNIHIKER light sensor
- servo-based door control

---

# ✍️ Medium

## RinGPT 1.0

**[RinGPT: agregar IA al timbre de la casa](https://bandini.medium.com/ringpt-agregar-ia-al-timbre-de-la-casa-759971d48014)**

Spanish-language article documenting the original LLM-powered version.

---

## RinGPT 2.0

**[Recepcionista con agente de IA vía OpenAI](https://bandini.medium.com/recepcionista-con-agente-de-ia-v%C3%ADa-openai-4e56ba8ef6db)**

Spanish-language article covering the AI Agent-powered version.

---

# 🎤 Contracultura Maker / Nerdearla

RinGPT was one of the projects discussed around **Contracultura Maker** at Nerdearla in 2024.

LA NACION's September 27, 2024 profile was published immediately before the Nerdearla talk and specifically highlights RinGPT as one of the projects behind the presentation.

**[LA NACION — Contracultura Maker, RinGPT and Nerdearla](https://www.lanacion.com.ar/tecnologia/este-sabado-una-charla-de-roni-bandini-el-creador-de-la-antena-anti-reggaeton-y-del-portero-que-nid27092024/)**


---

# 📚 Useful references

- [UNIHIKER](https://www.unihiker.com/)
- [UNIHIKER Documentation](https://www.unihiker.com/wiki/)
- [OpenAI API](https://developers.openai.com/api/docs/)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [gpt-3.5-turbo-instruct documentation](https://developers.openai.com/api/docs/models/gpt-3.5-turbo-instruct)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [edge-tts](https://github.com/rany2/edge-tts)

---

# 🔗 You may also be interested in...

Other projects by **Roni Bandini** combining AI, physical interfaces, computer vision, automation, and unconventional access systems.

## 🔔📷 AI Camera Doorbell

**Buttonless ESP32-S3 doorbell combining local Edge Impulse detection, speech transcription, LLM rules, Telegram notifications, and relay control.**

It extends several RinGPT ideas into an embedded camera-based implementation.

**[github.com/ronibandini/aicamdoorbell](https://github.com/ronibandini/aicamdoorbell)**

---

## 👁️🤖 HuskyLens2MCP

**Command-line client connecting HUSKYLENS 2 computer vision with Gemini through Model Context Protocol.**

Another project combining physical perception with an LLM reasoning layer and callable tools.

**[github.com/ronibandini/HuskyLens2MCP](https://github.com/ronibandini/HuskyLens2MCP)**

---

## 🖥️🔘 n8n Terminal

**Dedicated physical interface for n8n workflows using buttons, display, audio, RGB feedback, and QR codes.**

Another experiment in giving automation systems a tangible interface rather than keeping them entirely inside conventional software.

**[github.com/ronibandini/n8nTerminal](https://github.com/ronibandini/n8nTerminal)**

---

# 🔐 Security and privacy

## API credentials

RinGPT stores configuration values for:

```text
OpenAI API key
Telegram bot token
Telegram chat ID
```

Do not commit configured credentials to a public repository.

Use environment variables or a protected configuration file for a permanent installation.

---

## Visitor recordings

RinGPT records audio from people at the door.

Version 1.0 sends recognized text to external services for speech recognition and LLM processing.

Deployments should consider applicable privacy, recording, consent, and data-protection requirements.

---

## Logs

The application writes visitor interactions to:

```text
log.txt
```

The log may contain transcripts and generated responses.

Protect it appropriately if the system is installed in a real residence or workplace.

---

## AI decisions and physical access

Version 2.0 demonstrates an AI system that can participate in decisions about physical access.

LLM output is probabilistic and should not be treated as a sufficient authentication mechanism for a real security-critical lock.

A production access-control system should separate:

```text
conversation
     │
     ▼
AI interpretation
     │
     ▼
deterministic authorization
     │
     ▼
physical unlock
```

and validate authorization using independent rules or credentials.

---

## Default UNIHIKER credentials

If the device still uses factory credentials such as:

```text
root / dfrobot
```

change them before deploying RinGPT on a network accessible by other users.

---

# 📜 License

RinGPT is published under the **MIT License**.

The project source identifies:

```text
Roni Bandini
July 2024
Buenos Aires, Argentina
MIT License
```

Version 2.0 project publications also use the MIT License.

---

# 👤 Author

**Roni Bandini**

Maker, AI developer, electronic artist and writer.

- 🐙 GitHub: [@ronibandini](https://github.com/ronibandini)
- 💼 LinkedIn: [Roni Bandini](https://www.linkedin.com/in/ronibandini/)
- 📸 Instagram: [@ronibandini](https://www.instagram.com/ronibandini/)
- 🐦 X: [@RoniBandini](https://x.com/RoniBandini)
- ✍️ Medium: [bandini.medium.com](https://bandini.medium.com/)
- 🛠️ Hackster: [Roni Bandini](https://www.hackster.io/roni-bandini)
- 🔧 Hackaday.io: [Roni Bandini](https://hackaday.io/ronibandini)

Buenos Aires, Argentina.
