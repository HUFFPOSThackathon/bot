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
# from bot.models import  restraunts,person,feedback
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
                            "text":"OK great. What time would you like to book a table for? Select an option below, or alternatively just type your preferred time and if in advance enter the date as well ",
                            "quick_replies":[
                              {
                                "content_type":"text",
                                "title":'Manifestos',
                                "payload":"TIME"
                              },
                              {
                                "content_type":"text",
                                "title":'Issue',
                                "payload":"TIME"
                              },
                              {
                                "content_type":"text",
                                "title":'Contact details',
                                "payload":"TIME"
                              },
                              {
                                "content_type":"text",
                                "title":'Election Summary',
                                "payload":"TIME"
                              },
                              {
                                "content_type":"text",
                                "title":'Start Over',
                                "payload":"TIME"
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
                    w = feedback.objects.get_or_create(fbid = sender_id)[0]
                    r = restraunts.objects.get_or_create(payload = 'vishrut')[0]

                    name = '%s %s'%(a['first_name'],a['last_name'])  
                    if message_text.lower() in "hey,hi,supp,hello".split(','):
                    	post_facebook_message(sender_id,'Hey! whatsup Im constiuencyNow and im your new News partner So lets get started by telling us what you want to do today ')
                    	post_facebook_message(sender_id,'quickreply_first')


                except Exception as e:
                    print e
                    pass      

            return HttpResponse()  