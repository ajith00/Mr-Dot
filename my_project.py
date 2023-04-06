#from cProfile import run
#from turtle import onclick
import pyttsx3
import datetime
import speech_recognition as sr
import wikipediaapi
import webbrowser,requests
import os
#import pyautogui
import psutil
import pyjokes
import cv2,time
import streamlit as st
import openai
import re, requests, subprocess, urllib.parse, urllib.request
st.set_page_config(
    page_title="AVR-Virtual Assistance",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
openai.organization='org-J8FtIsqBBpO1anFFNMQElDFh'
openai.api_key='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'
model_engine="text-davinic-003"
container=st.container()
#For Help Desk
st.sidebar.write("KEYWORDS FOR BETTER USAGE")
st.sidebar.write("________________________________________")
st.sidebar.write("1)'TELL A JOKE' to listen a joke.")
st.sidebar.write("2)'CREATE IMAGE' to Generate a AI Based Image.")
st.sidebar.write("3)'OPEN YOUTUBE or SEARCH YOUTUBE' to perform the youtube search.")
st.sidebar.write("4)'WRITE A CODE or WRITE A SCRIPT' for Writing the code in multiple programming Language.")
st.sidebar.write("5)'ABOUT' for knowing the General Information.")
st.sidebar.write("6)'TAKE SCREENSHOT' for capturing the Screen Content.")
st.sidebar.write("7)'SYSTEM STATUS' for knowing the Current system CPU Status.")
st.sidebar.write("8)'OPEN BROWSER' for browsing in the internet.")
st.sidebar.write("9)'TAKE A SELFIE' for clicking the pic.")
st.sidebar.write("10)'WIKIPEDIA' for wikipedia search.")
st.sidebar.write("11)'PLAY SONG' to listen a song from internet.")
st.sidebar.write("12)'REMEMBER or MAKING A NOTE' for save the content in local system.")
st.sidebar.write("13)'OPEN NOTE' to listen to saved note.")

#help_desk,container=st.tabs(["Help...?","Virtual Machine"])
rec=sr.Recognizer()
def speech(script):
    engine = pyttsx3.init()
    container.success(script)
    engine.say(script)
    engine.runAndWait()
    engine.stop()

def take_instructions():
    with sr.Microphone() as source:
        try:
            rec.adjust_for_ambient_noise(source)
            container.write("Listening...")
            audio = rec.listen(source,10)
            container.write("Recognizing...")
            instruction = rec.recognize_google(audio, language='en-in')
            container.write(instruction)
        except LookupError:
             speech("Could not understand your voice")
             container.error("Could not understand your voice")
             return ""
        except Exception as ex:
            print(ex)
            #speech("Something went wrong")
            container.error("Something went wrong")
            return ""
        return instruction.lower()

def screenshot():
    img = pyautogui.screenshot()
    speech("By what name should I save it?")
    ans=take_instructions()
    ans="summa"+ans+".png"
    img.save(ans)
    speech("Screenshot taken")

def camera():
    speech("Press space to take image and escape to stop Camera")
    Camera = cv2.VideoCapture(0)
    cv2.namedWindow("Camera")
    img_counter = 0
    while True:
        ret, frame = Camera.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Camera", frame)
        k = cv2.waitKey(1)
        if k%256 == 27:
            speech("closing camera")
            break
        elif k%256 == 32:
            img_name = "camera{}.png".format(img_counter)
            #Replace CameraPath with the path of the folder where you want to save your photos taken by camera
            path="camera"
            cv2.imwrite(os.path.join(path , img_name), frame)
            cv2.imwrite(img_name, frame)
            speech("{} image taken".format(img_name))
            img_counter += 1
    Camera.release()
    cv2.destroyAllWindows()

def wikipedia(query):
    speech("Searching...")
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(query)
    print(page_py.summary)
    if page_py.exists():
        speech(page_py.summary)
        container.text_area(page_py.summary)
    else:
        speech("Strange Page Name Unable to get the detail")
        container.error("Strange Page, Unable to get the detail")

def open_website(query):
    urL='https://www.google.co.in/search?q='+query
    webbrowser.get('windows-default').open(urL)
    speech("Here is the search result")  

def Songs():
    speech("Which song you want to play?")
    Information=take_instructions()
    query_string = urllib.parse.urlencode({"search_query": Information})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    try:
        clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
        clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0]+"&autoplay=1")
        container.video(str(clip2),start_time=0)
    except Exception as ex:
        print(ex)
        container.error(ex)

def Remember():
    speech("What should I remember?")
    Information=take_instructions()
    speech('you said me to remember that '+Information)
    rem = open('data.txt','w') 
    rem.write(Information) 
    rem.close()

def Knowing():
    remember=open('data.txt','r')
    speech("you said me to remember that"+remember.read())

