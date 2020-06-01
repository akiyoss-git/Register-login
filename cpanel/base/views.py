from django.shortcuts import render
import json
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas
from base.models import Document
from base.forms import DocumentForm
import pyrebase
from django.contrib import auth
import time
from datetime import datetime, timezone
import pytz

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

def start(request):
    return render(request, "welcome.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message="invalid credentials"
        print(message)
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
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"messg":message})
    uid = user['localId']

    data={"name":name,"status":"1"}

    database.child("users").child("details").set(data)
    return render(request,"signIn.html")

def create(request):
    return render(request,'create.html',{'state':0})

def check(request):
    if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
        search = request.GET.get('search')
        search = search.lower()
        uid = request.GET.get('uid')
        timestamps = database.child('reports').shallow().get().val()
        price_id=[]
        for i in timestamps:

            wor = database.child('reports').child(i).child('name').get().val()
            wor = str(wor)+"$"+str(i)
            price_id.append(wor)

        matching = [str(string) for string in price_id if search in string.lower()]

        wnames=[]
        s_id=[]
        for i in matching:

            wname,ids=i.split('$')
            wnames.append(wname)
            s_id.append(ids)
        prices = []
        import datetime
        for i in s_id:
            price = database.child('reports').child(i).child('price').get().val()
            prices.append(price)
        comb_lis = QuerySet(s_id, wnames, prices)
        name = database.child('users').child('details').child('name').get().val()
        form = DocumentForm() # A empty, unbound form
        return render(request, 'check.html', {'comb_lis': comb_lis, 'e': name, 'uid': uid, 'form': form})

    else:
        import datetime
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']

        timestamps = database.child('reports').shallow().get().val()
        lis_time=[]
        if timestamps is not None:
            for i in timestamps:

                lis_time.append(i)

            lis_time.sort(reverse=True)

            print("lt= "+ str(lis_time))
            price = []
            name = []
            for i in lis_time:

                wor=database.child('reports').child(i).child('price').get().val()
                nam = database.child('reports').child(i).child('name').get().val()
                name.append(nam)
                price.append(wor)
            print("price= "+str(price))

            comb_lis = zip(lis_time,name,price)
        else:
            comb_lis = None
        username = database.child('users').child('details').child('name').get().val()
        form = DocumentForm() # A empty, unbound form
        return render(request,'check.html',{'comb_lis':comb_lis,'e':username,'uid':a, 'form':form})

def post_create(request):
    tz= pytz.timezone('Europe/Moscow')
    time_now= datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    price = request.POST.get('price')
    desc =request.POST.get('desc')
    url = request.POST.get('url')
    name = request.POST.get('name')
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    data = {
        "name": name,
        "price":price,
        'desc':desc,
    }
    database.child('reports').child(millis).set(data)
    name = database.child('users').child('details').child('name').get().val()
    return check(request)

def post_check(request):
    import datetime

    time = request.GET.get('z')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    wname =database.child('reports').child(time).child('name').get().val()
    price =database.child('reports').child(time).child('price').get().val()
    desc =database.child('reports').child(time).child('desc').get().val()
    name = database.child('users').child('details').child('name').get().val()
    return render(request,'post_check.html',{'price':price,'desc':desc,'name':wname,'e':name, 't':time})

def delete(request):
    time = request.POST.get('time')
    database.child('reports').child(time).remove()
    return check(request)

def change(request):
    time = request.POST.get('time')
    name = request.POST.get('name')
    desc = request.POST.get('desc')
    price = request.POST.get('price')
    print(time)
    print(price)
    print(desc)
    print(name)
    return render(request,'create.html', {
        'name':name,
        'price':price,
        'desc':desc,
        't':time,
        'state':1
    })

def post_change(request):
    time = request.POST.get('time')
    name = request.POST.get('name')
    desc = request.POST.get('desc')
    price = request.POST.get('price')
    data = {
        'name':name,
        'desc':desc,
        'price':price
    }
    database.child('reports').child(time).set(data)
    return check(request)

def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            print(newdoc)
            filename =  str(request.FILES['docfile'])
            if str(request.FILES['docfile'])[-3:] == 'xls' or str(request.FILES['docfile'])[-4:] == 'xlsx':
                newdoc.save()
                df = pandas.read_excel("media/"+filename.replace('(', '').replace(')', ''))
                json_str = df.to_json()
                tz= pytz.timezone('Europe/Moscow')
                time_now= datetime.now(timezone.utc).astimezone(tz)
                millis = int(time.mktime(time_now.timetuple()))
                js = json.loads(json_str)
                i = 0
                for stamp in js:
                    if stamp != 'Unnamed: 0':
                        price = js[stamp]['2']
                        desc = js[stamp]['0']
                        name = js[stamp]['1']
                        data = {
                            "name": name,
                            "price":price,
                            'desc':desc,
                        }
                        database.child('reports').child(millis+i).set(data)
                        i = i + 1
                        print(stamp)
                        print(data)
                        data = json.dumps(database.child('reports').get().val(), ensure_ascii=False).encode('utf8')
                        df = pandas.read_json(data)
                        df.to_excel('media/pricelist.xlsx')
                    
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('check'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    # Render list page with the documents and the form
    return render(request, 'check.html', {'form':form})
