import speech_recognition as sr
import pyttsx3
import datetime
from dotenv import load_dotenv
from AppOpener import open
import webbrowser
from playsound import playsound

apikey = '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'
load_dotenv()

import openai
openai.api_key = apikey

def speakText(command):

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 195)

    engine.say(command)
    engine.runAndWait()

r = sr.Recognizer()

def record_text():

    while(1):

        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                r.energy_threshold = 8000
                playsound('ui-wakesound-touch.mp3')
                print("Listening...")
                audio2 = r.listen(source2)

                MyText = r.recognize_google(audio2)

                return MyText
            
        except sr.RequestError as e: 
            speakText("I could not catch that.")
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            speakText("I could not catch that.")
            print("Unknown error occured. Please try again")

x = datetime.datetime.now()

date = "{} {} {}".format(x.strftime("%d"),x.strftime("%B"),x.strftime("%Y"))
time = "{}:{} {}".format(x.strftime("%I"),x.strftime("%M"),x.strftime("%p"))

def send_to_ChatGPT(messages, model="gpt-3.5-turbo"):

    response = openai.ChatCompletion.create(

        model = model,
        messages = messages,
        max_tokens = 1000,
        n = 1,
        stop = None,
        temperature = 0.5,

    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages = [{"role":"user", "content":"Your name is zira"}, ]

speakText("Starting up...")
playsound('alerts-notification.mp3')


if 5 <= int(x.strftime("%H")) < 12:
    speakText("Good Morning Sir, how may I help you today?")
elif 12 <= int(x.strftime("%H")) < 18:
    speakText("Good Afternoon Sir, how may I help you today?")
else:
    speakText("Good Evening Sir, how may I help you today?")
    
    
while True:
    
    txt = record_text()
    text = txt.lower()
    print(txt)    
    
    if "time right now" in text:        
        speakText("The time right now is {}".format(time))
            
    elif "date today" in text:
        speakText("Today's date is {}".format(date))

    elif "day today" in text:
        speakText("Today is {}".format(x.strftime("%A")))

    elif "open" in text:
        if "application" in text:
            speakText("Which application would you like me to open?")
            app = record_text().lower()
            speakText("Opening {}...".format(app))
            open(app, match_closest=True)

        elif "website" in text:
            speakText("Which website would you like me to open?")
            website = record_text().lower()
            speakText("Opening {}...".format(website))
            webbrowser.open("https://{}.com".format(website))

        else:
            exit

    elif "close the program" in text:
        speakText("shutting down")
        playsound('Shut-down.mp3')
        break

    else:
        messages.append({"role":"user", "content":txt})
        response = send_to_ChatGPT(messages)
        print(response)
        speakText(response)
        