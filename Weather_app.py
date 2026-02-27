import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton,QLabel,QLineEdit,QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()  #super is helping initializing parent class(required for inheritance)
        self.city_label= QLabel("Enter city name: ",self)
        self.city_input =QLineEdit(self)
        self.get_weather_button=QPushButton("Get Weather",self)
        self.unit_button = QPushButton("Switch to °F", self)
        self.unit = "C"
        self.last_data = None
        self.temp_label=QLabel("30°C",self)
        self.em_label=QLabel("☀️",self)
        self.description_label=QLabel("Sunny",self)
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("Weather App")
        vbox=QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.unit_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.em_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.em_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.unit_button.setObjectName("unit_button")
        self.temp_label.setObjectName("temp_label")
        self.em_label.setObjectName("em_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel,QPushButton{
                 font-family:calibri;}
            QLabel#city_label{
                 font-size:40px;
                 font-style: italic;}
            QLineEdit#city_input{
                 font-size: 40px;}
            QPushButton#get_weather_button{
                 font-size:30px;
                 font-weight:bold;}
            QPushButton#unit_button{
                 font-size:30px;
                 font-weight:bold;
                 font-style:italic;}
            QLabel#temp_label{
                 font-size:70px;}
            QLabel#em_label{
                 font-size:100px;
                 font-family:Segoe UI Emoji;}
            QLabel#description_label{
                 font-size:50px;}          
         """)
        self.get_weather_button.clicked.connect(self.get_weather) #we can search using pushbutton
        self.city_input.returnPressed.connect(self.get_weather)  #we can search using enter
        self.unit_button.clicked.connect(self.toggle_unit)
    
    def get_weather(self):
        api_key="YOUR_API_KEY"
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
               response=requests.get(url)
               response.raise_for_status()
               data=response.json()

               if data["cod"]==200:
                    self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\n Please check your input")
                case 401:
                    self.display_error("Unauthorized\n Please check your input")
                case 403:
                    self.display_error("Forbidden\n Access is denied")
                case 404:
                    self.display_error("Not found\n City not found")
                case 500:
                    self.display_errort("Internal Server Error\n Please try again later")
                case 502:
                    self.display_error("Bad gateway\n Invalid response from the server")
                case 503:
                    self.display_error("Service Unavailable\n Server is down")
                case 504:
                    self.display_error("Gateway Timeout\n No response from server")
                case _:
                    self.display_error(f"HTTP Error occured\n{http_error}")
              
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\n Check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\n The request is timeout")
        except requests.exceptions.TooManyRedirects:
            self.display_error("To Many Redirects:\n Check the URL")  
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n {req_error}")


    def toggle_unit(self):
        if self.unit == "C":
            self.unit = "F"
            self.unit_button.setText("Switch to °C")
        else:
            self.unit = "C"
            self.unit_button.setText("Switch to °F")

        if self.last_data:
            self.display_weather(self.last_data)

    def display_error(self,message):
        self.temp_label.setStyleSheet("font-size: 40px;")
        self.temp_label.setText(message)
        self.description_label.clear()
        self.em_label.clear()

    def display_weather(self,data):
        self.last_data = data
        temp_k=data["main"]["temp"]
        temp_fl=data["main"]["feels_like"]
        temp_c=temp_k-273.15
        feels_c=temp_fl-273.15
        #print(data) to find which data are present at what name in the .json format
        if self.unit == "C":
         temp = temp_c
         feels = feels_c
         symbol = "°C"
        else:
         temp = (temp_c * 9/5) + 32
         feels = (feels_c * 9/5) + 32
         symbol = "°F"
        weather_des=data["weather"][0]["description"]
        weather_id=data["weather"][0]["id"] #since the list had only 1 item so 0 
        self.temp_label.setStyleSheet("font-size: 40px;")
        self.temp_label.setText(f"Temp: {temp:.2f}{symbol}\nFeels Like: {feels:.2f}{symbol}")
        self.description_label.setText(weather_des)
        self.em_label.setText(self.get_weather_em(weather_id))
        
     
    def get_weather_em(self,weather_id):

          if 200 <= weather_id <= 232:
               return "⛈️"      # Thunderstorm

          elif 300 <= weather_id <= 321:
               return "🌦️"      # Drizzle

          elif 500 <= weather_id <= 531:
               return "🌧️"      # Rain

          elif 600 <= weather_id <= 622:
               return "❄️"      # Snow

          elif 701 <= weather_id <= 741:
               return "🌫️"      # Atmosphere (fog, mist, etc.)

          elif weather_id == 762:
               return "🌋"      # Volcanic ash

          elif weather_id == 771:
               return "💨"      # Squalls violent wind ghust

          elif weather_id == 781:
               return "🌪️"      # Tornado

          elif weather_id == 800:
               return "☀️"      # Clear sky

          elif 801 <= weather_id <= 804:
               return "⛅"      # Clouds

          else:
               return "❓"

if __name__=="__main__":
    app=QApplication(sys.argv)
    weather_app=WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())