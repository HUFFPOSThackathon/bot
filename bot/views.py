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

    if message_text == 'location_quickreply':
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
                    	post_facebook_message(sender_id,'location_quickreply')
                    	p.name = name
                    	# p.state = '1'
                    	p.save()

                    # elif p.state == '1':
                    # 	p.location = message_text
                    # 	post_facebook_message(sender_id , 'thanks , for providing location ')
                    # 	post_facebook_message(sender_id,'quickreply_first') 
                    # 	p.state = '0'
                    # 	p.save() 

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
                        handle_postback(message['sender']['id'],message['postback']['payload'])
                        return HttpResponse()
                    else:
                        pass

                except Exception as e:
                    print e
                    pass 
                    
                try:
                	if 'coordinates' in message['message']['attachments']['payload']:

                		p.location_lat =   message['message']['attachments']['payload']['coordinates']['lat']
                		p.location_long =   message['message']['attachments']['payload']['coordinates']['long']  
                		p.save()
                		post_facebook_message(sender_id , 'thanks , for providing location ')
                    	post_facebook_message(sender_id,'quickreply_first')         

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
        

        post_facebook_message(fbid,'This is the contact number of your MLA if you want to reguster an issue you can click the button below ') 
        return post_facebook_message(sender_id,'quickreply_first')   


    
    elif payload1 == "STARTOVER":
        # person.objects.filter(fbid=fbid).delete()
        
        # post_facebook_message(fbid,'No problem, please feel free to make a booking by saying hi again.')

        return  post_facebook_message(fbid,'quickreply_first')       

        
     


    elif payload1 == 'MANIFESTOS':
        # p = person.objects.get_or_create(fbid =fbid)[0]
        # p.state = '5'
        # p.save()
        # post_facebook_message(fbid,'Say hi to start talking')

        post_facebook_message(fbid,'These are the manifestos of your leader')
        return  post_facebook_message(fbid,'quickreply_first')  


    elif payload1 == 'SUMMARY':
        # p = person.objects.get_or_create(fbid =fbid)[0]
        # p.state = '5'
        # p.save()
        # post_facebook_message(fbid,'Say hi to start talking')
        post_facebook_message(fbid , 'This is the summary ')
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