def Weather():
    speech("Which city's weather you want to know?")
    city=take_instructions().lower()
    url="http://api.openweathermap.org/data/2.5/weather?q={}&appid=5907224a675c489e3c6d69e8336d1ba9".format(city)
    res=requests.get(url)
    data=res.json()
    climate=data["weather"][0]["description"]
    speech("Todays climate is "+climate)
    temp=data['main']['temp']
    temp=round(temp-273.15,2)
    speech("Average Temperature is "+str(temp)+"Degree Celsius")
    maxtemp=data['main']['temp_max']
    maxtemp=round(maxtemp-273.15,2)
    speech("Maximum temperature is "+ str(maxtemp)+" Degree Celsius")
    mintemp=data['main']['temp_min']
    mintemp=round(mintemp-273.15,2)
    speech("Minimum temperature is "+ str(mintemp)+ " Degree Celsius")
    wind=data["wind"]["speed"]
    speech("WindSpeed is "+str(wind)+" meters per second")
    humidity=data["main"]["humidity"]
    speech("Humidity is "+str(humidity)+"%")
    visible=data["visibility"]
    speech("Visibility is "+str(visible)+" meters")
    cloud=data["clouds"]["all"]
    speech("Its "+str(cloud)+" percent cloudy")
    pressure=data['main']["pressure"]
    speech("Air pressure is at "+ str(pressure)+"hpa")

def open_youtube():
    speech("What should I search?")
    SearchData=take_instructions()
    webbrowser.open("https://www.youtube.com/results?search_query="+SearchData)

def current_time():
    time = datetime.datetime.now().strftime("%I:%M:%S")
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        phase = "morning"
    elif 12 <= hour < 18:
        phase = "afternoon"
    elif 18 <= hour <= 24:
        phase = "evening"
    else:
        phase = "night"
    speech(f"It's {time} of {phase}")

def current_date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    speech(f"Today is {day} {month} {year}") 

def system_status():
    cpu_usage = psutil.cpu_percent()
    speech(f'Current CPU usage is at {cpu_usage}%')
    battery = psutil.sensors_battery()
    speech(f"Battery remaining is {battery.percent}%")
    hdd = psutil.disk_usage('/')
    hdd_usage = (hdd.used / hdd.total) * 100
    speech(f"Storage used in C Drive is {hdd_usage:.2f}%")
    frequency = psutil.cpu_freq()
    speech(f"Current frequency of CPU is {frequency.current} MHz")
    ram_used = psutil.virtual_memory().percent
    speech(f"RAM used is {ram_used}%")  

def tell_joke():
    speech(pyjokes.get_joke(category='all'))

#for Codding
def get_code(question):
    try:
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=question,
          temperature=0,
          max_tokens=4000,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        container.code(response["choices"][0]['text'])
    except Exception as ex:
        container.error(ex)
#for GK
def get_info(question):
    try:
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=question,
          temperature=0.5,
          max_tokens=4000,
          top_p=1.0,
          stop=None,
          n=1
        )
        #container.text_area(response["choices"][0]['text'])
        speech(response["choices"][0]['text'])
    except Exception as ex:
        container.error(ex)

def find(main,sub):
    x=main.find(sub)
    if x==-1:
        return False
    else:
        return True
    
def generate_image():
    speech("Give Your Idea..?")
    Search_Data=take_instructions()
    try:
        responce=openai.Image.create(
            prompt=Search_Data,
            n=1,
            size='512x512'
        )
        print(responce['data'][0]['url'])
        container.image(str(responce['data'][0]['url']))
    except Exception as ex:
        print(ex)
        container.error(ex)

def run_virtual_assistant(command):
    if len(command)>2:        
        print(command)    
        if find(command,'date'):
            current_date()
        elif find(command,'time') :
            current_time()
        elif find(command,'write a code') or find(command,'write a script'):
            get_code(command)
        elif find(command,'about'):
            get_info(command)
        elif find(command,'take a screenshot'):
            screenshot()
        elif find(command,'system status'):
            system_status()
        elif find(command,'open chrome') or find(command,'open browser'):
                speech("What are you trying to find online?")
                res=container.text_input("Enter the Keyword")
                SearchData=take_instructions()
                if res=="":
                    query=SearchData
                else:
                    query=res
                open_website(query)
        elif find(command,'take a selfie') or find(command,'open camera') or find(command,"webcam"):
            camera()
        elif find(command,'wikipedia'):
            speech("What are you trying to find in wikipedia?")
            res=container.text_input("Enter the Keyword")
            SearchData=take_instructions()
            if res=="":
                query=SearchData
            else:
                query=res
            wikipedia(query)
        elif find(command,'play song'):
            Songs()
        elif find(command,'remember') or find(command,'make a note'):
            Remember()
        elif find(command,"open note"):
            Knowing()
        elif find(command,'todays weather') or find(command,'weather'):
            Weather()
        elif find(command,'open youtube') or find (command,"search youtube"):
            open_youtube()
        elif find(command,'tell a joke') or find(command,'mood out'):
            tell_joke()
        elif find(command,'create image') or find(command,'generate image'):
            generate_image()
        else:
            container.error("Unable to Process Your Request, We are working to Fix it")
            speech("Unable to Process Your Request, We are working to Fix it")
    else:
        container.error("Invalid Command")
        speech("Invalid Command")

def main():
    container.title("Voice-Based Virtual Assistant")
    form = st.form(key='my-form')
    command = form.text_input('What do you want..?')
    submit = form.form_submit_button('Submit')
    mic_btn=form.form_submit_button('mic')
    if submit:
        speech(command)
        print(command)
        run_virtual_assistant(command.lower())
    if mic_btn:
        command=take_instructions()
        run_virtual_assistant(command.lower())

if __name__ == "__main__":
    main()


       
