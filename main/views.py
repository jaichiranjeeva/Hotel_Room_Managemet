from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from bson.objectid import ObjectId
from datetime import timedelta,date
from datetime import datetime
from django.utils import timezone

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from django.shortcuts import get_object_or_404
import pymongo
#connect_string = 'mongodb+srv://<username>:<password>@<atlas cluster>/<myFirstDatabase>?retryWrites=true&w=majority' 

from django.conf import settings
# my_client = pymongo.MongoClient("mongodb://localhost:27017")

# First define the database name
uri = "mongodb+srv://jaichiranjeeva:lmYlT6potgi5KvW9@hotelroommanagement.vtffr85.mongodb.net/?retryWrites=true&w=majority&appName=HotelRoomManagement"
# Create a new client and connect to the server
my_client = MongoClient(uri, server_api=ServerApi('1'))

# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection


# Create your views here.
def index(request):
    return render(request, "index.html")

def hotel(request):
    try:
        my_client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return render(request, "welcome.html",{})

def booking(request):
    # form = Check_Booking(request.POST) 
    # context = {'form':form}
    return render(request, "booking.html",{})
old={}
def saveEdits(request):
    if request.method == 'POST':
        RoomN = request.POST.get('RoomN')
        phone = request.POST.get('phone')
        date = request.POST.get('Check-In Date')
        time = request.POST.get('Check-In Time')

        dbname = my_client['Hotel_Room_Management']
        collection_name = dbname["currentBookings"]
        myquery = { "Room_No": old["RoomN"]  }
        newvalues = { "$set": { "Room_No": RoomN } }

        x = collection_name.update_one(myquery, newvalues)
        return render(request,"manageBooking.html",{})
def editBooking(request):
    if request.method == 'POST':
        RoomN = request.POST.get('RoomN')
        phone = request.POST.get('phone')
        date = request.POST.get('Check-In Date')
        time = request.POST.get('Check-In Time')

        dbname = my_client['Hotel_Room_Management']
        collection_name = dbname["currentBookings"]
        if(datetime.strptime(date+'-'+time, '%Y-%m-%d-%H:%M')<datetime.now()):
            return HttpResponse("Old Records Cant be Modified")
        x=collection_name.find_one({"Room_No":RoomN,"Phone":phone,"From_Date":date,"From_Time":time})
        
        
        if(x==type({})):
            context={"RoomN":x["Room_No"],"Name":x["Name"], 
                 "Email": x["Email"], "fd": x["From_Date"],
                 'td':x["To_Date"],"ft":x["From_Time"],
                 'tt':x["To_Time"],"ph":x["Phone"]}
            old=context
            return render(request,"updateBooking.html",context)
        else:
             HttpResponse("Record not found")
             return render(request,"manageBooking.html",{})
    
    else:
        # Render the form template
        return HttpResponse("Waiting for form response!")
def manageBooking(request):
    return  render(request,"manageBooking.html",{})
def allBookings(request):
    dbname = my_client['Hotel_Room_Management']
    collection_name = dbname["currentBookings"]
    l=[]
    for doc in collection_name.find():
        y=list(doc.values())
        l.append(y)
    context={'list':l}
    return render(request,"allBookings.html",context)

def cancellation(request):
    dbname = my_client['Hotel_Room_Management']
    collection_name = dbname["currentBookings"]
    l=[]
    for doc in collection_name.find():
        y=list(doc.values())
        l.append(y)
    dn=datetime.now()
    rp=[]
    for i in range(0,len(l)):
        if(datetime.strptime(l[i][2]+'-'+l[i][3], '%Y-%m-%d-%H:%M')>dn):
                rp.append(l[i])

    context={'list':rp}
    return render(request,'cancellation.html',context)

def deleteReservation(request,id):
    dbname = my_client['Hotel_Room_Management']
    collection_name = dbname["currentBookings"]
    collection_name.delete_one({"_id":ObjectId(id)})
    return cancellation(request)


def send(request):
    subject = request.POST['sub']
    message = request.POST['msg']
    settings.EMAIL_HOST_USER = request.POST['frm']
    settings.EMAIL_HOST_PASSWORD = request.POST['pswd']
    tom=request.POST['too'].split(';')
    if subject and message and settings.EMAIL_HOST_USER:
        send_mail(subject, message, settings.EMAIL_HOST_USER, tom, fail_silently=False)
        return HttpResponse('Mails Sent Succesfully!!!')
    else:
        return HttpResponse('Make sure all fields are entered and valid.')