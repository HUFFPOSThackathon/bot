from django.shortcuts import render
from django.http import HttpResponse
import urllib2
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests
from django.http import HttpResponse
import urllib2
from django.utils.decorators import method_decorator
from bot.models import  person
import datetime
from datetime import timedelta
import re

def userdeatils(fbid):
    url = 'https://graph.facebook.com/v2.6/' + fbid + '?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=' + PAGE_ACCESS_TOKEN
    resp = requests.get(url=url)
    data =json.loads(resp.text)
    # print "ghus gaye bhaiya"
    # print data 
    return data

VERIFY_TOKEN = 'huffpost' 
PAGE_ACCESS_TOKEN ='EAAEGzsQBZBt4BAHWYKTh3Cg5PERypIJSE08eGiydZASXVPylod3ZAZBbqfTtfqPv46XYc6zjy95ARR5Rd5rabn2kn6Up7MPPIYWZB6q5sDTiuzUhVoYQCii56mPvcbQKe9cmAvgLocVO7cTE22Hb5inVRSHlMyJ9pmn2TNB5MmQZDZD'


def post_facebook_message(fbid,message_text):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    
    if message_text == 'quickreply_first':
        response_msg = quickreply_first(fbid)

    elif message_text == 'location_quickreply':
        response_msg = location_quickreply(fbid)    
               



 



    else:
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message_text}})

    requests.post(post_message_url, 
                    headers={"Content-Type": "application/json"},
                    data=response_msg)  



def quickreply_first(fbid):

  
    response_object =   {
                          "recipient":{
                            "id":fbid
                          },
                          "message":{
                            "text":"Please select one of the little buttons below ",
                            "quick_replies":[
                              {
                                "content_type":"text",
                                "title":'Manifestos',
                                "payload":"MANIFESTOS"
                              },
                              {
                                "content_type":"text",
                                "title":'Issue',
                                "payload":"ISSUE"
                              },
                              {
                                "content_type":"text",
                                "title":'Contact details',
                                "payload":"CONTACT"
                              },
                              {
                                "content_type":"text",
                                "title":'Election Summary',
                                "payload":"SUMMARY"
                              },
                              {
                                "content_type":"text",
                                "title":'Start Over',
                                "payload":"STARTOVER"
                              },
                              
                              
                            ]
                          }
                        }
    return json.dumps(response_object)                     

