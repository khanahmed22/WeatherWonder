# Weather Wonder App made by Muhammad Ahmed Khan 

from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
import requests

Window.size = (300,500)

class SplashScreen(Screen):
    pass
 
class LoginScreen(Screen):
    pass
class Weather_WonderApp(MDApp):
    api_key = "Put your own OpenWeather API key"

    def on_start(self):
        default_city = "Karachi"  # Replace with your default city name
        try:
            self.get_weather(default_city)
        except requests.ConnectionError:
            print("No Internet Connection!")
            exit()
        Clock.schedule_once(self.login, 5)

    def build(self):
        self.icon = "main.png"
        
        global sm 
        sm = ScreenManager()
        sm.add_widget(Builder.load_file("splash.kv"))
        sm.add_widget(Builder.load_file("login.kv"))
        return sm
    
    def login(*args):
        sm.current = "login" 

    def search_weather(self):
        city_name = self.root.get_screen("login").ids.city_name.text
        if city_name != "":
            self.get_weather(city_name)

    def get_weather(self, city_name):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}"
            response = requests.get(url)
            x = response.json()
            print(x)
            if x["cod"] != "404":
                temperature = round(x["main"]["temp"] - 273.15)
                humidity = x["main"]["humidity"]
                weather = x["weather"][0]["main"]
                id = str(x["weather"][0]["id"])
                wind_speed = round(x["wind"]["speed"] * 18 / 5)
                location = x["name"] + ", " + x["sys"]["country"]

                # Access widgets within the "login" screen
                login_screen = self.root.get_screen("login")
                login_screen.ids.temperature.text = f"[b]{temperature}[/b]°"
                login_screen.ids.weather.text = str(weather)
                login_screen.ids.humidity.text = f"{humidity}%"
                login_screen.ids.wind_speed.text = f"{wind_speed} km/h"
                login_screen.ids.location.text = location

                if id == "800":
                    login_screen.ids.weather_image.source = "bigsun.png"  #
                elif "200" <= id <= "232":
                    login_screen.ids.weather_image.source = "storm.png"  #
                elif "300" <= id <= "321" and "500" <= id <= "531":
                    login_screen.ids.weather_image.source = "rain.png"  #
                elif "600" <= id <= "622":
                    login_screen.ids.weather_image.source = "snow.png"   #
                elif "701" <= id <= "781":
                    login_screen.ids.weather_image.source = "haze.png"  #
                elif "801" <= id <= "804":
                    login_screen.ids.weather_image.source = "clouds.png"  #
            else:
                print("City Not found")
        except requests.ConnectionError:
            print("No Internet Connection!")

if __name__=="__main__":
    Weather_WonderApp().run()
