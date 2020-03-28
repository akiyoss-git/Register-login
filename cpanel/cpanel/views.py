import pyrebase 
from django.shortcuts import render 
from django.contrib import auth

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

authe = firebase.auth()
database=firebase.database()

def signIn(request):

    return render(request, "signIn.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message="invalid credentials"
        return render(request,"signIn.html",{"messg":message})
    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request, "welcome.html",{"e":email})
def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')


def signUp(request):

    return render(request,"signup.html")
def postsignup(request):

    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=authe.create_user_with_email_and_password(email,passw)
        uid = user['localId']
        data={"name":name,"status":"1"}
        database.child("users").child(uid).child("details").set(data)
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"messg":message})
        

    
    return render(request,"signIn.html")
