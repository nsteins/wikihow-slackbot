from flask import Flask, request, jsonify
from whapi import search
from whapi import get_images
from whapi import random_article
from whapi import return_details
from whapi.exceptions import ParseError

import random
from threading import Thread
import requests
import json
  
app = Flask(__name__)
app.debug = True 

@app.route("/")
def index():
    return "<h1>test</h1>"

@app.route("/search", methods=['GET','POST']) 
def search_images():
    print(request.form)
    query = request.form.get('text')
    response_url = request.form.get('response_url')
    if query:
        thr = Thread(target=search_response, args=[query, response_url])
    else:
        thr = Thread(target=random_image, args=[response_url])
    thr.start()
    return jsonify({"response_type": "in_channel"}), 200, {'ContentType':'application/json'}

@app.route("/random", methods=['GET','POST'])


def search_response(query, response_url):
    search_results = search(query, 1)
    article_id = search_results[0]['article_id']
    create_response(article_id, response_url)

def create_response(article_id, response_url):
    title = return_details(article_id)['title']
    try:
        image_list = get_images(article_id)
    except ParseError:
        random_image(response_url)
        return
    image = random.choice(image_list) 
    response = {
            "response_type": "in_channel",
            "text": {
                "type": "markdown",
                "text": f'How to {title}'
            },
            "blocks": [
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": title,
                        "emoji": True
                    },
                    "image_url": image,
                    "alt_text": title
                }
            ]
        }
    requests.post(response_url, json.dumps(response))

def random_image(response_url):
    article_id = random_article()
    print(article_id)
    create_response(article_id, response_url)

 
