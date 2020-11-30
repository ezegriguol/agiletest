import json
import requests
import logging

from google.cloud import firestore

def search(request):
    try:
        result = ""
        request_json = request.get_json()
        rows = []

        db = firestore.Client()
        photos = db.collection(u'Photos')

        if request.args and 'author' in request.args:
            photos = photos.where(u'author', u'==', request.args.get('author'))

        if request.args and 'camera' in request.args:
            photos = photos.where(u'camera', u'==', request.args.get('camera'))

        if request.args and 'tags' in request.args:
            photos = photos.where(u'tags', u'array_contains', request.args.get('tags'))

        if request.args and 'id' in request.args:
            photos = photos.where(u'id', u'==', request.args.get('id'))

        for image in photos.get():
            url = image._data["full_picture"]
            rows.append(url)

        return json.dumps(rows)

    except Exception as e:
        logging.error(str(e))
        return str(e)
