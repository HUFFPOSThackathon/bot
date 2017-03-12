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
                # try:
                    
                #     sender_id = message['sender']['id']
                #     message_text = message['message']['text']
                #     a = userdeatils(sender_id)
                #     p = person.objects.get_or_create(fbid = sender_id)[0]
                #     w = feedback.objects.get_or_create(fbid = sender_id)[0]
                #     r = restraunts.objects.get_or_create(payload = 'vishrut')[0]

                #     name = '%s %s'%(a['first_name'],a['last_name'])  
