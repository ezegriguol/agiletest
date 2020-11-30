from google.cloud import pubsub_v1
from datetime import datetime
from google.cloud import firestore

import json
import logging
import requests
import os

def master(request):
    try:
        lastupdate = datetime.strptime('19900101',"%Y%m%d")
        db = firestore.Client()        
        ups = db.collection(u'CacheRefresh').order_by("updated").limit(1).get()
        if (len(ups) > 0):
            lastupdate = datetime.strptime(str(ups[0]._data["updated"]), '%Y%m%d')        
        days = (datetime.today() - lastupdate).days
        
        if days >= int(os.environ.get('CACHE_TIME')):
            publisher = pubsub_v1.PublisherClient()        
            
            #Get Token from API
            response = requests.post("http://interview.agileengine.com/auth",headers={'Content-Type': 'application/json'}, data='{"apiKey":"' + os.environ.get('API_KEY') + '"}')
            token = json.loads(response.text)        
            if (token["auth"] == True):            
                hasMore = True
                page = 1            
                while hasMore:
                    logging.info("Fetch page " + str(page))

                    response = requests.get("http://interview.agileengine.com/images?page=" + str(page),headers={'Authorization': 'Bearer ' + token["token"]})
                    pictures = json.loads(response.text)
                    for picture in pictures["pictures"]:
                        row = {
                                'id': picture["id"],
                                'token': token["token"],
                                'action': 'INSERT'
                                }
                        
                        #Send a message for each photo to trigger the function download_detail.
                        publisher.publish("projects/agileenginetest/topics/photos", data=json.dumps(row).encode("utf-8"))

                    hasMore = pictures["hasMore"]
                    page += 1
                
                #Update last update into DB
                db.collection(u'CacheRefresh').document().set( { u'updated': datetime.today().strftime('%Y%m%d') } )
            else:
                logging.error("Invalid API Key")
        else:
            logging.info("No cache update")

    except Exception as e:
        logging.error("master - " + str(e))