class MyChatBotView(generic.View):
    def get (self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Oops invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message= json.loads(self.request.body.decode('utf-8'))
        print  incoming_message 
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                print message
                try:
                    
                    sender_id = message['sender']['id']
                    message_text = message['message']['text']
                    a = userdeatils(sender_id)
                    p = person.objects.get_or_create(fbid = sender_id)[0]
                    # w = feedback.objects.get_or_create(fbid = sender_id)[0]
                    # r = restraunts.objects.get_or_create(payload = 'vishrut')[0]

                    name = '%s %s'%(a['first_name'],a['last_name'])  
                    if message_text.lower() in "hey,hi,supp,hello".split(','):
                    	post_facebook_message(sender_id,'Hey! '+name + ' whatsup Im constiuencyNow and im your new News partner So lets get started by telling us what you want to do today ')
                    	post_facebook_message(sender_id , 'you send your location by clicking the button below or typing ')
                    	post_facebook_message(sender_id,'location_quickreply')
                    	p.name = name
                    	# p.state = '1'
                    	p.save()


                    elif message_text.lower() == 'karhal':
                    	p.location = 'karhal'
                    	p.save()
                    	post_facebook_message(sender_id , 'thanks , for providing location ')
                    	x = constituencyInfo(sender_id)
                    	mlaname = x['Mla Name']
                    	post_facebook_message(sender_id,'your mla is ' + mlaname ) 
                    	post_facebook_message(sender_id,'quickreply_first') 	

               

                	# elif message_text.lower() == 'mainpuri':
                 #    	p.location = 'mainpuri'

                 #    	p.save()
                 #    	post_facebook_message(sender_id , 'thanks , for providing location ')
                 #    	post_facebook_message(sender_id,'quickreply_first') 	

                    elif p.state == '2':
                    	p.issue = message_text
                    	post_facebook_message(sender_id , 'We will forward your issue to the news channel ')
                    	post_facebook_message(sender_id,'quickreply_first') 
                    	p.state = '0'
                    	p.save() 	
                    		


                except Exception as e:
                    print e
                    pass 

                try:
                    if 'postback' in message:
                        # handle_postback(message['sender']['id'],message['postback']['payload'])
                        return HttpResponse()
                    else:
                        pass

                except Exception as e:
                    print e
                    pass 
                    
                try:
                    if 'quick_reply' in message['message']:
                        handle_postback(message['sender']['id'],
                        message['message']['quick_reply']['payload'])
                        return HttpResponse()
                    else:
                        pass
                except Exception as e:
                    print e
                    pass     

                try:
                	p = person.objects.get_or_create(fbid = sender_id)[0]
                	if 'coordinates' in message['message']['attachments'][0]['payload']:

                		p.location_lat =   message['message']['attachments'][0]['payload']['coordinates']['lat']
                		p.location_long =   message['message']['attachments'][0]['payload']['coordinates']['long']
                		p.location = 'noida'  
                		p.save()
                		# post_facebook_message(sender_id , 'thanks , for providing location ')
                		post_facebook_message(sender_id , 'thanks , for providing location ')
                    	x = constituencyInfo(sender_id)
                    	mlaname = x['Mla Name']
                    	post_facebook_message(sender_id,'your mla is ' + mlaname ) 
                    	post_facebook_message(sender_id,'quickreply_first')

                    	# post_facebook_message(sender_id,'quickreply_first')   

                except Exception as e:
                    print e
                    pass    	      

            return HttpResponse()  


def handle_postback(fbid,payload1):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    output_text = 'Payload Recieved: ' + payload1
    # q = restraunts.objects.all()
    # a =[]
    # for i in q:
    #     a.append(i.payload)

    # print payload1
    p = person.objects.get_or_create(fbid =fbid)[0]
    # r = restraunts.objects.get_or_create(payload = 'vishrut')[0]
    if payload1 == 'ISSUE':
        print "entered"
        # w = restraunts.objects.get(payload = payload1)[0]

        
        # p.state = '1'
        # print w.name
        # p.restraunt_name = w.name

        # p.save()
        p.state ='2'
        p.save()
        return post_facebook_message(fbid,'Go ahead and type what issue you are facing ')
        # post_facebook_message(sender_id,'quickreply_first')


    elif payload1 == "CONTACT":
        # p.state='6'
        # p.save()

        # post_facebook_message(r.owner , 'SPECIAL REQUESTS:' + p.requests)
        # post_facebook_message(r.owner , 'You have a new booking from this customer') # restraunts owner id 
        # post_facebook_message2(fbid , 'booking_cards')

        # post_facebook_message('1645722955444541' , 'SPECIAL REQUESTS:' + p.requests)
        x = getMLADetails(fbid)
        

        post_facebook_message(fbid,'This is the contact number of your MLA if you want to reguster an issue you can click the button below ' + x) 

        return post_facebook_message(fbid,'quickreply_first')   


    
    elif payload1 == "STARTOVER":
        # person.objects.filter(fbid=fbid).delete()
        
        # post_facebook_message(fbid,'No problem, please feel free to make a booking by saying hi again.')

        return  post_facebook_message(fbid,'quickreply_first')       

        
     


    elif payload1 == 'MANIFESTOS':
        # p = person.objects.get_or_create(fbid =fbid)[0]
        # p.state = '5'
        # p.save()
        # post_facebook_message(fbid,'Say hi to start talking')
        x = constituencyInfo(fbid)
        menifestos = x['Manifesto link']

        post_facebook_message(fbid,'These are the manifestos of your leader' +  menifestos)
        return  post_facebook_message(fbid,'quickreply_first')  


    elif payload1 == 'SUMMARY':
        # p = person.objects.get_or_create(fbid =fbid)[0]
        # p.state = '5'
        # p.save()
        # post_facebook_message(fbid,'Say hi to start talking')
        summary = test(p.location)
        nsummary = test1()

        post_facebook_message(fbid , summary )
        post_facebook_message(fbid , nsummary )


        return post_facebook_message(fbid,'quickreply_first')    
      

           
                              
        response_msg = json.dumps(response_object)
        requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)          

           
                              
        response_msg = json.dumps(response_object)
        requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)             

def location_quickreply(fbid):
	response_object = {
						  "recipient":{
						    "id":fbid
						  },
						  "message":{
						    "text":"Please share your location:",
						    "quick_replies":[
						      {
						        "content_type":"location",
						      }
						    ]
						  }
						}


	return json.dumps(response_object) 



import csv
import random
import math
def loadcsv(filename):
	lines=csv.reader(open(filename,"rb"))
	dataset=list(lines)
	for i in range(len(dataset)):
			dataset[i]=[x for x in dataset[i]]
	return dataset
def seperateByClass(dataset):
	seperated={}
	vector=[]
	for i in range(len(dataset)):
		vector=dataset[i]
		vector[1]=vector[1].lower()
		if vector[1] not in seperated:
			seperated[vector[1]]=vector
	return seperated

