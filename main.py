import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import requests
import os
import subprocess
import sys

class PersonalAssistant:
    def __init__(self, name="JARVIS"):
        # Initialize text-to-speech with error handling
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
        except Exception as e:
            print(f"Error initializing text-to-speech: {e}")
            sys.exit(1)
            
        self.name = name
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        """Convert text to speech"""
        print(f"{self.name}: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

    def listen(self):
        """Listen to user's voice command"""
        with sr.Microphone() as source:
            self.speak("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except Exception as e:
                self.speak(f"Sorry, there was an error: {str(e)}")
                return None

    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")

    def open_website(self, url):
        """Open a website with better error handling"""
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.get().open(url)
            self.speak(f"Opening {url}")
        except Exception as e:
            self.speak(f"Failed to open website: {str(e)}")

    def get_weather(self, city):
        """Get weather information"""
        try:
            url = f"https://wttr.in/{city}?format=3"
            response = requests.get(url, timeout=5)
            self.speak(f"Weather in {city}: {response.text}")
        except:
            self.speak("Sorry, I couldn't fetch the weather information")

    def open_application(self, app_name):
        """Open applications on the computer"""
        try:
            if sys.platform == "win32":  # Windows
                os.startfile(app_name)
            elif sys.platform == "darwin":  # Mac
                subprocess.call(["open", "-a", app_name])
            else:  # Linux
                subprocess.call(["xdg-open", app_name])
            self.speak(f"Opening {app_name}")
        except Exception as e:
            self.speak(f"Could not open {app_name}: {str(e)}")

    def create_file(self, filename):
        """Create a new file"""
        try:
            with open(filename, 'w') as f:
                f.write("")
            self.speak(f"Created file {filename}")
        except Exception as e:
            self.speak(f"Failed to create file: {str(e)}")

    def shutdown(self):
        """Shutdown computer"""
        try:
            if sys.platform == "win32":
                subprocess.call("shutdown /s /t 1")
            elif sys.platform in ["darwin", "linux"]:
                subprocess.call(["shutdown", "-h", "now"])
            self.speak("Shutting down the computer")
        except:
            self.speak("Failed to shutdown computer")

    def run(self):
        """Main running loop"""
        self.speak(f"Hello! I am {self.name}, your personal assistant. How can I help you?")
        
        while True:
            command = self.listen()
            
            if command:
                # Exit command
                if "exit" in command or "quit" in command:
                    self.speak("Goodbye")
                    break
                
                # Time command
                elif "time" in command:
                    self.get_time()
                
                # Website command
                elif "open website" in command:
                    url = command.replace("open website", "").strip()
                    self.open_website(url)
                
                # Weather command
                elif "weather in" in command:
                    city = command.replace("weather in", "").strip()
                    self.get_weather(city)
                
                # Open application
                elif "open" in command:
                    app = command.replace("open", "").strip()
                    self.open_application(app)
                
                # Create file
                elif "create file" in command:
                    filename = command.replace("create file", "").strip()
                    self.create_file(filename)
                
                # Shutdown
                elif "shutdown" in command or "turn off" in command:
                    self.speak("Are you sure you want to shutdown?")
                    confirm = self.listen()
                    if confirm and "yes" in confirm:
                        self.shutdown()
                
                # Basic greeting
                elif "hello" in command:
                    self.speak("Hello! How can I assist you today?")
                
                else:
                    self.speak("I'm not sure how to help with that. Try asking to open a website, application, or get the time!")

if __name__ == "__main__":
    # Required libraries installation command:
    # pip install speechrecognition pyttsx3 requests pyaudio
    
    assistant = PersonalAssistant()
    assistant.run()