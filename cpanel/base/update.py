import json
import pandas
import time
import pyrebase

config = {
  'apiKey': "AIzaSyBXgvtowzljY_2UjRnO4BeRY1CXP55jrXk",
  'authDomain': "pybase-1b3fc.firebaseapp.com",
  'databaseURL': "https://pybase-1b3fc.firebaseio.com",
  'projectId': "pybase-1b3fc",
  'storageBucket': "pybase-1b3fc.appspot.com",
  'messagingSenderId': "861383523187",
  'appId': "1:861383523187:web:d5522045e7a07840e36306",
  'measurementId': "G-LB3XQ55WF4"
}

firebase = pyrebase.initialize_app(config)
database=firebase.database()

def update(df):
    json_str = df.to_json()
    json = json.dumps(json_str).decode('utf8')


data = "{'Unnamed: 0': {'0': 'desc', '1': 'name', '2': 'price', '3': 'url'}, '1586011149000': {'0': 'asdasda', '1': 'aaaa', '2': '125', '3': None}, '1586015858000': {'0': 'desc', '1': 'BBB', '2': '123', '3': None}, '1589800451000': {'0': 'фывф', '1': 'Говна поешь', '2': '200', '3': None}, '1591016808000': {'0': 'СОЛО 322', '1': 'Новая услуга', '2': '322', '3': None}}"
js = json.loads(data).encode('utf8')
print((type(js)))