def summarize(dataset):
	summaries=' '
	summaries=summaries+dataset[3]+" from "+dataset[2]+" won from constituency "+dataset[1]+" by "+dataset[-1]+" percentage of votes "
	return summaries
def summarizeByClass(dataset):
	seperated={}
	seperated=seperateByClass(dataset)
	summaries={}
	for classvalue,instances in seperated.iteritems():
		summaries[classvalue]=summarize(instances)
	return summaries

def summarizeByClass(dataset):
	seperated={}
	seperated=seperateByClass(dataset)
	summaries={}
	for classvalue,instances in seperated.iteritems():
		summaries[classvalue]=summarize(instances)
	return summaries



def test(test):
	filename="bot/static/up.csv"
	dataset=loadcsv(filename)
	summ=summarizeByClass(dataset)
	
	# print summ[test]
	return summ[test]
# main()



from bot.models import person
def mapLatitudeToPincode(lattitude,longitude):
	################# give constituency info based on latitude and longitude #######
	pass
def getConstituency(pincode=None,latitude=None,longitude=None):
	########## get constituency name from  pincode given it is not null else call constituency mapping function and save it in the current user's database ########
	pass

def registerUserLocation(fbid,pincode=None,latitude=None,longitude=None):
	########### register the user location by getConstituency #######
	pass

def constituencyInfo(fbid):
	################ Gives Manifesto link,MlA name according to location in Fbid############
	current_person=person.objects.filter(fbid=fbid)[0]
	if (current_person.location=="noida"):
		return {"Mla Name":"Pankaj Singh","Manifesto link":"http://timesofindia.indiatimes.com/elections/assembly-elections/uttar-pradesh/news/bjp-releases-poll-manifesto-for-uttar-pradesh-highlights/listshow/56831761.cms"}
	if (current_person.location=="mainpuri"):
		return {"Mla Name":"Raju Yadav","Manifesto link":"http://timesofindia.indiatimes.com/elections/assembly-elections/uttar-pradesh/interactives/samajwadi-partys-manifesto-for-up-polls-highlights/articleshow/56715454.cms"}
	if (current_person.location=="karhal"):
		return {"Mla Name":"Sobaran Singh","Manifesto link":"http://timesofindia.indiatimes.com/elections/assembly-elections/uttar-pradesh/interactives/samajwadi-partys-manifesto-for-up-polls-highlights/articleshow/56715454.cms"}
	
def registerIssue(fbid,Issue):
	######### Register Issue at your OWN location by getting name from calling getConstituency funtion to get  and Trigger on database to check whether the issue has been repoted many times#############
	pass
def getMLADetails(fbid):
	######## FROM  fbid queryuser location and give mla suitably ##########
	current_person=person.objects.filter(fbid=fbid)[0]
	if current_person.location=="noida":
		return "Name Of Mla:Pankaj Singh \n Contact Detail:9868074022"

	else:
		if current_person.location=="mainpuri":
			return "Name Of Mla:Raju Yadav \n Contact Detail:9560117494"

		else:
			return "Name of Mla:Sobaran Singh Yadav \n Contact Detail:8800125071"





def genElectionSummary(electionName):
	####################  get the election name at select the csv you want to query for ad return the tota #########
	pass



########################################
def loadcsv1(filename):
	lines=csv.reader(open(filename,"rb"))
	dataset=list(lines)
	for i in range(len(dataset)):
			dataset[i]=[x for x in dataset[i]]
	return dataset
def seperateByClass1(dataset):
	seperated={}
	for i in range(len(dataset)):
		vector=dataset[i]
		vector[2]=vector[2].lower()
		if vector[2] not in seperated:
			seperated[vector[2]]=0
	for i in range(len(dataset)):
		vector=dataset[i]
		seperated[vector[2]]=seperated[vector[2]]+1
	return seperated

def summarize1(dataset):
	summaries=''
	for value in dataset:
		summaries=summaries+value+" won "+str(dataset[value])+" seats , "
	summaries=summaries+"in Uttar pradesh"
	return summaries
def summarizeByClass1(dataset):
	seperated={}
	seperated=seperateByClass1(dataset)
	summaries={}
	for classvalue,instances in seperated.iteritems():
		summaries[classvalue]=summarize1(instances)
	return summaries

def summarizeByClass1(dataset):
	seperated={}
	seperated=seperateByClass1(dataset)
	summaries=summarize1(seperated)
	return summaries



def test1():
	filename="bot/static/up.csv"
	dataset=loadcsv1(filename)
	summ=summarizeByClass1(dataset)
	
	# print summ[test]
	return summ