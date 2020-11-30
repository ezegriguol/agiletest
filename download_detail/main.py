import base64
import json
import requests
import logging

from datetime import datetime
from google.cloud import storage
from google.cloud.storage import Blob
from google.oauth2 import service_account
from google.cloud import firestore

def master(event, context):
    try:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')           
        msg = json.loads(pubsub_message)

        logging.debug("Image: " + msg['id'])
        
        ##1. Get image details
        response = requests.get("http://interview.agileengine.com/images/" + msg['id'],headers={'Authorization': 'Bearer ' + msg['token']})
        image_detail = json.loads(response.text)

        ##2. Save metadata into Firestore 
        db = firestore.Client()
        
        data_tag = []
        tag_values = image_detail['tags'].strip().split(" ")
        for tag in tag_values:
            data_tag.append({ u'tag': tag })

        data = {
                u'id': msg['id'],
                u'author': image_detail['author'],
                u'camera': image_detail['camera'],
                u'tags': data_tag,
                u'full_picture': image_detail['full_picture'],
                u'cropped_picture': image_detail['cropped_picture'],
                u'updated': datetime.today()
            }
            
        db.collection(u'Photos').document(msg['id']).set(data)
        
        ##3. Download image from URL
        datatoupload = requests.get(image_detail['full_picture'], stream = True)
        datatoupload.raw.decode_content = True

        ##4. Save image into Google Bucket
        file_name = msg['id'] + ".jpg"
        _google_client = storage.Client()
        bucket = _google_client.get_bucket('photos_cache')
        blob = Blob(file_name, bucket)
        blob.upload_from_string(datatoupload.raw.data)

    except Exception as e:
        logging.error(str(e))


