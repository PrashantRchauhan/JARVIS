from click import command, prompt
import pyttsx3
import speech_recognition as sr
import eel
import time
import threading

def speak(text):
    text = str(text)
    #sapi5 speech api of windows
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)#david voice
    engine.setProperty('rate', 145)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takeCommand():  
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listnening...")
        eel.DisplayMessage('Listnening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 15)
    try:
        print("Recognizing...")
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language= 'en-in')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(1) 
    except Exception as e:
        return        
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takeCommand()
        if query is None:  
            return  
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    recognize = False
    #while True:
    try:
        if "wish" in query:
            from engine.features import wishMe
            wishMe()
            recognize = True

        elif "owner" in query:
            speak("I am developed by Mr. Prashant Chauhan")
            recognize = True

        elif "open camera" in query:
            from engine.features import open_camera
            threading.Thread(target=open_camera).start()
            recognize = True

        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)
            recognize = True

        elif "your" in query and "name" in query:
            speak("I'm Jarvis, here to help you!")
            recognize = True
        
        elif "hello" in query:
            speak("Hello sir, how are you ?")
            recognize = True
        elif "i am fine" in query:
            speak("that's great, sir")
            recognize = True
        elif "how are you" in query:
            speak("Perfect, sir")
            recognize = True
        elif "thank you" in query:
            speak("you are welcome, sir")
            recognize = True

        if "time" in query:
            from engine.features import get_time
            speak(get_time())
            recognize = True
            
        elif "date" in query:
            from engine.features import get_date
            speak(get_date())
            recognize = True

        elif "weather" in query:
            from engine.features import get_weather
            from engine.helper import remove_words
            from engine.config import ASSISTANT_NAME
            words_to_remove = [ASSISTANT_NAME, 'what', 'the', 'right', 'now', 'tell', 'me', 'going', 'on', 'weather','in',"what's"]
            query = remove_words(query, words_to_remove)
            city = query.replace("tell me", "").strip()
            if city == "":
                city = "Mumbai"  # Default city
            speak(get_weather(city))
            recognize = True
            
        elif "calculate" in query:
            from engine.features import WolfRamAlpha
            from engine.features import Calc
            query = query.replace("calculate","")
            query = query.replace("jarvis","")
            speak(Calc(query))
            recognize = True

        elif "music"in query:
            from engine.features import play_random_song
            speak("playing a song for you")
            play_random_song()
            recognize = True

        elif "remember that" in query:
            rememberMessage = query.replace("remember that","")
            rememberMessage = query.replace("jarvis","")
            speak("You told me to remember that"+rememberMessage)
            remember = open("Remember.txt","a")
            remember.write(rememberMessage)
            remember.close()
            recognize = True

        elif "what" and "remember" in query:
            remember = open("Remember.txt","r")
            speak("You told me to remember that" + remember.read())
            recognize = True

        elif "internet speed" in query:
            from engine.features import check_speed
            speak(check_speed())
            recognize = True

        elif "close" in query:
            from engine.features import close_application
            app = query.replace("close", "").strip()
            close_application(app)
            recognize = True

        elif "screenshot" in query:
            from engine.features import take_screenshot
            take_screenshot()
            recognize = True

        elif "battery" in query:
            from engine.features import battery
            speak(battery())
            recognize = True

        elif "increase volume" in query:
            from engine.features import get_current_volume, set_system_volume
            speak("By how much do you want to increase the volume?")
            level = takeCommand().lower()  # Listen for response
            if level is None:
                speak("I didn't understand. Please say a number.")
            elif not level.isdigit():
                speak("i heard but i need a number")
            else:
                level = int(level)
                current_volume = get_current_volume()
                new_volume = min(100, current_volume + level)
                result = set_system_volume(new_volume)
                speak(result)
            recognize = True

        elif "decrease volume" in query:
            from engine.features import get_current_volume, set_system_volume
            speak("By how much do you want to decrease the volume?")
            level = takeCommand()
            if level is None:
                speak("I didn't understand. Please say a number.")
            elif not level.isdigit():
                speak("I heard but i need a number")
            else:
                level = int(level)
                current_volume = get_current_volume()
                new_volume = max(0, current_volume - level)
                result = set_system_volume(new_volume)
                speak(result)
            recognize = True

        elif "volume" in query:
            from engine.features import get_current_volume
            speak("your current volume is"+str(get_current_volume()))
            recognize = True

        elif "mute" in query:
            from engine.features import mute_audio
            mute_audio()
            recognize = True
        
        elif "ip" in query:
            from engine.features import get_ip_address
            speak(get_ip_address())
            recognize = True

        elif "news" in query:
            from engine.features import get_news
            get_news()
            recognize = True

        elif "ram" in query:
            from engine.features import get_ram_usage
            speak(get_ram_usage())
            recognize = True

        elif "rom" in query:
            from engine.features import rom_info
            speak(rom_info())
            recognize = True

        elif "alarm" in query:
            from engine.features import set_alarm
            threading.Thread(target=set_alarm).start()
            recognize = True

        elif "internet" in query:
            from engine.features import check_internet_connection
            check_internet_connection()
            recognize = True

        elif "increase brightness" in query:
            from engine.features import increase_brightness
            speak(increase_brightness())
            recognize = True

        elif "decrease brightness" in query:
            from engine.features import decrease_brightness
            speak(decrease_brightness())
            recognize = True

        elif "google" in query:
            from engine.features import searchGoogle
            searchGoogle(query)
            recognize = True

        elif "photo" in query:
            import pyautogui
            import time
            pyautogui.press("super") 
            time.sleep(1)  
            pyautogui.typewrite("Camera")  
            pyautogui.press("enter")  
            time.sleep(5)  
            speak("SMILE")  
            pyautogui.press("space") 
            recognize = True
        
        elif "joke" in query:
            from engine.features import tell_joke
            speak(tell_joke())
            recognize = True

        elif "roast" in query:
            from engine.features import roast
            speak(roast())
            recognize = True

        elif "whatsapp" in query or "send message on whatsapp" in query or "message on whatsapp" in query or "whatsapp message" in query or "send message" in query or "message" in query:
            from engine.features import send_whatsapp_message
            speak("Tell me the number to send message")
            number=takeCommand().lower()
            speak("what is the message sir!")
            message=takeCommand().lower()
            send_whatsapp_message(number,message)
            speak("sent successfully!")
            recognize = True

        elif not recognize:
            from engine.features import chatBot
            speak(chatBot(query))

    except Exception as e:
            print(e)

    eel.ShowHood()


