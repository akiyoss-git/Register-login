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

while(True):
    data = json.dumps(database.child('reports').get().val(), ensure_ascii=False).encode('utf8')
    df = pandas.read_json(data)
    df.to_excel('../media/pricelist.xlsx')
    print('data updated')
    time.sleep(1800)