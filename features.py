
import random
import socket
import struct
import time
from urllib.parse import quote
import pywhatkit
import threading
import winsound
import speech_recognition as sr
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import webbrowser
from google.auth.transport import Request
from playsound import playsound
import eel
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
import os
import pywhatkit as kit
import sqlite3
import pyaudio
import pvporcupine
import datetime
import requests
import pyttsx3
import speedtest
import psutil
from engine.helper import extract_yt_term
from hugchat import hugchat
import screen_brightness_control as sbc
import pyautogui as autogui
import pyjokes

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "engine/www/assets/audio/www_assets_audio_start_sound.mp3"
    playsound(music_dir)

# Initialize the voice engine
engine = pyttsx3.init()
from engine.command import speak

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Pre-trained keywords porcupine developed by picovoice 
        porcupine = pvporcupine.create(access_key="enter yours",keywords=["jarvis"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)

        # Loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            # Process the keyword from the mic & checks jarvis is detecting or not
            keyword_index = porcupine.process(keyword)

            # Check if the first keyword "jarvis" is detected
            if keyword_index >= 0:
                print("Hotword detected")

                # Pressing shortcut key Win + J
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
    except Exception as e:
        print(f"Error: {e}")
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12 :
        speak("Good Morning")
    elif hour>=12 and hour<18 :
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Jarvis , how may I help you?")

def openCommand(query):
    try:
        print(f"Original Query: {query}")  
        query = query.lower().replace(ASSISTANT_NAME, "").replace("open", "").strip()
        print(f"Processed Query: {query}")  

        if query:
            # Check sys_command table
            cursor.execute('SELECT path FROM sys_command WHERE name = ?', (query,))
            results = cursor.fetchall()
            print(f"Database sys_command Results: {results}")  

            if results:
                file_path = results[0][0]
                if os.path.exists(file_path):
                    speak(f"Opening {query}")
                    os.startfile(file_path)
                    return
                else:
                    speak("File not found")
            else:
                # Check web_command2 table
                cursor.execute('SELECT path FROM web_command WHERE name = ?', (query,))
                results = cursor.fetchall()
                print(f"Database web_command Results: {results}")  

                if results:
                    speak(f"Opening {query}")
                    webbrowser.open(results[0][0])
                    return
                else:
                    # Try opening via command
                    speak(f"Opening {query}")
                    print(f"Running system command: start {query}")  
                    try:
                        os.system(f'start {query}')
                        return
                    except Exception as e:
                        speak("Command execution failed")
                        print(f"System Command Error: {e}")  

    except Exception as e:
        speak("Something went wrong")
        print(f"General Error: {e}")

#closing command
def close_application(app):
    try:
        os.system(f"taskkill /f /im {app}.exe")
        speak(f"Closing {app}")
    except Exception as e:
        speak("Sorry, I couldn't close the application.")

# get the current IP address
def get_ip_address():
    ip = socket.gethostbyname(socket.gethostname())
    print(ip)
    return f"Your IP address is {ip}"
    
# get RAM usage
def get_ram_usage():
    ram = psutil.virtual_memory()
    return f"RAM Usage: {ram.percent}%"
#rom status
def rom_info():
    partitions = psutil.disk_partitions()
    storage_info = {}

    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        storage_info[partition.device] = {
            "Total": round(usage.total / (1024**3), 2),  # Rounded to 2 decimal places for better readability
            "Used": round(usage.used / (1024**3), 2),
            "Free": round(usage.free / (1024**3), 2),
            "Percentage": usage.percent
        }

    return storage_info

# Function to play alarm
def play_alarm():
    print("Alarm ringing!")
    for _ in range(5):  # Repeat the sound 5 times
        winsound.Beep(1000, 1000)  # Frequency and duration of sound

# Function to listen for input and recognize speech
def listen_for_input(prompt):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print(prompt)
        speak(prompt)  # Speak the prompt before listening
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        response = recognizer.recognize_google(audio)
        print(f"Recognized: {response}")
        return response
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError:
        speak("Sorry, there was an issue with the speech service.")
        return None

# Listen for hour input
def listen_for_hour():
    while True:
        speak("Please say the hour for the alarm.")
        hour_str = listen_for_input("Listening for hour...")

        if hour_str is not None:
            try:
                hour = int(hour_str)
                if 0 <= hour <= 23:
                    return hour
                else:
                    speak("The hour must be between 0 and 23. Please try again.")
            except ValueError:
                speak("Sorry, I didn't understand the hour. Please try again.")

# Listen for minute input
def listen_for_minute():
    while True:
        speak("Please say the minute for the alarm.")
        minute_str = listen_for_input("Listening for minute...")

        if minute_str is not None:
            try:
                minute = int(minute_str)
                if 0 <= minute <= 59:
                    return minute
                else:
                    speak("The minute must be between 0 and 59. Please try again.")
            except ValueError:
                speak("Sorry, I didn't understand the minute. Please try again.")

# Function to set an alarm
def set_alarm():
    alarm_hour = listen_for_hour()
    alarm_minute = listen_for_minute()

    speak(f"Alarm has been set for {alarm_hour}:{alarm_minute}.")

    # Wait until the alarm time is reached
    while True:
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min

        if current_hour == alarm_hour and current_minute == alarm_minute:
            threading.Thread(target=play_alarm).start()
            break

        time.sleep(60)  # Sleep for 60 seconds to check again

def check_internet_connection():        #check internet connectivity
    try:
        response = requests.get("http://www.google.com")
        speak("You are connected to the internet.")
    except requests.exceptions.RequestException:
        speak("No internet connection.")

def get_news():     #current news
    url = " "  # NewsAPI key
    response = requests.get(url)
    #json converts the http response into python dir
    news_data = response.json()
    articles = news_data['articles']
    headlines = [article['title'] for article in articles[:5]]
    speak('\n'.join(headlines))

def get_time():
    from datetime import datetime
    now = datetime.now().strftime("%H:%M:%S")
    return now

#function for screenshot
def take_screenshot():
    img = pyautogui.screenshot()
    img.save("screenshot.png")
    speak("Screenshot taken")

def get_date():     #current date
    today = datetime.datetime.today()
    date_str = today.strftime("%A, %d %B %Y")
    return date_str
    
def get_weather(city="Mumbai"):
    API_KEY = ""  # OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q=mumbai&appid=60780f2ca3d954588691968b80e4145d&units=metric"
    
    try:
        response = requests.get(url).json()
        print("API Response:", response) 
        #status code if not 200 then error
        if response.get("cod") != 200:
            error_message = response.get("message", "Unable to fetch weather details")
            return speak(f"Error fetching weather: {error_message}")

        temperature = response['main']['temp']
        description = response['weather'][0]['description']
        weather_report = f"The current temperature in {city} is {temperature}°C with {description}."
        return weather_report

    except Exception as e:
        print("Exception:", e)  
        return speak("Sorry, I couldn't fetch the weather details. Please try again later.")
    
def check_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  
        download_speed = st.download() / 1_000_000  # converts mpbs
        upload_speed = st.upload() / 1_000_000
        return f"Download speed: {download_speed:.2f} Mbps, Upload speed: {upload_speed:.2f} Mbps"
    except Exception as e:
        return f"Error: {str(e)}"

#playing song on youtube
def playYoutube(query):
    search_term = extract_yt_term(query)
    speak("playing"+search_term+"on youtube")
    kit.playonyt(search_term)

def chatBot(query):
    try:
        print(f"User input: {query}")

        if "play" in query.lower() and "youtube" in query.lower():
            threading.Thread(target=lambda: playYoutube(query)).start()
            return

        chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(query)
        print(f"Chatbot response: {response}")
        return response

    except Exception as e:
        print(f"Chatbot error: {e}")
        speak("Sorry, I encountered an error while trying to chat.")
        return "Sorry, I encountered an error."


#battery
def battery():
    battery = psutil.sensors_battery().percent
    return f"Battery is at {battery} percent"

#playing system music
def play_random_song():
    music_dir = "C:/Users/prash/Music/music"  #music folder path
    songs = [song for song in os.listdir(music_dir) if song.endswith(".mp3")]

    if not songs:
        speak("No songs found!")
        return

    random_song = random.choice(songs)
    song_path = os.path.join(music_dir, random_song)

    speak(f"Playing: {random_song}")
    os.startfile(song_path)  # Opens song in default player

#sets the brightness
def set_brightness(level):
    try:
        sbc.set_brightness(level)
        speak(f"Brightness set to {level}%")
    except Exception as e:
        speak("Error setting brightness:", e)

#increase the brightness
def increase_brightness():
    try:
        current_brightness = sbc.get_brightness(display=0)[0]
        new_brightness = min(current_brightness + 10, 100)
        sbc.set_brightness(new_brightness)
        return f"Brightness increased to {new_brightness}%"
    except Exception as e:
        speak("Error increasing brightness:", e)
#decrease the brightness
def decrease_brightness():
    try:
        current_brightness = sbc.get_brightness(display=0)[0]
        new_brightness = max(current_brightness - 10, 0)
        sbc.set_brightness(new_brightness)
        return f"Brightness decreased to {new_brightness}%"
    except Exception as e:
        speak("Error decreasing brightness:", e)

def set_system_volume(volume_level):
    try:
        volume_level = max(0, min(100, volume_level))  #volume between 0-100
        os.system(f"nircmd.exe setsysvolume {int(volume_level * 655.35)}")
        return f"Volume set to {volume_level}%"
    except Exception as e:
        return "Failed to set volume"
    
#finds current volume of the system
def get_current_volume():
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        current_volume = int(volume.GetMasterVolumeLevelScalar() * 100)
        return current_volume
    except Exception as e:
        return 50  # Default value if detection fails
#mutes the audio
def mute_audio():
    
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMute(1, None)
    print("Muted")

def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("jarvis","")
        query = query.replace("google search","")
        query = query.replace("google","")
        speak("This is what i found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query,1)#1 mean one paragraph
            speak(result)

        except:
            speak("No speakable output available")
 
def WolfRamAlpha(query):
    import wolframalpha
    apikey = ""  #this is wolframalpa api key 
    requester = wolframalpha.Client(apikey)
    requested = requester.query(query)

    try:
        answer = next(requested.results).text
        return answer
    except:
        speak("The value is not answerable")
        
#calculating simple calculations
def Calc(query):
    Term = str(query)
    Term = Term.replace("jarvis","")
    Term = Term.replace("multiply","*")
    Term = Term.replace("plus","+")
    Term = Term.replace("minus","-")
    Term = Term.replace("divide","/")

    Final = str(Term)
    try:
        result = WolfRamAlpha(Final)
        print(f"{result}")
        return result

    except:
        speak("The value is not answerable")

#for jokes
def tell_joke():
    joke = pyjokes.get_joke()
    print(f"Jarvis: {joke}")
    return joke

#random roasts
def roast():
    roasts = [
        "Your secrets are safe with me. I never even listen when you tell me them.",
        "You're like a cloud. When you disappear, it’s a beautiful day.",
        "You're proof that even evolution takes a break sometimes.",
        "You're as useless as the 'ueue' in 'queue'."
    ]
    roast = random.choice(roasts)
    print(f"Jarvis: {roast}")
    return roast

def open_camera():
    import cv2
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Jarvis Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

#sending whatsapp message by mobile number
def send_whatsapp_message(number,message):
    kit.sendwhatmsg_instantly(f"+91{number}",message)

